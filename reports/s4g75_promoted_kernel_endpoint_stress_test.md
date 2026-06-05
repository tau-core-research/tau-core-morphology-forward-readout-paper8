# S4G75 Promoted-Kernel Endpoint Stress Test

This diagnostic reruns the S4G75 endpoint after replacing filled proxy values with direct S4G kernel measurements where available. It is not accepted validation.

## Holdout Verdict

Holdout galaxies: 21.
Matched formula beats wrong-family mean: 0.9524.
Matched formula beats TPG/v6: 0.4286.
Matched formula beats MOND: 0.5714.

## Promoted Versus Filled

| split | n_galaxies | promoted_improves_old_matched_rmse_fraction | promoted_improves_old_vs_tpg_fraction | promoted_improves_old_vs_mond_fraction | promoted_improves_filled_matched_rmse_fraction | median_promoted_minus_filled_matched_rmse | median_promoted_minus_filled_vs_tpg | median_promoted_minus_filled_vs_mond | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 75 | 0.0933 | 0.1200 | 0.1467 | 0.0400 | 0.0000 | 0.0000 | 0.0000 | s4g75_promoted_kernel_endpoint_stress_test_not_validation |
| holdout | 21 | 0.2857 | 0.2857 | 0.2857 | 0.0952 | 0.0000 | 0.0000 | 0.0000 | s4g75_promoted_kernel_endpoint_stress_test_not_validation |
| train | 54 | 0.0185 | 0.0556 | 0.0926 | 0.0185 | 0.0000 | 0.0000 | 0.0000 | s4g75_promoted_kernel_endpoint_stress_test_not_validation |

## Holdout By Family

| split | formula_family | n_galaxies | matched_beats_wrong_fraction | matched_rank1_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | median_matched_minus_wrong | median_matched_minus_tpg_v6 | median_matched_minus_mond | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | K_compact_finite | 2 | 0.5000 | 0.5000 | 0.5000 | 0.5000 | -8.9679 | -8.7676 | -8.3559 | s4g75_promoted_kernel_endpoint_stress_test_not_validation |
| holdout | K_exponential_disk | 1 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | -7.5356 | -0.2651 | -4.1304 | s4g75_promoted_kernel_endpoint_stress_test_not_validation |
| holdout | K_scale_tail_spiral | 10 | 1.0000 | 0.3000 | 0.3000 | 0.4000 | -21.9689 | 1.1327 | 0.2288 | s4g75_promoted_kernel_endpoint_stress_test_not_validation |
| holdout | K_thick_flared | 8 | 1.0000 | 0.1250 | 0.5000 | 0.7500 | -7.9853 | -0.1275 | -2.5729 | s4g75_promoted_kernel_endpoint_stress_test_not_validation |

## Holdout Rows Changed By Direct Kernel Promotion

| galaxy | formula_family | filled_rmse_matched_family | promoted_rmse_matched_family | promoted_minus_filled_matched_rmse | promoted_minus_filled_matched_minus_tpg | promoted_minus_filled_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | K_thick_flared | 17.0133 | 17.0253 | 0.0120 | 0.0120 | 0.0120 |
| NGC5985 | K_compact_finite | 59.8967 | 50.0325 | -9.8642 | -9.8642 | -9.8642 |

## Claim Boundary

This is a stress diagnostic over a two-row strict kernel-ready subset embedded in the S4G75 lane. It is too small for accepted endpoint validation.
