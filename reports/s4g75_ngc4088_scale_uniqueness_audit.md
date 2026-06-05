# NGC4088 Scale-Uniqueness Audit

This audit enumerates residual-blind, dimensionally valid scale carriers
for the NGC4088 warp/asymmetry readout lane. It does not compare any
scale to observed velocities.

## Verdict

The current `x_w * Vflat^2` carrier is a valid selected candidate, but it
is not unique at theory level. Several residual-blind alternatives exist,
so `SCALE_UNIQUENESS` remains blocked until a Tau-side principle selects
or rejects them without endpoint residual tuning.

## Scale Candidates

| galaxy | scale_id | scale_formula | scale_value_km2_s2 | current_prefactor_ratio | source_status | uses_vobs_or_residual | selection_status | tau_side_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | CURRENT_XW_VFLAT2 | x_w * Vflat^2 | 8324.02 | 1 | CURRENT_FORMULA_CONDITIONAL_CANDIDATE | False | SELECTED_CANDIDATE_NOT_UNIQUE | derive why onset fraction times catalog flat-speed carrier is selected | False | s4g75_ngc4088_scale_uniqueness_audit_not_endpoint |
| NGC4088 | XW_MEDIAN_VN2 | x_w * median_r(v_n^2) | 6038.61 | 0.725444 | RESIDUAL_BLIND_BARYONIC_SCALE_ALTERNATIVE | False | ALTERNATIVE_NOT_SELECTED | rule out if flat-speed carrier is required rather than baryonic readout carrier | False | s4g75_ngc4088_scale_uniqueness_audit_not_endpoint |
| NGC4088 | XW_MEDIAN_VV62 | x_w * median_r(v_v6^2) | 12316.1 | 1.47959 | RESIDUAL_BLIND_TPG_CLOSURE_SCALE_ALTERNATIVE | False | ALTERNATIVE_NOT_SELECTED | rule out if external TPG-like closure carrier is not allowed as Tau-side normalizer | False | s4g75_ngc4088_scale_uniqueness_audit_not_endpoint |
| NGC4088 | CLOSURE_FRACTION_MEDIAN_VN2 | c_g * median_r(v_n^2) | 10509.2 | 1.26251 | TAU_SOURCE_NORMALIZATION_RULE_ALTERNATIVE | False | ALTERNATIVE_NOT_SELECTED | decide whether NGC4088 warp lane must use local closure fraction instead of x_w | False | s4g75_ngc4088_scale_uniqueness_audit_not_endpoint |
| NGC4088 | XW_CLOSURE_FRACTION_MEDIAN_VN2 | x_w * c_g * median_r(v_n^2) | 2967.29 | 0.356473 | COMPOSITE_ONSET_CLOSURE_SCALE_ALTERNATIVE | False | ALTERNATIVE_NOT_SELECTED | derive or reject a two-factor onset-plus-closure carrier | False | s4g75_ngc4088_scale_uniqueness_audit_not_endpoint |

## Summary

| galaxy | n_scale_candidates | n_dimensionally_valid | n_residual_blind | current_scale_id | current_prefactor_km2_s2 | scale_uniqueness_decision | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 5 | 5 | 5 | CURRENT_XW_VFLAT2 | 8324.02 | BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES | False | s4g75_ngc4088_scale_uniqueness_audit_not_endpoint |

## Claim Boundary

This is a theory audit, not a performance diagnostic. The listed scales
must not be selected by endpoint scores.
