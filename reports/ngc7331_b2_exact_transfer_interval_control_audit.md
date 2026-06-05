# NGC7331 B2 Exact Transfer Interval-Control Audit

This audit scores the frozen interval readout as an interval, not as a
single fitted point curve. It does not choose q_warp from residuals.

## Summary

| galaxy | formula_id | audit_status | n_points | coverage_fraction | coverage_fraction_cross_caveated | interval_distance_rmse_km_s | interval_distance_rmse_cross_caveated_km_s | best_baseline_rmse_km_s | best_baseline_model | best_baseline_inside_cross_caveated_interval_fraction | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | point_q_selected_from_residual | claim_boundary | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | NGC7331_EXACT_B2_INTERVAL_CONTROL_AUDIT_COMPLETE_NOT_POINT_ENDPOINT | 36 | 0 | 0 | 56.2674 | 54.8119 | 23.473 | EXPONENTIAL_DISK_CARRIER | 0 | False | True | True | False | ngc7331_b2_exact_transfer_interval_control_audit_not_point_endpoint | interval-control audit only; not a point endpoint and not population validation |

## Interval Scores

| galaxy | model_id | model_role | n_points | coverage_fraction | coverage_fraction_cross_caveated | interval_distance_rmse_km_s | interval_distance_rmse_cross_caveated_km_s | interval_midpoint_rmse_km_s | interval_midpoint_rmse_cross_caveated_km_s | construction_used_vobs | scoring_used_vobs | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | source_frozen_interval_readout | 36 | 0 | 0 | 56.2674 | 54.8119 | 57.8045 | 57.0728 | False | True | ngc7331_b2_exact_transfer_interval_control_audit_not_point_endpoint |

## Baseline Context

| galaxy | model_id | model_role | n_points | rmse_km_s | mae_km_s | fraction_inside_exact_b2_cross_caveated_interval | construction_used_vobs | scoring_used_vobs | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NEWTONIAN_vn | baseline_point_curve | 36 | 59.3544 | 51.4592 | 0.416667 | False | True | ngc7331_b2_exact_transfer_interval_control_audit_not_point_endpoint |
| NGC7331 | TPG_V6_v_v6 | baseline_point_curve | 36 | 25.4851 | 22.2152 | 0 | False | True | ngc7331_b2_exact_transfer_interval_control_audit_not_point_endpoint |
| NGC7331 | MOND_v_mond | baseline_point_curve | 36 | 29.3117 | 26.452 | 0 | False | True | ngc7331_b2_exact_transfer_interval_control_audit_not_point_endpoint |
| NGC7331 | EXPONENTIAL_DISK_CARRIER | baseline_point_curve | 36 | 23.473 | 19.5632 | 0 | False | True | ngc7331_b2_exact_transfer_interval_control_audit_not_point_endpoint |

## Claim Boundary

The audit reads observed velocities only after the formula freeze. Its
primary metrics are interval coverage and distance-to-interval, not a
post-hoc selected q_warp point. A future accepted endpoint may use this
manifest only if it keeps the interval protocol unchanged or declares a
new pre-frozen point-branch protocol before scoring.
