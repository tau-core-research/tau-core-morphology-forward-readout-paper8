# NGC4088 Filled Warp Closure Mapping

This report injects the residual-blind NGC4088 `x_w` estimate into the
warp closure-source mapping shell. It is still not an endpoint kernel or
velocity prediction.

## Verdict

NGC4088 now has a filled source-side onset control for the closure-source
lane. The remaining blocker is not the onset any more; it is the
kernel-to-velocity normalization and final readout law.

## Filled Mapping Rule

| galaxy | mapping_name | dimensionless_radius | basis_formula | known_source_strength_q_warp | filled_x_warp_onset | filled_x_warp_uncertainty | filled_onset_kpc | filled_onset_source | allowed_turn_on_powers | mapping_status | accepted_for_mapping_rule | endpoint_scores_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | filled_dimensionless_outer_warp_asymmetry_ramp | x := R / R_HI | C_warp(x; x_w, p) = q_warp * max(0, (x - x_w)/(1 - x_w))^p | 1 | 0.282353 | 0.0705882 | 6.28319 | channel-map digitization response + x_w conversion audit | 1.0;2.0 | FILLED_SOURCE_BASIS_PROFILE_NORMALIZATION_OPEN | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |

## Filled Profile Grid

| galaxy | x_R_over_RHI | filled_x_warp_onset | x_warp_uncertainty | turn_on_power_control | q_warp | filled_basis_value | profile_status | accepted_for_mapping_rule | endpoint_scores_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 0 | 0.282353 | 0.0705882 | 1 | 1 | 0 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 0.1 | 0.282353 | 0.0705882 | 1 | 1 | 0 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 0.2 | 0.282353 | 0.0705882 | 1 | 1 | 0 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 0.282353 | 0.282353 | 0.0705882 | 1 | 1 | 0 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 0.4 | 0.282353 | 0.0705882 | 1 | 1 | 0.163934 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 0.6 | 0.282353 | 0.0705882 | 1 | 1 | 0.442623 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 0.8 | 0.282353 | 0.0705882 | 1 | 1 | 0.721311 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 1 | 0.282353 | 0.0705882 | 1 | 1 | 1 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 0 | 0.282353 | 0.0705882 | 2 | 1 | 0 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 0.1 | 0.282353 | 0.0705882 | 2 | 1 | 0 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 0.2 | 0.282353 | 0.0705882 | 2 | 1 | 0 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 0.282353 | 0.282353 | 0.0705882 | 2 | 1 | 0 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 0.4 | 0.282353 | 0.0705882 | 2 | 1 | 0.0268745 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 0.6 | 0.282353 | 0.0705882 | 2 | 1 | 0.195915 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 0.8 | 0.282353 | 0.0705882 | 2 | 1 | 0.52029 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |
| NGC4088 | 1 | 0.282353 | 0.0705882 | 2 | 1 | 1 | FILLED_SOURCE_BASIS_NOT_ENDPOINT | True | False | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |

## Summary

| galaxy | filled_x_warp_onset | filled_x_warp_uncertainty | filled_onset_kpc | n_profile_rows | mapping_status | accepted_for_mapping_rule | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 0.282353 | 0.0705882 | 6.28319 | 16 | FILLED_SOURCE_BASIS_PROFILE_NORMALIZATION_OPEN | True | False | s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint |

## Claim Boundary

This artifact only fills the source-side onset control in the mapping
shell. It does not authorize endpoint scoring, baseline comparison, or a
matched-family validation claim.
