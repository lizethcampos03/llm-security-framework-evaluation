# Retrieval Quality Metrics

## Purpose

This document defines the evaluation metrics used during Context Profile + RAG calibration.

The retrieval system is evaluated not only on retrieval similarity, but also on whether retrieved information improves downstream workflow behavior.

The purpose of these metrics is to measure:

- retrieval relevance
- retrieval usefulness
- retrieval consistency
- retrieval noise
- downstream workflow impact

---

## Retrieval Evaluation Philosophy

Traditional retrieval systems are often evaluated only using similarity metrics.

However, within this workflow, retrieval quality should also be evaluated based on whether retrieved context improves:

- vulnerability detection
- secure repair
- repair verification
- reporting quality

The retrieval system is therefore evaluated as part of the workflow, not as an isolated component.

---

# Primary Retrieval Metrics

## Top-K Relevance

Measures whether relevant CWE/security guidance appears within the top retrieved results.

Example:

```text
Top-1 relevance
Top-3 relevance
Top-5 relevance

Higher relevance indicates better retrieval quality.

Retrieval Precision

Measures the proportion of retrieved results that are actually useful.

Example:

useful_results / total_results

Higher precision indicates lower retrieval noise.

Retrieval Noise Rate

Measures how often irrelevant or weakly related retrievals appear.

Examples of noisy retrieval include:

unrelated CWE entries
weakly related mitigation guidance
incorrect security context
irrelevant examples

Lower noise rates are preferred.

Retrieval Consistency

Measures whether repeated retrievals remain stable across runs.

Large variations in retrieved guidance may negatively affect downstream workflow consistency.

Retrieval Ranking Quality

Measures whether the most useful security guidance appears near the top of retrieval results.

Relevant guidance should appear before weakly related guidance whenever possible.

Context Profile Metrics
Context Contribution

Measures whether context profile fields improve retrieval quality.

Examples:

application type
deployment context
threat concerns
protected assets
authorization rules

The calibration process should identify which fields provide meaningful improvements.

Context Overhead

Measures whether the amount of required context becomes excessive.

The goal is to balance:

workflow usefulness
vs
user burden
Downstream Workflow Metrics
Detection Improvement

Measures whether improved retrieval increases:

detection accuracy
precision
recall
reasoning quality
Repair Improvement

Measures whether improved retrieval increases:

repair quality
mitigation quality
functionality preservation
repair consistency
Report Improvement

Measures whether improved retrieval increases:

evidence usefulness
report clarity
report completeness
Retrieval Calibration Comparisons

The calibration stage may compare:

Semantic Retrieval Only

Embedding similarity only.

Semantic + Keyword Retrieval

Embedding similarity combined with keyword matching.

Context-Aware Hybrid Retrieval

Embedding similarity combined with:

keyword retrieval
metadata-aware ranking
context-aware ranking
CWE-aware prioritization
Main Retrieval Calibration Hypothesis

The primary hypothesis is:

Context-aware hybrid retrieval
improves retrieval quality
and downstream workflow performance
compared to semantic-only retrieval.
Manual Review

Manual review is important during retrieval calibration.

Retrieved guidance should be inspected to determine whether:

the retrieved CWE is correct
the mitigation guidance is relevant
the retrieved context supports downstream reasoning
retrieval noise is present
ranking quality is acceptable
Calibration Decision

After calibration, the following should be documented:

selected retrieval strategy
selected ranking strategy
selected context fields
selected retrieval filters
known retrieval limitations
examples of improved retrieval behavior
