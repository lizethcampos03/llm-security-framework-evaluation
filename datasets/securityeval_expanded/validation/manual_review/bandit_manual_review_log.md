# Bandit Manual Review Log

## Purpose

This document records manual review observations for Bandit findings generated during Phase 2 dataset validation.

Bandit detections on secure samples are not automatically treated as false positives.

Each flagged case should be manually reviewed before final classification.

---

# Review Labels

Possible review labels:

```text
flagged_needs_review
confirmed_safe_false_positive
confirmed_remaining_vulnerability
needs_fix_regeneration
tool_error

Review Entries

| Sample ID | Bandit Rule | Initial Severity | Initial Confidence | Manual Review Status | Final Verdict | Notes |
| --------- | ----------- | ---------------- | ------------------ | -------------------- | ------------- | ----- |
