# 03 Vulnerable Import Methodology

## Purpose

This document defines the procedure used to construct the vulnerable class of the SecurityEval-derived contextual vulnerability benchmark.

The objective is to ensure consistency, reproducibility, traceability, and methodological rigor across all imported vulnerable samples.

---

## Vulnerable Sample Source

All vulnerable samples originate from SecurityEval reference vulnerable implementations.

The project does not generate vulnerable examples from scratch.

Instead, SecurityEval serves as the authoritative source of vulnerable benchmark samples.

---

## Naming Convention

Each vulnerable sample follows the format:

```text
SE-CWE<ID>-<NUMBER>
```

Examples:

```text
SE-CWE89-001
SE-CWE89-002
SE-CWE79-001
SE-CWE22-001
```

This convention improves:

- traceability
- experiment organization
- CWE-level analysis
- reporting consistency

---

## Sample Structure

Each vulnerable sample contains:

```text
SE-CWE<ID>-<NUMBER>/
├── vulnerable.py
├── metadata.json
└── validation_notes.md
```

Additional files may be added in later phases.

---

## Import Procedure

For each SecurityEval task:

1. Identify task identifier.
2. Identify associated CWE.
3. Extract vulnerable implementation.
4. Create sample directory.
5. Store implementation as vulnerable.py.
6. Create metadata.json.
7. Create validation_notes.md.
8. Verify traceability to original SecurityEval task.

---

## Metadata Requirements

Each sample metadata record must include:

- sample_id
- task_id
- cwe_id
- cwe_name
- owasp_category
- vulnerability_status
- source
- generation_method
- validation_status

Additional metadata fields may be added in later phases.

---

## Validation Requirements

Each imported sample should be reviewed to confirm:

- task mapping correctness
- CWE mapping correctness
- metadata correctness
- source traceability
- file completeness

Validation status should be recorded in validation_notes.md.

---

## Methodology Statement

The vulnerable class consists exclusively of SecurityEval-derived vulnerable implementations.

Secure counterparts, context profiles, and validation artifacts are generated in later phases using separate documented methodologies.
