# S4G75 Holdout Repair Review Packet

This packet converts the S4G75 holdout P0/P1/P2 repair queue into residual-blind source-review fields. It uses existing S4G/SPARC and crossmatch tables where available, but it does not promote accepted labels and does not run endpoint scores.

## Verdict

Galaxies in packet: 15.
Review fields: 71.

Existing S4G/SPARC scale evidence is present for these rows, but family labels and family-specific kernel fields remain blocked until the review fields below are completed.

## Galaxy Summary

| galaxy | repair_priority | formula_family | n_review_fields | scale_radius_kpc | sparc_inclination_deg | manifest_caveat | missing_required_fields | s4g_support_status | audit_lane | dustpedia_match_status | phangs_match_status | hi_survey_match_status | endpoint_blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5985 | P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | K_compact_finite | 5 | 6.75573 | 60 | large_distance_error | compact_support_radius_kpc | S4G_EXPDISK_SUPPORT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;compact_support_radius_kpc |
| UGC00891 | P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | K_scale_tail_spiral | 5 | 1.14578 | 60 | few_rotation_points;large_distance_error | tail_inner_radius_kpc;tail_cutoff_radius_kpc | S4G_EXPDISK_SUPPORT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;tail_inner_radius_kpc;tail_cutoff_radius_kpc |
| UGC04499 | P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | K_scale_tail_spiral | 5 | 1.05871 | 50 | large_distance_error | tail_inner_radius_kpc;tail_cutoff_radius_kpc | S4G_EXPDISK_SUPPORT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;tail_inner_radius_kpc;tail_cutoff_radius_kpc |
| NGC4214 | P1_INCLINATION_PROJECTION_REVIEW | K_scale_tail_spiral | 5 | 0.646451 | 15 | low_inclination | tail_inner_radius_kpc;tail_cutoff_radius_kpc | S4G_EXPDISK_WITH_BAR_CAVEAT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;tail_inner_radius_kpc;tail_cutoff_radius_kpc |
| UGC05829 | P1_INCLINATION_PROJECTION_REVIEW | K_scale_tail_spiral | 5 | 1.73625 | 34 | low_inclination;large_distance_error | tail_inner_radius_kpc;tail_cutoff_radius_kpc | S4G_EXPDISK_SUPPORT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;tail_inner_radius_kpc;tail_cutoff_radius_kpc |
| NGC0024 | P1_VERTICAL_GEOMETRY_SOURCE | K_thick_flared | 5 | 1.3969 | 64 | vertical_geometry_proxy_only | thickness_h_over_rs | S4G_EXPDISK_WITH_BAR_CAVEAT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;thickness_h_over_rs |
| NGC2683 | P1_VERTICAL_GEOMETRY_SOURCE | K_thick_flared | 5 | 2.20965 | 80 | vertical_geometry_proxy_only | thickness_h_over_rs | S4G_EXPDISK_WITH_BAR_CAVEAT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;thickness_h_over_rs |
| NGC3726 | P1_VERTICAL_GEOMETRY_SOURCE | K_thick_flared | 5 | 4.36245 | 53 | vertical_geometry_proxy_only | thickness_h_over_rs | S4G_EXPDISK_SUPPORT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;thickness_h_over_rs |
| NGC3949 | P1_VERTICAL_GEOMETRY_SOURCE | K_thick_flared | 5 | 1.44775 | 55 | few_rotation_points;vertical_geometry_proxy_only | thickness_h_over_rs | S4G_EXPDISK_SUPPORT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;thickness_h_over_rs |
| NGC3972 | P1_VERTICAL_GEOMETRY_SOURCE | K_thick_flared | 5 | 2.44957 | 77 | vertical_geometry_proxy_only | thickness_h_over_rs | S4G_EXPDISK_SUPPORT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;thickness_h_over_rs |
| NGC4088 | P1_VERTICAL_GEOMETRY_SOURCE | K_thick_flared | 5 | 3.25591 | 69 | vertical_geometry_proxy_only | thickness_h_over_rs | S4G_EXPDISK_SUPPORT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;thickness_h_over_rs |
| NGC4389 | P1_VERTICAL_GEOMETRY_SOURCE | K_thick_flared | 5 | 2.0272 | 50 | few_rotation_points;vertical_geometry_proxy_only | thickness_h_over_rs | S4G_EXPDISK_WITH_BAR_CAVEAT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;thickness_h_over_rs |
| NGC5907 | P1_VERTICAL_GEOMETRY_SOURCE | K_thick_flared | 5 | 4.43267 | 88 | vertical_geometry_proxy_only | thickness_h_over_rs | S4G_EDGEDISK_SUPPORT_CAVEATED | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;thickness_h_over_rs |
| UGC06917 | P2_SOURCE_NORMALIZATION_REVIEW | K_scale_tail_spiral | 3 | 2.9592 | 56 | none | tail_inner_radius_kpc;tail_cutoff_radius_kpc | S4G_EXPDISK_WITH_BAR_CAVEAT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;tail_inner_radius_kpc;tail_cutoff_radius_kpc |
| UGC06983 | P2_SOURCE_NORMALIZATION_REVIEW | K_scale_tail_spiral | 3 | 3.13897 | 49 | none | tail_inner_radius_kpc;tail_cutoff_radius_kpc | S4G_EXPDISK_WITH_BAR_CAVEAT | PARTIAL_SCALE_READY_KERNEL_BLOCKED | TO_BE_CHECKED | TO_BE_CHECKED | TO_BE_CHECKED | external_family_label_audit_pending;tail_inner_radius_kpc;tail_cutoff_radius_kpc |

## Field Summary

| repair_priority | review_field | n_galaxies |
| --- | --- | --- |
| P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | distance_source_review | 3 |
| P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | family_label_external_audit | 3 |
| P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | kernel_observable_completion | 3 |
| P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | projection_safety_review | 3 |
| P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | scale_radius_consistency_review | 3 |
| P1_INCLINATION_PROJECTION_REVIEW | distance_source_review | 2 |
| P1_INCLINATION_PROJECTION_REVIEW | family_label_external_audit | 2 |
| P1_INCLINATION_PROJECTION_REVIEW | inclination_source_review | 2 |
| P1_INCLINATION_PROJECTION_REVIEW | projection_safety_review | 2 |
| P1_INCLINATION_PROJECTION_REVIEW | tail_extent_source_review | 2 |
| P1_VERTICAL_GEOMETRY_SOURCE | edge_projection_safety_review | 8 |
| P1_VERTICAL_GEOMETRY_SOURCE | family_label_external_audit | 8 |
| P1_VERTICAL_GEOMETRY_SOURCE | thick_flared_kernel_observable_completion | 8 |
| P1_VERTICAL_GEOMETRY_SOURCE | vertical_thickness_or_flare_source_review | 8 |
| P1_VERTICAL_GEOMETRY_SOURCE | warp_or_gas_plane_source_review | 8 |
| P2_SOURCE_NORMALIZATION_REVIEW | baryonic_scale_consistency_review | 2 |
| P2_SOURCE_NORMALIZATION_REVIEW | component_weight_review | 2 |
| P2_SOURCE_NORMALIZATION_REVIEW | source_normalization_factor_review | 2 |

## Claim Boundary

This packet is a repair workflow, not a validation result. Filling it may make a future frozen endpoint cleaner, but no endpoint gate changes here.