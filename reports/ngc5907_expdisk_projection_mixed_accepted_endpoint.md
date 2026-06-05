# NGC5907 Exponential-Disk + Projection Mixed Accepted Endpoint

This run scores the frozen NGC5907 mixed endpoint protocol. The formula
is read from the accepted endpoint manifest unchanged. Observed
velocities enter only in the scoring block.

## Summary

| endpoint_status | galaxy | formula_id | n_points | rmse_mixed_accepted | best_baseline_model | best_baseline_rmse_km_s | wrong_mixed_mean_rmse_km_s | wrong_mixed_best_rmse_km_s | matched_minus_best_baseline_rmse_km_s | matched_minus_wrong_mixed_mean_rmse_km_s | matched_minus_best_wrong_mixed_rmse_km_s | matched_rank_among_all_models | matched_beats_all_baselines | matched_beats_all_wrong_mixed_families | previous_projection_endpoint_used_as_mixed_evidence | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | claim_boundary | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT | NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | 19 | 16.3725 | TPG_V6_v_v6 | 16.7855 | 17.0552 | 16.848 | -0.412978 | -0.682634 | -0.475457 | 1 | True | True | False | False | True | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_preliminary_control | accepted single-galaxy mixed control endpoint; not population validation |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | mae_km_s | construction_used_vobs | scoring_used_vobs | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | TAU_NGC5907_EXPDISK_PROJECTION_MIXED_ACCEPTED | matched_frozen_mixed_readout | 19 | 16.3725 | 9.94217 | False | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_preliminary_control |
| NGC5907 | TPG_V6_v_v6 | baseline | 19 | 16.7855 | 11.4745 | False | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_preliminary_control |
| NGC5907 | WRONG_MIXED_NGC7331_VOW | wrong_mixed_family_control | 19 | 16.848 | 10.6125 | False | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_preliminary_control |
| NGC5907 | WRONG_MIXED_NGC4013_WVO | wrong_mixed_family_control | 19 | 17.2623 | 11.6311 | False | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_preliminary_control |
| NGC5907 | EXPONENTIAL_DISK_CARRIER | baseline | 19 | 17.3695 | 11.7237 | False | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_preliminary_control |
| NGC5907 | MOND_v_mond | baseline | 19 | 18.5954 | 15.1311 | False | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_preliminary_control |
| NGC5907 | NEWTONIAN_vn | baseline | 19 | 86.4837 | 85.6717 | False | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_preliminary_control |

## Claim Boundary

This is an accepted single-galaxy mixed control endpoint. The earlier
projection endpoint is not used as mixed-label evidence, and this result
is not a population validation.

## Figure

paper8_submission_source/figures/fig11_ngc5907_expdisk_projection_mixed_accepted_endpoint.png
