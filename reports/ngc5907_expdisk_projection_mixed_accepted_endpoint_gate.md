# NGC5907 Exponential-Disk + Projection Mixed Accepted Endpoint Gate

This gate promotes the frozen NGC5907 mixed readout protocol to a
single-galaxy accepted endpoint gate. It does not score the curve.

## Summary

| galaxy | formula_id | accepted_endpoint_freeze_status | n_gates | n_pass_like | n_caveated | n_blocked | source_rule_candidate | formula_frozen_before_endpoint_scoring | previous_projection_endpoint_used_as_mixed_evidence | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | ACCEPTED_MIXED_ENDPOINT_FREEZE_READY | 6 | 6 | 1 | 0 | True | True | False | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_gate_not_score |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MAEG1_SOURCE_RULE_READY | PASS | K_expdisk_projection_warp_vertical_overlay_review | none for this single-galaxy mixed endpoint gate | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_gate_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MAEG2_FORMULA_FROZEN_BEFORE_SCORING | PASS | MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING | scoring script must read this manifest unchanged | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_gate_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MAEG3_ENDPOINT_BLIND_CONSTRUCTION | PASS | freeze construction uses source queue and frozen projection manifest only | vobs may enter only in the separate endpoint scoring script | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_gate_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MAEG4_PRIOR_PROJECTION_NOT_MIXED_EVIDENCE | PASS_CAVEATED | previous_projection_endpoint_used_as_mixed_evidence=False | preserve this caveat: prior projection endpoint is control context, not mixed-label evidence | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_gate_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MAEG5_NO_BLOCKED_FREEZE_GATES | PASS | n_blocked=0 | none | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_gate_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MAEG6_NO_RETUNING_RULE | PASS | posthoc_retuning_allowed=False; sign, carrier, kernel, amplitude, and window are frozen | any post-score formula change demotes this row to diagnostic | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_gate_not_score |

## Frozen Manifest

| galaxy | formula_id | mixed_readout_candidate | carrier | overlay_formula_id | formula_text | delta_text | kernel_text | sign_rule | carrier_selection_rule | overlay_selection_rule | amplitude_rule | r_in_kpc | r_out_kpc | truncation_contrast | pi_projection | h_over_r | gamma_projection | disk_scale_kpc | warp_displacement_kpc | dimension_check | inactive_window_limit | zero_amplitude_limit | projection_absent_limit | source_rule_candidate | uses_vobs_or_residual_in_construction | formula_frozen_before_mixed_scoring | previous_projection_endpoint_used_as_mixed_evidence | previous_projection_endpoint_caveat | mixed_endpoint_scores_allowed | prospective_mixed_protocol_ready | claim_boundary | accepted_endpoint_formula_id | formula_frozen_before_endpoint_scoring | endpoint_scores_allowed | posthoc_retuning_allowed | accepted_endpoint_freeze_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | K_expdisk_projection_warp_vertical_overlay_review | v_K_exponential_disk | NGC5907_PROJECTION_ATTENUATION_V1 | v_mix^2(R)=v_K_exponential_disk^2(R)*(1-gamma_proj*K_proj(R)) | Delta v_mix^2(R)=-gamma_proj*K_proj(R)*v_K_exponential_disk^2(R) | K_proj=smoothstep((R-r_in)/(r_out-r_in))*(1+truncation_contrast*smoothstep((R-r_in)/(r_out-r_in)))/(1+truncation_contrast) | attenuation_not_added_gravity | smooth_exponential_disk_carrier_from_source_disk_truncation_scales_and_positive_disk_scale | source_windowed_projection_warp_vertical_overlay_from_NGC5907_projection_freeze | gamma_proj=0.5*Pi_projection*h_over_r | 13.3 | 24.0 | 0.7382978723404255 | 0.7891282494318128 | 0.1733207190160832 | 0.0683861377937124 | 5.34 | 1.7 | PASS: gamma_proj and K_proj are dimensionless; correction has velocity-squared units | K_proj=0 implies v_mix=v_K_exponential_disk | gamma_proj=0 implies v_mix=v_K_exponential_disk | source_rule_candidate=False blocks mixed formula use | True | False | True | False | True | False | True | ngc5907_expdisk_projection_mixed_accepted_endpoint_gate_not_score | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | True | True | False | ACCEPTED_MIXED_ENDPOINT_FREEZE_READY |

## Formula-Freeze Gate Input

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | mixed_endpoint_scores_allowed | prospective_mixed_protocol_ready | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MXF1_QUEUE_SOURCE_RULE | PASS | P0_FORMULA_FREEZE_CANDIDATE_REVIEW_REQUIRED | source rule supports formula-freeze candidate only; scoring remains separate | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MXF2_CARRIER_FREEZE | PASS_CAVEATED | carrier=v_K_exponential_disk; disk_scale_kpc=5.34; disk/truncation scales are source fields | future population use must apply the same carrier rule before mixed scoring | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MXF3_PROJECTION_KERNEL_REUSE | PASS | NGC5907_PROJECTION_ATTENUATION_V1 | use the already frozen projection kernel unchanged | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MXF4_DIMENSION_AND_LIMITS | PASS | dimensionless attenuation times velocity-squared carrier; K=0 and gamma=0 recover carrier | none at formula-shell level | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MXF5_ENDPOINT_BLINDNESS | PASS | construction reads queue row and projection freeze manifest only; no vobs or residuals | mixed scoring, if run, must be a separate script reading this manifest unchanged | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MXF6_PRIOR_PROJECTION_ENDPOINT_CAVEAT | PASS_CAVEATED | prior projection endpoint exists, but previous_projection_endpoint_used_as_mixed_evidence=False | do not count the earlier projection endpoint as mixed-readout validation | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |

## Claim Boundary

The earlier NGC5907 projection endpoint is not counted as evidence for
the mixed readout label. It is control context only. Endpoint scoring
must be run by a separate script that reads this accepted manifest
unchanged.
