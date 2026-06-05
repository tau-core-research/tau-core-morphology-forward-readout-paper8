# NGC7331 THINGS q_warp First-Pass Measurement

Status: `NGC7331_THINGS_QWARP_FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED`.

This is a residual-blind source-native measurement candidate. It uses cached
THINGS H I moment-0 products and the previously frozen scalar geometry only.
It does not read observed rotation velocities, residuals, baseline scores, or
best-fit readout-family information.

The result is not an accepted formula input. The PA/ridge definition, sign rule,
and epsilon_cross bound still require independent review before exact-transfer
formula freeze or endpoint scoring.

## Product measurements

| galaxy | product_id | source_product_path | threshold_rule | p95_positive_mom0 | signal_threshold | inner_signal_pixels | outer_side_a_pixels | outer_side_b_pixels | inner_disk_pa_image_deg | inner_axis_ratio_from_mom0 | v_inner_side_a_pix | v_inner_side_b_pix | v_outer_side_a_pix | v_outer_side_b_pix | outer_ridge_offset_side_a_pix | outer_ridge_offset_side_b_pix | local_disk_reference_extent_pix | side_a_weight | side_b_weight | q_side_a | q_side_b | q_warp_first_pass | side_asymmetry_fraction | endpoint_scores_allowed | uses_vobs_or_residual | measurement_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NA_MOM0 | data/external/literature/ngc7331_things_hi_route/NGC_7331_NA_MOM0_THINGS.FITS | positive_mom0_pixels_above_0p20_p95 | 119.534 | 23.9068 | 24619 | 3853 | 6984 | 79.8886 | 0.345191 | 4.48192 | 3.23607 | 3.59707 | 2.61468 | 0.88485 | 0.621399 | 117.663 | 0.320323 | 0.679677 | 0.00752022 | 0.00528119 | 0.0059984 | 0.373272 | False | False | FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED | ngc7331_things_qwarp_first_pass_measurement_not_endpoint |
| NGC7331 | RO_MOM0 | data/external/literature/ngc7331_things_hi_route/NGC_7331_RO_MOM0_THINGS.FITS | positive_mom0_pixels_above_0p20_p95 | 99.2223 | 19.8445 | 23211 | 4036 | 6523 | 79.9889 | 0.361658 | 5.01879 | 3.65222 | 3.93385 | 2.86206 | 1.08495 | 0.790155 | 117.663 | 0.343354 | 0.656646 | 0.00922081 | 0.00671542 | 0.00757566 | 0.330716 | False | False | FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED | ngc7331_things_qwarp_first_pass_measurement_not_endpoint |

## First-pass response

| galaxy | response_id | inner_disk_pa_image_deg_first_pass | inner_disk_pa_product_spread_deg | q_warp_first_pass | q_warp_uncertainty_first_pass | side_asymmetry_fraction_max | sigma_warp_sign | epsilon_cross_bound_or_interval | response_status | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_THINGS_QWARP_FIRST_PASS_RESPONSE_V1 | 79.9387 | 0.100276 | 0.00678703 | 0.0012667 | 0.373272 | <NA> | <NA> | FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | False | ngc7331_things_qwarp_first_pass_measurement_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_QWFP1_SOURCE_PRODUCTS | PASS | NA_MOM0 and RO_MOM0 THINGS maps measured from local FITS cache | none at product availability level | False | False | ngc7331_things_qwarp_first_pass_measurement_not_endpoint |
| NGC7331 | N7331_QWFP2_SOURCE_NATIVE_PA | FIRST_PASS_REVIEW_REQUIRED | inner PA image-frame mean=79.9387 deg; product spread=0.100276 deg | independent reviewer or literature PA profile must accept/reject orientation reference | False | False | ngc7331_things_qwarp_first_pass_measurement_not_endpoint |
| NGC7331 | N7331_QWFP3_QWARP_MEASUREMENT | FIRST_PASS_REVIEW_REQUIRED | q_warp_first_pass=0.00678703; uncertainty=0.0012667 | review threshold, ridge definition, and product agreement before formula freeze | False | False | ngc7331_things_qwarp_first_pass_measurement_not_endpoint |
| NGC7331 | N7331_QWFP4_SIGN_AND_CROSS_TERMS | BLOCKED_REVIEW_REQUIRED | source-native q_warp candidate exists, but sigma sign and epsilon_cross remain unfilled | derive sign and cross-term bound from MOM1/context before exact transfer | False | False | ngc7331_things_qwarp_first_pass_measurement_not_endpoint |
| NGC7331 | N7331_QWFP5_ENDPOINT_BLINDNESS | PASS | script reads THINGS moment maps and geometry only; no vobs/residual/baseline columns | keep endpoint scoring in a separate script after freeze | False | False | ngc7331_things_qwarp_first_pass_measurement_not_endpoint |

## Summary

| galaxy | qwarp_first_pass_status | n_products_measured | q_warp_first_pass | q_warp_uncertainty_first_pass | inner_disk_pa_image_deg_first_pass | sign_ready | epsilon_cross_ready | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_THINGS_QWARP_FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED | 2 | 0.00678703 | 0.0012667 | 79.9387 | False | False | False | False | False | independent review of PA/ridge threshold plus MOM1 sign and epsilon_cross extraction | ngc7331_things_qwarp_first_pass_measurement_not_endpoint |
