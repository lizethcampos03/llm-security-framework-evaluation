You will be provided with a complete LangGraph security audit report for a Python code sample.

Your task is to generate the complete final fixed Python code.

Requirements:
- Remove the confirmed vulnerability.
- Preserve the intended functionality.
- Do not introduce new vulnerabilities.
- Use the evidence, reasoning, and remediation guidance from the report.
- If the report includes candidate fixed code, use it as guidance but verify and improve it if necessary.
- Return only the complete fixed Python code.
- Do not include markdown, explanations, or commentary.

CASE ID:
{repair_input.get("case_id")}

CWE:
{repair_input.get("cwe")}

ORIGINAL CODE:
{repair_input.get("original_code", "")}

LANGGRAPH SECURITY REPORT:
{json.dumps(compact_report(repair_input), indent=2, ensure_ascii=False)}