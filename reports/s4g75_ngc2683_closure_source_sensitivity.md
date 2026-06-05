# NGC2683 Closure-Source Sensitivity Audit

This audit varies only residual-blind prototype knobs: locality width and ring-offset strength. It is not accepted validation.

## Verdict

Grid points checked: 12.
Grid points improving over scalar thick/flared: 12.
Best delta RMSE: -0.353217.
Best locality multiplier: 2.
Best ring strength: 1.

## Sensitivity Table

| galaxy | post22_policy | locality_multiplier | locality_width_kpc | ring_strength | beta_delta_v2_amplitude | scalar_rmse_K_thick_flared | closure_source_rmse_K_thick_flared | closure_source_minus_scalar_rmse | closure_kernel_min | closure_kernel_median | closure_kernel_max | accepted_endpoint_ready | endpoint_scores_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC2683 | post22_linear_taper_to_inner_height | 0.5 | 1.10482 | 0 | -522.962 | 10.3319 | 10.1455 | -0.186388 | 5.07953e-42 | 2.84625e-05 | 1.69557 | False | False | True | s4g75_ngc2683_closure_source_sensitivity_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | 0.5 | 1.10482 | 0.5 | -522.962 | 10.3319 | 10.1271 | -0.20474 | 6.24775e-11 | 0.0251862 | 1.69557 | False | False | True | s4g75_ngc2683_closure_source_sensitivity_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | 0.5 | 1.10482 | 1 | -522.962 | 10.3319 | 10.1088 | -0.223062 | 1.24955e-10 | 0.0503438 | 1.69558 | False | False | True | s4g75_ngc2683_closure_source_sensitivity_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | 1 | 2.20965 | 0 | -522.962 | 10.3319 | 10.2031 | -0.128714 | 4.28508e-15 | 0.0105068 | 1.47391 | False | False | True | s4g75_ngc2683_closure_source_sensitivity_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | 1 | 2.20965 | 0.5 | -522.962 | 10.3319 | 10.1909 | -0.140928 | 2.32311e-05 | 0.0439748 | 1.47396 | False | False | True | s4g75_ngc2683_closure_source_sensitivity_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | 1 | 2.20965 | 1 | -522.962 | 10.3319 | 10.1787 | -0.153128 | 4.64623e-05 | 0.0795902 | 1.47401 | False | False | True | s4g75_ngc2683_closure_source_sensitivity_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | 1.5 | 3.31447 | 0 | -522.962 | 10.3319 | 10.1415 | -0.1904 | 1.12277e-05 | 0.0958884 | 1.12966 | False | False | True | s4g75_ngc2683_closure_source_sensitivity_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | 1.5 | 3.31447 | 0.5 | -522.962 | 10.3319 | 10.1332 | -0.198676 | 0.00227779 | 0.0958884 | 1.1305 | False | False | True | s4g75_ngc2683_closure_source_sensitivity_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | 1.5 | 3.31447 | 1 | -522.962 | 10.3319 | 10.1249 | -0.206936 | 0.00227779 | 0.0958885 | 1.13134 | False | False | True | s4g75_ngc2683_closure_source_sensitivity_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | 2 | 4.41929 | 0 | -522.962 | 10.3319 | 9.99276 | -0.339095 | 0.00601462 | 0.162745 | 0.882025 | False | False | True | s4g75_ngc2683_closure_source_sensitivity_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | 2 | 4.41929 | 0.5 | -522.962 | 10.3319 | 9.98569 | -0.346167 | 0.00601462 | 0.162751 | 0.883692 | False | False | True | s4g75_ngc2683_closure_source_sensitivity_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | 2 | 4.41929 | 1 | -522.962 | 10.3319 | 9.97864 | -0.353217 | 0.00601462 | 0.162756 | 0.885358 | False | False | True | s4g75_ngc2683_closure_source_sensitivity_not_validation |

## Claim Boundary

This grid is a formula-development sensitivity map. The best row is not selected as an endpoint model, because the grid itself is a prototype design audit and not a predeclared population protocol.
