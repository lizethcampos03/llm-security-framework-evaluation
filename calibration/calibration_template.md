Calibration Record Template
Calibration Information
Calibration Identifier
CAL-XXX-###

Examples:

CAL-RAG-001
CAL-CTX-002
CAL-VAL-003
CAL-PRM-004
CAL-LLM-005
Date
YYYY-MM-DD
Calibration Category

Select one:

Context Engineering
Retrieval
Validation
Prompt Engineering
Model Configuration
Workflow Design
Other
Research Question Alignment

Select applicable research question(s):

RQ1 – Architectural Calibration and Evolution
RQ2 – Contextual Vulnerability Reasoning
RQ3 – Comparative Detection Performance
RQ4 – End-to-End Workflow Integration
Objective
Calibration Goal

Describe the specific question being investigated.

Example:

Evaluate whether including authorization context improves vulnerability detection accuracy for access-control weaknesses.

Motivation

Why is this calibration necessary?

Example:

Previous evaluations produced inconsistent classifications when authorization requirements were not explicitly provided.

Observation
Initial Observation

Describe the issue, weakness, inconsistency, or opportunity for improvement that motivated this calibration.

Examples:

Irrelevant retrieval results
False-positive increase
Weak explanations
Missing vulnerabilities
Validation inconsistency
Context interpretation errors
Evidence Supporting Observation

Provide supporting evidence.

Examples:

Prior calibration results
Experiment observations
Example outputs
Literature references
Hypothesis
Proposed Explanation

State the hypothesis being tested.

Example:

Providing structured authorization context will improve vulnerability reasoning and reduce false positives associated with access-control decisions.

Expected Outcome

Describe what improvement is expected.

Examples:

Improved classification accuracy
Better explanation quality
Reduced false positives
Higher retrieval relevance
Increased consistency
Configuration
Baseline Configuration

Describe the original configuration.

Example:

Code only
No authorization context
Single retrieval query
10 validation runs
Modified Configuration

Describe the new configuration being tested.

Example:

Code + authorization context
Role descriptions included
Single retrieval query
10 validation runs
Evaluation Methodology
Evaluation Dataset

Describe the samples used.

Examples:

SecurityEval subset
Authorization vulnerabilities
Custom benchmark samples
Calibration dataset
Sample Size
Number of evaluation samples
Evaluation Procedure

Document the process used.

Example:

Run baseline configuration.
Record outputs.
Apply modification.
Re-run evaluation.
Compare outcomes.
Analyze differences.
Metrics

Select applicable metrics.

Accuracy
False Positive Rate
False Negative Rate
Confidence Consistency
Retrieval Relevance
Explanation Quality
Remediation Quality
Latency
Other
Results
Quantitative Results
Metric	Baseline	Modified	Difference
Accuracy			
False Positives			
False Negatives			
Confidence			
Latency			
Qualitative Observations

Describe important observations.

Examples:

Improved contextual reasoning
Better authorization interpretation
More relevant retrieval results
Reduced hallucinations
Improved explanation clarity
Example Outputs

(Optional)

Provide representative examples.

Include:

Input summary
Output summary
Observed differences
Analysis
Did the Results Support the Hypothesis?

Describe whether findings aligned with expectations.

Example:

Results partially supported the hypothesis. Authorization context reduced false positives but introduced additional latency.

Benefits Observed

Examples:

Improved reasoning
Better retrieval grounding
More accurate classifications
Improved consistency
Drawbacks Observed

Examples:

Increased latency
Additional complexity
Marginal improvement
Larger prompts
Unexpected Findings

Document any surprising outcomes.

Decision
Outcome

Select one:

Adopt
Reject
Requires Additional Investigation
Integrate Into Future Experiment
Decision Rationale

Explain why the decision was reached.

Example:

The improvement in classification accuracy outweighed the minor increase in latency.

Architectural Impact

Describe how this calibration influences the framework.

Examples:

Retrieval modification adopted
Validation strategy updated
Prompt revised
Context profile expanded
Follow-Up Actions

List future actions.

Examples:

Expand evaluation dataset
Investigate retrieval ranking
Test additional models
Incorporate into Experiment 1
Related Documentation

Reference supporting materials.

Examples:

decision_log.md
docs/architecture_summary.md
docs/experimental_methodology.md
calibration/rag/
experiments/experiment1_securityeval/
Summary

Provide a concise summary of the calibration.

Example:

Structured authorization context improved vulnerability classification accuracy and reduced false positives for access-control weaknesses. The modification was adopted for future experimentation and integrated into the framework configuration used for Experiment 1.
