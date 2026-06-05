# NGC4088 B2 Source-Load Origin Derivation Gate

This gate decomposes the frozen `Lambda_tau` source-load using the
accepted formula-freeze manifest. It does not score rotations and does
not use endpoint residuals.

## Factors

| galaxy | factor_id | symbol | value | unit | factor_status | source_evidence | remaining_law_obligation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | SLF1_ORIENTATION_SIGN | sigma_warp | 1 | dimensionless | SOURCE_PROTOCOL_FROZEN_CONDITIONAL | positive outer warp/history added-readout sign frozen from source-side orientation protocol | derive the sign from Tau-side orientation/readout geometry | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |
| NGC4088 | SLF2_SOURCE_STRENGTH | q_warp | 1 | dimensionless | SOURCE_PROTOCOL_FROZEN_QUALITATIVE | source-response review / filled warp closure mapping | replace qualitative q_warp=1 by source-native amplitude law or uncertainty interval | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |
| NGC4088 | SLF3_ONSET_SUPPORT | x_w | 0.298333 | dimensionless | SOURCE_FROZEN_CAVEATED_ACCEPTED | WHISP graphical-overview frozen extraction, caveated | carry WHISP graphical provenance caveat; direct H I product remains provenance upgrade | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |
| NGC4088 | SLF4_ASYMPTOTIC_CARRIER | Vflat^2 | 29480.9 | km2_s2 | SOURCE_CATALOG_CANDIDATE_LAW_OPEN | MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE; FROZEN_VFLAT2_CARRIER_CONDITIONAL_THEOREM_LAW_PROOF_OPEN | upgrade the frozen-protocol Vflat^2 carrier theorem to a final Tau-side carrier law and population-transfer result | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |
| NGC4088 | SLF5_SOURCE_LOAD_PRODUCT | Lambda_tau | 8795.11 | km2_s2 | FREEZE_ALIGNED_PRODUCT_CONDITIONAL | lambda_w=sigma_warp*q_warp*x_w*Vflat^2 | derive source-load uniqueness and separability/cross-term suppression | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | SLO1_FREEZE_ALIGNMENT | PASS | source-load product reproduces the formula-freeze manifest lambda_w | none at freeze-alignment level | False | False | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |
| NGC4088 | SLO2_DIMENSION_AND_LIMITS | PASS | dimensionless factors times Vflat^2 yield km^2/s^2; zero-source and inactive-window limits pass | none at dimension/limit level | False | False | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |
| NGC4088 | SLO3_CLOSURE_FUNCTIONAL_STATIONARITY | PASS | SOURCE_LOAD_CLOSURE_FUNCTIONAL_CONSTRUCTED_CONDITIONALLY | derive closure weight and source-load origin from Tau-side geometry | False | False | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |
| NGC4088 | SLO4_ONSET_SOURCE_ACCEPTANCE | PASS_CAVEATED | x_w is accepted for formula freeze from WHISP graphical-overview extraction | direct source-coordinate H I/FITS product would reduce provenance caveat | False | False | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |
| NGC4088 | SLO5_STRENGTH_AND_SIGN_LAW | FORMULA_CONDITIONAL | sigma_warp and q_warp are frozen by source protocol, but not derived as Tau-side laws | derive sign/strength mapping from orientation and source response | False | False | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |
| NGC4088 | SLO6_ASYMPTOTIC_CARRIER_THEOREM | CONDITIONAL_CARRIER_THEOREM | ASYMPTOTIC_CARRIER_DOMINANCE_NOT_DERIVED; FROZEN_VFLAT2_CARRIER_CONDITIONAL_THEOREM_LAW_PROOF_OPEN | promote frozen single-galaxy carrier theorem to final Tau-side/population law | False | False | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |
| NGC4088 | SLO7_CROSS_TERM_SUPPRESSION_BOUND | PARTIAL | SOURCE_BOUND_PROTOCOL_PARTIAL_NUMERIC_BOUND_BLOCKED; BI_COEFFICIENTS_SHARPENED_PROTOCOL_BOUND_READY; numeric_bound_authorized=True | complete q/memory source observables or keep epsilon_cross as explicit uncertainty | False | False | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |
| NGC4088 | SLO8_POPULATION_TRANSFER | OPEN_FOR_CLAIMS | NGC4088-only source-load origin ladder | repeat on a predeclared warp/history source-rich sample | False | False | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |

## Summary

| galaxy | source_load_origin_status | lambda_tau_km2_s2 | formula_freeze_alignment_pass | n_factors | n_gates | n_pass_like | n_formula_conditional | n_partial | n_conditional_carrier_theorem | n_open_or_open_for_claims | law_level_closed | endpoint_scores_allowed | uses_vobs_or_residual | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | SOURCE_LOAD_ORIGIN_PARTIALLY_GROUNDED_CARRIER_AND_CROSS_OPEN | 8795.11 | True | 5 | 8 | 4 | 1 | 1 | 1 | 1 | False | False | False | upgrade frozen Vflat^2 carrier dominance to a final Tau-side law and close or carry epsilon_cross as source-side uncertainty | ngc4088_b2_source_load_origin_derivation_gate_not_endpoint |

## Interpretation

The source-load is now partially grounded at protocol level: the product
is aligned to the frozen manifest, the conditional source-load closure
functional supplies the stationarity equation, and the onset factor is
accepted with a provenance caveat. The remaining law-level work is the
forced `Vflat^2` carrier theorem and a closed or explicitly carried
`epsilon_cross` source-side uncertainty.
