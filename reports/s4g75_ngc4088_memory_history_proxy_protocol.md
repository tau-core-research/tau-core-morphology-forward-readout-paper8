# NGC4088 Morphological-History Proxy Protocol

This protocol defines a residual-blind morphological-history proxy
lane for NGC4088 warp/asymmetry. It explicitly excludes the generic
rotation-inferred proxy. In this context, memory means only
morphology-carried source history.

## Protocol

| galaxy | protocol_id | proxy_definition | allowed_sources | forbidden_inputs | current_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_WARP_MEMORY_HISTORY_SOURCE_PROXY_PROTOCOL | m_history_warp = weighted_source_score(warp_persistence, HI_lopsidedness, outer_disk_asymmetry, interaction_context) | WHISP/HI morphology; channel-map persistence; outer-disk asymmetry; residual-blind environment notes | vobs; rotation residuals; rotation-inferred family; endpoint-selected model | PROTOCOL_READY_RESPONSE_EMPTY | s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint |

## Components

| galaxy | component_id | component_symbol | description | current_value | availability_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | H1_WARP_PERSISTENCE | h_warp_persist | warp/asymmetry appears across multiple adjacent channel-map panels or HI contours | None | MEASUREMENT_REQUIRED | s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint |
| NGC4088 | H2_HI_LOPSIDEDNESS | h_lopsided_hi | side-to-side HI morphology imbalance independent of rotation residuals | None | MEASUREMENT_REQUIRED | s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint |
| NGC4088 | H3_OUTER_DISK_ASYMMETRY | h_outer_asym | outer-disk non-axisymmetric asymmetry visible in source morphology | None | MEASUREMENT_REQUIRED | s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint |
| NGC4088 | H4_INTERACTION_CONTEXT | h_env | residual-blind environmental or interaction context from literature/source registry | None | SOURCE_REVIEW_REQUIRED | s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint |

## Response Template

| galaxy | response_id | m_history_warp | m_history_uncertainty | n_components_measured | n_components_required | source_ready_whisp | response_status | uses_rotation_inferred_proxy | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_MEMORY_HISTORY_PROXY_RESPONSE_V1 | None | None | 0 | 4 | True | MEASUREMENT_EMPTY | False | False | False | s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | H1_PROTOCOL_DEFINED | PASS | morphological-history proxy components are declared | none at protocol-definition level | False | False | s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint |
| NGC4088 | H2_SOURCE_LANE_AVAILABLE | PASS | WHISP warp/asymmetry source lane is available | none at source-lane level | False | False | s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint |
| NGC4088 | H3_INVERSE_PROXY_EXCLUDED | PASS | protocol forbids rotation-inferred family and endpoint residuals | keep generic inverse morphology-history proxy separate | False | False | s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint |
| NGC4088 | H4_COMPONENT_MEASUREMENTS_FILLED | BLOCKED | m_history components are empty | perform residual-blind source review/measurement | False | False | s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint |
| NGC4088 | H5_INDEPENDENT_REVIEW | BLOCKED | no independent morphological-history review exists | independent reviewer must verify m_history_warp | False | False | s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint |
| NGC4088 | H6_EPSILON_BOUND_CONNECTION | FORMULA_CONDITIONAL | m_history_warp would supply the B_mem f_mem term in the epsilon_cross bound | derive/predeclare B_mem coefficient | False | False | s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint |

## Summary

| galaxy | protocol_id | n_components | n_components_measured | source_ready_whisp | n_gates | n_pass | n_formula_conditional | n_blocked | memory_proxy_status | epsilon_cross_impact | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_WARP_MEMORY_HISTORY_SOURCE_PROXY_PROTOCOL | 4 | 0 | True | 6 | 3 | 1 | 2 | MEMORY_PROTOCOL_READY_MEASUREMENT_BLOCKED | UNBLOCKS_MEMORY_COMPONENT_AFTER_MEASUREMENT_AND_REVIEW | False | False | s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint |

## Claim Boundary

m_history_warp remains empty until residual-blind source measurement and
independent review are completed.
