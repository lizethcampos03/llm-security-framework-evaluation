# Datasets

This directory contains the datasets used throughout the experimental evaluation accompanying the paper:

> **A LangGraph-Orchestrated Framework for Secure Analysis and Repair of LLM-Generated Code**

The datasets support workflow calibration, vulnerability detection, secure remediation, and preliminary chained-vulnerability reasoning.

All datasets were finalized prior to experimentation and remained unchanged throughout the reported evaluation to ensure consistency and reproducibility.

---

# Directory Structure

```
datasets/

├── securityeval/
└── chains/
```

Each dataset serves a distinct purpose within the experimental evaluation and reflects a different stage of the proposed methodology.

---

# SecurityEval Benchmark Dataset

The primary benchmark used throughout the evaluation is derived from the **SecurityEval** dataset.

The benchmark consists of representative software samples covering multiple Common Weakness Enumeration (CWE) categories.

SecurityEval provides the vulnerable benchmark samples used throughout the evaluation.

To create a balanced benchmark for vulnerability detection, a corresponding secure counterpart was generated for each vulnerable sample through an automated prompt-based procedure using **GPT-5.5**.

The prompt template used during benchmark preparation is provided in:

```
prompts/
    secure_counterpart_generation_prompt.md
```

This benchmark preparation process was completed before the experimental evaluation began, and the resulting benchmark remained fixed throughout all reported experiments.

The SecurityEval benchmark dataset is used in:

- Workflow Calibration
- Experiment 1 – Detection and Comparative Analysis
- Experiment 2 – End-to-End Secure Remediation

---

# Chained-Vulnerability Dataset

The **chains** dataset supports the preliminary chained-vulnerability evaluation introduced in this work.

Rather than introducing an entirely separate benchmark, the chained-vulnerability dataset was constructed by combining representative SecurityEval benchmark samples into curated multi-component attack scenarios.

Each scenario contains multiple software components representing different stages of a representative attack path, enabling evaluation of reasoning across interacting vulnerabilities rather than isolated code samples.

This dataset is used exclusively for:

- Experiment 3 – Chained-Vulnerability Evaluation

---

# Benchmark Construction Workflow

The overall dataset preparation process is summarized below.

```
SecurityEval Vulnerable Samples
                │
                ▼
Automated Secure Counterpart Generation
          (GPT-5.5 Prompt)
                │
                ▼
Balanced Evaluation Benchmark
                │
        Frozen Prior to Evaluation
                │
      ┌─────────┴─────────┐
      ▼                   ▼
Experiments 1 & 2     Representative Sample Selection
                              │
                              ▼
               Curated Multi-Component Attack Scenarios
                              │
                              ▼
                     Experiment 3 Dataset
```

This preparation workflow ensures that all experiments operate on a fixed benchmark, preventing changes to the datasets during evaluation.

---

# Relationship to the Experiments

| Experimental Stage | Dataset |
|--------------------|---------|
| Workflow Calibration | SecurityEval Benchmark |
| Experiment 1 – Detection and Comparative Analysis | SecurityEval Benchmark |
| Experiment 2 – End-to-End Secure Remediation | SecurityEval Benchmark |
| Experiment 3 – Chained-Vulnerability Evaluation | Chains Dataset |

---

# Reproducibility

The datasets included in this repository correspond to those used during the reported experimental evaluation.

Researchers reproducing the experiments should use these datasets without modification to obtain results comparable to those reported in the accompanying paper.

The prompt used to generate the secure counterparts is included in the `prompts/` directory to support transparency and reproducibility of the benchmark preparation process.

---

# External Resources

This repository contains the experimental artifacts necessary to reproduce the evaluation reported in the accompanying paper.

External datasets and software tools referenced throughout the evaluation remain subject to their respective licenses and terms of use.

---

# Summary

The datasets contained in this directory provide the experimental foundation for the reported evaluation.

Together, they support reproducible assessment of:

- workflow calibration
- vulnerability detection
- secure remediation
- preliminary chained-vulnerability reasoning

while maintaining a clear distinction between the benchmark dataset used for evaluation and the derived dataset introduced to explore chained-vulnerability reasoning.