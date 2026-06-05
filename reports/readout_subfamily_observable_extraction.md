# Readout-Subfamily Observable Extraction

This report extracts residual-blind observables from cached literature
sources. It records source fields only: no endpoint residual, required-S_tau
diagnostic, or best-fit readout family is used to promote a label.

## Acceptance Summary

| galaxy | proposed_readout_subfamily | n_extracted | n_source_accepted | n_blocked | n_caveat |
| --- | --- | --- | --- | --- | --- |
| IC2574 | K_disturbed_outer_tail | 6 | 5 | 1 | 0 |
| NGC4013 | K_true_compact | 4 | 3 | 0 | 1 |
| NGC4088 | K_warp_history_coupled | 7 | 1 | 2 | 0 |
| NGC4183 | K_expdisk_overlay | 1 | 0 | 0 | 1 |
| NGC5907 | K_projection_dominated | 5 | 5 | 0 | 0 |
| NGC7331 | K_thick_regular | 4 | 3 | 0 | 1 |
| UGC05716 | K_disturbed_outer_tail | 3 | 2 | 1 | 0 |

## Status Summary

| galaxy | extraction_status | n_observables |
| --- | --- | --- |
| IC2574 | ACCEPTED_CONTEXT_SOURCE_FIELD | 3 |
| IC2574 | ACCEPTED_NUMERIC_SOURCE_FIELD | 2 |
| IC2574 | BLOCKED_NEEDS_MEASUREMENT | 1 |
| NGC4013 | ACCEPTED_CONTEXT_SOURCE_FIELD | 1 |
| NGC4013 | ACCEPTED_NUMERIC_SOURCE_FIELD | 2 |
| NGC4013 | RECLASSIFICATION_PRESSURE_SOURCE_FIELD | 1 |
| NGC4088 | ACCEPTED_NUMERIC_SOURCE_FIELD | 1 |
| NGC4088 | BLOCKED_NEEDS_MEASUREMENT | 2 |
| NGC4088 | PRELIMINARY_SOURCE_FIELD_REVIEW_REQUIRED | 4 |
| NGC4183 | CONTEXT_ONLY_NOT_GALAXY_SPECIFIC | 1 |
| NGC5907 | ACCEPTED_CONTEXT_SOURCE_FIELD | 2 |
| NGC5907 | ACCEPTED_NUMERIC_SOURCE_FIELD | 3 |
| NGC7331 | ACCEPTED_NUMERIC_SOURCE_FIELD | 3 |
| NGC7331 | CAVEAT_CONTEXT_SOURCE_FIELD | 1 |
| UGC05716 | ACCEPTED_CONTEXT_SOURCE_FIELD | 1 |
| UGC05716 | ACCEPTED_NUMERIC_SOURCE_FIELD | 1 |
| UGC05716 | BLOCKED_NEEDS_MEASUREMENT | 1 |

## Extracted Observable Ledger

