# Experimental Results

This directory contains the outputs generated throughout the experimental evaluation accompanying the paper:

> **A LangGraph-Orchestrated Framework for Secure Analysis and Repair of LLM-Generated Code**

The results are organized to distinguish the published experimental artifacts from outputs generated during future reproductions of the evaluation.

---

# Directory Structure

```
results/

├── paper_results/
└── reproduced_results/
```

Each directory serves a distinct purpose within the reproducibility workflow.

---

# Reported Results

The `paper_results/` directory contains the archived experimental outputs corresponding to the results presented in the accompanying paper.

These files represent the official outputs used to generate the reported evaluation, including:

- performance tables
- summary statistics
- evaluation logs
- workflow outputs
- publication figures

The contents of this directory should remain unchanged, as they provide the reference results associated with the published evaluation.

---

# Reproduced Results

The `reproduced_results/` directory stores outputs generated when the experiments are executed again using this repository.

Examples include:

- newly generated evaluation logs
- reproduced performance metrics
- regenerated figures
- regenerated tables
- workflow outputs

Separating reproduced results from the archived paper results prevents accidental modification of the published experimental artifacts.

---

# Relationship to the Experiments

Each experiment produces its own collection of outputs.

Typical outputs include:

## Workflow Calibration

- calibration summaries
- configuration comparisons
- selected workflow configuration

## Experiment 1 – Detection and Comparative Analysis

- evaluation metrics
- confusion matrices
- benchmark summaries
- comparative analysis tables

## Experiment 2 – End-to-End Secure Remediation

- remediation outcomes
- secure-output summaries
- repair success metrics
- workflow execution logs

## Experiment 3 – Chained-Vulnerability Evaluation

- chain reasoning outputs
- validated component findings
- generated repair plans
- experimental summaries

---

# Reproducing the Published Results

Researchers wishing to verify the published evaluation should compare newly generated outputs against the archived files stored in:

```
results/paper_results/
```

Minor numerical differences may occur when reproducing experiments that depend on external LLM services, model updates, or nondeterministic inference.

Such differences are expected and should be interpreted in the context of evolving foundation models.

---

# File Organization

Within each directory, outputs are organized according to the experiment that generated them.

A typical structure is:

```
reported/

├── calibration/
├── experiment1/
├── experiment2/
└── experiment3/
```

The same organization is recommended for the `reproduced_results/` directory.

Maintaining identical directory structures simplifies comparison between archived and reproduced results.

---

# Reproducibility

The separation between archived and reproduced outputs supports transparent scientific reporting by preserving the original evaluation while allowing independent verification of the experiments.

Researchers are encouraged to retain reproduced outputs separately rather than replacing the archived reference results.

---

# Summary

The results contained in this directory document both the published evaluation and future reproductions of the experimental workflow.

This organization preserves the integrity of the reported findings while supporting transparent, repeatable experimentation.