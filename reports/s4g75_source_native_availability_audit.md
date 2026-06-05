# S4G75 Source-Native Availability Audit

This audit checks the S4G75 direct source-native acquisition queue against already acquired local S4G, SPARC/HI, DustPedia, and PHANGS tables. It is not an endpoint and does not promote accepted labels.

## Source Coverage

| source_column | positive_status | n_positive | n_total | positive_fraction | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| s4g_match_status | S4G_MATCHED | 15 | 15 | 1 | s4g75_source_native_availability_audit_not_endpoint |
| dustpedia_status | DUSTPEDIA_MATCHED | 3 | 15 | 0.2 | s4g75_source_native_availability_audit_not_endpoint |
| phangs_status | PHANGS_PUBLIC_SAMPLE_MATCH | 0 | 15 | 0 | s4g75_source_native_availability_audit_not_endpoint |
| SPARC_RHI | RHI_kpc_positive | 14 | 15 | 0.933333 | s4g75_source_native_availability_audit_not_endpoint |

## Kernel-Specific Availability Summary

| formula_family | observable_driver_type | source_priority | kernel_specific_source_status | n_galaxies | galaxies | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| K_compact_finite | compact_support_candidate | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | PARTIAL_COMPACT_COMPONENT_READY_RADIUS_MISSING | 1 | NGC5985 | s4g75_source_native_availability_audit_not_endpoint |
| K_scale_tail_spiral | tail_inner_cutoff_candidate | P0_DIRECT_SOURCE_NATIVE_REQUIRED | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | 3 | NGC4214;UGC06917;UGC06983 | s4g75_source_native_availability_audit_not_endpoint |
| K_scale_tail_spiral | tail_inner_cutoff_candidate | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | 3 | UGC00891;UGC04499;UGC05829 | s4g75_source_native_availability_audit_not_endpoint |
| K_thick_flared | thickness_h_over_rs_candidate | P0_DIRECT_SOURCE_NATIVE_REQUIRED | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | 5 | NGC0024;NGC2683;NGC3726;NGC3949;NGC4088 | s4g75_source_native_availability_audit_not_endpoint |
| K_thick_flared | thickness_h_over_rs_candidate | P0_DIRECT_SOURCE_NATIVE_REQUIRED | PARTIAL_EDGE_DISK_VERTICAL_EVIDENCE_READY | 1 | NGC5907 | s4g75_source_native_availability_audit_not_endpoint |
| K_thick_flared | thickness_h_over_rs_candidate | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | 2 | NGC3972;NGC4389 | s4g75_source_native_availability_audit_not_endpoint |

## Galaxy-Level Availability

