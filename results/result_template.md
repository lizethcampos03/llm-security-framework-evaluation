Result Documentation Template

Result Information

Result Identifier

RESULT-###

Examples:

RESULT-001
RESULT-002
RESULT-003
Associated Study

Specify the experiment or calibration study.

Examples:

Experiment 1 – Contextual Vulnerability Evaluation

Experiment 2 – Comparative Evaluation

Experiment 3 – End-to-End Workflow Integration

CAL-RAG-001

CAL-CTX-003
Date
YYYY-MM-DD
Author

Document who generated the result.

Example:

Lizeth Campos
Executive Summary

Provide a concise summary of the result.

Example:

The framework achieved 87% classification accuracy across ten CWE categories and demonstrated improved performance on context-dependent access-control vulnerabilities compared to baseline approaches.

Limit to approximately one paragraph.

Objective

Describe the purpose of the study that produced this result.

Example:

Evaluate vulnerability classification performance across a SecurityEval-derived benchmark spanning multiple CWE categories.

Research Question Alignment

Select applicable research questions.

RQ1 – Architectural Calibration and Evolution
RQ2 – Contextual Vulnerability Reasoning
RQ3 – Comparative Detection Performance
RQ4 – End-to-End Workflow Integration
Experimental Configuration
Dataset

Specify:

Dataset name
Dataset version
Number of samples
Vulnerability categories

Example:

SecurityEval-Derived Contextual Benchmark v1

100 samples

10 CWE categories
Framework Configuration

Specify:

Model
Retrieval configuration
Validation configuration
Prompt version
Context profile version

Example:

GPT-5

Hybrid Retrieval v2

Validation Strategy v1

Prompt Template v3
Comparison Systems

If applicable:

Bandit
CodeQL
Published methodology
Previous framework version

If none:

Not Applicable
Quantitative Results
Primary Metrics
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
Validation Metrics
Metric	Value
Consistency	
Agreement Rate	
Confidence Average	
Retrieval Metrics
Metric	Value
Retrieval Relevance	
Context Coverage	
Retrieval Success Rate	
Remediation Metrics
Metric	Value
Fix Correctness	
Fix Completeness	
Security Relevance	
Visualizations

List figures associated with the result.

Example:

Figure 1 – Accuracy by CWE Category

Figure 2 – False Positive Distribution

Figure 3 – Retrieval Quality Comparison

Figure 4 – Tool Comparison Summary
Figure Locations
results/figures/
Comparative Analysis

(Optional)

Used when comparing multiple systems.

Tool	Accuracy	Precision	Recall
Framework			
Bandit			
CodeQL			
Key Findings

Document the most important observations.

Examples:

Strong performance on authorization vulnerabilities
Improved retrieval grounding
Reduced false positives
Improved explanation quality
Better remediation guidance
Failure Cases

Document important failures.

Examples:

Missed vulnerabilities
Incorrect classifications
Weak explanations
Retrieval mismatches
Validation inconsistencies
Representative Examples

(Optional)

Provide notable examples.

For each example include:

Example Identifier
Context
Expected Outcome
Observed Outcome
Analysis
Interpretation
What Do These Results Mean?

Provide interpretation of findings.

Examples:

Architectural strengths
Architectural weaknesses
Retrieval observations
Validation observations
Context-engineering impact
Relationship to Research Questions

Explain how findings contribute to the associated research question(s).

Example:

The results support RQ2 by demonstrating improved reasoning performance for context-dependent authorization vulnerabilities.

Threats to Validity

Document factors that may influence interpretation.

Examples:

Dataset limitations
Model variability
Prompt sensitivity
Benchmark bias
Limited sample size
Conclusions

Summarize the most important outcomes.

Example:

The framework demonstrated strong contextual reasoning capability and benefited from retrieval augmentation, although retrieval quality remained a critical factor influencing overall performance.

Follow-Up Actions

Document future work motivated by the result.

Examples:

Expand dataset coverage
Improve retrieval ranking
Investigate failure cases
Refine validation strategy
Conduct comparative evaluation
Related Documentation

Examples:

experiments/experiment1_securityeval/

calibration/CAL-RAG-002.md

docs/experimental_methodology.md

decision_log.md

CHANGELOG.md
Artifact Locations
Raw Data
results/raw/
Tables
results/summary_tables/
Figures
results/figures/
Supporting Materials
results/supporting_materials/
Summary Statement

Provide a final one-paragraph summary suitable for inclusion in reports, presentations, or future publications.

Example:

The evaluation demonstrated that the proposed framework effectively combines contextual grounding, retrieval-augmented security knowledge, validation strategies, and remediation generation to support vulnerability analysis across multiple CWE categories. Comparative evaluation and end-to-end workflow studies provide additional evidence regarding the strengths and limitations of orchestration-oriented security analysis.
