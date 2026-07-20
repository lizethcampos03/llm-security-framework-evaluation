# **Experiment 3 Log – Chained Vulnerability Evaluation**

---

# **LangGraph-Orchestrated Chained Vulnerability Reasoning Evaluation**

---

# **Document Outline**

1. Purpose and Experiment Scope  
2. Research Question  
3. Motivation  
4. Final Architecture Under Test  
5. Benchmark Design  
6. Evaluation Methodology  
7. Aggregate Results  
8. Scenario-Level Results  
9. Experimental Observations  
10. Limitations  
11. Final Assessment

---

# **1\. Purpose and Experiment Scope**

This document records the final execution results for **Experiment 3**, which evaluates the proposed chained-vulnerability reasoning extension of the LangGraph Security Framework. Unlike Experiments 1 and 2, which focused on vulnerability detection and downstream repair, this experiment investigates whether the architecture can reason about relationships among multiple independently detected weaknesses to identify representative multi-step attack paths.

The objective is not to construct complete attack graphs or perform exhaustive exploit-path analysis. Instead, this experiment evaluates whether the proposed workflow can successfully extend beyond isolated vulnerability detection toward preliminary attack-path reasoning by combining multiple findings with contextual software understanding and CAPEC/CWE knowledge.

The experiment serves as an exploratory evaluation of the framework's ability to identify candidate vulnerability chains, confirm chained attack paths, and generate remediation strategies capable of disrupting those chains.

---

# **2\. Research Question**

**RQ5**

Can the proposed LangGraph Security Framework extend beyond isolated vulnerability detection to identify representative chained vulnerabilities, reason about multi-step attack paths, and generate repair strategies capable of disrupting those attack chains?

---

# **3\. Motivation**

Modern cyberattacks rarely rely on a single isolated vulnerability. Instead, attackers frequently combine multiple weaknesses across software components to achieve privilege escalation, sensitive information disclosure, remote code execution, or unauthorized system access.

Traditional vulnerability scanners primarily evaluate weaknesses independently and generally do not reason about how individually benign findings may combine into a larger attack path. Motivated by this limitation, Experiment 3 evaluates a preliminary extension of the proposed framework that performs chain-level reasoning after individual vulnerabilities have been identified.

The chained-vulnerability extension integrates:

* Context-aware software profiles  
* Hybrid RAG retrieval  
* CWE knowledge  
* CAPEC attack-pattern knowledge  
* Structured security reasoning  
* Chain-level repair planning

Rather than replacing traditional vulnerability detection, this extension investigates whether retrieval-enhanced orchestration can provide an additional reasoning layer capable of identifying representative attack paths across multiple related weaknesses. This aligns with the paper's goal of extending the framework toward early-stage attack-path reasoning rather than presenting a complete attack-graph solution.

---

# **4\. Final Architecture Under Test**

The chained-vulnerability experiment evaluated the finalized LangGraph architecture with an additional reasoning stage following individual vulnerability detection.

| Stage | Role in Experiment |
| ----- | ----- |
| Input / Preprocess | Receives multiple vulnerable software components together with the associated context profile. |
| Hybrid RAG | Retrieves relevant CWE knowledge, CAPEC attack patterns, vulnerable examples, and secure examples. |
| Individual Vulnerability Detection | Identifies vulnerabilities independently within each component. |
| Chain Reasoning Node | Evaluates relationships among validated vulnerabilities to determine whether they form a representative attack chain. |
| Chain Repair Planner | Generates a coordinated mitigation strategy intended to interrupt the attack path. |
| Output Node | Produces the final structured chain analysis report, including evidence, reasoning, attack-path assessment, and repair recommendations. |

---

# **5\. Benchmark Design**

The benchmark consists of four representative chained-vulnerability scenarios spanning multiple application domains. Each scenario combines multiple vulnerabilities that commonly appear together in realistic attack sequences.

| Property | Value |
| ----- | ----- |
| Representative chain scenarios | 4 |
| Context profiles | 4 |
| Software domains | Cloud, Web/Social, Financial, Developer Platform |
| Evaluation objective | Candidate chain identification, attack-path reasoning, and chain-level repair planning |

