Project Overview
Project Title

AI-Assisted Vulnerability Detection in LLM-Generated Code: A LangGraph-Orchestrated Workflow for Context-Aware Vulnerability Detection and Secure Code Fixing

Project Summary

Artificial intelligence has become an increasingly important component of modern software development. Large language models can generate functional source code, accelerate prototyping, and assist developers throughout the software engineering lifecycle. However, recent research has demonstrated that AI-generated code may contain security vulnerabilities, including weaknesses that depend on contextual interpretation, authorization behavior, workflow semantics, operational assumptions, and business logic.

Traditional static-analysis systems such as Bandit and CodeQL remain highly effective for many vulnerability categories. However, some vulnerabilities require deeper contextual reasoning regarding intended application behavior, protected resources, authorization expectations, and operational security requirements.

This project investigates whether orchestration-oriented workflows can improve vulnerability analysis of AI-generated software by combining contextual grounding, retrieval-augmented security knowledge, large language model reasoning, repeated validation, remediation generation, and structured reporting within a unified LangGraph-based framework.

The project explores how these components contribute to vulnerability detection, explainability, reliability, and integration within secure software development workflows.

Problem Statement

AI-generated code can contain security vulnerabilities that are difficult to identify using traditional vulnerability-detection approaches alone.

Many modern vulnerabilities involve:

Authorization misuse
Broken access control
Workflow-level security failures
Insecure operational assumptions
Missing security processes
Context-dependent business logic
Dependency and configuration risks

Traditional static-analysis systems excel at identifying many syntax-oriented and semantic vulnerability patterns. However, contextual vulnerabilities often require understanding intended application behavior, security expectations, protected resources, user roles, and operational constraints.

At the same time, large language models provide promising contextual reasoning capabilities but introduce challenges involving:

Hallucinations
Output variability
Prompt sensitivity
Weak reproducibility
Inconsistent explanations

This project investigates whether structured orchestration can help address some of these limitations.

Research Motivation

Recent research has shown that large language models can generate vulnerable software and may struggle to consistently identify or repair security weaknesses within generated code.

These findings raise important questions regarding the role of contextual reasoning, retrieval augmentation, validation strategies, and workflow orchestration in improving AI-assisted vulnerability analysis.

Rather than treating vulnerability detection as a single inference task, this project explores whether a coordinated multi-stage workflow can improve reliability, explainability, and contextual understanding.

The project is motivated by the belief that future advances in AI-assisted security analysis may depend not only on stronger language models, but also on better orchestration, contextual grounding, retrieval quality, validation strategies, and workflow design.

Research Questions

The project investigates four primary research questions.

RQ1 – Architectural Calibration and Evolution

How do orchestration-oriented architectural components—including contextual grounding, retrieval augmentation, prompt engineering, and validation strategies—evolve through calibration, and how do they contribute to the effectiveness of LLM-based vulnerability analysis?

RQ2 – Contextual Vulnerability Reasoning

To what extent can the proposed framework identify vulnerabilities that depend on contextual interpretation, authorization behavior, workflow semantics, operational assumptions, or business logic?

RQ3 – Comparative Detection Performance

How does the proposed framework compare with traditional static-analysis tools and prior secure-code-agent methodologies across diverse vulnerability categories?

RQ4 – End-to-End Workflow Integration

How does integrating the proposed framework into an AI-assisted secure-code-generation workflow influence vulnerability detection, remediation quality, and overall security outcomes?

High-Level Framework

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

The workflow combines source code, contextual security information, external vulnerability knowledge, vulnerability reasoning, validation mechanisms, remediation generation, and explainable reporting into a unified analysis process.

The architecture is intentionally modular and designed to support future experimentation involving retrieval refinement, model comparisons, expanded datasets, and workflow integration studies.

Current Development Phase

The project is currently focused on:

SecurityEval-derived dataset construction
Security context profile generation
Architectural calibration
Hybrid retrieval refinement
Prompt engineering improvements
Validation methodology documentation
Expanded CWE coverage
Comparative evaluation planning
End-to-end workflow integration preparation

These activities are intended to strengthen the framework before executing expanded experimental studies.

Experimental Roadmap

The project currently includes three major experimental studies.

Experiment 1 – Safe vs Vulnerable Classification

Evaluate vulnerability classification performance across a SecurityEval-derived dataset spanning broad CWE coverage.

Primary metrics include:

Accuracy
False positives
False negatives
Confidence
Retrieval quality
Latency
Remediation quality
Experiment 2 – Comparative Evaluation

Compare the proposed framework against:

Bandit
CodeQL
Prior secure-code-agent methodologies

The objective is to identify strengths, limitations, and areas where contextual reasoning provides additional value.

Experiment 3 – End-to-End Workflow Integration

Evaluate the framework within a secure code-generation workflow inspired by prior secure-code-agent research.

This experiment investigates how contextual retrieval, validation, explainability, and remediation influence overall workflow security outcomes.

Expected Contributions

This project aims to contribute:

A context-aware vulnerability-analysis framework for AI-generated software
A structured orchestration approach combining retrieval, reasoning, validation, and remediation
Insights regarding contextual vulnerability detection
Experimental evaluation across expanded CWE coverage
Comparative analysis against established security-analysis tools
Investigation of end-to-end workflow integration
Documentation of architectural calibration and evolution

The project additionally explores how orchestration-oriented design decisions influence the effectiveness, explainability, and reliability of AI-assisted vulnerability analysis.

Future Directions

Potential future research directions include:

Evaluation on larger real-world software systems
Graph-based and relationship-aware security retrieval
Code-aware retrieval techniques
Multi-language vulnerability analysis
Human-in-the-loop security review workflows
Production software-development integration
Specialized security-oriented model adaptation
Expanded contextual vulnerability benchmarks
Repository Relationship

This document provides a high-level overview of the project.

Additional details can be found throughout the repository:

Calibration documentation → calibration/
Experimental methodology → experiments/
Dataset documentation → datasets/
Results and figures → results/
References and supporting literature → references/
Research reports and presentations → reports/
