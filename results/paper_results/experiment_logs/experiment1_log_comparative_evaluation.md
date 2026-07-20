# **Experiment 1 Log \- Comparative Evaluation Against Traditional and LLM-Based Security Analysis Methods**

---

## **Objective**

Evaluate the detection performance of the proposed LangGraph Security Framework against:

1. State-of-the-art LLM-based secure code agent methodology from EASE 2025  
2. CodeQL static analysis engine  
3. Bandit static analysis engine

The goal of this experiment is to determine whether the proposed retrieval-enhanced architecture provides measurable improvements over both traditional security analysis tools and contemporary LLM-based vulnerability detection approaches.

---

# **Research Question**

How does the proposed LangGraph Security Framework compare against traditional static-analysis tools and state-of-the-art LLM-based security agents when detecting vulnerabilities in Python code?

---

# **Dataset**

* 69 CWE categories  
* Vulnerable samples from securityeval benchmark  
* Secure samples (generated as counterparts to vulnerable samples)

---

# **Compared Methods**

## **Method A — Proposed LangGraph Security Framework**

### **Architecture Components**

* Context Profiles  
* Hybrid RAG Retrieval  
* CWE Knowledge Base  
* Vulnerable Example Retrieval  
* Safe Counterpart Retrieval  
* Claude Opus Detection Agent  
* GPT-5.5 Repair Agent  
* Structured Security Reasoning

---

## **Method B — GPT-4 Secure Code Agent (EASE 2025\)**

### **Reference**

“How Well Do Large Language Models Serve as End-to-End Secure Code Agents for Python?”

EASE 2025\.

### **Configuration**

#### **Detection Model**

* GPT-4-0613

#### **Repair Model**

* GPT-4-0613

#### **Prompting Strategy**

* Direct CWE Prompting

#### **Knowledge Sources**

* No Retrieval  
* No Context Profiles  
* No Example Database

---

## **Method C — CodeQL**

### **Version**

CodeQL CLI 2.25.5

### **Language Pack**

Python Analysis Pack

### **Detection Method**

Static Semantic Analysis

### **Evaluation Configuration**

Single CodeQL database constructed from the complete 138-case benchmark source tree.

Security findings were evaluated using the Python Security and Quality query suite.

Quality-only findings (for example unused variables, unused imports, and regex quality warnings) were excluded from vulnerability classification metrics to ensure a fair comparison against security-focused detection methods.

---

## **Method D — Bandit**

### **Version**

Bandit 1.9.4

### **Detection Method**

Python Security Static Analysis

---

# **Evaluation Metrics**

## **Detection Metrics**

* Accuracy  
* Precision  
* Recall  
* F1 Score

## **Error Metrics**

* True Positives  
* True Negatives  
* False Positives  
* False Negatives

## **Operational Metrics**

* Average Runtime  
* Analysis Latency  
* Tool Coverage

---

# **Results Summary**

## **Detection Performance**

| Metric | LangGraph Framework | GPT-4 Secure Agent (EASE 2025\) | CodeQL | Bandit |
| ----- | ----- | ----- | ----- | ----- |
| Accuracy | 88.41% | 74.60% | 65.22% | 61.59% |
| Precision | 83.54% | TBD | 86.21% | 73.53% |
| Recall | 95.65% | TBD | 36.23% | 36.23% |
| F1 Score | 89.19% | TBD | 51.02% | 48.54% |

---

# **Classification Outcomes**

## **LangGraph Framework**

| Metric | Value |
| ----- | ----- |
| True Positives | 66 |
| True Negatives | 42 |
| False Positives | 13 |
| False Negatives | 3 |

---

## **GPT-4 Secure Agent (EASE 2025\)**

| Metric | Value |
| ----- | ----- |
| Accuracy | 74.60% |
| False Positive Rate | 3.10% |

Additional metrics were not reported by the authors.

Source: EASE 2025\.

---

## **CodeQL**

