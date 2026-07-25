Experiment Overview
Objective

Evaluate the end-to-end performance of the End-to-End Workflow baseline described in the EASE 2025 study using the SecurityEval benchmark. The experiment reproduces the published workflow configuration while measuring vulnerability detection, repair effectiveness, and overall secure-code generation performance under the same experimental protocol.

Unlike the LangGraph workflow evaluated separately, this experiment serves as the reference baseline against which workflow enhancements are compared. Its purpose is to establish reproducible baseline metrics for end-to-end secure code generation using GPT-4-0613 as both the detection and repair model.

Execution Methodology

The experiment followed the original End-to-End Workflow (RQ1-RQ2):

Code Generation
        ↓
Detection LLM (GPT-4-0613)
        ↓
Detected Vulnerabilities
        ↓
Repair LLM (GPT-4-0613)
        ↓
Repaired Code
        ↓
Automated Verification
        ↓
Manual Review (when required)
        ↓
Final Security Status

The workflow operated in a single-pass repair configuration. Vulnerable samples that were not detected during the detection stage did not proceed to repair and were counted as End-to-End Workflow failures.

Baseline Configuration
Component	Configuration
Baseline	End-to-End Workflow (EASE 2025)
Detection Model	GPT-4-0613
Repair Model	GPT-4-0613
Repair Strategy	Single-pass repair
Successful Repair Definition	Final status = SECURE
Dataset	SecurityEval
Vulnerable benchmark cases	69
Verified safe counterparts	69
Total benchmark cases	138
Benchmark Scope
Detection Benchmark
Component	Count
Vulnerable SecurityEval cases	69
Verified safe counterparts	69
Total benchmark cases	138
Repair Benchmark
Component	Count
Vulnerable benchmark cases	69
Detection-stage false negatives	13
Repair attempts	56
Evaluated repairs	56
Detection Performance
Metric	Result
Total detection cases	138
True Positives	56
True Negatives	59
False Positives	10
False Negatives	13
Accuracy	83.33%
Precision	84.85%
Recall	81.16%
F1 Score	82.96%
Detection Coverage	81.16%
Detection Interpretation

The End-to-End Workflow baseline correctly identified 56 of the 69 vulnerable benchmark cases. Thirteen vulnerable samples were classified as safe and therefore did not enter the repair stage. These detection misses established the upper bound on the workflow's achievable end-to-end repair performance.

Detection Confusion Matrix
	Predicted Vulnerable	Predicted Safe
Actual Vulnerable	56 (TP)	13 (FN)
Actual Safe	10 (FP)	59 (TN)
Repair Execution
Repair Configuration
Field	Value
Repair Model	GPT-4-0613
Repair Strategy	Single-pass repair
Iterative Repair	Not used
Repair Attempts	56

Only vulnerabilities successfully detected during the detection stage were submitted to the repair model.

Manual Review Summary

Automated post-repair verification identified cases requiring additional manual inspection. Final repair decisions combined automated verification with author manual review for ambiguous cases.

Metric	Result
Repair evaluation cases	56
Manual review cases	51
Automated final cases	5
Reviewer	Author
Unresolved cases	0
Final Repair Performance
Repair Status Distribution
Final Status	Cases
SECURE	31
INSECURE	15
INVALID_REPAIR	10
MANUAL_REVIEW_REQUIRED	0
Repair Metrics
Metric	Result
Repair Attempts	56
Successful Repairs	31
Repair Success Rate	55.36%
Final Secure Output Rate	44.93%
Repair Attempt Coverage	81.16%
Successful Repair Coverage	44.93%
End-to-End Workflow Results

The final workflow performance is computed over the original set of 69 vulnerable benchmark cases.

Stage	Count
Original vulnerable benchmark cases	69
Successfully detected	56
Detection-stage false negatives	13
Repair attempts	56
Secure repairs	31
Remaining vulnerable outputs	38
Final End-to-End Metrics
Metric	Result
Final Secure Outputs	31
Final Secure Output Rate	44.93%
Remaining Vulnerable Outputs	38
Remaining Vulnerability Rate	55.07%
Repair Success Among Detected Vulnerabilities	55.36%
Detection-to-Repair Conversion Rate	55.36%
Interpretation

The End-to-End Workflow baseline repaired 31 of the 56 vulnerabilities that successfully reached the repair stage, corresponding to a repair success rate of 55.36%. Detection performance limited repair coverage because thirteen vulnerable benchmark cases were not identified and therefore never entered the repair pipeline.

Across the complete benchmark of 69 vulnerable cases, the workflow produced 31 final secure outputs, yielding an end-to-end secure output rate of 44.93%. The remaining 38 vulnerable outputs consisted of thirteen detection-stage false negatives, fifteen repairs that remained insecure after repair, and ten repairs classified as invalid because the intended functionality was not preserved.

Threats to Validity
Detection–Repair Coupling

Repair performance depends directly on detection performance. Vulnerabilities not identified during the detection stage cannot proceed to repair and therefore contribute to the final end-to-end failure rate.

Manual Review Dependence

Final repair outcomes incorporate author manual review for cases requiring additional analysis beyond automated verification. Automated scanner results alone were insufficient to determine the final security status for all repaired outputs.

Benchmark Scope

The evaluation was conducted on the SecurityEval benchmark containing 69 vulnerable benchmark cases and 69 verified safe counterparts. Results should be interpreted within the scope of this benchmark.

Conclusion

The End-to-End Workflow baseline established the reference end-to-end performance for Experiment 2. Using GPT-4-0613 for both vulnerability detection and repair, the workflow detected 56 of the 69 vulnerable benchmark cases and successfully repaired 31 of those detected vulnerabilities.

The experiment achieved a repair success rate of 55.36% among repair attempts and a final secure output rate of 44.93% across the complete benchmark. These results provide the baseline against which the proposed LangGraph-enhanced workflow is evaluated in subsequent analyses.

Final Metrics Summary
Metric	Result
Total benchmark cases	138
Vulnerable benchmark cases	69
Detection Accuracy	83.33%
Detection Precision	84.85%
Detection Recall	81.16%
Detection F1 Score	82.96%
Repair Attempts	56
Successful Repairs	31
Repair Success Rate	55.36%
Final Secure Outputs	31
Final Secure Output Rate	44.93%
Remaining Vulnerable Outputs	38
Remaining Vulnerability Rate	55.07%