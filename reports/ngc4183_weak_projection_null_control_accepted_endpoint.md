# NGC4183 Weak-Projection Null-Control Accepted Endpoint

This endpoint is scored as a frozen interval-control branch, not as a
single fitted point curve. It reads observed velocities only after the
accepted null-control gate and frozen formula manifest have passed.

## Summary

| endpoint_status | galaxy | formula_id | n_points | coverage_fraction | interval_distance_rmse_km_s | interval_midpoint_rmse_km_s | best_baseline_rmse_km_s | best_baseline_model | best_baseline_inside_interval_fraction | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | point_selected_from_residual | claim_boundary | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183_ACCEPTED_NULL_CONTROL_INTERVAL_ENDPOINT_COMPLETE | NGC4183 | N4183_WEAK_PROJECTION_NULL_CONTROL_BOUND | 23 | 0.0434783 | 6.20036 | 6.24727 | 6.22458 | EXPONENTIAL_DISK_CARRIER | 1 | False | True | True | False | ngc4183_weak_projection_null_control_accepted_endpoint_preliminary_control | accepted null-control interval endpoint only; not a point-fit endpoint and not population validation |

## Interval Score

| galaxy | model_id | model_role | n_points | coverage_fraction | interval_distance_rmse_km_s | interval_midpoint_rmse_km_s | gamma_bound | max_velocity_fractional_change | construction_used_vobs | scoring_used_vobs | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183 | N4183_WEAK_PROJECTION_NULL_CONTROL_BOUND | accepted_null_control_interval_readout | 23 | 0.0434783 | 6.20036 | 6.24727 | 0.00269837 | 0.0013501 | False | True | ngc4183_weak_projection_null_control_accepted_endpoint_preliminary_control |

## Baseline Context

| galaxy | model_id | model_role | n_points | rmse_km_s | mae_km_s | fraction_inside_null_control_interval | construction_used_vobs | scoring_used_vobs | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183 | NEWTONIAN_vn | baseline_point_curve | 23 | 48.4109 | 47.4836 | 0 | False | True | ngc4183_weak_projection_null_control_accepted_endpoint_preliminary_control |
| NGC4183 | TPG_V6_v_v6 | baseline_point_curve | 23 | 6.48969 | 5.6918 | 0 | False | True | ngc4183_weak_projection_null_control_accepted_endpoint_preliminary_control |
| NGC4183 | MOND_v_mond | baseline_point_curve | 23 | 10.355 | 9.23844 | 0 | False | True | ngc4183_weak_projection_null_control_accepted_endpoint_preliminary_control |
| NGC4183 | EXPONENTIAL_DISK_CARRIER | baseline_point_curve | 23 | 6.22458 | 4.86106 | 1 | False | True | ngc4183_weak_projection_null_control_accepted_endpoint_preliminary_control |

## Claim Boundary

The branch preserves the frozen null-control interval unchanged. It does
not select a residual-tuned point coefficient inside the interval. The
endpoint result is therefore an accepted single-galaxy interval-control
readout, not a point-fit validation and not population validation.
