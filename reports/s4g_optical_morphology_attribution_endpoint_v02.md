# S4G Optical Morphology Attribution Endpoint v0.2

**Status:** `RETROSPECTIVE_S4G_OPTICAL_MORPHOLOGY_INCREMENTAL_SIGNAL_FAIL`

## Frozen Holdout Result

| target | baseline MSE | augmented MSE | reduction | proportional reduction |
| --- | ---: | ---: | ---: | ---: |
| projection residual | 0.37528793 | 0.54740751 | -0.17211958 | -45.863% |
| Newtonian control residual | 0.20553454 | 0.50093111 | -0.29539656 | -143.721% |

## Null Controls

| control | p | 95th percentile reduction |
| --- | ---: | ---: |
| morphology row shuffle | 0.607393 | 0.03878496 |
| independent morphology column shuffle | 0.380619 | 0.00369795 |

## Promotion Gates

| gate | result |
| --- | --- |
| `positive_projection_holdout_reduction` | FAIL |
| `row_shuffle_p_le_0p05` | FAIL |
| `column_shuffle_p_le_0p05` | FAIL |
| `above_row_shuffle_q95` | FAIL |
| `above_column_shuffle_q95` | FAIL |
| `projection_gain_exceeds_newtonian_control` | PASS |

The source manifest, feature list, deterministic split, model, metrics,
controls, and promotion rule were frozen by a separate source-only script.
The scorer verified the frozen feature hash before opening the endpoint.

## Claim Boundary

This is a retrospective locked SPARC/S4G prevalidation test. It is not an
independent external replication, physical `M_tau` channel derivation,
dynamics-lensing shared-parent result, or morphological-body attribution.
