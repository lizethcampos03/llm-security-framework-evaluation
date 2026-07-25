"""
Evaluate the configured repaired SecurityEval dataset with syntax validation,
Bandit, CodeQL, and an optional human-review decision file.

Run from the repository root:

    python experiments/experiment2/scripts/03_repair_evaluation.py

Typical first run:

    python experiments/experiment2/scripts/03_repair_evaluation.py

After completing manual_review_decisions.json:

    python experiments/experiment2/scripts/03_repair_evaluation.py --reuse-scanner-results

Useful options:

    --overwrite
        Replace scanner outputs and per-case evaluation records.

    --reuse-scanner-results
        Reuse existing syntax, Bandit, and CodeQL outputs and rebuild only the
        combined per-case records and summary.

    --codeql-path PATH
        Use an explicit CodeQL executable.

    --bandit-path PATH
        Use an explicit Bandit executable. By default, the script runs
        "<current-python> -m bandit".

    --codeql-suite SUITE
        Override the CodeQL query suite.

The repair-evaluation output directory is read from config.py using
REPAIR_EVALUATION_OUTPUT_NAME.

The script deliberately does not compute the final paper-level repair metrics.
That belongs to 04_metrics.py.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import time
import uuid
import warnings
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_VERSION = "1.1.0"
DEFAULT_TIMEOUT_SECONDS = 1800
DEFAULT_CODEQL_SUITE = (
    "codeql/python-queries:"
    "codeql-suites/python-security-and-quality.qls"
)

EXPERIMENT = Path("experiments/experiment2")
CONFIG_PATH = EXPERIMENT / "scripts/config.py"

# These relative paths are initialized from config.py in main().
EVALUATION_ROOT = EXPERIMENT / "outputs/repair_evaluation"
PREPARED_MANIFEST_PATH = EVALUATION_ROOT / "manifest.json"
PREPARED_SOURCE_ROOT = EVALUATION_ROOT / "prepared_source"
CODEQL_DB_PATH = EVALUATION_ROOT / "codeql_db"
CODEQL_BUILD_METADATA_PATH = EVALUATION_ROOT / "codeql_database_build.json"
SYNTAX_ROOT = EVALUATION_ROOT / "syntax"
SYNTAX_RESULTS_PATH = SYNTAX_ROOT / "results.json"
BANDIT_ROOT = EVALUATION_ROOT / "bandit"
BANDIT_RESULTS_PATH = BANDIT_ROOT / "results.json"
BANDIT_METADATA_PATH = BANDIT_ROOT / "analysis_metadata.json"
CODEQL_ROOT = EVALUATION_ROOT / "codeql"
CODEQL_SARIF_PATH = CODEQL_ROOT / "results.sarif"
CODEQL_METADATA_PATH = CODEQL_ROOT / "analysis_metadata.json"
RECORDS_ROOT = EVALUATION_ROOT / "records"
SUMMARY_PATH = EVALUATION_ROOT / "evaluation_summary.json"
MANUAL_REVIEW_PATH = EVALUATION_ROOT / "manual_review_decisions.json"


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


def configure_paths(config: RuntimeConfig) -> None:
    """Initialize model-specific relative paths used throughout this script."""
    global EVALUATION_ROOT
    global PREPARED_MANIFEST_PATH, PREPARED_SOURCE_ROOT
    global CODEQL_DB_PATH, CODEQL_BUILD_METADATA_PATH
    global SYNTAX_ROOT, SYNTAX_RESULTS_PATH
    global BANDIT_ROOT, BANDIT_RESULTS_PATH, BANDIT_METADATA_PATH
    global CODEQL_ROOT, CODEQL_SARIF_PATH, CODEQL_METADATA_PATH
    global RECORDS_ROOT, SUMMARY_PATH, MANUAL_REVIEW_PATH

    EVALUATION_ROOT = (
        EXPERIMENT / "outputs" / config.repair_evaluation_output_name
    )
    PREPARED_MANIFEST_PATH = EVALUATION_ROOT / "manifest.json"
    PREPARED_SOURCE_ROOT = EVALUATION_ROOT / "prepared_source"
    CODEQL_DB_PATH = EVALUATION_ROOT / "codeql_db"
    CODEQL_BUILD_METADATA_PATH = EVALUATION_ROOT / "codeql_database_build.json"

    SYNTAX_ROOT = EVALUATION_ROOT / "syntax"
    SYNTAX_RESULTS_PATH = SYNTAX_ROOT / "results.json"

    BANDIT_ROOT = EVALUATION_ROOT / "bandit"
    BANDIT_RESULTS_PATH = BANDIT_ROOT / "results.json"
    BANDIT_METADATA_PATH = BANDIT_ROOT / "analysis_metadata.json"

    CODEQL_ROOT = EVALUATION_ROOT / "codeql"
    CODEQL_SARIF_PATH = CODEQL_ROOT / "results.sarif"
    CODEQL_METADATA_PATH = CODEQL_ROOT / "analysis_metadata.json"

    RECORDS_ROOT = EVALUATION_ROOT / "records"
    SUMMARY_PATH = EVALUATION_ROOT / "evaluation_summary.json"
    MANUAL_REVIEW_PATH = EVALUATION_ROOT / "manual_review_decisions.json"


def run_command(
    command: list[str],
    *,
    timeout_seconds: int,
) -> tuple[int, str, str, float]:
    started = time.perf_counter()
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
        )
        return (
            result.returncode,
            result.stdout,
            result.stderr,
            time.perf_counter() - started,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = (
            exc.stdout.decode("utf-8", errors="replace")
            if isinstance(exc.stdout, bytes)
            else (exc.stdout or "")
        )
        stderr = (
            exc.stderr.decode("utf-8", errors="replace")
            if isinstance(exc.stderr, bytes)
            else (exc.stderr or "")
        )
        stderr = (
            f"{stderr}\nCommand timed out after {timeout_seconds} seconds."
        ).strip()
        return 124, stdout, stderr, time.perf_counter() - started


def resolve_executable(
    explicit_path: str | None,
    names: list[str],
    label: str,
) -> str:
    if explicit_path:
        candidate = Path(explicit_path).expanduser().resolve()
        if not candidate.is_file():
            raise FileNotFoundError(f"{label} executable not found: {candidate}")
        return str(candidate)

    for name in names:
        resolved = shutil.which(name)
        if resolved:
            return resolved

    raise FileNotFoundError(
        f"{label} was not found on PATH. Use the corresponding explicit-path "
        "option."
    )


def normalize_cwe(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().upper()
    digits = "".join(character for character in text if character.isdigit())
    if not digits:
        return None
    return f"CWE-{int(digits)}"


def normalize_uri_to_filename(uri: str) -> str:
    return Path(uri.replace("\\", "/")).name


def validate_inputs(
    *,
    project_root: Path,
    config: RuntimeConfig,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    manifest_path = project_root / PREPARED_MANIFEST_PATH
    source_root = project_root / PREPARED_SOURCE_ROOT
    database_path = project_root / CODEQL_DB_PATH
    build_metadata_path = project_root / CODEQL_BUILD_METADATA_PATH

    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise TypeError("Prepared manifest must be a JSON object.")

    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Prepared manifest has no cases.")

    if manifest.get("case_count") != len(cases):
        raise ValueError("Prepared manifest case_count does not match cases.")

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

    build_metadata = load_json(build_metadata_path)
    if build_metadata.get("status") != "SUCCESS":
        raise ValueError("CodeQL database-build metadata is not SUCCESS.")

    build_eval_name = str(
        build_metadata.get("repair_evaluation_output_name", "")
    ).strip()
    if build_eval_name and build_eval_name != config.repair_evaluation_output_name:
        raise ValueError(
            "CodeQL build metadata repair_evaluation_output_name does not match "
            f"config.py: {build_eval_name!r} != "
            f"{config.repair_evaluation_output_name!r}"
        )

    if not database_path.is_dir():
        raise FileNotFoundError(f"CodeQL database not found: {database_path}")

    if not (database_path / "codeql-database.yml").is_file():
        raise FileNotFoundError(
            "CodeQL database is missing codeql-database.yml."
        )

    cases_by_filename: dict[str, dict[str, Any]] = {}
    for case in cases:
        filename = str(case["prepared_file_name"])
        path = project_root / str(case["prepared_file_path"])

        if filename in cases_by_filename:
            raise ValueError(f"Duplicate prepared filename: {filename}")
        if not path.is_file():
            raise FileNotFoundError(f"Prepared source missing: {path}")
        if sha256_file(path) != case["repaired_source_sha256"]:
            raise ValueError(f"Prepared source hash mismatch: {path}")

        cases_by_filename[filename] = case

    actual_files = {path.name for path in source_root.glob("*.py")}
    expected_files = set(cases_by_filename)
    if actual_files != expected_files:
        raise ValueError(
            "Prepared source tree no longer matches the frozen manifest."
        )

    return manifest, cases_by_filename


def evaluate_syntax(
    *,
    project_root: Path,
    cases_by_filename: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    results: dict[str, Any] = {}

    for filename, case in sorted(cases_by_filename.items()):
        source_path = project_root / case["prepared_file_path"]
        source = source_path.read_text(encoding="utf-8")

        syntax_valid = True
        error: dict[str, Any] | None = None
        warning_records: list[dict[str, Any]] = []

        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                ast.parse(source, filename=str(source_path))
                compile(source, str(source_path), "exec")

            for item in caught:
                warning_records.append(
                    {
                        "category": item.category.__name__,
                        "message": str(item.message),
                        "line": item.lineno,
                    }
                )
        except SyntaxError as exc:
            syntax_valid = False
            error = {
                "type": "SyntaxError",
                "message": exc.msg,
                "line": exc.lineno,
                "offset": exc.offset,
                "end_line": getattr(exc, "end_lineno", None),
                "end_offset": getattr(exc, "end_offset", None),
                "text": exc.text.rstrip("\n") if exc.text else None,
            }
        except Exception as exc:
            syntax_valid = False
            error = {
                "type": type(exc).__name__,
                "message": str(exc),
            }

        results[filename] = {
            "case_id": case["case_id"],
            "sample_id": case["sample_id"],
            "cwe_id": case["cwe_id"],
            "prepared_file_name": filename,
            "prepared_file_path": case["prepared_file_path"],
            "sha256": case["repaired_source_sha256"],
            "syntax_valid": syntax_valid,
            "error": error,
            "warnings": warning_records,
        }

    return {
        "schema_version": "1.0",
        "generated_at_utc": utc_now(),
        "case_count": len(results),
        "valid_count": sum(
            1 for result in results.values() if result["syntax_valid"]
        ),
        "invalid_count": sum(
            1 for result in results.values() if not result["syntax_valid"]
        ),
        "results_by_file": results,
    }


def run_bandit(
    *,
    project_root: Path,
    bandit_path: str | None,
    timeout_seconds: int,
) -> dict[str, Any]:
    source_root = project_root / PREPARED_SOURCE_ROOT
    output_path = project_root / BANDIT_RESULTS_PATH
    metadata_path = project_root / BANDIT_METADATA_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if bandit_path:
        executable = resolve_executable(
            bandit_path,
            [],
            "Bandit",
        )
        command = [
            executable,
            "-r",
            str(source_root),
            "-f",
            "json",
            "-o",
            str(output_path),
        ]
    else:
        command = [
            sys.executable,
            "-m",
            "bandit",
            "-r",
            str(source_root),
            "-f",
            "json",
            "-o",
            str(output_path),
        ]

    returncode, stdout, stderr, latency = run_command(
        command,
        timeout_seconds=timeout_seconds,
    )

    # Bandit returns 1 when findings exist. That is still a successful scan.
    scan_success = returncode in {0, 1} and output_path.is_file()

    metadata = {
        "schema_version": "1.0",
        "generated_at_utc": utc_now(),
        "status": "SUCCESS" if scan_success else "FAILED",
        "command": command,
        "returncode": returncode,
        "latency_seconds": round(latency, 6),
        "results_path": output_path.relative_to(project_root).as_posix(),
        "results_exist": output_path.is_file(),
        "stdout": stdout,
        "stderr": stderr,
    }
    write_json_atomic(metadata_path, metadata)
    return metadata


def run_codeql(
    *,
    project_root: Path,
    codeql_path: str | None,
    codeql_suite: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    database_path = project_root / CODEQL_DB_PATH
    output_path = project_root / CODEQL_SARIF_PATH
    metadata_path = project_root / CODEQL_METADATA_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)

    executable = resolve_executable(
        codeql_path,
        ["codeql", "codeql.exe"],
        "CodeQL",
    )

    command = [
        executable,
        "database",
        "analyze",
        str(database_path),
        codeql_suite,
        "--format=sarif-latest",
        f"--output={output_path}",
        "--rerun",
    ]

    returncode, stdout, stderr, latency = run_command(
        command,
        timeout_seconds=timeout_seconds,
    )

    scan_success = returncode == 0 and output_path.is_file()

    metadata = {
        "schema_version": "1.0",
        "generated_at_utc": utc_now(),
        "status": "SUCCESS" if scan_success else "FAILED",
        "command": command,
        "query_suite": codeql_suite,
        "returncode": returncode,
        "latency_seconds": round(latency, 6),
        "sarif_path": output_path.relative_to(project_root).as_posix(),
        "sarif_exists": output_path.is_file(),
        "stdout": stdout,
        "stderr": stderr,
    }
    write_json_atomic(metadata_path, metadata)
    return metadata


def extract_codeql_rule_cwes(rule: dict[str, Any]) -> list[str]:
    properties = rule.get("properties", {}) or {}
    values: list[Any] = []

    values.extend(properties.get("tags", []) or [])
    values.extend(properties.get("cwe", []) or [])

    cwes = {
        normalized
        for value in values
        if (normalized := normalize_cwe(value)) is not None
    }
    return sorted(cwes, key=lambda value: int(value.split("-")[1]))


def is_codeql_security_rule(rule: dict[str, Any]) -> bool:
    properties = rule.get("properties", {}) or {}
    tags = [str(value).lower() for value in properties.get("tags", []) or []]
    rule_id = str(rule.get("id", "")).lower()

    return (
        "security" in tags
        or any(tag.startswith("external/cwe/") for tag in tags)
        or "/cwe-" in rule_id
        or bool(properties.get("security-severity"))
    )


def parse_codeql_sarif(
    path: Path,
    cases_by_filename: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    sarif = load_json(path)
    security_by_file: dict[str, list[dict[str, Any]]] = defaultdict(list)
    quality_by_file: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for run in sarif.get("runs", []) or []:
        rules_by_id: dict[str, dict[str, Any]] = {}
        driver = run.get("tool", {}).get("driver", {}) or {}

        for rule in driver.get("rules", []) or []:
            rules_by_id[str(rule.get("id", ""))] = rule

        for result in run.get("results", []) or []:
            rule_id = str(result.get("ruleId", ""))
            rule = rules_by_id.get(rule_id, {})
            locations = result.get("locations", []) or []
            if not locations:
                continue

            uri = (
                locations[0]
                .get("physicalLocation", {})
                .get("artifactLocation", {})
                .get("uri", "")
            )
            filename = normalize_uri_to_filename(uri)
            if filename not in cases_by_filename:
                continue

            region = (
                locations[0]
                .get("physicalLocation", {})
                .get("region", {})
            )

            finding = {
                "rule_id": rule_id,
                "rule_name": rule.get("name", ""),
                "message": result.get("message", {}).get("text", ""),
                "level": result.get("level"),
                "security_severity": (
                    rule.get("properties", {}) or {}
                ).get("security-severity"),
                "problem_severity": (
                    rule.get("properties", {}) or {}
                ).get("problem.severity"),
                "tags": (
                    rule.get("properties", {}) or {}
                ).get("tags", []) or [],
                "cwes": extract_codeql_rule_cwes(rule),
                "line": region.get("startLine"),
                "column": region.get("startColumn"),
            }

            if is_codeql_security_rule(rule):
                security_by_file[filename].append(finding)
            else:
                quality_by_file[filename].append(finding)

    return {
        filename: {
            "security_findings": security_by_file.get(filename, []),
            "quality_findings": quality_by_file.get(filename, []),
        }
        for filename in cases_by_filename
    }


def parse_bandit_results(
    path: Path,
    cases_by_filename: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    payload = load_json(path)
    findings_by_file: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for result in payload.get("results", []) or []:
        filename = Path(str(result.get("filename", ""))).name
        if filename not in cases_by_filename:
            continue

        issue_cwe = result.get("issue_cwe")
        cwe = None
        if isinstance(issue_cwe, dict):
            cwe = normalize_cwe(issue_cwe.get("id"))
        elif issue_cwe is not None:
            cwe = normalize_cwe(issue_cwe)

        findings_by_file[filename].append(
            {
                "test_id": result.get("test_id"),
                "test_name": result.get("test_name"),
                "issue_text": result.get("issue_text"),
                "issue_severity": result.get("issue_severity"),
                "issue_confidence": result.get("issue_confidence"),
                "cwe": cwe,
                "line_number": result.get("line_number"),
                "line_range": result.get("line_range"),
                "code": result.get("code"),
                "more_info": result.get("more_info"),
            }
        )

    return {
        filename: findings_by_file.get(filename, [])
        for filename in cases_by_filename
    }


def load_manual_reviews(
    path: Path,
    cases_by_filename: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        return {}

    payload = load_json(path)
    reviews = payload.get("reviews", [])
    if not isinstance(reviews, list):
        raise ValueError("manual_review_decisions.json reviews must be a list.")

    valid_decisions = {"SECURE", "INSECURE", "INVALID_REPAIR"}
    by_case_id: dict[str, dict[str, Any]] = {}

    valid_case_ids = {
        case["case_id"]
        for case in cases_by_filename.values()
    }

    for review in reviews:
        if not isinstance(review, dict):
            continue

        case_id = str(review.get("case_id", "")).strip()
        decision = str(review.get("decision", "")).strip().upper()

        if not case_id or not decision:
            continue
        if case_id not in valid_case_ids:
            raise ValueError(f"Unknown manual-review case_id: {case_id}")
        if decision not in valid_decisions:
            raise ValueError(
                f"Invalid manual decision for {case_id}: {decision}"
            )

        by_case_id[case_id] = {
            "decision": decision,
            "reviewer": review.get("reviewer"),
            "reviewed_at_utc": review.get("reviewed_at_utc"),
            "rationale": review.get("rationale"),
            "target_cwe_present": review.get("target_cwe_present"),
            "other_security_issue_present": review.get(
                "other_security_issue_present"
            ),
        }

    return by_case_id


def create_manual_review_template(
    *,
    path: Path,
    cases: list[dict[str, Any]],
) -> None:
    if path.exists():
        return

    payload = {
        "schema_version": "1.0",
        "instructions": [
            "Review the repaired source, original vulnerable source, target CWE, and scanner evidence.",
            "Set decision to SECURE, INSECURE, or INVALID_REPAIR.",
            "Do not change case_id values.",
            "Complete only cases whose current decision is blank.",
        ],
        "reviews": [
            {
                "case_id": case["case_id"],
                "sample_id": case["sample_id"],
                "cwe_id": case["cwe_id"],
                "prepared_file_path": case["prepared_file_path"],
                "decision": "",
                "target_cwe_present": None,
                "other_security_issue_present": None,
                "reviewer": "",
                "reviewed_at_utc": "",
                "rationale": "",
            }
            for case in cases
        ],
    }
    write_json_atomic(path, payload)


def combine_case_results(
    *,
    project_root: Path,
    manifest: dict[str, Any],
    syntax_payload: dict[str, Any],
    bandit_by_file: dict[str, list[dict[str, Any]]],
    codeql_by_file: dict[str, dict[str, Any]],
    manual_reviews: dict[str, dict[str, Any]],
    scanner_status: dict[str, str],
    run_id: str,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    syntax_by_file = syntax_payload["results_by_file"]

    for case in manifest["cases"]:
        filename = case["prepared_file_name"]
        target_cwe = normalize_cwe(case["expected_target_cwe"])
        syntax_result = syntax_by_file[filename]
        bandit_findings = bandit_by_file.get(filename, [])
        codeql_security = codeql_by_file[filename]["security_findings"]
        codeql_quality = codeql_by_file[filename]["quality_findings"]

        codeql_target = [
            finding
            for finding in codeql_security
            if target_cwe in finding.get("cwes", [])
        ]
        bandit_target = [
            finding
            for finding in bandit_findings
            if finding.get("cwe") == target_cwe
        ]

        detected_cwes = sorted(
            {
                cwe
                for finding in codeql_security
                for cwe in finding.get("cwes", [])
            }
            | {
                finding["cwe"]
                for finding in bandit_findings
                if finding.get("cwe")
            },
            key=lambda value: int(value.split("-")[1]),
        )

        target_detected = bool(codeql_target or bandit_target)
        other_security_findings = bool(
            [
                finding
                for finding in codeql_security
                if target_cwe not in finding.get("cwes", [])
            ]
            or [
                finding
                for finding in bandit_findings
                if finding.get("cwe") != target_cwe
            ]
        )

        manual_review = manual_reviews.get(case["case_id"])

        if not syntax_result["syntax_valid"]:
            automated_status = "INVALID_REPAIR"
            final_status = "INVALID_REPAIR"
            decision_source = "syntax_validation"
        elif (
            scanner_status["bandit"] != "SUCCESS"
            or scanner_status["codeql"] != "SUCCESS"
        ):
            automated_status = "EVALUATION_FAILED"
            final_status = "EVALUATION_FAILED"
            decision_source = "scanner_execution"
        elif target_detected:
            automated_status = "TARGET_CWE_DETECTED"
            final_status = "INSECURE"
            decision_source = "automated_scanners"
        else:
            automated_status = "TARGET_CWE_NOT_DETECTED"
            if manual_review:
                final_status = manual_review["decision"]
                decision_source = "manual_review"
            else:
                final_status = "MANUAL_REVIEW_REQUIRED"
                decision_source = "pending_manual_review"

        record = {
            "schema_version": "1.0",
            "run_id": run_id,
            "generated_at_utc": utc_now(),
            "stage": "repair_evaluation",
            "configuration": manifest.get(
                "configuration",
                "secure_code_agent_baseline",
            ),
            "repair_output_name": manifest.get("repair_output_name"),
            "repair_evaluation_output_name": manifest.get(
                "repair_evaluation_output_name"
            ),
            "case": {
                "case_id": case["case_id"],
                "sample_id": case["sample_id"],
                "cwe_id": case["cwe_id"],
                "cwe_name": case.get("cwe_name"),
                "cwe_definition": case.get("cwe_definition"),
                "expected_target_cwe": target_cwe,
                "repair_model": case.get("repair_model"),
                "repair_run_id": case.get("repair_run_id"),
                "detection_run_id": case.get("detection_run_id"),
                "original_vulnerable_source_path": (
                    case.get("original_vulnerable_source_path")
                ),
                "repair_record_path": case.get("repair_record_path"),
                "repaired_source_path": case.get("repaired_source_path"),
                "prepared_file_path": case["prepared_file_path"],
                "prepared_file_name": filename,
                "repaired_source_sha256": (
                    case["repaired_source_sha256"]
                ),
                "repair_parse_status": case.get("repair_parse_status"),
            },
            "syntax": syntax_result,
            "bandit": {
                "scanner_status": scanner_status["bandit"],
                "finding_count": len(bandit_findings),
                "target_cwe_finding_count": len(bandit_target),
                "target_cwe_findings": bandit_target,
                "all_findings": bandit_findings,
            },
            "codeql": {
                "scanner_status": scanner_status["codeql"],
                "security_finding_count": len(codeql_security),
                "quality_finding_count": len(codeql_quality),
                "target_cwe_finding_count": len(codeql_target),
                "target_cwe_findings": codeql_target,
                "security_findings": codeql_security,
                "ignored_quality_findings": codeql_quality,
            },
            "automated_assessment": {
                "status": automated_status,
                "target_cwe_detected": target_detected,
                "other_security_findings_detected": other_security_findings,
                "detected_cwes": detected_cwes,
            },
            "manual_review": manual_review,
            "final_assessment": {
                "status": final_status,
                "decision_source": decision_source,
            },
        }

        output_path = (
            project_root
            / RECORDS_ROOT
            / case["cwe_id"]
            / "evaluation.json"
        )
        write_json_atomic(output_path, record)
        records.append(record)

    return records


def summarize(
    *,
    records: list[dict[str, Any]],
    run_id: str,
    started_at_utc: str,
    scanner_metadata: dict[str, Any],
    project_root: Path,
    config: RuntimeConfig,
    config_path: Path,
) -> dict[str, Any]:
    status_counts: dict[str, int] = defaultdict(int)
    automated_counts: dict[str, int] = defaultdict(int)

    for record in records:
        status_counts[
            record["final_assessment"]["status"]
        ] += 1
        automated_counts[
            record["automated_assessment"]["status"]
        ] += 1

    invalid_cases = [
        record["case"]["cwe_id"]
        for record in records
        if record["final_assessment"]["status"] == "INVALID_REPAIR"
    ]
    target_detected_cases = [
        record["case"]["cwe_id"]
        for record in records
        if record["automated_assessment"]["target_cwe_detected"]
    ]

    return {
        "schema_version": "1.0",
        "run_id": run_id,
        "stage": "repair_evaluation",
        "configuration": config.configuration_name,
        "repair_output_name": config.repair_output_name,
        "repair_evaluation_output_name": config.repair_evaluation_output_name,
        "evaluation_output_root": EVALUATION_ROOT.as_posix(),
        "started_at_utc": started_at_utc,
        "finished_at_utc": utc_now(),
        "evaluated_case_count": len(records),
        "final_status_counts": dict(sorted(status_counts.items())),
        "automated_status_counts": dict(sorted(automated_counts.items())),
        "invalid_repair_cases": invalid_cases,
        "target_cwe_detected_cases": target_detected_cases,
        "manual_review_required_count": status_counts.get(
            "MANUAL_REVIEW_REQUIRED",
            0,
        ),
        "scanner_metadata": scanner_metadata,
        "records_root": (
            (project_root / RECORDS_ROOT)
            .relative_to(project_root)
            .as_posix()
        ),
        "manual_review_path": (
            (project_root / MANUAL_REVIEW_PATH)
            .relative_to(project_root)
            .as_posix()
        ),
        "notes": [
            "A syntactically invalid repaired file is classified as INVALID_REPAIR.",
            "An exact target-CWE finding from CodeQL or Bandit is classified as INSECURE.",
            "Absence of an automated target-CWE finding is not treated as proof of security.",
            "SECURE status requires a completed manual-review decision.",
            "Paper-level repair metrics are intentionally deferred to 04_metrics.py.",
        ],
        "configuration_file": {
            "path": config_path.relative_to(project_root).as_posix(),
            "sha256": sha256_file(config_path),
        },
        "script": {
            "name": Path(__file__).name,
            "version": SCRIPT_VERSION,
            "sha256": sha256_file(Path(__file__).resolve()),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate repaired samples using syntax validation, Bandit, "
            "CodeQL, and optional human review."
        )
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing scanner outputs and evaluation records.",
    )
    parser.add_argument(
        "--reuse-scanner-results",
        action="store_true",
        help=(
            "Reuse existing syntax, Bandit, and CodeQL results and rebuild "
            "combined records."
        ),
    )
    parser.add_argument(
        "--codeql-path",
        type=str,
        default=None,
        help="Explicit path to codeql or codeql.exe.",
    )
    parser.add_argument(
        "--bandit-path",
        type=str,
        default=None,
        help="Explicit path to a Bandit executable.",
    )
    parser.add_argument(
        "--codeql-suite",
        type=str,
        default=DEFAULT_CODEQL_SUITE,
        help="CodeQL query suite to execute.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=(
            "Maximum execution time per scanner. "
            f"Default: {DEFAULT_TIMEOUT_SECONDS}."
        ),
    )

    args = parser.parse_args()

    if args.timeout_seconds < 1:
        parser.error("--timeout-seconds must be at least 1.")
    if args.overwrite and args.reuse_scanner_results:
        parser.error(
            "--overwrite and --reuse-scanner-results cannot be combined."
        )

    return args


def main() -> int:
    args = parse_args()
    started_at_utc = utc_now()
    run_id = (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        + "_"
        + uuid.uuid4().hex[:8]
    )

    try:
        project_root = find_project_root(Path(__file__).resolve().parent)
        config_path = project_root / CONFIG_PATH
        config = load_config(config_path)
        configure_paths(config)

        manifest, cases_by_filename = validate_inputs(
            project_root=project_root,
            config=config,
        )

        output_paths = [
            project_root / SYNTAX_RESULTS_PATH,
            project_root / BANDIT_RESULTS_PATH,
            project_root / BANDIT_METADATA_PATH,
            project_root / CODEQL_SARIF_PATH,
            project_root / CODEQL_METADATA_PATH,
            project_root / SUMMARY_PATH,
            project_root / RECORDS_ROOT,
        ]

        if args.overwrite:
            for path in output_paths:
                if path.is_dir():
                    shutil.rmtree(path)
                elif path.exists():
                    path.unlink()
        elif not args.reuse_scanner_results:
            existing = [str(path) for path in output_paths if path.exists()]
            if existing:
                raise FileExistsError(
                    "Repair-evaluation outputs already exist. Use "
                    "--overwrite to replace them or "
                    "--reuse-scanner-results to reuse them.\n"
                    + "\n".join(existing)
                )

        create_manual_review_template(
            path=project_root / MANUAL_REVIEW_PATH,
            cases=manifest["cases"],
        )

        if args.reuse_scanner_results:
            syntax_payload = load_json(project_root / SYNTAX_RESULTS_PATH)
            bandit_metadata = load_json(
                project_root / BANDIT_METADATA_PATH
            )
            codeql_metadata = load_json(
                project_root / CODEQL_METADATA_PATH
            )
        else:
            syntax_payload = evaluate_syntax(
                project_root=project_root,
                cases_by_filename=cases_by_filename,
            )
            write_json_atomic(
                project_root / SYNTAX_RESULTS_PATH,
                syntax_payload,
            )

            bandit_metadata = run_bandit(
                project_root=project_root,
                bandit_path=args.bandit_path,
                timeout_seconds=args.timeout_seconds,
            )

            codeql_metadata = run_codeql(
                project_root=project_root,
                codeql_path=args.codeql_path,
                codeql_suite=args.codeql_suite,
                timeout_seconds=args.timeout_seconds,
            )

        if not (project_root / BANDIT_RESULTS_PATH).is_file():
            raise FileNotFoundError(
                f"Bandit results missing: {project_root / BANDIT_RESULTS_PATH}"
            )
        if not (project_root / CODEQL_SARIF_PATH).is_file():
            raise FileNotFoundError(
                f"CodeQL SARIF missing: {project_root / CODEQL_SARIF_PATH}"
            )

        bandit_by_file = parse_bandit_results(
            project_root / BANDIT_RESULTS_PATH,
            cases_by_filename,
        )
        codeql_by_file = parse_codeql_sarif(
            project_root / CODEQL_SARIF_PATH,
            cases_by_filename,
        )
        manual_reviews = load_manual_reviews(
            project_root / MANUAL_REVIEW_PATH,
            cases_by_filename,
        )

        scanner_status = {
            "bandit": bandit_metadata.get("status", "FAILED"),
            "codeql": codeql_metadata.get("status", "FAILED"),
        }

        records = combine_case_results(
            project_root=project_root,
            manifest=manifest,
            syntax_payload=syntax_payload,
            bandit_by_file=bandit_by_file,
            codeql_by_file=codeql_by_file,
            manual_reviews=manual_reviews,
            scanner_status=scanner_status,
            run_id=run_id,
        )

        summary = summarize(
            records=records,
            run_id=run_id,
            started_at_utc=started_at_utc,
            scanner_metadata={
                "syntax_results_path": (
                    SYNTAX_RESULTS_PATH.as_posix()
                ),
                "bandit": bandit_metadata,
                "codeql": codeql_metadata,
            },
            project_root=project_root,
            config=config,
            config_path=config_path,
        )
        write_json_atomic(project_root / SUMMARY_PATH, summary)

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("\nRepair evaluation complete.")
    print(f"  Configuration:         {summary['configuration']}")
    print(f"  Evaluation output:     {project_root / EVALUATION_ROOT}")
    print(f"  Evaluated cases:       {summary['evaluated_case_count']}")
    print(
        "  Invalid repairs:       "
        f"{summary['final_status_counts'].get('INVALID_REPAIR', 0)}"
    )
    print(
        "  Insecure:              "
        f"{summary['final_status_counts'].get('INSECURE', 0)}"
    )
    print(
        "  Manual review needed:  "
        f"{summary['manual_review_required_count']}"
    )
    print(f"  Summary:               {project_root / SUMMARY_PATH}")
    print(f"  Manual review file:    {project_root / MANUAL_REVIEW_PATH}")

    if (
        summary["scanner_metadata"]["bandit"].get("status") != "SUCCESS"
        or summary["scanner_metadata"]["codeql"].get("status") != "SUCCESS"
    ):
        print(
            "\nOne or more scanners failed. Review their metadata before "
            "using these evaluation records.",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
