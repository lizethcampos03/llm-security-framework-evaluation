Method Reproduction Details – Secure Code Agent Baseline

Purpose

This document specifies the implementation details used to reproduce the Secure Code Agent baseline proposed in the paper called "How Well Do Large Language Models Serve as End-to-End Secure Code Agents for Python?". The objective of this reproduction is to preserve the original LLM-based vulnerability detection and repair workflow while introducing only the modifications required for the experimental evaluation performed in this repository. 

Original Method

The original study evaluates an end-to-end secure code generation pipeline through four research questions:

RQ1: Code Generation
RQ2: Vulnerability Detection
RQ3: Vulnerability Repair
RQ4: Iterative Secure Code Agent

The Secure Code Agent baseline reproduced in this repository preserves the LLM-based detection and repair methodology evaluated in RQ2 and RQ3 while adapting the evaluation protocol to the experimental design of this work.

Reproduction Scope

The reproduced baseline follows the original methodology with two controlled modifications.

Modification 1 — Evaluation Dataset

The original paper generates code using the complete SecurityEval benchmark consisting of 121 Python programming tasks spanning 69 CWEs.

For this reproduction, the code generation stage is omitted because the benchmark samples are already provided within this repository. The evaluation is therefore performed directly on the predefined SecurityEval evaluation dataset containing representative vulnerable samples for the same 69 CWEs.

Modification 2 — Single-Pass Repair

The original Secure Code Agent repeatedly repairs vulnerable code until no vulnerabilities remain or a maximum iteration limit is reached.

This reproduction performs one repair attempt for each vulnerable sample.

The iterative repair stage is intentionally omitted to maintain a consistent evaluation protocol across all compared methods, isolate the effects of architectural modifications introduced by this work, and reduce computational cost and execution time.

Experimental Workflow

The reproduced Secure Code Agent consists of the following stages.

Stage 1 — Input Dataset

For each benchmark sample:

Load the vulnerable source code.
Load the associated target CWE identifier.
Load the corresponding CWE definition.
Stage 2 — Vulnerability Detection

Following the methodology evaluated in RQ2, vulnerability detection is performed using GPT-4.

For each benchmark sample:

Provide the vulnerable code.
Provide the associated CWE identifier.
Provide the corresponding CWE definition.
Execute GPT-4 using the original vulnerability detection prompt.
Record the predicted vulnerability classification.

The objective of this stage is to reproduce the LLM-based vulnerability detection methodology evaluated in the original paper before the proposed workflow-based replacement introduced in this work.

Stage 3 — Vulnerability Repair

For samples identified as vulnerable:

Provide the vulnerable code.
Provide the associated CWE identifier.
Provide the corresponding CWE definition.
Execute GPT-4 using the original repair prompt.
Generate repaired code.
Record the repaired implementation.
Stage 4 — Repair Evaluation

The repaired code is evaluated using the same review methodology adopted by the original study.

The evaluation consists of:

CodeQL
Bandit
Manual review (when required)

A repaired sample is considered successful only when the target vulnerability is no longer present.

Only the predefined target CWE associated with each benchmark sample is evaluated.

Large Language Model

The reproduced baseline uses GPT-4 for both stages originally evaluated using an LLM.

Stage	Model
Vulnerability Detection	GPT-4
Vulnerability Repair	GPT-4

This configuration reproduces the LLM-based Secure Code Agent baseline used for comparison throughout this study.

Prompts
Vulnerability Detection

The original RQ2 detection prompt is reproduced without modification.

Your task is to determine whether the following Python code is vulnerable to CWE-<SN>(<Definition>). Return True for vulnerable or False for invulnerable.

Vulnerability Repair

The original repair prompt is reproduced without modification.

You will be provided with a piece of Python code vulnerable to CWE-<SN>(<Definition>). Your task is to generate the complete fixed code.

Model Configuration

The reproduction follows the configuration reported in the original study.

Default GPT parameters
Independent execution for every benchmark sample
One conversation per sample

Evaluation Metrics

To facilitate a comprehensive comparison between the reproduced Secure Code Agent baseline and the proposed comparison methods, the reproduction records the original evaluation metrics reported by the authors together with additional performance metrics used throughout this study.

Vulnerability Detection

The following metrics are collected to evaluate vulnerability detection performance:

Accuracy
Precision
Recall
F1 Score
Detection Coverage

These metrics quantify the ability of the vulnerability detection component to correctly identify the target CWE associated with each benchmark sample.

Vulnerability Repair

The following metrics are collected to evaluate repair performance:

Final Secure Output Rate
Repair Success Rate
CWE Coverage

In addition, the repair model used during each experiment is recorded as part of the experimental configuration to ensure reproducibility and facilitate comparison across different repair strategies.

Notes

This reproduction intentionally preserves the original LLM-based vulnerability detection and repair methodology so that the LLM components can be directly compared against the workflow-based approach proposed in this work.By modifying only the LLM components within the secure code agent, the experimental evaluation isolates the contribution of langgraph workflow to vulnerability detection and repair performance.  The only deviations from the original study are the use of the predefined SecurityEval evaluation dataset included in this repository, the omission of iterative repair in favor of a single-pass evaluation protocol, and the collection of additional evaluation metrics to enable a more comprehensive comparison between the reproduced baseline and the modified comparison methods.