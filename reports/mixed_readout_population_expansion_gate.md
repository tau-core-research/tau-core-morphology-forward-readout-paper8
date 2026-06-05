# Mixed Readout Population Expansion Gate

This gate ranks next candidates after the three-case matched-vs-wrong
control. It does not score rotations and does not promote endpoint
labels. Its job is to prevent the next expansion from being driven by
the already inspected endpoint residuals.

## Summary

| expansion_gate_status | three_case_control_passed | next_primary_galaxy | next_primary_candidate_readout | next_primary_formula_freeze_allowed_now | n_candidates_ranked | n_formula_freeze_allowed_now | n_source_acquisition_required | n_review_required | endpoint_scores_allowed | uses_vobs_or_residual_in_selection | claim_boundary | next_required_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT_MIXED_CASE_IDENTIFIED_FORMULA_FREEZE_BLOCKED | True | NGC4088 | K_expdisk_warp_history_coupled_mixed_review | False | 10 | 1 | 8 | 0 | False | False | mixed_readout_population_expansion_gate_not_endpoint | resolve independent digitization review, physical normalization law, and scale-uniqueness before any mixed formula freeze |

## Candidate Ranking

| galaxy | expansion_priority | candidate_readout | source_side_strength | source_rule_candidate | formula_freeze_allowed_now | has_numeric_source_onset | has_q_memory_review | has_epsilon_bound | has_smooth_disk_scale | main_blockers | next_required_gate | source_evidence_summary | endpoint_scores_allowed | uses_vobs_or_residual_in_selection | expansion_gate_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | P0_CLOSEST_SOURCE_BOUND_MIXED_PROTOCOL | K_expdisk_warp_history_coupled_mixed_review | BREAKTHROUGH_PROTOCOL_BOUND_READY_NOT_ENDPOINT | False | False | True | True | True | True | INDEPENDENT_DIGITIZATION_REVIEW;PHYSICAL_NORMALIZATION_LAW;POPULATION_GENERALIZATION;BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES | resolve independent digitization review, physical normalization law, and scale-uniqueness before any mixed formula freeze | x_w=0.282353; q=1; m_history=1; |epsilon_cross|<=0.6875; input_review=INPUT_REVIEW_PACKET_NUMERIC_PROTOCOL_BOUND_READY | False | False | FORMULA_FREEZE_BLOCKED_SOURCE_PROTOCOL_CLOSEST | mixed_readout_population_expansion_gate_not_endpoint |
| NGC4183 | P1_WEAK_PROJECTION_NULL_CONTROL_REVIEW | K_expdisk_edge_on_projection_weak_null_control_review | NGC4183_WEAK_PROJECTION_CONTROL_PREFLIGHT_COMPLETE_NOT_ENDPOINT | False | True | True | False | True | True | none | none | tilted-ring orientation profile supports weak projection/null-control; gamma_bound<=0.00269837 | True | False | SEPARATE_NULL_CONTROL_BRANCH_COMPLETE_NOT_MIXED_PROMOTION_CANDIDATE | mixed_readout_population_expansion_gate_not_endpoint |
| IC2574 | P1_DISTURBED_TAIL_NUMERIC_RADIUS_REQUIRED | K_expdisk_disturbed_outer_tail_overlay_review | DISTURBED_CONTEXT_ACCEPTED_NUMERIC_KERNEL_BLOCKED | False | False | False | False | False | False | outer_tail_transition_radius_missing | extract tail/envelope transition radius or HI radial support kernel | extended HI envelope and HI-hole/history context accepted; numeric tail transition missing | False | False | SOURCE_ACQUISITION_REQUIRED | mixed_readout_population_expansion_gate_not_endpoint |
| UGC05716 | P1_TAIL_ASYMMETRY_NUMERIC_FIELDS_REQUIRED | K_expdisk_tail_asymmetry_projection_overlay_review | HI_ROTATION_CONTEXT_ACCEPTED_NUMERIC_KERNEL_BLOCKED | False | False | False | False | False | False | HI_asymmetry_or_tail_measurement_missing | extract HI asymmetry/tail observable from source map or profile | HI/projection context available; no extracted asymmetry/tail metric | False | False | SOURCE_ACQUISITION_REQUIRED | mixed_readout_population_expansion_gate_not_endpoint |
| NGC0024 | P2_BULK_SOURCE_ACQUISITION | K_expdisk_thick_flared_overlay_review | S4G75_DIRECT_SOURCE_NATIVE_ACQUISITION_ROW | False | False | False | False | False | True | external_family_label_audit_pending;thickness_h_over_rs | source_acquisition_and_extraction_before_formula_freeze | vertical_scale_height_kpc; h_over_Rs; flare_or_warp_radius_kpc; edge_on_thickness_evidence; gas_plane_thickness_or_warp | False | False | BULK_SOURCE_ACQUISITION_REQUIRED | mixed_readout_population_expansion_gate_not_endpoint |
| NGC2683 | P2_BULK_SOURCE_ACQUISITION | K_expdisk_thick_flared_overlay_review | S4G75_DIRECT_SOURCE_NATIVE_ACQUISITION_ROW | False | False | False | False | False | True | external_family_label_audit_pending;thickness_h_over_rs | source_acquisition_and_extraction_before_formula_freeze | vertical_scale_height_kpc; h_over_Rs; flare_or_warp_radius_kpc; edge_on_thickness_evidence; gas_plane_thickness_or_warp | False | False | BULK_SOURCE_ACQUISITION_REQUIRED | mixed_readout_population_expansion_gate_not_endpoint |
| NGC3726 | P2_BULK_SOURCE_ACQUISITION | K_expdisk_thick_flared_overlay_review | S4G75_DIRECT_SOURCE_NATIVE_ACQUISITION_ROW | False | False | False | False | False | True | external_family_label_audit_pending;thickness_h_over_rs | source_acquisition_and_extraction_before_formula_freeze | vertical_scale_height_kpc; h_over_Rs; flare_or_warp_radius_kpc; edge_on_thickness_evidence; gas_plane_thickness_or_warp | False | False | BULK_SOURCE_ACQUISITION_REQUIRED | mixed_readout_population_expansion_gate_not_endpoint |
| NGC3949 | P2_BULK_SOURCE_ACQUISITION | K_expdisk_thick_flared_overlay_review | S4G75_DIRECT_SOURCE_NATIVE_ACQUISITION_ROW | False | False | False | False | False | True | external_family_label_audit_pending;thickness_h_over_rs | source_acquisition_and_extraction_before_formula_freeze | vertical_scale_height_kpc; h_over_Rs; flare_or_warp_radius_kpc; edge_on_thickness_evidence; gas_plane_thickness_or_warp | False | False | BULK_SOURCE_ACQUISITION_REQUIRED | mixed_readout_population_expansion_gate_not_endpoint |
| NGC4214 | P2_BULK_SOURCE_ACQUISITION | K_expdisk_tail_or_outer_disk_overlay_review | S4G75_DIRECT_SOURCE_NATIVE_ACQUISITION_ROW | False | False | False | False | False | True | external_family_label_audit_pending;tail_inner_radius_kpc;tail_cutoff_radius_kpc | source_acquisition_and_extraction_before_formula_freeze | outer_disk_break_radius_kpc; HI_radial_profile_or_RHI_kpc; tail_inner_radius_kpc; tail_cutoff_radius_kpc; truncation_radius_kpc | False | False | BULK_SOURCE_ACQUISITION_REQUIRED | mixed_readout_population_expansion_gate_not_endpoint |
| UGC06917 | P2_BULK_SOURCE_ACQUISITION | K_expdisk_tail_or_outer_disk_overlay_review | S4G75_DIRECT_SOURCE_NATIVE_ACQUISITION_ROW | False | False | False | False | False | True | external_family_label_audit_pending;tail_inner_radius_kpc;tail_cutoff_radius_kpc | source_acquisition_and_extraction_before_formula_freeze | outer_disk_break_radius_kpc; HI_radial_profile_or_RHI_kpc; tail_inner_radius_kpc; tail_cutoff_radius_kpc; truncation_radius_kpc | False | False | BULK_SOURCE_ACQUISITION_REQUIRED | mixed_readout_population_expansion_gate_not_endpoint |

