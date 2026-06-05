# Readout-Subfamily Source Evidence Matrix

This matrix audits which source observables are already present for the
first-pass readout-subfamily proposals and which source families must be
queried next. It does not score endpoints or accept subfamily labels.

## By Galaxy

| galaxy | proposed_readout_subfamily | n_evidence_items | n_accepted_ready | n_source_context_ready | n_proxy_only | n_missing_or_review | subfamily_acceptance_status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IC2574 | K_disturbed_outer_tail | 4 | 0 | 1 | 0 | 3 | SOURCE_ACQUISITION_REQUIRED | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| IC4202 | K_true_compact | 3 | 0 | 0 | 2 | 1 | SOURCE_ACQUISITION_REQUIRED | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC4013 | K_true_compact | 3 | 0 | 0 | 2 | 1 | SOURCE_ACQUISITION_REQUIRED | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC4088 | K_warp_history_coupled | 4 | 0 | 4 | 0 | 0 | SOURCE_ACQUISITION_REQUIRED | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC4183 | K_expdisk_overlay | 3 | 1 | 0 | 0 | 2 | SOURCE_ACQUISITION_REQUIRED | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC5907 | K_projection_dominated | 3 | 0 | 0 | 2 | 1 | SOURCE_ACQUISITION_REQUIRED | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC7331 | K_thick_regular | 3 | 0 | 1 | 1 | 1 | SOURCE_ACQUISITION_REQUIRED | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| UGC05716 | K_disturbed_outer_tail | 4 | 0 | 1 | 0 | 3 | SOURCE_ACQUISITION_REQUIRED | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| UGC12506 | K_expdisk_overlay | 3 | 0 | 0 | 0 | 3 | SOURCE_ACQUISITION_REQUIRED | False | readout_subfamily_source_evidence_matrix_not_endpoint |

## Evidence Status Summary

| proposed_readout_subfamily | evidence_status | n_items | n_galaxies |
| --- | --- | --- | --- |
| K_disturbed_outer_tail | MISSING_OR_REVIEW_REQUIRED | 6 | 2 |
| K_disturbed_outer_tail | SOURCE_READY_CONTEXT_ONLY | 2 | 2 |
| K_expdisk_overlay | ACCEPTED_FIELD_READY | 1 | 1 |
| K_expdisk_overlay | MISSING | 1 | 1 |
| K_expdisk_overlay | MISSING_OR_REVIEW_REQUIRED | 4 | 2 |
| K_projection_dominated | MISSING_OR_REVIEW_REQUIRED | 1 | 1 |
| K_projection_dominated | PROXY_SUPPORT_ONLY | 2 | 1 |
| K_thick_regular | MISSING_OR_REVIEW_REQUIRED | 1 | 1 |
| K_thick_regular | PROXY_SUPPORT_ONLY | 1 | 1 |
| K_thick_regular | SOURCE_READY_CONTEXT_ONLY | 1 | 1 |
| K_true_compact | MISSING_OR_REVIEW_REQUIRED | 2 | 2 |
| K_true_compact | PROXY_SUPPORT_ONLY | 4 | 2 |
| K_warp_history_coupled | SOURCE_BOUND_PARTIAL | 3 | 1 |
| K_warp_history_coupled | SOURCE_BOUND_READY_FOR_DIAGNOSTIC | 1 | 1 |

## Acquisition / Review Priorities

| galaxy | proposed_readout_subfamily | evidence_id | preferred_source_family | evidence_status | next_action |
| --- | --- | --- | --- | --- | --- |
| IC2574 | K_disturbed_outer_tail | hi_asymmetry_map | HI surveys / THINGS / LITTLE THINGS / WHISP / literature | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |
| IC2574 | K_disturbed_outer_tail | outer_tail_transition | HI profile or deep optical/IR outer disk | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |
| IC2574 | K_disturbed_outer_tail | environment_history | NED/SIMBAD/literature | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |
| IC4202 | K_true_compact | compact_support_radius | S4G/NED/SIMBAD/decomposition | PROXY_SUPPORT_ONLY | extract compact support radius from decomposition/literature |
| IC4202 | K_true_compact | bulge_core_decomposition | S4G Pipeline4 or literature | PROXY_SUPPORT_ONLY | promote with S4G/literature component evidence |
| IC4202 | K_true_compact | disk_overlay_check | S4G/SPARC/literature | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |
| NGC4013 | K_true_compact | compact_support_radius | S4G/NED/SIMBAD/decomposition | PROXY_SUPPORT_ONLY | extract compact support radius from decomposition/literature |
| NGC4013 | K_true_compact | bulge_core_decomposition | S4G Pipeline4 or literature | PROXY_SUPPORT_ONLY | promote with S4G/literature component evidence |
| NGC4013 | K_true_compact | disk_overlay_check | S4G/SPARC/literature | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |
| NGC4183 | K_expdisk_overlay | bar_core_projection_history_overlay | S4G/NED/SIMBAD/HI/projection review | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |
| NGC4183 | K_expdisk_overlay | clean_disk_rejection_reason | source review | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |
| NGC5907 | K_projection_dominated | projection_geometry | SPARC/S4G/dust lane/velocity field | PROXY_SUPPORT_ONLY | needs residual-blind projection review or velocity field |
| NGC5907 | K_projection_dominated | velocity_field_sanity | HI/PHANGS/literature | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |
| NGC5907 | K_projection_dominated | vertical_or_warp_source | S4G/HI/literature | PROXY_SUPPORT_ONLY | promote with direct vertical/flare/warp source |
| NGC7331 | K_thick_regular | vertical_scale_or_thickness | edge-on morphology/S4G/literature | PROXY_SUPPORT_ONLY | promote with direct vertical/flare/warp source |
| NGC7331 | K_thick_regular | low_warp_asymmetry | HI/projection review | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |
| UGC05716 | K_disturbed_outer_tail | hi_asymmetry_map | HI surveys / THINGS / LITTLE THINGS / WHISP / literature | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |
| UGC05716 | K_disturbed_outer_tail | outer_tail_transition | HI profile or deep optical/IR outer disk | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |
| UGC05716 | K_disturbed_outer_tail | environment_history | NED/SIMBAD/literature | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |
| UGC12506 | K_expdisk_overlay | disk_scale | S4G/SPARC | MISSING | query S4G/NED/decomposition |
| UGC12506 | K_expdisk_overlay | bar_core_projection_history_overlay | S4G/NED/SIMBAD/HI/projection review | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |
| UGC12506 | K_expdisk_overlay | clean_disk_rejection_reason | source review | MISSING_OR_REVIEW_REQUIRED | query/review listed source family before endpoint use |

