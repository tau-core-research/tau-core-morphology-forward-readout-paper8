# L2 Readout-Weight Intake Candidates

This preflight converts residual-blind source coverage into candidate
readout-component weights for the morphology-information-gain path.
It is an intake layer only: it does not create accepted labels, does not
score rotation curves, and does not use endpoint residuals.

## Full-Sample Verdict

- Galaxies: 175
- Source-informative candidates: 174
- Uninformative fallbacks: 1
- Mean effective component count: 2.260
- Tail nonzero count: 172
- Exponential-disk nonzero count: 75
- Compact nonzero count: 48
- Thick/flared nonzero count: 107

## Summary

| split | n_galaxies | source_informative_count | uninformative_fallback_count | mean_effective_component_count | median_effective_component_count | claim_boundary | dominant_K_compact_finite_count | nonzero_K_compact_finite_count | mean_w_K_compact_finite | dominant_K_scale_tail_spiral_count | nonzero_K_scale_tail_spiral_count | mean_w_K_scale_tail_spiral | dominant_K_exponential_disk_count | nonzero_K_exponential_disk_count | mean_w_K_exponential_disk | dominant_K_thick_flared_count | nonzero_K_thick_flared_count | mean_w_K_thick_flared |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 175 | 174 | 1 | 2.26025 | 1.98676 | l2_weight_intake_candidate_not_endpoint_not_accepted_state | 23 | 48 | 0.091854 | 76 | 172 | 0.510022 | 43 | 75 | 0.163537 | 33 | 107 | 0.234587 |
| holdout | 44 | 44 | 0 | 2.36367 | 1.99541 | l2_weight_intake_candidate_not_endpoint_not_accepted_state | 4 | 14 | 0.096802 | 16 | 44 | 0.480421 | 15 | 21 | 0.194676 | 9 | 28 | 0.2281 |
| train | 131 | 130 | 1 | 2.22552 | 1.9834 | l2_weight_intake_candidate_not_endpoint_not_accepted_state | 19 | 34 | 0.090192 | 60 | 128 | 0.519964 | 28 | 54 | 0.153078 | 24 | 79 | 0.236766 |

## Dominant Candidate Families

| split | dominant_intake_family | n_galaxies |
| --- | --- | --- |
| holdout | K_compact_finite | 4 |
| holdout | K_exponential_disk | 15 |
| holdout | K_scale_tail_spiral | 16 |
| holdout | K_thick_flared | 9 |
| train | K_compact_finite | 19 |
| train | K_exponential_disk | 28 |
| train | K_scale_tail_spiral | 60 |
| train | K_thick_flared | 24 |

## Claim Boundary

These are weight-intake candidates, not accepted Tau-side readout
states. The tail, exponential-disk, compact, and thick/flared signals
come from currently available residual-blind source coverage and
present-day morphology proxies. The thick/flared channel remains
especially proxy-like because no dedicated source-native thickness
or velocity-field layer is assembled here.
Endpoint use requires a separate freeze-and-audit step.
