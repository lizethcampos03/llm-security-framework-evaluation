from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path.cwd()
EXPERIMENT3_ROOT = ROOT / "outputs" / "experiment3_repair"
REPAIR_INPUTS_DIR = EXPERIMENT3_ROOT / "repair_inputs"
MANIFEST_PATH = EXPERIMENT3_ROOT / "experiment3_repair_manifest.json"


def find_latest_experiment1_json() -> Path:
    candidates = sorted(
        (ROOT / "outputs" / "architecture_calibration").glob("calibration_results_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not candidates:
        raise FileNotFoundError(
            "Could not find calibration_results_*.json under "
            "outputs/architecture_calibration/."
        )

    return candidates[0]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def extract_cases(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload

    for key in ["results", "cases", "case_results", "evaluations", "records"]:
        value = payload.get(key) if isinstance(payload, dict) else None
        if isinstance(value, list):
            return value

    raise ValueError(
        "Could not locate case list in Experiment 1 JSON. "
        "Expected one of: results, cases, case_results, evaluations, records."
    )


def get_case_id(case: dict[str, Any], index: int) -> str:
    return (
        case.get("case_id")
        or case.get("id")
        or case.get("sample_id")
        or case.get("name")
        or f"CASE-{index:03d}"
    )


def get_cwe(case: dict[str, Any]) -> str:
    cwe = case.get("cwe") or case.get("cwe_id") or case.get("expected_cwe") or ""
    cwe = str(cwe)
    if cwe and not cwe.upper().startswith("CWE-"):
        cwe = f"CWE-{cwe}"
    return cwe


def get_expected_label(case: dict[str, Any]) -> str:
    for key in ["expected_label", "ground_truth", "label", "expected", "true_label"]:
        value = case.get(key)
        if value:
            return str(value).lower()

    case_id = str(case.get("case_id", "")).lower()
    if "vulnerable" in case_id:
        return "vulnerable"
    if "safe" in case_id:
        return "safe"

    return ""


def get_original_code(case: dict[str, Any]) -> str:
    full_result = case.get("full_result", {})
    if isinstance(full_result, dict):
        for key in ["code", "cleaned_code", "original_code", "input_code", "source_code"]:
            value = full_result.get(key)
            if isinstance(value, str) and value.strip():
                return value

    for key in ["code", "original_code", "input_code", "source_code", "sample_code"]:
        value = case.get(key)
        if isinstance(value, str) and value.strip():
            return value

    for key in ["static_file_path", "original_path", "file_path", "path"]:
        value = case.get(key)
        if value and Path(value).exists():
            return Path(value).read_text(encoding="utf-8", errors="replace")

    return ""


def build_langgraph_report(case: dict[str, Any]) -> dict[str, Any]:
    full_result = case.get("full_result", {})

    if (
        isinstance(full_result, dict)
        and isinstance(full_result.get("final_report"), dict)
    ):
        return {
            "report_source": "output_node_final_report",
            "final_report": full_result["final_report"],
            "full_result": full_result,
        }

    if isinstance(case.get("final_report"), dict):
        return {
            "report_source": "record_final_report",
            "final_report": case["final_report"],
            "full_result": full_result,
        }

    return {
        "report_source": "fallback_full_case_record",
        "final_report": {},
        "full_result": full_result,
        "full_case_record": case,
    }


def main() -> int:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    EXPERIMENT3_ROOT.mkdir(parents=True, exist_ok=True)

    if REPAIR_INPUTS_DIR.exists():
        backup = EXPERIMENT3_ROOT / f"repair_inputs_backup_{timestamp}"
        shutil.move(str(REPAIR_INPUTS_DIR), str(backup))
        print(f"Existing repair_inputs moved to: {backup}")

    REPAIR_INPUTS_DIR.mkdir(parents=True, exist_ok=True)

    exp1_json = find_latest_experiment1_json()
    print(f"Using Experiment 1 JSON: {exp1_json}")

    payload = load_json(exp1_json)
    cases = extract_cases(payload)

    repair_cases = []

    for i, case in enumerate(cases, start=1):
        expected_label = get_expected_label(case)

        if expected_label != "vulnerable":
            continue

        case_id = get_case_id(case, i)
        cwe = get_cwe(case)
        original_code = get_original_code(case)
        langgraph_report = build_langgraph_report(case)

        repair_input = {
            "case_id": case_id,
            "cwe": cwe,
            "expected_label": expected_label,
            "original_code": original_code,
            "langgraph_report": langgraph_report,
            "repair_instruction": (
                "Use the complete LangGraph security report as guidance. "
                "Generate complete fixed Python code that removes the confirmed vulnerability, "
                "preserves intended functionality, and does not introduce new vulnerabilities."
            ),
        }

        safe_case_id = (
            case_id.replace("_vulnerable", "_safe")
            if "_vulnerable" in case_id
            else case_id.replace("vulnerable", "safe")
        )

        output_path = REPAIR_INPUTS_DIR / f"{case_id}_repair_input.json"
        output_path.write_text(
            json.dumps(repair_input, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        repair_cases.append({
            "case_id": case_id,
            "cwe": cwe,
            "expected_label": expected_label,
            "repair_input_path": str(output_path),
            "has_original_code": bool(original_code.strip()),
            "report_source": langgraph_report.get("report_source", ""),
            "has_output_node_final_report": bool(langgraph_report.get("final_report")),
            "safe_counterpart_case_id_guess": safe_case_id,
        })

    manifest = {
        "generated_at": timestamp,
        "source_experiment1_json": str(exp1_json),
        "benchmark_scope": {
            "securityeval_vulnerable_tasks": 69,
            "safe_counterparts": 69,
            "total_benchmark_cases": 138,
            "repair_target_cases": len(repair_cases),
        },
        "repair_cases": repair_cases,
        "notes": [
            "This script prepares repair inputs only. It does not call the repair LLM.",
            "Each repair input prioritizes the actual output_node final_report from full_result.final_report.",
            "The repair LLM should receive the complete LangGraph report, not only the CWE label.",
        ],
    }

    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nExperiment 3 repair input preparation complete.")
    print(f"Repair cases prepared: {len(repair_cases)}")
    print(f"Repair inputs folder: {REPAIR_INPUTS_DIR}")
    print(f"Manifest: {MANIFEST_PATH}")

    report_sources = {}
    missing_code = 0
    missing_final_report = 0

    for case in repair_cases:
        report_sources[case["report_source"]] = report_sources.get(case["report_source"], 0) + 1
        if not case["has_original_code"]:
            missing_code += 1
        if not case["has_output_node_final_report"]:
            missing_final_report += 1

    print("\nVerification summary:")
    print(f"Report sources: {report_sources}")
    print(f"Cases missing original code: {missing_code}")
    print(f"Cases missing output-node final_report: {missing_final_report}")

    if len(repair_cases) != 69:
        print("\nWARNING: Expected 69 vulnerable repair cases.")
        print("Please inspect the manifest before proceeding.")

    if missing_final_report:
        print("\nWARNING: Some cases are missing output-node final_report.")
        print("Please inspect those repair inputs before proceeding.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())