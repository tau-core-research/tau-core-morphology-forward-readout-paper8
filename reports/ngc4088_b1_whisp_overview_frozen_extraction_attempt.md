# NGC4088 WHISP Overview Frozen Extraction Attempt

This attempt uses only the cached WHISP UGC 7081 graphical H I overview.
It extracts a source-side x_w candidate from the position-velocity panel
with the source-provided arcmin offset axis. It is not an endpoint score
and does not use observed rotation residuals.

## Summary

| frozen_extraction_attempt_status | galaxy | b1_resolution_status | source_product | posvel_crop | extraction_overlay | side_a_onset_offset_arcmin | side_b_onset_offset_arcmin | combined_onset_arcmin | uncertainty_arcmin | x_w_review | first_pass_x_w | acceptance_tolerance_x_w | agrees_with_first_pass_within_tolerance | accepted_x_w_for_formula_freeze | formula_freeze_allowed_now | endpoint_scores_allowed | uses_vobs_or_residual | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FROZEN_WHISP_OVERVIEW_EXTRACTION_ATTEMPT_COMPLETE_AGREES_WITH_FIRST_PASS | NGC4088 | B1_NOT_RESOLVED_FROZEN_EXTRACTION_PROMOTION_REVIEW_REQUIRED | data/external/literature/ngc4088_source_native_hi_route/whisp_ugc7081_overview.gif | data/external/literature/ngc4088_source_native_hi_route/whisp_ugc7081_posvel_crop.png | data/external/literature/ngc4088_source_native_hi_route/whisp_ugc7081_posvel_frozen_extraction_overlay.png | 1.40955 | -1.12628 | 1.26791 | 0.15 | 0.298333 | 0.282353 | 0.0705882 | True | False | False | False | False | promote B1 explicitly only after reviewing this frozen extraction or obtaining independent review/direct FITS data | ngc4088_b1_whisp_overview_frozen_extraction_attempt_not_endpoint |

## Response Candidate

| galaxy | packet_id | reviewer_or_method_id | review_timestamp_utc | source_product_used | source_product_hash | side_a_onset_offset_arcmin | side_b_onset_offset_arcmin | side_combination_rule | combined_onset_arcmin | uncertainty_arcmin | x_w_review | agrees_with_first_pass_within_tolerance | review_notes | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_WHISP_OVERVIEW_ARCMIN_EXTRACTION_REVIEW_PACKET_V1 | FROZEN_SCRIPT_WHISP_OVERVIEW_SATURATION_COMPONENT_CENTROID_V1 | REPRODUCIBLE_SCRIPT_RUN | data/external/literature/ngc4088_source_native_hi_route/whisp_ugc7081_overview.gif | not_hashed_in_this_attempt | 1.40955 | -1.12628 | mean(abs(two_largest_opposite-side saturation-component centroids)) | 1.26791 | 0.15 | 0.298333 | True | Frozen algorithmic candidate from WHISP graphical overview; agreement supports B1 but does not by itself authorize formula freeze. | False | False | ngc4088_b1_whisp_overview_frozen_extraction_attempt_not_endpoint |

## Component Ledger

| component_id | label_id | area_px | x_min_px | x_max_px | y_min_px | y_max_px | x_centroid_px | y_centroid_px | offset_centroid_arcmin | abs_offset_centroid_arcmin | component_side | selected_for_response | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C2 | 117 | 777 | 49 | 89 | 101 | 148 | 72.5521 | 126.776 | 1.40955 | 1.40955 | positive_offset_side | True | False | False | ngc4088_b1_whisp_overview_frozen_extraction_attempt_not_endpoint |
| C1 | 9 | 744 | 80 | 131 | 24 | 99 | 98.5444 | 53.6035 | -1.12628 | 1.12628 | negative_offset_side | True | False | False | ngc4088_b1_whisp_overview_frozen_extraction_attempt_not_endpoint |

## Obligations

| obligation_id | status | evidence | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| WHEXATT1_SOURCE_PRODUCT_AND_AXIS | PASS | cached WHISP overview and frozen pos-vel panel geometry are used | False | False | ngc4088_b1_whisp_overview_frozen_extraction_attempt_not_endpoint |
| WHEXATT2_TWO_OPPOSITE_COMPONENTS | PASS | selected_components=2, side_count=2 | False | False | ngc4088_b1_whisp_overview_frozen_extraction_attempt_not_endpoint |
| WHEXATT3_FIRST_PASS_AGREEMENT | PASS | x_w_review=0.298333, first_pass_x_w=0.282353, tolerance=0.0705882 | False | False | ngc4088_b1_whisp_overview_frozen_extraction_attempt_not_endpoint |
| WHEXATT4_FORMULA_FREEZE_PROMOTION | PENDING_REVIEW | requires explicit B1 promotion decision or independent review before accepting x_w | False | False | ngc4088_b1_whisp_overview_frozen_extraction_attempt_not_endpoint |

## Interpretation

The frozen WHISP overview extraction gives a source-side x_w candidate that
agrees with the first-pass value within the predeclared tolerance. This is
a real strengthening of B1 provenance, but it is still marked as a
promotion-review input rather than an accepted formula-freeze value.
