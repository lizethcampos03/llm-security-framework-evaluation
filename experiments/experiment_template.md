Experiment Record Template
Experiment Information
Experiment Identifier
EXP-###

Examples:

EXP-001
EXP-002
EXP-003
Experiment Title

Provide a concise descriptive title.

Example:

Contextual Vulnerability Evaluation Across SecurityEval-Derived Samples
Date
YYYY-MM-DD
Experiment Category

Select one:

Vulnerability Classification
Comparative Evaluation
Workflow Integration
Retrieval Evaluation
Validation Evaluation
Model Comparison
Other
Research Question Alignment

Select applicable research question(s):

RQ1 – Architectural Calibration and Evolution
RQ2 – Contextual Vulnerability Reasoning
RQ3 – Comparative Detection Performance
RQ4 – End-to-End Workflow Integration
Objective
Purpose

Describe the purpose of the experiment.

Example:

Evaluate the framework's ability to distinguish vulnerable and secure implementations across multiple CWE categories.

Motivation

Why is this experiment important?

Example:

The experiment provides quantitative evidence regarding contextual vulnerability reasoning capability.

Experimental Design
Dataset

Describe the dataset used.

Include:

Dataset source
Dataset version
Number of samples
Vulnerability categories
Ground-truth methodology

Example:

SecurityEval-derived dataset
100 samples
10 CWE categories
Balanced secure/vulnerable distribution
Framework Configuration

Describe the evaluated configuration.

Examples:

Model used
Retrieval configuration
Validation strategy
Prompt version
Context profile version
Baselines

List comparison systems if applicable.

Examples:

Bandit
CodeQL
Published methodology
Previous framework version

If no baselines exist:

Not Applicable
Procedure

Describe the experiment step-by-step.

Example:

Load evaluation samples.
Execute framework analysis.
Record classifications.
Record explanations.
Record remediation outputs.
Compare results against ground truth.
Compute evaluation metrics.
Analyze findings.
Evaluation Metrics

Select all applicable metrics.

Classification Metrics
Accuracy
Precision
Recall
F1 Score
False Positive Rate
False Negative Rate
Reliability Metrics
Confidence Consistency
Validation Agreement
Stability Across Runs
Retrieval Metrics
Retrieval Relevance
Retrieved Context Quality
Context Coverage
Explainability Metrics
Explanation Completeness
Explanation Correctness
Explanation Clarity
Remediation Metrics
Fix Correctness
Fix Completeness
Security Relevance
Efficiency Metrics
Latency
Runtime
Computational Cost
Results
Quantitative Results
Metric	Value
Accuracy	
Precision	
Recall	
F1 Score	
False Positive Rate	
False Negative Rate	
Latency	
Vulnerability Coverage
CWE	Samples	Correct	Incorrect
CWE-XX			
CWE-YY			
CWE-ZZ			
Baseline Comparison

(Optional)

Tool	Accuracy	Precision	Recall
Framework			
Bandit			
CodeQL			
Qualitative Analysis
Observations

Describe notable findings.

Examples:

Strong contextual reasoning
Improved access-control analysis
Retrieval relevance improvements
Explanation quality strengths
Failure Cases

Describe important failures.

Examples:

Missed vulnerabilities
False positives
Context interpretation errors
Retrieval mismatches
Representative Examples

(Optional)

Provide selected examples demonstrating:

Successful detections
Missed vulnerabilities
Interesting behavior
Unexpected findings
Discussion
Research Question Interpretation

Explain how findings relate to the targeted research question.

Example:

Results suggest contextual grounding improves identification of authorization-related vulnerabilities compared to code-only analysis.

Strengths

Examples:

High detection accuracy
Strong explanation quality
Consistent outputs
Effective retrieval grounding
Limitations

Examples:

Limited dataset size
Retrieval failures
Context sensitivity
Benchmark constraints
Threats to Validity

Describe factors that may influence interpretation.

Examples:

Dataset bias
Model variability
Ground-truth uncertainty
Tool-version differences
Conclusions

Summarize key findings.

Example:

The framework demonstrated strong performance on context-dependent vulnerability scenarios and produced useful remediation guidance. Retrieval quality remained a significant factor influencing overall effectiveness.

Follow-Up Actions

List future work resulting from this experiment.

Examples:

Expand dataset coverage
Refine retrieval strategy
Improve validation methodology
Investigate failure cases
Conduct comparative evaluation
Related Documentation

Reference associated materials.

Examples:

docs/experimental_methodology.md

calibration/CAL-RAG-003.md

results/experiment1/

decision_log.md
Artifact Locations
Raw Results
results/experimentX/raw/
Figures
results/figures/
Tables
results/summary_tables/
Supporting Files
experiments/experimentX/supporting_materials/
Summary

Provide a concise executive summary of the experiment.

Example:

The experiment evaluated contextual vulnerability reasoning across a SecurityEval-derived dataset covering ten CWE categories. The framework achieved strong classification performance and demonstrated improved reasoning for context-dependent vulnerabilities while revealing several retrieval-related limitations that warrant future investigation.
