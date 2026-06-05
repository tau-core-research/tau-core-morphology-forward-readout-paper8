# NGC7331 B2 Exact Transfer Formula-Freeze Gate

This gate freezes an interval-valued exact B2 transfer formula for NGC7331.
It does not score an endpoint and it does not collapse the q_warp interval
to whichever value would fit the rotation curve.

## Summary

| galaxy | formula_id | formula_freeze_status | q_warp_min | q_warp_max | x_w_formula_freeze | vflat_km_s | lambda_w_min_km2_s2 | lambda_w_max_km2_s2 | epsilon_cross_bound | lambda_w_min_cross_caveated_km2_s2 | lambda_w_max_cross_caveated_km2_s2 | n_kernel_grid_rows | n_pass_like | n_caveated | n_blocked | uses_vobs_or_residual_in_construction | formula_frozen_before_endpoint_scoring | prospective_endpoint_protocol_ready | endpoint_scores_allowed | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FORMULA_FREEZE_READY_NOT_SCORE | 0.00794045 | 0.205796 | 0.534309 | 239 | 242.345 | 6280.94 | 0.488571 | 123.942 | 9349.63 | 36 | 7 | 3 | 0 | False | True | True | False | build separate accepted endpoint gate or predeclared interval-control audit before any scoring | ngc7331_b2_exact_transfer_formula_freeze_not_score |

## Manifest

| galaxy | formula_id | readout_family | carrier | formula_text | delta_text | kernel_text | amplitude_rule | q_transfer_convention_caveat | x_w_formula_freeze | q_warp_min | q_warp_max | q_warp_rule | sigma_warp | sigma_rule | vflat_km_s | lambda_w_min_km2_s2 | lambda_w_max_km2_s2 | epsilon_cross_bound | lambda_w_min_cross_caveated_km2_s2 | lambda_w_max_cross_caveated_km2_s2 | turn_on_power_frozen | turn_on_power_rule | rhi_kpc | profile_source | dimension_check | inactive_window_limit | zero_source_limit | cross_term_caveat | law_level_caveat | uses_vobs_or_residual_in_construction | formula_frozen_before_endpoint_scoring | endpoint_scores_allowed | prospective_endpoint_protocol_ready | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | K_warp_history_exact_b2_transfer_interval | v_Newtonian_baryonic | v_readout^2(R)=v_Newtonian_baryonic^2(R)+lambda_w*C_warp(R/R_HI;x_w,p) | Delta v^2_warp(R;p)=lambda_w*C_warp(R/R_HI;x_w,p) | C_warp(x;x_w,p)=q_warp*max(0,(x-x_w)/(1-x_w))^p | lambda_w=sigma_warp*q_warp*x_w*Vflat^2 | strictly transfers the existing NGC4088 B2 q-in-lambda and q-in-kernel convention; final Tau-side q placement remains law-level open | 0.534309 | 0.00794045 | 0.205796 | CARRY_INTERVAL from source-only THINGS centroid/envelope review | 1 | positive exact-transfer branch carried from MOM1 orientation context; not endpoint selected | 239 | 242.345 | 6280.94 | 0.488571 | 123.942 | 9349.63 | 1 | minimal linear onset ramp transferred from NGC4088 protocol | 27.01 | ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_points.csv columns r,vn only | PASS: lambda_w interval has km^2 s^-2 units; C_warp interval is dimensionless; Delta v^2 interval has velocity-squared units | R/R_HI <= x_w implies C_warp=0 and v_readout=v_Newtonian_baryonic for the full interval | q_warp=0 or sigma_warp=0 implies Delta v^2=0 and carrier recovery | epsilon_cross is carried as an interval-widening caveat, not as endpoint-tuned error | B2 source-load law, q placement, sign law, and population transfer remain open | False | True | False | True | ngc7331_b2_exact_transfer_formula_freeze_not_score |

## Factors

