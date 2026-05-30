# Security Context Profiles

## Purpose

Security Context Profiles provide structured application context that can be supplied to the workflow during vulnerability detection and secure repair.

The goal is to evaluate whether application-specific security context improves:

* vulnerability detection quality
* secure repair quality
* retrieval relevance
* repair consistency
* workflow reasoning quality

These profiles are used during:

* Context + RAG Calibration
* Detection Node Calibration
* Fix Node Calibration
* Final Workflow Evaluation

---

## Context Profile Schema

Each profile contains:

* application_type
* protected_assets
* user_roles
* authorization_rules
* security_requirements
* threat_concerns
* deployment_context
* dependencies
* expected_security_behavior

---

## Usage

Profiles are assigned to SecurityEval samples during calibration and experimentation.

The same vulnerable sample may be evaluated under multiple context profiles when studying context sensitivity.

---

## Research Hypothesis

CWE guidance

*

security context profile

*

optimized prompts

improves vulnerability detection and secure repair quality compared to context-free workflows.
