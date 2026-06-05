# NGC4013 Warp/Vertical-Overlay Endpoint-Freeze Gate

This gate freezes the source-side formula ingredients for the replacement
warp/vertical-overlay shell. It does not score the rotation curve because
the replacement readout label is not yet accepted for endpoint use.

## Summary

| galaxy | formula_id | r_warp_kpc | r_outer_kpc | r_lag_start_kpc | r_lag_zero_kpc | r_s_kpc | gamma_overlay_upper | n_gates | n_pass_like | n_blocked | formula_freeze_status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | NGC4013_WARP_VERTICAL_OVERLAY_V1 | 10 | 11.2 | 5.8 | 11.2 | 2.39023 | 0.216466 | 6 | 5 | 1 | FORMULA_FREEZE_PROTOCOL_READY_LABEL_BLOCKED | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |

## Frozen Manifest

| galaxy | formula_id | readout_subfamily | formula_text | kernel_text | warp_window_text | K_z_text | K_EC_text | K_lag_text | sign_rule | weight_rule | amplitude_rule | r_warp_kpc | r_outer_kpc | r25_kpc | r_lag_start_kpc | r_lag_zero_kpc | lag_inner_value_km_s_kpc | r_s_kpc | h_over_rs | z_ec_kpc | gamma_overlay_upper | omega_z | omega_ec | omega_lag | uses_vobs_or_residual_in_construction | formula_frozen_before_endpoint_scoring | accepted_replacement_label_promoted | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | NGC4013_WARP_VERTICAL_OVERLAY_V1 | K_warp_vertical_overlay_candidate | v_wvo^2(R)=v_TPG^2(R)*(1-Gamma_wvo*K_wvo(R)) | K_wvo=W_warp*(omega_z*K_z+omega_EC*K_EC+omega_lag*K_lag) | W_warp=smoothstep((R-R_w)/(R_o-R_w)) | K_z=1/(1+R/R_s) | K_EC=1/(1+R/z_EC) | K_lag=clip((R25-R)/(R25-R_lag_start),0,1) | attenuation_not_added_gravity | uniform_over_three_source_supported_channels | Gamma_wvo <= 0.5*h_over_Rs + 0.5*f_EC | 10 | 11.2 | 11.2 | 5.8 | 11.2 | -35 | 2.39023 | 0.232932 | 3 | 0.216466 | 0.333333 | 0.333333 | 0.333333 | False | True | False | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |

## Kernel Grid

| galaxy | r_kpc | W_warp | K_z | K_EC | K_lag | K_wvo | kernel_status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | 0 | 0 | 1 | 1 | 1 | 0 | SOURCE_FROZEN_KERNEL_GRID_NOT_ENDPOINT_SCORE | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |
| NGC4013 | 5.8 | 0 | 0.291839 | 0.340909 | 1 | 0 | SOURCE_FROZEN_KERNEL_GRID_NOT_ENDPOINT_SCORE | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |
| NGC4013 | 10 | 0 | 0.192912 | 0.230769 | 0.222222 | 0 | SOURCE_FROZEN_KERNEL_GRID_NOT_ENDPOINT_SCORE | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |
| NGC4013 | 11.2 | 1 | 0.175878 | 0.211268 | 0 | 0.129049 | SOURCE_FROZEN_KERNEL_GRID_NOT_ENDPOINT_SCORE | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |
| NGC4013 | 14 | 1 | 0.145832 | 0.176471 | 0 | 0.107434 | SOURCE_FROZEN_KERNEL_GRID_NOT_ENDPOINT_SCORE | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |
| NGC4013 | 16.8 | 1 | 0.124554 | 0.151515 | 0 | 0.0920232 | SOURCE_FROZEN_KERNEL_GRID_NOT_ENDPOINT_SCORE | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |
| NGC4013 | 22.4 | 1 | 0.0964181 | 0.11811 | 0 | 0.0715094 | SOURCE_FROZEN_KERNEL_GRID_NOT_ENDPOINT_SCORE | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | N4013_EFG1_FORMULA_SHELL_DERIVED | PASS | FORMULA_SHELL_DERIVED_ENDPOINT_FREEZE_BLOCKED | none at formula-shell level | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |
| NGC4013 | N4013_EFG2_OUTER_WARP_WINDOW_FREEZE | PASS_CAVEATED | source gives R25=11.2 kpc and line-of-sight warp onset near 10 kpc | independent review should verify whether R25 is acceptable as R_o | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |
| NGC4013 | N4013_EFG3_LAG_KERNEL_FREEZE | PASS_CAVEATED | lag shallows from -35 km/s/kpc at 5.8 kpc to zero near R25 | source figure digitization can later replace the linear lag-shell | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |
| NGC4013 | N4013_EFG4_WEIGHT_RULE_FREEZE | PASS_CAVEATED | uniform weights are used because all three channels are source-supported and no residual-blind hierarchy is available | derive evidence-strength weights before promotion beyond caveated freeze | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |
| NGC4013 | N4013_EFG5_ENDPOINT_BLINDNESS | PASS | construction uses source fields and the predeclared TPG carrier; vobs is forbidden | keep scoring in a separate script only after label promotion | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |
| NGC4013 | N4013_EFG6_REPLACEMENT_LABEL_PROMOTION | BLOCKED | compact lane is rejected, but K_warp_vertical_overlay_candidate is not yet an accepted endpoint label | promote replacement label with an accepted morphology manifest before endpoint scoring | False | ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score |

## Claim Boundary

The formula ingredients are source-frozen at caveated protocol level. The
row remains endpoint-label blocked: scoring before replacement-label
promotion would demote the result to a diagnostic.
