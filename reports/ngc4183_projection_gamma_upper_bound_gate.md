# NGC4183 Projection Gamma Upper-Bound Gate

Status: `NGC4183_PROJECTION_GAMMA_UPPER_BOUND_DERIVED_WEAK_NOT_ENDPOINT`

This is a source-side upper-bound derivation, not an endpoint score.  It asks
whether the extracted NGC4183 tilted-ring orientation profile can support a
large projection attenuation coefficient.

## Summary

| upper_bound_gate_status | galaxy | p_edge | max_twist_kernel_sin2_delta_pa | max_inclination_kernel_sin2_delta_i | gamma_projection_upper_bound | strong_projection_endpoint_supported | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary | next_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183_PROJECTION_GAMMA_UPPER_BOUND_DERIVED_WEAK_NOT_ENDPOINT | NGC4183 | 0.985148 | 0.00273905 | 0 | 0.00269837 | False | False | False | ngc4183_projection_gamma_upper_bound_gate_not_endpoint | decide_ngc4183_as_weak_projection_control_or_acquire_higher_quality_orientation_profile |

## Components

| component_id | value | unit | source | status | interpretation |
| --- | --- | --- | --- | --- | --- |
| edge_on_kernel_strength | 0.985148 | dimensionless | NGC4183 projection formula summary | SOURCE_SIDE_ACCEPTED_CAVEATED | large edge-on factor, already assigned to K_proj |
| max_pa_twist_kernel | 0.00273905 | dimensionless | tilted-ring PA drift profile | OCR_REVIEW_REQUIRED | small radial orientation drift |
| max_inclination_drift_kernel | 0 | dimensionless | tilted-ring inclination drift profile | OCR_REVIEW_REQUIRED | zero inclination drift in extracted profile |
| gamma_projection_upper_bound | 0.00269837 | dimensionless | p_edge * max(orientation drift kernels) | FORMULA_CONDITIONAL_UPPER_BOUND_NOT_FREEZE | source-side bound is too small for a strong correction |

## Gates

| gate_id | gate_status | evidence | remaining_obligation |
| --- | --- | --- | --- |
| N4183_UB_G1_SOURCE_PROFILE_AVAILABLE | PASS_REVIEW_REQUIRED | NGC4183_TILTED_RING_PROFILE_EXTRACTED_REVIEW_REQUIRED_NOT_FREEZE_READY | independent review of OCR/profile extraction |
| N4183_UB_G2_DIMENSIONLESS_BOUND | PASS | p_edge and orientation drift kernels are dimensionless | none for upper-bound algebra |
| N4183_UB_G3_BOUND_STRENGTH | WEAK_CORRECTION_BOUND | gamma_upper_bound=0.00269837 | treat as limiting evidence, not a strong endpoint candidate |
| N4183_UB_G4_ENDPOINT_SCORE_ALLOWED | BLOCKED | upper bound only; no frozen predictive coefficient rule | either freeze as a null/weak-control formula after review or acquire stronger source profile |

## Profile Bound Preview

| radius_arcsec | x_R_over_RHI | delta_pa_deg | delta_i_deg | gamma_profile_bound |
| --- | --- | --- | --- | --- |
| 10 | 0.0546448 | 0 | 0 | 0 |
| 20 | 0.10929 | 0 | 0 | 0 |
| 30 | 0.163934 | 0 | 0 | 0 |
| 40 | 0.218579 | 0 | 0 | 0 |
| 50 | 0.273224 | 0 | 0 | 0 |
| 60 | 0.327869 | 0 | 0 | 0 |
| 70 | 0.382514 | 0 | 0 | 0 |
| 80 | 0.437158 | 0 | 0 | 0 |
| 90 | 0.491803 | 0 | 0 | 0 |
| 100 | 0.546448 | 0 | 0 | 0 |
| 110 | 0.601093 | 0 | 0 | 0 |
| 120 | 0.655738 | 0 | 0 | 0 |

## Derived Bound

Definition:

```text
gamma_proj <= p_edge * max_R { sin^2(Delta PA(R)), sin^2(Delta i(R)) }
```

For the current NGC4183 source profile:

```text
p_edge = 0.985148
max sin^2(Delta PA) = 0.002739
max sin^2(Delta i)  = 0.000000
gamma_proj <= 0.002698
```

## Verdict

The source-side projection bound is very small.  This is useful limiting
evidence: NGC4183 can remain a projection/outer-warp caveated object, but the
currently extracted orientation profile does not support a strong projection
attenuation endpoint.  The fair next choice is either to treat NGC4183 as a
weak-projection control after independent review, or to acquire a higher-quality
machine-readable tilted-ring/velocity-field source before scoring.
