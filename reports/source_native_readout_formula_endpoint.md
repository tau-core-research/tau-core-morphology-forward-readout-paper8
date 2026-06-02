# Source-Native Bridge Readout Formula Endpoint

This preflight uses the concrete Tau Core bridge morphology formulas as
`delta v^2` readout kernels. It is not yet the final Paper 8 endpoint,
because the morphology scale parameters are still available-data proxies.

## Holdout Verdict

- Holdout galaxies: 44
- Matched bridge formula beats wrong-formula mean: 0.886
- Matched bridge formula rank-1 fraction: 0.295
- Matched bridge formula beats TPG/v6: 0.477
- Matched bridge formula beats MOND: 0.477
- Mean matched-minus-wrong RMSE: -17.6838
- Mean matched-minus-TPG/v6 RMSE: 1.29546
- Mean matched-minus-MOND RMSE: 0.824211

## Shuffled-Label Null

- Shuffles: 1000
- Seed: 31415
- Holdout observed mean matched-minus-wrong: -17.6838
- Holdout shuffled-null mean: -7.02836
- P(null at least as good; mean-minus-wrong): 0.0020
- Holdout observed beats-wrong fraction: 0.886
- Holdout shuffled beats-wrong mean: 0.773
- P(null at least as good; beats-wrong fraction): 0.0060
- Holdout observed rank-1 fraction: 0.295
- Holdout shuffled rank-1 mean: 0.254
- P(null at least as good; rank-1 fraction): 0.3017

## Bridge Formula Amplitudes

| formula_family | beta_delta_v2_amplitude | n_train_points | n_train_galaxies | kernel | formula_source | fit_policy |
| --- | --- | --- | --- | --- | --- | --- |
| K_compact_finite | 108797 | 765 | 22 | kernel_K_compact_finite | tau_core_gravity_rmond_compact_finite_source_readout_formula_001 | least_squares_train_only_on_vobs2_minus_v6_2_over_bridge_formula_kernel |
| K_scale_tail_spiral | 758.092 | 742 | 60 | kernel_K_scale_tail_spiral | tau_core_gravity_rmond_scale_tail_spiral_readout_formula_001:n=2 | least_squares_train_only_on_vobs2_minus_v6_2_over_bridge_formula_kernel |
| K_exponential_disk | -1003.88 | 586 | 25 | kernel_K_exponential_disk | tau_core_gravity_rmond_exponential_disk_readout_formula_001:Freeman_Bessel | least_squares_train_only_on_vobs2_minus_v6_2_over_bridge_formula_kernel |
| K_thick_flared | -522.962 | 461 | 24 | kernel_K_thick_flared | tau_core_gravity_rmond_thick_flared_disk_readout_formula_001:constant_h_exponential_vertical | least_squares_train_only_on_vobs2_minus_v6_2_over_bridge_formula_kernel |

## Holdout By Family

| split | formula_family | n_galaxies | matched_beats_wrong_fraction | matched_rank1_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | median_matched_minus_wrong | median_matched_minus_tpg_v6 | median_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | K_compact_finite | 7 | 0.571429 | 0.571429 | 0.571429 | 0.571429 | -0.427522 | -0.15256 | -0.179075 |
| holdout | K_exponential_disk | 7 | 0.857143 | 0.142857 | 0.285714 | 0.285714 | -10.251 | 1.93808 | 4.33761 |
| holdout | K_scale_tail_spiral | 20 | 1 | 0.35 | 0.4 | 0.4 | -22.4516 | 1.50648 | 0.228813 |
| holdout | K_thick_flared | 10 | 0.9 | 0.1 | 0.7 | 0.7 | -4.54121 | -0.485566 | -2.62895 |

## Label Counts

| split | formula_family | n_galaxies |
| --- | --- | --- |
| holdout | K_compact_finite | 7 |
| holdout | K_exponential_disk | 7 |
| holdout | K_scale_tail_spiral | 20 |
| holdout | K_thick_flared | 10 |
| train | K_compact_finite | 22 |
| train | K_exponential_disk | 25 |
| train | K_scale_tail_spiral | 60 |
| train | K_thick_flared | 24 |

## Claim Boundary

This is a source-native formula-shape preflight, not empirical validation.
The weak link is the available-data morphology scale proxy, not the bridge
formula registry itself. A final endpoint requires source-native
morphology scale extraction and a nonleaky amplitude policy.
