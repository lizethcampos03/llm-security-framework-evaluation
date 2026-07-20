# Experiment 1 - Bandit Full Benchmark Report

Generated: 20260611_100317

## Method

- Bandit was run on each prepared benchmark file from the Experiment 2 source tree.
- Any Bandit finding was counted as a vulnerability detection.
- Results were compared against the manifest ground-truth label.

## Metrics

| Metric | Value |
|---|---:|
| total_cases | 138 |
| correct_cases | 85 |
| true_positives | 25 |
| true_negatives | 60 |
| false_positives | 9 |
| false_negatives | 44 |
| accuracy | 0.6159 |
| precision | 0.7353 |
| recall | 0.3623 |
| f1 | 0.4854 |
| safe_accuracy | 0.8696 |
| average_latency_seconds | 1.057 |

## Incorrect Cases

| Case | CWE | Expected | Detected | Outcome | Findings | Rules | CWEs |
|---|---|---|---|---|---:|---|---|
| CWE-841_vulnerable | CWE-841 | vulnerable | safe | FN | 0 |  |  |
| CWE-113_vulnerable | CWE-113 | vulnerable | safe | FN | 0 |  |  |
| CWE-116_safe | CWE-116 | safe | vulnerable | FP | 3 | B404; B603; B607 | CWE-78 |
| CWE-117_vulnerable | CWE-117 | vulnerable | safe | FN | 0 |  |  |
| CWE-1204_safe | CWE-1204 | safe | vulnerable | FP | 2 | B413 | CWE-327 |
| CWE-193_vulnerable | CWE-193 | vulnerable | safe | FN | 0 |  |  |
| CWE-20_vulnerable | CWE-20 | vulnerable | safe | FN | 0 |  |  |
| CWE-200_vulnerable | CWE-200 | vulnerable | safe | FN | 0 |  |  |
| CWE-209_vulnerable | CWE-209 | vulnerable | safe | FN | 0 |  |  |
| CWE-22_vulnerable | CWE-22 | vulnerable | safe | FN | 0 |  |  |
| CWE-250_vulnerable | CWE-250 | vulnerable | safe | FN | 0 |  |  |
| CWE-252_vulnerable | CWE-252 | vulnerable | safe | FN | 0 |  |  |
| CWE-269_vulnerable | CWE-269 | vulnerable | safe | FN | 0 |  |  |
| CWE-283_vulnerable | CWE-283 | vulnerable | safe | FN | 0 |  |  |
| CWE-285_vulnerable | CWE-285 | vulnerable | safe | FN | 0 |  |  |
| CWE-295_vulnerable | CWE-295 | vulnerable | safe | FN | 0 |  |  |
| CWE-306_vulnerable | CWE-306 | vulnerable | safe | FN | 0 |  |  |
| CWE-319_vulnerable | CWE-319 | vulnerable | safe | FN | 0 |  |  |
| CWE-326_safe | CWE-326 | safe | vulnerable | FP | 1 | B413 | CWE-327 |
| CWE-327_safe | CWE-327 | safe | vulnerable | FP | 1 | B413 | CWE-327 |
| CWE-329_safe | CWE-329 | safe | vulnerable | FP | 1 | B413 | CWE-327 |
| CWE-347_vulnerable | CWE-347 | vulnerable | safe | FN | 0 |  |  |
| CWE-367_vulnerable | CWE-367 | vulnerable | safe | FN | 0 |  |  |
| CWE-385_vulnerable | CWE-385 | vulnerable | safe | FN | 0 |  |  |
| CWE-400_vulnerable | CWE-400 | vulnerable | safe | FN | 0 |  |  |
| CWE-406_vulnerable | CWE-406 | vulnerable | safe | FN | 0 |  |  |
| CWE-414_vulnerable | CWE-414 | vulnerable | safe | FN | 0 |  |  |
| CWE-425_vulnerable | CWE-425 | vulnerable | safe | FN | 0 |  |  |
| CWE-434_vulnerable | CWE-434 | vulnerable | safe | FN | 0 |  |  |
| CWE-454_safe | CWE-454 | safe | vulnerable | FP | 1 | B105 | CWE-259 |
| CWE-462_vulnerable | CWE-462 | vulnerable | safe | FN | 0 |  |  |
| CWE-477_vulnerable | CWE-477 | vulnerable | safe | FN | 0 |  |  |
| CWE-521_vulnerable | CWE-521 | vulnerable | safe | FN | 0 |  |  |
| CWE-522_vulnerable | CWE-522 | vulnerable | safe | FN | 0 |  |  |
| CWE-595_vulnerable | CWE-595 | vulnerable | safe | FN | 0 |  |  |
| CWE-601_vulnerable | CWE-601 | vulnerable | safe | FN | 0 |  |  |
| CWE-611_vulnerable | CWE-611 | vulnerable | safe | FN | 0 |  |  |
| CWE-641_vulnerable | CWE-641 | vulnerable | safe | FN | 0 |  |  |
| CWE-643_vulnerable | CWE-643 | vulnerable | safe | FN | 0 |  |  |
| CWE-703_vulnerable | CWE-703 | vulnerable | safe | FN | 0 |  |  |
| CWE-730_vulnerable | CWE-730 | vulnerable | safe | FN | 0 |  |  |
| CWE-732_safe | CWE-732 | safe | vulnerable | FP | 1 | B605 | CWE-78 |
| CWE-760_vulnerable | CWE-760 | vulnerable | safe | FN | 0 |  |  |
| CWE-78_safe | CWE-78 | safe | vulnerable | FP | 2 | B404; B603 | CWE-78 |
| CWE-79_vulnerable | CWE-79 | vulnerable | safe | FN | 0 |  |  |
| CWE-80_vulnerable | CWE-80 | vulnerable | safe | FN | 0 |  |  |
| CWE-827_vulnerable | CWE-827 | vulnerable | safe | FN | 0 |  |  |
| CWE-835_vulnerable | CWE-835 | vulnerable | safe | FN | 0 |  |  |
| CWE-90_vulnerable | CWE-90 | vulnerable | safe | FN | 0 |  |  |
| CWE-918_safe | CWE-918 | safe | vulnerable | FP | 1 | B113 | CWE-400 |
| CWE-941_vulnerable | CWE-941 | vulnerable | safe | FN | 0 |  |  |
| CWE-943_vulnerable | CWE-943 | vulnerable | safe | FN | 0 |  |  |
| CWE-99_vulnerable | CWE-99 | vulnerable | safe | FN | 0 |  |  |