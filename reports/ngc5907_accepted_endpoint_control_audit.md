# NGC5907 Accepted Endpoint Control Audit

This audit compares the accepted projection-dominated endpoint against
wrong-family controls and a single-galaxy uniform label-null control.
It is not a population shuffled-null test.

## Summary

| galaxy | accepted_candidate | n_wrong_family_controls | accepted_rmse | wrong_family_mean_rmse | wrong_family_best_rmse | accepted_minus_wrong_mean | accepted_minus_wrong_best | accepted_beats_all_wrong_families | family_label_null_mean_rmse | accepted_minus_family_label_null_mean | accepted_rank_among_family_labels | n_family_label_candidates | uniform_label_null_best_probability | accepted_endpoint_control_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | accepted_K_projection_dominated | 4 | 15.4952 | 17.6277 | 16.9722 | -2.13255 | -1.47703 | True | 17.2012 | -1.70604 | 1 | 5 | 0.2 | PASSED_SINGLE_GALAXY_WRONG_FAMILY_CONTROL | ngc5907_accepted_endpoint_control_audit_single_galaxy |

## Candidates

| galaxy | candidate_id | candidate_role | rmse | endpoint_scores_allowed | claim_boundary | rank_all_candidates |
| --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | accepted_K_projection_dominated | matched_accepted_projection_family | 15.4952 | True | ngc5907_accepted_endpoint_control_audit_single_galaxy | 1 |
| NGC5907 | baseline_TPG_v6 | external_baseline | 16.7855 | True | ngc5907_accepted_endpoint_control_audit_single_galaxy | 2 |
| NGC5907 | wrong_K_scale_tail_spiral | wrong_family_control | 16.9722 | True | ngc5907_accepted_endpoint_control_audit_single_galaxy | 3 |
| NGC5907 | wrong_K_thick_flared | wrong_family_control_generic_parent | 17.0253 | True | ngc5907_accepted_endpoint_control_audit_single_galaxy | 4 |
| NGC5907 | wrong_K_exponential_disk | wrong_family_control | 17.3695 | True | ngc5907_accepted_endpoint_control_audit_single_galaxy | 5 |
| NGC5907 | baseline_MOND | external_baseline | 18.5954 | True | ngc5907_accepted_endpoint_control_audit_single_galaxy | 6 |
| NGC5907 | wrong_K_compact_finite | wrong_family_control | 19.1439 | True | ngc5907_accepted_endpoint_control_audit_single_galaxy | 7 |
| NGC5907 | baseline_Newtonian | external_baseline | 86.4837 | True | ngc5907_accepted_endpoint_control_audit_single_galaxy | 8 |

## Claim Boundary

The accepted projection readout ranks first among the inspected family
labels for NGC5907 and beats all wrong-family controls. This strengthens
NGC5907 as a projection-dominated control, but it remains a one-galaxy
control audit until the same endpoint-blind procedure is repeated across
a predeclared source-rich sample.
