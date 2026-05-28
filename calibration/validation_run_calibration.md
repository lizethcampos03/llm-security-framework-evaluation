# Validation Run Calibration

## Purpose

This document defines the calibration strategy for repeated validation within the LLM security framework.

The validation stage improves workflow reliability by executing the detection node multiple times and aggregating the results.

The purpose of validation calibration is to determine the optimal balance between:

- reliability
- consistency
- false-positive reduction
- false-negative reduction
- workflow cost
- workflow latency

---

## Motivation

LLM outputs may vary across runs.

A single detection result may be:

- inconsistent
- uncertain
- hallucinated
- incomplete
- overly confident

The workflow therefore introduces repeated validation and aggregation to improve overall reliability.

---

## Workflow Placement

The validation stage appears after detection:

```text
Detection
→ Validation
→ Fix
→ Fix Verification
→ Report

The validation stage aggregates multiple detection runs before downstream repair generation.

Validation Philosophy

The workflow assumes that repeated reasoning may improve reliability.

Instead of trusting a single detection result, the workflow evaluates multiple outputs and aggregates them using a configurable threshold.

The goal is not perfect certainty, but improved workflow robustness.

Validation Configurations
Configuration A — Single Detection Run

Only one detection result is used.

This configuration acts as the baseline workflow.

Configuration B — Moderate Validation

A moderate number of repeated runs is used.

Example:

4 runs

This configuration evaluates whether repeated reasoning improves consistency without excessive cost.

Configuration C — Extended Validation

A larger number of repeated runs is used.

Examples:

8 runs
12 runs

This configuration evaluates whether additional runs meaningfully improve workflow reliability.

Aggregation Strategy

The workflow aggregates repeated detection outputs using configurable thresholds.

Examples:

50% threshold
majority threshold
high-confidence threshold

The calibration process should determine which aggregation strategy provides the best tradeoff.

Validation Evaluation Areas
Consistency Improvement

Whether repeated runs reduce inconsistent outputs.

False Positive Reduction

Whether repeated validation reduces incorrect vulnerability detections.

False Negative Reduction

Whether repeated validation reduces missed vulnerabilities.

Confidence Stability

Whether confidence estimates become more stable across runs.

Workflow Reliability

Whether downstream repair quality improves due to more reliable detection outputs.

Workflow Cost

Whether repeated validation creates excessive latency or API cost.

Validation Metrics

Calibration may record:

detection consistency
agreement rate
false-positive rate
false-negative rate
confidence stability
downstream repair quality
validation latency
API cost where available
Example Aggregation Output

Example aggregated validation output:

{
  "validation_status": "vulnerable",
  "agreement_rate": 0.75,
  "target_cwe": "CWE-089",
  "confidence": 0.82,
  "runs": 8,
  "summary": "Most runs identified SQL injection behavior."
}
Manual Review

Manual review is important during calibration.

Validation outputs should be inspected to determine whether:

aggregation improves reliability
repeated runs reduce noise
repeated runs reduce hallucinations
the selected threshold is reasonable
additional runs meaningfully improve workflow quality
Relationship to Detection Node

The validation stage depends on the quality of individual detection outputs.

Detection calibration improves each run.

Validation calibration improves aggregation across runs.

Relationship to Workflow Reliability

Validation directly affects:

repair quality
verification quality
report quality
experiment reliability

Weak validation may propagate incorrect findings throughout the workflow.

Main Validation Hypothesis

The primary hypothesis is:

Repeated validation
+
aggregated reasoning
improve workflow reliability
compared to single-run detection.
Calibration Decision

After calibration, the following should be documented:

selected validation run count
selected aggregation threshold
selected confidence policy
selected validation outputs
known validation limitations
examples of improved workflow consistency
Future Directions

Future validation improvements may include:

adaptive validation depth
confidence-aware validation
detector ensembles
weighted aggregation
workflow-aware validation policies
uncertainty estimation
validation-feedback integration
