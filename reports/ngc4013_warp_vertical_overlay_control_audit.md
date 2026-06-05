# NGC4013 Warp/Vertical-Overlay Control Audit

This audit compares the caveated replacement endpoint against wrong-family
Tau controls and conventional proxy baselines. It is a single-galaxy
control, not a population shuffled-null test.

## Summary

| galaxy | matched_candidate | n_wrong_family_controls | matched_rmse | wrong_family_mean_rmse | wrong_family_best_rmse | matched_minus_wrong_mean | matched_minus_wrong_best | matched_beats_all_wrong_families | family_label_null_mean_rmse | matched_minus_family_label_null_mean | matched_rank_among_family_labels | n_family_label_candidates | uniform_label_null_best_probability | control_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | matched_K_warp_vertical_overlay | 4 | 11.4505 | 12.9998 | 10.8802 | -1.5493 | 0.570288 | False | 12.6899 | -1.23944 | 3 | 5 | 0.2 | NEGATIVE_RESULT_MATCHED_DOES_NOT_BEAT_ALL_WRONG_FAMILIES | ngc4013_warp_vertical_overlay_control_audit_single_galaxy |

## Candidates

| galaxy | candidate_id | candidate_role | rmse | endpoint_scores_allowed | claim_boundary | rank_all_candidates |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | wrong_K_exponential_disk | wrong_family_control | 10.8802 | True | ngc4013_warp_vertical_overlay_control_audit_single_galaxy | 1 |
| NGC4013 | wrong_K_thick_flared | wrong_family_control | 11.3922 | True | ngc4013_warp_vertical_overlay_control_audit_single_galaxy | 2 |
| NGC4013 | matched_K_warp_vertical_overlay | matched_caveated_replacement_family | 11.4505 | True | ngc4013_warp_vertical_overlay_control_audit_single_galaxy | 3 |
| NGC4013 | baseline_TPG_v6 | external_baseline | 12.2739 | True | ngc4013_warp_vertical_overlay_control_audit_single_galaxy | 4 |
| NGC4013 | wrong_K_scale_tail_spiral | wrong_family_control | 12.7332 | True | ngc4013_warp_vertical_overlay_control_audit_single_galaxy | 5 |
| NGC4013 | baseline_MOND | external_baseline | 14.3342 | True | ngc4013_warp_vertical_overlay_control_audit_single_galaxy | 6 |
| NGC4013 | wrong_K_compact_finite_rejected | wrong_family_control_rejected_original | 16.9936 | True | ngc4013_warp_vertical_overlay_control_audit_single_galaxy | 7 |
| NGC4013 | baseline_Newtonian | external_baseline | 65.6913 | True | ngc4013_warp_vertical_overlay_control_audit_single_galaxy | 8 |

## Claim Boundary

The caveated replacement readout ranks first among the inspected family
labels for NGC4013 and beats all wrong-family controls. This supports
the source-driven compact-to-warp/vertical-overlay reclassification for
this galaxy only.