| galaxy | proposed_readout_subfamily | evidence_id | observable_name | observable_value | observable_unit | source_line_refs | extraction_status | acceptance_use | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IC2574 | K_disturbed_outer_tail | hi_asymmetry_map | extended_hi_envelope_present | true | boolean | 20-29;392-395;544-545 | ACCEPTED_CONTEXT_SOURCE_FIELD | supports disturbed-gas/envelope review; not a complete tail-transition radius | source_extraction_not_endpoint_label_acceptance |
| IC2574 | K_disturbed_outer_tail | outer_tail_transition | hi_cloud_connection_or_tail_context | HIJASS_J1021+68_clouds_connected_to_IC2574_envelope | categorical | 20-29;1017-1027 | ACCEPTED_CONTEXT_SOURCE_FIELD | supports morphology-history/tail context; exact transition radius still missing | source_extraction_not_endpoint_label_acceptance |
| IC2574 | K_disturbed_outer_tail | outer_tail_transition | outer_tail_transition_radius | not_reported_in_extracted_text | kpc | 20-29 | BLOCKED_NEEDS_MEASUREMENT | needs map/profile extraction before numeric kernel use | source_extraction_not_endpoint_label_acceptance |
| IC2574 | K_disturbed_outer_tail | environment_history | hi_holes_shells_count | 48 | count | 17-29 | ACCEPTED_NUMERIC_SOURCE_FIELD | supports morphology-memory/disturbed-ISM source layer | source_extraction_not_endpoint_label_acceptance |
| IC2574 | K_disturbed_outer_tail | environment_history | hi_layer_scaleheight | 350 | pc | 47-49 | ACCEPTED_NUMERIC_SOURCE_FIELD | supports disturbed/thick gas context, not by itself a tail label | source_extraction_not_endpoint_label_acceptance |
| IC2574 | K_disturbed_outer_tail | outer_tail_transition | sided_hole_age_asymmetry | receding_and_approaching_age_distributions_differ | categorical | html-meta-description | ACCEPTED_CONTEXT_SOURCE_FIELD | supports asymmetry context; no radius extracted | source_extraction_not_endpoint_label_acceptance |
| NGC4013 | K_true_compact | disk_overlay_check | compact_only_overlay_flag | warp_flare_disk_halo_overlay_present | categorical | 13-23;126-128;170-172 | RECLASSIFICATION_PRESSURE_SOURCE_FIELD | warns that K_true_compact needs overlay or rejection before endpoint use | source_extraction_not_endpoint_label_acceptance |
| NGC4013 | K_true_compact | disk_overlay_check | line_of_sight_warp_onset | 10 | kpc | 406-409 | ACCEPTED_NUMERIC_SOURCE_FIELD | supports disk/warp overlay review | source_extraction_not_endpoint_label_acceptance |
| NGC4013 | K_true_compact | disk_overlay_check | final_hi_scaleheight_central | 210 | pc | 430-439 | ACCEPTED_NUMERIC_SOURCE_FIELD | supports thin/flaring disk overlay review | source_extraction_not_endpoint_label_acceptance |
| NGC4013 | K_true_compact | disk_overlay_check | rotational_lag_profile | lag_shallows_radially_from_minus35_to_zero_near_R25 | km/s/kpc profile | 13-20;474-480;527-528 | ACCEPTED_CONTEXT_SOURCE_FIELD | supports disk-halo/vertical-flow overlay review | source_extraction_not_endpoint_label_acceptance |
| NGC5907 | K_projection_dominated | projection_geometry | optical_warp_radial_range | 13.3-24.0 | kpc | 9-23 | ACCEPTED_NUMERIC_SOURCE_FIELD | supports projection/warp geometry review | source_extraction_not_endpoint_label_acceptance |
| NGC5907 | K_projection_dominated | projection_geometry | optical_warp_max_displacement | 1.7 | kpc | 15-23 | ACCEPTED_NUMERIC_SOURCE_FIELD | supports projection/warp amplitude review | source_extraction_not_endpoint_label_acceptance |
| NGC5907 | K_projection_dominated | projection_geometry | disk_truncation_scale_lengths | main_disk_4.92_kpc;corrected_4.70_kpc;outer_truncated_1.23_kpc | kpc | 9-15 | ACCEPTED_NUMERIC_SOURCE_FIELD | supports projection/truncation review | source_extraction_not_endpoint_label_acceptance |
| NGC5907 | K_projection_dominated | velocity_field_sanity | interaction_warp_context | warp_and_dwarf_interaction_context_present | categorical | title/abstract source | ACCEPTED_CONTEXT_SOURCE_FIELD | supports projection/history review | source_extraction_not_endpoint_label_acceptance |
| NGC5907 | K_projection_dominated | vertical_or_warp_source | edge_on_vertical_structure_source | CO_HI_Spitzer_vertical_structure_study_present | categorical | 14-23;52-59 | ACCEPTED_CONTEXT_SOURCE_FIELD | supports vertical/projection sanity; exact extracted h/Rs still pending | source_extraction_not_endpoint_label_acceptance |
| NGC7331 | K_thick_regular | vertical_scale_or_thickness | molecular_scaleheight_range | 100-200 | pc | 16-24;715-721;984-986 | ACCEPTED_NUMERIC_SOURCE_FIELD | supports K_thick_regular vertical-scale evidence | source_extraction_not_endpoint_label_acceptance |
| NGC7331 | K_thick_regular | vertical_scale_or_thickness | edge_on_projected_hwhm | 500 | pc | 23-26;955-981;1033-1037 | ACCEPTED_NUMERIC_SOURCE_FIELD | supports K_thick_regular observable thickness | source_extraction_not_endpoint_label_acceptance |
| NGC7331 | K_thick_regular | projection_safety | inclination_review_range | 72-80;adopted_76 | deg | 108-110;864-867;960-965;1028-1031 | ACCEPTED_NUMERIC_SOURCE_FIELD | supports projection-safety context for NGC7331 | source_extraction_not_endpoint_label_acceptance |
| NGC7331 | K_thick_regular | low_warp_asymmetry | possible_outer_warp_caveat | possible_extra_outer_emission_from_warp | categorical | 960-968 | CAVEAT_CONTEXT_SOURCE_FIELD | prevents unconditional low-warp acceptance without HI/projection review | source_extraction_not_endpoint_label_acceptance |
| NGC4183 | K_expdisk_overlay | bar_core_projection_history_overlay | whisp_lopsidedness_context | whisp_kinematic_lopsidedness_method_context | categorical | 23-36;103-128;907-923 | CONTEXT_ONLY_NOT_GALAXY_SPECIFIC | needs primary table/galaxy-specific extraction before subfamily acceptance | source_extraction_not_endpoint_label_acceptance |
| NGC4088 | K_warp_history_coupled | warp_onset_asymmetry | orientation_mismatch_first_pass | 90 | deg | O1_ORIENTATION_MISMATCH | PRELIMINARY_SOURCE_FIELD_REVIEW_REQUIRED | supports warp/history review only; independent source review still required before numeric bound use | source_extraction_not_endpoint_label_acceptance |
| NGC4088 | K_warp_history_coupled | warp_onset_asymmetry | side_asymmetry_first_pass | 0.40 | arcmin | O2_SIDE_ASYMMETRY | PRELIMINARY_SOURCE_FIELD_REVIEW_REQUIRED | supports asymmetry review only; independent source review still required before numeric bound use | source_extraction_not_endpoint_label_acceptance |
| NGC4088 | K_warp_history_coupled | warp_onset_asymmetry | x_warp_onset_value | not_extracted | dimensionless_RHI_fraction | WARP_PRESENT_ONSET_NOT_EXTRACTED | BLOCKED_NEEDS_MEASUREMENT | requires radial PA profile, radial warp-angle profile, or channel-map digitization before accepted subfamily use | source_extraction_not_endpoint_label_acceptance |
| NGC4088 | K_warp_history_coupled | hi_disturbance | q_warp_measured_first_pass | 1.0 | dimensionless | QWARP_FIRST_PASS_SOURCE_RESPONSE_V1 | PRELIMINARY_SOURCE_FIELD_REVIEW_REQUIRED | cannot be used as an accepted numeric bound until independently reviewed | source_extraction_not_endpoint_label_acceptance |
| NGC4088 | K_warp_history_coupled | interaction_history | h4_interaction_context | 1.0 | dimensionless | H4_INTERACTION_CONTEXT_ACCEPTED_SOURCE_REVIEWED | ACCEPTED_NUMERIC_SOURCE_FIELD | supports interaction/history context for K_warp_history_coupled, but does not by itself accept the subfamily | source_extraction_not_endpoint_label_acceptance |
| NGC4088 | K_warp_history_coupled | interaction_history | m_history_warp_first_pass | 1.0 | dimensionless | PARTIAL_FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED | PRELIMINARY_SOURCE_FIELD_REVIEW_REQUIRED | supports memory/history review only; not accepted for numeric endpoint or bound use | source_extraction_not_endpoint_label_acceptance |
| NGC4088 | K_warp_history_coupled | epsilon_cross_bound | epsilon_cross_numeric_bound | blocked_until_q_and_memory_ready | dimensionless | SYMBOLIC_UNBOUNDED_UNTIL_Q_AND_MEMORY_READY | BLOCKED_NEEDS_MEASUREMENT | blocks endpoint-safe epsilon_cross use for K_warp_history_coupled | source_extraction_not_endpoint_label_acceptance |
| UGC05716 | K_disturbed_outer_tail | hi_asymmetry_map | hi_rotation_context | rotation_dominated_HI_velocity_field | categorical | 634-659 | ACCEPTED_CONTEXT_SOURCE_FIELD | supports HI source availability; not a disturbed-tail acceptance | source_extraction_not_endpoint_label_acceptance |
| UGC05716 | K_disturbed_outer_tail | hi_asymmetry_map | ugc05716_kinematic_inclination | 57 | deg | 640-659 | ACCEPTED_NUMERIC_SOURCE_FIELD | supports projection context; not HI asymmetry | source_extraction_not_endpoint_label_acceptance |
| UGC05716 | K_disturbed_outer_tail | hi_asymmetry_map | hi_asymmetry_or_tail_measurement | not_extracted | categorical | 634-659 | BLOCKED_NEEDS_MEASUREMENT | needs HI map/asymmetry extraction before K_disturbed_outer_tail acceptance | source_extraction_not_endpoint_label_acceptance |

## Remaining Blockers

- IC2574 still lacks a numeric outer-tail transition radius.
- UGC05716 has HI rotation/projection context but no extracted HI asymmetry or tail measurement.
- NGC4183 currently has WHISP-method context, not a direct galaxy-specific overlay measurement.
- NGC7331 has vertical-scale support, but low-warp acceptance remains caveated by possible outer-warp emission.
- NGC4013 source evidence pressures the current compact-only subfamily toward an overlay/warp review.
- NGC4088 has residual-blind first-pass warp/history fields, but x_warp, q_warp, memory/history, and epsilon_cross still need independent promotion before subfamily acceptance.
