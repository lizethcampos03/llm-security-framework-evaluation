"""Run the Secure Code Agent baseline vulnerability-detection experiment.

Usage from the repository root:

    python experiments/experiment2/scripts/01_detection.py

Optional controls:

    --dry-run                 Render prompts without calling the API.
    --limit 5                 Process only the first five selected samples.
    --cwe CWE-22              Process only one CWE.
    --sample-kind vulnerable  Process only vulnerable samples.
    --overwrite               Replace existing output records.
    --retry-failed            Re-run FAILED or PARSE_FAILED records.

The script uses the OpenAI Responses API. OPENAI_API_KEY must be set for live
execution. Temperature and top_p are intentionally omitted so provider/model
defaults remain in effect, matching the frozen reproduction specification.
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
from typing import Any, Iterable

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore[assignment]

SCRIPT_VERSION = "1.0.0"
STAGE_NAME = "detection"
EXPERIMENT_RELATIVE_PATH = Path("experiments/experiment2")
CONFIG_RELATIVE_PATH = EXPERIMENT_RELATIVE_PATH / "scripts/config.py"
MANIFEST_RELATIVE_PATH = EXPERIMENT_RELATIVE_PATH / "manifests/securityeval_manifest.json"
PROMPT_RELATIVE_PATH = EXPERIMENT_RELATIVE_PATH / "prompts/detection_prompt.md"
OUTPUT_RELATIVE_PATH = EXPERIMENT_RELATIVE_PATH / "outputs/detection"
LOG_RELATIVE_PATH = EXPERIMENT_RELATIVE_PATH / "logs/experiment_log.csv"

LOG_FIELDS = [
    "run_id",
    "timestamp_utc",
    "configuration",
    "stage",
    "sample_id",
    "cwe_id",
    "sample_kind",
    "model",
    "status",
    "latency_seconds",
    "input_path",
    "output_path",
    "error_message",
]


@dataclass(frozen=True)
class RuntimeConfig:
    configuration_name: str
    detection_model: str
    max_api_attempts: int = 3
    retry_base_seconds: float = 2.0
    request_timeout_seconds: float = 120.0


@dataclass
class Counters:
    selected: int = 0
    completed: int = 0
    failed: int = 0
    skipped: int = 0
    dry_run: int = 0


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
        if (candidate / MANIFEST_RELATIVE_PATH).is_file():
            return candidate
    raise FileNotFoundError(
        "Could not locate the repository root. Run 00_initialize_experiment.py first."
    )


def normalize_cwe_id(value: str) -> str:
    digits = "".join(character for character in value if character.isdigit())
    if not digits:
        raise ValueError(f"Invalid CWE identifier: {value!r}")
    return f"CWE-{int(digits)}"


def load_python_module(path: Path) -> Any:
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    spec = importlib.util.spec_from_file_location("experiment2_config", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load configuration from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_runtime_config(path: Path) -> RuntimeConfig:
    module = load_python_module(path)
    model = str(getattr(module, "DETECTION_MODEL", "")).strip()
    if not model:
        raise ValueError(
            "config.py must define DETECTION_MODEL, for example:\n"
            'DETECTION_MODEL = "your-exact-model-id"'
        )

    config = RuntimeConfig(
        configuration_name=str(
            getattr(module, "CONFIGURATION_NAME", "secure_code_agent_baseline")
        ).strip(),
        detection_model=model,
        max_api_attempts=int(getattr(module, "MAX_API_ATTEMPTS", 3)),
        retry_base_seconds=float(getattr(module, "RETRY_BASE_SECONDS", 2.0)),
        request_timeout_seconds=float(
            getattr(module, "REQUEST_TIMEOUT_SECONDS", 120.0)
        ),
    )
    if config.max_api_attempts < 1:
        raise ValueError("MAX_API_ATTEMPTS must be at least 1.")
    if config.retry_base_seconds < 0:
        raise ValueError("RETRY_BASE_SECONDS cannot be negative.")
    if config.request_timeout_seconds <= 0:
        raise ValueError("REQUEST_TIMEOUT_SECONDS must be positive.")
    return config


def validate_manifest_record(record: dict[str, Any], index: int) -> None:
    required = {
        "sample_id",
        "cwe_id",
        "cwe_definition",
        "sample_kind",
        "ground_truth_vulnerable",
        "source_code_path",
    }
    missing = sorted(required - record.keys())
    if missing:
        raise ValueError(
            f"Manifest record {index} is missing: {', '.join(missing)}"
        )
    if record["sample_kind"] not in {"safe", "vulnerable"}:
        raise ValueError(
            f"Manifest record {index} has invalid sample_kind: "
            f"{record['sample_kind']!r}"
        )
    if not isinstance(record["ground_truth_vulnerable"], bool):
        raise ValueError(
            f"Manifest record {index} must use a Boolean ground truth."
        )


def load_manifest(path: Path) -> list[dict[str, Any]]:
    raw = load_json(path)
    if not isinstance(raw, list):
        raise TypeError("The manifest must contain a JSON list.")
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise TypeError(f"Manifest record {index} is not an object.")
        validate_manifest_record(item, index)
        sample_id = str(item["sample_id"])
        if sample_id in seen:
            raise ValueError(f"Duplicate sample_id: {sample_id}")
        seen.add(sample_id)
        records.append(item)
    return records


def strip_markdown_fence(text: str) -> str:
    stripped = text.strip()
    match = re.fullmatch(
        r"```(?:text|markdown|md)?\s*(.*?)\s*```",
        stripped,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return match.group(1).strip() if match else stripped


def validate_prompt_template(template: str) -> None:
    if not template.strip():
        raise ValueError("The detection prompt file is empty.")
    if "replace this placeholder" in template.lower():
        raise ValueError(
            "The detection prompt still contains the initialization placeholder."
        )


def render_prompt(
    template: str,
    *,
    cwe_id: str,
    cwe_definition: str,
    source_code: str,
) -> str:
    """Render the frozen RQ2 prompt and append code when no code token exists."""
    cwe_number = cwe_id.split("-", maxsplit=1)[1]
    rendered = template
    replacements = {
        "<SN>": cwe_number,
        "<Definition>": cwe_definition,
        "{{CWE_ID}}": cwe_id,
        "{{CWE_NUMBER}}": cwe_number,
        "{{CWE_DEFINITION}}": cwe_definition,
    }
    for token, replacement in replacements.items():
        rendered = rendered.replace(token, replacement)

    if "{{SOURCE_CODE}}" in rendered:
        rendered = rendered.replace("{{SOURCE_CODE}}", source_code)
    else:
        rendered = (
            f"{rendered.rstrip()}\n\n"
            "Python code:\n"
            "```python\n"
            f"{source_code.rstrip()}\n"
            "```"
        )
    return rendered.strip()


def select_records(
    manifest: Iterable[dict[str, Any]],
    *,
    cwe_filter: str | None,
    sample_kind: str,
    limit: int | None,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    normalized = normalize_cwe_id(cwe_filter) if cwe_filter else None
    for record in manifest:
        if normalized and record["cwe_id"] != normalized:
            continue
        if sample_kind != "all" and record["sample_kind"] != sample_kind:
            continue
        selected.append(record)
    selected.sort(
        key=lambda item: (
            int(str(item["cwe_id"]).split("-")[1]),
            0 if item["sample_kind"] == "vulnerable" else 1,
        )
    )
    return selected[:limit] if limit is not None else selected


def create_client(timeout_seconds: float) -> Any:
    if OpenAI is None:
        raise RuntimeError(
            "The OpenAI Python package is not installed. Run:\n"
            "  python -m pip install --upgrade openai"
        )
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not defined.")
    return OpenAI(timeout=timeout_seconds)


def call_model_with_retry(
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
                input=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": prompt}
                        ],
                    }
                ],
            )
            return response, attempt
        except Exception as exc:
            last_error = exc
            if attempt >= max_attempts:
                break
            delay = retry_base_seconds * (2 ** (attempt - 1))
            delay += random.uniform(0.0, min(1.0, retry_base_seconds))
            print(
                f"    Attempt {attempt} failed ({type(exc).__name__}); "
                f"retrying in {delay:.1f}s..."
            )
            time.sleep(delay)
    assert last_error is not None
    raise last_error


def extract_response_text(response: Any) -> str:
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    fragments: list[str] = []
    for output_item in getattr(response, "output", []) or []:
        for content_item in getattr(output_item, "content", []) or []:
            text = getattr(content_item, "text", None)
            if isinstance(text, str) and text.strip():
                fragments.append(text.strip())
    if not fragments:
        raise ValueError("The model returned no readable text.")
    return "\n".join(fragments)


def serialize_sdk_object(value: Any) -> Any:
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if isinstance(value, (dict, list, str, int, float, bool)):
        return value
    return str(value)


def parse_boolean_prediction(raw_response: str) -> tuple[bool | None, str]:
    """Parse True/False while preserving ambiguous responses for review."""
    normalized = raw_response.strip()
    normalized = re.sub(
        r"^```(?:text|json|markdown)?\s*|\s*```$",
        "",
        normalized,
        flags=re.IGNORECASE,
    ).strip()

    exact = re.fullmatch(
        r"[\s\"'`]*(true|false)[\s\"'`.!]*",
        normalized,
        flags=re.IGNORECASE,
    )
    if exact:
        return exact.group(1).lower() == "true", "EXACT"

    tokens = re.findall(r"\b(true|false)\b", normalized, flags=re.IGNORECASE)
    unique = {token.lower() for token in tokens}
    if len(unique) == 1:
        return next(iter(unique)) == "true", "EMBEDDED"
    if len(unique) > 1:
        return None, "AMBIGUOUS"
    return None, "UNPARSEABLE"


def sample_output_path(output_root: Path, record: dict[str, Any]) -> Path:
    return output_root / str(record["cwe_id"]) / f"{record['sample_kind']}.json"


def existing_status(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        value = load_json(path)
    except Exception:
        return "INVALID"
    if isinstance(value, dict):
        return str(value.get("status", "UNKNOWN")).upper()
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
        "FAILED",
        "PARSE_FAILED",
        "INVALID",
        "UNKNOWN",
    }:
        return False, status
    return True, status


def append_log_row(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    needs_header = not path.exists() or path.stat().st_size == 0
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOG_FIELDS, extrasaction="ignore")
        if needs_header:
            writer.writeheader()
        writer.writerow(row)


def save_snapshot(
    *,
    output_root: Path,
    run_id: str,
    runtime_config: RuntimeConfig,
    manifest_path: Path,
    prompt_path: Path,
    config_path: Path,
    selected: list[dict[str, Any]],
    args: argparse.Namespace,
) -> Path:
    snapshot = {
        "run_id": run_id,
        "created_at_utc": utc_now(),
        "script": {
            "name": Path(__file__).name,
            "version": SCRIPT_VERSION,
            "sha256": sha256_file(Path(__file__).resolve()),
        },
        "configuration": asdict(runtime_config),
        "files": {
            "config_path": str(config_path),
            "config_sha256": sha256_file(config_path),
            "manifest_path": str(manifest_path),
            "manifest_sha256": sha256_file(manifest_path),
            "prompt_path": str(prompt_path),
            "prompt_sha256": sha256_file(prompt_path),
        },
        "selection": {
            "sample_count": len(selected),
            "sample_ids": [record["sample_id"] for record in selected],
            "filters": {
                "cwe": args.cwe,
                "sample_kind": args.sample_kind,
                "limit": args.limit,
            },
        },
        "execution_options": {
            "dry_run": args.dry_run,
            "overwrite": args.overwrite,
            "retry_failed": args.retry_failed,
        },
    }
    path = output_root / f"config_snapshot_{run_id}.json"
    write_json_atomic(path, snapshot)
    return path


def execute_sample(
    *,
    project_root: Path,
    record: dict[str, Any],
    prompt_template: str,
    runtime_config: RuntimeConfig,
    client: Any,
    output_path: Path,
    run_id: str,
    dry_run: bool,
) -> tuple[str, float, str | None]:
    started = time.perf_counter()
    source_path = project_root / str(record["source_code_path"])
    source_code = read_text(source_path)
    prompt = render_prompt(
        prompt_template,
        cwe_id=str(record["cwe_id"]),
        cwe_definition=str(record["cwe_definition"]),
        source_code=source_code,
    )

    result: dict[str, Any] = {
        "schema_version": "1.0",
        "run_id": run_id,
        "timestamp_utc": utc_now(),
        "stage": STAGE_NAME,
        "configuration": runtime_config.configuration_name,
        "sample": {
            "sample_id": record["sample_id"],
            "cwe_id": record["cwe_id"],
            "cwe_name": record.get("cwe_name", ""),
            "cwe_definition": record["cwe_definition"],
            "sample_kind": record["sample_kind"],
            "ground_truth_vulnerable": record["ground_truth_vulnerable"],
            "source_code_path": record["source_code_path"],
            "source_code_sha256": sha256_text(source_code),
            "metadata_path": record.get("metadata_path"),
            "assignment_path": record.get("assignment_path"),
            "context_profile_path": record.get("context_profile_path"),
        },
        "model": {
            "provider": "openai",
            "model_id": runtime_config.detection_model,
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
        "evaluation": None,
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
        result["execution"].update(
            {"status": "DRY_RUN", "latency_seconds": round(latency, 6)}
        )
        result["status"] = "DRY_RUN"
        write_json_atomic(output_path, result)
        return "DRY_RUN", latency, None

    try:
        response, attempts = call_model_with_retry(
            client,
            model=runtime_config.detection_model,
            prompt=prompt,
            max_attempts=runtime_config.max_api_attempts,
            retry_base_seconds=runtime_config.retry_base_seconds,
        )
        raw_text = extract_response_text(response)
        prediction, parse_status = parse_boolean_prediction(raw_text)
        latency = time.perf_counter() - started
        ground_truth = bool(record["ground_truth_vulnerable"])
        status = "SUCCESS" if prediction is not None else "PARSE_FAILED"

        usage = serialize_sdk_object(getattr(response, "usage", None))
        result["response"] = {
            "response_id": getattr(response, "id", None),
            "raw_text": raw_text,
            "prediction_vulnerable": prediction,
            "parse_status": parse_status,
            "usage": usage if isinstance(usage, dict) else None,
            "raw_response_object": serialize_sdk_object(response),
        }
        result["evaluation"] = {
            "ground_truth_vulnerable": ground_truth,
            "prediction_vulnerable": prediction,
            "correct": prediction == ground_truth if prediction is not None else None,
        }
        result["execution"].update(
            {
                "status": status,
                "attempts": attempts,
                "latency_seconds": round(latency, 6),
            }
        )
        result["status"] = status
        write_json_atomic(output_path, result)
        return status, latency, None

    except Exception as exc:
        latency = time.perf_counter() - started
        message = str(exc)
        result["execution"].update(
            {
                "status": "FAILED",
                "latency_seconds": round(latency, 6),
                "error_type": type(exc).__name__,
                "error_message": message,
            }
        )
        result["status"] = "FAILED"
        write_json_atomic(output_path, result)
        return "FAILED", latency, message


def save_summary(
    *,
    output_root: Path,
    run_id: str,
    runtime_config: RuntimeConfig,
    counters: Counters,
    started_at_utc: str,
    elapsed_seconds: float,
    latencies: list[float],
    snapshot_path: Path,
) -> Path:
    summary = {
        "run_id": run_id,
        "stage": STAGE_NAME,
        "configuration": runtime_config.configuration_name,
        "model": runtime_config.detection_model,
        "started_at_utc": started_at_utc,
        "finished_at_utc": utc_now(),
        "elapsed_seconds": round(elapsed_seconds, 6),
        "selected_samples": counters.selected,
        "completed_samples": counters.completed,
        "failed_samples": counters.failed,
        "skipped_samples": counters.skipped,
        "dry_run_samples": counters.dry_run,
        "average_api_latency_seconds": (
            round(sum(latencies) / len(latencies), 6) if latencies else None
        ),
        "minimum_api_latency_seconds": round(min(latencies), 6) if latencies else None,
        "maximum_api_latency_seconds": round(max(latencies), 6) if latencies else None,
        "config_snapshot_path": str(snapshot_path),
        "metrics_computed": False,
        "metrics_note": "Detection metrics are deferred to 04_metrics.py.",
    }
    path = output_root / f"detection_summary_{run_id}.json"
    write_json_atomic(path, summary)
    write_json_atomic(output_root / "detection_summary_latest.json", summary)
    return path


def print_progress(
    position: int,
    total: int,
    record: dict[str, Any],
    status: str,
    latency: float | None = None,
) -> None:
    suffix = f" | {latency:.2f}s" if latency is not None else ""
    print(
        f"[{position:>3}/{total}] "
        f"{record['cwe_id']:<8} "
        f"{str(record['sample_kind']).upper():<10} "
        f"{status}{suffix}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run GPT-based vulnerability detection over the manifest."
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--cwe", type=str, default=None)
    parser.add_argument(
        "--sample-kind",
        choices=("all", "safe", "vulnerable"),
        default="all",
    )
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
    script_path = Path(__file__).resolve()

    try:
        project_root = find_project_root(script_path.parent)
        config_path = project_root / CONFIG_RELATIVE_PATH
        manifest_path = project_root / MANIFEST_RELATIVE_PATH
        prompt_path = project_root / PROMPT_RELATIVE_PATH
        output_root = project_root / OUTPUT_RELATIVE_PATH
        log_path = project_root / LOG_RELATIVE_PATH
        output_root.mkdir(parents=True, exist_ok=True)

        runtime_config = load_runtime_config(config_path)
        manifest = load_manifest(manifest_path)
        prompt_template = strip_markdown_fence(read_text(prompt_path))
        validate_prompt_template(prompt_template)
        selected = select_records(
            manifest,
            cwe_filter=args.cwe,
            sample_kind=args.sample_kind,
            limit=args.limit,
        )
        if not selected:
            raise ValueError("No manifest records matched the selected filters.")
        client = None if args.dry_run else create_client(
            runtime_config.request_timeout_seconds
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    run_id = (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        + "_"
        + uuid.uuid4().hex[:8]
    )
    started_at_utc = utc_now()
    started = time.perf_counter()
    snapshot_path = save_snapshot(
        output_root=output_root,
        run_id=run_id,
        runtime_config=runtime_config,
        manifest_path=manifest_path,
        prompt_path=prompt_path,
        config_path=config_path,
        selected=selected,
        args=args,
    )

    print("\nSecure Code Agent Baseline — Detection")
    print("--------------------------------------")
    print(f"Run ID:        {run_id}")
    print(f"Model:         {runtime_config.detection_model}")
    print(f"Configuration: {runtime_config.configuration_name}")
    print(f"Selected:      {len(selected)}")
    print(f"Dry run:       {args.dry_run}\n")

    counters = Counters(selected=len(selected))
    successful_latencies: list[float] = []

    for position, record in enumerate(selected, start=1):
        output_path = sample_output_path(output_root, record)
        skip, status_before = should_skip(
            output_path,
            overwrite=args.overwrite,
            retry_failed=args.retry_failed,
        )
        if skip:
            counters.skipped += 1
            print_progress(
                position,
                len(selected),
                record,
                f"SKIPPED ({status_before})",
            )
            continue

        source_path = project_root / str(record["source_code_path"])
        status, latency, error_message = execute_sample(
            project_root=project_root,
            record=record,
            prompt_template=prompt_template,
            runtime_config=runtime_config,
            client=client,
            output_path=output_path,
            run_id=run_id,
            dry_run=args.dry_run,
        )

        if status == "SUCCESS":
            counters.completed += 1
            successful_latencies.append(latency)
        elif status == "DRY_RUN":
            counters.dry_run += 1
        else:
            counters.failed += 1

        append_log_row(
            log_path,
            {
                "run_id": run_id,
                "timestamp_utc": utc_now(),
                "configuration": runtime_config.configuration_name,
                "stage": STAGE_NAME,
                "sample_id": record["sample_id"],
                "cwe_id": record["cwe_id"],
                "sample_kind": record["sample_kind"],
                "model": runtime_config.detection_model,
                "status": status,
                "latency_seconds": round(latency, 6),
                "input_path": source_path.relative_to(project_root).as_posix(),
                "output_path": output_path.relative_to(project_root).as_posix(),
                "error_message": error_message or "",
            },
        )
        print_progress(position, len(selected), record, status, latency)

    elapsed = time.perf_counter() - started
    summary_path = save_summary(
        output_root=output_root,
        run_id=run_id,
        runtime_config=runtime_config,
        counters=counters,
        started_at_utc=started_at_utc,
        elapsed_seconds=elapsed,
        latencies=successful_latencies,
        snapshot_path=snapshot_path,
    )

    print("\nDetection run complete.")
    print(f"  Completed: {counters.completed}")
    print(f"  Failed:    {counters.failed}")
    print(f"  Skipped:   {counters.skipped}")
    print(f"  Dry run:   {counters.dry_run}")
    print(f"  Summary:   {summary_path}")

    if counters.failed:
        print(
            "\nReview failed records, then rerun with --retry-failed.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
