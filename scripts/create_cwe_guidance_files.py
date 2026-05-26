from pathlib import Path
import re

VULNERABLE_DIR = Path("datasets/securityeval_expanded/vulnerable")
GUIDANCE_DIR = Path("datasets/securityeval_expanded/metadata/cwe_guidance")

GUIDANCE_DIR.mkdir(parents=True, exist_ok=True)

cwe_ids = set()

for folder in VULNERABLE_DIR.iterdir():
    if folder.is_dir():
        match = re.search(r"CWE(\d+)", folder.name)
        if match:
            cwe_ids.add(match.group(1))

for cwe_num in sorted(cwe_ids, key=lambda x: int(x)):
    cwe_id = f"CWE-{cwe_num.zfill(3)}"
    mitre_num = str(int(cwe_num))
    output_file = GUIDANCE_DIR / f"{cwe_id}.md"

    if output_file.exists():
        print(f"Skipping existing file: {output_file}")
        continue

    content = f"""# {cwe_id} Guidance

## CWE ID

{cwe_id}

## CWE Name

TO_BE_FILLED

## Source

MITRE CWE official entry:

https://cwe.mitre.org/data/definitions/{mitre_num}.html

## Weakness Summary

TO_BE_FILLED

## Mitigation Guidance

TO_BE_FILLED

## Dataset Usage

This guidance will be used when generating secure counterparts for vulnerable samples mapped to {cwe_id}.

The secure counterpart should preserve intended functionality while removing or mitigating the target weakness using CWE-specific guidance.

## Notes

This file summarizes CWE guidance for dataset generation and secure counterpart creation.
"""

    output_file.write_text(content, encoding="utf-8")
    print(f"Created: {output_file}")

print("Done.")