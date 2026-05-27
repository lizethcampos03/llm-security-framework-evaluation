# Manual Review Checklist for Secure Counterparts

## Purpose

This checklist is used to review secure counterparts generated from SecurityEval-derived vulnerable samples.

The goal is to ensure that each secure counterpart preserves intended functionality while mitigating the target CWE.

---

## Sample Information

- Sample ID:
- Source vulnerable sample:
- CWE ID:
- CWE name:
- Reviewer:
- Review date:

---

## Review Criteria

### 1. Functionality Preservation

- [ ] The secure version preserves the original intended behavior.
- [ ] Original function names are preserved where reasonable.
- [ ] Inputs and outputs remain compatible where reasonable.
- [ ] No unrelated features were added.

### 2. CWE Mitigation

- [ ] The target CWE is directly addressed.
- [ ] The secure version follows MITRE CWE mitigation guidance.
- [ ] The vulnerable pattern from the original sample is removed or mitigated.
- [ ] The fix is specific to the weakness, not generic.

### 3. Code Quality

- [ ] The code is syntactically valid Python.
- [ ] The code is readable.
- [ ] The code avoids unnecessary rewrites.
- [ ] The code avoids overly complex changes.

### 4. Security Quality

- [ ] The secure version does not introduce an obvious new vulnerability.
- [ ] Input validation is applied where relevant.
- [ ] Sensitive operations are protected where relevant.
- [ ] Error handling does not leak unnecessary sensitive information.

### 5. Tool Validation

- [ ] Bandit result reviewed.
- [ ] CodeQL result reviewed.
- [ ] Any warnings documented.
- [ ] False positives documented where applicable.

---

## Final Review Status

Choose one:

- [ ] Accepted
- [ ] Needs revision
- [ ] Rejected

## Notes

Add reviewer observations here.