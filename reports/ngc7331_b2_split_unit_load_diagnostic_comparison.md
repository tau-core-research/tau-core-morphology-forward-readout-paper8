# NGC7331 split-B2 unit-load diagnostic comparison

This comparison scores the split-B2 unit-load freeze candidate after the
negative exact-transfer interval audit. It is diagnostic only and does
not promote an accepted endpoint.

## Summary

| galaxy | formula_id | comparison_status | n_points | split_b2_rmse_km_s | failed_exact_b2_cross_interval_distance_rmse_km_s | rmse_improvement_vs_failed_exact_b2_km_s | best_baseline_model | best_baseline_rmse_km_s | split_minus_best_baseline_rmse_km_s | construction_used_vobs | diagnostic_scoring_used_vobs | endpoint_scores_allowed | claim_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_SPLIT_B2_UNIT_LOAD_FREEZE_DIAGNOSTIC_V1 | NGC7331_SPLIT_B2_UNIT_LOAD_DIAGNOSTIC_COMPARISON_COMPLETE_NOT_ENDPOINT | 36 | 21.7334 | 54.8119 | 33.0785 | EXPONENTIAL_DISK_CARRIER | 23.473 | -1.73956 | False | True | False | diagnostic comparison only; confirms q-role repair improves the failed exact-B2 transfer but cannot promote same-curve endpoint | ngc7331_b2_split_unit_load_diagnostic_comparison_not_endpoint |

## Scores

| galaxy | model_id | rmse_km_s | mae_km_s | bias_km_s | within_err_fraction | claim_boundary | construction_used_vobs | diagnostic_scoring_used_vobs | endpoint_scores_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | SPLIT_B2_UNIT_LOAD_DIAGNOSTIC | 21.7334 | 19.0392 | -2.25362 | 0.111111 | ngc7331_b2_split_unit_load_diagnostic_comparison_not_endpoint | False | True | False |
| NGC7331 | EXPONENTIAL_DISK_CARRIER | 23.473 | 19.5632 | 19.1914 | 0.166667 | ngc7331_b2_split_unit_load_diagnostic_comparison_not_endpoint | False | True | False |
| NGC7331 | TPG_V6_v_v6 | 25.4851 | 22.2152 | 22.2056 | 0.0833333 | ngc7331_b2_split_unit_load_diagnostic_comparison_not_endpoint | False | True | False |
| NGC7331 | MOND_v_mond | 29.3117 | 26.452 | 26.452 | 0.0555556 | ngc7331_b2_split_unit_load_diagnostic_comparison_not_endpoint | False | True | False |
| NGC7331 | FAILED_EXACT_B2_CROSS_CAVEATED_UPPER | 54.8119 | 48.2656 | -38.8557 | 0.0277778 | ngc7331_b2_split_unit_load_diagnostic_comparison_not_endpoint | False | True | False |
| NGC7331 | NEWTONIAN_vn | 59.3544 | 51.4592 | -42.0494 | 0.0277778 | ngc7331_b2_split_unit_load_diagnostic_comparison_not_endpoint | False | True | False |

## Interpretation

The split unit-load branch substantially improves the failed exact-B2
transfer distance, which confirms that q-role conflation was a real
failure mode. Because the branch was selected after inspecting the
failure, this result is a repair diagnostic. It can motivate a future
predeclared holdout/population protocol, but it is not an accepted
NGC7331 endpoint.
