# 01 SecurityEval Overview

## Purpose

This document explains the role of SecurityEval in the dataset-generation methodology for the project:

AI-Assisted Vulnerability Detection in LLM-Generated Code: A LangGraph-Orchestrated Workflow for Context-Aware Vulnerability Detection and Secure Code Fixing.

The purpose of this phase is to acquire, inspect, and document SecurityEval before constructing the expanded contextual benchmark.

---

## Why SecurityEval Is Used

SecurityEval is used as the dataset foundation because it provides established vulnerability-oriented code-generation tasks mapped to CWE categories.

Using SecurityEval improves:

- Reproducibility
- Alignment with prior research
- Benchmark credibility
- CWE coverage
- Fairness in evaluation

Rather than generating vulnerable samples from scratch, this project uses SecurityEval reference vulnerable implementations as the vulnerable class.

---

## Role in the Expanded Dataset

SecurityEval serves as the foundation for the expanded benchmark.

The expanded dataset will include:

- Vulnerable implementations
- CWE-guided secure counterparts
- Security context profiles
- Metadata records
- Validation notes
- Tool-analysis results

---

## Expanded Dataset Structure

```text
datasets/securityeval_expanded/
├── vulnerable/
├── secure/
├── context_profiles/
├── labels/
├── metadata/
├── validation/
└── README.md
```

Each final sample should eventually include:

```text
sample_id/
├── vulnerable.py
├── secure.py
├── context_profile.json
├── metadata.json
└── validation_notes.md
```

---

## Methodology Statement

Vulnerable samples are derived from SecurityEval reference vulnerable implementations and used as the vulnerable class for evaluation.

Secure counterparts are generated separately using CWE-specific mitigation guidance and a standardized secure-rewrite methodology.

Security context profiles are added to support context-aware vulnerability analysis.

---

## Phase 1 Output

The output of Phase 1 is:

- SecurityEval inspected
- Dataset source documented
- Expanded dataset structure defined
- Foundation prepared for schema definition and vulnerable sample extraction
