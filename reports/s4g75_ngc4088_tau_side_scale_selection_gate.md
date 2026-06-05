# NGC4088 Tau-Side Scale Selection Gate

This gate applies a pre-endpoint Tau-side selection rule to the
residual-blind scale alternatives. It is a theory-selection audit, not an
endpoint comparison.

## Verdict

Under the minimal source-onset asymptotic-carrier rule, the current
`x_w * Vflat^2` scale is the only selected candidate. This narrows the
`SCALE_UNIQUENESS` blocker, but it does not prove the physical
normalization law because the selection rule itself still needs a
Tau-side closure/readout derivation.

## Selection Criteria

| criterion_id | criterion | galaxy | claim_boundary |
| --- | --- | --- | --- |
| C1_RESIDUAL_BLIND | scale carrier must not use vobs, endpoint residuals, or endpoint scores | NGC4088 | s4g75_ngc4088_tau_side_scale_selection_gate_not_endpoint |
| C2_SOURCE_ONSET_COUPLED | warp/asymmetry scale must carry the measured source onset x_w | NGC4088 | s4g75_ngc4088_tau_side_scale_selection_gate_not_endpoint |
| C3_ASYMPTOTIC_READOUT_CARRIER | dimensionful carrier should be a source/catalog asymptotic readout scale, not a point-sampled median curve statistic | NGC4088 | s4g75_ngc4088_tau_side_scale_selection_gate_not_endpoint |
| C4_NO_EXTERNAL_CLOSURE_COMPARATOR | scale should not require a TPG-like v_v6 closure carrier as the normalizer | NGC4088 | s4g75_ngc4088_tau_side_scale_selection_gate_not_endpoint |
| C5_MINIMAL_SINGLE_SOURCE_FACTOR | scale should not multiply independent onset and closure fractions unless Tau-side theory derives the composite | NGC4088 | s4g75_ngc4088_tau_side_scale_selection_gate_not_endpoint |

## Candidate Gate

| galaxy | scale_id | scale_formula | scale_value_km2_s2 | passes_C1_RESIDUAL_BLIND | passes_C2_SOURCE_ONSET_COUPLED | passes_C3_ASYMPTOTIC_READOUT_CARRIER | passes_C4_NO_EXTERNAL_CLOSURE_COMPARATOR | passes_C5_MINIMAL_SINGLE_SOURCE_FACTOR | n_selection_criteria_passed | failed_criteria | selection_gate_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | CURRENT_XW_VFLAT2 | x_w * Vflat^2 | 8324.02 | True | True | True | True | True | 5 | none | SELECTED_BY_MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE | False | False | s4g75_ngc4088_tau_side_scale_selection_gate_not_endpoint |
| NGC4088 | XW_MEDIAN_VN2 | x_w * median_r(v_n^2) | 6038.61 | True | True | False | True | True | 4 | C3_ASYMPTOTIC_READOUT_CARRIER | THEORY_ALTERNATIVE_REJECTED_BY_ADDITIONAL_CRITERIA | False | False | s4g75_ngc4088_tau_side_scale_selection_gate_not_endpoint |
| NGC4088 | XW_MEDIAN_VV62 | x_w * median_r(v_v6^2) | 12316.1 | True | True | False | False | True | 3 | C3_ASYMPTOTIC_READOUT_CARRIER;C4_NO_EXTERNAL_CLOSURE_COMPARATOR | THEORY_ALTERNATIVE_REJECTED_BY_ADDITIONAL_CRITERIA | False | False | s4g75_ngc4088_tau_side_scale_selection_gate_not_endpoint |
| NGC4088 | CLOSURE_FRACTION_MEDIAN_VN2 | c_g * median_r(v_n^2) | 10509.2 | True | False | False | True | False | 2 | C2_SOURCE_ONSET_COUPLED;C3_ASYMPTOTIC_READOUT_CARRIER;C5_MINIMAL_SINGLE_SOURCE_FACTOR | THEORY_ALTERNATIVE_REJECTED_SOURCE_ONSET_OR_BLINDNESS | False | False | s4g75_ngc4088_tau_side_scale_selection_gate_not_endpoint |
| NGC4088 | XW_CLOSURE_FRACTION_MEDIAN_VN2 | x_w * c_g * median_r(v_n^2) | 2967.29 | True | True | False | True | False | 3 | C3_ASYMPTOTIC_READOUT_CARRIER;C5_MINIMAL_SINGLE_SOURCE_FACTOR | THEORY_ALTERNATIVE_REJECTED_BY_ADDITIONAL_CRITERIA | False | False | s4g75_ngc4088_tau_side_scale_selection_gate_not_endpoint |

## Summary

| galaxy | selection_principle | n_candidates | n_selected_candidates | selected_scale_ids | selection_status | law_status_after_selection | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE | 5 | 1 | CURRENT_XW_VFLAT2 | THEORY_SELECTION_CONDITIONAL_CURRENT_ONLY | SELECTION_RULE_CONDITIONAL_NOT_DERIVED_LAW | False | s4g75_ngc4088_tau_side_scale_selection_gate_not_endpoint |

## Claim Boundary

The selected scale must not be promoted by endpoint performance. This gate
only records a conditional theory-side selection rule.
