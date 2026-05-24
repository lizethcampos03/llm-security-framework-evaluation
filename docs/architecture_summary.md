Architecture Summary
Purpose

This document provides a high-level overview of the architecture used throughout the project AI-Assisted Vulnerability Detection in LLM-Generated Code: A LangGraph-Orchestrated Workflow for Context-Aware Vulnerability Detection and Secure Code Fixing.

The framework investigates how orchestration-oriented workflows can improve vulnerability analysis of AI-generated software through contextual grounding, retrieval-augmented security knowledge, large language model reasoning, validation strategies, remediation generation, and structured reporting.

The objective is not to replace traditional security-analysis tools. Rather, the framework explores whether coordinated contextual reasoning workflows can provide additional value for vulnerability categories that depend on authorization behavior, workflow semantics, operational assumptions, business logic, and other forms of contextual interpretation.

Architectural Philosophy

The architecture is based on a simple principle:

Better context, better security knowledge, better validation, and better workflow coordination can improve vulnerability-analysis reliability.

Rather than treating vulnerability detection as a single inference task, the framework organizes analysis into multiple stages that contribute different forms of information and reasoning.

The design emphasizes:

Contextual grounding
Retrieval-augmented reasoning
Explainability
Validation consistency
Modular experimentation
Workflow transparency

This philosophy guides both the current implementation and the ongoing calibration and evaluation efforts.

High-Level Workflow

The framework follows a multi-stage orchestration pipeline:

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

Each stage contributes a specific function within the overall vulnerability-analysis workflow.
Architectural Components
Input Layer

The workflow begins with source code and associated contextual security information.

In addition to the code itself, the framework supports structured contextual information describing factors such as:

Application purpose
Protected resources
User roles
Authorization requirements
Security expectations
Threat concerns
Operational assumptions
Deployment considerations

The inclusion of context is motivated by the observation that many vulnerabilities cannot be accurately interpreted through source code alone.

For example, vulnerabilities involving access control, workflow behavior, authorization misuse, insecure operational assumptions, or missing security processes often depend on understanding intended application behavior.

Preprocessing Layer

The preprocessing stage prepares incoming information for downstream analysis.

Responsibilities include:

Context normalization
Input formatting
Structured context representation
Workflow state preparation

Although preprocessing does not perform vulnerability analysis directly, it improves consistency throughout the pipeline and reduces variability in downstream reasoning stages.

Security Knowledge Retrieval Layer

The retrieval layer introduces external security knowledge into the analysis process.

The retrieval process is designed to provide contextual grounding through vulnerability-related information derived from sources such as:

Common Weakness Enumeration (CWE)
Common Vulnerabilities and Exposures (CVE)
Vulnerability descriptions
Mitigation guidance
Security terminology
Related weakness relationships

The purpose of retrieval is to support vulnerability reasoning with established security knowledge rather than relying solely on model memory.

Retrieval quality is considered one of the most important factors influencing contextual vulnerability analysis.

Vulnerability Detection Layer

The detection stage performs the primary vulnerability-analysis task.

This stage combines:

Source code
Security context
Retrieved security knowledge

to evaluate whether security weaknesses may be present.

The detector is designed to reason about:

Vulnerability indicators
Authorization behavior
Workflow intent
Business logic
Security assumptions
Operational context

The framework focuses particularly on vulnerabilities that require contextual interpretation beyond recognizable syntax-level patterns.

Validation Layer

The validation stage addresses one of the central challenges associated with large language models: output variability.

Rather than relying on a single analysis result, the framework applies repeated evaluation and aggregation strategies to improve consistency.

The validation process seeks to:

Reduce unstable classifications
Improve confidence estimation
Increase reasoning consistency
Improve trustworthiness of findings

Validation is treated as an architectural component rather than a post-processing step because it directly influences reliability.

Fix Generation Layer

When vulnerabilities are identified, the framework generates remediation guidance and secure-code recommendations.

The remediation stage uses:

Detection findings
Contextual information
Retrieved security knowledge
Mitigation guidance

to produce actionable security recommendations.

In addition to suggesting fixes, this stage contributes to explainability by connecting identified vulnerabilities with appropriate remediation strategies.

Reporting Layer

The final stage generates structured vulnerability-analysis outputs.

Reports may include:

Classification outcomes
Vulnerability mappings
Confidence indicators
Supporting reasoning
Retrieved evidence
Remediation guidance

The reporting stage supports explainability, evaluation, auditing, and comparison with alternative analysis approaches.

Architectural Principles

The framework is guided by several core architectural principles.

Contextual Grounding

Security analysis should consider the operational context surrounding software behavior rather than relying exclusively on source code patterns.

Retrieval-Augmented Reasoning

External security knowledge can improve vulnerability interpretation and strengthen contextual understanding.

Validation-Oriented Analysis

Repeated evaluation and aggregation can improve stability and reduce probabilistic variability.

Explainability

Security findings should be accompanied by reasoning, evidence, and remediation guidance whenever possible.

Modularity

Architectural components should remain separable and independently improvable.

This allows retrieval, validation, prompting, remediation, and contextual-engineering strategies to evolve through experimentation.

Current Architectural Investigation Areas

Several architectural areas are currently being investigated through calibration and experimentation.

These include:

Security context engineering
Structured context representation
Hybrid retrieval strategies
Retrieval reranking approaches
Prompt refinement
Validation methodology optimization
Model allocation strategies
Expanded CWE coverage
SecurityEval-based evaluation
End-to-end workflow integration

These investigations are intended to strengthen contextual reasoning, retrieval quality, explainability, and evaluation rigor.

Architectural Scope

The framework should be viewed as an orchestration-oriented research platform rather than a production-ready security product.

The primary purpose of the architecture is to investigate how contextual grounding, retrieval augmentation, validation strategies, and workflow orchestration influence vulnerability-analysis performance and reliability.

The architecture is therefore designed to support experimentation, evaluation, refinement, and comparative analysis across multiple security-analysis scenarios.

Relationship to the Research Questions

The architecture directly supports the four research questions guiding the project.

RQ1 – Architectural Calibration and Evolution

Investigates how architectural components evolve through calibration and refinement.

RQ2 – Contextual Vulnerability Reasoning

Evaluates the framework's ability to reason about context-dependent vulnerabilities.

RQ3 – Comparative Detection Performance

Supports comparison against traditional static-analysis tools and prior methodologies.

RQ4 – End-to-End Workflow Integration

Examines the role of the framework within broader AI-assisted secure-development workflows.

Summary

The proposed framework combines contextual security information, retrieval-augmented security knowledge, vulnerability reasoning, validation strategies, remediation generation, and structured reporting within a unified orchestration workflow.

The architecture is designed to support systematic experimentation into how workflow coordination, contextual grounding, retrieval quality, and validation mechanisms influence the effectiveness, explainability, and reliability of AI-assisted vulnerability analysis.
