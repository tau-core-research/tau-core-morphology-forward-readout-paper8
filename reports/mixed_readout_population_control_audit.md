# Mixed Readout Population Wrong-Label Control Audit

This audit applies each frozen mixed formula shell to each of the three
scored galaxies, then evaluates all one-to-one formula-label shuffles.
The construction reads frozen manifests only; observed velocities are
used only for scoring.

## Summary

| control_status | n_galaxies | n_formula_labels | mean_matched_rmse | mean_wrong_label_rmse | matched_minus_wrong_label_mean | n_matched_beats_all_wrong_labels | matched_permutation_mean_rmse | best_shuffled_mean_rmse | matched_minus_best_shuffled | matched_permutation_rank | n_shuffled_permutations | uniform_shuffled_best_probability | construction_used_vobs | scoring_used_vobs | claim_boundary | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PASSED_3CASE_WRONG_LABEL_AND_SHUFFLED_CONTROL | 3 | 3 | 16.4143 | 17.2868 | -0.872473 | 3 | 16.4143 | 16.7103 | -0.296014 | 1 | 5 | 0.166667 | False | True | mixed_readout_population_wrong_label_control_audit | wrong-label control on three frozen formula shells; still small-N and not population validation |

## Per-Galaxy Matched vs Wrong Labels

| galaxy | matched_rmse | wrong_mean_rmse | wrong_best_rmse | matched_minus_wrong_mean | matched_minus_wrong_best | matched_rank_within_galaxy | matched_beats_all_wrong_labels | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | 10.6148 | 12.1321 | 11.367 | -1.51738 | -0.752249 | 1 | True | mixed_readout_population_wrong_label_control_audit |
| NGC5907 | 16.3725 | 17.0552 | 16.848 | -0.682634 | -0.475457 | 1 | True | mixed_readout_population_wrong_label_control_audit |
| NGC7331 | 22.2557 | 22.6731 | 22.6682 | -0.417405 | -0.412584 | 1 | True | mixed_readout_population_wrong_label_control_audit |

## Formula Matrix

| galaxy | applied_formula_source | applied_formula_label | label_assignment_role | rmse | construction_used_vobs | scoring_used_vobs | claim_boundary | rank_within_galaxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | NGC4013 | K_expdisk_warp_vertical_overlay | matched | 10.6148 | False | True | mixed_readout_population_wrong_label_control_audit | 1 |
| NGC4013 | NGC7331 | K_expdisk_vertical_outer_warp_overlay | wrong_label_control | 11.367 | False | True | mixed_readout_population_wrong_label_control_audit | 2 |
| NGC4013 | NGC5907 | K_expdisk_projection_overlay | wrong_label_control | 12.8973 | False | True | mixed_readout_population_wrong_label_control_audit | 3 |
| NGC5907 | NGC5907 | K_expdisk_projection_overlay | matched | 16.3725 | False | True | mixed_readout_population_wrong_label_control_audit | 1 |
| NGC5907 | NGC7331 | K_expdisk_vertical_outer_warp_overlay | wrong_label_control | 16.848 | False | True | mixed_readout_population_wrong_label_control_audit | 2 |
| NGC5907 | NGC4013 | K_expdisk_warp_vertical_overlay | wrong_label_control | 17.2623 | False | True | mixed_readout_population_wrong_label_control_audit | 3 |
| NGC7331 | NGC7331 | K_expdisk_vertical_outer_warp_overlay | matched | 22.2557 | False | True | mixed_readout_population_wrong_label_control_audit | 1 |
| NGC7331 | NGC5907 | K_expdisk_projection_overlay | wrong_label_control | 22.6682 | False | True | mixed_readout_population_wrong_label_control_audit | 2 |
| NGC7331 | NGC4013 | K_expdisk_warp_vertical_overlay | wrong_label_control | 22.6779 | False | True | mixed_readout_population_wrong_label_control_audit | 3 |

## Label Permutations

| assignment_id | assignment_role | mean_rmse | sum_rmse | n_matched_labels | claim_boundary | rank_by_mean_rmse |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4013->NGC4013;NGC5907->NGC5907;NGC7331->NGC7331 | matched_diagonal | 16.4143 | 49.243 | 3 | mixed_readout_population_wrong_label_control_audit | 1 |
| NGC4013->NGC4013;NGC5907->NGC7331;NGC7331->NGC5907 | shuffled_label_null | 16.7103 | 50.131 | 1 | mixed_readout_population_wrong_label_control_audit | 2 |
| NGC4013->NGC7331;NGC5907->NGC5907;NGC7331->NGC4013 | shuffled_label_null | 16.8058 | 50.4174 | 1 | mixed_readout_population_wrong_label_control_audit | 3 |
| NGC4013->NGC7331;NGC5907->NGC4013;NGC7331->NGC5907 | shuffled_label_null | 17.0992 | 51.2976 | 0 | mixed_readout_population_wrong_label_control_audit | 4 |
| NGC4013->NGC5907;NGC5907->NGC4013;NGC7331->NGC7331 | shuffled_label_null | 17.4718 | 52.4153 | 1 | mixed_readout_population_wrong_label_control_audit | 5 |
| NGC4013->NGC5907;NGC5907->NGC7331;NGC7331->NGC4013 | shuffled_label_null | 17.4744 | 52.4231 | 0 | mixed_readout_population_wrong_label_control_audit | 6 |

## Claim Boundary

This is a small-N wrong-label control, not a population validation. It
tests whether the source-matched frozen mixed formula labels beat the
available wrong mixed labels within the three-case packet.
