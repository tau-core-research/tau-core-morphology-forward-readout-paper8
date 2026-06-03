# P0 Visual Review Template

This report records the residual-blind visual review template generated
from the P0 SkyView preview panels. The template is a reviewer-fillable
source layer only. It is not an accepted morphology manifest, not an
image classification, and not an endpoint score.

## Review Template Rows

| galaxy | inspection_priority_tier | inspection_priority_score | preview_surveys_available | present_day_morphology_label | morphological_memory_history_proxy_judgment | residual_blind_family_recommendation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0100 | P0 | 88 | 2MASS-K;DSS2 Red;WISE 3.4 | TO_BE_FILLED_RESIDUAL_BLIND | TO_BE_FILLED_RESIDUAL_BLIND | TO_BE_FILLED_RESIDUAL_BLIND | p0_visual_review_template_not_accepted_label_not_endpoint |
| NGC0247 | P0 | 88 | 2MASS-K;DSS2 Red;WISE 3.4 | TO_BE_FILLED_RESIDUAL_BLIND | TO_BE_FILLED_RESIDUAL_BLIND | TO_BE_FILLED_RESIDUAL_BLIND | p0_visual_review_template_not_accepted_label_not_endpoint |
| NGC0300 | P0 | 98 | 2MASS-K;DSS2 Red;WISE 3.4 | TO_BE_FILLED_RESIDUAL_BLIND | TO_BE_FILLED_RESIDUAL_BLIND | TO_BE_FILLED_RESIDUAL_BLIND | p0_visual_review_template_not_accepted_label_not_endpoint |
| NGC6503 | P0 | 98 | 2MASS-K;DSS2 Red;WISE 3.4 | TO_BE_FILLED_RESIDUAL_BLIND | TO_BE_FILLED_RESIDUAL_BLIND | TO_BE_FILLED_RESIDUAL_BLIND | p0_visual_review_template_not_accepted_label_not_endpoint |

## Review Field Schema

| field | value_type | initial_value | may_use_endpoint_scores |
| --- | --- | --- | --- |
| reviewer_id | text | TO_BE_FILLED_RESIDUAL_BLIND | False |
| review_timestamp_utc | datetime | TO_BE_FILLED_RESIDUAL_BLIND | False |
| present_day_morphology_label | controlled_text | TO_BE_FILLED_RESIDUAL_BLIND | False |
| outer_disk_lsb_tail_evidence | yes_no_uncertain | TO_BE_FILLED_RESIDUAL_BLIND | False |
| hi_extent_or_asymmetry_evidence | yes_no_uncertain | TO_BE_FILLED_RESIDUAL_BLIND | False |
| bar_m2_evidence | yes_no_uncertain | TO_BE_FILLED_RESIDUAL_BLIND | False |
| edge_projection_caveat | yes_no_uncertain | TO_BE_FILLED_RESIDUAL_BLIND | False |
| vertical_flare_warp_evidence | yes_no_uncertain | TO_BE_FILLED_RESIDUAL_BLIND | False |
| compact_bulge_evidence | yes_no_uncertain | TO_BE_FILLED_RESIDUAL_BLIND | False |
| ring_resonance_evidence | yes_no_uncertain | TO_BE_FILLED_RESIDUAL_BLIND | False |
| morphological_memory_history_proxy_judgment | controlled_text | TO_BE_FILLED_RESIDUAL_BLIND | False |
| review_confidence | low_medium_high | TO_BE_FILLED_RESIDUAL_BLIND | False |
| residual_blind_family_recommendation | controlled_text | TO_BE_FILLED_RESIDUAL_BLIND | False |
| review_sources_used | semicolon_list | TO_BE_FILLED_RESIDUAL_BLIND | False |
| review_notes | free_text | TO_BE_FILLED_RESIDUAL_BLIND | False |

## Forbidden Inputs

- endpoint residual gain
- required-S_tau diagnostic as a label input
- best-fit Tau Core readout family
- MOND/RAR/TGP comparison score
- post-hoc family switching after endpoint scoring

## Claim Boundary

All review fields are initialized as residual-blind placeholders. The
template must be filled before endpoint residual gains, required-S_tau
diagnostics, best-fit readout families, MOND/RAR/TGP comparison scores,
or post-hoc family switching are inspected.

Claim boundary: `p0_visual_review_template_not_accepted_label_not_endpoint`.
