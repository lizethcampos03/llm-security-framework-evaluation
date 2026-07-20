# Workflow Configuration

## Purpose

This document describes the final workflow configuration evaluated in the
accompanying paper.

The primary LangGraph Security Framework was established after calibration
and remained frozen during the detection, comparative, and remediation
evaluations. A separate optional chained-vulnerability branch was added for
the preliminary multi-component attack-path evaluation.

This document provides a concise technical specification of both:

1. the frozen primary workflow; and
2. the experimental chained-vulnerability analysis extension.

It does not require readers to inspect the private implementation code.

---

# 1. Frozen Primary Workflow

The finalized primary LangGraph Security Framework consists of the following
stages:

```text
Input
    ↓
Preprocessing
    ↓
Full Hybrid Evidence Retrieval
    ↓
Claude Opus Vulnerability Detection
    ↓
Vulnerability Detected?
      ├── No → Structured Security Report
      └── Yes
              ↓
      Conditional Secure Repair
              ↓
      Structured Security Report
```

The primary workflow was used for:

- workflow calibration;
- the 138-case detection benchmark;
- comparison with GPT-4, CodeQL, and Bandit; and
- end-to-end remediation analysis.

The chained-vulnerability evaluation did not replace this architecture.
Instead, it extended the workflow through an optional reasoning branch for
multi-component inputs.

---

# 2. Primary Workflow Components

| Stage | Purpose |
|---|---|
| Input | Receives source code, a context profile, and optional user-supplied security concerns. |
| Preprocessing | Normalizes the source code, prepares contextual information, and formats the analysis input. |
| Full Hybrid Evidence Retrieval | Retrieves relevant CWE knowledge, vulnerable examples, safe counterparts, and mitigation evidence through hybrid keyword and vector retrieval. |
| Claude Opus Detection | Determines whether the code contains a security weakness using code-first reasoning supported by retrieved evidence. |
| Conditional Repair | Generates a secure implementation only when a vulnerability is detected and the workflow is operating in repair mode. |
| Structured Report | Produces a machine-readable security report containing findings, evidence, reasoning, CWE mappings, confidence information, and remediation guidance. |

---

# 3. Model Configuration

The workflow uses specialized language models for different tasks.

| Component | Configured Model |
|---|---|
| Vulnerability Detection | Claude Opus |
| Primary Secure-Repair Configuration | GPT-5.5 |
| Chained-Vulnerability Reasoning | Claude Opus |
| Chain Repair Planning | GPT-5.5 |

Claude Opus was selected for vulnerability detection and reasoning because the task
requires reasoning about code behavior, attack surfaces, application
context, and security implications.

GPT-5.5 was selected as the configured repair model because the repair task
requires code synthesis, instruction following, and
functionality-preserving modification.

Default provider API parameters were used without manual tuning of
temperature, top-p, or other generation settings.

## Comparative Remediation Control

The comparative end-to-end remediation experiment used GPT-4-0613 as the
repair model for both the published GPT-4 baseline and the proposed
workflow.

This controlled comparison isolated the effect of the structured LangGraph
security report. Therefore, the reported improvement in remediation could
not be attributed to using a stronger repair model.

The GPT-4-0613 experiment-specific control should not be confused with the
framework's configured GPT-5.5 repair stage.

---

# 4. Retrieval Configuration

The primary workflow uses the **Full Hybrid Evidence Reranker** configuration.

The retrieval pipeline combines multiple complementary sources of evidence.

## Retrieval Channels

- code keyword retrieval;
- code vector retrieval;
- CWE keyword retrieval;
- CWE vector retrieval.

Retrieved evidence is subsequently:

- merged;
- deduplicated;
- weighted;
- reranked.

The resulting evidence package is supplied to the vulnerability detector.

This configuration was selected during calibration because it produced
stronger contextual evidence than keyword-only or vector-only retrieval.

---

# 5. Prompt Design Philosophy

The workflow emphasizes evidence quality and disciplined reasoning rather
than prompt length alone.

## Code-First Reasoning

Source code is treated as the primary source of truth.