## Obligations

| gate_id | gate_status | obligation | claim_boundary |
| --- | --- | --- | --- |
| EXP1_NO_ENDPOINT_SCORING | PASS | expansion gate ranks candidates but scores no rotation curve | mixed_readout_population_expansion_gate_not_endpoint |
| EXP2_CONTROL_SIGNAL_PRESERVED | PASS | three-case matched-vs-wrong control must remain recorded before expanding | mixed_readout_population_expansion_gate_not_endpoint |
| EXP3_NGC4088_NOT_PROMOTED | PASS | NGC4088 diagnostic signal cannot be used as source-label evidence | mixed_readout_population_expansion_gate_not_endpoint |
| EXP4_FORMULA_FREEZE_BLOCKED_UNTIL_SOURCE_RULE | PASS | no fourth mixed formula freeze until blockers are resolved residual-blind | mixed_readout_population_expansion_gate_not_endpoint |

## Interpretation

NGC4088 is the closest next mixed case because it has a source-bound
warp/history protocol chain, including x_w, q, memory, and epsilon-cross
bound ingredients. It is still blocked from formula freeze by independent
digitization review, physical normalization-law derivation, and scale
uniqueness. The diagnostic NGC4088 curve is not used as promotion evidence.

NGC4183 is no longer a pending review candidate in this queue. Its
weak-projection/null-control branch has already passed independent source
review, freeze, accepted-control promotion, and interval-control scoring
as a separate single-galaxy control lane. It therefore stays outside the
next mixed-case promotion race, while preserving a narrow null-control
claim boundary rather than a mixed population-validation role.
