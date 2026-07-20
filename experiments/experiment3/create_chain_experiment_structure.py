from pathlib import Path

# Root location
ROOT = Path("Data") / "chain_vulnerability_experiment"

# Folder structure
structure = {
    "chain_01_cloud_credential_exposure": {
        "files": [
            "context_profile.json",
            "chain_spec.json"
        ],
        "components": [
            "cwe_918_ssrf.py",
            "cwe_200_sensitive_exposure.py",
            "cwe_306_missing_auth.py"
        ]
    },
    "chain_02_path_traversal_secret_disclosure": {
        "files": [
            "context_profile.json",
            "chain_spec.json"
        ],
        "components": [
            "cwe_22_path_traversal.py",
            "cwe_200_sensitive_exposure.py",
            "cwe_798_hardcoded_credentials.py"
        ]
    },
    "chain_03_privileged_transaction_access": {
        "files": [
            "context_profile.json",
            "chain_spec.json"
        ],
        "components": [
            "cwe_798_hardcoded_credentials.py",
            "cwe_306_missing_auth.py"
        ]
    },
    "chain_04_code_injection_sensitive_operation": {
        "files": [
            "context_profile.json",
            "chain_spec.json"
        ],
        "components": [
            "cwe_94_code_injection.py",
            "cwe_200_sensitive_exposure.py"
        ]
    }
}

# Create root folder
ROOT.mkdir(parents=True, exist_ok=True)

# Create experiment README
(ROOT / "README.md").touch(exist_ok=True)

for chain_name, chain_data in structure.items():

    chain_dir = ROOT / chain_name
    chain_dir.mkdir(exist_ok=True)

    # Create root files
    for file_name in chain_data["files"]:
        (chain_dir / file_name).touch(exist_ok=True)

    # Create components folder
    components_dir = chain_dir / "components"
    components_dir.mkdir(exist_ok=True)

    for component_file in chain_data["components"]:
        (components_dir / component_file).touch(exist_ok=True)

    # Create ground truth folder
    ground_truth_dir = chain_dir / "ground_truth"
    ground_truth_dir.mkdir(exist_ok=True)

    # Ground truth files
    (ground_truth_dir / "expected_attack_path.json").touch(exist_ok=True)
    (ground_truth_dir / "expected_cwes.json").touch(exist_ok=True)
    (ground_truth_dir / "expected_capec.json").touch(exist_ok=True)
    (ground_truth_dir / "expected_results.json").touch(exist_ok=True)

print("Chain vulnerability experiment folder structure created successfully.")