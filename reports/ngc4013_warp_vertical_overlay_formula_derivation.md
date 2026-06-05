# NGC4013 Warp/Vertical-Overlay Formula Derivation

This report derives a source-side formula shell for NGC4013 after the
compact endpoint lane is rejected. It does not score the rotation curve.

## Formula

The derived shell is

`v_wvo^2(R)=v_TPG^2(R)*(1-Gamma_wvo*K_wvo(R))`,

with

`K_wvo(R)=W_warp(R;R_w,R_o)*[omega_z*K_z(R)+omega_EC*K_EC(R)+omega_lag*K_lag(R)]`.

The current source-derived upper coefficient is
`Gamma_wvo <= 0.216466`.

## Summary

| galaxy | formula_id | r_warp_kpc | h_over_rs | z_ec_kpc | f_ec | gamma_overlay_upper | n_derivation_steps | n_endpoint_blockers | derivation_status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | NGC4013_WARP_VERTICAL_OVERLAY_V1 | 10 | 0.232932 | 3 | 0.2 | 0.216466 | 7 | 3 | FORMULA_SHELL_DERIVED_ENDPOINT_FREEZE_BLOCKED | False | ngc4013_warp_vertical_overlay_formula_derivation_not_endpoint |

## Manifest

| galaxy | formula_id | readout_subfamily | carrier | solved_response_formula | kernel_formula | warp_window | vertical_kernel | extended_component_kernel | lag_kernel | sign_rule | amplitude_rule | r_warp_kpc | r_outer_kpc | h_over_rs | z_ec_kpc | f_ec | rs_proxy_kpc | gamma_z | gamma_ec | gamma_overlay_upper | uses_vobs_or_residual_in_derivation | formula_frozen_for_endpoint | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | NGC4013_WARP_VERTICAL_OVERLAY_V1 | K_warp_vertical_overlay_candidate | v_TPG | v_wvo^2(R)=v_TPG^2(R)*(1-Gamma_wvo*K_wvo(R)) | K_wvo(R)=W_warp(R;R_w,R_o)*[omega_z*K_z(R)+omega_EC*K_EC(R)+omega_lag*K_lag(R)] | W_warp=smoothstep((R-R_w)/(R_o-R_w)) | K_z(R)=1/(1+R/R_s) | K_EC(R)=1/(1+R/z_EC) | K_lag(R)=normalized lag-shallowing profile; source map still required | attenuation_not_added_gravity | Gamma_wvo <= 0.5*h_over_Rs + 0.5*f_EC until lag map is frozen | 10 |  | 0.232932 | 3 | 0.2 | 10.8641 | 0.116466 | 0.1 | 0.216466 | False | False | False | ngc4013_warp_vertical_overlay_formula_derivation_not_endpoint |

## Derivation Steps

| galaxy | step_id | status | statement | formula_consequence | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | D1_COMPACT_REJECTION | DERIVED_FROM_SOURCE_AUDIT | S4G has no bulge B component for NGC4013; compact endpoint is not source-supported. | replace K_compact_finite by K_warp_vertical_overlay_candidate | False | ngc4013_warp_vertical_overlay_formula_derivation_not_endpoint |
| NGC4013 | D2_CARRIER_CHOICE | DEFINITION | Use v_TPG as the already available solved-response carrier for overlay attenuation. | v_wvo^2 = v_TPG^2(1 - overlay attenuation) | False | ngc4013_warp_vertical_overlay_formula_derivation_not_endpoint |
| NGC4013 | D3_SIGN_RULE | ASSUMPTION_WITH_SOURCE_MOTIVATION | Edge-on warp/vertical/lag overlay is treated as apparent overread/projection contamination. | attenuation sign, not added-gravity sign | False | ngc4013_warp_vertical_overlay_formula_derivation_not_endpoint |
| NGC4013 | D4_WARP_WINDOW | FORMULA_CONDITIONAL | The source gives warp onset near 10 kpc but not a fully accepted outer window. | W_warp=smoothstep((R-R_w)/(R_o-R_w)); R_o remains a freeze blocker | False | ngc4013_warp_vertical_overlay_formula_derivation_not_endpoint |
| NGC4013 | D5_VERTICAL_OVERLAY_STRENGTH | SOURCE_DERIVED_BOUND | S4G edge-disk h/R and Comeron extended-component mass fraction set a conservative first-order bound. | Gamma_wvo <= 0.5*h/Rs + 0.5*f_EC | False | ngc4013_warp_vertical_overlay_formula_derivation_not_endpoint |
| NGC4013 | D6_LAG_KERNEL | BLOCKED_SOURCE_MAP_REQUIRED | Rotational lag context is present, but a normalized radial lag map is not yet frozen. | K_lag is symbolic until lag-to-kernel mapping is accepted | False | ngc4013_warp_vertical_overlay_formula_derivation_not_endpoint |
| NGC4013 | D7_ENDPOINT_STATUS | ENDPOINT_BLOCKED | No endpoint score is allowed until R_o and K_lag are frozen without vobs. | formula shell derived; endpoint formula not frozen | False | ngc4013_warp_vertical_overlay_formula_derivation_not_endpoint |

## Endpoint Blockers

| galaxy | blocker_id | required_input | why_required | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| NGC4013 | B1_OUTER_WARP_WINDOW | accepted outer warp/projection support radius R_o | without R_o, W_warp cannot be endpoint-frozen | False | ngc4013_warp_vertical_overlay_formula_derivation_not_endpoint |
| NGC4013 | B2_LAG_TO_KERNEL_MAP | accepted normalized radial lag-shallowing profile K_lag(R) | lag context cannot become a numerical kernel without a source-side map | False | ngc4013_warp_vertical_overlay_formula_derivation_not_endpoint |
| NGC4013 | B3_WEIGHT_RULE | residual-blind omega_z, omega_EC, omega_lag weighting rule | component weights cannot be selected by endpoint residuals | False | ngc4013_warp_vertical_overlay_formula_derivation_not_endpoint |

## Claim Boundary

This is a formula derivation shell. The endpoint remains blocked until the
outer warp window, lag-to-kernel map, and component weighting rule are
frozen without using observed rotation residuals.
