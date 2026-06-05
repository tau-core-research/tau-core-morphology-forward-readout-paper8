# Four inspected endpoint cases status

Status: `FOUR_INSPECTED_CASES_HETEROGENEOUS_PRELIMINARY_EVIDENCE`

This report consolidates the four already inspected galaxies without turning
them into a uniform population-validation claim. Three cases belong to the
mixed-readout population/control packet; NGC5907 and caveated NGC7331 are
additionally promoted to mixed single-galaxy endpoint rows inside that packet,
while NGC4088 is an additional caveated warp/history accepted endpoint.

| galaxy | evidence_packet | endpoint_status | matched_formula_id | matched_rmse_km_s | best_baseline_rmse_km_s | wrong_family_mean_rmse_km_s | best_wrong_family_rmse_km_s | matched_beats_best_baseline | matched_beats_all_wrong_families | claim_boundary | case_caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | three_case_mixed_readout_control | MIXED_ACCEPTED_ENDPOINT_BLOCKED_RETROACTIVE_PROTOCOL_READY | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | 10.6148 | 10.8802 | 12.1321 | 11.367 | True | True | retrospective_frozen_reference_not_accepted_endpoint | mixed accepted endpoint blocked: protocol ready but retroactive; predeclared replay/holdout required |
| NGC5907 | accepted_mixed_single_galaxy_endpoint_inside_three_case_packet | ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | 16.3725 | 16.7855 | 17.0552 | 16.848 | True | True | accepted_single_galaxy_mixed_control_not_population_validation | prior projection endpoint not used as mixed-readout evidence |
| NGC7331 | caveated_accepted_mixed_single_galaxy_endpoint_inside_three_case_packet | CAVEATED_ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT | NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1 | 22.2557 | 23.473 | 22.6731 | 22.6682 | True | True | caveated_accepted_single_galaxy_mixed_control_not_population_validation | broad outer window retained; numeric outer-warp onset unavailable |
| NGC4088 | additional_caveated_single_galaxy_endpoint | CAVEATED_ACCEPTED_ENDPOINT_PRELIMINARY_CONTROL_RESULT | NGC4088_WARP_HISTORY_FREEZE_V1 | 11.619 | 25.3963 | 41.8579 | 37.87 | True | True | caveated_single_galaxy_endpoint_not_population_validation | B1 graphical-overview provenance plus B2/B3 law-level open |

## Summary

| summary_status | n_inspected_cases | n_three_case_mixed_packet | n_additional_caveated_endpoint | n_accepted_single_galaxy_endpoints | n_matched_beats_best_baseline | n_matched_beats_all_wrong_families | mean_matched_rmse_km_s | claim_boundary | construction_used_vobs | scoring_used_vobs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FOUR_INSPECTED_CASES_HETEROGENEOUS_PRELIMINARY_EVIDENCE | 4 | 3 | 1 | 3 | 4 | 4 | 15.2155 | four inspected cases, not a uniform population validation; three-case mixed control with NGC5907 and caveated NGC7331 accepted-mixed promotions plus one additional caveated accepted endpoint | False | True |

Interpretation: the current package contains four inspected cases in which the
source- or morphology-matched Tau Core readout beats the best local baseline
and the inspected wrong-family controls. This is encouraging small-N evidence
for readout specificity, but it is not yet population validation because the
evidence packets are heterogeneous: NGC4013 remains retrospective, NGC7331 is
accepted only with a broad-window caveat, and NGC4088 carries explicit B1/B2/B3
caveats.