Retrieved evidence supports the analysis but is not considered proof of a
vulnerability by itself.

## Context-Aware Analysis

Context profiles describe intended behavior, deployment assumptions, trust
boundaries, authentication expectations, and other information that may
affect whether observed code behavior is security relevant.

## Safe-Counterpart Reasoning

When applicable, the detector compares potentially vulnerable behavior with
retrieved secure examples before issuing its final classification.

## Evidence-Guided Decisions

A vulnerability should be reported only when the observed implementation
and the retrieved security evidence jointly support the finding.

## Structured Output

The detector produces structured outputs containing:

- vulnerability classification;
- associated CWE information;
- code evidence;
- retrieved evidence;
- confidence;
- reasoning;
- remediation guidance.

---

# 6. Workflow Optimizations

Calibration produced several architectural decisions that became part of
the frozen primary workflow.

| Optimization | Final Decision |
|---|---|
| Retrieval Strategy | Full Hybrid Evidence Reranker |
| Detector Model | Claude Opus |
| Validation Node | Removed |
| Repair Generation | Conditional |
| Output Format | Structured security report |

The dedicated validation node was removed because repeated detector
execution substantially increased latency without producing measurable
improvement in detection quality.

Repair generation became conditional so that safe samples did not incur
unnecessary repair-model calls, reducing latency and API cost.

---

# 7. Chained-Vulnerability Analysis Extension

## Purpose

The chained-vulnerability extension provides a preliminary mechanism for
reasoning about relationships among vulnerabilities detected across multiple
software components.

Its purpose is to move beyond isolated weakness classification toward:

- candidate attack-chain construction;
- evidence-supported attack-path reasoning;
- chain validation and prioritization;
- chain-aware remediation planning; and
- structured chain reporting.

The extension is experimental and was used only for the preliminary
chained-vulnerability evaluation.

## Relationship to the Primary Workflow

The extension begins after the primary framework has analyzed individual
components.

The primary workflow remains responsible for:

- component preprocessing;
- evidence retrieval;
- vulnerability detection;
- CWE-oriented findings; and
- structured component reports.

When a multi-component input contains sufficient validated findings, the
optional chain-analysis branch receives those findings together with
architectural context.

```text
Frozen Primary Workflow
        ↓
Confirmed Component Vulnerabilities
        ↓
Candidate Chain Construction
        ↓
CWE/CAPEC-Guided Attack-Path Reasoning
        ↓
Chain Validation and Prioritization
        ↓
Chain-Aware Repair Planning
        ↓
Extended Chain Report
```

## Multi-Component Inputs

The extension operates on scenarios containing multiple related component
files and supporting context describing:

- component relationships;
- data flows;
- shared resources;
- trust boundaries;
- attacker capabilities;
- deployment assumptions.

Expected CWE assignments are withheld during execution and are used only
afterward for evaluation.

## Stage 1: Confirmed Component Vulnerabilities

The branch receives independently detected component-level findings from
the primary workflow.

Each finding may include:

- affected component;
- detected vulnerability;
- code evidence;
- component context;
- CWE information;
- confidence and reasoning.

**Output:** confirmed component vulnerability findings.

## Stage 2: Candidate Chain Construction

The system searches for plausible relationships among independently
detected vulnerabilities.

Candidate relationships are informed by:

- cross-component data flow;
- trust-boundary crossings;
- shared credentials or resources;
- attacker-controlled inputs;
- preconditions and postconditions;
- escalation opportunities.

**Output:** candidate vulnerability chains.

## Stage 3: Attack-Path Reasoning

An LLM-based reasoning stage evaluates each proposed chain using component
context and retrieved CWE/CAPEC evidence.

The reasoning process considers:

- whether one vulnerability enables or strengthens another;
- required attacker capabilities;
- exploit preconditions;
- intermediate state transitions;
- likely impact;
- whether the proposed progression is supported by available evidence.

**Output:** feasibility analysis and attack-path reasoning evidence.

## Stage 4: Chain Validation and Prioritization

Candidate chains are validated according to the strength of the supporting
evidence.

Unsupported relationships are not accepted as confirmed attack paths.

