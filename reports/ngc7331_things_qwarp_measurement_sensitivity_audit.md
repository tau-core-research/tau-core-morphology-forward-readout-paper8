# NGC7331 THINGS q_warp Measurement Sensitivity Audit

Status: `CENTROID_STABLE_BUT_ENVELOPE_STRONGER_REVIEW_REQUIRED`.

This audit compares a conservative centroid q_warp observable with an
outer-envelope p80 observable across fixed moment-0 signal thresholds.
It is residual-blind and endpoint-blocked.

The purpose is to decide which source-native observable should be frozen
before any exact-transfer formula or endpoint score is allowed.

## Aggregate sensitivity

| galaxy | threshold_fraction_of_p95 | q_centroid_mean | q_centroid_spread | q_envelope_p80_mean | q_envelope_p80_spread | q_centroid_side_asymmetry_max | q_envelope_side_asymmetry_max | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | 0.1 | 0.00710511 | 0.00179469 | 0.216899 | 0.0208693 | 0.418022 | 0.210329 | False | False | ngc7331_things_qwarp_measurement_sensitivity_audit_not_endpoint |
| NGC7331 | 0.15 | 0.00666612 | 0.00181607 | 0.209391 | 0.0168385 | 0.522529 | 0.245838 | False | False | ngc7331_things_qwarp_measurement_sensitivity_audit_not_endpoint |
| NGC7331 | 0.2 | 0.00678703 | 0.00157726 | 0.203765 | 0.0129456 | 0.349811 | 0.250917 | False | False | ngc7331_things_qwarp_measurement_sensitivity_audit_not_endpoint |
| NGC7331 | 0.25 | 0.00752434 | 0.00162436 | 0.198832 | 0.0107401 | 0.166834 | 0.24778 | False | False | ngc7331_things_qwarp_measurement_sensitivity_audit_not_endpoint |
| NGC7331 | 0.3 | 0.00921478 | 0.000851173 | 0.194693 | 0.0101862 | 0.641678 | 0.237152 | False | False | ngc7331_things_qwarp_measurement_sensitivity_audit_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_QWS1_CENTROID_STABILITY | REVIEW_REQUIRED | centroid q range=0.00666612..0.00921478 | choose whether centroid or envelope observable is the correct q_warp carrier | False | False | ngc7331_things_qwarp_measurement_sensitivity_audit_not_endpoint |
| NGC7331 | N7331_QWS2_ENVELOPE_STRENGTH | REVIEW_REQUIRED | envelope p80 q range=0.194693..0.216899 | review whether warp/readout strength should track ridge centroid or outer envelope | False | False | ngc7331_things_qwarp_measurement_sensitivity_audit_not_endpoint |
| NGC7331 | N7331_QWS3_ENDPOINT_BLINDNESS | PASS | sensitivity audit reads THINGS moment-0 maps and geometry only | none at endpoint-blindness level | False | False | ngc7331_things_qwarp_measurement_sensitivity_audit_not_endpoint |

## Summary

| galaxy | sensitivity_status | q_centroid_mean_min | q_centroid_mean_max | q_envelope_p80_mean_min | q_envelope_p80_mean_max | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | CENTROID_STABLE_BUT_ENVELOPE_STRONGER_REVIEW_REQUIRED | 0.00666612 | 0.00921478 | 0.194693 | 0.216899 | False | False | False | freeze a source-native q_warp observable definition after independent review | ngc7331_things_qwarp_measurement_sensitivity_audit_not_endpoint |
