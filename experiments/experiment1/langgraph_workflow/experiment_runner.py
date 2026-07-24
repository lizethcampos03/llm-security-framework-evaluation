"""
Experiment Runner — LangGraph Security Tool

Purpose:
This script runs Experiment 1 cases through the LangGraph-based
security auditing pipeline and records:

- detection output
- confidence
- latency
- retrieval context
- fix generation
- validation consistency

Current Scope:
- CWE vector RAG
- Detection node integration
- Structured experiment execution
"""

import time
import json

from src.nodes.detection_node import detection_node


# =====================================================
# EXPERIMENT CASES
# =====================================================

EXPERIMENT_CASES = {

    "CASE-001": {
        "expected_label": "vulnerable",
        "owasp_category": "Injection",
        "cwe": "CWE-89",

        "application_context": """
Online banking login system.

Protected assets:
- customer accounts
- account balances
- transaction history

Security expectations:
- user input must never directly modify SQL behavior
- login queries must use parameterized queries

Threat concern:
An attacker attempts to bypass authentication using SQL injection.
""",

        "code": """
def login_user(cursor, username, password):
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    cursor.execute(query)
    user = cursor.fetchone()
    return user is not None
"""
    },


    "CASE-002": {
        "expected_label": "safe",
        "owasp_category": "Injection",
        "cwe": "CWE-89",

        "application_context": """
Online banking login system.

Protected assets:
- customer accounts
- account balances
- transaction history

Security expectations:
- SQL queries must use parameterized statements
- user input must not directly modify SQL behavior

Threat concern:
An attacker attempts SQL injection through login input.
""",

        "code": """
def login_user(cursor, username, password):
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    return user is not None
"""
    },


    "CASE-003": {
        "expected_label": "vulnerable",
        "owasp_category": "Identification and Authentication Failures",
        "cwe": "CWE-798",

        "application_context": """
Internal admin dashboard.

Protected assets:
- administrator accounts
- customer records
- inventory management tools

Security expectations:
- credentials must not be stored directly in source code
- secrets should be securely managed

Threat concern:
Attackers may recover credentials from leaked source code.
""",

        "code": """
def admin_login(username, password):
    admin_username = "admin"
    admin_password = "SuperSecret123"

    if username == admin_username and password == admin_password:
        return True

    return False
"""
    },


    "CASE-004": {
        "expected_label": "safe",
        "owasp_category": "Identification and Authentication Failures",
        "cwe": "CWE-798",

        "application_context": """
Internal admin dashboard.

Protected assets:
- administrator accounts
- customer records
- inventory management tools

Security expectations:
- credentials must not be hardcoded
- secrets should be loaded from environment variables

Threat concern:
Attackers may inspect source code repositories.
""",

        "code": """
import os


def admin_login(username, password):
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        return False

    if username == admin_username and password == admin_password:
        return True

    return False
"""
    }
}


# =====================================================
# RUN SINGLE CASE
# =====================================================

def run_case(case_id, case_data):

    print("\n" + "=" * 80)
    print(f"RUNNING {case_id}")
    print("=" * 80)

    state = {
        "cleaned_code": case_data["code"],
        "application_context": case_data["application_context"]
    }

    start_time = time.time()

    result_state = detection_node(state)

    end_time = time.time()

    latency = round(end_time - start_time, 2)

    detection_result = result_state.get("detection_result", {})

    detected_label = detection_result.get(
        "overall_security_status",
        "unknown"
    )

    correctness = (
        "Yes"
        if detected_label == case_data["expected_label"]
        else "No"
    )

    print(f"Expected Label: {case_data['expected_label']}")
    print(f"Detected Label: {detected_label}")
    print(f"Correctness: {correctness}")
    print(f"Latency: {latency} seconds")

    print("\nDETECTION RESULT:\n")

    print(json.dumps(
        detection_result,
        indent=2
    ))

    print("\nRETRIEVED CONTEXT PREVIEW:\n")

    retrieved_context = result_state.get(
        "retrieved_context",
        "No retrieved context"
    )

    print(retrieved_context[:1500])

    return {
        "case_id": case_id,
        "expected_label": case_data["expected_label"],
        "detected_label": detected_label,
        "correctness": correctness,
        "latency": latency,
        "result": detection_result
    }


# =====================================================
# MAIN
# =====================================================

def main():

    all_results = []

    print("\nSTARTING EXPERIMENT 1 EXECUTION")

    for case_id, case_data in EXPERIMENT_CASES.items():

        case_result = run_case(case_id, case_data)

        all_results.append(case_result)

    print("\n" + "=" * 80)
    print("EXPERIMENT SUMMARY")
    print("=" * 80)

    correct = 0

    for result in all_results:

        if result["correctness"] == "Yes":
            correct += 1

        print(
            f"{result['case_id']} | "
            f"Expected: {result['expected_label']} | "
            f"Detected: {result['detected_label']} | "
            f"Correct: {result['correctness']} | "
            f"Latency: {result['latency']}s"
        )

    total_cases = len(all_results)

    accuracy = round((correct / total_cases) * 100, 2)

    print("\nFINAL METRICS")
    print(f"Total Cases: {total_cases}")
    print(f"Correct: {correct}")
    print(f"Accuracy: {accuracy}%")


if __name__ == "__main__":
    main()