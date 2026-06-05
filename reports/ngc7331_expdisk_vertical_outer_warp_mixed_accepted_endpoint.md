# NGC7331 Exponential-Disk + Vertical/Outer-Warp Mixed Accepted Endpoint

This run scores the frozen caveated NGC7331 mixed endpoint protocol.
The formula is read from the accepted endpoint manifest unchanged.
Observed velocities enter only in the scoring block.

## Summary

| endpoint_status | galaxy | formula_id | n_points | rmse_mixed_accepted | best_baseline_model | best_baseline_rmse_km_s | wrong_mixed_mean_rmse_km_s | wrong_mixed_best_rmse_km_s | matched_minus_best_baseline_rmse_km_s | matched_minus_wrong_mixed_mean_rmse_km_s | matched_minus_best_wrong_mixed_rmse_km_s | matched_rank_among_all_models | matched_beats_all_baselines | matched_beats_all_wrong_mixed_families | outer_warp_numeric_onset_available | broad_outer_window_caveat_attached | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | claim_boundary | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAVEATED_ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT | NGC7331 | NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1 | 36 | 22.2557 | EXPONENTIAL_DISK_CARRIER | 23.473 | 22.6731 | 22.6682 | -1.21731 | -0.417405 | -0.412584 | 1 | True | True | False | True | False | True | True | ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_preliminary_control | caveated accepted single-galaxy mixed control endpoint; not population validation |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | mae_km_s | construction_used_vobs | scoring_used_vobs | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | TAU_NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_ACCEPTED | matched_caveated_frozen_mixed_readout | 36 | 22.2557 | 17.631 | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_preliminary_control |
| NGC7331 | WRONG_MIXED_NGC5907_PROJ | wrong_mixed_family_control | 36 | 22.6682 | 18.2649 | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_preliminary_control |
| NGC7331 | WRONG_MIXED_NGC4013_WVO | wrong_mixed_family_control | 36 | 22.6779 | 18.3413 | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_preliminary_control |
| NGC7331 | EXPONENTIAL_DISK_CARRIER | baseline | 36 | 23.473 | 19.5632 | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_preliminary_control |
| NGC7331 | TPG_V6_v_v6 | baseline | 36 | 25.4851 | 22.2152 | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_preliminary_control |
| NGC7331 | MOND_v_mond | baseline | 36 | 29.3117 | 26.452 | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_preliminary_control |
| NGC7331 | NEWTONIAN_vn | baseline | 36 | 59.3544 | 51.4592 | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_preliminary_control |

## Claim Boundary

This is a caveated accepted single-galaxy mixed control endpoint. It
preserves the broad outer-window caveat because no numeric outer-warp
onset has been extracted. It is not population validation.

## Figure

paper8_submission_source/figures/fig12_ngc7331_vertical_outer_warp_mixed_accepted_endpoint.png
