# S4G75 Kernel-Ready Promotion Gate

This gate separates source-rich rows from kernel-ready rows. A row is strictly kernel-ready only when the source constrains the same morphology kernel used by the formula family. It is not an endpoint.

## Verdict

Strict kernel-ready endpoint rows: 2.
Conditional kernel rows: 6.
Proxy-only kernel rows: 7.

A strict S4G75 kernel-ready endpoint subset is not runnable yet if the strict count is zero. Conditional rows may guide acquisition and promotion work, but they must not be used as accepted endpoint rows.

## Promotion Summary

| formula_family | observable_driver_type | source_priority | kernel_promotion_status | n_galaxies | galaxies | endpoint_eligible_count | median_delta_matched_rmse | median_delta_vs_tpg | median_delta_vs_mond | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K_compact_finite | compact_support_candidate | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | KERNEL_READY_STRICT | 1 | NGC5985 | 1 | -6.3057 | -6.3057 | -6.3057 | s4g75_kernel_ready_promotion_gate_not_endpoint |
| K_scale_tail_spiral | tail_inner_cutoff_candidate | P0_DIRECT_SOURCE_NATIVE_REQUIRED | KERNEL_READY_CONDITIONAL | 3 | NGC4214;UGC06917;UGC06983 | 0 | 0.677872 | 0.677872 | 0.677872 | s4g75_kernel_ready_promotion_gate_not_endpoint |
| K_scale_tail_spiral | tail_inner_cutoff_candidate | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | KERNEL_READY_CONDITIONAL | 3 | UGC00891;UGC04499;UGC05829 | 0 | -0.656043 | -0.656043 | -0.656043 | s4g75_kernel_ready_promotion_gate_not_endpoint |
| K_thick_flared | thickness_h_over_rs_candidate | P0_DIRECT_SOURCE_NATIVE_REQUIRED | KERNEL_PROXY_ONLY | 5 | NGC0024;NGC2683;NGC3726;NGC3949;NGC4088 | 0 | 0.469746 | 0.469746 | 0.469746 | s4g75_kernel_ready_promotion_gate_not_endpoint |
| K_thick_flared | thickness_h_over_rs_candidate | P0_DIRECT_SOURCE_NATIVE_REQUIRED | KERNEL_READY_STRICT | 1 | NGC5907 | 1 | 0.629947 | 0.629947 | 0.629947 | s4g75_kernel_ready_promotion_gate_not_endpoint |
| K_thick_flared | thickness_h_over_rs_candidate | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | KERNEL_PROXY_ONLY | 2 | NGC3972;NGC4389 | 0 | -0.0710088 | -0.0710088 | -0.0710088 | s4g75_kernel_ready_promotion_gate_not_endpoint |

## Endpoint Subset Status

| kernel_promotion_status | n_galaxies | endpoint_eligible_count | p0_count | p1_count | galaxies | endpoint_subset_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| KERNEL_PROXY_ONLY | 7 | 0 | 5 | 2 | NGC0024;NGC2683;NGC3726;NGC3949;NGC4088;NGC3972;NGC4389 | NO_STRICT_ENDPOINT_ROWS | s4g75_kernel_ready_promotion_gate_not_endpoint |
| KERNEL_READY_CONDITIONAL | 6 | 0 | 3 | 3 | NGC4214;UGC06917;UGC06983;UGC00891;UGC04499;UGC05829 | NO_STRICT_ENDPOINT_ROWS | s4g75_kernel_ready_promotion_gate_not_endpoint |
| KERNEL_READY_STRICT | 2 | 2 | 1 | 1 | NGC5907;NGC5985 | RUNNABLE_STRICT_SUBSET | s4g75_kernel_ready_promotion_gate_not_endpoint |

## Galaxy-Level Gate

