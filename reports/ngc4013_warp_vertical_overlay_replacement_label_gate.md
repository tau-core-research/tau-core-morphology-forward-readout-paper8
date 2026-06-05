# NGC4013 Warp/Vertical-Overlay Replacement-Label Gate

This gate promotes the replacement readout label only at source-side,
caveated preliminary endpoint level. It does not score the rotation curve
and does not validate Tau Core.

## Summary

| galaxy | rejected_label | accepted_replacement_label | n_source_fields | n_gates | n_pass_like | n_blocked | formula_id | label_promotion_status | accepted_replacement_label_promoted | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | K_true_compact | K_warp_vertical_overlay_candidate | 7 | 6 | 6 | 0 | NGC4013_WARP_VERTICAL_OVERLAY_V1 | CAVEATED_REPLACEMENT_LABEL_PROMOTED_ENDPOINT_SCORE_ALLOWED | True | True | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |

## Source Fields

| field_id | field_name | field_value | field_status | source | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| RL1_COMPACT_REJECTION | compact_lane_decision | COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED | ACCEPTED_NEGATIVE_COMPACT_EVIDENCE | S4G decomposition + Comeron vertical decomposition review | False | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |
| RL2_WARP_OVERLAY_PRESSURE | compact_only_overlay_flag | warp_flare_disk_halo_overlay_present | ACCEPTED_RECLASSIFICATION_PRESSURE | ngc4013_zschaechner_rand_2015_hi_kinematics.txt | False | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |
| RL3_WARP_ONSET | line_of_sight_warp_onset | 10 | ACCEPTED_NUMERIC_SOURCE_FIELD | ngc4013_zschaechner_rand_2015_hi_kinematics.txt | False | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |
| RL4_VERTICAL_KERNEL | s4g_edge_disk_h_over_r | 0.2329317269076305 | ACQUIRED_VERTICAL_KERNEL_EVIDENCE | S4G Pipeline 4 edge-disk decomposition | False | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |
| RL5_EXTENDED_COMPONENT | extended_component_mass_fraction | 0.2 | ACQUIRED_EXTENDED_VERTICAL_COMPONENT_EVIDENCE | Comeron et al. 2011 | False | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |
| RL6_CENTRAL_HI_SCALEHEIGHT | final_hi_scaleheight_central | 210 | ACCEPTED_NUMERIC_SOURCE_FIELD | ngc4013_zschaechner_rand_2015_hi_kinematics.txt | False | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |
| RL7_ROTATIONAL_LAG | rotational_lag_profile | lag_shallows_radially_from_minus35_to_zero_near_R25 | ACCEPTED_CONTEXT_SOURCE_FIELD | ngc4013_zschaechner_rand_2015_hi_kinematics.txt | False | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |

## Gates

| galaxy | replacement_label | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | K_warp_vertical_overlay_candidate | N4013_RLG1_COMPACT_LABEL_REJECTED | PASS | COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED | none if compact lane remains rejected | True | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |
| NGC4013 | K_warp_vertical_overlay_candidate | N4013_RLG2_REPLACEMENT_LANE_RECOMMENDED | PASS | PROMOTE_WARP_VERTICAL_OVERLAY_PREFLIGHT_NOT_ENDPOINT | none at source-recommendation level | True | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |
| NGC4013 | K_warp_vertical_overlay_candidate | N4013_RLG3_WARP_VERTICAL_SOURCE_FIELDS | PASS | warp onset, vertical thickness, extended component, and lag context are present | future review may refine R_o, K_lag, or weights without using endpoint residuals | True | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |
| NGC4013 | K_warp_vertical_overlay_candidate | N4013_RLG4_PREFLIGHT_READY | PASS | COMPACT_REJECTED_WARP_OVERLAY_PREFLIGHT_READY_FORMULA_BLOCKED | none at preflight level | True | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |
| NGC4013 | K_warp_vertical_overlay_candidate | N4013_RLG5_FORMULA_FREEZE_PROTOCOL_READY | PASS_CAVEATED | FORMULA_FREEZE_PROTOCOL_READY_LABEL_BLOCKED | caveats: R_o=R25 proxy, linear K_lag shell, uniform weights | True | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |
| NGC4013 | K_warp_vertical_overlay_candidate | N4013_RLG6_ENDPOINT_BLINDNESS | PASS | freeze manifest forbids vobs/residual construction inputs | endpoint scoring must run in a separate script | True | ngc4013_warp_vertical_overlay_replacement_label_gate_not_score |

## Claim Boundary

A promoted replacement label here means that the compact lane has failed
source review and the warp/vertical-overlay lane has enough residual-blind
source support to run a caveated preliminary endpoint. It is not a
population validation claim.
