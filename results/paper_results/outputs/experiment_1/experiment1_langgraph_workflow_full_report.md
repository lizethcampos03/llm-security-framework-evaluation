# Experiment 1 - Langgraph Workflow Full Benchmark Report 

Generated: `2026-06-10T21:40:38`
Run mode: `all_discovered_cwes`

## Fairness Note
Expected labels and CWE IDs were hidden from the graph and used only after execution for scoring.

## Aggregate Metrics
- **total_cases**: `138`
- **correct_cases**: `122`
- **overall_accuracy**: `0.8841`
- **vulnerable_detection_accuracy**: `0.9565`
- **safe_classification_accuracy**: `0.8116`
- **true_positives**: `66`
- **false_positives**: `13`
- **false_negatives**: `3`
- **true_negatives**: `56`
- **precision**: `0.8354`
- **recall**: `0.9565`
- **f1**: `0.8919`
- **average_confidence**: `0.8319`
- **average_validation_consistency**: `0.0`

## Case Results
| Case | CWE | Expected | Detected | Correct | Predicted CWE | RAG Config | Confidence | Consistency | Latency |
|---|---|---|---|---|---|---|---:|---:|---:|
| CAL-001 | CWE-20 | vulnerable | safe | No |  | full_hybrid_evidence_reranker | None | 0.0 | 24.92 |
| CAL-002 | CWE-20 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 15.009 |
| CAL-003 | CWE-22 | vulnerable | vulnerable | Yes | CWE-22 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 39.313 |
| CAL-004 | CWE-22 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 15.538 |
| CAL-005 | CWE-78 | vulnerable | vulnerable | Yes | CWE-78 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 42.588 |
| CAL-006 | CWE-78 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 14.329 |
| CAL-007 | CWE-79 | vulnerable | vulnerable | Yes | CWE-79 | full_hybrid_evidence_reranker | 0.74 | 0.0 | 41.156 |
| CAL-008 | CWE-79 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 12.281 |
| CAL-009 | CWE-80 | vulnerable | vulnerable | Yes | CWE-79 | full_hybrid_evidence_reranker | 0.95 | 0.0 | 29.895 |
| CAL-010 | CWE-80 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 12.691 |
| CAL-011 | CWE-89 | vulnerable | vulnerable | Yes | CWE-89 | full_hybrid_evidence_reranker | 0.97 | 0.0 | 78.222 |
| CAL-012 | CWE-89 | safe | vulnerable | No | CWE-306 | full_hybrid_evidence_reranker | 0.7 | 0.0 | 39.314 |
| CAL-013 | CWE-90 | vulnerable | vulnerable | Yes | CWE-90 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 41.977 |
| CAL-014 | CWE-90 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 15.561 |
| CAL-015 | CWE-94 | vulnerable | vulnerable | Yes | CWE-20 | full_hybrid_evidence_reranker | 0.7 | 0.0 | 55.081 |
| CAL-016 | CWE-94 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 16.788 |
| CAL-017 | CWE-95 | vulnerable | vulnerable | Yes | CWE-95 | full_hybrid_evidence_reranker | 0.97 | 0.0 | 95.203 |
| CAL-018 | CWE-95 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 17.09 |
| CAL-019 | CWE-99 | vulnerable | vulnerable | Yes | CWE-22 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 329.697 |
| CAL-020 | CWE-99 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 15.97 |
| CAL-021 | CWE-113 | vulnerable | vulnerable | Yes | CWE-113 | full_hybrid_evidence_reranker | 0.82 | 0.0 | 45.501 |
| CAL-022 | CWE-113 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.625 |
| CAL-023 | CWE-116 | vulnerable | vulnerable | Yes | CWE-78 | full_hybrid_evidence_reranker | 0.97 | 0.0 | 45.984 |
| CAL-024 | CWE-116 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 16.752 |
| CAL-025 | CWE-117 | vulnerable | vulnerable | Yes | CWE-755 | full_hybrid_evidence_reranker | 0.82 | 0.0 | 41.76 |
| CAL-026 | CWE-117 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.513 |
| CAL-027 | CWE-193 | vulnerable | vulnerable | Yes | CWE-193 | full_hybrid_evidence_reranker | 0.95 | 0.0 | 32.76 |
| CAL-028 | CWE-193 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.382 |
| CAL-029 | CWE-200 | vulnerable | vulnerable | Yes | CWE-89 | full_hybrid_evidence_reranker | 0.95 | 0.0 | 46.067 |
| CAL-030 | CWE-200 | safe | vulnerable | No | CWE-306 | full_hybrid_evidence_reranker | 0.78 | 0.0 | 38.699 |
| CAL-031 | CWE-209 | vulnerable | vulnerable | Yes | CWE-209 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 156.261 |
| CAL-032 | CWE-209 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 12.892 |
| CAL-033 | CWE-215 | vulnerable | vulnerable | Yes | CWE-215 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 29.479 |
| CAL-034 | CWE-215 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.312 |
| CAL-035 | CWE-250 | vulnerable | vulnerable | Yes | CWE-250 | full_hybrid_evidence_reranker | 0.78 | 0.0 | 62.656 |
| CAL-036 | CWE-250 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 14.512 |
| CAL-037 | CWE-252 | vulnerable | vulnerable | Yes | CWE-252 | full_hybrid_evidence_reranker | 0.7 | 0.0 | 41.59 |
| CAL-038 | CWE-252 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.716 |
| CAL-039 | CWE-259 | vulnerable | vulnerable | Yes | CWE-259 | full_hybrid_evidence_reranker | 0.92 | 0.0 | 45.045 |
| CAL-040 | CWE-259 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.309 |
| CAL-041 | CWE-269 | vulnerable | vulnerable | Yes | CWE-250 | full_hybrid_evidence_reranker | 0.7 | 0.0 | 118.364 |
| CAL-042 | CWE-269 | safe | vulnerable | No | CWE-250 | full_hybrid_evidence_reranker | 0.7 | 0.0 | 47.509 |
| CAL-043 | CWE-283 | vulnerable | vulnerable | Yes | CWE-285 | full_hybrid_evidence_reranker | 0.82 | 0.0 | 90.31 |
| CAL-044 | CWE-283 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.307 |
| CAL-045 | CWE-285 | vulnerable | vulnerable | Yes | CWE-287 | full_hybrid_evidence_reranker | 0.83 | 0.0 | 116.58 |
| CAL-046 | CWE-285 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 17.141 |
| CAL-047 | CWE-295 | vulnerable | vulnerable | Yes | CWE-295 | full_hybrid_evidence_reranker | 0.95 | 0.0 | 31.283 |
| CAL-048 | CWE-295 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 11.099 |
| CAL-049 | CWE-306 | vulnerable | vulnerable | Yes | CWE-798 | full_hybrid_evidence_reranker | 0.74 | 0.0 | 72.894 |
| CAL-050 | CWE-306 | safe | vulnerable | No | CWE-798 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 66.144 |
| CAL-051 | CWE-319 | vulnerable | vulnerable | Yes | CWE-614 | full_hybrid_evidence_reranker | 0.74 | 0.0 | 36.86 |
| CAL-052 | CWE-319 | safe | vulnerable | No | CWE-287 | full_hybrid_evidence_reranker | 0.72 | 0.0 | 41.559 |
| CAL-053 | CWE-321 | vulnerable | vulnerable | Yes | CWE-798 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 96.057 |
| CAL-054 | CWE-321 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.861 |
| CAL-055 | CWE-326 | vulnerable | vulnerable | Yes | CWE-326 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 34.8 |
| CAL-056 | CWE-326 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.709 |
| CAL-057 | CWE-327 | vulnerable | vulnerable | Yes | CWE-327 | full_hybrid_evidence_reranker | 0.95 | 0.0 | 53.645 |
| CAL-058 | CWE-327 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 15.35 |
| CAL-059 | CWE-329 | vulnerable | vulnerable | Yes | CWE-329 | full_hybrid_evidence_reranker | 0.88 | 0.0 | 42.59 |
| CAL-060 | CWE-329 | safe | vulnerable | No | CWE-330 | full_hybrid_evidence_reranker | 0.6 | 0.0 | 35.824 |
| CAL-061 | CWE-330 | vulnerable | vulnerable | Yes | CWE-330 | full_hybrid_evidence_reranker | 0.92 | 0.0 | 39.723 |
| CAL-062 | CWE-330 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 12.426 |
| CAL-063 | CWE-331 | vulnerable | vulnerable | Yes | CWE-330 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 31.721 |
| CAL-064 | CWE-331 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 12.484 |
| CAL-065 | CWE-339 | vulnerable | vulnerable | Yes | CWE-330 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 34.395 |
| CAL-066 | CWE-339 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.103 |
| CAL-067 | CWE-347 | vulnerable | vulnerable | Yes | CWE-347 | full_hybrid_evidence_reranker | 0.95 | 0.0 | 1277.422 |
| CAL-068 | CWE-347 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 12.56 |
| CAL-069 | CWE-367 | vulnerable | vulnerable | Yes | CWE-22 | full_hybrid_evidence_reranker | 0.7 | 0.0 | 60.465 |
| CAL-070 | CWE-367 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 12.643 |
| CAL-071 | CWE-377 | vulnerable | vulnerable | Yes | CWE-377 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 31.596 |
| CAL-072 | CWE-377 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.049 |
| CAL-073 | CWE-379 | vulnerable | vulnerable | Yes | CWE-379 | full_hybrid_evidence_reranker | 0.85 | 0.0 | 37.166 |
| CAL-074 | CWE-379 | safe | vulnerable | No | CWE-377 | full_hybrid_evidence_reranker | 0.7 | 0.0 | 53.95 |
| CAL-075 | CWE-385 | vulnerable | vulnerable | Yes | CWE-208 | full_hybrid_evidence_reranker | 0.78 | 0.0 | 56.749 |
| CAL-076 | CWE-385 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 12.335 |
| CAL-077 | CWE-400 | vulnerable | vulnerable | Yes | CWE-625 | full_hybrid_evidence_reranker | 0.74 | 0.0 | 79.4 |
| CAL-078 | CWE-400 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 15.342 |
| CAL-079 | CWE-406 | vulnerable | vulnerable | Yes | CWE-941 | full_hybrid_evidence_reranker | 0.7 | 0.0 | 40.791 |
| CAL-080 | CWE-406 | safe | vulnerable | No | CWE-941 | full_hybrid_evidence_reranker | 0.78 | 0.0 | 42.155 |
| CAL-081 | CWE-414 | vulnerable | safe | No |  | full_hybrid_evidence_reranker | None | 0.0 | 13.71 |
| CAL-082 | CWE-414 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 14.377 |
| CAL-083 | CWE-425 | vulnerable | vulnerable | Yes | CWE-22 | full_hybrid_evidence_reranker | 0.92 | 0.0 | 43.346 |
| CAL-084 | CWE-425 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.733 |
| CAL-085 | CWE-434 | vulnerable | vulnerable | Yes | CWE-434 | full_hybrid_evidence_reranker | 0.85 | 0.0 | 44.462 |
| CAL-086 | CWE-434 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.341 |
| CAL-087 | CWE-454 | vulnerable | vulnerable | Yes | CWE-259 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 53.456 |
| CAL-088 | CWE-454 | safe | vulnerable | No | CWE-798 | full_hybrid_evidence_reranker | 0.85 | 0.0 | 36.628 |
| CAL-089 | CWE-462 | vulnerable | vulnerable | Yes | CWE-462 | full_hybrid_evidence_reranker | 0.7 | 0.0 | 36.865 |
| CAL-090 | CWE-462 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 14.09 |
| CAL-091 | CWE-477 | vulnerable | vulnerable | Yes | CWE-477 | full_hybrid_evidence_reranker | 0.85 | 0.0 | 27.618 |
| CAL-092 | CWE-477 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 10.549 |
| CAL-093 | CWE-502 | vulnerable | vulnerable | Yes | CWE-502 | full_hybrid_evidence_reranker | 0.95 | 0.0 | 44.623 |
| CAL-094 | CWE-502 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 12.18 |
| CAL-095 | CWE-521 | vulnerable | vulnerable | Yes | CWE-521 | full_hybrid_evidence_reranker | 0.72 | 0.0 | 53.721 |
| CAL-096 | CWE-521 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.757 |
| CAL-097 | CWE-522 | vulnerable | vulnerable | Yes | CWE-522 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 83.375 |
| CAL-098 | CWE-522 | safe | vulnerable | No | CWE-798 | full_hybrid_evidence_reranker | 0.74 | 0.0 | 57.469 |
| CAL-099 | CWE-595 | vulnerable | vulnerable | Yes | CWE-595 | full_hybrid_evidence_reranker | 0.86 | 0.0 | 33.545 |
| CAL-100 | CWE-595 | safe | vulnerable | No | CWE-595 | full_hybrid_evidence_reranker | 0.62 | 0.0 | 34.024 |
| CAL-101 | CWE-601 | vulnerable | vulnerable | Yes | CWE-601 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 50.239 |
| CAL-102 | CWE-601 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 12.626 |
| CAL-103 | CWE-605 | vulnerable | vulnerable | Yes | CWE-605 | full_hybrid_evidence_reranker | 0.62 | 0.0 | 41.009 |
| CAL-104 | CWE-605 | safe | vulnerable | No | CWE-605 | full_hybrid_evidence_reranker | 0.55 | 0.0 | 33.315 |
| CAL-105 | CWE-611 | vulnerable | vulnerable | Yes | CWE-611 | full_hybrid_evidence_reranker | 0.88 | 0.0 | 63.681 |
| CAL-106 | CWE-611 | safe | safe | Yes | CWE-611 | full_hybrid_evidence_reranker | 0.74 | 0.0 | 338.958 |
| CAL-107 | CWE-641 | vulnerable | vulnerable | Yes | CWE-22 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 62.472 |
| CAL-108 | CWE-641 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 15.249 |
| CAL-109 | CWE-643 | vulnerable | vulnerable | Yes | CWE-643 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 51.084 |
| CAL-110 | CWE-643 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 14.277 |
| CAL-111 | CWE-703 | vulnerable | safe | No |  | full_hybrid_evidence_reranker | None | 0.0 | 13.787 |
| CAL-112 | CWE-703 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 12.072 |
| CAL-113 | CWE-730 | vulnerable | vulnerable | Yes | CWE-730 | full_hybrid_evidence_reranker | 0.82 | 0.0 | 44.225 |
| CAL-114 | CWE-730 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.068 |
| CAL-115 | CWE-732 | vulnerable | vulnerable | Yes | CWE-732 | full_hybrid_evidence_reranker | 0.86 | 0.0 | 69.447 |
| CAL-116 | CWE-732 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.517 |
| CAL-117 | CWE-759 | vulnerable | vulnerable | Yes | CWE-759 | full_hybrid_evidence_reranker | 0.93 | 0.0 | 52.471 |
| CAL-118 | CWE-759 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 109.504 |
| CAL-119 | CWE-760 | vulnerable | vulnerable | Yes | CWE-760 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 39.41 |
| CAL-120 | CWE-760 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 14.391 |
| CAL-121 | CWE-776 | vulnerable | vulnerable | Yes | CWE-611 | full_hybrid_evidence_reranker | 0.82 | 0.0 | 71.612 |
| CAL-122 | CWE-776 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 14.134 |
| CAL-123 | CWE-798 | vulnerable | vulnerable | Yes | CWE-798 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 36.225 |
| CAL-124 | CWE-798 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 12.485 |
| CAL-125 | CWE-827 | vulnerable | vulnerable | Yes | CWE-827 | full_hybrid_evidence_reranker | 0.7 | 0.0 | 37.466 |
| CAL-126 | CWE-827 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 12.898 |
| CAL-127 | CWE-835 | vulnerable | vulnerable | Yes | CWE-835 | full_hybrid_evidence_reranker | 0.92 | 0.0 | 34.189 |
| CAL-128 | CWE-835 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 14.022 |
| CAL-129 | CWE-841 | vulnerable | vulnerable | Yes | CWE-285 | full_hybrid_evidence_reranker | 0.82 | 0.0 | 45.964 |
| CAL-130 | CWE-841 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 16.999 |
| CAL-131 | CWE-918 | vulnerable | vulnerable | Yes | CWE-918 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 59.327 |
| CAL-132 | CWE-918 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 13.717 |
| CAL-133 | CWE-941 | vulnerable | vulnerable | Yes | CWE-941 | full_hybrid_evidence_reranker | 0.82 | 0.0 | 43.603 |
| CAL-134 | CWE-941 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 15.151 |
| CAL-135 | CWE-943 | vulnerable | vulnerable | Yes | CWE-943 | full_hybrid_evidence_reranker | 0.86 | 0.0 | 38.897 |
| CAL-136 | CWE-943 | safe | vulnerable | No | CWE-256 | full_hybrid_evidence_reranker | 0.78 | 0.0 | 101.374 |
| CAL-137 | CWE-1204 | vulnerable | vulnerable | Yes | CWE-1204 | full_hybrid_evidence_reranker | 0.9 | 0.0 | 41.676 |
| CAL-138 | CWE-1204 | safe | safe | Yes |  | full_hybrid_evidence_reranker | None | 0.0 | 14.984 |