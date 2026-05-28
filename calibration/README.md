# Workflow Calibration

## Purpose

This folder contains the workflow calibration documentation for the LLM security framework.

Calibration is the engineering stage used to refine the workflow before final evaluation experiments.

The purpose of calibration is to improve:

- retrieval quality
- vulnerability detection
- secure repair generation
- repair verification
- reporting quality
- workflow reliability

Calibration is separate from final experiments.

Calibration improves the workflow.

Final experiments evaluate the frozen workflow.

---

# Calibration Philosophy

The workflow is calibrated as an integrated orchestration system rather than as isolated components.

The calibration process focuses on whether workflow behavior improves through:

- context engineering
- retrieval improvements
- prompt engineering
- validation strategies
- repair verification
- structured reporting

---

# Calibration Flow

The workflow calibration process follows this order:

```text
Context Profile + RAG Calibration
→ Detection Node Calibration
→ Fix Node Calibration
→ Fix Verification Calibration
→ Report Node Calibration
→ Validation Run Calibration
→ Architecture Freeze
Calibration Sections
Context Profile + RAG Calibration

Folder:

context_rag_calibration/

Focuses on:

context profile design
retrieval quality
hybrid retrieval
retrieval ranking
retrieval usefulness
retrieval noise reduction
Detection Node Calibration

Document:

detection_node_calibration.md

Focuses on improving vulnerability detection quality.

Fix Node Calibration

Document:

fix_node_calibration.md

Focuses on improving secure repair quality.

Fix Verification Calibration

Document:

fix_verification_calibration.md

Focuses on validating generated repairs before reporting.

Report Node Calibration

Document:

report_node_calibration.md

Focuses on improving report usefulness and auditability.

Validation Run Calibration

Document:

validation_run_calibration.md

Focuses on repeated validation and aggregation reliability.

Architecture Freeze

Calibration ends when the workflow is stable enough to freeze.

After the architecture is frozen, final experiments begin.
