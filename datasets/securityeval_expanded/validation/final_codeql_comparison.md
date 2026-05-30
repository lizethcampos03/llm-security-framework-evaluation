# Final CodeQL Comparison

## Purpose

This document summarizes CodeQL findings before and after manual review and refinement of secure counterparts generated for the SecurityEval-expanded dataset.

The objective of this review process was to determine whether CodeQL findings represented:

* remaining vulnerabilities
* repair-quality issues
* false positives
* implementation bugs
* dataset generation artifacts

and to improve secure counterparts where appropriate.

---

# Initial CodeQL Review

Initial CodeQL analysis identified several high-priority findings requiring manual review.

Reviewed samples:

| Sample        | Finding                      |
| ------------- | ---------------------------- |
| SE-CWE095-009 | eval usage                   |
| SE-CWE918-067 | Full SSRF                    |
| SE-CWE601-052 | Open redirect                |
| SE-CWE090-007 | LDAP query construction      |
| SE-CWE099-010 | Uncontrolled path expression |
| SE-CWE434-044 | Uncontrolled path expression |
| SE-CWE641-055 | Uncontrolled path expression |
| SE-CWE116-012 | Uncontrolled path expression |

---

# Manual Review Methodology

Each finding was manually reviewed using the following process:

1. Inspect CodeQL finding.
2. Review generated secure counterpart.
3. Determine whether finding represented:

   * remaining vulnerability
   * repair-quality issue
   * false positive
   * implementation defect
4. Refine secure counterpart where necessary.
5. Re-run dataset integrity audit.
6. Re-run Bandit validation.
7. Commit validated refinement.
8. Re-run CodeQL.

---

# First Refinement Pass

Refinements performed:

| Sample        | Action                                            |
| ------------- | ------------------------------------------------- |
| SE-CWE095-009 | Removed eval() usage                              |
| SE-CWE918-067 | Added allowlist validation and output handling    |
| SE-CWE601-052 | Replaced redirect targets with fixed mappings     |
| SE-CWE090-007 | Added LDAP DN allowlist                           |
| SE-CWE099-010 | Replaced path construction with file identifiers  |
| SE-CWE434-044 | Hardened upload path validation                   |
| SE-CWE641-055 | Replaced path construction with approved mappings |
| SE-CWE116-012 | Removed subprocess usage                          |

All refinements passed dataset integrity validation and Bandit validation.

---

# Post-Rerun Findings

After the first refinement pass, CodeQL findings were reduced substantially.

Remaining findings:

| Sample        | Finding                                       |
| ------------- | --------------------------------------------- |
| SE-CWE090-007 | LDAP query built from user-controlled sources |
| SE-CWE918-067 | Full SSRF                                     |
| SE-CWE094-008 | Information exposure through exception        |
| SE-CWE117-013 | Potentially uninitialized local variable      |

---

# Second Refinement Pass

Additional refinements performed:

| Sample        | Action                                                               |
| ------------- | -------------------------------------------------------------------- |
| SE-CWE090-007 | Replaced username flow with approved user mapping                    |
| SE-CWE918-067 | Replaced URL construction with fixed endpoint mappings               |
| SE-CWE116-012 | Replaced username path construction with approved directory mappings |
| SE-CWE094-008 | Removed exception detail disclosure                                  |
| SE-CWE117-013 | Fixed uninitialized variable handling                                |

All refinements again passed dataset integrity validation and Bandit validation.

---

# Findings Resolved

Resolved findings included:

* eval usage
* open redirect
* LDAP query construction
* SSRF URL construction
* uncontrolled path expressions
* exception information disclosure
* uninitialized variable defect

---

# Lessons Learned

The review process demonstrated that generated secure counterparts should not automatically be assumed secure.

Several generated repairs required:

* stronger allowlists
* removal of user-controlled resource construction
* elimination of dangerous primitives
* additional validation logic
* implementation bug fixes

Manual review combined with static analysis provided substantially stronger validation than either approach alone.

---

# Final Assessment

The review process significantly improved the quality of secure counterparts contained in the dataset.

Dataset integrity validation, Bandit validation, manual review, and CodeQL validation collectively provide evidence that the final dataset is substantially stronger than the initially generated secure counterparts and is suitable for experimental evaluation.
