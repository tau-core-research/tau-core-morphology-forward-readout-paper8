# L2 Weight Freeze-Readiness Audit

This audit checks whether the residual-blind L2 weight-intake candidates
can be frozen for endpoint use. It computes no endpoint score.

## Verdict

- Galaxies audited: 175
- Endpoint-freeze allowed: 0
- Proxy-gate blocker resolved by derived coarse-grid E_tau product: 175
- Blocked by missing Tau-side normalization: 0
- Source-native orientation ready after promotion gate: 67
- Blocked by source-native orientation promotion: 108
- Blocked by projection acceptance after orientation: 47
- Blocked by memory/history acceptance after orientation and projection: 19
- Blocked by q_i/normalization acceptance after memory/projection: 1
- Blocked by proxy-or-missing active components after orientation: 0
- Formula-conditional normalization candidates present: 175
- Dominant components with source-candidate support: 141
- Dominant components proxy/partial only: 31
- Dominant components missing source support: 3

The endpoint remains blocked for every galaxy, but the blocker has
changed. The proxy gate is no longer treated as a free protocol
constant: it is resolved as the conservative coarse-grid E_tau product.
The source-native orientation gate now partially promotes the
theory-conditional orientation signs. The remaining blockers split
into still-unpromoted orientation rows, projection caveats,
morphology-memory/history acceptance, and the final accepted q_i plus
normalization-law step. This is a protocol safeguard, not a negative
empirical result.

## Summary

| split | n_galaxies | freeze_allowed_count | blocked_normalization_count | blocked_orientation_count | orientation_ready_count | orientation_blocked_count | blocked_memory_projection_count | blocked_projection_acceptance_count | blocked_qi_normalization_acceptance_count | blocked_proxy_or_missing_component_count | proxy_gate_resolved_count | normalization_candidate_present_count | component_proxy_or_missing_count | source_candidates_present_count | dominant_source_candidate_count | dominant_proxy_or_partial_count | dominant_missing_source_count | nonzero_source_candidate_components | nonzero_proxy_or_partial_components | nonzero_missing_components | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 175 | 0 | 0 | 108 | 67 | 108 | 19 | 47 | 1 | 0 | 175 | 175 | 108 | 67 | 141 | 31 | 3 | 295 | 105 | 6 | l2_weight_freeze_readiness_audit_not_endpoint |
| holdout | 44 | 0 | 0 | 28 | 16 | 28 | 2 | 14 | 0 | 0 | 44 | 44 | 28 | 16 | 35 | 9 | 0 | 79 | 28 | 0 | l2_weight_freeze_readiness_audit_not_endpoint |
| train | 131 | 0 | 0 | 80 | 51 | 80 | 17 | 33 | 1 | 0 | 131 | 131 | 80 | 51 | 106 | 22 | 3 | 216 | 77 | 6 | l2_weight_freeze_readiness_audit_not_endpoint |

## Component Evidence Counts

| component_family | component_evidence_status | n_components |
| --- | --- | --- |
| K_compact_finite | MISSING_SOURCE_SUPPORT | 1 |
| K_compact_finite | SOURCE_CANDIDATE_COMPACT_READY | 48 |
| K_exponential_disk | MISSING_SOURCE_SUPPORT | 1 |
| K_exponential_disk | SOURCE_CANDIDATE_S4G_SCALE_READY | 75 |
| K_scale_tail_spiral | MISSING_SOURCE_SUPPORT | 1 |
| K_scale_tail_spiral | SOURCE_CANDIDATE_HI_TAIL_READY | 172 |
| K_thick_flared | MISSING_SOURCE_SUPPORT | 3 |
| K_thick_flared | PROXY_OR_PARTIAL_SOURCE_ONLY | 105 |

## Claim Boundary

This audit may identify source-supported candidate components, but it does
not accept weights, does not launch the endpoint, and does not use
rotation residuals. A later endpoint requires source-native orientation
promotion, accepted per-galaxy evidence assignments, and an accepted
morphology-memory/projection audit.