The benchmark includes the following representative scenarios:

| Chain | Context Profile |
| ----- | ----- |
| Cloud Credential Exposure Chain | Cloud Management Platform |
| Path Traversal Secret Disclosure Chain | Web/Social Platform |
| Privileged Transaction Access Chain | Financial Application |
| Code Injection Sensitive Operation Chain | Developer Platform |

---

# **6\. Evaluation Methodology**

Each representative scenario was executed using the finalized chained-vulnerability workflow.

The evaluation proceeded through the following stages:

1. Detect individual vulnerabilities within each software component.  
2. Determine whether the detected weaknesses collectively represent a candidate attack chain.  
3. Use retrieved CWE and CAPEC evidence to reason about exploit relationships.  
4. Confirm whether a valid chained attack path exists.  
5. Generate a coordinated repair strategy intended to disrupt the attack chain.  
6. Manually review the generated reasoning and repair recommendations.

The following evaluation criteria were recorded for every scenario.

| Metric | Interpretation |
| ----- | ----- |
| Individual Vulnerabilities Detected | Whether the component vulnerabilities were successfully identified. |
| Candidate Chain Triggered | Whether the workflow recognized a potential chained attack. |
| Attack Path Confirmed | Whether the reasoning stage confirmed a valid attack sequence. |
| CAPEC/CWE Evidence Used | Whether external security knowledge supported the reasoning process. |
| Repair Plan Generated | Whether a coordinated chain-level remediation strategy was produced. |
| Repair Breaks Chain | Whether the proposed remediation interrupts the attack path. |
| Manual Review Status | Human verification of the generated reasoning and repair assessment. |

---

# **7\. Aggregate Results**

The proposed framework successfully identified representative chained-vulnerability candidates in all benchmark scenarios.

Three of the four scenarios progressed beyond candidate identification and were confirmed as valid chained attack paths through structured reasoning supported by retrieved CAPEC and CWE evidence. Corresponding repair plans were generated for these confirmed chains, and manual review verified that the proposed mitigations would interrupt the representative attack paths.

| Metric | Result |
| ----- | ----- |
| Representative chain scenarios | 4 |
| Individual vulnerabilities detected | **4 / 4 (100%)** |
| Candidate chains identified | **4 / 4 (100%)** |
| Confirmed chained attack paths | **3 / 4 (75%)** |
| CAPEC/CWE-supported reasoning | **4 / 4 (100%)** |
| Chain repair plans generated | **3 / 4 (75%)** |
| Repair plans successfully breaking the chain | **3 / 4 (75%)** |
| Manual review confirmation | **4 / 4 (100%)** |

These aggregate results are consistent with the paper's summary that the framework identified candidate chains in all four representative scenarios while confirming three chained attack paths.

---

# **8\. Scenario-Level Results**

---

## **8.1 Cloud Credential Exposure Chain**

**Context Profile**

Cloud Management Platform

**Expected Chain**

CWE-918 → CWE-200 → CWE-306

**Detected Vulnerabilities**

* CWE-306  
* CWE-798  
* CWE-89  
* CWE-918

| Evaluation | Result |
| ----- | ----- |
| Individual vulnerabilities detected | ✓ |
| Candidate chain identified | ✓ |
| Attack path confirmed | ✓ |
| CAPEC/CWE evidence incorporated | ✓ |
| Repair plan generated | ✓ |
| Proposed repair breaks attack chain | ✓ |
| Manual review | **Confirmed** |

**Interpretation**

The framework successfully identified the representative cloud attack chain, incorporated retrieved security knowledge during reasoning, and generated a coordinated remediation strategy capable of interrupting the attack sequence.

---

## **8.2 Path Traversal Secret Disclosure Chain**

**Context Profile**

Web/Social Platform

**Expected Chain**

CWE-22 → CWE-200 → CWE-798

**Detected Vulnerabilities**

* CWE-209  
* CWE-22  
* CWE-798  
* CWE-89

| Evaluation | Result |
| ----- | ----- |
| Individual vulnerabilities detected | ✓ |
| Candidate chain identified | ✓ |
| Attack path confirmed | ✓ |
| CAPEC/CWE evidence incorporated | ✓ |
| Repair plan generated | ✓ |
| Proposed repair breaks attack chain | ✓ |
| Manual review | **Confirmed** |

