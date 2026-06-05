# NGC4013 Mixed Overlay Prospective Replay Gate

Status: `NGC4013_MIXED_OVERLAY_PROSPECTIVE_REPLAY_RECORDED_NOT_VALIDATION`

This gate records the frozen NGC4013 mixed-overlay score under the new
readout-lane freeze discipline. It is a replay/continuity check, not
retroactive endpoint validation.

## Summary

| galaxy | prospective_replay_gate_status | lane_status | formula_freeze_status | rmse_frozen_protocol | beats_tpg_v6_by_km_s | beats_expdisk_by_km_s | beats_wvo_by_km_s | validation_claim_allowed | endpoint_scores_allowed | future_population_protocol_candidate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | NGC4013_MIXED_OVERLAY_PROSPECTIVE_REPLAY_RECORDED_NOT_VALIDATION | FROZEN_PASS_CAVEATED_PROSPECTIVE_ONLY | MIXED_FORMULA_FREEZE_READY_NOT_RETROACTIVE_ENDPOINT | 10.6148 | 1.65915 | 0.265449 | 0.835737 | False | False | True | ngc4013_mixed_overlay_prospective_replay_gate_not_validation |

## Score Summary

| galaxy | formula_id | n_points | rmse_expdisk_wvo_frozen_protocol | rmse_exponential_disk | rmse_warp_vertical_overlay | rmse_tpg_v6 | rmse_mond | frozen_minus_expdisk | frozen_minus_wvo | frozen_minus_tpg_v6 | score_role | validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | 36 | 10.6148 | 10.8802 | 11.4505 | 12.2739 | 14.3342 | -0.265449 | -0.835737 | -1.65915 | prospective_protocol_replay_continuity_check | False | ngc4013_mixed_overlay_prospective_replay_gate_not_validation |

## Gates

| gate_id | gate_status | evidence | remaining_obligation | galaxy | endpoint_scores_allowed | validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| N4013_PRG1_SOURCE_FREEZE_REVIEW | PASS_CAVEATED | NGC4013_MIXED_OVERLAY_SOURCE_FREEZE_PASS_CAVEATED_PROSPECTIVE_ONLY | keep prior diagnostic score out of label evidence | NGC4013 | False | False | ngc4013_mixed_overlay_prospective_replay_gate_not_validation |
| N4013_PRG2_LANE_FREEZE | PASS_CAVEATED | L_mixed_overlay_protocol_ready_not_retroactive | no retroactive validation claim | NGC4013 | False | False | ngc4013_mixed_overlay_prospective_replay_gate_not_validation |
| N4013_PRG3_FORMULA_FREEZE | PASS | MIXED_FORMULA_FREEZE_READY_NOT_RETROACTIVE_ENDPOINT | use same manifest unchanged in future population tests | NGC4013 | False | False | ngc4013_mixed_overlay_prospective_replay_gate_not_validation |
| N4013_PRG4_RETROACTIVE_CLAIM_BOUNDARY | PASS | retrospective_endpoint_scores_allowed=False | score can be continuity evidence only | NGC4013 | False | False | ngc4013_mixed_overlay_prospective_replay_gate_not_validation |
| N4013_PRG5_REPLAY_SCORE | PASS_RECORDED_NOT_VALIDATION | frozen protocol RMSE=10.6148 | repeat prospectively on future predeclared cases | NGC4013 | False | False | ngc4013_mixed_overlay_prospective_replay_gate_not_validation |

## Interpretation

The frozen mixed-overlay protocol remains numerically strong for NGC4013:
`RMSE = 10.6148 km/s`, better
than the TPG/v6 proxy by `1.65915 km/s`.
However, because this galaxy had already been inspected diagnostically, this
score is not an accepted endpoint validation. Its proper role is to define a
future population protocol candidate.

## Claim Boundary

`ngc4013_mixed_overlay_prospective_replay_gate_not_validation`
