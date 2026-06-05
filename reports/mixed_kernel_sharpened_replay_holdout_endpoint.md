# Mixed Kernel Sharpened Replay/Holdout Endpoint

This endpoint scores only the frozen source-sharpened replay formulas.
Observed velocities are read only by this scoring script. The result is
a small-N replay/holdout control, not population validation.

## Summary

| endpoint_status | n_cases_scored | mean_rmse_mixed_sharpened_replay | mean_rmse_newton | mean_rmse_tpg_v6 | mean_rmse_mond | mean_rmse_exponential_disk_carrier | n_beats_newton | n_beats_tpg_v6 | n_beats_mond | n_beats_exponential_disk_carrier | n_matched_beats_all_wrong_labels | matched_permutation_rank | best_shuffled_mean_rmse | matched_minus_best_shuffled | construction_used_vobs | scoring_used_vobs | claim_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SHARPENED_REPLAY_HOLDOUT_2CASE_PRELIMINARY_CONTROL_RESULT | 2 | 19.2243 | 72.9191 | 21.1353 | 23.9535 | 20.4213 | 2 | 2 | 2 | 2 | 2 | 1 | 19.2243 | 0 | False | True | small-N sharpened replay/holdout control result; not population validation | mixed_kernel_sharpened_replay_holdout_endpoint_small_n_not_validation |

## Scores

| galaxy | n_points | rmse_newton | rmse_tpg_v6 | rmse_mond | rmse_exponential_disk_carrier | rmse_mixed_sharpened_replay | mixed_minus_newton | mixed_minus_tpg_v6 | mixed_minus_mond | mixed_minus_exponential_disk_carrier | beats_newton | beats_tpg_v6 | beats_mond | beats_exponential_disk_carrier | applied_formula_source | applied_formula_id | applied_kernel_label | case_status | construction_used_vobs | scoring_used_vobs | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | 19 | 86.4837 | 16.7855 | 18.5954 | 17.3695 | 16.3178 | -70.1659 | -0.467673 | -2.27753 | -1.0517 | True | True | True | True | NGC5907 | NGC5907_EXPDISK_PROJECTION_SHARPENED_REPLAY_V2 | K_projection_source_sharpened | SHARPENED_REPLAY_HOLDOUT_SCORED | False | True | mixed_kernel_sharpened_replay_holdout_endpoint_small_n_not_validation |
| NGC7331 | 36 | 59.3544 | 25.4851 | 29.3117 | 23.473 | 22.1308 | -37.2235 | -3.35422 | -7.18083 | -1.34213 | True | True | True | True | NGC7331 | NGC7331_VOW_SHARPENED_REPLAY_V3 | K_vertical_outer_warp_source_sharpened | SHARPENED_REPLAY_HOLDOUT_SCORED | False | True | mixed_kernel_sharpened_replay_holdout_endpoint_small_n_not_validation |

## Wrong-Label Control

| galaxy | matched_rmse | wrong_best_rmse | matched_minus_wrong_best | matched_rank_within_galaxy | matched_beats_all_wrong_labels | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | 16.3178 | 16.7709 | -0.453071 | 1 | True | mixed_kernel_sharpened_replay_holdout_endpoint_small_n_not_validation |
| NGC7331 | 22.1308 | 22.9064 | -0.775549 | 1 | True | mixed_kernel_sharpened_replay_holdout_endpoint_small_n_not_validation |

## Shuffled Assignments

| assignment_id | assignment_role | mean_rmse | sum_rmse | n_matched_labels | claim_boundary | rank_by_mean_rmse |
| --- | --- | --- | --- | --- | --- | --- |
| NGC5907->NGC5907;NGC7331->NGC7331 | matched_diagonal | 19.2243 | 38.4487 | 2 | mixed_kernel_sharpened_replay_holdout_endpoint_small_n_not_validation | 1 |
| NGC5907->NGC7331;NGC7331->NGC5907 | shuffled_label_null | 19.8387 | 39.6773 | 0 | mixed_kernel_sharpened_replay_holdout_endpoint_small_n_not_validation | 2 |

## Claim Boundary

This score tests whether source-sharpened kernels repair the two-case
replay/holdout specificity failure. It is not a population claim and it
does not update accepted single-galaxy endpoints retroactively.
