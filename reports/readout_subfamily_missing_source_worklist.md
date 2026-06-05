# Readout-Subfamily Missing-Source Worklist

This worklist is generated from the accepted-manifest audit. It is an
acquisition/review guide only: it does not score rotation endpoints and
does not validate Tau Core.

## Priority Summary

| priority_rank | galaxy | proposed_readout_subfamily | n_open_items | blocker_types |
| --- | --- | --- | --- | --- |
| 1 | NGC4088 | K_warp_history_coupled | 4 | missing_required_observable |
| 2 | NGC5907 | K_projection_dominated | 1 | endpoint_freeze_gate |
| 3 | IC2574 | K_disturbed_outer_tail | 1 | missing_required_observable |
| 4 | UGC05716 | K_disturbed_outer_tail | 3 | blocked_observable;missing_required_observable |
| 5 | NGC4013 | K_true_compact | 3 | missing_required_observable;reclassification_review |
| 6 | NGC7331 | K_thick_regular | 1 | caveat_to_resolve |
| 7 | NGC4183 | K_expdisk_overlay | 1 | missing_required_observable |
| 8 | IC4202 | K_true_compact | 1 | missing_required_observable |
| 9 | UGC12506 | K_expdisk_overlay | 1 | missing_required_observable |

## Open Items

| priority_rank | galaxy | proposed_readout_subfamily | audit_decision | blocker_type | needed_observable_or_review | recommended_source_path | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | NGC4088 | K_warp_history_coupled | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | missing_required_observable | epsilon_cross_numeric_bound | accepted q_warp plus accepted memory/history proxy, then source-bound protocol rerun | readout_subfamily_missing_source_worklist_not_endpoint |
| 1 | NGC4088 | K_warp_history_coupled | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | missing_required_observable | m_history_warp_first_pass | residual-blind interaction/environment/history review | readout_subfamily_missing_source_worklist_not_endpoint |
| 1 | NGC4088 | K_warp_history_coupled | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | missing_required_observable | q_warp_measured_first_pass | independent channel-map review or published warp/asymmetry amplitude | readout_subfamily_missing_source_worklist_not_endpoint |
| 1 | NGC4088 | K_warp_history_coupled | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | missing_required_observable | x_warp_onset_value | HI velocity-field radial PA profile; radial warp-angle profile; channel-map digitization | readout_subfamily_missing_source_worklist_not_endpoint |
| 2 | NGC5907 | K_projection_dominated | ACCEPTED_SUBFAMILY_SOURCE_FIELDS_ENDPOINT_STILL_BLOCKED | endpoint_freeze_gate | frozen endpoint protocol and source-native normalization gate | no new rotation scoring; freeze predeclared endpoint-use rule | readout_subfamily_missing_source_worklist_not_endpoint |
| 3 | IC2574 | K_disturbed_outer_tail | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | missing_required_observable | outer_tail_transition_radius | resolved HI radius/profile map; tail/envelope transition measurement | readout_subfamily_missing_source_worklist_not_endpoint |
| 4 | UGC05716 | K_disturbed_outer_tail | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | blocked_observable | hi_asymmetry_or_tail_measurement | resolved HI asymmetry map or published lopsidedness/tail metric | readout_subfamily_missing_source_worklist_not_endpoint |
| 4 | UGC05716 | K_disturbed_outer_tail | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | missing_required_observable | extended_hi_envelope_present | targeted residual-blind literature/source review | readout_subfamily_missing_source_worklist_not_endpoint |
| 4 | UGC05716 | K_disturbed_outer_tail | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | missing_required_observable | outer_tail_transition_radius | resolved HI radius/profile map; tail/envelope transition measurement | readout_subfamily_missing_source_worklist_not_endpoint |
| 5 | NGC4013 | K_true_compact | RECLASSIFICATION_REVIEW_REQUIRED | missing_required_observable | bulge_core_decomposition | S4G component table or independent bulge/core decomposition | readout_subfamily_missing_source_worklist_not_endpoint |
| 5 | NGC4013 | K_true_compact | RECLASSIFICATION_REVIEW_REQUIRED | missing_required_observable | compact_support_radius | S4G/NED/DustPedia decomposition; compact support radius source | readout_subfamily_missing_source_worklist_not_endpoint |
| 5 | NGC4013 | K_true_compact | RECLASSIFICATION_REVIEW_REQUIRED | reclassification_review | compact_only_overlay_flag | reclassify against disk/warp overlay sources before endpoint use | readout_subfamily_missing_source_worklist_not_endpoint |
| 6 | NGC7331 | K_thick_regular | CAVEATED_ACCEPTED_SOURCE_FIELDS_NOT_ENDPOINT_READY | caveat_to_resolve | possible_outer_warp_caveat | HI/projection review to confirm or reject outer-warp emission | readout_subfamily_missing_source_worklist_not_endpoint |
| 7 | NGC4183 | K_expdisk_overlay | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | missing_required_observable | bar_core_projection_history_overlay | S4G bar/core decomposition plus NED/HI projection-history review | readout_subfamily_missing_source_worklist_not_endpoint |
| 8 | IC4202 | K_true_compact | NO_EXTRACTION_AVAILABLE | missing_required_observable | compact support radius and bulge/core decomposition | S4G/NED/DustPedia decomposition; compact support radius source | readout_subfamily_missing_source_worklist_not_endpoint |
| 9 | UGC12506 | K_expdisk_overlay | NO_EXTRACTION_AVAILABLE | missing_required_observable | bar/core/projection/history overlay source review | S4G/NED/HI source review for bar, core, projection, and history overlays | readout_subfamily_missing_source_worklist_not_endpoint |

## Immediate Next Target

NGC4088 remains the highest-priority case because the targeted warp/history
diagnostic already has a strong shape signal, while accepted subfamily use
is still blocked by source-review and numeric-bound requirements. The next
source task is to promote or reject its first-pass warp onset, q-warp,
memory/history, and epsilon-cross inputs without using the rotation endpoint.
