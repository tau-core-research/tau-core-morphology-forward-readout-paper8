# NGC4183 Mixed-Overlay Observable Sheet

Status: `NGC4183_MIXED_OVERLAY_OBSERVABLE_SHEET_PARTIAL_PASS_LABEL_AND_FORMULA_BLOCKED`

This sheet turns residual-blind NGC4183 source information into candidate
observables for a later readout formula.  It is not an endpoint score and does
not read observed velocity residuals.

## Summary

| observable_sheet_status | galaxy | n_observables | n_freeze_candidates | rhi_source_kpc | rhi_sparc_kpc | rhi_relative_difference | projection_edge_on_strength_p_edge | has_numeric_warp_kernel | has_bar_core_history_overlay | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary | next_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183_MIXED_OVERLAY_OBSERVABLE_SHEET_PARTIAL_PASS_LABEL_AND_FORMULA_BLOCKED | NGC4183 | 9 | 5 | 15.9698 | 16.07 | 0.00623754 | 0.985148 | False | False | False | False | ngc4183_mixed_overlay_observable_sheet_not_endpoint | narrow_or_promote_label_then_derive_projection_or_outer_warp_formula_shell |

## Observables

| observable_id | value | unit | source_basis | source_id | status | freeze_candidate | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R_HI_source_native_kpc | 15.969762655748113 | kpc | HI diameter 6.1 arcmin at SPARC D=18.0 Mpc | VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI | ACCEPTED_NUMERIC_CAVEATED_REVIEWED | True | Independent H I support radius proxy; consistent with SPARC RHI. |
| R_HI_source_vs_SPARC_relative_difference | 0.006237544757429206 | dimensionless | source-native R_HI compared to SPARC RHI | SPARC_MASTER+VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI | CONSISTENCY_CHECK_PASS | False | Agreement below 1%; supports using RHI as denominator. |
| projection_edge_on_strength_p_edge | 0.9851478631379982 | dimensionless | sin^2(i_HI), i_HI=83 deg | VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI | ACCEPTED_NUMERIC_CAVEATED_REVIEWED | True | High-inclination projection observable; not a residual fit. |
| disk_scale_fraction_x_scale | 0.17470516376120188 | dimensionless | Rdisk/R_HI_source | SPARC_MASTER+VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI | ACCEPTED_NUMERIC_RESIDUAL_BLIND | True | Scale placement observable for smooth disk carrier. |
| hi_extent_in_disk_scales | 5.72392926729323 | dimensionless | R_HI_source/Rdisk | SPARC_MASTER+VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI | ACCEPTED_NUMERIC_RESIDUAL_BLIND | True | Extended support observable; large value favors outer-overlay review. |
| outer_warp_flag | 1.0 | dimensionless flag | source note: slightly warped in the outer regions | VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI | ACCEPTED_CONTEXT_CAVEATED | False | Qualitative source support; no numeric warp onset/amplitude yet. |
| hi_position_angle_deg | 347.0 | deg | total H I map position angle | VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI | ACCEPTED_NUMERIC_CAVEATED_REVIEWED | True | Orientation field; formula use requires a declared projection kernel. |
| warp_onset_or_amplitude | <NA> | dimensionless_or_kpc | not available in current reviewed sources | PENDING | BLOCKED_NUMERIC_FIELD_MISSING | False | Prevents a source-native warp ramp freeze. |
| bar_core_history_overlay | <NA> | mixed | not available in current reviewed sources | PENDING | BLOCKED_REQUIRED_FIELD_MISSING | False | Current worklist readout name requires this review before label promotion. |

## Gates

| gate_id | gate_status | evidence | remaining_obligation |
| --- | --- | --- | --- |
| N4183_OBS_G1_SOURCE_AUDIT_INPUT | PASS | NGC4183_MIXED_OVERLAY_SOURCE_AUDIT_LOCAL_SOURCE_PRESENT_REVIEW_REQUIRED_NOT_FREEZE_READY | observable sheet only; no scoring |
| N4183_OBS_G2_RHI_DENOMINATOR | PASS_CAVEATED | source-native RHI=15.970 kpc vs SPARC RHI=16.070 kpc | choose formula lane before using denominator |
| N4183_OBS_G3_PROJECTION_OBSERVABLE | PASS_CAVEATED | HI inclination=83.0 deg gives p_edge=0.985 | derive projection kernel and coefficient rule |
| N4183_OBS_G4_WARP_NUMERIC_KERNEL | BLOCKED | outer warp is qualitative only; no onset/amplitude frozen | acquire source-native warp onset/amplitude or use a projection-only lane |
| N4183_OBS_G5_LABEL_PROMOTION | BLOCKED | bar/core/history overlay field remains missing for current proposed label | either acquire missing fields or narrow label to projection/outer-warp caveated lane |

## Source Fields Used

| field_id | value | unit | field_status | freeze_usable |
| --- | --- | --- | --- | --- |
| disk_scale_Rdisk_kpc | 2.79 | kpc | ACCEPTED_NUMERIC_RESIDUAL_BLIND | True |
| RHI_kpc | 16.07 | kpc | ACCEPTED_NUMERIC_RESIDUAL_BLIND | True |
| Vflat_km_s | 110.6 | km/s | ACCEPTED_NUMERIC_RESIDUAL_BLIND | True |
| inclination_deg_sparc | 82.0 | deg | ACCEPTED_NUMERIC_EDGE_ON_CAVEATED | True |
| hi_position_angle_deg_source_native | 347.0 | deg | SOURCE_PRESENT_REVIEW_REQUIRED | False |
| hi_inclination_deg_source_native | 83.0 | deg | SOURCE_PRESENT_REVIEW_REQUIRED | False |
| hi_diameter_arcmin_source_native | 6.1 | arcmin | SOURCE_PRESENT_REVIEW_REQUIRED | False |
| outer_warp_context | slightly warped in the outer regions | context | ACCEPTED_CONTEXT_CAVEATED | False |
| edge_on_projection_context | optical-axis inclination likely too high | context | ACCEPTED_CONTEXT_CAVEATED | False |
| bar_core_history_overlay_observables | nan | mixed | BLOCKED_REQUIRED_FIELD_MISSING | False |

## Dimensional/Limit Notes

- `R_HI_source_native_kpc`, `Rdisk`, and `Vflat` carry physical units and can
  only enter a future formula through a dimensionally checked shell.
- `p_edge = sin^2(i_HI)` and `Rdisk/R_HI` are dimensionless.
- The zero-overlay/no-warp limit must recover the chosen carrier before any
  endpoint scoring.

## Verdict

NGC4183 now has a partial residual-blind observable sheet: H I support radius,
high-inclination projection strength, disk-scale fraction, and qualitative outer
warp context.  It is still blocked for formula freeze because the current
mixed-overlay label requires either numeric warp/onset amplitude or a narrowed
projection-dominated label with an independently justified coefficient rule.
