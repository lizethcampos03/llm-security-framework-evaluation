# Code Embedding Strategy

## Purpose

The purpose of the Code Pattern Knowledge Base is to improve CWE discovery by matching user-provided code against previously embedded vulnerability patterns.

The goal is not to find identical code.

The goal is to identify similar vulnerability structures that may indicate the presence of the same CWE.

---

# Design Objective

Given:

* source code
* security context profile

The retrieval system should identify:

* similar vulnerability patterns
* likely CWE candidates
* supporting evidence

without requiring the user to specify the CWE.

---

# Why Code Embeddings

Traditional keyword search may fail when:

* variable names differ
* function names differ
* implementation details differ

However, the underlying vulnerability pattern may remain similar.

Code embeddings help identify:

* structural similarity
* semantic similarity
* behavioral similarity

between code samples.

---

# Knowledge Base Contents

The Code Pattern Knowledge Base should contain:

## Vulnerable Examples

Small vulnerability-focused code snippets.

Each snippet should be labeled with:

* CWE identifier
* CWE name

Examples:

* SQL Injection
* Command Injection
* Path Traversal
* Missing Authentication
* Hardcoded Credentials

---

## Secure Examples

Secure implementations corresponding to vulnerable patterns.

Purpose:

Provide repair-oriented context and improve downstream reasoning.

---

# Evaluation Leakage Prevention

The Code Pattern Knowledge Base should not contain:

* exact evaluation samples
* exact calibration samples

Reason:

The goal is to evaluate generalization rather than memorization.

The retrieval system should identify similar patterns rather than identical code.

---

# Metadata

Each embedded code sample should store:

* sample identifier
* CWE identifier
* CWE name
* language
* vulnerability category
* vulnerable or secure label

Example:

CWE-89

Language:
Python

Category:
SQL Injection

Label:
Vulnerable

---

# Retrieval Process

Step 1

Embed user code.

---

Step 2

Search nearest code embeddings.

---

Step 3

Retrieve candidate vulnerability patterns.

---

Step 4

Collect associated CWE candidates.

---

Step 5

Combine with CWE retrieval results.

---

Step 6

Generate ranked CWE candidates.

---

# Calibration Configurations

Configuration A

No code embeddings.

Use CWE retrieval only.

---

Configuration B

Code embeddings only.

Use nearest-neighbor retrieval.

---

Configuration C

CWE retrieval
+
Code embeddings

Use combined candidate ranking.

---

# Future Extensions

Future versions may include:

* graph-based code representations
* AST embeddings
* CFG embeddings
* vulnerability-specific embedding models
* multi-language support

These extensions are outside the scope of the initial calibration study.

---

# Expected Outcome

The expected outcome is that code embeddings improve:

* Top-1 CWE accuracy
* Top-3 CWE accuracy
* ranking quality
* downstream detection usefulness

compared to CWE retrieval alone.
