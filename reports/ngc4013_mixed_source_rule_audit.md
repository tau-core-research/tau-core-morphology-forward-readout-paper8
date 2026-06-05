# NGC4013 Mixed Source-Rule Audit

This audit asks whether the mixed `K_expdisk_warp_vertical_overlay`
interpretation has source-side support beyond intuition. It separates
allowed source evidence from the diagnostic RMSE signal, which is recorded
but forbidden as a label input.

## Summary

| galaxy | mixed_readout_candidate | source_support_status | smooth_disk_source_supported | overlay_source_supported | compact_only_rejected | general_mixed_source_rule_pass | diagnostic_score_used_as_label_input | n_evidence_rows | n_endpoint_label_allowed_evidence_rows | n_gates | n_endpoint_blockers | endpoint_scores_allowed | diagnostic_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | K_expdisk_warp_vertical_overlay | SOURCE_SUPPORTED_MIXED_HYPOTHESIS_FORMULA_FREEZE_BLOCKED | True | True | True | True | False | 8 | 7 | 5 | 1 | False | True | ngc4013_mixed_source_rule_audit_not_endpoint |

## Evidence

| galaxy | evidence_id | evidence_lane | source_field | source_value | pass_rule | pass_status | endpoint_label_input_allowed | interpretation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | E1_SMOOTH_EDGE_DISK_COMPONENT | smooth_disk_carrier | S4G component decomposition | Z:edgedisk;N:psf | edge-disk component present and no Sersic bulge component | PASS | True | supports an exponential/smooth disk carrier rather than a compact-core carrier | ngc4013_mixed_source_rule_audit_not_endpoint |
| NGC4013 | E2_DISK_SCALE_PRESENT | smooth_disk_carrier | SPARC/S4G disk scale | Rdisk=3.53 kpc; S4G hr=2.39 kpc | disk scale exists before endpoint scoring | PASS | True | supports a source-native smooth disk radial carrier | ngc4013_mixed_source_rule_audit_not_endpoint |
| NGC4013 | E3_COMPACT_LANE_REJECTED | anti_compact | compact lane source review | COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED | compact endpoint not source supported | PASS | True | prevents treating the galaxy as pure K_true_compact | ngc4013_mixed_source_rule_audit_not_endpoint |
| NGC4013 | E4_WARP_OVERLAY_PRESENT | overlay | warp/flare/disk-halo pressure | warp_flare_disk_halo_overlay_present | warp/overlay source pressure present | PASS | True | supports a source-windowed overlay correction, not a pure smooth disk only | ngc4013_mixed_source_rule_audit_not_endpoint |
| NGC4013 | E5_WARP_ONSET_NUMERIC | overlay | line_of_sight_warp_onset | 10.0 | numeric source onset available | PASS | True | supplies the radial activation window for the overlay component | ngc4013_mixed_source_rule_audit_not_endpoint |
| NGC4013 | E6_VERTICAL_EXTENDED_COMPONENT | overlay | h/R and extended component | h/R=0.232932; f_EC=0.2 | vertical h/R and extended-component fraction available | PASS | True | supports the vertical-overlay attenuation amplitude | ngc4013_mixed_source_rule_audit_not_endpoint |
| NGC4013 | E7_LAG_CONTEXT | overlay | rotational lag | lag shallows from -35 km/s/kpc at 5.8 kpc to zero near R25 | source lag context and caveated kernel shell available | PASS_CAVEATED | True | supports the overlay kernel, but figure-level digitization would strengthen it | ngc4013_mixed_source_rule_audit_not_endpoint |
| NGC4013 | E8_DIAGNOSTIC_RMSE_SIGNAL | forbidden_label_input | mixed diagnostic score | mixed RMSE=10.6148 | must not be used to promote the source label | RECORDED_FOR_MOTIVATION_ONLY | False | can motivate a future source-blind rule, but cannot itself justify the mixed label | ngc4013_mixed_source_rule_audit_not_endpoint |

## Gates

| galaxy | mixed_readout_candidate | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | diagnostic_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | K_expdisk_warp_vertical_overlay | MSR1_SMOOTH_DISK_CARRIER_SUPPORTED | PASS | S4G edge-disk component and source disk scales are present | covered by the residual-blind mixed source-selection rule | False | True | ngc4013_mixed_source_rule_audit_not_endpoint |
| NGC4013 | K_expdisk_warp_vertical_overlay | MSR2_OVERLAY_COMPONENT_SUPPORTED | PASS_CAVEATED | warp onset, vertical h/R, extended component, and lag context are present | replace caveated lag shell with source-map digitization if needed | False | True | ngc4013_mixed_source_rule_audit_not_endpoint |
| NGC4013 | K_expdisk_warp_vertical_overlay | MSR3_COMPACT_ONLY_REJECTED | PASS | COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED | none unless future compact evidence overturns this review | False | True | ngc4013_mixed_source_rule_audit_not_endpoint |
| NGC4013 | K_expdisk_warp_vertical_overlay | MSR4_DIAGNOSTIC_SCORE_EXCLUDED | PASS | diagnostic RMSE row is marked endpoint_label_input_allowed=False | do not use diagnostic fit as source-label evidence | False | True | ngc4013_mixed_source_rule_audit_not_endpoint |
| NGC4013 | K_expdisk_warp_vertical_overlay | MSR5_GENERAL_SOURCE_RULE | PASS_FORMULA_FREEZE_REQUIRED | residual-blind mixed source-selection rule passes this case | freeze the mixed carrier-plus-overlay formula before endpoint scoring | False | True | ngc4013_mixed_source_rule_audit_not_endpoint |

## Claim Boundary

NGC4013 has source support for a mixed smooth-disk plus warp/vertical-overlay hypothesis. The general residual-blind mixed source-selection rule now passes this case, but the mixed formula itself is still endpoint-blocked until a separate formula-freeze gate is run.
