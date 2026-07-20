# Experiment 1 - CodeQL Full Benchmark Report

Generated: 20260611_093617

## Configuration

- CodeQL database: `D:\vuln-tool\outputs\experiment1_static_baselines\codeql_db`
- Query suite: `codeql/python-queries:codeql-suites/python-security-and-quality.qls`
- SARIF output: `D:\vuln-tool\outputs\experiment1_static_baselines\experiment1_codeql_full_results_20260611_081837.sarif`
- Security filter: counts only rules tagged as `security` or `external/cwe/*`.
- Non-security quality findings are ignored for vulnerability metrics.

## Method

- This report reprocesses the original CodeQL SARIF output.
- CodeQL was not rerun.
- The evaluator excludes known quality-only rules from vulnerability metrics.

## Excluded Non-Security Rule IDs

- `py/mixed-returns`
- `py/regex/unmatchable-caret`
- `py/regex/unmatchable-dollar`
- `py/unused-import`
- `py/unused-local-variable`

## Metrics

| Metric | Value |
|---|---:|
| total_cases | 138 |
| correct_cases | 90 |
| true_positives | 25 |
| true_negatives | 65 |
| false_positives | 4 |
| false_negatives | 44 |
| accuracy | 0.6522 |
| precision | 0.8621 |
| recall | 0.3623 |
| f1 | 0.5102 |
| safe_accuracy | 0.942 |

## Incorrect Cases

| Case | CWE | Expected | Detected | Outcome | Security Findings | Rules | Ignored Rules |
|---|---|---|---|---|---:|---|---|
| CWE-113_safe | CWE-113 | safe | vulnerable | FP | 1 | py/url-redirection |  |
| CWE-117_vulnerable | CWE-117 | vulnerable | safe | FN | 0 |  |  |
| CWE-1204_vulnerable | CWE-1204 | vulnerable | safe | FN | 0 |  |  |
| CWE-193_vulnerable | CWE-193 | vulnerable | safe | FN | 0 |  |  |
| CWE-22_safe | CWE-22 | safe | vulnerable | FP | 2 | py/path-injection |  |
| CWE-250_vulnerable | CWE-250 | vulnerable | safe | FN | 0 |  |  |
| CWE-252_vulnerable | CWE-252 | vulnerable | safe | FN | 0 |  |  |
| CWE-259_vulnerable | CWE-259 | vulnerable | safe | FN | 0 |  |  |
| CWE-269_vulnerable | CWE-269 | vulnerable | safe | FN | 0 |  |  |
| CWE-283_vulnerable | CWE-283 | vulnerable | safe | FN | 0 |  |  |
| CWE-285_vulnerable | CWE-285 | vulnerable | safe | FN | 0 |  |  |
| CWE-295_vulnerable | CWE-295 | vulnerable | safe | FN | 0 |  |  |
| CWE-306_vulnerable | CWE-306 | vulnerable | safe | FN | 0 |  |  |
| CWE-321_vulnerable | CWE-321 | vulnerable | safe | FN | 0 |  |  |
| CWE-329_vulnerable | CWE-329 | vulnerable | safe | FN | 0 |  |  |
| CWE-330_vulnerable | CWE-330 | vulnerable | safe | FN | 0 |  |  |
| CWE-331_vulnerable | CWE-331 | vulnerable | safe | FN | 0 |  |  |
| CWE-339_vulnerable | CWE-339 | vulnerable | safe | FN | 0 |  |  |
| CWE-347_vulnerable | CWE-347 | vulnerable | safe | FN | 0 |  |  |
| CWE-367_vulnerable | CWE-367 | vulnerable | safe | FN | 0 |  |  |
| CWE-385_vulnerable | CWE-385 | vulnerable | safe | FN | 0 |  |  |
| CWE-406_vulnerable | CWE-406 | vulnerable | safe | FN | 0 |  |  |
| CWE-414_vulnerable | CWE-414 | vulnerable | safe | FN | 0 |  |  |
| CWE-425_vulnerable | CWE-425 | vulnerable | safe | FN | 0 |  |  |
| CWE-454_vulnerable | CWE-454 | vulnerable | safe | FN | 0 |  |  |
| CWE-462_vulnerable | CWE-462 | vulnerable | safe | FN | 0 |  |  |
| CWE-477_vulnerable | CWE-477 | vulnerable | safe | FN | 0 |  |  |
| CWE-502_vulnerable | CWE-502 | vulnerable | safe | FN | 0 |  |  |
| CWE-521_vulnerable | CWE-521 | vulnerable | safe | FN | 0 |  |  |
| CWE-522_vulnerable | CWE-522 | vulnerable | safe | FN | 0 |  |  |
| CWE-595_vulnerable | CWE-595 | vulnerable | safe | FN | 0 |  |  |
| CWE-601_safe | CWE-601 | safe | vulnerable | FP | 1 | py/url-redirection |  |
| CWE-643_vulnerable | CWE-643 | vulnerable | safe | FN | 0 |  |  |
| CWE-703_vulnerable | CWE-703 | vulnerable | safe | FN | 0 |  | py/mixed-returns |
| CWE-730_vulnerable | CWE-730 | vulnerable | safe | FN | 0 |  | py/regex/unmatchable-caret; py/regex/unmatchable-dollar |
| CWE-760_vulnerable | CWE-760 | vulnerable | safe | FN | 0 |  |  |
| CWE-78_vulnerable | CWE-78 | vulnerable | safe | FN | 0 |  |  |
| CWE-798_vulnerable | CWE-798 | vulnerable | safe | FN | 0 |  |  |
| CWE-827_vulnerable | CWE-827 | vulnerable | safe | FN | 0 |  |  |
| CWE-835_vulnerable | CWE-835 | vulnerable | safe | FN | 0 |  |  |
| CWE-841_vulnerable | CWE-841 | vulnerable | safe | FN | 0 |  |  |
| CWE-89_vulnerable | CWE-89 | vulnerable | safe | FN | 0 |  |  |
| CWE-90_vulnerable | CWE-90 | vulnerable | safe | FN | 0 |  | py/unused-import |
| CWE-918_safe | CWE-918 | safe | vulnerable | FP | 2 | py/full-ssrf; py/reflective-xss |  |
| CWE-94_vulnerable | CWE-94 | vulnerable | safe | FN | 0 |  |  |
| CWE-941_vulnerable | CWE-941 | vulnerable | safe | FN | 0 |  |  |
| CWE-943_vulnerable | CWE-943 | vulnerable | safe | FN | 0 |  |  |
| CWE-95_vulnerable | CWE-95 | vulnerable | safe | FN | 0 |  |  |