from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path.cwd()
DATASET_DIR = ROOT / "embedding_candidates" / "approved"
OUTPUT_DIR = ROOT / "outputs" / "experiment2_static_baselines"
CODEQL_SUITE = "codeql/python-queries:codeql-suites/python-security-and-quality.qls"


def run_command(command: list[str], cwd: Path | None = None, timeout: int = 300) -> tuple[int, str, str, float]:
    start = time.time()
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        return result.returncode, result.stdout, result.stderr, round(time.time() - start, 3)
    except subprocess.TimeoutExpired as e:
        return 124, e.stdout or "", e.stderr or "TIMEOUT", round(time.time() - start, 3)


def discover_cases() -> list[dict[str, Any]]:
    cases = []

    if not DATASET_DIR.exists():
        raise FileNotFoundError(f"Dataset folder not found: {DATASET_DIR}")

    for cwe_dir in sorted(DATASET_DIR.iterdir()):
        if not cwe_dir.is_dir():
            continue
        if not cwe_dir.name.upper().startswith("CWE"):
            continue

        cwe = cwe_dir.name.replace(" ", "-")

        vulnerable_file = cwe_dir / "candidate_a.py"
        safe_file = cwe_dir / "candidate_b.py"

        if vulnerable_file.exists():
            cases.append({
                "case_id": f"{cwe}_vulnerable",
                "cwe": cwe,
                "expected_label": "vulnerable",
                "file_path": str(vulnerable_file),
                "file_name": vulnerable_file.name,
            })

        if safe_file.exists():
            cases.append({
                "case_id": f"{cwe}_safe",
                "cwe": cwe,
                "expected_label": "safe",
                "file_path": str(safe_file),
                "file_name": safe_file.name,
            })

    return cases


def classify_detection(expected_label: str, detected: bool) -> dict[str, Any]:
    detected_label = "vulnerable" if detected else "safe"

    if expected_label == "vulnerable" and detected:
        outcome = "TP"
        correct = "Yes"
    elif expected_label == "vulnerable" and not detected:
        outcome = "FN"
        correct = "No"
    elif expected_label == "safe" and detected:
        outcome = "FP"
        correct = "No"
    else:
        outcome = "TN"
        correct = "Yes"

    return {
        "detected_label": detected_label,
        "correct": correct,
        "outcome": outcome,
    }


def run_bandit(case: dict[str, Any]) -> dict[str, Any]:
    command = [
        "bandit",
        "-f", "json",
        "-q",
        case["file_path"],
    ]

    returncode, stdout, stderr, latency = run_command(command, timeout=120)

    findings = []
    parse_error = ""

    try:
        data = json.loads(stdout) if stdout.strip() else {}
        findings = data.get("results", []) or []
    except Exception as e:
        parse_error = str(e)

    detected = len(findings) > 0
    classification = classify_detection(case["expected_label"], detected)

    cwe_ids = []
    test_ids = []
    issue_texts = []

    for finding in findings:
        test_id = finding.get("test_id", "")
        test_name = finding.get("test_name", "")
        issue_text = finding.get("issue_text", "")
        issue_cwe = finding.get("issue_cwe", {})

        test_ids.append(test_id)
        issue_texts.append(f"{test_id} {test_name}: {issue_text}".strip())

        if isinstance(issue_cwe, dict):
            cwe_id = issue_cwe.get("id")
            if cwe_id:
                cwe_ids.append(f"CWE-{cwe_id}")

    return {
        **case,
        "tool": "bandit",
        "detected": "Yes" if detected else "No",
        **classification,
        "finding_count": len(findings),
        "predicted_cwes": "; ".join(sorted(set(cwe_ids))),
        "rule_ids": "; ".join(sorted(set(test_ids))),
        "evidence": " | ".join(issue_texts[:5]),
        "returncode": returncode,
        "latency_seconds": latency,
        "error": parse_error or stderr.strip(),
    }


def run_codeql(case: dict[str, Any], temp_root: Path) -> dict[str, Any]:
    source_file = Path(case["file_path"])
    safe_case_name = case["case_id"].replace(":", "_").replace("/", "_").replace("\\", "_")
    work_dir = temp_root / safe_case_name
    src_dir = work_dir / "src"
    db_dir = work_dir / "db"
    sarif_path = work_dir / "results.sarif"

    if work_dir.exists():
        shutil.rmtree(work_dir)

    src_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, src_dir / source_file.name)

    create_command = [
        "codeql",
        "database",
        "create",
        str(db_dir),
        "--language=python",
        f"--source-root={src_dir}",
        "--overwrite",
    ]

    analyze_command = [
        "codeql",
        "database",
        "analyze",
        str(db_dir),
        CODEQL_SUITE,
        "--format=sarif-latest",
        f"--output={sarif_path}",
    ]

    rc1, out1, err1, latency1 = run_command(create_command, timeout=300)
    rc2, out2, err2, latency2 = run_command(analyze_command, timeout=600)

    findings = []
    parse_error = ""

    if sarif_path.exists():
        try:
            sarif = json.loads(sarif_path.read_text(encoding="utf-8", errors="replace"))
            runs = sarif.get("runs", [])
            for run in runs:
                rules_by_id = {}
                for rule in run.get("tool", {}).get("driver", {}).get("rules", []) or []:
                    rules_by_id[rule.get("id", "")] = rule

                for result in run.get("results", []) or []:
                    rule_id = result.get("ruleId", "")
                    rule = rules_by_id.get(rule_id, {})
                    message = result.get("message", {}).get("text", "")
                    tags = rule.get("properties", {}).get("tags", []) or []
                    findings.append({
                        "rule_id": rule_id,
                        "message": message,
                        "tags": tags,
                    })
        except Exception as e:
            parse_error = str(e)

    detected = len(findings) > 0
    classification = classify_detection(case["expected_label"], detected)

    predicted_cwes = []
    rule_ids = []
    evidence = []

    for finding in findings:
        rule_id = finding.get("rule_id", "")
        rule_ids.append(rule_id)

        for tag in finding.get("tags", []):
            tag_upper = str(tag).upper()
            if tag_upper.startswith("CWE-"):
                predicted_cwes.append(tag_upper)

        evidence.append(f"{rule_id}: {finding.get('message', '')}".strip())

    return {
        **case,
        "tool": "codeql",
        "detected": "Yes" if detected else "No",
        **classification,
        "finding_count": len(findings),
        "predicted_cwes": "; ".join(sorted(set(predicted_cwes))),
        "rule_ids": "; ".join(sorted(set(rule_ids))),
        "evidence": " | ".join(evidence[:5]),
        "returncode": rc2 if rc1 == 0 else rc1,
        "latency_seconds": round(latency1 + latency2, 3),
        "error": parse_error or (err1.strip() + " " + err2.strip()).strip(),
    }


