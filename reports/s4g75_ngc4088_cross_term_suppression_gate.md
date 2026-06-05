# NGC4088 Cross-Term Suppression Gate

This gate records the correction structure that remains after the
conditional separable product. The current product formula is a
leading-order expression until mixed source-source terms are suppressed
or bounded from residual-blind source observables.

## Leading-Plus-Cross Model

| galaxy | model_id | leading_formula | extended_formula | lambda0_km2_s2 | epsilon_cross_status | proof_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | LEADING_PRODUCT_PLUS_EPSILON_CROSS | lambda_0 = sigma_warp q_warp x_w Vflat^2 | lambda_w = lambda_0 * (1 + epsilon_cross) | 8324.02 | UNBOUNDED_SYMBOLIC_CORRECTION | LEADING_ORDER_ONLY_UNTIL_CROSS_TERMS_SUPPRESSED | s4g75_ngc4088_cross_term_suppression_gate_not_endpoint |

## Cross-Term Ledger

| galaxy | term_id | term_symbol | term_status | interpretation | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| NGC4088 | CROSS_ORIENTATION_STRENGTH | epsilon_sigma_q | NOT_DERIVED | orientation sign and source strength may couple beyond a product factor | s4g75_ngc4088_cross_term_suppression_gate_not_endpoint |
| NGC4088 | CROSS_ONSET_STRENGTH | epsilon_x_q | NOT_DERIVED | onset radius and warp source strength may have mixed dependence | s4g75_ngc4088_cross_term_suppression_gate_not_endpoint |
| NGC4088 | CROSS_ONSET_CARRIER | epsilon_x_vflat | NOT_DERIVED | onset support and asymptotic carrier may not separate exactly | s4g75_ngc4088_cross_term_suppression_gate_not_endpoint |
| NGC4088 | CROSS_GEOMETRY_MEMORY | epsilon_memory | NOT_DERIVED | morphological history/memory may modify the present-day source product | s4g75_ngc4088_cross_term_suppression_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | X1_LEADING_PRODUCT_AVAILABLE | PASS | lambda_0 = sigma q x_w Vflat^2 is conditionally derived under separability | none for leading product algebra | False | False | s4g75_ngc4088_cross_term_suppression_gate_not_endpoint |
| NGC4088 | X2_DIMENSIONAL_EXTENSION_VALID | PASS | epsilon_cross is dimensionless, so lambda_w keeps km^2/s^2 units | none at dimensional level | False | False | s4g75_ngc4088_cross_term_suppression_gate_not_endpoint |
| NGC4088 | X3_CROSS_TERM_PARAMETER_DECLARED | FORMULA_CONDITIONAL | epsilon_cross explicitly represents all omitted mixed source-source terms | derive or bound epsilon_cross from source data | False | False | s4g75_ngc4088_cross_term_suppression_gate_not_endpoint |
| NGC4088 | X4_ZERO_CROSS_TERM_LIMIT | PASS | epsilon_cross = 0 recovers the current multiplicative readout formula | none for the limiting check | False | False | s4g75_ngc4088_cross_term_suppression_gate_not_endpoint |
| NGC4088 | X5_CROSS_TERM_SUPPRESSION_DERIVED | BLOCKED | no Tau-side argument yet proves epsilon_cross is zero or higher-order | derive suppression from locality, independence, symmetry, or scale separation | False | False | s4g75_ngc4088_cross_term_suppression_gate_not_endpoint |
| NGC4088 | X6_SOURCE_BOUND_AVAILABLE | BLOCKED | no residual-blind source bound on epsilon_cross is currently available | define source observables that bound mixed geometry/memory terms | False | False | s4g75_ngc4088_cross_term_suppression_gate_not_endpoint |
| NGC4088 | X7_ENDPOINT_BLINDNESS | PASS | epsilon_cross is symbolic and is not fit to observed rotation residuals | do not tune epsilon_cross in endpoint tests | False | False | s4g75_ngc4088_cross_term_suppression_gate_not_endpoint |

## Summary

| galaxy | model_id | lambda0_km2_s2 | n_cross_terms | n_gates | n_pass | n_formula_conditional | n_blocked | cross_term_status | law_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | LEADING_PRODUCT_PLUS_EPSILON_CROSS | 8324.02 | 4 | 7 | 4 | 1 | 2 | CROSS_TERMS_DECLARED_NOT_SUPPRESSED | LEADING_PRODUCT_ONLY_UNTIL_EPSILON_CROSS_BOUND | False | False | s4g75_ngc4088_cross_term_suppression_gate_not_endpoint |

## Claim Boundary

This is not an endpoint fit. epsilon_cross is symbolic and must not be
tuned against observed rotation residuals.
