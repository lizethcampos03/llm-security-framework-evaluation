"""
04_metrics.py


Aggregate Experiment 2 detection and repair-evaluation outputs into final
metrics for the reproduced end-to-end workflow baseline.


Expected experiment layout:


experiments/experiment2/
├── outputs/
│   ├── detection/
│   ├── repair/
│   │   └── records/
│   ├── repair_evaluation/
│   │   ├── records/
│   │   └── evaluation_summary.json
│   └── metrics/
└── scripts/
    └── 04_metrics.py


The script:
1. Reconstructs the detection confusion matrix directly from detection records.
2. Calculates accuracy, precision, recall, F1, and detection coverage.
3. Reads finalized repair-evaluation records.
4. Calculates repair success rate, final secure output rate, repair-attempt
   coverage, and successful CWE coverage.
5. Writes auditable JSON and CSV outputs.


Only final repair status "SECURE" counts as a successful repair.
"INSECURE" and "INVALID_REPAIR" count as unsuccessful outcomes.
"""


from __future__ import annotations


import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable




SCHEMA_VERSION = "1.0"
VALID_FINAL_REPAIR_STATUSES = {
    "SECURE",
    "INSECURE",
    "INVALID_REPAIR",
    "MANUAL_REVIEW_REQUIRED",
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
            f"Invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
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




def first_present(data: dict[str, Any], candidates: Iterable[tuple[str, ...]]) -> Any:
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




def safe_divide(numerator: int | float, denominator: int | float) -> float | None:
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




def discover_detection_records(detection_dir: Path) -> list[dict[str, Any]]:
    if not detection_dir.is_dir():
        raise MetricsError(f"Detection output directory not found: {detection_dir}")


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
                f"Duplicate detection sample_id {sample_id!r}; latest file: {path}"
            )
        seen_sample_ids.add(sample_id)


        ground_truth = parse_bool(
            ground_truth_raw,
            field_name="ground_truth_vulnerable",
            source=path,
        )
        prediction = parse_bool(
            prediction_raw,
            field_name="prediction_vulnerable",
            source=path,
        )


        model_id = first_present(
            data,
            [
                ("model", "model_id"),
                ("model_id",),
                ("configuration", "model_id"),
            ],
        )
        run_id = first_present(data, [("run_id",), ("metadata", "run_id")])


        records.append(
            {
                "source_path": path.as_posix(),
                "sample_id": sample_id,
                "cwe_id": cwe_id,
                "ground_truth_vulnerable": ground_truth,
                "prediction_vulnerable": prediction,
                "model_id": model_id,
                "run_id": run_id,
            }
        )


    if not records:
        raise MetricsError(
            f"No usable detection records were found under {detection_dir}. "
            "Expected JSON records containing sample_id, cwe_id, "
            "ground_truth_vulnerable, and prediction_vulnerable."
        )


    return records