def compute_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    tp = sum(1 for r in rows if r["outcome"] == "TP")
    tn = sum(1 for r in rows if r["outcome"] == "TN")
    fp = sum(1 for r in rows if r["outcome"] == "FP")
    fn = sum(1 for r in rows if r["outcome"] == "FN")

    total = len(rows)
    correct = tp + tn

    accuracy = correct / total if total else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0
    safe_accuracy = tn / (tn + fp) if (tn + fp) else 0
    avg_latency = sum(float(r["latency_seconds"]) for r in rows) / total if total else 0

    return {
        "total_cases": total,
        "correct_cases": correct,
        "true_positives": tp,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "safe_accuracy": round(safe_accuracy, 4),
        "average_latency_seconds": round(avg_latency, 3),
    }


def write_outputs(tool: str, rows: list[dict[str, Any]], timestamp: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = OUTPUT_DIR / f"experiment2_{tool}_results_{timestamp}.csv"
    json_path = OUTPUT_DIR / f"experiment2_{tool}_results_{timestamp}.json"
    md_path = OUTPUT_DIR / f"experiment2_{tool}_report_{timestamp}.md"

    fieldnames = [
        "case_id",
        "cwe",
        "expected_label",
        "detected_label",
        "correct",
        "outcome",
        "tool",
        "detected",
        "finding_count",
        "predicted_cwes",
        "rule_ids",
        "evidence",
        "file_path",
        "file_name",
        "returncode",
        "latency_seconds",
        "error",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    metrics = compute_metrics(rows)

    json_payload = {
        "generated_at": timestamp,
        "tool": tool,
        "dataset_dir": str(DATASET_DIR),
        "case_count": len(rows),
        "metrics": metrics,
        "results": rows,
    }

    json_path.write_text(json.dumps(json_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    md_lines = [
        f"# Experiment 2 Static Baseline Report — {tool}",
        "",
        f"Generated: {timestamp}",
        "",
        "## Dataset",
        "",
        f"- Dataset folder: `{DATASET_DIR}`",
        f"- Total cases: {len(rows)}",
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]

    for key, value in metrics.items():
        md_lines.append(f"| {key} | {value} |")

    md_lines.extend([
        "",
        "## Incorrect Cases",
        "",
        "| Case | CWE | Expected | Detected | Outcome | Findings | Rules |",
        "|---|---|---|---|---|---:|---|",
    ])

    for r in rows:
        if r["correct"] == "No":
            md_lines.append(
                f"| {r['case_id']} | {r['cwe']} | {r['expected_label']} | "
                f"{r['detected_label']} | {r['outcome']} | {r['finding_count']} | {r['rule_ids']} |"
            )

    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"\nSaved outputs:")
    print(f"- CSV: {csv_path}")
    print(f"- JSON: {json_path}")
    print(f"- Markdown: {md_path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", choices=["bandit", "codeql", "both"], default="both")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--cwe", type=str, default=None, help="Optional CWE filter, e.g. CWE-89")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cases = discover_cases()

    if args.cwe:
        target = args.cwe.replace(" ", "-").upper()
        cases = [c for c in cases if c["cwe"].upper() == target]

    if args.limit:
        cases = cases[:args.limit]

    print("EXPERIMENT 2 STATIC BASELINE RUNNER")
    print(f"Dataset: {DATASET_DIR}")
    print(f"Cases discovered: {len(cases)}")
    print(f"Tool mode: {args.tool}")

    if not cases:
        raise RuntimeError("No cases found. Check dataset path and candidate filenames.")

    temp_root = OUTPUT_DIR / "_codeql_temp"
    temp_root.mkdir(parents=True, exist_ok=True)

    if args.tool in {"bandit", "both"}:
        bandit_rows = []
        print("\nRunning Bandit...")
        for i, case in enumerate(cases, start=1):
            row = run_bandit(case)
            bandit_rows.append(row)
            print(
                f"[Bandit {i}/{len(cases)}] {case['case_id']} -> "
                f"{row['detected_label']} | correct={row['correct']} | {row['latency_seconds']}s"
            )
        write_outputs("bandit", bandit_rows, timestamp)

    if args.tool in {"codeql", "both"}:
        codeql_rows = []
        print("\nRunning CodeQL...")
        for i, case in enumerate(cases, start=1):
            row = run_codeql(case, temp_root)
            codeql_rows.append(row)
            print(
                f"[CodeQL {i}/{len(cases)}] {case['case_id']} -> "
                f"{row['detected_label']} | correct={row['correct']} | {row['latency_seconds']}s"
            )
        write_outputs("codeql", codeql_rows, timestamp)

    print("\nExperiment 2 static baseline run complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())