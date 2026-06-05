# NGC4088 Independent x_w Digitization Review Packet

This is the residual-blind second-review route for blocker B1. It prepares
the independent review of the current first-pass x_w digitization. It does
not change x_w, does not score rotations, and does not authorize endpoint
use.

## Summary

| galaxy | review_status | b1_resolution_status | first_pass_x_w | acceptance_tolerance_x_w | n_pending_obligations | formula_freeze_allowed_now | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | INDEPENDENT_XW_REVIEW_PACKET_READY_RESPONSE_PENDING | B1_NOT_RESOLVED_INDEPENDENT_REVIEW_PENDING | 0.282353 | 0.0705882 | 3 | False | False | False | ngc4088_independent_xw_digitization_review_not_endpoint |

## Review Packet

| galaxy | review_packet_id | review_route | first_pass_digitizer_id | first_pass_x_w | first_pass_onset_arcmin | first_pass_uncertainty_x_w | acceptance_tolerance_x_w | acceptance_tolerance_arcmin | source_images | forbidden_inputs | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_INDEPENDENT_XW_DIGITIZATION_REVIEW_PACKET_V1 | INDEPENDENT_MANUAL_OR_FROZEN_IMAGE_ANALYSIS_REPEAT | codex_manual_page76_page77_v1 | 0.282353 | 1.2 | 0.0705882 | 0.0705882 | 0.3 | data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_76_channel_maps_roi.png;data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_76_channel_maps_roi_worksheet_overlay.png;data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_77-077.png | vobs;rotation_residual;endpoint_score;best_fit_family;required_S_tau_diagnostic | False | ngc4088_independent_xw_digitization_review_not_endpoint |

## Obligations

| obligation_id | obligation_status | requirement | acceptance_condition | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| XWREV1_SOURCE_LOCK | READY | reviewer must use only the frozen page-76 ROI, worksheet overlay, and page-77 cross-check image | source_images_used must be a subset of the packet source image list | False | ngc4088_independent_xw_digitization_review_not_endpoint |
| XWREV2_INDEPENDENT_REVIEWER | PENDING | reviewer identity or frozen image-analysis method must differ from first_pass_digitizer_id | independent_reviewer_id != first_pass_digitizer_id OR method_id is a frozen script/hash | False | ngc4088_independent_xw_digitization_review_not_endpoint |
| XWREV3_NO_ENDPOINT_INPUTS | READY | review notes and method must not use endpoint residuals, vobs, or fit ranks | forbidden_input_detected=False | False | ngc4088_independent_xw_digitization_review_not_endpoint |
| XWREV4_SIDE_BY_SIDE_ONSET_REPEAT | PENDING | repeat side-A and side-B onset measurements under the frozen protocol | independent onset fields are numeric and side_combination_rule_applied is frozen | False | ngc4088_independent_xw_digitization_review_not_endpoint |
| XWREV5_TOLERANCE_OR_ESCALATION | PENDING | compare independent x_w to the first-pass value before any endpoint use | |x_w_independent - 0.282353| <= 0.0705882; otherwise freeze an uncertainty interval or mark x_w unresolved | False | ngc4088_independent_xw_digitization_review_not_endpoint |

## Response Template

| galaxy | review_packet_id | independent_reviewer_id | review_timestamp_utc | review_method_id | source_images_used | inner_disk_axis_pa_deg | outer_ridge_axis_side_a_pa_deg | outer_ridge_axis_side_b_pa_deg | onset_radius_side_a_arcmin | onset_radius_side_b_arcmin | side_combination_rule_applied | xw_combined_arcmin | uncertainty_arcmin | x_w_independent | review_notes | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_INDEPENDENT_XW_DIGITIZATION_REVIEW_PACKET_V1 | PENDING_INDEPENDENT_REVIEW | PENDING_INDEPENDENT_REVIEW | PENDING_INDEPENDENT_REVIEW | PENDING_INDEPENDENT_REVIEW | PENDING_INDEPENDENT_REVIEW | PENDING_INDEPENDENT_REVIEW | PENDING_INDEPENDENT_REVIEW | PENDING_INDEPENDENT_REVIEW | PENDING_INDEPENDENT_REVIEW | PENDING_INDEPENDENT_REVIEW | PENDING_INDEPENDENT_REVIEW | PENDING_INDEPENDENT_REVIEW | PENDING_INDEPENDENT_REVIEW | PENDING_INDEPENDENT_REVIEW | False | False | ngc4088_independent_xw_digitization_review_not_endpoint |

## Interpretation

The current first-pass x_w value is protocol-usable for preflight mapping,
but B1 remains unresolved. To close B1, an independent reviewer or frozen
image-analysis repeat must reproduce the side-by-side onset measurement
without endpoint inputs and must either agree within the frozen tolerance
or explicitly widen/freeze the source-side uncertainty interval.
