# NGC4088 Asymptotic-Carrier Dominance Gate

This subgate asks whether `Vflat^2` is a derived asymptotic Tau-side
readout carrier, rather than merely a residual-blind catalog scale.

## Verdict

`Vflat^2` passes availability and dimensional checks, and the selection
protocol rejects point-sampled medians and external TPG-like comparators.
However, asymptotic-carrier dominance is not derived: a Tau-side
closure/readout functional and population transfer remain blocked.

## Carrier

| galaxy | carrier_id | source_constant | selected_scale_id | carrier_value_km2_s2 | unit | source_status | current_interpretation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | VFLAT2_ASYMPTOTIC_CARRIER_CANDIDATE | velocity_scale_candidate | CURRENT_XW_VFLAT2 | 29480.9 | km2_s2 | SOURCE_CATALOG_SCALE_CANDIDATE | SOURCE_CATALOG_SCALE_CANDIDATE_NOT_DERIVED_CARRIER | s4g75_ngc4088_asymptotic_carrier_dominance_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | A1_CATALOG_ASYMPTOTIC_SCALE_AVAILABLE | PASS | Vflat^2 is available as a residual-blind source/catalog velocity-squared scale | none at availability level | False | False | s4g75_ngc4088_asymptotic_carrier_dominance_gate_not_endpoint |
| NGC4088 | A2_DIMENSIONAL_CARRIER | PASS | Vflat^2 has the required delta-v-squared dimension | none at dimensional level | False | False | s4g75_ngc4088_asymptotic_carrier_dominance_gate_not_endpoint |
| NGC4088 | A3_POINT_SAMPLED_MEDIANS_REJECTED | PASS | selection gate rejects x_w * median_r(v_n^2) and x_w * median_r(v_v6^2) | derive why point-sampled curve statistics are not Tau-side carriers | False | False | s4g75_ngc4088_asymptotic_carrier_dominance_gate_not_endpoint |
| NGC4088 | A4_EXTERNAL_COMPARATOR_REJECTED | PASS | selection gate rejects the v_v6 normalizer as an external TPG-like comparator | derive comparator autonomy from the closure/readout architecture | False | False | s4g75_ngc4088_asymptotic_carrier_dominance_gate_not_endpoint |
| NGC4088 | A5_ASYMPTOTIC_READOUT_INTERPRETATION | FORMULA_CONDITIONAL | Vflat^2 can be read as an outer/asymptotic source carrier in the current formula shell | show that this interpretation is forced by Tau-side readout geometry | False | False | s4g75_ngc4088_asymptotic_carrier_dominance_gate_not_endpoint |
| NGC4088 | A6_TAU_CLOSURE_DERIVES_VFLAT | BLOCKED | no Tau-side closure functional currently solves for Vflat^2 as the preferred carrier | derive the asymptotic carrier from a closure/readout functional | False | False | s4g75_ngc4088_asymptotic_carrier_dominance_gate_not_endpoint |
| NGC4088 | A7_UNIQUENESS_AGAINST_OTHER_ASYMPTOTIC_CARRIERS | BLOCKED | other source-native asymptotic carriers could exist but have not been enumerated for a sample | audit Vflat^2 against predeclared alternatives such as HI widths or outer-source speeds | False | False | s4g75_ngc4088_asymptotic_carrier_dominance_gate_not_endpoint |
| NGC4088 | A8_POPULATION_TRANSFER | BLOCKED | current carrier-dominance audit is NGC4088-specific | test the same residual-blind carrier rule on a predeclared warp/asymmetry population | False | False | s4g75_ngc4088_asymptotic_carrier_dominance_gate_not_endpoint |

## Summary

| galaxy | carrier_id | selected_scale_id | n_gates | n_pass | n_formula_conditional | n_blocked | dominance_status | law_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | VFLAT2_ASYMPTOTIC_CARRIER_CANDIDATE | CURRENT_XW_VFLAT2 | 8 | 4 | 1 | 3 | ASYMPTOTIC_CARRIER_DOMINANCE_NOT_DERIVED | VFLAT2_SOURCE_CANDIDATE_NOT_TAU_SIDE_CARRIER_PROOF | False | False | s4g75_ngc4088_asymptotic_carrier_dominance_gate_not_endpoint |

## Claim Boundary

This audit preserves the distinction between a source-catalog carrier
candidate and a derived Tau-side carrier. It uses no endpoint residuals
or observed rotation velocities.
