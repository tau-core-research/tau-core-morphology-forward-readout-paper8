# Manifest Confidence Diagnostics

This diagnostic asks whether the source-native bridge formula endpoint
improves when restricted to higher-confidence morphology-parameter
manifest subsets. It is a data-quality and manifest-quality diagnostic,
not a new fit.

## Holdout Subsets

| subset | n_galaxies | mean_confidence | matched_beats_wrong_fraction | matched_rank1_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | mean_matched_minus_wrong | median_matched_minus_wrong | mean_matched_minus_tpg_v6 | median_matched_minus_tpg_v6 | mean_matched_minus_mond | median_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout:all | 44 | 0.838636 | 0.886364 | 0.295455 | 0.477273 | 0.477273 | -17.6838 | -13.9742 | 1.29546 | 0.644948 | 0.824211 | 0.173401 |
| holdout:confidence_ge_0_75 | 32 | 0.91875 | 0.90625 | 0.375 | 0.53125 | 0.46875 | -18.4883 | -10.8174 | 1.36233 | -0.208836 | 0.890472 | 0.173401 |
| holdout:confidence_ge_0_85 | 30 | 0.926667 | 0.9 | 0.333333 | 0.5 | 0.466667 | -15.3421 | -9.85972 | 1.68469 | 0.174901 | 1.07425 | 0.228813 |
| holdout:confidence_ge_0_95 | 13 | 1 | 0.846154 | 0.307692 | 0.384615 | 0.307692 | -23.9546 | -16.186 | 2.30662 | 2.80844 | 0.981832 | 0.307546 |
| holdout:no_large_distance_error | 26 | 0.907692 | 0.884615 | 0.269231 | 0.538462 | 0.5 | -20.7466 | -13.9742 | 0.85666 | -0.208836 | -0.357516 | -0.0259862 |
| holdout:no_low_inclination | 35 | 0.894286 | 0.914286 | 0.314286 | 0.514286 | 0.514286 | -18.87 | -14.0923 | 1.41485 | -0.15256 | 0.680905 | -0.156779 |
| holdout:no_manifest_caveat | 13 | 1 | 0.846154 | 0.307692 | 0.384615 | 0.307692 | -23.9546 | -16.186 | 2.30662 | 2.80844 | 0.981832 | 0.307546 |

## Holdout Shuffled Nulls

| subset | n_shuffles | seed | observed_mean_minus_wrong | null_mean_minus_wrong_mean | p_mean_minus_wrong_at_least_as_good | observed_beats_wrong_fraction | null_beats_wrong_fraction_mean | p_beats_wrong_fraction_at_least_as_good | observed_rank1_fraction | null_rank1_fraction_mean | p_rank1_fraction_at_least_as_good |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout:all | 1000 | 16180 | -17.6838 | -7.09465 | 0.003996 | 0.886364 | 0.775114 | 0.00999001 | 0.295455 | 0.254364 | 0.298701 |
| holdout:confidence_ge_0_75 | 1000 | 16180 | -18.4883 | -7.69872 | 0.00899101 | 0.90625 | 0.799125 | 0.026973 | 0.375 | 0.2815 | 0.138861 |
| holdout:confidence_ge_0_85 | 1000 | 16180 | -15.3421 | -5.94565 | 0.00999001 | 0.9 | 0.7858 | 0.027972 | 0.333333 | 0.265267 | 0.235764 |
| holdout:confidence_ge_0_95 | 1000 | 16180 | -23.9546 | -9.31463 | 0.0689311 | 0.846154 | 0.836231 | 0.653347 | 0.307692 | 0.242308 | 0.390609 |
| holdout:no_large_distance_error | 1000 | 16180 | -20.7466 | -14.7588 | 0.117882 | 0.884615 | 0.840385 | 0.25974 | 0.269231 | 0.208385 | 0.283716 |
| holdout:no_low_inclination | 1000 | 16180 | -18.87 | -8.47223 | 0.00599401 | 0.914286 | 0.811686 | 0.012987 | 0.314286 | 0.260543 | 0.26973 |
| holdout:no_manifest_caveat | 1000 | 16180 | -23.9546 | -9.31463 | 0.0689311 | 0.846154 | 0.836231 | 0.653347 | 0.307692 | 0.242308 | 0.390609 |

## Claim Boundary

If high-confidence subsets improve baseline performance, the bottleneck is
likely morphology parameter quality. If they do not, the bottleneck is
more likely amplitude policy, formula normalization, or missing source-native
morphology observables.
