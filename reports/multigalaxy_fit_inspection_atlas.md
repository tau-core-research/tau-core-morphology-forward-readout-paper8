# Multi-Galaxy Fit Inspection Atlas

This diagnostic inspects several galaxies with available SPARC rotation
points and morphology-manifest inputs. It reuses the source-native bridge
formula pipeline and scores against observed rotation curves. It is an
endpoint diagnostic only, not a validation endpoint.

## Overview

| diagnostic_id | n_selected_galaxies | n_families | n_tau_matched_beats_best_baseline | selection_policy | uses_vobs_for_generation | uses_vobs_for_scoring | validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MULTIGALAXY_FIT_INSPECTION_ATLAS | 9 | 4 | 5 | predeclared_diverse_available_data_examples_plus_stress_cases | False | True | False | multigalaxy_fit_inspection_atlas_endpoint_diagnostic_not_validation |

## Atlas

![Multi-galaxy fit inspection atlas](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/reports/multigalaxy_fit_inspection_atlas.png)

## Selected Galaxies and Availability

| galaxy | formula_family | type_bin | inc_bin | manifest_confidence | manifest_caveat | n_points | best_baseline_model | tau_matched_beats_best_baseline |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IC2574 | K_scale_tail_spiral | irregular_T_ge_9 | inc_high_60_80 | 1 | none | 34 | TPG_V6 | False |
| IC4202 | K_compact_finite | mid_T_3_5 | inc_edge_ge_80 | 1 | none | 32 | TPG_V6 | True |
| NGC4013 | K_compact_finite | mid_T_3_5 | inc_edge_ge_80 | 1 | none | 36 | TPG_V6 | False |
| NGC4088 | K_thick_flared | mid_T_3_5 | inc_high_60_80 | 0.9 | vertical_geometry_proxy_only | 12 | NEWTONIAN_vn | False |
| NGC4183 | K_exponential_disk | late_T_6_8 | inc_edge_ge_80 | 1 | none | 23 | TPG_V6 | True |
| NGC5907 | K_thick_flared | mid_T_3_5 | inc_edge_ge_80 | 0.9 | vertical_geometry_proxy_only | 19 | TPG_V6 | True |
| NGC7331 | K_thick_flared | mid_T_3_5 | inc_high_60_80 | 0.9 | vertical_geometry_proxy_only | 36 | TPG_V6 | True |
| UGC05716 | K_scale_tail_spiral | irregular_T_ge_9 | inc_mid_40_60 | 0.85 | large_distance_error | 12 | MOND | True |
| UGC12506 | K_exponential_disk | late_T_6_8 | inc_edge_ge_80 | 1 | none | 31 | MOND | False |

## RMSE by Model

| galaxy | MOND | NEWTONIAN_vn | TAU_BEST_FAMILY | TAU_MATCHED | TPG_V6 |
| --- | --- | --- | --- | --- | --- |
| IC2574 | 13.5132 | 23.7835 | 3.11332 | 10.567 | 7.51382 |
| IC4202 | 26.128 | 69.1216 | 25.949 | 25.949 | 26.1015 |
| NGC4013 | 14.3342 | 65.6913 | 10.8802 | 16.9936 | 12.2739 |
| NGC4088 | 42.1838 | 25.3963 | 36.4889 | 37.8114 | 38.9877 |
| NGC4183 | 10.355 | 48.4109 | 5.86059 | 6.22458 | 6.48969 |
| NGC5907 | 18.5954 | 86.4837 | 16.3834 | 16.3834 | 16.7855 |
| NGC7331 | 29.3117 | 59.3544 | 23.473 | 24.5226 | 25.4851 |
| UGC05716 | 5.60565 | 38.5957 | 4.21204 | 4.21204 | 5.84487 |
| UGC12506 | 38.1227 | 116.023 | 37.3633 | 44.9992 | 40.6978 |

## NGC4088 Warp/History Cross-Check

NGC4088 is intentionally included as a stress case. In the generic
source-native family atlas it is treated as the current thick/flared
proxy row, and that generic row is not the good fit. The separate
targeted warp/history diagnostic is different: it uses the source-built
warp branches p1/p2 and the bounded epsilon_cross modulation.

| galaxy | generic_family_atlas_tau_rmse | targeted_warp_fixed_tau_rmse | targeted_warp_bounded_tau_rmse | interpretation |
| --- | --- | --- | --- | --- |
| NGC4088 | 37.8114 | 12.1897 | 6.92711 | correct_readout_subfamily_matters |

## Claim Boundary

The selected set deliberately mixes encouraging rows and stress rows.
The diagnostic answers whether the current executable readout curves look
plausible across varied available-data cases. It does not prove population
superiority over TPG/MOND/Newton and does not replace the frozen endpoint
protocol.
