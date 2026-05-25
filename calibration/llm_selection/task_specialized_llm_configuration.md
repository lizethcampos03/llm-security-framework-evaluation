# Task-Specialized LLM Configuration

## Purpose

This document records the selected large language model configuration used by the framework and explains the rationale behind the decision.

The purpose of this document is not to compare language models or establish model rankings. Instead, it documents the task-specialized configuration adopted for framework calibration and experimentation.

The selected configuration reflects the differing requirements of vulnerability detection and secure code remediation within the orchestration workflow.

---

# Architectural Principle

Different security-analysis tasks place different demands on language models.

Vulnerability detection requires:

- Security reasoning
- Contextual interpretation
- Business-logic understanding
- Authorization analysis
- Vulnerability classification
- Explainability

Secure remediation requires:

- Code generation
- Code transformation
- Refactoring
- Secure implementation generation
- Preservation of intended functionality

Because these tasks emphasize different capabilities, the framework adopts a task-specialized model allocation strategy.

---

# Selected Configuration

## Vulnerability Detection

Model:

Claude Opus

Responsibilities:

- Vulnerability identification
- Contextual vulnerability reasoning
- Security analysis
- Vulnerability classification
- Security explanation generation
- Structured detection output generation

The detector is responsible for determining whether vulnerabilities exist and producing the evidence required to support the decision.

---

## Secure Code Remediation

Model:

Claude Sonnet

Responsibilities:

- Secure code repair
- Vulnerability remediation generation
- Secure implementation suggestions
- Refactored code generation
- Fix explanation generation

The repair model receives validated vulnerability findings and produces remediation recommendations intended to remove identified weaknesses while preserving intended functionality.

---

# Validation Architecture

The framework does not employ a separate validation model.

Instead, validation is performed through repeated execution of the vulnerability-detection process.

Current validation configuration:

- Number of detector runs: 10
- Validation threshold: 0.50
- Aggregation method: majority voting

Each detector execution produces an independent detection result.

The validation stage aggregates:

- Vulnerable votes
- Safe votes
- Uncertain votes
- Confidence values

These results are combined to produce:

- Final decision
- Average confidence
- Consistency score
- Vote distribution statistics

This approach reduces sensitivity to stochastic model variation and provides additional transparency regarding detector reliability.

---

# Calibration Objectives

Calibration activities focus on understanding how the selected configuration behaves within the framework.

Areas of investigation include:

- Detection consistency
- Contextual reasoning quality
- Security explanation quality
- Retrieval effectiveness
- Confidence behavior
- Validation stability
- Repair quality
- Latency
- Cost characteristics

The objective is to improve workflow performance rather than identify a superior language model.

---

# Relationship to Framework Research Questions

The selected configuration supports investigation of all framework research questions.

RQ1:
Architectural calibration and evolution

RQ2:
Contextual vulnerability reasoning

RQ3:
Comparative performance against static-analysis approaches

RQ4:
End-to-end workflow integration

The language models function as components within the broader orchestration framework and are evaluated in the context of overall workflow performance.

---

# Design Rationale

The project's primary contribution is the orchestration workflow rather than the underlying language models.

Consequently, the framework adopts a deliberately selected task-specialized configuration and focuses calibration efforts on:

- Workflow reliability
- Explainability
- Retrieval integration
- Validation mechanisms
- Remediation quality
- End-to-end security outcomes

rather than conducting a broad model-comparison study.

This decision allows development effort to be concentrated on architectural refinement and framework evaluation while maintaining the use of state-of-the-art reasoning and coding capabilities.