**Interpretation**

The reasoning workflow correctly associated multiple related weaknesses into a representative chained attack and generated a coordinated repair strategy addressing the overall exploit path rather than isolated vulnerabilities.

---

## **8.3 Privileged Transaction Access Chain**

**Context Profile**

Financial Application

**Expected Chain**

CWE-798 → CWE-306

**Detected Vulnerabilities**

* CWE-306  
* CWE-798

| Evaluation | Result |
| ----- | ----- |
| Individual vulnerabilities detected | ✓ |
| Candidate chain identified | ✓ |
| Attack path confirmed | ✓ |
| CAPEC/CWE evidence incorporated | ✓ |
| Repair plan generated | ✓ |
| Proposed repair breaks attack chain | ✓ |
| Manual review | **Confirmed** |

**Interpretation**

The framework successfully recognized the relationship between authentication weaknesses and privileged transaction access, producing a coherent chain-level repair strategy.

---

## **8.4 Code Injection Sensitive Operation Chain**

**Context Profile**

Developer Platform

**Expected Chain**

CWE-94 → CWE-200

**Detected Vulnerabilities**

* CWE-209  
* CWE-89  
* CWE-94

| Evaluation | Result |
| ----- | ----- |
| Individual vulnerabilities detected | ✓ |
| Candidate chain identified | ✓ |
| Attack path confirmed | ✗ |
| CAPEC/CWE evidence incorporated | ✓ |
| Repair plan generated | ✗ |
| Proposed repair breaks attack chain | ✗ |
| Manual review | **Confirmed** |

**Interpretation**

The framework successfully detected the constituent vulnerabilities and recognized the possibility of a chained attack. However, the reasoning stage did not confirm sufficient evidence to establish a complete representative attack path, and therefore no coordinated chain-level repair strategy was produced.

---

# **9\. Experimental Observations**

Several consistent patterns emerged during the evaluation.

The individual vulnerability detector successfully identified vulnerabilities across all representative scenarios, providing a reliable foundation for downstream reasoning.

Candidate chain identification succeeded in every scenario, indicating that the framework consistently recognized meaningful relationships among independently detected weaknesses.

Retrieved CWE descriptions and CAPEC attack-pattern knowledge contributed to reasoning throughout the benchmark, demonstrating that retrieval augmentation supported chain-level analysis beyond isolated vulnerability classification.

The primary limitation occurred during attack-path confirmation rather than vulnerability detection. The developer-platform scenario illustrates that identifying multiple related weaknesses does not necessarily imply the existence of a sufficiently supported exploit chain. This distinction suggests that future improvements should focus on strengthening multi-step reasoning rather than expanding vulnerability detection alone.

---

# **10\. Limitations**

This experiment represents an exploratory evaluation rather than a comprehensive attack-graph framework.

Several limitations remain:

* Only four representative chained-vulnerability scenarios were evaluated.  
* The benchmark emphasizes representative attack reasoning rather than exhaustive attack-path enumeration.  
* Dynamic exploit validation was not performed.  
* Chain confirmation relied on structured LLM reasoning supported by retrieved security knowledge and subsequent manual review.  
* Larger-scale evaluation across additional software ecosystems remains future work.

---

# **11\. Final Assessment**

Experiment 3 demonstrates that the proposed LangGraph Security Framework can extend beyond isolated vulnerability detection toward structured reasoning about representative chained attacks.

Across four representative scenarios, the framework successfully detected the constituent vulnerabilities in every case, identified candidate attack chains in all scenarios, confirmed three representative chained attack paths, and generated coordinated remediation strategies capable of disrupting those confirmed attack sequences.

Although additional research is needed to support large-scale attack-graph construction and more complex exploit reasoning, these preliminary results demonstrate that retrieval-enhanced orchestration can provide meaningful chain-level security analysis while remaining consistent with the broader architecture presented throughout the paper. This complements the paper's conclusion that the chained-vulnerability extension is an initial step toward attack-path reasoning rather than a complete attack-graph solution.

