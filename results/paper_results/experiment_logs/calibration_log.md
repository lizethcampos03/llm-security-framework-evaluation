# **Calibration Experiment Log**

---

## **Calibration Experiment Purpose**

The calibration experiment was conducted to transform the initial research-driven architecture into a fully calibrated architecture suitable for large-scale benchmark evaluation. The primary objective was to identify which architectural design choices produced measurable improvements in vulnerability detection accuracy, retrieval quality, false positive behavior, false negative behavior, repair performance, latency, and overall workflow efficiency before executing the full SecurityEval benchmark.

The experiment evaluated retrieval strategies, prompt design refinements, detector model selection, workflow optimizations, validation approaches, and repair generation behavior. The resulting architecture was frozen and subsequently used for the full 69-CWE benchmark evaluation.

---

# **Calibration Scope**

## **Calibration CWE Set**

The calibration benchmark consisted of the following CWE families:

* CWE-89 – SQL Injection  
* CWE-798 – Hardcoded Credentials  
* CWE-327 – Broken or Risky Cryptographic Algorithm  
* CWE-306 – Missing Authentication for Critical Function  
* CWE-285 – Improper Authorization  
* CWE-215 – Information Exposure Through Debug Information  
* CWE-200 – Information Exposure  
* CWE-117 – Improper Output Neutralization for Logs  
* CWE-94 – Code Injection

For each CWE:

* One vulnerable sample was evaluated.  
* One secure counterpart was evaluated.

Total evaluation set:

* 9 CWE families  
* 18 benchmark samples  
* 9 vulnerable samples  
* 9 safe samples

Ground-truth labels and CWE identifiers were intentionally hidden from the LangGraph workflow to preserve fairness and prevent leakage.

---

# **Architectural Variables Evaluated**

## **Retrieval Strategy**

Several retrieval configurations were evaluated during calibration.

Evaluated approaches included:

* Keyword retrieval  
* Vector retrieval  
* Hybrid retrieval  
* Evidence reranking  
* Weighted retrieval fusion

Observations showed that hybrid retrieval consistently produced stronger contextual evidence than either keyword-only or vector-only retrieval.

The final retrieval configuration adopted:

* Code keyword retrieval  
* Code vector retrieval  
* CWE keyword retrieval  
* CWE vector retrieval  
* Weighted evidence fusion  
* Evidence reranking

This configuration was designated:

Full Hybrid Evidence Reranker

---

## **Detection Prompt Calibration**

Prompt engineering represented one of the most significant calibration activities.

Multiple revisions were performed to improve:

* False positive handling  
* False negative handling  
* Safe counterpart reasoning  
* Code-first reasoning  
* CWE alignment

Several additions proved particularly valuable:

### **Code-First Reasoning**

The detector was explicitly instructed to treat code as the primary source of truth and retrieval evidence as supporting context rather than proof.

### **Safe Counterpart Reasoning**

The detector was instructed to compare retrieved vulnerable examples against retrieved secure examples before making a final classification.

### **Uncertainty Handling**

The detector was instructed to prefer uncertainty over unsupported vulnerability findings whenever exploitability could not be demonstrated from the code itself.

These prompt refinements substantially improved classification quality throughout calibration.

---

## **Detector Model Selection**

Several model configurations were considered during calibration.

The final detector model selected was:

Claude Opus

Selection was based on:

* Strong code comprehension  
* Strong security reasoning  
* Consistent structured outputs  
* Reliable CWE recognition

Throughout calibration, Claude Opus consistently produced the most useful security analyses and the most stable structured JSON outputs.

---

## **Validation Strategy**

The original architecture included a dedicated validation node using repeated detector executions and majority voting.

Calibration revealed several limitations:

* Significant latency overhead  
* Increased cost  
* Minimal improvement in classification quality

After experimentation, validation iterations were progressively reduced.

Final observations demonstrated that single-pass validation contributed little measurable benefit while significantly increasing runtime.

The validation node was therefore removed from the final architecture.

---

## **Repair Generation Optimization**

Calibration also evaluated repair generation behavior.

Originally, repair generation occurred regardless of final classification.

Observations revealed that generating repairs for safe samples produced unnecessary latency and cost.

The final workflow therefore generated repairs only when a vulnerability was detected.

Safe samples bypassed repair generation entirely.

---

# **Calibration Metrics**

The following metrics were used throughout calibration:

* Overall Accuracy  
* Vulnerable Detection Accuracy  
* Safe Classification Accuracy  
* Precision  
* Recall  
* F1 Score  
* Average Confidence  
* Retrieval Quality  
* Retrieval Success Rate  
* Average Latency  
* Fix Generation Behavior  
* False Positive Count  
* False Negative Count

---

# **Calibration Results**

## **Final Calibration Outcome**

| Metric | Result |
| ----- | ----- |
| Total Samples | 18 |
| Correct Classifications | 15 |
| Overall Accuracy | 83.33% |
| Vulnerable Detection Accuracy | 88.89% |
| Safe Classification Accuracy | 77.78% |
| Precision | 80.00% |
| Recall | 88.89% |
| F1 Score | 84.21% |
| Retrieval Success Rate | 100% |
| Average Latency | Approximately 59 seconds |

---

# **Major Observations**

## **Retrieval Performance**

Hybrid retrieval consistently produced the strongest evidence quality.

Keyword-only retrieval frequently missed relevant examples, while vector-only retrieval occasionally retrieved semantically related but less relevant artifacts.

Combining both approaches produced the most reliable evidence.

---

## **Prompt Design Impact**

Prompt refinements produced one of the largest improvements observed during calibration.

In particular:

* Safe counterpart reasoning  
* Code-first reasoning

substantially reduced unsupported findings.

---

## **False Positive Behavior**

Most remaining false positives occurred within:

* Authentication-related weaknesses  
* Authorization-related weaknesses  
* Information disclosure weaknesses

These categories often involve contextual assumptions that are difficult to fully resolve using code alone.

---

## **False Negative Behavior**

False negatives were relatively uncommon.

Most missed vulnerabilities involved subtle implementations requiring more nuanced reasoning than explicit insecure patterns.

This observation supported prioritizing recall throughout the remainder of calibration.

---

## **Workflow Simplification**

Removing validation reduced latency without producing measurable degradation in detection quality.

This was one of the most impactful workflow optimizations identified during calibration.

---

# **Final Architecture Adopted**

The architecture frozen after the calibration experiment consisted of:

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

Key characteristics:

* Full Hybrid Retrieval  
* Claude Opus Detection  
* Configuration B Prompt  
* Validation Removed  
* Conditional Repair Generation  
* Structured JSON Reporting

---

# **Calibration Conclusions**

The calibration experiment successfully transformed the initial research-driven workflow into a substantially more accurate and efficient architecture.

The calibration process demonstrated that retrieval quality, detector prompting, workflow simplification, and model selection each contributed meaningfully to system performance.

Among all evaluated design choices, hybrid retrieval, prompt engineering, safe counterpart reasoning, and removal of unnecessary workflow overhead produced the largest measurable improvements.

The resulting architecture achieved strong detection performance while maintaining a low false negative rate, which was prioritized due to the security-critical nature of vulnerability detection.

Based on these results, the architecture was frozen and subsequently used for the full 69-CWE benchmark evaluation documented in experiment 1\.

