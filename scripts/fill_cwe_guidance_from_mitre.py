from pathlib import Path
import re
import json
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

VULNERABLE_DIR = Path("datasets/securityeval_expanded/vulnerable")
GUIDANCE_DIR = Path("datasets/securityeval_expanded/metadata/cwe_guidance")
DATA_JSON = Path("datasets/securityeval_expanded/metadata/cwe_guidance_data.json")

CWE_ZIP_URL = "https://cwe.mitre.org/data/xml/cwec_latest.xml.zip"
DOWNLOAD_DIR = Path("data/raw/cwe")
ZIP_PATH = DOWNLOAD_DIR / "cwec_latest.xml.zip"

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
GUIDANCE_DIR.mkdir(parents=True, exist_ok=True)

def get_needed_cwes():
    cwe_ids = set()
    for folder in VULNERABLE_DIR.iterdir():
        if folder.is_dir():
            match = re.search(r"CWE(\d+)", folder.name)
            if match:
                num = int(match.group(1))
                cwe_ids.add(f"CWE-{num:03d}")
    return sorted(cwe_ids, key=lambda x: int(x.split("-")[1]))

def download_cwe_zip():
    if ZIP_PATH.exists():
        print(f"Using existing download: {ZIP_PATH}")
        return
    print(f"Downloading CWE XML from: {CWE_ZIP_URL}")
    urllib.request.urlretrieve(CWE_ZIP_URL, ZIP_PATH)
    print(f"Downloaded: {ZIP_PATH}")

def extract_xml():
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        xml_files = [name for name in z.namelist() if name.endswith(".xml")]
        if not xml_files:
            raise FileNotFoundError("No XML file found inside CWE zip.")
        xml_name = xml_files[0]
        xml_path = DOWNLOAD_DIR / Path(xml_name).name
        if not xml_path.exists():
            z.extract(xml_name, DOWNLOAD_DIR)
            extracted = DOWNLOAD_DIR / xml_name
            if extracted != xml_path:
                extracted.rename(xml_path)
        print(f"Using XML: {xml_path}")
        return xml_path

def text_or_empty(element):
    if element is None or element.text is None:
        return ""
    return " ".join(element.text.split())

def collect_text(element):
    if element is None:
        return ""
    return " ".join(" ".join(element.itertext()).split())

def parse_cwe_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    ns_match = re.match(r"\{(.+)\}", root.tag)
    ns = {"cwe": ns_match.group(1)} if ns_match else {}

    cwe_data = {}

    for weakness in root.findall(".//cwe:Weakness", ns):
        cwe_num = weakness.attrib.get("ID")
        name = weakness.attrib.get("Name", "")
        cwe_id = f"CWE-{int(cwe_num):03d}"

        description = collect_text(weakness.find("cwe:Description", ns))
        extended_description = collect_text(weakness.find("cwe:Extended_Description", ns))

        mitigations = []
        potential_mitigations = weakness.find("cwe:Potential_Mitigations", ns)
        if potential_mitigations is not None:
            for mitigation in potential_mitigations.findall("cwe:Mitigation", ns):
                phase = collect_text(mitigation.find("cwe:Phase", ns))
                strategy = collect_text(mitigation.find("cwe:Strategy", ns))
                description_text = collect_text(mitigation.find("cwe:Description", ns))

                parts = []
                if phase:
                    parts.append(f"Phase: {phase}")
                if strategy:
                    parts.append(f"Strategy: {strategy}")
                if description_text:
                    parts.append(description_text)

                if parts:
                    mitigations.append(" - ".join(parts))

        cwe_data[cwe_id] = {
            "name": name,
            "description": description,
            "extended_description": extended_description,
            "mitigations": mitigations,
            "source_url": f"https://cwe.mitre.org/data/definitions/{int(cwe_num)}.html"
        }

    return cwe_data

def create_summary_text(entry):
    description = entry.get("description", "")
    extended = entry.get("extended_description", "")

    if extended:
        return f"{description}\n\n{extended}"
    return description

def create_mitigation_text(entry):
    mitigations = entry.get("mitigations", [])
    if not mitigations:
        return "No specific potential mitigation guidance was available in the parsed CWE entry. Use the CWE description and related secure-design principles to guide secure counterpart generation."

    return "\n".join(f"- {m}" for m in mitigations)

def write_guidance_files(needed_cwes, all_cwe_data):
    selected_data = {}

    for cwe_id in needed_cwes:
        entry = all_cwe_data.get(cwe_id)

        if entry is None:
            print(f"WARNING: {cwe_id} not found in CWE XML.")
            continue

        selected_data[cwe_id] = entry

        cwe_num = int(cwe_id.split("-")[1])
        output_file = GUIDANCE_DIR / f"{cwe_id}.md"

        content = f"""# {cwe_id} Guidance

## CWE ID

{cwe_id}

## CWE Name

{entry["name"]}

## Source

MITRE CWE official entry:

{entry["source_url"]}

## Weakness Summary

{create_summary_text(entry)}

## Mitigation Guidance

{create_mitigation_text(entry)}

## Dataset Usage

This guidance will be used when generating secure counterparts for vulnerable samples mapped to {cwe_id}.

The secure counterpart should preserve intended functionality while removing or mitigating the target weakness using CWE-specific guidance.

## Notes

This file summarizes MITRE CWE guidance for dataset generation and secure counterpart creation.
"""

        output_file.write_text(content, encoding="utf-8")
        print(f"Wrote: {output_file}")

    DATA_JSON.write_text(json.dumps(selected_data, indent=2), encoding="utf-8")
    print(f"Wrote structured CWE guidance data: {DATA_JSON}")

def main():
    needed_cwes = get_needed_cwes()
    print(f"Found {len(needed_cwes)} CWE IDs from vulnerable dataset:")
    print(", ".join(needed_cwes))

    download_cwe_zip()
    xml_path = extract_xml()
    all_cwe_data = parse_cwe_xml(xml_path)
    write_guidance_files(needed_cwes, all_cwe_data)

    print("Done.")

if __name__ == "__main__":
    main()