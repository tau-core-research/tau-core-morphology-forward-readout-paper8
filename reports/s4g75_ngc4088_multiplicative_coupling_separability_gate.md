# NGC4088 Multiplicative-Coupling Separability Gate

This gate records a conditional derivation of the product target. It
shows what follows if the Tau-side source readout is separable, while
preserving the fact that separability and cross-term suppression are not
yet derived.

## Conditional Theorem

| galaxy | theorem_id | statement | derived_product_formula | derived_product_value_km2_s2 | proof_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | CONDITIONAL_SEPARABLE_SOURCE_READOUT_PRODUCT | If the warp/asymmetry readout amplitude separates into orientation sign, source strength, onset support fraction, and asymptotic carrier factors, then the first-order target scale is lambda_w = sigma_warp q_warp x_w Vflat^2. | lambda_w = sigma_warp q_warp x_w Vflat^2 | 8324.02 | FORMULA_DERIVED_GIVEN_SEPARABILITY_ASSUMPTIONS | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |

## Assumptions

| galaxy | assumption_id | assumption_status | content | claim_boundary |
| --- | --- | --- | --- | --- |
| NGC4088 | S1_FACTOR_SEPARABILITY | ASSUMPTION_NOT_DERIVED | readout amplitude factorizes into independent local source factors | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |
| NGC4088 | S2_ORIENTATION_SIGN | THEORY_CONDITIONAL | sigma_warp supplies the readout orientation/sign | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |
| NGC4088 | S3_SOURCE_STRENGTH | SOURCE_NATIVE_QUALITATIVE_GATE | q_warp supplies source strength; currently q_warp=1 qualitative gate | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |
| NGC4088 | S4_ONSET_SUPPORT | SOURCE_MEASURED_FORMULA_CONDITIONAL | x_w supplies the dimensionless onset/support fraction | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |
| NGC4088 | S5_ASYMPTOTIC_CARRIER | SOURCE_CATALOG_CANDIDATE_NOT_DERIVED | Vflat^2 supplies the dimensionful asymptotic carrier | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |
| NGC4088 | S6_NO_CROSS_TERMS_AT_FIRST_ORDER | ASSUMPTION_NOT_DERIVED | mixed source-source coupling terms are absent or higher-order | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | M1_PRODUCT_ALGEBRA | PASS | the factor product reproduces lambda_w = 8324.016 km^2/s^2 | none at algebra level | False | False | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |
| NGC4088 | M2_DIMENSIONAL_CONSISTENCY | PASS | dimensionless factors times Vflat^2 yield km^2/s^2 | none at dimensional level | False | False | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |
| NGC4088 | M3_SEPARABILITY_ASSUMPTION | FORMULA_CONDITIONAL | product follows if the local source readout is separable | derive separability from Tau-side slice/readout geometry | False | False | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |
| NGC4088 | M4_SOURCE_FACTOR_GROUNDING | FORMULA_CONDITIONAL | q_warp and x_w are source-side factors but q_warp is qualitative and x_w needs independent review | replace qualitative strength and independently review onset | False | False | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |
| NGC4088 | M5_CARRIER_GROUNDING | FORMULA_CONDITIONAL | Vflat^2 is a source-catalog carrier candidate | derive asymptotic carrier dominance | False | False | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |
| NGC4088 | M6_NO_CROSS_TERMS | BLOCKED | no derivation yet excludes mixed source-source coupling corrections | derive absence/suppression of cross terms | False | False | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |
| NGC4088 | M7_POPULATION_TRANSFER | BLOCKED | the separability statement is currently NGC4088-specific | run on a predeclared warp/asymmetry source-rich sample | False | False | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |

## Summary

| galaxy | theorem_id | lambda_product_km2_s2 | n_assumptions | n_gates | n_pass | n_formula_conditional | n_blocked | coupling_status | law_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | CONDITIONAL_SEPARABLE_SOURCE_READOUT_PRODUCT | 8324.02 | 6 | 7 | 2 | 3 | 2 | CONDITIONAL_PRODUCT_DERIVED_IF_SEPARABLE | SEPARABILITY_AND_CROSS_TERM_SUPPRESSION_NOT_DERIVED | False | False | s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint |

## Claim Boundary

This is not an endpoint test and not a final law. It upgrades the
multiplicative coupling from arbitrary composition to a conditional
separability result.