Supported chains may be prioritized according to:

- likelihood;
- exploit feasibility;
- potential impact;
- criticality of affected resources;
- importance of the involved control points.

**Output:** validated and prioritized chains.

## Stage 5: Chain-Aware Repair Planning

For evidence-supported chains, the extension generates a remediation plan
designed to break the attack path.

The plan identifies:

- vulnerabilities requiring remediation;
- critical control points;
- cross-component mitigations;
- recommended validation steps;
- dependencies among repairs.

The experimental extension produces repair plans rather than automatically
applying coordinated multi-file patches.

**Output:** chain-aware remediation plan.

## Stage 6: Extended Chain Report

The final output extends the standard security report with:

- component findings;
- candidate chains;
- validated attack paths;
- CWE/CAPEC supporting evidence;
- feasibility reasoning;
- preconditions and progression;
- expected impact;
- prioritization;
- chain-aware remediation guidance.

**Output:** structured chain-aware report and summary.

---

# 8. Chained-Vulnerability Evaluation Scope

The preliminary evaluation included four representative multi-component
scenarios.

The framework reported:

- component-level vulnerability detection in four of four scenarios;
- candidate-chain identification in four of four scenarios;
- confirmed attack paths in three of four scenarios; and
- repair plans in three of four scenarios.

The Code Injection–Sensitive Operation scenario remained unconfirmed because
the available evidence did not support a complete attack path.

The extension should not be interpreted as:

- a complete attack-graph construction system;
- a generalizable attack-chain accuracy benchmark;
- dynamic exploit validation;
- proof that every candidate relationship is exploitable;
- an automated multi-file patching system.

Chain confirmation represents evidence-supported reasoning under controlled
experimental conditions and was manually reviewed.

---

# 9. Architecture Figures

The repository contains separate figures for the two architectural views:

- the frozen primary workflow used for the main benchmark; and
- the optional chained-vulnerability analysis extension used for the
  preliminary attack-path experiment.

The extension figure illustrates the progression from confirmed component
vulnerabilities through chain construction, LLM-based attack-path reasoning,
chain validation, repair planning, and extended reporting.

---

# 10. Final Evaluated Configuration

## Primary Workflow

| Component | Configuration |
|---|---|
| Workflow | LangGraph Security Framework |
| Retrieval | Full Hybrid Evidence Reranker |
| Detection Model | Claude Opus |
| Configured Repair Model | GPT-5.5 |
| Prompt Philosophy | Code-first, context-aware, evidence-guided reasoning |
| Validation Node | Removed |
| Repair Strategy | Conditional repair generation |
| Primary Output | Structured security report |

## Optional Experimental Extension

| Component | Configuration |
|---|---|
| Input Type | Multi-component scenarios |
| Starting Evidence | Confirmed component vulnerability findings |
| Chain Construction | Component relationships, data flow, trust boundaries, and attacker capabilities |
| Security Knowledge | CWE and CAPEC evidence |
| Reasoning | LLM-based attack-path feasibility analysis |
| Validation | Evidence-supported chain confirmation and prioritization |
| Remediation | Chain-aware repair planning |
| Extension Output | Structured chain report and remediation plan |
| Automatic Multi-File Patching | Not performed |

No architectural modifications were introduced into the frozen primary
workflow after calibration.

The chain-analysis capability was evaluated as a separate optional branch and
did not alter the configuration used to report the primary benchmark
detection results.

---

# 11. Relationship to the Repository

This document specifies **what** workflow configuration was evaluated.

Additional repository artifacts provide complementary information:

- `prompts/` contains the archived prompt templates;
- `datasets/` contains benchmark samples, context profiles, and chain
  scenarios;
- `experiments/` contains experiment-specific execution scripts;
- `results/paper_results/experiment_logs/` contains experiment logs;
- `results/paper_results/outputs/` contains representative archived outputs;
- `results/paper_results/tables/` contains the values reported in the paper;
- `results/paper_results/figures/` contains the architecture figures.

Together, these resources document the evaluated workflow, experimental
extension, procedures, and reported results while keeping configuration,
experimentation, and outputs logically separated.