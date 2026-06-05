# S4G75 Filled-Kernel Endpoint Stress Test

This stress test reruns the source-native bridge formula endpoint after overriding the S4G75 repair rows with concrete residual-blind filled kernel observables. It is not accepted validation.

## Holdout Verdict

Holdout galaxies: 21.
Matched formula beats wrong-family mean: 0.9524.
Matched formula beats TPG/v6: 0.4286.
Matched formula beats MOND: 0.5714.
Median matched-minus-wrong: -14.0492.
Median matched-minus-TPG/v6: 0.227829.
Median matched-minus-MOND: -1.34256.

## Filled Versus Old S4G75 Proxy

| split | n_galaxies | filled_improves_matched_rmse_fraction | filled_improves_vs_wrong_fraction | filled_improves_vs_tpg_fraction | filled_improves_vs_mond_fraction | median_filled_minus_old_matched_rmse | median_filled_minus_old_matched_minus_wrong | median_filled_minus_old_matched_minus_tpg | median_filled_minus_old_matched_minus_mond | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 75 | 0.0933 | 0.1067 | 0.1200 | 0.1467 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | s4g75_filled_kernel_endpoint_stress_test_not_validation |
| holdout | 21 | 0.2857 | 0.1905 | 0.2857 | 0.2857 | 0.0000 | 0.0058 | 0.0000 | 0.0000 | s4g75_filled_kernel_endpoint_stress_test_not_validation |
| train | 54 | 0.0185 | 0.0741 | 0.0556 | 0.0926 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | s4g75_filled_kernel_endpoint_stress_test_not_validation |

## Holdout By Family

| split | formula_family | n_galaxies | matched_beats_wrong_fraction | matched_rank1_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | median_matched_minus_wrong | median_matched_minus_tpg_v6 | median_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | K_compact_finite | 2 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | -4.0358 | -3.8355 | -3.4238 |
| holdout | K_exponential_disk | 1 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | -7.5356 | -0.2651 | -4.1304 |
| holdout | K_scale_tail_spiral | 10 | 1.0000 | 0.3000 | 0.3000 | 0.4000 | -21.9689 | 1.1327 | 0.2288 |
| holdout | K_thick_flared | 8 | 1.0000 | 0.1250 | 0.5000 | 0.7500 | -7.9853 | -0.1275 | -2.5729 |

## Holdout Rows Changed By Filled Observables

| galaxy | formula_family | old_rmse_matched_family | filled_rmse_matched_family | filled_minus_old_matched_rmse | filled_minus_old_matched_minus_tpg | filled_minus_old_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- |
| NGC0024 | K_thick_flared | 22.6602 | 22.7566 | 0.0964 | 0.0964 | 0.0964 |
| NGC2683 | K_thick_flared | 9.4417 | 10.3319 | 0.8902 | 0.8902 | 0.8902 |
| NGC3726 | K_thick_flared | 22.3278 | 22.7976 | 0.4697 | 0.4697 | 0.4697 |
| NGC3949 | K_thick_flared | 8.5532 | 8.6782 | 0.1250 | 0.1250 | 0.1250 |
| NGC3972 | K_thick_flared | 8.5940 | 8.4649 | -0.1291 | -0.1291 | -0.1291 |
| NGC4088 | K_thick_flared | 37.8114 | 38.4554 | 0.6440 | 0.6440 | 0.6440 |
| NGC4214 | K_scale_tail_spiral | 15.4060 | 15.7453 | 0.3393 | 0.3393 | 0.3393 |
| NGC4389 | K_thick_flared | 45.9879 | 45.9750 | -0.0130 | -0.0130 | -0.0130 |
| NGC5907 | K_thick_flared | 16.3834 | 17.0133 | 0.6299 | 0.6299 | 0.6299 |
| NGC5985 | K_compact_finite | 66.2024 | 59.8967 | -6.3057 | -6.3057 | -6.3057 |
| UGC00891 | K_scale_tail_spiral | 7.2253 | 6.5693 | -0.6560 | -0.6560 | -0.6560 |
| UGC04499 | K_scale_tail_spiral | 8.0710 | 7.6425 | -0.4285 | -0.4285 | -0.4285 |
| UGC05829 | K_scale_tail_spiral | 7.7202 | 6.9726 | -0.7477 | -0.7477 | -0.7477 |
| UGC06818 | K_scale_tail_spiral | 13.9016 | 13.9016 | 0.0000 | 0.0000 | 0.0000 |
| UGC06917 | K_scale_tail_spiral | 4.9226 | 5.8084 | 0.8858 | 0.8858 | 0.8858 |
| UGC06983 | K_scale_tail_spiral | 9.7006 | 10.3784 | 0.6779 | 0.6779 | 0.6779 |

## Claim Boundary

The filled observables are concrete but mostly source-constrained or formula-conditional candidates. This is a pre-endpoint stress test, not an empirical Tau Core validation claim.