Method Reproduction Details – LangGraph Secure Code Agent

Purpose

This document specifies the implementation details used to reproduce the LangGraph Secure Code Agent, a modified version of the Secure Code Agent baseline presented in How Well Do Large Language Models Serve as End-to-End Secure Code Agents for Python? The objective of this modified implementation is to replace the original LLM-based vulnerability detection stage with the proposed LangGraph security workflow and redesigning the repair prompt while preserving the remainder of the end-to-end remediation pipeline. This implementation serves as the primary experimental method for evaluating the contribution of workflow-based vulnerability detection within an existing LLM-based secure remediation architecture.

Architecture Diagram

A visual representation of the LangGraph Secure Code Agent is provided in figures/langgraph_secure_code_agent.png.

Original Method

The original study evaluates an end-to-end secure code generation pipeline through four research questions:

RQ1: Code Generation
RQ2: Vulnerability Detection
RQ3: Vulnerability Repair
RQ4: Iterative Secure Code Agent

The LangGraph Secure Code Agent preserves the overall Secure Code Agent architecture while modifying two components. First, the vulnerability detection methodology evaluated in RQ2 is replaced with the LangGraph workflow proposed in this work. Second, the prompt for the LLM in RQ3 is redesigned in order to support the implementation of the security report for the repair phase.

Reproduction Scope

The reproduced method follows the Secure Code Agent baseline with four controlled modifications.

Modification 1 — Evaluation Dataset

The original paper generates code using the complete SecurityEval benchmark consisting of 121 Python programming tasks spanning 69 CWEs.

For this reproduction, the code generation stage is omitted because the benchmark samples are already provided within this repository. The evaluation is therefore performed directly on the predefined SecurityEval evaluation dataset containing representative vulnerable samples for the same 69 CWEs.

Modification 2 — LangGraph Vulnerability Detection

The original Secure Code Agent performs vulnerability detection using a single GPT-4 prompt.

This implementation replaces the single LLM detector with the LangGraph security workflow developed in this work.

The workflow performs structured vulnerability analysis through multiple specialized processing stages before producing a validated security report used by the repair stage.

Modification 3 — Structured Repair Prompt

The prompt for the repair stage is redesigned in order to support the implementation of the security report for the repair phase. 

Modification 4 — Single-Pass Repair

The original Secure Code Agent repeatedly repairs vulnerable code until no vulnerabilities remain or a maximum iteration limit is reached.

This reproduction performs one repair attempt for each vulnerable sample.

The iterative repair stage is intentionally omitted to maintain a consistent evaluation protocol across all compared methods, isolate the effects of the proposed workflow architecture, and reduce computational cost and execution time.

Experimental Workflow

The reproduced LangGraph Secure Code Agent consists of the following stages.

Stage 1 — Input Dataset

For each benchmark sample:

Load the vulnerable source code.
Load the associated target CWE identifier.
Load the corresponding CWE definition.
Stage 2 — LangGraph Vulnerability Detection

The original GPT-4 vulnerability detector is replaced by the LangGraph security workflow.

For each benchmark sample:

Load the vulnerable source code.
Execute the LangGraph workflow.
Retrieve relevant security knowledge through the Retrieval-Augmented Generation (RAG) component.
Perform structured vulnerability reasoning.
Validate the predicted vulnerabilities.
Generate the final LangGraph Security Report.

The LangGraph Security Report contains the validated vulnerability findings and serves as the primary input for the subsequent repair stage.

Stage 3 — Vulnerability Repair

For samples identified as vulnerable:

Provide the vulnerable source code.
Provide the LangGraph Security Report.
Execute GPT-4 using the LangGraph Secure Code Agent Repair Prompt.
Generate repaired code.
Record the repaired implementation.

The repair prompt used in this stage is provided separately under:

Prompts/
LangGraph Secure Code Agent Repair Prompt.md
Stage 4 — Repair Evaluation

The repaired code is evaluated using the same review methodology adopted by the original study.

The evaluation consists of:

CodeQL
Bandit
Manual review (when required)

A repaired sample is considered successful only when the target vulnerability is no longer present.

Only the predefined target CWE associated with each benchmark sample is evaluated.

LangGraph Workflow

The vulnerability detection stage is performed using the LangGraph workflow proposed in this work.

Large Language Models

The reproduced method uses the following language models.

Stage	Model
Vulnerability Detection	LangGraph Workflow
Vulnerability Repair	GPT-4
Prompts
Vulnerability Detection

The vulnerability detection stage is performed entirely by the LangGraph workflow.

No standalone vulnerability detection prompt is used.

Vulnerability Repair

The repair stage uses the dedicated repair prompt developed for the LangGraph Secure Code Agent.

The prompt is provided separately under:

Prompts/
langgraph_secure_code_agent_repair_prompt.md

Model Configuration

The reproduction follows the Secure Code Agent baseline configuration except for the modified vulnerability detection stage and the redesign of the repair prompt.

LangGraph workflow used for vulnerability detection
Repair prompt redesigned
GPT-4 used for vulnerability repair
Independent execution for every benchmark sample
One execution per sample
Evaluation Metrics

To facilitate a comprehensive comparison between the reproduced LangGraph Secure Code Agent and the comparison methods, the following evaluation metrics are collected.

Vulnerability Detection
Accuracy
Precision
Recall
F1 Score
Detection Coverage

These metrics quantify the ability of the LangGraph workflow to correctly identify the target CWE associated with each benchmark sample.

Vulnerability Repair

The following metrics are collected to evaluate repair performance:

Final Secure Output Rate
Repair Success Rate
CWE Coverage

In addition, the repair model used during each experiment is recorded as part of the experimental configuration to ensure reproducibility and facilitate comparison across different repair strategies.

Notes

This reproduction preserves the overall Secure Code Agent architecture while replacing the original single LLM vulnerability detector with the LangGraph workflow proposed in this work and redesigning the repair prompt. The validated security report generated by the workflow is supplied as the primary input to the repair stage, allowing the repair model to operate on structured vulnerability findings rather than the original detection prompt. The only deviations from the Secure Code Agent baseline are the replacement of the vulnerability detection component with the LangGraph workflow, the redesign of the repair prompt, the use of the LangGraph Security Report as input to the LLM for repair, the use of the predefined SecurityEval evaluation dataset included in this repository, the omission of iterative repair in favor of a single-pass evaluation protocol, and the collection of additional evaluation metrics to enable a comprehensive comparison between the methods.