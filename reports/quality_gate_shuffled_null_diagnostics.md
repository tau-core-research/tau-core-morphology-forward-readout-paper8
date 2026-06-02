# Quality Gate Shuffled Null Diagnostics

This diagnostic reruns the shuffled-family label null inside each
predeclared quality gate under the fixed train-selected shrinkage
policy. It tests whether a quality gate keeps morphology-family
specificity beyond what shuffled labels produce.

## Holdout Shuffled Null Summary

| quality_gate | n_galaxies | observed_beats_wrong_fraction | null_beats_wrong_fraction_mean | p_beats_wrong_fraction_at_least_as_good | observed_mean_minus_wrong | null_mean_minus_wrong_mean | p_mean_minus_wrong_at_least_as_good | observed_rank1_fraction | null_rank1_fraction_mean | p_rank1_fraction_at_least_as_good |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 44 | 0.818182 | 0.719818 | 0.035964 | -8.55421 | -3.26965 | 0.012987 | 0.272727 | 0.241341 | 0.362637 |
| no_low_inclination | 35 | 0.857143 | 0.754171 | 0.040959 | -9.40436 | -4.34266 | 0.010989 | 0.285714 | 0.232229 | 0.265734 |
| confidence_ge_0_75 | 32 | 0.84375 | 0.736656 | 0.0529471 | -9.05639 | -3.43462 | 0.023976 | 0.34375 | 0.261875 | 0.187812 |
| confidence_ge_0_85 | 30 | 0.833333 | 0.720667 | 0.0659341 | -7.4704 | -2.67175 | 0.031968 | 0.3 | 0.25 | 0.321678 |
| no_few_rotation_points | 36 | 0.777778 | 0.670056 | 0.0669331 | -6.48205 | -1.60265 | 0.016983 | 0.305556 | 0.237333 | 0.204795 |
| confidence_ge_0_75_and_clean | 20 | 0.9 | 0.798 | 0.118881 | -9.67091 | -5.81435 | 0.10989 | 0.25 | 0.191 | 0.313686 |
| no_large_distance_error | 26 | 0.884615 | 0.807154 | 0.130869 | -10.4694 | -7.40449 | 0.121878 | 0.269231 | 0.178885 | 0.11988 |
| clean_manifest_proxy | 20 | 0.9 | 0.80015 | 0.13986 | -9.67091 | -5.69645 | 0.12987 | 0.25 | 0.1887 | 0.311688 |

## Claim Boundary

A low shuffled-null p-value is evidence for morphology-label specificity
inside the selected quality gate, not empirical validation of Tau Core.
Quality gates must be declared before endpoint scoring in any future
paper endpoint, and caveated rows remain scientifically relevant.
