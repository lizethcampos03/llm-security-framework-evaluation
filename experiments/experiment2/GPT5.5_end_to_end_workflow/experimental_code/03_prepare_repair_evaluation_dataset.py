"""
Prepare model-specific repaired SecurityEval samples for repair evaluation.

Run from the repository root:

    python experiments/experiment2/scripts/03_prepare_repair_evaluation_dataset.py

Options:
    --overwrite
    --cwe CWE-22
    --limit 5

Input and output directory names are read from config.py using
REPAIR_OUTPUT_NAME and REPAIR_EVALUATION_OUTPUT_NAME.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_VERSION = "1.1.0"
EXPERIMENT = Path("experiments/experiment2")
CONFIG_PATH = EXPERIMENT / "scripts/config.py"
MANIFEST_PATH = EXPERIMENT / "manifests/securityeval_manifest.json"


@dataclass(frozen=True)
class RuntimeConfig:
    configuration_name: str
    repair_output_name: str
    repair_evaluation_output_name: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise FileNotFoundError(f"Required JSON file not found: {path}")
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    temporary.replace(path)


def find_project_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / MANIFEST_PATH).is_file():
            return candidate
    raise FileNotFoundError(
        "Could not locate the repository root. Expected to find:\n"
        f"  {MANIFEST_PATH}"
    )


def validate_output_name(value: str, *, field_name: str) -> str:
    """Validate a safe, single directory name supplied by config.py."""
    name = value.strip()
    if not name:
        raise ValueError(f"config.py must define a non-empty {field_name}.")
    if name in {".", ".."}:
        raise ValueError(f"{field_name} cannot be {name!r}.")
    if Path(name).name != name:
        raise ValueError(
            f"{field_name} must be a single directory name, not a path: {name!r}"
        )
    if not re.fullmatch(r"[A-Za-z0-9._-]+", name):
        raise ValueError(
            f"{field_name} may contain only letters, numbers, '.', '_', and '-': "
            f"{name!r}"
        )
    return name


def load_config(path: Path) -> RuntimeConfig:
    if not path.is_file():
        raise FileNotFoundError(f"Required configuration file not found: {path}")

    spec = importlib.util.spec_from_file_location("experiment2_config", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load configuration file: {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    configuration_name = str(
        getattr(module, "CONFIGURATION_NAME", "secure_code_agent_baseline")
    ).strip()
    if not configuration_name:
        raise ValueError("CONFIGURATION_NAME cannot be empty.")

    repair_output_name = validate_output_name(
        str(getattr(module, "REPAIR_OUTPUT_NAME", "")).strip(),
        field_name="REPAIR_OUTPUT_NAME",
    )
    repair_evaluation_output_name = validate_output_name(
        str(getattr(module, "REPAIR_EVALUATION_OUTPUT_NAME", "")).strip(),
        field_name="REPAIR_EVALUATION_OUTPUT_NAME",
    )

    if repair_output_name == repair_evaluation_output_name:
        raise ValueError(
            "REPAIR_OUTPUT_NAME and REPAIR_EVALUATION_OUTPUT_NAME must be different."
        )

    return RuntimeConfig(
        configuration_name=configuration_name,
        repair_output_name=repair_output_name,
        repair_evaluation_output_name=repair_evaluation_output_name,
    )


def normalize_cwe_id(value: str) -> str:
    digits = "".join(character for character in value if character.isdigit())
    if not digits:
        raise ValueError(f"Invalid CWE identifier: {value!r}")
    return f"CWE-{int(digits)}"


def load_securityeval_manifest(path: Path) -> list[dict[str, Any]]:
    raw = load_json(path)
    if not isinstance(raw, list):
        raise TypeError("The SecurityEval manifest must contain a JSON list.")

    records: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise TypeError(f"Manifest record {index} is not an object.")
        required = {
            "sample_id", "cwe_id", "cwe_name", "cwe_definition",
            "sample_kind", "ground_truth_vulnerable", "source_code_path",
        }
        missing = sorted(required - item.keys())
        if missing:
            raise ValueError(
                f"Manifest record {index} is missing: {', '.join(missing)}"
            )
        sample_id = str(item["sample_id"])
        if sample_id in seen_ids:
            raise ValueError(f"Duplicate sample_id in manifest: {sample_id}")
        seen_ids.add(sample_id)
        records.append(item)
    return records


def validate_repair_artifacts(
    manifest_record: dict[str, Any],
    repair_record_file: Path,
    repaired_code_file: Path,
) -> dict[str, Any]:
    repair_record = load_json(repair_record_file)
    if not isinstance(repair_record, dict):
        raise ValueError("Repair record is not a JSON object.")
    if str(repair_record.get("status", "")).upper() != "SUCCESS":
        raise ValueError("Repair record status is not SUCCESS.")

    sample = repair_record.get("sample")
    model = repair_record.get("model")
    repair_output = repair_record.get("repair_output")
    if not isinstance(sample, dict):
        raise ValueError("Repair record has no valid sample block.")
    if not isinstance(model, dict):
        raise ValueError("Repair record has no valid model block.")
    if not isinstance(repair_output, dict):
        raise ValueError("Repair record has no valid repair_output block.")
    if sample.get("sample_id") != manifest_record["sample_id"]:
        raise ValueError("Repair sample_id does not match the manifest.")
    if sample.get("cwe_id") != manifest_record["cwe_id"]:
        raise ValueError("Repair CWE does not match the manifest.")
    if not repaired_code_file.is_file():
        raise FileNotFoundError(f"Repaired code file is missing: {repaired_code_file}")

    source_code = repaired_code_file.read_text(encoding="utf-8")
    if not source_code.strip():
        raise ValueError("Repaired code file is empty.")

    code_hash = sha256_file(repaired_code_file)
    recorded_hash = repair_output.get("repaired_code_sha256")
    if recorded_hash and recorded_hash != code_hash:
        raise ValueError("Repaired code SHA-256 does not match repair.json.")

    return {
        "repair_record": repair_record,
        "source_code": source_code,
        "source_code_sha256": code_hash,
        "repair_model": str(model.get("model_id", "")).strip(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare successful repaired samples for CodeQL and Bandit evaluation."
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--cwe")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be at least 1.")
    return args


def main() -> int:
    args = parse_args()
    try:
        project_root = find_project_root(Path(__file__).resolve().parent)
        config_file = project_root / CONFIG_PATH
        manifest_file = project_root / MANIFEST_PATH
        config = load_config(config_file)

        repair_root = (
            project_root / EXPERIMENT / "outputs" / config.repair_output_name
        )
        repair_code_root = repair_root / "code"
        repair_record_root = repair_root / "records"

        evaluation_root = (
            project_root
            / EXPERIMENT
            / "outputs"
            / config.repair_evaluation_output_name
        )
        prepared_source_root = evaluation_root / "prepared_source"
        prepared_manifest_path = evaluation_root / "manifest.json"
        preparation_summary_path = evaluation_root / "preparation_summary.json"

        if not repair_code_root.is_dir():
            raise FileNotFoundError(
                f"Configured repair code directory not found: {repair_code_root}"
            )
        if not repair_record_root.is_dir():
            raise FileNotFoundError(
                f"Configured repair records directory not found: {repair_record_root}"
            )

        manifest = load_securityeval_manifest(manifest_file)
        vulnerable_records = [
            record for record in manifest
            if record["sample_kind"] == "vulnerable"
            and record["ground_truth_vulnerable"] is True
        ]
        vulnerable_records.sort(key=lambda item: int(str(item["cwe_id"]).split("-")[1]))

        if args.cwe:
            cwe_filter = normalize_cwe_id(args.cwe)
            vulnerable_records = [r for r in vulnerable_records if r["cwe_id"] == cwe_filter]
        if args.limit is not None:
            vulnerable_records = vulnerable_records[:args.limit]
        if not vulnerable_records:
            raise ValueError("No vulnerable manifest records matched the filters.")

        if (
            prepared_source_root.exists()
            or prepared_manifest_path.exists()
            or preparation_summary_path.exists()
        ) and not args.overwrite:
            raise FileExistsError(
                "Prepared evaluation artifacts already exist. Use --overwrite to replace them."
            )

        if args.overwrite and evaluation_root.exists():
            if prepared_source_root.exists():
                shutil.rmtree(prepared_source_root)
            prepared_manifest_path.unlink(missing_ok=True)
            preparation_summary_path.unlink(missing_ok=True)

        prepared_source_root.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8]
    started_at = utc_now()
    prepared_cases: list[dict[str, Any]] = []
    skipped_not_repaired: list[dict[str, str]] = []
    invalid_artifacts: list[dict[str, str]] = []

    for record in vulnerable_records:
        cwe_id = str(record["cwe_id"])
        repair_json = repair_record_root / cwe_id / "repair.json"
        repaired_py = repair_code_root / cwe_id / "repaired.py"

        if not repair_json.is_file():
            skipped_not_repaired.append({
                "sample_id": record["sample_id"],
                "cwe_id": cwe_id,
                "reason": "No repair.json exists; sample did not reach repair.",
            })
            continue

        try:
            validated = validate_repair_artifacts(record, repair_json, repaired_py)
        except Exception as exc:
            invalid_artifacts.append({
                "sample_id": record["sample_id"],
                "cwe_id": cwe_id,
                "reason": str(exc),
            })
            continue

        destination = prepared_source_root / f"{cwe_id}_repaired.py"
        destination.write_text(validated["source_code"], encoding="utf-8", newline="\n")
        destination_hash = sha256_file(destination)
        if destination_hash != validated["source_code_sha256"]:
            invalid_artifacts.append({
                "sample_id": record["sample_id"],
                "cwe_id": cwe_id,
                "reason": "Copied file hash does not match source repair artifact.",
            })
            destination.unlink(missing_ok=True)
            continue

        repair_record = validated["repair_record"]
        prepared_cases.append({
            "case_id": f"{record['sample_id']}_repair",
            "sample_id": record["sample_id"],
            "cwe_id": cwe_id,
            "numeric_cwe_id": int(cwe_id.split("-")[1]),
            "cwe_name": record["cwe_name"],
            "cwe_definition": record["cwe_definition"],
            "expected_target_cwe": cwe_id,
            "expected_label": "secure_after_repair",
            "repair_model": validated["repair_model"],
            "repair_run_id": repair_record.get("run_id"),
            "detection_run_id": (
                repair_record.get("detection_input", {}).get("detection_run_id")
                if isinstance(repair_record.get("detection_input"), dict)
                else None
            ),
            "original_vulnerable_source_path": record["source_code_path"],
            "repair_record_path": repair_json.relative_to(project_root).as_posix(),
            "repaired_source_path": repaired_py.relative_to(project_root).as_posix(),
            "prepared_file_name": destination.name,
            "prepared_file_path": destination.relative_to(project_root).as_posix(),
            "repaired_source_sha256": destination_hash,
            "repair_parse_status": (
                repair_record.get("repair_output", {}).get("parse_status")
                if isinstance(repair_record.get("repair_output"), dict)
                else None
            ),
        })
        print(f"[{len(prepared_cases):>2}] {cwe_id:<9} PREPARED -> {destination.name}")

    prepared_cases.sort(key=lambda item: item["numeric_cwe_id"])
    manifest_payload = {
        "schema_version": "1.0",
        "run_id": run_id,
        "generated_at_utc": utc_now(),
        "stage": "repair_evaluation_preparation",
        "configuration": config.configuration_name,
        "repair_output_name": config.repair_output_name,
        "repair_evaluation_output_name": config.repair_evaluation_output_name,
        "source_manifest_path": manifest_file.relative_to(project_root).as_posix(),
        "repair_input_root": repair_root.relative_to(project_root).as_posix(),
        "prepared_source_root": prepared_source_root.relative_to(project_root).as_posix(),
        "case_count": len(prepared_cases),
        "cases": prepared_cases,
    }
    summary_payload = {
        "schema_version": "1.0",
        "run_id": run_id,
        "started_at_utc": started_at,
        "finished_at_utc": utc_now(),
        "configuration": config.configuration_name,
        "repair_output_name": config.repair_output_name,
        "repair_evaluation_output_name": config.repair_evaluation_output_name,
        "repair_input_root": repair_root.relative_to(project_root).as_posix(),
        "evaluation_output_root": evaluation_root.relative_to(project_root).as_posix(),
        "manifest_vulnerable_samples_considered": len(vulnerable_records),
        "prepared_case_count": len(prepared_cases),
        "not_repaired_case_count": len(skipped_not_repaired),
        "invalid_artifact_count": len(invalid_artifacts),
        "prepared_manifest_path": prepared_manifest_path.relative_to(project_root).as_posix(),
        "prepared_source_root": prepared_source_root.relative_to(project_root).as_posix(),
        "skipped_not_repaired": skipped_not_repaired,
        "invalid_artifacts": invalid_artifacts,
        "configuration_file": {
            "path": config_file.relative_to(project_root).as_posix(),
            "sha256": sha256_file(config_file),
        },
        "script": {
            "name": Path(__file__).name,
            "version": SCRIPT_VERSION,
            "sha256": sha256_file(Path(__file__).resolve()),
        },
    }

    write_json_atomic(prepared_manifest_path, manifest_payload)
    write_json_atomic(preparation_summary_path, summary_payload)

    print("\nRepair-evaluation dataset preparation complete.")
    print(f"  Prepared cases:       {len(prepared_cases)}")
    print(f"  Not repaired:         {len(skipped_not_repaired)}")
    print(f"  Invalid artifacts:    {len(invalid_artifacts)}")
    print(f"  Prepared source tree: {prepared_source_root}")
    print(f"  Manifest:             {prepared_manifest_path}")
    print(f"  Summary:              {preparation_summary_path}")

    if invalid_artifacts:
        print("\nResolve invalid repair artifacts before building CodeQL.", file=sys.stderr)
        return 2
    if not prepared_cases:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
