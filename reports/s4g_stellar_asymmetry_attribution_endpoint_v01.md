# S4G Stellar Asymmetry Attribution Endpoint v0.1

**Status:** `RETROSPECTIVE_S4G_STELLAR_ASYMMETRY_SIGNAL_FAIL`

## Five-Fold Out-of-Fold Result

| target/coordinate | baseline MSE | augmented MSE | reduction | proportional reduction |
| --- | ---: | ---: | ---: | ---: |
| TPG-v6, 3.6 micron A | 0.50984497 | 0.51834705 | -0.00850208 | -1.668% |
| TPG-v6, 4.5 micron A | 0.50984497 | 0.51519876 | -0.00535379 | -1.050% |
| Newtonian control, 3.6 micron A | 0.45778314 | 0.46068248 | -0.00289935 | -0.633% |

## Null And Sign Checks

| quantity | 3.6 micron | 4.5 micron |
| --- | ---: | ---: |
| positive coefficient folds | 2/5 | 0/5 |
| paired-row shuffle p | 0.372314 | 0.292354 |
| shuffle 95th percentile | 0.02245401 | 0.02255314 |

## Promotion Gates

| gate | result |
| --- | --- |
| `source_channel_correlation_ge_0p8` | PASS |
| `positive_tpg_oof_reduction_3p6` | FAIL |
| `positive_tpg_oof_reduction_4p5` | FAIL |
| `shuffle_p_le_0p05_3p6` | FAIL |
| `shuffle_p_le_0p05_4p5` | FAIL |
| `above_shuffle_q95_3p6` | FAIL |
| `above_shuffle_q95_4p5` | FAIL |
| `positive_coefficient_in_4_of_5_folds_3p6` | FAIL |
| `positive_coefficient_in_4_of_5_folds_4p5` | FAIL |
| `tpg_gain_exceeds_newtonian_control` | FAIL |

The source coordinate, sign, broad structural controls, folds, model, metric,
null, and Newtonian control were frozen before this scorer opened the endpoint.

## Claim Boundary

This is retrospective source-family prevalidation. Even a pass would establish
only incremental stellar-asymmetry information, not unique morphological-body
attribution, physical channel descent, or proof of `M_tau`.
