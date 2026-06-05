# NGC7331 V2/V3 Replay/Holdout Endpoint

This dedicated replay/holdout endpoint scores the NGC7331 V2 fractional
onset and V3 source-sharpened manifests. It does not update the accepted
V1 endpoint.

## Summary

| endpoint_status | galaxy | n_points | v1_reference_rmse_km_s | v2_fractional_onset_rmse_km_s | v3_source_sharpened_rmse_km_s | best_baseline_rmse_km_s | wrong_projection_sharpened_rmse_km_s | v3_minus_v1_rmse_km_s | v3_minus_v2_rmse_km_s | v3_minus_best_baseline_rmse_km_s | v3_minus_wrong_projection_rmse_km_s | v3_beats_v1_reference | v3_beats_v2_fractional_onset | v3_beats_best_baseline | v3_beats_wrong_projection_control | current_v1_endpoint_updated | construction_used_vobs | scoring_used_vobs | claim_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331_V2_V3_REPLAY_HOLDOUT_PRELIMINARY_CONTROL_RESULT | NGC7331 | 36 | 22.2557 | 22.7324 | 22.1308 | 23.473 | 22.9064 | -0.124817 | -0.601535 | -1.34213 | -0.775549 | True | True | True | True | False | False | True | dedicated NGC7331 replay/holdout result; not a retroactive V1 endpoint update | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | mae_km_s | construction_used_vobs | scoring_used_vobs | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | TAU_NGC7331_V3_SOURCE_SHARPENED_REPLAY | matched_v3_replay | 36 | 22.1308 | 17.1125 | False | True | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |
| NGC7331 | TAU_NGC7331_V1_ACCEPTED_REFERENCE_NOT_UPDATED | v1_accepted_reference | 36 | 22.2557 | 17.631 | False | True | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |
| NGC7331 | TAU_NGC7331_V2_FRACTIONAL_ONSET_REPLAY | matched_v2_replay | 36 | 22.7324 | 18.3271 | False | True | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |
| NGC7331 | WRONG_SHARPENED_NGC5907_PROJECTION | wrong_sharpened_replay_control | 36 | 22.9064 | 18.592 | False | True | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |
| NGC7331 | EXPONENTIAL_DISK_CARRIER | baseline | 36 | 23.473 | 19.5632 | False | True | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |
| NGC7331 | TPG_V6_v_v6 | baseline | 36 | 25.4851 | 22.2152 | False | True | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |
| NGC7331 | MOND_v_mond | baseline | 36 | 29.3117 | 26.452 | False | True | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |
| NGC7331 | NEWTONIAN_vn | baseline | 36 | 59.3544 | 51.4592 | False | True | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |

## Gates

| gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | current_v1_endpoint_updated | uses_vobs_or_residual_in_construction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| N7331_RHG1_V2_FREEZE_READY | PASS | V2_REPLAY_PROTOCOL_READY_NOT_SCORED | none at V2 replay-freeze level | True | False | False | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |
| N7331_RHG2_V3_SHARPENED_FREEZE_READY | PASS | SHARPENED_REPLAY_FREEZE_READY_NOT_SCORED | none at V3 sharpened-freeze level | True | False | False | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |
| N7331_RHG3_ENDPOINT_BLIND_CONSTRUCTION | PASS | all replay manifests have uses_vobs_or_residual_in_construction=false | scoring reads vobs only in this script | True | False | False | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |
| N7331_RHG4_NO_RETROACTIVE_V1_UPDATE | PASS | current_v1_endpoint_updated=false | accepted V1 score remains caveated accepted endpoint | True | False | False | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |
| N7331_RHG5_REPLAY_CONTROL_SCOPE | PASS_CLAIM_BOUNDED | single-galaxy replay/holdout control | do not use as population validation | True | False | False | ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update |

## Claim Boundary

Status: this is not a retroactive update of the accepted V1 endpoint.

The result is a single-galaxy replay/holdout control. It can reduce the
NGC7331 broad-window caveat for the replay path, but it is not a
retroactive update of the already accepted V1 endpoint and not population
validation.
