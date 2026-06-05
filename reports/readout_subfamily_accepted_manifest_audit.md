# Readout-Subfamily Accepted-Manifest Audit

This audit decides which extracted residual-blind source fields are strong
enough for accepted-manifest use. It does not score endpoints and does not
validate Tau Core.

## Decision Summary

| audit_decision | n_galaxies | galaxies | n_promoted |
| --- | --- | --- | --- |
| ACCEPTED_SUBFAMILY_SOURCE_FIELDS_ENDPOINT_STILL_BLOCKED | 1 | NGC5907 | 1 |
| BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | 4 | IC2574;NGC4088;NGC4183;UGC05716 | 0 |
| CAVEATED_ACCEPTED_SOURCE_FIELDS_NOT_ENDPOINT_READY | 1 | NGC7331 | 0 |
| NO_EXTRACTION_AVAILABLE | 2 | IC4202;UGC12506 | 0 |
| RECLASSIFICATION_REVIEW_REQUIRED | 1 | NGC4013 | 0 |

## Galaxy Decisions

| galaxy | proposed_readout_subfamily | audit_decision | accepted_subfamily_label_promoted | accepted_observables | missing_required_observables | caveat_observables | reclassification_pressure_observables | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IC2574 | K_disturbed_outer_tail | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | False | extended_hi_envelope_present;hi_cloud_connection_or_tail_context;hi_holes_shells_count;hi_layer_scaleheight;sided_hole_age_asymmetry | outer_tail_transition_radius |  |  | readout_subfamily_accepted_manifest_audit_not_endpoint |
| IC4202 | K_true_compact | NO_EXTRACTION_AVAILABLE | False |  | compact support radius and bulge/core decomposition |  |  | readout_subfamily_accepted_manifest_audit_not_endpoint |
| NGC4013 | K_true_compact | RECLASSIFICATION_REVIEW_REQUIRED | False | final_hi_scaleheight_central;line_of_sight_warp_onset;rotational_lag_profile | bulge_core_decomposition;compact_support_radius |  | compact_only_overlay_flag | readout_subfamily_accepted_manifest_audit_not_endpoint |
| NGC4088 | K_warp_history_coupled | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | False | h4_interaction_context | epsilon_cross_numeric_bound;m_history_warp_first_pass;q_warp_measured_first_pass;x_warp_onset_value |  |  | readout_subfamily_accepted_manifest_audit_not_endpoint |
| NGC4183 | K_expdisk_overlay | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | False |  | bar_core_projection_history_overlay |  |  | readout_subfamily_accepted_manifest_audit_not_endpoint |
| NGC5907 | K_projection_dominated | ACCEPTED_SUBFAMILY_SOURCE_FIELDS_ENDPOINT_STILL_BLOCKED | True | disk_truncation_scale_lengths;edge_on_vertical_structure_source;interaction_warp_context;optical_warp_max_displacement;optical_warp_radial_range |  |  |  | readout_subfamily_accepted_manifest_audit_not_endpoint |
| NGC7331 | K_thick_regular | CAVEATED_ACCEPTED_SOURCE_FIELDS_NOT_ENDPOINT_READY | False | edge_on_projected_hwhm;inclination_review_range;molecular_scaleheight_range |  | possible_outer_warp_caveat |  | readout_subfamily_accepted_manifest_audit_not_endpoint |
| UGC05716 | K_disturbed_outer_tail | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | False | hi_rotation_context;ugc05716_kinematic_inclination | extended_hi_envelope_present;outer_tail_transition_radius |  |  | readout_subfamily_accepted_manifest_audit_not_endpoint |
| UGC12506 | K_expdisk_overlay | NO_EXTRACTION_AVAILABLE | False |  | bar/core/projection/history overlay source review |  |  | readout_subfamily_accepted_manifest_audit_not_endpoint |

## Claim Boundary

Accepted source fields are not endpoint validation. A promoted subfamily
label in this audit only means that the required residual-blind source
observables for that subfamily are present in the cached literature layer.
Endpoint scoring remains blocked.
