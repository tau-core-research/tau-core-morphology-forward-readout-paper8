# Endpoint Decision Matrix

This matrix combines the predeclared quality-gate endpoint metrics with
the shuffled-family null diagnostics. It is a protocol decision aid, not
a new fit and not an empirical validation claim.

## Holdout Decision Matrix

| quality_gate | n_galaxies | matched_beats_wrong_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | p_beats_wrong_fraction_at_least_as_good | p_mean_minus_wrong_at_least_as_good | null_support_status | recommended_endpoint_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no_large_distance_error | 26 | 0.884615 | 0.538462 | 0.730769 | 0.130869 | 0.121878 | weak_null | baseline_competitiveness_secondary |
| confidence_ge_0_75_and_clean | 20 | 0.9 | 0.5 | 0.75 | 0.118881 | 0.10989 | weak_null | baseline_competitiveness_secondary |
| clean_manifest_proxy | 20 | 0.9 | 0.5 | 0.75 | 0.13986 | 0.12987 | weak_null | baseline_competitiveness_secondary |
| confidence_ge_0_85 | 30 | 0.833333 | 0.5 | 0.6 | 0.0659341 | 0.031968 | mean_null_only | baseline_competitiveness_secondary |
| no_few_rotation_points | 36 | 0.777778 | 0.5 | 0.555556 | 0.0669331 | 0.016983 | mean_null_only | limited_or_negative_control |
| no_low_inclination | 35 | 0.857143 | 0.514286 | 0.657143 | 0.040959 | 0.010989 | strong_fraction_and_mean_null | primary_endpoint_candidate |
| all | 44 | 0.818182 | 0.477273 | 0.613636 | 0.035964 | 0.012987 | strong_fraction_and_mean_null | specificity_null_primary |
| confidence_ge_0_75 | 32 | 0.84375 | 0.53125 | 0.59375 | 0.0529471 | 0.023976 | mean_null_only | specificity_only_diagnostic |

## Claim-Safe Endpoint Recommendation

At least one gate currently satisfies both baseline-competitiveness and strong shuffled-null support. This would be the natural primary endpoint candidate, subject to predeclaration.
Current primary endpoint candidate: no_low_inclination (n=35).
Fuller-sample specificity support remains visible in: all (n=44).
Current baseline-competitiveness secondary candidate: no_large_distance_error (n=26).

## Claim Boundary

This recommendation must not be read as selecting a winning endpoint
after seeing the data. It records the present preparation-state tradeoff
so that a future Paper 8 run can predeclare its primary and secondary
endpoint lanes before endpoint scoring.
