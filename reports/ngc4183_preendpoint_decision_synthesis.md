# NGC4183 Pre-Endpoint Decision Synthesis

Status: `NGC4183_PREENDPOINT_SYNTHESIS_WEAK_PROJECTION_CONTROL_NOT_ENDPOINT`

This synthesis combines the NGC4183 source audit, observable sheet, label gate,
formula derivation, coefficient gate, tilted-ring extraction, and projection
upper-bound gate.  It does not score an endpoint.

## Summary

| preendpoint_decision_status | galaxy | current_role | strong_endpoint_supported | gamma_projection_upper_bound | max_abs_pa_drift_deg | max_abs_inclination_drift_deg | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary | next_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183_PREENDPOINT_SYNTHESIS_WEAK_PROJECTION_CONTROL_NOT_ENDPOINT | NGC4183 | WEAK_PROJECTION_CONTROL_CANDIDATE | False | 0.00269837 | 3 | 0 | False | False | ngc4183_preendpoint_decision_synthesis_not_endpoint | either_independent_source_review_then_null_control_freeze_or_acquire_better_velocity_field |

## Gate Chain

| stage | status | allowed_next | endpoint_scores_allowed | main_message |
| --- | --- | --- | --- | --- |
| source_audit | NGC4183_MIXED_OVERLAY_SOURCE_AUDIT_LOCAL_SOURCE_PRESENT_REVIEW_REQUIRED_NOT_FREEZE_READY | observable_sheet | False | galaxy-specific H I source is present |
| observable_sheet | NGC4183_MIXED_OVERLAY_OBSERVABLE_SHEET_PARTIAL_PASS_LABEL_AND_FORMULA_BLOCKED | label_narrowing | False | RHI and projection observables are available; broad overlay fields missing |
| label_gate | NARROW_REPLACEMENT_LABEL_SUPPORTED_FOR_FORMULA_DERIVATION_NOT_ENDPOINT | formula_derivation | False | narrow projection/outer-warp caveated label supported for derivation |
| formula_derivation | NGC4183_PROJECTION_OUTER_WARP_FORMULA_SHELL_DERIVED_FREEZE_BLOCKED | coefficient_gate | False | projection attenuation shell derived; coefficient blocked |
| gamma_coefficient_gate | NGC4183_PROJECTION_GAMMA_RULE_BLOCKED_SOURCE_NATIVE_RADIAL_MODEL_REQUIRED | tilted_ring_profile_review | False | no source-blind gamma coefficient frozen |
| tilted_ring_profile | NGC4183_TILTED_RING_PROFILE_EXTRACTED_REVIEW_REQUIRED_NOT_FREEZE_READY | upper_bound_or_independent_review | False | source profile extracted; nearly constant orientation |
| gamma_upper_bound | NGC4183_PROJECTION_GAMMA_UPPER_BOUND_DERIVED_WEAK_NOT_ENDPOINT | weak_control_or_more_data | False | source-side projection bound is very small |

## Decisions

| decision_id | decision | evidence | consequence |
| --- | --- | --- | --- |
| D1_STRONG_ENDPOINT | REJECT_FOR_NOW | gamma upper bound 0.00269837 | do not run NGC4183 as a strong projection endpoint from current sources |
| D2_WEAK_PROJECTION_CONTROL | PROMOTE_AS_CONTROL_CANDIDATE | source-native H I profile supports edge-on/projection caveat but weak radial orientation drift | NGC4183 can test whether the protocol correctly predicts a near-carrier result |
| D3_MORE_DATA_ROUTE | OPTIONAL_ACQUIRE | OCR profile needs independent review; no numeric warp onset/amplitude | machine-readable tilted-ring or velocity-field source could reopen endpoint path |
| D4_NO_RESIDUAL_PATCHING | PASS_GUARDRAIL | all gates keep endpoint_scores_allowed=False | do not tune gamma_proj using observed rotation residuals |

## Scientific Interpretation

NGC4183 is no longer merely a context-only candidate: it has source-native H I
geometry, a strong edge-on projection observable, and a consistent H I support
radius.  However, the extracted tilted-ring orientation profile is almost flat:
the PA drift is only about 3 degrees and the inclination drift is zero in the
current extraction.  The resulting source-side projection coefficient bound is
therefore tiny.

This is useful.  It means the pipeline should not force NGC4183 into a strong
Tau Core projection endpoint.  With the present sources it is better treated as
a weak-projection control candidate: the protocol predicts that a large
projection correction is not source-supported.  A stronger endpoint route would
require better source-native velocity-field or tilted-ring data, not residual
tuning.
