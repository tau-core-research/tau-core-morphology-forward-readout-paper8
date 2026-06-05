# Mixed Overlay Future Protocol Worklist

Status: `MIXED_OVERLAY_FUTURE_PROTOCOL_WORKLIST_COMPLETE_NOT_ENDPOINT`

This worklist turns NGC4013 into a prospective-only template and identifies
future galaxies where the mixed-overlay lane can be tested without using the
template score as validation.

## Summary

| worklist_status | template_galaxy | primary_fresh_target | n_candidates | n_primary_fresh_targets | n_secondary_acquisition_targets | endpoint_scores_allowed | uses_vobs_or_residual_in_selection | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MIXED_OVERLAY_FUTURE_PROTOCOL_WORKLIST_COMPLETE_NOT_ENDPOINT | NGC4013 | NGC4183 | 8 | 1 | 4 | False | False | mixed_overlay_future_protocol_worklist_not_endpoint |

## Worklist

| galaxy | protocol_role | candidate_lane | candidate_readout | priority | source_status | score_status | ready_for_future_scoring | needed_next_action | source_basis | blocking_reason | uses_vobs_or_residual_in_selection | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | TEMPLATE_PROSPECTIVE_ONLY_NOT_VALIDATION | L_mixed_overlay | K_expdisk_warp_vertical_overlay | REFERENCE_TEMPLATE | SOURCE_FREEZE_AND_FORMULA_FREEZE_PASS_CAVEATED | REPLAY_RECORDED_NOT_VALIDATION | False | repeat protocol on future predeclared galaxies | smooth disk carrier + warp/vertical/lag overlay source fields | same galaxy already inspected diagnostically | False | False | mixed_overlay_future_protocol_worklist_not_endpoint |
| NGC4183 | PRIMARY_FRESH_MIXED_OVERLAY_ACQUISITION_TARGET | L_mixed_overlay | K_expdisk_bar_core_projection_history_overlay_review | P0 | CONTEXT_ONLY_NOT_GALAXY_SPECIFIC | NOT_SCORED | False | acquire galaxy-specific bar/core/projection/history overlay observables | WHISP lopsidedness source is method/sample context only | numeric_overlay_activation_missing;context_only_not_galaxy_specific | False | False | mixed_overlay_future_protocol_worklist_not_endpoint |
| NGC0024 | SECONDARY_VERTICAL_OVERLAY_ACQUISITION_TARGET | L_mixed_overlay | K_expdisk_thick_flared_overlay_review | P1 | TO_BE_ACQUIRED_OR_DIRECTLY_MEASURED_RESIDUAL_BLIND | NOT_SCORED | False | acquire direct vertical/thickness/flare/warp/projection source fields | vertical_scale_height_kpc; h_over_Rs; flare_or_warp_radius_kpc; edge_on_thickness_evidence; gas_plane_thickness_or_warp | vertical/projection source observables | False | False | mixed_overlay_future_protocol_worklist_not_endpoint |
| NGC2683 | SECONDARY_VERTICAL_OVERLAY_ACQUISITION_TARGET | L_mixed_overlay | K_expdisk_thick_flared_overlay_review | P1 | TO_BE_ACQUIRED_OR_DIRECTLY_MEASURED_RESIDUAL_BLIND | NOT_SCORED | False | acquire direct vertical/thickness/flare/warp/projection source fields | vertical_scale_height_kpc; h_over_Rs; flare_or_warp_radius_kpc; edge_on_thickness_evidence; gas_plane_thickness_or_warp | vertical/projection source observables | False | False | mixed_overlay_future_protocol_worklist_not_endpoint |
| NGC3726 | SECONDARY_VERTICAL_OVERLAY_ACQUISITION_TARGET | L_mixed_overlay | K_expdisk_thick_flared_overlay_review | P1 | TO_BE_ACQUIRED_OR_DIRECTLY_MEASURED_RESIDUAL_BLIND | NOT_SCORED | False | acquire direct vertical/thickness/flare/warp/projection source fields | vertical_scale_height_kpc; h_over_Rs; flare_or_warp_radius_kpc; edge_on_thickness_evidence; gas_plane_thickness_or_warp | vertical/projection source observables | False | False | mixed_overlay_future_protocol_worklist_not_endpoint |
| NGC3949 | SECONDARY_VERTICAL_OVERLAY_ACQUISITION_TARGET | L_mixed_overlay | K_expdisk_thick_flared_overlay_review | P1 | TO_BE_ACQUIRED_OR_DIRECTLY_MEASURED_RESIDUAL_BLIND | NOT_SCORED | False | acquire direct vertical/thickness/flare/warp/projection source fields | vertical_scale_height_kpc; h_over_Rs; flare_or_warp_radius_kpc; edge_on_thickness_evidence; gas_plane_thickness_or_warp | vertical/projection source observables | False | False | mixed_overlay_future_protocol_worklist_not_endpoint |
| NGC4088 | ADDED_OR_MIXED_WARP_HISTORY_PROTOCOL_BLOCKED | L_added_source_or_L_mixed_overlay | K_expdisk_warp_history_coupled_mixed_review | P1_BLOCKED | BREAKTHROUGH_PROTOCOL_BOUND_READY_NOT_ENDPOINT | NOT_SCORED | False | resolve independent digitization review, physical normalization law, and scale-uniqueness before any mixed formula freeze | x_w=0.282353; q=1; m_history=1; |epsilon_cross|<=0.6875; input_review=INPUT_REVIEW_PACKET_NUMERIC_PROTOCOL_BOUND_READY | INDEPENDENT_DIGITIZATION_REVIEW;PHYSICAL_NORMALIZATION_LAW;POPULATION_GENERALIZATION;BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES | False | False | mixed_overlay_future_protocol_worklist_not_endpoint |
| NGC5907 | NEGATIVE_CONTROL_FOR_ADDED_MIXED_CONFUSION | L_projection_attenuation | K_projection_dominated | CONTROL | FROZEN_PASS_CAVEATED | NOT_SCORED | False | do not use as standalone mixed-overlay population template unless projection-specific | ACCEPTED_SUBFAMILY_SOURCE_FIELDS_ENDPOINT_STILL_BLOCKED | standalone added split-B2 ramp; unbounded added warp-history ramp | False | False | mixed_overlay_future_protocol_worklist_not_endpoint |

