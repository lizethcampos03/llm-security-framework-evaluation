from pathlib import Path
import json

VULNERABLE_DIR = Path("datasets/securityeval_expanded/vulnerable")
OUTPUT_DIR = Path("datasets/securityeval_expanded/secure_generation_inputs")
CWE_GUIDANCE_JSON = Path(
    "datasets/securityeval_expanded/metadata/cwe_guidance_data.json"
)
PROMPT_FILE = Path("prompts/secure_counterpart_prompt_v1.md")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def read_text(path):
    return path.read_text(encoding="utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_cwe_id(cwe_id):
    if not cwe_id:
        return None

    cwe_id = str(cwe_id).strip()

    if cwe_id.startswith("CWE-"):
        number = cwe_id.split("-")[1]
        return f"CWE-{int(number):03d}"

    if cwe_id.startswith("CWE"):
        number = cwe_id.replace("CWE", "")
        return f"CWE-{int(number):03d}"

    return f"CWE-{int(cwe_id):03d}"


def build_generation_input(sample_dir, cwe_guidance, prompt_template):
    sample_id = sample_dir.name

    vulnerable_path = sample_dir / "vulnerable.py"
    metadata_path = sample_dir / "metadata.json"

    if not vulnerable_path.exists():
        print(f"Skipping {sample_id}: missing vulnerable.py")
        return None

    if not metadata_path.exists():
        print(f"Skipping {sample_id}: missing metadata.json")
        return None

    vulnerable_code = read_text(vulnerable_path)
    metadata = read_json(metadata_path)

    cwe_id = normalize_cwe_id(metadata.get("cwe_id"))

    if cwe_id not in cwe_guidance:
        print(f"Skipping {sample_id}: missing CWE guidance for {cwe_id}")
        return None

    guidance = cwe_guidance[cwe_id]

    mitigations = guidance.get("mitigations", [])
    mitigation_text = "\n".join(f"- {item}" for item in mitigations)

    content = f"""
# Secure Counterpart Generation Input

## Sample ID

{sample_id}

## Source Vulnerable Sample

{sample_id}

## Metadata

{json.dumps(metadata, indent=2)}

## CWE ID

{cwe_id}

## CWE Name

{guidance.get("name", "")}

## MITRE Source

{guidance.get("source_url", "")}

## CWE Description

{guidance.get("description", "")}

## CWE Extended Description

{guidance.get("extended_description", "")}

## CWE Mitigation Guidance

{mitigation_text}

## Secure Counterpart Prompt

{prompt_template}

## Vulnerable Python Code

{vulnerable_code}
"""

    return content


def main():
    cwe_guidance = read_json(CWE_GUIDANCE_JSON)
    prompt_template = read_text(PROMPT_FILE)

    sample_dirs = sorted(
        [p for p in VULNERABLE_DIR.iterdir() if p.is_dir()]
    )

    created = 0
    skipped = 0

    for sample_dir in sample_dirs:
        content = build_generation_input(
            sample_dir,
            cwe_guidance,
            prompt_template
        )

        if content is None:
            skipped += 1
            continue

        output_file = (
            OUTPUT_DIR /
            f"{sample_dir.name}_generation_input.md"
        )

        output_file.write_text(
            content,
            encoding="utf-8"
        )

        print(f"Wrote: {output_file}")
        created += 1

    print()
    print(f"Generation input files created: {created}")
    print(f"Samples skipped: {skipped}")


if __name__ == "__main__":
    main()