# NGC4088 Warp/History Formula-Freeze Gate

This gate freezes the NGC4088 warp/history formula at protocol level. It
does not score an endpoint and it does not claim a final Tau-side
physical-normalization law.

## Summary

| galaxy | formula_id | formula_freeze_status | b1_status | b2_protocol_status | b3_protocol_status | b2_law_level_open | b3_law_level_open | x_w_formula_freeze | vflat_km_s | q_warp | sigma_warp | turn_on_power_frozen | lambda_w_km2_s2 | n_kernel_grid_rows | n_pass_like | n_caveated | n_blocked | uses_vobs_or_residual_in_construction | formula_frozen_before_endpoint_scoring | prospective_endpoint_protocol_ready | endpoint_scores_allowed | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_WARP_HISTORY_FREEZE_V1 | NGC4088_WARP_HISTORY_FORMULA_FREEZE_READY_LAW_CAVEATED_NOT_SCORE | B1_RESOLVED_CAVEATED_WHISP_GRAPHICAL_XW | B2_PROTOCOL_FORMULA_FREEZE_READY_LAW_LEVEL_OPEN | B3_PROTOCOL_UNIQUE_SCALE_SELECTED_LAW_LEVEL_OPEN | True | True | 0.298333 | 171.7 | 1 | 1 | 1 | 8795.11 | 12 | 6 | 4 | 0 | False | True | True | False | build a separate accepted endpoint gate before any scoring; preserve B1/B2/B3 law/provenance caveats | ngc4088_warp_history_formula_freeze_protocol_not_score |

## Frozen Manifest

| galaxy | formula_id | readout_family | carrier | formula_text | delta_text | kernel_text | amplitude_rule | x_w_formula_freeze | x_w_first_pass | x_w_source | x_w_provenance_caveat | q_warp | q_warp_source | sigma_warp | sigma_rule | vflat_km_s | lambda_w_km2_s2 | turn_on_power_frozen | turn_on_power_rule | turn_on_power_sensitivity_control | selected_scale_id | selection_principle | dimension_check | inactive_window_limit | zero_source_limit | law_level_caveat | b1_formula_freeze_status | b2_protocol_status | b3_protocol_status | uses_vobs_or_residual_in_construction | formula_frozen_before_endpoint_scoring | endpoint_scores_allowed | prospective_endpoint_protocol_ready | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_WARP_HISTORY_FREEZE_V1 | K_warp_history | v_Newtonian_baryonic | v_readout^2(R)=v_Newtonian_baryonic^2(R)+lambda_w*C_warp(R/R_HI;x_w,p) | Delta v^2_warp(R;p)=lambda_w*C_warp(R/R_HI;x_w,p) | C_warp(x;x_w,p)=q_warp*max(0,(x-x_w)/(1-x_w))^p | lambda_w=sigma_warp*q_warp*x_w*Vflat^2 | 0.298333 | 0.282353 | WHISP graphical-overview frozen extraction, caveated | accepted for formula freeze from residual-blind WHISP graphical overview; direct source-coordinate H I/FITS product remains uncached | 1 | source-response review / filled warp closure mapping | 1 | positive outer warp/history added-readout sign frozen from source-side orientation protocol | 171.7 | 8795.11 | 1 | minimal linear onset ramp is the predeclared formula-freeze branch | p=2 remains a sensitivity/control branch only, not the endpoint formula | CURRENT_XW_VFLAT2 | MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE | PASS: lambda_w has km^2 s^-2 units; C_warp is dimensionless; Delta v^2 has velocity-squared units | R/R_HI <= x_w implies C_warp=0 and v_readout=v_Newtonian_baryonic | q_warp=0 or sigma_warp=0 implies Delta v^2=0 and carrier recovery | B2 physical-normalization law and B3 law-level uniqueness remain open; this is a protocol formula freeze | B1_RESOLVED_CAVEATED_WHISP_GRAPHICAL_XW | B2_PROTOCOL_FORMULA_FREEZE_READY_LAW_LEVEL_OPEN | B3_PROTOCOL_UNIQUE_SCALE_SELECTED_LAW_LEVEL_OPEN | False | True | False | True | ngc4088_warp_history_formula_freeze_protocol_not_score |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | formula_freeze_ready | endpoint_scores_allowed | uses_vobs_or_residual_in_construction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_WARP_HISTORY_FREEZE_V1 | N4088_FF1_B1_XW_FREEZE | PASS_CAVEATED | x_w=0.298333; B1_CAVEATED_XW_ACCEPTED_FOR_FORMULA_FREEZE_NOT_ENDPOINT | cache direct source-coordinate H I/FITS product when available; carry WHISP graphical-overview caveat | True | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | NGC4088_WARP_HISTORY_FREEZE_V1 | N4088_FF2_B2_DIMENSIONAL_FORMULA | PASS_CAVEATED | DIMENSIONALLY_VALID_RESIDUAL_BLIND_EXECUTABLE; FORMULA_CONDITIONAL_NOT_FINAL_LAW; lambda_w recomputed from caveated x_w | derive final Tau-side physical-normalization law; do not claim law-level validation | True | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | NGC4088_WARP_HISTORY_FREEZE_V1 | N4088_FF3_B3_PROTOCOL_SCALE_UNIQUENESS | PASS_CAVEATED | selected_scale_id=CURRENT_XW_VFLAT2; conditional_uniqueness_resolved=True | law-level uniqueness still depends on B2 closure/asymptotic-carrier derivation | True | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | NGC4088_WARP_HISTORY_FREEZE_V1 | N4088_FF4_BRANCH_FREEZE | PASS_CAVEATED | p=1 selected by minimal linear onset ramp; p=2 retained only as sensitivity control | future endpoint/control scripts must not choose p from residuals | True | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | NGC4088_WARP_HISTORY_FREEZE_V1 | N4088_FF5_DIMENSIONS_AND_LIMITS | PASS | dimensionless kernel times lambda_w[km^2/s^2]; inactive-window and zero-source carrier limits pass | none at formula-shell level | True | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | NGC4088_WARP_HISTORY_FREEZE_V1 | N4088_FF6_ENDPOINT_BLINDNESS | PASS | manifest and kernel grid are built from source ledgers and preflight carrier columns; vobs is not copied into the freeze grid | accepted endpoint gate and scoring must be separate and read this manifest unchanged | True | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |

