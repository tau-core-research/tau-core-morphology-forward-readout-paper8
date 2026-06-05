# NGC4088 Epsilon-Cross Source-Bound Protocol

This protocol defines residual-blind source observables that could bound
`epsilon_cross`. It does not fit endpoint residuals and does not yet
produce a numeric bound.

## Bound Protocol

| galaxy | protocol_id | bound_form | allowed_inputs | forbidden_inputs | current_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | EPSILON_CROSS_RESIDUAL_BLIND_SOURCE_BOUND_PROTOCOL | |epsilon_cross| <= B_PA f_PA + B_R f_R + B_q f_q + B_mem f_mem | orientation mismatch; side onset asymmetry; onset uncertainty; source-measured warp amplitude; memory/history proxy | vobs; endpoint residuals; endpoint-selected family or amplitude | BOUND_FORM_DECLARED_NUMERIC_BOUND_BLOCKED | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |

## Source Observables

| galaxy | observable_id | observable_symbol | source_role | current_value | unit | availability_status | source | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | O1_ORIENTATION_MISMATCH | Delta_PA_outer_inner | bounds orientation-strength and onset-carrier cross terms | 90 | deg | AVAILABLE_FIRST_PASS_NOT_INDEPENDENTLY_REVIEWED | NGC4088 channel-map digitization response | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |
| NGC4088 | O2_SIDE_ASYMMETRY | Delta_R_onset_sides | bounds onset-strength asymmetry cross term | 0.4 | arcmin | AVAILABLE_FIRST_PASS_NOT_INDEPENDENTLY_REVIEWED | NGC4088 channel-map digitization response | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |
| NGC4088 | O3_ONSET_UNCERTAINTY_FRACTION | sigma_xw_over_xw | bounds onset-support ambiguity | 0.25 | dimensionless | AVAILABLE_FIRST_PASS_NOT_INDEPENDENTLY_REVIEWED | x_w conversion audit | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |
| NGC4088 | O4_SOURCE_STRENGTH_AMPLITUDE | q_warp_measured | bounds q_warp-strength cross terms | nan | dimensionless | MISSING_QUANTITATIVE_SOURCE_AMPLITUDE | requires source-measured warp/asymmetry amplitude | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |
| NGC4088 | O5_MEMORY_HISTORY_PROXY | m_history_warp | bounds geometry-memory cross term | nan | dimensionless | MISSING_HISTORY_MEMORY_SOURCE_PROXY | requires residual-blind morphology memory/history proxy | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | B1_BOUND_FORM_DECLARED | PASS | a residual-blind symbolic bound form is declared | derive coefficients B_i from Tau-side geometry or predeclare them | False | False | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |
| NGC4088 | B2_ENDPOINT_BLINDNESS | PASS | bound protocol forbids vobs and endpoint residuals | keep endpoint evaluation separate | False | False | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |
| NGC4088 | B3_PARTIAL_SOURCE_OBSERVABLES_AVAILABLE | FORMULA_CONDITIONAL | orientation mismatch, side asymmetry, and onset uncertainty are available from first-pass digitization | independent digitization review | False | False | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |
| NGC4088 | B4_QUANTITATIVE_Q_WARP_AVAILABLE | BLOCKED | q_warp is currently qualitative q_warp=1 | measure quantitative source amplitude from channel maps or HI morphology | False | False | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |
| NGC4088 | B5_MEMORY_PROXY_AVAILABLE | BLOCKED | no NGC4088-specific memory/history source proxy is currently accepted | construct residual-blind memory/history proxy for warp/asymmetry lane | False | False | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |
| NGC4088 | B6_BOUND_COEFFICIENTS_DERIVED | BLOCKED | B_i coefficients are not derived from Tau-side geometry | derive or predeclare coefficient rule before endpoint use | False | False | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |
| NGC4088 | B7_CROSS_TERM_GATE_CONNECTION | PASS | CROSS_TERMS_DECLARED_NOT_SUPPRESSED | use this protocol to move epsilon_cross from symbolic to bounded | False | False | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |

## Summary

| galaxy | protocol_id | n_observables | n_available_observables | n_missing_observables | n_gates | n_pass | n_formula_conditional | n_blocked | bound_status | epsilon_cross_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | EPSILON_CROSS_RESIDUAL_BLIND_SOURCE_BOUND_PROTOCOL | 5 | 3 | 2 | 7 | 3 | 1 | 3 | SOURCE_BOUND_PROTOCOL_PARTIAL_NUMERIC_BOUND_BLOCKED | SYMBOLIC_UNBOUNDED_UNTIL_Q_AND_MEMORY_READY | False | False | s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint |

## Claim Boundary

`epsilon_cross` remains symbolic until quantitative q_warp, memory/history
proxy, and bound coefficients are residual-blindly supplied.
