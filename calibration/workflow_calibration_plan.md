# Workflow Calibration Plan

## Purpose

This document defines the workflow calibration stage for the LLM security framework.

Calibration is the engineering stage that occurs before final experiments. Its purpose is to refine the workflow architecture, prompts, context usage, retrieval strategy, validation behavior, fix generation, fix verification, and reporting format before the final tool is evaluated.

Calibration is not the final experiment. Calibration improves the tool. Final experiments evaluate the frozen tool.

---

## Calibration Philosophy

The framework begins from a research-driven hypothesis:

```text
A context-aware, retrieval-supported, validated, and report-driven workflow can improve vulnerability detection and secure repair compared to simpler prompt-only LLM approaches.

Calibration tests this hypothesis on a smaller OWASP-focused subset before the architecture is frozen.

The calibration cycle is:

Observation
→ Hypothesis
→ Adjustment
→ Evaluation
→ Decision

High-Level Calibration Flow

The final calibration process follows this order:

Context Profile + RAG Calibration
→ Detection Node Calibration
→ Fix Node Calibration
→ Fix Verification Calibration
→ Report Node Calibration
→ Validation Run Calibration
→ Architecture Freeze

This order matters because retrieval and context quality affect detection, fixing, verification, and reporting.

Calibration Dataset

Calibration should use a smaller OWASP-focused subset rather than the full final evaluation dataset.

The calibration subset may include:

vulnerable samples
secure counterparts
CWE guidance
security context profiles
retrieval outputs
detection outputs
fix outputs
fix verification outputs
generated reports
manual review notes

The broader dataset should be reserved for final evaluation after calibration is complete.

Phase 1 — Context Profile + RAG Calibration

This phase calibrates how security context profiles and retrieval work together.

The goal is to improve the quality of CWE/security guidance retrieved for each case.

This phase evaluates:

whether the context profile improves retrieval quality
whether hybrid search reduces noisy retrieval
whether retrieved CWE guidance is relevant
whether retrieved context improves downstream detection
whether retrieved context improves downstream repair
which context fields are valuable without overburdening the user

RAG is calibrated based on workflow usefulness, not only similarity scores.

Phase 2 — Detection Node Calibration

This phase evaluates whether richer context improves vulnerability detection.

Configuration A — Reference Baseline Detection

The model receives:

code
+
basic reference-style detection prompt

This configuration follows the reference paper methodology as closely as possible.

Configuration B — CWE-Guided Detection

The model receives:

code
+
basic detection prompt
+
CWE guidance

This tests whether authoritative CWE information improves detection.

Configuration C — Context-Aware Detection

The model receives:

code
+
CWE guidance
+
security context profile
+
optimized detection prompt
+
structured output expectations

This tests the combined value of context engineering, prompt engineering, CWE-guided reasoning, and workflow orchestration.

Phase 3 — Fix Node Calibration

This phase evaluates whether richer context improves secure repair quality.

Configuration A — Reference Baseline Repair

The model receives:

vulnerable code
+
basic reference-style repair prompt

This configuration follows the reference paper methodology as closely as possible.

Configuration B — CWE-Guided Repair

The model receives:

vulnerable code
+
basic repair prompt
+
CWE guidance

This tests whether CWE guidance improves repair quality.

Configuration C — Context-Aware Repair

The model receives:

vulnerable code
+
CWE guidance
+
security context profile
+
optimized repair prompt
+
structured output expectations

This tests whether context-aware repair improves secure code quality.

Phase 4 — Fix Verification Calibration

The fix node should not be trusted blindly.

A fix verification stage is added after repair generation:

Detection
→ Validation
→ Fix
→ Fix Verification
→ Report

The fix verification stage checks:

syntax validity
target CWE mitigation
functionality preservation
new vulnerability introduction
optional Bandit/CodeQL results

A conditional loop may be used:

If verification passes:
    continue to report

If verification fails and attempts < max:
    regenerate repair

If verification fails and attempts >= max:
    continue to report with warning

Recommended initial setting:

max_fix_attempts = 2
Phase 5 — Report Node Calibration

This phase evaluates whether structured reports improve auditability and downstream repair.

The report should support:

human code reviewers
experiment comparison
downstream fix LLMs
reproducibility
evidence-based decisions

The report node should make the workflow more trustworthy, not just more verbose.

Phase 6 — Validation Run Calibration

This phase determines the best repeated-validation strategy for detection.

Test:

4 runs
8 runs
12 runs

Evaluate:

accuracy
false-positive rate
consistency
latency
cost

The selected setting should balance reliability and efficiency.

Calibration Metrics

Calibration may record:

detection accuracy
precision
recall
false positives
false negatives
confidence
consistency
fix quality
vulnerability removal
functionality preservation
report usefulness
retrieval relevance
latency
cost where available
Calibration Outputs

Calibration should produce:

calibration logs
prompt/version decisions
context profile decisions
RAG retrieval decisions
fix verification decisions
validation-run decisions
report-format decisions
comparison tables
notes explaining why changes were accepted or rejected
Relationship to Final Experiments

Calibration is separate from final experiments.

Calibration improves the tool.

Final experiments evaluate the frozen tool.

This separation helps avoid tuning the tool directly on the final evaluation results.

Architecture Freeze

Calibration ends when the workflow is stable enough to freeze.

At that point, the following should be documented:

detector prompt
fixer prompt
fix verification logic
context profile schema
RAG retrieval strategy
validation run count
aggregation threshold
report format
model choices
conditional loop behavior

After the architecture is frozen, final experiments can begin.