## Kernel Preview

| galaxy | split | r_kpc | x_R_over_RHI | carrier_velocity_km_s | x_w_formula_freeze | q_warp | sigma_warp | turn_on_power_frozen | kernel_warp_history | lambda_w_km2_s2 | delta_v2_warp_history_km2_s2 | v_warp_history_formula_freeze_km_s | uses_vobs_or_residual_in_construction | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | holdout | 1.74 | 0.0781918 | 96.9585 | 0.298333 | 1 | 1 | 1 | 0 | 8795.11 | 0 | 96.9585 | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | holdout | 3.5 | 0.157282 | 127.47 | 0.298333 | 1 | 1 | 1 | 0 | 8795.11 | 0 | 127.47 | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | holdout | 5.24 | 0.235474 | 171.208 | 0.298333 | 1 | 1 | 1 | 0 | 8795.11 | 0 | 171.208 | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | holdout | 6.98 | 0.313666 | 189.424 | 0.298333 | 1 | 1 | 1 | 0.021853 | 8795.11 | 192.199 | 189.931 | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | holdout | 8.72 | 0.391858 | 177.32 | 0.298333 | 1 | 1 | 1 | 0.13329 | 8795.11 | 1172.3 | 180.596 | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | holdout | 10.47 | 0.470499 | 169.962 | 0.298333 | 1 | 1 | 1 | 0.245368 | 8795.11 | 2158.04 | 176.196 | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | holdout | 12.19 | 0.547792 | 163.94 | 0.298333 | 1 | 1 | 1 | 0.355524 | 8795.11 | 3126.87 | 173.214 | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | holdout | 13.94 | 0.626434 | 151.086 | 0.298333 | 1 | 1 | 1 | 0.467602 | 8795.11 | 4112.61 | 164.132 | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | holdout | 15.68 | 0.704625 | 141.233 | 0.298333 | 1 | 1 | 1 | 0.579039 | 8795.11 | 5092.71 | 158.238 | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | holdout | 17.42 | 0.782817 | 133.58 | 0.298333 | 1 | 1 | 1 | 0.690476 | 8795.11 | 6072.82 | 154.649 | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | holdout | 19.28 | 0.866402 | 126.405 | 0.298333 | 1 | 1 | 1 | 0.809599 | 8795.11 | 7120.51 | 151.983 | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |
| NGC4088 | holdout | 21.48 | 0.965265 | 118.916 | 0.298333 | 1 | 1 | 1 | 0.950496 | 8795.11 | 8359.72 | 150.002 | False | False | ngc4088_warp_history_formula_freeze_protocol_not_score |

## Claim Boundary

The formula is frozen before endpoint scoring as a prospective NGC4088
warp/history protocol. B1 is caveated by the WHISP graphical-overview
source, B2 remains formula-conditional rather than law-derived, and B3 is
protocol-unique rather than law-level unique. Any endpoint score must be
run by a separate accepted endpoint script that reads this manifest
unchanged.
