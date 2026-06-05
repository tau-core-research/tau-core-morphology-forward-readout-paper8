# Split-B2 Independent Holdout Candidate Selector

Status: `SPLIT_B2_INDEPENDENT_HOLDOUT_SELECTOR_COMPLETE_NOT_ENDPOINT`

This selector is a residual-blind candidate gate. It does not read observed
velocities, does not score endpoints, and does not promote the NGC7331
split-B2 repair as a same-curve result.

## Summary

| selector_status | n_candidates_reviewed | top_candidate | top_candidate_status | top_blocker | endpoint_scores_allowed | uses_vobs_or_residual_in_selection | recommended_next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SPLIT_B2_INDEPENDENT_HOLDOUT_SELECTOR_COMPLETE_NOT_ENDPOINT | 5 | NGC5907 | P0_PREDECLARED_SPLIT_B2_HOLDOUT_CANDIDATE_RHI_BLOCKED_OR_CAVEATED | sparc_rhi_missing_or_zero | False | False | NGC5907 split-B2 denominator/source-radius gate before formula freeze | split_b2_independent_holdout_candidate_selector_not_endpoint |

## Candidate Ranking

| galaxy | split_b2_holdout_status | sparc_status | sparc_vflat_km_s | sparc_rhi_kpc | has_numeric_warp_activation | split_b2_blockers | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | P0_PREDECLARED_SPLIT_B2_HOLDOUT_CANDIDATE_RHI_BLOCKED_OR_CAVEATED | SPARC_RHI_MISSING_OR_ZERO | 215 | 0 | True | sparc_rhi_missing_or_zero | build NGC5907 split-B2 denominator gate; if source-native denominator passes, freeze split-B2 formula before any scoring |
| NGC4013 | P1_RETROSPECTIVE_ANALOGUE_HAS_RHI_NOT_CLEAN_HOLDOUT | SPARC_VFLAT_RHI_READY | 172.9 | 31.35 | True | retrospective_or_reference_case;exact_b2_fields_incomplete | use as secondary analogue after a fresh residual-blind source freeze |
| NGC4183 | P1_SOURCE_ACQUISITION_REQUIRED_HAS_SPARC_RHI_VFLAT | SPARC_VFLAT_RHI_READY | 110.6 | 16.07 | False | source_acquisition_required;numeric_warp_activation_missing | acquire source-native warp/history observables before formula freeze |
| NGC4088 | REFERENCE_ONLY_NOT_HOLDOUT | SPARC_VFLAT_RHI_READY | 171.7 | 22.25 | False | reference_case | use only as protocol reference and limit check |
| NGC7331 | EXCLUDED_DIAGNOSTIC_ORIGIN | SPARC_VFLAT_RHI_READY | 239 | 27.01 | False | same_curve_post_failure_branch | do not use as split-B2 holdout; keep only diagnostic comparison |

## Action Items

| priority | galaxy | action | details | endpoint_scores_allowed_after_action | next_gate_after_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | NGC5907 | resolve denominator | SPARC RHI is zero/missing; acquire source-native HI/support radius or predeclare caveated optical-warp support denominator from 13.3-24.0 kpc. | False | split-B2 formula freeze gate if denominator passes | split_b2_independent_holdout_candidate_selector_not_endpoint |
| P1 | NGC4013 | fresh residual-blind source freeze | Has RHI/Vflat but is not a clean split-B2 holdout until exact source fields are re-frozen without using prior mixed endpoint information. | False | secondary analogue freeze gate | split_b2_independent_holdout_candidate_selector_not_endpoint |
| P1 | NGC4183 | source acquisition | Has RHI/Vflat but lacks galaxy-specific warp/history activation fields. | False | source acquisition and preflight gate | split_b2_independent_holdout_candidate_selector_not_endpoint |

## Interpretation

NGC5907 is the best next split-B2 holdout candidate because it has strong
source-supported warp/projection evidence and a pre-existing mixed-readout
source-rule lane. It is not score-ready because the SPARC master row has
`RHI_kpc=0.0`, while the split-B2 normalized radial coordinate needs a frozen
outer support denominator.

NGC4013 is useful as a secondary analogue but is not a clean independent
holdout in the current state. NGC4183 is scientifically useful because SPARC
RHI and Vflat are available, but it needs galaxy-specific source acquisition.

NGC4088 remains the reference case. NGC7331 remains the diagnostic origin of
the split-B2 repair and must not be counted as an independent holdout endpoint.

## Claim Boundary

`split_b2_independent_holdout_candidate_selector_not_endpoint`
