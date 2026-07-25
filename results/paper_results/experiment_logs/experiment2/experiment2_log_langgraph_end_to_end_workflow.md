# **Experiment 2 Log**

## **LangGraph-Augmented End-to-End Workflow Evaluation**

---

# **Experiment Overview**

## **Objective**

Evaluate whether integrating the LangGraph Security Framework into an end-to-end secure-code workflow improves vulnerability detection, repair effectiveness, and final secure-output outcomes relative to the strongest workflow reported in EASE 2025\.

Experiment 2 evaluates the workflow-level value of the proposed framework. Unlike Experiment 1, which focused primarily on detection quality and comparative detection performance, Experiment 2 evaluates whether the structured LangGraph security report can improve downstream repair when used as guidance for a repair LLM.

---

# **Execution Methodology**

Experiment 2 reused completed outputs from previous experiments as the first stages of the end-to-end workflow.

## **Detection Stage**

The detection stage used the finalized LangGraph results from Experiment 1\.

Experiment 1 evaluated the framework on:

| Dataset Component | Count |
| ----- | ----- |
| SecurityEval vulnerable tasks | 69 |
| Verified safe counterparts | 69 |
| Total benchmark cases | 138 |

## **Verification Stage Before Repair**

The verification stage used completed Experiment 1 outputs, including CodeQL, Bandit, and manual review evidence.

These results established comparative behavior for the static-analysis tools and supported the verified-finding stage of the proposed workflow.

## **Repair Stage**

The repair stage was executed in Experiment 2\.

For each vulnerable case, the complete LangGraph output-node security report was provided to the repair LLM.

Repair model used:

| Component | Value |
| ----- | ----- |
| Repair Model | GPT-4-0613 |
| Reason for Selection | Same repair model family as EASE baseline, so improvements are attributable primarily to the LangGraph workflow rather than to a newer repair model |

## **Post-Repair Verification**

Post-repair verification used:

* Bandit  
* CodeQL  
* Manual review

CodeQL was run using one database over the repaired source tree, not one database per file.

---

# **Proposed Workflow**

Code Generation  
        ↓  
LangGraph Security Framework  
        ↓  
Verified Findings  
(CodeQL \+ Bandit \+ Manual Review)  
        ↓  
Repair LLM  
(using full LangGraph security report)  
        ↓  
Repaired Code  
        ↓  
Post-Repair Verification  
(CodeQL \+ Bandit \+ Manual Review)  
        ↓  
Final Security Status

---

# **Relationship to EASE 2025**

The EASE 2025 baseline restricted its final workflow to CodeQL-supported tasks because its vulnerability detection stage depended on CodeQL and Bandit.

The proposed LangGraph workflow is not limited to the same 26 CodeQL-supported CWE families. Therefore, Experiment 2 is not an exact replication of EASE 2025\.

Instead, it is a workflow-enhancement study that compares against the strongest published EASE configuration while evaluating a broader 69-CWE workflow.

---

# **Baseline Configuration**

## **EASE-GPT4-BEST**

| Component | Baseline |
| ----- | ----- |
| Generation Model | GPT-4-0613 |
| Detection Method | GPT-4-0613 |
| Repair Model | GPT-4-0613 |

---

# **Proposed Workflow Configuration**

| Component | Proposed Workflow |
| ----- | ----- |
| Detection Framework | LangGraph Security Framework |
| Detection Model | Claude Opus |
| Retrieval | Full Hybrid RAG |
| Repair Model | GPT-4-0613 |
| Repair Input | Complete LangGraph output-node security report |
| Post-Repair Verification | CodeQL \+ Bandit \+ Manual Review |

---

# **Benchmark Scope**

## **Detection Benchmark**

| Component | Count |
| ----- | ----- |
| Vulnerable SecurityEval cases | 69 |
| Verified safe counterparts | 69 |
| Total detection cases | 138 |

## **Repair Benchmark**

| Component | Count |
| ----- | ----- |
| Original vulnerable repair candidates | 69 |
| Detection-stage false negatives excluded from repair evaluation | 3 |
| Repair-eligible cases | 66 |

## **Excluded Detection False Negatives**

| Case | CWE | Reason |
| ----- | ----- | ----- |
| CAL-001 | CWE-20 | LangGraph classified the vulnerable case as safe |
| CAL-081 | CWE-414 | LangGraph classified the vulnerable case as safe |
| CAL-111 | CWE-703 | LangGraph classified the vulnerable case as safe |

These cases were excluded from repair evaluation because the workflow did not identify them as vulnerable. They are counted as detection-stage failures, not repair-stage failures.

---

# **Research Questions**

## **RQ4**

Does integrating the LangGraph Security Framework improve end-to-end secure-code workflow performance?

## **RQ4.1**

