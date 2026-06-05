# NGC4088 B1 Source-Native Radial Calibration Packet

This packet separates warp-like image evidence from accepted source-native
radial calibration. It does not use observed rotation residuals and does
not authorize endpoint scoring.

## Summary

| galaxy | calibration_packet_status | radial_calibration_acceptance_status | b1_resolution_status | first_pass_x_w | first_pass_onset_arcmin | first_pass_uncertainty_arcmin | hi_diameter_arcmin | hi_radius_arcmin | image_repeat_status | n_ready_routes | n_open_routes | accepted_x_w_for_formula_freeze | formula_freeze_allowed_now | endpoint_scores_allowed | uses_vobs_or_residual | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | B1_SOURCE_NATIVE_RADIAL_CALIBRATION_PACKET_CREATED | RADIAL_CALIBRATION_NOT_ACCEPTED | B1_NOT_RESOLVED_RADIAL_CALIBRATION_OPEN | 0.282353 | 1.2 | 0.3 | 8.5 | 4.25 | FROZEN_IMAGE_REPEAT_ATTEMPT_COMPLETE_INCONCLUSIVE | 1 | 2 | False | False | False | False | complete RC1 independent reviewer response, or close RC2/RC3 with source-native radial calibration before accepting x_w | ngc4088_b1_source_native_radial_calibration_packet_not_endpoint |

## Calibration Formula Ledger

| quantity | formula | value | unit | source | status | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R_HI_arcmin | 0.5 * D_HI_arcmin | 4.25 | arcmin | Verheijen-Sancisi HI diameter | SOURCE_NATIVE_READY | False | False | ngc4088_b1_source_native_radial_calibration_packet_not_endpoint |
| x_w | R_warp_onset_arcmin / R_HI_arcmin | 0.282353 | dimensionless | first-pass manual digitization plus HI radius | FIRST_PASS_DIMENSIONALLY_VALID_NOT_B1_ACCEPTED | False | False | ngc4088_b1_source_native_radial_calibration_packet_not_endpoint |
| Delta_x_w | Delta_R_onset_arcmin / R_HI_arcmin | 0.0705882 | dimensionless | frozen first-pass tolerance | FIRST_PASS_TOLERANCE_NOT_B1_ACCEPTED | False | False | ngc4088_b1_source_native_radial_calibration_packet_not_endpoint |

## Allowed Closure Routes

| route_id | route_status | allowed_inputs | required_output | acceptance_condition | why_not_currently_closed | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RC1_INDEPENDENT_REVIEWER_DIRECT_ARCMIN | READY | page76 ROI; worksheet overlay; page77 cross-check; HI diameter | onset_radius_side_a_arcmin; onset_radius_side_b_arcmin; x_w_independent | numeric side onsets and |x_w_independent-first_pass_x_w| <= frozen tolerance | review response remains pending | False | False | ngc4088_b1_source_native_radial_calibration_packet_not_endpoint |
| RC2_FROZEN_IMAGE_REPEAT_WITH_RADIAL_TICK_CALIBRATION | OPEN | page76 ROI; worksheet grid; printed coordinate/radial ticks; HI diameter | arcmin_per_pixel_or_direct_radial_axis_mapping plus onset radius | calibration reproducibly maps image departure to arcmin before scoring | current image repeat detects PA departure but lacks accepted source-native radial calibration | False | False | ngc4088_b1_source_native_radial_calibration_packet_not_endpoint |
| RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE | PREFERRED_OPEN_IF_AVAILABLE | original WHISP/FITS channel-map product or table with source-native coordinates | source-native warp onset radius with uncertainty | coordinate-calibrated source product reproduces or revises x_w without endpoint inputs | original data product is not yet cached in this package | False | False | ngc4088_b1_source_native_radial_calibration_packet_not_endpoint |
| RC4_FIRST_PASS_ONLY | NOT_ACCEPTABLE_FOR_FORMULA_FREEZE_ALONE | existing first-pass manual digitization | none | not applicable | dimensionally valid but not independent and not enough for B1 closure | False | False | ngc4088_b1_source_native_radial_calibration_packet_not_endpoint |

## Interpretation

The first-pass x_w conversion is dimensionally valid, and the frozen image
repeat detects a warp-like position-angle departure. B1 remains open
because an accepted source-native radial calibration is still missing for
the machine repeat, and the independent reviewer response is not filled.
