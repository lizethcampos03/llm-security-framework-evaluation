# Fix Node Calibration

## Purpose

This document defines the calibration strategy for the fix node within the LLM security framework.

The purpose of the fix node is to generate secure repairs for vulnerable code while preserving the intended functionality of the original implementation.

The calibration process evaluates whether context-aware repair generation improves fix quality compared to simpler prompt-only approaches.

---

## Motivation

Traditional static analysis tools primarily focus on vulnerability detection.

However, modern LLM-based workflows can also recommend or generate secure repairs.

The fix node is intended to support:

- secure counterpart generation
- vulnerability remediation
- end-to-end secure code workflows
- downstream repair LLMs
- human reviewers

The repair process should produce fixes that are:

- secure
- functional
- readable
- context-aware
- auditable

---

## Calibration Hypothesis

The calibration process tests the hypothesis that repair quality improves when the model receives richer contextual information.

The workflow assumes that:

```text
vulnerable code
+
CWE guidance
+
security context profile
+
optimized prompt
=
higher-quality secure repair

compared to:

vulnerable code
+
simple repair prompt

Calibration Configurations
Configuration A: Prompt-Only Repair

The model receives:

vulnerable code
simple repair instruction

This configuration serves as a lightweight baseline.

Configuration B: CWE-Guided Repair

The model receives:

vulnerable code
CWE guidance
mitigation recommendations

This configuration evaluates the value of authoritative CWE information.

Configuration C: Context-Aware Repair

The model receives:

vulnerable code
CWE guidance
security context profile
application context
optimized repair instructions
structured repair expectations

This configuration approximates the intended final workflow.

Calibration Dataset

Calibration should use a smaller OWASP-focused subset.

The calibration dataset may contain:

vulnerable implementations
secure counterparts
context profiles
CWE guidance
manual review notes

This subset is reused during calibration before final experiments are executed on the broader dataset.

Calibration Evaluation Areas
Security Improvement

The generated repair should remove or mitigate the target vulnerability.

Functionality Preservation

The intended functionality of the original implementation should remain intact.

Secure Coding Quality

The repair should follow secure coding practices and avoid introducing additional vulnerabilities.

Context Awareness

The repair should appropriately reflect the provided security and application context.

Readability and Maintainability

The generated repair should remain understandable and professionally structured.

Report Usefulness

The generated report should provide enough evidence and explanation to support both human reviewers and downstream repair workflows.

Calibration Metrics

Calibration may record:

successful vulnerability removal
functionality preservation
Bandit results
CodeQL results
manual reviewer scores
repair readability
consistency across runs
latency
cost where available
Manual Review

Manual review is important during calibration.

Flagged repairs should be inspected to determine whether:

the vulnerability was fully mitigated
functionality changed unexpectedly
the repair introduced new risks
the repair quality is sufficient for evaluation purposes
Relationship to Secure Counterpart Generation

The secure counterpart dataset generation process contributes to fix-node calibration.

Observations made during secure counterpart generation may be used to:

improve repair prompts
improve context usage
refine structured outputs
identify weak repair patterns
strengthen mitigation quality

This allows dataset generation and calibration to reinforce each other.

Future Directions

Future versions of the fix node may include:

iterative repair loops
automatic repair verification
repair ranking
repair confidence estimation
multi-stage repair generation
GraphRAG-enhanced mitigation retrieval
repair benchmarking against additional LLM systems
