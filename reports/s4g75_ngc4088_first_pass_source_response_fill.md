# NGC4088 First-Pass Source Response Fill

This artifact fills provisional q_warp and morphological-history source values
from the already frozen channel-map digitization response. It does not
authorize a numeric epsilon_cross bound.

## Summary

| galaxy | fill_id | q_warp_measured | m_history_warp | n_memory_components_measured | n_gates | n_pass | n_formula_conditional | n_blocked | fill_status | accepted_for_numeric_bound | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_FIRST_PASS_QWARP_MEMORY_SOURCE_RESPONSE_FILL | 1 | 1 | 3 | 4 | 1 | 2 | 1 | FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED | False | False | False | s4g75_ngc4088_first_pass_source_response_fill_not_endpoint |

## q_warp Response

| galaxy | response_id | q_warp_measured | q_warp_uncertainty | n_panels_used | n_panel_measurements_required | inner_axis_pa_deg | outer_axis_side_a_pa_deg | outer_axis_side_b_pa_deg | source_rule | response_status | accepted_for_numeric_bound | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | QWARP_FIRST_PASS_SOURCE_RESPONSE_V1 | 1 | 0.25 | 23 | 23 | 229 | 319 | 229 | clipped(max_outer_inner_PA_mismatch / 90deg) | FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED | False | False | False | s4g75_ngc4088_first_pass_source_response_fill_not_endpoint |

## Memory Components

| galaxy | component_id | component_symbol | component_value | evidence | component_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | H1_WARP_PERSISTENCE | h_warp_persist | 1 | warp/asymmetry visible across the frozen channel-map panel sequence | FIRST_PASS_FILLED_REVIEW_REQUIRED | False | False | s4g75_ngc4088_first_pass_source_response_fill_not_endpoint |
| NGC4088 | H2_HI_LOPSIDEDNESS | h_lopsided_hi | 1 | side A outer ridge differs strongly from the inner axis while side B remains aligned | FIRST_PASS_FILLED_REVIEW_REQUIRED | False | False | s4g75_ngc4088_first_pass_source_response_fill_not_endpoint |
| NGC4088 | H3_OUTER_DISK_ASYMMETRY | h_outer_asym | 1 | outer ridge PA and onset side asymmetry are present in source digitization | FIRST_PASS_FILLED_REVIEW_REQUIRED | False | False | s4g75_ngc4088_first_pass_source_response_fill_not_endpoint |
| NGC4088 | H4_INTERACTION_CONTEXT | h_env | nan | environment/interaction context not filled from source registry in this pass | SOURCE_REVIEW_REQUIRED | False | False | s4g75_ngc4088_first_pass_source_response_fill_not_endpoint |

## Memory Response

| galaxy | response_id | m_history_warp | m_history_uncertainty | n_components_measured | n_components_required | source_ready_whisp | response_status | accepted_for_numeric_bound | uses_rotation_inferred_proxy | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_MEMORY_HISTORY_FIRST_PASS_RESPONSE_V1 | 1 | 0.25 | 3 | 4 | True | PARTIAL_FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED | False | False | False | False | s4g75_ngc4088_first_pass_source_response_fill_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | FP1_Q_SOURCE_FILL_AVAILABLE | FORMULA_CONDITIONAL | q_warp filled from source PA mismatch rule | independent source review before accepted numeric bound | False | False | s4g75_ngc4088_first_pass_source_response_fill_not_endpoint |
| NGC4088 | FP2_MEMORY_SOURCE_FILL_AVAILABLE | FORMULA_CONDITIONAL | morphological-history proxy partially filled from source morphology components | fill environment context and independently review components | False | False | s4g75_ngc4088_first_pass_source_response_fill_not_endpoint |
| NGC4088 | FP3_ENDPOINT_BLINDNESS | PASS | fills use channel-map/source morphology and forbid endpoint residuals | keep endpoint scoring separate | False | False | s4g75_ngc4088_first_pass_source_response_fill_not_endpoint |
| NGC4088 | FP4_NUMERIC_BOUND_AUTHORIZATION | BLOCKED | first-pass fills are not accepted inputs | accepted numeric bound requires independent review and B_i values | False | False | s4g75_ngc4088_first_pass_source_response_fill_not_endpoint |

## Claim Boundary

These are first-pass source fills only. They are useful for checking the
algebraic pipeline, but accepted numeric bounds still require independent
review and B_i coefficient values.
