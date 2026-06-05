# S4G 75 Scale-Source Subset Endpoint Stress Test

This is a source-subset stress test over galaxies with S4G scale-radius source candidates. It is not an accepted endpoint-validation lane.

## Summary
| split | n_galaxies | hard_beats_wrong_fraction | hard_rank1_fraction | hard_beats_tpg_v6_fraction | hard_beats_mond_fraction | tau_l2_beats_old_l2_fraction | tau_l2_beats_tpg_v6_fraction | tau_l2_beats_mond_fraction | median_hard_minus_wrong | median_tau_l2_minus_tpg_v6 | median_tau_l2_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 75 | 0.9067 | 0.2933 | 0.5200 | 0.5333 | 0.6267 | 0.4000 | 0.4933 | -9.8840 | 0.4840 | 0.0287 |
| holdout | 21 | 0.9524 | 0.2381 | 0.5238 | 0.5714 | 0.6190 | 0.3810 | 0.6190 | -14.6779 | 0.4576 | -0.5407 |
| train | 54 | 0.8889 | 0.3148 | 0.5185 | 0.5185 | 0.6296 | 0.4074 | 0.4444 | -8.7610 | 0.5179 | 0.2163 |

## By Family
| split | formula_family | n_galaxies | hard_beats_wrong_fraction | hard_rank1_fraction | hard_beats_tpg_v6_fraction | hard_beats_mond_fraction | tau_l2_beats_tpg_v6_fraction | tau_l2_beats_mond_fraction | median_hard_minus_wrong | median_tau_l2_minus_tpg_v6 | median_tau_l2_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | K_compact_finite | 2 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | -1.0473 | -1.7364 | -1.3247 |
| holdout | K_exponential_disk | 1 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | -7.5356 | 1.0687 | -2.7966 |
| holdout | K_scale_tail_spiral | 10 | 1.0000 | 0.3000 | 0.3000 | 0.4000 | 0.5000 | 0.7000 | -22.4516 | -0.0767 | -2.0395 |
| holdout | K_thick_flared | 8 | 1.0000 | 0.1250 | 0.7500 | 0.7500 | 0.2500 | 0.5000 | -8.0521 | 2.4010 | 1.2122 |
| train | K_compact_finite | 5 | 0.4000 | 0.4000 | 0.4000 | 0.2000 | 0.4000 | 0.6000 | 3.8069 | 0.4075 | -1.0372 |
| train | K_exponential_disk | 12 | 0.8333 | 0.3333 | 0.4167 | 0.5000 | 0.5000 | 0.4167 | -9.2627 | -0.1202 | 0.4092 |
| train | K_scale_tail_spiral | 20 | 1.0000 | 0.5000 | 0.5000 | 0.4500 | 0.5000 | 0.5000 | -29.1641 | -0.2134 | -0.9129 |
| train | K_thick_flared | 17 | 0.9412 | 0.0588 | 0.6471 | 0.7059 | 0.2353 | 0.3529 | -3.2731 | 1.7014 | 0.2305 |

## Lane Summary
| split | inclusion_lane | allowed_use | n_galaxies |
| --- | --- | --- | --- |
| holdout | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 12 |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 2 |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 7 |
| train | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 35 |
| train | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 4 |
| train | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 15 |

## Repair Status
| split | repair_status | n_galaxies |
| --- | --- | --- |
| holdout | NEEDS_INCLINATION_PROJECTION_REVIEW | 2 |
| holdout | NEEDS_VERTICAL_GEOMETRY_SOURCE | 8 |
| holdout | NO_PROJECTION_SCALE_REPAIR_REQUIRED | 8 |
| holdout | REPAIRABLE_WITH_EXISTING_SCALE_SOURCE_PLUS_DISTANCE_AUDIT | 3 |
| train | NEEDS_INCLINATION_PROJECTION_REVIEW | 7 |
| train | NEEDS_VERTICAL_GEOMETRY_SOURCE | 17 |
| train | NO_PROJECTION_SCALE_REPAIR_REQUIRED | 19 |
| train | REPAIRABLE_WITH_EXISTING_SCALE_SOURCE_PLUS_DISTANCE_AUDIT | 11 |

## Claim Boundary
The 75-row subset is source-richer than the full sample for disk scale, but it still mixes strict, caution, and acquisition lanes. The result is a sensitivity/preflight test, not Tau Core empirical validation.