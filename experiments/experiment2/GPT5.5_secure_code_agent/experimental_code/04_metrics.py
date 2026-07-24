#!/usr/bin/env python3
"""
04_metrics.py

Aggregate Experiment 2 detection, GPT-5.5 repair, repair-evaluation, and
manual-review outputs into final auditable metrics.

The script preserves the reproduced detection workflow and finalizes repair
outcomes by combining:

1. Automated repair-evaluation records.
2. Completed manual-review decisions for cases whose automated status is
   MANUAL_REVIEW_REQUIRED.

Only final status SECURE counts as a successful repair.
INSECURE and INVALID_REPAIR count as unsuccessful outcomes.

Expected experiment layout:

experiments/experiment2/
├── outputs/
│   ├── detection/
│   ├── repair_gpt55/
│   │   └── records/
│   ├── repair_evaluation_gpt55/
│   │   ├── records/
│   │   ├── evaluation_summary.json
│   │   └── manual_review_decisions.json
│   └── metrics_gpt55/
└── scripts/
    ├── config.py
    └── 04_metrics.py
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "1.1"

FINAL_REPAIR_STATUSES = {
    "SECURE",
    "INSECURE",
    "INVALID_REPAIR",
}

EVALUATION_STATUSES = FINAL_REPAIR_STATUSES | {
    "MANUAL_REVIEW_REQUIRED",
}

EXPECTED_DETECTION_SAMPLE_COUNT = 138
EXPECTED_VULNERABLE_SAMPLE_COUNT = 69
EXPECTED_SAFE_SAMPLE_COUNT = 69
EXPECTED_REPAIR_ATTEMPT_COUNT = 56
EXPECTED_MANUAL_REVIEW_COUNT = 51
EXPECTED_AUTOMATED_FINAL_COUNT = 5

EXPECTED_DETECTION_CONFUSION_MATRIX = {
    "true_positive": 56,
    "true_negative": 59,
    "false_positive": 10,
    "false_negative": 13,
}

EXPECTED_FINAL_REPAIR_STATUS_COUNTS = {
    "SECURE": 46,
    "INSECURE": 9,
    "INVALID_REPAIR": 1,
}


class MetricsError(RuntimeError):
    """Raised when experiment outputs are missing, malformed, or inconsistent."""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise MetricsError(f"Required file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise MetricsError(
            f"Invalid JSON in {path}: line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        ) from exc


def write_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def nested_get(data: Any, path: Iterable[str]) -> Any:
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def first_present(
    data: dict[str, Any],
    candidates: Iterable[tuple[str, ...]],
) -> Any:
    for candidate in candidates:
        value = nested_get(data, candidate)
        if value is not None:
            return value
    return None


def parse_bool(value: Any, *, field_name: str, source: Path) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and value in (0, 1):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "vulnerable"}:
            return True
        if normalized in {"false", "0", "no", "safe", "invulnerable"}:
            return False
    raise MetricsError(
        f"Could not parse {field_name} as boolean in {source}: {value!r}"
    )


def safe_divide(
    numerator: int | float,
    denominator: int | float,
) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def rounded(value: float | None, digits: int = 6) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def percentage(value: float | None) -> float | None:
    if value is None:
        return None
    return round(value * 100.0, 4)


def collect_distinct(values: Iterable[Any]) -> list[Any]:
    return sorted({value for value in values if value not in (None, "")})


def load_configuration(experiment_root: Path) -> dict[str, str]:
    """
    Load output names and model identifiers from scripts/config.py when present.

    The function intentionally falls back to the frozen GPT-5.5 configuration
    values so the metrics script remains runnable if config.py exposes different
    implementation details or cannot be imported in isolation.
    """
    defaults = {
        "configuration_name": "secure_code_agent_baseline",
        "detection_model": "gpt-4-0613",
        "repair_model": "gpt-5.5",
        "repair_output_name": "repair_gpt55",
        "repair_evaluation_output_name": "repair_evaluation_gpt55",
        "metrics_output_name": "metrics_gpt55",
    }

    config_path = experiment_root / "scripts" / "config.py"
    if not config_path.is_file():
        return {**defaults, "config_path": config_path.as_posix(), "config_loaded": "false"}

    try:
        spec = importlib.util.spec_from_file_location(
            "experiment2_metrics_config",
            config_path,
        )
        if spec is None or spec.loader is None:
            raise ImportError("Could not create import specification.")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as exc:
        raise MetricsError(
            f"Could not import Experiment 2 configuration from {config_path}: {exc}"
        ) from exc

    mappings = {
        "configuration_name": "CONFIGURATION_NAME",
        "detection_model": "DETECTION_MODEL",
        "repair_model": "REPAIR_MODEL",
        "repair_output_name": "REPAIR_OUTPUT_NAME",
        "repair_evaluation_output_name": "REPAIR_EVALUATION_OUTPUT_NAME",
        "metrics_output_name": "METRICS_OUTPUT_NAME",
    }

    loaded = dict(defaults)
    for output_key, attribute_name in mappings.items():
        value = getattr(module, attribute_name, None)
        if value not in (None, ""):
            loaded[output_key] = str(value)

    loaded["config_path"] = config_path.as_posix()
    loaded["config_loaded"] = "true"
    return loaded


def discover_detection_records(
    detection_dir: Path,
) -> list[dict[str, Any]]:
    if not detection_dir.is_dir():
        raise MetricsError(
            f"Detection output directory not found: {detection_dir}"
        )

    records: list[dict[str, Any]] = []
    seen_sample_ids: set[str] = set()

    for path in sorted(detection_dir.rglob("*.json")):
        data = read_json(path)
        if not isinstance(data, dict):
            continue

        sample_id = first_present(
            data,
            [
                ("sample", "sample_id"),
                ("case", "sample_id"),
                ("sample_id",),
            ],
        )
        cwe_id = first_present(
            data,
            [
                ("sample", "cwe_id"),
                ("case", "cwe_id"),
                ("cwe_id",),
            ],
        )
        ground_truth_raw = first_present(
            data,
            [
                ("sample", "ground_truth_vulnerable"),
                ("ground_truth_vulnerable",),
                ("ground_truth", "vulnerable"),
            ],
        )
        prediction_raw = first_present(
            data,
            [
                ("prediction_vulnerable",),
                ("prediction", "prediction_vulnerable"),
                ("result", "prediction_vulnerable"),
                ("output", "prediction_vulnerable"),
                ("response", "prediction_vulnerable"),
            ],
        )

        # Skip summaries, manifests, and unrelated JSON files.
        if (
            sample_id is None
            or cwe_id is None
            or ground_truth_raw is None
            or prediction_raw is None
        ):
            continue

        sample_id = str(sample_id)
        cwe_id = str(cwe_id)

        if sample_id in seen_sample_ids:
            raise MetricsError(
                f"Duplicate detection sample_id {sample_id!r}; "
                f"latest file: {path}"
            )
        seen_sample_ids.add(sample_id)

        records.append(
            {
                "source_path": path.as_posix(),
                "sample_id": sample_id,
                "cwe_id": cwe_id,
                "ground_truth_vulnerable": parse_bool(
                    ground_truth_raw,
                    field_name="ground_truth_vulnerable",
                    source=path,
                ),
                "prediction_vulnerable": parse_bool(
                    prediction_raw,
                    field_name="prediction_vulnerable",
                    source=path,
                ),
                "model_id": first_present(
                    data,
                    [
                        ("model", "model_id"),
                        ("model_id",),
                        ("configuration", "model_id"),
                    ],
                ),
                "run_id": first_present(
                    data,
                    [
                        ("run_id",),
                        ("metadata", "run_id"),
                    ],
                ),
            }
        )

    if not records:
        raise MetricsError(
            f"No usable detection records were found under {detection_dir}."
        )

    return records


def discover_repair_records(
    repair_records_dir: Path,
) -> list[dict[str, Any]]:
    if not repair_records_dir.is_dir():
        raise MetricsError(
            f"Repair records directory not found: {repair_records_dir}"
        )

    records: list[dict[str, Any]] = []
    seen_sample_ids: set[str] = set()

    for path in sorted(repair_records_dir.rglob("*.json")):
        data = read_json(path)
        if not isinstance(data, dict):
            continue

        sample_id = first_present(
            data,
            [
                ("sample", "sample_id"),
                ("case", "sample_id"),
                ("sample_id",),
            ],
        )
        cwe_id = first_present(
            data,
            [
                ("sample", "cwe_id"),
                ("case", "cwe_id"),
                ("cwe_id",),
            ],
        )

        if sample_id is None or cwe_id is None:
            continue

        sample_id = str(sample_id)
        cwe_id = str(cwe_id)

        if sample_id in seen_sample_ids:
            raise MetricsError(
                f"Duplicate repair record for sample_id "
                f"{sample_id!r}: {path}"
            )
        seen_sample_ids.add(sample_id)

        records.append(
            {
                "source_path": path.as_posix(),
                "sample_id": sample_id,
                "cwe_id": cwe_id,
                "model_id": first_present(
                    data,
                    [
                        ("model", "model_id"),
                        ("repair_model",),
                        ("model_id",),
                    ],
                ),
                "run_id": first_present(
                    data,
                    [
                        ("run_id",),
                        ("metadata", "run_id"),
                    ],
                ),
                "status": first_present(
                    data,
                    [
                        ("status",),
                        ("execution", "status"),
                    ],
                ),
            }
        )

    if not records:
        raise MetricsError(
            f"No usable repair records were found under {repair_records_dir}."
        )

    return records


def discover_repair_evaluation_records(
    evaluation_records_dir: Path,
) -> list[dict[str, Any]]:
    if not evaluation_records_dir.is_dir():
        raise MetricsError(
            "Repair-evaluation records directory not found: "
            f"{evaluation_records_dir}"
        )

    records: list[dict[str, Any]] = []
    seen_case_ids: set[str] = set()
    seen_sample_ids: set[str] = set()

    for path in sorted(evaluation_records_dir.rglob("*.json")):
        data = read_json(path)
        if not isinstance(data, dict):
            continue

        case_id = first_present(
            data,
            [
                ("case", "case_id"),
                ("case_id",),
            ],
        )
        sample_id = first_present(
            data,
            [
                ("case", "sample_id"),
                ("sample_id",),
            ],
        )
        cwe_id = first_present(
            data,
            [
                ("case", "cwe_id"),
                ("cwe_id",),
            ],
        )
        automated_status = first_present(
            data,
            [
                ("final_assessment", "status"),
                ("final_status",),
                ("status",),
            ],
        )

        if (
            case_id is None
            or sample_id is None
            or cwe_id is None
            or automated_status is None
        ):
            continue

        case_id = str(case_id)
        sample_id = str(sample_id)
        cwe_id = str(cwe_id)
        automated_status = str(automated_status).upper()

        if automated_status not in EVALUATION_STATUSES:
            raise MetricsError(
                f"Unexpected repair-evaluation status "
                f"{automated_status!r} in {path}"
            )
        if case_id in seen_case_ids:
            raise MetricsError(
                f"Duplicate evaluation case_id {case_id!r}: {path}"
            )
        if sample_id in seen_sample_ids:
            raise MetricsError(
                f"Duplicate evaluation sample_id {sample_id!r}: {path}"
            )

        seen_case_ids.add(case_id)
        seen_sample_ids.add(sample_id)

        records.append(
            {
                "source_path": path.as_posix(),
                "case_id": case_id,
                "sample_id": sample_id,
                "cwe_id": cwe_id,
                "automated_status": automated_status,
                "automated_decision_source": first_present(
                    data,
                    [
                        ("final_assessment", "decision_source"),
                        ("decision_source",),
                    ],
                ),
                "run_id": first_present(
                    data,
                    [
                        ("run_id",),
                        ("metadata", "run_id"),
                    ],
                ),
            }
        )

    if not records:
        raise MetricsError(
            "No usable repair-evaluation records were found under "
            f"{evaluation_records_dir}."
        )

    return records


def discover_manual_review_decisions(
    decisions_path: Path,
) -> list[dict[str, Any]]:
    payload = read_json(decisions_path)

    if not isinstance(payload, dict):
        raise MetricsError(
            f"Manual-review decisions file must contain a JSON object: "
            f"{decisions_path}"
        )

    reviews = payload.get("reviews")
    if not isinstance(reviews, list):
        raise MetricsError(
            f"Manual-review decisions file must contain a reviews list: "
            f"{decisions_path}"
        )

    results: list[dict[str, Any]] = []
    seen_case_ids: set[str] = set()

    for index, review in enumerate(reviews):
        if not isinstance(review, dict):
            raise MetricsError(
                f"Manual-review entry {index} is not an object in "
                f"{decisions_path}"
            )

        case_id = review.get("case_id")
        sample_id = review.get("sample_id")
        cwe_id = review.get("cwe_id")
        decision_raw = review.get("decision", "")

        if case_id in (None, ""):
            raise MetricsError(
                f"Manual-review entry {index} is missing case_id."
            )
        if sample_id in (None, ""):
            raise MetricsError(
                f"Manual-review entry {case_id!r} is missing sample_id."
            )
        if cwe_id in (None, ""):
            raise MetricsError(
                f"Manual-review entry {case_id!r} is missing cwe_id."
            )

        case_id = str(case_id)
        sample_id = str(sample_id)
        cwe_id = str(cwe_id)

        if case_id in seen_case_ids:
            raise MetricsError(
                f"Duplicate manual-review case_id {case_id!r} in "
                f"{decisions_path}"
            )
        seen_case_ids.add(case_id)

        decision = (
            str(decision_raw).strip().upper()
            if decision_raw not in (None, "")
            else None
        )

        if decision is not None and decision not in FINAL_REPAIR_STATUSES:
            raise MetricsError(
                f"Unexpected manual-review decision {decision!r} for "
                f"{case_id!r}."
            )

        results.append(
            {
                "source_path": decisions_path.as_posix(),
                "case_id": case_id,
                "sample_id": sample_id,
                "cwe_id": cwe_id,
                "decision": decision,
                "target_cwe_present": review.get("target_cwe_present"),
                "other_security_issue_present": review.get(
                    "other_security_issue_present"
                ),
                "reviewer": review.get("reviewer"),
                "reviewed_at_utc": review.get("reviewed_at_utc"),
                "rationale": review.get("rationale"),
            }
        )

    if not results:
        raise MetricsError(
            f"No manual-review entries were found in {decisions_path}."
        )

    return results


def finalize_repair_evaluations(
    evaluation_records: list[dict[str, Any]],
    manual_decisions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    evaluation_by_case = {
        record["case_id"]: record for record in evaluation_records
    }
    decision_by_case = {
        record["case_id"]: record for record in manual_decisions
    }

    unknown_decision_cases = sorted(
        set(decision_by_case) - set(evaluation_by_case)
    )
    if unknown_decision_cases:
        raise MetricsError(
            "Manual-review decisions reference cases that do not exist in "
            f"repair-evaluation records: {unknown_decision_cases}"
        )

    finalized: list[dict[str, Any]] = []
    completed_manual_decisions_used: set[str] = set()
    blank_automated_cases: set[str] = set()
    automated_final_cases: set[str] = set()

    for evaluation in evaluation_records:
        case_id = evaluation["case_id"]
        manual = decision_by_case.get(case_id)

        if manual is not None:
            mismatches: list[str] = []
            if manual["sample_id"] != evaluation["sample_id"]:
                mismatches.append(
                    f"sample_id manual={manual['sample_id']!r} "
                    f"evaluation={evaluation['sample_id']!r}"
                )
            if manual["cwe_id"] != evaluation["cwe_id"]:
                mismatches.append(
                    f"cwe_id manual={manual['cwe_id']!r} "
                    f"evaluation={evaluation['cwe_id']!r}"
                )
            if mismatches:
                raise MetricsError(
                    f"Manual-review identity mismatch for {case_id!r}: "
                    + "; ".join(mismatches)
                )

        automated_status = evaluation["automated_status"]

        if automated_status == "MANUAL_REVIEW_REQUIRED":
            if manual is None:
                raise MetricsError(
                    f"Case {case_id!r} requires manual review but has no "
                    "entry in manual_review_decisions.json."
                )
            if manual["decision"] is None:
                raise MetricsError(
                    f"Case {case_id!r} still requires manual review but its "
                    "manual decision is blank."
                )

            final_status = manual["decision"]
            decision_source = "manual_review"
            completed_manual_decisions_used.add(case_id)
            reviewer = manual["reviewer"]
            reviewed_at_utc = manual["reviewed_at_utc"]
            rationale = manual["rationale"]
            target_cwe_present = manual["target_cwe_present"]
            other_security_issue_present = manual[
                "other_security_issue_present"
            ]
        else:
            final_status = automated_status
            decision_source = (
                evaluation["automated_decision_source"]
                or "automated_evaluation"
            )
            automated_final_cases.add(case_id)

            if manual is not None and manual["decision"] is not None:
                raise MetricsError(
                    f"Case {case_id!r} already has automated final status "
                    f"{automated_status}, but the manual-review file also "
                    f"contains completed decision {manual['decision']}."
                )

            if manual is not None and manual["decision"] is None:
                blank_automated_cases.add(case_id)

            reviewer = None
            reviewed_at_utc = None
            rationale = None
            target_cwe_present = None
            other_security_issue_present = None

        finalized.append(
            {
                **evaluation,
                "final_status": final_status,
                "decision_source": decision_source,
                "manual_review_applied": (
                    automated_status == "MANUAL_REVIEW_REQUIRED"
                ),
                "reviewer": reviewer,
                "reviewed_at_utc": reviewed_at_utc,
                "rationale": rationale,
                "target_cwe_present": target_cwe_present,
                "other_security_issue_present": (
                    other_security_issue_present
                ),
            }
        )

    unused_completed_decisions = sorted(
        {
            record["case_id"]
            for record in manual_decisions
            if record["decision"] is not None
        }
        - completed_manual_decisions_used
    )
    if unused_completed_decisions:
        raise MetricsError(
            "Completed manual decisions were not used to finalize a "
            f"MANUAL_REVIEW_REQUIRED case: {unused_completed_decisions}"
        )

    unresolved = [
        record["case_id"]
        for record in finalized
        if record["final_status"] not in FINAL_REPAIR_STATUSES
    ]
    if unresolved:
        raise MetricsError(
            f"Unresolved final repair statuses remain: {unresolved}"
        )

    provenance = {
        "evaluation_case_count": len(evaluation_records),
        "manual_review_entry_count": len(manual_decisions),
        "manual_review_required_count": sum(
            record["automated_status"] == "MANUAL_REVIEW_REQUIRED"
            for record in evaluation_records
        ),
        "completed_manual_decisions_used": len(
            completed_manual_decisions_used
        ),
        "automated_final_cases_retained": len(automated_final_cases),
        "blank_manual_entries_for_automated_cases": len(
            blank_automated_cases
        ),
        "unresolved_case_count": len(unresolved),
        "manual_review_case_ids": sorted(completed_manual_decisions_used),
        "automated_final_case_ids": sorted(automated_final_cases),
        "blank_automated_case_ids": sorted(blank_automated_cases),
    }

    return finalized, provenance


def calculate_detection_metrics(
    records: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    tp = tn = fp = fn = 0

    by_cwe: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "vulnerable_sample_ids": [],
            "safe_sample_ids": [],
            "true_positive_sample_ids": [],
            "false_negative_sample_ids": [],
            "true_negative_sample_ids": [],
            "false_positive_sample_ids": [],
        }
    )

    for record in records:
        truth = record["ground_truth_vulnerable"]
        prediction = record["prediction_vulnerable"]
        cwe_id = record["cwe_id"]
        sample_id = record["sample_id"]

        if truth:
            by_cwe[cwe_id]["vulnerable_sample_ids"].append(sample_id)
            if prediction:
                tp += 1
                by_cwe[cwe_id]["true_positive_sample_ids"].append(
                    sample_id
                )
            else:
                fn += 1
                by_cwe[cwe_id]["false_negative_sample_ids"].append(
                    sample_id
                )
        else:
            by_cwe[cwe_id]["safe_sample_ids"].append(sample_id)
            if prediction:
                fp += 1
                by_cwe[cwe_id]["false_positive_sample_ids"].append(
                    sample_id
                )
            else:
                tn += 1
                by_cwe[cwe_id]["true_negative_sample_ids"].append(
                    sample_id
                )

    total = tp + tn + fp + fn
    vulnerable_count = tp + fn
    safe_count = tn + fp

    accuracy = safe_divide(tp + tn, total)
    precision = safe_divide(tp, tp + fp)
    recall = safe_divide(tp, tp + fn)
    f1 = (
        None
        if precision is None
        or recall is None
        or precision + recall == 0
        else 2 * precision * recall / (precision + recall)
    )

    vulnerable_cwes = {
        record["cwe_id"]
        for record in records
        if record["ground_truth_vulnerable"]
    }
    detected_vulnerable_cwes = {
        record["cwe_id"]
        for record in records
        if (
            record["ground_truth_vulnerable"]
            and record["prediction_vulnerable"]
        )
    }

    detection_coverage = safe_divide(
        len(detected_vulnerable_cwes),
        len(vulnerable_cwes),
    )

    metrics = {
        "sample_counts": {
            "total": total,
            "vulnerable": vulnerable_count,
            "safe": safe_count,
        },
        "confusion_matrix": {
            "true_positive": tp,
            "true_negative": tn,
            "false_positive": fp,
            "false_negative": fn,
        },
        "metrics": {
            "accuracy": rounded(accuracy),
            "accuracy_percent": percentage(accuracy),
            "precision": rounded(precision),
            "precision_percent": percentage(precision),
            "recall": rounded(recall),
            "recall_percent": percentage(recall),
            "f1_score": rounded(f1),
            "f1_score_percent": percentage(f1),
            "detection_coverage": rounded(detection_coverage),
            "detection_coverage_percent": percentage(
                detection_coverage
            ),
        },
        "coverage_counts": {
            "detected_vulnerable_cwes": len(
                detected_vulnerable_cwes
            ),
            "total_vulnerable_cwes": len(vulnerable_cwes),
        },
        "definitions": {
            "positive_class": (
                "The benchmark sample contains its predefined target CWE."
            ),
            "detection_coverage": (
                "Unique target CWEs correctly detected in vulnerable "
                "samples divided by all unique target CWEs represented "
                "by vulnerable samples."
            ),
        },
    }

    return metrics, by_cwe


def calculate_repair_metrics(
    detection_records: list[dict[str, Any]],
    repair_records: list[dict[str, Any]],
    finalized_evaluations: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    vulnerable_detection_records = [
        record
        for record in detection_records
        if record["ground_truth_vulnerable"]
    ]
    true_positive_detection_records = [
        record
        for record in vulnerable_detection_records
        if record["prediction_vulnerable"]
    ]

    vulnerable_sample_ids = {
        record["sample_id"] for record in vulnerable_detection_records
    }
    true_positive_sample_ids = {
        record["sample_id"] for record in true_positive_detection_records
    }
    vulnerable_cwes = {
        record["cwe_id"] for record in vulnerable_detection_records
    }

    repair_by_sample = {
        record["sample_id"]: record for record in repair_records
    }
    evaluation_by_sample = {
        record["sample_id"]: record
        for record in finalized_evaluations
    }

    unknown_repair_samples = sorted(
        set(repair_by_sample) - vulnerable_sample_ids
    )
    if unknown_repair_samples:
        raise MetricsError(
            "Repair records exist for samples that are not vulnerable "
            f"detection inputs: {unknown_repair_samples}"
        )

    non_true_positive_repairs = sorted(
        set(repair_by_sample) - true_positive_sample_ids
    )
    if non_true_positive_repairs:
        raise MetricsError(
            "Repair records exist for vulnerable samples not detected as "
            f"true positives: {non_true_positive_repairs}"
        )

    missing_repairs_for_true_positives = sorted(
        true_positive_sample_ids - set(repair_by_sample)
    )
    if missing_repairs_for_true_positives:
        raise MetricsError(
            "Detected vulnerable samples are missing repair records: "
            f"{missing_repairs_for_true_positives}"
        )

    unknown_evaluation_samples = sorted(
        set(evaluation_by_sample) - set(repair_by_sample)
    )
    if unknown_evaluation_samples:
        raise MetricsError(
            "Repair-evaluation records exist without matching repair "
            f"records: {unknown_evaluation_samples}"
        )

    missing_evaluations = sorted(
        set(repair_by_sample) - set(evaluation_by_sample)
    )
    if missing_evaluations:
        raise MetricsError(
            "Repair records are missing finalized evaluation records for: "
            f"{missing_evaluations}"
        )

    for sample_id, repair in repair_by_sample.items():
        evaluation = evaluation_by_sample[sample_id]
        if repair["cwe_id"] != evaluation["cwe_id"]:
            raise MetricsError(
                f"CWE mismatch for repair/evaluation sample "
                f"{sample_id!r}: repair={repair['cwe_id']!r}, "
                f"evaluation={evaluation['cwe_id']!r}"
            )

    status_counts = Counter(
        record["final_status"]
        for record in finalized_evaluations
    )

    secure_count = status_counts.get("SECURE", 0)
    insecure_count = status_counts.get("INSECURE", 0)
    invalid_count = status_counts.get("INVALID_REPAIR", 0)

    repair_attempt_count = len(repair_records)
    evaluated_repair_count = len(finalized_evaluations)
    vulnerable_input_count = len(vulnerable_detection_records)
    skipped_due_to_detection_count = (
        vulnerable_input_count - repair_attempt_count
    )

    repair_success_rate = safe_divide(
        secure_count,
        repair_attempt_count,
    )
    evaluated_repair_success_rate = safe_divide(
        secure_count,
        evaluated_repair_count,
    )
    final_secure_output_rate = safe_divide(
        secure_count,
        vulnerable_input_count,
    )

    attempted_cwes = {
        record["cwe_id"] for record in repair_records
    }
    secure_cwes = {
        record["cwe_id"]
        for record in finalized_evaluations
        if record["final_status"] == "SECURE"
    }

    repair_attempt_coverage = safe_divide(
        len(attempted_cwes),
        len(vulnerable_cwes),
    )
    successful_cwe_coverage = safe_divide(
        len(secure_cwes),
        len(vulnerable_cwes),
    )

    by_cwe: dict[str, dict[str, Any]] = defaultdict(dict)

    for cwe_id in vulnerable_cwes:
        by_cwe[cwe_id].update(
            {
                "repair_attempted": False,
                "repair_sample_id": None,
                "final_repair_status": None,
                "final_secure_output": False,
            }
        )

    for repair in repair_records:
        by_cwe[repair["cwe_id"]].update(
            {
                "repair_attempted": True,
                "repair_sample_id": repair["sample_id"],
                "repair_model_id": repair["model_id"],
                "repair_run_id": repair["run_id"],
            }
        )

    for evaluation in finalized_evaluations:
        by_cwe[evaluation["cwe_id"]].update(
            {
                "evaluation_case_id": evaluation["case_id"],
                "evaluation_run_id": evaluation["run_id"],
                "automated_status": evaluation["automated_status"],
                "final_repair_status": evaluation["final_status"],
                "final_secure_output": (
                    evaluation["final_status"] == "SECURE"
                ),
                "decision_source": evaluation["decision_source"],
                "manual_review_applied": evaluation[
                    "manual_review_applied"
                ],
                "reviewer": evaluation["reviewer"],
            }
        )

    metrics = {
        "input_counts": {
            "vulnerable_samples": vulnerable_input_count,
            "target_cwes": len(vulnerable_cwes),
        },
        "pipeline_counts": {
            "repair_attempts": repair_attempt_count,
            "evaluated_repairs": evaluated_repair_count,
            "skipped_due_to_detection_false_negative": (
                skipped_due_to_detection_count
            ),
        },
        "final_status_counts": {
            "SECURE": secure_count,
            "INSECURE": insecure_count,
            "INVALID_REPAIR": invalid_count,
            "MANUAL_REVIEW_REQUIRED": 0,
        },
        "metrics": {
            "repair_success_rate": rounded(repair_success_rate),
            "repair_success_rate_percent": percentage(
                repair_success_rate
            ),
            "evaluated_repair_success_rate": rounded(
                evaluated_repair_success_rate
            ),
            "evaluated_repair_success_rate_percent": percentage(
                evaluated_repair_success_rate
            ),
            "final_secure_output_rate": rounded(
                final_secure_output_rate
            ),
            "final_secure_output_rate_percent": percentage(
                final_secure_output_rate
            ),
            "repair_attempt_coverage": rounded(
                repair_attempt_coverage
            ),
            "repair_attempt_coverage_percent": percentage(
                repair_attempt_coverage
            ),
            "cwe_coverage": rounded(successful_cwe_coverage),
            "cwe_coverage_percent": percentage(
                successful_cwe_coverage
            ),
        },
        "coverage_counts": {
            "attempted_cwes": len(attempted_cwes),
            "successfully_repaired_cwes": len(secure_cwes),
            "total_vulnerable_cwes": len(vulnerable_cwes),
        },
        "definitions": {
            "repair_success_rate": (
                "Final SECURE repairs divided by repair attempts."
            ),
            "evaluated_repair_success_rate": (
                "Final SECURE repairs divided by finalized repair "
                "evaluations."
            ),
            "final_secure_output_rate": (
                "Final SECURE repairs divided by all vulnerable benchmark "
                "inputs, including detector false negatives that never "
                "reached repair."
            ),
            "repair_attempt_coverage": (
                "Unique target CWEs sent to repair divided by all "
                "vulnerable target CWEs represented in the benchmark."
            ),
            "cwe_coverage": (
                "Unique target CWEs with a final SECURE repair divided by "
                "all vulnerable target CWEs represented in the benchmark."
            ),
            "successful_repair_status": (
                "Only final status SECURE is successful."
            ),
        },
    }

    return metrics, by_cwe


def build_per_cwe_results(
    detection_by_cwe: dict[str, dict[str, Any]],
    repair_by_cwe: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    all_cwes = sorted(
        set(detection_by_cwe) | set(repair_by_cwe),
        key=lambda value: (
            int(value.split("-", 1)[1])
            if (
                value.upper().startswith("CWE-")
                and value.split("-", 1)[1].isdigit()
            )
            else math.inf,
            value,
        ),
    )

    results: list[dict[str, Any]] = []

    for cwe_id in all_cwes:
        detection = detection_by_cwe.get(cwe_id, {})
        repair = repair_by_cwe.get(cwe_id, {})

        vulnerable_ids = detection.get(
            "vulnerable_sample_ids",
            [],
        )
        safe_ids = detection.get("safe_sample_ids", [])
        tp_ids = detection.get(
            "true_positive_sample_ids",
            [],
        )
        fn_ids = detection.get(
            "false_negative_sample_ids",
            [],
        )
        tn_ids = detection.get(
            "true_negative_sample_ids",
            [],
        )
        fp_ids = detection.get(
            "false_positive_sample_ids",
            [],
        )

        results.append(
            {
                "cwe_id": cwe_id,
                "vulnerable_sample_ids": vulnerable_ids,
                "safe_sample_ids": safe_ids,
                "detection": {
                    "true_positive_count": len(tp_ids),
                    "false_negative_count": len(fn_ids),
                    "true_negative_count": len(tn_ids),
                    "false_positive_count": len(fp_ids),
                    "vulnerable_detected": bool(tp_ids),
                    "safe_correctly_classified": (
                        bool(safe_ids) and not bool(fp_ids)
                    ),
                },
                "repair": {
                    "attempted": repair.get(
                        "repair_attempted",
                        False,
                    ),
                    "sample_id": repair.get("repair_sample_id"),
                    "automated_status": repair.get(
                        "automated_status"
                    ),
                    "final_status": repair.get(
                        "final_repair_status"
                    ),
                    "final_secure_output": repair.get(
                        "final_secure_output",
                        False,
                    ),
                    "decision_source": repair.get(
                        "decision_source"
                    ),
                    "manual_review_applied": repair.get(
                        "manual_review_applied",
                        False,
                    ),
                    "reviewer": repair.get("reviewer"),
                },
            }
        )

    return results


def write_summary_csv(
    path: Path,
    summary: dict[str, Any],
) -> None:
    rows = [
        (
            "detection.total_samples",
            summary["detection"]["sample_counts"]["total"],
        ),
        (
            "detection.vulnerable_samples",
            summary["detection"]["sample_counts"]["vulnerable"],
        ),
        (
            "detection.safe_samples",
            summary["detection"]["sample_counts"]["safe"],
        ),
        (
            "detection.true_positive",
            summary["detection"]["confusion_matrix"]["true_positive"],
        ),
        (
            "detection.true_negative",
            summary["detection"]["confusion_matrix"]["true_negative"],
        ),
        (
            "detection.false_positive",
            summary["detection"]["confusion_matrix"]["false_positive"],
        ),
        (
            "detection.false_negative",
            summary["detection"]["confusion_matrix"]["false_negative"],
        ),
        (
            "detection.accuracy_percent",
            summary["detection"]["metrics"]["accuracy_percent"],
        ),
        (
            "detection.precision_percent",
            summary["detection"]["metrics"]["precision_percent"],
        ),
        (
            "detection.recall_percent",
            summary["detection"]["metrics"]["recall_percent"],
        ),
        (
            "detection.f1_score_percent",
            summary["detection"]["metrics"]["f1_score_percent"],
        ),
        (
            "detection.detection_coverage_percent",
            summary["detection"]["metrics"][
                "detection_coverage_percent"
            ],
        ),
        (
            "repair.repair_attempts",
            summary["repair"]["pipeline_counts"]["repair_attempts"],
        ),
        (
            "repair.evaluated_repairs",
            summary["repair"]["pipeline_counts"]["evaluated_repairs"],
        ),
        (
            "repair.skipped_due_to_detection_false_negative",
            summary["repair"]["pipeline_counts"][
                "skipped_due_to_detection_false_negative"
            ],
        ),
        (
            "repair.secure",
            summary["repair"]["final_status_counts"]["SECURE"],
        ),
        (
            "repair.insecure",
            summary["repair"]["final_status_counts"]["INSECURE"],
        ),
        (
            "repair.invalid_repair",
            summary["repair"]["final_status_counts"][
                "INVALID_REPAIR"
            ],
        ),
        (
            "repair.repair_success_rate_percent",
            summary["repair"]["metrics"][
                "repair_success_rate_percent"
            ],
        ),
        (
            "repair.evaluated_repair_success_rate_percent",
            summary["repair"]["metrics"][
                "evaluated_repair_success_rate_percent"
            ],
        ),
        (
            "repair.final_secure_output_rate_percent",
            summary["repair"]["metrics"][
                "final_secure_output_rate_percent"
            ],
        ),
        (
            "repair.repair_attempt_coverage_percent",
            summary["repair"]["metrics"][
                "repair_attempt_coverage_percent"
            ],
        ),
        (
            "repair.cwe_coverage_percent",
            summary["repair"]["metrics"]["cwe_coverage_percent"],
        ),
        (
            "manual_review.completed_decisions_used",
            summary["manual_review"][
                "completed_manual_decisions_used"
            ],
        ),
        (
            "manual_review.automated_final_cases_retained",
            summary["manual_review"][
                "automated_final_cases_retained"
            ],
        ),
        (
            "manual_review.unresolved_case_count",
            summary["manual_review"]["unresolved_case_count"],
        ),
    ]

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "value"])
        writer.writerows(rows)


def write_per_cwe_csv(
    path: Path,
    rows: list[dict[str, Any]],
) -> None:
    fieldnames = [
        "cwe_id",
        "vulnerable_sample_ids",
        "safe_sample_ids",
        "true_positive_count",
        "false_negative_count",
        "true_negative_count",
        "false_positive_count",
        "vulnerable_detected",
        "safe_correctly_classified",
        "repair_attempted",
        "repair_sample_id",
        "automated_status",
        "final_repair_status",
        "final_secure_output",
        "decision_source",
        "manual_review_applied",
        "reviewer",
    ]

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow(
                {
                    "cwe_id": row["cwe_id"],
                    "vulnerable_sample_ids": ";".join(
                        row["vulnerable_sample_ids"]
                    ),
                    "safe_sample_ids": ";".join(
                        row["safe_sample_ids"]
                    ),
                    "true_positive_count": row["detection"][
                        "true_positive_count"
                    ],
                    "false_negative_count": row["detection"][
                        "false_negative_count"
                    ],
                    "true_negative_count": row["detection"][
                        "true_negative_count"
                    ],
                    "false_positive_count": row["detection"][
                        "false_positive_count"
                    ],
                    "vulnerable_detected": row["detection"][
                        "vulnerable_detected"
                    ],
                    "safe_correctly_classified": row["detection"][
                        "safe_correctly_classified"
                    ],
                    "repair_attempted": row["repair"]["attempted"],
                    "repair_sample_id": row["repair"]["sample_id"],
                    "automated_status": row["repair"][
                        "automated_status"
                    ],
                    "final_repair_status": row["repair"][
                        "final_status"
                    ],
                    "final_secure_output": row["repair"][
                        "final_secure_output"
                    ],
                    "decision_source": row["repair"][
                        "decision_source"
                    ],
                    "manual_review_applied": row["repair"][
                        "manual_review_applied"
                    ],
                    "reviewer": row["repair"]["reviewer"],
                }
            )


def validate_expected_results(
    detection_metrics: dict[str, Any],
    repair_metrics: dict[str, Any],
    manual_review_provenance: dict[str, Any],
) -> None:
    sample_counts = detection_metrics["sample_counts"]

    expected_sample_counts = {
        "total": EXPECTED_DETECTION_SAMPLE_COUNT,
        "vulnerable": EXPECTED_VULNERABLE_SAMPLE_COUNT,
        "safe": EXPECTED_SAFE_SAMPLE_COUNT,
    }

    if sample_counts != expected_sample_counts:
        raise MetricsError(
            "Detection sample counts do not match the frozen experiment "
            f"expectation.\nExpected: {expected_sample_counts}\n"
            f"Calculated: {sample_counts}"
        )

    confusion = detection_metrics["confusion_matrix"]
    if confusion != EXPECTED_DETECTION_CONFUSION_MATRIX:
        raise MetricsError(
            "Detection confusion matrix does not match the reproduced "
            f"baseline.\nExpected: "
            f"{EXPECTED_DETECTION_CONFUSION_MATRIX}\n"
            f"Calculated: {confusion}"
        )

    pipeline_counts = repair_metrics["pipeline_counts"]
    if (
        pipeline_counts["repair_attempts"]
        != EXPECTED_REPAIR_ATTEMPT_COUNT
    ):
        raise MetricsError(
            "Repair-attempt count does not match the frozen experiment "
            f"expectation: expected={EXPECTED_REPAIR_ATTEMPT_COUNT}, "
            f"calculated={pipeline_counts['repair_attempts']}"
        )

    if (
        pipeline_counts["evaluated_repairs"]
        != EXPECTED_REPAIR_ATTEMPT_COUNT
    ):
        raise MetricsError(
            "Finalized repair-evaluation count does not match repair "
            f"attempt count: repairs={EXPECTED_REPAIR_ATTEMPT_COUNT}, "
            f"evaluations={pipeline_counts['evaluated_repairs']}"
        )

    if (
        manual_review_provenance["completed_manual_decisions_used"]
        != EXPECTED_MANUAL_REVIEW_COUNT
    ):
        raise MetricsError(
            "Completed manual-review count does not match expectation: "
            f"expected={EXPECTED_MANUAL_REVIEW_COUNT}, "
            f"calculated="
            f"{manual_review_provenance['completed_manual_decisions_used']}"
        )

    if (
        manual_review_provenance["automated_final_cases_retained"]
        != EXPECTED_AUTOMATED_FINAL_COUNT
    ):
        raise MetricsError(
            "Automated final-case count does not match expectation: "
            f"expected={EXPECTED_AUTOMATED_FINAL_COUNT}, "
            f"calculated="
            f"{manual_review_provenance['automated_final_cases_retained']}"
        )

    calculated_status_counts = {
        status: repair_metrics["final_status_counts"][status]
        for status in FINAL_REPAIR_STATUSES
    }

    if (
        calculated_status_counts
        != EXPECTED_FINAL_REPAIR_STATUS_COUNTS
    ):
        raise MetricsError(
            "Final repair status counts do not match the completed "
            f"evaluation.\nExpected: "
            f"{EXPECTED_FINAL_REPAIR_STATUS_COUNTS}\n"
            f"Calculated: {calculated_status_counts}"
        )


def cross_check_evaluation_summary(
    evaluation_summary: Any,
    *,
    evaluation_record_count: int,
) -> dict[str, Any]:
    """
    Validate stable structural facts from evaluation_summary.json.

    The pre-manual-review final_status_counts are intentionally not required
    to match the finalized metrics because the summary may still contain
    MANUAL_REVIEW_REQUIRED for cases subsequently resolved by author review.
    """
    result = {
        "available": isinstance(evaluation_summary, dict),
        "case_count_checked": False,
        "status_counts_treated_as_pre_manual_review": False,
    }

    if not isinstance(evaluation_summary, dict):
        return result

    summary_case_count = evaluation_summary.get(
        "evaluated_case_count"
    )

    if (
        summary_case_count is not None
        and int(summary_case_count) != evaluation_record_count
    ):
        raise MetricsError(
            "Repair-evaluation summary count does not match individual "
            f"records: summary={summary_case_count}, "
            f"records={evaluation_record_count}"
        )

    result["case_count_checked"] = summary_case_count is not None
    result["status_counts_treated_as_pre_manual_review"] = isinstance(
        evaluation_summary.get("final_status_counts"),
        dict,
    )

    return result


def parse_args() -> argparse.Namespace:
    default_experiment_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(
        description=(
            "Calculate final Experiment 2 detection and GPT-5.5 repair "
            "metrics after completed manual review."
        )
    )
    parser.add_argument(
        "--experiment-root",
        type=Path,
        default=default_experiment_root,
        help=(
            "Path to experiments/experiment2. Defaults to the parent "
            "directory of this script's scripts folder."
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing metrics_gpt55 output files.",
    )
    parser.add_argument(
        "--skip-expected-result-checks",
        action="store_true",
        help=(
            "Skip frozen expected-count checks. Structural validation "
            "still runs. Use only for deliberate non-baseline datasets."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    experiment_root = args.experiment_root.resolve()
    outputs_dir = experiment_root / "outputs"
    configuration = load_configuration(experiment_root)

    detection_dir = outputs_dir / "detection"
    repair_records_dir = (
        outputs_dir
        / configuration["repair_output_name"]
        / "records"
    )
    evaluation_dir = (
        outputs_dir
        / configuration["repair_evaluation_output_name"]
    )
    evaluation_records_dir = evaluation_dir / "records"
    evaluation_summary_path = (
        evaluation_dir / "evaluation_summary.json"
    )
    manual_review_decisions_path = (
        evaluation_dir / "manual_review_decisions.json"
    )
    metrics_dir = (
        outputs_dir / configuration["metrics_output_name"]
    )

    output_paths = {
        "metrics_summary_json": (
            metrics_dir / "metrics_summary.json"
        ),
        "per_cwe_results_json": (
            metrics_dir / "per_cwe_results.json"
        ),
        "finalized_repair_evaluations_json": (
            metrics_dir / "finalized_repair_evaluations.json"
        ),
        "metrics_summary_csv": (
            metrics_dir / "metrics_summary.csv"
        ),
        "per_cwe_results_csv": (
            metrics_dir / "per_cwe_results.csv"
        ),
    }

    existing_outputs = [
        path for path in output_paths.values() if path.exists()
    ]
    if existing_outputs and not args.overwrite:
        joined = "\n".join(
            f"  {path}" for path in existing_outputs
        )
        raise MetricsError(
            "Metrics outputs already exist. Use --overwrite to replace "
            f"them:\n{joined}"
        )

    detection_records = discover_detection_records(
        detection_dir
    )
    repair_records = discover_repair_records(
        repair_records_dir
    )
    evaluation_records = discover_repair_evaluation_records(
        evaluation_records_dir
    )
    manual_decisions = discover_manual_review_decisions(
        manual_review_decisions_path
    )

    finalized_evaluations, manual_review_provenance = (
        finalize_repair_evaluations(
            evaluation_records,
            manual_decisions,
        )
    )

    detection_metrics, detection_by_cwe = (
        calculate_detection_metrics(detection_records)
    )
    repair_metrics, repair_by_cwe = calculate_repair_metrics(
        detection_records,
        repair_records,
        finalized_evaluations,
    )

    if not args.skip_expected_result_checks:
        validate_expected_results(
            detection_metrics,
            repair_metrics,
            manual_review_provenance,
        )

    per_cwe_results = build_per_cwe_results(
        detection_by_cwe,
        repair_by_cwe,
    )

    evaluation_summary = (
        read_json(evaluation_summary_path)
        if evaluation_summary_path.exists()
        else None
    )
    evaluation_summary_check = cross_check_evaluation_summary(
        evaluation_summary,
        evaluation_record_count=len(evaluation_records),
    )

    detection_models = collect_distinct(
        record["model_id"] for record in detection_records
    )
    repair_models = collect_distinct(
        record["model_id"] for record in repair_records
    )
    detection_run_ids = collect_distinct(
        record["run_id"] for record in detection_records
    )
    repair_run_ids = collect_distinct(
        record["run_id"] for record in repair_records
    )
    evaluation_run_ids = collect_distinct(
        record["run_id"] for record in evaluation_records
    )
    manual_reviewers = collect_distinct(
        record["reviewer"]
        for record in manual_decisions
        if record["decision"] is not None
    )

    generated_at_utc = utc_now_iso()

    summary = {
        "schema_version": SCHEMA_VERSION,
        "stage": "metrics",
        "generated_at_utc": generated_at_utc,
        "experiment": "experiment2_secure_code_agent_baseline",
        "configuration": {
            "configuration_name": configuration[
                "configuration_name"
            ],
            "experiment_root": experiment_root.as_posix(),
            "protocol": "single_pass_repair",
            "successful_repair_status": "SECURE",
            "configured_detection_model": configuration[
                "detection_model"
            ],
            "configured_repair_model": configuration[
                "repair_model"
            ],
            "repair_output_name": configuration[
                "repair_output_name"
            ],
            "repair_evaluation_output_name": configuration[
                "repair_evaluation_output_name"
            ],
            "metrics_output_name": configuration[
                "metrics_output_name"
            ],
            "config_path": configuration["config_path"],
            "config_loaded": (
                configuration["config_loaded"] == "true"
            ),
            "observed_detection_models": detection_models,
            "observed_repair_models": repair_models,
            "detection_run_ids": detection_run_ids,
            "repair_run_ids": repair_run_ids,
            "repair_evaluation_run_ids": evaluation_run_ids,
        },
        "inputs": {
            "detection_directory": detection_dir.as_posix(),
            "repair_records_directory": (
                repair_records_dir.as_posix()
            ),
            "repair_evaluation_records_directory": (
                evaluation_records_dir.as_posix()
            ),
            "repair_evaluation_summary": (
                evaluation_summary_path.as_posix()
                if evaluation_summary_path.exists()
                else None
            ),
            "manual_review_decisions": (
                manual_review_decisions_path.as_posix()
            ),
        },
        "manual_review": {
            **manual_review_provenance,
            "reviewers": manual_reviewers,
            "decision_file": (
                manual_review_decisions_path.as_posix()
            ),
            "merge_policy": (
                "Manual decisions are applied only to evaluation cases "
                "whose automated status is MANUAL_REVIEW_REQUIRED. "
                "Existing automated SECURE, INSECURE, or INVALID_REPAIR "
                "statuses are retained."
            ),
        },
        "evaluation_summary_check": evaluation_summary_check,
        "expected_result_checks": {
            "enabled": not args.skip_expected_result_checks,
            "expected_detection_sample_count": (
                EXPECTED_DETECTION_SAMPLE_COUNT
            ),
            "expected_repair_attempt_count": (
                EXPECTED_REPAIR_ATTEMPT_COUNT
            ),
            "expected_manual_review_count": (
                EXPECTED_MANUAL_REVIEW_COUNT
            ),
            "expected_final_repair_status_counts": (
                EXPECTED_FINAL_REPAIR_STATUS_COUNTS
            ),
        },
        "detection": detection_metrics,
        "repair": repair_metrics,
    }

    metrics_dir.mkdir(parents=True, exist_ok=True)

    write_json(
        output_paths["metrics_summary_json"],
        summary,
    )
    write_json(
        output_paths["per_cwe_results_json"],
        {
            "schema_version": SCHEMA_VERSION,
            "generated_at_utc": generated_at_utc,
            "experiment": summary["experiment"],
            "results": per_cwe_results,
        },
    )
    write_json(
        output_paths["finalized_repair_evaluations_json"],
        {
            "schema_version": SCHEMA_VERSION,
            "generated_at_utc": generated_at_utc,
            "experiment": summary["experiment"],
            "merge_provenance": manual_review_provenance,
            "evaluations": finalized_evaluations,
        },
    )
    write_summary_csv(
        output_paths["metrics_summary_csv"],
        summary,
    )
    write_per_cwe_csv(
        output_paths["per_cwe_results_csv"],
        per_cwe_results,
    )

    detection = summary["detection"]
    repair = summary["repair"]
    manual = summary["manual_review"]

    print("\nMetrics calculation complete.")
    print(
        f"  Configuration: "
        f"{configuration['configuration_name']}"
    )
    print(
        f"  Detection model: "
        f"{configuration['detection_model']}"
    )
    print(
        f"  Repair model: "
        f"{configuration['repair_model']}"
    )
    print(
        f"  Detection samples: "
        f"{detection['sample_counts']['total']}"
    )
    print(
        "  Confusion matrix: "
        f"TP={detection['confusion_matrix']['true_positive']}, "
        f"TN={detection['confusion_matrix']['true_negative']}, "
        f"FP={detection['confusion_matrix']['false_positive']}, "
        f"FN={detection['confusion_matrix']['false_negative']}"
    )
    print(
        "  Detection metrics: "
        f"accuracy={detection['metrics']['accuracy_percent']}%, "
        f"precision={detection['metrics']['precision_percent']}%, "
        f"recall={detection['metrics']['recall_percent']}%, "
        f"F1={detection['metrics']['f1_score_percent']}%, "
        f"coverage="
        f"{detection['metrics']['detection_coverage_percent']}%"
    )
    print(
        "  Manual review merge: "
        f"applied={manual['completed_manual_decisions_used']}, "
        f"automated_retained="
        f"{manual['automated_final_cases_retained']}, "
        f"unresolved={manual['unresolved_case_count']}"
    )
    print(
        "  Repair outcomes: "
        f"SECURE={repair['final_status_counts']['SECURE']}, "
        f"INSECURE={repair['final_status_counts']['INSECURE']}, "
        f"INVALID_REPAIR="
        f"{repair['final_status_counts']['INVALID_REPAIR']}"
    )
    print(
        "  Repair metrics: "
        f"success="
        f"{repair['metrics']['repair_success_rate_percent']}%, "
        f"final_secure_output="
        f"{repair['metrics']['final_secure_output_rate_percent']}%, "
        f"attempt_coverage="
        f"{repair['metrics']['repair_attempt_coverage_percent']}%, "
        f"CWE_coverage="
        f"{repair['metrics']['cwe_coverage_percent']}%"
    )
    print("\nOutputs:")
    for path in output_paths.values():
        print(f"  {path}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except MetricsError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
