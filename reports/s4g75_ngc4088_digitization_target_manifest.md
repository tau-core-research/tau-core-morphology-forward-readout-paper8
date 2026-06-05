# NGC4088 Digitization Target Manifest

This manifest identifies the source pages/panels needed for a residual-blind NGC4088 warp-onset extraction. It does not perform digitization.

## Verdict

The N4088 channel-map page is available as a rendered source target. The next action is a frozen channel-map digitization protocol that measures an onset radius or PA bend. No `x_w` has been extracted here.

## Targets

| galaxy | source_authors_year | source_pdf | source_pdf_page | rendered_page_png | target_panel | target_observable | digitization_route | required_measurement_outputs | acceptance_rule | page_render_available | x_warp_onset_available | endpoint_scores_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | Verheijen & Sancisi 2001 | data/external/literature/2001_verheijen_sancisi_ursa_major_hi.pdf | 76 | data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_76-076.png | N4088 channel maps | warp_onset_radius_or_PA_bend_from_channel_map | CHANNEL_MAP_DIGITIZATION | inner_disk_axis;outer_ridge_axis_by_side;onset_radius_arcmin;side_combination_rule;uncertainty_arcmin | digitization protocol, tolerance, and side-combination rule must be frozen before any endpoint scoring | True | False | False | False | s4g75_ngc4088_digitization_target_manifest_not_endpoint |
| NGC4088 | Verheijen & Sancisi 2001 | data/external/literature/2001_verheijen_sancisi_ursa_major_hi.pdf | 77 | data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_77-077.png | N4088 continuation panels / position-velocity diagnostics | cross-check_PA_or_PV_asymmetry | PV_OR_CONTINUATION_CROSS_CHECK | PV_asymmetry_side;outer_extent_side;consistency_with_channel_map | cross-check only unless a radial onset can be measured | True | False | False | False | s4g75_ngc4088_digitization_target_manifest_not_endpoint |

## Summary

| galaxy | n_digitization_targets | n_rendered_pages_available | primary_digitization_route | x_warp_onset_available | manifest_status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 2 | 2 | CHANNEL_MAP_DIGITIZATION | False | DIGITIZATION_TARGET_READY_XW_NOT_EXTRACTED | False | s4g75_ngc4088_digitization_target_manifest_not_endpoint |

## Claim Boundary

A digitization target is not a measurement. The endpoint remains blocked until the digitization protocol produces a residual-blind `x_w` with a predeclared uncertainty and side-combination rule.
