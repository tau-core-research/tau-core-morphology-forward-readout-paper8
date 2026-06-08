# NGC4013 Predeclared Replay/Holdout Gate

This gate converts the NGC4013 retrospective caveat into explicit future-use
rules. It does not score a rotation curve and does not change the endpoint
status.

## Summary

| predeclared_replay_gate_status | source_rule_transferable | formula_manifest_transferable | prospective_endpoint_protocol_ready | existing_score_quarantined | same_curve_replay_allowed | future_holdout_route_defined | future_analogue_route_defined | exact_non_ngc4013_analogue_ready_count | endpoint_scores_allowed | endpoint_scores_recomputed | uses_vobs_or_residual | uses_existing_score_summary_as_diagnostic_context | next_required_gate | formula_id | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013_PREDECLARED_REPLAY_HOLDOUT_GATE_BUILT_ENDPOINT_STILL_BLOCKED | True | True | True | True | False | True | True | 0 | False | False | False | True | FUTURE_UNINSPECTED_HOLDOUT_OR_SOURCE_SELECTED_ANALOGUE | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | ngc4013_predeclared_replay_holdout_gate_not_endpoint |

## Gates

| gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| N4013_PRH1_SOURCE_RULE_TRANSFER | PASS | NGC4013_RETROSPECTIVE_CAVEAT_CLOSURE_PATH_FORMALIZED_NOT_CLOSED | future route must read the source rule unchanged | False | False | ngc4013_predeclared_replay_holdout_gate_not_endpoint |
| N4013_PRH2_FORMULA_MANIFEST_TRANSFER | PASS | MIXED_FORMULA_FREEZE_READY_NOT_RETROACTIVE_ENDPOINT | future route must read the frozen formula manifest unchanged | False | False | ngc4013_predeclared_replay_holdout_gate_not_endpoint |
| N4013_PRH3_RETROSPECTIVE_SCORE_QUARANTINE | PASS_SCORE_QUARANTINED | MIXED_ACCEPTED_ENDPOINT_BLOCKED_RETROACTIVE_PROTOCOL_READY | do not use the existing NGC4013 score as accepted endpoint evidence | False | False | ngc4013_predeclared_replay_holdout_gate_not_endpoint |
| N4013_PRH4_EXACT_ANALOGUE_AVAILABILITY | BLOCKED_FUTURE_ANALOGUE_REQUIRED | exact_non_ngc4013_analogue_ready_count=0 | source-select a non-NGC4013 analogue before analogue endpoint scoring | False | False | ngc4013_predeclared_replay_holdout_gate_not_endpoint |
| N4013_PRH5_NO_CURRENT_ENDPOINT_SCORE | BLOCKED_ENDPOINT_SCORE_NOT_ALLOWED_NOW | this gate does not read vobs and does not score a curve | endpoint scoring requires a future predeclared route | False | False | ngc4013_predeclared_replay_holdout_gate_not_endpoint |

## Future Routes

| route_id | route_status | allowed_future_use | endpoint_scores_allowed_now | reason | required_next_input | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| R1_SAME_CURVE_REPLAY | BLOCKED_RETROSPECTIVE_CURVE_ALREADY_INSPECTED | False | False | the existing NGC4013 rotation curve and controls have already been inspected; rescoring the same curve cannot remove the retrospective caveat | none; route is protocol-forbidden | ngc4013_predeclared_replay_holdout_gate_not_endpoint |
| R2_PREDECLARED_NEW_HOLDOUT | FUTURE_ONLY_REQUIRES_UNINSPECTED_HOLDOUT_DATA | True | False | the frozen source rule and formula may be applied only if the holdout target is declared before endpoint residuals or score ranks are inspected | new uninspected NGC4013-compatible holdout target or data release | ngc4013_predeclared_replay_holdout_gate_not_endpoint |
| R3_SOURCE_SELECTED_ANALOGUE | BLOCKED_NO_EXACT_ANALOGUE_READY | False | False | no non-NGC4013 galaxy currently has the same expdisk+WVO source-rule readiness | promote an exact non-NGC4013 source-selected analogue | ngc4013_predeclared_replay_holdout_gate_not_endpoint |
| R4_POPULATION_REPLAY | FUTURE_ONLY_POPULATION_PROTOCOL | True | False | the NGC4013 protocol can be one predeclared member of a future population replay, but not a standalone retroactive endpoint | predeclared population packet with source-selected rows | ngc4013_predeclared_replay_holdout_gate_not_endpoint |

