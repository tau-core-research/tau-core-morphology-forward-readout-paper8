# S4G75 Kernel-Observable Fill

This table fills concrete kernel-observable candidates for the S4G75 holdout repair set using residual-blind S4G/SPARC/HI fields and predeclared bridge rules. It does not promote endpoint-ready accepted labels.

## Status Summary

| observable_status_field | status | n_galaxies | claim_boundary |
| --- | --- | --- | --- |
| scale_radius_status | SOURCE_DERIVED_S4G_SPARC_SCALE | 15 | s4g75_kernel_observable_fill_not_endpoint |
| tail_observable_status | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | 6 | s4g75_kernel_observable_fill_not_endpoint |
| compact_observable_status | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | 1 | s4g75_kernel_observable_fill_not_endpoint |
| thickness_observable_status | SOURCE_CONSTRAINED_EDGE_DISK_CANDIDATE | 1 | s4g75_kernel_observable_fill_not_endpoint |
| thickness_observable_status | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | 7 | s4g75_kernel_observable_fill_not_endpoint |

## Filled Kernel Observables

| galaxy | formula_family | scale_radius_kpc | tail_inner_radius_kpc | tail_cutoff_radius_kpc | compact_support_radius_kpc | thickness_h_over_rs | tail_observable_status | compact_observable_status | thickness_observable_status | kernel_observable_provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5985 | K_compact_finite | 6.75573 | nan | nan | 10.71 | nan | NOT_APPLICABLE | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | NOT_APPLICABLE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;SPARC_Reff_used_as_compact_support_candidate_no_S4G_bulge_radius |
| UGC00891 | K_scale_tail_spiral | 1.14578 | 2.29156 | 6.23 | nan | nan | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | NOT_APPLICABLE | NOT_APPLICABLE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;tail_cutoff_from_SPARC_RHI;tail_inner_from_predeclared_disk_to_HI_transition_rule |
| UGC04499 | K_scale_tail_spiral | 1.05871 | 2.11742 | 8.67 | nan | nan | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | NOT_APPLICABLE | NOT_APPLICABLE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;tail_cutoff_from_SPARC_RHI;tail_inner_from_predeclared_disk_to_HI_transition_rule |
| NGC4214 | K_scale_tail_spiral | 0.646451 | 1.2929 | 5.84 | nan | nan | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | NOT_APPLICABLE | NOT_APPLICABLE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;tail_cutoff_from_SPARC_RHI;tail_inner_from_predeclared_disk_to_HI_transition_rule |
| UGC05829 | K_scale_tail_spiral | 1.73625 | 3.4725 | 7.87 | nan | nan | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | NOT_APPLICABLE | NOT_APPLICABLE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;tail_cutoff_from_SPARC_RHI;tail_inner_from_predeclared_disk_to_HI_transition_rule |
| NGC0024 | K_thick_flared | 1.3969 | nan | nan | nan | 0.132187 | NOT_APPLICABLE | NOT_APPLICABLE | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;predeclared_h_over_rs_from_inclination_and_HI_extent_no_direct_vertical_scale |
| NGC2683 | K_thick_flared | 2.20965 | nan | nan | nan | 0.202408 | NOT_APPLICABLE | NOT_APPLICABLE | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;predeclared_h_over_rs_from_inclination_and_HI_extent_no_direct_vertical_scale |
| NGC3726 | K_thick_flared | 4.36245 | nan | nan | nan | 0.130889 | NOT_APPLICABLE | NOT_APPLICABLE | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;predeclared_h_over_rs_from_inclination_and_HI_extent_no_direct_vertical_scale |
| NGC3949 | K_thick_flared | 1.44775 | nan | nan | nan | 0.174768 | NOT_APPLICABLE | NOT_APPLICABLE | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;predeclared_h_over_rs_from_inclination_and_HI_extent_no_direct_vertical_scale |
| NGC3972 | K_thick_flared | 2.44957 | nan | nan | nan | 0.181028 | NOT_APPLICABLE | NOT_APPLICABLE | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;predeclared_h_over_rs_from_inclination_and_HI_extent_no_direct_vertical_scale |
| NGC4088 | K_thick_flared | 3.25591 | nan | nan | nan | 0.178337 | NOT_APPLICABLE | NOT_APPLICABLE | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;predeclared_h_over_rs_from_inclination_and_HI_extent_no_direct_vertical_scale |
| NGC4389 | K_thick_flared | 2.0272 | nan | nan | nan | 0.113593 | NOT_APPLICABLE | NOT_APPLICABLE | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;predeclared_h_over_rs_from_inclination_and_HI_extent_no_direct_vertical_scale |
| NGC5907 | K_thick_flared | 4.43267 | nan | nan | nan | 0.22 | NOT_APPLICABLE | NOT_APPLICABLE | SOURCE_CONSTRAINED_EDGE_DISK_CANDIDATE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;S4G_edge_disk_component_supports_thick_flared_candidate_h_over_rs |
| UGC06917 | K_scale_tail_spiral | 2.9592 | 5.91841 | 12.67 | nan | nan | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | NOT_APPLICABLE | NOT_APPLICABLE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;tail_cutoff_from_SPARC_RHI;tail_inner_from_predeclared_disk_to_HI_transition_rule |
| UGC06983 | K_scale_tail_spiral | 3.13897 | 6.27794 | 16.07 | nan | nan | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | NOT_APPLICABLE | NOT_APPLICABLE | scale_radius_from_S4G_Pipeline4_x_SPARC_distance;tail_cutoff_from_SPARC_RHI;tail_inner_from_predeclared_disk_to_HI_transition_rule |

## Claim Boundary

Concrete means numerically filled. It does not mean accepted. Direct S4G/SPARC scale values are source-derived; tail, compact, and thickness fields are source-constrained or formula-conditional candidates unless a direct source-native morphology measurement is present.