Reproducibility and Transparency

Purpose

This document describes the procedures, documentation practices, and experimental standards used to support transparency and reproducibility throughout the AI-Assisted Vulnerability Detection in LLM-Generated Code project.

The objective is to ensure that architectural decisions, calibration activities, dataset construction procedures, experimental configurations, evaluation metrics, and reported findings can be understood, reviewed, and independently evaluated by future researchers.

While the framework itself continues to evolve as an active research effort, the project emphasizes methodological transparency and systematic documentation throughout the evaluation process.

Reproducibility Philosophy

The project follows four guiding principles.

Transparency

Research procedures, evaluation methodology, calibration activities, and experimental design decisions should be documented whenever possible.

Traceability

Reported findings should be traceable to:

Experimental records
Calibration records
Dataset definitions
Evaluation metrics
Architectural decisions
Consistency

Experiments should be conducted using clearly documented procedures and evaluation criteria.

Continuous Documentation

Architectural evolution, calibration outcomes, and experimental changes should be recorded as the project progresses.

Repository Documentation Structure

The repository organizes information into dedicated sections to support reproducibility.

docs/
calibration/
experiments/
datasets/
results/
references/
reports/

Each section contributes to documenting a specific aspect of the research process.

Project Documentation

Location:

docs/

Contains:

Project overview
Architecture summary
Experimental methodology
Reproducibility procedures
Research roadmap

Purpose:

Provide high-level project documentation and methodological context.

Calibration Documentation

Location:

calibration/

Contains:

Context-engineering studies
Retrieval investigations
Prompt-calibration studies
Validation evaluations
Model-comparison studies

Purpose:

Document architectural evolution and evidence supporting design decisions.

Experimental Documentation

Location:

experiments/

Contains:

Experiment objectives
Evaluation procedures
Metric definitions
Experimental observations
Study-specific conclusions

Purpose:

Document how formal evaluations were conducted.

Dataset Documentation

Location:

datasets/

Contains:

Dataset descriptions
Dataset generation procedures
Security context profiles
Ground-truth definitions
Benchmark mappings

Purpose:

Provide transparency regarding evaluation data.

Results Documentation

Location:

results/

Contains:

Figures
Tables
Raw measurements
Summary statistics
Comparative analyses

Purpose:

Provide supporting evidence for reported findings.

Dataset Reproducibility

The project documents dataset construction procedures to support understanding and future replication.

Documentation may include:

Dataset sources
Generation methodology
Prompt templates
SecurityEval alignment
Sample selection criteria
Ground-truth assignment procedures
Vulnerability-category mappings

Where applicable, references to original benchmark sources are maintained.

Calibration Reproducibility

Each calibration study should document:

Calibration Identifier

Example:

CAL-RAG-001
Objective

What architectural question is being investigated?

Observation

What motivated the calibration?

Hypothesis

What explanation is being tested?

Adjustment

What modification was introduced?

Evaluation Method

How was the modification assessed?

Results

What outcomes were observed?

Decision

What conclusion was reached?

Architectural Impact

How did the result influence the framework?

Experimental Reproducibility

Each experiment should document:

Research Question

Which research question is being addressed?

Dataset

Which evaluation samples were used?

Configuration

Which framework configuration was evaluated?

Procedure

How was the experiment conducted?

Metrics

Which metrics were measured?

Results

What outcomes were observed?

Limitations

What factors may influence interpretation?

Conclusions

What findings were obtained?

Configuration Documentation

Whenever possible, evaluation records should document relevant configuration information.

Examples include:

Programming language version
Framework version
Model configuration
Retrieval configuration
Validation configuration
Evaluation parameters
Tool versions

Examples of comparison tools may include:

Bandit version
CodeQL version
Additional analysis tools used during evaluation

The goal is to improve interpretability of experimental outcomes.

Evaluation Metrics Documentation

Metric definitions should remain consistent across experiments whenever possible.

Examples include:

Accuracy
False positive rate
False negative rate
Confidence consistency
Retrieval relevance
Explanation quality
Remediation quality
Latency

Changes to metric definitions should be documented explicitly.

Decision Documentation

Architectural decisions are recorded separately through the project decision log.

Examples include:

Retrieval strategy selection
Validation methodology selection
Context-engineering decisions
Model configuration decisions
Experimental design decisions

Decision records improve transparency regarding project evolution.

Version Documentation

Project evolution is tracked through repository version history and change records.

Examples include:

Architectural updates
Calibration updates
Dataset updates
Evaluation updates
Documentation revisions

Version tracking helps preserve historical context throughout development.

Limitations of Reproducibility

Several factors may influence exact reproduction of results.

Examples include:

Probabilistic model behavior
Model updates over time
Retrieval variability
Tool-version changes
Benchmark evolution
Environmental differences

Consequently, exact numerical replication may not always be possible.

However, the objective is to provide sufficient documentation for researchers to understand, evaluate, and reproduce the overall methodology.

Relationship to Research Questions

Reproducibility supports all project research questions by ensuring that:

Calibration procedures are documented
Experimental procedures are transparent
Dataset construction is traceable
Evaluation metrics are defined
Findings can be independently assessed

This documentation strengthens the credibility and interpretability of reported results.

Summary

This project emphasizes transparency, traceability, consistency, and continuous documentation throughout calibration, experimentation, and evaluation.

By maintaining structured records of datasets, calibration studies, experimental procedures, evaluation metrics, configuration information, and architectural decisions, the repository seeks to provide a clear and reproducible record of the research process and the evidence supporting its conclusions.
