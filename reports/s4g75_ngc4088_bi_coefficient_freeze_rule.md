# NGC4088 B_i Coefficient Freeze Rule

This artifact freezes a residual-blind conservative coefficient rule for
the epsilon_cross protocol bound. It sets all B_i values to 1 under a
unit-Lipschitz triangle-bound default. This is deliberately cautious and
not an endpoint fit.

## Summary

| galaxy | freeze_rule_id | n_coefficients | n_frozen_coefficients | coefficient_value_min | coefficient_value_max | n_gates | n_pass | n_blocked | freeze_rule_status | numeric_bound_coefficient_authorization | claim_scope | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_UNIT_LIPSCHITZ_BI_FREEZE_RULE_V1 | 4 | 4 | 1 | 1 | 5 | 5 | 0 | BI_COEFFICIENTS_FROZEN_PROTOCOL_BOUND_READY | True | conservative_protocol_upper_bound_not_final_tau_side_coefficient_derivation | False | False | s4g75_ngc4088_bi_coefficient_freeze_rule_not_endpoint |

## Frozen Coefficients

| galaxy | coefficient_id | multiplies_feature | frozen_value | unit | freeze_rule | freeze_status | derivation_status | justification | forbidden_origin | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | B_PA | f_PA | 1 | dimensionless | unit_Lipschitz_triangle_bound_default | FROZEN_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | PROTOCOL_BOUND_NOT_FINAL_TAU_SIDE_DERIVATION | For normalized features f_i in [0,1], |sum c_i f_i| <= sum |c_i| f_i; set B_i=1 as conservative first protocol bound. | vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit | False | False | s4g75_ngc4088_bi_coefficient_freeze_rule_not_endpoint |
| NGC4088 | B_R | f_R | 1 | dimensionless | unit_Lipschitz_triangle_bound_default | FROZEN_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | PROTOCOL_BOUND_NOT_FINAL_TAU_SIDE_DERIVATION | For normalized features f_i in [0,1], |sum c_i f_i| <= sum |c_i| f_i; set B_i=1 as conservative first protocol bound. | vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit | False | False | s4g75_ngc4088_bi_coefficient_freeze_rule_not_endpoint |
| NGC4088 | B_q | f_q | 1 | dimensionless | unit_Lipschitz_triangle_bound_default | FROZEN_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | PROTOCOL_BOUND_NOT_FINAL_TAU_SIDE_DERIVATION | For normalized features f_i in [0,1], |sum c_i f_i| <= sum |c_i| f_i; set B_i=1 as conservative first protocol bound. | vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit | False | False | s4g75_ngc4088_bi_coefficient_freeze_rule_not_endpoint |
| NGC4088 | B_mem | f_mem | 1 | dimensionless | unit_Lipschitz_triangle_bound_default | FROZEN_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | PROTOCOL_BOUND_NOT_FINAL_TAU_SIDE_DERIVATION | For normalized features f_i in [0,1], |sum c_i f_i| <= sum |c_i| f_i; set B_i=1 as conservative first protocol bound. | vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit | False | False | s4g75_ngc4088_bi_coefficient_freeze_rule_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | BF1_SOURCE_REVIEW_AUTHORIZED | PASS | SOURCE_RESPONSES_ACCEPTED_FOR_PROTOCOL_BOUND | preserve caveated source-review status | False | False | s4g75_ngc4088_bi_coefficient_freeze_rule_not_endpoint |
| NGC4088 | BF2_DIMENSIONLESS_FEATURE_DOMAIN | PASS | all f_i are normalized dimensionless features in [0,1] | preserve feature clipping and units | False | False | s4g75_ngc4088_bi_coefficient_freeze_rule_not_endpoint |
| NGC4088 | BF3_UNIT_LIPSCHITZ_BOUND_RULE | PASS | B_i=1 is a conservative triangle-bound coefficient, not an endpoint fit | replace with sharper Tau-side derivation when available | False | False | s4g75_ngc4088_bi_coefficient_freeze_rule_not_endpoint |
| NGC4088 | BF4_ENDPOINT_BLINDNESS | PASS | freeze rule forbids vobs and endpoint residuals | keep endpoint tests separate | False | False | s4g75_ngc4088_bi_coefficient_freeze_rule_not_endpoint |
| NGC4088 | BF5_COEFFICIENT_FREEZE_AUTHORIZATION | PASS | four B_i coefficients frozen at 1 under the protocol rule | evaluate epsilon_cross as protocol upper bound | False | False | s4g75_ngc4088_bi_coefficient_freeze_rule_not_endpoint |

## Claim Boundary

The frozen coefficients authorize only a conservative protocol upper
bound for epsilon_cross. They do not claim a final Tau-side derivation of
the sharp B_i amplitudes.
