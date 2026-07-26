from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

ROOT = Path.cwd()
DEFAULT_EXPERIMENT_ROOT = ROOT / "outputs" / "experiment3_repair"
DEFAULT_MANIFEST_PATH = DEFAULT_EXPERIMENT_ROOT / "experiment3_repair_manifest.json"

DEFAULT_MODEL = "gpt-5.5"
DEFAULT_RUN_LABEL = "gpt5_5"
EXPECTED_CASES = 69

SYSTEM_MESSAGE = (
    "You are a secure Python code repair assistant. "
    "Return only complete fixed Python code."
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    temporary.replace(path)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sanitize_label(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    cleaned = cleaned.strip("._-")
    if not cleaned:
        raise ValueError("Run label cannot be empty.")
    return cleaned


def extract_code(text: str) -> str:
    # This intentionally preserves the extraction behavior used in the GPT-4 run.
    fenced = re.search(
        r"```(?:python)?\s*(.*?)```",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if fenced:
        return fenced.group(1).strip()
    return text.strip()


def compact_report(repair_input: dict[str, Any]) -> dict[str, Any]:
    # This intentionally preserves the exact GPT-4 compact-report fields.
    report_wrapper = repair_input.get("langgraph_report", {})
    final_report = report_wrapper.get("final_report", {})
    full_result = report_wrapper.get("full_result", {})

    return {
        "case_id": repair_input.get("case_id"),
        "cwe": repair_input.get("cwe"),
        "original_code": repair_input.get("original_code", ""),
        "executive_summary": final_report.get("executive_summary", {}),
        "security_findings": final_report.get("security_findings", []),
        "false_positive_considerations": final_report.get(
            "false_positive_considerations", []
        ),
        "reasoning_summary": final_report.get("reasoning_summary", ""),
        "fix_recommendation": final_report.get("fix_recommendation", {}),
        "validation_evidence": final_report.get("validation_evidence", {}),
        "comparison_ready": final_report.get("comparison_ready", {}),
        "retrieved_context_summary": {
            "retrieved_cwe_record_count": final_report.get(
                "rag_evidence", {}
            ).get("retrieved_cwe_record_count"),
            "retrieved_vulnerable_example_count": final_report.get(
                "rag_evidence", {}
            ).get("retrieved_vulnerable_example_count"),
            "retrieved_safe_counterpart_count": final_report.get(
                "rag_evidence", {}
            ).get("retrieved_safe_counterpart_count"),
        },
        "detection_result": full_result.get("detection_result", {}),
    }


def build_prompt(repair_input: dict[str, Any]) -> str:
    # Do not revise this prompt for the GPT-5.5 comparison.
    # It matches the prompt used in the GPT-4 repair experiment.
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


def resolve_repair_input_path(
    manifest_value: str,
    repair_inputs_dir: Path,
) -> Path:
    recorded = Path(manifest_value)

    # Use the recorded path when it is valid on the current machine.
    if recorded.exists():
        return recorded.resolve()

    # Historical manifest paths are absolute Windows paths. Resolve their
    # filename against the frozen local repair-input directory.
    candidate = repair_inputs_dir / recorded.name
    if candidate.exists():
        return candidate.resolve()

    raise FileNotFoundError(
        f"Repair input not found. Recorded path: {recorded}; "
        f"local candidate: {candidate}"
    )


def get_final_status(repair_input: dict[str, Any]) -> str:
    value = (
        repair_input.get("langgraph_report", {})
        .get("final_report", {})
        .get("executive_summary", {})
        .get("final_status", "")
    )
    return str(value).strip().lower()


def validate_inputs(
    manifest: dict[str, Any],
    repair_inputs_dir: Path,
    expected_cases: int,
) -> list[dict[str, Any]]:
    repair_cases = manifest.get("repair_cases", [])
    if not isinstance(repair_cases, list):
        raise ValueError("Manifest field 'repair_cases' must be a list.")

    errors: list[str] = []
    seen_case_ids: set[str] = set()
    validated: list[dict[str, Any]] = []

    if len(repair_cases) != expected_cases:
        errors.append(
            f"Expected {expected_cases} manifest cases, found {len(repair_cases)}."
        )

    for position, case_meta in enumerate(repair_cases, start=1):
        case_id = str(case_meta.get("case_id", "")).strip()
        manifest_cwe = str(case_meta.get("cwe", "")).strip()

        if not case_id:
            errors.append(f"Manifest case {position} has no case_id.")
            continue

        if case_id in seen_case_ids:
            errors.append(f"Duplicate manifest case_id: {case_id}")
            continue
        seen_case_ids.add(case_id)

        try:
            input_path = resolve_repair_input_path(
                str(case_meta.get("repair_input_path", "")),
                repair_inputs_dir,
            )
            repair_input = load_json(input_path)
        except Exception as exc:
            errors.append(f"{case_id}: cannot load repair input: {exc}")
            continue

        input_case_id = str(repair_input.get("case_id", "")).strip()
        input_cwe = str(repair_input.get("cwe", "")).strip()
        original_code = repair_input.get("original_code", "")
        report = repair_input.get("langgraph_report", {})
        final_report = report.get("final_report", {}) if isinstance(report, dict) else {}

        if input_case_id != case_id:
            errors.append(
                f"{case_id}: input case_id is {input_case_id!r}."
            )
        if input_cwe != manifest_cwe:
            errors.append(
                f"{case_id}: manifest CWE {manifest_cwe!r} "
                f"does not match input CWE {input_cwe!r}."
            )
        if not isinstance(original_code, str) or not original_code.strip():
            errors.append(f"{case_id}: original_code is missing or empty.")
        if not isinstance(final_report, dict) or not final_report:
            errors.append(f"{case_id}: LangGraph final_report is missing.")

        prompt = build_prompt(repair_input)
        validated.append(
            {
                "case_id": case_id,
                "cwe": manifest_cwe,
                "repair_input_path": input_path,
                "repair_input": repair_input,
                "input_sha256": sha256_file(input_path),
                "prompt": prompt,
                "prompt_sha256": sha256_text(prompt),
                "langgraph_final_status": get_final_status(repair_input),
            }
        )

    if errors:
        formatted = "\n".join(f"- {item}" for item in errors)
        raise ValueError(
            "Frozen repair-input verification failed:\n" + formatted
        )

    return validated


def call_repair_model(
    client: OpenAI,
    model: str,
    prompt: str,
) -> tuple[str, str | None, dict[str, Any]]:
    # Chat Completions and the historical message structure are retained.
    # GPT-5.5 uses its model-default inference configuration.
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt},
        ],
    )

    raw_output = response.choices[0].message.content or ""
    response_id = getattr(response, "id", None)

    usage = getattr(response, "usage", None)
    usage_dict: dict[str, Any] = {}
    if usage is not None:
        if hasattr(usage, "model_dump"):
            usage_dict = usage.model_dump()
        else:
            usage_dict = {
                "prompt_tokens": getattr(usage, "prompt_tokens", None),
                "completion_tokens": getattr(usage, "completion_tokens", None),
                "total_tokens": getattr(usage, "total_tokens", None),
            }

    return raw_output, response_id, usage_dict


