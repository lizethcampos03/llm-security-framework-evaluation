# Bandit Manual Review Log

## Purpose

This document records manual review observations for Bandit findings generated during Phase 2 dataset validation.

Bandit detections on secure samples are not automatically treated as false positives.

Each flagged case should be manually reviewed before final classification.

---

## Bandit Run Summary

Run date: 2026-05-28  
Target directory:

```text
datasets/securityeval_expanded/secure

Bandit output files:

datasets/securityeval_expanded/validation/bandit/bandit_secure_results.json
datasets/securityeval_expanded/validation/bandit/bandit_secure_results.txt

Total findings:

18

Severity summary:

Low: 10
Medium: 1
High: 7

Confidence summary:

Medium: 3
High: 15

Review Labels

flagged_needs_review
confirmed_safe_false_positive
confirmed_remaining_vulnerability
needs_fix_regeneration
repair_quality_issue
tool_error

Initial Manual Review Table

| Sample ID      | Bandit Rule | Severity | Confidence | Initial Review Status | Preliminary Verdict            | Notes                                                                                                             |
| -------------- | ----------- | -------- | ---------- | --------------------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| SE-CWE078-003  | B404        | Low      | High       | reviewed_preliminary  | likely_false_positive          | Subprocess import is expected for this secure rewrite; review together with B603.                                 |
| SE-CWE078-003  | B603        | Low      | High       | reviewed_preliminary  | review_needed                  | Uses shell=False, but command arguments may not enforce the allowlist strictly enough. Consider refinement later. |
| SE-CWE089-006  | B106        | Low      | Medium     | reviewed_preliminary  | repair_quality_issue           | Empty database password placeholder should be avoided in secure sample.                                           |
| SE-CWE095-009  | B307        | Medium   | High       | reviewed_preliminary  | likely_remaining_vulnerability | Secure sample still uses eval. This likely requires repair refinement.                                            |
| SE-CWE116-012  | B404        | Low      | High       | reviewed_preliminary  | likely_false_positive          | Subprocess import alone is not necessarily unsafe.                                                                |
| SE-CWE116-012  | B607        | Low      | High       | reviewed_preliminary  | review_needed                  | Uses partial executable path. Check whether command can be replaced with Python-native logic or absolute path.    |
| SE-CWE116-012  | B603        | Low      | High       | reviewed_preliminary  | review_needed                  | Uses subprocess with shell=False. Needs manual review to confirm user input is controlled.                        |
| SE-CWE1204-014 | B413        | High     | High       | reviewed_preliminary  | repair_quality_issue           | Uses deprecated pyCrypto-style imports. Should consider pyca/cryptography for stronger secure sample quality.     |
| SE-CWE1204-014 | B413        | High     | High       | reviewed_preliminary  | repair_quality_issue           | Same deprecated crypto-library concern.                                                                           |
| SE-CWE1204-014 | B413        | High     | High       | reviewed_preliminary  | repair_quality_issue           | Same deprecated crypto-library concern.                                                                           |
| SE-CWE306-026  | B105        | Low      | Medium     | reviewed_preliminary  | repair_quality_issue           | Hardcoded Flask secret placeholder should be replaced with environment-based configuration.                       |
| SE-CWE326-029  | B413        | High     | High       | reviewed_preliminary  | repair_quality_issue           | Uses deprecated pyCrypto-style RSA import. Should consider pyca/cryptography.                                     |
| SE-CWE327-030  | B413        | High     | High       | reviewed_preliminary  | repair_quality_issue           | Uses deprecated pyCrypto-style AES import. Should consider pyca/cryptography.                                     |
| SE-CWE327-030  | B413        | High     | High       | reviewed_preliminary  | repair_quality_issue           | Same deprecated crypto-library concern.                                                                           |
| SE-CWE327-030  | B413        | High     | High       | reviewed_preliminary  | repair_quality_issue           | Same deprecated crypto-library concern.                                                                           |
| SE-CWE522-050  | B106        | Low      | Medium     | reviewed_preliminary  | repair_quality_issue           | Empty database password placeholder should be avoided in secure sample.                                           |
| SE-CWE732-059  | B404        | Low      | High       | reviewed_preliminary  | review_needed                  | Subprocess import used to execute generated file. Needs review in context of this sample.                         |
| SE-CWE732-059  | B603        | Low      | High       | reviewed_preliminary  | review_needed                  | Uses subprocess with shell=False. Need to confirm this is acceptable or should be removed.                        |
Preliminary Findings

Bandit validation identified three main categories of issues:

1. Likely Tool Noise or Acceptable Warnings

Some subprocess-related findings may be acceptable after manual review, especially when:

shell=False is used
arguments are controlled
no user-controlled shell command is executed

These should not be automatically accepted, but they may become confirmed false positives after review.

2. Repair Quality Issues

Several findings suggest that secure counterparts could be improved, including:

empty password placeholders
hardcoded secret placeholders
deprecated crypto-library usage

These may not always represent the original target CWE, but they weaken secure sample quality.

3. Likely Remaining Vulnerability

The eval finding in SE-CWE095-009 is the strongest candidate for a remaining vulnerability and should be prioritized for repair refinement.

Next Actions
Manually inspect each flagged secure sample.
Prioritize likely remaining vulnerabilities and high-severity findings.
Repair or regenerate samples if necessary.
Rerun Bandit after fixes.
Update final verdicts after review and rerun.


