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

# Reproduction Modes

## Analysis Mode

Analysis mode uses the archived outputs stored in:

```text
results/paper_results/
```

It reproduces the reported metrics, tables, and figures without making external LLM API calls.

This is the recommended mode for reviewers who want to verify the reported analysis quickly and without incurring API costs.

## Full Execution Mode

Full execution mode reruns the supported experimental workflow using the repository datasets, prompts, configurations, and experiment scripts.

This mode requires user-provided API credentials and may incur inference costs.

Because hosted language models may change over time and can produce nondeterministic outputs, newly generated results may differ slightly from the archived paper results.

---

# Recommended Reviewer Workflow

Reviewers may use the notebook in the following order:

1. Verify the repository structure and environment.
2. Load the frozen experimental configuration.
3. Inspect the benchmark and prompt artifacts.
4. Recompute metrics from the archived outputs.
5. Regenerate the paper tables and figures.
6. Optionally enable full execution mode.

---

# Running in Google Colab

Open `paper_reproduction.ipynb` in Google Colab and execute the cells in order.

The notebook installs the required dependencies and loads repository-relative files automatically.

API credentials are required only for cells marked as part of full execution mode. Credentials should be supplied through environment variables or Colab secrets and should never be committed to the repository.

---

# Reproducibility Notes

The archived outputs represent the exact experimental results used in the accompanying paper.

Full reruns should use the frozen configuration documented in:

```text
configs/configuration_manifest.md
```

Newly generated outputs should be written to:

```text
results/reproduced_results/
```

The archived paper results should remain unchanged.

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

It supports rapid analysis of the archived results while also providing an optional path for rerunning the supported experimental workflow.