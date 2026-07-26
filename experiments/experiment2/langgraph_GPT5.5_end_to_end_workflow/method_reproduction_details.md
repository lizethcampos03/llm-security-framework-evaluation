# Method Reproduction Details – LangGraph GPT-5.5 End-to-End Workflow

## Purpose

This document specifies the implementation details used to reproduce the **LangGraph GPT-5.5 End-to-End Workflow**. The method reproduces the end-to-end secure remediation workflow while replacing the original vulnerability detection stage with the proposed LangGraph security workflow and replacing the repair model with GPT-5.5. The workflow preserves the overall evaluation methodology, benchmark composition, and repair-validation process to enable a controlled comparison between repair models.

## Architecture Diagram

A visual representation of the LangGraph End-to-End Workflow is provided in:

`figures/langgraph_end_to_end_workflow.png`

## Original Method

The reproduced workflow follows the same high-level pipeline as the original End-to-End Workflow:

- RQ1: Code Generation
- RQ2: Vulnerability Detection
- RQ3: Vulnerability Repair

This reproduction omits code generation because the SecurityEval benchmark is already provided in the repository.

## Reproduction Scope

The reproduction introduces four controlled modifications:

### Modification 1 — Evaluation Dataset

Use the predefined SecurityEval benchmark consisting of 69 vulnerable samples and 69 verified safe counterparts instead of regenerating benchmark programs.

### Modification 2 — LangGraph Vulnerability Detection

Replace the original single-LLM detector with the proposed LangGraph security workflow, including RAG-based knowledge retrieval, structured reasoning, validation, and generation of a LangGraph Security Report.

### Modification 3 — GPT-5.5 Repair

Replace the original repair model with GPT-5.5 while preserving the single-pass repair protocol.

### Modification 4 — Structured Repair Prompt

Use the redesigned LangGraph repair prompt that consumes the LangGraph Security Report as structured repair guidance.

# Experimental Workflow

## Stage 1 — Benchmark Input

For each benchmark sample:

- Load vulnerable source code.
- Load the target CWE.
- Load the corresponding CWE definition.

## Stage 2 — LangGraph Vulnerability Detection

For each benchmark sample:

- Execute the LangGraph workflow.
- Retrieve relevant security knowledge through RAG.
- Perform structured vulnerability reasoning.
- Validate predicted findings.
- Produce the LangGraph Security Report.

## Stage 3 — GPT-5.5 Repair

For each detected vulnerable sample:

- Provide vulnerable source code.
- Provide the LangGraph Security Report.
- Execute GPT-5.5 using the LangGraph repair prompt.
- Generate one repaired implementation.

## Stage 4 — Repair Evaluation

Evaluate each repaired program using:

- Syntax validation
- Bandit
- CodeQL
- Author manual review when required

A repair is considered successful only when the finalized evaluation status is **SECURE**.

# Language Models

| Stage | Model |
|-------|-------|
| Vulnerability Detection | LangGraph Workflow |
| Vulnerability Repair | GPT-5.5 |

# Prompts

## Vulnerability Detection

Performed entirely by the LangGraph workflow.

## Vulnerability Repair

The dedicated LangGraph GPT-5.5 repair prompt is used.

# Model Configuration

- LangGraph workflow for vulnerability detection
- GPT-5.5 for vulnerability repair
- Single-pass repair
- One execution per benchmark sample
- Independent execution for every sample
- Final repair decisions validated using syntax validation, Bandit, CodeQL, and author manual review

# Evaluation Metrics

## Detection (reported from the detection experiment)

- Accuracy
- Precision
- Recall
- F1 Score
- Detection Coverage

## Repair

- Repair Success Rate
- Evaluated Repair Success Rate
- Final Secure Output Rate
- Repair Attempt Coverage
- CWE Repair Coverage

# Notes

The only methodological changes relative to the reproduced End-to-End Workflow baseline are replacement of the vulnerability detector with the LangGraph workflow, replacement of the repair model with GPT-5.5, redesign of the repair prompt, and use of the LangGraph Security Report as the structured repair input. The benchmark, evaluation methodology, and final repair decision criteria remain unchanged to support controlled comparison across repair-model configurations.
