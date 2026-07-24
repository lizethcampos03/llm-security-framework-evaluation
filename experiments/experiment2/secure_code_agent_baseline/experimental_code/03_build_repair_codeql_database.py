"""Build one Python CodeQL database for the configured repaired-code evaluation dataset.

Run from repository root:
    python experiments/experiment2/scripts/03_build_repair_codeql_database.py

Options:
    --overwrite
    --codeql-path PATH
    --timeout-seconds N

The repair-evaluation output directory is read from config.py using
REPAIR_EVALUATION_OUTPUT_NAME.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_VERSION = "1.1.0"
EXPERIMENT = Path("experiments/experiment2")
CONFIG_PATH = EXPERIMENT / "scripts/config.py"
DEFAULT_TIMEOUT = 1800


@dataclass(frozen=True)
class RuntimeConfig:
    configuration_name: str
    repair_output_name: str
    repair_evaluation_output_name: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise FileNotFoundError(f"Required JSON file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write("\n")
    tmp.replace(path)


def find_project_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / CONFIG_PATH).is_file():
            return candidate
    raise FileNotFoundError(
        "Could not locate the repository root. Expected to find:\n"
        f"  {CONFIG_PATH}"
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


def resolve_codeql(explicit: str | None) -> str:
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"CodeQL executable not found: {path}")
        return str(path)
    resolved = shutil.which("codeql") or shutil.which("codeql.exe")
    if not resolved:
        raise FileNotFoundError(
            "CodeQL was not found on PATH. Use --codeql-path <path-to-codeql.exe>."
        )
    return resolved


def run(command: list[str], timeout: int) -> tuple[int, str, str, float]:
    started = time.perf_counter()
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return result.returncode, result.stdout, result.stderr, time.perf_counter() - started
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        stderr = (stderr + f"\nTimed out after {timeout} seconds.").strip()
        return 124, stdout, stderr, time.perf_counter() - started


def validate_dataset(root: Path, manifest_path: Path, source_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("cases"), list):
        raise ValueError("Prepared manifest must contain a cases list.")
    cases = manifest["cases"]
    if manifest.get("case_count") != len(cases):
        raise ValueError("Prepared manifest case_count does not match cases length.")
    if not source_root.is_dir():
        raise FileNotFoundError(f"Prepared source directory not found: {source_root}")

    validated: list[dict[str, Any]] = []
    expected_names: set[str] = set()
    for i, case in enumerate(cases):
        if not isinstance(case, dict):
            raise TypeError(f"Case {i} is not an object.")
        required = {
            "case_id", "sample_id", "cwe_id", "prepared_file_name",
            "prepared_file_path", "repaired_source_sha256",
        }
        missing = sorted(required - case.keys())
        if missing:
            raise ValueError(f"Case {i} missing: {', '.join(missing)}")
        name = str(case["prepared_file_name"])
        if name in expected_names:
            raise ValueError(f"Duplicate prepared filename: {name}")
        expected_names.add(name)
        path = root / str(case["prepared_file_path"])
        if not path.is_file():
            raise FileNotFoundError(f"Prepared source file missing: {path}")
        actual_hash = sha256_file(path)
        if actual_hash != str(case["repaired_source_sha256"]):
            raise ValueError(f"SHA-256 mismatch: {path}")
        validated.append({
            "case_id": case["case_id"],
            "sample_id": case["sample_id"],
            "cwe_id": case["cwe_id"],
            "prepared_file_name": name,
            "prepared_file_path": path.relative_to(root).as_posix(),
            "sha256": actual_hash,
        })

    actual_names = {p.name for p in source_root.glob("*.py")}
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        extra = sorted(actual_names - expected_names)
        raise ValueError(f"Prepared tree mismatch. Missing={missing}; Extra={extra}")
    if not validated:
        raise ValueError("Prepared dataset contains no cases.")
    return manifest, validated


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the repair-evaluation CodeQL database.")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--codeql-path")
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT)
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("--timeout-seconds must be at least 1.")
    return args


def main() -> int:
    args = parse_args()
    try:
        root = find_project_root(Path(__file__).resolve().parent)
        config_path = root / CONFIG_PATH
        config = load_config(config_path)

        evaluation_root = (
            root
            / EXPERIMENT
            / "outputs"
            / config.repair_evaluation_output_name
        )
        manifest_path = evaluation_root / "manifest.json"
        source_root = evaluation_root / "prepared_source"
        db_path = evaluation_root / "codeql_db"
        metadata_path = evaluation_root / "codeql_database_build.json"

        codeql = resolve_codeql(args.codeql_path)
        manifest, cases = validate_dataset(root, manifest_path, source_root)

        manifest_configuration = str(manifest.get("configuration", "")).strip()
        if manifest_configuration and manifest_configuration != config.configuration_name:
            raise ValueError(
                "Prepared manifest configuration does not match config.py: "
                f"{manifest_configuration!r} != {config.configuration_name!r}"
            )

        manifest_eval_name = str(
            manifest.get("repair_evaluation_output_name", "")
        ).strip()
        if (
            manifest_eval_name
            and manifest_eval_name != config.repair_evaluation_output_name
        ):
            raise ValueError(
                "Prepared manifest repair_evaluation_output_name does not match "
                f"config.py: {manifest_eval_name!r} != "
                f"{config.repair_evaluation_output_name!r}"
            )

        if db_path.exists():
            if not args.overwrite:
                raise FileExistsError(f"Database already exists: {db_path}. Use --overwrite.")
            shutil.rmtree(db_path) if db_path.is_dir() else db_path.unlink()
        if args.overwrite:
            metadata_path.unlink(missing_ok=True)
        db_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8]
    started = utc_now()

    version_cmd = [codeql, "version", "--format=json"]
    vrc, vout, verr, vlat = run(version_cmd, min(args.timeout_seconds, 120))
    try:
        version: Any = json.loads(vout) if vrc == 0 else None
    except json.JSONDecodeError:
        version = {"raw_stdout": vout.strip()}

    create_cmd = [
        codeql,
        "database",
        "create",
        str(db_path),
        "--language=python",
        f"--source-root={source_root}",
    ]

    print("\nBuild Repair CodeQL Database")
    print("----------------------------")
    print(f"Run ID:         {run_id}")
    print(f"Configuration:  {config.configuration_name}")
    print(f"Eval output:    {config.repair_evaluation_output_name}")
    print(f"Prepared cases: {len(cases)}")
    print(f"Source root:    {source_root}")
    print(f"Database:       {db_path}")
    print("\nCommand:")
    print(" ".join(create_cmd))
    print()

    rc, stdout, stderr, latency = run(create_cmd, args.timeout_seconds)
    success = rc == 0 and db_path.is_dir()
    markers = [
        p.relative_to(root).as_posix()
        for p in [db_path / "codeql-database.yml", db_path / "db-python"]
        if p.exists()
    ]

    metadata = {
        "schema_version": "1.0",
        "run_id": run_id,
        "stage": "repair_evaluation_codeql_database_build",
        "configuration": config.configuration_name,
        "repair_output_name": config.repair_output_name,
        "repair_evaluation_output_name": config.repair_evaluation_output_name,
        "evaluation_output_root": evaluation_root.relative_to(root).as_posix(),
        "started_at_utc": started,
        "finished_at_utc": utc_now(),
        "status": "SUCCESS" if success else "FAILED",
        "prepared_manifest_path": manifest_path.relative_to(root).as_posix(),
        "prepared_manifest_sha256": sha256_file(manifest_path),
        "prepared_source_root": source_root.relative_to(root).as_posix(),
        "prepared_case_count": len(cases),
        "prepared_cases": cases,
        "codeql": {
            "executable": codeql,
            "version_command": version_cmd,
            "version_returncode": vrc,
            "version_latency_seconds": round(vlat, 6),
            "version": version,
            "version_stderr": verr,
        },
        "database": {
            "path": db_path.relative_to(root).as_posix(),
            "language": "python",
            "create_command": create_cmd,
            "returncode": rc,
            "latency_seconds": round(latency, 6),
            "exists": db_path.is_dir(),
            "markers": markers,
            "stdout": stdout,
            "stderr": stderr,
        },
        "configuration_file": {
            "path": config_path.relative_to(root).as_posix(),
            "sha256": sha256_file(config_path),
        },
        "script": {
            "name": Path(__file__).name,
            "version": SCRIPT_VERSION,
            "sha256": sha256_file(Path(__file__).resolve()),
        },
    }
    write_json_atomic(metadata_path, metadata)

    print("CodeQL database build complete.")
    print(f"  Status:      {metadata['status']}")
    print(f"  Eval output: {evaluation_root}")
    print(f"  Return code: {rc}")
    print(f"  Latency:     {latency:.2f}s")
    print(f"  Database:    {db_path}")
    print(f"  Metadata:    {metadata_path}")
    if stdout.strip():
        print("\nSTDOUT:\n" + stdout)
    if stderr.strip():
        print("\nSTDERR:\n" + stderr)

    if not success:
        print("\nDatabase build failed. Review the metadata and terminal output.", file=sys.stderr)
        return rc if rc != 0 else 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())