## Gates

| gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| MOFPW_G1_TEMPLATE_AVAILABLE | PASS | NGC4013_MIXED_OVERLAY_PROSPECTIVE_REPLAY_RECORDED_NOT_VALIDATION | do not count template as validation | False | mixed_overlay_future_protocol_worklist_not_endpoint |
| MOFPW_G2_PRIMARY_FRESH_TARGET | PASS_CAVEATED | NGC4183 has SPARC scale but needs galaxy-specific overlay observables | source acquisition before any formula freeze | False | mixed_overlay_future_protocol_worklist_not_endpoint |
| MOFPW_G3_SECONDARY_VERTICAL_TARGETS | PASS_CAVEATED | bulk S4G/DustPedia/HI source targets exist | direct source-native observables still missing | False | mixed_overlay_future_protocol_worklist_not_endpoint |
| MOFPW_G4_NO_ENDPOINT_SCORING | PASS | worklist uses only source/gate metadata | separate source acquisition and formula freeze before scoring | False | mixed_overlay_future_protocol_worklist_not_endpoint |

## Interpretation

The next scientifically clean move is not to keep reusing NGC4013. NGC4013
defines the protocol shape. NGC4183 is the primary fresh acquisition target
because it already has a smooth-disk scale but lacks galaxy-specific overlay
activation fields. The secondary targets are vertical/projection acquisition
cases that can broaden the mixed-overlay lane after source-native observables
are filled.

## Claim Boundary

`mixed_overlay_future_protocol_worklist_not_endpoint`
