# NGC4088 q_warp Measurement Protocol

This protocol turns the qualitative q_warp=1 gate into a residual-blind
measurement task. It does not fill q_warp and does not use endpoint
residuals.

## Protocol

| galaxy | protocol_id | definition | allowed_sources | forbidden_inputs | normalization | current_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | QWARP_CHANNEL_MAP_SOURCE_STRENGTH_PROTOCOL | q_warp_measured = clipped_mean_over_target_panels(outer_asymmetry_extent / local_disk_reference_extent) | page76 channel-map ROI; worksheet overlay; page77 PA cross-check; HI morphology maps | vobs; endpoint residuals; best-fit amplitude; endpoint-selected family | dimensionless ratio with q=0 no detected outer warp/asymmetry and q=1 strong source lane | PROTOCOL_READY_MEASUREMENT_RESPONSE_EMPTY | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |

## Measurement Fields

| galaxy | field_id | field_name | description | required | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| NGC4088 | F1_OUTER_ASYMMETRY_EXTENT | outer_asymmetry_extent_px | outer displaced HI ridge or warp/asymmetry extent in panel coordinates | True | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |
| NGC4088 | F2_LOCAL_DISK_REFERENCE_EXTENT | local_disk_reference_extent_px | local inner/ordinary disk reference extent in the same panel | True | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |
| NGC4088 | F3_PANEL_WEIGHT | panel_source_weight | residual-blind panel reliability/source strength weight | True | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |
| NGC4088 | F4_SIDE_LABEL | side_label | approaching/receding or side A/B label used only for source symmetry checks | True | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |
| NGC4088 | F5_REVIEW_FLAG | review_flag | independent-review status and caveat flag | True | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |

## Response Template

| galaxy | response_id | q_warp_measured | q_warp_uncertainty | n_panels_used | n_panel_measurements_required | inner_axis_pa_deg | outer_axis_side_a_pa_deg | outer_axis_side_b_pa_deg | response_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | QWARP_MEASUREMENT_RESPONSE_V1 | None | None | 0 | 23 | 229 | 319 | 229 | MEASUREMENT_EMPTY | False | False | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | Q1_PROTOCOL_DEFINED | PASS | dimensionless q_warp measurement rule is declared | none at protocol-definition level | False | False | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |
| NGC4088 | Q2_SOURCE_IMAGES_AVAILABLE | PASS | page76 ROI, worksheet overlay, and page77 cross-check are already present | none at source-availability level | False | False | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |
| NGC4088 | Q3_PANEL_WORKSHEET_READY | PASS | 23 measurement targets are available | fill q_warp-specific measurement fields | False | False | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |
| NGC4088 | Q4_RESPONSE_FILLED | BLOCKED | q_warp_measured and uncertainty are empty | perform residual-blind source measurement | False | False | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |
| NGC4088 | Q5_INDEPENDENT_REVIEW | BLOCKED | no independent q_warp review exists | independent reviewer must verify measurement | False | False | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |
| NGC4088 | Q6_ENDPOINT_BLINDNESS | PASS | protocol forbids vobs and endpoint residuals | keep endpoint scoring separate | False | False | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |

## Summary

| galaxy | protocol_id | n_measurement_fields | n_panel_measurements_required | n_gates | n_pass | n_blocked | q_warp_status | epsilon_cross_impact | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | QWARP_CHANNEL_MAP_SOURCE_STRENGTH_PROTOCOL | 5 | 23 | 6 | 4 | 2 | QWARP_PROTOCOL_READY_MEASUREMENT_BLOCKED | UNBLOCKS_Q_COMPONENT_AFTER_MEASUREMENT_AND_REVIEW | False | False | s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint |

## Claim Boundary

q_warp remains qualitative until this protocol is measured and
independently reviewed.
