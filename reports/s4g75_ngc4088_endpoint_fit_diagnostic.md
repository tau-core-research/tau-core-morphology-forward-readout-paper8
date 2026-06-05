# NGC4088 Endpoint Fit Diagnostic

This diagnostic scores generated readout profiles against the observed
rotation curve. It is useful for fit inspection, but it is not a
source-bound derivation and does not authorize a validation claim.

## Summary

| galaxy | diagnostic_id | n_points | outer_threshold_x_R_over_RHI | best_baseline_model | best_baseline_rmse_kms | best_fixed_tau_model | best_fixed_tau_rmse_kms | fixed_tau_minus_best_baseline_rmse_kms | best_bounded_tau_model | best_bounded_tau_rmse_kms | bounded_tau_minus_best_baseline_rmse_kms | newton_rmse_kms | tpg_v6_rmse_kms | mond_rmse_kms | fixed_tau_beats_newton | fixed_tau_beats_tpg_v6 | fixed_tau_beats_mond | bounded_tau_beats_newton | bounded_tau_beats_tpg_v6 | bounded_tau_beats_mond | endpoint_selected_best_is_diagnostic_only | uses_vobs_for_generation | uses_vobs_for_scoring | validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_ENDPOINT_FIT_DIAGNOSTIC | 12 | 0.5 | NEWTONIAN_vn | 25.3963 | TAU_WARP_p1_eps0 | 12.1897 | -13.2066 | TAU_WARP_p1_eps_+0.687500 | 6.92711 | -18.4692 | 25.3963 | 38.9877 | 42.1838 | True | True | True | True | True | True | True | False | True | False | s4g75_ngc4088_endpoint_fit_diagnostic_not_validation |

## Figure

![NGC4088 endpoint fit diagnostic](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/reports/s4g75_ngc4088_endpoint_fit_diagnostic.png)

## Fixed Models

| model_id | scenario_role | rmse_kms | mae_kms | bias_kms | inner_rmse_kms | outer_rmse_kms |
| --- | --- | --- | --- | --- | --- | --- |
| TAU_WARP_p1_eps0 | predeclared_fixed_epsilon_zero | 12.1897 | 10.0361 | -4.59482 | 8.57561 | 14.9544 |
| TAU_WARP_p2_eps0 | predeclared_fixed_epsilon_zero | 14.5041 | 12.8946 | -7.58656 | 8.94207 | 18.4601 |
| NEWTONIAN_vn | baseline | 25.3963 | 20.1483 | -14.8664 | 9.26655 | 34.6998 |
| TPG_V6_v_v6 | baseline | 38.9877 | 37.9843 | 37.9843 | 37.927 | 40.0204 |
| MOND_v_mond | baseline | 42.1838 | 41.2137 | 41.2137 | 41.4811 | 42.8751 |

## Bounded Tau Sensitivity Scores

| model_id | scenario_role | rmse_kms | mae_kms | bias_kms | inner_rmse_kms | outer_rmse_kms |
| --- | --- | --- | --- | --- | --- | --- |
| TAU_WARP_p1_eps_+0.687500 | bounded_epsilon_cross_sensitivity | 6.92711 | 5.45506 | 1.76327 | 8.6754 | 4.55052 |
| TAU_WARP_p2_eps_+0.687500 | bounded_epsilon_cross_sensitivity | 8.80039 | 8.39126 | -3.06519 | 8.76665 | 8.83399 |
| TAU_WARP_p1_eps_+0.343750 | bounded_epsilon_cross_sensitivity | 8.84296 | 7.21556 | -1.35702 | 8.56773 | 9.10989 |
| TAU_WARP_p2_eps_+0.343750 | bounded_epsilon_cross_sensitivity | 11.4048 | 10.6026 | -5.2855 | 8.84938 | 13.4843 |
| TAU_WARP_p1_eps0 | predeclared_fixed_epsilon_zero | 12.1897 | 10.0361 | -4.59482 | 8.57561 | 14.9544 |
| TAU_WARP_p2_eps0 | predeclared_fixed_epsilon_zero | 14.5041 | 12.8946 | -7.58656 | 8.94207 | 18.4601 |
| TAU_WARP_p1_eps_-0.343750 | bounded_epsilon_cross_sensitivity | 16.2796 | 13.3539 | -7.96727 | 8.7024 | 21.3147 |
| TAU_WARP_p2_eps_-0.343750 | bounded_epsilon_cross_sensitivity | 17.9554 | 15.2792 | -9.98014 | 9.04453 | 23.7273 |
| TAU_WARP_p1_eps_-0.687500 | bounded_epsilon_cross_sensitivity | 20.86 | 16.8284 | -11.4966 | 8.94681 | 28.1111 |
| TAU_WARP_p2_eps_-0.687500 | bounded_epsilon_cross_sensitivity | 21.7123 | 17.7716 | -12.4815 | 9.15657 | 29.3088 |

## Best Bounded Tau Profile

| model_id | r_kpc | x_R_over_RHI | vobs_kms | vpred_kms | residual_kms |
| --- | --- | --- | --- | --- | --- |
| TAU_WARP_p1_eps_+0.687500 | 1.74 | 0.0781918 | 84.9 | 96.9585 | 12.0585 |
| TAU_WARP_p1_eps_+0.687500 | 3.5 | 0.157282 | 136 | 127.47 | -8.52986 |
| TAU_WARP_p1_eps_+0.687500 | 5.24 | 0.235474 | 162 | 171.208 | 9.20843 |
| TAU_WARP_p1_eps_+0.687500 | 6.98 | 0.313666 | 179 | 191.035 | 12.0354 |
| TAU_WARP_p1_eps_+0.687500 | 8.72 | 0.391858 | 182 | 183.265 | 1.26457 |
| TAU_WARP_p1_eps_+0.687500 | 10.47 | 0.470499 | 179 | 180.471 | 1.47094 |
| TAU_WARP_p1_eps_+0.687500 | 12.19 | 0.547792 | 174 | 179.086 | 5.08614 |
| TAU_WARP_p1_eps_+0.687500 | 13.94 | 0.626434 | 171 | 171.935 | 0.935012 |
| TAU_WARP_p1_eps_+0.687500 | 15.68 | 0.704625 | 168 | 167.964 | -0.0358257 |
| TAU_WARP_p1_eps_+0.687500 | 17.42 | 0.782817 | 165 | 166.251 | 1.25096 |
| TAU_WARP_p1_eps_+0.687500 | 19.28 | 0.866402 | 171 | 165.56 | -5.44014 |
| TAU_WARP_p1_eps_+0.687500 | 21.48 | 0.965265 | 174 | 165.855 | -8.14489 |

## Claim Boundary

The bounded Tau best row is endpoint-selected from predeclared sensitivity
scenarios. It is a diagnostic of where the generated morphology readout can
move the curve, not proof that the galaxy validates Tau Core.