def discover_repair_records(repair_records_dir: Path) -> list[dict[str, Any]]:
    if not repair_records_dir.is_dir():
        raise MetricsError(f"Repair records directory not found: {repair_records_dir}")


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
        if sample_id in seen_sample_ids:
            raise MetricsError(
                f"Duplicate repair record for sample_id {sample_id!r}: {path}"
            )
        seen_sample_ids.add(sample_id)


        records.append(
            {
                "source_path": path.as_posix(),
                "sample_id": sample_id,
                "cwe_id": str(cwe_id),
                "model_id": first_present(
                    data,
                    [
                        ("model", "model_id"),
                        ("repair_model",),
                        ("model_id",),
                    ],
                ),
                "run_id": first_present(data, [("run_id",), ("metadata", "run_id")]),
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
            f"Repair-evaluation records directory not found: {evaluation_records_dir}"
        )


    records: list[dict[str, Any]] = []
    seen_case_ids: set[str] = set()


    for path in sorted(evaluation_records_dir.rglob("*.json")):
        data = read_json(path)
        if not isinstance(data, dict):
            continue


        case_id = first_present(data, [("case", "case_id"), ("case_id",)])
        sample_id = first_present(data, [("case", "sample_id"), ("sample_id",)])
        cwe_id = first_present(data, [("case", "cwe_id"), ("cwe_id",)])
        final_status = first_present(
            data,
            [
                ("final_assessment", "status"),
                ("final_status",),
                ("status",),
            ],
        )


        if case_id is None or sample_id is None or cwe_id is None or final_status is None:
            continue


        case_id = str(case_id)
        final_status = str(final_status).upper()


        if final_status not in VALID_FINAL_REPAIR_STATUSES:
            raise MetricsError(
                f"Unexpected final repair status {final_status!r} in {path}"
            )
        if case_id in seen_case_ids:
            raise MetricsError(f"Duplicate evaluation case_id {case_id!r}: {path}")
        seen_case_ids.add(case_id)


        records.append(
            {
                "source_path": path.as_posix(),
                "case_id": case_id,
                "sample_id": str(sample_id),
                "cwe_id": str(cwe_id),
                "final_status": final_status,
                "run_id": first_present(data, [("run_id",), ("metadata", "run_id")]),
                "decision_source": first_present(
                    data,
                    [
                        ("final_assessment", "decision_source"),
                        ("decision_source",),
                    ],
                ),
            }
        )


    if not records:
        raise MetricsError(
            f"No usable repair-evaluation records were found under "
            f"{evaluation_records_dir}."
        )


    return records




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
                by_cwe[cwe_id]["true_positive_sample_ids"].append(sample_id)
            else:
                fn += 1
                by_cwe[cwe_id]["false_negative_sample_ids"].append(sample_id)
        else:
            by_cwe[cwe_id]["safe_sample_ids"].append(sample_id)
            if prediction:
                fp += 1
                by_cwe[cwe_id]["false_positive_sample_ids"].append(sample_id)
            else:
                tn += 1
                by_cwe[cwe_id]["true_negative_sample_ids"].append(sample_id)


    total = tp + tn + fp + fn
    vulnerable_count = tp + fn
    safe_count = tn + fp


    accuracy = safe_divide(tp + tn, total)
    precision = safe_divide(tp, tp + fp)
    recall = safe_divide(tp, tp + fn)
    f1 = (
        None
        if precision is None or recall is None or precision + recall == 0
        else 2 * precision * recall / (precision + recall)
    )


    vulnerable_cwes = {
        record["cwe_id"] for record in records if record["ground_truth_vulnerable"]
    }
    detected_vulnerable_cwes = {
        record["cwe_id"]
        for record in records
        if record["ground_truth_vulnerable"] and record["prediction_vulnerable"]
    }
    detection_coverage = safe_divide(
        len(detected_vulnerable_cwes), len(vulnerable_cwes)
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
            "detection_coverage_percent": percentage(detection_coverage),
        },
        "coverage_counts": {
            "detected_vulnerable_cwes": len(detected_vulnerable_cwes),
            "total_vulnerable_cwes": len(vulnerable_cwes),
        },
        "definitions": {
            "positive_class": "The benchmark sample contains its predefined target CWE.",
            "detection_coverage": (
                "Unique target CWEs correctly detected in vulnerable samples divided "
                "by all unique target CWEs represented by vulnerable samples."
            ),
        },
    }


    return metrics, by_cwe




