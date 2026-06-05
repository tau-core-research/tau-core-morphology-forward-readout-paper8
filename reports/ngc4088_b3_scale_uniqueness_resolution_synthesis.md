# NGC4088 B3 Scale-Uniqueness Resolution Synthesis

This report separates protocol-level uniqueness from law-level uniqueness.
The minimal source-onset asymptotic-carrier rule selects one scale, but
that rule is still conditional on B2. No endpoint score is used.

## Summary

| galaxy | b3_synthesis_status | initial_uniqueness_decision | selection_principle | n_initial_residual_blind_scales | n_selected_by_protocol_rule | selected_scale_ids | conditional_uniqueness_resolved | law_level_uniqueness_resolved | formula_freeze_allowed_now | endpoint_scores_allowed | uses_vobs_or_residual | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | B3_CONDITIONAL_UNIQUE_SCALE_SELECTED_LAW_LEVEL_UNIQUENESS_OPEN | BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES | MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE | 5 | 1 | CURRENT_XW_VFLAT2 | True | False | False | False | False | close B2 asymptotic-carrier and closure-functional obligations, or keep B3 as protocol-conditional only | ngc4088_b3_scale_uniqueness_resolution_synthesis_not_endpoint |

## Candidate Resolution

| galaxy | scale_id | scale_formula | scale_value_km2_s2 | current_prefactor_ratio | source_status | selection_gate_status | n_selection_criteria_passed | failed_criteria | tau_side_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | CURRENT_XW_VFLAT2 | x_w * Vflat^2 | 8324.02 | 1 | CURRENT_FORMULA_CONDITIONAL_CANDIDATE | SELECTED_BY_MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE | 5 | none | derive why onset fraction times catalog flat-speed carrier is selected | False | False | ngc4088_b3_scale_uniqueness_resolution_synthesis_not_endpoint |
| NGC4088 | XW_MEDIAN_VN2 | x_w * median_r(v_n^2) | 6038.61 | 0.725444 | RESIDUAL_BLIND_BARYONIC_SCALE_ALTERNATIVE | THEORY_ALTERNATIVE_REJECTED_BY_ADDITIONAL_CRITERIA | 4 | C3_ASYMPTOTIC_READOUT_CARRIER | rule out if flat-speed carrier is required rather than baryonic readout carrier | False | False | ngc4088_b3_scale_uniqueness_resolution_synthesis_not_endpoint |
| NGC4088 | XW_MEDIAN_VV62 | x_w * median_r(v_v6^2) | 12316.1 | 1.47959 | RESIDUAL_BLIND_TPG_CLOSURE_SCALE_ALTERNATIVE | THEORY_ALTERNATIVE_REJECTED_BY_ADDITIONAL_CRITERIA | 3 | C3_ASYMPTOTIC_READOUT_CARRIER;C4_NO_EXTERNAL_CLOSURE_COMPARATOR | rule out if external TPG-like closure carrier is not allowed as Tau-side normalizer | False | False | ngc4088_b3_scale_uniqueness_resolution_synthesis_not_endpoint |
| NGC4088 | CLOSURE_FRACTION_MEDIAN_VN2 | c_g * median_r(v_n^2) | 10509.2 | 1.26251 | TAU_SOURCE_NORMALIZATION_RULE_ALTERNATIVE | THEORY_ALTERNATIVE_REJECTED_SOURCE_ONSET_OR_BLINDNESS | 2 | C2_SOURCE_ONSET_COUPLED;C3_ASYMPTOTIC_READOUT_CARRIER;C5_MINIMAL_SINGLE_SOURCE_FACTOR | decide whether NGC4088 warp lane must use local closure fraction instead of x_w | False | False | ngc4088_b3_scale_uniqueness_resolution_synthesis_not_endpoint |
| NGC4088 | XW_CLOSURE_FRACTION_MEDIAN_VN2 | x_w * c_g * median_r(v_n^2) | 2967.29 | 0.356473 | COMPOSITE_ONSET_CLOSURE_SCALE_ALTERNATIVE | THEORY_ALTERNATIVE_REJECTED_BY_ADDITIONAL_CRITERIA | 3 | C3_ASYMPTOTIC_READOUT_CARRIER;C5_MINIMAL_SINGLE_SOURCE_FACTOR | derive or reject a two-factor onset-plus-closure carrier | False | False | ngc4088_b3_scale_uniqueness_resolution_synthesis_not_endpoint |

## Remaining Obligations

| obligation_id | obligation_status | requirement | current_evidence | why_not_final | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| B3O1_PROTOCOL_SELECTION_RULE_FROZEN | CONDITIONAL_PASS | use the minimal source-onset asymptotic-carrier rule before endpoint scoring | THEORY_SELECTION_CONDITIONAL_CURRENT_ONLY | the rule is conditional until B2 derives the carrier principle | False | ngc4088_b3_scale_uniqueness_resolution_synthesis_not_endpoint |
| B3O2_REJECT_BARYONIC_MEDIAN_CARRIER | CONDITIONAL_PASS | reject x_w * median_r(v_n^2) as a local baryonic readout statistic | fails C3_ASYMPTOTIC_READOUT_CARRIER | requires the asymptotic-carrier theorem from B2 | False | ngc4088_b3_scale_uniqueness_resolution_synthesis_not_endpoint |
| B3O3_REJECT_EXTERNAL_TPG_COMPARATOR | CONDITIONAL_PASS | reject x_w * median_r(v_v6^2) as an external comparator normalizer | fails C3_ASYMPTOTIC_READOUT_CARRIER and C4_NO_EXTERNAL_CLOSURE_COMPARATOR | requires comparator-autonomy derivation, not only protocol exclusion | False | ngc4088_b3_scale_uniqueness_resolution_synthesis_not_endpoint |
| B3O4_REJECT_CLOSURE_FRACTION_COMPOSITES | CONDITIONAL_PASS | reject c_g and x_w*c_g composite scales unless Tau-side theory derives extra factors | fails C2 or C5 depending on candidate | requires minimal-source-factor theorem or explicit source-factor coupling law | False | ngc4088_b3_scale_uniqueness_resolution_synthesis_not_endpoint |
| B3O5_LAW_LEVEL_UNIQUENESS | OPEN | derive why only CURRENT_XW_VFLAT2 survives as a Tau-side scale law | NOT_DERIVED_TAU_SIDE_PHYSICAL_NORMALIZATION_LAW | B2 closure functional and asymptotic-carrier theorem remain open | False | ngc4088_b3_scale_uniqueness_resolution_synthesis_not_endpoint |

## Interpretation

B3 is no longer an unstructured multiple-scale problem: under the frozen
conditional selection rule, CURRENT_XW_VFLAT2 is the only selected scale.
However, law-level scale uniqueness remains open because the rule depends
on the B2 asymptotic-carrier and closure-functional derivations. Thus B3
remains endpoint-blocking until B2 is closed or the lane is explicitly
demoted to a sensitivity-only formula shell.
