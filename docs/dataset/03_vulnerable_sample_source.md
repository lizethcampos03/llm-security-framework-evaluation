# 03 Vulnerable Sample Source

## Purpose

This document describes the methodology used to construct the vulnerable class of the SecurityEval-derived contextual benchmark.

---

## Source of Vulnerable Samples

Vulnerable samples are derived directly from SecurityEval reference vulnerable implementations.

The project does not generate vulnerable examples from scratch.

Instead, SecurityEval serves as the authoritative source for vulnerable benchmark samples.

---

## Rationale

Using SecurityEval reference implementations provides:

- reproducibility
- alignment with prior research
- benchmark credibility
- consistent CWE coverage
- fair comparison conditions

---

## Methodology

For each selected SecurityEval task:

1. Identify task ID
2. Identify CWE mapping
3. Copy vulnerable implementation
4. Store implementation as vulnerable.py
5. Create metadata record
6. Create validation notes
7. Preserve traceability to original task

---

## Vulnerable Class Definition

The vulnerable class consists exclusively of SecurityEval-derived vulnerable implementations.

Secure counterparts are generated separately during a later dataset-construction phase using CWE-guided mitigation procedures.

---

## Current Status

Dataset construction in progress.
