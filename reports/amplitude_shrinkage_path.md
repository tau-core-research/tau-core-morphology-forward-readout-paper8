# Amplitude Shrinkage Path

This scan varies only the linear family-to-global amplitude shrinkage
weight for the source-native bridge formula kernels. It is a diagnostic
for the Tau-side amplitude-normalization gate, not a selected endpoint.

## Holdout Path

| family_weight | matched_beats_wrong_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | mean_matched_minus_wrong | mean_matched_minus_tpg_v6 | mean_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.590909 | 0.545455 | 0.568182 | -0.123899 | -0.0970081 | -0.568253 |
| 0.05 | 0.613636 | 0.568182 | 0.568182 | -1.22678 | -0.0631209 | -0.534366 |
| 0.1 | 0.636364 | 0.568182 | 0.545455 | -2.36582 | -0.0232053 | -0.494451 |
| 0.15 | 0.681818 | 0.568182 | 0.545455 | -3.49453 | 0.022832 | -0.448413 |
| 0.2 | 0.704545 | 0.568182 | 0.545455 | -4.59539 | 0.0738743 | -0.397371 |
| 0.25 | 0.772727 | 0.568182 | 0.545455 | -5.64679 | 0.129264 | -0.341981 |
| 0.3 | 0.772727 | 0.477273 | 0.568182 | -6.65632 | 0.18847 | -0.282775 |
| 0.35 | 0.818182 | 0.477273 | 0.568182 | -7.62618 | 0.251071 | -0.220174 |
| 0.4 | 0.818182 | 0.477273 | 0.613636 | -8.55421 | 0.316746 | -0.154499 |
| 0.45 | 0.840909 | 0.477273 | 0.613636 | -9.44379 | 0.385255 | -0.0859905 |
| 0.5 | 0.863636 | 0.477273 | 0.636364 | -10.3006 | 0.456422 | -0.0148234 |
| 0.55 | 0.863636 | 0.477273 | 0.568182 | -11.1318 | 0.530117 | 0.0588719 |
| 0.6 | 0.863636 | 0.477273 | 0.545455 | -11.9426 | 0.606243 | 0.134997 |
| 0.65 | 0.863636 | 0.477273 | 0.545455 | -12.7326 | 0.684722 | 0.213476 |
| 0.7 | 0.863636 | 0.477273 | 0.522727 | -13.5005 | 0.765492 | 0.294247 |
| 0.75 | 0.886364 | 0.477273 | 0.5 | -14.2465 | 0.8485 | 0.377255 |
| 0.8 | 0.886364 | 0.477273 | 0.5 | -14.9715 | 0.933696 | 0.462451 |
| 0.85 | 0.886364 | 0.477273 | 0.5 | -15.6766 | 1.02103 | 0.549789 |
| 0.9 | 0.886364 | 0.477273 | 0.477273 | -16.363 | 1.11047 | 0.639225 |
| 0.95 | 0.886364 | 0.477273 | 0.477273 | -17.0317 | 1.20196 | 0.730714 |
| 1 | 0.886364 | 0.477273 | 0.477273 | -17.6838 | 1.29546 | 0.824211 |

## Tradeoff Ranking

| family_weight | specificity_ok | mond_win_ok | tpg_win_ok | tradeoff_score | matched_beats_wrong_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | mean_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5 | True | True | False | 1.97727 | 0.863636 | 0.477273 | 0.636364 | -0.0148234 |
| 0.45 | True | True | False | 1.93182 | 0.840909 | 0.477273 | 0.613636 | -0.0859905 |
| 0.4 | True | True | False | 1.90909 | 0.818182 | 0.477273 | 0.613636 | -0.154499 |
| 0.55 | True | False | False | 1.90909 | 0.863636 | 0.477273 | 0.568182 | 0.0588719 |
| 0.6 | True | False | False | 1.88636 | 0.863636 | 0.477273 | 0.545455 | 0.134997 |
| 0.65 | True | False | False | 1.88636 | 0.863636 | 0.477273 | 0.545455 | 0.213476 |
| 0.35 | True | False | False | 1.86364 | 0.818182 | 0.477273 | 0.568182 | -0.220174 |
| 0.7 | True | False | False | 1.86364 | 0.863636 | 0.477273 | 0.522727 | 0.294247 |

## Claim Boundary

The best-looking shrinkage point is not a validated physical policy.
It identifies the amplitude-normalization range that the Tau-side theory
would need to justify before Paper 8 can claim baseline competitiveness.
