# NGC4088 Warp Closure Mapping Rule

This report defines a residual-blind mapping shell from NGC4088 warp/asymmetry evidence into a dimensionless closure-source basis. It does not create an endpoint kernel.

## Verdict

The bridge can now express the NGC4088 warp/asymmetry lane as a concrete dimensionless source basis, but the onset and radial profile are still source-missing. The formula is therefore a development shell, not a validated 4D readout.

## Mapping Rule

| mapping_name | dimensionless_radius | basis_formula | known_source_strength | free_source_required | dimensional_status | mapping_status | endpoint_scores_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dimensionless_outer_warp_asymmetry_ramp | x := R / R_HI | C_warp(x; x_w, p) = q_warp * max(0, (x - x_w)/(1 - x_w))^p | 1 | x_w := warp_onset_radius / R_HI | DIMENSIONLESS_BASIS_ONLY | FORMULA_DEVELOPMENT_SHELL_PROFILE_ONSET_BLOCKED | False |

## Sensitivity Basis Grid

| galaxy | x_R_over_RHI | x_warp_onset_control | turn_on_power_control | q_warp | basis_value | grid_status | uses_vobs_or_residual | endpoint_scores_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 0 | 0.5 | 1 | 1 | 0 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0.25 | 0.5 | 1 | 1 | 0 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0.5 | 0.5 | 1 | 1 | 0 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0.75 | 0.5 | 1 | 1 | 0.5 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 1 | 0.5 | 1 | 1 | 1 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0 | 0.5 | 2 | 1 | 0 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0.25 | 0.5 | 2 | 1 | 0 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0.5 | 0.5 | 2 | 1 | 0 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0.75 | 0.5 | 2 | 1 | 0.25 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 1 | 0.5 | 2 | 1 | 1 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0 | 0.7 | 1 | 1 | 0 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0.25 | 0.7 | 1 | 1 | 0 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0.5 | 0.7 | 1 | 1 | 0 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0.75 | 0.7 | 1 | 1 | 0.166667 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 1 | 0.7 | 1 | 1 | 1 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0 | 0.7 | 2 | 1 | 0 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0.25 | 0.7 | 2 | 1 | 0 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |
| NGC4088 | 0.5 | 0.7 | 2 | 1 | 0 | SENSITIVITY_BASIS_NOT_ENDPOINT | False | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |

## Summary

| galaxy | mapping_status | n_basis_grid_rows | known_source_strength_q_warp | known_scale_R_HI_over_Rdisk | known_scale_R_HI_over_Rs4g | required_source_native_onset | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | FORMULA_DEVELOPMENT_SHELL_PROFILE_ONSET_BLOCKED | 30 | 1 | 8.62518 | 6.83464 | warp_onset_radius_or_PA_profile | False | False | s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint |

## Claim Boundary

The onset controls in the grid are sensitivity controls, not fitted parameters and not accepted source measurements. Endpoint use requires a source-native warp-onset or PA/theta profile and a fixed readout map.
