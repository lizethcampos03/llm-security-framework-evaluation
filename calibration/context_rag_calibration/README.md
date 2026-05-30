# Context Profile + RAG Calibration

## Purpose

This calibration phase evaluates how security context profiles and retrieval strategies influence workflow performance.

The objective is to determine whether improved context engineering and retrieval quality improve downstream:

* vulnerability detection
* secure repair
* reasoning quality
* workflow consistency

This phase precedes final workflow evaluation and is used to calibrate retrieval behavior before architecture freeze.

---

# Calibration Scope

This phase evaluates:

* context profile usefulness
* CWE retrieval quality
* retrieval ranking quality
* retrieval consistency
* retrieval usefulness for detection
* retrieval usefulness for repair
* hybrid retrieval strategy

---

# Main Research Questions

RQ1:

Does the security context profile improve retrieval quality?

RQ2:

Does hybrid retrieval reduce noisy retrieval results?

RQ3:

Does improved retrieval improve downstream vulnerability detection?

RQ4:

Does improved retrieval improve secure repair quality?

RQ5:

Which context profile fields provide the most value without excessive user burden?

---

# Calibration Dataset

A smaller OWASP-focused subset will be used rather than the full evaluation dataset.

The goal is workflow calibration rather than final evaluation.

---

# Outputs

This calibration phase produces:

* retrieval logs
* retrieval quality measurements
* context profile observations
* retrieval configuration decisions
* architecture decisions for workflow freeze
