# NGC4088 B2 Frozen Asymptotic-Carrier Theorem Gate

This gate records the conditional carrier theorem for the accepted
formula-freeze manifest. It does not use endpoint velocities, residuals,
or score ranks.

## Conditional Theorem

| galaxy | theorem_id | conditional_statement | carrier | carrier_value_km2_s2 | lambda_tau_km2_s2 | formula_freeze_lambda_w_km2_s2 | formula_freeze_alignment_pass | theorem_status | law_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | FROZEN_MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_THEOREM | For a frozen warp/history source-load whose dimensionful normalizer must be residual-blind, source-native, asymptotic, non-comparator, and minimally factorized with the onset x_w, the manifest carrier is Vflat^2 and the source load is Lambda_tau = sigma_warp q_warp x_w Vflat^2. | Vflat^2 | 29480.9 | 8795.11 | 8795.11 | True | CONDITIONAL_CARRIER_THEOREM_FOR_FROZEN_PROTOCOL | FINAL_TAU_SIDE_CARRIER_PROOF_OPEN | ngc4088_b2_frozen_asymptotic_carrier_theorem_gate_not_endpoint |

## Criteria

| galaxy | criterion_id | criterion_status | evidence | law_obligation | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | FC1_RESIDUAL_BLIND | PASS | Vflat is a source/catalog value; no vobs residual or endpoint score is used | none at residual-blindness level | False | False | ngc4088_b2_frozen_asymptotic_carrier_theorem_gate_not_endpoint |
| NGC4088 | FC2_SOURCE_NATIVE_ASYMPTOTIC | PASS | Vflat is the manifest's source/catalog flat-speed asymptotic carrier | derive why the outer readout carrier must be the flat-speed carrier | False | False | ngc4088_b2_frozen_asymptotic_carrier_theorem_gate_not_endpoint |
| NGC4088 | FC3_SOURCE_ONSET_COUPLED | PASS | carrier enters only through x_w Vflat^2 in the frozen source-load | none at frozen source-load bookkeeping level | False | False | ngc4088_b2_frozen_asymptotic_carrier_theorem_gate_not_endpoint |
| NGC4088 | FC4_NO_EXTERNAL_COMPARATOR | PASS | the frozen manifest does not use TPG/v6, MOND, RAR, or Newtonian residual comparators as normalizers | derive comparator autonomy from Tau-side readout architecture | False | False | ngc4088_b2_frozen_asymptotic_carrier_theorem_gate_not_endpoint |
| NGC4088 | FC5_MINIMAL_FACTORIZATION | PASS | source-load uses one onset factor and one asymptotic carrier, not extra closure-fraction composites | derive minimal factorization or carry it as a protocol premise | False | False | ngc4088_b2_frozen_asymptotic_carrier_theorem_gate_not_endpoint |
| NGC4088 | FC6_FREEZE_ALIGNMENT | PASS | sigma*q*x_w*Vflat^2 reproduces the frozen lambda_w | none at arithmetic freeze-alignment level | False | False | ngc4088_b2_frozen_asymptotic_carrier_theorem_gate_not_endpoint |
| NGC4088 | FC7_ALTERNATIVE_CARRIER_EXCLUSION | CONDITIONAL | older first-pass audit rejects point medians and external comparators under the same selection logic | repeat alternative enumeration on the frozen manifest protocol or a predeclared sample | False | False | ngc4088_b2_frozen_asymptotic_carrier_theorem_gate_not_endpoint |
| NGC4088 | FC8_POPULATION_TRANSFER | OPEN_FOR_CLAIMS | single-galaxy frozen carrier theorem only | apply to a predeclared source-rich warp/history sample | False | False | ngc4088_b2_frozen_asymptotic_carrier_theorem_gate_not_endpoint |

## Summary

| galaxy | frozen_carrier_theorem_status | carrier_value_km2_s2 | lambda_tau_km2_s2 | formula_freeze_alignment_pass | source_load_origin_status | n_criteria | n_pass | n_conditional | n_open_for_claims | law_level_closed | endpoint_scores_allowed | uses_vobs_or_residual | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | FROZEN_VFLAT2_CARRIER_CONDITIONAL_THEOREM_LAW_PROOF_OPEN | 29480.9 | 8795.11 | True | SOURCE_LOAD_ORIGIN_PARTIALLY_GROUNDED_CARRIER_AND_CROSS_OPEN | 8 | 6 | 1 | 1 | False | False | False | derive comparator autonomy and minimal asymptotic carrier dominance on a predeclared warp/history population | ngc4088_b2_frozen_asymptotic_carrier_theorem_gate_not_endpoint |

## Interpretation

`Vflat^2` is conditionally justified as the frozen protocol carrier under
the minimal residual-blind source-onset asymptotic-carrier rule. This
sharpens the B2 carrier premise, but it is not yet a final Tau-side law:
alternative-carrier exclusion, comparator autonomy, and population
transfer remain open.
