# NGC4088 Epsilon-Cross Bound Expression Shell

This shell combines the feature-normalization gate with the blocked B_i
coefficient obligations. It computes a numeric protocol bound only
when accepted source features and frozen residual-blind B_i values are
available.

## Expression

| galaxy | expression_id | bound_expression | known_feature_subexpression | blocked_feature_subexpression | numeric_bound_value | expression_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_EPSILON_CROSS_BOUND_EXPRESSION_SHELL | |epsilon_cross| <= 0.5*B_PA + 0.25*B_R + 1*B_q + 1*B_mem | 0.5*B_PA + 0.25*B_R + 1*B_q + 1*B_mem | none | 1.375 | NUMERIC_EPSILON_PROTOCOL_BOUND_READY_CAVEATED | False | False | s4g75_ngc4088_epsilon_cross_bound_expression_shell_not_endpoint |

## Terms

| galaxy | term_id | coefficient_id | feature_symbol | feature_value | feature_status | coefficient_status | term_expression | term_numeric_value | term_status | unit | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | TERM_B_PA | B_PA | f_PA | 0.5 | ACCEPTED_FROM_FROZEN_DIGITIZATION_VALIDATION | SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | 0.5*B_PA | 0.25 | TERM_NUMERIC_PROTOCOL_BOUND_READY | dimensionless | False | False | s4g75_ngc4088_epsilon_cross_bound_expression_shell_not_endpoint |
| NGC4088 | TERM_B_R | B_R | f_R | 0.25 | ACCEPTED_FROM_FROZEN_DIGITIZATION_VALIDATION | SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | 0.25*B_R | 0.125 | TERM_NUMERIC_PROTOCOL_BOUND_READY | dimensionless | False | False | s4g75_ngc4088_epsilon_cross_bound_expression_shell_not_endpoint |
| NGC4088 | TERM_B_q | B_q | f_q | 1 | ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND | SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | 1*B_q | 0.5 | TERM_NUMERIC_PROTOCOL_BOUND_READY | dimensionless | False | False | s4g75_ngc4088_epsilon_cross_bound_expression_shell_not_endpoint |
| NGC4088 | TERM_B_mem | B_mem | f_mem | 1 | ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND | SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | 1*B_mem | 0.5 | TERM_NUMERIC_PROTOCOL_BOUND_READY | dimensionless | False | False | s4g75_ngc4088_epsilon_cross_bound_expression_shell_not_endpoint |

## Summary

| galaxy | expression_id | n_terms | n_terms_with_feature_values | n_terms_numeric | n_blocked_terms | bound_expression_status | numeric_bound_status | next_required_action | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_EPSILON_CROSS_BOUND_EXPRESSION_SHELL | 4 | 4 | 4 | 0 | NUMERIC_EPSILON_PROTOCOL_BOUND_READY_CAVEATED | NUMERIC_EPSILON_PROTOCOL_BOUND_AVAILABLE | numeric_protocol_bound_ready_interpret_with_caveats | False | False | s4g75_ngc4088_epsilon_cross_bound_expression_shell_not_endpoint |

## Claim Boundary

The expression is residual-blind. A numeric value, when present, is a
conservative protocol upper bound for epsilon_cross, not an endpoint
fit or a final sharp Tau-side amplitude derivation.
