# NGC4088 B_i Coefficient-Rule Gate

This gate fixes the residual-blind feature-normalization side of the
`epsilon_cross` bound. If a residual-blind sharpened coefficient rule
is available, this gate carries it into the numeric-bound shell;
otherwise it falls back to the conservative unit-bound freeze. Neither
path uses endpoint residuals.

## Summary

| galaxy | rule_id | n_features | n_available_features | n_coefficients | n_available_coefficients | n_gates | n_pass | n_blocked | coefficient_rule_status | numeric_bound_status | source_response_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_EPSILON_CROSS_BI_COEFFICIENT_RULE_GATE | 4 | 4 | 4 | 4 | 6 | 6 | 0 | FEATURE_NORMALIZATION_AND_B_VALUES_READY_PROTOCOL_BOUND | NUMERIC_EPSILON_PROTOCOL_BOUND_READY | SOURCE_RESPONSES_ACCEPTED_FOR_PROTOCOL_BOUND | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |

## Feature Normalization

| galaxy | feature_id | feature_symbol | definition | source_inputs | feature_value | unit | status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | F_PA | f_PA | min(|Delta_PA_outer_inner| / 180 deg, 1) | Delta_PA_outer_inner | 0.5 | dimensionless | ACCEPTED_FROM_FROZEN_DIGITIZATION_VALIDATION | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |
| NGC4088 | F_R | f_R | min(max(|Delta_R_onset_sides| / R_HI, sigma_xw/xw), 1) | Delta_R_onset_sides; R_HI; sigma_xw_over_xw | 0.25 | dimensionless | ACCEPTED_FROM_FROZEN_DIGITIZATION_VALIDATION | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |
| NGC4088 | F_Q | f_q | q_warp_measured after residual-blind source review | q_warp_measured | 1 | dimensionless | ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |
| NGC4088 | F_MEM | f_mem | morphological-history warp proxy after residual-blind source review | m_history_warp | 1 | dimensionless | ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |

## Coefficient Obligations

| galaxy | coefficient_id | multiplies_feature | unit | allowed_origin | forbidden_origin | current_value | status | active_coefficient_source | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | B_PA | f_PA | dimensionless | Tau-side geometry derivation or predeclared residual-blind coefficient protocol | vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit | 0.5 | SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | second_order_remainder_half_bound | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |
| NGC4088 | B_R | f_R | dimensionless | Tau-side geometry derivation or predeclared residual-blind coefficient protocol | vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit | 0.5 | SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | second_order_remainder_half_bound | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |
| NGC4088 | B_q | f_q | dimensionless | Tau-side geometry derivation or predeclared residual-blind coefficient protocol | vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit | 0.5 | SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | second_order_remainder_half_bound | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |
| NGC4088 | B_mem | f_mem | dimensionless | Tau-side geometry derivation or predeclared residual-blind coefficient protocol | vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit | 0.5 | SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT | second_order_remainder_half_bound | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | BI1_DIMENSIONLESS_FORM | PASS | epsilon_cross, f_i, and B_i are all dimensionless | preserve dimensionless coefficient rule | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |
| NGC4088 | BI2_FEATURE_NORMALIZATION_DECLARED | PASS | f_PA and f_R are normalized from source observables; f_q and f_mem use accepted q and caveated morphological-history source review if available | preserve source-review provenance | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |
| NGC4088 | BI3_COEFFICIENT_ORIGIN_RESTRICTED | PASS | allowed and forbidden coefficient origins are explicit | derive or freeze coefficient values without endpoint residuals | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |
| NGC4088 | BI4_COEFFICIENT_VALUES_AVAILABLE | PASS | B_PA, B_R, B_q, and B_mem supplied by residual-blind protocol | derive the active protocol coefficients from Tau-side geometry before final physical claims | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |
| NGC4088 | BI5_NUMERIC_BOUND_READY | PASS | accepted q/morphological-history source responses and residual-blind B_i values are available | evaluate numeric epsilon_cross protocol bound | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |
| NGC4088 | BI6_ENDPOINT_BLINDNESS | PASS | rule forbids vobs and endpoint residuals | keep endpoint scoring separate | False | False | s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint |

## Claim Boundary

The feature definitions are dimensionless and residual-blind. Frozen
or sharpened B_i values, when present, are protocol coefficients, not
final Tau-side sharp-amplitude derivations.
