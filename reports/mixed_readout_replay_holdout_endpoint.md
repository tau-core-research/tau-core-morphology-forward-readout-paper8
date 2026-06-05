# Mixed Readout Replay/Holdout Endpoint

This endpoint scores the strict fresh replay/holdout subset. NGC4013 is
excluded because it is a retrospective frozen reference protocol. NGC7331
uses the V2 fractional-onset replay freeze manifest rather than the V1
broad-window endpoint manifest.

## Summary

| endpoint_status | n_cases_scored | case_set | ngc4013_excluded_reason | mean_rmse_mixed_replay_holdout | mean_rmse_newton | mean_rmse_tpg_v6 | mean_rmse_mond | mean_rmse_exponential_disk_carrier | n_beats_newton | n_beats_tpg_v6 | n_beats_mond | n_beats_exponential_disk_carrier | n_matched_beats_all_wrong_labels | matched_permutation_rank | best_shuffled_mean_rmse | matched_minus_best_shuffled | construction_used_vobs | scoring_used_vobs | claim_boundary | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MIXED_REPLAY_HOLDOUT_2CASE_PRELIMINARY_RESULT | 2 | NGC5907_fresh_prospective;NGC7331_v2_fractional_onset_replay | retrospective_reference_protocol_not_fresh_replay_holdout | 19.5525 | 72.9191 | 21.1353 | 23.9535 | 20.4213 | 2 | 2 | 2 | 2 | 0 | 2 | 19.5085 | 0.0439718 | False | True | mixed_readout_replay_holdout_endpoint_small_n_not_validation | two-case replay/holdout endpoint; encouraging if matched labels win, but still small-N and not population validation |

## Scores

| galaxy | n_points | rmse_newton | rmse_tpg_v6 | rmse_mond | rmse_exponential_disk_carrier | rmse_mixed_replay_holdout | mixed_minus_newton | mixed_minus_tpg_v6 | mixed_minus_mond | mixed_minus_exponential_disk_carrier | beats_newton | beats_tpg_v6 | beats_mond | beats_exponential_disk_carrier | applied_formula_source | applied_formula_label | applied_formula_id | case_status | construction_used_vobs | scoring_used_vobs | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | 19 | 86.4837 | 16.7855 | 18.5954 | 17.3695 | 16.3725 | -70.1112 | -0.412978 | -2.22283 | -0.99701 | True | True | True | True | NGC5907 | K_expdisk_projection_overlay | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | FRESH_PROSPECTIVE_MIXED_PROTOCOL_REPLAY_HOLDOUT_SCORED | False | True | mixed_readout_replay_holdout_endpoint_small_n_not_validation |
| NGC7331 | 36 | 59.3544 | 25.4851 | 29.3117 | 23.473 | 22.7324 | -36.622 | -2.75268 | -6.57929 | -0.740593 | True | True | True | True | NGC7331 | K_expdisk_vertical_outer_warp_fractional_onset_v2 | NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1 | V2_REPLAY_FRACTIONAL_ONSET_HOLDOUT_SCORED | False | True | mixed_readout_replay_holdout_endpoint_small_n_not_validation |

## Matched vs Wrong Labels

| galaxy | matched_rmse | wrong_best_rmse | matched_minus_wrong_best | matched_rank_within_galaxy | matched_beats_all_wrong_labels | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | 16.3725 | 16.3487 | 0.0238101 | 2 | False | mixed_readout_replay_holdout_endpoint_small_n_not_validation |
| NGC7331 | 22.7324 | 22.6682 | 0.0641335 | 2 | False | mixed_readout_replay_holdout_endpoint_small_n_not_validation |

## Shuffled Label Permutations

| assignment_id | assignment_role | mean_rmse | sum_rmse | n_matched_labels | claim_boundary | rank_by_mean_rmse |
| --- | --- | --- | --- | --- | --- | --- |
| NGC5907->NGC7331;NGC7331->NGC5907 | shuffled_label_null | 19.5085 | 39.017 | 0 | mixed_readout_replay_holdout_endpoint_small_n_not_validation | 1 |
| NGC5907->NGC5907;NGC7331->NGC7331 | matched_diagonal | 19.5525 | 39.1049 | 2 | mixed_readout_replay_holdout_endpoint_small_n_not_validation | 2 |

## Claim Boundary

This is a two-case replay/holdout endpoint. It is not population validation,
not a universal baseline-superiority claim, and not a replacement for the
larger predeclared population test.
