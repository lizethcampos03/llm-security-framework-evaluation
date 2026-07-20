#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


ORIGINAL_CALIBRATION_CWES = [
    "CWE-89",
    "CWE-798",
    "CWE-327",
    "CWE-306",
    "CWE-285",
    "CWE-215",
    "CWE-200",
    "CWE-117",
    "CWE-94",
]

# Default behavior remains the same as before.
SELECTED_CWES = ORIGINAL_CALIBRATION_CWES

# Error cases from the final 18-case calibration run.
ERROR_CASES_TO_RERUN = [
    {"case_id": "CAL-008", "cwe": "CWE-306", "expected_label": "safe"},
    {"case_id": "CAL-015", "cwe": "CWE-117", "expected_label": "vulnerable"},
    {"case_id": "REM-001", "cwe": "CWE-20", "expected_label": "vulnerable"},
    {"case_id": "REM-027", "cwe": "CWE-252", "expected_label": "vulnerable"},
    {"case_id": "REM-044", "cwe": "CWE-329", "expected_label": "safe"},
    {"case_id": "REM-064", "cwe": "CWE-406", "expected_label": "safe"},
    {"case_id": "REM-065", "cwe": "CWE-414", "expected_label": "vulnerable"},
    {"case_id": "REM-072", "cwe": "CWE-454", "expected_label": "safe"},
    {"case_id": "REM-073", "cwe": "CWE-462", "expected_label": "vulnerable"},
    {"case_id": "REM-075", "cwe": "CWE-477", "expected_label": "vulnerable"},
    {"case_id": "REM-082", "cwe": "CWE-522", "expected_label": "safe"},
    {"case_id": "REM-095", "cwe": "CWE-703", "expected_label": "vulnerable"},
    {"case_id": "REM-097", "cwe": "CWE-730", "expected_label": "vulnerable"},
    {"case_id": "REM-109", "cwe": "CWE-835", "expected_label": "vulnerable"},
    {"case_id": "REM-118", "cwe": "CWE-943", "expected_label": "safe"},
]

CONFIG_C_CHALLENGE_CASES = [
    {"case_id": "CAL-008", "cwe": "CWE-306", "expected_label": "safe"},
    {"case_id": "REM-044", "cwe": "CWE-329", "expected_label": "safe"},
    {"case_id": "REM-064", "cwe": "CWE-406", "expected_label": "safe"},
    {"case_id": "REM-072", "cwe": "CWE-454", "expected_label": "safe"},
    {"case_id": "REM-082", "cwe": "CWE-522", "expected_label": "safe"},
    {"case_id": "REM-118", "cwe": "CWE-943", "expected_label": "safe"},

    {"case_id": "CAL-015", "cwe": "CWE-117", "expected_label": "vulnerable"},
    {"case_id": "REM-027", "cwe": "CWE-252", "expected_label": "vulnerable"},
    {"case_id": "REM-073", "cwe": "CWE-462", "expected_label": "vulnerable"},
    {"case_id": "REM-075", "cwe": "CWE-477", "expected_label": "vulnerable"},
    {"case_id": "REM-097", "cwe": "CWE-730", "expected_label": "vulnerable"},
    {"case_id": "REM-109", "cwe": "CWE-835", "expected_label": "vulnerable"},
]

DATASET_DIR = Path("data/securityeval_dataset")
OUTPUT_DIR = Path("outputs/architecture_calibration")

def build_config_c_challenge_cases(dataset_dir: Path) -> List[Dict[str, Any]]:
    return [
        build_case(
            dataset_dir=dataset_dir,
            cwe=case["cwe"],
            expected_label=case["expected_label"],
            case_id=case["case_id"],
        )
        for case in CONFIG_C_CHALLENGE_CASES
    ]

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_label(value: Any) -> str:
    text = str(value or "uncertain").lower().strip()
    return text if text in {"vulnerable", "safe", "uncertain"} else "uncertain"


def primary_finding(detection: Dict[str, Any]) -> Dict[str, Any]:
    findings = detection.get("findings") or []
    return findings[0] if isinstance(findings, list) and findings and isinstance(findings[0], dict) else {}


def cwe_sort_key(cwe: str) -> int:
    match = re.search(r"CWE-(\d+)", cwe)
    return int(match.group(1)) if match else 10**9


def discover_cwe_folders(dataset_dir: Path) -> List[str]:
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Missing dataset directory: {dataset_dir}")

    cwes = [
        path.name
        for path in dataset_dir.iterdir()
        if path.is_dir() and re.match(r"^CWE-\d+$", path.name)
    ]

    return sorted(cwes, key=cwe_sort_key)