| galaxy | formula_family | source_priority | observable_driver_type | kernel_specific_source_status | s4g_match_status | dustpedia_status | phangs_status | RHI_kpc | s4g_model_components | s4g_disk_component_source | source_status_notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4214 | K_scale_tail_spiral | P0_DIRECT_SOURCE_NATIVE_REQUIRED | tail_inner_cutoff_candidate | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | S4G_MATCHED | DUSTPEDIA_MATCHED | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 5.84 | D;BAR | D:expdisk_hr3 | S4G matched; DustPedia matched; SPARC HI radius ready; no PHANGS public sample match; HI extent is not a direct outer-disk transition profile |
| UGC06917 | K_scale_tail_spiral | P0_DIRECT_SOURCE_NATIVE_REQUIRED | tail_inner_cutoff_candidate | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | S4G_MATCHED | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 12.67 | D;BAR | D:expdisk_hr3 | S4G matched; SPARC HI radius ready; no DustPedia direct match; no PHANGS public sample match; HI extent is not a direct outer-disk transition profile |
| UGC06983 | K_scale_tail_spiral | P0_DIRECT_SOURCE_NATIVE_REQUIRED | tail_inner_cutoff_candidate | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | S4G_MATCHED | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 16.07 | D;BAR | D:expdisk_hr3 | S4G matched; SPARC HI radius ready; no DustPedia direct match; no PHANGS public sample match; HI extent is not a direct outer-disk transition profile |
| NGC0024 | K_thick_flared | P0_DIRECT_SOURCE_NATIVE_REQUIRED | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | S4G_MATCHED | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 7.29 | D;BAR | D:expdisk_hr3 | S4G matched; SPARC HI radius ready; no DustPedia direct match; no PHANGS public sample match; no direct vertical scale height / flare / warp measurement |
| NGC2683 | K_thick_flared | P0_DIRECT_SOURCE_NATIVE_REQUIRED | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | S4G_MATCHED | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 13.79 | D;BAR;N | D:expdisk_hr3 | S4G matched; SPARC HI radius ready; no DustPedia direct match; no PHANGS public sample match; no direct vertical scale height / flare / warp measurement |
| NGC3726 | K_thick_flared | P0_DIRECT_SOURCE_NATIVE_REQUIRED | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | S4G_MATCHED | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 22.2 | B;D | D:expdisk_hr3 | S4G matched; SPARC HI radius ready; no DustPedia direct match; no PHANGS public sample match; no direct vertical scale height / flare / warp measurement |
| NGC3949 | K_thick_flared | P0_DIRECT_SOURCE_NATIVE_REQUIRED | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | S4G_MATCHED | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 13.72 | B;D | D:expdisk_hr3 | S4G matched; SPARC HI radius ready; no DustPedia direct match; no PHANGS public sample match; no direct vertical scale height / flare / warp measurement |
| NGC4088 | K_thick_flared | P0_DIRECT_SOURCE_NATIVE_REQUIRED | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | S4G_MATCHED | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 22.25 | D;N | D:expdisk_hr3 | S4G matched; SPARC HI radius ready; no DustPedia direct match; no PHANGS public sample match; no direct vertical scale height / flare / warp measurement |
| NGC5907 | K_thick_flared | P0_DIRECT_SOURCE_NATIVE_REQUIRED | thickness_h_over_rs_candidate | PARTIAL_EDGE_DISK_VERTICAL_EVIDENCE_READY | S4G_MATCHED | DUSTPEDIA_MATCHED | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 0 | Z | Z:edgedisk_hr2 | S4G matched; DustPedia matched; S4G edge-disk component supports vertical candidate; no SPARC HI radius; no PHANGS public sample match |
| NGC5985 | K_compact_finite | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | compact_support_candidate | PARTIAL_COMPACT_COMPONENT_READY_RADIUS_MISSING | S4G_MATCHED | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 39.5 | B;D | D:expdisk_hr3 | S4G matched; SPARC HI radius ready; no DustPedia direct match; no PHANGS public sample match; S4G bulge component present but no direct compact radius |
| UGC00891 | K_scale_tail_spiral | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | tail_inner_cutoff_candidate | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | S4G_MATCHED | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 6.23 | D | D:expdisk_hr3 | S4G matched; SPARC HI radius ready; no DustPedia direct match; no PHANGS public sample match; HI extent is not a direct outer-disk transition profile |
| UGC04499 | K_scale_tail_spiral | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | tail_inner_cutoff_candidate | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | S4G_MATCHED | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 8.67 | D | D:expdisk_hr3 | S4G matched; SPARC HI radius ready; no DustPedia direct match; no PHANGS public sample match; HI extent is not a direct outer-disk transition profile |
| UGC05829 | K_scale_tail_spiral | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | tail_inner_cutoff_candidate | PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING | S4G_MATCHED | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 7.87 | D | D:expdisk_hr3 | S4G matched; SPARC HI radius ready; no DustPedia direct match; no PHANGS public sample match; HI extent is not a direct outer-disk transition profile |
| NGC3972 | K_thick_flared | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | S4G_MATCHED | DUSTPEDIA_MATCHED | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 10.05 | B;D | D:expdisk_hr3 | S4G matched; DustPedia matched; SPARC HI radius ready; no PHANGS public sample match; no direct vertical scale height / flare / warp measurement |
| NGC4389 | K_thick_flared | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | thickness_h_over_rs_candidate | KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY | S4G_MATCHED | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_PUBLIC_SAMPLE_MATCH | 6.81 | D;BAR | D:expdisk_hr3 | S4G matched; SPARC HI radius ready; no DustPedia direct match; no PHANGS public sample match; no direct vertical scale height / flare / warp measurement |

## Claim Boundary

Generic source coverage is not the same as kernel-specific direct observables. HI radius can support a tail cutoff candidate but does not by itself provide an outer-disk transition profile. Inclination plus HI extent can support a thickness proxy but does not provide a vertical scale height, flare, or warp measurement.
