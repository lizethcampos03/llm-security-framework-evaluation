# Workflow Configuration

## Purpose

This document describes the **final frozen workflow configuration** used throughout the experimental evaluation presented in the accompanying paper.

The configuration documented here was established after the calibration phase and remained unchanged during the primary benchmark evaluation. Its purpose is to provide a concise technical specification of the evaluated architecture without requiring readers to inspect the implementation code.

---

# Frozen Workflow

The finalized LangGraph Security Framework consists of the following stages:

```text
Input
    ↓
Preprocessing
    ↓
Full Hybrid Evidence Retrieval (RAG)
    ↓
Claude Opus Vulnerability Detection
    ↓
Vulnerability Detected?
      ├── No → Structured Security Report
      └── Yes
              ↓
      GPT-5.5 Secure Repair
              ↓
      Structured Security Report
```

The chained-vulnerability evaluation extends this workflow with an optional reasoning branch for multi-component inputs. The primary workflow remained unchanged throughout the benchmark evaluation.

---

# Workflow Components

| Stage | Purpose |
|--------|---------|
| Input | Receives the source code, context profile, and optional user security concerns. |
| Preprocessing | Normalizes the source code, prepares contextual information, and formats the analysis input. |
| Full Hybrid Evidence Retrieval | Retrieves relevant CWE knowledge and security code examples using hybrid retrieval with evidence fusion and reranking. |
| Claude Opus Detection | Determines whether the code contains security vulnerabilities using code-first reasoning supported by retrieved evidence. |
| GPT-5.5 Repair | Generates a secure implementation only when a validated vulnerability is detected. |
| Structured Report | Produces a machine-readable security report containing findings, supporting evidence, reasoning, and repair guidance. |

---

# LLM Configuration

The workflow uses specialized language models for different stages of the analysis.

| Component | Model |
|-----------|-------|
| Vulnerability Detection | Claude Opus |
| Secure Repair | GPT-5.5 |

The models were selected during calibration according to their respective strengths.

Claude Opus was chosen for vulnerability detection because of its strong code comprehension, security reasoning, and structured analytical output.

GPT-5.5 was selected for repair generation because of its code synthesis capabilities and ability to preserve intended functionality while applying targeted security fixes.

Default provider API parameters were used throughout the experiments without manual tuning.

---

# Retrieval Configuration

The workflow uses the **Full Hybrid Evidence Reranker** configuration.

The retrieval pipeline combines multiple complementary sources of evidence before presenting the final context to the detector.

### Retrieval Sources

- Code keyword retrieval
- Code vector retrieval
- CWE keyword retrieval
- CWE vector retrieval

Retrieved evidence is subsequently:

- merged,
- deduplicated,
- weighted,
- reranked,

before being supplied to the detector.

This configuration was selected during calibration because it consistently produced stronger contextual evidence than either keyword-only or vector-only retrieval.

---

# Prompt Design Philosophy

Rather than relying on prompt length, the workflow emphasizes several guiding principles established during calibration.

## Code-First Reasoning

The detector treats the source code as the primary source of truth.

Retrieved evidence supports the analysis but is not considered proof of a vulnerability by itself.

---

## Safe Counterpart Reasoning

Whenever possible, the detector compares vulnerable patterns against retrieved secure examples before making a final classification.

---

## Evidence-Guided Decisions

Vulnerabilities are reported only when the observed code behavior is supported by both the implementation and the retrieved security evidence.

---

## Structured Output

The detector produces structured JSON outputs containing vulnerability classification, supporting evidence, confidence, reasoning, and remediation guidance.

---

# Workflow Optimizations

Calibration resulted in several architectural improvements that became part of the frozen workflow.

| Optimization | Final Decision |
|-------------|----------------|
| Retrieval Strategy | Full Hybrid Evidence Reranker |
| Detector Model | Claude Opus |
| Validation Node | Removed |
| Repair Generation | Conditional |
| Output Format | Structured JSON Report |

The validation node was removed because calibration demonstrated that repeated detector execution substantially increased runtime while providing minimal measurable improvement in detection quality.

Repair generation became conditional so that only vulnerable samples proceed to remediation, reducing unnecessary latency and computational cost.

---

# Final Frozen Configuration

The experimental results reported in the accompanying paper were produced using the following configuration.

| Component | Configuration |
|-----------|---------------|
| Workflow | LangGraph Security Framework |
| Retrieval | Full Hybrid Evidence Reranker |
| Detection Model | Claude Opus |
| Repair Model | GPT-5.5 |
| Prompt Philosophy | Code-first reasoning with secure-counterpart comparison |
| Validation | Removed |
| Repair Strategy | Conditional repair generation |
| Output | Structured security report |

No architectural modifications were introduced after calibration. This configuration remained fixed throughout the primary benchmark evaluation to ensure consistent and reproducible experimental results.

---

# Relationship to the Repository

This document specifies **what** configuration was evaluated.

Additional repository artifacts provide complementary information:

- `prompts/` contains the prompt templates.
- `datasets/` documents the benchmark datasets.
- `experiments/` contains experiment-specific execution procedures.
- `outputs/` contains calibration reports, experiment logs, and evaluation results.

Together, these resources fully describe the evaluated workflow while keeping configuration, experimentation, and results logically separated.