# Calibration Framework

## Purpose

The calibration phase is conducted before formal experimentation and serves as the primary mechanism for refining the framework architecture, improving reliability, and documenting evidence-driven design decisions.

Calibration is not intended to maximize benchmark performance through repeated trial-and-error. Instead, it provides a structured methodology for understanding system behavior, identifying weaknesses, evaluating architectural modifications, and documenting decisions that influence subsequent experimentation.

The outcome of calibration is a stable framework configuration that can be evaluated through controlled experiments.

---

## Calibration Philosophy

The project adopts an evidence-driven calibration methodology based on iterative observation and refinement.

Each calibration cycle follows the process:

Observation
↓
Hypothesis
↓
Adjustment
↓
Evaluation
↓
Decision

Observed behaviors motivate hypotheses regarding architectural improvements. Proposed modifications are implemented and evaluated. Results are documented and ultimately accepted, rejected, or revised.

This process creates a transparent record of architectural evolution and supports reproducibility.

---

## Task-Specialized LLM Configuration

This project does not conduct a broad large-language-model comparison study.

Instead, the framework adopts a deliberately selected task-specialized LLM configuration based on the differing requirements of vulnerability detection and secure code remediation.

The selected configuration is:

Detection Model
- Claude Opus
- Responsible for vulnerability analysis, contextual security reasoning, explanation generation, and vulnerability classification

Repair Model
- Claude Sonnet
- Responsible for remediation generation, secure code rewriting, and vulnerability-fix recommendations

The objective of calibration is therefore not to determine which model is "best" among multiple candidates. Instead, calibration focuses on understanding how the selected configuration behaves within the overall framework architecture.

The primary research contribution of the project is the orchestration workflow itself, including contextual grounding, retrieval augmentation, validation mechanisms, remediation generation, and structured reporting.

---

## Calibration Areas

Calibration activities focus on the following framework components:

### Security Context Engineering

Evaluation and refinement of contextual information provided to the detection process.

Areas of interest include:

- Business logic context
- Authorization assumptions
- Operational assumptions
- Intended application behavior
- Security concerns supplied by the user

---

### Retrieval-Augmented Security Knowledge

Evaluation of security knowledge retrieval quality.

Areas of interest include:

- CWE retrieval accuracy
- CVE retrieval usefulness
- Context relevance
- Retrieval completeness
- Retrieval ranking quality

---

### Prompt Engineering

Evaluation of detector and repair prompts.

Areas of interest include:

- Detection consistency
- Explanation quality
- Vulnerability classification quality
- Structured output reliability
- Repair usefulness

---

### Validation Methodology

Evaluation of the framework's multi-run validation strategy.

The validation stage does not use a separate evaluator model.

Instead, the detection process is executed repeatedly and aggregated using threshold-based majority voting.

Calibration activities investigate:

- Consistency across runs
- Vote distributions
- Confidence aggregation
- Stability of final decisions
- Sensitivity to threshold selection

---

### Explanation Quality

Evaluation of:

- Clarity
- Technical correctness
- Supporting evidence
- Actionability
- Human interpretability

---

### Remediation Quality

Evaluation of generated fixes.

Areas of interest include:

- Vulnerability removal
- Functional preservation
- Security improvement
- Explanation quality
- Code quality

---

## Calibration Metrics

The following metrics may be recorded during calibration activities:

### Detection Metrics

- Detection consistency
- Vote agreement percentage
- Vulnerable vote ratio
- Safe vote ratio
- Uncertain vote ratio
- Average confidence

### Retrieval Metrics

- Context relevance
- CWE retrieval accuracy
- CVE retrieval usefulness
- Retrieval coverage

### Repair Metrics

- Vulnerability removal success
- Functional correctness
- Fix completeness
- Repair quality assessment

### Operational Metrics

- Latency
- Token usage
- Workflow efficiency

---

## Calibration Deliverables

Calibration activities generate:

- Calibration logs
- Architectural observations
- Design decisions
- Prompt revisions
- Retrieval refinements
- Validation analyses
- Updated framework documentation

These artifacts provide traceability between observed behaviors, implemented modifications, and final architectural decisions.

---

## Relationship to Experiments

Calibration precedes formal experimentation.

The purpose of calibration is to establish a stable framework configuration suitable for evaluation.

Once calibration is complete, experimental studies evaluate:

1. Safe versus vulnerable classification performance
2. Comparative performance against static-analysis tools
3. End-to-end workflow integration effectiveness

Experimental results are reported separately from calibration findings.

---

## Guiding Principle

Calibration is used to understand and improve the selected framework configuration.

The goal is not to rank language models.

The goal is to improve the reliability, explainability, contextual reasoning capability, remediation quality, and overall effectiveness of the orchestration workflow.
