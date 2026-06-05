# S4G75 Source-Rich Lane Action Plan

The S4G75 lane is the current source-rich scale-radius subset. This plan keeps it separate from the full 175-row stress sample and lists the next residual-blind source repairs.

## Verdict

S4G75 rows: 75.
Holdout S4G75 rows: 15.
P0 existing-scale plus distance-audit rows: 14.
P1 projection/vertical-geometry rows: 34.

The next improvement should stay on the 75-row source-rich lane first. The full 175-row sample remains useful as a stress/acquisition lane, but not as the main accepted-claim lane.

## Source Action Summary
| split | repair_priority | source_targets | n_galaxies | n_hard_specific | median_matched_minus_wrong | median_source_norm_minus_tpg_v6 | median_source_norm_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | S4G;SPARC_DISTANCE;NED_NEDD | 3 | 3 | -18.6148 | -0.8856 | -3.1339 |
| holdout | P1_INCLINATION_PROJECTION_REVIEW | NED_NEDD;S4G;SPARC_METADATA | 2 | 2 | -24.8062 | -0.4710 | -0.3070 |
| holdout | P1_VERTICAL_GEOMETRY_SOURCE | S4G;DustPedia;HI_SURVEYS;PHANGS_IF_AVAILABLE | 8 | 8 | -8.0521 | 2.4010 | 1.2122 |
| holdout | P2_SOURCE_NORMALIZATION_REVIEW | S4G;SPARC_BARYONIC;HI_SURVEYS | 2 | 2 | -11.3877 | 0.9919 | 2.8438 |
| train | P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | S4G;SPARC_DISTANCE;NED_NEDD | 11 | 10 | -16.7254 | 0.6398 | 0.4742 |
| train | P1_INCLINATION_PROJECTION_REVIEW | NED_NEDD;S4G;SPARC_METADATA | 7 | 7 | -18.8308 | 0.0244 | -1.9743 |
| train | P1_VERTICAL_GEOMETRY_SOURCE | S4G;DustPedia;HI_SURVEYS;PHANGS_IF_AVAILABLE | 17 | 16 | -3.2731 | 1.7014 | 0.2305 |
| train | P2_SOURCE_NORMALIZATION_REVIEW | S4G;SPARC_BARYONIC;HI_SURVEYS | 3 | 3 | -22.3146 | 1.3758 | 3.9453 |

## Lane Context
| split | inclusion_lane | allowed_use | n_s4g75_galaxies | hard_beats_wrong_fraction | tau_l2_beats_tpg_v6_fraction | tau_l2_beats_mond_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| holdout | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 12 | 0.9167 | 0.3333 | 0.8333 |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 2 | 1.0000 | 0.5000 | 0.5000 |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 7 | 1.0000 | 0.4286 | 0.2857 |
| train | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 35 | 0.9429 | 0.4571 | 0.5429 |
| train | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 4 | 0.5000 | 0.2500 | 0.2500 |
| train | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 15 | 0.8667 | 0.3333 | 0.2667 |

