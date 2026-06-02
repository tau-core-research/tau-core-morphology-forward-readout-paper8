# Morphology-Matched Tau-Proxy Endpoint

This is the first proxy implementation of the Paper 8 matched-family idea:
galaxy morphology metadata selects a Tau-proxy family, family amplitudes
are fit on the train split only, and the holdout split is scored against
wrong families, TPG/v6, and MOND.

It is not the final Paper 8 endpoint because the families are still proxy
families built from the available `rparent_cd` channel rather than the
final morphology-specific `delta_g^K` formula shells.

## Holdout Verdict

- Holdout galaxies: 44
- Matched family beats wrong-family mean: 0.568
- Matched family rank-1 fraction: 0.250
- Matched family beats TPG/v6: 0.636
- Matched family beats MOND: 0.614
- Mean matched-minus-wrong RMSE: -0.0326133
- Mean matched-minus-TPG/v6 RMSE: -0.0806188
- Mean matched-minus-MOND RMSE: -0.551864

## Shuffled-Label Null

The morphology labels are shuffled within each split with a deterministic
seed (`1729`) and 1000 permutations. Lower
matched-minus-wrong is better for the RMSE endpoint.

- Holdout observed mean matched-minus-wrong: -0.0326133
- Holdout shuffled-null mean: 0.0132684
- Holdout shuffled-null median: 0.0133246
- P(null at least as good; mean-minus-wrong): 0.2637
- Holdout observed beats-wrong fraction: 0.568
- Holdout shuffled beats-wrong mean: 0.541
- P(null at least as good; beats-wrong fraction): 0.4316
- Holdout observed rank-1 fraction: 0.250
- Holdout shuffled rank-1 mean: 0.198
- P(null at least as good; rank-1 fraction): 0.2298

## Family Amplitudes

| morphology_family | beta | n_train_points | n_train_galaxies | fit_policy |
| --- | --- | --- | --- | --- |
| K_compact_bulge | -18.2774 | 765 | 22 | least_squares_train_only_on_vobs_minus_v6_over_rparent_cd |
| K_diffuse_scale_tail | -0.548069 | 742 | 60 | least_squares_train_only_on_vobs_minus_v6_over_rparent_cd |
| K_global_tau_proxy | -11.2825 | 2554 | 131 | global_train_only_reference |
| K_late_exponential | 0.565161 | 586 | 25 | least_squares_train_only_on_vobs_minus_v6_over_rparent_cd |
| K_mid_regular | -10.1324 | 461 | 24 | least_squares_train_only_on_vobs_minus_v6_over_rparent_cd |

## Holdout By Family

| split | morphology_family | n_galaxies | matched_beats_wrong_fraction | matched_rank1_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | median_matched_minus_wrong | median_matched_minus_tpg_v6 | median_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | K_compact_bulge | 7 | 0.571429 | 0.428571 | 0.571429 | 0.714286 | -0.0767775 | -0.115059 | -1.35376 |
| holdout | K_diffuse_scale_tail | 20 | 0.55 | 0.2 | 0.7 | 0.6 | -0.013374 | -0.00306811 | -1.72341 |
| holdout | K_late_exponential | 7 | 0.571429 | 0.571429 | 0.571429 | 0.428571 | -0.0139028 | -7.40256e-05 | 2.39402 |
| holdout | K_mid_regular | 10 | 0.6 | 0 | 0.6 | 0.7 | -0.0280942 | -0.0627481 | -2.2703 |

## Label Counts

| split | morphology_family | n_galaxies |
| --- | --- | --- |
| holdout | K_compact_bulge | 7 |
| holdout | K_diffuse_scale_tail | 20 |
| holdout | K_late_exponential | 7 |
| holdout | K_mid_regular | 10 |
| train | K_compact_bulge | 22 |
| train | K_diffuse_scale_tail | 60 |
| train | K_late_exponential | 25 |
| train | K_mid_regular | 24 |

## Claim Boundary

A positive matched-vs-wrong result here would be a useful preflight signal.
It is not a claim that final Tau Core morphology readout formulas beat
TGP/RMOND/MOND/Newtonian. RMOND and Newtonian are not both available in
this 175-galaxy point-level runner.
