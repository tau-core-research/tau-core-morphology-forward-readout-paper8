# UNGC Theta1 Environment Attribution Endpoint v0.1

**Status:** `RETROSPECTIVE_UNGC_THETA1_ENVIRONMENT_SIGNAL_FAIL`

## Five-Fold Out-of-Fold Result

| target | baseline MSE | augmented MSE | reduction | proportional reduction |
| --- | ---: | ---: | ---: | ---: |
| TPG-v6 residual | 0.55427679 | 0.53865584 | 0.01562095 | 2.818% |
| Newtonian residual control | 0.27341801 | 0.22191738 | 0.05150063 | 18.836% |

## Frozen Sign And Null

| quantity | value |
| --- | ---: |
| positive Theta1 coefficient folds | 0/5 |
| standardized fold coefficients | `[-0.2575220630294331, -0.12575218516132822, -0.2008604229958157, -0.10918919960896643, -0.2293909072968394]` |
| shuffle p | 0.164918 |
| shuffle 95th percentile | 0.06597350 |
| observed MSE reduction | 0.01562095 |

## Promotion Gates

| gate | result |
| --- | --- |
| `positive_tpg_oof_mse_reduction` | PASS |
| `theta1_shuffle_p_le_0p05` | FAIL |
| `above_theta1_shuffle_q95` | FAIL |
| `positive_theta1_coefficient_in_4_of_5_folds` | FAIL |
| `tpg_gain_exceeds_newtonian_control` | FAIL |

The catalog, crossmatch, hypothesis, sign, folds, baseline, model, metric, and
controls were frozen before this scorer opened the endpoint. The scorer
verified the source-feature hash.

## Claim Boundary

This is retrospective source-family prevalidation. Even a positive result
would remain compatible with ordinary tidal astrophysics and would not prove
`M_tau`, physical channel descent, or shared-parent covariance.
