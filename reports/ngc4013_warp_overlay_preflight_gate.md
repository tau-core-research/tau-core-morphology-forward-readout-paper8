# NGC4013 Warp/Overlay Preflight Gate

This gate does not score an endpoint. It records that residual-blind
source evidence pressures the current compact-only label toward a
warp/vertical-overlay readout review.

## Summary

| galaxy | current_manifest_family | preflight_subfamily_candidate | current_matched_rmse | best_existing_family | best_existing_family_rank_of_current | warp_onset_kpc | central_hi_scaleheight_kpc | central_h_over_rs_proxy | s4g_edge_disk_h_over_r | compact_lane_decision | n_gates | n_pass_like | n_blocked | preflight_status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | K_compact_finite | K_warp_vertical_overlay_candidate | 16.9936 | K_exponential_disk | 4 | 10 | 0.21 | 0.0193297 | 0.232932 | COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED | 7 | 6 | 1 | COMPACT_REJECTED_WARP_OVERLAY_PREFLIGHT_READY_FORMULA_BLOCKED | False | ngc4013_warp_overlay_preflight_not_endpoint |

## Source Fields

| field_id | observable | value | numeric_value | unit | status | source | source_line_refs | role | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N4013_F1_OVERLAY_PRESSURE | compact_only_overlay_flag | warp_flare_disk_halo_overlay_present |  | categorical | RECLASSIFICATION_PRESSURE_SOURCE_FIELD | ngc4013_zschaechner_rand_2015_hi_kinematics.txt | 13-23;126-128;170-172 | blocks compact-only endpoint use and motivates warp/overlay review | False | ngc4013_warp_overlay_preflight_not_endpoint |
| N4013_F2_WARP_ONSET | line_of_sight_warp_onset | 10.0 | 10.0 | kpc | ACCEPTED_NUMERIC_SOURCE_FIELD | ngc4013_zschaechner_rand_2015_hi_kinematics.txt | 406-409 | sets first-pass inner support for a future warp/overlay window | False | ngc4013_warp_overlay_preflight_not_endpoint |
| N4013_F3_CENTRAL_HI_SCALEHEIGHT | final_hi_scaleheight_central | 210.0 | 0.21 | kpc | ACCEPTED_NUMERIC_SOURCE_FIELD_CENTRAL_ONLY | ngc4013_zschaechner_rand_2015_hi_kinematics.txt | 430-439 | supplies central vertical kernel proxy, not full radial vertical profile | False | ngc4013_warp_overlay_preflight_not_endpoint |
| N4013_F4_ROTATIONAL_LAG | rotational_lag_profile | lag_shallows_radially_from_minus35_to_zero_near_R25 |  | profile_context | ACCEPTED_CONTEXT_SOURCE_FIELD | ngc4013_zschaechner_rand_2015_hi_kinematics.txt | 13-20;474-480;527-528 | supports disk-halo/vertical-overlay readout review | False | ngc4013_warp_overlay_preflight_not_endpoint |

## Gates

| galaxy | preflight_subfamily_candidate | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | K_warp_vertical_overlay_candidate | N4013_PG1_CURRENT_COMPACT_LABEL_FAILS_AUDIT | PASS | audit decision=RECLASSIFICATION_REVIEW_REQUIRED; matched compact rank=4 | do not use compact-only label for endpoint promotion | False | ngc4013_warp_overlay_preflight_not_endpoint |
| NGC4013 | K_warp_vertical_overlay_candidate | N4013_PG2_WARP_OVERLAY_SOURCE_PRESSURE | PASS | warp_flare_disk_halo_overlay_present | define an explicit replacement readout subfamily | False | ngc4013_warp_overlay_preflight_not_endpoint |
| NGC4013 | K_warp_vertical_overlay_candidate | N4013_PG3_WARP_ONSET_AVAILABLE | PASS | line-of-sight warp onset near 10 kpc | outer warp/projection window still missing | False | ngc4013_warp_overlay_preflight_not_endpoint |
| NGC4013 | K_warp_vertical_overlay_candidate | N4013_PG4_VERTICAL_KERNEL_PARTIAL | PASS_CAVEATED | central HI scaleheight=0.21 kpc; h/Rs proxy=0.01933 | radial vertical profile or endpoint-freeze vertical rule required | False | ngc4013_warp_overlay_preflight_not_endpoint |
| NGC4013 | K_warp_vertical_overlay_candidate | N4013_PG5_ROTATIONAL_LAG_CONTEXT | PASS_CAVEATED | lag_shallows_radially_from_minus35_to_zero_near_R25 | lag profile must be mapped into a source-side readout kernel before scoring | False | ngc4013_warp_overlay_preflight_not_endpoint |
| NGC4013 | K_warp_vertical_overlay_candidate | N4013_PG6_COMPACT_LANE_SOURCE_REVIEW | PASS | COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED | compact endpoint lane rejected unless later independent compact support evidence overturns this review | False | ngc4013_warp_overlay_preflight_not_endpoint |
| NGC4013 | K_warp_vertical_overlay_candidate | N4013_PG7_ENDPOINT_FREEZE_BLOCKED | BLOCKED | no full source-frozen warp/projection radial window and no accepted overlay formula | freeze replacement subfamily formula before any endpoint score | False | ngc4013_warp_overlay_preflight_not_endpoint |

## Interpretation

NGC4013 is not an accepted endpoint row. The current compact-only lane
performs poorly against the wrong-family controls, and the source layer
contains direct warp, scaleheight, rotational-lag, and negative compact
support evidence. The correct next step is a replacement warp/vertical
overlay readout subfamily and formula-freeze protocol, not endpoint
scoring.
