# NGC7331 THINGS MOM1 Sign/Cross-Term Review

Status: `NGC7331_THINGS_MOM1_SIGN_CROSS_REVIEW_BUILT_FREEZE_BLOCKED`.

This packet measures residual-blind kinematic orientation context from
THINGS moment-1 maps. It does not freeze the B2 sign and it does not
close epsilon_cross.

## MOM1 measurements

| galaxy | product_prefix | mom0_path | mom1_path | threshold_rule | systemic_velocity_km_s_source_native | morph_pa_image_deg | kinematic_pa_image_deg | morph_kin_delta_pa_deg | f_pa | v_side_a_inner_km_s | v_side_b_inner_km_s | v_side_a_outer_km_s | v_side_b_outer_km_s | receding_side_inner | inner_outer_receding_orientation_same | outer_to_inner_velocity_contrast_ratio | f_velocity_side_asymmetry | n_inner_pixels | n_outer_pixels | endpoint_scores_allowed | uses_vobs_or_residual | measurement_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NATURAL | data/external/literature/ngc7331_things_hi_route/NGC_7331_NA_MOM0_THINGS.FITS | data/external/literature/ngc7331_things_hi_route/NGC_7331_NA_MOM1_THINGS.FITS | mom0_positive_above_0p20_p95_and_finite_mom1 | 817.61 | 79.8886 | -102.566 | 2.45489 | 0.0428328 | -135.673 | 124.992 | -207.797 | 211.077 | B_NEG_MAJOR_AXIS | True | 1.60694 | 0.0156604 | 24619 | 11166 | False | False | MOM1_KINEMATIC_CONTEXT_REVIEW_REQUIRED | ngc7331_things_mom1_sign_cross_review_not_endpoint |
| NGC7331 | ROBUST | data/external/literature/ngc7331_things_hi_route/NGC_7331_RO_MOM0_THINGS.FITS | data/external/literature/ngc7331_things_hi_route/NGC_7331_RO_MOM1_THINGS.FITS | mom0_positive_above_0p20_p95_and_finite_mom1 | 819.978 | 79.9889 | -102.058 | 2.04668 | 0.0357138 | -133.127 | 120.742 | -204.095 | 206.924 | B_NEG_MAJOR_AXIS | True | 1.61902 | 0.0137621 | 23211 | 10953 | False | False | MOM1_KINEMATIC_CONTEXT_REVIEW_REQUIRED | ngc7331_things_mom1_sign_cross_review_not_endpoint |

## Review response

| galaxy | response_id | receding_side_consensus | inner_outer_receding_orientation_same_all | f_pa_max | f_velocity_side_asymmetry_max | f_q_observable_choice | f_context_complex_warp | epsilon_cross_candidate_bound | sigma_warp_sign_status | epsilon_cross_status | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_THINGS_MOM1_SIGN_CROSS_REVIEW_V1 | CONSISTENT | True | 0.0428328 | 0.0156604 | 0.961416 | 1 | 0.488571 | KINEMATIC_CONTEXT_AVAILABLE_SIGN_NOT_FROZEN | CANDIDATE_BOUND_REVIEW_REQUIRED_NOT_CLOSED | False | False | False | ngc7331_things_mom1_sign_cross_review_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_MOM1SC1_PRODUCTS | PASS | NA_MOM1 and RO_MOM1 are cached and paired with MOM0 masks | none at product availability level | False | False | ngc7331_things_mom1_sign_cross_review_not_endpoint |
| NGC7331 | N7331_MOM1SC2_KINEMATIC_ORIENTATION | REVIEW_REQUIRED | max morph/kin delta PA=0.0428328 as sin(delta); consensus=CONSISTENT | independent review must define sign convention for B2 added-readout vs attenuation | False | False | ngc7331_things_mom1_sign_cross_review_not_endpoint |
| NGC7331 | N7331_MOM1SC3_EPSILON_CROSS | CANDIDATE_BOUND_REVIEW_REQUIRED | epsilon_cross_candidate_bound=0.488571 | review f_pa, f_R, f_q, and context factor before accepting or carrying interval | False | False | ngc7331_things_mom1_sign_cross_review_not_endpoint |
| NGC7331 | N7331_MOM1SC4_FORMULA_FREEZE | BLOCKED | sign not frozen and epsilon_cross bound not closed | freeze sign and close/carry epsilon_cross before exact B2 transfer | False | False | ngc7331_things_mom1_sign_cross_review_not_endpoint |
| NGC7331 | N7331_MOM1SC5_ENDPOINT_BLINDNESS | PASS | script reads THINGS moment maps and source geometry only | none at endpoint-blindness level | False | False | ngc7331_things_mom1_sign_cross_review_not_endpoint |

## Summary

| galaxy | mom1_sign_cross_status | n_products_measured | sigma_warp_sign_ready | epsilon_cross_bound_ready | epsilon_cross_candidate_bound | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_THINGS_MOM1_SIGN_CROSS_REVIEW_BUILT_FREEZE_BLOCKED | 2 | False | False | 0.488571 | False | False | False | independent sign review and accepted epsilon_cross interval/decision | ngc7331_things_mom1_sign_cross_review_not_endpoint |
