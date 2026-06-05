# NGC7331 THINGS q_warp Measurement Worksheet

This worksheet fixes the source-native THINGS map geometry and declares
the residual-blind measurements needed for q_warp, sigma_warp, and
epsilon_cross. It does not fill those measurements and does not score
the rotation curve.

## Geometry

| galaxy | geometry_id | reference_product | crpix1 | crpix2 | crval1_deg | crval2_deg | arcsec_per_pixel | kpc_per_pixel | rdisk_kpc | rhi_kpc | x_warp_onset_over_rhi | warp_onset_kpc | rdisk_pix | rhi_pix | warp_onset_pix | inclination_deg | inner_disk_pa_deg | pa_status | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_THINGS_GEOM_V1 | NGC_7331_NA_MOM0_THINGS.FITS | 512 | 513 | 339.267 | 34.4156 | 1.5 | 0.106901 | 5.02 | 27.01 | 0.534309 | 14.4317 | 46.9592 | 252.663 | 135 | 75 | <NA> | PENDING_SOURCE_MEASUREMENT_OR_LITERATURE_VALUE | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |

## Worksheet

| galaxy | target_id | target_class | source_product | measurement | unit | accepted_value | measurement_rule | status | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_QW1_INNER_DISK_PA | orientation_reference | NA_MOM1;RO_MOM1;literature_PA_profile | inner_disk_pa_deg | deg | <NA> | freeze inner disk line-of-nodes/major-axis PA before measuring ridge offsets | MEASUREMENT_PENDING | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |
| NGC7331 | N7331_QW2_OUTER_RIDGE_OFFSET_SIDE_A | q_warp_strength | NA_MOM0;RO_MOM0 | outer_ridge_offset_side_a_pix | pixel | <NA> | measure residual-blind outer H I ridge displacement from inner disk reference on side A | MEASUREMENT_PENDING | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |
| NGC7331 | N7331_QW3_OUTER_RIDGE_OFFSET_SIDE_B | q_warp_strength | NA_MOM0;RO_MOM0 | outer_ridge_offset_side_b_pix | pixel | <NA> | measure residual-blind outer H I ridge displacement from inner disk reference on side B | MEASUREMENT_PENDING | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |
| NGC7331 | N7331_QW4_LOCAL_REFERENCE_EXTENT | q_warp_normalization | NA_MOM0;RO_MOM0 | local_disk_reference_extent_pix | pixel | <NA> | use same map frame; default reference candidates are warp_onset_pix to rhi_pix | MEASUREMENT_PENDING | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |
| NGC7331 | N7331_QW5_SIDE_RELIABILITY_WEIGHTS | q_warp_weighting | NA_MOM0;RO_MOM0;source_quality_review | side_a_weight;side_b_weight | dimensionless | <NA> | assign side weights from source quality only, not from rotation residuals | MEASUREMENT_PENDING | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |
| NGC7331 | N7331_QW6_SIGMA_WARP_SIGN | sign_rule | NA_MOM1;RO_MOM1;Bosma tilted-ring context | sigma_warp_sign | sign_or_enum | <NA> | decide added-readout vs attenuation from source-side orientation/readout geometry | MEASUREMENT_PENDING | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |
| NGC7331 | N7331_QW7_EPSILON_CROSS_BOUND | cross_term_bound | NA_MOM0;NA_MOM1;RO_MOM0;RO_MOM1;context_sources | epsilon_cross_bound_or_interval | dimensionless | <NA> | bound orientation, side-asymmetry, history/context, and locality cross terms | MEASUREMENT_PENDING | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |

## Response Template

| galaxy | response_id | inner_disk_pa_deg | outer_ridge_offset_side_a_pix | outer_ridge_offset_side_b_pix | local_disk_reference_extent_pix | side_a_weight | side_b_weight | q_warp_measured | q_warp_uncertainty | sigma_warp_sign | epsilon_cross_bound_or_interval | response_status | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_THINGS_QWARP_RESPONSE_V1 | <NA> | <NA> | <NA> | <NA> | <NA> | <NA> | <NA> | <NA> | <NA> | <NA> | RESPONSE_EMPTY_MEASUREMENT_PENDING | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_QWG1_THINGS_PRODUCTS_AUDITED | PASS | NGC7331_THINGS_HI_PRODUCTS_AUDITED_WORKSHEET_READY | none at product-audit level | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |
| NGC7331 | N7331_QWG2_GEOMETRY_SCALES_DEFINED | PASS | Rdisk=5.020 kpc, RHI=27.010 kpc, x_w=0.534309 | none at scalar geometry level | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |
| NGC7331 | N7331_QWG3_PA_REFERENCE | BLOCKED_MEASUREMENT_PENDING | inner_disk_pa_deg is not frozen in this worksheet | measure from THINGS MOM1/MOM0 or cite source PA profile | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |
| NGC7331 | N7331_QWG4_Q_WARP_RESPONSE | BLOCKED_MEASUREMENT_PENDING | q_warp response fields are empty | fill ridge offsets, reference extent, and side weights | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |
| NGC7331 | N7331_QWG5_ENDPOINT_BLINDNESS | PASS | worksheet uses map geometry and source products only | do not score until formula freeze passes | False | False | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |

## Summary

| galaxy | qwarp_worksheet_status | n_measurement_targets | n_gates | n_pass | n_blocked | things_products_audited | geometry_defined | pa_reference_frozen | q_warp_measurement_ready | sigma_warp_sign_ready | epsilon_cross_bound_ready | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | population_claim_allowed | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_THINGS_QWARP_WORKSHEET_READY_MEASUREMENT_PENDING | 7 | 5 | 3 | 2 | True | True | False | False | False | False | False | False | False | False | fill inner PA, ridge offsets, side weights, sign, and cross-term response fields | ngc7331_things_qwarp_measurement_worksheet_not_endpoint |
