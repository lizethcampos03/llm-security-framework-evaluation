Decision Log

Purpose

This document records significant architectural, methodological, experimental, and project-level decisions made throughout the development of the AI-Assisted Vulnerability Detection in LLM-Generated Code framework.

The purpose of the decision log is to preserve the reasoning behind important choices, improve transparency, support reproducibility, and provide historical context for future project evolution.

Rather than documenting only final outcomes, the project records the rationale, alternatives, evidence, and conclusions that contributed to major decisions.

This document complements the calibration records, experimental documentation, and project roadmap by explaining why specific directions were adopted.

Decision-Making Philosophy

The project follows an evidence-driven approach to decision making.

Whenever possible, significant decisions are based on:

Calibration findings
Experimental observations
Prior research
Benchmark requirements
Reproducibility considerations
Engineering practicality

The objective is not to optimize for novelty alone, but rather to pursue decisions that improve methodological rigor, transparency, explainability, and evaluation quality.

Decision Categories

Decisions generally fall into one or more of the following categories.

Architecture Decisions

Examples:

Workflow design
Component selection
Retrieval architecture
Validation strategy
Reporting structure
Context-engineering approach
Calibration Decisions

Examples:

Retrieval modifications
Prompt adjustments
Validation refinements
Model-selection choices
Context-profile design
Dataset Decisions

Examples:

Benchmark selection
Dataset expansion
Ground-truth methodology
Vulnerability-category coverage
Context-generation procedures
Experimental Decisions

Examples:

Experiment design
Evaluation metrics
Comparison methodology
Baseline selection
Statistical procedures
Documentation Decisions

Examples:

Repository organization
Reporting structure
Versioning practices
Reproducibility standards
Decision Record Format

Every decision should follow a consistent structure.

Decision Identifier

Unique identifier for traceability.

Example:

DEC-001
Date

Date the decision was finalized.

Example:

2026-06-01
Category

Examples:

Architecture
Calibration
Dataset
Experiment
Documentation
Decision Statement

Brief summary of the decision.

Example:

Adopt SecurityEval-derived evaluation methodology as the primary benchmark foundation.

Context

What problem or question motivated the decision?

Example:

A reproducible benchmark was required to support fair comparison with existing research and improve methodological rigor.

Alternatives Considered

Document other options that were evaluated.

Example:

Custom dataset generation
Existing benchmark reuse without modification
SecurityEval-derived methodology
Evidence

Summarize observations, calibration results, literature, or evaluation findings that informed the decision.

Where applicable, reference:

Calibration records
Experiments
Reports
Research papers
Decision

Describe the final outcome.

Example:

The project adopts a SecurityEval-derived methodology with contextual extensions and expanded CWE coverage.

Expected Impact

Describe the anticipated benefits.

Examples:

Improved reproducibility
Broader benchmark coverage
Better comparison quality
Increased evaluation rigor
Follow-Up Actions

Document any future work resulting from the decision.

Examples:

Generate contextual security profiles
Expand benchmark coverage
Update experiment documentation
Example Decision Record
DEC-001
Date

2026-06-01

Category

Dataset

Decision Statement

Adopt a SecurityEval-derived methodology as the primary dataset foundation.

Context

The project required a reproducible and research-aligned benchmark capable of supporting comparison with existing vulnerability-analysis approaches.

Alternatives Considered
Fully custom dataset
Existing benchmark without modification
SecurityEval-derived methodology
Evidence

SecurityEval provides established vulnerability categories, reproducible generation procedures, and compatibility with prior research.

Decision

A SecurityEval-derived dataset with contextual extensions will serve as the foundation for experimental evaluation.

Expected Impact
Improved reproducibility
Stronger comparison capability
Better alignment with existing literature
Follow-Up Actions
Generate contextual security profiles
Expand CWE coverage
Document dataset-generation procedures
Relationship to Calibration

Many decisions originate from calibration activities.

Examples include:

Retrieval modifications
Prompt refinements
Validation adjustments
Model-selection choices

Where applicable, decisions should reference supporting calibration records.

This creates traceability between:

Observation
↓
Hypothesis
↓
Adjustment
↓
Evaluation
↓
Decision

and the resulting architectural evolution.

Relationship to Experiments

Experimental outcomes may motivate new decisions.

Examples include:

Metric revisions
Dataset expansion
Baseline additions
Retrieval refinements
Workflow modifications

Documenting these decisions helps preserve the evolution of the research process.

Documentation Standards

Decision records should be:

Clear

State what was decided.

Concise

Focus on relevant information.

Evidence-Based

Reference observations whenever possible.

Traceable

Link decisions to calibration and experimentation.

Honest

Document limitations and uncertainties when appropriate.

Summary

The decision log serves as the historical record of architectural, methodological, experimental, and organizational choices made throughout the project.

By documenting context, alternatives, evidence, decisions, and expected impact, the project preserves the reasoning behind its evolution and supports transparency, reproducibility, and long-term maintainability.