def load_graph(repo_root: Path):
    sys.path.insert(0, str(repo_root))
    sys.path.insert(0, str(repo_root / "src"))

    try:
        from src.graph import build_graph
        return build_graph()
    except Exception:
        from graph import graph
        return graph


def build_case(
    dataset_dir: Path,
    cwe: str,
    expected_label: str,
    case_id: str,
) -> Dict[str, Any]:
    cwe_dir = dataset_dir / cwe
    if not cwe_dir.exists():
        raise FileNotFoundError(f"Missing folder: {cwe_dir}")

    context_profile_path = cwe_dir / "context_profile.json"
    context_profile = read_json(context_profile_path) if context_profile_path.exists() else {}

    filename = (
        "vulnerable_securityeval_sample.py"
        if expected_label == "vulnerable"
        else "safe_verified_counterpart.py"
    )

    code_path = cwe_dir / filename
    if not code_path.exists():
        raise FileNotFoundError(f"Missing sample: {code_path}")

    return {
        "case_id": case_id,
        "cwe": cwe,
        "expected_label": expected_label,
        "code_path": str(code_path),
        "file_name": f"{cwe}_{expected_label}.py",
        "context_profile": context_profile,
    }


def build_cases(dataset_dir: Path, selected_cwes: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    cases = []
    case_number = 1

    cwes = selected_cwes if selected_cwes is not None else SELECTED_CWES

    for cwe in cwes:
        for expected_label in ["vulnerable", "safe"]:
            cases.append(
                build_case(
                    dataset_dir=dataset_dir,
                    cwe=cwe,
                    expected_label=expected_label,
                    case_id=f"CAL-{case_number:03d}",
                )
            )
            case_number += 1

    return cases


def build_error_and_remaining_cases(dataset_dir: Path) -> List[Dict[str, Any]]:
    cases = []

    # First: rerun the known error cases using their original calibration IDs.
    for error_case in ERROR_CASES_TO_RERUN:
        cases.append(
            build_case(
                dataset_dir=dataset_dir,
                cwe=error_case["cwe"],
                expected_label=error_case["expected_label"],
                case_id=error_case["case_id"],
            )
        )

    # Second: run all CWE folders that were not part of the original 9-CWE calibration set.
    all_cwes = discover_cwe_folders(dataset_dir)
    remaining_cwes = [cwe for cwe in all_cwes if cwe not in ORIGINAL_CALIBRATION_CWES]

    remaining_case_number = 1
    for cwe in remaining_cwes:
        for expected_label in ["vulnerable", "safe"]:
            cases.append(
                build_case(
                    dataset_dir=dataset_dir,
                    cwe=cwe,
                    expected_label=expected_label,
                    case_id=f"REM-{remaining_case_number:03d}",
                )
            )
            remaining_case_number += 1

    return cases

def build_error_cases_only(dataset_dir: Path) -> List[Dict[str, Any]]:
    return [
        build_case(
            dataset_dir=dataset_dir,
            cwe=error_case["cwe"],
            expected_label=error_case["expected_label"],
            case_id=error_case["case_id"],
        )
        for error_case in ERROR_CASES_TO_RERUN
    ]

def apply_start_case(cases: List[Dict[str, Any]], start_case: str | None) -> List[Dict[str, Any]]:
    if not start_case:
        return cases

    normalized_start_case = start_case.strip().upper()

    for index, case in enumerate(cases):
        if case["case_id"].upper() == normalized_start_case:
            return cases[index:]

    valid_cases = ", ".join(case["case_id"] for case in cases)
    raise ValueError(
        f"Start case '{start_case}' was not found. Valid case IDs are: {valid_cases}"
    )


def classify_retrieval_success(result_data: Dict[str, Any]) -> str:
    rag = result_data.get("rag_results", {})
    if isinstance(rag, dict):
        if rag.get("configuration") == "full_hybrid_evidence_reranker":
            return "Yes"
        if rag.get("retrieved_cwe_records") or rag.get("ranked_cwe_candidates"):
            return "Yes"
    if result_data.get("retrieved_context"):
        return "Partial"
    return "No"


def retrieval_quality(result_data: Dict[str, Any], expected_cwe: str) -> str:
    text = json.dumps(result_data.get("rag_results", {}), default=str).lower()
    if expected_cwe.lower() in text:
        return "Strong"
    if "cwe" in text:
        return "Moderate"
    return "Weak"


def run_case(graph: Any, case: Dict[str, Any]) -> Dict[str, Any]:
    code = read_text(Path(case["code_path"]))

    # Fairness: expected_label and cwe are NOT passed into the graph.
    initial_data = {
        "case_id": case["case_id"],
        "code": code,
        "context": json.dumps(case["context_profile"], indent=2),
        "context_profile": case["context_profile"],
        "file_name": case["file_name"],
        "number_of_runs": 1,
    }

    start = time.perf_counter()
    error = ""

    try:
        result = graph.invoke({"data": initial_data})
        result_data = result.get("data", result)
    except Exception as exc:
        result_data = {}
        error = f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}"

    latency = round(time.perf_counter() - start, 3)

    detection = result_data.get("detection_result", {})
    validation = result_data.get("validation_result", {})
    fix = result_data.get("fix_result", {})
    finding = primary_finding(detection)

    detected_label = normalize_label(validation.get("final_decision"))
    if detected_label == "uncertain":
        detected_label = normalize_label(detection.get("overall_security_status"))

    expected_label = case["expected_label"]
    correct = detected_label == expected_label

    confidence = None

    if finding.get("confidence") is not None:
        confidence = finding.get("confidence")
    elif detection.get("classification_confidence") is not None:
        confidence = detection.get("classification_confidence")
    elif validation.get("average_confidence") not in (None, "", 0, 0.0):
        confidence = validation.get("average_confidence")

    try:
        confidence = float(confidence) if confidence is not None else None
    except Exception:
        confidence = None

    record = {
        "case_id": case["case_id"],
        "cwe": case["cwe"],
        "expected_label": expected_label,
        "detected_label": detected_label,
        "correctness": "Yes" if correct else "No",
        "predicted_cwe": finding.get("cwe_id", ""),
        "confidence_score": confidence,
        "validation_consistency": validation.get("consistency_score", 0.0),
        "vulnerable_votes": validation.get("vulnerable_votes", ""),
        "safe_votes": validation.get("safe_votes", ""),
        "uncertain_votes": validation.get("uncertain_votes", ""),
        "retrieval_success": classify_retrieval_success(result_data),
        "retrieved_cwe_quality": retrieval_quality(result_data, case["cwe"]),
        "rag_configuration": result_data.get("rag_results", {}).get("configuration", ""),
        "total_latency_seconds": latency,
        "fix_generated": fix.get("fix_generated", False) if isinstance(fix, dict) else False,
        "fix_quality": "Generated" if isinstance(fix, dict) and fix.get("fix_generated") else "Not Generated",
        "error": error,
        "full_result": result_data,
    }

    print(
        f"{case['case_id']} {case['cwe']} {expected_label} -> "
        f"{detected_label} | correct={record['correctness']} | "
        f"rag={record['rag_configuration']} | {latency}s"
    )

    return record


