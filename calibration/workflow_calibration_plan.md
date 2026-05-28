# Workflow Calibration Plan

## Purpose

This document defines the workflow calibration stage for the LLM security framework.

The purpose of calibration is to refine the tool before final evaluation. Calibration is not treated as the final experiment. Instead, it is an engineering and research step used to improve the architecture, prompts, context usage, validation strategy, and reporting format before the final experiments are executed.

---

## Calibration Philosophy

The tool begins from a research-driven architecture based on the hypothesis that context-aware orchestration can improve vulnerability detection and secure repair of LLM-generated code.

Calibration tests this hypothesis on a smaller OWASP-focused subset before the architecture is frozen.

The calibration process follows this cycle:

```text
Observation
→ Hypothesis
→ Adjustment
→ Evaluation
→ Decision

Calibration Scope

The calibration stage focuses on:

Detection quality
Fix quality
Context engineering
Prompt engineering
CWE/RAG guidance usage
Validation consistency
Report usefulness
Latency and cost tradeoffs
Calibration Dataset

Calibration should use a smaller OWASP-focused subset rather than the full final evaluation dataset.

The calibration subset may include:

vulnerable samples
secure counterparts
context profiles
CWE guidance
generated reports
tool outputs

This subset is used repeatedly during calibration. The broader dataset should be reserved for final evaluation after the tool architecture is frozen.

Main Calibration Configurations
Configuration A: Reference-Style Prompt Only

This configuration uses a minimal prompt style inspired by the reference methodology.

It is used as a baseline to understand how a simpler LLM approach performs without the full workflow context.

Configuration B: CWE-Guided Prompt

This configuration provides the vulnerable code and CWE guidance.

It tests whether authoritative CWE information improves detection and repair quality.

Configuration C: Full Workflow Context

This configuration simulates the final tool workflow by providing:

vulnerable code
CWE guidance
retrieved context
security context profile
optimized prompt
structured output expectations

This configuration tests the value of the full architecture.

Metrics

Calibration should record:

detection accuracy
false positives
false negatives
confidence
consistency across repeated runs
fix quality
functionality preservation
security improvement
report usefulness
latency
cost where available
Calibration Outputs

Calibration should produce:

calibration logs
comparison tables
prompt/version decisions
context-profile design decisions
validation-run decisions
notes explaining why changes were accepted or rejected
Relationship to Final Experiments

Calibration is separate from final experiments.

Calibration improves the tool.

Final experiments evaluate the frozen tool.

This separation helps avoid tuning the tool directly on the final evaluation results.

Final Calibration Decision

Calibration ends when the architecture is stable enough to freeze.

At that point, the following should be documented:

final detector prompt
final fixer prompt
final context profile schema
final CWE/RAG input format
final validation run count
final aggregation rule
final report format
final model choices
