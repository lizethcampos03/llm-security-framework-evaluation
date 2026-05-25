# Experimental Methodology

# Purpose

This document describes the experimental methodology used to evaluate the AI-Assisted Vulnerability Detection in LLM-Generated Code framework.

The objective of the experimental phase is to systematically investigate the effectiveness of contextual grounding, retrieval-augmented security knowledge, validation strategies, remediation generation, and workflow orchestration within AI-assisted vulnerability analysis.

The methodology is designed to support reproducibility, transparency, fair comparison, and evidence-based evaluation.

The experiments directly address the four research questions guiding the project and provide the empirical foundation for evaluating architectural decisions documented throughout the repository.

---

# Research Question Mapping

The experimental design is organized around four primary research questions.

## RQ1 – Architectural Calibration and Evolution

How do orchestration-oriented architectural components—including contextual grounding, retrieval augmentation, prompt engineering, and validation strategies—evolve through calibration, and how do they contribute to the effectiveness of LLM-based vulnerability analysis?

Addressed through:

- Calibration studies
- Architectural refinement records
- Validation experiments
- Retrieval investigations
- Context-engineering evaluations

## RQ2 – Contextual Vulnerability Reasoning

To what extent can the proposed framework identify vulnerabilities that depend on contextual interpretation, authorization behavior, workflow semantics, operational assumptions, or business logic?

Addressed through:

- Experiment 1
- Context-dependent vulnerability scenarios
- Safe versus vulnerable classification evaluation

## RQ3 – Comparative Detection Performance

How does the proposed framework compare with traditional static-analysis tools and prior secure-code-agent methodologies across diverse vulnerability categories?

Addressed through:

- Experiment 2
- Tool comparison studies
- Cross-method evaluation

## RQ4 – End-to-End Workflow Integration

How does integrating the proposed framework into an AI-assisted secure-code-generation workflow influence vulnerability detection, remediation quality, and overall security outcomes?

Addressed through:

- Experiment 3
- Workflow integration evaluation
- Security outcome analysis

---

# Experimental Overview

The project consists of three major experimental studies.

Calibration  
↓  
Experiment 1  
↓  
Experiment 2  
↓  
Experiment 3

The experiments are intentionally sequential.

Calibration activities establish architectural justification before expanded evaluation.

Experiment 1 evaluates vulnerability-analysis capability.

Experiment 2 compares performance against alternative approaches.

Experiment 3 investigates integration within broader AI-assisted software-development workflows.

Together, these studies provide a comprehensive evaluation of the framework.

---

# Selected LLM Configuration and Calibration Scope

The framework adopts a task-specialized large language model configuration as a deliberate architectural design choice.

The objective of the project is not to compare large language models or establish model rankings. Instead, the project investigates how contextual grounding, retrieval augmentation, validation mechanisms, remediation generation, and workflow orchestration influence vulnerability-analysis performance.

The selected configuration assigns different workflow responsibilities to models chosen for their respective strengths.

## Detection Model

Claude Opus

Responsibilities include:

- Vulnerability identification
- Contextual security reasoning
- Vulnerability classification
- Security explanation generation
- Structured vulnerability reporting

## Repair Model

Claude Sonnet

Responsibilities include:

- Secure code remediation
- Vulnerability-fix generation
- Secure implementation recommendations
- Refactored code generation
- Repair explanation generation

## Validation Methodology

The framework does not use a separate validation model.

Instead, the vulnerability detector is executed repeatedly and the resulting outputs are aggregated using threshold-based majority voting.

Current validation configuration:

- Detector executions: 10
- Validation threshold: 0.50
- Aggregation method: majority voting

The validation stage aggregates:

- Vulnerable votes
- Safe votes
- Uncertain votes
- Confidence values

and produces:

- Final decision
- Average confidence
- Consistency score
- Vote distribution statistics

The purpose of calibration is therefore not to determine which language model performs best.

Instead, calibration investigates how the selected configuration behaves within the broader orchestration workflow.

Calibration activities focus on:

- Detection consistency
- Contextual reasoning quality
- Retrieval effectiveness
- Confidence behavior
- Validation stability
- Explanation quality
- Remediation quality
- Workflow reliability

The language models are evaluated as components within the framework rather than as standalone research subjects.

The primary contribution of the project is the orchestration workflow itself, including contextual grounding, retrieval integration, validation mechanisms, remediation generation, and structured reporting.

---

# Dataset Methodology

## Dataset Foundation

The experimental dataset is derived from SecurityEval methodology and expanded to support contextual vulnerability analysis.

The dataset includes:

- Vulnerable implementations
- Secure implementations
- Ground-truth vulnerability labels
- Contextual security descriptions
- Expanded CWE coverage

The objective is to evaluate vulnerability reasoning under conditions that more closely resemble realistic software-development scenarios.

## Vulnerability Categories

The dataset is designed to include multiple classes of vulnerabilities, including:

- Input-validation weaknesses
- Authentication vulnerabilities
- Authorization vulnerabilities
- Access-control weaknesses
- Injection vulnerabilities
- Configuration weaknesses
- Dependency-related risks
- Workflow-oriented security failures
- Context-dependent business-logic vulnerabilities

Coverage may expand throughout the project as additional evaluation scenarios are introduced.

## Ground Truth

Each evaluation sample is associated with:

