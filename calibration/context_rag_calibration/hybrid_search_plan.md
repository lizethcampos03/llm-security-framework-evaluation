# Hybrid Search Calibration Plan

## Purpose

This document defines the calibration strategy for hybrid retrieval within the LLM security framework.

The retrieval system is responsible for providing relevant CWE and security guidance to downstream workflow stages, including:

- detection
- repair generation
- repair verification
- reporting

The purpose of hybrid retrieval calibration is to improve retrieval quality while reducing noisy or irrelevant results.

---

## Motivation

Early retrieval experiments showed that purely semantic retrieval may return:

- partially related CWE entries
- weakly relevant security guidance
- noisy context
- incomplete mitigation information

These retrieval issues may negatively affect downstream workflow quality.

Therefore, retrieval calibration focuses on improving:

- relevance
- ranking quality
- retrieval consistency
- workflow usefulness

---

## Hybrid Retrieval Philosophy

The workflow assumes that no single retrieval strategy is sufficient for all cases.

Instead, retrieval should combine multiple signals.

The hybrid retrieval strategy may combine:

```text
semantic similarity
+
keyword matching
+
CWE-aware retrieval
+
metadata-aware retrieval
+
context-aware ranking

The goal is to improve the quality of retrieved security guidance.

Retrieval Inputs

The retrieval system may use:

vulnerable code
detected CWE candidates
context profile fields
security requirements
threat concerns
application type
deployment context
metadata filters
extracted keywords
Context Profile Integration

The context profile is expected to improve retrieval quality.

Examples:

application type may influence relevant CWE prioritization
threat concerns may improve keyword selection
deployment context may improve mitigation relevance
protected assets may improve ranking quality

The calibration process should evaluate which context fields provide meaningful retrieval improvements.

Hybrid Retrieval Experiments

The calibration stage may compare:

Strategy A — Semantic Retrieval Only

Embedding similarity only.

Strategy B — Semantic + Keyword Retrieval

Embedding similarity combined with keyword overlap.

Strategy C — Context-Aware Hybrid Retrieval

Embedding similarity combined with:

keyword retrieval
metadata-aware ranking
context-profile-aware ranking
CWE-aware prioritization
Retrieval Evaluation Areas
Retrieval Relevance

Whether retrieved guidance is actually relevant to the target case.

Retrieval Ranking Quality

Whether the most useful results appear near the top.

Retrieval Consistency

Whether repeated retrievals remain stable.

Retrieval Noise Reduction

Whether irrelevant retrievals are reduced.

Workflow Impact

Whether improved retrieval improves downstream:

vulnerability detection
secure repair
repair verification
reporting quality
Retrieval Calibration Metrics

Calibration may record:

top-k relevance
retrieval precision
retrieval consistency
retrieval noise rate
downstream detection improvement
downstream repair improvement
retrieval latency
Main Retrieval Hypothesis

The primary hypothesis is:

Context-aware hybrid retrieval
improves the quality of retrieved security guidance
compared to semantic-only retrieval.
Relationship to Detection and Repair

The retrieval system directly influences downstream workflow quality.

Poor retrieval quality may negatively affect:

detection accuracy
repair quality
repair verification
report usefulness

Therefore, retrieval calibration occurs before downstream node calibration.

Calibration Decision

After calibration, the following should be documented:

selected retrieval strategy
selected ranking strategy
selected context fields
selected retrieval filters
known retrieval limitations
examples of improved retrieval behavior
Future Directions

Future retrieval improvements may include:

GraphRAG integration
CWE relationship traversal
CVE-to-CWE retrieval augmentation
retrieval reranking models
retrieval confidence estimation
adaptive retrieval depth
workflow-aware retrieval feedback
