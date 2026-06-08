# NGC4013 Retrospective Caveat Closure Gate

This gate formalizes the closure path for the NGC4013 retrospective
caveat. It does not change the endpoint status and does not score a
curve.

## Summary

| closure_gate_status | source_rule_transferable | formula_freeze_transferable | control_signal_recorded | retrospective_endpoint_score_forbidden | exact_non_ngc4013_analogue_ready_count | nearest_analogue_candidate | nearest_analogue_freeze_allowed_now | endpoint_status_changed | endpoint_scores_recomputed | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013_RETROSPECTIVE_CAVEAT_CLOSURE_PATH_FORMALIZED_NOT_CLOSED | True | True | True | True | 0 | NGC4088 | False | False | False | False | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |

## Gates

| gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| N4013_RCC1_SOURCE_RULE_TRANSFERABLE | PASS | SOURCE_SUPPORTED_MIXED_HYPOTHESIS_FORMULA_FREEZE_BLOCKED | none for protocol transfer | False | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |
| N4013_RCC2_FORMULA_FREEZE_TRANSFERABLE | PASS | MIXED_FORMULA_FREEZE_READY_NOT_RETROACTIVE_ENDPOINT | future use must read the frozen manifest unchanged | False | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |
| N4013_RCC3_CONTROL_SIGNAL_RECORDED | PASS_DIAGNOSTIC | matched rank=1; matched-minus-best-wrong=-0.752249 | diagnostic/control score cannot be used to accept the old endpoint | False | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |
| N4013_RCC4_RETROACTIVE_SCORE_FORBIDDEN | BLOCKED_RETROACTIVE_ENDPOINT | MIXED_ACCEPTED_ENDPOINT_BLOCKED_RETROACTIVE_PROTOCOL_READY | do not promote the existing NGC4013 score to accepted endpoint evidence | False | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |
| N4013_RCC5_EXACT_ANALOGUE_NOT_READY | BLOCKED_FUTURE_ANALOGUE_REQUIRED | exact non-NGC4013 source-rule analogue ready count=0 | acquire or promote a future source-selected analogue before claiming retrospective-caveat reduction | False | False | ngc4013_retrospective_caveat_closure_gate_not_endpoint |

## Analogue Candidates

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

Status: the retrospective caveat is formalized, but it is not closed.

NGC4013's mixed protocol is transferable: the source rule is ready, the
formula is frozen, and the control signal is recorded. The caveat is not
closed; it is only formalized because the score was inspected before accepted endpoint
promotion. The current package has no exact non-NGC4013 analogue with the
same source-rule readiness. NGC4088 is the closest source-bound analogue,
but its warp/history lane is not the same protocol and remains caveated.
