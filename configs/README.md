# Configuration Files

## Purpose

This directory documents the **frozen experimental configuration** used to evaluate the LangGraph Security Framework presented in the accompanying paper.

The configuration described in these documents corresponds to the architecture finalized after calibration and subsequently used for all reported experiments, including vulnerability detection, comparative evaluation, secure remediation, and preliminary chained-vulnerability reasoning.

The purpose of this directory is to provide a concise reference describing how the experimental workflow was configured, allowing readers to understand and reproduce the reported evaluation without navigating the implementation code.

---

## Directory Contents

| Document | Description |
|----------|-------------|
| `workflow_configuration.md` | Documents the finalized workflow architecture, including the processing pipeline, retrieval strategy, LLM roles, prompt design philosophy, workflow optimizations, and the frozen configuration used throughout the experiments. |
| 

---

## Relationship to the Paper

This configuration document complements the paper by providing implementation-oriented details that support reproducibility.

The paper presents the methodology and experimental results, whereas this directory documents the specific configuration used to obtain those results.

---

## Frozen Experimental Configuration

All experiments in this repository were executed using the same calibrated architecture:

- Full Hybrid Evidence Reranker
- Claude Opus for vulnerability detection
- GPT-5.5 for secure repair generation
- Code-first reasoning with structured prompting
- Conditional repair generation
- Structured security reporting

This configuration was frozen after calibration and remained unchanged throughout the primary benchmark evaluation.

---

## Repository Organization

The configuration document should be read together with the remaining repository artifacts:

- `prompts/` — Prompt templates used by the workflow
- `datasets/` — Evaluation datasets and benchmark information
- `experiments/` — Experiment-specific execution scripts
- `outputs/` — Calibration reports, experiment logs, and evaluation results

Together, these artifacts provide the information necessary to understand, reproduce, and evaluate the experiments presented in the paper.