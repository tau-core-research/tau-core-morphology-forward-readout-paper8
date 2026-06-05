# L2 Weight-Intake Endpoint Preflight

This endpoint preflight scores the residual-blind L2 weight-intake
candidates. It is not validation and does not promote accepted Tau-side
readout-state weights. It asks whether the source-derived candidate
weights already improve over the older coarse mixture proxy.

## Holdout Verdict

- Holdout galaxies: 44
- Beats old L2 mixture proxy: 0.409
- Beats hard source-native matched family: 0.409
- Beats TPG/v6: 0.477
- Beats MOND: 0.432
- Median intake-minus-old-L2 RMSE: 0.84736
- Median intake-minus-MOND RMSE: 0.282598

## Summary

| split | n_galaxies | median_rmse_l2_weight_intake | mean_rmse_l2_weight_intake | beats_old_l2_proxy_fraction | beats_single_matched_fraction | beats_tpg_v6_fraction | beats_mond_fraction | dominant_matches_coarse_family_fraction | median_intake_minus_old_l2_proxy | median_intake_minus_single_matched | median_intake_minus_tpg_v6 | median_intake_minus_mond | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | 44 | 15.5368 | 19.9064 | 0.409091 | 0.409091 | 0.477273 | 0.431818 | 0.136364 | 0.84736 | 0.316261 | 0.220612 | 0.282598 | l2_weight_intake_endpoint_preflight_not_validation |
| train | 131 | 12.9467 | 18.4525 | 0.534351 | 0.465649 | 0.450382 | 0.503817 | 0.229008 | -0.100825 | 0 | 0.12753 | -0.00401125 | l2_weight_intake_endpoint_preflight_not_validation |

## Dominant Intake Family Breakdown

| split | dominant_intake_family | n_galaxies | beats_old_l2_proxy_fraction | beats_tpg_v6_fraction | beats_mond_fraction | median_intake_minus_old_l2_proxy | median_intake_minus_tpg_v6 | median_intake_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | K_compact_finite | 4 | 0.25 | 0 | 0.5 | 4.25725 | 3.62795 | 2.66221 |
| holdout | K_exponential_disk | 15 | 0.4 | 0.466667 | 0.533333 | 2.27498 | 0.91054 | -0.613349 |
| holdout | K_scale_tail_spiral | 16 | 0.375 | 0.5625 | 0.3125 | 0.867245 | -0.109309 | 1.35421 |
| holdout | K_thick_flared | 9 | 0.555556 | 0.555556 | 0.444444 | -2.96397 | -0.142698 | 0.0965235 |
| train | K_compact_finite | 19 | 0.421053 | 0.421053 | 0.315789 | 1.46151 | 1.75008 | 1.86932 |
| train | K_exponential_disk | 28 | 0.571429 | 0.464286 | 0.5 | -0.186952 | 0.33335 | -0.00653476 |
| train | K_scale_tail_spiral | 60 | 0.533333 | 0.433333 | 0.55 | -0.103266 | 0.0994826 | -0.808792 |
| train | K_thick_flared | 24 | 0.583333 | 0.5 | 0.541667 | -2.31731 | -0.101992 | -0.11009 |

## Claim Boundary

The weights were not selected from endpoint residuals. The endpoint score
is a preflight stress test of the intake map, not an accepted readout
state, not a baseline-superiority claim, and not a Tau Core validation.
