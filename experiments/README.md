# Experimental Evaluation

This directory contains the complete experimental evaluation accompanying the paper:

> **A LangGraph-Orchestrated Framework for Secure Analysis and Repair of LLM-Generated Code**

The experiments implemented here reproduce the evaluation presented in the manuscript, including workflow calibration, vulnerability detection, end-to-end remediation, and preliminary chained-vulnerability reasoning.

Each experiment corresponds directly to a section of the paper, enabling reviewers and researchers to reproduce the reported results in a structured and transparent manner.

---

# Experimental Organization

The evaluation consists of four stages:

1. Workflow Calibration
2. Experiment 1 – Detection and Comparative Analysis
3. Experiment 2 – End-to-End Secure Remediation
4. Experiment 3 – Chained-Vulnerability Evaluation

The workflow calibration establishes the final architecture used throughout the remaining experiments.

---

# Directory Contents

```
experiments/

├── workflow_calibration.py
├── experiment1_detection_and_comparative_analysis.py
├── experiment2_end_to_end_secure_remediation.py
├── experiment3_chained_vulnerability_evaluation.py
└── methodology.md
```

---

# Workflow Calibration

The calibration stage evaluates multiple architectural design choices before freezing the final workflow used in the primary evaluation.

Calibration includes:

- retrieval strategy
- prompt refinement
- detector model selection
- workflow structure
- repair strategy

The resulting configuration is fixed before running the benchmark experiments.

---

# Experiment 1
## Detection and Comparative Analysis

Evaluates vulnerability detection performance across a balanced benchmark derived from SecurityEval.

Primary evaluation metrics include:

- Accuracy
- Precision
- Recall
- F1 Score
- False Positives
- False Negatives
- Vulnerability Coverage

The framework is compared against:

- CodeQL
- Bandit
- GPT-4 secure-code-agent baseline (EASE 2025)

---

# Experiment 2
## End-to-End Secure Remediation

Evaluates the complete secure-code workflow after successful vulnerability detection.

Primary metrics include:

- Repair Success Rate
- Final Secure-Output Rate

This experiment measures the effectiveness of the generated structured security report for supporting downstream remediation.

---

# Experiment 3
## Chained-Vulnerability Evaluation

Provides a preliminary evaluation of reasoning across multiple interacting vulnerabilities.

The evaluation measures:

- component-level detection
- candidate-chain identification
- evidence-supported chain confirmation
- repair-plan generation

The experiment is intended as an exploratory assessment of attack-path reasoning rather than a comprehensive attack-graph evaluation.

---

# Experimental Methodology

A detailed description of the complete experimental methodology is provided in:

```
methodology.md
```

This document describes:

- datasets
- evaluation procedure
- manual validation
- benchmark preparation
- metric computation
- reproducibility considerations

---

# Reproducing the Evaluation

The experiments may be executed individually or through the repository's primary reproduction notebook.

Execution order:

1. Workflow Calibration
2. Detection and Comparative Analysis
3. End-to-End Secure Remediation
4. Chained-Vulnerability Evaluation

Following this order reproduces the evaluation pipeline described in the accompanying paper.

---

# Reproducibility Statement

These experiments are provided to support transparency and reproducibility of the published evaluation.

The experimental artifact reproduces the reported results while remaining separate from the complete research prototype used during development.