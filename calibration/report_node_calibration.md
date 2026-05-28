# Report Node Calibration

## Purpose

This document defines the calibration strategy for the report node within the LLM security framework.

The report node is responsible for generating structured, human-readable, and workflow-useful security reports based on the outputs of previous workflow stages.

The goal of the report node is not only to summarize findings, but also to improve:

- auditability
- repair usefulness
- workflow transparency
- downstream workflow support
- evidence-based reasoning

---

## Motivation

Traditional security tools often provide outputs that are:

- difficult to interpret
- incomplete
- inconsistent
- difficult to use for downstream repair

The workflow assumes that report quality directly affects the usefulness of the overall system.

A strong report should help:

- human reviewers
- downstream repair workflows
- experiment analysis
- reproducibility
- audit processes

---

## Workflow Placement

The report node appears near the end of the workflow:

```text
Detection
→ Validation
→ Fix
→ Fix Verification
→ Report

The report aggregates and organizes information from earlier workflow stages.

Report Philosophy

The report should act as:

a workflow summary
an evidence container
a repair-support document
a security reasoning artifact

The report should improve trustworthiness, not simply increase output length.

Report Inputs

The report node may receive:

vulnerable code
secure repair
detection findings
validation outputs
fix verification outputs
CWE guidance
security context profiles
retrieval outputs
confidence values
workflow metadata
Report Goals
Human Readability

The report should remain understandable for human reviewers.

Evidence Clarity

The report should clearly explain:

why a vulnerability was detected
what evidence supports the conclusion
why the repair was generated
whether verification passed
Structured Consistency

The report should remain consistent enough for downstream workflow stages and experiment analysis.

Repair Support

The report should provide useful repair-relevant information for downstream repair workflows or repair LLMs.

Auditability

The report should support:

manual inspection
experiment reproducibility
workflow transparency
research analysis
Report Configurations
Configuration A — Minimal Reporting

Basic vulnerability summary only.

Configuration B — Structured Reporting

Structured detection findings, repair outputs, and verification summaries.

Configuration C — Context-Aware Reporting

Structured reporting using:

CWE guidance
context profiles
verification outputs
workflow-aware explanations
evidence-based reasoning

This configuration approximates the intended final workflow.

Report Evaluation Areas
Clarity

Whether the report is understandable and logically organized.

Evidence Usefulness

Whether the report provides meaningful supporting evidence.

Repair Usefulness

Whether the report helps downstream repair generation or repair review.

Structured Consistency

Whether reports remain consistently formatted across cases.

Workflow Transparency

Whether the report improves understanding of workflow decisions.

Report Completeness

Whether important workflow information is missing.

Report Metrics

Calibration may record:

readability
evidence usefulness
repair usefulness
report completeness
structured consistency
workflow transparency
report latency
report length
Structured Report Example Fields

Example report fields may include:

{
  "overall_security_status": "",
  "target_cwe": "",
  "detection_summary": "",
  "evidence": [],
  "repair_summary": "",
  "verification_summary": "",
  "remaining_risks": [],
  "confidence": 0.0
}
Manual Review

Manual review is important during calibration.

Reports should be inspected to determine whether:

the report is understandable
the evidence is useful
the repair explanation is meaningful
the report supports downstream workflows
the report improves auditability
Relationship to Experiment 3

The report node is especially important for the end-to-end workflow experiment.

The workflow hypothesis assumes that structured reports improve:

downstream repair quality
workflow integration
human review usefulness
workflow trustworthiness
Main Report Hypothesis

The primary hypothesis is:

Structured, context-aware, evidence-based reports
improve workflow usefulness,
repair support,
and auditability.
Calibration Decision

After calibration, the following should be documented:

selected report format
selected report fields
selected evidence structure
selected workflow summaries
known reporting limitations
examples of improved report usefulness
Future Directions

Future report improvements may include:

interactive reports
visualization support
report confidence estimation
workflow trace visualization
multi-stage workflow summaries
human feedback integration
