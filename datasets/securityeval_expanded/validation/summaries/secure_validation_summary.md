# Secure Dataset Validation Summary

## Purpose

This document summarizes the current validation status of the secure dataset generated during Phase 2.

The purpose of this validation stage is to evaluate whether the generated secure counterparts remain vulnerable after repair generation and to identify cases requiring refinement, regeneration, or deeper manual review.

This validation stage is part of the broader calibration workflow and is not yet considered the final Experiment 2 evaluation.

---

# Validation Components Completed

## Dataset Integrity Audit

Status: COMPLETE

Validation checks performed:

- duplicate sample detection
- missing file detection
- metadata consistency checks
- label consistency checks
- directory structure validation
- secure/vulnerable pair validation

Result:

```text
PASS

Bandit Validation

Status: COMPLETE

Validation tools:

Bandit JSON output
Bandit text output
manual review log

Output files:

datasets/securityeval_expanded/validation/bandit/bandit_secure_results.json
datasets/securityeval_expanded/validation/bandit/bandit_secure_results.txt
datasets/securityeval_expanded/validation/manual_review/bandit_manual_review_log.md

Observations:

Most Bandit findings were low-complexity detections.
Several findings were likely false positives.
Some findings indicated repair-quality weaknesses.
Some findings suggested possible remaining vulnerabilities requiring review.

Bandit primarily detected:

subprocess usage
weak hashing usage
dynamic execution patterns
insecure deserialization patterns
hardcoded values
SQL query construction patterns

CodeQL Validation

Status: COMPLETE

Validation tools:

CodeQL SARIF output
CodeQL CSV output
manual review log

Output files:

datasets/securityeval_expanded/validation/codeql/results/codeql_secure_results.sarif
datasets/securityeval_expanded/validation/codeql/results/codeql_secure_results.csv
datasets/securityeval_expanded/validation/manual_review/codeql_manual_review_log.md

Observations:

CodeQL identified deeper semantic and dataflow-oriented findings than Bandit.

Detected categories included:

uncontrolled path expressions
SSRF-related flows
reflected XSS concerns
LDAP query construction
redirect validation issues
information exposure through exceptions
repair-quality implementation issues
code-quality warnings

Several findings are strong candidates for true remaining vulnerabilities.

Current Interpretation

The validation results strongly support the need for:

repair verification
context-aware repair generation
structured repair expectations
CWE-guided reasoning
manual review checkpoints
validation loops
workflow orchestration

The results also support the hypothesis that:

secure rewrites can still preserve unsafe logic
different tools detect different vulnerability classes
static analysis tools alone are insufficient for final validation
repair quality must be evaluated separately from detection accuracy

High-Priority Samples Requiring Review

Likely Remaining Vulnerabilities

SE-CWE099-010
SE-CWE434-044
SE-CWE641-055
SE-CWE116-012
SE-CWE918-067
SE-CWE090-007
SE-CWE601-052

Repair Quality Issues

SE-CWE117-013
SE-CWE269-022
SE-CWE406-041
SE-CWE611-054
SE-CWE200-016

Important Limitation

These validation results should not yet be treated as final Experiment 2 results.

Reasons:

manual review is still ongoing
some findings may be false positives
some secure rewrites may require regeneration
repair refinement has not yet been completed
fix verification calibration is still ongoing

Next Planned Actions

manually inspect high-priority findings
regenerate weak secure samples if needed
improve repair prompts and structured outputs
strengthen CWE-guided repair logic
rerun Bandit and CodeQL after refinements
finalize validated secure dataset
proceed to calibration experiments

Current Validation Status

| Validation Component          | Status      |
| ----------------------------- | ----------- |
| Dataset Integrity Audit       | COMPLETE    |
| Bandit Validation             | COMPLETE    |
| Bandit Manual Review          | COMPLETE    |
| CodeQL Validation             | COMPLETE    |
| CodeQL Manual Review          | COMPLETE    |
| Secure Dataset Finalization   | IN PROGRESS |
| Repair Refinement             | PENDING     |
| Final Experiment 2 Validation | PENDING     |
