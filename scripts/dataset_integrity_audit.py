from pathlib import Path
import ast
import json
import csv

ROOT = Path("datasets/securityeval_expanded")
VULNERABLE_DIR = ROOT / "vulnerable"
SECURE_DIR = ROOT / "secure"
OUTPUT_DIR = ROOT / "validation" / "integrity_audit"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

errors = []
warnings = []
records = []


def check_python(path):
    text = path.read_text(encoding="utf-8")
    try:
        ast.parse(text)
        return "valid", ""
    except SyntaxError as e:
        return "invalid", str(e)


def check_json(path):
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return "valid", ""
    except Exception as e:
        return "invalid", str(e)


def audit_sample(sample_dir, sample_type):
    sample_id = sample_dir.name

    if sample_type == "vulnerable":
        required = ["vulnerable.py"]
        code_file = sample_dir / "vulnerable.py"
    else:
        required = ["secure.py", "metadata.json", "generation_notes.md"]
        code_file = sample_dir / "secure.py"

    missing = []

    for file_name in required:
        if not (sample_dir / file_name).exists():
            missing.append(file_name)

    syntax_status = "not_checked"
    syntax_error = ""

    if code_file.exists():
        syntax_status, syntax_error = check_python(code_file)

    metadata_status = "not_checked"
    metadata_error = ""

    metadata_path = sample_dir / "metadata.json"
    if metadata_path.exists():
        metadata_status, metadata_error = check_json(metadata_path)

    record = {
        "sample_id": sample_id,
        "sample_type": sample_type,
        "missing_files": "; ".join(missing),
        "python_syntax_status": syntax_status,
        "python_syntax_error": syntax_error,
        "metadata_status": metadata_status,
        "metadata_error": metadata_error,
    }

    records.append(record)

    if missing:
        errors.append(f"{sample_id}: missing {missing}")

    if syntax_status == "invalid":
        errors.append(f"{sample_id}: Python syntax error: {syntax_error}")

    if metadata_status == "invalid":
        errors.append(f"{sample_id}: metadata JSON error: {metadata_error}")


def main():
    vulnerable_samples = sorted([p for p in VULNERABLE_DIR.iterdir() if p.is_dir()])
    secure_samples = sorted([p for p in SECURE_DIR.iterdir() if p.is_dir()])

    if len(vulnerable_samples) != 69:
        warnings.append(f"Expected 69 vulnerable samples, found {len(vulnerable_samples)}")

    if len(secure_samples) != 69:
        warnings.append(f"Expected 69 secure samples, found {len(secure_samples)}")

    for sample in vulnerable_samples:
        audit_sample(sample, "vulnerable")

    for sample in secure_samples:
        audit_sample(sample, "secure")

    csv_path = OUTPUT_DIR / "dataset_integrity_audit.csv"
    txt_path = OUTPUT_DIR / "dataset_integrity_audit_summary.md"

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    summary = [
        "# Dataset Integrity Audit Summary",
        "",
        f"Vulnerable samples found: {len(vulnerable_samples)}",
        f"Secure samples found: {len(secure_samples)}",
        "",
        "## Warnings",
        "",
    ]

    summary.extend([f"- {w}" for w in warnings] if warnings else ["None"])

    summary.extend(["", "## Errors", ""])
    summary.extend([f"- {e}" for e in errors] if errors else ["None"])

    summary.extend(["", "## Result", ""])
    summary.append("PASS" if not errors else "FAIL")

    txt_path.write_text("\n".join(summary), encoding="utf-8")

    print(f"Wrote: {csv_path}")
    print(f"Wrote: {txt_path}")
    print()
    print("Warnings:", len(warnings))
    print("Errors:", len(errors))

    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
