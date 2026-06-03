# Readout-Mixture Proxy Endpoint

This diagnostic keeps the same concrete bridge formula kernels as the
source-native endpoint, but replaces hard morphology-family selection by
a residual-blind proxy mixture over readout components. It is not an
accepted Tau-side readout state and not a final endpoint.

## Holdout Verdict

- Holdout galaxies: 44
- Mixture beats hard matched family: 0.455
- Mixture beats TPG/v6: 0.500
- Mixture beats MOND: 0.455
- Mean mixture-minus-hard-family RMSE: 1.75933
- Mean mixture-minus-TPG/v6 RMSE: 3.05479
- Mean mixture-minus-MOND RMSE: 2.58354

## Summary

| split | n_galaxies | mixture_beats_single_matched_fraction | mixture_beats_tpg_v6_fraction | mixture_beats_mond_fraction | mean_mixture_minus_single_matched | median_mixture_minus_single_matched | mean_mixture_minus_tpg_v6 | median_mixture_minus_tpg_v6 | mean_mixture_minus_mond | median_mixture_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | 44 | 0.454545 | 0.5 | 0.454545 | 1.75933 | 0.445057 | 3.05479 | 0.111816 | 2.58354 | 0.298487 |
| train | 131 | 0.435115 | 0.419847 | 0.458015 | 1.939 | 0.343317 | 2.49149 | 0.40461 | 2.00927 | 0.20171 |

## Mixture Weight Counts

| split | dominant_mixture_family | n_galaxies |
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

This is not an accepted Tau-side readout state.
The weights are available-data morphology proxies. They are not inferred
from endpoint residuals, but they are also not accepted Tau-side readout
states. A future run must replace them with residual-blind source-native
readout-state or morphology-memory observables.
