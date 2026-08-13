# UNGC Theta1 Environment Attribution Freeze v0.1

**Status:** `SOURCE_ONLY_THETA1_ENVIRONMENT_FREEZE_READY`

This freeze selects one theory-derived environment coordinate: the UNGC
dominant-neighbor tidal index `Theta1`. Higher values are frozen to predict
higher low-acceleration residual burden through the environment-channel
coupling hypothesis.

| quantity | value |
| --- | ---: |
| usable galaxies | 36 |
| folds | 5 |
| fold counts | `{'0': 5, '1': 7, '2': 11, '3': 8, '4': 5}` |
| baseline features | 6 |
| environment features | 1 |

The source builder reads no velocity endpoint, residual, model RMSE, or score.
The hypothesis, sign, folds, baseline, model, metrics, controls, and promotion
rule are frozen before the separate endpoint scorer runs.

This is retrospective prevalidation. A positive result would remain compatible
with ordinary tidal astrophysics and would not prove `M_tau`.