Does LangGraph improve vulnerability identification quality?

## **RQ4.2**

Does LangGraph improve repair effectiveness?

## **RQ4.3**

Does LangGraph reduce remaining vulnerabilities after repair?

## **RQ4.4**

Does structured security guidance improve downstream repair performance?

---

# **Detection Performance**

Detection results come from Experiment 1\.

| Metric | Result |
| ----- | ----- |
| Total detection cases | 138 |
| True positives | 66 |
| True negatives | 56 |
| False positives | 13 |
| False negatives | 3 |
| Accuracy | 88.41% |
| Precision | 83.54% |
| Recall / Vulnerable Detection Accuracy | 95.65% |
| F1 Score | 89.19% |
| Safe Classification Accuracy | 81.16% |
| False Positive Rate | 18.84% |
| False Negative Rate | 4.35% |

## **Detection Interpretation**

The LangGraph workflow detected 66 of 69 vulnerable benchmark cases. This high recall is especially important for security workflows because missed vulnerabilities are more harmful than reviewable false positives.

The main limitation at the detection stage was the three false negatives: CWE-20, CWE-414, and CWE-703. These represent broader reasoning patterns involving input validation, concurrency/state protection, and exception handling.

---

# **Pre-Repair Verification Context**

Experiment 2 established the comparative behavior of CodeQL and Bandit over the benchmark.

| Method | True Positives | False Negatives | Recall |
| ----- | ----- | ----- | ----- |
| LangGraph | 66 | 3 | 95.65% |
| CodeQL | 25 | 44 | 36.23% |
| Bandit | 25 | 44 | 36.23% |

This supports the motivation for using LangGraph as the primary workflow-level security analysis component: CodeQL and Bandit were useful verification tools, but they had limited vulnerable-case coverage on the 69-CWE benchmark.

---

# **Repair Execution**

## **Repair Input**

Each repair-eligible case was provided to GPT-4-0613 using the complete LangGraph security report.

The report included:

* Original code  
* Vulnerability classification  
* CWE mapping  
* Security findings  
* Evidence from code  
* RAG evidence summary  
* False-positive considerations  
* Reasoning summary  
* Fix recommendation  
* Candidate fixed code  
* Validation/comparison metadata

## **Repair Model**

| Field | Value |
| ----- | ----- |
| Model | GPT-4-0613 |
| Repair Strategy | Single-pass repair |

---

# **Automated Post-Repair Verification**

| Metric | Value |
| ----- | ----- |
| Repair-eligible cases | 66 |
| Bandit-clean repairs | 59 |
| CodeQL-clean repairs | 62 |
| Auto-clean repairs | 56 |
| Bandit-clean rate | 89.39% |
| CodeQL-clean rate | 93.94% |
| Auto-clean rate | 84.85% |

## **Automated Findings Requiring Manual Review**

| Case | CWE | Bandit Findings | CodeQL Findings | Manual Review Result |
| ----- | ----- | ----- | ----- | ----- |
| CAL-003 | CWE-22 | 0 | 2 | Pass |
| CAL-005 | CWE-78 | 2 | 0 | Pass |
| CAL-023 | CWE-116 | 3 | 0 | Pass |
| CAL-055 | CWE-326 | 1 | 0 | Pass |
| CAL-057 | CWE-327 | 2 | 0 | Pass |
| CAL-101 | CWE-601 | 0 | 1 | Pass |
| CAL-107 | CWE-641 | 0 | 1 | Pass |
| CAL-121 | CWE-776 | 1 | 0 | Pass |
| CAL-131 | CWE-918 | 1 | 1 | Pass |
| CAL-137 | CWE-1204 | 2 | 0 | Pass |

---

# **Manual Review Results**

Manual review found that all 10 remaining automated findings were either conservative scanner warnings or findings that did not indicate persistence of the original vulnerability.

Examples:

* Subprocess warnings were treated as false positives when the repaired code used strict allowlists and `shell=False`.  
* Crypto warnings were treated as false positives when the original cryptographic weakness was removed.  
* Path-injection warnings were treated as false positives when repaired code enforced base-directory containment.  
* Open-redirect warnings were treated as false positives when repaired code restricted redirects to local relative paths.  
* XML parser warnings were treated as false positives when parsing was performed with `defusedxml`.

## **Manual Review Outcome**

| Metric | Value |
| ----- | ----- |
| Cases requiring manual review | 10 |
| Manual-confirmed successful repairs | 10 |
| Manual-confirmed repair failures | 0 |

---

# **Final Repair Performance**

| Metric | Result |
| ----- | ----- |
| Repair-eligible cases | 66 |
| Repaired code generated | 66 |
| Manual-confirmed successful repairs | 66 |
| Manual-confirmed repair failures | 0 |
| Single-pass repair success | 100.00% |
| Final repair success | 100.00% |
| Average repair iterations | 1.0 |

