# High-Priority Secure Sample Review

## Purpose

This document records detailed manual review for secure samples flagged by Bandit and/or CodeQL during Phase 2 validation.

The goal is to determine whether each flagged secure sample is:

* actually secure
* still vulnerable
* a repair-quality issue
* a tool false positive
* requiring regeneration or manual refinement

---

## Review Labels

confirmed_safe_false_positive

confirmed_remaining_vulnerability

repair_quality_issue

needs_fix_regeneration

needs_manual_refinement

tool_error

---

# Review Queue

## 1. SE-CWE095-009

Flagged by:

Bandit: B307 eval usage

Preliminary concern:

Likely remaining vulnerability because secure.py still uses eval().

Final verdict:

confirmed_remaining_vulnerability

Notes:

Bandit correctly flagged B307 because the generated secure counterpart still used eval(). Even though the code attempted AST validation and restricted builtins, the secure counterpart preserved dynamic code evaluation behavior. The sample requires manual refinement to remove eval() entirely and use explicit AST interpretation instead.

Refinement completed.

The secure counterpart was updated to remove eval() entirely and replace it with explicit AST interpretation. Dataset integrity validation passed and Bandit reported no remaining issues after refinement.

Final status:

resolved_after_refinement

---

## 2. SE-CWE918-067

Flagged by:

CodeQL: Full server-side request forgery

CodeQL: Reflected server-side cross-site scripting

Preliminary concern:

Likely remaining SSRF and output-handling issue.

Final verdict:

confirmed_remaining_vulnerability

Notes:

CodeQL correctly identified remaining SSRF and reflected output concerns. The generated secure counterpart restricted the constructed URL to example.com, but still allowed user-controlled subdomain selection and returned the external response body directly. The sample requires manual refinement using a strict subdomain allowlist, disabled redirects, timeout handling, response validation, and safe text output.

---

## 3. SE-CWE601-052

Flagged by:

CodeQL: URL redirection from remote source

CodeQL: potentially uninitialized local variable

Preliminary concern:

Redirect validation may be incomplete and implementation may contain a bug.

Final verdict:

PENDING

Notes:

PENDING

---

## 4. SE-CWE090-007

Flagged by:

CodeQL: LDAP query built from user-controlled sources

Preliminary concern:

LDAP DN/filter may still depend on user-controlled input.

Final verdict:

PENDING

Notes:

PENDING

---

## 5. SE-CWE099-010

Flagged by:

CodeQL: uncontrolled path expression

Preliminary concern:

Path handling may still be influenced by user input.

Final verdict:

PENDING

Notes:

PENDING

---

## 6. SE-CWE434-044

Flagged by:

CodeQL: uncontrolled path expression

Preliminary concern:

File upload path handling may still be unsafe.

Final verdict:

PENDING

Notes:

PENDING

---

## 7. SE-CWE641-055

Flagged by:

CodeQL: uncontrolled path expression

Preliminary concern:

Path or file handling may still be influenced by user input.

Final verdict:

PENDING

Notes:

PENDING

---

## 8. SE-CWE116-012

Flagged by:

Bandit: subprocess warning

CodeQL: uncontrolled path expression

Preliminary concern:

Subprocess and path usage need review.

Final verdict:

PENDING

Notes:

PENDING
