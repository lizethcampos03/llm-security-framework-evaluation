# Embedding Model Selection

## Purpose

This document records the initial embedding model strategy for the CWE Discovery subsystem.

The goal is to support retrieval over:

- CWE descriptive guidance
- code vulnerability patterns
- future CVE evidence

---

# Requirements

The embedding model should support:

- code similarity
- semantic similarity
- reproducible retrieval experiments
- reasonable implementation effort
- acceptable latency
- integration with the existing RAG pipeline

---

# Candidate Options

## Option A — OpenAI Embeddings

Advantages:

- easiest to integrate
- strong semantic performance
- low implementation complexity
- works for both code and natural language text
- practical for prototype calibration

Limitations:

- external API dependency
- not specifically trained only for code structure

---

## Option B — CodeBERT

Advantages:

- code-focused representation model
- research-aligned
- useful for code similarity tasks

Limitations:

- more setup complexity
- local model management required
- may require additional preprocessing

---

## Option C — GraphCodeBERT

Advantages:

- incorporates code structure and data-flow information
- more theoretically aligned with vulnerability analysis

Limitations:

- highest setup complexity
- more difficult to implement quickly
- may be better suited for future work than current calibration

---

# Initial Decision

The initial implementation will use OpenAI embeddings.

Reason:

This option provides the best balance between:

- implementation speed
- reproducibility
- semantic retrieval quality
- integration simplicity

The project can later compare OpenAI embeddings against CodeBERT or GraphCodeBERT if time allows.

---

# Future Work

Future embedding comparisons may evaluate:

- CodeBERT
- GraphCodeBERT
- vulnerability-specific code embeddings
- AST-based embeddings
- graph-based code representations

These comparisons may help determine whether code-specialized embeddings improve CWE discovery beyond general-purpose embedding models.

---

# Final Selection for Initial Calibration

Initial embedding model:

OpenAI embedding model

Future comparison candidates:

- CodeBERT
- GraphCodeBERT