# NGC4183 Tilted-Ring Independent Review Packet

Status: `NGC4183_TILTED_RING_REVIEW_PACKET_CREATED_FREEZE_BLOCKED`

This packet is for independent source review.  It does not freeze a formula and
does not authorize endpoint scoring.

## Summary

| review_packet_status | galaxy | profile_status | weak_control_status | n_review_items | review_response_received | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary | next_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183_TILTED_RING_REVIEW_PACKET_CREATED_FREEZE_BLOCKED | NGC4183 | NGC4183_TILTED_RING_PROFILE_EXTRACTED_REVIEW_REQUIRED_NOT_FREEZE_READY | NGC4183_WEAK_PROJECTION_CONTROL_PREFLIGHT_COMPLETE_NOT_ENDPOINT | 5 | True | False | False | ngc4183_tilted_ring_independent_review_packet_not_endpoint | review_response_intake |

## Review Items

| review_item | field_or_range | current_value | review_question | required_response |
| --- | --- | --- | --- | --- |
| source_identity | Verheijen & Sancisi 2001 / NGC4183 / Table 4 | local PDF + OCR cache | Does the cited table block correspond to NGC4183 tilted-ring rows? | accept/reject/correct |
| radius_series | radius_arcsec | 10..241 arcsec, n=23 | Are all radial rings transcribed correctly, including 229 and 241 arcsec rows? | accept/reject/correct |
| orientation_series | inclination_deg, pa_deg | i=82..82 deg; PA=346..349 deg | Is the near-constant i=82 deg and PA=346..349 deg transcription correct? | accept/reject/correct |
| velocity_columns_not_endpoint | Vrot app/rec/ave | transcribed for source consistency only | Do not use Vrot columns for residual fitting; only confirm table transcription. | accept/reject/correct |
| upper_bound_conclusion | gamma_proj upper bound | 0.00269837 | If orientation series is accepted, does the weak-control conclusion follow? | accept/reject/correct |

## Response Template

| reviewer | date | source_identity_decision | radius_series_decision | orientation_series_decision | velocity_columns_decision | upper_bound_conclusion_decision | corrections | review_verdict | may_freeze_null_control_after_review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codex_internal_source_review_not_independent | 2026-06-05 | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | No correction from local visual review of the rendered Table 4 page/crop. NGC4183 rows match the extracted radius series 10..241 arcsec, constant i=82 deg, and PA=346..349 deg. Outer 229/241 arcsec rows have missing approaching-side velocity entries, as represented in the extracted profile. | INTERNAL_CODEX_SOURCE_REVIEW_ACCEPTS_TRANSCRIPTION_NOT_INDEPENDENT_FREEZE_BLOCKED | False |

## Visual Sources

| visual_source_id | path | role | review_use |
| --- | --- | --- | --- |
| N4183_TABLE4_FULL_PAGE | /Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/2001_verheijen_sancisi_pages/ngc4183_review/page-013.png | full rendered PDF page containing NGC4183 Table 4 rows | check context and column headers |
| N4183_TABLE4_FULL_COLUMN_CROP | /Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/2001_verheijen_sancisi_pages/ngc4183_review/ngc4183_table4_full_column_crop.png | focused crop containing NGC4183 tilted-ring rows | primary visual transcription check |
| N4183_OBSERVING_PARAMETERS_PAGE | /Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/2001_verheijen_sancisi_pages/page_84-084.png | rendered page with NGC4183 H I parameters and warp note | check PA=347, i=83, H I diameter=6.1 arcmin, slight outer warp note |

## Gates

| gate_id | gate_status | evidence | remaining_obligation |
| --- | --- | --- | --- |
| N4183_REVIEW_G1_PACKET_CREATED | PASS | profile, source excerpt, and response template written | independent response required |
| N4183_REVIEW_G2_FREEZE_ALLOWED | BLOCKED | independent review response is present but freeze remains separate | review intake determines whether source-only acceptance or freeze authorization applies |

## Packet State

The packet preserves the latest response template if one has already been
filled. A filled source-review response does not by itself imply freeze
authorization.

## Source Pointers

- PDF: `/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/2001_verheijen_sancisi_ursa_major_hi.pdf`
- OCR text: `/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/2001_verheijen_sancisi_ursa_major_hi.txt`
- Full rendered table page: `/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/2001_verheijen_sancisi_pages/ngc4183_review/page-013.png`
- NGC4183 table crop: `/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/2001_verheijen_sancisi_pages/ngc4183_review/ngc4183_table4_full_column_crop.png`
- Observing-parameters page: `/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/2001_verheijen_sancisi_pages/page_84-084.png`
- Extracted profile: `/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/derived/ngc4183_tilted_ring_orientation_profile.csv`

## OCR Excerpt To Review

> N4183 / 10 / 56 12 / 10 38 15 / 10 / 47 82 346 / 20 / 71 7 / 7 61 12 / 10 / 66 82 346 / 30 / 78 7 / 7 74 10 / 7 / 76 82 346 / 40 / 88 7 / 7 84 10 / 7 / 86 82 346 / 50 / 97 7 / 7 97 7 / 7 / 97 82 346 / 60 100 7 / 7 99 7 / 7 / 99 82 346 / 70 103 7 / 7 103 7 / 7 / 103 82 346 / 80 106 7 / 7 107 7 / 7 / 107 82 346 / 90 110 7 / 7 113 7 / 7 / 111 82 346 / 100 112 7 / 7 117 10 / 10 / 114 82 346 / 110 112 7 / 7 118 10 / 10 / 115 82 346 / 120 108 7 / 7 114 10 / 7 / 111 82 346 / 130 108 7 / 7 113 10 / 7 / 110 82 347 / 141 111 7 / 7 112 7 / 7 / 111 82 347 / 151 108 7 / 5 110 7 / 7 / 109 82 347 / 161 106 5 / 5 109 7 / 7 / 108 82 347 / 172 109 7 / 7 109 7 / 7 / 109 82 347 / 183 112 7 / 7 110 7 / 7 / 111 82 348 / 194 108 5 / 8 111 8 / 8 / 110 82 348 / 205 106 5 / 8 111 8 / 8 / 109 82 348 / 217 107 7 / 8 112 8 / 8 / 110 82 348 / 229 / - - 112 10 / 10 / 112 82 348 / 241 / - - 113 13 / 10 / 113 82 349

## Current Derived Consequence

If the orientation transcription is accepted, the source-side projection
correction remains a weak/null-control case:

```text
max |Delta PA| = 3.000 deg
max |Delta i|  = 0.000 deg
gamma_proj <= 0.00269837
|Delta v|/v <= 0.00135010
```
