# Experiment 2 Benchmark Log

## Secure Code Agent Baseline with GPT-5.5 Repair

**Detection:** GPT-4-0613  
**Repair:** GPT-5.5

> **Purpose:** Evaluate how replacing the baseline repair model with GPT-5.5 changes repair effectiveness while preserving the original GPT-4-0613 detection stage.

| **Field**                | **Value**                              |
|--------------------------|----------------------------------------|
| Experiment               | experiment2_secure_code_agent_baseline |
| Protocol                 | Single-pass repair                     |
| Detection model          | GPT-4-0613                             |
| Repair model             | GPT-5.5                                |
| Generated at             | 2026-07-24 05:37:46 UTC                |
| Successful repair status | SECURE                                 |

# Experiment Overview

## Objective

Evaluate the end-to-end performance of the Secure Code Agent workflow when GPT-5.5 is used as the repair model while the reproduced GPT-4-0613 detection stage remains unchanged.

This configuration isolates the contribution of a newer repair model. The detection records, benchmark composition, repair eligibility rules, and final security-status definitions remain consistent with the Secure Code Agent baseline. Therefore, changes in repair outcomes can be attributed primarily to the repair-model substitution.

## Evaluation Question

How effectively does GPT-5.5 repair vulnerabilities detected by the reproduced Secure Code Agent detection stage, and what final secure-output rate does the resulting end-to-end workflow achieve?

# Execution Methodology

The workflow followed the sequence below:

1. Evaluate 69 vulnerable and 69 verified-safe benchmark samples with GPT-4-0613.
2. Send only correctly detected vulnerable samples to the repair stage.
3. Generate one repair per eligible sample using GPT-5.5.
4. Evaluate repaired code with automated scanners and syntax validation.
5. Apply author manual review to cases requiring semantic judgment.
6. Assign one final status: SECURE, INSECURE, or INVALID_REPAIR.

## Workflow

**SecurityEval Benchmark (138 samples)**

↓

**GPT-4-0613 Detection**

↓

**56 Detected Vulnerable Cases**

↓

**GPT-5.5 Single-Pass Repair**

↓

**Automated Evaluation + Author Manual Review**

↓

**Final Security Status**

# Configuration

| **Component**                | **Configuration**          |
|------------------------------|----------------------------|
| Configuration name           | secure_code_agent_baseline |
| Detection model              | GPT-4-0613                 |
| Repair model                 | GPT-5.5                    |
| Repair strategy              | Single-pass repair         |
| Repair output                | repair_gpt55               |
| Repair evaluation output     | repair_evaluation_gpt55    |
| Metrics output               | metrics_gpt55              |
| Successful repair definition | Final status = SECURE      |

## Run Provenance

| **Stage**             | **Run ID**                |
|-----------------------|---------------------------|
| Detection run 1       | 20260723T170530Z_cdbd14c5 |
| Detection run 2       | 20260723T171922Z_cf0dd8b9 |
| Repair run            | 20260724T005516Z_b49019c6 |
| Repair evaluation run | 20260724T014803Z_64bf1b9a |

# Benchmark Scope

## Detection Benchmark

| **Dataset Component**           | **Count** |
|---------------------------------|-----------|
| SecurityEval vulnerable samples | 69        |
| Verified safe counterparts      | 69        |
| Total detection samples         | 138       |
| Unique vulnerable CWE families  | 69        |

## Repair Benchmark

| **Pipeline Component**          | **Count** |
|---------------------------------|-----------|
| Original vulnerable samples     | 69        |
| Detected vulnerable samples     | 56        |
| Detection-stage false negatives | 13        |
| Repair attempts                 | 56        |
| Evaluated repairs               | 56        |

# Detection Performance

| **Metric**              | **Result** |
|-------------------------|------------|
| Total detection samples | 138        |
| True positives          | 56         |
| True negatives          | 59         |
| False positives         | 10         |
| False negatives         | 13         |
| Accuracy                | 83.33%     |
| Precision               | 84.85%     |
| Recall                  | 81.16%     |
| F1 score                | 82.96%     |
| Detection coverage      | 81.16%     |

## Detection Confusion Matrix

| **Actual Class**  | **Predicted Vulnerable** | **Predicted Safe** |
|-------------------|--------------------------|--------------------|
| Actual Vulnerable | 56 (TP)                  | 13 (FN)            |
| Actual Safe       | 10 (FP)                  | 59 (TN)            |

