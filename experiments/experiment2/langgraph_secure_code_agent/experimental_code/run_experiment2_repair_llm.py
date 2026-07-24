from __future__ import annotations

import argparse
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

ROOT = Path.cwd()
EXPERIMENT3_ROOT = ROOT / "outputs" / "experiment3_repair"
MANIFEST_PATH = EXPERIMENT3_ROOT / "experiment3_repair_manifest.json"
REPAIRED_CODE_DIR = EXPERIMENT3_ROOT / "repaired_code"
REPAIR_RESULTS_DIR = EXPERIMENT3_ROOT / "repair_llm_results"


DEFAULT_MODEL = "GPT-4-0613"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def save_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def extract_code(text: str) -> str:
    fenced = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        return fenced.group(1).strip()
    return text.strip()

def compact_report(repair_input: dict[str, Any]) -> dict[str, Any]:
    report_wrapper = repair_input.get("langgraph_report", {})
    final_report = report_wrapper.get("final_report", {})
    full_result = report_wrapper.get("full_result", {})

    return {
        "case_id": repair_input.get("case_id"),
        "cwe": repair_input.get("cwe"),
        "original_code": repair_input.get("original_code", ""),
        "executive_summary": final_report.get("executive_summary", {}),
        "security_findings": final_report.get("security_findings", []),
        "false_positive_considerations": final_report.get("false_positive_considerations", []),
        "reasoning_summary": final_report.get("reasoning_summary", ""),
        "fix_recommendation": final_report.get("fix_recommendation", {}),
        "validation_evidence": final_report.get("validation_evidence", {}),
        "comparison_ready": final_report.get("comparison_ready", {}),
        "retrieved_context_summary": {
            "retrieved_cwe_record_count": final_report.get("rag_evidence", {}).get("retrieved_cwe_record_count"),
            "retrieved_vulnerable_example_count": final_report.get("rag_evidence", {}).get("retrieved_vulnerable_example_count"),
            "retrieved_safe_counterpart_count": final_report.get("rag_evidence", {}).get("retrieved_safe_counterpart_count"),
        },
        "detection_result": full_result.get("detection_result", {}),
    }

def build_prompt(repair_input: dict[str, Any]) -> str:
    return f"""
You will be provided with a complete LangGraph security audit report for a Python code sample.

Your task is to generate the complete final fixed Python code.

Requirements:
- Remove the confirmed vulnerability.
- Preserve the intended functionality.
- Do not introduce new vulnerabilities.
- Use the evidence, reasoning, and remediation guidance from the report.
- If the report includes candidate fixed code, use it as guidance but verify and improve it if necessary.
- Return only the complete fixed Python code.
- Do not include markdown, explanations, or commentary.

CASE ID:
{repair_input.get("case_id")}

CWE:
{repair_input.get("cwe")}

ORIGINAL CODE:
{repair_input.get("original_code", "")}

LANGGRAPH SECURITY REPORT:
{json.dumps(compact_report(repair_input), indent=2, ensure_ascii=False)}
""".strip()


def call_repair_model(client: OpenAI, model: str, prompt: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a secure Python code repair assistant. "
                    "Return only complete fixed Python code."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    return response.choices[0].message.content or ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--sleep", type=float, default=0.5)
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest not found: {MANIFEST_PATH}")

    REPAIRED_CODE_DIR.mkdir(parents=True, exist_ok=True)
    REPAIR_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    manifest = load_json(MANIFEST_PATH)
    repair_cases = manifest.get("repair_cases", [])

    selected_cases = repair_cases[args.start_index:]
    if args.limit is not None:
        selected_cases = selected_cases[:args.limit]

    client = OpenAI()

    results = []

    print(f"Experiment 3 repair LLM runner")
    print(f"Model: {args.model}")
    print(f"Cases selected: {len(selected_cases)}")

    for index, case_meta in enumerate(selected_cases, start=args.start_index + 1):
        case_id = case_meta["case_id"]
        cwe = case_meta.get("cwe", "")
        repair_input_path = Path(case_meta["repair_input_path"])

        print(f"\n[{index}] Repairing {case_id} ({cwe})")

        repair_input = load_json(repair_input_path)
        prompt = build_prompt(repair_input)

        started = time.time()

        try:
            raw_output = call_repair_model(client, args.model, prompt)
            fixed_code = extract_code(raw_output)
            latency = round(time.time() - started, 3)

            repaired_path = REPAIRED_CODE_DIR / f"{case_id}_{cwe}_repaired.py"
            repaired_path.write_text(fixed_code, encoding="utf-8")

            result = {
                "case_id": case_id,
                "cwe": cwe,
                "repair_input_path": str(repair_input_path),
                "repaired_code_path": str(repaired_path),
                "model": args.model,
                "repair_generated": bool(fixed_code.strip()),
                "latency_seconds": latency,
                "error": "",
                "raw_output": raw_output,
            }

            print(f"Saved: {repaired_path}")
            print(f"Latency: {latency}s")

        except Exception as exc:
            result = {
                "case_id": case_id,
                "cwe": cwe,
                "repair_input_path": str(repair_input_path),
                "repaired_code_path": "",
                "model": args.model,
                "repair_generated": False,
                "latency_seconds": round(time.time() - started, 3),
                "error": str(exc),
                "raw_output": "",
            }

            print(f"ERROR: {exc}")

        results.append(result)

        partial_path = REPAIR_RESULTS_DIR / f"experiment3_repair_llm_partial_{timestamp}.json"
        save_json(partial_path, {
            "generated_at": timestamp,
            "model": args.model,
            "results": results,
        })

        time.sleep(args.sleep)

    final_path = REPAIR_RESULTS_DIR / f"experiment3_repair_llm_results_{timestamp}.json"
    save_json(final_path, {
        "generated_at": timestamp,
        "model": args.model,
        "total_cases_attempted": len(results),
        "repairs_generated": sum(1 for r in results if r["repair_generated"]),
        "results": results,
    })

    print("\nRepair LLM run complete.")
    print(f"Results: {final_path}")
    print(f"Repaired code folder: {REPAIRED_CODE_DIR}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())