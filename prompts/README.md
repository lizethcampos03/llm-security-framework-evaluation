# Prompt Templates

This directory contains the prompt templates used throughout the experimental artifact accompanying the paper:

> **A LangGraph-Orchestrated Framework for Secure Analysis and Repair of LLM-Generated Code**

The prompts support both benchmark preparation and execution of the experimental workflow.

Separating prompts from the implementation improves transparency, simplifies maintenance, and allows the evaluation methodology to be inspected independently of the experiment scripts.

---

# Directory Structure

```
prompts/

├── chain_reasoning_prompt.md
├── chain_repair_prompt.md
├── detector_prompt.md
├── repair_prompt.md
└── secure_counterpart_generation_prompt.md
```

Each prompt serves a specific role within the methodology.

---

# Prompt Overview

## detector_prompt.md

Defines the instructions used during vulnerability detection.

This prompt guides the language model in identifying potential software vulnerabilities and producing structured security findings used throughout the evaluation.

Used in:

- Workflow Calibration
- Experiment 1 – Detection and Comparative Analysis
- Experiment 2 – End-to-End Secure Remediation
- Experiment 3 – Chained-Vulnerability Evaluation

---

## repair_prompt.md

Defines the instructions used to generate secure code repairs after vulnerabilities have been identified.

The generated repairs are evaluated as part of the end-to-end remediation workflow.

Used in:

- Workflow Calibration
- Experiment 2 – End-to-End Secure Remediation

---

## chain_reasoning_prompt.md

Defines the reasoning process used to analyze relationships among multiple validated vulnerabilities.

The prompt supports preliminary attack-path reasoning across multiple software components.

Used in:

- Experiment 3 – Chained-Vulnerability Evaluation

---

## chain_repair_prompt.md

Defines the instructions used to generate coordinated repair recommendations for chained vulnerabilities.

Rather than repairing vulnerabilities independently, this prompt generates repair plans that consider interactions across multiple components.

Used in:

- Experiment 3 – Chained-Vulnerability Evaluation

---

## secure_counterpart_generation_prompt.md

Defines the prompt used during benchmark preparation to generate secure counterparts for the vulnerable SecurityEval samples.

The secure counterparts were generated through an automated prompt-based procedure using GPT-5.5 prior to experimentation.

This prompt was used exclusively during dataset preparation and was **not** used during the reported experimental evaluation.

Its inclusion in this repository supports transparency and reproducibility of the benchmark construction process.

---

# Prompt Interfaces Within the Workflow

The table below summarizes the responsibility of each prompt within the methodology.

| Prompt | Primary Input | Primary Output |
|---------|---------------|----------------|
| **detector_prompt.md** | Source code and supporting context | Structured vulnerability findings |
| **repair_prompt.md** | Source code and validated vulnerability findings | Secure code repair and remediation output |
| **chain_reasoning_prompt.md** | Validated findings from multiple software components | Candidate chained-vulnerability analysis and attack-path reasoning |
| **chain_repair_prompt.md** | Confirmed vulnerability chain and associated findings | Coordinated repair strategy for the complete attack chain |
| **secure_counterpart_generation_prompt.md** | Vulnerable SecurityEval benchmark sample | Secure counterpart used during benchmark construction |

This modular organization allows each prompt to perform a single well-defined task while maintaining clear interfaces between workflow stages.

---

# Relationship to the Experimental Workflow

The prompts correspond to different stages of the methodology.

```
Dataset Preparation

    secure_counterpart_generation_prompt.md

                │
                ▼

Experimental Evaluation

    detector_prompt.md
            │
            ▼
    repair_prompt.md

                │

Experiment 3 Extension

    chain_reasoning_prompt.md
            │
            ▼
    chain_repair_prompt.md
```

This organization reflects the progression of the proposed methodology from benchmark construction to vulnerability detection, secure remediation, and preliminary chained-vulnerability reasoning.

---

# Prompt Design Philosophy

Each prompt was designed to perform a single, well-defined task within the workflow.

By separating prompt templates from the implementation, the repository promotes modularity, transparency, and reproducibility. Individual prompts may be refined or replaced without requiring changes to the surrounding experimental pipeline, provided that their expected inputs and outputs remain consistent.

This design also mirrors the node-based organization of the LangGraph workflow presented in the accompanying paper, where each prompt corresponds to a distinct stage of the overall methodology.

---

# Reproducibility

The prompt templates included in this directory correspond to those used during the reported evaluation.

Providing the prompts separately from the implementation enables researchers to inspect, reproduce, and extend the methodology while preserving a clear separation between prompt engineering and workflow logic.

The prompt used to generate the secure benchmark counterparts is also included to document the benchmark construction process and improve transparency of the experimental artifact.

---

# Summary

The prompts contained in this directory document the language-model interactions that support both benchmark construction and experimental evaluation.

Together, they provide the prompt-level methodology underlying:

- benchmark preparation
- vulnerability detection
- secure code remediation
- preliminary chained-vulnerability reasoning

while clearly documenting the responsibility, inputs, and outputs of each prompt within the overall workflow.