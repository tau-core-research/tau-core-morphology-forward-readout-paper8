# S4G75 Direct Kernel Measurement Extraction

This report extracts direct S4G Table 7 kernel measurements for the stable S4G75 direct-source acquisition manifest. It does not use endpoint residuals and does not rerun scores.

## Verdict

Acquisition-manifest rows checked: 15.
Direct kernel measurements found: 2.
Rows still missing direct kernel measurements: 13.

## Summary

| observable_driver_type | direct_measurement_status | kernel_parameter_filled | n_galaxies | galaxies | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| compact_support_candidate | DIRECT_S4G_BULGE_RE_READY | compact_support_radius_kpc | 1 | NGC5985 | s4g75_direct_kernel_measurement_extraction_not_endpoint |
| tail_inner_cutoff_candidate | NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7 | tail_inner_radius_kpc;tail_cutoff_radius_kpc | 6 | NGC4214;UGC06917;UGC06983;UGC00891;UGC04499;UGC05829 | s4g75_direct_kernel_measurement_extraction_not_endpoint |
| thickness_h_over_rs_candidate | DIRECT_S4G_EDGEDISK_HZ_HR_READY | thickness_h_over_rs | 1 | NGC5907 | s4g75_direct_kernel_measurement_extraction_not_endpoint |
| thickness_h_over_rs_candidate | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | 7 | NGC0024;NGC2683;NGC3726;NGC3949;NGC4088;NGC3972;NGC4389 | s4g75_direct_kernel_measurement_extraction_not_endpoint |

## Galaxy-Level Measurements

| galaxy | formula_family | observable_driver_type | direct_measurement_status | kernel_parameter_filled | value_kpc | secondary_value_kpc | dimensionless_value | source_component | promotion_interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4214 | K_scale_tail_spiral | tail_inner_cutoff_candidate | NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7 | tail_inner_radius_kpc;tail_cutoff_radius_kpc | nan | nan | nan |  | S4G Table 7 does not provide the HI/outer-disk transition profile required by the tail kernel |
| UGC06917 | K_scale_tail_spiral | tail_inner_cutoff_candidate | NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7 | tail_inner_radius_kpc;tail_cutoff_radius_kpc | nan | nan | nan |  | S4G Table 7 does not provide the HI/outer-disk transition profile required by the tail kernel |
| UGC06983 | K_scale_tail_spiral | tail_inner_cutoff_candidate | NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7 | tail_inner_radius_kpc;tail_cutoff_radius_kpc | nan | nan | nan |  | S4G Table 7 does not provide the HI/outer-disk transition profile required by the tail kernel |
| NGC0024 | K_thick_flared | thickness_h_over_rs_candidate | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | nan |  | no S4G edge-disk hz2/hr2 found |
| NGC2683 | K_thick_flared | thickness_h_over_rs_candidate | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | nan |  | no S4G edge-disk hz2/hr2 found |
| NGC3726 | K_thick_flared | thickness_h_over_rs_candidate | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | nan |  | no S4G edge-disk hz2/hr2 found |
| NGC3949 | K_thick_flared | thickness_h_over_rs_candidate | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | nan |  | no S4G edge-disk hz2/hr2 found |
| NGC4088 | K_thick_flared | thickness_h_over_rs_candidate | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | nan |  | no S4G edge-disk hz2/hr2 found |
| NGC5907 | K_thick_flared | thickness_h_over_rs_candidate | DIRECT_S4G_EDGEDISK_HZ_HR_READY | thickness_h_over_rs | 0.768275 | 4.43268 | 0.173321 | Z:edgedisk_hz2_over_hr2 | S4G edge-disk hz2/hr2 directly constrains the vertical kernel ratio |
| NGC5985 | K_compact_finite | compact_support_candidate | DIRECT_S4G_BULGE_RE_READY | compact_support_radius_kpc | 0.735239 | nan | nan | B:sersic_Re | S4G Sersic bulge effective radius directly constrains a compact support candidate |
| UGC00891 | K_scale_tail_spiral | tail_inner_cutoff_candidate | NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7 | tail_inner_radius_kpc;tail_cutoff_radius_kpc | nan | nan | nan |  | S4G Table 7 does not provide the HI/outer-disk transition profile required by the tail kernel |
| UGC04499 | K_scale_tail_spiral | tail_inner_cutoff_candidate | NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7 | tail_inner_radius_kpc;tail_cutoff_radius_kpc | nan | nan | nan |  | S4G Table 7 does not provide the HI/outer-disk transition profile required by the tail kernel |
| UGC05829 | K_scale_tail_spiral | tail_inner_cutoff_candidate | NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7 | tail_inner_radius_kpc;tail_cutoff_radius_kpc | nan | nan | nan |  | S4G Table 7 does not provide the HI/outer-disk transition profile required by the tail kernel |
| NGC3972 | K_thick_flared | thickness_h_over_rs_candidate | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | nan |  | no S4G edge-disk hz2/hr2 found |
| NGC4389 | K_thick_flared | thickness_h_over_rs_candidate | NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7 | thickness_h_over_rs | nan | nan | nan |  | no S4G edge-disk hz2/hr2 found |

## Claim Boundary

A direct S4G decomposition parameter can support kernel promotion only for the matching kernel. Bulge Re can support compact finite-source; edge-disk hz/hr can support thick/flared. This pass does not promote RHI-only scale-tail rows because S4G Table 7 does not supply their outer transition profile.
