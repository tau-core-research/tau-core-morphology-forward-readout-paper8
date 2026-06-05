# NGC4088 Channel-Map Digitization Worksheet

This worksheet freezes panel coordinates for the N4088 channel-map digitization target. It does not measure the warp onset.

## Verdict

The channel-map ROI has been split into panel-level measurement targets. All measurement fields remain empty; `x_w` is still unavailable.

## Summary

| galaxy | roi_png | overlay_png | n_panel_rows | n_measurement_targets | n_empty_measurement_fields | worksheet_status | x_warp_onset_available | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_76_channel_maps_roi.png | data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_76_channel_maps_roi_worksheet_overlay.png | 24 | 23 | 92 | PANEL_WORKSHEET_READY_MEASUREMENTS_EMPTY | False | False | s4g75_ngc4088_channel_map_digitization_worksheet_not_endpoint |

## Panel Targets

| panel_id | channel_velocity_kms | roi_x0_px | roi_y0_px | roi_x1_px | roi_y1_px | panel_status | x_warp_onset_available |
| --- | --- | --- | --- | --- | --- | --- | --- |
| r1c1 | 568 | 0 | 22 | 171 | 179 | MEASUREMENT_TARGET | False |
| r1c2 | 585 | 171 | 22 | 342 | 179 | MEASUREMENT_TARGET | False |
| r1c3 | 601 | 342 | 22 | 513 | 179 | MEASUREMENT_TARGET | False |
| r1c4 | 618 | 513 | 22 | 684 | 179 | MEASUREMENT_TARGET | False |
| r2c1 | 634 | 0 | 179 | 171 | 336 | MEASUREMENT_TARGET | False |
| r2c2 | 651 | 171 | 179 | 342 | 336 | MEASUREMENT_TARGET | False |
| r2c3 | 667 | 342 | 179 | 513 | 336 | MEASUREMENT_TARGET | False |
| r2c4 | 684 | 513 | 179 | 684 | 336 | MEASUREMENT_TARGET | False |
| r3c1 | 701 | 0 | 336 | 171 | 493 | MEASUREMENT_TARGET | False |
| r3c2 | 717 | 171 | 336 | 342 | 493 | MEASUREMENT_TARGET | False |
| r3c3 | 734 | 342 | 336 | 513 | 493 | MEASUREMENT_TARGET | False |
| r3c4 | 750 | 513 | 336 | 684 | 493 | MEASUREMENT_TARGET | False |
| r4c1 | 767 | 0 | 493 | 171 | 650 | MEASUREMENT_TARGET | False |
| r4c2 | 783 | 171 | 493 | 342 | 650 | MEASUREMENT_TARGET | False |
| r4c3 | 800 | 342 | 493 | 513 | 650 | MEASUREMENT_TARGET | False |
| r4c4 | 817 | 513 | 493 | 684 | 650 | MEASUREMENT_TARGET | False |
| r5c1 | 833 | 0 | 650 | 171 | 807 | MEASUREMENT_TARGET | False |
| r5c2 | 850 | 171 | 650 | 342 | 807 | MEASUREMENT_TARGET | False |
| r5c3 | 866 | 342 | 650 | 513 | 807 | MEASUREMENT_TARGET | False |
| r5c4 | 883 | 513 | 650 | 684 | 807 | MEASUREMENT_TARGET | False |
| r6c1 | 899 | 0 | 807 | 171 | 964 | MEASUREMENT_TARGET | False |
| r6c2 | 916 | 171 | 807 | 342 | 964 | MEASUREMENT_TARGET | False |
| r6c3 | 933 | 342 | 807 | 513 | 964 | MEASUREMENT_TARGET | False |
| r6c4 |  | 513 | 807 | 684 | 964 | NON_TARGET_EDGE_PANEL | False |

## Claim Boundary

Panel boxes are digitization scaffolding, not source measurements. A human or frozen image-analysis protocol must fill the measurement fields before any `x_w` candidate can be computed.