def calculate_repair_metrics(
    detection_records: list[dict[str, Any]],
    repair_records: list[dict[str, Any]],
    evaluation_records: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    vulnerable_detection_records = [
        record for record in detection_records if record["ground_truth_vulnerable"]
    ]
    vulnerable_sample_ids = {record["sample_id"] for record in vulnerable_detection_records}
    vulnerable_cwes = {record["cwe_id"] for record in vulnerable_detection_records}


    repair_by_sample = {record["sample_id"]: record for record in repair_records}
    evaluation_by_sample = {record["sample_id"]: record for record in evaluation_records}


    unknown_repair_samples = sorted(set(repair_by_sample) - vulnerable_sample_ids)
    if unknown_repair_samples:
        raise MetricsError(
            "Repair records exist for samples that are not vulnerable detection "
            f"inputs: {unknown_repair_samples}"
        )


    unknown_evaluation_samples = sorted(set(evaluation_by_sample) - vulnerable_sample_ids)
    if unknown_evaluation_samples:
        raise MetricsError(
            "Repair-evaluation records exist for samples that are not vulnerable "
            f"detection inputs: {unknown_evaluation_samples}"
        )


    missing_evaluations = sorted(set(repair_by_sample) - set(evaluation_by_sample))
    if missing_evaluations:
        raise MetricsError(
            "Repair records are missing finalized evaluation records for: "
            f"{missing_evaluations}"
        )


    status_counts = Counter(
        record["final_status"] for record in evaluation_records
    )


    secure_count = status_counts.get("SECURE", 0)
    insecure_count = status_counts.get("INSECURE", 0)
    invalid_count = status_counts.get("INVALID_REPAIR", 0)
    manual_review_count = status_counts.get("MANUAL_REVIEW_REQUIRED", 0)


    if manual_review_count:
        raise MetricsError(
            f"{manual_review_count} repair evaluations still require manual review. "
            "Finalize manual review before calculating final metrics."
        )


    repair_attempt_count = len(repair_records)
    evaluated_repair_count = len(evaluation_records)
    vulnerable_input_count = len(vulnerable_detection_records)
    skipped_due_to_detection_count = vulnerable_input_count - repair_attempt_count


    repair_success_rate = safe_divide(secure_count, repair_attempt_count)
    evaluated_repair_success_rate = safe_divide(
        secure_count, evaluated_repair_count
    )
    final_secure_output_rate = safe_divide(secure_count, vulnerable_input_count)


    attempted_cwes = {record["cwe_id"] for record in repair_records}
    secure_cwes = {
        record["cwe_id"]
        for record in evaluation_records
        if record["final_status"] == "SECURE"
    }


    repair_attempt_coverage = safe_divide(len(attempted_cwes), len(vulnerable_cwes))
    successful_cwe_coverage = safe_divide(len(secure_cwes), len(vulnerable_cwes))


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


    for evaluation in evaluation_records:
        by_cwe[evaluation["cwe_id"]].update(
            {
                "evaluation_case_id": evaluation["case_id"],
                "evaluation_run_id": evaluation["run_id"],
                "final_repair_status": evaluation["final_status"],
                "final_secure_output": evaluation["final_status"] == "SECURE",
                "decision_source": evaluation["decision_source"],
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
            "skipped_due_to_detection_false_negative": skipped_due_to_detection_count,
        },
        "final_status_counts": {
            "SECURE": secure_count,
            "INSECURE": insecure_count,
            "INVALID_REPAIR": invalid_count,
            "MANUAL_REVIEW_REQUIRED": manual_review_count,
        },
        "metrics": {
            "repair_success_rate": rounded(repair_success_rate),
            "repair_success_rate_percent": percentage(repair_success_rate),
            "evaluated_repair_success_rate": rounded(
                evaluated_repair_success_rate
            ),
            "evaluated_repair_success_rate_percent": percentage(
                evaluated_repair_success_rate
            ),
            "final_secure_output_rate": rounded(final_secure_output_rate),
            "final_secure_output_rate_percent": percentage(final_secure_output_rate),
            "repair_attempt_coverage": rounded(repair_attempt_coverage),
            "repair_attempt_coverage_percent": percentage(repair_attempt_coverage),
            "cwe_coverage": rounded(successful_cwe_coverage),
            "cwe_coverage_percent": percentage(successful_cwe_coverage),
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
            "final_secure_output_rate": (
                "Final SECURE repairs divided by all vulnerable benchmark inputs, "
                "including detector false negatives that never reached repair."
            ),
            "repair_attempt_coverage": (
                "Unique target CWEs sent to repair divided by all vulnerable target "
                "CWEs represented in the benchmark."
            ),
            "cwe_coverage": (
                "Unique target CWEs with a final SECURE repair divided by all "
                "vulnerable target CWEs represented in the benchmark."
            ),
            "successful_repair_status": "Only final status SECURE is successful.",
        },
    }


    return metrics, by_cwe




def collect_distinct(values: Iterable[Any]) -> list[Any]:
    return sorted({value for value in values if value not in (None, "")})




def build_per_cwe_results(
    detection_by_cwe: dict[str, dict[str, Any]],
    repair_by_cwe: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    all_cwes = sorted(
        set(detection_by_cwe) | set(repair_by_cwe),
        key=lambda value: (
            int(value.split("-", 1)[1])
            if value.upper().startswith("CWE-") and value.split("-", 1)[1].isdigit()
            else math.inf,
            value,
        ),
    )


    results: list[dict[str, Any]] = []
    for cwe_id in all_cwes:
        detection = detection_by_cwe.get(cwe_id, {})
        repair = repair_by_cwe.get(cwe_id, {})


        vulnerable_ids = detection.get("vulnerable_sample_ids", [])
        safe_ids = detection.get("safe_sample_ids", [])
        tp_ids = detection.get("true_positive_sample_ids", [])
        fn_ids = detection.get("false_negative_sample_ids", [])
        tn_ids = detection.get("true_negative_sample_ids", [])
        fp_ids = detection.get("false_positive_sample_ids", [])


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
                    "safe_correctly_classified": bool(safe_ids) and not bool(fp_ids),
                },
                "repair": {
                    "attempted": repair.get("repair_attempted", False),
                    "sample_id": repair.get("repair_sample_id"),
                    "final_status": repair.get("final_repair_status"),
                    "final_secure_output": repair.get(
                        "final_secure_output", False
                    ),
                    "decision_source": repair.get("decision_source"),
                },
            }
        )


    return results