## Detection Interpretation

GPT-4-0613 detected 56 of the 69 vulnerable benchmark cases. The 13 false negatives did not enter the repair stage, so detection coverage limited the maximum possible end-to-end secure-output rate to 81.16%.

The detection results are identical to the reproduced Secure Code Agent baseline because the detection model and records were intentionally held constant.

# GPT-5.5 Repair Execution

## Repair Input and Strategy

Each of the 56 correctly detected vulnerable samples was provided to GPT-5.5 for a single repair attempt. No iterative repair loop was used. A repair counted as successful only when the finalized evaluation status was SECURE.

| **Field**                     | **Value**   |
|-------------------------------|-------------|
| Repair model                  | GPT-5.5     |
| Repair strategy               | Single pass |
| Repair attempts               | 56          |
| Evaluated repairs             | 56          |
| Average repair iterations     | 1.0         |
| All repair attempts evaluated | Yes         |

## Post-Repair Evaluation

Post-repair evaluation combined syntax validation, Bandit, CodeQL, and author manual review. Automated statuses were retained for cases with definitive scanner findings. Cases requiring semantic judgment were finalized using the completed manual-review decision file.

# Manual Review Summary

| **Metric**                               | **Result** |
|------------------------------------------|------------|
| Repair evaluation cases                  | 56         |
| Cases requiring manual review            | 51         |
| Completed author decisions used          | 51         |
| Automated final cases retained           | 5          |
| Blank manual entries for automated cases | 5          |
| Unresolved cases                         | 0          |
| Reviewer                                 | Author     |

Manual decisions were applied only when the automated evaluation status was MANUAL_REVIEW_REQUIRED. Existing automated SECURE, INSECURE, or INVALID_REPAIR statuses were retained without being overwritten.

# Final Repair Performance

## Final Status Distribution

| **Final Status**       | **Count** | **Share of 56 Repairs** |
|------------------------|-----------|-------------------------|
| SECURE                 | 46        | 82.14%                  |
| INSECURE               | 9         | 16.07%                  |
| INVALID_REPAIR         | 1         | 1.79%                   |
| MANUAL_REVIEW_REQUIRED | 0         | 0.00%                   |

## Repair Metrics

| **Metric**                     | **Result** |
|--------------------------------|------------|
| Repair success rate            | 82.14%     |
| Evaluated repair success rate  | 82.14%     |
| Final secure output rate       | 66.67%     |
| Repair attempt coverage        | 81.16%     |
| Successful repair CWE coverage | 66.67%     |

## Repair Interpretation

GPT-5.5 produced 46 secure repairs among the 56 detected vulnerable cases, yielding an 82.14% repair success rate. Nine repairs remained insecure and one was classified as invalid because meaningful intended functionality was not securely preserved.

Because every repair attempt was evaluated, repair success rate and evaluated repair success rate are identical.

# End-to-End Workflow Results

| **Stage**                           | **Count** |
|-------------------------------------|-----------|
| Original vulnerable benchmark cases | 69        |
| Vulnerabilities detected            | 56        |
| Detection-stage false negatives     | 13        |
| Repair attempts                     | 56        |
| Final secure repairs                | 46        |
| Insecure repaired outputs           | 9         |
| Invalid repaired outputs            | 1         |
| Total remaining non-secure outputs  | 23        |

## Final End-to-End Metrics

| **Metric**                                    | **Result** |
|-----------------------------------------------|------------|
| Final secure outputs                          | 46         |
| Final secure output rate                      | 66.67%     |
| Remaining non-secure outputs                  | 23         |
| Remaining non-secure output rate              | 33.33%     |
| Repair success among detected vulnerabilities | 82.14%     |
| Detection-stage repair eligibility            | 81.16%     |

## End-to-End Interpretation

Across the complete set of 69 vulnerable benchmark cases, the workflow produced 46 final secure outputs. The remaining 23 non-secure outputs consisted of 13 vulnerabilities missed at detection, nine repairs that remained insecure, and one invalid repair.

The final secure output rate was 66.67%. Therefore, both detection misses and unsuccessful repairs contributed to the remaining workflow risk, although repair performance was substantially stronger than in the GPT-4-0613 repair baseline.

# Comparison with the GPT-4-0613 Repair Baseline

