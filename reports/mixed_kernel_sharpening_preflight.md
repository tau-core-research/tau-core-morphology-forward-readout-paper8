# Mixed Kernel Sharpening Preflight

Status label: `DIAGNOSTIC_ONLY_NOT_ENDPOINT`.

This is a source-side formula-shape preflight. It does not score
rotation curves and does not modify accepted endpoint rows. It follows
from the source-observable separation gate: the fresh NGC5907 and
NGC7331 lanes separate in source-observable space, but their current
attenuation kernels are too similar for strict replay/holdout
specificity.

## Summary

| preflight_status | diagnostic_status | current_kernel_cross_similarity | source_sharpened_kernel_cross_similarity | kernel_shape_separation_gain | projection_edge_exponent | vertical_decay | projected_thickness_norm | uses_vobs_or_residual | endpoint_scores_allowed | endpoint_score_inputs_read | dimension_check | known_limit_check | next_obligation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SOURCE_KERNEL_SHARPENING_PREFLIGHT_READY_NOT_ENDPOINT | DIAGNOSTIC_ONLY_NOT_ENDPOINT | 0.991418 | 0.643996 | 0.347422 | 2.52743 | 2.16512 | 0.398406 | False | False | False | PASS: all sharpened kernel arguments and coefficients are dimensionless | PASS: inactive source windows recover zero correction; carrier recovery remains available at gamma=0 | freeze V2/V3 manifests with these source-sharpened kernels before any new replay/holdout endpoint score | mixed_kernel_sharpening_preflight_not_endpoint |

## Source-Sharpened Formula Shells

| formula_label | source_lane | kernel_formula | source_parameters | dimension_check | known_limit_check | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| K_projection_source_sharpened | NGC5907 projection/truncation dominated mixed lane | K_proj_sharp(u)=S(u)^(1+Pi_projection+C_trunc) *(1+C_trunc*S(u))/(1+C_trunc) | Pi_projection=0.789128; C_trunc=0.738298 | PASS: u, S(u), Pi_projection, and C_trunc are dimensionless | Pi_projection=0 and C_trunc=0 recovers a simple active-window kernel; inactive window gives K=0 | False | mixed_kernel_sharpening_preflight_not_endpoint |
| K_vertical_outer_warp_source_sharpened | NGC7331 V2 fractional-onset vertical/outer-warp mixed lane | K_vow_sharp(u)=S(u)*exp(-(1+R_onset/R_HI+A_vertical)u) + T_projected*S(u)*(1-S(u)) | R_onset/R_HI=0.534309; A_vertical=0.63081; T_projected=0.398406 | PASS: u, S(u), R_onset/R_HI, A_vertical, and T_projected are dimensionless | absent fractional onset or absent vertical activation blocks this lane; inactive window gives K=0 | False | mixed_kernel_sharpening_preflight_not_endpoint |

## Profile Grid

| u_active_window | K_projection_current_normalized | K_vertical_outer_warp_current_normalized | K_projection_source_sharpened_normalized | K_vertical_outer_warp_source_sharpened_normalized | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | False | False | mixed_kernel_sharpening_preflight_not_endpoint |
| 0.005 | 4.30042e-05 | 9.94177e-05 | 2.14169e-11 | 0.000381166 | False | False | mixed_kernel_sharpening_preflight_not_endpoint |
| 0.01 | 0.00017147 | 0.000395624 | 7.06014e-10 | 0.0015078 | False | False | mixed_kernel_sharpening_preflight_not_endpoint |
| 0.015 | 0.000384617 | 0.000885567 | 5.43698e-09 | 0.00335493 | False | False | mixed_kernel_sharpening_preflight_not_endpoint |
| 0.02 | 0.000681721 | 0.00156622 | 2.3087e-08 | 0.005898 | False | False | mixed_kernel_sharpening_preflight_not_endpoint |
| 0.025 | 0.00106211 | 0.00243457 | 7.07507e-08 | 0.00911285 | False | False | mixed_kernel_sharpening_preflight_not_endpoint |
| 0.03 | 0.00152515 | 0.00348764 | 1.76404e-07 | 0.0129757 | False | False | mixed_kernel_sharpening_preflight_not_endpoint |
| 0.035 | 0.00207028 | 0.00472247 | 3.81485e-07 | 0.0174633 | False | False | mixed_kernel_sharpening_preflight_not_endpoint |
| 0.04 | 0.00269696 | 0.00613612 | 7.43382e-07 | 0.0225526 | False | False | mixed_kernel_sharpening_preflight_not_endpoint |
| 0.045 | 0.0034047 | 0.00772568 | 1.33784e-06 | 0.028221 | False | False | mixed_kernel_sharpening_preflight_not_endpoint |
| 0.05 | 0.00419307 | 0.00948825 | 2.26129e-06 | 0.0344464 | False | False | mixed_kernel_sharpening_preflight_not_endpoint |
| 0.055 | 0.00506166 | 0.011421 | 3.63308e-06 | 0.0412069 | False | False | mixed_kernel_sharpening_preflight_not_endpoint |

## Interpretation

The current normalized projection and vertical/outer-warp kernels have
cross-similarity 0.991418. The source-sharpened preflight
reduces that to 0.643996, a separation gain of
 0.347422. This is not a fit improvement claim. It is a
formula-shape obligation: future V2/V3 replay manifests should freeze
source-sharpened kernels before scoring, then rerun the same
wrong-label and shuffled-label replay/holdout controls.

## Claim Boundary

No observed velocity, residual, RMSE, or endpoint rank is read by this
gate. The result is a residual-blind kernel-design preflight, not an
endpoint result and not empirical validation.
