# Source-Normalization Failure Modes By Lane

This diagnostic compares morphology-family specificity with Tau evidence
L2 baseline behavior. It does not tune the normalization rule and does
not select an endpoint.

## Holdout Projection-Caveat Failure Modes

| split | inclusion_lane | allowed_use | failure_mode | n_galaxies | hard_beats_wrong_fraction | tau_beats_tpg_v6_fraction | tau_beats_mond_fraction | median_tau_minus_tpg_v6 | median_tau_minus_mond | median_signed_cancellation_ratio | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | NO_SPECIFICITY_AND_BASELINE_WEAK | 2 | 0 | 0 | 0 | 14.134 | 11.9436 | 1 | source_normalization_failure_modes_by_lane_not_endpoint |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | OTHER_NORMALIZATION_DIAGNOSTIC | 1 | 0 | 1 | 1 | -4.49146 | -0.965039 | 1 | source_normalization_failure_modes_by_lane_not_endpoint |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | PROJECTION_SCALE_NORMALIZATION_FAILURE | 7 | 1 | 0 | 0 | 5.17511 | 2.87649 | 0.363846 | source_normalization_failure_modes_by_lane_not_endpoint |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | SPECIFICITY_AND_BASELINE_PARTLY_TRANSFER | 4 | 1 | 1 | 0.75 | -4.84113 | -4.37131 | 0.298752 | source_normalization_failure_modes_by_lane_not_endpoint |

## Summary

| split | inclusion_lane | allowed_use | failure_mode | n_galaxies | hard_beats_wrong_fraction | tau_beats_tpg_v6_fraction | tau_beats_mond_fraction | median_tau_minus_tpg_v6 | median_tau_minus_mond | median_signed_cancellation_ratio | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | NO_SPECIFICITY_AND_BASELINE_WEAK | 1 | 0 | 0 | 0 | 2.66287 | 0.602558 | 0.313108 | source_normalization_failure_modes_by_lane_not_endpoint |
| holdout | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | OTHER_NORMALIZATION_DIAGNOSTIC | 1 | 0 | 1 | 1 | -6.17015 | -3.595 | 0.764864 | source_normalization_failure_modes_by_lane_not_endpoint |
| holdout | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | PROXY_GATE_OR_COMPONENT_WEIGHT_FAILURE | 2 | 1 | 0 | 0 | 9.14876 | 7.2222 | 0.838179 | source_normalization_failure_modes_by_lane_not_endpoint |
| holdout | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | SIGNED_COMPONENT_CANCELLATION_FAILURE | 1 | 1 | 0 | 0 | 1.1232 | 3.01107 | 0.179475 | source_normalization_failure_modes_by_lane_not_endpoint |
| holdout | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | SPECIFICITY_AND_BASELINE_PARTLY_TRANSFER | 23 | 1 | 0.565217 | 0.782609 | -0.364261 | -0.771532 | 0.297357 | source_normalization_failure_modes_by_lane_not_endpoint |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | SIGNED_COMPONENT_CANCELLATION_FAILURE | 1 | 1 | 0 | 0 | 0.9649 | 2.78076 | 0.124569 | source_normalization_failure_modes_by_lane_not_endpoint |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | SPECIFICITY_AND_BASELINE_PARTLY_TRANSFER | 1 | 1 | 1 | 1 | -0.616576 | -3.14062 | 0.375 | source_normalization_failure_modes_by_lane_not_endpoint |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | NO_SPECIFICITY_AND_BASELINE_WEAK | 2 | 0 | 0 | 0 | 14.134 | 11.9436 | 1 | source_normalization_failure_modes_by_lane_not_endpoint |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | OTHER_NORMALIZATION_DIAGNOSTIC | 1 | 0 | 1 | 1 | -4.49146 | -0.965039 | 1 | source_normalization_failure_modes_by_lane_not_endpoint |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | PROJECTION_SCALE_NORMALIZATION_FAILURE | 7 | 1 | 0 | 0 | 5.17511 | 2.87649 | 0.363846 | source_normalization_failure_modes_by_lane_not_endpoint |
| holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | SPECIFICITY_AND_BASELINE_PARTLY_TRANSFER | 4 | 1 | 1 | 0.75 | -4.84113 | -4.37131 | 0.298752 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | NO_SPECIFICITY_AND_BASELINE_WEAK | 3 | 0 | 0 | 0 | 5.74639 | 2.74301 | 0.653746 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | OTHER_NORMALIZATION_DIAGNOSTIC | 2 | 0 | 1 | 0.5 | -7.17028 | -3.90109 | 0.550181 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | PROXY_GATE_OR_COMPONENT_WEIGHT_FAILURE | 4 | 1 | 0 | 0 | 5.63637 | 5.58637 | 0.653374 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | SIGNED_COMPONENT_CANCELLATION_FAILURE | 10 | 1 | 0 | 0 | 0.860539 | 2.76789 | 0.269407 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | SPECIFICITY_AND_BASELINE_PARTLY_TRANSFER | 61 | 1 | 0.639344 | 0.737705 | -0.29719 | -1.97466 | 0.332787 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | NO_SPECIFICITY_AND_BASELINE_WEAK | 5 | 0 | 0 | 0 | 19.2039 | 15.3475 | 1 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | OTHER_NORMALIZATION_DIAGNOSTIC | 5 | 0.6 | 0.2 | 0.4 | 1.11095 | 1.24046 | 1 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | SIGNED_COMPONENT_CANCELLATION_FAILURE | 1 | 1 | 0 | 0 | 1.3758 | 1.04131 | 0.295811 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | SPECIFICITY_AND_BASELINE_PARTLY_TRANSFER | 6 | 1 | 1 | 0.666667 | -3.16775 | -1.07657 | 1 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | NO_SPECIFICITY_AND_BASELINE_WEAK | 3 | 0 | 0 | 0 | 10.3577 | 8.50906 | 1 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | OTHER_NORMALIZATION_DIAGNOSTIC | 2 | 0 | 1 | 0.5 | -2.57416 | 0.285309 | 0.332558 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | PROJECTION_SCALE_NORMALIZATION_FAILURE | 15 | 1 | 0 | 0 | 4.39623 | 2.61544 | 0.348857 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | SPECIFICITY_AND_BASELINE_PARTLY_TRANSFER | 13 | 1 | 0.769231 | 0.846154 | -1.83462 | -3.19783 | 1 | source_normalization_failure_modes_by_lane_not_endpoint |
| train | STRICT_READY_CANDIDATE | strict_preendpoint_freeze_candidate | OTHER_NORMALIZATION_DIAGNOSTIC | 1 | 1 | 0 | 0 | 16.2164 | 13.0075 | 1 | source_normalization_failure_modes_by_lane_not_endpoint |

## Claim Boundary

Failure mode labels are diagnostic. They do not use endpoint residuals to
change any gate, family, sign, or normalization constant.
