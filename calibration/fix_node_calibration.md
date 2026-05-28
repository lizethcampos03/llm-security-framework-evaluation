# Fix Node Calibration

## Purpose

This document defines the calibration strategy for the fix node within the LLM security framework.

The fix node is responsible for generating secure repairs for vulnerable code while preserving the intended functionality of the original implementation.

Calibration evaluates whether progressively richer contextual information improves secure repair quality compared to simpler prompt-only repair approaches.

---

## Calibration Goal

The goal of fix-node calibration is to determine whether the workflow improves secure repair quality through:

- CWE-guided reasoning
- security context profiles
- optimized prompt engineering
- structured output expectations
- workflow orchestration

The fix node should generate repairs that are:

- secure
- functional
- readable
- context-aware
- auditable

---

## Calibration Dataset

Fix calibration should use a smaller OWASP-focused calibration subset before final evaluation on the broader dataset.

The calibration subset may include:

- vulnerable samples
- secure counterparts
- CWE guidance
- security context profiles
- repair outputs
- repair verification outputs
- Bandit outputs
- CodeQL outputs
- manual review notes

---

## Fix Configurations

### Configuration A — Reference Baseline Repair

This configuration follows the reference paper methodology as closely as possible.

The model receives:

```text
vulnerable code
+
basic reference-style repair prompt

This configuration serves as the baseline repair workflow.

Configuration B — CWE-Guided Repair

This configuration extends the baseline repair workflow by adding CWE security guidance.

The model receives:

vulnerable code
+
basic repair prompt
+
CWE guidance

This configuration evaluates whether authoritative CWE security information improves repair quality.

Configuration C — Context-Aware Repair

This configuration approximates the intended final workflow.

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

This configuration evaluates the combined value of:

context engineering
prompt engineering
CWE-guided reasoning
workflow orchestration
Repair Evaluation Areas
Vulnerability Removal

The generated repair should remove or mitigate the target vulnerability.

Functionality Preservation

The intended behavior of the original implementation should remain intact.

Secure Coding Quality

The repair should follow secure coding practices and avoid introducing additional vulnerabilities.

Context Awareness

The repair should appropriately reflect the provided security and application context.

Readability and Maintainability

The generated repair should remain understandable and professionally structured.

Structured Output Quality

The repair output should remain machine-readable and consistent enough for downstream workflow stages.

Fix Calibration Metrics

Calibration may record:

successful vulnerability removal
functionality preservation
Bandit results
CodeQL results
manual reviewer scores
repair readability
repair consistency
repair latency
cost where available
Structured Repair Output

The fix node should produce structured outputs where possible.

Example fields:

{
  "fix_status": "success | partial | failed",
  "target_cwe": "",
  "repair_summary": "",
  "security_improvements": [],
  "remaining_risks": [],
  "fixed_code": "",
  "confidence": 0.0
}
Manual Review

Manual review is important during calibration.

Generated repairs should be inspected to determine whether:

the vulnerability was actually mitigated
functionality changed unexpectedly
the repair introduced new risks
the repair quality is sufficient for evaluation
the repair output is useful for downstream reporting

A repair should not be accepted only because the LLM claimed the repair was successful.

Relationship to Fix Verification

The fix node generates candidate repairs.

The fix verification stage evaluates whether the repair should be accepted.

The fix verification stage may evaluate:

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
    continue with warning

Recommended initial setting:

max_fix_attempts = 2
Relationship to Context Profiles

Security context profiles are expected to influence repair quality.

Examples of context-sensitive repair behavior include:

stricter authorization requirements
stronger logging requirements
stricter validation logic
deployment-specific security expectations
protection of sensitive assets

The calibration process should evaluate whether contextual information meaningfully improves repair quality.

Relationship to Secure Counterpart Generation

The secure counterpart generation process contributes to fix-node calibration.

Observations made during secure counterpart generation may be used to:

improve repair prompts
improve context usage
refine structured outputs
identify weak repair patterns
strengthen mitigation quality

Dataset generation and calibration should reinforce each other.

Main Calibration Hypothesis

The primary hypothesis is:

CWE guidance
+
security context
+
optimized prompt engineering
improves secure repair quality
compared to the reference-style baseline workflow.
Calibration Decision

After calibration, the following should be documented:

selected repair prompt
selected context fields
selected CWE/RAG input format
selected structured repair schema
selected verification strategy
selected conditional loop behavior
known repair limitations
examples of improved repair behavior
Future Directions

Future versions of the fix node may include:

iterative repair loops
automatic repair verification
repair ranking
repair confidence estimation
multi-stage repair generation
GraphRAG-enhanced mitigation retrieval
repair benchmarking against additional LLM systems
