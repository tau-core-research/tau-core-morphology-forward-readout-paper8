# Mixed Kernel Sharpened Replay Freeze

This gate freezes source-sharpened replay formulas. It does not score
rotation curves and does not update accepted endpoint rows.

## Summary

| freeze_status | n_formulas_frozen | n_gates | n_pass_like | uses_vobs_or_residual_in_construction | endpoint_scores_allowed_by_this_gate | current_kernel_cross_similarity | source_sharpened_kernel_cross_similarity | kernel_shape_separation_gain | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SHARPENED_REPLAY_FREEZE_READY_NOT_SCORED | 2 | 4 | 4 | False | False | 0.991418 | 0.643996 | 0.347422 | mixed_kernel_sharpened_replay_freeze_not_score |

## Manifest

| galaxy | formula_id | parent_formula_id | source_matched_formula | carrier | kernel_label | kernel_formula | gamma | r_window_inner_kpc | r_window_outer_kpc | projection_bound | truncation_contrast | projection_edge_exponent | vertical_decay | projected_thickness_norm | dimension_check | known_limit_check | formula_frozen_before_sharpened_replay_scoring | uses_vobs_or_residual_in_construction | endpoint_scores_allowed_by_this_gate | freeze_status | claim_boundary | fractional_warp_onset_over_RHI | vertical_activation_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_SHARPENED_REPLAY_V2 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | K_expdisk_projection_mixed | v_K_exponential_disk | K_projection_source_sharpened | K_proj_sharp(u)=S(u)^(1+Pi_projection+C_trunc) *(1+C_trunc*S(u))/(1+C_trunc) | 0.0683861 | 13.3 | 24 | 0.7891282494318128 | 0.7382978723404255 | 2.5274261217722382 | <NA> | <NA> | PASS: u, S(u), Pi_projection, and C_trunc are dimensionless | Pi_projection=0 and C_trunc=0 recovers a simple active-window kernel; inactive window gives K=0 | True | False | False | SHARPENED_REPLAY_FREEZE_READY_NOT_SCORED | mixed_kernel_sharpened_replay_freeze_not_score | nan | nan |
| NGC7331 | NGC7331_VOW_SHARPENED_REPLAY_V3 | NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1 | K_expdisk_vertical_outer_warp_v2 | v_K_exponential_disk | K_vertical_outer_warp_source_sharpened | K_vow_sharp(u)=S(u)*exp(-(1+R_onset/R_HI+A_vertical)u) + T_projected*S(u)*(1-S(u)) | 0.315405 | 14.4317 | 27.01 | <NA> | <NA> | <NA> | 2.1651192840917393 | 0.398406374501992 | PASS: u, S(u), R_onset/R_HI, A_vertical, and T_projected are dimensionless | absent fractional onset or absent vertical activation blocks this lane; inactive window gives K=0 | True | False | False | SHARPENED_REPLAY_FREEZE_READY_NOT_SCORED | mixed_kernel_sharpened_replay_freeze_not_score | 0.534309 | 0.63081 |

## Gates

| gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| MSKRF1_PREFLIGHT_READY | PASS | SOURCE_KERNEL_SHARPENING_PREFLIGHT_READY_NOT_ENDPOINT | none at sharpened freeze level | False | False | mixed_kernel_sharpened_replay_freeze_not_score |
| MSKRF2_DIMENSION_AND_LIMITS | PASS | all sharpened kernel coefficients are dimensionless; inactive window gives K=0; gamma=0 recovers carrier | none at formula-shell level | False | False | mixed_kernel_sharpened_replay_freeze_not_score |
| MSKRF3_ENDPOINT_BLINDNESS | PASS | construction reads source manifests and preflight formulas only | scoring must remain a separate script reading this manifest unchanged | False | False | mixed_kernel_sharpened_replay_freeze_not_score |
| MSKRF4_REPLAY_ONLY_BOUNDARY | PASS | freeze records V2/V3 replay formulas, not accepted endpoint updates | do not retroactively alter accepted NGC5907/NGC7331 rows | False | False | mixed_kernel_sharpened_replay_freeze_not_score |

## Claim Boundary

The frozen V2/V3 formulas may be used by a separate replay/holdout scoring
script. This freeze is not an endpoint result and not validation.
