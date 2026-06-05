# NGC4183 Projection/Outer-Warp Label Gate

Status: `NARROW_REPLACEMENT_LABEL_SUPPORTED_FOR_FORMULA_DERIVATION_NOT_ENDPOINT`

This is a label-narrowing gate.  It does not freeze a formula and does not
authorize endpoint scoring.

## Summary

| label_gate_status | galaxy | replacement_candidate_readout | replacement_lane | formula_derivation_allowed | formula_freeze_allowed | endpoint_scores_allowed | p_edge | rhi_relative_difference | observable_sheet_status | claim_boundary | next_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NARROW_REPLACEMENT_LABEL_SUPPORTED_FOR_FORMULA_DERIVATION_NOT_ENDPOINT | NGC4183 | K_expdisk_edge_on_projection_outer_warp_caveated | L_projection_attenuation_with_outer_warp_caveat | True | False | False | 0.985148 | 0.00623754 | NGC4183_MIXED_OVERLAY_OBSERVABLE_SHEET_PARTIAL_PASS_LABEL_AND_FORMULA_BLOCKED | ngc4183_projection_outer_warp_label_gate_not_endpoint | derive_projection_attenuation_outer_warp_caveated_formula_shell |

## Source Evidence

| evidence_id | evidence_status | value | threshold_or_reason | interpretation |
| --- | --- | --- | --- | --- |
| E1_EDGE_ON_PROJECTION | SUPPORTS_NARROW_LABEL | 0.9851478631379982 | p_edge > 0.95 | edge-on projection observable is strong enough for projection-overlay derivation |
| E2_RHI_DENOMINATOR_CONSISTENCY | SUPPORTS_NARROW_LABEL | 0.0062375447574292 | relative difference < 0.02 | source-native H I diameter and SPARC RHI agree as support scale |
| E3_OUTER_WARP_CONTEXT | SUPPORTS_CAVEATED_LABEL_ONLY | ACCEPTED_CONTEXT_CAVEATED | qualitative source note only | outer-warp context can name the caveat but cannot freeze a numeric ramp |
| E4_NUMERIC_WARP_KERNEL | BLOCKS_WARP_RAMP_FREEZE | BLOCKED_NUMERIC_FIELD_MISSING | no onset/amplitude | do not use standalone warp-ramp or added-source formula yet |
| E5_BROAD_BAR_CORE_HISTORY | REJECTS_BROAD_LABEL_FOR_NOW | BLOCKED_REQUIRED_FIELD_MISSING | required field missing | broad proposed label is too specific for available source evidence |

## Proposed Replacement

| galaxy | previous_candidate_readout | replacement_candidate_readout | replacement_lane | label_gate_status | formula_derivation_allowed | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual_in_selection | why_narrowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183 | K_expdisk_bar_core_projection_history_overlay_review | K_expdisk_edge_on_projection_outer_warp_caveated | L_projection_attenuation_with_outer_warp_caveat | NARROW_REPLACEMENT_LABEL_SUPPORTED_FOR_FORMULA_DERIVATION_NOT_ENDPOINT | True | False | False | False | source supports high-inclination projection plus qualitative outer warp; bar/core/history overlay fields remain missing | ngc4183_projection_outer_warp_label_gate_not_endpoint |

## Gates

| gate_id | gate_status | evidence | remaining_obligation |
| --- | --- | --- | --- |
| N4183_LABEL_G1_NO_RESIDUAL_SELECTION | PASS | label gate reads observable sheet only | separate endpoint script may read vobs only after freeze |
| N4183_LABEL_G2_BROAD_LABEL_REJECTED | PASS | bar/core/history overlay observables missing | do not score broad label |
| N4183_LABEL_G3_NARROW_LABEL_SUPPORTED | PASS_CAVEATED | p_edge=0.985 and RHI denominator consistency plus qualitative outer warp | derive projection attenuation formula shell and coefficient rule |
| N4183_LABEL_G4_ENDPOINT_ALLOWED | BLOCKED | no frozen formula yet | formula derivation and source-side formula freeze |

## Verdict

The broad `K_expdisk_bar_core_projection_history_overlay_review` label is too
strong for the available NGC4183 source evidence.  A narrower
`K_expdisk_edge_on_projection_outer_warp_caveated` label is supported for
formula derivation because the galaxy has a strong edge-on projection observable
and a source-native H I support scale that agrees with SPARC.  The qualitative
outer-warp statement is a caveat, not a numeric warp ramp.  Endpoint scoring
remains blocked until a dimensionally checked projection formula is frozen
without using residuals.
