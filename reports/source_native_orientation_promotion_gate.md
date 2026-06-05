# Source-Native Orientation Promotion Gate

This audit asks whether the predeclared source-normalization orientation
signs can be promoted from theory-conditional bridge signs to
source-native readout-orientation candidates. It computes no endpoint
scores and uses no rotation residuals.

## Verdict

- Family orientations promoted: 3/4
- Family orientations blocked: 1/4
- Active components promoted: 295/406
- Active components blocked: 111/406
- Galaxies orientation-ready: 67/175
- Galaxies orientation-blocked: 108/175

The proxy-gate blocker has already been resolved by the conservative
E_tau readout-admission product. This audit shows the next blocker:
orientation promotion is partially source-native at the family level,
but still blocked for galaxies whose active components require the
thick/flared vertical channel or have proxy/missing component evidence.

## Family Orientation Gate

| component_family | predeclared_orientation_sign | expected_orientation_sign | sign_matches_family_rule | orientation_role | promotion_basis | required_statuses | n_components | n_required_source_components | n_proxy_components | n_missing_components | status_counts | promotion_status | endpoint_scores_computed | uses_vobs_or_residual | weakest_step | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K_compact_finite | 1 | 1 | True | positive finite-source residual orientation | compact/core finite-support source candidate | SOURCE_CANDIDATE_COMPACT_READY | 49 | 48 | 0 | 1 | MISSING_SOURCE_SUPPORT:1;SOURCE_CANDIDATE_COMPACT_READY:48 | PROMOTED_WITHIN_CURRENT_BRIDGE_READOUT_GEOMETRY | False | False | needs covariant/source-native variational promotion before physical acceptance | source_native_orientation_promotion_gate_not_endpoint |
| K_exponential_disk | -1 | -1 | True | negative smoothing/counter-readout orientation | S4G disk-scale source candidate | SOURCE_CANDIDATE_S4G_SCALE_READY | 76 | 75 | 0 | 1 | MISSING_SOURCE_SUPPORT:1;SOURCE_CANDIDATE_S4G_SCALE_READY:75 | PROMOTED_WITHIN_CURRENT_BRIDGE_READOUT_GEOMETRY | False | False | needs covariant/source-native variational promotion before physical acceptance | source_native_orientation_promotion_gate_not_endpoint |
| K_scale_tail_spiral | 1 | 1 | True | positive n=2 tail/closure-source orientation | HI/tail source candidate | SOURCE_CANDIDATE_HI_TAIL_READY | 173 | 172 | 0 | 1 | MISSING_SOURCE_SUPPORT:1;SOURCE_CANDIDATE_HI_TAIL_READY:172 | PROMOTED_WITHIN_CURRENT_BRIDGE_READOUT_GEOMETRY | False | False | needs covariant/source-native variational promotion before physical acceptance | source_native_orientation_promotion_gate_not_endpoint |
| K_thick_flared | -1 | -1 | True | negative projection/vertical smoothing orientation | velocity-field or vertical-structure source candidate | SOURCE_CANDIDATE_VELOCITY_FIELD_READY | 108 | 0 | 105 | 3 | MISSING_SOURCE_SUPPORT:3;PROXY_OR_PARTIAL_SOURCE_ONLY:105 | BLOCKED_SOURCE_NATIVE_ORIENTATION_EVIDENCE_MISSING | False | False | required source-native orientation evidence is not assembled | source_native_orientation_promotion_gate_not_endpoint |

## Summary

| split | n_galaxies | n_family_orientation_promoted | n_family_orientation_blocked | n_active_components | n_promoted_active_components | n_blocked_active_components | n_galaxies_orientation_ready | n_galaxies_orientation_blocked | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 175 | 3 | 1 | 406 | 295 | 111 | 67 | 108 | False | source_native_orientation_promotion_gate_not_endpoint |
| holdout | 44 | 3 | 1 | 107 | 79 | 28 | 16 | 28 | False | source_native_orientation_promotion_gate_not_endpoint |
| train | 131 | 3 | 1 | 299 | 216 | 83 | 51 | 80 | False | source_native_orientation_promotion_gate_not_endpoint |

## Active Component Status Counts

| component_family | component_orientation_status | n_components |
| --- | --- | --- |
| K_compact_finite | BLOCKED_COMPONENT_SOURCE_NOT_ACCEPTED | 1 |
| K_compact_finite | COMPONENT_ORIENTATION_PROMOTED | 48 |
| K_exponential_disk | BLOCKED_COMPONENT_SOURCE_NOT_ACCEPTED | 1 |
| K_exponential_disk | COMPONENT_ORIENTATION_PROMOTED | 75 |
| K_scale_tail_spiral | BLOCKED_COMPONENT_SOURCE_NOT_ACCEPTED | 1 |
| K_scale_tail_spiral | COMPONENT_ORIENTATION_PROMOTED | 172 |
| K_thick_flared | BLOCKED_FAMILY_ORIENTATION_NOT_PROMOTED | 108 |

## Claim Boundary

This gate is a source-native promotion audit, not empirical validation.
A promoted orientation is still a current-bridge readout-orientation
candidate, not a covariant Tau-side physical law. Endpoint use remains
blocked until orientation, per-galaxy q_i evidence, and
morphology-memory/projection evidence are accepted residual-blindly.
