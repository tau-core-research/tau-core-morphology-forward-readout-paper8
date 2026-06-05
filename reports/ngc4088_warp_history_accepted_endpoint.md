# NGC4088 Warp/History Accepted Endpoint

This run scores the caveated accepted NGC4088 warp/history endpoint from
the unchanged frozen formula-freeze manifest. Observed velocities are read
only in this scoring script.

## Summary

| endpoint_status | galaxy | formula_id | n_points | rmse_warp_history_accepted | best_baseline_model | best_baseline_rmse_km_s | wrong_family_mean_rmse_km_s | wrong_family_best_rmse_km_s | matched_minus_best_baseline_rmse_km_s | matched_minus_wrong_family_mean_rmse_km_s | matched_minus_best_wrong_family_rmse_km_s | matched_rank_among_all_models | matched_beats_all_baselines | matched_beats_all_wrong_families | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | claim_boundary | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAVEATED_ACCEPTED_ENDPOINT_PRELIMINARY_CONTROL_RESULT | NGC4088 | NGC4088_WARP_HISTORY_FREEZE_V1 | 12 | 11.619 | NEWTONIAN_vn | 25.3963 | 41.8579 | 37.87 | -13.7773 | -30.2389 | -26.251 | 1 | True | True | False | True | True | ngc4088_warp_history_accepted_endpoint_preliminary_control | single-galaxy caveated control endpoint; not population validation |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | mae_km_s | bias_km_s | inner_rmse_km_s | outer_rmse_km_s | construction_used_vobs | scoring_used_vobs | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | TAU_NGC4088_WARP_HISTORY_ACCEPTED | matched_frozen_readout | 12 | 11.619 | 9.64302 | -4.27668 | 10.0492 | 12.0971 | False | True | ngc4088_warp_history_accepted_endpoint_preliminary_control |
| NGC4088 | NEWTONIAN_vn | baseline | 12 | 25.3963 | 20.1483 | -14.8664 | 10.0492 | 28.7454 | False | True | ngc4088_warp_history_accepted_endpoint_preliminary_control |
| NGC4088 | WRONG_K_exponential_disk | wrong_family_control | 12 | 37.87 | 36.8393 | 36.8393 | 29.778 | 40.207 | False | True | ngc4088_warp_history_accepted_endpoint_preliminary_control |
| NGC4088 | WRONG_K_thick_flared | wrong_family_control | 12 | 38.4554 | 37.4445 | 37.4445 | 30.5199 | 40.7586 | False | True | ngc4088_warp_history_accepted_endpoint_preliminary_control |
| NGC4088 | TPG_V6_v_v6 | baseline | 12 | 38.9877 | 37.9843 | 37.9843 | 31.0718 | 41.2905 | False | True | ngc4088_warp_history_accepted_endpoint_preliminary_control |
| NGC4088 | WRONG_K_scale_tail_spiral | wrong_family_control | 12 | 39.7702 | 38.7664 | 38.7664 | 31.4579 | 42.1784 | False | True | ngc4088_warp_history_accepted_endpoint_preliminary_control |
| NGC4088 | MOND_v_mond | baseline | 12 | 42.1838 | 41.2137 | 41.2137 | 34.1357 | 44.5446 | False | True | ngc4088_warp_history_accepted_endpoint_preliminary_control |
| NGC4088 | WRONG_K_compact_finite | wrong_family_control | 12 | 51.3362 | 49.6383 | 49.6383 | 34.1777 | 55.8973 | False | True | ngc4088_warp_history_accepted_endpoint_preliminary_control |

## Claim Boundary

This is a single-galaxy caveated preliminary control endpoint. It is not a
population validation and it does not close the B2/B3 law-level caveats.

## Figure

paper8_submission_source/figures/fig10_ngc4088_warp_history_accepted_endpoint.png
