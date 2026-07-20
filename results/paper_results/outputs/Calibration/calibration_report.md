# Calibration Report

## Fairness Note

Ground-truth labels and expected CWE identifiers were hidden from the LangGraph workflow during execution and were used only after inference for scoring. The calibration benchmark contained one vulnerable sample and one verified safe counterpart for each of nine CWE families.

## Calibration Scope

- **cwe_families**: `9`
- **total_cases**: `18`
- **vulnerable_cases**: `9`
- **safe_cases**: `9`

The calibration set covered:

- CWE-89 — SQL Injection
- CWE-798 — Hardcoded Credentials
- CWE-327 — Broken or Risky Cryptographic Algorithm
- CWE-306 — Missing Authentication for Critical Function
- CWE-285 — Improper Authorization
- CWE-215 — Information Exposure Through Debug Information
- CWE-200 — Information Exposure
- CWE-117 — Improper Output Neutralization for Logs
- CWE-94 — Code Injection

## Aggregate Metrics

- **total_cases**: `18`
- **correct_cases**: `15`
- **overall_accuracy**: `0.8333`
- **vulnerable_detection_accuracy**: `0.8889`
- **safe_classification_accuracy**: `0.7778`
- **true_positives**: `8`
- **false_positives**: `2`
- **false_negatives**: `1`
- **true_negatives**: `7`
- **precision**: `0.8000`
- **recall**: `0.8889`
- **f1**: `0.8421`
- **retrieval_success_rate**: `1.0000`
- **average_latency_seconds**: `approximately 59`

The confusion-matrix counts above are derived from the reported 9 vulnerable and 9 safe samples together with the stated vulnerable-detection and safe-classification accuracies.

## Final Configuration

| Component | Final Selection |
|---|---|
| Retrieval configuration | `full_hybrid_evidence_reranker` |
| Retrieval channels | Code keyword, code vector, CWE keyword, CWE vector |
| Evidence processing | Weighted evidence fusion and reranking |
| Detector model | Claude Opus |
| Prompt configuration | Configuration B |
| Reasoning policy | Code-first reasoning with safe-counterpart comparison |
| Validation strategy | Dedicated validation node removed |
| Repair behavior | Conditional; generated only for vulnerable classifications |
| Output format | Structured JSON security report |

## Architectural Decisions

### Retrieval Strategy

Hybrid retrieval was selected after comparing keyword, vector, and combined retrieval approaches. The final configuration integrates code-level and CWE-level keyword and vector retrieval, followed by weighted fusion and evidence reranking.

### Detection Prompt

The final detector prompt emphasized:

- source code as the primary source of truth;
- retrieved evidence as supporting context rather than proof;
- comparison with secure counterparts;
- uncertainty instead of unsupported vulnerability findings;
- alignment between detected behavior and CWE evidence.

### Detector Model

Claude Opus was selected for vulnerability detection because calibration showed strong code comprehension, security reasoning, CWE recognition, and stable structured output behavior.

### Validation Strategy

The dedicated validation node was removed. Calibration showed that repeated detector execution and majority voting increased latency and cost without producing a measurable improvement in classification quality.

### Repair Optimization

Repair generation became conditional. Vulnerable classifications proceeded to repair, while safe classifications bypassed repair generation to avoid unnecessary latency and cost.

## Final Workflow

```text
Input
  ↓
Preprocessing
  ↓
Full Hybrid Evidence Reranker
  ↓
Claude Opus Detector
  ↓
Conditional Repair Generation
  ↓
Structured Output Report
```

## Calibration Outcome

| Metric | Result |
|---|---:|
| Total Samples | 18 |
| Correct Classifications | 15 |
| Overall Accuracy | 83.33% |
| Vulnerable Detection Accuracy | 88.89% |
| Safe Classification Accuracy | 77.78% |
| Precision | 80.00% |
| Recall | 88.89% |
| F1 Score | 84.21% |
| Retrieval Success Rate | 100.00% |
| Average Latency | Approximately 59 seconds |

## Final Assessment

Calibration transformed the initial research-driven workflow into the frozen architecture used for the full benchmark evaluation. The most consequential improvements came from full hybrid retrieval, evidence reranking, code-first prompting, secure-counterpart reasoning, Claude Opus detector selection, removal of the validation node, and conditional repair generation.

The resulting configuration achieved 83.33% accuracy and 88.89% recall on the balanced 18-case calibration benchmark while maintaining 100% retrieval success. The architecture was frozen after this stage and used for the subsequent 69-CWE evaluation.
