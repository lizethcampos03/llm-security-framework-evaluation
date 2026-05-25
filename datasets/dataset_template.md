Dataset Documentation Template

Dataset Information

Dataset Identifier

DATASET-###

Examples:

DATASET-001
DATASET-002
DATASET-003
Dataset Name

Provide a descriptive name.

Example:

SecurityEval-Derived Contextual Vulnerability Benchmark v1
Version
v1.0
Date Created
YYYY-MM-DD
Dataset Status

Select one:

Draft
Under Review
Approved for Calibration
Approved for Experiments
Archived
Purpose
Objective

Describe the purpose of the dataset.

Example:

Evaluate vulnerability-detection performance across context-dependent security weaknesses spanning multiple CWE categories.

Research Question Alignment

Select applicable research questions.

RQ1 – Architectural Calibration and Evolution
RQ2 – Contextual Vulnerability Reasoning
RQ3 – Comparative Detection Performance
RQ4 – End-to-End Workflow Integration
Dataset Origin
Source Methodology

Describe how the dataset was created.

Examples:

SecurityEval-derived generation
Manual construction
Existing benchmark adaptation
Real-world vulnerability collection
Reference Sources

List important references.

Examples:

SecurityEval
CWE
CVE
Published vulnerability benchmarks
Academic literature
Dataset Composition
Total Samples
Category	Count
Vulnerable Samples	
Secure Samples	
Total Samples	
Vulnerability Categories
CWE	Description	Sample Count
CWE-XX		
CWE-YY		
CWE-ZZ		
Programming Languages
Language	Count
Python	
Other	
Context Profiles

Indicate whether contextual information is included.

Examples:

Authorization requirements
User roles
Workflow descriptions
Operational assumptions
Protected resources
Security expectations
Sample Generation Methodology
Generation Procedure

Describe how samples were produced.

Example:

Select target CWE.
Generate vulnerable implementation.
Generate secure implementation.
Create security context profile.
Review outputs.
Assign ground truth.
Validate consistency.
Generation Parameters

Document relevant generation settings.

Examples:

Model used
Prompt version
Temperature
Context generation strategy
Ground Truth Methodology
Vulnerability Labeling

Describe how labels were assigned.

Examples:

Manual review
Benchmark labels
SecurityEval methodology
Literature-based validation
CWE Assignment

Describe how CWE mappings were determined.

Verification Procedure

Explain how correctness was reviewed.

Examples:

Manual inspection
Multiple reviewers
Reference comparison
Benchmark validation
Dataset Structure
File Organization

Example:

datasets/

dataset_v1/

vulnerable/

secure/

contexts/

ground_truth/
Sample Format

Document structure of each sample.

Example:

Source Code
Security Context
Ground Truth Label
CWE Mapping
Notes
Dataset Statistics
Vulnerability Distribution
Vulnerability Type	Count
Injection	
Access Control	
Authentication	
Configuration	
Dependency	
Secure/Vulnerable Balance
Class	Count
Secure	
Vulnerable	
Context Distribution

Describe context coverage.

Examples:

Authorization context
Business logic context
Workflow context
Operational context
Intended Usage

This dataset is intended for:

Calibration studies
Vulnerability detection evaluation
Comparative analysis
Retrieval investigations
Validation studies
End-to-end workflow experiments
Limitations

Describe known limitations.

Examples:

Synthetic generation
Limited language coverage
Benchmark constraints
Ground-truth ambiguity
Limited real-world complexity
Ethical Considerations

The dataset is intended for:

Security research
Educational use
Vulnerability-analysis evaluation

The dataset should not be used to facilitate malicious activity.

Reproducibility Information

Document:

Generation methodology
Prompt versions
Model versions
Review procedures
Validation procedures
Dataset versions

This information should allow future researchers to understand how the dataset was constructed.

Related Documentation

Examples:

docs/experimental_methodology.md

docs/reproducibility.md

experiments/experiment1_securityeval/

references/references.md

decision_log.md
Future Revisions

Potential future updates:

Additional CWE categories
Expanded context profiles
Additional programming languages
Real-world vulnerability examples
Benchmark expansion
Summary

Provide a concise summary of the dataset.

Example:

Dataset v1 contains 100 SecurityEval-derived samples spanning ten CWE categories. Each sample includes source code, contextual security information, vulnerability labels, and CWE mappings. The dataset is intended to support calibration activities, comparative evaluation, and contextual vulnerability-reasoning experiments.
