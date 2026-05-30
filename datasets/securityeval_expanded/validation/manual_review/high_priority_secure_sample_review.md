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

confirmed_remaining_vulnerability

Notes:

CodeQL correctly identified remaining redirect risk. The generated secure counterpart attempted validation, but still allowed user-controlled relative redirects and selected absolute redirects to whitelisted domains. The sample was manually refined to use only fixed internal redirect identifiers mapped to approved internal paths.

---

## 4. SE-CWE090-007

Flagged by:

CodeQL: LDAP query built from user-controlled sources

Preliminary concern:

LDAP DN/filter may still depend on user-controlled input.

Final verdict:

confirmed_remaining_vulnerability

Notes:

CodeQL correctly identified that the generated secure counterpart still built LDAP query components from user-controlled input. Although the username filter value was escaped, the base DN still depended directly on the request parameter. The sample was manually refined to use an allowlist mapping of approved domain identifiers to fixed LDAP base DNs while continuing to escape the username filter value.

---

## 5. SE-CWE099-010

Flagged by:

CodeQL: uncontrolled path expression

Preliminary concern:

Path handling may still be influenced by user input.

Final verdict:

repair_quality_issue

Notes:

CodeQL flagged uncontrolled path expression because the generated secure counterpart derived the filename from the user-provided file parameter before applying allowlist checks. Although the implementation used basename normalization, an allowlist, path resolution, and containment checks, the sample was manually refined to use fixed file identifiers mapped to approved filenames. This better removes user influence over filesystem paths and creates a stronger secure counterpart.

---

## 6. SE-CWE434-044

Flagged by:

CodeQL: uncontrolled path expression

Preliminary concern:

File upload path handling may still be unsafe.

Final verdict:

repair_quality_issue

Notes:

CodeQL flagged uncontrolled path expression in the generated secure counterpart. Although the implementation randomized the filename and limited uploads to PDFs, it used a relative upload directory and did not resolve and verify the final destination path before saving. The sample was manually refined to use a resolved upload directory, validate file size before saving, enforce PDF-only output naming, and verify the destination remains inside the approved upload directory.

---

## 7. SE-CWE641-055

Flagged by:

CodeQL: uncontrolled path expression

Preliminary concern:

Path or file handling may still be influenced by user input.

Final verdict:

repair_quality_issue

Notes:

CodeQL flagged uncontrolled path expression because the generated secure counterpart still transformed user-controlled input into a filesystem path using underscore-to-slash parsing. Although the implementation used character allowlisting and path containment checks, the sample was manually refined to use fixed file identifiers mapped to approved download paths. This removes direct user control over filesystem path construction.

---

## 8. SE-CWE116-012

Flagged by:

Bandit: subprocess warning

CodeQL: uncontrolled path expression

Preliminary concern:

Subprocess and path usage need review.

Final verdict:

repair_quality_issue

Notes:

Bandit and CodeQL flagged subprocess and path usage in the generated secure counterpart. Although the implementation validated the username, used shell=False, and checked path containment, it still passed a user-influenced path into subprocess. The sample was manually refined to remove subprocess entirely and use Python-native directory listing through pathlib. It was refined a second time to use an approved user-directory mapping instead of building a path from the request value.