| galaxy | formula_family | source_priority | observable_driver_type | kernel_specific_source_status | direct_measurement_status | kernel_parameter_filled | value_kpc | dimensionless_value | kernel_promotion_status | endpoint_eligible_after_kernel_gate | kernel_promotion_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4214 | K_scale_tail_spiral | P0_DIRECT_SOURCE_NATIVE_REQUIRED | tail_inner_cutoff_candidate | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7 | tail_inner_radius_kpc;tail_cutoff_radius_kpc | nan | nan | KERNEL_READY_CONDITIONAL | False | SPARC HI extent supports a tail cutoff candidate but does not directly constrain the transition profile |
| UGC06917 | K_scale_tail_spiral | P0_DIRECT_SOURCE_NATIVE_REQUIRED | tail_inner_cutoff_candidate | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7 | tail_inner_radius_kpc;tail_cutoff_radius_kpc | nan | nan | KERNEL_READY_CONDITIONAL | False | SPARC HI extent supports a tail cutoff candidate but does not directly constrain the transition profile |
| UGC06983 | K_scale_tail_spiral | P0_DIRECT_SOURCE_NATIVE_REQUIRED | tail_inner_cutoff_candidate | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7 | tail_inner_radius_kpc;tail_cutoff_radius_kpc | nan | nan | KERNEL_READY_CONDITIONAL | False | SPARC HI extent supports a tail cutoff candidate but does not directly constrain the transition profile |
| NGC0024 | K_thick_flared | P0_DIRECT_SOURCE_NATIVE_REQUIRED | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | KERNEL_PROXY_ONLY | False | thick/flared kernel lacks direct vertical scale height, flare, warp, or gas-plane thickness evidence |
| NGC2683 | K_thick_flared | P0_DIRECT_SOURCE_NATIVE_REQUIRED | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | KERNEL_PROXY_ONLY | False | thick/flared kernel lacks direct vertical scale height, flare, warp, or gas-plane thickness evidence |
| NGC3726 | K_thick_flared | P0_DIRECT_SOURCE_NATIVE_REQUIRED | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | KERNEL_PROXY_ONLY | False | thick/flared kernel lacks direct vertical scale height, flare, warp, or gas-plane thickness evidence |
| NGC3949 | K_thick_flared | P0_DIRECT_SOURCE_NATIVE_REQUIRED | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | KERNEL_PROXY_ONLY | False | thick/flared kernel lacks direct vertical scale height, flare, warp, or gas-plane thickness evidence |
| NGC4088 | K_thick_flared | P0_DIRECT_SOURCE_NATIVE_REQUIRED | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | KERNEL_PROXY_ONLY | False | thick/flared kernel lacks direct vertical scale height, flare, warp, or gas-plane thickness evidence |
| NGC5907 | K_thick_flared | P0_DIRECT_SOURCE_NATIVE_REQUIRED | thickness_h_over_rs_candidate | PARTIAL_EDGE_DISK_VERTICAL_EVIDENCE_READY | DIRECT_S4G_EDGEDISK_HZ_HR_READY | thickness_h_over_rs | 0.768275 | 0.173321 | KERNEL_READY_STRICT | True | DIRECT_S4G_EDGEDISK_HZ_HR_READY supplies the source-native kernel parameter used by the formula family |
| NGC5985 | K_compact_finite | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | compact_support_candidate | PARTIAL_COMPACT_COMPONENT_READY_RADIUS_MISSING | DIRECT_S4G_BULGE_RE_READY | compact_support_radius_kpc | 0.735239 | nan | KERNEL_READY_STRICT | True | DIRECT_S4G_BULGE_RE_READY supplies the source-native kernel parameter used by the formula family |
| UGC00891 | K_scale_tail_spiral | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | tail_inner_cutoff_candidate | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7 | tail_inner_radius_kpc;tail_cutoff_radius_kpc | nan | nan | KERNEL_READY_CONDITIONAL | False | SPARC HI extent supports a tail cutoff candidate but does not directly constrain the transition profile |
| UGC04499 | K_scale_tail_spiral | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | tail_inner_cutoff_candidate | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7 | tail_inner_radius_kpc;tail_cutoff_radius_kpc | nan | nan | KERNEL_READY_CONDITIONAL | False | SPARC HI extent supports a tail cutoff candidate but does not directly constrain the transition profile |
| UGC05829 | K_scale_tail_spiral | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | tail_inner_cutoff_candidate | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7 | tail_inner_radius_kpc;tail_cutoff_radius_kpc | nan | nan | KERNEL_READY_CONDITIONAL | False | SPARC HI extent supports a tail cutoff candidate but does not directly constrain the transition profile |
| NGC3972 | K_thick_flared | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | KERNEL_PROXY_ONLY | False | thick/flared kernel lacks direct vertical scale height, flare, warp, or gas-plane thickness evidence |
| NGC4389 | K_thick_flared | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | KERNEL_PROXY_ONLY | False | thick/flared kernel lacks direct vertical scale height, flare, warp, or gas-plane thickness evidence |

## Claim Boundary

The gate is deliberately conservative. Generic S4G/SPARC/HI source coverage is not enough. Endpoint eligibility requires direct or accepted-promoted evidence for the kernel observable actually used by the morphology formula family.
