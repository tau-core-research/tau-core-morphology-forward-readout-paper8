# NGC4013 Warp/Vertical-Overlay Radial-Zone Audit

This audit separates the caveated NGC4013 endpoint into inner, transition,
and outer radial zones. It preserves whether the source-windowed readout
acts only where its source morphology is active.

## Summary

| galaxy | r_warp_kpc | r_outer_kpc | inner_n_points | inner_K_wvo_mean | inner_rmse_warp_vertical_overlay | inner_rmse_tpg_v6 | inner_wvo_minus_tpg_rmse | active_window_points | active_window_weighted_wvo_minus_tpg_rmse | outer_lane_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | 10 | 11.2 | 7 | 0 | 12.7954 | 12.7954 | 0 | 29 | -1.03689 | WARP_VERTICAL_OVERLAY_ENDPOINT_IS_OUTER_LANE_NOT_FULL_PROFILE | ngc4013_warp_vertical_overlay_radial_zone_audit_not_full_profile_solution |

## Zone Scores

| galaxy | radial_zone | r_min_kpc | r_max_kpc | n_points | mean_K_wvo | mean_wvo_attenuation | rmse_tpg_v6 | rmse_warp_vertical_overlay | wvo_minus_tpg_rmse | mean_abs_wvo_shift_kms | zone_interpretation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | inner_pre_warp_window | 5.49 | 9.88 | 7 | 0 | 0 | 12.7954 | 12.7954 | 0 | 0 | warp/overlay kernel inactive; this endpoint does not address inner structure | ngc4013_warp_vertical_overlay_radial_zone_audit_not_full_profile_solution |
| NGC4013 | transition_warp_window | 10.56 | 10.56 | 1 | 0.0786621 | 0.0170277 | 16.2853 | 14.5386 | -1.74672 | 1.74672 | source warp window turns on between R_w and R_o | ngc4013_warp_vertical_overlay_radial_zone_audit_not_full_profile_solution |
| NGC4013 | outer_overlay_window | 11.31 | 31.01 | 28 | 0.0803823 | 0.0174 | 11.9703 | 10.9588 | -1.01154 | 1.59184 | warp/vertical-overlay kernel active; endpoint lane should act here | ngc4013_warp_vertical_overlay_radial_zone_audit_not_full_profile_solution |

## Interpretation

Before the source-frozen warp onset \(R=10\,{\rm kpc}\),
the warp/vertical-overlay kernel is inactive and the curve equals the TPG
carrier. Improvement outside that window supports the source-lane reading;
a remaining inner mismatch would require a separately frozen inner
disk/core/readout component.