## Analogue Snapshot

| galaxy | candidate_readout | analogue_class | source_side_strength | formula_freeze_allowed_now | main_blockers | next_required_gate | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | K_expdisk_warp_history_coupled_mixed_review | closest_warp_history_not_same_protocol | BREAKTHROUGH_PROTOCOL_BOUND_READY_NOT_ENDPOINT | False | INDEPENDENT_DIGITIZATION_REVIEW;PHYSICAL_NORMALIZATION_LAW;POPULATION_GENERALIZATION;BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES | resolve independent digitization review, physical normalization law, and scale-uniqueness before any mixed formula freeze | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |
| NGC4183 | K_expdisk_edge_on_projection_weak_null_control_review | source_acquisition_candidate | NGC4183_WEAK_PROJECTION_CONTROL_PREFLIGHT_COMPLETE_NOT_ENDPOINT | True | none | none | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |
| IC2574 | K_expdisk_disturbed_outer_tail_overlay_review | source_acquisition_candidate | DISTURBED_CONTEXT_ACCEPTED_NUMERIC_KERNEL_BLOCKED | False | outer_tail_transition_radius_missing | extract tail/envelope transition radius or HI radial support kernel | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |
| UGC05716 | K_expdisk_tail_asymmetry_projection_overlay_review | source_acquisition_candidate | HI_ROTATION_CONTEXT_ACCEPTED_NUMERIC_KERNEL_BLOCKED | False | HI_asymmetry_or_tail_measurement_missing | extract HI asymmetry/tail observable from source map or profile | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |
| NGC0024 | K_expdisk_thick_flared_overlay_review | source_acquisition_candidate | S4G75_DIRECT_SOURCE_NATIVE_ACQUISITION_ROW | False | external_family_label_audit_pending;thickness_h_over_rs | source_acquisition_and_extraction_before_formula_freeze | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |
| NGC2683 | K_expdisk_thick_flared_overlay_review | source_acquisition_candidate | S4G75_DIRECT_SOURCE_NATIVE_ACQUISITION_ROW | False | external_family_label_audit_pending;thickness_h_over_rs | source_acquisition_and_extraction_before_formula_freeze | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |
| NGC3726 | K_expdisk_thick_flared_overlay_review | source_acquisition_candidate | S4G75_DIRECT_SOURCE_NATIVE_ACQUISITION_ROW | False | external_family_label_audit_pending;thickness_h_over_rs | source_acquisition_and_extraction_before_formula_freeze | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |
| NGC3949 | K_expdisk_thick_flared_overlay_review | source_acquisition_candidate | S4G75_DIRECT_SOURCE_NATIVE_ACQUISITION_ROW | False | external_family_label_audit_pending;thickness_h_over_rs | source_acquisition_and_extraction_before_formula_freeze | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |
| NGC4214 | K_expdisk_tail_or_outer_disk_overlay_review | source_acquisition_candidate | S4G75_DIRECT_SOURCE_NATIVE_ACQUISITION_ROW | False | external_family_label_audit_pending;tail_inner_radius_kpc;tail_cutoff_radius_kpc | source_acquisition_and_extraction_before_formula_freeze | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |
| UGC06917 | K_expdisk_tail_or_outer_disk_overlay_review | source_acquisition_candidate | S4G75_DIRECT_SOURCE_NATIVE_ACQUISITION_ROW | False | external_family_label_audit_pending;tail_inner_radius_kpc;tail_cutoff_radius_kpc | source_acquisition_and_extraction_before_formula_freeze | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |

## Interpretation

Status: the NGC4013 source rule and frozen expdisk+WVO formula are transferable,
but the existing score remains quarantined. A same-curve replay is explicitly
blocked because the NGC4013 curve and controls have already been inspected.
The admissible routes are future-only: a genuinely predeclared uninspected
holdout target, a source-selected non-NGC4013 analogue, or a predeclared
population replay packet. Therefore this gate narrows the caveat but does
not close it.
