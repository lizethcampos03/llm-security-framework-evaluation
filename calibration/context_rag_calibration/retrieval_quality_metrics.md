# Retrieval Quality Metrics

## Purpose

This document defines the measurements used during Context + RAG Calibration.

---

# Retrieval Metrics

## Retrieval Accuracy

Did the retrieval return the expected CWE guidance?

Values:

* correct
* partially_correct
* incorrect

---

## Retrieval Ranking Quality

Was the most relevant guidance ranked near the top?

Values:

* high
* medium
* low

---

## Retrieval Consistency

Did repeated retrievals produce similar results?

Values:

* consistent
* moderately_consistent
* inconsistent

---

## Retrieval Usefulness

Did retrieved information help downstream reasoning?

Values:

1–5

1 = not useful

5 = highly useful

---

## Detection Usefulness

Did retrieval improve vulnerability detection?

Values:

1–5

---

## Repair Usefulness

Did retrieval improve repair quality?

Values:

1–5

---

# Decision Criteria

A retrieval strategy will be preferred if it:

* improves retrieval usefulness
* improves detection usefulness
* improves repair usefulness
* maintains acceptable consistency
* avoids excessive retrieval noise
