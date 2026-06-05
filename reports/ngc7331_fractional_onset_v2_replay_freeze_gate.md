# NGC7331 Fractional-Onset V2 Replay Freeze Gate

This gate freezes a V2 replay protocol from the fractional warp-onset source
gate. It does not score the rotation curve and it does not update the
already scored NGC7331 V1 accepted endpoint.

## Summary

| galaxy | formula_id | v2_replay_freeze_status | parent_v1_formula_id | v1_window_inner_kpc | v1_window_outer_kpc | v2_window_inner_kpc | v2_window_outer_kpc | fractional_warp_onset_over_Rdisk | fractional_warp_onset_over_RHI | n_gates | n_pass_like | n_replay_blocked | uses_vobs_or_residual_in_construction | formula_update_allowed_for_current_endpoint | v2_replay_scores_allowed_by_this_gate | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1 | V2_REPLAY_PROTOCOL_READY_NOT_SCORED | NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1 | 5.02 | 27.01 | 14.4317 | 27.01 | 2.87484 | 0.534309 | 6 | 5 | 1 | False | False | False | False | ngc7331_fractional_onset_v2_replay_freeze_not_score |

## V2 Frozen Manifest

| galaxy | formula_id | mixed_readout_candidate | carrier | formula_text | delta_text | kernel_text | sign_rule | carrier_selection_rule | overlay_selection_rule | amplitude_rule | r_window_inner_kpc | r_window_outer_kpc | intrinsic_h_over_Rs_mid | projected_hwhm_over_Rs | projected_hwhm_over_RHI | vertical_activation_candidate | gamma_vow | outer_warp_numeric_onset_available | outer_warp_context_present | dimension_check | inactive_window_limit | zero_amplitude_limit | vertical_absent_limit | caveat_status | source_rule_candidate | uses_vobs_or_residual_in_construction | formula_frozen_before_mixed_scoring | mixed_endpoint_scores_allowed | prospective_mixed_protocol_ready | claim_boundary | parent_formula_id | formula_version | v1_broad_window_inner_kpc | v1_broad_window_outer_kpc | fractional_onset_source_status | fractional_warp_onset_arcmin | fractional_warp_onset_kpc | fractional_warp_onset_over_Rdisk | fractional_warp_onset_over_RHI | formula_frozen_before_replay_scoring | formula_update_allowed_for_current_endpoint | replay_or_holdout_required | v2_replay_scores_allowed_by_this_gate | current_v1_endpoint_scores_allowed_by_this_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1 | K_expdisk_thick_outer_warp_overlay_review | v_K_exponential_disk | v_mix^2(R)=v_K_exponential_disk^2(R)*(1-gamma_vow*K_vow(R)) | Delta v_mix^2(R)=-gamma_vow*K_vow(R)*v_K_exponential_disk^2(R) | K_vow_v2(R)=W_outer(R;R_onset_frac,R_HI)*(0.5/(1+R/R_s)+0.5*projected_hwhm_over_Rs) | attenuation_not_added_gravity | smooth_exponential_disk_carrier_from_positive_SPARK_Rdisk_and_caveated_mixed_queue | accepted_vertical_scale_fields_plus_Bosma_fractional_Holmberg_warp_onset | gamma_vow=min(0.75,0.5*vertical_activation_candidate) | 14.431691252428111 | 27.01 | 0.0298804780876494 | 0.099601593625498 | 0.0185116623472787 | 0.6308100929614875 | 0.3154050464807437 | True | True | PASS: gamma_vow and K_vow_v2 are dimensionless; correction has velocity-squared units | W_outer=0 before V2 onset implies v_mix=v_K_exponential_disk | gamma_vow=0 implies v_mix=v_K_exponential_disk | vertical_activation_candidate=0 blocks the mixed overlay amplitude | V2_REPLAY_FRACTIONAL_ONSET_SOURCE_READY_NOT_SCORED | True | False | True | False | True | ngc7331_fractional_onset_v2_replay_freeze_not_score | NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1 | V2_REPLAY_FRACTIONAL_ONSET | 5.02 | 27.01 | FRACTIONAL_WARP_ONSET_SOURCE_READY_REPLAY_REQUIRED | 3.375 | 14.431691252428111 | 2.874838894905998 | 0.5343091911302521 | True | False | True | False | False |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | v2_replay_scores_allowed_by_this_gate | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1 | N7331_V2G1_SOURCE_ONSET_READY | PASS | FRACTIONAL_WARP_ONSET_SOURCE_READY_REPLAY_REQUIRED | none at V2 source-onset freeze level | False | False | False | ngc7331_fractional_onset_v2_replay_freeze_not_score |
| NGC7331 | NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1 | N7331_V2G2_WINDOW_REPLACEMENT_DEFINED | PASS | V1 window 5.02->27.01 kpc; V2 replay window 14.4317->27.01 kpc | do not apply V2 window to the already scored V1 endpoint | False | False | False | ngc7331_fractional_onset_v2_replay_freeze_not_score |
| NGC7331 | NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1 | N7331_V2G3_DIMENSION_AND_LIMITS | PASS | dimensionless window/kernel times velocity-squared carrier | none at formula-shell level | False | False | False | ngc7331_fractional_onset_v2_replay_freeze_not_score |
| NGC7331 | NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1 | N7331_V2G4_ENDPOINT_BLINDNESS | PASS | uses V1 source manifest and fractional-onset source gate only | replay scoring must remain a separate script | False | False | False | ngc7331_fractional_onset_v2_replay_freeze_not_score |
| NGC7331 | NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1 | N7331_V2G5_REPLAY_REQUIRED | BLOCKED_REPLAY_REQUIRED | V2 source onset was introduced after the V1 endpoint score | predeclare replay/holdout scoring before reading V2 endpoint RMSE | False | False | False | ngc7331_fractional_onset_v2_replay_freeze_not_score |
| NGC7331 | NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1 | N7331_V2G6_NO_RETROACTIVE_ENDPOINT_UPDATE | PASS | formula_update_allowed_for_current_endpoint=False | V1 accepted endpoint remains unchanged | False | False | False | ngc7331_fractional_onset_v2_replay_freeze_not_score |

## Claim Boundary

The V2 formula is replay/holdout-ready but not endpoint-scored. The current
NGC7331 V1 score remains the caveated accepted endpoint. Any V2 score must
come from a separate predeclared replay or holdout script.
