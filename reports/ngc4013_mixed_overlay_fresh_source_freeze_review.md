# NGC4013 Mixed Overlay Fresh Source-Freeze Review

Status: `NGC4013_MIXED_OVERLAY_SOURCE_FREEZE_PASS_CAVEATED_PROSPECTIVE_ONLY`

This review separates the source-side mixed-overlay protocol from the earlier
diagnostic score. It does not score an endpoint.

## Summary

| galaxy | fresh_source_freeze_review_status | previous_lane_freeze_status | recommended_lane_status_update | source_rule_pass | formula_blind | prospective_protocol_ready | retroactive_endpoint_scores_allowed | n_allowed_source_evidence | n_forbidden_evidence_rows | endpoint_scores_allowed | future_prospective_scoring_allowed_after_separate_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | NGC4013_MIXED_OVERLAY_SOURCE_FREEZE_PASS_CAVEATED_PROSPECTIVE_ONLY | PENDING_FRESH_SOURCE_FREEZE | L_mixed_overlay_protocol_ready_not_retroactive | True | True | True | False | 7 | 1 | False | True | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |

## Allowed Source Evidence

| evidence_id | evidence_lane | source_field | source_value | pass_status | interpretation | galaxy | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E1_SMOOTH_EDGE_DISK_COMPONENT | smooth_disk_carrier | S4G component decomposition | Z:edgedisk;N:psf | PASS | supports an exponential/smooth disk carrier rather than a compact-core carrier | NGC4013 | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |
| E2_DISK_SCALE_PRESENT | smooth_disk_carrier | SPARC/S4G disk scale | Rdisk=3.53 kpc; S4G hr=2.39 kpc | PASS | supports a source-native smooth disk radial carrier | NGC4013 | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |
| E3_COMPACT_LANE_REJECTED | anti_compact | compact lane source review | COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED | PASS | prevents treating the galaxy as pure K_true_compact | NGC4013 | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |
| E4_WARP_OVERLAY_PRESENT | overlay | warp/flare/disk-halo pressure | warp_flare_disk_halo_overlay_present | PASS | supports a source-windowed overlay correction, not a pure smooth disk only | NGC4013 | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |
| E5_WARP_ONSET_NUMERIC | overlay | line_of_sight_warp_onset | 10.0 | PASS | supplies the radial activation window for the overlay component | NGC4013 | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |
| E6_VERTICAL_EXTENDED_COMPONENT | overlay | h/R and extended component | h/R=0.232932; f_EC=0.2 | PASS | supports the vertical-overlay attenuation amplitude | NGC4013 | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |
| E7_LAG_CONTEXT | overlay | rotational lag | lag shallows from -35 km/s/kpc at 5.8 kpc to zero near R25 | PASS_CAVEATED | supports the overlay kernel, but figure-level digitization would strengthen it | NGC4013 | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |

## Forbidden/Non-Label Evidence

| evidence_id | evidence_lane | source_field | source_value | pass_status | interpretation | galaxy | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E8_DIAGNOSTIC_RMSE_SIGNAL | forbidden_label_input | mixed diagnostic score | mixed RMSE=10.6148 | RECORDED_FOR_MOTIVATION_ONLY | can motivate a future source-blind rule, but cannot itself justify the mixed label | NGC4013 | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |

## Gates

| gate_id | gate_status | evidence | remaining_obligation | galaxy | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| N4013_FSFR1_SOURCE_RULE | PASS | SOURCE_SUPPORTED_MIXED_HYPOTHESIS_FORMULA_FREEZE_BLOCKED | none at source-rule level | NGC4013 | False | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |
| N4013_FSFR2_FORBIDDEN_SCORE_EXCLUDED | PASS | diagnostic score row is endpoint_label_input_allowed=False | do not use previous RMSE as source-label evidence | NGC4013 | False | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |
| N4013_FSFR3_SOURCE_TRIAD | PASS | smooth=True; overlay=True; compact_rejected=True | lag map digitization can strengthen but is not required for protocol | NGC4013 | False | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |
| N4013_FSFR4_FORMULA_FREEZE_BLINDNESS | PASS | formula manifest uses_vobs_or_residual_in_construction=False | future scoring script must read manifest unchanged | NGC4013 | False | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |
| N4013_FSFR5_PROSPECTIVE_READY | PASS_CAVEATED | prospective_ready=True; retroactive_scores_allowed=False | may be used prospectively, but not as retroactive accepted validation | NGC4013 | False | ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint |

## Interpretation

NGC4013 has enough residual-blind source evidence to be treated as a
prospective mixed-overlay protocol case: smooth disk carrier evidence, overlay
evidence, and compact-only rejection are all present. The earlier diagnostic
RMSE remains explicitly forbidden as label evidence. Therefore this case can
be moved from `pending` to a prospective-only lane status, but it still cannot
be counted as retroactive endpoint validation.

## Claim Boundary

`ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint`
