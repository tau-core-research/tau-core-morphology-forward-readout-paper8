# NGC4088 Mixed Formula-Freeze Blocker Resolution Plan

This report is a source-side planning gate. It does not score the
rotation curve, does not promote an endpoint, and does not use the
previous NGC4088 diagnostic curve as evidence.

## Summary

| resolution_plan_status | galaxy | candidate_readout | n_formula_freeze_blockers | n_population_claim_blockers | n_protocol_ready_supports | all_formula_freeze_blockers_resolved | formula_freeze_allowed_now | endpoint_scores_allowed | uses_vobs_or_residual | promotion_decision_now | scale_selection_status | scale_derivation_status | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088_FORMULA_FREEZE_BLOCKER_RESOLUTION_PLAN_CREATED | NGC4088 | K_expdisk_warp_history_coupled_mixed_review | 3 | 1 | 3 | False | False | False | False | PROMOTION_BLOCKED_PREFLIGHT_READY | THEORY_SELECTION_CONDITIONAL_CURRENT_ONLY | DERIVATION_BLOCKED_SELECTION_RULE_AUDITED | resolve B1, B2, and B3 residual-blind; keep B4 as a population-claim caveat unless a population test is launched | ngc4088_mixed_formula_freeze_blocker_resolution_not_endpoint |

## Formula-Freeze And Population Blockers

| blocker_id | blocker_scope | current_status | current_evidence | resolution_condition | source_files | endpoint_scores_allowed_after_this_alone | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B1_INDEPENDENT_XW_DIGITIZATION_REVIEW | formula_freeze | BLOCKED | x_w conversion status=XW_READY_FOR_MAPPING_RULE; accepted_for_mapping_rule=True | obtain independent residual-blind channel-map digitization review or freeze a reproducible image-analysis extraction for x_w | s4g75_ngc4088_xw_conversion_summary.csv;s4g75_ngc4088_readout_promotion_gate.csv | False | ngc4088_mixed_formula_freeze_blocker_resolution_not_endpoint |
| B2_PHYSICAL_NORMALIZATION_LAW | formula_freeze | FORMULA_CONDITIONAL_PHYSICAL_LAW_BLOCKED | candidate prefactor 8324.02 km2/s2; formula is dimensionally consistent but Tau-side law is not derived | derive or explicitly predeclare the Tau-side mapping from the dimensionless closure-source basis to delta v^2 | s4g75_ngc4088_physical_normalization_law_summary.csv;s4g75_ngc4088_physical_normalization_law_gate.csv | False | ngc4088_mixed_formula_freeze_blocker_resolution_not_endpoint |
| B3_SCALE_UNIQUENESS | formula_freeze | BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES | 5 residual-blind candidate scales exist; current conditional choice=CURRENT_XW_VFLAT2; candidate_ids=CURRENT_XW_VFLAT2;XW_MEDIAN_VN2;XW_MEDIAN_VV62;CLOSURE_FRACTION_MEDIAN_VN2;XW_CLOSURE_FRACTION_MEDIAN_VN2 | freeze a residual-blind theory criterion selecting one scale before endpoint scoring, or demote the lane to sensitivity analysis | s4g75_ngc4088_scale_uniqueness_summary.csv;s4g75_ngc4088_scale_uniqueness_audit.csv;s4g75_ngc4088_tau_side_scale_selection_summary.csv;s4g75_ngc4088_tau_side_scale_derivation_summary.csv | False | ngc4088_mixed_formula_freeze_blocker_resolution_not_endpoint |
| B4_POPULATION_GENERALIZATION | population_claim | BLOCKED_FOR_POPULATION_CLAIMS | NGC4088 is one source-filled warp/history lane; the three-case mixed control is promising but small-N | repeat the same source-side freeze protocol on a predeclared source-rich warp/history sample before making population claims | s4g75_ngc4088_readout_promotion_summary.csv;mixed_readout_population_expansion_summary.csv | False | ngc4088_mixed_formula_freeze_blocker_resolution_not_endpoint |

## Protocol-Ready Supports

| support_id | support_status | evidence | why_it_is_not_enough | claim_boundary |
| --- | --- | --- | --- | --- |
| S1_BREAKTHROUGH_PROTOCOL_CHAIN | BREAKTHROUGH_PROTOCOL_BOUND_READY_NOT_ENDPOINT | x_w=0.282353; q_warp=1; m_history=1; |epsilon_cross|<=0.6875 | protocol-bound ingredients exist, but accepted endpoint use still requires formula-freeze blockers to close | ngc4088_mixed_formula_freeze_blocker_resolution_not_endpoint |
| S2_Q_MEMORY_AND_BI_REVIEW | PROTOCOL_BOUND_READY | source_review=SOURCE_RESPONSES_ACCEPTED_FOR_PROTOCOL_BOUND; bi_rule=FEATURE_NORMALIZATION_AND_B_VALUES_READY_PROTOCOL_BOUND; epsilon_review=INPUT_REVIEW_PACKET_NUMERIC_PROTOCOL_BOUND_READY | these pass the epsilon-cross bound protocol, but do not derive the velocity normalization law or select a unique scale | ngc4088_mixed_formula_freeze_blocker_resolution_not_endpoint |
| S3_EXPANSION_GATE_PRIORITY | NEXT_MIXED_CASE_IDENTIFIED_FORMULA_FREEZE_BLOCKED | next_primary=NGC4088; candidate_readout=K_expdisk_warp_history_coupled_mixed_review; uses_vobs_or_residual_in_selection=False | candidate priority is not endpoint authorization; it only says where the next residual-blind source work should focus | ngc4088_mixed_formula_freeze_blocker_resolution_not_endpoint |

## Interpretation

NGC4088 remains the closest fourth mixed-readout candidate, but the
formula-freeze path is still blocked by three local source-side issues:
independent x_w digitization review, a Tau-side physical normalization
law, and a unique residual-blind scale-selection rule. Population
generalization is tracked separately: it blocks broad claims, but it is
not a substitute for the three local formula-freeze obligations.
