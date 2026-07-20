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

> **Reviewer path:** Select **Runtime → Run all**.
>
> The notebook loads the public evaluation repository and presents its
> archived artifacts. It does not call Anthropic, OpenAI, LangSmith, or
> any other external model service.

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
