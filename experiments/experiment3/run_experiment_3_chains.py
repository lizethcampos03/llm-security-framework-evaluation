from pathlib import Path
import json
import csv
from datetime import datetime

from src.graph import build_graph


ROOT = Path("Data") / "chain_vulnerability_experiment"
REPORTS_DIR = ROOT / "reports"
LOG_PATH = ROOT / "experiment_4_log.csv"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_components(chain_dir: Path):
    components = []
    for file_path in sorted((chain_dir / "components").glob("*.py")):
        components.append({
            "file_name": file_path.name,
            "code": file_path.read_text(encoding="utf-8"),
        })
    return components


def run_chain(chain_dir: Path, graph):
    context_profile = read_json(chain_dir / "context_profile.json")
    chain_spec = read_json(chain_dir / "chain_spec.json")
    component_relationships = read_json(chain_dir / "component_relationships.json")
    components = read_components(chain_dir)

    initial_state = {
        "data": {
            "chain_mode": True,
            "chain_id": chain_spec["chain_id"],
            "chain_name": chain_spec["chain_name"],
            "context_profile": context_profile,
            "component_relationships": component_relationships,
            "components": components,
        }
    }

    result = graph.invoke(initial_state)
    data = result.get("data", {})
    report = data.get("chain_final_report", data.get("final_report", {}))

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{chain_spec['chain_id']}_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    chain_reasoning = report.get("chain_reasoning", {})
    component_findings = report.get("component_level_findings", [])

    detected_cwes = set()
    for component in component_findings:
        for finding in component.get("findings", []):
            cwe_id = finding.get("cwe_id")
            if cwe_id:
                detected_cwes.add(cwe_id)

    return {
        "chain_id": chain_spec["chain_id"],
        "chain_name": chain_spec["chain_name"],
        "context_profile": chain_spec["context_profile"],
        "expected_cwes": "; ".join(chain_spec.get("involved_cwes", [])),
        "detected_cwes": "; ".join(sorted(detected_cwes)),
        "individual_vulnerabilities_detected": bool(detected_cwes),
        "candidate_chain_triggered": report.get("chain_candidate_evidence", {}).get("vulnerable_finding_count", 0) >= 2,
        "chain_detected": chain_reasoning.get("chain_detected", False),
        "attack_path_correct": "",
        "capec_cwe_evidence_used": bool(
            chain_reasoning.get("related_capec_patterns")
            or chain_reasoning.get("supporting_evidence")
        ),
        "repair_plan_generated": report.get("chain_repair_plan", {}).get("repair_generated", False),
        "repair_plan_breaks_chain": "",
        "manual_review_status": "pending",
        "notes": f"Report saved to {report_path}",
    }


def write_log(rows):
    fieldnames = [
        "chain_id",
        "chain_name",
        "context_profile",
        "expected_cwes",
        "detected_cwes",
        "individual_vulnerabilities_detected",
        "candidate_chain_triggered",
        "chain_detected",
        "attack_path_correct",
        "capec_cwe_evidence_used",
        "repair_plan_generated",
        "repair_plan_breaks_chain",
        "manual_review_status",
        "notes",
    ]

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with LOG_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    graph = build_graph()
    rows = []

    chain_dirs = sorted([
        path for path in ROOT.iterdir()
        if path.is_dir() and path.name.startswith("chain_")
    ])

    for chain_dir in chain_dirs:
        print(f"Running {chain_dir.name}...")
        try:
            row = run_chain(chain_dir, graph)
            rows.append(row)
        except Exception as error:
            rows.append({
                "chain_id": chain_dir.name,
                "chain_name": "",
                "context_profile": "",
                "expected_cwes": "",
                "detected_cwes": "",
                "individual_vulnerabilities_detected": False,
                "candidate_chain_triggered": False,
                "chain_detected": False,
                "attack_path_correct": "",
                "capec_cwe_evidence_used": False,
                "repair_plan_generated": False,
                "repair_plan_breaks_chain": "",
                "manual_review_status": "error",
                "notes": str(error),
            })

    write_log(rows)

    run_summary_path = REPORTS_DIR / "run_summary.json"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    run_summary_path.write_text(
        json.dumps({
            "run_timestamp": datetime.now().isoformat(),
            "chains_run": len(rows),
            "log_path": str(LOG_PATH),
            "reports_dir": str(REPORTS_DIR),
            "rows": rows,
        }, indent=2),
        encoding="utf-8",
    )

    print("Experiment 4 complete.")
    print(f"Log saved to: {LOG_PATH}")
    print(f"Reports saved to: {REPORTS_DIR}")


if __name__ == "__main__":
    main()