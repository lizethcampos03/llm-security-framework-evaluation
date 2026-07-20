# Reproduction Notebook

This directory contains the primary Google Colab-compatible notebook for reproducing the experimental evaluation accompanying the paper:

> **A LangGraph-Orchestrated Framework for Secure Analysis and Repair of LLM-Generated Code**

The notebook provides a guided entry point to the datasets, configurations, prompts, experiment scripts, and reported results contained in this repository.

---

# Directory Contents

```text
notebooks/

└── paper_reproduction.ipynb
```

---

# Notebook Scope

The notebook supports reproduction of:

- workflow calibration results
- vulnerability detection metrics
- comparative results for CodeQL and Bandit
- end-to-end remediation results
- chained-vulnerability evaluation summaries
- runtime and cost summaries
- paper tables and figures

The notebook coordinates the experimental artifact but does not contain the complete production implementation of the research prototype.

---

# Reproduction 

## Analysis Mode

Analysis mode uses the archived outputs stored in:

```text
results/paper_results/
```

It reproduces the reported metrics, tables, and figures without making external LLM API calls.

This is the recommended mode for reviewers who want to verify the reported analysis.

---

# Recommended Reviewer Workflow

Reviewers may use the notebook in the following order:

1. Verify the repository structure and environment.
2. Load the frozen experimental configuration.
3. Inspect the benchmark and prompt artifacts.
4. Recompute metrics from the archived outputs.
5. Regenerate the paper tables and figures.

---

# Reproducibility Notes

The archived outputs represent the exact experimental results used in the accompanying paper.

---

# Related Documentation

Additional details are available in:

- `experiments/methodology.md`
- `datasets/README.md`
- `prompts/README.md`
- `configs/README.md`
- `configs/configuration_manifest.md`
- `results/README.md`

---

# Summary

The reproduction notebook is the primary reviewer-facing interface for verifying the reported evaluation.
