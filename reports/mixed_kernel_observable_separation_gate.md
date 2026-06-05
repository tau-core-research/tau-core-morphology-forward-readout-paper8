# Mixed Kernel Observable Separation Gate

Status label: `DIAGNOSTIC_ONLY_NOT_ENDPOINT`.

This gate is a residual-blind follow-up to the strict replay/holdout
mixed endpoint. It does not read observed velocities, residuals, RMSE
scores, required-S_tau diagnostics, or endpoint ranks. It only asks
whether the source-native observables already separate the fresh
NGC5907 projection-dominated mixed lane from the NGC7331 V2
vertical/outer-warp mixed lane.

## Summary

| gate_status | diagnostic_status | cases_audited | matched_source_rank_first | min_source_similarity_margin | mean_source_similarity_margin | uses_vobs_or_residual | endpoint_scores_allowed | endpoint_score_inputs_read | dimension_check | known_limit_check | bridge_interpretation | next_obligation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SOURCE_KERNEL_OBSERVABLE_SEPARATION_PASS | DIAGNOSTIC_ONLY_NOT_ENDPOINT | 2 | 2 | 0.501384 | 0.651317 | False | False | False | PASS: all audited features are dimensionless source-native proxies | PASS: absent projection, absent truncation, or absent fractional onset drives the corresponding prototype evidence to zero | source_fields_separate_lanes_kernel_mapping_needs_sharpening | derive sharper projection and vertical/outer-warp kernel maps from these separated source fields before rerunning replay/holdout specificity | mixed_kernel_observable_separation_source_side_not_endpoint |

## Source Fingerprints

| galaxy | source_matched_formula | source_lane | projection_bound | disk_truncation_or_break | fractional_onset_available | fractional_onset_over_RHI | vertical_activation | projected_thickness | source_onset_kpc | source_window_outer_kpc | source_window_width_kpc | dimension_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | K_expdisk_projection_mixed | projection_dominated_expdisk_mixed | 0.789128 | 0.738298 | 0 | 0 | 0.693283 | 0.693283 | 13.3 | 24 | 10.7 | dimensionless_source_features | False | False | mixed_kernel_observable_separation_source_side_not_endpoint |
| NGC7331 | K_expdisk_vertical_outer_warp_v2 | vertical_outer_warp_fractional_onset_mixed | 0 | 0 | 1 | 0.534309 | 0.63081 | 0.398406 | 14.4317 | 27.01 | 12.5783 | dimensionless_source_features | False | False | mixed_kernel_observable_separation_source_side_not_endpoint |

## Prototype Similarity Matrix

| galaxy | source_matched_formula | prototype_formula | source_similarity | is_matched_formula | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary | rank_within_galaxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | K_expdisk_projection_mixed | K_expdisk_projection_mixed | 0.920617 | True | False | False | mixed_kernel_observable_separation_source_side_not_endpoint | 1 |
| NGC5907 | K_expdisk_projection_mixed | K_expdisk_vertical_outer_warp_v2 | 0.419233 | False | False | False | mixed_kernel_observable_separation_source_side_not_endpoint | 2 |
| NGC7331 | K_expdisk_vertical_outer_warp_v2 | K_expdisk_vertical_outer_warp_v2 | 0.978387 | True | False | False | mixed_kernel_observable_separation_source_side_not_endpoint | 1 |
| NGC7331 | K_expdisk_vertical_outer_warp_v2 | K_expdisk_projection_mixed | 0.177136 | False | False | False | mixed_kernel_observable_separation_source_side_not_endpoint | 2 |

## Interpretation

If this gate passes while the replay/holdout endpoint still fails
wrong-label or shuffled-label specificity, the immediate bottleneck is
not the residual-blind source separation itself. The bottleneck is the
current source-to-kernel map: the projection and vertical/outer-warp
attenuation curves remain too similar after they are converted into
4D readout kernels.

If this gate fails, the next obligation is different: acquire stronger
source-native morphology fields before changing kernels.

## Claim Boundary

This is not an endpoint score and not empirical validation. It is a
source-side diagnostic for where to sharpen the next replay/holdout
mixed-readout protocol.
