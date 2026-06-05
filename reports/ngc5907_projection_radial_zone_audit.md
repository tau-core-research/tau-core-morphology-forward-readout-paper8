# NGC5907 Projection Radial-Zone Audit

This audit separates the accepted projection endpoint into inner, transition,
and outer radial zones. It preserves the negative result that the inner
profile mismatch is not addressed by the frozen projection lane.

## Summary

| galaxy | r_in_kpc | r_out_kpc | inner_n_points | inner_projection_kernel_mean | inner_rmse_projection_accepted | inner_rmse_tpg_v6 | inner_projection_minus_tpg_rmse | active_window_points | active_window_weighted_projection_minus_tpg_rmse | outer_lane_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | 13.3 | 24 | 4 | 0 | 32.516 | 32.516 | 0 | 15 | -3.74784 | ACCEPTED_PROJECTION_ENDPOINT_IS_OUTER_LANE_NOT_FULL_PROFILE | ngc5907_projection_radial_zone_audit_not_full_profile_solution |

## Zone Scores

| galaxy | radial_zone | r_min_kpc | r_max_kpc | n_points | mean_projection_kernel | rmse_tpg_v6 | rmse_projection_accepted | projection_minus_tpg_rmse | mean_abs_projection_shift_kms | zone_interpretation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | inner_pre_projection_window | 5.03 | 12.58 | 4 | 0 | 32.516 | 32.516 | 0 | 0 | projection kernel inactive; inner mismatch is outside this endpoint lane | ngc5907_projection_radial_zone_audit_not_full_profile_solution |
| NGC5907 | transition_projection_window | 15.1 | 22.65 | 4 | 0.464075 | 4.76517 | 3.20103 | -1.56413 | 3.74053 | source-windowed projection kernel turns on | ngc5907_projection_radial_zone_audit_not_full_profile_solution |
| NGC5907 | outer_full_projection_window | 25.16 | 50.33 | 11 | 1 | 9.69225 | 5.15034 | -4.54191 | 7.83882 | projection kernel fully active | ngc5907_projection_radial_zone_audit_not_full_profile_solution |

## Interpretation

The accepted projection endpoint is an outer/projection-lane control. Before
the source-frozen warp onset \(R=13.3\,{\rm kpc}\), the projection
kernel is inactive, so the accepted projection curve is identical to the
TPG carrier. The large inner mismatch is therefore a documented limitation,
not a hidden fitting success. A full-profile NGC5907 model would require a
separately frozen inner disk/core/readout component before scoring.
