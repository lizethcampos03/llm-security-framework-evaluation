Experimental Evaluation

Overview

This directory contains the experimental studies conducted throughout the development and evaluation of the AI-Assisted Vulnerability Detection in LLM-Generated Code framework.

The experiments investigate the effectiveness of contextual grounding, retrieval-augmented security knowledge, validation strategies, remediation generation, and workflow orchestration for vulnerability analysis of AI-generated software.

The experimental phase is organized around the four research questions guiding the project and serves as the primary mechanism for evaluating architectural decisions documented elsewhere in the repository.

Additional details regarding evaluation procedures, datasets, metrics, and reproducibility can be found in:

docs/experimental_methodology.md
Experimental Philosophy

The experiments are designed to support evidence-based evaluation rather than demonstration-oriented testing.

The goal is not to prove universal superiority over existing approaches. Instead, the objective is to understand:

Where orchestration-oriented vulnerability analysis provides value
Which architectural components contribute meaningfully to performance
Which vulnerability categories benefit from contextual reasoning
How the framework compares with alternative approaches
How the framework behaves within larger software-development workflows

Each experiment is designed to answer a specific research question while contributing to the overall evaluation of the framework.

Relationship Between Experiments

The experiments are intentionally structured as a progressive evaluation sequence.

Calibration
↓
Experiment 1
↓
Experiment 2
↓
Experiment 3
Calibration

Architectural components are refined and evaluated through systematic calibration before formal experimentation.

The calibration phase investigates:

Context engineering
Retrieval strategies
Prompt refinement
Validation methodologies
Model configurations

Calibration documentation can be found in:

calibration/
Experiment 1

Establishes baseline vulnerability-analysis capability.

Focus:

Secure vs vulnerable classification
Context-dependent vulnerabilities
Retrieval effectiveness
Explanation quality
Remediation quality

Addresses:

RQ2 – Contextual Vulnerability Reasoning
Experiment 2

Compares the framework against established security-analysis approaches.

Focus:

Detection effectiveness
Vulnerability coverage
Strengths and limitations of alternative approaches
Contextual reasoning capability

Addresses:

RQ3 – Comparative Detection Performance
Experiment 3

Evaluates the framework within a broader AI-assisted software-development workflow.

Focus:

Workflow-level security analysis
Remediation effectiveness
Security outcome improvement
Integration behavior

Addresses:

RQ4 – End-to-End Workflow Integration
Experiment Directory Structure

The experiments are organized as follows:

experiments/

├── README.md
│
├── experiment1_securityeval/
│
├── experiment2_tool_comparison/
│
└── experiment3_end_to_end/

Each experiment directory contains documentation describing:

Objectives
Methodology
Evaluation procedures
Metrics
Results
Observations
Limitations
Conclusions
Experiment 1 – Contextual Vulnerability Evaluation
Purpose

Evaluate the framework's ability to identify vulnerabilities across a SecurityEval-derived dataset spanning multiple vulnerability categories and contextual scenarios.

Particular emphasis is placed on vulnerabilities requiring contextual interpretation beyond recognizable syntax-level patterns.

Examples include:

Authorization weaknesses
Access-control failures
Workflow-level vulnerabilities
Operational security assumptions
Context-dependent business-logic weaknesses
Research Question

RQ2 – Contextual Vulnerability Reasoning

To what extent can the proposed framework identify vulnerabilities that depend on contextual interpretation, authorization behavior, workflow semantics, operational assumptions, or business logic?

Primary Evaluation Areas
Classification accuracy
False positives
False negatives
Confidence consistency
Retrieval relevance
Explanation quality
Remediation quality
Latency
Directory
experiment1_securityeval/
Experiment 2 – Comparative Evaluation
Purpose

Compare the proposed framework against established vulnerability-analysis approaches.

The experiment investigates how different analysis paradigms perform across diverse vulnerability categories and contextual scenarios.

Comparison systems may include:

Bandit
CodeQL
Prior secure-code-agent methodologies
Proposed framework
Research Question

RQ3 – Comparative Detection Performance

How does the proposed framework compare with traditional static-analysis tools and prior secure-code-agent methodologies across diverse vulnerability categories?

Primary Evaluation Areas
Detection accuracy
False positives
False negatives
Vulnerability coverage
CWE coverage
Contextual reasoning capability
Explanation quality
Remediation quality
Directory
experiment2_tool_comparison/
Experiment 3 – End-to-End Workflow Integration
Purpose

Evaluate the framework as a security-analysis and remediation component within an AI-assisted secure-code-generation workflow.

The objective is to investigate how vulnerability detection, explanation, validation, and remediation influence security outcomes throughout the development lifecycle.

Research Question

RQ4 – End-to-End Workflow Integration

How does integrating the proposed framework into an AI-assisted secure-code-generation workflow influence vulnerability detection, remediation quality, and overall security outcomes?

Primary Evaluation Areas
Vulnerability detection rate
Vulnerability reduction rate
Remediation quality
Workflow consistency
Explanation quality
Security outcome improvement
Directory
experiment3_end_to_end/
Experimental Results

Results generated throughout experimentation are maintained separately from experimental procedures.

Result documentation can be found in:

results/

This separation helps preserve clarity between:

Experimental design
Experimental execution
Experimental outcomes
Relationship to Research Questions

The experiments collectively address the project's research questions.

Research Question	Evaluation Source
RQ1 – Architectural Calibration and Evolution	Calibration Studies
RQ2 – Contextual Vulnerability Reasoning	Experiment 1
RQ3 – Comparative Detection Performance	Experiment 2
RQ4 – End-to-End Workflow Integration	Experiment 3

Together, these studies provide a structured evaluation of the framework's architecture, reasoning capability, comparative performance, and workflow-level effectiveness.

Future Experimental Expansion

As the project evolves, additional experiments may be introduced to investigate:

Larger real-world software systems
Expanded benchmark coverage
Multi-language vulnerability analysis
Alternative retrieval architectures
Graph-based security retrieval
Human-in-the-loop workflows
Production-development integration scenarios
Specialized security-model adaptation

Future experiments will be organized using the same documentation and evaluation standards established throughout this repository.

Summary

This directory serves as the central hub for experimental evaluation within the project.

The experiments are organized to progressively investigate contextual vulnerability reasoning, comparative performance, and workflow-level security integration while maintaining transparency, reproducibility, and alignment with the project's research questions.

Together with the calibration records, methodology documentation, datasets, and results, these experiments provide the empirical foundation for evaluating the effectiveness of orchestration-oriented vulnerability analysis in AI-generated software.
