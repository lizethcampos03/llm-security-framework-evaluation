# Context Profile + RAG Calibration

## Purpose

This calibration stage evaluates how security context profiles and retrieval strategies influence workflow behavior.

The goal is to improve the quality of retrieved CWE and security guidance used by downstream workflow stages.

This calibration focuses on:

- context profile design
- retrieval quality
- hybrid retrieval
- retrieval ranking
- retrieval consistency
- retrieval usefulness
- downstream workflow usefulness

The retrieval system is calibrated based on whether retrieved context improves downstream detection and repair quality, not only retrieval similarity scores.

---

## Main Hypothesis

```text
Better context profiles
+
better retrieval strategies
+
higher-quality CWE/security guidance
improve downstream detection and repair quality.
Calibration Areas
Context Profile Design

Evaluates which context fields improve retrieval and downstream workflow quality.

Hybrid Retrieval

Evaluates retrieval approaches that combine:

semantic retrieval
keyword retrieval
metadata-aware retrieval
CWE-aware retrieval
Retrieval Quality

Evaluates whether retrieved guidance is relevant, useful, and context-aware.

Retrieval Noise Reduction

Evaluates methods for reducing unrelated or low-quality retrieval results.

Workflow Impact

Evaluates whether improved retrieval improves:

vulnerability detection
secure repair
report usefulness
workflow consistency
Related Documents
hybrid_search_plan.md
retrieval_quality_metrics.md
context_profile_design.md
