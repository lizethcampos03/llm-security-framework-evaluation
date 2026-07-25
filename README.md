# LangGraph Workflow Evaluation

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lizethcampos03/llm-security-framework-evaluation/blob/main/notebooks/paper_reproduction.ipynb)

Official experimental artifact accompanying the research paper:

> **A LangGraph-Orchestrated Framework for Secure Analysis and Repair of LLM-Generated Code**

**Authors**

- Lizeth Campos Velazquez
- Bikash Chandra Singh

Department of Computer Science  
California State University, Fresno

---

# Overview

This repository contains the official experimental artifact accompanying the paper *A LangGraph-Orchestrated Framework for Secure Analysis and Repair of LLM-Generated Code*.

The proposed framework investigates how retrieval-enhanced workflow orchestration can improve the secure software lifecycle by combining contextual vulnerability analysis, hybrid retrieval over security knowledge, specialized large language model (LLM) roles, structured remediation guidance, and preliminary chained-vulnerability reasoning within a unified LangGraph workflow.

This repository is intended to facilitate **reproducibility** of the reported experimental evaluation. It provides the datasets, prompts, experiment scripts, configurations, notebooks, and archived outputs necessary to reproduce the results presented in the paper.

---

# Repository Scope

This repository contains the **experimental evaluation artifact** only.

Included:

- Experimental methodology
- Reproduction notebook
- Experiment scripts
- Calibration configuration
- Evaluation datasets
- Prompt templates
- Configuration files
- Reported experimental outputs
- Figures and tables generated for the paper

---

# Repository Structure

```text
langgraph-workflow-evaluation/

├── notebooks/
│   └── paper_reproduction.ipynb
│
├── experiments/
│
├── datasets/
│
├── prompts/
│
├── configs/
│
└── results/
```

---

# Experimental Evaluation

The experimental evaluation follows the same structure presented in the paper.

## Workflow Calibration

Calibration was performed before large-scale evaluation to determine the final architecture used throughout the experiments.

The calibration process evaluated:

- retrieval strategy
- prompt design
- detector model selection
- workflow structure
- repair strategy

The resulting configuration was frozen before the primary benchmark evaluation.

---

## Experiment 1 — Detection and Comparative Analysis

Evaluates vulnerability detection performance across a balanced benchmark derived from SecurityEval.

Performance is compared against:

- CodeQL
- Bandit
- GPT-4 End-to-End Workflow baseline (EASE 2025)

Reported metrics include:

- Accuracy
- Precision
- Recall
- F1 Score
- Vulnerability coverage

---

## Experiment 2 — End-to-End Secure Remediation

Evaluates the complete secure-code workflow after vulnerability detection.

This experiment measures:

- repair success
- final secure-output rate
- end-to-end workflow effectiveness

---

## Experiment 3 — Chained-Vulnerability Evaluation

Provides a preliminary evaluation of multi-component attack-path reasoning.

The framework evaluates:

- component-level vulnerability detection
- candidate-chain identification
- evidence-supported chain confirmation
- repair-plan generation

---

# Reproducing the Paper

The easiest way to reproduce the experimental evaluation is through the accompanying Google Colab notebook.

Click the **Open in Colab** badge at the top of this page.

The notebook reproduces the experiments in the same order presented in the manuscript:

1. Workflow Calibration
2. Experiment 1 – Detection and Comparative Analysis
3. Experiment 2 – End-to-End Secure Remediation
4. Experiment 3 – Chained-Vulnerability Evaluation
5. Generation of tables and figures

---

# Citation

If you use this repository in academic work, please cite the accompanying paper.

A GitHub-compatible citation is also provided through the included `CITATION.cff` file.

---

# Acknowledgment

This repository accompanies the research paper:

> **A LangGraph-Orchestrated Framework for Secure Analysis and Repair of LLM-Generated Code**

developed in the Department of Computer Science at California State University, Fresno.

The repository is intended solely to support transparency and reproducibility of the experimental evaluation presented in the manuscript.
