# Experimental Methodology

## Purpose

This document describes the common experimental methodology used throughout the evaluation of the proposed LangGraph Security Framework.

Rather than documenting the results of individual experiments, this document defines the shared evaluation procedures, benchmark configuration, fairness policy, validation process, and metric definitions used across the calibration phase and all reported experiments.

Individual experiment logs reference this methodology while documenting experiment-specific objectives and results.

---

# Experimental Overview

The experimental evaluation was conducted in four stages:

1. Calibration
2. Experiment 1 — Vulnerability Detection and Comparative Evaluation
3. Experiment 2 — End-to-End Secure Remediation Evaluation
4. Experiment 3 — Chained-Vulnerability Evaluation

Each stage evaluates a different aspect of the proposed framework while using the same frozen workflow configuration established during calibration.

---

# Frozen Experimental Configuration

Following calibration, the workflow configuration was frozen and remained unchanged throughout all reported experiments.

The finalized workflow consisted of:

```text
Input
    ↓
Preprocessing
    ↓
Full Hybrid Evidence Retrieval
    ↓
Claude Opus Detection
    ↓
Conditional GPT-5.5 Repair
    ↓
Structured Security Report
```

The chained-vulnerability evaluation extended this workflow with an optional reasoning branch for multi-component inputs while preserving the primary architecture.

---

# Benchmark Configuration

The primary benchmark was derived from the SecurityEval dataset.

One representative vulnerable implementation was selected for each CWE family, and a verified safe counterpart was created for every vulnerable sample.

| Dataset Component | Count |
|-------------------|------:|
| CWE Families | 69 |
| Vulnerable Samples | 69 |
| Verified Safe Counterparts | 69 |
| Total Detection Cases | 138 |

Calibration used a smaller benchmark consisting of one vulnerable and one safe sample from nine representative CWE families.

---

# Experimental Platform

The experiments used cloud-hosted language models together with locally executed security analysis tools.

| Component | Configuration |
|-----------|---------------|
| Detection Model | Claude Opus |
| Repair Model | GPT-5.5* |
| Workflow | LangGraph |
| Static Analysis | CodeQL, Bandit |
| LLM Analysis (comparison method) | EASE 2025 End-to-End Workflow |
| Knowledge Sources | CWE knowledge, security code examples |
| Retrieval Strategy | Full Hybrid Evidence Reranker |

---

# Evaluation Procedure

Each benchmark case followed the same evaluation pipeline.

1. Load the benchmark sample.
2. Construct the workflow input using the source code and context profile.
3. Execute the frozen LangGraph workflow.
4. Record the detector output and generated security report.
5. Compute evaluation metrics after execution.
6. Perform manual review when required.
7. Aggregate results for experiment-level analysis.

All benchmark cases were processed using the same workflow configuration.

---

# Fairness Policy

To preserve experimental fairness, benchmark labels and expected CWE assignments were withheld from the LangGraph workflow during execution.

Ground-truth information was used only after inference for metric computation.

Similarly, comparison tools were evaluated using consistent benchmark inputs and standardized evaluation procedures whenever possible.

---

# Manual Review Methodology

Manual review complemented automated analysis throughout the evaluation.

Manual review was performed to:

- verify vulnerability classifications,
- evaluate disagreements between automated tools,
- assess generated repairs,
- confirm chained-vulnerability reasoning,
- distinguish conservative scanner warnings from persistent vulnerabilities.

Review decisions considered:

- benchmark labels,
- CWE definitions,
- source-code behavior,
- retrieved security evidence,
- generated reasoning,
- repair correctness.

---

# Evaluation Metrics

Depending on the experiment, the following metrics were reported.

## Detection Metrics

- Overall Accuracy
- Precision
- Recall
- F1 Score
- Safe Classification Accuracy

## Classification Metrics

- True Positives
- True Negatives
- False Positives
- False Negatives

## Repair Metrics

- Repair Success Rate
- Final Secure-Output Rate
- Repair Iterations

## Chain Reasoning Metrics

- Candidate Chains Identified
- Confirmed Attack Paths
- CAPEC/CWE Evidence Utilization
- Chain Repair Success

Operational metrics such as runtime and cost are documented separately because they characterize the execution of the finalized workflow rather than the outcome of an individual experiment.

---

# Experiment Relationships

The experiments build upon one another.

| Stage | Purpose |
|--------|---------|
| Calibration | Finalize and freeze the workflow configuration. |
| Experiment 1 | Evaluate vulnerability detection and compare against existing approaches. |
| Experiment 2 | Evaluate repair performance within an End-to-End Workflow using the structured LangGraph security report. |
| Experiment 3 | Evaluate preliminary chained-vulnerability reasoning across representative multi-component scenarios. |

Each experiment reused the finalized workflow produced during calibration.

---

# Runtime and Cost Characterization

Runtime and cost measurements were collected after completion of the experimental evaluation to characterize the operational requirements of the finalized workflow.

Execution metadata was obtained from the workflow execution platform together with usage information reported by the language-model providers. Aggregate statistics were then computed from these execution traces to summarize latency and operational cost for the finalized architecture.

These measurements describe the computational characteristics of the workflow and are reported independently from the experimental outcome metrics.

---

# Reproducibility

The evaluation repository contains the datasets, prompts, workflow configuration, experiment logs, calibration artifacts, and output reports necessary to reproduce the reported experiments.

All experiments were executed using the same frozen architecture established during calibration, ensuring that reported differences reflect the experimental objectives rather than changes to the workflow configuration.