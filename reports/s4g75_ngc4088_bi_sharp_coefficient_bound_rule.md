# NGC4088 Sharpened B_i Coefficient Bound Rule

This artifact adds a residual-blind sharper B_i rule on top of the
conservative B_i=1 baseline. The active coefficient is B_i=0.5 only under
the declared second-order Taylor-remainder interpretation with normalized
source-space Hessian cap <= 1.

## Summary

| galaxy | sharp_rule_id | n_coefficients | n_sharp_coefficients | coefficient_value_min | coefficient_value_max | n_gates | n_pass | n_blocked | sharp_rule_status | numeric_bound_coefficient_authorization | claim_scope | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_SECOND_ORDER_REMAINDER_BI_HALF_BOUND_V1 | 4 | 4 | 0.5 | 0.5 | 4 | 4 | 0 | BI_COEFFICIENTS_SHARPENED_PROTOCOL_BOUND_READY | True | formula_conditional_second_order_protocol_bound_not_final_tau_side_derivation | False | False | s4g75_ngc4088_bi_sharp_coefficient_bound_rule_not_endpoint |

## Sharpened Coefficients

| galaxy | coefficient_id | multiplies_feature | sharp_value | unit | sharp_rule | sharp_status | derivation_status | justification | forbidden_origin | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | B_PA | f_PA | 0.5 | dimensionless | second_order_remainder_half_bound | SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | FORMULA_CONDITIONAL_NOT_FINAL_TAU_SIDE_AMPLITUDE_DERIVATION | For a normalized second-order remainder with source-space Hessian cap <= 1, the Taylor remainder contributes a factor 1/2 before the normalized feature magnitude. | vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit | False | False | s4g75_ngc4088_bi_sharp_coefficient_bound_rule_not_endpoint |
| NGC4088 | B_R | f_R | 0.5 | dimensionless | second_order_remainder_half_bound | SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | FORMULA_CONDITIONAL_NOT_FINAL_TAU_SIDE_AMPLITUDE_DERIVATION | For a normalized second-order remainder with source-space Hessian cap <= 1, the Taylor remainder contributes a factor 1/2 before the normalized feature magnitude. | vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit | False | False | s4g75_ngc4088_bi_sharp_coefficient_bound_rule_not_endpoint |
| NGC4088 | B_q | f_q | 0.5 | dimensionless | second_order_remainder_half_bound | SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | FORMULA_CONDITIONAL_NOT_FINAL_TAU_SIDE_AMPLITUDE_DERIVATION | For a normalized second-order remainder with source-space Hessian cap <= 1, the Taylor remainder contributes a factor 1/2 before the normalized feature magnitude. | vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit | False | False | s4g75_ngc4088_bi_sharp_coefficient_bound_rule_not_endpoint |
| NGC4088 | B_mem | f_mem | 0.5 | dimensionless | second_order_remainder_half_bound | SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | FORMULA_CONDITIONAL_NOT_FINAL_TAU_SIDE_AMPLITUDE_DERIVATION | For a normalized second-order remainder with source-space Hessian cap <= 1, the Taylor remainder contributes a factor 1/2 before the normalized feature magnitude. | vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit | False | False | s4g75_ngc4088_bi_sharp_coefficient_bound_rule_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | SB1_SOURCE_REVIEW_READY | PASS | SOURCE_RESPONSES_ACCEPTED_FOR_PROTOCOL_BOUND | none | False | False | s4g75_ngc4088_bi_sharp_coefficient_bound_rule_not_endpoint |
| NGC4088 | SB2_CONSERVATIVE_BASELINE_EXISTS | PASS | BI_COEFFICIENTS_FROZEN_PROTOCOL_BOUND_READY | keep B_i=1 baseline available for comparison | False | False | s4g75_ngc4088_bi_sharp_coefficient_bound_rule_not_endpoint |
| NGC4088 | SB3_SECOND_ORDER_REMAINDER_ASSUMPTION_DECLARED | PASS | B_i=0.5 is conditional on the normalized second-order remainder/Hessian-cap interpretation | derive the Hessian cap from Tau-side geometry before calling this final | False | False | s4g75_ngc4088_bi_sharp_coefficient_bound_rule_not_endpoint |
| NGC4088 | SB4_ENDPOINT_BLINDNESS | PASS | sharp rule uses no vobs, residuals, or endpoint scores | keep endpoint tests separate | False | False | s4g75_ngc4088_bi_sharp_coefficient_bound_rule_not_endpoint |

## Claim Boundary

The sharpened coefficients are formula-conditional protocol coefficients.
They are residual-blind and stricter than the unit bound, but they are not
yet a final Tau-side derivation of the sharp cross-term amplitudes.
