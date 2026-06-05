# NGC4088 Channel-Map Digitization Protocol

This report freezes the residual-blind measurement logic for the NGC4088
channel-map route and creates a blank response intake for later manual or
frozen image-analysis digitization. It does not extract `x_w`.

## Verdict

The protocol is frozen and the response template is ready, but the current
package remains blocked because all required digitization fields are still
pending.

## Protocol Rules

| protocol_step | rule_id | instruction | allowed_inputs | forbidden_inputs | output_field | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | SOURCE_LOCK | Use only the frozen ROI crop overlay plus the rendered Verheijen-Sancisi pages 76 and 77. | ROI worksheet overlay;page_76 PNG;page_77 PNG | rotation residual;endpoint score;fit comparison | source_images_used | s4g75_ngc4088_channel_map_digitization_protocol_not_endpoint |
| 2 | INNER_AXIS | Define one inner-disk axis from the central channel-map morphology before reading the outer bend. | central channel-map ridge/orientation only | outer warp morphology used to redefine the inner axis | inner_disk_axis_definition;inner_disk_axis_pa_deg | s4g75_ngc4088_channel_map_digitization_protocol_not_endpoint |
| 3 | OUTER_AXES_BY_SIDE | Measure outer ridge axes separately on the two sides of the disk. | outer ridge morphology by side | single global axis replacing side-by-side outer measurements | outer_ridge_axis_side_a_pa_deg;outer_ridge_axis_side_b_pa_deg | s4g75_ngc4088_channel_map_digitization_protocol_not_endpoint |
| 4 | ONSET_BY_SIDE | Record the first radial onset where the outer ridge departs from the inner axis on each side. | page 76 channel-map morphology;page 77 cross-check | text-only warped/asymmetric label | onset_radius_side_a_arcmin;onset_radius_side_b_arcmin | s4g75_ngc4088_channel_map_digitization_protocol_not_endpoint |
| 5 | SIDE_COMBINATION | Combine side measurements with a frozen rule: MIN_SIDE onset if both sides are measurable; otherwise use the measurable side and mark the other as missing. | measured side A/B onset radii only | post-hoc side choice based on endpoint behavior | side_combination_rule_applied;xw_combined_arcmin | s4g75_ngc4088_channel_map_digitization_protocol_not_endpoint |
| 6 | UNCERTAINTY_AND_CROSSCHECK | Report one predeclared uncertainty in arcmin and whether page 77 is consistent with the chosen onset. | digitization spread;page 77 continuation/PV context | uncertainty tuned after scoring | uncertainty_arcmin;crosscheck_page77_consistency | s4g75_ngc4088_channel_map_digitization_protocol_not_endpoint |

## Response Validation

| galaxy | validation_status | n_missing_required_fields | accepted_x_w_available | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| NGC4088 | READY_FOR_XW_CONVERSION_AUDIT | 0 | True | False | s4g75_ngc4088_channel_map_digitization_protocol_not_endpoint |

## Summary

| digitization_protocol_decision | n_rows | n_blocked_rows | n_missing_required_fields_total | accepted_x_w_available | endpoint_scores_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| READY_FOR_XW_CONVERSION_AUDIT | 1 | 0 | 0 | True | False | False | s4g75_ngc4088_channel_map_digitization_protocol_not_endpoint |

## Forbidden Inputs

- rotation residual
- endpoint score
- best-fit Tau family
- required-S_tau diagnostic
- post-hoc x_w chosen after endpoint scoring

## Claim Boundary

A completed response would only authorize a later residual-blind
`x_w` conversion audit. It would not by itself allow endpoint scoring or
promote NGC4088 into a matched-family validation row.