## Full Evidence Matrix

| galaxy | parent_family | proposed_readout_subfamily | evidence_id | target_field | preferred_source_family | evidence_status | current_evidence | next_action | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IC2574 | K_scale_tail_spiral | K_disturbed_outer_tail | hi_radius_mass | MHI_1e9Msun;RHI_kpc | SPARC master table | SOURCE_READY_CONTEXT_ONLY | SPARC HI mass/radius present | needs resolved HI asymmetry/profile for subfamily acceptance | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| IC2574 | K_scale_tail_spiral | K_disturbed_outer_tail | hi_asymmetry_map | HI asymmetry or tail map | HI surveys / THINGS / LITTLE THINGS / WHISP / literature | MISSING_OR_REVIEW_REQUIRED | hi_asymmetry_map requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| IC2574 | K_scale_tail_spiral | K_disturbed_outer_tail | outer_tail_transition | tail inner/cutoff radius | HI profile or deep optical/IR outer disk | MISSING_OR_REVIEW_REQUIRED | outer_tail_transition requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| IC2574 | K_scale_tail_spiral | K_disturbed_outer_tail | environment_history | interaction or companion evidence | NED/SIMBAD/literature | MISSING_OR_REVIEW_REQUIRED | environment_history requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| IC4202 | K_compact_finite | K_true_compact | compact_support_radius | compact support radius or bulge/core scale | S4G/NED/SIMBAD/decomposition | PROXY_SUPPORT_ONLY | bulge/core proxy present | extract compact support radius from decomposition/literature | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| IC4202 | K_compact_finite | K_true_compact | bulge_core_decomposition | B/N/component evidence | S4G Pipeline4 or literature | PROXY_SUPPORT_ONLY | bulge/core proxy present from manifest | promote with S4G/literature component evidence | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| IC4202 | K_compact_finite | K_true_compact | disk_overlay_check | extended disk influence check | S4G/SPARC/literature | MISSING_OR_REVIEW_REQUIRED | disk_overlay_check requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC4013 | K_compact_finite | K_true_compact | compact_support_radius | compact support radius or bulge/core scale | S4G/NED/SIMBAD/decomposition | PROXY_SUPPORT_ONLY | bulge/core proxy present | extract compact support radius from decomposition/literature | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC4013 | K_compact_finite | K_true_compact | bulge_core_decomposition | B/N/component evidence | S4G Pipeline4 or literature | PROXY_SUPPORT_ONLY | bulge/core proxy present from manifest | promote with S4G/literature component evidence | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC4013 | K_compact_finite | K_true_compact | disk_overlay_check | extended disk influence check | S4G/SPARC/literature | MISSING_OR_REVIEW_REQUIRED | disk_overlay_check requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC4088 | K_thick_flared | K_warp_history_coupled | warp_onset | warp onset radius | HI velocity field / outer disk review | SOURCE_BOUND_PARTIAL | NGC4088 targeted warp/history protocol exists | accept warp_onset from independent HI/literature review | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC4088 | K_thick_flared | K_warp_history_coupled | warp_asymmetry | warp or lopsided asymmetry | HI maps/literature | SOURCE_BOUND_PARTIAL | NGC4088 targeted warp/history protocol exists | accept warp_asymmetry from independent HI/literature review | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC4088 | K_thick_flared | K_warp_history_coupled | interaction_history | interaction or morphology-memory evidence | NED/SIMBAD/literature | SOURCE_BOUND_PARTIAL | NGC4088 targeted warp/history protocol exists | accept interaction_history from independent HI/literature review | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC4088 | K_thick_flared | K_warp_history_coupled | epsilon_cross_bound | bounded cross-coupling interval | Tau Core source-bound protocol | SOURCE_BOUND_READY_FOR_DIAGNOSTIC | NGC4088 epsilon_cross locality bound exists | not accepted endpoint; repeat source-bound derivation for more galaxies | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC4183 | K_exponential_disk | K_expdisk_overlay | disk_scale | disk scale radius | S4G/SPARC | ACCEPTED_FIELD_READY | scale_radius_kpc present in accepted manifest | family/subfamily label audit still needed | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC4183 | K_exponential_disk | K_expdisk_overlay | bar_core_projection_history_overlay | overlay type and strength | S4G/NED/SIMBAD/HI/projection review | MISSING_OR_REVIEW_REQUIRED | bar_core_projection_history_overlay requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC4183 | K_exponential_disk | K_expdisk_overlay | clean_disk_rejection_reason | why K_clean_expdisk is insufficient | source review | MISSING_OR_REVIEW_REQUIRED | clean_disk_rejection_reason requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC5907 | K_thick_flared | K_projection_dominated | projection_geometry | inclination/projection/deprojection support | SPARC/S4G/dust lane/velocity field | PROXY_SUPPORT_ONLY | projection-sensitive inclination/caveat present: inc=88.0 | needs residual-blind projection review or velocity field | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC5907 | K_thick_flared | K_projection_dominated | velocity_field_sanity | non-1D projection audit | HI/PHANGS/literature | MISSING_OR_REVIEW_REQUIRED | velocity_field_sanity requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC5907 | K_thick_flared | K_projection_dominated | vertical_or_warp_source | separate true vertical/warp support from projection | S4G/HI/literature | PROXY_SUPPORT_ONLY | thickness_h_over_rs proxy present | promote with direct vertical/flare/warp source | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC7331 | K_thick_flared | K_thick_regular | vertical_scale_or_thickness | accepted thickness or h/rs | edge-on morphology/S4G/literature | PROXY_SUPPORT_ONLY | thickness_h_over_rs proxy present | promote with direct vertical/flare/warp source | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC7331 | K_thick_flared | K_thick_regular | low_warp_asymmetry | absence of warp/history dominance | HI/projection review | MISSING_OR_REVIEW_REQUIRED | low_warp_asymmetry requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| NGC7331 | K_thick_flared | K_thick_regular | projection_safety | projection not dominant | SPARC/S4G/literature | SOURCE_READY_CONTEXT_ONLY | inclination context present: inc=75.0 | needs explicit projection-safety acceptance | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| UGC05716 | K_scale_tail_spiral | K_disturbed_outer_tail | hi_radius_mass | MHI_1e9Msun;RHI_kpc | SPARC master table | SOURCE_READY_CONTEXT_ONLY | SPARC HI mass/radius present | needs resolved HI asymmetry/profile for subfamily acceptance | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| UGC05716 | K_scale_tail_spiral | K_disturbed_outer_tail | hi_asymmetry_map | HI asymmetry or tail map | HI surveys / THINGS / LITTLE THINGS / WHISP / literature | MISSING_OR_REVIEW_REQUIRED | hi_asymmetry_map requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| UGC05716 | K_scale_tail_spiral | K_disturbed_outer_tail | outer_tail_transition | tail inner/cutoff radius | HI profile or deep optical/IR outer disk | MISSING_OR_REVIEW_REQUIRED | outer_tail_transition requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| UGC05716 | K_scale_tail_spiral | K_disturbed_outer_tail | environment_history | interaction or companion evidence | NED/SIMBAD/literature | MISSING_OR_REVIEW_REQUIRED | environment_history requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| UGC12506 | K_exponential_disk | K_expdisk_overlay | disk_scale | disk scale radius | S4G/SPARC | MISSING | scale_radius_kpc missing | query S4G/NED/decomposition | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| UGC12506 | K_exponential_disk | K_expdisk_overlay | bar_core_projection_history_overlay | overlay type and strength | S4G/NED/SIMBAD/HI/projection review | MISSING_OR_REVIEW_REQUIRED | bar_core_projection_history_overlay requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |
| UGC12506 | K_exponential_disk | K_expdisk_overlay | clean_disk_rejection_reason | why K_clean_expdisk is insufficient | source review | MISSING_OR_REVIEW_REQUIRED | clean_disk_rejection_reason requires source review | query/review listed source family before endpoint use | False | readout_subfamily_source_evidence_matrix_not_endpoint |

## Claim Boundary

Accepted source evidence is still incomplete. SPARC/S4G provide useful
scale and HI context for several rows, but subfamily acceptance requires
additional residual-blind evidence such as resolved HI asymmetry, warp
onset, compact support, vertical flare, projection safety, or overlay
decomposition. No endpoint labels are promoted here.
