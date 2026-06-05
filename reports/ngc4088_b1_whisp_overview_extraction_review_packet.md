# NGC4088 WHISP Overview Extraction Review Packet

This packet turns the cached WHISP UGC 7081 graphical H I overview into a
residual-blind B1 review task. It is not a formula freeze and not an
endpoint score.

## Summary

| whisp_overview_extraction_status | galaxy | b1_resolution_status | whisp_graphical_overview_cached | original_hi_data_audit_status | n_review_panels | n_pending_obligations | accepted_x_w_for_formula_freeze | formula_freeze_allowed_now | endpoint_scores_allowed | uses_vobs_or_residual | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WHISP_OVERVIEW_EXTRACTION_PACKET_READY_RESPONSE_PENDING | NGC4088 | B1_NOT_RESOLVED_WHISP_OVERVIEW_REVIEW_PENDING | True | RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE_AUDITED_NO_DIRECT_PRODUCT_CACHED | 6 | 3 | False | False | False | False | fill the WHISP overview extraction response or obtain direct FITS/source-coordinate H I data | ngc4088_b1_whisp_overview_extraction_review_not_endpoint |

## Packet

| galaxy | packet_id | source_product | source_product_status | primary_panel | primary_axis | hi_radius_arcmin | first_pass_x_w | acceptance_tolerance_x_w | acceptance_tolerance_arcmin | forbidden_inputs | formula_freeze_allowed_now | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_WHISP_OVERVIEW_ARCMIN_EXTRACTION_REVIEW_PACKET_V1 | data/external/literature/ngc4088_source_native_hi_route/whisp_ugc7081_overview.gif | WHISP_GRAPHICAL_OVERVIEW_CACHED_REVIEW_READY | P3_POSITION_VELOCITY_MAJOR_AXIS | Offset from center (arcmin) | 4.25 | 0.2823529411764706 | 0.0705882352941176 | 0.2999999999999998 | vobs;rotation_residual;endpoint_score;fit_rank;required_S_tau_diagnostic | False | False | False | ngc4088_b1_whisp_overview_extraction_review_not_endpoint |

## Review Panels

| panel_id | panel_role | review_use | overview_image |
| --- | --- | --- | --- |
| P1_OPTICAL_SKY | context_only | optical orientation/context; not sufficient for x_w | data/external/literature/ngc4088_source_native_hi_route/whisp_ugc7081_overview.gif |
| P3_POSITION_VELOCITY_MAJOR_AXIS | primary_arcmin_onset_candidate | direct arcmin offset axis along major axis; candidate source for side onsets | data/external/literature/ngc4088_source_native_hi_route/whisp_ugc7081_overview.gif |
| P5_TOTAL_HI_30_ARCSEC | hi_morphology_cross_check | 30 arcsec total HI morphology and sky-coordinate cross-check | data/external/literature/ngc4088_source_native_hi_route/whisp_ugc7081_overview.gif |
| P6_TOTAL_HI_60_ARCSEC | hi_morphology_cross_check | 60 arcsec total HI morphology and sky-coordinate cross-check | data/external/literature/ngc4088_source_native_hi_route/whisp_ugc7081_overview.gif |
| P8_IWM_VELOCITY_30_ARCSEC | velocity_field_cross_check | 30 arcsec velocity-field orientation/asymmetry cross-check | data/external/literature/ngc4088_source_native_hi_route/whisp_ugc7081_overview.gif |
| P9_IWM_VELOCITY_60_ARCSEC | velocity_field_cross_check | 60 arcsec velocity-field orientation/asymmetry cross-check | data/external/literature/ngc4088_source_native_hi_route/whisp_ugc7081_overview.gif |

## Obligations

| obligation_id | status | requirement | acceptance_condition | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| WHEX1_SOURCE_PRODUCT_CACHED | PASS | WHISP UGC7081 overview GIF is cached with provenance | source_product_status=WHISP_GRAPHICAL_OVERVIEW_CACHED_REVIEW_READY | False | False | ngc4088_b1_whisp_overview_extraction_review_not_endpoint |
| WHEX2_ARCMIN_AXIS_PRESENT | PASS | position-velocity panel has Offset from center (arcmin) axis | reviewer uses P3 axis rather than endpoint residuals | False | False | ngc4088_b1_whisp_overview_extraction_review_not_endpoint |
| WHEX3_RESPONSE_FILLED | PENDING | reviewer fills side-A/side-B onset offsets and uncertainty | numeric arcmin offsets and uncertainty present | False | False | ngc4088_b1_whisp_overview_extraction_review_not_endpoint |
| WHEX4_TOLERANCE_OR_INTERVAL | PENDING | x_w review agrees with first pass or freezes an uncertainty interval | |x_w_review - 0.282353| <= 0.0705882, or source-side interval is frozen before formula use | False | False | ngc4088_b1_whisp_overview_extraction_review_not_endpoint |
| WHEX5_INDEPENDENT_OR_FROZEN_METHOD | PENDING | measurement is performed by independent reviewer or frozen image script | reviewer_or_method_id is not the first-pass digitizer | False | False | ngc4088_b1_whisp_overview_extraction_review_not_endpoint |

## Response Template

| galaxy | packet_id | reviewer_or_method_id | review_timestamp_utc | source_product_used | source_product_hash | side_a_onset_offset_arcmin | side_b_onset_offset_arcmin | side_combination_rule | combined_onset_arcmin | uncertainty_arcmin | x_w_review | agrees_with_first_pass_within_tolerance | review_notes | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_WHISP_OVERVIEW_ARCMIN_EXTRACTION_REVIEW_PACKET_V1 | PENDING_WHISP_OVERVIEW_REVIEW | PENDING_WHISP_OVERVIEW_REVIEW | data/external/literature/ngc4088_source_native_hi_route/whisp_ugc7081_overview.gif | PENDING_OPTIONAL_HASH | PENDING_WHISP_OVERVIEW_REVIEW | PENDING_WHISP_OVERVIEW_REVIEW | mean(abs(side_a), abs(side_b)) unless one side is explicitly flagged unusable | PENDING_WHISP_OVERVIEW_REVIEW | PENDING_WHISP_OVERVIEW_REVIEW | PENDING_WHISP_OVERVIEW_REVIEW | PENDING_WHISP_OVERVIEW_REVIEW | PENDING_WHISP_OVERVIEW_REVIEW | False | False | ngc4088_b1_whisp_overview_extraction_review_not_endpoint |

## Interpretation

The WHISP overview gives a stronger source-provenance route than the printed
paper crop because the position-velocity panel includes an arcmin offset
axis. B1 still remains open: the packet must be filled by an independent
reviewer or frozen extraction method, and the resulting x_w must either
agree with the first-pass value within tolerance or produce a frozen
source-side uncertainty interval before formula use.
