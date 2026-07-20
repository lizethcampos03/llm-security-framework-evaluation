from pathlib import Path
import json
import shutil

BASE_DIR = Path("data")
SECURITYEVAL_DIR = BASE_DIR / "securityeval_dataset"
CONTEXT_PROFILE_DIR = BASE_DIR / "context_profiles"
CHAIN_DIR = BASE_DIR / "chain_vulnerability_experiment"

CHAINS = {
    "chain_01_cloud_credential_exposure": {
        "chain_name": "Cloud Credential Exposure Chain",
        "platform_category": "Cloud-Native Applications",
        "context_profile": "cloud_management_platform",
        "primary_capec": "CAPEC-664 – Server-Side Request Forgery (SSRF)",
        "components": {
            "CWE-918": "cwe_918_ssrf.py",
            "CWE-200": "cwe_200_sensitive_exposure.py",
            "CWE-306": "cwe_306_missing_auth.py",
        },
        "attack_path": [
            "attacker-controlled URL input",
            "server-side request forgery",
            "cloud metadata service access",
            "credential disclosure",
            "access to critical cloud resources",
            "unauthorized cloud resource access",
        ],
        "expected_reasoning": (
            "SSRF enables access to internal metadata services. Metadata access exposes "
            "sensitive cloud credentials. Those credentials enable unauthorized access to "
            "protected cloud resources or critical cloud functionality."
        ),
        "expected_repair": [
            "validate and restrict outbound URLs",
            "block access to metadata service endpoints",
            "protect cloud credentials",
            "enforce authentication for critical cloud functionality",
        ],
    },
    "chain_02_path_traversal_secret_disclosure": {
        "chain_name": "Path Traversal Secret Disclosure Chain",
        "platform_category": "Web Applications / SaaS Platforms / Cloud Services",
        "context_profile": "web_social_platform",
        "primary_capec": "CAPEC-126 – Path Traversal",
        "components": {
            "CWE-22": "cwe_22_path_traversal.py",
            "CWE-200": "cwe_200_sensitive_exposure.py",
            "CWE-798": "cwe_798_hardcoded_credentials.py",
        },
        "attack_path": [
            "attacker-controlled file path",
            "path traversal",
            "access to restricted configuration files",
            "disclosure of sensitive information",
            "credential discovery",
            "unauthorized service access",
        ],
        "expected_reasoning": (
            "Path traversal enables access to restricted configuration files. Those files "
            "may expose sensitive information or credentials, which can then be used to "
            "access downstream services without authorization."
        ),
        "expected_repair": [
            "validate and normalize file paths",
            "enforce directory containment",
            "avoid storing secrets in readable configuration files",
            "remove hardcoded credentials",
        ],
    },
    "chain_03_privileged_transaction_access": {
        "chain_name": "Privileged Transaction Access Chain",
        "platform_category": "Fintech Platforms / Digital Asset Management Systems / Transaction Processing Services",
        "context_profile": "financial_application",
        "primary_capec": "CAPEC-16 – Dictionary-Based Password Attack",
        "components": {
            "CWE-798": "cwe_798_hardcoded_credentials.py",
            "CWE-306": "cwe_306_missing_auth.py",
        },
        "attack_path": [
            "hardcoded credential exposure",
            "credential discovery",
            "authentication bypass",
            "access to transaction functionality",
            "unauthorized transaction execution",
            "privilege abuse",
        ],
        "expected_reasoning": (
            "Hardcoded credentials expose authentication material. The exposed credentials "
            "can be used to reach transaction-processing functionality, and missing "
            "authentication protections allow unauthorized privileged operations."
        ),
        "expected_repair": [
            "remove hardcoded credentials",
            "use secure credential management",
            "enforce authentication before transaction operations",
            "apply least-privilege access controls",
        ],
    },
    "chain_04_code_injection_sensitive_operation": {
        "chain_name": "Code Injection Sensitive Operation Chain",
        "platform_category": "Web Applications / Cloud Services / Automation Platforms",
        "context_profile": "developer_platform",
        "primary_capec": "CAPEC-242 – Code Injection",
        "components": {
            "CWE-94": "cwe_94_code_injection.py",
            "CWE-200": "cwe_200_sensitive_exposure.py",
        },
        "attack_path": [
            "attacker-controlled input",
            "code injection",
            "execution of malicious logic",
            "access to sensitive resources",
            "exposure of sensitive information",
            "unauthorized administrative action",
        ],
        "expected_reasoning": (
            "Code injection enables attacker-controlled logic to execute inside the "
            "application. That execution can access sensitive resources and expose "
            "information that may enable unauthorized administrative actions."
        ),
        "expected_repair": [
            "eliminate dynamic code execution",
            "use safe parsing or interpretation alternatives",
            "validate and constrain untrusted input",
            "protect sensitive resources from untrusted execution paths",
        ],
    },
}


