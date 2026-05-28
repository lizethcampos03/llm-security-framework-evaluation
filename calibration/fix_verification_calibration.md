# Fix Verification Calibration

## Purpose

This document defines the calibration strategy for the fix verification stage within the LLM security framework.

The fix verification stage evaluates whether generated repairs should be accepted before final reporting.

The purpose of this stage is to improve workflow reliability by reducing the risk of:

- incomplete repairs
- incorrect repairs
- unsafe repairs
- syntax failures
- security regressions
- functionality-breaking repairs

---

## Motivation

The fix node should not be blindly trusted.

LLM-generated repairs may:

- fail to mitigate the target vulnerability
- introduce new vulnerabilities
- break functionality
- produce invalid code
- partially fix the issue

Therefore, the workflow introduces a dedicated verification stage after repair generation.

---

## Workflow Placement

The fix verification stage appears after repair generation:

```text
Detection
→ Validation
→ Fix
→ Fix Verification
→ Report

The verification stage determines whether the generated repair is reliable enough to continue through the workflow.

Verification Philosophy

The workflow assumes that secure repair generation should include verification.

The goal is not to assume perfect repairs, but to reduce workflow risk through verification and controlled regeneration.

The verification stage acts as a checkpoint before final reporting.

Verification Checks
Syntax Validation

The generated repair should produce valid code.

Examples:

Python syntax validation
parsing validation
structural validation

Invalid syntax should fail verification.

Target CWE Mitigation

The workflow should evaluate whether the original target vulnerability still appears to be present.

Examples:

shell injection still present
unsafe deserialization still present
missing authorization checks
weak input validation

The goal is to verify that the repair meaningfully mitigates the original issue.

Functionality Preservation

The workflow should evaluate whether the repair preserves the intended functionality of the original implementation.

The repair should not completely remove functionality unless explicitly required for security.

Security Regression Detection

The workflow should evaluate whether the repair introduces obvious new vulnerabilities.

Examples:

insecure workaround logic
unsafe bypasses
weaker authorization logic
unsafe fallback behavior
Optional Static Analysis Verification

Optional verification may include:

Bandit
CodeQL
syntax tools
linting tools

These tools may provide additional verification evidence.

Conditional Repair Loop

The workflow may use a conditional repair loop.

Example:

If verification passes:
    continue to report

If verification fails and attempts < max:
    regenerate repair

If verification fails and attempts >= max:
    continue with warning

Recommended initial setting:

max_fix_attempts = 2

The goal is to improve reliability without creating excessive workflow cost or latency.

Verification Configurations
Configuration A — Minimal Verification

Basic syntax and mitigation checks only.

Configuration B — Structured Verification

Syntax checks plus structured reasoning about:

vulnerability mitigation
functionality preservation
security regression
Configuration C — Context-Aware Verification

Verification using:

CWE guidance
security context profiles
structured verification prompts
workflow-aware reasoning

This configuration approximates the intended final workflow.

Verification Evaluation Areas
Verification Accuracy

Whether the verification stage correctly identifies weak or failed repairs.

Repair Acceptance Quality

Whether accepted repairs are genuinely higher quality.

False Verification Passes

Cases where weak repairs incorrectly pass verification.

False Verification Failures

Cases where valid repairs incorrectly fail verification.

Workflow Reliability

Whether the verification stage improves overall workflow trustworthiness.

Workflow Cost

Whether verification creates excessive latency or regeneration cost.

Verification Metrics

Calibration may record:

verification pass rate
regeneration frequency
syntax failure rate
remaining vulnerability rate
repair acceptance quality
workflow consistency
latency
cost where available
Manual Review

Manual review is important during calibration.

Verification results should be inspected to determine whether:

the verification logic is reasonable
repairs were incorrectly accepted
repairs were incorrectly rejected
regeneration improved repair quality
workflow reliability improved overall
Relationship to Detection Node

The fix verification stage depends heavily on detection quality.

Weak or incorrect detection outputs may negatively affect:

repair quality
mitigation verification
workflow reliability
Relationship to Context Profiles and RAG

Verification quality may improve when the workflow receives:

relevant CWE guidance
contextual security expectations
deployment-specific requirements
threat-sensitive reasoning

The calibration process should evaluate whether context-aware verification improves reliability.

Main Verification Hypothesis

The primary hypothesis is:

Verification checkpoints
+
controlled regeneration
+
context-aware verification
improve workflow reliability and repair quality.
Calibration Decision

After calibration, the following should be documented:

selected verification strategy
selected verification prompts
selected regeneration policy
selected maximum repair attempts
selected verification outputs
known verification limitations
examples of improved workflow reliability
Future Directions

Future verification improvements may include:

automated testing integration
symbolic verification
repair ranking
confidence estimation
multi-stage verification
workflow-aware repair feedback
static-analysis-guided regeneration
