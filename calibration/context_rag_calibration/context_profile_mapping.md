# Context Profile Mapping

## Purpose

This document maps the OWASP-inspired calibration subset to reusable security context profiles.

The calibration subset uses the same ten vulnerability categories presented in Table 1 of the current report so that calibration results remain aligned with the existing experimental story.

This mapping will be used during:

- Context + RAG Calibration
- Detection Node Calibration
- Fix Node Calibration

---

## Calibration Subset

| Vulnerability Category | CWE |
|---|---|
| SQL Injection | CWE-89 |
| Hardcoded Credentials | CWE-798 |
| Weak Cryptography | CWE-327 |
| Missing Authentication | CWE-306 |
| Broken Access Control | CWE-284 |
| Security Misconfiguration | CWE-489 |
| Sensitive Information Exposure | CWE-200 |
| Vulnerable and Outdated Components | CWE-1104 |
| Security Logging and Monitoring Failures | CWE-778 |
| Insecure Design / Code Injection | CWE-94 |

---

## Context Profile Mapping

| Vulnerability Category | CWE | Context Profile |
|---|---|---|
| SQL Injection | CWE-89 | financial_application |
| Hardcoded Credentials | CWE-798 | authentication_service |
| Weak Cryptography | CWE-327 | financial_application |
| Missing Authentication | CWE-306 | authentication_service |
| Broken Access Control | CWE-284 | healthcare_application |
| Security Misconfiguration | CWE-489 | enterprise_internal_tool |
| Sensitive Information Exposure | CWE-200 | healthcare_application |
| Vulnerable and Outdated Components | CWE-1104 | cloud_management_platform |
| Security Logging and Monitoring Failures | CWE-778 | enterprise_internal_tool |
| Insecure Design / Code Injection | CWE-94 | developer_platform |

---

## Rationale

The calibration subset intentionally uses the same ten OWASP-inspired categories from the current report.

This keeps the calibration study aligned with the existing analysis and allows future report updates to connect calibration results directly to the prototype evaluation.

---

## Calibration Use

These mappings will support:

- context-aware retrieval testing
- detection prompt calibration
- fix prompt calibration
- repair-context usefulness analysis
- final workflow configuration decisions

---

## Evaluation Goal

Determine whether adding structured security context improves:

- retrieval usefulness
- detection quality
- repair quality
- consistency
- contextual reasoning

compared to context-free baseline workflows.