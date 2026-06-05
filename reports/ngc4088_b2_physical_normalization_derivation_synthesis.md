# NGC4088 B2 Physical-Normalization Derivation Synthesis

This report consolidates the B2 status. It asks whether the conditional
normalization `lambda_w = sigma_warp q_warp x_w Vflat^2` is already a
Tau-side physical law. The answer is no: it is a strong formula shell and
a conditional derivation path, but the final law-level proof is still open.

## Summary

| galaxy | b2_synthesis_status | formula_quality | law_quality | formula_freeze_alignment_status | numeric_lambda_w_km2_s2 | first_pass_lambda_w_km2_s2 | normalization_source | n_components | n_open_law_obligations | formula_freeze_allowed_now | endpoint_scores_allowed | uses_vobs_or_residual | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | B2_FORMULA_CONDITIONAL_DERIVATION_SYNTHESIZED_LAW_STILL_OPEN | DIMENSIONALLY_VALID_RESIDUAL_BLIND_EXECUTABLE | NOT_DERIVED_TAU_SIDE_PHYSICAL_NORMALIZATION_LAW | ALIGNED_TO_FORMULA_FREEZE_MANIFEST | 8795.11 | 8324.02 | FORMULA_FREEZE_MANIFEST_REVIEW_ACCEPTED_XW | 9 | 4 | False | False | False | construct closure functional and asymptotic-carrier theorem, or explicitly demote NGC4088 to sensitivity-only formula shell | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |

## Candidate Formula

| galaxy | candidate_formula | lambda_w_conditional | numeric_lambda_w_km2_s2 | formula_freeze_manifest_lambda_w_km2_s2 | first_pass_lambda_w_km2_s2 | x_w_formula_freeze | q_warp | sigma_warp | vflat_km_s | normalization_source | formula_freeze_alignment_pass | source_note | status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | delta_v2_warp(R;p) = lambda_w C_warp(R/R_HI; x_w,p) | sigma_warp q_warp x_w Vflat^2 | 8795.11 | 8795.11 | 8324.02 | 0.298333 | 1 | 1 | 171.7 | FORMULA_FREEZE_MANIFEST_REVIEW_ACCEPTED_XW | True | aligned to the caveated formula-freeze manifest; the earlier physical-normalization law gate value is retained as superseded first-pass provenance | FORMULA_CONDITIONAL_NOT_FINAL_LAW | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |

The numerical normalization is aligned to the accepted formula-freeze
manifest when that manifest is present. This supersedes the earlier
first-pass physical-normalization value for the endpoint formula, while
preserving the first-pass value as provenance rather than deleting it.

## Components

| component_id | component_status | what_is_established | what_is_missing | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| B2C1_DIMENSIONAL_AND_RESIDUAL_BLIND_FORMULA | FORMULA_CONDITIONAL_PHYSICAL_LAW_BLOCKED | formula is executable, dimensionally consistent, generated without endpoint residuals, and aligned to the accepted formula-freeze source manifest | law-level Tau-side derivation | False | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |
| B2C2_SCALE_SELECTION | THEORY_SELECTION_CONDITIONAL_CURRENT_ONLY | minimal source-onset asymptotic-carrier rule selects CURRENT_XW_VFLAT2 | selection rule itself is conditional, not a final law | False | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |
| B2C3_SCALE_DERIVATION_GATE | DERIVATION_BLOCKED_SELECTION_RULE_AUDITED | derivation skeleton identifies the needed Tau-side assumptions | asymptotic carrier dominance and closure functional derivation | False | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |
| B2C4_ASYMPTOTIC_CARRIER | ASYMPTOTIC_CARRIER_DOMINANCE_NOT_DERIVED | Vflat^2 is a valid residual-blind source/catalog carrier candidate | proof that Vflat^2 is forced as Tau-side asymptotic carrier | False | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |
| B2C5_CLOSURE_FUNCTIONAL | CLOSURE_FUNCTIONAL_REQUIREMENT_SPECIFIED_NOT_DERIVED | required functional form and solved target are specified | actual Tau-side closure functional and Euler stationarity proof | False | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |
| B2C6_TARGET_ORIGIN | SOURCE_FACTORS_AVAILABLE_COUPLING_NOT_DERIVED | source factors for the target lambda are available | source-factor coupling is not derived as Tau-side law | False | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |
| B2C7_EULER_ANSATZ | EULER_CONDITION_SOLVED_GIVEN_TARGET_ANSATZ | given a target quadratic ansatz, the Euler condition solves to the candidate lambda | the target ansatz itself is not yet Tau-side derived | False | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |
| B2C8_SEPARABILITY | CONDITIONAL_PRODUCT_DERIVED_IF_SEPARABLE | conditional product form follows if separable source factors and suppressed cross terms hold | separability and cross-term suppression are not final derived laws | False | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |
| B2C9_CROSS_TERM_SUPPRESSION | CROSS_TERMS_DECLARED_NOT_SUPPRESSED | cross-term status has an explicit source-side audit | final Tau-side bound/vanishing theorem for cross terms | False | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |

## Remaining Law Obligations

| obligation_id | obligation_status | requirement | why_required | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| B2O1_CLOSURE_FUNCTIONAL_CONSTRUCTION | OPEN | construct J_tau[lambda_w] from Tau-side morphology/readout and closure data, not from endpoint residuals | without J_tau, the Euler solution remains an ansatz rather than a derivation | False | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |
| B2O2_ASYMPTOTIC_CARRIER_THEOREM | OPEN | derive Vflat^2 as the asymptotic Tau-side readout carrier | otherwise Vflat^2 is a good residual-blind catalog scale, not a forced carrier | False | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |
| B2O3_SEPARABILITY_OR_CROSS_TERM_BOUND | OPEN | prove separable product coupling or freeze a source-side cross-term uncertainty interval | otherwise sigma*q*x_w*Vflat^2 is conditional on unproved coupling assumptions | False | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |
| B2O4_POPULATION_TRANSFER | OPEN_FOR_CLAIMS | repeat the same derivation gate on a predeclared warp/history source-rich sample | single-galaxy derivation support cannot justify broad population claims | False | ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint |

## Interpretation

B2 has been narrowed substantially. The package now knows exactly how the
candidate law would look and which assumptions make it work. However, the
Tau-side closure functional, the asymptotic-carrier theorem, and the
separability/cross-term bound remain open. Therefore the formula remains
formula-conditional and endpoint-blocked.
