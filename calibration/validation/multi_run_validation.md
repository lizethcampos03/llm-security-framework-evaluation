# Multi-Run Validation Methodology

## Purpose

This document describes the validation methodology used by the framework.

The validation stage is designed to improve reliability by reducing sensitivity to stochastic variation in LLM-based vulnerability detection.

The validator is not a separate language model. Instead, it repeatedly invokes the detection node and aggregates the detector outputs.

---

## Validation Design

The validation node performs multi-run verification.

The detection node is executed multiple times on the same input. Each run produces a detection result that includes a security status, findings, confidence values, and a summary.

The validation node then aggregates those results to produce a final decision.

Current configuration:

- Number of runs: 10
- Validation threshold: 0.50
- Aggregation method: threshold-based majority voting

---

## Validation Inputs

The validation node receives the current workflow state, including the preprocessed code, retrieved context, security context, and configuration values.

Relevant configuration fields include:

- `number_of_runs`
- `validation_threshold`

If these values are not supplied, the default configuration is:

- `number_of_runs = 10`
- `validation_threshold = 0.5`

---

## Validation Process

For each run, the validation node invokes the detection node.

Each detection result is categorized as one of the following:

- vulnerable
- safe
- uncertain

The validation node counts:

- vulnerable votes
- safe votes
- uncertain votes

It also collects confidence values from individual findings when confidence values are available.

---

## Final Decision Rule

The validation node calculates the vulnerable ratio:

```text
vulnerable_ratio = vulnerable_votes / number_of_runs

The final decision is determined as follows:

If the vulnerable ratio is greater than or equal to the validation threshold, the final decision is vulnerable.
If safe votes exceed vulnerable votes and safe votes are at least as many as uncertain votes, the final decision is safe.
Otherwise, the final decision is uncertain.

This decision rule allows the framework to identify strong vulnerable decisions, strong safe decisions, and ambiguous cases.

Validation Outputs

The validation node produces a structured validation result containing:

validation method
number of runs
threshold
vulnerable votes
safe votes
uncertain votes
final decision
average confidence
consistency score
individual run results

The output supports both automated analysis and human inspection.

Consistency Score

The consistency score is calculated using the largest vote category:

consistency_score = max(vulnerable_votes, safe_votes, uncertain_votes) / number_of_runs

A higher consistency score indicates stronger agreement across detector runs.

A lower consistency score indicates that the detector is producing unstable or mixed judgments and may require further calibration.

Average Confidence

Average confidence is computed from confidence values reported in individual findings.

If no confidence values are available, average confidence is reported as 0.0.

Average confidence is useful for analyzing whether detector confidence aligns with vote stability and final correctness.

Role in Calibration

During calibration, the validation node is used to study:

detection stability
stochastic variation
sensitivity to context
sensitivity to retrieval quality
confidence behavior
threshold behavior
failure patterns

The goal is not only to produce a final label, but also to expose how reliable the detector appears across repeated runs.

Role in Experiments

During formal experiments, the validation result serves as the framework's final classification output.

For safe versus vulnerable classification experiments, the final decision is compared against the ground-truth label.

For comparative experiments, the validated framework output is compared against Bandit, CodeQL, and prior secure-code-agent methodologies.

Important Clarification

The validation node does not introduce a separate evaluator LLM.

It is an aggregation mechanism over repeated detector outputs.

This distinction is important because the framework's reliability improvement comes from repeated sampling and threshold-based voting, not from a second model judging the detector.


