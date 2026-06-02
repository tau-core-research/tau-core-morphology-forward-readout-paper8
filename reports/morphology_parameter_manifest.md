# Morphology Parameter Manifest

This manifest freezes the currently available residual-blind morphology
parameters for Paper 8 preflights. It is an available-data proxy manifest,
not the final hand-curated source-native morphology catalog.

## Outputs

- `data/derived/morphology_parameter_manifest.csv`
- `data/derived/morphology_parameter_manifest_family_counts.csv`
- `data/derived/morphology_parameter_manifest_confidence_summary.csv`

## Family Counts

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

## Confidence Summary

| split | formula_family | n_galaxies | mean_confidence | median_confidence |
| --- | --- | --- | --- | --- |
| holdout | K_compact_finite | 7 | 0.835714 | 0.85 |
| holdout | K_exponential_disk | 7 | 0.857143 | 0.85 |
| holdout | K_scale_tail_spiral | 20 | 0.8325 | 0.85 |
| holdout | K_thick_flared | 10 | 0.84 | 0.9 |
| train | K_compact_finite | 22 | 0.922727 | 1 |
| train | K_exponential_disk | 25 | 0.936 | 1 |
| train | K_scale_tail_spiral | 60 | 0.821667 | 0.85 |
| train | K_thick_flared | 24 | 0.825 | 0.9 |

## Claim Boundary

The manifest does not use endpoint residual gains, required S_tau, or
post-hoc family choice. Its weak point is that scale/cutoff/thickness
parameters are still proxies extracted from available 1D data and metadata.