def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def copy_required_file(source: Path, destination: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Missing required source file: {source}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def populate_chain(chain_id: str, chain: dict) -> None:
    chain_path = CHAIN_DIR / chain_id
    components_path = chain_path / "components"
    ground_truth_path = chain_path / "ground_truth"

    chain_path.mkdir(parents=True, exist_ok=True)
    components_path.mkdir(exist_ok=True)
    ground_truth_path.mkdir(exist_ok=True)

    # 1. Copy context profile
    context_source = CONTEXT_PROFILE_DIR / f"{chain['context_profile']}.json"
    context_destination = chain_path / "context_profile.json"
    copy_required_file(context_source, context_destination)

    # 2. Copy vulnerable SecurityEval component files
    for cwe_id, output_filename in chain["components"].items():
        source_file = SECURITYEVAL_DIR / cwe_id / "vulnerable_securityeval_sample.py"
        destination_file = components_path / output_filename
        copy_required_file(source_file, destination_file)

    involved_cwes = list(chain["components"].keys())

    # 3. Write chain_spec.json
    chain_spec = {
        "chain_id": chain_id,
        "chain_name": chain["chain_name"],
        "platform_category": chain["platform_category"],
        "context_profile": chain["context_profile"],
        "primary_capec": chain["primary_capec"],
        "involved_cwes": involved_cwes,
        "component_files": chain["components"],
        "attack_path": chain["attack_path"],
        "expected_chain_detected": True,
        "expected_reasoning": chain["expected_reasoning"],
        "expected_repair": chain["expected_repair"],
        "status": "selected",
    }
    write_json(chain_path / "chain_spec.json", chain_spec)

    # 4. Write ground truth files
    write_json(
        ground_truth_path / "expected_attack_path.json",
        {
            "chain_id": chain_id,
            "chain_name": chain["chain_name"],
            "attack_path": chain["attack_path"],
            "expected_reasoning": chain["expected_reasoning"],
        },
    )

    write_json(
        ground_truth_path / "expected_cwes.json",
        {
            "chain_id": chain_id,
            "expected_cwes": involved_cwes,
            "expected_individual_vulnerabilities_detected": True,
        },
    )

    write_json(
        ground_truth_path / "expected_capec.json",
        {
            "chain_id": chain_id,
            "primary_capec": chain["primary_capec"],
            "capec_role": "attack-pattern evidence supporting the chained vulnerability scenario",
        },
    )

    write_json(
        ground_truth_path / "expected_results.json",
        {
            "chain_id": chain_id,
            "expected_chain_detected": True,
            "expected_individual_detection": {
                cwe_id: True for cwe_id in involved_cwes
            },
            "expected_chain_explanation_correct": True,
            "expected_repair_guidance_generated": True,
            "expected_chain_breaking_guidance": True,
        },
    )

    notes = f"""# Evaluation Notes: {chain["chain_name"]}

## Purpose

This file records observations from running the chained vulnerability experiment.

## Expected Outcome

The framework should detect the individual vulnerabilities, infer the attack path, and generate chain-aware remediation guidance.

## Notes

- Chain ID: {chain_id}
- Context Profile: {chain["context_profile"]}
- Primary CAPEC: {chain["primary_capec"]}
- Involved CWEs: {", ".join(involved_cwes)}

## Run Observations

[TBD]

## Errors / False Positives / False Negatives

[TBD]

## Final Assessment

[TBD]
"""
    (ground_truth_path / "evaluation_notes.md").write_text(notes, encoding="utf-8")


def main() -> None:
    if not BASE_DIR.exists():
        raise FileNotFoundError(f"Could not find base data folder: {BASE_DIR}")

    for chain_id, chain in CHAINS.items():
        populate_chain(chain_id, chain)

    print("Chain vulnerability experiment data populated successfully.")
    print(f"Output folder: {CHAIN_DIR}")


if __name__ == "__main__":
    main()