def write_summary_csv(path: Path, summary: dict[str, Any]) -> None:
    rows = [
        ("detection.total_samples", summary["detection"]["sample_counts"]["total"]),
        (
            "detection.vulnerable_samples",
            summary["detection"]["sample_counts"]["vulnerable"],
        ),
        ("detection.safe_samples", summary["detection"]["sample_counts"]["safe"]),
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
            summary["detection"]["metrics"]["detection_coverage_percent"],
        ),
        (
            "repair.repair_attempts",
            summary["repair"]["pipeline_counts"]["repair_attempts"],
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
            summary["repair"]["final_status_counts"]["INVALID_REPAIR"],
        ),
        (
            "repair.repair_success_rate_percent",
            summary["repair"]["metrics"]["repair_success_rate_percent"],
        ),
        (
            "repair.final_secure_output_rate_percent",
            summary["repair"]["metrics"]["final_secure_output_rate_percent"],
        ),
        (
            "repair.repair_attempt_coverage_percent",
            summary["repair"]["metrics"]["repair_attempt_coverage_percent"],
        ),
        (
            "repair.cwe_coverage_percent",
            summary["repair"]["metrics"]["cwe_coverage_percent"],
        ),
    ]


    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "value"])
        writer.writerows(rows)




def write_per_cwe_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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
        "final_repair_status",
        "final_secure_output",
        "decision_source",
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
                    "safe_sample_ids": ";".join(row["safe_sample_ids"]),
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
                    "final_repair_status": row["repair"]["final_status"],
                    "final_secure_output": row["repair"][
                        "final_secure_output"
                    ],
                    "decision_source": row["repair"]["decision_source"],
                }
            )




