AI-Assisted Vulnerability Detection in LLM-Generated Code

Overview

This repository serves as the public research archive for the project:

AI-Assisted Vulnerability Detection in LLM-Generated Code: A LangGraph-Orchestrated Workflow for Context-Aware Vulnerability Detection and Secure Code Fixing

The project investigates how orchestration-oriented workflows combining contextual grounding, retrieval-augmented security knowledge, large language model reasoning, validation strategies, and remediation generation can support more reliable vulnerability analysis of AI-generated software.

The repository documents the calibration process, experimental methodology, datasets, evaluation results, architectural evolution, and supporting materials associated with the project.

Motivation

Artificial intelligence has rapidly become an important component of modern software development. Large language models can generate functional source code, accelerate prototyping, and assist developers throughout the software engineering lifecycle.

However, recent research has shown that AI-generated code may contain security vulnerabilities, including weaknesses that depend on contextual interpretation, authorization behavior, workflow semantics, operational assumptions, and business logic. Traditional static-analysis tools remain highly effective for many vulnerability categories, but certain security problems require deeper contextual reasoning.

This project explores whether a structured orchestration framework can improve vulnerability detection, explanation quality, remediation guidance, and workflow-level security analysis by combining retrieval-augmented security knowledge with contextual LLM reasoning and validation-oriented workflows.

Research Questions

The project investigates four primary research questions.

RQ1 – Architectural Calibration and Evolution

How do orchestration-oriented architectural components—including contextual grounding, retrieval augmentation, prompt engineering, and validation strategies—evolve through calibration, and how do they contribute to the effectiveness of LLM-based vulnerability analysis?

This question motivates the calibration phase and investigates how architectural refinements influence vulnerability-analysis performance, explainability, and reliability.

RQ2 – Contextual Vulnerability Reasoning

To what extent can the proposed framework identify vulnerabilities that depend on contextual interpretation, authorization behavior, workflow semantics, operational assumptions, or business logic?

This question evaluates the framework's ability to reason about vulnerabilities that extend beyond recognizable syntax-level patterns.

RQ3 – Comparative Detection Performance

How does the proposed framework compare with traditional static-analysis tools and prior secure-code-agent methodologies across diverse vulnerability categories?

This question investigates the relative strengths and limitations of orchestration-based vulnerability analysis compared with established approaches.

RQ4 – End-to-End Workflow Integration

How does integrating the proposed framework into an AI-assisted secure-code-generation workflow influence vulnerability detection, remediation quality, and overall security outcomes?

This question examines the role of the framework within broader secure-development workflows and end-to-end code-generation pipelines.

High-Level Framework Overview

The proposed framework follows a multi-stage orchestration workflow:

Input
↓
Preprocessing
↓
Security Knowledge Retrieval
↓
LLM Vulnerability Detection
↓
Validation
↓
Fix Generation
↓
Structured Reporting

The workflow combines source code, contextual security information, external vulnerability knowledge, vulnerability reasoning, validation mechanisms, remediation generation, and explainable reporting into a unified analysis pipeline.

This repository provides high-level architectural descriptions, experimental methodology, calibration documentation, and evaluation results associated with the project.

Repository Objectives

This repository is intended to:

Document architectural evolution and calibration activities
Provide experimental methodology and evaluation procedures
Maintain dataset documentation and generation protocols
Archive experimental results and supporting visualizations
Record design decisions and project milestones
Support reproducibility and transparency
Serve as a companion resource to the research report

The repository functions as the public documentation and evaluation archive supporting the project.

Calibration Strategy

Prior to expanded experimentation, the framework undergoes a structured calibration phase focused on improving:

Security context engineering
Retrieval quality
Contextual grounding
Prompt design
Validation consistency
Explanation quality

The calibration methodology follows an evidence-driven process:

Observation
↓
Hypothesis
↓
Adjustment
↓
Evaluation
↓
Decision

Calibration documentation is maintained throughout the repository and serves as the foundation for subsequent experimental evaluation.

Experimental Roadmap

The project currently consists of three major experimental studies.

Experiment 1 – Safe vs Vulnerable Classification

Evaluate the framework's ability to classify secure and vulnerable implementations across a SecurityEval-derived dataset spanning multiple CWE categories.

Primary evaluation metrics include:

Classification accuracy
False positives
False negatives
Confidence
Retrieval quality
Latency
Fix quality
Experiment 2 – Comparative Evaluation

Compare the proposed framework against:

Bandit
CodeQL
Published secure-code-agent methodologies

The goal is to investigate how different analysis paradigms behave across syntax-oriented, semantic, contextual, authorization-related, and workflow-oriented vulnerability categories.

Experiment 3 – End-to-End Workflow Integration

Evaluate the framework as a security-analysis and remediation component within an AI-assisted secure-code-generation workflow inspired by prior secure-code-agent research.

The experiment investigates how contextual retrieval, validation, explanation, and remediation contribute to overall workflow security outcomes.

Dataset

The experimental dataset is derived from SecurityEval methodology and expanded to support:

Vulnerable implementations
Secure implementations
Ground-truth vulnerability labels
Security context profiles
Expanded CWE coverage

The dataset is designed to support reproducibility, broad vulnerability coverage, contextual evaluation, and comparison across multiple analysis approaches.

Dataset documentation is available throughout the repository.

Current Development Focus

Current development activities include:

SecurityEval-derived dataset creation
Security context profile generation
Calibration execution
Hybrid retrieval refinement
Validation methodology documentation
Model configuration evaluation
Expanded CWE coverage
Experimental execution
Comparative evaluation
End-to-end workflow integration
Future Directions

Future research directions include:

Evaluation on larger real-world software systems
Expanded code-aware retrieval techniques
Relationship-aware and graph-based security retrieval
Multi-language vulnerability analysis
Adaptive context engineering
Human-in-the-loop security review workflows
Production development pipeline integration
Specialized security-oriented model adaptation
Reproducibility

The repository documents:

Dataset generation methodology
Calibration procedures
Experimental protocols
Evaluation metrics
Tool configurations
Software versions
Design decisions

The objective is to support transparency, reproducibility, and long-term project evolution.

Repository Structure
docs/
calibration/
experiments/
results/
datasets/
reports/
references/
appendix/
archive/

Each directory contains documentation describing its purpose and relationship to the overall research workflow.

References

Project references, supporting literature, benchmark sources, and related research materials are maintained in the references/ directory.

Key references include literature on:

AI-generated code security
Secure code agents
Retrieval-augmented generation
Common Weakness Enumeration (CWE)
Common Vulnerabilities and Exposures (CVE)
LangGraph orchestration workflows
Static-analysis systems
Disclaimer

This repository documents an active research effort. Methodology, datasets, calibration findings, experimental results, and architectural decisions may evolve as additional evaluation and refinement are completed.
