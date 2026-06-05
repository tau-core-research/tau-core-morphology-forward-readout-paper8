# Mixed Readout Population Endpoint

This script scores the three frozen mixed-readout protocols from unchanged
manifests. Observed velocities are read only by this scoring script.

## Summary

| endpoint_status | n_cases_scored | n_fresh_prospective_cases | n_caveated_cases | mean_rmse_mixed_population | mean_rmse_newton | mean_rmse_tpg_v6 | mean_rmse_mond | mean_rmse_exponential_disk_carrier | n_beats_newton | n_beats_tpg_v6 | n_beats_mond | n_beats_exponential_disk_carrier | construction_used_vobs | scoring_used_vobs | claim_boundary | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MIXED_POPULATION_ENDPOINT_PRELIMINARY_CONTROL_RESULT | 3 | 2 | 1 | 16.4143 | 70.5098 | 18.1815 | 20.7471 | 17.2409 | 3 | 3 | 3 | 3 | False | True | mixed_readout_population_endpoint_preliminary_control | preliminary endpoint scores from frozen mixed manifests; not population validation and not baseline-superiority proof |

## Scores

| galaxy | n_points | rmse_newton | rmse_tpg_v6 | rmse_mond | rmse_exponential_disk_carrier | rmse_mixed_population | mixed_minus_newton | mixed_minus_tpg_v6 | mixed_minus_mond | mixed_minus_exponential_disk_carrier | beats_newton | beats_tpg_v6 | beats_mond | beats_exponential_disk_carrier | mixed_formula_id | mixed_case_status | mixed_case_caveat | construction_used_vobs | scoring_used_vobs | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | 36 | 65.6913 | 12.2739 | 14.3342 | 10.8802 | 10.6148 | -55.0765 | -1.65915 | -3.71946 | -0.265449 | True | True | True | True | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | RETROSPECTIVE_REFERENCE_FROZEN_PROTOCOL_SCORED | not_new_prospective_endpoint_validation | False | True | mixed_readout_population_endpoint_preliminary_control |
| NGC5907 | 19 | 86.4837 | 16.7855 | 18.5954 | 17.3695 | 16.3725 | -70.1112 | -0.412978 | -2.22283 | -0.99701 | True | True | True | True | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | FRESH_PROSPECTIVE_MIXED_PROTOCOL_SCORED | prior_projection_endpoint_not_reused_as_mixed_evidence | False | True | mixed_readout_population_endpoint_preliminary_control |
| NGC7331 | 36 | 59.3544 | 25.4851 | 29.3117 | 23.473 | 22.2557 | -37.0987 | -3.2294 | -7.05601 | -1.21731 | True | True | True | True | NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1 | CAVEATED_FRESH_PROSPECTIVE_MIXED_PROTOCOL_SCORED | broad_outer_window_no_numeric_warp_onset | False | True | mixed_readout_population_endpoint_preliminary_control |

## Claim Boundary

This is a preliminary control endpoint, not a validation claim. NGC4013 is
a frozen retrospective reference protocol; NGC5907 and caveated NGC7331
are fresh prospective mixed protocols. The NGC7331 broad-window caveat is
preserved.