def parse_args() -> argparse.Namespace:
    default_experiment_root = Path(__file__).resolve().parents[1]


    parser = argparse.ArgumentParser(
        description=(
            "Calculate final detection and repair metrics for Experiment 2."
        )
    )
    parser.add_argument(
        "--experiment-root",
        type=Path,
        default=default_experiment_root,
        help=(
            "Path to experiments/experiment2. Defaults to the parent directory "
            "of this script's scripts folder."
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing metrics output files.",
    )
    return parser.parse_args()




def main() -> int:
    args = parse_args()
    experiment_root = args.experiment_root.resolve()
    outputs_dir = experiment_root / "outputs"


    detection_dir = outputs_dir / "detection"
    repair_records_dir = outputs_dir / "repair" / "records"
    evaluation_dir = outputs_dir / "repair_evaluation"
    evaluation_records_dir = evaluation_dir / "records"
    evaluation_summary_path = evaluation_dir / "evaluation_summary.json"
    metrics_dir = outputs_dir / "metrics"


    output_paths = {
        "metrics_summary_json": metrics_dir / "metrics_summary.json",
        "per_cwe_results_json": metrics_dir / "per_cwe_results.json",
        "metrics_summary_csv": metrics_dir / "metrics_summary.csv",
        "per_cwe_results_csv": metrics_dir / "per_cwe_results.csv",
    }


    existing_outputs = [path for path in output_paths.values() if path.exists()]
    if existing_outputs and not args.overwrite:
        joined = "\n".join(f"  {path}" for path in existing_outputs)
        raise MetricsError(
            "Metrics outputs already exist. Use --overwrite to replace them:\n"
            f"{joined}"
        )


    detection_records = discover_detection_records(detection_dir)
    repair_records = discover_repair_records(repair_records_dir)
    evaluation_records = discover_repair_evaluation_records(
        evaluation_records_dir
    )


    detection_metrics, detection_by_cwe = calculate_detection_metrics(
        detection_records
    )
    repair_metrics, repair_by_cwe = calculate_repair_metrics(
        detection_records,
        repair_records,
        evaluation_records,
    )


    per_cwe_results = build_per_cwe_results(
        detection_by_cwe, repair_by_cwe
    )


    evaluation_summary = (
        read_json(evaluation_summary_path)
        if evaluation_summary_path.exists()
        else None
    )


    # Cross-check against the finalized evaluation summary when available.
    if isinstance(evaluation_summary, dict):
        summary_case_count = evaluation_summary.get("evaluated_case_count")
        if (
            summary_case_count is not None
            and summary_case_count != len(evaluation_records)
        ):
            raise MetricsError(
                "Repair-evaluation summary count does not match individual "
                f"records: summary={summary_case_count}, "
                f"records={len(evaluation_records)}"
            )


        summary_status_counts = evaluation_summary.get("final_status_counts")
        if isinstance(summary_status_counts, dict):
            normalized_summary_counts = {
                status: int(summary_status_counts.get(status, 0))
                for status in (
                    "SECURE",
                    "INSECURE",
                    "INVALID_REPAIR",
                    "MANUAL_REVIEW_REQUIRED",
                )
            }
            calculated_counts = repair_metrics["final_status_counts"]
            if normalized_summary_counts != calculated_counts:
                raise MetricsError(
                    "Repair-evaluation summary status counts do not match "
                    "individual evaluation records.\n"
                    f"Summary: {normalized_summary_counts}\n"
                    f"Calculated: {calculated_counts}"
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


    summary = {
        "schema_version": SCHEMA_VERSION,
        "stage": "metrics",
        "generated_at_utc": utc_now_iso(),
        "experiment": "experiment2_secure_code_agent_baseline",
        "configuration": {
            "experiment_root": experiment_root.as_posix(),
            "protocol": "single_pass_repair",
            "successful_repair_status": "SECURE",
            "detection_models": detection_models,
            "repair_models": repair_models,
            "detection_run_ids": detection_run_ids,
            "repair_run_ids": repair_run_ids,
            "repair_evaluation_run_ids": evaluation_run_ids,
        },
        "inputs": {
            "detection_directory": detection_dir.as_posix(),
            "repair_records_directory": repair_records_dir.as_posix(),
            "repair_evaluation_records_directory": (
                evaluation_records_dir.as_posix()
            ),
            "repair_evaluation_summary": (
                evaluation_summary_path.as_posix()
                if evaluation_summary_path.exists()
                else None
            ),
        },
        "detection": detection_metrics,
        "repair": repair_metrics,
    }


    metrics_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_paths["metrics_summary_json"], summary)
    write_json(
        output_paths["per_cwe_results_json"],
        {
            "schema_version": SCHEMA_VERSION,
            "generated_at_utc": summary["generated_at_utc"],
            "experiment": summary["experiment"],
            "results": per_cwe_results,
        },
    )
    write_summary_csv(output_paths["metrics_summary_csv"], summary)
    write_per_cwe_csv(output_paths["per_cwe_results_csv"], per_cwe_results)


    detection = summary["detection"]
    repair = summary["repair"]


    print("\nMetrics calculation complete.")
    print(f"  Detection samples: {detection['sample_counts']['total']}")
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
        f"coverage={detection['metrics']['detection_coverage_percent']}%"
    )
    print(
        "  Repair outcomes: "
        f"SECURE={repair['final_status_counts']['SECURE']}, "
        f"INSECURE={repair['final_status_counts']['INSECURE']}, "
        f"INVALID_REPAIR={repair['final_status_counts']['INVALID_REPAIR']}"
    )
    print(
        "  Repair metrics: "
        f"success={repair['metrics']['repair_success_rate_percent']}%, "
        f"final_secure_output={repair['metrics']['final_secure_output_rate_percent']}%, "
        f"attempt_coverage={repair['metrics']['repair_attempt_coverage_percent']}%, "
        f"CWE_coverage={repair['metrics']['cwe_coverage_percent']}%"
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