def is_syntax_valid_python(code: str) -> tuple[bool, str]:
    if not code.strip():
        return False, "Empty output."
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as exc:
        return False, f"{exc.__class__.__name__}: {exc}"


def load_existing_results(checkpoint_path: Path) -> list[dict[str, Any]]:
    if not checkpoint_path.exists():
        return []
    payload = load_json(checkpoint_path)
    results = payload.get("results", [])
    if not isinstance(results, list):
        raise ValueError(f"Invalid checkpoint results: {checkpoint_path}")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the frozen LangGraph repair inputs with GPT-5.5 while "
            "preserving the completed GPT-4 experiment."
        )
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--run-label", default=DEFAULT_RUN_LABEL)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--repair-inputs-dir", type=Path, default=None)
    parser.add_argument("--output-root", type=Path, default=None)
    parser.add_argument("--expected-cases", type=int, default=EXPECTED_CASES)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=5.0)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reuse successful records from the run checkpoint.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacement of existing per-case output files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Verify inputs and write metadata without calling the API.",
    )
    args = parser.parse_args()

    if args.start_index < 0:
        raise ValueError("--start-index cannot be negative.")
    if args.limit is not None and args.limit < 1:
        raise ValueError("--limit must be at least 1.")
    if args.max_retries < 1:
        raise ValueError("--max-retries must be at least 1.")

    manifest_path = args.manifest.resolve()
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    experiment_root = manifest_path.parent
    repair_inputs_dir = (
        args.repair_inputs_dir.resolve()
        if args.repair_inputs_dir
        else (experiment_root / "repair_inputs").resolve()
    )

    run_label = sanitize_label(args.run_label)
    output_root = (
        args.output_root.resolve()
        if args.output_root
        else (experiment_root / "model_comparison" / run_label).resolve()
    )

    repaired_code_dir = output_root / "repaired_code"
    raw_outputs_dir = output_root / "raw_outputs"
    prompts_dir = output_root / "prompts"
    case_results_dir = output_root / "case_results"
    run_metadata_dir = output_root / "run_metadata"
    checkpoint_path = output_root / "repair_llm_checkpoint.json"

    for directory in [
        repaired_code_dir,
        raw_outputs_dir,
        prompts_dir,
        case_results_dir,
        run_metadata_dir,
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    manifest = load_json(manifest_path)
    validated_cases = validate_inputs(
        manifest=manifest,
        repair_inputs_dir=repair_inputs_dir,
        expected_cases=args.expected_cases,
    )

    all_case_ids = [case["case_id"] for case in validated_cases]
    safe_report_cases = [
        case["case_id"]
        for case in validated_cases
        if case["langgraph_final_status"] == "safe"
    ]
    vulnerable_report_cases = [
        case["case_id"]
        for case in validated_cases
        if case["langgraph_final_status"] == "vulnerable"
    ]
    other_status_cases = [
        case["case_id"]
        for case in validated_cases
        if case["langgraph_final_status"] not in {"safe", "vulnerable"}
    ]

    selected_cases = validated_cases[args.start_index :]
    if args.limit is not None:
        selected_cases = selected_cases[: args.limit]

    generated_at = datetime.now(timezone.utc).isoformat()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    configuration = {
        "generated_at_utc": generated_at,
        "experiment": "LangGraph End-to-End Workflow Repair Comparison",
        "run_label": run_label,
        "model_requested": args.model,
        "api_endpoint": "chat.completions.create",
        "inference_configuration": {
            "temperature": "model_default"
        },
        "system_message": SYSTEM_MESSAGE,
        "prompt_method": "historical_gpt4_prompt_preserved",
        "manifest_path": str(manifest_path),
        "manifest_sha256": sha256_file(manifest_path),
        "repair_inputs_dir": str(repair_inputs_dir),
        "expected_cases": args.expected_cases,
        "verified_manifest_cases": len(validated_cases),
        "selected_cases": len(selected_cases),
        "start_index": args.start_index,
        "limit": args.limit,
        "all_case_ids": all_case_ids,
        "langgraph_report_status_counts": {
            "vulnerable": len(vulnerable_report_cases),
            "safe": len(safe_report_cases),
            "other_or_missing": len(other_status_cases),
        },
        "safe_report_case_ids": safe_report_cases,
        "other_or_missing_status_case_ids": other_status_cases,
        "input_fingerprints": {
            case["case_id"]: {
                "input_sha256": case["input_sha256"],
                "prompt_sha256": case["prompt_sha256"],
            }
            for case in validated_cases
        },
        "dry_run": args.dry_run,
    }
    save_json(
        run_metadata_dir / f"run_configuration_{timestamp}.json",
        configuration,
    )

    # Prompts are written before API execution so the exact model input is
    # preserved even if the run is interrupted.
    for case in selected_cases:
        prompt_path = prompts_dir / f"{case['case_id']}_{case['cwe']}_prompt.txt"
        
        if prompt_path.exists() and not args.overwrite:
            existing_prompt = prompt_path.read_text(
                encoding="utf-8",
                errors="replace",
            )
            existing_hash = sha256_text(existing_prompt)
            expected_hash = sha256_text(case["prompt"])

            if existing_hash != expected_hash:
                raise FileExistsError(
                    f"Existing prompt differs from the frozen prompt: {prompt_path}"
                )
        else:
            prompt_path.write_text(case["prompt"], encoding="utf-8")

    print("Frozen repair-input verification: PASS")
    print(f"Manifest cases verified: {len(validated_cases)}")
    print(f"LangGraph vulnerable reports: {len(vulnerable_report_cases)}")
    print(f"LangGraph safe reports: {len(safe_report_cases)}")
    print(f"Cases selected for this invocation: {len(selected_cases)}")
    print(f"Model: {args.model}")
    print(f"Output root: {output_root}")

    if args.dry_run:
        print("\nDry run complete. No API requests were made.")
        return 0

    client = OpenAI()

    existing_results = load_existing_results(checkpoint_path) if args.resume else []
    successful_by_case = {
        str(result.get("case_id")): result
        for result in existing_results
        if result.get("repair_generated") and not result.get("error")
    }
    results_by_case = {
        str(result.get("case_id")): result for result in existing_results
    }

    for ordinal, case in enumerate(
        selected_cases,
        start=args.start_index + 1,
    ):
        case_id = case["case_id"]
        cwe = case["cwe"]
        prompt = case["prompt"]

        if args.resume and case_id in successful_by_case:
            print(f"\n[{ordinal}] Skipping completed case {case_id} ({cwe})")
            continue

        repaired_path = repaired_code_dir / f"{case_id}_{cwe}_repaired.py"
        raw_output_path = raw_outputs_dir / f"{case_id}_{cwe}_raw.txt"
        case_result_path = case_results_dir / f"{case_id}_{cwe}_result.json"

        if (
            not args.overwrite
            and not args.resume
            and any(
                path.exists()
                for path in [repaired_path, raw_output_path, case_result_path]
            )
        ):
            raise FileExistsError(
                f"Output already exists for {case_id}. "
                "Use a new --run-label, --resume, or --overwrite."
            )

        print(f"\n[{ordinal}] Repairing {case_id} ({cwe})")

        result: dict[str, Any] | None = None

        for attempt in range(1, args.max_retries + 1):
            started = time.perf_counter()
            try:
                raw_output, response_id, usage = call_repair_model(
                    client=client,
                    model=args.model,
                    prompt=prompt,
                )
                latency = round(time.perf_counter() - started, 3)
                fixed_code = extract_code(raw_output)
                syntax_valid, syntax_error = is_syntax_valid_python(fixed_code)

                repaired_path.write_text(fixed_code, encoding="utf-8")
                raw_output_path.write_text(raw_output, encoding="utf-8")

                result = {
                    "case_id": case_id,
                    "cwe": cwe,
                    "model": args.model,
                    "run_label": run_label,
                    "repair_input_path": str(case["repair_input_path"]),
                    "repair_input_sha256": case["input_sha256"],
                    "prompt_path": str(
                        prompts_dir / f"{case_id}_{cwe}_prompt.txt"
                    ),
                    "prompt_sha256": case["prompt_sha256"],
                    "repaired_code_path": str(repaired_path),
                    "repaired_code_sha256": sha256_file(repaired_path),
                    "raw_output_path": str(raw_output_path),
                    "raw_output_sha256": sha256_file(raw_output_path),
                    "langgraph_final_status": case[
                        "langgraph_final_status"
                    ],
                    "repair_generated": bool(fixed_code.strip()),
                    "syntax_valid_python": syntax_valid,
                    "syntax_error": syntax_error,
                    "latency_seconds": latency,
                    "attempts": attempt,
                    "response_id": response_id,
                    "usage": usage,
                    "error": "",
                }

                print(f"Saved: {repaired_path}")
                print(f"Latency: {latency}s")
                print(f"Python syntax valid: {syntax_valid}")
                break

            except Exception as exc:
                latency = round(time.perf_counter() - started, 3)
                error_message = f"{exc.__class__.__name__}: {exc}"
                print(
                    f"Attempt {attempt}/{args.max_retries} failed: "
                    f"{error_message}"
                )

                if attempt < args.max_retries:
                    time.sleep(args.retry_delay * attempt)
                    continue

                result = {
                    "case_id": case_id,
                    "cwe": cwe,
                    "model": args.model,
                    "run_label": run_label,
                    "repair_input_path": str(case["repair_input_path"]),
                    "repair_input_sha256": case["input_sha256"],
                    "prompt_path": str(
                        prompts_dir / f"{case_id}_{cwe}_prompt.txt"
                    ),
                    "prompt_sha256": case["prompt_sha256"],
                    "repaired_code_path": "",
                    "repaired_code_sha256": "",
                    "raw_output_path": "",
                    "raw_output_sha256": "",
                    "langgraph_final_status": case[
                        "langgraph_final_status"
                    ],
                    "repair_generated": False,
                    "syntax_valid_python": False,
                    "syntax_error": "",
                    "latency_seconds": latency,
                    "attempts": attempt,
                    "response_id": None,
                    "usage": {},
                    "error": error_message,
                }

        assert result is not None
        save_json(case_result_path, result)
        results_by_case[case_id] = result

        ordered_checkpoint_results = [
            results_by_case[cid]
            for cid in all_case_ids
            if cid in results_by_case
        ]
        save_json(
            checkpoint_path,
            {
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "model": args.model,
                "run_label": run_label,
                "results": ordered_checkpoint_results,
            },
        )

        time.sleep(args.sleep)

    selected_ids = {case["case_id"] for case in selected_cases}
    final_results = [
        results_by_case[case_id]
        for case_id in all_case_ids
        if case_id in selected_ids and case_id in results_by_case
    ]

    final_payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "run_label": run_label,
        "configuration_path": str(
            run_metadata_dir / f"run_configuration_{timestamp}.json"
        ),
        "selected_cases": len(selected_cases),
        "total_case_records": len(final_results),
        "repairs_generated": sum(
            1 for result in final_results if result["repair_generated"]
        ),
        "syntax_valid_repairs": sum(
            1 for result in final_results
            if result.get("syntax_valid_python")
        ),
        "failed_cases": [
            result["case_id"]
            for result in final_results
            if result.get("error")
        ],
        "results": final_results,
    }

    final_path = (
        output_root
        / f"experiment3_repair_llm_results_{run_label}_{timestamp}.json"
    )
    save_json(final_path, final_payload)

    reproducibility_manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": (
            "complete"
            if len(final_results) == len(selected_cases)
            and not final_payload["failed_cases"]
            else "incomplete"
        ),
        "model": args.model,
        "run_label": run_label,
        "manifest_sha256": configuration["manifest_sha256"],
        "case_count": len(final_results),
        "successful_generation_count": final_payload[
            "repairs_generated"
        ],
        "syntax_valid_count": final_payload["syntax_valid_repairs"],
        "failed_case_ids": final_payload["failed_cases"],
        "result_file": str(final_path),
        "result_file_sha256": sha256_file(final_path),
        "checkpoint_file": str(checkpoint_path),
        "output_root": str(output_root),
    }
    save_json(
        run_metadata_dir
        / f"reproducibility_manifest_{run_label}_{timestamp}.json",
        reproducibility_manifest,
    )

    print("\nRepair LLM run complete.")
    print(f"Final results: {final_path}")
    print(f"Repaired code: {repaired_code_dir}")
    print(f"Raw outputs: {raw_outputs_dir}")
    print(f"Saved prompts: {prompts_dir}")
    print(f"Failed cases: {len(final_payload['failed_cases'])}")

    if len(final_results) != len(selected_cases):
        print(
            "WARNING: The final result count does not match the selected "
            "case count. Resume the run before evaluation."
        )
        return 2

    if final_payload["failed_cases"]:
        print(
            "WARNING: Some cases failed. Resume the run before evaluation."
        )
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