## Holdout Repair Queue
| galaxy | formula_family | repair_priority | repair_status | failure_mode | source_targets | residual_blind_action |
| --- | --- | --- | --- | --- | --- | --- |
| NGC5985 | K_compact_finite | P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | REPAIRABLE_WITH_EXISTING_SCALE_SOURCE_PLUS_DISTANCE_AUDIT | SPECIFICITY_TRANSFERS_TO_BOTH_BASELINES | S4G;SPARC_DISTANCE;NED_NEDD | audit existing S4G scale radius against distance/projection caveat and freeze usable scale if residual-blind consistency passes |
| UGC00891 | K_scale_tail_spiral | P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | REPAIRABLE_WITH_EXISTING_SCALE_SOURCE_PLUS_DISTANCE_AUDIT | SPECIFICITY_TRANSFERS_TO_BOTH_BASELINES | S4G;SPARC_DISTANCE;NED_NEDD | audit existing S4G scale radius against distance/projection caveat and freeze usable scale if residual-blind consistency passes |
| UGC04499 | K_scale_tail_spiral | P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT | REPAIRABLE_WITH_EXISTING_SCALE_SOURCE_PLUS_DISTANCE_AUDIT | SPECIFICITY_TRANSFERS_TO_BOTH_BASELINES | S4G;SPARC_DISTANCE;NED_NEDD | audit existing S4G scale radius against distance/projection caveat and freeze usable scale if residual-blind consistency passes |
| NGC4214 | K_scale_tail_spiral | P1_INCLINATION_PROJECTION_REVIEW | NEEDS_INCLINATION_PROJECTION_REVIEW | SPECIFICITY_PARTLY_TRANSFERS_TO_BASELINES | NED_NEDD;S4G;SPARC_METADATA | review inclination, distance uncertainty, and projection caveats before using scale-sensitive readout |
| UGC05829 | K_scale_tail_spiral | P1_INCLINATION_PROJECTION_REVIEW | NEEDS_INCLINATION_PROJECTION_REVIEW | SPECIFICITY_PARTLY_TRANSFERS_TO_BASELINES | NED_NEDD;S4G;SPARC_METADATA | review inclination, distance uncertainty, and projection caveats before using scale-sensitive readout |
| NGC0024 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | NEEDS_VERTICAL_GEOMETRY_SOURCE | SPECIFICITY_SURVIVES_PROJECTION_SCALE_REPAIR_NEEDED | S4G;DustPedia;HI_SURVEYS;PHANGS_IF_AVAILABLE | seek vertical thickness, flare, warp, edge/projection, or gas-plane evidence for thick/flared readout support |
| NGC2683 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | NEEDS_VERTICAL_GEOMETRY_SOURCE | SPECIFICITY_PARTLY_TRANSFERS_TO_BASELINES | S4G;DustPedia;HI_SURVEYS;PHANGS_IF_AVAILABLE | seek vertical thickness, flare, warp, edge/projection, or gas-plane evidence for thick/flared readout support |
| NGC3726 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | NEEDS_VERTICAL_GEOMETRY_SOURCE | SPECIFICITY_SURVIVES_PROJECTION_SCALE_REPAIR_NEEDED | S4G;DustPedia;HI_SURVEYS;PHANGS_IF_AVAILABLE | seek vertical thickness, flare, warp, edge/projection, or gas-plane evidence for thick/flared readout support |
| NGC3949 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | NEEDS_VERTICAL_GEOMETRY_SOURCE | SPECIFICITY_SURVIVES_PROJECTION_SCALE_REPAIR_NEEDED | S4G;DustPedia;HI_SURVEYS;PHANGS_IF_AVAILABLE | seek vertical thickness, flare, warp, edge/projection, or gas-plane evidence for thick/flared readout support |
| NGC3972 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | NEEDS_VERTICAL_GEOMETRY_SOURCE | SPECIFICITY_TRANSFERS_TO_BOTH_BASELINES | S4G;DustPedia;HI_SURVEYS;PHANGS_IF_AVAILABLE | seek vertical thickness, flare, warp, edge/projection, or gas-plane evidence for thick/flared readout support |
| NGC4088 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | NEEDS_VERTICAL_GEOMETRY_SOURCE | SPECIFICITY_SURVIVES_PROJECTION_SCALE_REPAIR_NEEDED | S4G;DustPedia;HI_SURVEYS;PHANGS_IF_AVAILABLE | seek vertical thickness, flare, warp, edge/projection, or gas-plane evidence for thick/flared readout support |
| NGC4389 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | NEEDS_VERTICAL_GEOMETRY_SOURCE | SPECIFICITY_TRANSFERS_TO_BOTH_BASELINES | S4G;DustPedia;HI_SURVEYS;PHANGS_IF_AVAILABLE | seek vertical thickness, flare, warp, edge/projection, or gas-plane evidence for thick/flared readout support |
| NGC5907 | K_thick_flared | P1_VERTICAL_GEOMETRY_SOURCE | NEEDS_VERTICAL_GEOMETRY_SOURCE | SPECIFICITY_PARTLY_TRANSFERS_TO_BASELINES | S4G;DustPedia;HI_SURVEYS;PHANGS_IF_AVAILABLE | seek vertical thickness, flare, warp, edge/projection, or gas-plane evidence for thick/flared readout support |
| UGC06917 | K_scale_tail_spiral | P2_SOURCE_NORMALIZATION_REVIEW | NO_PROJECTION_SCALE_REPAIR_REQUIRED | SPECIFICITY_SURVIVES_NORMALIZATION_WEAK | S4G;SPARC_BARYONIC;HI_SURVEYS | inspect source-normalization inputs after projection/scale-clean status; do not tune from endpoint residuals |
| UGC06983 | K_scale_tail_spiral | P2_SOURCE_NORMALIZATION_REVIEW | NO_PROJECTION_SCALE_REPAIR_REQUIRED | SPECIFICITY_SURVIVES_NORMALIZATION_WEAK | S4G;SPARC_BARYONIC;HI_SURVEYS | inspect source-normalization inputs after projection/scale-clean status; do not tune from endpoint residuals |

## Claim Boundary
This action plan does not create accepted labels, does not run a new endpoint, and does not claim empirical validation. It identifies which source evidence should be acquired or reviewed before the next frozen S4G75 source-rich endpoint stress test.