def aggregate(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(records)
    correct = sum(r["correctness"] == "Yes" for r in records)

    vuln = [r for r in records if r["expected_label"] == "vulnerable"]
    safe = [r for r in records if r["expected_label"] == "safe"]

    tp = sum(r["expected_label"] == "vulnerable" and r["detected_label"] == "vulnerable" for r in records)
    fp = sum(r["expected_label"] == "safe" and r["detected_label"] == "vulnerable" for r in records)
    fn = sum(r["expected_label"] == "vulnerable" and r["detected_label"] != "vulnerable" for r in records)
    tn = sum(r["expected_label"] == "safe" and r["detected_label"] == "safe" for r in records)

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    def avg(key: str) -> float:
        values = []
        for r in records:
            try:
                value = r.get(key)
                if value is not None and value != "":
                    values.append(float(value))
            except Exception:
                pass
        return round(sum(values) / len(values), 4) if values else 0.0

    return {
        "total_cases": total,
        "correct_cases": correct,
        "overall_accuracy": round(correct / total, 4) if total else 0.0,
        "vulnerable_detection_accuracy": round(sum(r["detected_label"] == "vulnerable" for r in vuln) / len(vuln), 4) if vuln else 0.0,
        "safe_classification_accuracy": round(sum(r["detected_label"] == "safe" for r in safe) / len(safe), 4) if safe else 0.0,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "average_confidence": avg("confidence_score"),
        "average_validation_consistency": avg("validation_consistency"),
        "average_latency_seconds": avg("total_latency_seconds"),
    }


def write_outputs(records: List[Dict[str, Any]], metrics: Dict[str, Any], run_mode: str) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = OUTPUT_DIR / f"calibration_results_{timestamp}.json"
    csv_path = OUTPUT_DIR / f"calibration_results_{timestamp}.csv"
    md_path = OUTPUT_DIR / f"calibration_report_{timestamp}.md"

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "experiment": "Final Architecture Calibration",
        "run_mode": run_mode,
        "fairness_note": "Expected labels and CWE IDs were hidden from graph.invoke and used only for scoring after execution.",
        "original_calibration_cwes": ORIGINAL_CALIBRATION_CWES,
        "error_cases_to_rerun": ERROR_CASES_TO_RERUN,
        "aggregate_metrics": metrics,
        "records": records,
    }
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    fieldnames = [
        "case_id", "cwe", "expected_label", "detected_label", "correctness",
        "predicted_cwe", "confidence_score", "validation_consistency",
        "vulnerable_votes", "safe_votes", "uncertain_votes",
        "retrieval_success", "retrieved_cwe_quality", "rag_configuration",
        "total_latency_seconds", "fix_generated", "fix_quality", "error",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            writer.writerow({k: r.get(k, "") for k in fieldnames})

    lines = [
        "# Final Architecture Calibration Report",
        "",
        f"Generated: `{datetime.now().isoformat(timespec='seconds')}`",
        f"Run mode: `{run_mode}`",
        "",
        "## Fairness Note",
        "Expected labels and CWE IDs were hidden from the graph and used only after execution for scoring.",
        "",
        "## Aggregate Metrics",
    ]

    for key, value in metrics.items():
        lines.append(f"- **{key}**: `{value}`")

    lines.extend([
        "",
        "## Case Results",
        "| Case | CWE | Expected | Detected | Correct | Predicted CWE | RAG Config | Confidence | Consistency | Latency |",
        "|---|---|---|---|---|---|---|---:|---:|---:|",
    ])

    for r in records:
        lines.append(
            f"| {r['case_id']} | {r['cwe']} | {r['expected_label']} | {r['detected_label']} | "
            f"{r['correctness']} | {r.get('predicted_cwe','')} | {r.get('rag_configuration','')} | "
            f"{r.get('confidence_score',0)} | {r.get('validation_consistency',0)} | "
            f"{r.get('total_latency_seconds',0)} |"
        )

    md_path.write_text("\n".join(lines), encoding="utf-8")

    return {
        "json": str(json_path),
        "csv": str(csv_path),
        "markdown": str(md_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--start-case", type=str, default=None)
    parser.add_argument("--list-cases", action="store_true")
    parser.add_argument(
        "--error-and-remaining-69",
        action="store_true",
        help="Run known error cases plus all CWE folders not included in the original 9-CWE calibration set.",
    )
    parser.add_argument(
        "--all-cwes",
        action="store_true",
        help="Run all CWE folders found in data/securityeval_dataset.",
    )
    parser.add_argument(
        "--error-cases-only",
        action="store_true",
        help="Run only the 15 known error cases from the previous full calibration run.",
    )

    parser.add_argument(
        "--config-c-challenge",
        action="store_true",
        help="Run the 12-case Configuration C challenge set.",
    )

    args = parser.parse_args()

    graph = load_graph(Path.cwd())

    run_mode = "original_9_cwe_calibration"

    if args.config_c_challenge:
        cases = build_config_c_challenge_cases(DATASET_DIR)
        run_mode = "configuration_c_challenge_set"
    elif args.error_cases_only:
        cases = build_error_cases_only(DATASET_DIR)
        run_mode = "known_error_cases_only"
    elif args.error_and_remaining_69:
        cases = build_error_and_remaining_cases(DATASET_DIR)
        run_mode = "error_cases_plus_remaining_69_cwes"
    elif args.all_cwes:
        all_cwes = discover_cwe_folders(DATASET_DIR)
        cases = build_cases(DATASET_DIR, selected_cwes=all_cwes)
        run_mode = "all_discovered_cwes"
    else:
        cases = build_cases(DATASET_DIR, selected_cwes=SELECTED_CWES)
    
        cases = apply_start_case(cases, args.start_case)

    if args.limit:
        cases = cases[:args.limit]

    if args.list_cases:
        for case in cases:
            print(f"{case['case_id']} | {case['cwe']} | {case['expected_label']} | {case['code_path']}")
        return 0

    print("\nFINAL ARCHITECTURE CALIBRATION")
    print(f"Run mode: {run_mode}")
    print(f"Cases: {len(cases)}")
    if args.start_case:
        print(f"Starting from: {args.start_case}")
    print("Fairness: expected labels/CWEs are hidden from graph.invoke().\n")

    records = [run_case(graph, case) for case in cases]
    metrics = aggregate(records)
    outputs = write_outputs(records, metrics, run_mode)

    print("\nCALIBRATION COMPLETE")
    print(json.dumps({
        "status": "complete",
        "run_mode": run_mode,
        "cases": len(records),
        "aggregate_metrics": metrics,
        "outputs": outputs,
    }, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())