# NGC4013 Exponential-Disk + WVO Mixed Formula Freeze Gate

This gate freezes the mixed formula selected by the residual-blind mixed
source rule. It does not read observed velocities and does not convert the
existing diagnostic score into an accepted endpoint.

## Summary

| galaxy | formula_id | mixed_readout_candidate | source_rule_pass | overlay_formula_frozen | uses_vobs_or_residual_in_construction | n_kernel_grid_rows | n_gates | n_pass_like | n_retrospective_blockers | formula_freeze_status | retrospective_endpoint_scores_allowed | prospective_endpoint_protocol_ready | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | K_expdisk_warp_vertical_overlay | True | True | False | 7 | 6 | 5 | 1 | MIXED_FORMULA_FREEZE_READY_NOT_RETROACTIVE_ENDPOINT | False | True | ngc4013_expdisk_wvo_formula_freeze_not_retroactive_endpoint |

## Frozen Manifest

| galaxy | formula_id | mixed_readout_candidate | carrier | overlay_formula_id | formula_text | delta_text | kernel_text | sign_rule | carrier_selection_rule | overlay_selection_rule | amplitude_rule | gamma_overlay_upper | r_warp_kpc | r_outer_kpc | r_lag_start_kpc | r_lag_zero_kpc | r_s_kpc | z_ec_kpc | omega_z | omega_ec | omega_lag | dimension_check | inactive_window_limit | zero_amplitude_limit | overlay_absent_limit | uses_vobs_or_residual_in_construction | formula_frozen_before_scoring | retrospective_endpoint_scores_allowed | prospective_endpoint_protocol_ready | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | K_expdisk_warp_vertical_overlay | v_K_exponential_disk | NGC4013_WARP_VERTICAL_OVERLAY_V1 | v_mix^2(R)=v_K_exponential_disk^2(R)*(1-Gamma_wvo*K_wvo(R)) | Delta v_mix^2(R)=-Gamma_wvo*K_wvo(R)*v_K_exponential_disk^2(R) | K_wvo=W_warp*(omega_z*K_z+omega_EC*K_EC+omega_lag*K_lag) | attenuation_not_added_gravity | smooth_disk_carrier_from_source_component_and_disk_scale | source_windowed_warp_vertical_lag_overlay | Gamma_wvo <= 0.5*h_over_Rs + 0.5*f_EC | 0.216466 | 10 | 11.2 | 5.8 | 11.2 | 2.39023 | 3 | 0.333333 | 0.333333 | 0.333333 | PASS: Gamma_wvo and K_wvo are dimensionless; correction has velocity-squared units | K_wvo=0 implies v_mix=v_K_exponential_disk | Gamma_wvo=0 implies v_mix=v_K_exponential_disk | source_rule_pass=False or overlay_modifier_gate=False blocks mixed formula | False | True | False | True | ngc4013_expdisk_wvo_formula_freeze_not_retroactive_endpoint |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | retrospective_endpoint_scores_allowed | prospective_endpoint_protocol_ready | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | MXF1_GENERAL_MIXED_SOURCE_RULE | PASS | MIXED_SOURCE_RULE_PASS_FORMULA_FREEZE_REQUIRED | none for source-rule selection; formula gate still needed | False | True | ngc4013_expdisk_wvo_formula_freeze_not_retroactive_endpoint |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | MXF2_CARRIER_FREEZE | PASS_CAVEATED | carrier is v_K_exponential_disk selected by the mixed source rule from disk component plus disk scale | future sample-level use should apply the same carrier rule before scoring | False | True | ngc4013_expdisk_wvo_formula_freeze_not_retroactive_endpoint |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | MXF3_OVERLAY_KERNEL_REUSE | PASS | NGC4013_WARP_VERTICAL_OVERLAY_V1 | none; use the already frozen WVO kernel unchanged | False | True | ngc4013_expdisk_wvo_formula_freeze_not_retroactive_endpoint |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | MXF4_DIMENSION_AND_LIMITS | PASS | dimensionless attenuation times velocity-squared carrier; K=0 and Gamma=0 recover carrier | none at formula-shell level | False | True | ngc4013_expdisk_wvo_formula_freeze_not_retroactive_endpoint |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | MXF5_ENDPOINT_BLINDNESS | PASS | manifest construction reads source-rule fields and WVO freeze manifest only; no vobs | scoring must remain in a separate script | False | True | ngc4013_expdisk_wvo_formula_freeze_not_retroactive_endpoint |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | MXF6_RETROACTIVE_ENDPOINT_STATUS | BLOCKED_RETROACTIVE_ENDPOINT | NGC4013 mixed branch was previously inspected diagnostically after wrong-family controls | use as prospective/preregistered formula protocol, not as retroactive accepted endpoint validation | False | True | ngc4013_expdisk_wvo_formula_freeze_not_retroactive_endpoint |

## Claim Boundary

The formula is now suitable as a prospective/preregistered mixed-readout
protocol. The already inspected NGC4013 diagnostic score remains
diagnostic evidence, not a retroactive accepted endpoint validation.
