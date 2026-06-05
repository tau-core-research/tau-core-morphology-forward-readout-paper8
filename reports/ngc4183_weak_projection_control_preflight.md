# NGC4183 Weak-Projection Control Preflight

Status: `NGC4183_WEAK_PROJECTION_CONTROL_PREFLIGHT_COMPLETE_NOT_ENDPOINT`

This is a control preflight, not an endpoint score.  It uses the source-side
projection upper bound to decide whether NGC4183 is a strong correction
candidate or a near-carrier control candidate.

## Summary

| weak_control_preflight_status | galaxy | recommended_role | gamma_projection_upper_bound | max_velocity_fractional_change | strong_projection_endpoint_supported | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary | next_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183_WEAK_PROJECTION_CONTROL_PREFLIGHT_COMPLETE_NOT_ENDPOINT | NGC4183 | WEAK_PROJECTION_NULL_CONTROL_AFTER_REVIEW | 0.00269837 | 0.0013501 | False | False | False | ngc4183_weak_projection_control_preflight_not_endpoint | independent_profile_review_then_optional_null_control_freeze |

## Control Formulas

| formula_id | formula | gamma_bound | max_velocity_fractional_change | formula_status | dimension_check | limit_check | uses_vobs_or_residual | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N4183_WEAK_PROJECTION_NULL_CONTROL_BOUND | v_readout^2/v_carrier^2 in [1-gamma_bound, 1] | 0.00269837 | 0.0013501 | CONTROL_BOUND_DERIVED_REVIEW_REQUIRED_NOT_FREEZE | all terms dimensionless ratios | gamma_bound -> 0 recovers carrier exactly | False | False | False | ngc4183_weak_projection_control_preflight_not_endpoint |
| N4183_NEAR_CARRIER_CONTROL_READOUT | v_readout^2 ~= v_carrier^2 within gamma_bound | 0.00269837 | 0.0013501 | NULL_CONTROL_CANDIDATE_AFTER_INDEPENDENT_SOURCE_REVIEW | velocity-squared carrier retained | no residual-side correction introduced | False | False | False | ngc4183_weak_projection_control_preflight_not_endpoint |

## Gates

| gate_id | gate_status | evidence | remaining_obligation |
| --- | --- | --- | --- |
| N4183_WPC_G1_PREENDPOINT_DECISION | PASS | NGC4183_PREENDPOINT_SYNTHESIS_WEAK_PROJECTION_CONTROL_NOT_ENDPOINT | none for preflight |
| N4183_WPC_G2_NEAR_CARRIER_BOUND | PASS | gamma_bound=0.00269837; velocity fractional bound=0.0013501 | independent source review before freeze |
| N4183_WPC_G3_ENDPOINT_USE | BLOCKED | control preflight is not formula freeze or scoring | review OCR/profile extraction; then optionally freeze as null-control |

## Interpretation

The current source-side bound implies:

```text
v_readout^2 / v_carrier^2 >= 1 - 0.002698
|Delta v| / v_carrier <= 0.001350
```

So the present NGC4183 sources do not support a large Tau Core projection
correction.  The scientifically useful role is a weak-projection/null-control
case: the pipeline predicts a near-carrier readout unless better independent
velocity-field evidence reveals a larger source-side orientation effect.