- Vulnerability status
- Relevant CWE mappings
- Security context profile
- Expected security interpretation

Ground-truth information provides the basis for quantitative evaluation and comparison.

---

# Evaluation Metrics

Multiple evaluation metrics are used to assess framework behavior.

## Classification Accuracy

Measures the percentage of correctly classified samples.

Used primarily during:

- Experiment 1
- Experiment 2

## False Positive Rate

Measures the frequency of incorrectly identifying vulnerabilities in secure code.

Used to evaluate over-detection behavior.

## False Negative Rate

Measures the frequency of missed vulnerabilities.

Used to evaluate vulnerability coverage.

## Confidence Consistency

Measures stability across repeated validation runs.

Supports evaluation of reliability and output consistency.

## Retrieval Relevance

Evaluates the usefulness and appropriateness of retrieved security knowledge.

Supports investigation of retrieval quality and contextual grounding.

## Explanation Quality

Evaluates the clarity, completeness, and usefulness of vulnerability explanations.

Supports explainability assessment.

## Remediation Quality

Evaluates the usefulness, correctness, and security relevance of generated fix recommendations.

Supports assessment of repair-oriented functionality.

## Latency

Measures execution time required to complete analysis workflows.

Supports investigation of practical trade-offs between quality and computational cost.

---

# Experiment 1 – Contextual Vulnerability Evaluation

## Objective

Evaluate the framework's ability to classify secure and vulnerable implementations across multiple vulnerability categories.

Particular emphasis is placed on vulnerabilities requiring contextual interpretation.

## Research Question

RQ2 – Contextual Vulnerability Reasoning

## Procedure

For each evaluation sample:

1. Provide source code and associated security context.
2. Execute framework analysis.
3. Record classification outcomes.
4. Record confidence values.
5. Record retrieved security knowledge.
6. Record generated explanations.
7. Record remediation outputs.
8. Compare results against ground truth.

## Metrics

- Accuracy
- False positives
- False negatives
- Confidence consistency
- Retrieval relevance
- Explanation quality
- Remediation quality
- Latency

---

# Experiment 2 – Comparative Evaluation

## Objective

Compare the framework against established security-analysis approaches.

Comparison systems include:

- Bandit
- CodeQL
- Prior secure-code-agent methodologies
- Proposed framework

## Research Question

RQ3 – Comparative Detection Performance

## Procedure

1. Execute all tools on equivalent evaluation samples.
2. Collect vulnerability classifications.
3. Record CWE coverage.
4. Compare detections against ground truth.
5. Analyze strengths and limitations of each approach.
6. Evaluate contextual reasoning capability where applicable.

## Metrics

- Accuracy
- False positives
- False negatives
- Vulnerability coverage
- CWE detection distribution
- Explanation quality
- Remediation quality (where available)

---

# Experiment 3 – End-to-End Workflow Integration

## Objective

Evaluate the framework as a security-analysis and remediation component within an AI-assisted secure-code-generation workflow.

The experiment investigates how security outcomes change when the framework participates in a larger software-development process.

## Research Question

RQ4 – End-to-End Workflow Integration

## Procedure

1. Generate software artifacts using an LLM-based coding workflow.
2. Analyze generated code using the framework.
3. Generate remediation recommendations.
4. Apply fixes where appropriate.
5. Re-evaluate resulting code.
6. Compare security outcomes across workflow stages.

## Metrics

- Vulnerability detection rate
- Vulnerability reduction rate
- Remediation quality
- Security outcome improvement
- Workflow consistency
- Explanation quality

---

# Reproducibility Procedures

To support transparency and reproducibility, the repository maintains documentation for:

- Dataset generation methodology
- Security context generation methodology
- Calibration procedures
- Tool versions
- Software versions
- Experimental configurations
- Evaluation metrics
- Architectural decisions

Experimental records are preserved throughout the repository whenever possible.

---

# Fairness Considerations

Several measures are taken to promote fair evaluation.

These include:

- Consistent datasets across tools
- Shared evaluation criteria
- Ground-truth verification
- Transparent metric definitions
- Documentation of limitations
- Reporting of both strengths and weaknesses

The goal is to understand relative behavior rather than demonstrate universal superiority.

---

# Threats to Validity

Several limitations may influence experimental outcomes.

Potential threats include:

- Dataset construction bias
- Ground-truth interpretation challenges
- LLM output variability
- Retrieval-quality limitations
- Prompt sensitivity
- Tool-version differences
- Coverage limitations of benchmark datasets

These factors are documented and discussed whenever relevant.

---

# Relationship to Repository Documentation

This methodology is supported by additional repository documentation:

- Calibration studies → calibration/
- Dataset information → datasets/
- Experimental execution records → experiments/
- Results and visualizations → results/
- References and supporting literature → references/
- Research reports and presentations → reports/

Together, these materials provide a complete record of the project's evaluation process.

---

# Summary

The experimental methodology is designed to systematically evaluate contextual vulnerability reasoning, comparative detection performance, architectural evolution, and end-to-end workflow integration.

By combining structured datasets, multiple evaluation metrics, comparative analysis, calibration-driven refinement, reproducibility-focused documentation, task-specialized model utilization, and validation-oriented evaluation, the methodology provides a rigorous framework for investigating the effectiveness of orchestration-oriented vulnerability analysis in AI-generated software.
