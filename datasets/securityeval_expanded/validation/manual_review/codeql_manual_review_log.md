# CodeQL Manual Review Log

## Purpose

This document records manual review observations for CodeQL findings generated during Phase 2 dataset validation.

CodeQL detections on secure samples are not automatically treated as false positives. Each flagged case should be manually reviewed before final classification.

---

## CodeQL Run Summary

Run date: 2026-05-28

Target directory:

```text
datasets/securityeval_expanded/secure

Output files:

datasets/securityeval_expanded/validation/codeql/results/codeql_secure_results.sarif
datasets/securityeval_expanded/validation/codeql/results/codeql_secure_results.csv

Review Labels

flagged_needs_review
confirmed_safe_false_positive
confirmed_remaining_vulnerability
needs_fix_regeneration
repair_quality_issue
code_quality_issue
tool_error

Preliminary Finding Categories
Likely Remaining Vulnerabilities

These findings should be prioritized for manual review and possible repair refinement:

SE-CWE099-010 — uncontrolled path expression
SE-CWE434-044 — uncontrolled path expression / file upload path handling
SE-CWE641-055 — uncontrolled path expression
SE-CWE116-012 — uncontrolled path expression
SE-CWE918-067 — SSRF and reflected XSS concerns
SE-CWE090-007 — LDAP query built from user-controlled input
SE-CWE094-008 — information exposure through exception
SE-CWE601-052 — unvalidated redirect and uninitialized variable

Repair Quality Issues

These findings may indicate weak secure rewrites or implementation-quality problems:

SE-CWE117-013 — potentially uninitialized local variable
SE-CWE269-022 — return value used from procedure
SE-CWE406-041 — return value used from procedure
SE-CWE611-054 — return value used from procedure
SE-CWE200-016 — return value used from procedure

Code Quality / Low Priority Findings

These findings may not represent security vulnerabilities but should be cleaned later if time allows:

unused imports
unused local variables
import * namespace pollution
mixed implicit/explicit returns

Manual Review Table

| Sample ID     | CodeQL Finding                                | Severity       | Initial Review Status | Preliminary Verdict            | Notes                                                        |
| ------------- | --------------------------------------------- | -------------- | --------------------- | ------------------------------ | ------------------------------------------------------------ |
| SE-CWE099-010 | Uncontrolled path expression                  | error          | flagged_needs_review  | likely_remaining_vulnerability | Needs review for path traversal or unsafe file access.       |
| SE-CWE434-044 | Uncontrolled path expression                  | error          | flagged_needs_review  | likely_remaining_vulnerability | File upload path handling may still be unsafe.               |
| SE-CWE641-055 | Uncontrolled path expression                  | error          | flagged_needs_review  | likely_remaining_vulnerability | Review path handling and validation logic.                   |
| SE-CWE116-012 | Uncontrolled path expression                  | error          | flagged_needs_review  | review_needed                  | Review whether path is properly constrained.                 |
| SE-CWE918-067 | Reflected XSS / SSRF                          | error          | flagged_needs_review  | likely_remaining_vulnerability | High-priority review; may require repair refinement.         |
| SE-CWE090-007 | LDAP query from user-controlled input         | error          | flagged_needs_review  | likely_remaining_vulnerability | Review escaping and LDAP filter construction.                |
| SE-CWE094-008 | Information exposure through exception        | error          | flagged_needs_review  | repair_quality_issue           | Should avoid exposing exception details externally.          |
| SE-CWE601-052 | Unvalidated redirect / uninitialized variable | error          | flagged_needs_review  | likely_remaining_vulnerability | High-priority review; redirect validation may be incomplete. |
| SE-CWE117-013 | Potentially uninitialized variable            | error          | flagged_needs_review  | repair_quality_issue           | May require code cleanup.                                    |
| Multiple      | Unused imports / unused variables             | recommendation | flagged_needs_review  | code_quality_issue             | Lower priority cleanup.                                      |


Preliminary Interpretation

CodeQL identified several findings that are stronger candidates for true remaining vulnerabilities than the Bandit findings.

These results support the need for:

fix verification
manual review
repair-quality calibration
context-aware repair generation
static-analysis-assisted validation

The findings should not be used as final Experiment 2 results until manual review and any required reruns are complete.

Next Actions
Inspect high-priority CodeQL findings.
Repair or regenerate confirmed weak secure samples.
Rerun CodeQL after fixes.
Update final verdicts.
Use validated results later for Experiment 2 if appropriate.