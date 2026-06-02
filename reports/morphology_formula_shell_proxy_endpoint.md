# Morphology Formula-Shell Proxy Endpoint

This is an available-data preflight for morphology-specific formula shells.
It is closer to the final Paper 8 target than the single-channel Tau proxy,
but it is still not the final endpoint because the shell features are
dimensionless radial proxies built from available SPARC-like metadata.

## Holdout Verdict

- Holdout galaxies: 44
- Matched shell beats wrong-shell mean: 0.500
- Matched shell rank-1 fraction: 0.295
- Matched shell beats TPG/v6: 0.477
- Matched shell beats MOND: 0.591
- Mean matched-minus-wrong RMSE: 0.00150059
- Mean matched-minus-TPG/v6 RMSE: 0.104294
- Mean matched-minus-MOND RMSE: -0.366951

## Shuffled-Label Null

- Shuffles: 1000
- Seed: 2718
- Holdout observed mean matched-minus-wrong: 0.00150059
- Holdout shuffled-null mean: 0.00489545
- P(null at least as good; mean-minus-wrong): 0.4785
- Holdout observed beats-wrong fraction: 0.500
- Holdout shuffled beats-wrong mean: 0.518
- P(null at least as good; beats-wrong fraction): 0.6843
- Holdout observed rank-1 fraction: 0.295
- Holdout shuffled rank-1 mean: 0.277
- P(null at least as good; rank-1 fraction): 0.4406

## Shell Amplitudes

| formula_family | beta | n_train_points | n_train_galaxies | feature | fit_policy |
| --- | --- | --- | --- | --- | --- |
| K_compact_finite | 5.24841 | 765 | 22 | shell_K_compact_finite | least_squares_train_only_on_vobs_minus_v6_over_predeclared_shell_feature |
| K_scale_tail_spiral | 3.65848 | 742 | 60 | shell_K_scale_tail_spiral | least_squares_train_only_on_vobs_minus_v6_over_predeclared_shell_feature |
| K_exponential_disk | 1.12838 | 586 | 25 | shell_K_exponential_disk | least_squares_train_only_on_vobs_minus_v6_over_predeclared_shell_feature |
| K_thick_flared | -4.58013 | 461 | 24 | shell_K_thick_flared | least_squares_train_only_on_vobs_minus_v6_over_predeclared_shell_feature |

## Holdout By Family

| split | formula_family | n_galaxies | matched_beats_wrong_fraction | matched_rank1_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | median_matched_minus_wrong | median_matched_minus_tpg_v6 | median_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | K_compact_finite | 7 | 0.285714 | 0.285714 | 0.285714 | 0.285714 | 1.21068 | 1.20513 | 0.996602 |
| holdout | K_exponential_disk | 7 | 0.857143 | 0 | 0.714286 | 0.428571 | -0.151501 | -0.262732 | 2.1368 |
| holdout | K_scale_tail_spiral | 20 | 0.4 | 0.25 | 0.4 | 0.7 | 0.888937 | 0.958384 | -0.41503 |
| holdout | K_thick_flared | 10 | 0.6 | 0.6 | 0.6 | 0.7 | -1.53667 | -0.922146 | -3.948 |

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

This is a preparation endpoint, not empirical validation. A strong final
Paper 8 result still requires source-native morphology labels, physically
audited 4D readout shells, dimensional checks, and baseline comparisons
including Newtonian/RAR layers where available.
