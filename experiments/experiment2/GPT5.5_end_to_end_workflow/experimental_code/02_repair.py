"""
End-to-End Workflow baseline: configurable single-pass repair stage.

Run from the repository root:

    python experiments/experiment2/scripts/02_repair.py

Options:
    --dry-run
    --limit N
    --cwe CWE-22
    --overwrite
    --retry-failed

The script repairs only ground-truth vulnerable samples that the detection
stage predicted as vulnerable. Vulnerable false negatives are intentionally
left unrepaired because they never reach the baseline repair stage.

Repair artifacts are written beneath outputs/<REPAIR_OUTPUT_NAME>/, where
REPAIR_OUTPUT_NAME is read from experiments/experiment2/scripts/config.py.
This allows multiple repair-model configurations to reuse the same detection
outputs without overwriting one another.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import random
import re
import sys
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore[assignment]


SCRIPT_VERSION = "1.1.0"
STAGE = "repair"
EXPERIMENT = Path("experiments/experiment2")
CONFIG_PATH = EXPERIMENT / "scripts/config.py"
MANIFEST_PATH = EXPERIMENT / "manifests/securityeval_manifest.json"
PROMPT_PATH = EXPERIMENT / "prompts/repair_prompt.md"
DETECTION_ROOT = EXPERIMENT / "outputs/detection"
LOG_PATH = EXPERIMENT / "logs/experiment_log.csv"

LOG_FIELDS = [
    "run_id", "timestamp_utc", "configuration", "stage", "sample_id",
    "cwe_id", "sample_kind", "model", "status", "latency_seconds",
    "input_path", "output_path", "error_message",
]


@dataclass(frozen=True)
class RuntimeConfig:
    configuration_name: str
    repair_model: str
    repair_output_name: str
    max_attempts: int
    retry_base_seconds: float
    timeout_seconds: float


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"Required file not found: {path}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise FileNotFoundError(f"Required JSON file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    temporary.replace(path)


def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)


def find_project_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / MANIFEST_PATH).is_file():
            return candidate
    raise FileNotFoundError(
        f"Could not locate repository root containing {MANIFEST_PATH}"
    )



def validate_output_name(value: str, *, field_name: str) -> str:
    """Validate a single safe directory name from config.py."""
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
    spec = importlib.util.spec_from_file_location("experiment2_config", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    model = str(getattr(module, "REPAIR_MODEL", "")).strip()
    if not model:
        raise ValueError("config.py must define a non-empty REPAIR_MODEL.")

    repair_output_name = validate_output_name(
        str(getattr(module, "REPAIR_OUTPUT_NAME", "")).strip(),
        field_name="REPAIR_OUTPUT_NAME",
    )

    config = RuntimeConfig(
        configuration_name=str(
            getattr(module, "CONFIGURATION_NAME", "secure_code_agent_baseline")
        ).strip(),
        repair_model=model,
        repair_output_name=repair_output_name,
        max_attempts=int(getattr(module, "MAX_API_ATTEMPTS", 3)),
        retry_base_seconds=float(getattr(module, "RETRY_BASE_SECONDS", 2.0)),
        timeout_seconds=float(getattr(module, "REQUEST_TIMEOUT_SECONDS", 120.0)),
    )
    if config.max_attempts < 1:
        raise ValueError("MAX_API_ATTEMPTS must be at least 1.")
    return config


def normalize_cwe(value: str) -> str:
    digits = "".join(ch for ch in value if ch.isdigit())
    if not digits:
        raise ValueError(f"Invalid CWE identifier: {value!r}")
    return f"CWE-{int(digits)}"


def strip_fence(text: str) -> str:
    stripped = text.strip()
    match = re.fullmatch(
        r"```(?:text|markdown|md)?\s*(.*?)\s*```",
        stripped,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return match.group(1).strip() if match else stripped


def render_prompt(
    template: str,
    *,
    cwe_id: str,
    definition: str,
    source_code: str,
) -> str:
    number = cwe_id.split("-", 1)[1]
    rendered = template
    replacements = {
        "<SN>": number,
        "<Definition>": definition,
        "{{CWE_ID}}": cwe_id,
        "{{CWE_NUMBER}}": number,
        "{{CWE_DEFINITION}}": definition,
    }
    for token, replacement in replacements.items():
        rendered = rendered.replace(token, replacement)

    if "{{SOURCE_CODE}}" in rendered:
        rendered = rendered.replace("{{SOURCE_CODE}}", source_code)
    else:
        rendered += (
            "\n\nVulnerable Python code:\n```python\n"
            + source_code.rstrip()
            + "\n```"
        )
    return rendered.strip()


def create_client(timeout_seconds: float) -> Any:
    if OpenAI is None:
        raise RuntimeError(
            "Install the OpenAI SDK with: python -m pip install --upgrade openai"
        )
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not defined.")
    return OpenAI(timeout=timeout_seconds)


def call_with_retry(
    client: Any,
    *,
    model: str,
    prompt: str,
    max_attempts: int,
    retry_base_seconds: float,
) -> tuple[Any, int]:
    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            response = client.responses.create(
                model=model,
                input=[{
                    "role": "user",
                    "content": [{"type": "input_text", "text": prompt}],
                }],
            )
            return response, attempt
        except Exception as exc:
            last_error = exc
            if attempt == max_attempts:
                break
            delay = retry_base_seconds * (2 ** (attempt - 1))
            delay += random.uniform(0, min(1.0, retry_base_seconds))
            print(
                f"    Attempt {attempt} failed ({type(exc).__name__}); "
                f"retrying in {delay:.1f}s..."
            )
            time.sleep(delay)
    assert last_error is not None
    raise last_error


def response_text(response: Any) -> str:
    text = getattr(response, "output_text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()

    fragments: list[str] = []
    for output_item in getattr(response, "output", []) or []:
        for content_item in getattr(output_item, "content", []) or []:
            item_text = getattr(content_item, "text", None)
            if isinstance(item_text, str) and item_text.strip():
                fragments.append(item_text.strip())
    if not fragments:
        raise ValueError("The model returned no readable text.")
    return "\n".join(fragments)


def serialize(value: Any) -> Any:
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if isinstance(value, (dict, list, str, int, float, bool)):
        return value
    return str(value)


def extract_python(raw: str) -> tuple[str | None, str]:
    blocks = re.findall(
        r"```([A-Za-z0-9_+\-]*)\s*\n?(.*?)```",
        raw.strip(),
        flags=re.DOTALL,
    )
    if blocks:
        python_blocks = [
            body.strip()
            for language, body in blocks
            if language.lower() in {"python", "py"} and body.strip()
        ]
        generic_blocks = [
            body.strip()
            for language, body in blocks
            if not language and body.strip()
        ]
        candidates = python_blocks or generic_blocks
        if candidates:
            code = max(candidates, key=len)
            if len(blocks) > 1:
                return code, "MULTIPLE_FENCES"
            return code, "PYTHON_FENCE" if python_blocks else "GENERIC_FENCE"

    text = raw.strip()
    if any(marker in text for marker in (
        "def ", "class ", "import ", "from ", "async def ", "if __name__"
    )):
        return text, "RAW_CODE"
    return None, "UNPARSEABLE"


def detection_path(root: Path, record: dict[str, Any]) -> Path:
    return root / record["cwe_id"] / "vulnerable.json"


def repair_record_path(root: Path, record: dict[str, Any]) -> Path:
    return root / record["cwe_id"] / "repair.json"


def repaired_code_path(root: Path, record: dict[str, Any]) -> Path:
    return root / record["cwe_id"] / "repaired.py"


def existing_status(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        value = load_json(path)
        return str(value.get("status", "UNKNOWN")).upper()
    except Exception:
        return "INVALID"


def should_skip(
    path: Path,
    *,
    overwrite: bool,
    retry_failed: bool,
) -> tuple[bool, str | None]:
    status = existing_status(path)
    if status is None:
        return False, None
    if overwrite:
        return False, status
    if retry_failed and status in {
        "FAILED", "PARSE_FAILED", "INVALID", "UNKNOWN"
    }:
        return False, status
    return True, status


def append_log(path: Path, row: dict[str, Any]) -> None:
    needs_header = not path.exists() or path.stat().st_size == 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOG_FIELDS, extrasaction="ignore")
        if needs_header:
            writer.writeheader()
        writer.writerow(row)


def select_candidates(
    manifest: list[dict[str, Any]],
    detection_root: Path,
    cwe_filter: str | None,
) -> tuple[list[tuple[dict[str, Any], dict[str, Any], Path]], dict[str, int], list[str]]:
    selected: list[tuple[dict[str, Any], dict[str, Any], Path]] = []
    counts = {
        "vulnerable_samples": 0,
        "eligible": 0,
        "false_negatives": 0,
        "unusable_detection_records": 0,
    }
    warnings: list[str] = []
    normalized = normalize_cwe(cwe_filter) if cwe_filter else None

    vulnerable = [
        item for item in manifest
        if item.get("sample_kind") == "vulnerable"
        and item.get("ground_truth_vulnerable") is True
    ]
    vulnerable.sort(key=lambda item: int(item["cwe_id"].split("-")[1]))

    for record in vulnerable:
        if normalized and record["cwe_id"] != normalized:
            continue
        counts["vulnerable_samples"] += 1
        path = detection_path(detection_root, record)
        try:
            detection = load_json(path)
            if detection.get("status") != "SUCCESS":
                raise ValueError("status is not SUCCESS")
            evaluation = detection.get("evaluation")
            if not isinstance(evaluation, dict):
                raise ValueError("missing evaluation block")
            prediction = evaluation.get("prediction_vulnerable")
            if not isinstance(prediction, bool):
                raise ValueError("prediction_vulnerable is not Boolean")
            if detection.get("sample", {}).get("sample_id") != record["sample_id"]:
                raise ValueError("sample_id does not match manifest")
        except Exception as exc:
            counts["unusable_detection_records"] += 1
            warnings.append(f"{record['sample_id']}: {exc}")
            continue

        if prediction is False:
            counts["false_negatives"] += 1
            continue

        counts["eligible"] += 1
        selected.append((record, detection, path))

    return selected, counts, warnings


def execute_one(
    *,
    project_root: Path,
    manifest_record: dict[str, Any],
    detection_record: dict[str, Any],
    detection_file: Path,
    prompt_template: str,
    config: RuntimeConfig,
    client: Any,
    record_file: Path,
    code_file: Path,
    run_id: str,
    dry_run: bool,
) -> tuple[str, float, str | None]:
    started = time.perf_counter()
    source_file = project_root / manifest_record["source_code_path"]
    source_code = read_text(source_file)
    prompt = render_prompt(
        prompt_template,
        cwe_id=manifest_record["cwe_id"],
        definition=manifest_record["cwe_definition"],
        source_code=source_code,
    )

    result: dict[str, Any] = {
        "schema_version": "1.0",
        "run_id": run_id,
        "timestamp_utc": utc_now(),
        "stage": STAGE,
        "configuration": config.configuration_name,
        "sample": {
            "sample_id": manifest_record["sample_id"],
            "cwe_id": manifest_record["cwe_id"],
            "cwe_name": manifest_record.get("cwe_name", ""),
            "cwe_definition": manifest_record["cwe_definition"],
            "sample_kind": manifest_record["sample_kind"],
            "ground_truth_vulnerable": manifest_record["ground_truth_vulnerable"],
            "source_code_path": manifest_record["source_code_path"],
            "source_code_sha256": sha256_text(source_code),
            "metadata_path": manifest_record.get("metadata_path"),
            "assignment_path": manifest_record.get("assignment_path"),
            "context_profile_path": manifest_record.get("context_profile_path"),
        },
        "detection_input": {
            "detection_record_path": detection_file.relative_to(project_root).as_posix(),
            "detection_run_id": detection_record.get("run_id"),
            "detection_model": detection_record.get("model", {}).get("model_id"),
            "prediction_vulnerable": True,
            "raw_detection_response": detection_record.get("response", {}).get("raw_text"),
        },
        "model": {
            "provider": "openai",
            "model_id": config.repair_model,
            "parameters": {
                "temperature": "provider_default",
                "top_p": "provider_default",
            },
        },
        "prompt": {
            "rendered_text": prompt,
            "sha256": sha256_text(prompt),
        },
        "response": None,
        "repair_output": {
            "repaired_code_path": code_file.relative_to(project_root).as_posix(),
            "repaired_code_sha256": None,
            "parse_status": None,
        },
        "execution": {
            "status": "RUNNING",
            "attempts": 0,
            "latency_seconds": None,
            "error_type": None,
            "error_message": None,
        },
        "status": "RUNNING",
    }

    if dry_run:
        latency = time.perf_counter() - started
        result["execution"].update({
            "status": "DRY_RUN",
            "latency_seconds": round(latency, 6),
        })
        result["status"] = "DRY_RUN"
        write_json_atomic(record_file, result)
        return "DRY_RUN", latency, None

    try:
        response, attempts = call_with_retry(
            client,
            model=config.repair_model,
            prompt=prompt,
            max_attempts=config.max_attempts,
            retry_base_seconds=config.retry_base_seconds,
        )
        raw = response_text(response)
        repaired_code, parse_status = extract_python(raw)
        latency = time.perf_counter() - started
        status = "SUCCESS" if repaired_code is not None else "PARSE_FAILED"

        result["response"] = {
            "response_id": getattr(response, "id", None),
            "raw_text": raw,
            "usage": serialize(getattr(response, "usage", None)),
            "raw_response_object": serialize(response),
        }
        result["repair_output"]["parse_status"] = parse_status

        if repaired_code is not None:
            normalized_code = repaired_code.rstrip() + "\n"
            write_text_atomic(code_file, normalized_code)
            result["repair_output"]["repaired_code_sha256"] = sha256_text(
                normalized_code
            )

        result["execution"].update({
            "status": status,
            "attempts": attempts,
            "latency_seconds": round(latency, 6),
        })
        result["status"] = status
        write_json_atomic(record_file, result)
        return status, latency, None

    except Exception as exc:
        latency = time.perf_counter() - started
        message = str(exc)
        result["execution"].update({
            "status": "FAILED",
            "latency_seconds": round(latency, 6),
            "error_type": type(exc).__name__,
            "error_message": message,
        })
        result["status"] = "FAILED"
        write_json_atomic(record_file, result)
        return "FAILED", latency, message


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run single-pass repair for detector-positive vulnerable samples."
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--cwe")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--retry-failed", action="store_true")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be at least 1.")
    if args.overwrite and args.retry_failed:
        parser.error("Use either --overwrite or --retry-failed, not both.")
    return args


def main() -> int:
    args = parse_args()
    try:
        project_root = find_project_root(Path(__file__).resolve().parent)
        
        env_path = project_root / ".env"
        load_dotenv(env_path)
        
        config_path = project_root / CONFIG_PATH
        manifest_path = project_root / MANIFEST_PATH
        prompt_path = project_root / PROMPT_PATH
        detection_root = project_root / DETECTION_ROOT
        log_path = project_root / LOG_PATH

        config = load_config(config_path)
        repair_output_root = (
            project_root / EXPERIMENT / "outputs" / config.repair_output_name
        )
        code_root = repair_output_root / "code"
        record_root = repair_output_root / "records"

        manifest = load_json(manifest_path)
        if not isinstance(manifest, list):
            raise TypeError("The manifest must contain a JSON list.")

        prompt_template = strip_fence(read_text(prompt_path))
        if not prompt_template or "replace this placeholder" in prompt_template.lower():
            raise ValueError("The repair prompt file is empty or still a placeholder.")

        candidates, selection_counts, warnings = select_candidates(
            manifest,
            detection_root,
            args.cwe,
        )
        if args.limit is not None:
            candidates = candidates[:args.limit]
        if not candidates:
            raise ValueError("No samples are eligible for repair.")

        code_root.mkdir(parents=True, exist_ok=True)
        record_root.mkdir(parents=True, exist_ok=True)
        client = None if args.dry_run else create_client(config.timeout_seconds)

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    run_id = (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        + "_" + uuid.uuid4().hex[:8]
    )
    started_utc = utc_now()
    started = time.perf_counter()

    snapshot = {
        "run_id": run_id,
        "created_at_utc": started_utc,
        "script": {
            "name": Path(__file__).name,
            "version": SCRIPT_VERSION,
            "sha256": sha256_file(Path(__file__).resolve()),
        },
        "configuration": asdict(config),
        "files": {
            "config_path": config_path.relative_to(project_root).as_posix(),
            "config_sha256": sha256_file(config_path),
            "manifest_path": manifest_path.relative_to(project_root).as_posix(),
            "manifest_sha256": sha256_file(manifest_path),
            "prompt_path": prompt_path.relative_to(project_root).as_posix(),
            "prompt_sha256": sha256_file(prompt_path),
            "detection_root": detection_root.relative_to(project_root).as_posix(),
            "repair_output_root": repair_output_root.relative_to(project_root).as_posix(),
            "repair_code_root": code_root.relative_to(project_root).as_posix(),
            "repair_record_root": record_root.relative_to(project_root).as_posix(),
        },
        "selection": {
            **selection_counts,
            "processed_after_limit": len(candidates),
            "sample_ids": [item[0]["sample_id"] for item in candidates],
            "filter_cwe": args.cwe,
            "limit": args.limit,
        },
        "options": {
            "dry_run": args.dry_run,
            "overwrite": args.overwrite,
            "retry_failed": args.retry_failed,
        },
    }
    snapshot_path = record_root / f"config_snapshot_{run_id}.json"
    write_json_atomic(snapshot_path, snapshot)

    print("\nSecure Code Agent Baseline — Single-Pass Repair")
    print("-----------------------------------------------")
    print(f"Run ID:                    {run_id}")
    print(f"Repair model:              {config.repair_model}")
    print(f"Configuration:             {config.configuration_name}")
    print(f"Repair output:             {repair_output_root.relative_to(project_root)}")
    print(f"Vulnerable samples:        {selection_counts['vulnerable_samples']}")
    print(f"Eligible for repair:       {selection_counts['eligible']}")
    print(f"Detection false negatives: {selection_counts['false_negatives']}")
    print(f"Unusable detection files:  {selection_counts['unusable_detection_records']}")
    print(f"Selected this run:         {len(candidates)}")
    print(f"Dry run:                   {args.dry_run}\n")

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
        print()

    completed = failed = skipped = dry_count = 0
    latencies: list[float] = []

    for position, (manifest_record, detection_record, detection_file) in enumerate(
        candidates, start=1
    ):
        record_file = repair_record_path(record_root, manifest_record)
        code_file = repaired_code_path(code_root, manifest_record)
        skip, old_status = should_skip(
            record_file,
            overwrite=args.overwrite,
            retry_failed=args.retry_failed,
        )

        if skip:
            skipped += 1
            print(
                f"[{position:>3}/{len(candidates)}] "
                f"{manifest_record['cwe_id']:<9} SKIPPED ({old_status})"
            )
            continue

        status, latency, error_message = execute_one(
            project_root=project_root,
            manifest_record=manifest_record,
            detection_record=detection_record,
            detection_file=detection_file,
            prompt_template=prompt_template,
            config=config,
            client=client,
            record_file=record_file,
            code_file=code_file,
            run_id=run_id,
            dry_run=args.dry_run,
        )

        if status == "SUCCESS":
            completed += 1
            latencies.append(latency)
        elif status == "DRY_RUN":
            dry_count += 1
        else:
            failed += 1

        append_log(log_path, {
            "run_id": run_id,
            "timestamp_utc": utc_now(),
            "configuration": config.configuration_name,
            "stage": STAGE,
            "sample_id": manifest_record["sample_id"],
            "cwe_id": manifest_record["cwe_id"],
            "sample_kind": manifest_record["sample_kind"],
            "model": config.repair_model,
            "status": status,
            "latency_seconds": round(latency, 6),
            "input_path": manifest_record["source_code_path"],
            "output_path": record_file.relative_to(project_root).as_posix(),
            "error_message": error_message or "",
        })

        print(
            f"[{position:>3}/{len(candidates)}] "
            f"{manifest_record['cwe_id']:<9} {status} | {latency:.2f}s"
        )

    elapsed = time.perf_counter() - started
    summary = {
        "run_id": run_id,
        "stage": STAGE,
        "configuration": config.configuration_name,
        "model": config.repair_model,
        "repair_output_name": config.repair_output_name,
        "repair_output_root": repair_output_root.relative_to(project_root).as_posix(),
        "started_at_utc": started_utc,
        "finished_at_utc": utc_now(),
        "elapsed_seconds": round(elapsed, 6),
        **selection_counts,
        "selected_this_run": len(candidates),
        "completed_repairs": completed,
        "failed_repairs": failed,
        "skipped_existing_repairs": skipped,
        "dry_run_repairs": dry_count,
        "average_api_latency_seconds": (
            round(sum(latencies) / len(latencies), 6) if latencies else None
        ),
        "minimum_api_latency_seconds": round(min(latencies), 6) if latencies else None,
        "maximum_api_latency_seconds": round(max(latencies), 6) if latencies else None,
        "config_snapshot_path": snapshot_path.relative_to(project_root).as_posix(),
        "warnings": warnings,
        "repair_security_evaluated": False,
        "evaluation_note": (
            "Repair security evaluation is deferred to 03_repair_evaluation.py."
        ),
    }
    summary_path = record_root / f"repair_summary_{run_id}.json"
    write_json_atomic(summary_path, summary)
    write_json_atomic(record_root / "repair_summary_latest.json", summary)

    print("\nRepair run complete.")
    print(f"  Completed: {completed}")
    print(f"  Failed:    {failed}")
    print(f"  Skipped:   {skipped}")
    print(f"  Dry run:   {dry_count}")
    print(f"  Output:    {repair_output_root}")
    print(f"  Summary:   {summary_path}")

    if failed:
        print(
            "\nReview failed records and rerun with --retry-failed.",
            file=sys.stderr,
        )
        return 2
    if selection_counts["unusable_detection_records"]:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
