Calibration Methodology
Overview

This directory documents the calibration activities conducted throughout the development of the AI-Assisted Vulnerability Detection in LLM-Generated Code framework.

The purpose of calibration is to systematically evaluate and refine architectural components before large-scale experimental evaluation. Rather than treating architectural decisions as fixed assumptions, the project adopts an iterative evidence-driven process in which observations, hypotheses, adjustments, and evaluation outcomes guide architectural evolution.

Calibration serves two primary purposes:

Improve the effectiveness, consistency, and explainability of vulnerability analysis.
Provide empirical justification for architectural decisions investigated throughout the project.

The calibration process directly supports RQ1 – Architectural Calibration and Evolution, which investigates how orchestration-oriented components contribute to the effectiveness of LLM-based vulnerability analysis.

Calibration Philosophy

The framework is based on the principle that vulnerability-analysis performance depends not only on model capability, but also on the quality of contextual information, retrieval mechanisms, validation strategies, workflow design, and architectural coordination.

As a result, architectural components are continuously evaluated and refined prior to expanded experimentation.

Calibration therefore focuses on understanding:

Which architectural components contribute meaningful value
Which configurations improve reliability
Which design choices reduce instability
Which modifications improve contextual reasoning
Which adjustments improve explainability and remediation quality

The objective is not to optimize for a single benchmark result, but rather to improve the overall robustness and transparency of the framework.

Calibration Process

All calibration activities follow the same evidence-driven methodology:

Observation
↓
Hypothesis
↓
Adjustment
↓
Evaluation
↓
Decision
Observation

A limitation, inconsistency, weakness, or opportunity for improvement is identified.

Examples include:

Incorrect vulnerability classifications
Irrelevant retrieval results
Excessive false positives
Inconsistent reasoning
Weak remediation suggestions
Context interpretation failures
Hypothesis

A possible explanation for the observed behavior is proposed.

Examples include:

Missing contextual information
Insufficient retrieval quality
Prompt ambiguity
Validation instability
Incomplete security knowledge
Adjustment

A targeted architectural or configuration modification is introduced.

Examples include:

Context engineering changes
Retrieval strategy modifications
Validation adjustments
Prompt refinements
Model configuration updates
Evaluation

The modified configuration is tested and compared against previous behavior.

Evaluation may include:

Accuracy measurements
Consistency analysis
Retrieval relevance
Explanation quality
Remediation quality
Latency observations
Decision

The results are reviewed and documented.

Potential outcomes include:

Adopt modification
Reject modification
Require additional investigation
Integrate into future experiments
Calibration Categories

Calibration activities are organized into several architectural categories.

Context Engineering Calibration

Directory:

calibration/context/

Purpose:

Evaluate how contextual information influences vulnerability detection, reasoning quality, remediation generation, and explainability.

Examples:

Code-only analysis
Code plus security context
Expanded authorization context
Workflow-oriented context descriptions
Operational security assumptions

Questions investigated:

How much context is necessary?
Which contextual attributes are most valuable?
Does additional context reduce false positives?
Does context improve vulnerability reasoning?
Retrieval Calibration

Directory:

calibration/rag/

Purpose:

Evaluate how external security knowledge contributes to vulnerability analysis.

Areas of investigation include:

CWE retrieval
CVE retrieval
Hybrid retrieval strategies
Retrieval ranking
Context-aware retrieval
Knowledge relevance

Questions investigated:

Does retrieval improve reasoning quality?
Which retrieval strategies provide the most relevant information?
How does retrieval influence explainability?
How does retrieval affect vulnerability coverage?
Validation Calibration

Directory:

calibration/validation/

Purpose:

Investigate strategies for reducing instability associated with probabilistic model outputs.

Areas of investigation include:

Repeated evaluations
Aggregation strategies
Confidence estimation
Consistency measurements

Questions investigated:

How many validation runs are appropriate?
Does aggregation improve stability?
How does validation influence reliability?
What trade-offs exist between consistency and execution cost?
Prompt Calibration

Directory:

calibration/prompts/

Purpose:

Evaluate how prompt design influences vulnerability detection behavior and explanation quality.

Areas of investigation include:

Output structure
Vulnerability reasoning
Explanation formatting
Remediation guidance
Context integration

Questions investigated:

Which prompt structures improve consistency?
Which prompts improve explainability?
How sensitive are results to prompt modifications?
Model Configuration Calibration

Directory:

calibration/llm_selection/

Purpose:

Investigate how model selection and configuration influence analysis outcomes.

Areas of investigation include:

Model comparisons
Configuration comparisons
Multi-model workflows
Performance trade-offs

Questions investigated:

How do different models perform on vulnerability analysis tasks?
What trade-offs exist between quality, latency, and consistency?
Which configurations best support the architectural goals of the framework?
Relationship to Experimental Evaluation

Calibration is conducted prior to expanded experimentation.

The purpose of calibration is not to generate final research conclusions, but rather to improve the quality and justification of the architectural configuration used during formal evaluation.

Insights obtained through calibration inform:

Experimental design
Dataset construction
Retrieval configuration
Validation strategy
Model selection
Reporting methodology

As a result, calibration serves as the foundation for all subsequent experiments.

Documentation Standards

Each calibration record should include:

Calibration Identifier

Unique identifier for traceability.

Example:

CAL-RAG-001
Objective

What is being investigated?

Observation

What motivated the calibration?

Hypothesis

What explanation is being tested?

Adjustment

What change was introduced?

Evaluation Method

How was the adjustment evaluated?

Results

What outcomes were observed?

Decision

What conclusions were reached?

Impact on Architecture

How did the calibration influence architectural evolution?

Connection to Research Question 1

The calibration activities documented in this directory collectively support:

RQ1 – Architectural Calibration and Evolution

How do orchestration-oriented architectural components—including contextual grounding, retrieval augmentation, prompt engineering, and validation strategies—evolve through calibration, and how do they contribute to the effectiveness of LLM-based vulnerability analysis?

The results of these calibration studies provide empirical evidence supporting architectural decisions and establish the foundation for the formal experimental evaluation documented elsewhere in the repository.

Summary

Calibration is treated as a first-class component of the research methodology.

Rather than assuming architectural decisions are correct from the outset, the project adopts a systematic process of observation, hypothesis formation, adjustment, evaluation, and decision-making.

This approach enables architectural evolution to be documented, justified, and connected directly to the research objectives guiding the project.
