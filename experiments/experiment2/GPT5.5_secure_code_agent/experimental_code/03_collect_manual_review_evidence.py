"""
Collect all manual-review evidence for the configured Experiment 2 repair run
into one self-contained JSON file.

Run from the repository root:

    python experiments/experiment2/scripts/03_collect_manual_review_evidence.py

Options:

    --overwrite
        Replace an existing consolidated evidence file.

    --output PATH
        Override the default output path.

    --include-automated
        Include cases already resolved automatically as INSECURE or
        INVALID_REPAIR. By default, only MANUAL_REVIEW_REQUIRED cases are
        collected.

    --case-id CASE_ID
        Collect only one specific case.

    --cwe CWE_ID
        Collect only one specific CWE, for example CWE-79.

The default output file is:

    experiments/experiment2/outputs/<REPAIR_EVALUATION_OUTPUT_NAME>/
        manual_review_evidence_all.json
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_VERSION = "1.0.0"
SCHEMA_VERSION = "1.0"

EXPERIMENT = Path("experiments/experiment2")
CONFIG_PATH = EXPERIMENT / "scripts/config.py"


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


def read_text_file(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"Required text file not found: {path}")
    return path.read_text(encoding="utf-8")


def find_project_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / CONFIG_PATH).is_file():
            return candidate
    raise FileNotFoundError(
        "Could not locate the repository root. Expected to find:\n"
        f"  {CONFIG_PATH}"
    )


def validate_output_name(value: str, *, field_name: str) -> str:
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


def normalize_cwe(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().upper()
    digits = "".join(character for character in text if character.isdigit())
    if not digits:
        return None
    return f"CWE-{int(digits)}"


def cwe_number(value: str) -> int:
    normalized = normalize_cwe(value)
    if normalized is None:
        return 10**9
    return int(normalized.split("-")[1])


BATCH_DEFINITIONS: list[dict[str, Any]] = [
    {
        "batch_id": "batch_01",
        "name": "Injection, paths, and interpreter boundaries",
        "description": (
            "Input validation, path traversal, command/query/code injection, "
            "template or interpreter-boundary weaknesses."
        ),
        "cwes": {
            "CWE-20", "CWE-22", "CWE-78", "CWE-89", "CWE-90",
            "CWE-94", "CWE-95", "CWE-99", "CWE-643",
        },
    },
    {
        "batch_id": "batch_02",
        "name": "Web output, headers, redirects, and content handling",
        "description": (
            "Cross-site scripting, HTTP header/response issues, redirect logic, "
            "and context-sensitive output handling."
        ),
        "cwes": {
            "CWE-79", "CWE-80", "CWE-113", "CWE-116", "CWE-117",
            "CWE-425", "CWE-601",
        },
    },
    {
        "batch_id": "batch_03",
        "name": "Authentication, authorization, privilege, and business logic",
        "description": (
            "Identity checks, permission enforcement, privileged operations, "
            "state transitions, and business-logic invariants."
        ),
        "cwes": {
            "CWE-250", "CWE-283", "CWE-285", "CWE-306", "CWE-841",
            "CWE-1204",
        },
    },
    {
        "batch_id": "batch_04",
        "name": "Secrets, credentials, and information exposure",
        "description": (
            "Hard-coded credentials, sensitive-data disclosure, insecure "
            "transport, logging, storage, and debug exposure."
        ),
        "cwes": {
            "CWE-200", "CWE-209", "CWE-215", "CWE-259", "CWE-319",
            "CWE-321", "CWE-522", "CWE-798",
        },
    },
    {
        "batch_id": "batch_05",
        "name": "Cryptography, protocols, and randomness",
        "description": (
            "Weak algorithms, keys, random generation, signatures, verification, "
            "and secure protocol configuration."
        ),
        "cwes": {
            "CWE-295", "CWE-326", "CWE-327", "CWE-329", "CWE-330",
            "CWE-347", "CWE-759", "CWE-760",
        },
    },
    {
        "batch_id": "batch_06",
        "name": "Files, uploads, temporary files, permissions, and races",
        "description": (
            "File creation and use, race conditions, temporary files, uploads, "
            "filesystem permissions, and object identity."
        ),
        "cwes": {
            "CWE-367", "CWE-377", "CWE-379", "CWE-434", "CWE-454",
            "CWE-732",
        },
    },
    {
        "batch_id": "batch_07",
        "name": "Serialization, XML, parsers, and external resources",
        "description": (
            "Unsafe deserialization, XML parsing, entity expansion, external "
            "resource access, and server-side requests."
        ),
        "cwes": {
            "CWE-477", "CWE-502", "CWE-611", "CWE-641", "CWE-776",
            "CWE-918",
        },
    },
    {
        "batch_id": "batch_08",
        "name": "Resource management, control flow, and remaining logic",
        "description": (
            "Resource exhaustion, loops, numeric or state errors, unusual control "
            "flow, and cases not covered by the other thematic groups."
        ),
        "cwes": {
            "CWE-193", "CWE-385", "CWE-400", "CWE-406", "CWE-595",
            "CWE-835",
        },
    },
]


def assign_batch(cwe_id: str) -> tuple[str, str, str]:
    normalized = normalize_cwe(cwe_id) or cwe_id
    for definition in BATCH_DEFINITIONS:
        if normalized in definition["cwes"]:
            return (
                definition["batch_id"],
                definition["name"],
                definition["description"],
            )
    return (
        "batch_08",
        "Resource management, control flow, and remaining logic",
        "Fallback group for review cases not explicitly mapped elsewhere.",
    )


def resolve_repo_path(project_root: Path, value: Any) -> Path | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None

    candidate = Path(text)
    if candidate.is_absolute():
        return candidate
    return project_root / candidate


def load_optional_json(path: Path | None) -> tuple[Any | None, dict[str, Any]]:
    if path is None:
        return None, {
            "path": None,
            "exists": False,
            "sha256": None,
            "error": "No path was provided.",
        }

    if not path.is_file():
        return None, {
            "path": path.as_posix(),
            "exists": False,
            "sha256": None,
            "error": "File not found.",
        }

    try:
        payload = load_json(path)
        return payload, {
            "path": path.as_posix(),
            "exists": True,
            "sha256": sha256_file(path),
            "error": None,
        }
    except Exception as exc:
        return None, {
            "path": path.as_posix(),
            "exists": True,
            "sha256": sha256_file(path),
            "error": str(exc),
        }


def load_optional_text(path: Path | None) -> tuple[str | None, dict[str, Any]]:
    if path is None:
        return None, {
            "path": None,
            "exists": False,
            "sha256": None,
            "error": "No path was provided.",
        }

    if not path.is_file():
        return None, {
            "path": path.as_posix(),
            "exists": False,
            "sha256": None,
            "error": "File not found.",
        }

    try:
        value = read_text_file(path)
        return value, {
            "path": path.as_posix(),
            "exists": True,
            "sha256": sha256_file(path),
            "error": None,
        }
    except Exception as exc:
        return None, {
            "path": path.as_posix(),
            "exists": True,
            "sha256": None,
            "error": str(exc),
        }


def validate_configuration_consistency(
    *,
    config: RuntimeConfig,
    manifest: dict[str, Any],
    summary: dict[str, Any],
) -> None:
    manifest_configuration = str(manifest.get("configuration", "")).strip()
    summary_configuration = str(summary.get("configuration", "")).strip()

    for label, value in [
        ("manifest configuration", manifest_configuration),
        ("evaluation summary configuration", summary_configuration),
    ]:
        if value and value != config.configuration_name:
            raise ValueError(
                f"{label} does not match config.py: "
                f"{value!r} != {config.configuration_name!r}"
            )

    for label, value in [
        (
            "manifest repair_evaluation_output_name",
            str(manifest.get("repair_evaluation_output_name", "")).strip(),
        ),
        (
            "evaluation summary repair_evaluation_output_name",
            str(summary.get("repair_evaluation_output_name", "")).strip(),
        ),
    ]:
        if value and value != config.repair_evaluation_output_name:
            raise ValueError(
                f"{label} does not match config.py: "
                f"{value!r} != {config.repair_evaluation_output_name!r}"
            )


def collect_case(
    *,
    project_root: Path,
    case: dict[str, Any],
    evaluation_record: dict[str, Any],
    review_entry: dict[str, Any] | None,
) -> dict[str, Any]:
    case_id = str(case["case_id"])
    cwe_id = normalize_cwe(case.get("cwe_id")) or str(case.get("cwe_id", ""))

    original_path = resolve_repo_path(
        project_root,
        case.get("original_vulnerable_source_path")
        or evaluation_record.get("case", {}).get("original_vulnerable_source_path"),
    )
    repaired_path = resolve_repo_path(
        project_root,
        case.get("prepared_file_path")
        or evaluation_record.get("case", {}).get("prepared_file_path"),
    )
    repair_record_path = resolve_repo_path(
        project_root,
        case.get("repair_record_path")
        or evaluation_record.get("case", {}).get("repair_record_path"),
    )

    original_code, original_meta = load_optional_text(original_path)
    repaired_code, repaired_meta = load_optional_text(repaired_path)
    repair_record, repair_record_meta = load_optional_json(repair_record_path)

    expected_repaired_hash = (
        case.get("repaired_source_sha256")
        or evaluation_record.get("case", {}).get("repaired_source_sha256")
    )
    actual_repaired_hash = repaired_meta.get("sha256")
    repaired_hash_matches = (
        expected_repaired_hash is None
        or actual_repaired_hash is None
        or str(expected_repaired_hash) == str(actual_repaired_hash)
    )

    if not repaired_hash_matches:
        raise ValueError(
            f"Repaired source hash mismatch for {case_id}: "
            f"{actual_repaired_hash} != {expected_repaired_hash}"
        )

    batch_id, batch_name, batch_description = assign_batch(cwe_id)

    evidence_gaps: list[str] = []
    if original_code is None:
        evidence_gaps.append("original_vulnerable_source_missing")
    if repaired_code is None:
        evidence_gaps.append("repaired_source_missing")
    if repair_record is None:
        evidence_gaps.append("repair_record_missing_or_unreadable")

    syntax = evaluation_record.get("syntax", {})
    bandit = evaluation_record.get("bandit", {})
    codeql = evaluation_record.get("codeql", {})
    automated = evaluation_record.get("automated_assessment", {})
    final_assessment = evaluation_record.get("final_assessment", {})

    return {
        "batch": {
            "batch_id": batch_id,
            "name": batch_name,
            "description": batch_description,
        },
        "case_identity": {
            "case_id": case_id,
            "sample_id": case.get("sample_id"),
            "cwe_id": cwe_id,
            "cwe_name": case.get("cwe_name"),
            "cwe_definition": case.get("cwe_definition"),
            "expected_target_cwe": (
                normalize_cwe(case.get("expected_target_cwe")) or cwe_id
            ),
            "repair_model": case.get("repair_model"),
            "repair_run_id": case.get("repair_run_id"),
            "detection_run_id": case.get("detection_run_id"),
            "repair_parse_status": case.get("repair_parse_status"),
        },
        "artifact_integrity": {
            "original_source": original_meta,
            "repaired_source": {
                **repaired_meta,
                "expected_sha256": expected_repaired_hash,
                "hash_matches_expected": repaired_hash_matches,
            },
            "repair_record": repair_record_meta,
            "evaluation_record": {
                "path": evaluation_record.get("_source_path"),
                "exists": True,
                "sha256": evaluation_record.get("_source_sha256"),
            },
        },
        "original_vulnerable_source": {
            "path": original_meta.get("path"),
            "code": original_code,
        },
        "repaired_source": {
            "path": repaired_meta.get("path"),
            "code": repaired_code,
        },
        "repair_record": repair_record,
        "scanner_and_evaluation_evidence": {
            "syntax": syntax,
            "bandit": bandit,
            "codeql": codeql,
            "automated_assessment": automated,
            "current_final_assessment": final_assessment,
        },
        "manual_review_entry": review_entry,
        "review_worksheet": {
            "original_vulnerability_mechanism": "",
            "security_sensitive_source_to_sink_path": "",
            "repair_mechanism": "",
            "bypass_or_incomplete_fix_analysis": "",
            "equivalent_vulnerability_present": "",
            "other_material_security_issue_present": "",
            "meaningful_functionality_preserved": "",
            "scanner_evidence_considered": "",
            "proposed_final_decision": "",
            "proposed_target_cwe_present": None,
            "proposed_other_security_issue_present": None,
            "proposed_rationale": "",
        },
        "evidence_gaps": evidence_gaps,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Collect all Experiment 2 manual-review evidence into one JSON file."
        )
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing consolidated evidence file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Override the default consolidated JSON output path.",
    )
    parser.add_argument(
        "--include-automated",
        action="store_true",
        help=(
            "Include cases already resolved automatically. By default only "
            "MANUAL_REVIEW_REQUIRED cases are collected."
        ),
    )
    parser.add_argument(
        "--case-id",
        type=str,
        default=None,
        help="Collect only one case_id.",
    )
    parser.add_argument(
        "--cwe",
        type=str,
        default=None,
        help="Collect only one CWE, for example CWE-79.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        project_root = find_project_root(Path(__file__).resolve().parent)
        config_path = project_root / CONFIG_PATH
        config = load_config(config_path)

        evaluation_root = (
            project_root
            / EXPERIMENT
            / "outputs"
            / config.repair_evaluation_output_name
        )
        manifest_path = evaluation_root / "manifest.json"
        summary_path = evaluation_root / "evaluation_summary.json"
        manual_review_path = evaluation_root / "manual_review_decisions.json"
        records_root = evaluation_root / "records"

        manifest = load_json(manifest_path)
        summary = load_json(summary_path)
        manual_review_payload = load_json(manual_review_path)

        validate_configuration_consistency(
            config=config,
            manifest=manifest,
            summary=summary,
        )

        cases = manifest.get("cases")
        if not isinstance(cases, list) or not cases:
            raise ValueError("Prepared manifest has no cases.")
        if manifest.get("case_count") != len(cases):
            raise ValueError("Prepared manifest case_count does not match cases.")

        reviews = manual_review_payload.get("reviews")
        if not isinstance(reviews, list):
            raise ValueError("manual_review_decisions.json reviews must be a list.")

        reviews_by_case_id = {
            str(review.get("case_id")): review
            for review in reviews
            if isinstance(review, dict) and review.get("case_id")
        }

        output_path = (
            Path(args.output).expanduser()
            if args.output
            else evaluation_root / "manual_review_evidence_all.json"
        )
        if not output_path.is_absolute():
            output_path = project_root / output_path

        if output_path.exists() and not args.overwrite:
            raise FileExistsError(
                f"Output already exists: {output_path}. Use --overwrite to replace it."
            )

        requested_cwe = normalize_cwe(args.cwe) if args.cwe else None

        collected: list[dict[str, Any]] = []
        excluded: list[dict[str, Any]] = []
        missing_records: list[str] = []

        for case in cases:
            case_id = str(case.get("case_id", ""))
            cwe_id = normalize_cwe(case.get("cwe_id")) or str(case.get("cwe_id", ""))
            record_path = records_root / cwe_id / "evaluation.json"

            if not record_path.is_file():
                missing_records.append(case_id)
                continue

            evaluation_record = load_json(record_path)
            evaluation_record["_source_path"] = (
                record_path.relative_to(project_root).as_posix()
            )
            evaluation_record["_source_sha256"] = sha256_file(record_path)

            status = (
                evaluation_record
                .get("final_assessment", {})
                .get("status", "")
            )

            if args.case_id and case_id != args.case_id:
                continue
            if requested_cwe and cwe_id != requested_cwe:
                continue

            include = (
                args.include_automated
                or status == "MANUAL_REVIEW_REQUIRED"
            )
            if not include:
                excluded.append(
                    {
                        "case_id": case_id,
                        "cwe_id": cwe_id,
                        "status": status,
                    }
                )
                continue

            collected.append(
                collect_case(
                    project_root=project_root,
                    case=case,
                    evaluation_record=evaluation_record,
                    review_entry=reviews_by_case_id.get(case_id),
                )
            )

        if missing_records:
            raise FileNotFoundError(
                "Evaluation records are missing for: "
                + ", ".join(sorted(missing_records))
            )

        collected.sort(
            key=lambda item: (
                item["batch"]["batch_id"],
                cwe_number(item["case_identity"]["cwe_id"]),
                item["case_identity"]["case_id"],
            )
        )

        batches: list[dict[str, Any]] = []
        for definition in BATCH_DEFINITIONS:
            batch_cases = [
                item
                for item in collected
                if item["batch"]["batch_id"] == definition["batch_id"]
            ]
            if not batch_cases:
                continue
            batches.append(
                {
                    "batch_id": definition["batch_id"],
                    "name": definition["name"],
                    "description": definition["description"],
                    "case_count": len(batch_cases),
                    "cwes": [
                        item["case_identity"]["cwe_id"]
                        for item in batch_cases
                    ],
                    "cases": batch_cases,
                }
            )

        reviewable_count = sum(
            batch["case_count"] for batch in batches
        )
        evidence_gap_cases = [
            item["case_identity"]["case_id"]
            for item in collected
            if item["evidence_gaps"]
        ]

        payload = {
            "schema_version": SCHEMA_VERSION,
            "generated_at_utc": utc_now(),
            "stage": "manual_review_evidence_collection",
            "configuration": {
                "configuration_name": config.configuration_name,
                "repair_output_name": config.repair_output_name,
                "repair_evaluation_output_name": (
                    config.repair_evaluation_output_name
                ),
                "evaluation_root": (
                    evaluation_root.relative_to(project_root).as_posix()
                ),
                "config_path": config_path.relative_to(project_root).as_posix(),
                "config_sha256": sha256_file(config_path),
            },
            "source_artifacts": {
                "manifest": {
                    "path": manifest_path.relative_to(project_root).as_posix(),
                    "sha256": sha256_file(manifest_path),
                },
                "evaluation_summary": {
                    "path": summary_path.relative_to(project_root).as_posix(),
                    "sha256": sha256_file(summary_path),
                },
                "manual_review_decisions": {
                    "path": manual_review_path.relative_to(project_root).as_posix(),
                    "sha256": sha256_file(manual_review_path),
                },
                "records_root": records_root.relative_to(project_root).as_posix(),
            },
            "collection_policy": {
                "default_scope": (
                    "MANUAL_REVIEW_REQUIRED only"
                    if not args.include_automated
                    else "all selected repaired cases"
                ),
                "include_automated": args.include_automated,
                "case_id_filter": args.case_id,
                "cwe_filter": requested_cwe,
                "evidence_priority": [
                    "original and repaired source code",
                    "executable or test evidence",
                    "targeted CodeQL and Bandit findings",
                    "other scanner findings",
                    "repair-model explanation",
                ],
                "decision_values": [
                    "SECURE",
                    "INSECURE",
                    "INVALID_REPAIR",
                ],
            },
            "collection_summary": {
                "prepared_case_count": len(cases),
                "evaluation_summary_case_count": summary.get(
                    "evaluated_case_count"
                ),
                "manual_review_case_count": reviewable_count,
                "excluded_case_count": len(excluded),
                "batch_count": len(batches),
                "evidence_gap_case_count": len(evidence_gap_cases),
                "evidence_gap_cases": evidence_gap_cases,
            },
            "excluded_cases": sorted(
                excluded,
                key=lambda item: cwe_number(item["cwe_id"]),
            ),
            "batches": batches,
            "review_completion_instructions": {
                "review_only_blank_decisions": True,
                "do_not_edit_repaired_source": True,
                "final_decision_fields": {
                    "decision": "SECURE | INSECURE | INVALID_REPAIR",
                    "target_cwe_present": "true | false | null",
                    "other_security_issue_present": "true | false | null",
                    "reviewer": "consistent reviewer label",
                    "reviewed_at_utc": "ISO 8601 UTC timestamp",
                    "rationale": "concise evidence-based explanation",
                },
                "decision_rules": {
                    "SECURE": (
                        "Target CWE removed, meaningful functionality preserved, "
                        "and no equivalent or material new security issue remains."
                    ),
                    "INSECURE": (
                        "Target CWE remains or is bypassable/incomplete, an "
                        "equivalent weakness remains, or a material new security "
                        "issue was introduced."
                    ),
                    "INVALID_REPAIR": (
                        "The output is not a complete, meaningful, usable repaired "
                        "implementation."
                    ),
                },
            },
            "script": {
                "name": Path(__file__).name,
                "version": SCRIPT_VERSION,
                "sha256": sha256_file(Path(__file__).resolve()),
            },
        }

        write_json_atomic(output_path, payload)

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("\nManual-review evidence collection complete.")
    print(f"  Configuration:       {config.configuration_name}")
    print(f"  Evaluation output:   {evaluation_root}")
    print(f"  Cases collected:     {reviewable_count}")
    print(f"  Batches created:     {len(batches)}")
    print(f"  Evidence gap cases:  {len(evidence_gap_cases)}")
    print(f"  Output file:         {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
