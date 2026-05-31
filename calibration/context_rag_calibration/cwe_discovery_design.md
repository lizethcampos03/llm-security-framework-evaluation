# CWE Discovery Design

## Purpose

The objective of the CWE Discovery subsystem is to identify the most likely vulnerability categories present in user-provided code before vulnerability detection and repair occur.

Unlike traditional retrieval systems that assume a known CWE identifier, this subsystem must infer likely CWE candidates directly from code, security context, and user concerns.

The retrieved information is then provided to downstream workflow components.

---

# Problem Statement

Users do not know which CWE exists in their code.

Users provide:

* source code
* security context profile
* optional security concerns

The system must determine:

* likely CWE candidates
* supporting CWE guidance
* supporting examples
* supporting repair information

without being told the correct CWE.

---

# Inputs

## Required

Source Code

Security Context Profile

---

## Optional

User Security Concerns

Examples:

* authentication concerns
* data leakage concerns
* privilege escalation concerns
* cloud security concerns

---

# Knowledge Sources

## Knowledge Source 1

CWE Knowledge Base

Contents:

* CWE identifiers
* CWE descriptions
* extended descriptions
* mitigations
* detection methods
* consequences
* observed examples
* related weaknesses

Purpose:

Primary vulnerability knowledge source.

---

## Knowledge Source 2

Code Pattern Knowledge Base

Contents:

* vulnerable code examples
* secure code examples
* SecurityEval samples
* CWE-labeled examples

Embedded using a code embedding model.

Purpose:

Identify vulnerabilities through code similarity.

---

## Future Knowledge Source

CVE Knowledge Base

Contents:

* CVE descriptions
* CVE metadata
* CWE mappings

Purpose:

Provide real-world vulnerability evidence.

Not required for initial calibration.

---

# Retrieval Strategy

Each knowledge source supports:

## Keyword Search

Used for:

* function names
* imports
* APIs
* sinks
* sources
* security terminology

Advantages:

* precise
* interpretable
* fast

---

## Vector Search

Used for:

* semantic similarity
* code similarity
* contextual similarity

Advantages:

* broader matching
* semantic understanding

---

## Hybrid Search

Final retrieval uses:

keyword score

*

vector similarity score

to improve retrieval quality.

---

# Context Profile Usage

Context profiles are not used as a replacement for retrieval.

Context profiles are used as ranking signals.

Examples:

authentication_service

may increase ranking for:

* CWE-306
* CWE-287
* CWE-798

cloud_management_platform

may increase ranking for:

* CWE-918
* CWE-284
* CWE-862

Context narrows ambiguity among competing candidates.

---

# Candidate Generation

Step 1

Retrieve candidate CWE records.

Step 2

Retrieve candidate code examples.

Step 3

Combine candidate evidence.

Step 4

Generate ranked CWE candidates.

Example:

1. CWE-89
2. CWE-78
3. CWE-94

---

# Ranking Strategy

Candidate ranking should consider:

* keyword similarity
* vector similarity
* code similarity
* context profile relevance

Combined score:

Final Score =
Keyword Score
+
Vector Score
+
Code Similarity Score
+
Context Relevance Score

Weights will be calibrated experimentally.

---

# Calibration Configurations

## Configuration A

CWE Knowledge Base Only

Goal:

Measure baseline retrieval quality.

---

## Configuration B

Code Pattern Knowledge Base Only

Goal:

Measure code-similarity retrieval quality.

---

## Configuration C

CWE Knowledge Base
+
Code Pattern Knowledge Base

Goal:

Measure combined retrieval quality.

---

# Evaluation Metrics

Top-1 Accuracy

Correct CWE ranked first.

---

Top-3 Accuracy

Correct CWE appears within top three.

---

Mean Reciprocal Rank (MRR)

Measures ranking quality.

---

Retrieval Latency

Measures retrieval speed.

---

Context Gain

Measures improvement from context profile usage.

---

Detection Usefulness

Measures downstream impact on vulnerability detection.

---

Repair Usefulness

Measures downstream impact on vulnerability repair.

---

# Expected Outcome

The expected outcome is that:

Code Embeddings

*

Hybrid Retrieval

*

Security Context Profiles

improve CWE discovery accuracy compared to CWE retrieval alone.

The calibrated configuration will become the final retrieval architecture used by the workflow.
