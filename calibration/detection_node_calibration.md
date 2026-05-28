# Detection Node Calibration

## Purpose

This document defines the calibration strategy for the detection node within the LLM security framework.

The detection node is responsible for analyzing code and determining whether a security vulnerability is present.

Calibration evaluates whether progressively richer contextual information improves vulnerability detection quality compared to simpler prompt-only detection approaches.

---

## Calibration Goal

The goal of detection-node calibration is to determine whether the workflow improves vulnerability detection quality through:

- CWE-guided reasoning
- security context profiles
- optimized prompt engineering
- structured output expectations
- workflow orchestration

The detection node should produce outputs that are:

- accurate
- consistent
- evidence-based
- context-aware
- useful for downstream repair generation

---

## Calibration Dataset

Detection calibration should use a smaller OWASP-focused calibration subset before final evaluation on the broader dataset.

The calibration subset may include:

- vulnerable samples
- secure samples
- CWE guidance
- security context profiles
- retrieval outputs
- expected labels
- detection outputs
- validation outputs
- manual review notes

---

## Detection Configurations

### Configuration A — Reference Baseline Detection

This configuration follows the reference paper methodology as closely as possible.

The model receives:

```text
vulnerable or secure code
+
basic reference-style detection prompt

This configuration serves as the baseline detection workflow.

Configuration B — CWE-Guided Detection

This configuration extends the baseline workflow by adding CWE security guidance.

The model receives:

vulnerable or secure code
+
basic detection prompt
+
CWE guidance

This configuration evaluates whether authoritative CWE security information improves detection quality.

Configuration C — Context-Aware Detection

This configuration approximates the intended final workflow.

The model receives:

vulnerable or secure code
+
CWE guidance
+
security context profile
+
optimized detection prompt
+
structured output expectations

This configuration evaluates the combined value of:

context engineering
prompt engineering
CWE-guided reasoning
workflow orchestration
Detection Evaluation Areas
Vulnerability Identification

The detector should correctly determine whether a vulnerability is present.

CWE Classification

The detector should correctly identify the relevant CWE where possible.

Evidence Quality

The detector should provide reasoning and evidence that support the conclusion.

Context Awareness

The detector should appropriately use the provided security and application context.

Output Usefulness

The detector output should be useful for downstream repair generation and reporting.

Structured Output Quality

The output should remain machine-readable and consistent enough for downstream workflow stages.

Detection Calibration Metrics

Calibration may record:

accuracy
precision
recall
false positives
false negatives
confidence
consistency across repeated runs
latency
explanation quality
evidence quality
Structured Detection Output

The detection node should produce structured outputs where possible.

Example fields:

{
  "overall_security_status": "vulnerable | safe | uncertain",
  "target_cwe": "",
  "summary": "",
  "evidence": [],
  "confidence": 0.0,
  "recommended_next_step": ""
}
Manual Review

Manual review is important during calibration.

Detections should be inspected to determine whether:

the vulnerability is actually present
the detected CWE is correct
the evidence supports the conclusion
the output is useful for downstream repair
the result should be marked as correct, incorrect, or needs review

A detection should not be accepted only because the LLM claimed the result is correct.

Relationship to Context Profiles and RAG

The detection node depends heavily on the quality of retrieved context.

The context profile and retrieval system are expected to influence:

CWE retrieval quality
retrieval relevance
detection reasoning quality
context-aware vulnerability analysis

Poor retrieval quality may negatively affect downstream detection quality.

Relationship to Validation Node

The detection node produces individual detection outputs.

The validation node improves reliability by running the detector multiple times and aggregating results.

Detection calibration focuses on improving the quality of each detection run.

Validation calibration focuses on determining the best repeated-run strategy and aggregation threshold.

Relationship to Fix Node

The detection output becomes an input to the fix node.

Therefore, detection quality directly affects repair quality.

Strong detection outputs should provide:

target CWE
vulnerable code evidence
reasoning summary
repair-relevant context
structured findings
Main Calibration Hypothesis

The primary hypothesis is:

CWE guidance
+
security context
+
optimized prompt engineering
improves vulnerability detection quality
compared to the reference-style baseline workflow.
Calibration Decision

After calibration, the following should be documented:

selected detection prompt
selected context fields
selected CWE/RAG input format
selected structured detection schema
selected validation settings
known detection limitations
examples of improved detection behavior
Future Directions

Future versions of the detection node may include:

multi-stage reasoning
GraphRAG-enhanced retrieval
confidence calibration
semantic code analysis
hybrid static-analysis integration
detector ensembles
retrieval ranking optimization