| **Metric**               | **GPT-4-0613 Repair** | **GPT-5.5 Repair** | **Change** |
|--------------------------|-----------------------|--------------------|------------|
| Detection accuracy       | 83.33%                | 83.33%             | No change  |
| Detection recall         | 81.16%                | 81.16%             | No change  |
| Repair success rate      | 55.36%                | 82.14%             | +26.79 pp  |
| Final secure output rate | 44.93%                | 66.67%             | +21.74 pp  |
| Secure repairs           | 31                    | 46                 | +15        |
| Insecure repairs         | 15                    | 9                  | -6         |
| Invalid repairs          | 10                    | 1                  | -9         |

## Comparison Interpretation

Replacing GPT-4-0613 with GPT-5.5 at the repair stage increased successful repairs from 31 to 46. The repair success rate improved by 26.79 percentage points, while the full-workflow secure-output rate improved by 21.74 percentage points.

Detection results remained identical because the same GPT-4-0613 detection outputs were reused. The observed improvement is therefore attributable to stronger repair performance rather than better vulnerability identification.

# Main Findings

## Finding 1 — Detection remained the same.

The GPT-5.5 configuration reused the reproduced GPT-4-0613 detector, so detection accuracy, recall, F1, and repair eligibility were unchanged.

## Finding 2 — GPT-5.5 substantially improved repair success.

GPT-5.5 secured 46 of 56 detected vulnerable cases, compared with 31 secure repairs under the GPT-4-0613 repair baseline.

## Finding 3 — Invalid repairs decreased sharply.

Only one GPT-5.5 repair was classified as invalid, compared with ten invalid repairs in the GPT-4-0613 repair baseline.

## Finding 4 — End-to-end performance remained constrained by detection misses.

Thirteen vulnerable cases never entered repair, limiting the maximum achievable secure-output rate.

## Finding 5 — Manual review remained essential.

Fifty-one cases required author review to determine whether the original weakness was removed, whether a replacement weakness was introduced, and whether functionality was preserved.

# Threats to Validity

## Detection–Repair Coupling

Only vulnerabilities detected by GPT-4-0613 entered the repair stage. Consequently, repair metrics describe performance on detected vulnerable cases, while the final secure-output rate captures the complete workflow.

## Manual Review Dependence

Final repair outcomes depend on author judgment for 51 cases. The review process used explicit criteria, including target-CWE removal, replacement weaknesses, and preservation of intended functionality, but semantic security review may still involve judgment.

## Single-Pass Protocol

The experiment measured one repair attempt per detected vulnerability. Results do not represent the performance of an iterative repair loop that could use evaluation feedback to generate additional revisions.

## Benchmark Scope

The experiment used 69 SecurityEval CWE tasks and verified safe counterparts. Performance may differ on larger, multi-file, production, or chained-vulnerability scenarios.

## Model Version Specificity

The repair results correspond to the observed GPT-5.5 model configuration and recorded run. Future model versions or provider-side changes may produce different outputs.

# Conclusion

The Secure Code Agent configuration using GPT-4-0613 for detection and GPT-5.5 for repair achieved substantially stronger repair performance than the reproduced GPT-4-0613 repair baseline.

GPT-5.5 generated 46 secure repairs from 56 repair attempts, corresponding to an 82.14% repair success rate. Across all 69 vulnerable benchmark cases, the workflow achieved a 66.67% final secure-output rate.

The results show that repair-model capability materially affects end-to-end secure-code workflow performance. However, the 13 detection-stage false negatives remained outside the repair pipeline, demonstrating that stronger repair alone cannot eliminate risk created by incomplete vulnerability detection.

# Final Metrics Summary

| **Metric**                       | **Result** |
|----------------------------------|------------|
| Total detection samples          | 138        |
| Vulnerable benchmark cases       | 69         |
| Detection accuracy               | 83.33%     |
| Detection precision              | 84.85%     |
| Detection recall                 | 81.16%     |
| Detection F1                     | 82.96%     |
| Vulnerable cases detected        | 56         |
| Repair attempts                  | 56         |
| Secure repairs                   | 46         |
| Insecure repairs                 | 9          |
| Invalid repairs                  | 1          |
| Repair success rate              | 82.14%     |
| Final secure outputs             | 46         |
| Final secure output rate         | 66.67%     |
| Remaining non-secure outputs     | 23         |
| Remaining non-secure output rate | 33.33%     |
| Manual-review decisions used     | 51         |
| Unresolved review cases          | 0          |