| galaxy | formula_id | factor_id | symbol | value | unit | factor_status | source_evidence | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF1_XW | x_w | 0.5343091911302521 | dimensionless | SOURCE_ONSET_AVAILABLE_REPLAY_ONLY | Bosma/NED fractional Holmberg onset converted with SPARC distance and R_HI | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF2_Q_INTERVAL | q_warp | [0.0079404475812108, 0.2057957876154617] | dimensionless_interval | SOURCE_ONLY_INTERVAL_CARRIED | Centroid and outer-envelope measurements are both source-native THINGS observables and differ by a large factor, so the review does not select a unique q_warp carrier by fiat. It carries the full interval into the formula-freeze preparation and uses MOM1 only for residual-blind orientation/cross-term context. | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF3_SIGMA | sigma_warp | 1.0 | dimensionless_sign | SOURCE_CONTEXT_CARRIED_AS_POSITIVE_TRANSFER_BRANCH | MOM1_CONTEXT_CONSISTENT_RECEDING_SIDE_ORIENTATION_CARRIED_TO_FORMULA_FREEZE | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF4_VFLAT2 | Vflat^2 | 57121.0 | km2_s2 | SOURCE_CATALOG_CARRIER_INPUT | SPARC external master table | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF5_LAMBDA_INTERVAL | lambda_w | [242.34464623579163, 6280.944094952416] | km2_s2_interval | FORMULA_FREEZE_INTERVAL | lambda_w=sigma_warp*q_warp*x_w*Vflat^2 with q interval | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF6_EPSILON_CROSS | epsilon_cross | 0.488571397976179 | dimensionless_bound | CONSERVATIVE_BOUND_CARRIED | CARRY_CONSERVATIVE_SOURCE_BOUND_0.488571397976179_WITH_Q_OBSERVABLE_AMBIGUITY | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF7_LAMBDA_INTERVAL_WITH_CROSS | lambda_w_cross_caveated | [123.94198363232837, 9349.633732033544] | km2_s2_interval | CROSS_CAVEATED_INTERVAL | lambda interval widened by carried epsilon_cross bound | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | formula_freeze_ready | endpoint_scores_allowed | uses_vobs_or_residual_in_construction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF1_UPGRADE_INPUT_READY | PASS | NGC7331_EXACT_TRANSFER_UPGRADE_FORMULA_FREEZE_INPUT_READY_NOT_ENDPOINT | none at source-input readiness level | True | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF2_Q_INTERVAL_CARRIED | PASS_INTERVAL_CARRIED | q_warp=[0.00794045,0.205796] | future source theorem may collapse interval; endpoint may not choose point q | True | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF3_SIGN_BRANCH | PASS_CAVEATED | MOM1_CONTEXT_CONSISTENT_RECEDING_SIDE_ORIENTATION_CARRIED_TO_FORMULA_FREEZE | derive final sign law from Tau-side orientation/readout geometry | True | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF4_EPSILON_CROSS | PASS_CAVEATED | epsilon_cross_bound=0.488571 | carry cross-term bound; do not absorb it by endpoint retuning | True | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF5_DIMENSIONS_AND_LIMITS | PASS | lambda interval has velocity-squared units; kernel interval is dimensionless; inactive and zero-source limits recover carrier | none at formula-shell level | True | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF6_ENDPOINT_BLINDNESS | PASS | formula freeze reads source fields plus r/vn carrier columns only; no vobs or residuals are written to the freeze grid | any endpoint must be a separate accepted-gate script reading this manifest unchanged | True | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | N7331_B2FF7_Q_PLACEMENT_CAVEAT | PASS_CAVEATED | strict NGC4088 B2 transfer keeps q_warp in lambda_w and in C_warp | derive final Tau-side q placement or compare q-placement branches as predeclared controls | True | False | False | ngc7331_b2_exact_transfer_formula_freeze_not_score |

## Claim Boundary

The formula is frozen at protocol level only. It strictly transfers the
current NGC4088 B2 convention, including the q_warp placement in both
lambda_w and C_warp. That q-placement is preserved for reproducibility
but remains a law-level caveat for future derivation or predeclared
control comparison.
