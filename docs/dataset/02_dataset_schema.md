# 02 Dataset Schema

## Purpose

This document defines the metadata schema used throughout the SecurityEval-derived contextual vulnerability benchmark.

The schema ensures consistency, reproducibility, traceability, and compatibility across dataset generation, validation, experimentation, and reporting activities.

---

## Required Metadata Fields

Each dataset sample must contain the following metadata fields.

### sample_id

Unique identifier for the sample.

Example:

```text
SE-CWE89-001
```

---

### task_id

Original SecurityEval task identifier.

Example:

```text
task_001
```

---

### cwe_id

Associated Common Weakness Enumeration identifier.

Example:

```text
CWE-89
```

---

### cwe_name

Human-readable CWE name.

Example:

```text
SQL Injection
```

---

### owasp_category

Associated OWASP category when applicable.

Example:

```text
A03:2021 Injection
```

---

### vulnerability_status

Classification label.

Allowed values:

- vulnerable
- secure

---

### source

Origin of the sample.

Examples:

- SecurityEval reference solution
- CWE-guided secure rewrite

---

### generation_method

Method used to create the sample.

Examples:

- SecurityEval reference implementation
- CWE-guided secure counterpart generation

---

### secure_generation_prompt_version

Version identifier used for secure counterpart generation.

Example:

```text
secure_prompt_v1
```

---

### context_profile_version

Version identifier of the associated security context profile.

Example:

```text
context_profile_v1
```

---

### validation_status

Current validation state.

Allowed values:

- pending
- validated
- rejected

---

### notes

Additional observations relevant to the sample.

---

## Sample Directory Structure

Each dataset sample should eventually contain:

```text
sample_id/
├── vulnerable.py
├── secure.py
├── context_profile.json
├── metadata.json
└── validation_notes.md
```

---

## Purpose of the Schema

The schema supports:

- reproducibility
- dataset validation
- experiment execution
- tool comparison
- reporting
- future dataset expansion

This schema serves as the official metadata specification for the SecurityEval-derived contextual benchmark.
