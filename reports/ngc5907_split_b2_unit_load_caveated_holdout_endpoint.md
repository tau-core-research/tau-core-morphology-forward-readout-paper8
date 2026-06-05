# NGC5907 Split-B2 Unit-Load Caveated Holdout Endpoint

Status: `CAVEATED_SPLIT_B2_HOLDOUT_PRELIMINARY_CONTROL_SCORED`

This scoring script reads the frozen split-B2 manifest and kernel grid
unchanged. It reads observed velocities only for endpoint scoring.

## Summary

| galaxy | formula_id | endpoint_status | n_points | split_b2_rmse_km_s | best_baseline_model | best_baseline_rmse_km_s | split_minus_best_baseline_rmse_km_s | best_existing_tau_context_model | best_existing_tau_context_rmse_km_s | split_minus_best_existing_tau_context_rmse_km_s | denominator_caveat | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | NGC5907_SPLIT_B2_UNIT_LOAD_FREEZE_CAVEATED_V1 | CAVEATED_SPLIT_B2_HOLDOUT_PRELIMINARY_CONTROL_SCORED | 19 | 62.0882 | TPG_V6_v_v6 | 16.7855 | 45.3027 | TAU_NGC5907_PROJECTION_ACCEPTED | 15.4952 | 46.593 | uses source-native optical warp outer support, not SPARC HI radius | False | True | True | ngc5907_split_b2_unit_load_caveated_holdout_preliminary_control |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | mae_km_s | bias_km_s | within_error_fraction | construction_used_vobs | scoring_used_vobs | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | TAU_NGC5907_PROJECTION_ACCEPTED | existing_projection_readout_context | 19 | 15.4952 | 9.25559 | -6.33278 | 0.315789 | False | True | ngc5907_split_b2_unit_load_caveated_holdout_preliminary_control |
| NGC5907 | TAU_NGC5907_EXPDISK_PROJECTION_MIXED_ACCEPTED | existing_matched_mixed_readout_context | 19 | 16.3725 | 9.94217 | -7.42199 | 0.315789 | False | True | ngc5907_split_b2_unit_load_caveated_holdout_preliminary_control |
| NGC5907 | TPG_V6_v_v6 | baseline | 19 | 16.7855 | 11.4745 | -1.00704 | 0.263158 | False | True | ngc5907_split_b2_unit_load_caveated_holdout_preliminary_control |
| NGC5907 | EXPONENTIAL_DISK_CARRIER | baseline | 19 | 17.3695 | 11.7237 | -2.1139 | 0.210526 | False | True | ngc5907_split_b2_unit_load_caveated_holdout_preliminary_control |
| NGC5907 | MOND_v_mond | baseline | 19 | 18.5954 | 15.1311 | 4.3498 | 0.105263 | False | True | ngc5907_split_b2_unit_load_caveated_holdout_preliminary_control |
| NGC5907 | TAU_NGC5907_SPLIT_B2_UNIT_LOAD_CAVEATED | matched_split_b2_holdout_readout | 19 | 62.0882 | 54.9086 | 7.07759 | 0.105263 | False | True | ngc5907_split_b2_unit_load_caveated_holdout_preliminary_control |
| NGC5907 | NEWTONIAN_vn | baseline | 19 | 86.4837 | 85.6717 | -85.6717 | 0 | False | True | ngc5907_split_b2_unit_load_caveated_holdout_preliminary_control |

## Interpretation

The split-B2 unit-load candidate is scored as a caveated preliminary control
because its denominator is the optical warp support radius, not SPARC/HI RHI.
It is therefore a useful independent-galaxy stress test of the NGC7331
split-B2 repair, but not yet a clean population endpoint.

## Claim Boundary

`ngc5907_split_b2_unit_load_caveated_holdout_preliminary_control`
