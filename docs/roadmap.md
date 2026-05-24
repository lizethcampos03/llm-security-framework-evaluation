Project Roadmap

Purpose

This document outlines the planned evolution of the AI-Assisted Vulnerability Detection in LLM-Generated Code project.

The roadmap serves as a planning and organizational resource that documents major development phases, research objectives, experimental milestones, and long-term investigation areas.

The purpose of the roadmap is not to guarantee specific outcomes or timelines, but rather to provide a structured view of the project's intended direction and research priorities.

As new findings emerge through calibration and experimentation, roadmap items may be refined, expanded, reprioritized, or replaced.

Project Vision

The project investigates how orchestration-oriented workflows combining contextual grounding, retrieval-augmented security knowledge, vulnerability reasoning, validation strategies, remediation generation, and structured reporting can contribute to more effective AI-assisted vulnerability analysis.

The long-term objective is to better understand how contextual reasoning workflows can support vulnerability detection, explainability, remediation, and secure software-development practices.

The project emphasizes:

Evidence-based evaluation
Architectural transparency
Reproducibility
Comparative analysis
Continuous refinement through experimentation
Current Phase
Phase 1 – Research Foundation and Repository Development
Objectives

Establish the documentation, methodology, organizational structure, and evaluation framework supporting the project.

Major Deliverables
Public research repository
Project overview documentation
Architecture documentation
Calibration methodology
Experimental methodology
Reproducibility documentation
Decision-tracking procedures
Reference management
Status

In Progress / Near Completion

Phase 2 – Calibration and Architectural Refinement
Objectives

Systematically investigate architectural design choices and improve framework reliability before expanded experimentation.

Investigation Areas
Context Engineering

Evaluate how contextual information influences:

Vulnerability reasoning
Explanation quality
Remediation generation
Classification accuracy
Retrieval Strategies

Evaluate:

CWE retrieval
CVE retrieval
Hybrid retrieval approaches
Retrieval ranking
Context-aware retrieval
Validation Strategies

Investigate:

Repeated evaluations
Aggregation approaches
Confidence estimation
Consistency measurements
Prompt Refinement

Investigate:

Structured outputs
Explanation quality
Remediation quality
Reasoning consistency
Model Configuration Evaluation

Investigate:

Model comparisons
Performance trade-offs
Multi-model workflows
Configuration strategies
Deliverables
Calibration records
Architectural refinements
Decision documentation
Updated evaluation configuration
Status

Planned

Phase 3 – Dataset Development
Objectives

Construct and document a reproducible evaluation dataset derived from SecurityEval methodology.

Deliverables
Vulnerable implementations
Secure implementations
Ground-truth labels
Security context profiles
Expanded CWE coverage
Dataset documentation
Status

Planned

Phase 4 – Experiment 1
Contextual Vulnerability Evaluation
Research Question

RQ2 – Contextual Vulnerability Reasoning

Objectives

Evaluate the framework's ability to identify vulnerabilities that depend on:

Authorization behavior
Workflow semantics
Operational assumptions
Business logic
Contextual interpretation
Deliverables
Evaluation results
Classification metrics
Retrieval analysis
Explanation analysis
Remediation analysis
Status

Planned

Phase 5 – Experiment 2
Comparative Evaluation
Research Question

RQ3 – Comparative Detection Performance

Objectives

Compare the framework against:

Bandit
CodeQL
Prior secure-code-agent methodologies
Deliverables
Comparative results
Vulnerability coverage analysis
Strengths and limitations assessment
Cross-method evaluation
Status

Planned

Phase 6 – Experiment 3
End-to-End Workflow Integration
Research Question

RQ4 – End-to-End Workflow Integration

Objectives

Evaluate the framework as a component within a broader AI-assisted secure-code-generation workflow.

Investigation Areas
Vulnerability detection
Remediation effectiveness
Workflow consistency
Security outcome improvement
Explainability
Deliverables
Workflow evaluation results
Security outcome analysis
Integration observations
Comparative findings
Status

Planned

Phase 7 – Research Report Revision
Objectives

Incorporate calibration findings and experimental results into the research report.

Activities
Methodology updates
Results integration
Figure creation
Table refinement
Reference expansion
Discussion updates
Future work revision
Deliverables
Updated report
Revised figures
Expanded analysis
Status

Future

Phase 8 – Presentation and Dissemination
Objectives

Communicate findings to faculty, researchers, students, and potential collaborators.

Deliverables
Research presentation
Poster updates
Repository updates
Supporting documentation
Status

Future

Long-Term Research Directions

The following areas extend beyond the scope of the current experimental plan but may be investigated in future versions of the project.

Real-World Software Evaluation

Move beyond isolated benchmark samples and evaluate larger software systems with interacting components.

Graph-Based Security Retrieval

Investigate relationship-aware retrieval using vulnerability relationships, dependency structures, and knowledge graphs.

Advanced Context Engineering

Explore automated generation and refinement of security context profiles.

Multi-Language Vulnerability Analysis

Expand evaluation beyond a single programming language.

Human-in-the-Loop Security Review

Investigate collaborative workflows combining automated reasoning and human expertise.

Production Workflow Integration

Evaluate integration within practical software-development environments.

Security-Specialized Model Adaptation

Explore model adaptation and security-focused optimization strategies.

Guiding Principles

Throughout all phases of development, the project follows several principles.

Evidence Before Claims

Architectural decisions should be supported by calibration or experimentation whenever possible.

Reproducibility

Methodology and evaluation procedures should remain transparent and documented.

Fair Comparison

Comparative evaluations should emphasize understanding strengths and limitations rather than demonstrating universal superiority.

Continuous Refinement

Architectural evolution should be guided by observations, experimentation, and documented reasoning.

Honest Reporting

Limitations, assumptions, and uncertainties should be acknowledged and discussed openly.

Summary

This roadmap outlines the planned progression of the project from architectural calibration and dataset construction through experimental evaluation, report refinement, and future research exploration.

The roadmap is intended to provide structure, maintain focus on research objectives, and support the continued evolution of the project through systematic investigation, documentation, and evidence-based evaluation.
