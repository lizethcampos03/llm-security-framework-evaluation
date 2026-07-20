# Runtime and Cost Report

## Purpose

This document describes how the runtime and API cost metrics reported in
`results/paper_results/tables/runtime_cost_summary.csv` were obtained.

---

## Runtime Metrics

Runtime metrics were collected directly from the LangSmith dashboard
using the final benchmark consisting of 138 workflow executions.

The following metrics were recorded directly from the LangSmith runtime
statistics:

- P50 / P99 trace latency
- Median detection runtime
- Median repair runtime
- Median RAG runtime
- Approximate end-to-end runtime

These metrics characterize the execution performance of the frozen
LangGraph workflow and are independent of the total number of benchmark
executions.

---

## API Cost Metrics

API usage information was obtained from the Anthropic Console and the
OpenAI Platform.

Because multiple benchmark batches were executed during the same billing
period using the same provider accounts, the provider dashboards could
not isolate the final 138-case benchmark directly. Consequently, the API
costs for the final benchmark were proportionally derived from a
previously measured 370-case benchmark that used the same frozen
workflow configuration, including the same models, prompts, retrieval
strategy, and benchmark composition.

The reported cost metrics include:

- Claude Opus cost
- GPT-5.5 cost
- Combined API cost
- Estimated cost per benchmark sample

Since the workflow configuration remained unchanged, these values provide
a representative characterization of the operational cost of the final
benchmark.

---

## Cost Calculation

The previously measured 370-case benchmark reported the following API
costs:

| Metric | 370-Case Benchmark |
|--------|-------------------:|
| Claude Opus cost | $97.75 |
| GPT-5.5 cost | $15.21 |
| Combined cost | $112.96 |
| Cost per sample | $0.31 |

The proportional scaling factor used to derive the 138-case benchmark
costs was:

```
Scaling Factor = 138 / 370 = 0.37297
```

The final benchmark costs were calculated as follows:

```
Claude Opus
$97.75 × (138 / 370)
= $36.46

GPT-5.5
$15.21 × (138 / 370)
= $5.67

Combined Cost
$112.96 × (138 / 370)
= $42.13

Cost per Sample
$42.13 / 138
= $0.305 ≈ $0.31
```

---

## Data Sources

- LangSmith (runtime statistics)
- Anthropic Console (Claude Opus usage)
- OpenAI Platform (GPT-5.5 usage)

---

## Notes

This report documents the methodology used to reproduce the runtime and
cost characterization for the final benchmark. Runtime metrics were
measured directly from LangSmith, while API costs were proportionally
derived from the previously measured 370-case benchmark because the
provider billing dashboards aggregated multiple benchmark executions
performed during the same billing period, preventing direct isolation of
the final 138-case batch.

Future reproductions using a dedicated provider project or isolated billing period can replace the proportionally derived cost values with directly measured benchmark costs without changing the reported methodology.