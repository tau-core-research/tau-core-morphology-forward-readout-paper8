# NGC5907 Exponential-Disk + Projection Mixed Formula Freeze Gate

This gate freezes a fresh mixed readout formula for NGC5907. It does not
score the mixed endpoint and it does not reuse the previous projection
endpoint as mixed-readout evidence.

## Summary

| galaxy | formula_id | mixed_readout_candidate | source_rule_candidate | projection_formula_frozen | uses_vobs_or_residual_in_construction | previous_projection_endpoint_used_as_mixed_evidence | n_gates | n_pass_like | n_caveated | n_blocked | formula_freeze_status | mixed_endpoint_scores_allowed | prospective_mixed_protocol_ready | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | K_expdisk_projection_warp_vertical_overlay_review | True | True | False | False | 6 | 6 | 2 | 0 | MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |

## Frozen Manifest

| galaxy | formula_id | mixed_readout_candidate | carrier | overlay_formula_id | formula_text | delta_text | kernel_text | sign_rule | carrier_selection_rule | overlay_selection_rule | amplitude_rule | r_in_kpc | r_out_kpc | truncation_contrast | pi_projection | h_over_r | gamma_projection | disk_scale_kpc | warp_displacement_kpc | dimension_check | inactive_window_limit | zero_amplitude_limit | projection_absent_limit | source_rule_candidate | uses_vobs_or_residual_in_construction | formula_frozen_before_mixed_scoring | previous_projection_endpoint_used_as_mixed_evidence | previous_projection_endpoint_caveat | mixed_endpoint_scores_allowed | prospective_mixed_protocol_ready | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | K_expdisk_projection_warp_vertical_overlay_review | v_K_exponential_disk | NGC5907_PROJECTION_ATTENUATION_V1 | v_mix^2(R)=v_K_exponential_disk^2(R)*(1-gamma_proj*K_proj(R)) | Delta v_mix^2(R)=-gamma_proj*K_proj(R)*v_K_exponential_disk^2(R) | K_proj=smoothstep((R-r_in)/(r_out-r_in))*(1+truncation_contrast*smoothstep((R-r_in)/(r_out-r_in)))/(1+truncation_contrast) | attenuation_not_added_gravity | smooth_exponential_disk_carrier_from_source_disk_truncation_scales_and_positive_disk_scale | source_windowed_projection_warp_vertical_overlay_from_NGC5907_projection_freeze | gamma_proj=0.5*Pi_projection*h_over_r | 13.3 | 24 | 0.738298 | 0.789128 | 0.173321 | 0.0683861 | 5.34 | 1.7 | PASS: gamma_proj and K_proj are dimensionless; correction has velocity-squared units | K_proj=0 implies v_mix=v_K_exponential_disk | gamma_proj=0 implies v_mix=v_K_exponential_disk | source_rule_candidate=False blocks mixed formula use | True | False | True | False | True | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | mixed_endpoint_scores_allowed | prospective_mixed_protocol_ready | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MXF1_QUEUE_SOURCE_RULE | PASS | P0_FORMULA_FREEZE_CANDIDATE_REVIEW_REQUIRED | source rule supports formula-freeze candidate only; scoring remains separate | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MXF2_CARRIER_FREEZE | PASS_CAVEATED | carrier=v_K_exponential_disk; disk_scale_kpc=5.34; disk/truncation scales are source fields | future population use must apply the same carrier rule before mixed scoring | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MXF3_PROJECTION_KERNEL_REUSE | PASS | NGC5907_PROJECTION_ATTENUATION_V1 | use the already frozen projection kernel unchanged | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MXF4_DIMENSION_AND_LIMITS | PASS | dimensionless attenuation times velocity-squared carrier; K=0 and gamma=0 recover carrier | none at formula-shell level | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MXF5_ENDPOINT_BLINDNESS | PASS | construction reads queue row and projection freeze manifest only; no vobs or residuals | mixed scoring, if run, must be a separate script reading this manifest unchanged | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |
| NGC5907 | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | N5907_MXF6_PRIOR_PROJECTION_ENDPOINT_CAVEAT | PASS_CAVEATED | prior projection endpoint exists, but previous_projection_endpoint_used_as_mixed_evidence=False | do not count the earlier projection endpoint as mixed-readout validation | False | True | ngc5907_expdisk_projection_mixed_formula_freeze_not_score |

## Claim Boundary

The formula is ready as a prospective mixed protocol prior to mixed
scoring. Because NGC5907 already has a projection endpoint, the earlier
projection score is treated only as a caveat/control context, not as
evidence for the mixed formula.
