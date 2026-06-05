# NGC4183 Projection Gamma Coefficient Gate

Status: `NGC4183_PROJECTION_GAMMA_RULE_BLOCKED_SOURCE_NATIVE_RADIAL_MODEL_REQUIRED`

This gate asks whether the projection attenuation formula can be frozen without
using endpoint residuals.

## Summary

| gamma_gate_status | galaxy | formula_derivation_status | gamma_82_to_83_diagnostic | p_edge_kernel_value | coefficient_rule_frozen | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary | next_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183_PROJECTION_GAMMA_RULE_BLOCKED_SOURCE_NATIVE_RADIAL_MODEL_REQUIRED | NGC4183 | NGC4183_PROJECTION_OUTER_WARP_FORMULA_SHELL_DERIVED_FREEZE_BLOCKED | 0.00458511 | 0.985148 | False | False | False | ngc4183_projection_gamma_coefficient_gate_not_endpoint | acquire_or_extract_source_native_tilted_ring_orientation_profile |

## Candidate Rules

| candidate_rule | candidate_gamma_proj | source_inputs | status | freeze_allowed | reason |
| --- | --- | --- | --- | --- | --- |
| inclination_difference_only | 0.00458511390812999 | SPARC Inc=82 deg; source-native HI inclination=83 deg | SOURCE_DERIVED_BUT_TOO_SMALL_AND_SIGNIFICANCE_LIMITED | False | only compares two nearly identical high inclinations; does not encode warp/profile overlay |
| edge_on_strength_direct | 0.9851478631379982 | p_edge=sin^2(i_HI) | REJECTED_DIMENSIONLESS_BUT_NOT_A_COEFFICIENT_DERIVATION | False | p_edge belongs inside the kernel; using it again as gamma would double-count projection |
| residual_fit_gamma | <NA> | endpoint residuals | FORBIDDEN_FOR_FREEZE | False | would violate residual-blind endpoint protocol |
| source_native_tilted_ring_gamma | <NA> | radial tilted-ring inclination/PA or velocity-field model | PREFERRED_BUT_MISSING | False | requires source-native radial orientation model not currently extracted |

## Gates

| gate_id | gate_status | evidence | remaining_obligation |
| --- | --- | --- | --- |
| N4183_GAMMA_G1_GEOMETRIC_CANDIDATE | PASS_AS_DIAGNOSTIC_ONLY | 82->83 deg gives gamma=0.00458511 | do not freeze because it only captures a near-identical inclination comparison |
| N4183_GAMMA_G2_NO_DOUBLE_COUNTING | PASS_BLOCKS_BAD_RULE | p_edge already enters K_proj | gamma must be an independent coefficient rule |
| N4183_GAMMA_G3_RESIDUAL_BLINDNESS | PASS_BLOCKS_ENDPOINT_FIT | no vobs/residual used | source-native radial model required |
| N4183_GAMMA_G4_FREEZE | BLOCKED | no acceptable gamma_proj rule is frozen | acquire tilted-ring/profile source or declare NGC4183 blocked |

## Verdict

The projection formula shell is useful, but the coefficient is not frozen.
The only purely local inclination comparison, 82 to 83 degrees, gives a tiny
diagnostic attenuation `gamma=0.00458511` and cannot represent the
radial projection/warp structure.  Using `p_edge` as both kernel and coefficient
would double-count the same evidence.  Therefore NGC4183 needs a source-native
tilted-ring or orientation-profile extraction before endpoint scoring.