| Metric | Value |
| ----- | ----- |
| True Positives | 25 |
| True Negatives | 65 |
| False Positives | 4 |
| False Negatives | 44 |
| Accuracy | 65.22% |
| Precision | 86.21% |
| Recall | 36.23% |
| F1 Score | 51.02% |
| Safe Accuracy | 94.20% |

---

## **Bandit**

| Metric | Value |
| ----- | ----- |
| True Positives | 25 |
| True Negatives | 60 |
| False Positives | 9 |
| False Negatives | 44 |
| Accuracy | 61.59% |
| Precision | 73.53% |
| Recall | 36.23% |
| F1 Score | 48.54% |
| Safe Accuracy | 86.96% |
| Average Latency | 1.057 seconds |

---

# **Repair Performance**

| Metric | LangGraph Framework | GPT-4 Secure Agent |
| ----- | ----- | ----- |
| Repair Model | GPT-5.5 | GPT-4 |
| Single-Pass Repair Success | TBD | 59.6% |
| Iterative Repair Success | Future Experiment 3 | 85.5% |

Source: EASE 2025\.

---

# **Architectural Comparison**

| Capability | LangGraph Framework | GPT-4 Secure Agent |
| ----- | ----- | ----- |
| Context Profiles | Yes | No |
| Hybrid Retrieval | Yes | No |
| CWE Knowledge Base | Yes | No |
| Vulnerable Examples | Yes | No |
| Safe Counterparts | Yes | No |
| Structured Security Reasoning | Yes | Limited |
| Explainable Findings | Yes | Limited |
| Repair Capability | Yes | Yes |
| Security-Aware Context Modeling | Yes | No |

---

# **Preliminary Observations**

The proposed LangGraph Security Framework achieved 88.41% detection accuracy on the SecurityEval benchmark.

The GPT-4-based secure code agent reported in EASE 2025 achieved 74.60% detection accuracy.

This represents an absolute improvement of:

88.41 − 74.60 \= 13.81 percentage points

over a contemporary LLM-based security analysis approach.

The comparison suggests that retrieval augmentation, contextual profiling, and structured security reasoning contribute substantially to vulnerability detection performance.

CodeQL achieved 65.22% overall accuracy.

CodeQL produced only 4 false positives, yielding a high precision score of 86.21% and a safe-case accuracy of 94.20%.

However, CodeQL detected only 25 of 69 vulnerable samples, resulting in a recall of 36.23%.

Bandit achieved 61.59% overall accuracy.

Bandit also detected only 25 of 69 vulnerable samples, resulting in the same recall score of 36.23%.

Bandit executed significantly faster than CodeQL and the proposed framework, with an average latency of only 1.057 seconds per analysis.

However, Bandit produced more false positives and lower precision than CodeQL.

Compared with both static-analysis baselines, the proposed framework demonstrated substantially higher vulnerability coverage.

LangGraph detected 66 of 69 vulnerable samples.

CodeQL detected 25 of 69 vulnerable samples.

Bandit detected 25 of 69 vulnerable samples.

The most significant finding of Experiment 2 is the dramatic improvement in vulnerability recall achieved by the proposed framework.

Although CodeQL achieved slightly higher precision (86.21%) than LangGraph (83.54%), the difference was relatively small compared with the substantial recall advantage obtained by the proposed framework.

LangGraph achieved a recall of 95.65%, while both CodeQL and Bandit achieved only 36.23%.

This indicates that the retrieval-enhanced architecture substantially improves vulnerability discovery coverage while maintaining competitive precision.

The results suggest that retrieval augmentation, contextual profiling, CWE-grounded reasoning, and example-based security analysis enable the framework to identify a broader range of vulnerability classes than traditional rule-based static-analysis systems.

---

# **Comparative Finding**

The completed benchmark shows that the LangGraph Security Framework substantially outperformed both static-analysis baselines in vulnerability recall.

LangGraph detected 66 of 69 vulnerable samples.

CodeQL detected 25 of 69 vulnerable samples.

Bandit detected 25 of 69 vulnerable samples.

This result suggests that the retrieval-enhanced LLM architecture provides broader vulnerability coverage across diverse CWE families than either static-analysis baseline under the evaluated configuration.