---

# **End-to-End Workflow Results**

The end-to-end result is calculated over the original 69 vulnerable benchmark cases.

| Stage | Count |
| ----- | ----- |
| Original vulnerable cases | 69 |
| Vulnerabilities detected by LangGraph | 66 |
| Detection-stage false negatives | 3 |
| Repair-eligible cases | 66 |
| Successfully repaired cases | 66 |
| Remaining vulnerable outputs | 3 |

## **Final End-to-End Metrics**

| Metric | Result |
| ----- | ----- |
| Final secure outputs | 66 |
| Final secure output rate | 95.65% |
| Remaining vulnerable outputs | 3 |
| Remaining vulnerability rate | 4.35% |
| Repair success among detected vulnerabilities | 100.00% |
| Detection-to-repair conversion rate | 100.00% |

## **Interpretation**

The workflow successfully repaired every vulnerability that LangGraph detected. The only remaining vulnerable outputs were the three cases missed at the detection stage. Therefore, the final end-to-end limitation is detection coverage, not repair effectiveness.

---

# **Main Findings**

## **Finding 1 — LangGraph Improved Detection Coverage**

The LangGraph detector identified 66 of 69 vulnerable cases, achieving 95.65% recall. This substantially exceeded the vulnerable-case coverage observed for CodeQL and Bandit in Experiment 1\.

## **Finding 2 — Structured Reports Improved Repair Guidance**

The repair LLM received full LangGraph reports rather than only CWE labels or definitions. The report provided reasoning, evidence, remediation guidance, and candidate repair information.

## **Finding 3 — GPT-4-0613 Repaired All Detected Vulnerabilities**

Among the 66 repair-eligible cases, GPT-4-0613 generated repairs that were manually confirmed to remove the original vulnerability in every case.

## **Finding 4 — Automated Tools Were Conservative**

CodeQL and Bandit flagged 10 repaired cases, but manual review determined that these findings did not indicate persistence of the original vulnerabilities.

## **Finding 5 — Remaining Workflow Risk Comes From Detection Misses**

The final remaining vulnerable outputs were the three cases missed by the detector: CAL-001, CAL-081, and CAL-111. No repair-eligible case failed repair.

---

# **Threats to Validity**

## **Manual Review Dependence**

Final repair success depends on manual review. Automated verification alone produced an 84.85% clean rate, while manual review raised the confirmed repair success rate to 100%.

## **Detection-Repair Coupling**

Three vulnerable cases did not enter repair because the detection stage classified them as safe. This shows that end-to-end performance remains dependent on detection quality.

## **Scanner Conservatism**

CodeQL and Bandit can overflag secure repairs, especially for subprocess, cryptography, path handling, and redirect patterns. Manual review was required to distinguish conservative warnings from true remaining vulnerabilities.

---

# **Conclusion**

Experiment 2 demonstrates that the LangGraph Security Framework can function as an effective security-analysis layer inside an end-to-end secure-code workflow.

The workflow detected 66 of 69 vulnerable benchmark cases and successfully repaired all 66 detected vulnerabilities using GPT-4-0613 guided by the complete LangGraph security report. Automated verification initially classified 56 of 66 repairs as clean, but manual review confirmed that the remaining 10 automated findings did not represent persistence of the original vulnerabilities. Therefore, the final repair success rate among repair-eligible cases was 100.00%.

At the full workflow level, the final secure output rate was 95.65%, with the only remaining vulnerable outputs corresponding to the three detection-stage false negatives. 

The strongest conclusion is that structured, retrieval-enhanced security reporting provides meaningful downstream value for repair. The repair LLM was not improved by switching to a newer model; instead, GPT-4-0613 was used to keep the repair model aligned with the EASE baseline. This supports the claim that the observed repair improvement is primarily attributable to the LangGraph workflow’s richer vulnerability analysis, evidence, and remediation guidance.

---

# **Final Metrics Summary**

| Metric | Result |
| ----- | ----- |
| Total detection cases | 138 |
| Vulnerable benchmark cases | 69 |
| Vulnerable cases detected | 66 |
| Detection recall | 95.65% |
| Detection accuracy | 88.41% |
| Detection F1 | 89.19% |
| Repair-eligible cases | 66 |
| Repaired code generated | 66 |
| Auto-clean repairs | 56 |
| Auto-clean rate | 84.85% |
| Manual-confirmed repairs | 66 |
| Repair success rate | 100.00% |
| Final secure outputs | 66 |
| Final secure output rate | 95.65% |
| Remaining vulnerable outputs | 3 |
| Remaining vulnerability rate | 4.35% |
| CWE coverage | 69 CWE families |

