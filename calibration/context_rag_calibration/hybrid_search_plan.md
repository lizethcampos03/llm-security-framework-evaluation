# Hybrid Search Calibration Plan

## Purpose

This document defines the retrieval strategies evaluated during Context + RAG Calibration.

---

# Retrieval Strategies

## Strategy A — Keyword Retrieval

Retrieve CWE guidance using:

* CWE identifier
* CWE name
* vulnerability description

Advantages:

* deterministic
* interpretable
* fast

Disadvantages:

* limited semantic matching
* may miss related guidance

---

## Strategy B — Vector Retrieval

Retrieve CWE guidance using semantic similarity.

Advantages:

* semantic matching
* broader retrieval

Disadvantages:

* possible retrieval noise
* embedding dependence

---

## Strategy C — Hybrid Retrieval

Combine:

* keyword retrieval
* vector retrieval

Merge results and rank retrieved documents.

Advantages:

* combines precision and recall
* reduces single-method weaknesses

Disadvantages:

* increased complexity

---

# Calibration Goal

Determine whether hybrid retrieval improves:

* retrieval relevance
* retrieval usefulness
* downstream detection quality
* downstream repair quality

compared to keyword-only retrieval.

---

# Planned Outcome

Select a final retrieval strategy before architecture freeze.
