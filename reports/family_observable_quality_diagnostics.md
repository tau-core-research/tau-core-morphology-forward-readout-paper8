# Family Observable Quality Diagnostics

This diagnostic joins the train-selected shrinkage scores with the
residual-blind morphology parameter manifest. It asks whether weak
family rows are primarily data/manifest-quality limited or formula/
normalization limited under the current available-data proxy setup.

## Holdout Family Quality Map

| formula_family | n_galaxies | mean_manifest_confidence | any_quality_caveat_fraction | low_inclination_fraction | large_distance_error_fraction | few_rotation_points_fraction | matched_beats_wrong_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | quality_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K_thick_flared | 10 | 0.84 | 0.3 | 0.1 | 0 | 0.2 | 0.9 | 0.7 | 0.7 | current_best_case |
| K_compact_finite | 7 | 0.835714 | 0.714286 | 0.285714 | 0.714286 | 0 | 0.571429 | 0.571429 | 0.571429 | quality_limited |
| K_exponential_disk | 7 | 0.857143 | 0.571429 | 0.142857 | 0.571429 | 0.142857 | 0.714286 | 0.285714 | 0.285714 | quality_limited |
| K_scale_tail_spiral | 20 | 0.8325 | 0.6 | 0.25 | 0.45 | 0.25 | 0.9 | 0.4 | 0.7 | quality_limited |

## Clean-vs-Caveated Manifest Comparison

| split | quality_group | n_galaxies | matched_beats_wrong_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | mean_matched_minus_wrong | mean_matched_minus_tpg_v6 | mean_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | clean_manifest_proxy | 20 | 0.9 | 0.5 | 0.75 | -9.67091 | 0.181798 | -1.32058 |
| holdout | quality_caveated | 24 | 0.75 | 0.458333 | 0.5 | -7.62363 | 0.429203 | 0.817235 |
| train | clean_manifest_proxy | 60 | 0.733333 | 0.483333 | 0.5 | -5.27679 | 0.249125 | 0.184748 |
| train | quality_caveated | 71 | 0.859155 | 0.478873 | 0.647887 | -10.3088 | -0.0807379 | -0.916061 |

## Claim Boundary

This is not a new fit and does not choose a new morphology family or
amplitude policy. It is a failure-map diagnostic. If a family is marked
quality-limited, the next step is better residual-blind morphology
observable extraction. If it is formula/normalization-limited, the next
step is a stronger Tau-side source normalization or readout kernel.
