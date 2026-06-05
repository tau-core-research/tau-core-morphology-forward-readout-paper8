# S4G75 Filled-Kernel Delta-Driver Audit

This diagnostic splits the filled-kernel stress-test delta by formula family, observable type, and repair priority. It is not a new endpoint and does not change the accepted-claim status.

## Main Reading

The filled candidates preserve morphology-family specificity in the S4G75 endpoint, but they do not uniformly improve baseline transfer. The delta-driver split identifies where direct source-native kernel observables are needed before a baseline-superiority claim is allowed.

## Outcome Summary

| driver_outcome | source_priority | n_galaxies | median_delta_matched_rmse | median_delta_vs_tpg | median_delta_vs_mond |
| --- | --- | --- | --- | --- | --- |
| FILLED_WORSENED_BASELINE_TRANSFER | P0_DIRECT_SOURCE_NATIVE_REQUIRED | 9 | 0.629947 | 0.629947 | 0.629947 |
| FILLED_IMPROVED_MATCHED_AND_BASELINES | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | 6 | -0.542295 | -0.542295 | -0.542295 |

## Driver Summary

| formula_family | observable_driver_type | driver_outcome | source_priority | n_galaxies | median_delta_matched_rmse | median_delta_vs_wrong | median_delta_vs_tpg | median_delta_vs_mond | improves_matched_fraction | improves_tpg_fraction | improves_mond_fraction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K_compact_finite | compact_support_candidate | FILLED_IMPROVED_MATCHED_AND_BASELINES | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | 1 | -6.3057 | -5.97701 | -6.3057 | -6.3057 | 1 | 1 | 1 | s4g75_filled_kernel_delta_driver_audit_not_endpoint |
| K_scale_tail_spiral | tail_inner_cutoff_candidate | FILLED_IMPROVED_MATCHED_AND_BASELINES | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | 3 | -0.656043 | -0.850256 | -0.656043 | -0.656043 | 1 | 1 | 1 | s4g75_filled_kernel_delta_driver_audit_not_endpoint |
| K_scale_tail_spiral | tail_inner_cutoff_candidate | FILLED_WORSENED_BASELINE_TRANSFER | P0_DIRECT_SOURCE_NATIVE_REQUIRED | 3 | 0.677872 | 1.13575 | 0.677872 | 0.677872 | 0 | 0 | 0 | s4g75_filled_kernel_delta_driver_audit_not_endpoint |
| K_thick_flared | thickness_h_over_rs_candidate | FILLED_IMPROVED_MATCHED_AND_BASELINES | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | 2 | -0.0710088 | -0.0216501 | -0.0710088 | -0.0710088 | 1 | 1 | 1 | s4g75_filled_kernel_delta_driver_audit_not_endpoint |
| K_thick_flared | thickness_h_over_rs_candidate | FILLED_WORSENED_BASELINE_TRANSFER | P0_DIRECT_SOURCE_NATIVE_REQUIRED | 6 | 0.549846 | 0.148341 | 0.549846 | 0.549846 | 0 | 0 | 0 | s4g75_filled_kernel_delta_driver_audit_not_endpoint |

## Direct Source-Native Observable Targets

| formula_family | observable_driver_type | source_priority | source_native_target | n_galaxies | galaxies | median_delta_matched_rmse | median_delta_vs_tpg | median_delta_vs_mond | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K_scale_tail_spiral | tail_inner_cutoff_candidate | P0_DIRECT_SOURCE_NATIVE_REQUIRED | direct outer-disk/HI transition observable: HI radial profile, break radius, truncation radius, or source-native tail cutoff | 3 | NGC4214;UGC06917;UGC06983 | 0.677872 | 0.677872 | 0.677872 | s4g75_filled_kernel_delta_driver_audit_not_endpoint |
| K_thick_flared | thickness_h_over_rs_candidate | P0_DIRECT_SOURCE_NATIVE_REQUIRED | direct vertical geometry observable: scale height, flare/warp profile, edge-on thickness, or gas-plane thickness | 6 | NGC0024;NGC2683;NGC3726;NGC3949;NGC4088;NGC5907 | 0.549846 | 0.549846 | 0.549846 | s4g75_filled_kernel_delta_driver_audit_not_endpoint |
| K_compact_finite | compact_support_candidate | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | direct compact support observable: bulge/component radius, central compact mass-light component, or decomposition support | 1 | NGC5985 | -6.3057 | -6.3057 | -6.3057 | s4g75_filled_kernel_delta_driver_audit_not_endpoint |
| K_scale_tail_spiral | tail_inner_cutoff_candidate | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | direct outer-disk/HI transition observable: HI radial profile, break radius, truncation radius, or source-native tail cutoff | 3 | UGC00891;UGC04499;UGC05829 | -0.656043 | -0.656043 | -0.656043 | s4g75_filled_kernel_delta_driver_audit_not_endpoint |
| K_thick_flared | thickness_h_over_rs_candidate | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | direct vertical geometry observable: scale height, flare/warp profile, edge-on thickness, or gas-plane thickness | 2 | NGC3972;NGC4389 | -0.0710088 | -0.0710088 | -0.0710088 | s4g75_filled_kernel_delta_driver_audit_not_endpoint |

