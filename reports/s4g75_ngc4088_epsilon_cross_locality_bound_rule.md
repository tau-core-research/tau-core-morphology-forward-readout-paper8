# NGC4088 Epsilon-Cross Locality Bound Rule

This artifact narrows the epsilon_cross audit bound by treating cross-terms
as adjacent source/readout couplings rather than as independent additive
linear feature terms.

## Summary

| galaxy | locality_rule_id | bound_expression | numeric_bound_value | linear_sharp_bound_reference | n_terms | n_gates | n_pass | n_warn | n_blocked | locality_bound_status | claim_scope | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_EPSILON_CROSS_ADJACENT_LOCALITY_BOUND_V1 | |epsilon_cross| <= 0.5*f_PA*f_R + 0.5*f_R*f_q + 0.5*f_q*f_mem | 0.6875 | 1.375 | 3 | 5 | 5 | 0 | 0 | LOCALITY_EPSILON_BOUND_READY_SIGN_STABLE | formula_conditional_locality_chain_bound_not_final_tau_side_derivation | False | False | s4g75_ngc4088_epsilon_cross_locality_bound_rule_not_endpoint |

## Locality Terms

| galaxy | term_id | left_feature | right_feature | left_feature_value | right_feature_value | half_remainder_factor | term_expression | term_numeric_value | term_interpretation | left_feature_status | right_feature_status | unit | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | L_PA_R | f_PA | f_R | 0.5 | 0.25 | 0.5 | 0.5*f_PA*f_R | 0.0625 | orientation_onset_locality | ACCEPTED_FROM_FROZEN_DIGITIZATION_VALIDATION | ACCEPTED_FROM_FROZEN_DIGITIZATION_VALIDATION | dimensionless | False | False | s4g75_ngc4088_epsilon_cross_locality_bound_rule_not_endpoint |
| NGC4088 | L_R_Q | f_R | f_q | 0.25 | 1 | 0.5 | 0.5*f_R*f_q | 0.125 | onset_warp_strength_locality | ACCEPTED_FROM_FROZEN_DIGITIZATION_VALIDATION | ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND | dimensionless | False | False | s4g75_ngc4088_epsilon_cross_locality_bound_rule_not_endpoint |
| NGC4088 | L_Q_MEM | f_q | f_mem | 1 | 1 | 0.5 | 0.5*f_q*f_mem | 0.5 | warp_strength_source_history_locality | ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND | ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND | dimensionless | False | False | s4g75_ngc4088_epsilon_cross_locality_bound_rule_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | LB1_SOURCE_FEATURES_AVAILABLE | PASS | f_PA, f_R, f_q, and f_mem are all available | none | False | False | s4g75_ngc4088_epsilon_cross_locality_bound_rule_not_endpoint |
| NGC4088 | LB2_SECOND_ORDER_HALF_RULE_READY | PASS | BI_COEFFICIENTS_SHARPENED_PROTOCOL_BOUND_READY | keep formula-conditional status explicit | False | False | s4g75_ngc4088_epsilon_cross_locality_bound_rule_not_endpoint |
| NGC4088 | LB3_LOCALITY_CHAIN_DECLARED | PASS | only adjacent source/readout couplings f_PA*f_R, f_R*f_q, and f_q*f_mem are admitted in this narrowed pass | derive or revise adjacency from a final Tau-side locality theorem before physical promotion | False | False | s4g75_ngc4088_epsilon_cross_locality_bound_rule_not_endpoint |
| NGC4088 | LB4_SIGN_STABILITY_BOUND | PASS | locality-coupled bound=0.6875 | none for sign-stability preflight | False | False | s4g75_ngc4088_epsilon_cross_locality_bound_rule_not_endpoint |
| NGC4088 | LB5_ENDPOINT_BLINDNESS | PASS | bound uses only source features and predeclared coupling adjacency | keep endpoint scoring separate | False | False | s4g75_ngc4088_epsilon_cross_locality_bound_rule_not_endpoint |

## Claim Boundary

The locality-coupled bound is residual-blind and sign-stable for NGC4088,
but remains formula-conditional. It does not authorize endpoint scoring and
does not replace a final Tau-side locality theorem.
