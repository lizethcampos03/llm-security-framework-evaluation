from pathlib import Path
import json

ROOT = Path("Data") / "chain_vulnerability_experiment"

RELATIONSHIPS = {
    "chain_01_cloud_credential_exposure": {
        "relationship_summary": (
            "The application includes an external request service, internal cloud configuration resources, "
            "and administrative functionality that operates on protected infrastructure assets."
        ),
        "components": [
            {
                "name": "external_request_service",
                "role": "accepts user-controlled request parameters and performs server-side outbound network requests"
            },
            {
                "name": "configuration_or_account_service",
                "role": "handles internal configuration, account, or tenant-related information"
            },
            {
                "name": "administrative_settings_service",
                "role": "controls protected cloud or infrastructure-related settings"
            }
        ],
        "data_flow": [
            "External user input may influence server-side network requests.",
            "Server-side requests may reach internal services that are not normally reachable by external users.",
            "Internal service responses may contain configuration, identity, credential, or tenant-related information.",
            "Administrative functionality may use protected information to perform cloud resource actions."
        ],
        "shared_assets": [
            "cloud credentials",
            "virtual machine metadata",
            "tenant data",
            "network configuration",
            "protected cloud resources"
        ],
        "trust_boundaries": [
            "external user input to server-side request logic",
            "server-side application to internal cloud service",
            "internal configuration data to administrative functionality",
            "tenant-level access to platform-level resources"
        ],
        "notes_for_chain_reasoning": (
            "Use this file only as architectural and data-flow context. "
            "Do not treat it as a ground-truth vulnerability label or expected chain answer."
        )
    },

    "chain_02_path_traversal_secret_disclosure": {
        "relationship_summary": (
            "The application includes user-facing file handling, configuration storage, and backend service "
            "connectivity for an internet-facing platform."
        ),
        "components": [
            {
                "name": "file_management_service",
                "role": "handles user-supplied file identifiers or paths for media or document operations"
            },
            {
                "name": "configuration_storage",
                "role": "stores application configuration, service settings, or connection information"
            },
            {
                "name": "backend_database_service",
                "role": "uses stored configuration to connect to protected backend data resources"
            }
        ],
        "data_flow": [
            "External users may submit file identifiers or filenames to the application.",
            "File operations may interact with local application directories or stored platform resources.",
            "Configuration files may contain service connection settings or operational secrets.",
            "Backend services may rely on configuration values to access protected user or platform data."
        ],
        "shared_assets": [
            "user profiles",
            "private messages",
            "uploaded media",
            "session data",
            "configuration files",
            "backend service credentials"
        ],
        "trust_boundaries": [
            "external user input to filesystem operation",
            "user-facing file handling to server-side storage",
            "application configuration storage to backend service access",
            "public web interface to protected platform data"
        ],
        "notes_for_chain_reasoning": (
            "Use this file only as architectural and data-flow context. "
            "Do not treat it as a ground-truth vulnerability label or expected chain answer."
        )
    },

    "chain_03_privileged_transaction_access": {
        "relationship_summary": (
            "The application includes credential-dependent service access and transaction-related functionality "
            "within a financial or digital asset environment."
        ),
        "components": [
            {
                "name": "service_connection_component",
                "role": "establishes connections to backend services using application-provided authentication material"
            },
            {
                "name": "transaction_operation_component",
                "role": "performs sensitive transaction or account-changing operations"
            }
        ],
        "data_flow": [
            "Application components may use stored authentication material to connect to protected backend services.",
            "Authenticated backend access may enable transaction-related operations.",
            "Transaction functionality may operate on sensitive account, wallet, or financial records.",
            "Privileged operations require strong authentication and authorization boundaries."
        ],
        "shared_assets": [
            "financial account records",
            "transaction data",
            "digital asset balances",
            "service credentials",
            "privileged transaction functions"
        ],
        "trust_boundaries": [
            "application code to backend financial service",
            "service authentication material to privileged operation",
            "ordinary user access to transaction-processing functionality",
            "transaction operation to protected financial assets"
        ],
        "notes_for_chain_reasoning": (
            "Use this file only as architectural and data-flow context. "
            "Do not treat it as a ground-truth vulnerability label or expected chain answer."
        )
    },

    "chain_04_code_injection_sensitive_operation": {
        "relationship_summary": (
            "The application includes developer-facing input processing, execution-like development functionality, "
            "and access to sensitive project or build-related resources."
        ),
        "components": [
            {
                "name": "developer_input_processing_service",
                "role": "accepts user-supplied development artifacts, expressions, commands, or configuration-like input"
            },
            {
                "name": "project_data_service",
                "role": "accesses repository, project, account, or build-related data"
            }
        ],
        "data_flow": [
            "Developer-supplied input may be processed by server-side development functionality.",
            "Development functionality may execute, compile, evaluate, transform, or otherwise process submitted artifacts.",
            "Project data services may access source code, repository metadata, build artifacts, or service tokens.",
            "Execution-related functionality and project data access may exist within the same developer-facing platform environment."
        ],
        "shared_assets": [
            "source code",
            "repository metadata",
            "API tokens",
            "build artifacts",
            "CI/CD service accounts",
            "project configuration"
        ],
        "trust_boundaries": [
            "developer-controlled input to server-side processing",
            "server-side processing to build or automation environment",
            "build environment to project secrets",
            "project data service to protected repository assets"
        ],
        "notes_for_chain_reasoning": (
            "Use this file only as architectural and data-flow context. "
            "Do not treat it as a ground-truth vulnerability label or expected chain answer."
        )
    }
}


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> None:
    if not ROOT.exists():
        raise FileNotFoundError(f"Could not find chain experiment folder: {ROOT}")

    for chain_id, relationship_data in RELATIONSHIPS.items():
        chain_dir = ROOT / chain_id
        if not chain_dir.exists():
            raise FileNotFoundError(f"Could not find chain folder: {chain_dir}")

        output_path = chain_dir / "component_relationships.json"
        write_json(output_path, relationship_data)
        print(f"Created: {output_path}")

    print("Component relationship files created successfully.")


if __name__ == "__main__":
    main()