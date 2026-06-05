# NGC4183 Null-Control Formula Freeze Gate

Status: `NGC4183_NULL_CONTROL_FORMULA_FROZEN_NOT_ENDPOINT`

This gate freezes, or blocks freezing, the NGC4183 weak-projection/null-control
formula.  It does not run endpoint scoring.

## Summary

| null_control_formula_freeze_status | galaxy | gamma_bound | max_velocity_fractional_change | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary | next_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183_NULL_CONTROL_FORMULA_FROZEN_NOT_ENDPOINT | NGC4183 | 0.00269837 | 0.0013501 | True | False | ngc4183_null_control_formula_freeze_gate_not_endpoint | accepted_null_control_gate |

## Manifest

| galaxy | formula_id | freeze_status | formula | carrier | gamma_bound | max_velocity_fractional_change | sign | kernel | coefficient_rule | coefficient_rule_status | uses_vobs_or_residual | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183 | N4183_WEAK_PROJECTION_NULL_CONTROL_BOUND | NGC4183_NULL_CONTROL_FORMULA_FROZEN_NOT_ENDPOINT | v_readout^2/v_carrier^2 in [1-gamma_bound, 1] | predeclared smooth exponential-disk carrier | 0.00269837 | 0.0013501 | bounded_attenuation_or_zero | source-side orientation drift upper bound | gamma_bound = p_edge * max_R{sin^2(Delta PA), sin^2(Delta i)} | FROZEN_AFTER_INDEPENDENT_REVIEW | False | True | False | ngc4183_null_control_formula_freeze_gate_not_endpoint |

## Gates

| gate_id | gate_status | evidence | remaining_obligation |
| --- | --- | --- | --- |
| N4183_NCFF_G1_READINESS | PASS | NGC4183_NULL_CONTROL_FREEZE_READY_REVIEW_ACCEPTED_NOT_ENDPOINT | none |
| N4183_NCFF_G2_VISUAL_PACKET | PASS | NGC4183_VISUAL_REVIEW_PACKET_READY_RESPONSE_RECEIVED | review response still required before freeze |
| N4183_NCFF_G3_DIMENSIONS_AND_LIMITS | PASS | v2 ratios are dimensionless; gamma_bound->0 recovers carrier | none for formula shell |
| N4183_NCFF_G4_ENDPOINT_SCORE | BLOCKED | null-control formula freeze is not endpoint validation | separate accepted endpoint/control gate required after freeze |

## Frozen/Blocked Formula

```text
v_readout^2 / v_carrier^2 in [1 - gamma_bound, 1]
gamma_bound = p_edge * max_R { sin^2(Delta PA), sin^2(Delta i) }
gamma_bound = 0.00269837
|Delta v|/v <= 0.00135010
```

## Verdict

The formula shell is dimensionally consistent and has the correct carrier
limit.  It remains blocked until the independent tilted-ring review response
accepts or corrects the source profile and explicitly authorizes null-control
freeze.
