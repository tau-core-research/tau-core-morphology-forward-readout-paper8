# NGC7331 Exponential-Disk + Vertical/Outer-Warp Mixed Formula Freeze Gate

This gate freezes a caveated NGC7331 mixed formula before mixed scoring.
It does not score the mixed endpoint. The broad outer window is used
because the current source layer has outer-warp context but no numeric
warp-onset radius.

## Summary

| galaxy | formula_id | mixed_readout_candidate | source_rule_candidate | caveat_gate_allows_formula_freeze | uses_vobs_or_residual_in_construction | outer_warp_numeric_onset_available | n_gates | n_pass_like | n_caveated | n_blocked | formula_freeze_status | mixed_endpoint_scores_allowed | prospective_mixed_protocol_ready | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1 | K_expdisk_thick_outer_warp_overlay_review | True | True | False | False | 5 | 5 | 2 | 0 | CAVEATED_MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_not_score |

## Frozen Manifest

| galaxy | formula_id | mixed_readout_candidate | carrier | formula_text | delta_text | kernel_text | sign_rule | carrier_selection_rule | overlay_selection_rule | amplitude_rule | r_window_inner_kpc | r_window_outer_kpc | intrinsic_h_over_Rs_mid | projected_hwhm_over_Rs | projected_hwhm_over_RHI | vertical_activation_candidate | gamma_vow | outer_warp_numeric_onset_available | outer_warp_context_present | dimension_check | inactive_window_limit | zero_amplitude_limit | vertical_absent_limit | caveat_status | source_rule_candidate | uses_vobs_or_residual_in_construction | formula_frozen_before_mixed_scoring | mixed_endpoint_scores_allowed | prospective_mixed_protocol_ready | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1 | K_expdisk_thick_outer_warp_overlay_review | v_K_exponential_disk | v_mix^2(R)=v_K_exponential_disk^2(R)*(1-gamma_vow*K_vow(R)) | Delta v_mix^2(R)=-gamma_vow*K_vow(R)*v_K_exponential_disk^2(R) | K_vow(R)=W_outer(R;R_s,R_HI)*(0.5/(1+R/R_s)+0.5*projected_hwhm_over_Rs) | attenuation_not_added_gravity | smooth_exponential_disk_carrier_from_positive_SPARK_Rdisk_and_caveated_mixed_queue | accepted_vertical_scale_fields_plus_context_outer_warp_caveat | gamma_vow=min(0.75,0.5*vertical_activation_candidate) | 5.02 | 27.01 | 0.0298805 | 0.0996016 | 0.0185117 | 0.63081 | 0.315405 | False | True | PASS: gamma_vow and K_vow are dimensionless; correction has velocity-squared units | W_outer=0 implies v_mix=v_K_exponential_disk | gamma_vow=0 implies v_mix=v_K_exponential_disk | vertical_activation_candidate=0 blocks the mixed overlay amplitude | CAVEATED_BROAD_OUTER_WINDOW_NO_NUMERIC_WARP_ONSET | True | False | True | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_not_score |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | mixed_endpoint_scores_allowed | prospective_mixed_protocol_ready | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1 | N7331_MXF1_CAVEAT_GATE | PASS_CAVEATED | CAVEAT_MAPPED_TO_MIXED_OVERLAY_CONTEXT_FORMULA_FREEZE_ALLOWED | numeric outer-warp onset still absent; broad source-scale window only | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_not_score |
| NGC7331 | NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1 | N7331_MXF2_VERTICAL_AMPLITUDE_MAPPING | PASS | vertical_activation_candidate=0.63081; gamma_vow=0.315405 | amplitude is source-rule candidate, not final Tau-side vertical law | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_not_score |
| NGC7331 | NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1 | N7331_MXF3_BROAD_OUTER_WINDOW | PASS_CAVEATED | R_inner=Rdisk=5.02 kpc; R_outer=RHI=27.01 kpc | replace with numeric HI/projection warp onset if extracted later | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_not_score |
| NGC7331 | NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1 | N7331_MXF4_DIMENSION_AND_LIMITS | PASS | dimensionless attenuation times velocity-squared carrier; inactive window and gamma=0 recover carrier | none at formula-shell level | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_not_score |
| NGC7331 | NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1 | N7331_MXF5_ENDPOINT_BLINDNESS | PASS | construction reads caveat summary, source queue, and SPARC scale metadata only; no vobs or residuals | mixed scoring, if run, must be a separate script reading this manifest unchanged | False | True | ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_not_score |

## Claim Boundary

The formula is a prospective, caveated protocol. It is not an endpoint
score and not proof that the mixed NGC7331 readout fits the observed
rotation curve. A future numeric HI/projection warp-onset extraction
should replace the broad Rdisk-to-RHI window.
