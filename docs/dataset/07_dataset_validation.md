# Dataset Validation Plan

## Purpose

This document defines the dataset validation strategy for the SecurityEval-derived contextual vulnerability benchmark.

The goal of validation is to determine whether the vulnerable and secure samples are trustworthy enough to support calibration, experimentation, and reporting.

This document is created during Phase 1 as a validation plan and template. The actual validation results will be added during Phase 2.

---

## Validation Philosophy

The dataset should not be trusted only because vulnerable and secure labels exist.

Each sample should be validated through a combination of:

- syntax checks
- metadata checks
- manual review
- Bandit analysis
- CodeQL analysis
- repair-quality review
- context/profile consistency checks

Validation is used to identify:

- formatting errors
- invalid Python files
- incorrect metadata
- remaining vulnerabilities in secure samples
- false positives from tools
- samples that require repair or regeneration

---

## Dataset Components to Validate

The validation process applies to:

```text
datasets/securityeval_expanded/vulnerable/
datasets/securityeval_expanded/secure/
datasets/securityeval_expanded/metadata/
datasets/securityeval_expanded/context_profiles/
datasets/securityeval_expanded/validation/
Validation Inputs

Validation may use:

vulnerable.py files
secure.py files
metadata.json files
CWE guidance data
secure generation inputs
context profiles
Bandit outputs
CodeQL outputs
manual review notes
Validation Step 1 — Dataset Integrity Audit

The dataset integrity audit checks:

number of vulnerable samples
number of secure samples
required files per sample
Python syntax validity
JSON validity
missing metadata
obvious placeholder values
formatting issues

Expected checks include:

69 vulnerable samples
69 secure samples
vulnerable.py exists
secure.py exists
metadata.json exists
generation_notes.md exists for secure samples
validation_notes.md exists for vulnerable samples
Validation Step 2 — Vulnerable Sample Review

Vulnerable samples should be checked to confirm:

they originate from SecurityEval vulnerable reference implementations
they preserve the original intended vulnerable behavior
only formatting transformations were applied where necessary
the target CWE is represented
metadata correctly records the CWE and task information
Validation Step 3 — Secure Sample Review

Secure samples should be checked to confirm:

intended functionality is preserved
the target CWE is mitigated
the secure code follows relevant CWE mitigation guidance
the repair does not introduce obvious new vulnerabilities
the secure code is syntactically valid
manual review supports the secure label
Validation Step 4 — Bandit Validation

Bandit will be used to scan the generated secure samples.

Bandit outputs should be stored as raw validation artifacts before being interpreted.

Bandit detections on secure samples should initially be labeled:

flagged_needs_review

They should not automatically be treated as false positives.

After manual review, each finding may be categorized as:

confirmed_safe_false_positive
confirmed_remaining_vulnerability
needs_fix_regeneration
tool_error
Validation Step 5 — CodeQL Validation

CodeQL will be used to scan generated secure samples where applicable.

CodeQL outputs should be stored as raw validation artifacts before being interpreted.

As with Bandit, CodeQL detections on secure samples should initially be labeled:

flagged_needs_review

Manual review should determine whether the finding is valid, a false positive, a dataset issue, or a tool/configuration issue.

Validation Step 6 — Manual Review

Manual review is required for:

flagged secure samples
tool disagreements
unclear cases
samples with suspicious repair quality
samples with syntax or metadata issues

Manual review should answer:

Is the target CWE actually mitigated?
Is functionality preserved?
Did the repair introduce a new vulnerability?
Is the tool finding valid?
Does the sample need regeneration or repair?
Validation Verdict Labels

Use the following labels:

clean
flagged_needs_review
confirmed_safe_false_positive
confirmed_remaining_vulnerability
needs_fix_regeneration
fixed_and_rerun_required
tool_error
Validation Output Structure

Recommended folders:

datasets/securityeval_expanded/validation/
├── integrity_audit/
├── bandit/
├── codeql/
├── manual_review/
└── summaries/

Recommended summary files:

secure_validation_summary.csv
bandit_secure_results.json
codeql_secure_results.sarif
manual_review_log.md
Validation Summary Schema

A validation summary should include:

sample_id
sample_type
tool
tool_flagged
rule_id
severity
confidence
initial_verdict
manual_review_status
final_verdict
rerun_required
notes
Relationship to Calibration

Dataset validation supports workflow calibration.

Validation helps identify:

weak secure repairs
remaining vulnerabilities
noisy tool findings
repair-quality issues
context or retrieval issues

These observations may inform:

fix node calibration
fix verification calibration
context/RAG calibration
report node calibration
Relationship to Experiment 2

Validation outputs may later support Experiment 2, but they should not be treated as final experiment results until:

raw outputs are saved
manual review is complete
flagged findings are categorized
any required repairs are made
reruns are performed if needed

This prevents premature or unfair claims.

Status

Current status:

Validation plan created.
Formal Phase 2 validation pending.
Bandit validation pending.
CodeQL validation pending.
Manual review pending.
Future Updates

During Phase 2, this document should be updated with:

validation run dates
Bandit version
CodeQL version
scan commands
output file locations
number of flagged samples
manual review findings
final validation summary