## Galaxy-Level Delta Drivers

| galaxy | formula_family | repair_priority | observable_driver_type | driver_outcome | source_priority | filled_minus_old_matched_rmse | filled_minus_old_matched_minus_tpg | filled_minus_old_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4214 | K_scale_tail_spiral | P1_INCLINATION_PROJECTION_REVIEW | tail_inner_cutoff_candidate | FILLED_WORSENED_BASELINE_TRANSFER | P0_DIRECT_SOURCE_NATIVE_REQUIRED | 0.339334 | 0.339334 | 0.339334 |
| UGC06917 | K_scale_tail_spiral | P2_SOURCE_NORMALIZATION_REVIEW | tail_inner_cutoff_candidate | FILLED_WORSENED_BASELINE_TRANSFER | P0_DIRECT_SOURCE_NATIVE_REQUIRED | 0.885803 | 0.885803 | 0.885803 |
| UGC06983 | K_scale_tail_spiral | P2_SOURCE_NORMALIZATION_REVIEW | tail_inner_cutoff_candidate | FILLED_WORSENED_BASELINE_TRANSFER | P0_DIRECT_SOURCE_NATIVE_REQUIRED | 0.677872 | 0.677872 | 0.677872 |
| NGC0024 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | thickness_h_over_rs_candidate | FILLED_WORSENED_BASELINE_TRANSFER | P0_DIRECT_SOURCE_NATIVE_REQUIRED | 0.0963948 | 0.0963948 | 0.0963948 |
| NGC2683 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | thickness_h_over_rs_candidate | FILLED_WORSENED_BASELINE_TRANSFER | P0_DIRECT_SOURCE_NATIVE_REQUIRED | 0.890204 | 0.890204 | 0.890204 |
| NGC3726 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | thickness_h_over_rs_candidate | FILLED_WORSENED_BASELINE_TRANSFER | P0_DIRECT_SOURCE_NATIVE_REQUIRED | 0.469746 | 0.469746 | 0.469746 |
| NGC3949 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | thickness_h_over_rs_candidate | FILLED_WORSENED_BASELINE_TRANSFER | P0_DIRECT_SOURCE_NATIVE_REQUIRED | 0.125025 | 0.125025 | 0.125025 |
| NGC4088 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | thickness_h_over_rs_candidate | FILLED_WORSENED_BASELINE_TRANSFER | P0_DIRECT_SOURCE_NATIVE_REQUIRED | 0.64399 | 0.64399 | 0.64399 |
| NGC5907 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | thickness_h_over_rs_candidate | FILLED_WORSENED_BASELINE_TRANSFER | P0_DIRECT_SOURCE_NATIVE_REQUIRED | 0.629947 | 0.629947 | 0.629947 |
| NGC5985 | K_compact_finite | P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | compact_support_candidate | FILLED_IMPROVED_MATCHED_AND_BASELINES | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | -6.3057 | -6.3057 | -6.3057 |
| UGC00891 | K_scale_tail_spiral | P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | tail_inner_cutoff_candidate | FILLED_IMPROVED_MATCHED_AND_BASELINES | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | -0.656043 | -0.656043 | -0.656043 |
| UGC04499 | K_scale_tail_spiral | P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | tail_inner_cutoff_candidate | FILLED_IMPROVED_MATCHED_AND_BASELINES | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | -0.428548 | -0.428548 | -0.428548 |
| UGC05829 | K_scale_tail_spiral | P1_INCLINATION_PROJECTION_REVIEW | tail_inner_cutoff_candidate | FILLED_IMPROVED_MATCHED_AND_BASELINES | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | -0.747652 | -0.747652 | -0.747652 |
| NGC3972 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | thickness_h_over_rs_candidate | FILLED_IMPROVED_MATCHED_AND_BASELINES | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | -0.129056 | -0.129056 | -0.129056 |
| NGC4389 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | thickness_h_over_rs_candidate | FILLED_IMPROVED_MATCHED_AND_BASELINES | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | -0.012962 | -0.012962 | -0.012962 |

## Claim Boundary

These rows are residual-blind diagnostics over already computed stress tests. They identify acquisition and promotion targets; they are not empirical validation and not accepted endpoint scoring.
