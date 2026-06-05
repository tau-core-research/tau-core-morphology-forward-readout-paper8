# NGC4088 B2 Closure/Asymptotic Conditional Derivation Gate

This gate records the strongest current B2 result without overclaiming.
It proves the normalization only conditionally: if the Tau-side closure
functional has the specified target-stationary form and `Vflat^2` is the
derived asymptotic carrier, then the stationary normalization is
`lambda_w = sigma_warp q_warp x_w Vflat^2`.

It does not use endpoint velocities, residuals, or score ranks.

## Conditional Theorem

| galaxy | theorem_id | conditional_statement | derived_formula | numeric_lambda_w_km2_s2 | formula_freeze_manifest_lambda_w_km2_s2 | formula_freeze_alignment_pass | mathematical_status | tau_side_law_status | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | B2_CLOSURE_ASYMPTOTIC_CONDITIONAL_DERIVATION | If J_tau[lambda_w] has the target-stationary closure form with positive stiffness, Vflat^2 is the Tau-side asymptotic carrier, and the source factors sigma_warp, q_warp, and x_w enter separably with suppressed cross terms, then the stationary normalization is lambda_w = sigma_warp q_warp x_w Vflat^2. | lambda_w = sigma_warp q_warp x_w Vflat^2 | 8795.11 | 8795.11 | True | ALGEBRAICALLY_DERIVED_GIVEN_TARGET_FUNCTIONAL | FORMULA_CONDITIONAL_PREMISES_OPEN | False | False | ngc4088_b2_closure_asymptotic_conditional_derivation_not_endpoint |

## Conditions

| condition_id | condition_type | current_status | what_is_established | what_remains_open | source_status | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B2D1_SOURCE_FREEZE_ALIGNMENT | derived_status_input | PASS | the conditional formula uses the accepted formula-freeze x_w and reproduces the frozen lambda_w | none at formula-freeze alignment level | NGC4088_WARP_HISTORY_FREEZE_V1 | False | False | ngc4088_b2_closure_asymptotic_conditional_derivation_not_endpoint |
| B2D2_DIMENSIONAL_AND_LIMIT_CHECK | derived_status_input | PASS | lambda_w has velocity-squared units; C_warp is dimensionless; zero-source and inactive-window limits recover the carrier | none at dimensional or limit-audit level | PASS: lambda_w has km^2 s^-2 units; C_warp is dimensionless; Delta v^2 has velocity-squared units | False | False | ngc4088_b2_closure_asymptotic_conditional_derivation_not_endpoint |
| B2D3_EULER_STATIONARITY_GIVEN_TARGET | conditional_derivation | FORMULA_CONDITIONAL_PASS | given a quadratic target functional, dJ/dlambda_w=0 solves to lambda_w = sigma_warp q_warp x_w Vflat^2 | derive the target functional itself from Tau-side closure/readout data | EULER_CONDITION_SOLVED_GIVEN_TARGET_ANSATZ | False | False | ngc4088_b2_closure_asymptotic_conditional_derivation_not_endpoint |
| B2D4_CLOSURE_FUNCTIONAL_ORIGIN | law_level_premise | CONDITIONAL_FUNCTIONAL_CONSTRUCTED | an explicit source-load norm-square J_load[lambda_w] yields the frozen normalization by Euler stationarity; the frozen source-load factor ladder is partially grounded | derive the source-load origin, closure weight, and uniqueness from Tau-side morphology/readout data | CLOSURE_FUNCTIONAL_REQUIREMENT_SPECIFIED_NOT_DERIVED; SOURCE_LOAD_CLOSURE_FUNCTIONAL_CONSTRUCTED_CONDITIONALLY; SOURCE_LOAD_ORIGIN_PARTIALLY_GROUNDED_CARRIER_AND_CROSS_OPEN | False | False | ngc4088_b2_closure_asymptotic_conditional_derivation_not_endpoint |
| B2D5_ASYMPTOTIC_CARRIER_ORIGIN | law_level_premise | CONDITIONAL_CARRIER_THEOREM | Vflat^2 is conditionally justified as the frozen protocol carrier under residual-blind source-onset asymptotic criteria | promote the frozen carrier theorem to final Tau-side law through alternative-carrier exclusion and population transfer | ASYMPTOTIC_CARRIER_DOMINANCE_NOT_DERIVED; FROZEN_VFLAT2_CARRIER_CONDITIONAL_THEOREM_LAW_PROOF_OPEN | False | False | ngc4088_b2_closure_asymptotic_conditional_derivation_not_endpoint |
| B2D6_SEPARABILITY_AND_CROSS_TERM_BOUND | law_level_premise | PARTIAL_SOURCE_BOUND | conditional product form is audited and cross-term handling has a partial source-bound/sharp-coefficient protocol | complete q/memory source observables, prove suppression, or carry epsilon_cross as explicit source-side uncertainty | CONDITIONAL_PRODUCT_DERIVED_IF_SEPARABLE; CROSS_TERMS_DECLARED_NOT_SUPPRESSED; SOURCE_LOAD_ORIGIN_PARTIALLY_GROUNDED_CARRIER_AND_CROSS_OPEN | False | False | ngc4088_b2_closure_asymptotic_conditional_derivation_not_endpoint |
| B2D7_POPULATION_TRANSFER | claim_scope_premise | OPEN_FOR_CLAIMS | single-galaxy conditional theorem is now explicit | repeat the gate on a predeclared warp/history source-rich sample | B2_FORMULA_CONDITIONAL_DERIVATION_SYNTHESIZED_LAW_STILL_OPEN | False | False | ngc4088_b2_closure_asymptotic_conditional_derivation_not_endpoint |

## Summary

| galaxy | b2_conditional_derivation_status | numeric_lambda_w_km2_s2 | formula_freeze_alignment_pass | n_conditions | n_pass_or_formula_conditional_pass | n_open_law_premises | law_level_closed | endpoint_scores_allowed | uses_vobs_or_residual | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | B2_CONDITIONAL_THEOREM_ALIGNED_TO_FREEZE_MANIFEST_LAW_PREMISES_OPEN | 8795.11 | True | 7 | 5 | 3 | False | False | False | derive the Tau-side source-load origin, upgrade the frozen Vflat^2 carrier theorem to a final carrier law/population transfer result, and prove the cross-term suppression bound | ngc4088_b2_closure_asymptotic_conditional_derivation_not_endpoint |

## Interpretation

B2 is now stronger than an informal ansatz: the formula-freeze-aligned
normalization is algebraically derived given the target functional and
carrier premises.  It is not yet a final Tau-side law because the
closure functional, the forced `Vflat^2` carrier theorem, and the
separability/cross-term proof remain open.
