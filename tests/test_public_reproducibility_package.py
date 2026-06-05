import subprocess
import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper8_submission_source"
DATA = ROOT / "data" / "derived"


def test_publication_files_exist():
    required = [
        ROOT / "README.md",
        ROOT / "docs" / "tau_core_gravity_bridge_central.md",
        ROOT / "LICENSE",
        ROOT / "CITATION.cff",
        ROOT / "DATA_NOTICE.md",
        ROOT / "requirements.txt",
        SOURCE / "main.tex",
        SOURCE / "refs.bib",
        SOURCE / "main.pdf",
        SOURCE / "figures",
        ROOT / "figures",
        ROOT / "scripts/generate_paper8_artifacts.py",
        ROOT / "scripts/audit_paper8_foundations.py",
        ROOT / "scripts/run_available_morphology_readout_pilot.py",
        ROOT / "scripts/run_morphology_matched_proxy_endpoint.py",
        ROOT / "scripts/run_morphology_formula_shell_proxy_endpoint.py",
        ROOT / "scripts/build_morphology_parameter_manifest.py",
        ROOT / "scripts/run_source_native_readout_formula_endpoint.py",
        ROOT / "scripts/run_readout_mixture_proxy_endpoint.py",
        ROOT / "scripts/run_manifest_confidence_diagnostics.py",
        ROOT / "scripts/run_amplitude_policy_diagnostics.py",
        ROOT / "scripts/run_amplitude_shrinkage_path.py",
        ROOT / "scripts/run_train_selected_shrinkage_diagnostic.py",
        ROOT / "scripts/run_family_breakdown_diagnostics.py",
        ROOT / "scripts/run_family_observable_quality_diagnostics.py",
        ROOT / "scripts/audit_baseline_success_morphology.py",
        ROOT / "scripts/run_predeclared_quality_gate_diagnostics.py",
        ROOT / "scripts/run_quality_gate_shuffled_null_diagnostics.py",
        ROOT / "scripts/run_endpoint_decision_matrix.py",
        ROOT / "scripts/build_predeclared_endpoint_protocol.py",
        ROOT / "scripts/build_readiness_upgrade_audit.py",
        ROOT / "scripts/build_morphology_observable_intake_schema.py",
        ROOT / "scripts/run_morphology_observable_gap_audit.py",
        ROOT / "scripts/build_morphology_observable_source_upgrade_plan.py",
        ROOT / "scripts/build_accepted_observable_manifest_template.py",
        ROOT / "scripts/run_accepted_manifest_readiness_gate.py",
        ROOT / "scripts/run_frozen_endpoint_launch_guard.py",
        ROOT / "scripts/build_external_morphology_source_registry.py",
        ROOT / "scripts/acquire_external_morphology_inputs.py",
        ROOT / "scripts/build_accepted_morphology_manifest.py",
        ROOT / "scripts/audit_accepted_morphology_manifest.py",
        ROOT / "scripts/audit_exponential_disk_family_labels.py",
        ROOT / "scripts/run_exponential_disk_narrow_dry_run.py",
        ROOT / "scripts/audit_exponential_disk_failure_sensitivity.py",
        ROOT / "scripts/run_rotation_inferred_morphology_diagnostic.py",
        ROOT / "scripts/build_morphological_memory_history_proxy.py",
        ROOT / "scripts/build_readout_state_vector_intake_schema.py",
        ROOT / "scripts/build_morphology_inspection_queue.py",
        ROOT / "scripts/build_p0_morphology_inspection_packets.py",
        ROOT / "scripts/build_p0_external_imaging_request_manifest.py",
        ROOT / "scripts/build_p0_external_imaging_review_dashboard.py",
        ROOT / "scripts/audit_p0_skyview_availability.py",
        ROOT / "scripts/acquire_p0_skyview_preview_images.py",
        ROOT / "scripts/build_p0_visual_review_template.py",
        ROOT / "scripts/run_p0_visual_review_completion_gate.py",
        ROOT / "scripts/build_p0_visual_review_handoff.py",
        ROOT / "scripts/build_p0_visual_review_response_intake.py",
        ROOT / "scripts/run_p0_response_to_manifest_promotion_gate.py",
        ROOT / "scripts/build_p0_missing_data_source_acquisition_plan.py",
        ROOT / "scripts/acquire_p0_dustpedia_hi_phangs_sources.py",
        ROOT / "scripts/build_p0_source_assisted_review_response_draft.py",
        ROOT / "scripts/build_p0_codex_source_review_response.py",
        ROOT / "scripts/build_p0_codex_accepted_label_manifest.py",
        ROOT / "scripts/build_p0_readout_relevant_morphology_proxy.py",
        ROOT / "scripts/run_p0_codex_source_review_pilot.py",
        ROOT / "scripts/audit_p0_requested_source_family_availability.py",
        ROOT / "scripts/build_p0_review_pipeline_status_dashboard.py",
        ROOT / "scripts/build_morphology_information_gain_source_expansion.py",
        ROOT / "scripts/build_l2_weight_intake_candidates.py",
        ROOT / "scripts/run_l2_weight_intake_endpoint_preflight.py",
        ROOT / "scripts/build_tau_side_source_normalization_derivation_audit.py",
        ROOT / "scripts/run_tau_side_source_normalized_l2_endpoint.py",
        ROOT / "scripts/audit_tau_side_source_normalization_sensitivity.py",
        ROOT / "scripts/build_source_native_orientation_promotion_gate.py",
        ROOT / "scripts/build_memory_projection_acceptance_gate.py",
        ROOT / "scripts/build_inclusion_lane_expansion_audit.py",
        ROOT / "scripts/run_inclusion_lane_endpoint_analysis.py",
        ROOT / "scripts/build_projection_scale_repair_audit.py",
        ROOT / "scripts/audit_source_normalization_failure_modes_by_lane.py",
        ROOT / "scripts/audit_l2_weight_freeze_readiness.py",
        ROOT / "scripts/build_tau_side_evidence_measure_gate.py",
        ROOT / "scripts/run_tau_side_evidence_measure_l2_endpoint.py",
        ROOT / "scripts/run_morphology_information_gain_test.py",
        ROOT / "scripts/acquire_s4g75_direct_kernel_measurements.py",
        ROOT / "scripts/build_s4g75_kernel_ready_promotion_gate.py",
        ROOT / "scripts/build_s4g75_promoted_kernel_observable_fill.py",
        ROOT / "scripts/run_s4g75_promoted_kernel_endpoint_stress_test.py",
        ROOT / "scripts/build_s4g75_tail_rhi_promotion_attempt.py",
        ROOT / "scripts/build_s4g75_remaining_kernel_acquisition_ledger.py",
        ROOT / "scripts/build_s4g75_literature_kernel_source_hits.py",
        ROOT / "scripts/build_s4g75_vertical_source_search_audit.py",
        ROOT / "scripts/build_s4g75_ngc4088_warp_asymmetry_extraction_gate.py",
        ROOT / "scripts/build_s4g75_ngc4088_warp_prekernel_observables.py",
        ROOT / "scripts/build_s4g75_ngc4088_warp_closure_mapping_rule.py",
        ROOT / "scripts/build_s4g75_ngc4088_warp_onset_extraction_protocol.py",
        ROOT / "scripts/build_s4g75_ngc4088_digitization_target_manifest.py",
        ROOT / "scripts/build_s4g75_ngc4088_channel_map_digitization_worksheet.py",
        ROOT / "scripts/build_s4g75_ngc4088_channel_map_digitization_protocol.py",
        ROOT / "scripts/build_s4g75_ngc4088_xw_conversion_audit.py",
        ROOT / "scripts/build_s4g75_ngc4088_filled_warp_closure_mapping.py",
        ROOT / "scripts/build_s4g75_ngc4088_kernel_to_velocity_normalization_candidate.py",
        ROOT / "scripts/build_s4g75_ngc4088_readout_preflight_profile.py",
        ROOT / "scripts/build_s4g75_ngc4088_physical_normalization_law_gate.py",
        ROOT / "scripts/build_s4g75_ngc4088_scale_uniqueness_audit.py",
        ROOT / "scripts/build_s4g75_ngc4088_tau_side_scale_selection_gate.py",
        ROOT / "scripts/build_s4g75_ngc4088_tau_side_scale_derivation_gate.py",
        ROOT / "scripts/build_s4g75_ngc4088_asymptotic_carrier_dominance_gate.py",
        ROOT / "scripts/build_s4g75_ngc4088_closure_functional_requirement_gate.py",
        ROOT / "scripts/build_s4g75_ngc4088_minimal_euler_ansatz_gate.py",
        ROOT / "scripts/build_s4g75_ngc4088_target_functional_origin_gate.py",
        ROOT / "scripts/build_s4g75_ngc4088_multiplicative_coupling_separability_gate.py",
        ROOT / "scripts/build_s4g75_ngc4088_cross_term_suppression_gate.py",
        ROOT / "scripts/build_s4g75_ngc4088_epsilon_cross_source_bound_protocol.py",
        ROOT / "scripts/build_s4g75_ngc4088_qwarp_measurement_protocol.py",
        ROOT / "scripts/build_s4g75_ngc4088_memory_history_proxy_protocol.py",
        ROOT / "scripts/build_s4g75_ngc4088_first_pass_source_response_fill.py",
        ROOT / "scripts/build_s4g75_ngc4088_h4_interaction_context_review.py",
        ROOT / "scripts/build_s4g75_ngc4088_source_response_independent_review.py",
        ROOT / "scripts/build_s4g75_ngc4088_bi_coefficient_freeze_rule.py",
        ROOT / "scripts/build_s4g75_ngc4088_bi_sharp_coefficient_bound_rule.py",
        ROOT / "scripts/build_s4g75_ngc4088_epsilon_cross_input_review_packet.py",
        ROOT / "scripts/build_s4g75_ngc4088_bi_coefficient_rule_gate.py",
        ROOT / "scripts/build_s4g75_ngc4088_epsilon_cross_bound_expression_shell.py",
        ROOT / "scripts/build_s4g75_ngc4088_epsilon_cross_locality_bound_rule.py",
        ROOT / "scripts/build_s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit.py",
        ROOT / "scripts/build_s4g75_ngc4088_readout_promotion_gate.py",
        ROOT / "scripts/build_s4g75_ngc2683_flare_profile_mapping_gate.py",
        ROOT / "scripts/run_s4g75_ngc2683_profile_aware_kernel_preflight.py",
        ROOT / "scripts/run_s4g75_ngc2683_hr_profile_kernel_prototype.py",
        ROOT / "scripts/run_s4g75_ngc2683_flare_closure_source_prototype.py",
        ROOT / "scripts/audit_s4g75_ngc2683_closure_source_sensitivity.py",
        ROOT / "scripts/build_s4g75_closure_source_generalization_gate.py",
        ROOT / "scripts/build_mixed_readout_source_selection_rule.py",
        ROOT / "scripts/build_ngc4013_expdisk_wvo_formula_freeze_gate.py",
        ROOT / "scripts/run_ngc4013_expdisk_wvo_frozen_protocol_audit.py",
        ROOT / "scripts/build_ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_gate.py",
        ROOT / "scripts/build_mixed_readout_population_validation_gate.py",
        ROOT / "scripts/build_mixed_readout_candidate_acquisition_queue.py",
        ROOT / "scripts/build_ngc4183_mixed_overlay_source_audit.py",
        ROOT / "scripts/build_ngc4183_mixed_overlay_observable_sheet.py",
        ROOT / "scripts/build_ngc4183_projection_outer_warp_label_gate.py",
        ROOT / "scripts/build_ngc4183_projection_outer_warp_formula_derivation.py",
        ROOT / "scripts/build_ngc4183_projection_gamma_coefficient_gate.py",
        ROOT / "scripts/build_ngc4183_tilted_ring_orientation_profile_extraction.py",
        ROOT / "scripts/build_ngc4183_projection_gamma_upper_bound_gate.py",
        ROOT / "scripts/build_ngc4183_preendpoint_decision_synthesis.py",
        ROOT / "scripts/build_ngc4183_weak_projection_control_preflight.py",
        ROOT / "scripts/build_ngc4183_tilted_ring_independent_review_packet.py",
        ROOT / "scripts/build_ngc4183_tilted_ring_review_handoff.py",
        ROOT / "scripts/build_ngc4183_codex_internal_review_response.py",
        ROOT / "scripts/build_ngc4183_tilted_ring_review_response_intake.py",
        ROOT / "scripts/build_ngc4183_visual_review_readiness_gate.py",
        ROOT / "scripts/build_ngc4183_null_control_freeze_readiness_gate.py",
        ROOT / "scripts/build_ngc4183_null_control_formula_freeze_gate.py",
        ROOT / "scripts/build_ngc4183_accepted_null_control_gate.py",
        ROOT / "scripts/build_ngc4183_control_promotion_roadmap.py",
        ROOT / "scripts/run_ngc4183_weak_projection_null_control_scoring_gate.py",
        ROOT / "scripts/run_ngc4183_weak_projection_null_control_accepted_endpoint.py",
        ROOT / "scripts/build_ngc4183_control_status_dashboard.py",
        ROOT / "scripts/build_ngc5907_expdisk_projection_mixed_formula_freeze_gate.py",
        ROOT / "scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py",
        ROOT / "scripts/build_ngc7331_fractional_warp_onset_source_gate.py",
        ROOT / "scripts/build_ngc7331_fractional_onset_v2_replay_freeze_gate.py",
        ROOT / "scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.py",
        ROOT / "scripts/run_mixed_readout_population_endpoint.py",
        ROOT / "scripts/run_mixed_readout_population_control_audit.py",
        ROOT / "scripts/run_mixed_readout_replay_holdout_endpoint.py",
        ROOT / "scripts/build_mixed_kernel_observable_separation_gate.py",
        ROOT / "scripts/build_mixed_kernel_sharpening_preflight.py",
        ROOT / "scripts/build_mixed_kernel_sharpened_replay_freeze.py",
        ROOT / "scripts/run_mixed_kernel_sharpened_replay_holdout_endpoint.py",
        ROOT / "scripts/build_ngc5907_expdisk_projection_mixed_accepted_endpoint_gate.py",
        ROOT / "scripts/run_ngc5907_expdisk_projection_mixed_accepted_endpoint.py",
        ROOT / "scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_gate.py",
        ROOT / "scripts/run_ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint.py",
        ROOT / "scripts/build_mixed_readout_population_expansion_gate.py",
        ROOT / "scripts/build_ngc4088_mixed_formula_freeze_blocker_resolution_plan.py",
        ROOT / "scripts/build_ngc4088_independent_xw_digitization_review_packet.py",
        ROOT / "scripts/build_ngc4088_b1_frozen_image_repeat_attempt.py",
        ROOT / "scripts/build_ngc4088_b1_source_native_radial_calibration_packet.py",
        ROOT / "scripts/build_ngc4088_b1_original_hi_data_acquisition_audit.py",
        ROOT / "scripts/build_ngc4088_b1_whisp_overview_extraction_review_packet.py",
        ROOT / "scripts/build_ngc4088_b1_whisp_overview_frozen_extraction_attempt.py",
        ROOT / "scripts/build_ngc4088_b1_whisp_promotion_review.py",
        ROOT / "scripts/build_ngc4088_b2_physical_normalization_derivation_synthesis.py",
        ROOT / "scripts/build_ngc4088_b2_source_load_closure_functional_gate.py",
        ROOT / "scripts/build_ngc4088_b2_frozen_asymptotic_carrier_theorem_gate.py",
        ROOT / "scripts/build_ngc4088_b2_population_transfer_preflight_gate.py",
        ROOT / "scripts/build_ngc4088_b2_exact_transfer_candidate_manifest.py",
        ROOT / "scripts/build_ngc7331_b2_exact_transfer_upgrade_gate.py",
        ROOT / "scripts/build_ngc7331_b2_exact_transfer_source_packet.py",
        ROOT / "scripts/build_ngc7331_b2_exact_transfer_source_evidence_review.py",
        ROOT / "scripts/acquire_ngc7331_things_hi_products.py",
        ROOT / "scripts/build_ngc7331_things_hi_product_audit.py",
        ROOT / "scripts/build_ngc7331_b2_hi_warp_acquisition_route.py",
        ROOT / "scripts/build_ngc7331_things_qwarp_measurement_worksheet.py",
        ROOT / "scripts/build_ngc7331_things_qwarp_first_pass_measurement.py",
        ROOT / "scripts/build_ngc7331_things_qwarp_measurement_sensitivity_audit.py",
        ROOT / "scripts/build_ngc7331_things_mom1_sign_cross_review.py",
        ROOT / "scripts/build_ngc7331_qwarp_observable_choice_review_gate.py",
        ROOT / "scripts/build_ngc7331_qwarp_observable_choice_review_packet.py",
        ROOT / "scripts/build_ngc7331_qwarp_source_only_review_response.py",
        ROOT / "scripts/run_ngc7331_qwarp_observable_choice_review_intake.py",
        ROOT / "scripts/build_ngc7331_b2_exact_transfer_formula_freeze_gate.py",
        ROOT / "scripts/run_ngc7331_b2_exact_transfer_interval_control_audit.py",
        ROOT / "scripts/build_ngc4088_b2_source_load_origin_derivation_gate.py",
        ROOT / "scripts/build_ngc4088_b2_closure_asymptotic_conditional_derivation_gate.py",
        ROOT / "scripts/build_ngc4088_b3_scale_uniqueness_resolution_synthesis.py",
        ROOT / "scripts/build_ngc4088_warp_history_formula_freeze_gate.py",
        ROOT / "scripts/build_ngc4088_formula_freeze_readiness_dashboard.py",
        ROOT / "scripts/build_ngc4088_warp_history_accepted_endpoint_gate.py",
        ROOT / "scripts/run_ngc4088_warp_history_accepted_endpoint.py",
        ROOT / "scripts/build_four_case_endpoint_status_summary.py",
        ROOT / "scripts/build_four_case_caveat_reduction_audit.py",
        ROOT / "scripts/build_ngc4013_retrospective_caveat_closure_gate.py",
        ROOT / "scripts/build_ngc4013_predeclared_replay_holdout_gate.py",
        ROOT / "scripts/build_ngc4088_remaining_caveat_action_gate.py",
        ROOT / "scripts/build_remaining_caveat_closure_roadmap.py",
        ROOT / "scripts/run_ngc7331_v2_v3_replay_holdout_endpoint.py",
        ROOT / "scripts/build_arxiv_source.py",
        ROOT / "scripts/reproduce.py",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == []


def test_manuscript_contains_forward_gate_and_claim_boundaries():
    source = (SOURCE / "main.tex").read_text(encoding="utf-8")
    assert "MORPHOLOGY-MATCHED-FORWARD-READOUT-GATE" in source
    assert "K_{\\rm obs}" in source
    assert "K_{\\rm readout}" in source
    assert "The equality $K_{\\rm obs}=K_{\\rm readout}$ is allowed but not assumed" in source
    assert "formula shell is selected as $\\mathcal{F}_{K_{\\rm readout}}$, not automatically as $\\mathcal{F}_{K_{\\rm obs}}$" in source
    assert "Paper 3 $S_\\tau$ diagnostic is useful but partly inverse" in source
    assert "\\Delta_{\\rm matched}" in source
    assert "This paper does not claim" in source
    assert "that Tau Core is proven" in source
    assert "that the morphology-matched gate has already won on real SPARC endpoints" in source
    assert "general residual-blind mixed source-selection rule" in source
    assert "SOURCE\\_SUPPORTED\\_MIXED\\_HYPOTHESIS\\_FORMULA\\_FREEZE\\_BLOCKED" in source
    assert "mixed carrier-plus-overlay formula must be frozen" in source
    assert "MIXED\\_FORMULA\\_FREEZE\\_READY\\_NOT\\_RETROACTIVE\\_ENDPOINT" in source
    assert "prospective mixed-readout protocol" in source
    assert "FROZEN\\_PROTOCOL\\_SCORE\\_RECORDED\\_NOT\\_RETROACTIVE\\_ENDPOINT" in source
    assert "disciplined intermediate result" in source
    assert "MIXED\\_POPULATION\\_VALIDATION\\_READY" in source
    assert "mixed-readout candidate acquisition queue" in source
    assert "MIXED\\_CANDIDATE\\_QUEUE\\_CREATED\\_NOT\\_ENDPOINT" in source
    assert "\\texttt{NGC5907} as the strongest fresh formula-freeze candidate" in source
    assert "previous\\_projection\\_endpoint\\_used\\_as\\_mixed\\_evidence=False" in source
    assert "MIXED\\_FORMULA\\_FREEZE\\_READY\\_PRIOR\\_TO\\_MIXED\\_SCORING" in source
    assert "previous\\_projection\\_endpoint\\_used\\_as\\_mixed\\_evidence=False" in source
    assert "three frozen prospective mixed protocols" in source
    assert "CAVEATED\\_MIXED\\_FORMULA\\_FREEZE\\_READY\\_PRIOR\\_TO\\_MIXED\\_SCORING" in source
    assert "projected HWHM/\\(R_s\\simeq0.0996\\)" in source
    assert "R_{\\rm onset}\\simeq0.5R_{\\rm Ho}" in source
    assert "R_{\\rm onset}\\simeq14.43\\,{\\rm kpc}" in source
    assert "replay/holdout-only V2 window" in source
    assert "NGC7331\\_FRACTIONAL\\_ONSET\\_V2\\_REPLAY\\_FREEZE\\_V1" in source
    assert "V2\\_REPLAY\\_PROTOCOL\\_READY\\_NOT\\_SCORED" in source
    assert "MIXED\\_POPULATION\\_ENDPOINT\\_PRELIMINARY\\_CONTROL\\_RESULT" in source
    assert "mean RMSE of the mixed readout is \\(16.41\\,{\\rm km\\,s^{-1}}\\)" in source
    assert "not yet a population-validation claim" in source
    assert "PASSED\\_3CASE\\_WRONG\\_LABEL\\_AND\\_SHUFFLED\\_CONTROL" in source
    assert "the wrong-label mean is \\(17.29\\,{\\rm km\\,s^{-1}}\\)" in source
    assert "best shuffled assignment at \\(16.71\\,{\\rm km\\,s^{-1}}\\)" in source
    assert "ACCEPTED\\_MIXED\\_ENDPOINT\\_FREEZE\\_READY" in source
    assert "ACCEPTED\\_MIXED\\_ENDPOINT\\_PRELIMINARY\\_CONTROL\\_RESULT" in source
    assert "accepted mixed readout has RMSE \\(16.37\\,{\\rm km\\,s^{-1}}\\)" in source
    assert "prior \\texttt{NGC5907} projection endpoint is explicitly not used as mixed-readout evidence" in source
    assert "MIXED\\_ACCEPTED\\_ENDPOINT\\_BLOCKED\\_RETROACTIVE\\_PROTOCOL\\_READY" in source
    assert "frozen mixed protocol has RMSE \\(10.61\\,{\\rm km\\,s^{-1}}\\)" in source
    assert "current \\texttt{NGC4013} mixed score remains a retrospective frozen-reference row" in source
    assert "NGC4013\\_RETROSPECTIVE\\_CAVEAT\\_CLOSURE\\_PATH\\_FORMALIZED\\_NOT\\_CLOSED" in source
    assert "no exact non-\\texttt{NGC4013} analogue" in source
    assert "operational rather than vague" in source
    assert "predeclared replay/holdout lane or by a future source-selected analogue" in source
    assert "NGC4013\\_PREDECLARED\\_REPLAY\\_HOLDOUT\\_GATE\\_BUILT\\_ENDPOINT\\_STILL\\_BLOCKED" in source
    assert "same-curve replay" in source
    assert "existing score is quarantined" in source
    assert (
        "REMAINING\\_CAVEAT\\_CLOSURE\\_ROADMAP\\_UPDATED\\_AFTER\\_NGC4088\\_ACTION\\_GATE\\_NOT\\_ENDPOINT"
        in source
    )
    assert "no route remains replay-ready without new source acquisition" in source
    assert "one replay path has been completed without updating the accepted V1 endpoint" in source
    assert "one predeclared replay gate has been built without endpoint permission" in source
    assert "one remaining-caveat action gate has been built" in source
    assert "next recommended gate is \\path{B2\\_CLOSURE\\_FUNCTIONAL" in source
    assert "NGC4088\\_REMAINING\\_CAVEAT\\_ACTION\\_GATE\\_BUILT\\_NOT\\_ENDPOINT" in source
    assert "direct H I provenance upgrade is useful but optional" in source
    assert "The next scientific action is therefore B2" in source
    assert "NGC7331\\_V2\\_V3\\_REPLAY\\_HOLDOUT\\_PRELIMINARY\\_CONTROL\\_RESULT" in source
    assert "V3 source-sharpened replay row improves to \\(22.13\\,{\\rm km\\,s^{-1}}\\)" in source
    assert "wrong sharpened projection control at \\(22.91\\,{\\rm km\\,s^{-1}}\\)" in source
    assert "not a retroactive update of the already accepted V1 endpoint" in source
    assert "CAVEATED\\_ACCEPTED\\_MIXED\\_ENDPOINT\\_FREEZE\\_READY" in source
    assert "CAVEATED\\_ACCEPTED\\_MIXED\\_ENDPOINT\\_PRELIMINARY\\_CONTROL\\_RESULT" in source
    assert "caveated accepted mixed readout has RMSE \\(22.26\\,{\\rm km\\,s^{-1}}\\)" in source
    assert "V2 replay freeze manifest gives a candidate inner window near \\(14.43\\,{\\rm kpc}\\)" in source
    assert "broad source-scale outer window from \\(R_s\\) to \\(R_{\\rm HI}\\)" in source
    assert "NEXT\\_MIXED\\_CASE\\_IDENTIFIED\\_FORMULA\\_FREEZE\\_BLOCKED" in source
    assert "closest next candidate is \\texttt{NGC4088}" in source
    assert "multiple residual-blind candidate scales" in source
    assert "NGC4088\\_FORMULA\\_FREEZE\\_BLOCKER\\_RESOLUTION\\_PLAN\\_CREATED" in source
    assert "three local formula-freeze blockers" in source
    assert "INDEPENDENT\\_XW\\_REVIEW\\_PACKET\\_READY\\_RESPONSE\\_PENDING" in source
    assert "B2\\_FORMULA\\_CONDITIONAL\\_DERIVATION\\_SYNTHESIZED\\_LAW\\_STILL\\_OPEN" in source
    assert "B3\\_CONDITIONAL\\_UNIQUE\\_SCALE\\_SELECTED\\_LAW\\_LEVEL\\_UNIQUENESS\\_OPEN" in source
    assert "NGC4088\\_FORMULA\\_FREEZE\\_READINESS\\_DASHBOARD\\_CREATED" in source
    assert "FROZEN\\_IMAGE\\_REPEAT\\_ATTEMPT\\_COMPLETE\\_INCONCLUSIVE" in source
    assert "RADIAL\\_CALIBRATION\\_NOT\\_ACCEPTED" in source
    assert "RC3\\_ORIGINAL\\_CHANNEL\\_MAP\\_DATA\\_ROUTE\\_AUDITED\\_NO\\_DIRECT\\_PRODUCT\\_CACHED" in source
    assert "WHISP\\_OVERVIEW\\_EXTRACTION\\_PACKET\\_READY\\_RESPONSE\\_PENDING" in source
    assert "FROZEN\\_WHISP\\_OVERVIEW\\_EXTRACTION\\_ATTEMPT\\_COMPLETE\\_AGREES\\_WITH\\_FIRST\\_PASS" in source
    assert "B1\\_CAVEATED\\_XW\\_ACCEPTED\\_FOR\\_FORMULA\\_FREEZE\\_NOT\\_ENDPOINT" in source
    assert "NGC4088\\_WARP\\_HISTORY\\_FORMULA\\_FREEZE\\_READY\\_LAW\\_CAVEATED\\_NOT\\_SCORE" in source
    assert "8795.111752" in source
    assert "3/3" in source
    assert "FORMULA\\_FREEZE\\_READY\\_ENDPOINT\\_GATE\\_REQUIRED" in source
    assert "CAVEATED\\_ACCEPTED\\_ENDPOINT\\_FREEZE\\_READY" in source
    assert "CAVEATED\\_ACCEPTED\\_ENDPOINT\\_PRELIMINARY\\_CONTROL\\_RESULT" in source
    assert "RMSE \\(11.62\\,{\\rm km\\,s^{-1}}\\)" in source
    assert "wrong-family mean is \\(41.86\\,{\\rm km\\,s^{-1}}\\)" in source
    assert "FOUR\\_INSPECTED\\_CASES\\_HETEROGENEOUS\\_PRELIMINARY\\_EVIDENCE" in source
    assert "\\texttt{NGC4013}, \\texttt{NGC5907}, and caveated \\texttt{NGC7331}" in source
    assert "additional caveated single-galaxy warp/history endpoint" in source
    assert "beats the best local baseline in \\(4/4\\) rows" in source
    assert "Three rows now have accepted single-galaxy endpoint status" in source
    assert "not empirical validation of the theory" in source
    assert "closure path formalized but not closed" in source
    assert "SOURCE\\_KERNEL\\_OBSERVABLE\\_SEPARATION\\_PASS" in source
    assert "does not read" in source
    assert "observed velocities, residuals, RMSE ranks" in source
    assert "At this stage the source observables" in source
    assert "do separate the lanes" in source
    assert "the bottleneck is the source-to-kernel map" in source
    assert "K_{\\rm proj}^{\\rm sharp}(u)" in source
    assert "K_{\\rm vow}^{\\rm sharp}(u)" in source
    assert "SOURCE\\_KERNEL\\_SHARPENING\\_PREFLIGHT\\_READY\\_NOT\\_ENDPOINT" in source
    assert "normalized cross-similarity of the two current kernel shapes from \\(0.991\\)" in source
    assert "a formula-freeze obligation, not a fit" in source
    assert "SHARPENED\\_REPLAY\\_FREEZE\\_READY\\_NOT\\_SCORED" in source
    assert "SHARPENED\\_REPLAY\\_HOLDOUT\\_2CASE\\_PRELIMINARY\\_CONTROL\\_RESULT" in source
    assert "mean sharpened mixed RMSE is" in source
    assert "\\(19.224\\,{\\rm km\\,s^{-1}}\\)" in source
    assert "beat all wrong-label controls in" in source
    assert "\\(2/2\\) cases" in source
    assert "matched diagonal is ranked first" in source
    assert "does not establish population validation" in source
    assert "it repairs the" in source
    assert "specific failure mode exposed by the unsharpened replay/holdout audit" in source
    assert "FOUR\\_CASE\\_CAVEAT\\_REDUCTION\\_AUDIT\\_COMPLETE" in source
    assert "three of" in source
    assert "the four inspected-case caveats are reduced" in source
    assert "NGC4013's retrospective caveat is only isolated" in source
    assert "No endpoint status is changed by this audit" in source
    assert "Available-data Tau-proxy preflight" in source
    assert "beats the wrong-family mean in 0.568" in source
    assert "p\\simeq0.264" in source
    assert "beats the wrong-shell mean in 0.500" in source
    assert "p\\simeq0.479" in source
    assert "beats the wrong-formula mean in 0.886" in source
    assert "p\\simeq0.002" in source
    assert "confidence $\\geq0.75$" in source
    assert "family-to-global shrinkage policy" in source
    assert "family weight 0.4--0.5" in source
    assert "train-selected shrinkage diagnostic" in source
    assert "family weight 0.40" in source
    assert "family-breakdown diagnostic" in source
    assert "scale-tail spiral and thick/flared families" in source
    assert "observable-quality diagnostic" in source
    assert "morphology-observable extraction as a required predeclared gate" in source
    assert "predeclared quality-gate diagnostic" in source
    assert "candidate observability rules" in source
    assert "shuffled-label null reveals the tradeoff" in source
    assert "prioritizes observability-clean baseline competitiveness" in source
    assert "endpoint decision matrix" in source
    assert "no-low-inclination gate" in source
    assert "predeclared endpoint protocol sheet" in source
    assert "post-hoc gate choice" in source
    assert "preparation-ready, not discovery-ready" in source
    assert "morphology-observable intake schema" in source
    assert "endpoint-selected radii" in source
    assert "A gap audit compares the proxy manifest" in source
    assert "coverage-rich but acceptance-limited" in source
    assert "morphology-observable source-upgrade plan" in source
    assert "P0 family-label, confidence, caveat, and provenance fields" in source
    assert "accepted-observable manifest template and validator" in source
    assert "intentionally endpoint-blocked" in source
    assert "accepted-manifest readiness gate" in source
    assert "BLOCKED\\_ACCEPTED\\_OBSERVABLES\\_MISSING" in source
    assert "frozen-endpoint launch guard" in source
    assert "LAUNCH\\_BLOCKED" in source
    assert "external morphology source registry" in source
    assert "S4G is the first morphology/decomposition source" in source
    assert "77 S4G crossmatches" in source
    assert "75 S4G/SPARC-derived disk-scale candidates" in source
    assert "partial accepted morphology-observable manifest" in source
    assert "75 S4G/SPARC-derived scale-radius observables" in source
    assert "all 175 rows endpoint-blocked" in source
    assert "13 exponential-disk rows" in source
    assert "next residual-blind morphology-label audit pool" in source
    assert "6 rows have strict \\texttt{D:expdisk} support" in source
    assert "7 rows remain caveated" in source
    assert "narrow dry-run" in source
    assert "beats TPG/v6 in 4/6 cases" in source
    assert "beats MOND in only 2/6 cases" in source
    assert "leave-one-galaxy-out all-13 policy beats TPG/v6 in 3/6 strict cases" in source
    assert "fixed multipliers 0.75, 1.0, and 1.25" in source
    assert "unlikely to be solved by a single radius rescaling alone" in source
    assert "rotation-inferred family matches the predeclared proxy family in about 0.354" in source
    assert "matches the external S4G-supported exponential-disk label in about 0.308" in source
    assert "not allowed to define the accepted Paper 8 morphology labels" in source
    assert "morphology-memory/history layer" in source
    assert "currently observed galaxy shape may be an insufficient proxy" in source
    assert "current proxy family and rotation-inferred family disagree in 113/175 rows" in source
    assert "9/13 S4G-supported exponential-disk rows do not infer the exponential-disk readout family" in source
    assert "not an accepted morphology label, not an endpoint score" in source
    assert "morphology inspection queue" in source
    assert "4 P0 and 18 P1 inspection targets" in source
    assert "\\texttt{NGC0300}, \\texttt{NGC6503}, \\texttt{NGC0100}, and \\texttt{NGC0247}" in source
    assert "not validation and not an accepted morphology manifest" in source
    assert "residual-blind inspection packets" in source
    assert "deep optical or infrared outer-disk profiles" in source
    assert "\\texttt{NGC0247} additionally requests bar-length and velocity-field support" in source
    assert "external imaging request manifest" in source
    assert "8.0 arcmin for \\texttt{NGC0100}" in source
    assert "29.745 arcmin for \\texttt{NGC0247}" in source
    assert "20.288 arcmin for \\texttt{NGC0300}" in source
    assert "10.030 arcmin for \\texttt{NGC6503}" in source
    assert "local HTML imaging-review dashboard" in source
    assert "offline launch page with per-galaxy source links" in source
    assert "does not embed a classification result or an accepted label" in source
    assert "SkyView for DSS2 Red, 2MASS-K, and WISE W1 availability" in source
    assert "All 12 P0 survey requests return at least one image candidate" in source
    assert "not temporary FITS URLs and not image classifications" in source
    assert "12 local PNG preview panels" in source
    assert "300 by 300 pixels" in source
    assert "no automated image classification, accepted label, or endpoint score is emitted" in source
    assert "residual-blind visual review template" in source
    assert "morphological memory/history proxy judgment" in source
    assert "all review fields remain unfilled placeholders" in source
    assert "completion gate" in source
    assert "BLOCKED\\_VISUAL\\_REVIEW\\_PENDING" in source
    assert "all 60 reviewer fields are still placeholders" in source
    assert "visual review handoff" in source
    assert "READY_FOR_RESIDUAL_BLIND_HUMAN_REVIEW" in source
    assert "does not promote labels or compute endpoint scores" in source
    assert "Codex/source-reviewed P0 response" in source
    assert "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT" in source
    assert "P0 Codex-source-reviewed label manifest" in source
    assert "readout-relevant morphology proxy" in source
    assert "projected 4D morphology handles" in source
    assert "response-to-manifest promotion gate" in source
    assert "P0_CODEX_SOURCE_REVIEW_LABELS_CREATED_NOT_ENDPOINT" in source
    assert "consolidated P0 review-pipeline status dashboard" in source
    assert "S4G, NED/NED-D, DustPedia, HI surveys, and PHANGS" in source
    assert "TO_BE_ACQUIRED_RESIDUAL_BLIND" in source
    assert "DustPedia direct matches are found for \\texttt{NGC0300} only" in source
    assert "source-assisted review response draft" in source
    assert "requested source-family availability" in source
    assert "P0_CODEX_SOURCE_REVIEW_LABELS_READY_FULL_ENDPOINT_BLOCKED" in source
    assert "full endpoint labels and endpoint scoring remain disabled" in source
    assert "baseline success is not discarded" in source
    assert "quiet baryonic-readout controls" in source
    assert "scalarized radial-readout controls" in source
    assert "closure-like or memory-integrated readout controls" in source
    assert "predeclared readout regimes rather than to post-hoc model choice" in source
    assert "conditional limiting-regime interpretation" in source
    assert "g_{\\rm eff}\\to g_{\\rm Newt}" in source
    assert "MOND/RAR-like solved response can be a special effective limit" in source
    assert "TPG-like formula can be the natural effective readout" in source
    assert "RMOND-facing" in source
    assert "not yet a derived relativistic MOND theory" in source
    assert "formula-derived when $\\delta g_{\\rm morph}\\to0$" in source
    assert "\\sigma_{\\rm morph}\\sim {A\\over r^2}" in source
    assert "\\delta\\Phi\\sim A\\log r" in source
    assert "formula-conditional" in source
    assert "A^2 = G M_b g_*" in source
    assert "g_*:=\\lambda_*\\ell_*" in source
    assert "not a numerical $a_0$ validation" in source
    assert "readout-form-only" in source
    assert "conditional baseline-selection theorem" in source
    assert "Let $R_g$ be a residual-blind readout-regime label" in source
    assert "If $R_g$ satisfies the quiet baryonic-readout assumptions" in source
    assert "If $R_g$ satisfies the scalarized radial low-acceleration assumptions" in source
    assert "If $R_g$ satisfies the smooth closure/readout source-tail assumptions" in source
    assert "if several regime predicates hold" in source
    assert "if none holds, the current bridge has not explained that baseline success" in source
    assert "morphology-information-gain test" in source
    assert "coarse $K_{\\rm obs}$ label" in source
    assert "source-reviewed $K_{\\rm readout}$" in source
    assert "readout-state vector" in source
    assert "source-native scales and amplitudes" in source
    assert "population-level trend should improve matched-vs-wrong rank" in source
    assert "rotation residuals are used to choose labels, weights, scales, or gates" in source
    assert "L0 &: K_{\\rm obs}" in source
    assert "population-level improvement curve" in source
    assert "first executable version of this test" in source
    assert "175 SPARC rows" in source
    assert "75 S4G scale-radius candidates" in source
    assert "31 DustPedia source-candidate matches" in source
    assert "171 SPARC HI-ready galaxies" in source
    assert "two PHANGS public-sample matches" in source
    assert "172 L2 tail candidates" in source
    assert "48 L2 compact candidates" in source
    assert "19 L2 bar candidates" in source
    assert "residual-blind candidate readout weights for 174 of 175 galaxies" in source
    assert "not accepted Tau-side readout-state weights" in source
    assert "beats the old L2 mixture proxy in 0.409" in source
    assert "median intake-minus-old-L2 RMSE $+0.847$" in source
    assert "blocks endpoint use for all 175 galaxies" in source
    assert "theory-conditional residual-blind Tau-side source-normalization candidate" in source
    assert "orientation signs as theory-conditional bridge derivations" in source
    assert "conservative Tau-side readout-admission product" in source
    assert "residual-blind evidence measure $e_{gK}=E_\\tau(g,K)$" in source
    assert "not a claim that the conservative three-status evidence geometry is the unique final Tau-side evidence law" in source
    assert "median proxy value is $E_\\tau=0.354025$" in source
    assert "median $E_\\tau$-minus-old-L2 RMSE is $-0.236$" in source
    assert "accepted source-native observables" in source
    assert "source-normalized L2 preflight beats the old L2 intake endpoint in 0.568" in source
    assert "median source-normalized-minus-old-L2 RMSE $-0.272$" in source
    assert "proxy-gate blocker is resolved for all 175 rows" in source
    assert "source-native orientation-promotion gate now promotes three of four family orientations" in source
    assert "67 of 175 rows are orientation-ready" in source
    assert "108 remain orientation-blocked" in source
    assert "47 projection-blocked rows" in source
    assert "19 memory/history-blocked rows" in source
    assert "one memory/projection-ready candidate" in source
    assert "lane-expansion audit" in source
    assert "66 additional galaxies are caution/proxy-supported" in source
    assert "67 of 175 galaxies are analysis-includable" in source
    assert "caution lane is explicitly not accepted evidence" in source
    assert "source-native hard-family formula keeps a morphology-specific signal" in source
    assert "beating the wrong-family mean in 0.8125" in source
    assert "beating TPG/v6 in 0.3750 and MOND in 0.3125" in source
    assert "Removing proxy support gives 0.545" in source
    assert "All-positive orientation signs reduce the old-L2 win fraction to 0.477" in source
    assert "remaining freeze blockers are the thick/flared orientation source layer plus accepted per-galaxy evidence" in source
    assert "zero MUSE-ready velocity-field matches" in source
    assert "not a monotonicity proof" in source
    forbidden_phrases = [
        "We prove Tau Core",
        "This paper demonstrates Tau Core has beaten MOND/RAR",
        "MOND and RAR are superseded",
        "we derive a universal galaxy law",
    ]
    for phrase in forbidden_phrases:
        assert phrase not in source


def test_bridge_central_doc_records_obs_vs_readout_layer():
    bridge = (ROOT / "docs" / "tau_core_gravity_bridge_central.md").read_text(
        encoding="utf-8"
    )
    assert "Observed 4D morphology handles are not fundamental Tau-side classes" in bridge
    assert "K_obs" in bridge
    assert "K_readout" in bridge
    assert "F = F_{K_readout}" in bridge
    assert "not automatically" in bridge
    assert "morphology-memory or history proxy layer" in bridge
    assert "endpoint residual gain" in bridge
    assert "best-fit Tau Core readout family" in bridge
    assert "NGC0247" in bridge
    assert "Baseline Success As Readout-Regime Control" in bridge
    assert "quiet / regular baryonic-readout regime" in bridge
    assert "scalarized radial low-acceleration or diffuse-disk regime" in bridge
    assert "smooth closure-like or memory-integrated readout regime" in bridge
    assert "Baseline winners may therefore become controls" in bridge
    assert "Baselines As Conditional Tau Core Limits" in bridge
    assert "Newtonian limit" in bridge
    assert "MOND/RAR-like scalarized limit" in bridge
    assert "TPG-like closure limit" in bridge
    assert "RMOND-facing metric limit" in bridge
    assert "not yet RMOND recovered" in bridge
    assert "Formula Status Imported From The Theory Bridge" in bridge
    assert "FORMULA-DERIVED" in bridge
    assert "FORMULA-CONDITIONAL" in bridge
    assert "READOUT-FORM-ONLY" in bridge
    assert "sigma_morph ~ A/r^2" in bridge
    assert "delta Phi ~ A log r" in bridge
    assert "A^2 = G M_b g_*" in bridge
    assert "g_* := lambda_* ell_*" in bridge
    assert "numerical a0 value" in bridge
    assert "Conditional Baseline-Selection Theorem" in bridge
    assert "residual-blind readout-regime label" in bridge
    assert "quiet baryonic-readout regime" in bridge
    assert "scalarized radial low-acceleration regime" in bridge
    assert "smooth closure/readout source-tail regime" in bridge
    assert "gauge-safe metric-readout descent regime" in bridge
    assert "overlap/control case" in bridge
    assert "current bridge has not explained" in bridge
    assert "that baseline success" in bridge
    assert "Morphology Information Gain Test" in bridge
    assert "L0 coarse K_obs" in bridge
    assert "L1 source-reviewed K_readout" in bridge
    assert "L2 readout-state vector" in bridge
    assert "L3 source-native scales and normalization" in bridge
    assert "L4 enriched morphology/kinematic evidence" in bridge
    assert "matched-vs-wrong rank" in bridge
    assert "shuffled-label separation" in bridge
    assert "0.886 matched-vs-wrong preflight result" in bridge
    assert "run_morphology_information_gain_test.py" in bridge
    assert "SPARC rows: 175 acquired" in bridge
    assert "S4G scale-radius candidates: 75 acquired" in bridge
    assert "DustPedia full-sample source-candidate matches: 31" in bridge
    assert "HI full-sample SPARC-ready galaxies: 171" in bridge
    assert "PHANGS full-sample public-sample matches: 2" in bridge
    assert "MUSE-ready velocity-field candidates: 0" in bridge
    assert "L2 tail source candidates: 172" in bridge
    assert "L2 compact source candidates: 48" in bridge
    assert "L2 bar source candidates: 19" in bridge
    assert "Accepted readout-state vector components: 0 endpoint-ready" in bridge
    assert "build_l2_weight_intake_candidates.py" in bridge
    assert "Source-informative L2 weight candidates: 174/175" in bridge
    assert "not an accepted Tau-side readout-state vector" in bridge
    assert "run_l2_weight_intake_endpoint_preflight.py" in bridge
    assert "Beats old L2 mixture proxy:       0.409" in bridge
    assert "source-intake weights are closer to a" in bridge
    assert "dominant `K_thick_flared` intake subgroup improves" in bridge
    assert "audit_l2_weight_freeze_readiness.py" in bridge
    assert "build_source_native_orientation_promotion_gate.py" in bridge
    assert "build_memory_projection_acceptance_gate.py" in bridge
    assert "build_inclusion_lane_expansion_audit.py" in bridge
    assert "run_inclusion_lane_endpoint_analysis.py" in bridge
    assert "build_projection_scale_repair_audit.py" in bridge
    assert "audit_source_normalization_failure_modes_by_lane.py" in bridge
    assert "Endpoint-freeze allowed:                  0/175" in bridge
    assert "Proxy-gate blocker resolved by E_tau:     175/175" in bridge
    assert "Blocked by missing Tau-side normalization: 0/175" in bridge
    assert "Family orientations promoted:             3/4" in bridge
    assert "Family orientations blocked:              1/4" in bridge
    assert "Galaxies orientation-ready:               67/175" in bridge
    assert "Blocked by source-native orientation:     108/175" in bridge
    assert "Blocked by projection acceptance:         47/175" in bridge
    assert "Blocked by memory/history acceptance:     19/175" in bridge
    assert "Blocked by q_i/normalization acceptance:  1/175" in bridge
    assert "Formula-conditional normalization present: 175/175" in bridge
    assert "Strict-ready candidates:                  1/175" in bridge
    assert "Caution/proxy-supported rows:             66/175" in bridge
    assert "Analysis-includable strict+caution rows:  67/175" in bridge
    assert "Acquisition-required rows:                108/175" in bridge
    assert "Holdout strict+caution rows:              16/44" in bridge
    assert "Hard-family beats wrong on strict+caution: 0.8125" in bridge
    assert "Tau evidence L2 beats TPG/v6 there:        0.3750" in bridge
    assert "Tau evidence L2 beats MOND there:          0.3125" in bridge
    assert "Projection-caveat sub-lane rows:           14/44" in bridge
    assert "Hard-family beats wrong there:             0.7857" in bridge
    assert "Tau evidence L2 beats TPG/v6 there:        0.3571" in bridge
    assert "Tau evidence L2 beats MOND there:          0.2857" in bridge
    assert "weights remain candidates and the endpoint launch stays blocked" in bridge
    assert "larger analysis-includable set for sensitivity and acquisition planning" in bridge
    assert "baseline" in bridge
    assert "superiority does not" in bridge
    assert "projection/scale quality plus source-normalization" in bridge
    assert "No projection/scale repair required:                         71/175" in bridge
    assert "Needs vertical-geometry source evidence:                     34/175" in bridge
    assert "Needs inclination/projection review:                         26/175" in bridge
    assert "Needs distance/scale source support:                         30/175" in bridge
    assert "Repairable with existing scale source plus distance audit:   14/175" in bridge
    assert "normalization failure:                                        7/14" in bridge
    assert "residual-blind repair map" in bridge
    assert "run_tau_side_source_normalized_l2_endpoint.py" in bridge
    assert "Beats old L2 intake endpoint: 0.568" in bridge
    assert "Median minus old L2 RMSE:   -0.272" in bridge
    assert "audit_tau_side_source_normalization_sensitivity.py" in bridge
    assert "all-positive signs:      beats old L2 0.477" in bridge
    assert "all-negative signs:      beats old L2 0.432" in bridge
    assert "orientation structure is not cosmetic" in bridge
    assert "Mixed Readout Candidate Acquisition Queue" in bridge
    assert "MIXED_CANDIDATE_QUEUE_CREATED_NOT_ENDPOINT" in bridge
    assert "Next recommended mixed freeze case:" in bridge
    assert "NGC5907" in bridge
    assert "projection endpoint cannot be reused as" in bridge
    assert "NGC5907 mixed formula-freeze" in bridge
    assert "MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING" in bridge
    assert "Prospective mixed protocols ready: 3/3" in bridge
    assert "Prior projection endpoint used as mixed evidence: false" in bridge
    assert "NGC7331 caveated mixed formula-freeze" in bridge
    assert "CAVEATED_MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING" in bridge
    assert "Window:  broad source-scale outer window R_s -> R_HI" in bridge
    assert "FRACTIONAL_WARP_ONSET_SOURCE_READY_REPLAY_REQUIRED" in bridge
    assert "candidate V2 window: 14.431691 -> 27.01 kpc" in bridge
    assert "V2_REPLAY_PROTOCOL_READY_NOT_SCORED" in bridge
    assert "formula_id = NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1" in bridge
    assert "Mixed-population endpoint run" in bridge
    assert "MIXED_POPULATION_ENDPOINT_PRELIMINARY_CONTROL_RESULT" in bridge
    assert "Mixed beats Newton/TPG/MOND/carrier:  3/3, 3/3, 3/3, 3/3" in bridge
    assert "wrong-family / shuffled-label mixed-population control" in bridge
    assert "PASSED_3CASE_WRONG_LABEL_AND_SHUFFLED_CONTROL" in bridge
    assert "Matched diagonal permutation rank:     1/6" in bridge
    assert "source-matched diagonal is the best" in bridge
    assert "Strict replay/holdout mixed endpoint" in bridge
    assert "MIXED_REPLAY_HOLDOUT_2CASE_PRELIMINARY_RESULT" in bridge
    assert "Matched permutation rank:               2/2" in bridge
    assert "Matched minus best shuffled:            +0.044 km/s" in bridge
    assert "Mixed kernel observable separation gate" in bridge
    assert "SOURCE_KERNEL_OBSERVABLE_SEPARATION_PASS" in bridge
    assert "Diagnostic status:                     DIAGNOSTIC_ONLY_NOT_ENDPOINT" in bridge
    assert "Minimum source-similarity margin:       0.501" in bridge
    assert "source-observable level, the two fresh lanes do separate" in bridge
    assert "current source-to-kernel map" in bridge
    assert "Mixed kernel sharpening preflight" in bridge
    assert "SOURCE_KERNEL_SHARPENING_PREFLIGHT_READY_NOT_ENDPOINT" in bridge
    assert "Current kernel cross-similarity:           0.991" in bridge
    assert "Source-sharpened kernel cross-similarity:  0.644" in bridge
    assert "K_proj_sharp(u)" in bridge
    assert "K_vow_sharp(u)" in bridge
    assert "not a fit improvement and not an endpoint score" in bridge
    assert "Four-case caveat reduction audit" in bridge
    assert "FOUR_CASE_CAVEAT_REDUCTION_AUDIT_COMPLETE" in bridge
    assert "Caveats reduced:                       3" in bridge
    assert "Caveats isolated but not removed:      1" in bridge
    assert "NGC4013: retrospective caveat isolated, not removed" in bridge
    assert "NGC7331: broad-window caveat reduced for V2/V3 replay" in bridge
    assert "NGC4013 retrospective-caveat closure gate" in bridge
    assert "NGC4013_RETROSPECTIVE_CAVEAT_CLOSURE_PATH_FORMALIZED_NOT_CLOSED" in bridge
    assert "exact non-NGC4013 analogue ready count:   0" in bridge
    assert "nearest analogue candidate:               NGC4088" in bridge
    assert "endpoint scores allowed:                  false" in bridge
    assert "reduces the NGC4013 caveat by making it" in bridge
    assert "operational, not by removing it" in bridge
    assert "NGC4013 predeclared replay/holdout gate" in bridge
    assert "NGC4013_PREDECLARED_REPLAY_HOLDOUT_GATE_BUILT_ENDPOINT_STILL_BLOCKED" in bridge
    assert "same-curve replay allowed:             false" in bridge
    assert "same-curve replay is not an" in bridge
    assert "Remaining caveat closure roadmap" in bridge
    assert "NGC4088 remaining-caveat action gate" in bridge
    assert "NGC4088_REMAINING_CAVEAT_ACTION_GATE_BUILT_NOT_ENDPOINT" in bridge
    assert "primary theory action is B2" in bridge
    assert "REMAINING_CAVEAT_CLOSURE_ROADMAP_UPDATED_AFTER_NGC4088_ACTION_GATE_NOT_ENDPOINT" in bridge
    assert "Replay-ready without new source:      0" in bridge
    assert "Replay completed without V1 update:   1" in bridge
    assert "Predeclared replay gates built:        1" in bridge
    assert "Remaining caveat action gates built:   1" in bridge
    assert (
        "Next recommended gate:                "
        "B2_SOURCE_LOAD_ORIGIN_AND_ASYMPTOTIC_CARRIER_DERIVATION_FOR_NGC4088"
    ) in bridge
    assert "NGC7331 V2/V3" in bridge
    assert "NGC7331 V2/V3 replay/holdout endpoint" in bridge
    assert "NGC7331_V2_V3_REPLAY_HOLDOUT_PRELIMINARY_CONTROL_RESULT" in bridge
    assert "V3 source-sharpened replay RMSE:       22.130849 km/s" in bridge
    assert "Wrong projection-sharpened RMSE:       22.906398 km/s" in bridge
    assert "Current V1 endpoint updated:           false" in bridge
    assert "NGC5907 accepted mixed endpoint promotion" in bridge
    assert "ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT" in bridge
    assert "matched mixed RMSE = 16.372532 km/s" in bridge
    assert "previous projection endpoint used as mixed evidence = false" in bridge
    assert "NGC4013 mixed accepted-endpoint blocker" in bridge
    assert "MIXED_ACCEPTED_ENDPOINT_BLOCKED_RETROACTIVE_PROTOCOL_READY" in bridge
    assert "frozen protocol RMSE = 10.614758 km/s" in bridge
    assert "endpoint scores allowed as accepted endpoint = false" in bridge
    assert "NGC7331 caveated accepted mixed endpoint promotion" in bridge
    assert "CAVEATED_ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT" in bridge
    assert "matched mixed RMSE = 22.255666 km/s" in bridge
    assert "outer-warp numeric onset available = false" in bridge
    assert "broad outer-window caveat attached = true" in bridge
    assert "fractional onset source gate = replay/holdout required" in bridge
    assert "candidate V2 onset = 14.431691 kpc" in bridge
    assert "V2 replay freeze status = V2_REPLAY_PROTOCOL_READY_NOT_SCORED" in bridge
    assert "Mixed-population expansion gate" in bridge
    assert "NEXT_MIXED_CASE_IDENTIFIED_FORMULA_FREEZE_BLOCKED" in bridge
    assert "NGC4088 warp/history formula-freeze gate" in bridge
    assert "NGC4088_WARP_HISTORY_FORMULA_FREEZE_READY_LAW_CAVEATED_NOT_SCORE" in bridge
    assert "lambda_w = 8795.111752 km^2/s^2" in bridge
    assert "resolved local blockers = 3 / 3" in bridge
    assert "NGC4088 caveated accepted endpoint gate and score" in bridge
    assert "CAVEATED_ACCEPTED_ENDPOINT_PRELIMINARY_CONTROL_RESULT" in bridge
    assert "matched warp/history RMSE = 11.619038 km/s" in bridge
    assert "matched rank among all inspected models = 1" in bridge
    assert "Four inspected endpoint/readout cases status" in bridge
    assert "FOUR_INSPECTED_CASES_HETEROGENEOUS_PRELIMINARY_EVIDENCE" in bridge
    assert "Accepted single-galaxy endpoints:        3" in bridge
    assert "Matched beats best local baseline:       4/4" in bridge
    assert "Matched beats inspected wrong families:  4/4" in bridge
    assert "readout-specificity evidence in four inspected" in bridge
    assert "Formula freeze allowed now:            false" in bridge


def test_derived_protocol_tables_exist_and_have_expected_content():
    registry = pd.read_csv(DATA / "morphology_family_registry.csv")
    schema = pd.read_csv(DATA / "forward_readout_gate_schema.csv")
    crosswalk = pd.read_csv(DATA / "paper3_candidate_control_crosswalk.csv")
    readiness = pd.read_csv(DATA / "paper8_readiness_table.csv")

    assert len(registry) == 7
    assert "K_scale_tail_spiral" in set(registry["family_id"])
    assert "velocity-field preferred" in set(registry["sparc_first_pass_status"])
    assert len(schema) == 6
    assert "shuffled-K null" in set(schema["gate_component"])
    assert "DDO126" in set(crosswalk["galaxy"])
    assert "DDO50" in set(crosswalk["galaxy"])
    real_endpoint = readiness.loc[
        readiness["item"] == "Real matched-vs-wrong family endpoint", "status"
    ].iloc[0]
    assert real_endpoint == "not_yet_run"


def test_foundation_audit_preserves_preparation_status():
    audit = pd.read_csv(DATA / "paper8_foundation_audit.csv")
    assert "paper3_inverse_to_forward_bridge" in set(audit["gate"])
    assert "empirical_endpoint_readiness" in set(audit["gate"])
    assert "formula_shell_dimensional_readiness" in set(audit["gate"])
    assert audit.loc[
        audit["gate"] == "paper3_inverse_to_forward_bridge", "status"
    ].iloc[0] == "PASS"
    assert audit.loc[
        audit["gate"] == "empirical_endpoint_readiness", "status"
    ].iloc[0] == "BLOCKED"
    assert audit.loc[
        audit["gate"] == "formula_shell_dimensional_readiness", "status"
    ].iloc[0] == "REVIEW"

    report = (ROOT / "reports" / "paper8_foundation_audit.md").read_text(encoding="utf-8")
    assert "not yet suitable for an empirical discovery claim" in report
    assert "residual-blind morphology-label manifest" in report


def test_mixed_readout_candidate_acquisition_queue_is_source_blind_and_not_endpoint():
    queue = pd.read_csv(DATA / "mixed_readout_candidate_acquisition_queue.csv")
    summary = pd.read_csv(DATA / "mixed_readout_candidate_acquisition_summary.csv").iloc[0]
    requirements = pd.read_csv(DATA / "mixed_readout_candidate_acquisition_requirements.csv")

    assert summary["queue_status"] == "MIXED_CANDIDATE_QUEUE_CREATED_NOT_ENDPOINT"
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual_in_selection"]) is False
    assert summary["next_recommended_case"] == "NGC5907"
    assert int(summary["additional_prospective_protocols_needed_after_reference"]) == 2

    assert "NGC4013" in set(queue["galaxy"])
    assert "NGC5907" in set(queue["galaxy"])
    assert "NGC7331" in set(queue["galaxy"])
    ngc4013 = queue.loc[queue["galaxy"].eq("NGC4013")].iloc[0]
    ngc5907 = queue.loc[queue["galaxy"].eq("NGC5907")].iloc[0]
    ngc7331 = queue.loc[queue["galaxy"].eq("NGC7331")].iloc[0]
    assert ngc4013["candidate_priority"] == "P0_REFERENCE_FROZEN_PROSPECTIVE_PROTOCOL"
    assert ngc5907["candidate_priority"] == "P0_FORMULA_FREEZE_CANDIDATE_REVIEW_REQUIRED"
    assert "fresh_mixed_freeze" in ngc5907["blocking_or_caution_notes"]
    assert ngc7331["candidate_priority"] == "P1_CAVEATED_VERTICAL_OVERLAY_CANDIDATE"
    assert queue["endpoint_scores_allowed"].eq(False).all()
    assert queue["uses_vobs_or_residual_in_selection"].eq(False).all()
    assert "vobs" in ";".join(requirements["forbidden_inputs"].astype(str))


def test_ngc5907_mixed_formula_freeze_is_ready_without_scoring_or_reusing_projection_endpoint():
    manifest = pd.read_csv(
        DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_manifest.csv"
    ).iloc[0]
    summary = pd.read_csv(
        DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_summary.csv"
    ).iloc[0]
    gates = pd.read_csv(DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_gate.csv")
    population = pd.read_csv(DATA / "mixed_readout_population_validation_summary.csv").iloc[0]
    cases = pd.read_csv(DATA / "mixed_readout_population_validation_cases.csv")

    assert summary["formula_freeze_status"] == "MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING"
    assert bool(summary["prospective_mixed_protocol_ready"]) is True
    assert bool(summary["mixed_endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual_in_construction"]) is False
    assert bool(summary["previous_projection_endpoint_used_as_mixed_evidence"]) is False

    assert manifest["carrier"] == "v_K_exponential_disk"
    assert "v_K_exponential_disk^2" in manifest["formula_text"]
    assert manifest["overlay_formula_id"] == "NGC5907_PROJECTION_ATTENUATION_V1"
    assert "velocity-squared" in manifest["dimension_check"]
    assert "v_mix=v_K_exponential_disk" in manifest["inactive_window_limit"]
    assert gates["gate_status"].str.startswith("PASS").all()

    assert int(population["n_prospective_protocol_ready_cases"]) == 3
    assert int(population["min_independent_prospective_cases_required"]) == 3
    assert bool(population["endpoint_scores_run"]) is False
    assert "NGC5907" in set(cases.loc[cases["prospective_protocol_ready"], "galaxy"])


def test_ngc7331_caveated_mixed_formula_freeze_is_ready_without_scoring():
    caveat_summary = pd.read_csv(
        DATA / "ngc7331_outer_warp_vertical_caveat_summary.csv"
    ).iloc[0]
    manifest = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_manifest.csv"
    ).iloc[0]
    summary = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_summary.csv"
    ).iloc[0]
    gates = pd.read_csv(DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.csv")
    population = pd.read_csv(DATA / "mixed_readout_population_validation_summary.csv").iloc[0]

    assert caveat_summary["caveat_gate_status"] == (
        "CAVEAT_MAPPED_TO_MIXED_OVERLAY_CONTEXT_FORMULA_FREEZE_ALLOWED"
    )
    assert abs(float(caveat_summary["intrinsic_h_over_Rs_mid"]) - 0.029880478) < 1.0e-6
    assert abs(float(caveat_summary["projected_hwhm_over_Rs"]) - 0.099601594) < 1.0e-6
    assert bool(caveat_summary["outer_warp_numeric_onset_available"]) is False
    assert bool(caveat_summary["uses_vobs_or_residual_in_construction"]) is False

    assert summary["formula_freeze_status"] == (
        "CAVEATED_MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING"
    )
    assert bool(summary["prospective_mixed_protocol_ready"]) is True
    assert bool(summary["mixed_endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual_in_construction"]) is False
    assert bool(summary["outer_warp_numeric_onset_available"]) is False

    assert manifest["carrier"] == "v_K_exponential_disk"
    assert "K_vow" in manifest["kernel_text"]
    assert "velocity-squared" in manifest["dimension_check"]
    assert manifest["caveat_status"] == "CAVEATED_BROAD_OUTER_WINDOW_NO_NUMERIC_WARP_ONSET"
    assert bool(manifest["formula_frozen_before_mixed_scoring"]) is True
    assert bool(manifest["mixed_endpoint_scores_allowed"]) is False
    assert gates["gate_status"].str.contains("PASS").all()

    assert population["validation_gate_status"] == "MIXED_POPULATION_VALIDATION_READY"
    assert int(population["n_prospective_protocol_ready_cases"]) == 3
    assert bool(population["endpoint_scores_run"]) is False


def test_available_morphology_readout_pilot_is_claim_bounded():
    availability = pd.read_csv(DATA / "available_data_morphology_readout_availability.csv")
    rank_summary = pd.read_csv(DATA / "available_data_wide_fixed_tpg_proxy_rank_summary.csv")
    morph_summary = pd.read_csv(DATA / "available_data_morphology_decomposition_summary.csv")
    full_overall = pd.read_csv(DATA / "available_data_full_sparc_tau_proxy_overall.csv")
    full_by_type = pd.read_csv(DATA / "available_data_full_sparc_tau_proxy_by_type.csv")
    paper1_summary = pd.read_csv(DATA / "available_data_paper1_73_galaxy_tau_baseline_summary.csv")

    final_endpoint = availability.loc[
        availability["layer"] == "real_paper8_morphology_family_endpoint", "status"
    ].iloc[0]
    rmond_status = availability.loc[
        availability["layer"] == "rmond_full_sample_comparator", "status"
    ].iloc[0]
    assert final_endpoint == "BLOCKED"
    assert rmond_status == "BLOCKED"

    core = rank_summary.loc[rank_summary["RotmodSpecificityFlagV02"] == "v02_core_like"].iloc[0]
    assert core["n_galaxies"] == 6
    assert core["fixed_tpg_beats_rar_fraction"] == 1.0
    assert core["fixed_tpg_beats_mond_fraction"] == 1.0
    assert core["fixed_tpg_beats_newtonian_fraction"] == 1.0

    assert len(morph_summary) > 0
    assert int(full_overall["n_galaxies"].sum()) == 175
    assert "type_bin" in full_by_type.columns
    assert "newtonian_baryonic" in set(paper1_summary["baseline"])
    assert "rar_mcgaugh" in set(paper1_summary["baseline"])
    assert (ROOT / "reports" / "available_morphology_readout_pilot.md").exists()
    report = (ROOT / "reports" / "available_morphology_readout_pilot.md").read_text(
        encoding="utf-8"
    )
    assert "not the final Paper 8" in report
    assert "175-Galaxy Proxy Runner" in report
    assert "Full-sample RMOND comparison is blocked" in report


def test_morphology_matched_tau_proxy_endpoint_is_claim_bounded():
    labels = pd.read_csv(DATA / "morphology_labels_predeclared_proxy.csv")
    betas = pd.read_csv(DATA / "morphology_matched_proxy_family_betas.csv")
    scores = pd.read_csv(DATA / "morphology_matched_proxy_scores_by_galaxy.csv")
    summary = pd.read_csv(DATA / "morphology_matched_proxy_endpoint_summary.csv")
    by_family = pd.read_csv(DATA / "morphology_matched_proxy_endpoint_by_family.csv")
    shuffled = pd.read_csv(DATA / "morphology_matched_proxy_shuffled_null.csv")
    shuffled_summary = pd.read_csv(DATA / "morphology_matched_proxy_shuffled_null_summary.csv")

    expected_families = {
        "K_compact_bulge",
        "K_diffuse_scale_tail",
        "K_late_exponential",
        "K_mid_regular",
    }
    assert expected_families == set(labels["morphology_family"])
    assert expected_families.issubset(set(betas["morphology_family"]))
    assert "K_global_tau_proxy" in set(betas["morphology_family"])
    assert labels["label_source"].str.contains("no residual endpoints").all()

    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    assert int(holdout["n_galaxies"]) == 44
    for column in [
        "matched_beats_wrong_fraction",
        "matched_rank1_fraction",
        "matched_beats_tpg_v6_fraction",
        "matched_beats_mond_fraction",
    ]:
        assert 0.0 <= float(holdout[column]) <= 1.0

    assert len(scores) == 175
    assert set(by_family["split"]) == {"holdout", "train"}
    assert len(shuffled) == 2000
    holdout_null = shuffled_summary.loc[shuffled_summary["split"] == "holdout"].iloc[0]
    assert int(holdout_null["n_shuffles"]) == 1000
    for column in [
        "p_mean_minus_wrong_at_least_as_good",
        "p_beats_wrong_fraction_at_least_as_good",
        "p_rank1_fraction_at_least_as_good",
    ]:
        assert 0.0 <= float(holdout_null[column]) <= 1.0
    report = (ROOT / "reports" / "morphology_matched_tau_proxy_endpoint.md").read_text(
        encoding="utf-8"
    )
    assert "not the final Paper 8 endpoint" in report
    assert "wrong families, TPG/v6, and MOND" in report
    assert "Shuffled-Label Null" in report


def test_morphology_formula_shell_proxy_endpoint_is_claim_bounded():
    labels = pd.read_csv(DATA / "morphology_formula_shell_proxy_labels.csv")
    amplitudes = pd.read_csv(DATA / "morphology_formula_shell_proxy_amplitudes.csv")
    scores = pd.read_csv(DATA / "morphology_formula_shell_proxy_scores_by_galaxy.csv")
    summary = pd.read_csv(DATA / "morphology_formula_shell_proxy_endpoint_summary.csv")
    by_family = pd.read_csv(DATA / "morphology_formula_shell_proxy_endpoint_by_family.csv")
    shuffled = pd.read_csv(DATA / "morphology_formula_shell_proxy_shuffled_null.csv")
    shuffled_summary = pd.read_csv(DATA / "morphology_formula_shell_proxy_shuffled_null_summary.csv")

    expected_families = {
        "K_compact_finite",
        "K_scale_tail_spiral",
        "K_exponential_disk",
        "K_thick_flared",
    }
    assert expected_families == set(labels["formula_family"])
    assert expected_families == set(amplitudes["formula_family"])
    assert labels["label_source"].str.contains("no residual endpoints").all()

    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    assert int(holdout["n_galaxies"]) == 44
    for column in [
        "matched_beats_wrong_fraction",
        "matched_rank1_fraction",
        "matched_beats_tpg_v6_fraction",
        "matched_beats_mond_fraction",
    ]:
        assert 0.0 <= float(holdout[column]) <= 1.0

    assert len(scores) == 175
    assert set(by_family["split"]) == {"holdout", "train"}
    assert len(shuffled) == 2000
    holdout_null = shuffled_summary.loc[shuffled_summary["split"] == "holdout"].iloc[0]
    assert int(holdout_null["n_shuffles"]) == 1000
    for column in [
        "p_mean_minus_wrong_at_least_as_good",
        "p_beats_wrong_fraction_at_least_as_good",
        "p_rank1_fraction_at_least_as_good",
    ]:
        assert 0.0 <= float(holdout_null[column]) <= 1.0
    report = (ROOT / "reports" / "morphology_formula_shell_proxy_endpoint.md").read_text(
        encoding="utf-8"
    )
    assert "not the final endpoint" in report
    assert "dimensionless radial proxies" in report


def test_morphology_parameter_manifest_is_residual_blind_and_complete():
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    counts = pd.read_csv(DATA / "morphology_parameter_manifest_family_counts.csv")
    confidence = pd.read_csv(DATA / "morphology_parameter_manifest_confidence_summary.csv")

    expected_families = {
        "K_compact_finite",
        "K_scale_tail_spiral",
        "K_exponential_disk",
        "K_thick_flared",
    }
    assert len(manifest) == 175
    assert expected_families == set(manifest["formula_family"])
    assert int(counts["n_galaxies"].sum()) == 175
    assert set(confidence["split"]) == {"holdout", "train"}
    assert manifest["parameter_source"].str.contains("available_data_proxy").all()
    assert manifest["forbidden_inputs"].str.contains("required_S_tau").all()
    for column in [
        "scale_radius_proxy_kpc",
        "tail_inner_radius_proxy_kpc",
        "tail_cutoff_radius_proxy_kpc",
        "compact_support_radius_proxy_kpc",
        "thickness_h_over_rs_proxy",
        "manifest_confidence",
    ]:
        assert manifest[column].notna().all()
    report = (ROOT / "reports" / "morphology_parameter_manifest.md").read_text(encoding="utf-8")
    assert "not the final hand-curated source-native morphology catalog" in report


def test_source_native_readout_formula_endpoint_is_claim_bounded():
    labels = pd.read_csv(DATA / "source_native_readout_formula_labels.csv")
    amplitudes = pd.read_csv(DATA / "source_native_readout_formula_amplitudes.csv")
    scores = pd.read_csv(DATA / "source_native_readout_formula_scores_by_galaxy.csv")
    summary = pd.read_csv(DATA / "source_native_readout_formula_endpoint_summary.csv")
    by_family = pd.read_csv(DATA / "source_native_readout_formula_endpoint_by_family.csv")
    shuffled = pd.read_csv(DATA / "source_native_readout_formula_shuffled_null.csv")
    shuffled_summary = pd.read_csv(DATA / "source_native_readout_formula_shuffled_null_summary.csv")

    expected_families = {
        "K_compact_finite",
        "K_scale_tail_spiral",
        "K_exponential_disk",
        "K_thick_flared",
    }
    assert expected_families == set(labels["formula_family"])
    assert expected_families == set(amplitudes["formula_family"])
    assert labels["parameter_source"].str.contains("available_data_proxy").all()
    assert labels["forbidden_inputs"].str.contains("required_S_tau").all()
    assert amplitudes["formula_source"].str.contains("tau_core_gravity").all()

    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    assert int(holdout["n_galaxies"]) == 44
    for column in [
        "matched_beats_wrong_fraction",
        "matched_rank1_fraction",
        "matched_beats_tpg_v6_fraction",
        "matched_beats_mond_fraction",
    ]:
        assert 0.0 <= float(holdout[column]) <= 1.0

    assert len(scores) == 175
    assert set(by_family["split"]) == {"holdout", "train"}
    assert len(shuffled) == 2000
    holdout_null = shuffled_summary.loc[shuffled_summary["split"] == "holdout"].iloc[0]
    assert int(holdout_null["n_shuffles"]) == 1000
    for column in [
        "p_mean_minus_wrong_at_least_as_good",
        "p_beats_wrong_fraction_at_least_as_good",
        "p_rank1_fraction_at_least_as_good",
    ]:
        assert 0.0 <= float(holdout_null[column]) <= 1.0
    report = (ROOT / "reports" / "source_native_readout_formula_endpoint.md").read_text(
        encoding="utf-8"
    )
    assert "concrete Tau Core bridge morphology formulas" in report
    assert "morphology_parameter_manifest.csv" in report
    assert "not empirical validation" in report


def test_readout_mixture_proxy_endpoint_preserves_negative_control():
    weights = pd.read_csv(DATA / "readout_mixture_proxy_weights.csv")
    scores = pd.read_csv(DATA / "readout_mixture_proxy_scores_by_galaxy.csv")
    summary = pd.read_csv(DATA / "readout_mixture_proxy_endpoint_summary.csv")
    expected_families = {
        "K_compact_finite",
        "K_scale_tail_spiral",
        "K_exponential_disk",
        "K_thick_flared",
    }
    assert len(weights) == 175
    assert len(scores) == 175
    assert expected_families == {
        column.removeprefix("w_") for column in weights.columns if column.startswith("w_")
    }
    weight_cols = [f"w_{family}" for family in expected_families]
    assert (weights[weight_cols].sum(axis=1).sub(1.0).abs() < 1.0e-12).all()
    assert weights["weight_source"].eq("available_data_residual_blind_morphology_proxy").all()
    assert weights["claim_boundary"].eq(
        "readout_mixture_proxy_not_accepted_tau_side_state_not_endpoint"
    ).all()
    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    assert int(holdout["n_galaxies"]) == 44
    assert abs(float(holdout["mixture_beats_single_matched_fraction"]) - 5 / 11) < 1.0e-12
    assert abs(float(holdout["mixture_beats_tpg_v6_fraction"]) - 0.5) < 1.0e-12
    assert abs(float(holdout["mixture_beats_mond_fraction"]) - 5 / 11) < 1.0e-12
    report = (ROOT / "reports" / "readout_mixture_proxy_endpoint.md").read_text(
        encoding="utf-8"
    )
    assert "residual-blind proxy mixture" in report
    assert "not an accepted Tau-side readout state" in report
    assert "not a final endpoint" in report


def test_manifest_confidence_diagnostics_are_claim_bounded():
    summary = pd.read_csv(DATA / "manifest_confidence_diagnostics_summary.csv")
    shuffled = pd.read_csv(DATA / "manifest_confidence_diagnostics_shuffled.csv")
    assert "holdout:all" in set(summary["subset"])
    assert "holdout:confidence_ge_0_75" in set(summary["subset"])
    assert "holdout:no_low_inclination" in set(summary["subset"])
    assert "holdout:all" in set(shuffled["subset"])
    assert "holdout:confidence_ge_0_75" in set(shuffled["subset"])
    holdout = summary.loc[summary["subset"] == "holdout:all"].iloc[0]
    assert int(holdout["n_galaxies"]) == 44
    for column in [
        "matched_beats_wrong_fraction",
        "matched_beats_tpg_v6_fraction",
        "matched_beats_mond_fraction",
    ]:
        assert 0.0 <= float(holdout[column]) <= 1.0
    holdout_null = shuffled.loc[shuffled["subset"] == "holdout:all"].iloc[0]
    assert int(holdout_null["n_shuffles"]) == 1000
    assert 0.0 <= float(holdout_null["p_mean_minus_wrong_at_least_as_good"]) <= 1.0
    report = (ROOT / "reports" / "manifest_confidence_diagnostics.md").read_text(
        encoding="utf-8"
    )
    assert "not a new fit" in report
    assert "morphology parameter quality" in report


def test_amplitude_policy_diagnostics_are_claim_bounded():
    amplitudes = pd.read_csv(DATA / "amplitude_policy_diagnostics_amplitudes.csv")
    scores = pd.read_csv(DATA / "amplitude_policy_diagnostics_scores_by_galaxy.csv")
    summary = pd.read_csv(DATA / "amplitude_policy_diagnostics_summary.csv")

    expected_policies = {
        "family_unconstrained",
        "family_attractive_only",
        "global_unconstrained",
        "global_attractive_only",
        "family_shrink_50_to_global",
    }
    assert expected_policies == set(summary["amplitude_policy"])
    assert expected_policies == set(amplitudes["amplitude_policy"])
    assert len(scores) == 175 * len(expected_policies)
    holdout = summary.loc[
        (summary["split"] == "holdout")
        & (summary["amplitude_policy"] == "family_shrink_50_to_global")
    ].iloc[0]
    assert int(holdout["n_galaxies"]) == 44
    for column in [
        "matched_beats_wrong_fraction",
        "matched_beats_tpg_v6_fraction",
        "matched_beats_mond_fraction",
    ]:
        assert 0.0 <= float(holdout[column]) <= 1.0
    report = (ROOT / "reports" / "amplitude_policy_diagnostics.md").read_text(
        encoding="utf-8"
    )
    assert "not a new endpoint claim" in report
    assert "amplitude-policy stress test" in report


def test_amplitude_shrinkage_path_is_claim_bounded():
    amplitudes = pd.read_csv(DATA / "amplitude_shrinkage_path_amplitudes.csv")
    scores = pd.read_csv(DATA / "amplitude_shrinkage_path_scores_by_galaxy.csv")
    summary = pd.read_csv(DATA / "amplitude_shrinkage_path_summary.csv")
    tradeoff = pd.read_csv(DATA / "amplitude_shrinkage_path_tradeoff.csv")

    assert len(set(summary["family_weight"])) == 21
    assert len(scores) == 175 * 21
    assert len(amplitudes) == 4 * 21
    holdout_05 = summary.loc[
        (summary["split"] == "holdout") & (summary["family_weight"] == 0.5)
    ].iloc[0]
    assert int(holdout_05["n_galaxies"]) == 44
    assert 0.0 <= float(holdout_05["matched_beats_wrong_fraction"]) <= 1.0
    assert 0.0 <= float(holdout_05["matched_beats_mond_fraction"]) <= 1.0
    assert "tradeoff_score" in tradeoff.columns
    report = (ROOT / "reports" / "amplitude_shrinkage_path.md").read_text(
        encoding="utf-8"
    )
    assert "not a validated physical policy" in report
    assert "amplitude-normalization range" in report


def test_train_selected_shrinkage_diagnostic_is_claim_bounded():
    selection = pd.read_csv(DATA / "train_selected_shrinkage_selection.csv")
    holdout = pd.read_csv(DATA / "train_selected_shrinkage_holdout.csv")

    expected_rules = {
        "train_balanced_max",
        "train_specificity_then_baseline",
        "train_mond_gap_min_with_specificity",
        "train_tpg_gap_min_with_specificity",
    }
    assert expected_rules == set(selection["selection_rule"])
    assert expected_rules == set(holdout["selection_rule"])
    assert len(selection) == 4
    assert len(holdout) == 4
    assert set(holdout["selected_family_weight"]) == {0.4}
    assert (holdout["holdout_n_galaxies"] == 44).all()
    for column in [
        "holdout_matched_beats_wrong_fraction",
        "holdout_matched_rank1_fraction",
        "holdout_matched_beats_tpg_v6_fraction",
        "holdout_matched_beats_mond_fraction",
    ]:
        assert ((0.0 <= holdout[column]) & (holdout[column] <= 1.0)).all()
    report = (ROOT / "reports" / "train_selected_shrinkage_diagnostic.md").read_text(
        encoding="utf-8"
    )
    assert "using train" in report
    assert "split metrics only" in report
    assert "not a validated amplitude-normalization law" in report


def test_family_breakdown_diagnostics_are_claim_bounded():
    breakdown = pd.read_csv(DATA / "family_breakdown_diagnostics.csv")
    expected_families = {
        "K_compact_finite",
        "K_scale_tail_spiral",
        "K_exponential_disk",
        "K_thick_flared",
    }
    assert expected_families == set(breakdown["formula_family"])
    assert set(breakdown["split"]) == {"holdout", "train"}
    assert set(breakdown["amplitude_path_id"]) == {"shrink_family_weight_0.40"}
    holdout = breakdown.loc[breakdown["split"] == "holdout"]
    assert int(holdout["n_galaxies"].sum()) == 44
    for column in [
        "matched_beats_wrong_fraction",
        "matched_rank1_fraction",
        "matched_beats_tpg_v6_fraction",
        "matched_beats_mond_fraction",
    ]:
        assert ((0.0 <= breakdown[column]) & (breakdown[column] <= 1.0)).all()
    assert "strong" in set(holdout["specificity_status"])
    assert "baseline_blocked" in set(holdout["baseline_status"])
    report = (ROOT / "reports" / "family_breakdown_diagnostics.md").read_text(
        encoding="utf-8"
    )
    assert "does not refit" in report
    assert "preparation diagnostic" in report
    assert "empirical validation claim" in report


def test_family_observable_quality_diagnostics_are_claim_bounded():
    summary = pd.read_csv(DATA / "family_observable_quality_diagnostics.csv")
    groups = pd.read_csv(DATA / "family_observable_quality_clean_vs_caveated.csv")
    expected_families = {
        "K_compact_finite",
        "K_scale_tail_spiral",
        "K_exponential_disk",
        "K_thick_flared",
    }
    assert expected_families == set(summary["formula_family"])
    assert set(summary["split"]) == {"holdout", "train"}
    assert {"clean_manifest_proxy", "quality_caveated"}.issubset(set(groups["quality_group"]))
    holdout = summary.loc[summary["split"] == "holdout"]
    assert int(holdout["n_galaxies"].sum()) == 44
    assert "quality_limited" in set(holdout["quality_status"])
    assert "current_best_case" in set(holdout["quality_status"])
    for column in [
        "low_confidence_fraction",
        "any_quality_caveat_fraction",
        "matched_beats_wrong_fraction",
        "matched_beats_tpg_v6_fraction",
        "matched_beats_mond_fraction",
    ]:
        assert ((0.0 <= summary[column]) & (summary[column] <= 1.0)).all()
    report = (ROOT / "reports" / "family_observable_quality_diagnostics.md").read_text(
        encoding="utf-8"
    )
    assert "not a new fit" in report
    assert "failure-map diagnostic" in report
    assert "better residual-blind morphology" in report


def test_baseline_success_morphology_audit_is_descriptive_control():
    audit = pd.read_csv(DATA / "baseline_success_morphology_audit.csv")
    summary = pd.read_csv(DATA / "baseline_success_morphology_summary.csv")
    by_family = pd.read_csv(DATA / "baseline_success_morphology_by_family.csv")
    conventional = pd.read_csv(DATA / "baseline_success_conventional_available_summary.csv")
    assert len(audit) == 175
    assert set(audit["winner_tau_tpg_mond"]) == {"tau_matched", "tpg_v6", "mond"}
    assert audit["claim_boundary"].eq(
        "baseline_success_morphology_audit_not_endpoint_not_validation"
    ).all()
    holdout = summary.loc[summary["split"] == "holdout"]
    assert int(holdout["n_galaxies"].sum()) == 44
    tpg = holdout.loc[holdout["winner_tau_tpg_mond"] == "tpg_v6"].iloc[0]
    tau = holdout.loc[holdout["winner_tau_tpg_mond"] == "tau_matched"].iloc[0]
    assert int(tpg["n_galaxies"]) == 16
    assert int(tau["n_galaxies"]) == 16
    assert float(tpg["current_memory_match_fraction"]) == 0.0
    assert float(tau["current_memory_match_fraction"]) > 0.5
    scale_tail_tpg = by_family.loc[
        (by_family["split"] == "holdout")
        & (by_family["formula_family"] == "K_scale_tail_spiral")
        & (by_family["winner_tau_tpg_mond"] == "tpg_v6")
    ].iloc[0]
    assert int(scale_tail_tpg["n_galaxies"]) == 12
    assert {"Newtonian", "RAR", "MOND", "FixedTPG"}.issubset(
        set(conventional["available_best_model"])
    )
    report = (ROOT / "reports" / "baseline_success_morphology_audit.md").read_text(
        encoding="utf-8"
    )
    assert "descriptive only" in report
    assert "memory-integrated" in report
    assert "regular baryonic-readout regime" in report
    assert "simple radial/low-acceleration" in report
    assert "diffuse-disk effective scaling regimes" in report


def test_predeclared_quality_gate_diagnostics_are_claim_bounded():
    summary = pd.read_csv(DATA / "predeclared_quality_gate_diagnostics.csv")
    by_family = pd.read_csv(DATA / "predeclared_quality_gate_by_family.csv")
    expected_gates = {
        "all",
        "confidence_ge_0_75",
        "confidence_ge_0_85",
        "no_low_inclination",
        "no_large_distance_error",
        "no_few_rotation_points",
        "clean_manifest_proxy",
        "confidence_ge_0_75_and_clean",
    }
    assert expected_gates == set(summary["quality_gate"])
    assert expected_gates.issubset(set(by_family["quality_gate"]))
    assert set(summary["split"]) == {"holdout", "train"}
    holdout = summary.loc[summary["split"] == "holdout"]
    assert "candidate_predeclared_gate" in set(holdout["gate_status"])
    clean = holdout.loc[holdout["quality_gate"] == "clean_manifest_proxy"].iloc[0]
    assert int(clean["n_galaxies"]) == 20
    assert int(clean["n_families_present"]) == 4
    for column in [
        "matched_beats_wrong_fraction",
        "matched_rank1_fraction",
        "matched_beats_tpg_v6_fraction",
        "matched_beats_mond_fraction",
    ]:
        assert ((0.0 <= summary[column]) & (summary[column] <= 1.0)).all()
    report = (ROOT / "reports" / "predeclared_quality_gate_diagnostics.md").read_text(
        encoding="utf-8"
    )
    assert "does not choose a gate by" in report
    assert "not a discovery claim" in report
    assert "declare the quality gate before endpoint scoring" in report


def test_quality_gate_shuffled_null_diagnostics_are_claim_bounded():
    shuffled = pd.read_csv(DATA / "quality_gate_shuffled_null.csv")
    summary = pd.read_csv(DATA / "quality_gate_shuffled_null_summary.csv")
    assert len(shuffled) >= 8 * 2 * 1000
    assert set(summary["split"]) == {"holdout", "train"}
    holdout = summary.loc[summary["split"] == "holdout"]
    assert "all" in set(holdout["quality_gate"])
    all_gate = holdout.loc[holdout["quality_gate"] == "all"].iloc[0]
    assert int(all_gate["n_shuffles"]) == 1000
    assert int(all_gate["n_galaxies"]) == 44
    for column in [
        "p_mean_minus_wrong_at_least_as_good",
        "p_beats_wrong_fraction_at_least_as_good",
        "p_rank1_fraction_at_least_as_good",
        "observed_beats_wrong_fraction",
        "null_beats_wrong_fraction_mean",
    ]:
        assert ((0.0 <= summary[column]) & (summary[column] <= 1.0)).all()
    report = (ROOT / "reports" / "quality_gate_shuffled_null_diagnostics.md").read_text(
        encoding="utf-8"
    )
    assert "predeclared quality gate" in report
    assert "not empirical validation" in report
    assert "declared before endpoint scoring" in report


def test_endpoint_decision_matrix_is_claim_bounded():
    matrix = pd.read_csv(DATA / "endpoint_decision_matrix.csv")
    expected_roles = {
        "primary_endpoint_candidate",
        "specificity_null_primary",
        "baseline_competitiveness_secondary",
        "limited_or_negative_control",
        "specificity_only_diagnostic",
    }
    assert expected_roles.issubset(set(matrix["recommended_endpoint_role"]))
    primary = matrix.loc[
        matrix["recommended_endpoint_role"] == "primary_endpoint_candidate"
    ].iloc[0]
    assert primary["quality_gate"] == "no_low_inclination"
    assert int(primary["n_galaxies"]) == 35
    assert primary["null_support_status"] == "strong_fraction_and_mean_null"
    assert bool(primary["baseline_competitive"])
    full = matrix.loc[matrix["quality_gate"] == "all"].iloc[0]
    assert full["recommended_endpoint_role"] == "specificity_null_primary"
    report = (ROOT / "reports" / "endpoint_decision_matrix.md").read_text(
        encoding="utf-8"
    )
    assert "protocol decision aid" in report
    assert "Current primary endpoint candidate: no_low_inclination" in report
    assert "must not be read as selecting a winning endpoint" in report


def test_predeclared_endpoint_protocol_is_claim_bounded():
    protocol = pd.read_csv(DATA / "predeclared_endpoint_protocol.csv")
    required_layers = {
        "primary_endpoint_lane",
        "fuller_sample_support_lane",
        "baseline_secondary_lane",
        "amplitude_policy",
        "morphology_family_assignment",
        "primary_specificity_metric",
        "baseline_metrics",
        "caveated_rows",
        "primary_endpoint_lane_current_metrics",
    }
    assert required_layers.issubset(set(protocol["protocol_layer"]))
    primary = protocol.loc[protocol["protocol_layer"] == "primary_endpoint_lane"].iloc[0]
    assert primary["predeclared_choice"] == "no_low_inclination"
    amplitude = protocol.loc[protocol["protocol_layer"] == "amplitude_policy"].iloc[0]
    assert "family_weight=0.40" in amplitude["rule"]
    assert "holdout-selected amplitude" in amplitude["forbidden_inputs"]
    forbidden = " ".join(protocol["forbidden_inputs"].astype(str))
    assert "required_S_tau" in forbidden
    assert "posthoc gate choice" in forbidden
    report = (ROOT / "reports" / "predeclared_endpoint_protocol.md").read_text(
        encoding="utf-8"
    )
    assert "predeclaration aid" in report
    assert "must freeze these" in report
    assert "must not silently drop caveated" in report


def test_readiness_upgrade_audit_preserves_claim_boundary():
    audit = pd.read_csv(DATA / "paper8_readiness_upgrade_audit.csv")
    assert "primary_endpoint_candidate" in set(audit["readiness_layer"])
    assert "empirical_discovery_claim" in set(audit["readiness_layer"])
    primary = audit.loc[audit["readiness_layer"] == "primary_endpoint_candidate"].iloc[0]
    assert primary["status"] == "predeclaration_ready"
    assert "no_low_inclination" in primary["evidence"]
    discovery = audit.loc[audit["readiness_layer"] == "empirical_discovery_claim"].iloc[0]
    assert discovery["status"] == "blocked"
    assert "Do not claim Tau Core validation" in discovery["next_action"]
    report = (ROOT / "reports" / "paper8_readiness_upgrade_audit.md").read_text(
        encoding="utf-8"
    )
    assert "preparation-ready" in report
    assert "not discovery-ready" in report
    assert "accepted residual-blind morphology inputs" in report


def test_morphology_observable_intake_schema_is_claim_bounded():
    schema = pd.read_csv(DATA / "morphology_observable_intake_schema.csv")
    gates = pd.read_csv(DATA / "morphology_observable_acceptance_gates.csv")
    required_fields = {
        "formula_family",
        "manifest_confidence",
        "manifest_caveat",
        "inclination_deg",
        "distance_frac_error",
        "scale_radius_kpc",
        "observable_provenance",
    }
    assert required_fields.issubset(set(schema["field"]))
    forbidden = " ".join(schema["forbidden_source"].astype(str))
    assert "required_S_tau" in forbidden
    assert "endpoint-selected" in forbidden
    assert "best-fit formula choice" in forbidden
    expected_gates = {
        "residual_blindness",
        "primary_quality_gate_ready",
        "family_kernel_parameters_ready",
        "provenance_ready",
        "caveated_rows_preserved",
    }
    assert expected_gates.issubset(set(gates["gate"]))
    report = (ROOT / "reports" / "morphology_observable_intake_schema.md").read_text(
        encoding="utf-8"
    )
    assert "data-intake contract" in report
    assert "not a fit" in report
    assert "current available-data manifest remains a proxy manifest" in report


def test_morphology_information_gain_test_is_claim_bounded():
    level_manifest = pd.read_csv(DATA / "morphology_information_gain_level_manifest.csv")
    summary = pd.read_csv(DATA / "morphology_information_gain_summary.csv")
    transitions = pd.read_csv(DATA / "morphology_information_gain_transitions.csv")
    acquisition = pd.read_csv(DATA / "morphology_information_gain_data_acquisition.csv")
    scores = pd.read_csv(DATA / "morphology_information_gain_scores_by_galaxy.csv")

    assert {"L0", "L1", "L2", "L3", "L4"}.issubset(
        set(level_manifest["information_level"])
    )
    assert "BLOCKED_DATA_NOT_ASSEMBLED" in set(level_manifest["current_status"])
    assert {"L0", "L1", "L2", "L3"}.issubset(set(scores["information_level"]))

    holdout = summary.loc[summary["split"] == "holdout"]
    l0 = holdout.loc[holdout["information_level"] == "L0"].iloc[0]
    l1 = holdout.loc[holdout["information_level"] == "L1"].iloc[0]
    l2 = holdout.loc[holdout["information_level"] == "L2"].iloc[0]
    l3 = holdout.loc[holdout["information_level"] == "L3"].iloc[0]
    assert l0["matched_beats_wrong_fraction"] == 0.5
    assert l1["matched_beats_wrong_fraction"] > l0["matched_beats_wrong_fraction"]
    assert pd.isna(l2["matched_beats_wrong_fraction"])
    assert l3["beats_mond_fraction"] > l1["beats_mond_fraction"]

    holdout_transitions = transitions.loc[transitions["split"] == "holdout"]
    assert "L0->L1_negative_or_overfit_proxy_warning" in set(
        holdout_transitions["interpretation"]
    )
    assert "L2->L3_supports_information_gain" in set(
        holdout_transitions["interpretation"]
    )

    source_counts = dict(zip(acquisition["source_family"], acquisition["available_count"]))
    assert source_counts["SPARC"] == 175
    assert source_counts["S4G"] == 75
    assert source_counts["DustPedia"] == 31
    assert source_counts["HI_surveys"] == 171
    assert source_counts["PHANGS"] == 2
    assert source_counts["L2_tail_candidates"] == 172
    assert source_counts["L2_compact_candidates"] == 48
    assert source_counts["L2_bar_candidates"] == 19
    assert source_counts["L4_velocity_field_candidates"] == 0
    assert source_counts["readout_state_vector_components"] == 0

    expansion = pd.read_csv(DATA / "morphology_information_gain_source_expansion.csv")
    expansion_summary = pd.read_csv(DATA / "morphology_information_gain_source_expansion_summary.csv")
    assert len(expansion) == 175
    summary_counts = dict(
        zip(expansion_summary["coverage_field"], expansion_summary["n_galaxies"])
    )
    assert summary_counts["q_tail_candidate"] == 172
    assert summary_counts["q_compact_candidate"] == 48
    assert summary_counts["q_bar_candidate"] == 19
    assert summary_counts["l4_velocity_field_candidate"] == 0

    report = (ROOT / "reports" / "morphology_information_gain_test.md").read_text(
        encoding="utf-8"
    )
    assert "first information-gain diagnostic" in report
    assert "L0->L1" in report
    assert "L1->L2" in report
    assert "L2->L3" in report
    assert "not an empirical validation claim" in report
    assert "accepted morphology-memory" in report
    assert "forbidden" in report

    source_report = (
        ROOT / "reports" / "morphology_information_gain_source_expansion.md"
    ).read_text(encoding="utf-8")
    assert "all-sample source expansion" in source_report
    assert "Full-Sample Coverage" in source_report
    assert "source candidates only" in source_report


def test_l2_weight_intake_candidates_are_claim_bounded():
    candidates = pd.read_csv(DATA / "morphology_information_gain_l2_weight_intake_candidates.csv")
    summary = pd.read_csv(DATA / "morphology_information_gain_l2_weight_intake_summary.csv")

    assert len(candidates) == 175
    assert candidates["uses_endpoint_residuals"].eq(False).all()
    assert candidates["accepted_label_output_allowed"].eq(False).all()
    assert candidates["endpoint_scores_computed"].eq(False).all()
    assert set(candidates["claim_boundary"]) == {
        "l2_weight_intake_candidate_not_endpoint_not_accepted_state"
    }

    weight_cols = [
        "w_K_compact_finite",
        "w_K_scale_tail_spiral",
        "w_K_exponential_disk",
        "w_K_thick_flared",
    ]
    assert candidates[weight_cols].sum(axis=1).round(12).eq(1.0).all()
    assert set(summary["split"]) == {"all", "holdout", "train"}
    full = summary.loc[summary["split"] == "all"].iloc[0]
    assert full["n_galaxies"] == 175
    assert full["source_informative_count"] == 174
    assert full["uninformative_fallback_count"] == 1
    assert full["nonzero_K_scale_tail_spiral_count"] == 172
    assert full["nonzero_K_exponential_disk_count"] == 75
    assert full["nonzero_K_compact_finite_count"] == 48
    assert full["nonzero_K_thick_flared_count"] == 107

    report = (ROOT / "reports" / "morphology_information_gain_l2_weight_intake.md").read_text(
        encoding="utf-8"
    )
    assert "intake layer only" in report
    assert "does not use endpoint residuals" in report
    assert "not accepted Tau-side readout" in report
    assert "Endpoint use requires a separate freeze-and-audit step" in report


def test_l2_weight_intake_endpoint_preflight_preserves_negative_result():
    scores = pd.read_csv(DATA / "morphology_information_gain_l2_weight_intake_endpoint_scores.csv")
    summary = pd.read_csv(DATA / "morphology_information_gain_l2_weight_intake_endpoint_summary.csv")
    by_family = pd.read_csv(DATA / "morphology_information_gain_l2_weight_intake_endpoint_by_family.csv")

    assert len(scores) == 175
    assert set(summary["split"]) == {"holdout", "train"}
    assert set(scores["claim_boundary"]) == {
        "l2_weight_intake_endpoint_preflight_not_validation"
    }
    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    assert holdout["n_galaxies"] == 44
    assert round(float(holdout["beats_old_l2_proxy_fraction"]), 6) == round(0.409091, 6)
    assert round(float(holdout["beats_single_matched_fraction"]), 6) == round(0.409091, 6)
    assert round(float(holdout["beats_tpg_v6_fraction"]), 6) == round(0.477273, 6)
    assert round(float(holdout["beats_mond_fraction"]), 6) == round(0.431818, 6)
    assert float(holdout["median_intake_minus_old_l2_proxy"]) > 0.0

    holdout_by_family = by_family.loc[by_family["split"] == "holdout"]
    thick = holdout_by_family.loc[
        holdout_by_family["dominant_intake_family"] == "K_thick_flared"
    ].iloc[0]
    compact = holdout_by_family.loc[
        holdout_by_family["dominant_intake_family"] == "K_compact_finite"
    ].iloc[0]
    assert float(thick["median_intake_minus_old_l2_proxy"]) < 0.0
    assert float(compact["median_intake_minus_old_l2_proxy"]) > 0.0

    report = (
        ROOT / "reports" / "morphology_information_gain_l2_weight_intake_endpoint_preflight.md"
    ).read_text(encoding="utf-8")
    assert "not validation" in report
    assert "not an accepted readout" in report
    assert "Beats old L2 mixture proxy: 0.409" in report
    assert "not a baseline-superiority claim" in report


def test_tau_side_source_normalization_rule_is_residual_blind_and_conditional():
    derivation_constants = pd.read_csv(
        DATA / "tau_side_source_normalization_derivation_constants.csv"
    )
    component_rule = pd.read_csv(DATA / "tau_side_source_normalization_component_rule.csv")
    galaxy_rule = pd.read_csv(DATA / "tau_side_source_normalization_galaxy_rule.csv")
    scores = pd.read_csv(DATA / "tau_side_source_normalized_l2_endpoint_scores.csv")
    summary = pd.read_csv(DATA / "tau_side_source_normalized_l2_endpoint_summary.csv")

    assert len(component_rule) == 700
    assert len(galaxy_rule) == 175
    assert len(scores) == 175
    assert component_rule["uses_vobs_or_residual"].eq(False).all()
    assert galaxy_rule["uses_vobs_or_residual"].eq(False).all()
    assert galaxy_rule["endpoint_freeze_allowed"].eq(False).all()
    assert set(component_rule["claim_boundary"]) == {
        "tau_side_source_normalization_formula_conditional_not_validation"
    }
    assert set(component_rule["orientation_sign_proof_status"]) == {"THEORY_CONDITIONAL"}
    assert {
        "THEORY_CONDITIONAL",
        "DERIVED_COARSE_GRID_PROXY_ADMISSION_PRODUCT",
        "DEFINITION_DEPENDENT",
        "DERIVED_FROM_GATE_DEFINITION",
    }.issuperset(
        set(component_rule["evidence_gate_proof_status"])
    )

    signs = dict(zip(component_rule["component_family"], component_rule["orientation_sign"]))
    manifest_signs = dict(
        zip(
            derivation_constants.loc[
                derivation_constants["constant_type"] == "orientation_sign", "constant_key"
            ],
            derivation_constants.loc[
                derivation_constants["constant_type"] == "orientation_sign", "constant_value"
            ],
        )
    )
    assert signs["K_compact_finite"] == 1.0
    assert signs["K_scale_tail_spiral"] == 1.0
    assert signs["K_exponential_disk"] == -1.0
    assert signs["K_thick_flared"] == -1.0
    assert signs == manifest_signs
    gates = dict(
        zip(component_rule["component_evidence_status"], component_rule["evidence_gate"])
    )
    manifest_gates = dict(
        zip(
            derivation_constants.loc[
                derivation_constants["constant_type"] == "evidence_gate", "constant_key"
            ],
            derivation_constants.loc[
                derivation_constants["constant_type"] == "evidence_gate", "constant_value"
            ],
        )
    )
    assert gates["PROXY_OR_PARTIAL_SOURCE_ONLY"] == manifest_gates["PROXY_OR_PARTIAL_SOURCE_ONLY"]
    assert gates["MISSING_SOURCE_SUPPORT"] == manifest_gates["MISSING_SOURCE_SUPPORT"]

    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    assert holdout["n_galaxies"] == 44
    assert round(float(holdout["beats_old_l2_intake_fraction"]), 6) == round(0.568182, 6)
    assert round(float(holdout["beats_tpg_v6_fraction"]), 6) == round(0.454545, 6)
    assert round(float(holdout["beats_mond_fraction"]), 6) == round(0.545455, 6)
    assert float(holdout["median_source_norm_minus_old_l2_intake"]) < 0.0

    report = (ROOT / "reports" / "tau_side_source_normalized_l2_endpoint.md").read_text(
        encoding="utf-8"
    )
    assert "residual-blind, theory-conditional" in report
    assert "uses no observed velocity endpoint" in report
    assert "Beats old L2 intake endpoint: 0.568" in report
    assert "not an accepted physical normalization law" in report


def test_tau_side_source_normalization_derivation_manifest_is_formula_conditional():
    constants = pd.read_csv(DATA / "tau_side_source_normalization_derivation_constants.csv")
    rule = pd.read_csv(DATA / "tau_side_source_normalization_derivation_rule.csv")
    summary = pd.read_csv(DATA / "tau_side_source_normalization_derivation_summary.csv")

    assert len(constants) == 10
    assert len(rule) == 4
    assert constants.loc[constants["constant_type"] == "orientation_sign"].shape[0] == 4
    assert constants.loc[constants["constant_type"] == "evidence_gate"].shape[0] == 6
    assert set(rule["dimension_status"]) == {"dimensionless", "velocity_squared"}

    summary_counts = {
        (row["constant_type"], row["proof_status"]): int(row["n_constants"])
        for _, row in summary.iterrows()
    }
    assert summary_counts[("orientation_sign", "THEORY_CONDITIONAL")] == 4
    assert summary_counts[("evidence_gate", "DEFINITION_DEPENDENT")] == 4
    assert summary_counts[("evidence_gate", "DERIVED_COARSE_GRID_PROXY_ADMISSION_PRODUCT")] == 1
    assert summary_counts[("evidence_gate", "DERIVED_FROM_GATE_DEFINITION")] == 1

    proxy = constants.loc[constants["constant_key"] == "PROXY_OR_PARTIAL_SOURCE_ONLY"].iloc[0]
    missing = constants.loc[constants["constant_key"] == "MISSING_SOURCE_SUPPORT"].iloc[0]
    assert float(proxy["constant_value"]) == 0.35
    assert proxy["proof_status"] == "DERIVED_COARSE_GRID_PROXY_ADMISSION_PRODUCT"
    assert float(missing["constant_value"]) == 0.0
    assert missing["proof_status"] == "DERIVED_FROM_GATE_DEFINITION"

    report = (
        ROOT / "reports" / "tau_side_source_normalization_derivation_audit.md"
    ).read_text(encoding="utf-8")
    assert "dimensionally consistent" in report
    assert "THEORY-CONDITIONAL" in report
    assert "coarse executable representative" in report
    assert "must not be selected from endpoint residuals" in report


def test_tau_side_source_normalization_sensitivity_is_not_model_selection():
    manifest = pd.read_csv(DATA / "tau_side_source_normalization_sensitivity_manifest.csv")
    components = pd.read_csv(DATA / "tau_side_source_normalization_sensitivity_components.csv")
    scores = pd.read_csv(DATA / "tau_side_source_normalization_sensitivity_scores.csv")
    summary = pd.read_csv(DATA / "tau_side_source_normalization_sensitivity_summary.csv")

    assert len(manifest) == 7
    assert len(components) == 4900
    assert len(scores) == 1225
    assert len(summary) == 14
    assert set(summary["claim_boundary"]) == {
        "tau_side_source_normalization_sensitivity_not_model_selection"
    }
    assert set(manifest["selection_policy"]) == {
        "predeclared_sensitivity_audit_not_endpoint_selection"
    }

    holdout = summary.loc[summary["split"] == "holdout"]
    primary = holdout.loc[holdout["variant_id"] == "primary_proxy_gate_0p35"].iloc[0]
    all_positive = holdout.loc[holdout["variant_id"] == "all_positive_orientation"].iloc[0]
    all_negative = holdout.loc[holdout["variant_id"] == "all_negative_orientation"].iloc[0]
    full_proxy = holdout.loc[holdout["variant_id"] == "full_proxy_gate_1p00"].iloc[0]

    assert round(float(primary["beats_old_l2_intake_fraction"]), 6) == round(0.568182, 6)
    assert float(primary["median_source_norm_minus_old_l2_intake"]) < 0.0
    assert float(all_positive["median_source_norm_minus_old_l2_intake"]) > 0.0
    assert float(all_negative["median_source_norm_minus_old_l2_intake"]) > 1.0
    assert round(float(full_proxy["beats_tpg_v6_fraction"]), 6) == round(0.522727, 6)

    report = (ROOT / "reports" / "tau_side_source_normalization_sensitivity.md").read_text(
        encoding="utf-8"
    )
    assert "does not choose a winning variant" in report
    assert "not be selected for the paper endpoint" in report
    assert "all_positive_orientation" in report
    assert "all_negative_orientation" in report


def test_tau_side_evidence_measure_gate_replaces_fixed_proxy_bin_as_candidate():
    gate = pd.read_csv(DATA / "tau_side_evidence_measure_gate_components.csv")
    summary = pd.read_csv(DATA / "tau_side_evidence_measure_gate_summary.csv")
    component_rule = pd.read_csv(DATA / "tau_side_evidence_measure_l2_component_rule.csv")
    scores = pd.read_csv(DATA / "tau_side_evidence_measure_l2_endpoint_scores.csv")
    endpoint_summary = pd.read_csv(DATA / "tau_side_evidence_measure_l2_endpoint_summary.csv")

    assert len(gate) == 406
    assert len(component_rule) == 700
    assert len(scores) == 175
    assert gate["uses_vobs_or_residual"].eq(False).all()
    assert gate["endpoint_scores_computed"].eq(False).all()
    assert set(gate["claim_boundary"]) == {"tau_side_evidence_measure_gate_candidate_not_endpoint"}
    assert set(component_rule["claim_boundary"]) == {
        "tau_side_evidence_measure_l2_endpoint_preflight_not_validation"
    }

    proxy = gate.loc[gate["component_evidence_status"] == "PROXY_OR_PARTIAL_SOURCE_ONLY"]
    assert len(proxy) == 105
    assert round(float(proxy["e_tau"].median()), 6) == round(0.354025, 6)
    assert round(float(proxy["gate_minus_fixed_manifest_gate"].median()), 6) == round(0.004025, 6)
    assert set(proxy["e_tau_status"]) == {"E_TAU_PROXY_PRODUCT_CANDIDATE"}
    assert set(proxy["factor_derivation_status"]) == {
        "THEORY_CANDIDATE_FACTOR_GEOMETRY_NOT_ACCEPTED"
    }
    for col in [
        "q_source_status",
        "q_geometry_status",
        "q_projection_status",
        "q_memory_status",
        "q_resolution_status",
    ]:
        assert proxy[col].notna().all()

    accepted = gate.loc[gate["component_evidence_status"].str.startswith("SOURCE_CANDIDATE")]
    missing = gate.loc[gate["component_evidence_status"] == "MISSING_SOURCE_SUPPORT"]
    assert set(accepted["factor_derivation_status"]) == {
        "DEFINITION_DERIVED_ACCEPTED_SOURCE_GATE"
    }
    assert set(missing["factor_derivation_status"]) == {
        "DEFINITION_DERIVED_MISSING_SOURCE_GATE"
    }

    full = summary.loc[summary["split"] == "all"].iloc[0]
    assert full["n_components"] == 406
    assert full["n_proxy_components"] == 105
    assert round(float(full["median_e_tau_proxy_components"]), 6) == round(0.354025, 6)

    holdout = endpoint_summary.loc[endpoint_summary["split"] == "holdout"].iloc[0]
    assert holdout["n_galaxies"] == 44
    assert round(float(holdout["beats_old_l2_intake_fraction"]), 6) == round(0.568182, 6)
    assert round(float(holdout["beats_tpg_v6_fraction"]), 6) == round(0.454545, 6)
    assert round(float(holdout["beats_mond_fraction"]), 6) == round(0.545455, 6)
    assert float(holdout["median_source_norm_minus_old_l2_intake"]) < 0.0

    gate_report = (ROOT / "reports" / "tau_side_evidence_measure_gate.md").read_text(
        encoding="utf-8"
    )
    endpoint_report = (
        ROOT / "reports" / "tau_side_evidence_measure_l2_endpoint.md"
    ).read_text(encoding="utf-8")
    assert "E_tau = q_source q_geometry q_projection q_memory q_resolution" in gate_report
    assert "Factor-Status Discipline" in gate_report
    assert "theory-candidate factor geometry" in gate_report
    assert "Median proxy E_tau: 0.354025" in gate_report
    assert "must not be selected from" in gate_report
    assert "not validation" in endpoint_report
    assert "E_tau-minus-old-L2 RMSE" in endpoint_report


def test_l2_weight_freeze_readiness_blocks_endpoint_launch():
    audit = pd.read_csv(DATA / "morphology_information_gain_l2_weight_freeze_readiness.csv")
    component_audit = pd.read_csv(
        DATA / "morphology_information_gain_l2_weight_freeze_component_audit.csv"
    )
    summary = pd.read_csv(DATA / "morphology_information_gain_l2_weight_freeze_readiness_summary.csv")

    assert len(audit) == 175
    assert len(component_audit) == 406
    assert audit["endpoint_scores_computed"].eq(False).all()
    assert audit["endpoint_freeze_allowed"].eq(False).all()
    assert set(audit["claim_boundary"]) == {"l2_weight_freeze_readiness_audit_not_endpoint"}

    full = summary.loc[summary["split"] == "all"].iloc[0]
    assert full["n_galaxies"] == 175
    assert full["freeze_allowed_count"] == 0
    assert full["blocked_normalization_count"] == 0
    assert full["blocked_orientation_count"] == 108
    assert full["orientation_ready_count"] == 67
    assert full["orientation_blocked_count"] == 108
    assert full["blocked_memory_projection_count"] == 19
    assert full["blocked_projection_acceptance_count"] == 47
    assert full["blocked_qi_normalization_acceptance_count"] == 1
    assert full["blocked_proxy_or_missing_component_count"] == 0
    assert full["proxy_gate_resolved_count"] == 175
    assert full["normalization_candidate_present_count"] == 175
    assert full["dominant_source_candidate_count"] == 141
    assert full["dominant_proxy_or_partial_count"] == 31
    assert full["dominant_missing_source_count"] == 3
    assert full["nonzero_source_candidate_components"] == 295
    assert full["nonzero_proxy_or_partial_components"] == 105
    assert full["nonzero_missing_components"] == 6

    orientation_summary = pd.read_csv(DATA / "source_native_orientation_promotion_summary.csv")
    orientation_family = pd.read_csv(DATA / "source_native_orientation_family_gate.csv")
    orientation_component = pd.read_csv(DATA / "source_native_orientation_component_gate.csv")
    orientation_galaxy = pd.read_csv(DATA / "source_native_orientation_galaxy_gate.csv")
    orientation_full = orientation_summary.loc[orientation_summary["split"] == "all"].iloc[0]
    assert orientation_full["n_family_orientation_promoted"] == 3
    assert orientation_full["n_family_orientation_blocked"] == 1
    assert orientation_full["n_promoted_active_components"] == 295
    assert orientation_full["n_blocked_active_components"] == 111
    assert orientation_full["n_galaxies_orientation_ready"] == 67
    assert orientation_full["n_galaxies_orientation_blocked"] == 108
    assert orientation_full["endpoint_scores_computed"] == False
    thick_status = orientation_family.loc[
        orientation_family["component_family"] == "K_thick_flared",
        "promotion_status",
    ].iloc[0]
    assert thick_status == "BLOCKED_SOURCE_NATIVE_ORIENTATION_EVIDENCE_MISSING"
    assert len(orientation_component) == 406
    assert len(orientation_galaxy) == 175

    memory_projection = pd.read_csv(DATA / "memory_projection_acceptance_gate.csv")
    memory_projection_summary = pd.read_csv(DATA / "memory_projection_acceptance_summary.csv")
    inclusion = pd.read_csv(DATA / "inclusion_lane_expansion_audit.csv")
    inclusion_summary = pd.read_csv(DATA / "inclusion_lane_expansion_summary.csv")
    lane_scores = pd.read_csv(DATA / "inclusion_lane_endpoint_scores.csv")
    lane_summary = pd.read_csv(DATA / "inclusion_lane_endpoint_summary.csv")
    allowed_use_summary = pd.read_csv(DATA / "inclusion_lane_endpoint_allowed_use_summary.csv")
    lane_transitions = pd.read_csv(DATA / "inclusion_lane_information_gain_transitions.csv")
    projection_repair_summary = pd.read_csv(DATA / "projection_scale_repair_summary.csv")
    normalization_failure_summary = pd.read_csv(
        DATA / "source_normalization_failure_modes_by_lane_summary.csv"
    )
    mp_full = memory_projection_summary.loc[memory_projection_summary["split"] == "all"].iloc[0]
    assert mp_full["orientation_ready_count"] == 67
    assert mp_full["projection_ready_count"] == 71
    assert mp_full["memory_ready_or_not_required_count"] == 4
    assert mp_full["memory_projection_ready_candidate_count"] == 1
    assert mp_full["blocked_orientation_count"] == 108
    assert mp_full["blocked_projection_count"] == 47
    assert mp_full["blocked_memory_history_count"] == 19
    assert memory_projection["endpoint_scores_computed"].eq(False).all()
    assert memory_projection["uses_vobs_or_residual"].eq(False).all()
    inc_full = inclusion_summary.loc[inclusion_summary["split"] == "all"].iloc[0]
    assert inc_full["strict_ready_count"] == 1
    assert inc_full["caution_ready_count"] == 66
    assert inc_full["analysis_includable_count"] == 67
    assert inc_full["acquisition_required_count"] == 108
    assert inc_full["orientation_required_count"] == 108
    assert inc_full["projection_required_count"] == 104
    assert inc_full["memory_required_count"] == 171
    assert set(inclusion["inclusion_lane"]) == {
        "STRICT_READY_CANDIDATE",
        "CAUTION_READY_PROXY_SUPPORTED",
        "ACQUISITION_REQUIRED",
    }
    assert inclusion["endpoint_scores_computed"].eq(False).all()
    assert inclusion["uses_vobs_or_residual"].eq(False).all()
    focus = lane_summary.loc[
        (lane_summary["split"] == "holdout")
        & (lane_summary["inclusion_lane"] == "STRICT_PLUS_CAUTION")
        & (lane_summary["score_layer"] == "source_native_hard_family")
    ].iloc[0]
    assert focus["n_galaxies"] == 16
    assert focus["beats_wrong_fraction"] == 0.8125
    assert focus["beats_tpg_v6_fraction"] == 0.5
    assert focus["beats_mond_fraction"] == 0.4375
    tau_focus = lane_summary.loc[
        (lane_summary["split"] == "holdout")
        & (lane_summary["inclusion_lane"] == "STRICT_PLUS_CAUTION")
        & (lane_summary["score_layer"] == "tau_side_evidence_measure_l2")
    ].iloc[0]
    assert tau_focus["beats_tpg_v6_fraction"] == 0.375
    assert tau_focus["beats_mond_fraction"] == 0.3125
    projection_focus = allowed_use_summary.loc[
        (allowed_use_summary["split"] == "holdout")
        & (allowed_use_summary["inclusion_lane"] == "CAUTION_READY_PROXY_SUPPORTED")
        & (allowed_use_summary["allowed_use"] == "support_lane_projection_caveat")
        & (allowed_use_summary["score_layer"] == "source_native_hard_family")
    ].iloc[0]
    assert projection_focus["n_galaxies"] == 14
    assert round(float(projection_focus["beats_wrong_fraction"]), 4) == 0.7857
    projection_tau_focus = allowed_use_summary.loc[
        (allowed_use_summary["split"] == "holdout")
        & (allowed_use_summary["inclusion_lane"] == "CAUTION_READY_PROXY_SUPPORTED")
        & (allowed_use_summary["allowed_use"] == "support_lane_projection_caveat")
        & (allowed_use_summary["score_layer"] == "tau_side_evidence_measure_l2")
    ].iloc[0]
    assert round(float(projection_tau_focus["beats_tpg_v6_fraction"]), 4) == 0.3571
    assert round(float(projection_tau_focus["beats_mond_fraction"]), 4) == 0.2857
    l2_l3 = lane_transitions.loc[
        (lane_transitions["split"] == "holdout")
        & (lane_transitions["inclusion_lane"] == "STRICT_PLUS_CAUTION")
        & (lane_transitions["transition"] == "L2_to_L3")
    ].iloc[0]
    assert l2_l3["improved_fraction"] == 0.625
    assert lane_scores["claim_boundary"].eq("inclusion_lane_endpoint_analysis_not_validation").all()

    repair_all = projection_repair_summary.loc[projection_repair_summary["split"] == "all"]
    repair_counts = {
        row["repair_status"]: int(row["n_galaxies"]) for _, row in repair_all.iterrows()
    }
    assert repair_counts == {
        "NO_PROJECTION_SCALE_REPAIR_REQUIRED": 71,
        "NEEDS_VERTICAL_GEOMETRY_SOURCE": 34,
        "NEEDS_INCLINATION_PROJECTION_REVIEW": 26,
        "NEEDS_DISTANCE_SCALE_SOURCE": 30,
        "REPAIRABLE_WITH_EXISTING_SCALE_SOURCE_PLUS_DISTANCE_AUDIT": 14,
    }
    assert projection_repair_summary["endpoint_scores_computed"].eq(False).all()
    assert set(projection_repair_summary["claim_boundary"]) == {
        "projection_scale_repair_audit_not_endpoint"
    }

    projection_failure = normalization_failure_summary.loc[
        (normalization_failure_summary["split"] == "holdout")
        & (
            normalization_failure_summary["inclusion_lane"]
            == "CAUTION_READY_PROXY_SUPPORTED"
        )
        & (
            normalization_failure_summary["allowed_use"]
            == "support_lane_projection_caveat"
        )
        & (
            normalization_failure_summary["failure_mode"]
            == "PROJECTION_SCALE_NORMALIZATION_FAILURE"
        )
    ].iloc[0]
    assert projection_failure["n_galaxies"] == 7
    assert projection_failure["hard_beats_wrong_fraction"] == 1.0
    assert projection_failure["tau_beats_tpg_v6_fraction"] == 0.0
    assert projection_failure["tau_beats_mond_fraction"] == 0.0
    partly_transfer = normalization_failure_summary.loc[
        (normalization_failure_summary["split"] == "holdout")
        & (
            normalization_failure_summary["inclusion_lane"]
            == "CAUTION_READY_PROXY_SUPPORTED"
        )
        & (
            normalization_failure_summary["allowed_use"]
            == "support_lane_projection_caveat"
        )
        & (
            normalization_failure_summary["failure_mode"]
            == "SPECIFICITY_AND_BASELINE_PARTLY_TRANSFER"
        )
    ].iloc[0]
    assert partly_transfer["n_galaxies"] == 4
    assert set(normalization_failure_summary["claim_boundary"]) == {
        "source_normalization_failure_modes_by_lane_not_endpoint"
    }

    statuses = set(component_audit["component_evidence_status"])
    assert "SOURCE_CANDIDATE_HI_TAIL_READY" in statuses
    assert "SOURCE_CANDIDATE_S4G_SCALE_READY" in statuses
    assert "SOURCE_CANDIDATE_COMPACT_READY" in statuses
    assert "PROXY_OR_PARTIAL_SOURCE_ONLY" in statuses

    report = (
        ROOT / "reports" / "morphology_information_gain_l2_weight_freeze_readiness.md"
    ).read_text(encoding="utf-8")
    assert "Endpoint-freeze allowed: 0" in report
    assert "Proxy-gate blocker resolved by derived coarse-grid E_tau product: 175" in report
    assert "Blocked by missing Tau-side normalization: 0" in report
    assert "Source-native orientation ready after promotion gate: 67" in report
    assert "Blocked by source-native orientation promotion: 108" in report
    assert "Blocked by projection acceptance after orientation: 47" in report
    assert "Blocked by memory/history acceptance after orientation and projection: 19" in report
    assert "Blocked by q_i/normalization acceptance after memory/projection: 1" in report
    assert "Formula-conditional normalization candidates present: 175" in report
    assert "protocol safeguard" in report
    assert "not a negative" in report
    assert "empirical result" in report

    orientation_report = (ROOT / "reports" / "source_native_orientation_promotion_gate.md").read_text(
        encoding="utf-8"
    )
    assert "Family orientations promoted: 3/4" in orientation_report
    assert "Family orientations blocked: 1/4" in orientation_report
    assert "Active components promoted: 295/406" in orientation_report
    assert "Galaxies orientation-ready: 67/175" in orientation_report
    assert "not empirical validation" in orientation_report

    memory_projection_report = (
        ROOT / "reports" / "memory_projection_acceptance_gate.md"
    ).read_text(encoding="utf-8")
    assert "Memory/projection ready candidates after orientation: 1" in memory_projection_report
    assert "Blocked by projection after orientation: 47" in memory_projection_report
    assert "Blocked by memory/history after orientation and projection: 19" in memory_projection_report
    assert "rotation-inferred component is inverse diagnostic information" in memory_projection_report

    inclusion_report = (ROOT / "reports" / "inclusion_lane_expansion_audit.md").read_text(
        encoding="utf-8"
    )
    assert "Strict-ready candidates: 1/175" in inclusion_report
    assert "Caution/proxy-supported rows: 66/175" in inclusion_report
    assert "Analysis-includable strict+caution rows: 67/175" in inclusion_report
    assert "Acquisition-required rows: 108/175" in inclusion_report
    assert "Caution rows are not accepted evidence" in inclusion_report

    lane_report = (ROOT / "reports" / "inclusion_lane_endpoint_analysis.md").read_text(
        encoding="utf-8"
    )
    assert "Tau evidence L2 rows: 16" in lane_report
    assert "Tau evidence L2 beats TPG/v6: 0.375" in lane_report
    assert "Source-native hard-family beats wrong mean: 0.812" in lane_report
    assert "Caution Sub-Lanes" in lane_report
    assert "support_lane_projection_caveat" in lane_report
    assert "not validation" in lane_report

    projection_repair_report = (
        ROOT / "reports" / "projection_scale_repair_audit.md"
    ).read_text(encoding="utf-8")
    assert "NEEDS_VERTICAL_GEOMETRY_SOURCE" in projection_repair_report
    assert "REPAIRABLE_WITH_EXISTING_SCALE_SOURCE_PLUS_DISTANCE_AUDIT" in projection_repair_report
    assert "not an empirical validation" in projection_repair_report

    normalization_failure_report = (
        ROOT / "reports" / "source_normalization_failure_modes_by_lane.md"
    ).read_text(encoding="utf-8")
    assert "PROJECTION_SCALE_NORMALIZATION_FAILURE" in normalization_failure_report
    assert "Failure mode labels are diagnostic" in normalization_failure_report


def test_morphology_observable_gap_audit_is_claim_bounded():
    gap = pd.read_csv(DATA / "morphology_observable_gap_audit.csv")
    by_family = pd.read_csv(DATA / "morphology_observable_gap_by_family.csv")
    required_fields = {
        "galaxy",
        "formula_family",
        "scale_radius_kpc",
        "tail_inner_radius_kpc",
        "compact_support_radius_kpc",
        "thickness_h_over_rs",
        "observable_provenance",
    }
    assert required_fields.issubset(set(gap["field"]))
    assert {"accepted_available", "proxy_available"}.issubset(
        set(gap["availability_status"])
    )
    assert "not_in_current_family_set" in set(gap["availability_status"])
    assert not (gap["availability_status"] == "missing_required").any()
    scale = gap.loc[gap["field"] == "scale_radius_kpc"].iloc[0]
    assert scale["manifest_source_field"] == "scale_radius_proxy_kpc"
    assert scale["availability_status"] == "proxy_available"
    provenance = gap.loc[gap["field"] == "observable_provenance"].iloc[0]
    assert provenance["availability_status"] == "proxy_available"
    assert set(by_family["readiness_status"]) == {
        "proxy_coverage_ready_acceptance_not_ready"
    }
    report = (ROOT / "reports" / "morphology_observable_gap_audit.md").read_text(
        encoding="utf-8"
    )
    assert "coverage-rich but acceptance-limited" in report
    assert "not accepted residual-blind observables yet" in report
    assert "not an endpoint score" in report


def test_morphology_observable_source_upgrade_plan_is_claim_bounded():
    plan = pd.read_csv(DATA / "morphology_observable_source_upgrade_plan.csv")
    batches = pd.read_csv(DATA / "morphology_observable_collection_batches.csv")
    required_fields = {
        "formula_family",
        "manifest_confidence",
        "manifest_caveat",
        "scale_radius_kpc",
        "observable_provenance",
    }
    assert required_fields.issubset(set(plan["field"]))
    assert {"P0", "P1"}.issubset(set(plan["upgrade_priority"]))
    formula = plan.loc[plan["field"] == "formula_family"].iloc[0]
    assert formula["upgrade_priority"] == "P0"
    assert "required_S_tau" in formula["leak_guard"]
    scale = plan.loc[plan["field"] == "scale_radius_kpc"].iloc[0]
    assert scale["upgrade_priority"] == "P1"
    assert "residual shape" in scale["leak_guard"]
    assert "B4_blind_endpoint_run" in set(batches["batch"])
    blind = batches.loc[batches["batch"] == "B4_blind_endpoint_run"].iloc[0]
    assert "frozen matched-vs-wrong family endpoint" in blind["purpose"]
    report = (ROOT / "reports" / "morphology_observable_source_upgrade_plan.md").read_text(
        encoding="utf-8"
    )
    assert "not a data source claim" in report
    assert "source replacement, not endpoint redesign" in report
    assert "would still not by itself prove Tau Core" in report


def test_accepted_observable_manifest_template_is_endpoint_blocked():
    template = pd.read_csv(DATA / "accepted_morphology_observable_manifest_template.csv")
    validation = pd.read_csv(DATA / "accepted_observable_manifest_template_validation.csv")
    assert len(template) == 175
    assert "proxy_formula_family_for_scope" in template.columns
    assert "source_dataset" in template.columns
    assert template["source_dataset"].eq("TO_BE_FILLED").all()
    assert template["galaxy"].notna().all()
    assert template["inclination_deg"].notna().all()
    formula = validation.loc[validation["field"] == "formula_family"].iloc[0]
    assert formula["template_validation_status"] == "blocked_missing_required_accepted_source"
    assert int(formula["n_missing_rows"]) == 175
    provenance = validation.loc[validation["field"] == "observable_provenance"].iloc[0]
    assert provenance["template_validation_status"] == "blocked_missing_required_accepted_source"
    scale = validation.loc[validation["field"] == "scale_radius_kpc"].iloc[0]
    assert int(scale["n_applicable_rows"]) == 146
    assert int(scale["n_missing_rows"]) == 146
    report = (ROOT / "reports" / "accepted_observable_manifest_template_validation.md").read_text(
        encoding="utf-8"
    )
    assert "template is intentionally blocked" in report
    assert "collection-ready but endpoint-blocked" in report
    assert "not the proxy manifest" in report


def test_accepted_manifest_readiness_gate_blocks_empty_template():
    gates = pd.read_csv(DATA / "accepted_manifest_readiness_gates.csv")
    summary = pd.read_csv(DATA / "accepted_manifest_readiness_summary.csv")
    decision = summary["endpoint_readiness_decision"].iloc[0]
    assert decision == "BLOCKED_ACCEPTED_OBSERVABLES_MISSING"
    assert int(summary["n_blocked_gates"].iloc[0]) == 4
    blocked = gates.loc[gates["gate_status"] == "BLOCKED"]
    assert {
        "residual_blind_family_labels_ready",
        "quality_and_caveat_ready",
        "active_kernel_observables_ready",
        "provenance_ready",
    }.issubset(set(blocked["gate"]))
    identity = gates.loc[gates["gate"] == "row_identity_and_geometry_ready"].iloc[0]
    assert identity["gate_status"] == "PASS"
    optional = gates.loc[gates["gate"] == "optional_non_axisymmetric_not_promoted"].iloc[0]
    assert optional["gate_status"] == "PASS_OR_CAVEATED"
    report = (ROOT / "reports" / "accepted_manifest_readiness_gate.md").read_text(
        encoding="utf-8"
    )
    assert "not an endpoint score" in report
    assert "The current empty accepted manifest template is correctly blocked" in report
    assert "would not by itself imply that Tau Core" in report


def test_frozen_endpoint_launch_guard_blocks_premature_endpoint():
    launch = pd.read_csv(DATA / "frozen_endpoint_launch_guard.csv")
    blockers = pd.read_csv(DATA / "frozen_endpoint_blockers.csv")
    row = launch.iloc[0]
    assert row["launch_status"] == "LAUNCH_BLOCKED"
    assert row["readiness_decision"] == "BLOCKED_ACCEPTED_OBSERVABLES_MISSING"
    assert bool(row["endpoint_scores_computed"]) is False
    assert int(row["blocked_gate_count"]) == 4
    assert {
        "residual_blind_family_labels_ready",
        "quality_and_caveat_ready",
        "active_kernel_observables_ready",
        "provenance_ready",
    }.issubset(set(blockers["gate"]))
    report = (ROOT / "reports" / "frozen_endpoint_launch_guard.md").read_text(
        encoding="utf-8"
    )
    assert "This launch guard is not an endpoint score" in report
    assert "Launch status: `LAUNCH_BLOCKED`" in report
    assert "endpoint_scores_computed" in report
    assert "not a negative empirical result" in report


def test_external_morphology_source_registry_is_acquisition_only():
    registry = pd.read_csv(DATA / "external_morphology_source_registry.csv")
    field_map = pd.read_csv(DATA / "morphology_field_source_map.csv")
    crossmatch = pd.read_csv(DATA / "sparc_external_source_crossmatch_template.csv")
    expected_sources = {"SPARC", "S4G", "NED_NEDD", "DustPedia", "HI_SURVEYS", "PHANGS"}
    assert expected_sources == set(registry["source_id"])
    s4g = registry.loc[registry["source_id"] == "S4G"].iloc[0]
    assert s4g["priority"] == "primary_morphology_decomposition"
    assert "scale_radius_kpc" in s4g["use_for_fields"]
    phangs = registry.loc[registry["source_id"] == "PHANGS"].iloc[0]
    assert "optional" in phangs["priority"]
    hi = registry.loc[registry["source_id"] == "HI_SURVEYS"].iloc[0]
    assert "gas_extent" in hi["priority"]
    assert {"formula_family", "scale_radius_kpc", "observable_provenance"}.issubset(
        set(field_map["field"])
    )
    scale = field_map.loc[field_map["field"] == "scale_radius_kpc"].iloc[0]
    assert scale["primary_source"] == "S4G"
    assert len(crossmatch) == 175
    assert crossmatch["sparc_present"].all()
    assert crossmatch["s4g_match_status"].eq("TO_BE_CHECKED").all()
    assert crossmatch["hi_survey_match_status"].eq("TO_BE_CHECKED").all()
    assert crossmatch["accepted_observable_collection_status"].eq("NOT_STARTED").all()
    report = (ROOT / "reports" / "external_morphology_source_registry.md").read_text(
        encoding="utf-8"
    )
    assert "source-acquisition plan and crossmatch template" in report
    assert "not accepted-source coverage yet" in report or "TO_BE_CHECKED" in report
    assert "would not by itself compute endpoint scores" in report


def test_external_morphology_input_acquisition_is_partial_and_claim_bounded():
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    s4g_galaxies = pd.read_csv(DATA / "external_s4g_galaxies.csv")
    s4g_table7 = pd.read_csv(DATA / "external_s4g_table7.csv")
    candidates = pd.read_csv(DATA / "external_s4g_sparc_observable_candidates.csv")
    crossmatch = pd.read_csv(DATA / "sparc_external_source_crossmatch_acquired.csv")
    assert (ROOT / "data/external/sparc/SPARC_Lelli2016c.mrt").exists()
    assert len(sparc) == 175
    assert len(s4g_galaxies) == 2352
    assert len(s4g_table7) == 4629
    assert len(candidates) == 175
    assert int((candidates["s4g_match_status"] == "S4G_MATCHED").sum()) == 77
    assert int(
        (candidates["candidate_observable_status"] == "ACQUIRED_S4G_SPARC_DERIVED").sum()
    ) == 75
    acquired = candidates.loc[
        candidates["candidate_observable_status"] == "ACQUIRED_S4G_SPARC_DERIVED"
    ]
    assert acquired["scale_radius_kpc"].notna().all()
    assert acquired["observable_provenance"].str.contains("VizieR_J/ApJS/219/4").all()
    assert "candidate_source_observable_not_family_label_validation" in set(
        candidates["claim_boundary"]
    )
    assert len(crossmatch) == 175
    assert "PARTIAL_S4G_SCALE_CANDIDATE" in set(
        crossmatch["accepted_observable_collection_status"]
    )
    report = (ROOT / "reports" / "external_morphology_input_acquisition.md").read_text(
        encoding="utf-8"
    )
    assert "first actual external-source acquisition" in report
    assert "S4G/SPARC-derived disk scale candidates acquired: 75" in report
    assert "not a completed accepted manifest" in report
    assert "does not compute endpoint scores" in report


def test_p0_missing_data_source_acquisition_plan_uses_requested_sources():
    plan = pd.read_csv(DATA / "p0_missing_data_source_acquisition_plan.csv")
    source_summary = pd.read_csv(DATA / "p0_missing_data_source_acquisition_summary.csv")
    galaxy_summary = pd.read_csv(DATA / "p0_missing_data_source_acquisition_by_galaxy.csv")
    assert len(plan) == 52
    assert set(plan["galaxy"]) == {"NGC0300", "NGC6503", "NGC0100", "NGC0247"}
    assert {
        "S4G",
        "NED_NEDD",
        "DustPedia",
        "HI_SURVEYS",
        "PHANGS",
    } == set(source_summary["source_family"])
    assert source_summary["n_p0_galaxies"].eq(4).all()
    assert plan["source_acquisition_status"].eq("TO_BE_ACQUIRED_RESIDUAL_BLIND").all()
    assert not plan["accepted_label_output_allowed"].any()
    assert not plan["endpoint_scores_allowed"].any()
    assert not plan["endpoint_scores_computed"].any()
    assert "p0_missing_data_source_plan_not_label_not_endpoint" in set(
        plan["claim_boundary"]
    )
    hi = plan.loc[plan["review_field"] == "hi_extent_or_asymmetry_evidence"].iloc[0]
    assert "HI_SURVEYS" in hi["required_source_families"]
    bar = plan.loc[
        (plan["galaxy"] == "NGC0247") & (plan["review_field"] == "bar_m2_evidence")
    ].iloc[0]
    assert bar["acquisition_priority"] == "P0_REQUIRED_NONAXISYMMETRIC_CHECK"
    assert "PHANGS" in bar["required_source_families"]
    edge = plan.loc[
        (plan["galaxy"] == "NGC0100") & (plan["review_field"] == "edge_projection_caveat")
    ].iloc[0]
    assert edge["acquisition_priority"] == "P0_REQUIRED_PROJECTION_CHECK"
    assert len(galaxy_summary) == 4
    assert not galaxy_summary["endpoint_scores_computed"].any()
    report = (
        ROOT / "reports" / "p0_missing_data_source_acquisition_plan.md"
    ).read_text(encoding="utf-8")
    assert "use S4G, NED/NED-D, DustPedia, HI survey data, and PHANGS" in report
    assert "not an accepted morphology manifest" in report
    assert "not an endpoint score" in report
    assert "TO_BE_ACQUIRED_RESIDUAL_BLIND" in report


def test_p0_requested_source_family_availability_is_preflight_only():
    availability = pd.read_csv(DATA / "p0_requested_source_family_availability.csv")
    summary = pd.read_csv(DATA / "p0_requested_source_family_availability_summary.csv")
    assert len(availability) == 20
    assert set(availability["galaxy"]) == {"NGC0300", "NGC6503", "NGC0100", "NGC0247"}
    assert {
        "S4G",
        "NED_NEDD",
        "DustPedia",
        "HI_SURVEYS",
        "PHANGS",
    } == set(availability["source_family"])
    assert (
        availability.loc[availability["source_family"] == "S4G", "availability_status"]
        .eq("PARTIAL_SOURCE_READY")
        .all()
    )
    assert (
        availability.loc[
            availability["source_family"] == "NED_NEDD", "availability_status"
        ]
        .eq("LOOKUP_READY")
        .all()
    )
    dust = availability.loc[availability["source_family"] == "DustPedia"]
    assert int((dust["availability_status"] == "MATCHED_SOURCE_EVIDENCE_REVIEW_PENDING").sum()) == 1
    assert int((dust["availability_status"] == "NO_DIRECT_DUSTPEDIA_MATCH").sum()) == 3
    hi = availability.loc[availability["source_family"] == "HI_SURVEYS"]
    assert hi["availability_status"].eq("HI_SOURCE_EVIDENCE_READY_REVIEW_PENDING").all()
    ngc247_phangs = availability.loc[
        (availability["galaxy"] == "NGC0247")
        & (availability["source_family"] == "PHANGS")
    ].iloc[0]
    assert ngc247_phangs["availability_status"] == "NO_PHANGS_COVERAGE_FOR_REQUIRED_OPTIONAL_BRANCH"
    other_phangs = availability.loc[
        (availability["galaxy"] != "NGC0247")
        & (availability["source_family"] == "PHANGS")
    ]
    assert other_phangs["availability_status"].eq("NO_PHANGS_SAMPLE_COVERAGE").all()
    assert not availability["accepted_label_output_allowed"].any()
    assert not availability["endpoint_scores_allowed"].any()
    assert not availability["endpoint_scores_computed"].any()
    assert "p0_requested_source_availability_not_label_not_endpoint" in set(
        availability["claim_boundary"]
    )
    assert len(summary) == 5
    assert int(summary["n_to_be_queried"].sum()) == 0
    assert int(summary["n_no_coverage"].sum()) == 7
    assert int(summary["n_review_pending"].sum()) == 5
    report = (
        ROOT / "reports" / "p0_requested_source_family_availability.md"
    ).read_text(encoding="utf-8")
    assert "availability preflight only" in report
    assert "DustPedia is directly matched only for NGC0300" in report
    assert "PHANGS public sample" in report
    assert "not an accepted morphology manifest" in report
    assert "not an endpoint score" in report


def test_p0_dustpedia_hi_phangs_source_evidence_and_response_draft_are_blocked():
    source_summary = pd.read_csv(DATA / "p0_external_source_evidence_summary.csv")
    dust = pd.read_csv(DATA / "p0_dustpedia_source_matches.csv")
    phangs = pd.read_csv(DATA / "p0_phangs_source_matches.csv")
    hi = pd.read_csv(DATA / "p0_hi_source_evidence.csv")
    draft = pd.read_csv(DATA / "p0_source_assisted_review_response_draft.csv")
    validation = pd.read_csv(DATA / "p0_source_assisted_review_response_validation.csv")

    assert set(source_summary["galaxy"]) == {"NGC0300", "NGC6503", "NGC0100", "NGC0247"}
    assert source_summary.set_index("galaxy").loc["NGC0300", "dustpedia_status"] == "MATCHED_SOURCE_EVIDENCE"
    assert int((source_summary["dustpedia_status"] == "NO_DIRECT_DUSTPEDIA_MATCH").sum()) == 3
    assert phangs["match_status"].eq("NO_PHANGS_SAMPLE_COVERAGE").all()
    assert hi["match_status"].eq("HI_SOURCE_EVIDENCE_READY").all()
    assert hi["rhi_kpc"].notna().all()
    assert "DUSTPEDIA_HI_MATCHED" in set(hi["dustpedia_hi_status"])
    assert not dust.empty
    assert len(draft) == 4
    assert draft["draft_status"].eq("SOURCE_ASSISTED_DRAFT_REVIEW_REQUIRED").all()
    assert draft["residual_blind_family_recommendation"].eq(
        "REVIEWER_REQUIRED_NOT_ACCEPTED_LABEL"
    ).all()
    assert not draft["accepted_manifest_promotion_allowed"].any()
    assert not draft["endpoint_scores_computed"].any()
    assert validation["draft_validation_status"].eq(
        "BLOCKED_DRAFT_NOT_ACCEPTED_REVIEW"
    ).all()
    assert not validation["accepted_labels_created"].any()
    ngc247 = validation.loc[validation["galaxy"] == "NGC0247"].iloc[0]
    assert "ngc0247_phangs_velocity_field_not_available" in ngc247["blockers"]
    report = (
        ROOT / "reports" / "p0_dustpedia_hi_phangs_source_evidence.md"
    ).read_text(encoding="utf-8")
    assert "DustPedia direct matches are found for NGC0300 only" in report
    assert "PHANGS public sample coverage is not found" in report
    draft_report = (
        ROOT / "reports" / "p0_source_assisted_review_response_draft.md"
    ).read_text(encoding="utf-8")
    assert "source-assisted draft response" in draft_report
    assert "not an accepted morphology manifest" in draft_report
    assert "not an endpoint score" in draft_report


def test_accepted_morphology_manifest_is_partial_and_endpoint_blocked():
    manifest = pd.read_csv(DATA / "accepted_morphology_manifest.csv")
    validation = pd.read_csv(DATA / "accepted_morphology_manifest_validation.csv")
    by_family = pd.read_csv(DATA / "accepted_morphology_manifest_by_family.csv")
    assert len(manifest) == 175
    assert int(
        (manifest["scale_radius_source_status"] == "ACCEPTED_SOURCE_OBSERVABLE").sum()
    ) == 75
    assert int(
        (
            manifest["family_label_source_status"]
            == "REVIEW_PROXY_LABEL_NEEDS_EXTERNAL_MORPHOLOGY_AUDIT"
        ).sum()
    ) == 175
    assert (
        manifest["endpoint_eligibility_status"]
        .eq("BLOCKED_NOT_ENDPOINT_ELIGIBLE")
        .sum()
        + manifest["endpoint_eligibility_status"]
        .eq("BLOCKED_FAMILY_LABEL_AUDIT_PENDING")
        .sum()
        == 175
    )
    assert "partial_field_level_accepted_observables_not_endpoint_validation" in set(
        manifest["claim_boundary"]
    )
    scale_gate = validation.loc[
        validation["gate"] == "scale_radius_source_observables"
    ].iloc[0]
    assert scale_gate["gate_status"] == "PARTIAL_PASS"
    assert int(scale_gate["n_pass"]) == 75
    family_gate = validation.loc[
        validation["gate"] == "external_family_label_audit"
    ].iloc[0]
    assert family_gate["gate_status"] == "BLOCKED"
    assert int(family_gate["n_blocked"]) == 175
    endpoint_gate = validation.loc[validation["gate"] == "endpoint_eligibility"].iloc[0]
    assert endpoint_gate["gate_status"] == "BLOCKED"
    assert int(endpoint_gate["n_pass"]) == 0
    exp = by_family.loc[by_family["formula_family"] == "K_exponential_disk"].iloc[0]
    assert int(exp["n_scale_radius_accepted"]) == 13
    assert int(exp["n_kernel_complete"]) == 13
    report = (ROOT / "reports" / "accepted_morphology_manifest.md").read_text(
        encoding="utf-8"
    )
    assert "partial accepted morphology-observable manifest" in report
    assert "Accepted S4G/SPARC scale-radius observables: 75" in report
    assert "Endpoint-ready rows: 0" in report
    assert "not an endpoint score" in report


def test_accepted_morphology_manifest_audit_identifies_next_pool():
    audit = pd.read_csv(DATA / "accepted_morphology_manifest_audit.csv")
    summary = pd.read_csv(DATA / "accepted_morphology_manifest_audit_summary.csv")
    assert len(audit) == 175
    near_lane = "NEAR_TERM_EXPONENTIAL_DISK_FAMILY_LABEL_AUDIT_POOL"
    near = audit.loc[audit["audit_lane"] == near_lane]
    assert len(near) == 13
    assert near["formula_family"].eq("K_exponential_disk").all()
    assert near["scale_radius_source_status"].eq("ACCEPTED_SOURCE_OBSERVABLE").all()
    assert near["primary_blocker"].eq("external_family_label_audit_only").all()
    assert (
        "accepted_manifest_audit_not_endpoint_score_not_family_validation"
        in set(audit["audit_claim_boundary"])
    )
    exp_summary = summary.loc[
        (summary["formula_family"] == "K_exponential_disk")
        & (summary["audit_lane"] == near_lane)
    ].iloc[0]
    assert int(exp_summary["n_rows"]) == 13
    assert int(exp_summary["n_accepted_scale"]) == 13
    assert int(exp_summary["n_s4g_matched"]) == 13
    assert "S4G_EXPDISK_SUPPORT" in set(audit["s4g_component_support_status"])
    report = (ROOT / "reports" / "accepted_morphology_manifest_audit.md").read_text(
        encoding="utf-8"
    )
    assert "closest near-term lane" in report
    assert "not an endpoint score" in report
    assert "does not promote proxy family labels" in report


def test_exponential_disk_family_label_audit_strengthens_near_term_pool():
    audit = pd.read_csv(DATA / "exponential_disk_family_label_audit.csv")
    summary = pd.read_csv(DATA / "exponential_disk_family_label_audit_summary.csv")
    assert len(audit) == 13
    assert audit["external_family_label"].eq("K_exponential_disk").all()
    assert audit["endpoint_scores_computed"].eq(False).all()
    strict = audit.loc[
        audit["narrow_dry_run_lane"] == "STRICT_NARROW_DRY_RUN_READY_CANDIDATE"
    ]
    caveated = audit.loc[
        audit["narrow_dry_run_lane"] == "CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL"
    ]
    assert len(strict) == 6
    assert len(caveated) == 7
    assert strict["external_family_label_status"].eq(
        "ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG"
    ).all()
    assert set(caveated["external_family_label_status"]) == {
        "ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_BAR",
        "ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON",
    }
    assert (
        "external_family_label_audit_not_endpoint_score_not_empirical_validation"
        in set(audit["claim_boundary"])
    )
    assert int(summary["n_rows"].sum()) == 13
    assert not summary["endpoint_scores_computed"].any()
    report = (ROOT / "reports" / "exponential_disk_family_label_audit.md").read_text(
        encoding="utf-8"
    )
    assert "Strict external expdisk support: 6" in report
    assert "Caveated external disk support: 7" in report
    assert "not an endpoint score" in report


def test_exponential_disk_narrow_dry_run_is_mixed_and_claim_bounded():
    amplitudes = pd.read_csv(DATA / "exponential_disk_narrow_dry_run_amplitudes.csv")
    scores = pd.read_csv(DATA / "exponential_disk_narrow_dry_run_scores_by_galaxy.csv")
    summary = pd.read_csv(DATA / "exponential_disk_narrow_dry_run_summary.csv")
    points = pd.read_csv(DATA / "exponential_disk_narrow_dry_run_points.csv")
    assert len(scores) == 13
    assert points["galaxy"].nunique() == 13
    assert set(amplitudes["amplitude_policy"]) == {
        "frozen_global_train_beta",
        "shrink_global_to_all13_0_25",
        "shrink_global_to_all13_0_50",
        "pool_fit_beta_all13",
        "pool_fit_beta_strict6",
        "leave_one_galaxy_out_beta_all13",
    }
    assert amplitudes.loc[
        amplitudes["amplitude_policy"] == "frozen_global_train_beta",
        "overfit_diagnostic",
    ].iloc[0] == False
    assert amplitudes.loc[
        amplitudes["amplitude_policy"] == "pool_fit_beta_all13",
        "overfit_diagnostic",
    ].iloc[0] == True
    strict_all13 = summary.loc[
        (summary["narrow_dry_run_lane"] == "STRICT_NARROW_DRY_RUN_READY_CANDIDATE")
        & (summary["amplitude_policy"] == "pool_fit_beta_all13")
    ].iloc[0]
    assert int(strict_all13["n_galaxies"]) == 6
    assert abs(float(strict_all13["beats_tpg_v6_fraction"]) - 4 / 6) < 1.0e-12
    assert abs(float(strict_all13["beats_mond_fraction"]) - 2 / 6) < 1.0e-12
    strict_frozen = summary.loc[
        (summary["narrow_dry_run_lane"] == "STRICT_NARROW_DRY_RUN_READY_CANDIDATE")
        & (summary["amplitude_policy"] == "frozen_global_train_beta")
    ].iloc[0]
    assert abs(float(strict_frozen["beats_tpg_v6_fraction"]) - 1 / 6) < 1.0e-12
    strict_loo = summary.loc[
        (summary["narrow_dry_run_lane"] == "STRICT_NARROW_DRY_RUN_READY_CANDIDATE")
        & (summary["amplitude_policy"] == "leave_one_galaxy_out_beta_all13")
    ].iloc[0]
    assert abs(float(strict_loo["beats_tpg_v6_fraction"]) - 3 / 6) < 1.0e-12
    assert abs(float(strict_loo["beats_mond_fraction"]) - 2 / 6) < 1.0e-12
    assert "narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation" in set(
        summary["claim_boundary"]
    )
    report = (ROOT / "reports" / "exponential_disk_narrow_dry_run.md").read_text(
        encoding="utf-8"
    )
    assert "not the frozen Paper 8 endpoint" in report
    assert "leave-one-galaxy-out all13 policy beats" in report
    assert "policy is a stability check" in report


def test_exponential_disk_failure_sensitivity_is_mixed():
    scores = pd.read_csv(DATA / "exponential_disk_failure_sensitivity_scores.csv")
    summary = pd.read_csv(DATA / "exponential_disk_failure_sensitivity_summary.csv")
    best = pd.read_csv(DATA / "exponential_disk_failure_sensitivity_best_by_galaxy.csv")
    assert len(scores) == 39
    assert set(scores["scale_multiplier"]) == {0.75, 1.0, 1.25}
    strict = summary.loc[
        summary["narrow_dry_run_lane"] == "STRICT_NARROW_DRY_RUN_READY_CANDIDATE"
    ]
    assert len(strict) == 3
    at_075 = strict.loc[strict["scale_multiplier"] == 0.75].iloc[0]
    at_100 = strict.loc[strict["scale_multiplier"] == 1.0].iloc[0]
    at_125 = strict.loc[strict["scale_multiplier"] == 1.25].iloc[0]
    assert abs(float(at_075["beats_tpg_v6_fraction"]) - 3 / 6) < 1.0e-12
    assert abs(float(at_100["beats_tpg_v6_fraction"]) - 3 / 6) < 1.0e-12
    assert abs(float(at_125["beats_tpg_v6_fraction"]) - 2 / 6) < 1.0e-12
    assert abs(float(at_075["beats_mond_fraction"]) - 1 / 6) < 1.0e-12
    assert abs(float(at_100["beats_mond_fraction"]) - 2 / 6) < 1.0e-12
    assert abs(float(at_125["beats_mond_fraction"]) - 2 / 6) < 1.0e-12
    assert "beats_neither" in set(best["failure_class"])
    assert "beats_both" in set(best["failure_class"])
    assert "scale_sensitivity_diagnostic_not_endpoint_not_validation" in set(
        scores["claim_boundary"]
    )
    report = (
        ROOT / "reports" / "exponential_disk_failure_sensitivity_audit.md"
    ).read_text(encoding="utf-8")
    assert "strict lane remains mixed" in report
    assert "not an endpoint score" in report


def test_rotation_inferred_morphology_is_inverse_diagnostic_only():
    diagnostic = pd.read_csv(DATA / "rotation_inferred_morphology_diagnostic.csv")
    summary = pd.read_csv(DATA / "rotation_inferred_morphology_summary.csv")
    external = pd.read_csv(DATA / "rotation_inferred_external_expdisk_summary.csv")
    assert len(diagnostic) == 175
    assert abs(float(diagnostic["matches_predeclared_family"].mean()) - 62 / 175) < 1.0e-12
    expdisk = diagnostic.loc[diagnostic["external_family_label"].notna()]
    assert len(expdisk) == 13
    assert abs(float(expdisk["matches_external_expdisk_label"].mean()) - 4 / 13) < 1.0e-12
    assert "inverse_rotation_diagnostic_not_residual_blind_label_not_endpoint" in set(
        diagnostic["claim_boundary"]
    )
    assert {
        "K_compact_finite",
        "K_scale_tail_spiral",
        "K_exponential_disk",
        "K_thick_flared",
    }.issubset(set(diagnostic["rotation_inferred_family"]))
    assert not summary.empty
    assert not external.empty
    report = (
        ROOT / "reports" / "rotation_inferred_morphology_diagnostic.md"
    ).read_text(encoding="utf-8")
    assert "hypothesis generator only" in report
    assert "not residual-blind" in report
    assert "must not be used as accepted morphology evidence" in report


def test_morphological_memory_history_proxy_is_hypothesis_layer_only():
    proxy = pd.read_csv(DATA / "morphological_memory_history_proxy.csv")
    summary = pd.read_csv(DATA / "morphological_memory_history_proxy_summary.csv")
    external = pd.read_csv(DATA / "morphological_memory_history_proxy_external_expdisk.csv")
    assert len(proxy) == 175
    assert int((~proxy["matches_current_proxy_family"]).sum()) == 113
    expdisk = proxy.loc[proxy["external_family_label"].notna()]
    assert len(expdisk) == 13
    assert int(expdisk["external_family_mismatch"].sum()) == 9
    assert int(
        (
            expdisk["memory_history_proxy_class"]
            == "expdisk_current_with_scale_tail_readout_memory_candidate"
        ).sum()
    ) == 6
    assert int(
        (
            expdisk["memory_history_proxy_class"]
            == "expdisk_current_with_vertical_projection_memory_candidate"
        ).sum()
    ) == 3
    assert "morphological_memory_proxy_not_accepted_label_not_endpoint_validation" in set(
        proxy["claim_boundary"]
    )
    assert not summary.empty
    assert not external.empty
    report = (ROOT / "reports" / "morphological_memory_history_proxy.md").read_text(
        encoding="utf-8"
    )
    assert "hypothesis generator only" in report
    assert "not an accepted morphology label" in report
    assert "not an endpoint score" in report
    assert "future residual-blind testing" in report


def test_readout_state_vector_intake_schema_blocks_proxy_mixture_promotion():
    schema = pd.read_csv(DATA / "readout_state_vector_intake_schema.csv")
    audit = pd.read_csv(DATA / "readout_state_vector_gap_audit.csv")
    summary = pd.read_csv(DATA / "readout_state_vector_gap_summary.csv")
    components = {
        "K_exponential_disk",
        "K_scale_tail_spiral",
        "K_compact_finite",
        "K_thick_flared",
        "normalization",
        "memory_history",
    }
    assert components == set(schema["readout_component"])
    assert len(audit) == 175 * len(components)
    assert schema["forbidden_inputs"].str.contains("required_S_tau").all()
    assert schema["claim_boundary"].eq(
        "readout_state_vector_intake_not_endpoint_not_accepted_state"
    ).all()
    assert audit["claim_boundary"].eq(
        "readout_state_vector_intake_not_endpoint_not_accepted_state"
    ).all()
    assert int(audit["endpoint_ready_component"].sum()) == 0
    assert "MISSING_TAU_SIDE_NORMALIZATION_RULE" in set(summary["component_status"])
    assert "PROXY_MEMORY_SIGNAL_NEEDS_ACCEPTED_SOURCE" in set(summary["component_status"])
    norm = summary.loc[summary["readout_component"] == "normalization"].iloc[0]
    assert int(norm["n_galaxies"]) == 175
    memory_proxy = summary.loc[
        (summary["readout_component"] == "memory_history")
        & (summary["component_status"] == "PROXY_MEMORY_SIGNAL_NEEDS_ACCEPTED_SOURCE")
    ].iloc[0]
    assert int(memory_proxy["n_galaxies"]) == 113
    report = (ROOT / "reports" / "readout_state_vector_intake_schema.md").read_text(
        encoding="utf-8"
    )
    assert "accepted Tau-side readout-state vector" in report
    assert "computes no endpoint score" in report
    assert "accepted residual-blind source observables" in report


def test_morphology_inspection_queue_is_acquisition_plan_only():
    queue = pd.read_csv(DATA / "morphology_inspection_queue.csv")
    summary = pd.read_csv(DATA / "morphology_inspection_queue_summary.csv")
    assert len(queue) == 175
    tier_counts = queue["inspection_priority_tier"].value_counts().to_dict()
    assert tier_counts["P0"] == 4
    assert tier_counts["P1"] == 18
    top_p0 = set(
        queue.loc[queue["inspection_priority_tier"] == "P0", "galaxy"].tolist()
    )
    assert top_p0 == {"NGC0300", "NGC6503", "NGC0100", "NGC0247"}
    assert not queue["accepted_label_output_allowed"].any()
    assert not queue["endpoint_scores_allowed"].any()
    assert "morphology_inspection_queue_not_accepted_label_not_endpoint" in set(
        queue["claim_boundary"]
    )
    assert not summary.empty
    report = (ROOT / "reports" / "morphology_inspection_queue.md").read_text(
        encoding="utf-8"
    )
    assert "acquisition and" in report
    assert "not an accepted morphology manifest" in report
    assert "not an endpoint score" in report
    assert "residual-blind source collection only" in report


def test_p0_morphology_inspection_packets_are_blank_review_templates():
    index = pd.read_csv(DATA / "p0_morphology_inspection_packet_index.csv")
    needs = pd.read_csv(DATA / "p0_morphology_inspection_source_needs.csv")
    assert len(index) == 4
    assert set(index["galaxy"]) == {"NGC0300", "NGC6503", "NGC0100", "NGC0247"}
    assert not index["accepted_label_output_allowed"].any()
    assert not index["endpoint_scores_allowed"].any()
    assert "p0_morphology_packets_not_accepted_label_not_endpoint" in set(
        index["claim_boundary"]
    )
    assert {
        "residual_blind_multiband_image_morphology_label",
        "deep_optical_or_ir_outer_disk_profile",
        "hi_extent_or_asymmetry",
    }.issubset(set(needs["source"]))
    for packet_path in index["packet_path"]:
        packet = (ROOT / packet_path).read_text(encoding="utf-8")
        assert "Blank Review Fields" in packet
        assert "Residual-blind family label recommended for future endpoint:" in packet
        assert "Forbidden Inputs" in packet
        assert "endpoint residual gain" in packet
        assert "not an endpoint score" in packet
    report = (ROOT / "reports" / "p0_morphology_inspection_packets.md").read_text(
        encoding="utf-8"
    )
    assert "manual residual-blind" in report
    assert "not accepted labels" in report
    assert "not endpoint scores" in report


def test_p0_external_imaging_request_manifest_is_source_request_only():
    manifest = pd.read_csv(DATA / "p0_external_imaging_request_manifest.csv")
    summary = pd.read_csv(DATA / "p0_external_imaging_request_summary.csv")
    assert len(manifest) == 4
    assert set(manifest["galaxy"]) == {"NGC0300", "NGC6503", "NGC0100", "NGC0247"}
    assert manifest["ra_deg"].notna().all()
    assert manifest["dec_deg"].notna().all()
    fov = manifest.set_index("galaxy")["suggested_fov_arcmin"].to_dict()
    assert abs(float(fov["NGC0100"]) - 8.000) < 1.0e-12
    assert abs(float(fov["NGC0247"]) - 29.745) < 1.0e-12
    assert abs(float(fov["NGC0300"]) - 20.288) < 1.0e-12
    assert abs(float(fov["NGC6503"]) - 10.030) < 1.0e-12
    assert not manifest["accepted_label_output_allowed"].any()
    assert not manifest["endpoint_scores_allowed"].any()
    assert "p0_external_imaging_request_not_morphology_label_not_endpoint" in set(
        manifest["claim_boundary"]
    )
    for column in [
        "ned_url",
        "simbad_url",
        "skyview_dss2_red_url",
        "skyview_2mass_ks_url",
        "skyview_wise_w1_url",
    ]:
        assert manifest[column].str.startswith("https://").all()
    assert not summary.empty
    report = (ROOT / "reports" / "p0_external_imaging_request_manifest.md").read_text(
        encoding="utf-8"
    )
    assert "does not download, classify" in report
    assert "not image-based validation" in report
    assert "not an endpoint score" in report


def test_p0_external_imaging_review_dashboard_is_launch_page_only():
    index = pd.read_csv(DATA / "p0_external_imaging_review_dashboard_index.csv")
    assert len(index) == 1
    assert int(index["n_galaxies"].iloc[0]) == 4
    assert index["galaxies"].iloc[0] == "NGC0100;NGC0247;NGC0300;NGC6503"
    assert not index["accepted_label_output_allowed"].any()
    assert not index["endpoint_scores_allowed"].any()
    assert "p0_imaging_review_dashboard_not_morphology_label_not_endpoint" in set(
        index["claim_boundary"]
    )
    dashboard = (ROOT / "reports" / "p0_external_imaging_review_dashboard.html").read_text(
        encoding="utf-8"
    )
    for galaxy in ["NGC0100", "NGC0247", "NGC0300", "NGC6503"]:
        assert galaxy in dashboard
    assert "DSS2 Red" in dashboard
    assert "2MASS-K" in dashboard
    assert "WISE W1" in dashboard
    assert "Blank Review Checklist" in dashboard
    assert "Forbidden inputs" in dashboard
    assert "does not classify images" in dashboard


def test_p0_skyview_availability_audit_is_source_availability_only():
    audit = pd.read_csv(DATA / "p0_skyview_availability_audit.csv")
    summary = pd.read_csv(DATA / "p0_skyview_availability_summary.csv")
    assert len(audit) == 12
    assert set(audit["galaxy"]) == {"NGC0300", "NGC6503", "NGC0100", "NGC0247"}
    assert set(audit["survey"]) == {"DSS2 Red", "2MASS-K", "WISE 3.4"}
    assert (audit["availability_status"] == "AVAILABLE").all()
    assert (audit["skyview_image_count"] >= 1).all()
    assert not audit["temporary_image_urls_recorded"].any()
    assert not audit["accepted_label_output_allowed"].any()
    assert not audit["endpoint_scores_allowed"].any()
    assert "p0_skyview_availability_not_image_classification_not_endpoint" in set(
        audit["claim_boundary"]
    )
    assert set(summary["survey"]) == {"DSS2 Red", "2MASS-K", "WISE 3.4"}
    assert (summary["n_available"] == 4).all()
    report = (ROOT / "reports" / "p0_skyview_availability_audit.md").read_text(
        encoding="utf-8"
    )
    assert "does not download" in report
    assert "temporary SkyView FITS" in report
    assert "not a morphology label" in report
    assert "not an endpoint score" in report


def test_p0_skyview_preview_images_are_source_material_only():
    manifest = pd.read_csv(DATA / "p0_skyview_preview_image_manifest.csv")
    summary = pd.read_csv(DATA / "p0_skyview_preview_image_summary.csv")
    assert len(manifest) == 12
    assert set(manifest["galaxy"]) == {"NGC0300", "NGC6503", "NGC0100", "NGC0247"}
    assert set(manifest["survey"]) == {"DSS2 Red", "2MASS-K", "WISE 3.4"}
    assert (manifest["preview_status"] == "PREVIEW_RENDERED").all()
    assert (manifest["preview_width_px"] == 300).all()
    assert (manifest["preview_height_px"] == 300).all()
    assert not manifest["image_classification_performed"].any()
    assert not manifest["accepted_label_output_allowed"].any()
    assert not manifest["endpoint_scores_allowed"].any()
    assert "p0_skyview_previews_not_image_classification_not_endpoint" in set(
        manifest["claim_boundary"]
    )
    for path in manifest["preview_png_path"]:
        assert (ROOT / path).exists()
        assert (ROOT / path).stat().st_size > 1000
    assert set(summary["survey"]) == {"DSS2 Red", "2MASS-K", "WISE 3.4"}
    assert (summary["n_rendered"] == 4).all()
    report = (ROOT / "reports" / "p0_skyview_preview_images.md").read_text(
        encoding="utf-8"
    )
    assert "not image classifications" in report
    assert "No image classification is performed" in report
    assert "No endpoint score is computed" in report


def test_p0_visual_review_template_is_blank_and_residual_blind():
    template = pd.read_csv(DATA / "p0_visual_review_template.csv")
    schema = pd.read_csv(DATA / "p0_visual_review_field_schema.csv")
    assert len(template) == 4
    assert set(template["galaxy"]) == {"NGC0300", "NGC6503", "NGC0100", "NGC0247"}
    assert (template["inspection_priority_tier"] == "P0").all()
    assert (template["preview_surveys_available"] == "2MASS-K;DSS2 Red;WISE 3.4").all()
    assert not template["accepted_label_output_allowed"].any()
    assert not template["endpoint_scores_allowed"].any()
    assert not template["image_classification_performed"].any()
    assert "p0_visual_review_template_not_accepted_label_not_endpoint" in set(
        template["claim_boundary"]
    )
    review_fields = [
        "reviewer_id",
        "review_timestamp_utc",
        "present_day_morphology_label",
        "outer_disk_lsb_tail_evidence",
        "hi_extent_or_asymmetry_evidence",
        "bar_m2_evidence",
        "edge_projection_caveat",
        "vertical_flare_warp_evidence",
        "compact_bulge_evidence",
        "ring_resonance_evidence",
        "morphological_memory_history_proxy_judgment",
        "review_confidence",
        "residual_blind_family_recommendation",
        "review_sources_used",
        "review_notes",
    ]
    for field in review_fields:
        assert (template[field] == "TO_BE_FILLED_RESIDUAL_BLIND").all()
    assert set(schema["field"]) == set(review_fields)
    assert (schema["initial_value"] == "TO_BE_FILLED_RESIDUAL_BLIND").all()
    assert schema["residual_blind_required"].all()
    assert not schema["may_use_endpoint_scores"].any()

    report = (ROOT / "reports" / "p0_visual_review_template.md").read_text(
        encoding="utf-8"
    )
    assert "not an accepted morphology manifest" in report
    assert "not an endpoint score" in report
    assert "required-S_tau" in report
    form = (ROOT / "reports" / "p0_visual_review_form.html").read_text(encoding="utf-8")
    for galaxy in ["NGC0100", "NGC0247", "NGC0300", "NGC6503"]:
        assert galaxy in form
    assert "p0_skyview_previews" in form
    assert "morphological_memory_history_proxy_judgment" in form
    assert "Forbidden inputs" in form
    assert "does not compute endpoint scores" in form


def test_p0_visual_review_completion_gate_blocks_unfilled_template():
    gates = pd.read_csv(DATA / "p0_visual_review_completion_gate.csv")
    summary = pd.read_csv(DATA / "p0_visual_review_completion_summary.csv")
    assert len(gates) == 4
    assert set(gates["galaxy"]) == {"NGC0300", "NGC6503", "NGC0100", "NGC0247"}
    assert (gates["completion_status"] == "BLOCKED_VISUAL_REVIEW_PENDING").all()
    assert (gates["n_review_fields"] == 15).all()
    assert (gates["n_pending_review_fields"] == 15).all()
    assert not gates["accepted_manifest_promotion_allowed"].any()
    assert not gates["endpoint_scores_computed"].any()
    assert "morphological_memory_history_proxy_judgment" in ";".join(
        gates["pending_review_fields"]
    )
    assert "p0_visual_review_completion_gate_not_endpoint" in set(
        gates["claim_boundary"]
    )

    row = summary.iloc[0]
    assert row["visual_review_completion_decision"] == "BLOCKED_VISUAL_REVIEW_PENDING"
    assert int(row["n_galaxies"]) == 4
    assert int(row["n_blocked_rows"]) == 4
    assert int(row["n_pending_review_fields_total"]) == 60
    assert bool(row["accepted_manifest_promotion_allowed"]) is False
    assert bool(row["endpoint_scores_computed"]) is False
    report = (ROOT / "reports" / "p0_visual_review_completion_gate.md").read_text(
        encoding="utf-8"
    )
    assert "This completion gate is not an endpoint score" in report
    assert "BLOCKED_VISUAL_REVIEW_PENDING" in report
    assert "all review fields remain residual-blind placeholders" in report
    assert "not a negative empirical result" in report


def test_p0_visual_review_handoff_is_review_task_only():
    tasks = pd.read_csv(DATA / "p0_visual_review_handoff_tasks.csv")
    summary = pd.read_csv(DATA / "p0_visual_review_handoff_summary.csv")
    assert len(tasks) == 4
    assert set(tasks["galaxy"]) == {"NGC0300", "NGC6503", "NGC0100", "NGC0247"}
    assert (tasks["review_status"] == "BLOCKED_VISUAL_REVIEW_PENDING").all()
    assert (tasks["n_pending_review_fields"] == 15).all()
    assert not tasks["accepted_manifest_promotion_allowed"].any()
    assert not tasks["endpoint_scores_computed"].any()
    assert "morphological_memory_history_proxy_judgment" in ";".join(
        tasks["required_review_fields"]
    )
    assert tasks["preview_png_paths"].str.contains("p0_skyview_previews").all()
    assert tasks["allowed_sources"].str.contains("local SkyView preview panels").all()
    assert tasks["forbidden_inputs"].str.contains("endpoint residual gain").all()
    assert "p0_visual_review_handoff_not_label_not_endpoint" in set(
        tasks["claim_boundary"]
    )

    row = summary.iloc[0]
    assert row["handoff_status"] == "READY_FOR_RESIDUAL_BLIND_HUMAN_REVIEW"
    assert int(row["n_galaxies"]) == 4
    assert int(row["n_blocked_review_rows"]) == 4
    assert int(row["n_pending_review_fields_total"]) == 60
    assert bool(row["accepted_manifest_promotion_allowed"]) is False
    assert bool(row["endpoint_scores_computed"]) is False
    report = (ROOT / "reports" / "p0_visual_review_handoff.md").read_text(
        encoding="utf-8"
    )
    assert "source-review handoff" in report
    assert "not an accepted morphology manifest" in report
    assert "not an endpoint score" in report
    form = (ROOT / "reports" / "p0_visual_review_handoff.html").read_text(
        encoding="utf-8"
    )
    for galaxy in ["NGC0100", "NGC0247", "NGC0300", "NGC6503"]:
        assert galaxy in form
    assert "Required Residual-Blind Fields" in form
    assert "Allowed Sources" in form
    assert "Forbidden inputs" in form


def test_p0_codex_source_review_response_intake_is_ready_for_audit():
    response = pd.read_csv(DATA / "p0_visual_review_response_template.csv")
    schema = pd.read_csv(DATA / "p0_visual_review_response_schema.csv")
    validation = pd.read_csv(DATA / "p0_visual_review_response_validation.csv")
    summary = pd.read_csv(DATA / "p0_visual_review_response_summary.csv")
    codex_response = pd.read_csv(DATA / "p0_codex_source_review_response.csv")
    codex_validation = pd.read_csv(DATA / "p0_codex_source_review_validation.csv")
    assert len(response) == 4
    assert set(response["galaxy"]) == {"NGC0300", "NGC6503", "NGC0100", "NGC0247"}
    assert len(codex_response) == 4
    assert len(schema) == 15
    required = schema.loc[schema["required_for_visual_review_completion"]]
    assert len(required) == 14
    assert not schema["may_use_endpoint_scores"].any()
    assert (
        validation["validation_status"]
        == "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
    ).all()
    assert (
        codex_validation["validation_status"]
        == "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
    ).all()
    assert (validation["n_required_fields"] == 14).all()
    assert (validation["n_missing_required_fields"] == 0).all()
    assert not validation["forbidden_input_detected"].any()
    assert validation["accepted_manifest_promotion_allowed"].all()
    assert not validation["endpoint_scores_computed"].any()
    assert response["reviewer_id"].eq("CODEX_SOURCE_REVIEWER_RESIDUAL_BLIND_001").all()
    assert response["residual_blind_family_recommendation"].eq("K_exponential_disk").all()
    assert response["review_notes"].str.contains("Forbidden endpoint-derived inputs were not used").all()
    assert "p0_codex_source_review_response_not_endpoint" in set(
        validation["claim_boundary"]
    )
    row = summary.iloc[0]
    assert row["response_intake_decision"] == "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
    assert int(row["n_galaxies"]) == 4
    assert int(row["n_blocked_rows"]) == 0
    assert int(row["n_missing_required_fields_total"]) == 0
    assert bool(row["accepted_manifest_promotion_allowed"]) is True
    assert bool(row["endpoint_scores_computed"]) is False
    report = (ROOT / "reports" / "p0_codex_source_review_response.md").read_text(
        encoding="utf-8"
    )
    assert "Codex/source-reviewed response" in report
    assert "not a human review" in report
    assert "not an endpoint score" in report
    assert "independent accepted-manifest audit" in report


def test_p0_response_to_manifest_promotion_gate_allows_audit_entry():
    gates = pd.read_csv(DATA / "p0_response_to_manifest_promotion_gates.csv")
    summary = pd.read_csv(DATA / "p0_response_to_manifest_promotion_summary.csv")
    assert len(gates) == 5
    blocked = gates.loc[gates["gate_status"] == "BLOCKED"]
    assert len(blocked) == 0
    assert {
        "response_intake_complete",
        "forbidden_inputs_absent",
        "review_confidence_present",
        "family_recommendation_present",
        "history_memory_judgment_present",
    } == set(gates["gate"])
    assert gates["gate_status"].eq("PASS").all()
    assert not gates["endpoint_scores_computed"].any()
    assert "p0_response_to_manifest_promotion_gate_not_endpoint" in set(
        gates["claim_boundary"]
    )

    row = summary.iloc[0]
    assert row["promotion_gate_decision"] == "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
    assert int(row["n_gates"]) == 5
    assert int(row["n_blocked_gates"]) == 0
    assert int(row["n_blocked_rows_total"]) == 0
    assert bool(row["accepted_manifest_audit_entry_allowed"]) is True
    assert bool(row["accepted_labels_created"]) is False
    assert bool(row["endpoint_scores_computed"]) is False
    report = (ROOT / "reports" / "p0_response_to_manifest_promotion_gate.md").read_text(
        encoding="utf-8"
    )
    assert "This promotion gate is not an endpoint score" in report
    assert "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT" in report
    assert "does not promote labels" in report
    assert "does not create full endpoint labels or endpoint scores" in report


def test_p0_codex_accepted_label_manifest_is_not_endpoint_launch():
    manifest = pd.read_csv(DATA / "p0_codex_accepted_label_manifest.csv")
    summary = pd.read_csv(DATA / "p0_codex_accepted_label_manifest_summary.csv")
    assert len(manifest) == 4
    assert set(manifest["galaxy"]) == {"NGC0300", "NGC6503", "NGC0100", "NGC0247"}
    assert manifest["accepted_label_status"].eq(
        "P0_CODEX_SOURCE_REVIEW_ACCEPTED_FOR_AUDIT"
    ).all()
    assert manifest["accepted_formula_family"].eq("K_exponential_disk").all()
    assert manifest["source_basis"].str.contains("no endpoint residuals used").all()
    assert not manifest["full_endpoint_manifest_row_created"].any()
    assert not manifest["endpoint_scores_computed"].any()
    assert "p0_codex_accepted_labels_not_endpoint" in set(manifest["claim_boundary"])
    row = summary.iloc[0]
    assert row["p0_label_manifest_decision"] == "P0_CODEX_SOURCE_REVIEW_LABELS_CREATED_NOT_ENDPOINT"
    assert int(row["n_p0_codex_source_review_accepted"]) == 4
    assert int(row["n_blocked"]) == 0
    assert bool(row["full_endpoint_manifest_rows_created"]) is False
    assert bool(row["endpoint_scores_computed"]) is False
    report = (ROOT / "reports" / "p0_codex_accepted_label_manifest.md").read_text(
        encoding="utf-8"
    )
    assert "P0 audit manifest only" in report
    assert "not a launch of the frozen 175-galaxy endpoint" in report


def test_p0_readout_relevant_morphology_proxy_separates_4d_handles():
    proxy = pd.read_csv(DATA / "p0_readout_relevant_morphology_proxy.csv")
    summary = pd.read_csv(DATA / "p0_readout_relevant_morphology_proxy_summary.csv")
    assert len(proxy) == 4
    assert set(proxy["galaxy"]) == {"NGC0100", "NGC0247", "NGC0300", "NGC6503"}
    required_columns = {
        "k_obs",
        "k_readout",
        "readout_proxy_source",
        "promotion_status",
        "formula_shell",
    }
    assert required_columns.issubset(proxy.columns)
    assert proxy["k_obs"].eq("K_exponential_disk").all()
    assert proxy["formula_shell"].equals(proxy["k_readout"])
    assert proxy["readout_proxy_source"].eq("p0_codex_source_review_caveat_mapping").all()
    assert int(proxy["promotion_status"].eq("K_OBS_DIRECT").sum()) == 1
    assert int(proxy["promotion_status"].eq("K_OBS_TO_K_READOUT_PROXY").sum()) == 3
    assert proxy["observed_4d_family_label"].eq("K_exponential_disk").all()
    assert not proxy["uses_rotation_residuals"].any()
    assert not proxy["endpoint_scores_computed"].any()
    assert {
        "K_clean_exponential_disk_control",
        "K_projection_corrected_expdisk",
        "K_barred_expdisk_m2_overlay",
        "K_expdisk_compact_core_overlay",
    } == set(proxy["readout_relevant_proxy_family"])
    assert "p0_readout_relevant_morphology_proxy_not_endpoint" in set(
        proxy["claim_boundary"]
    )
    assert int(summary["n_galaxies"].sum()) == 4
    assert int(summary["n_direct_k_obs"].sum()) == 1
    assert int(summary["n_proxy_promotions"].sum()) == 3
    report = (ROOT / "reports" / "p0_readout_relevant_morphology_proxy.md").read_text(
        encoding="utf-8"
    )
    assert "projected 4D morphology handles" in report
    assert "not as proven fundamental Tau-side classes" in report
    assert "plain P0 `K_exponential_disk` pilot can be weak" in report
    assert "formula shell is attached to `k_readout`, not automatically to `k_obs`" in report


def test_p0_codex_source_review_pilot_is_narrow_and_claim_bounded():
    scores = pd.read_csv(DATA / "p0_codex_source_review_pilot_scores.csv")
    summary = pd.read_csv(DATA / "p0_codex_source_review_pilot_summary.csv")
    assert len(scores) == 4
    assert set(scores["galaxy"]) == {"NGC0100", "NGC0247", "NGC0300", "NGC6503"}
    required_columns = {
        "k_obs",
        "k_readout",
        "readout_proxy_source",
        "promotion_status",
        "formula_shell",
        "scored_formula_shell",
        "readout_proxy_overlay_not_scored",
    }
    assert required_columns.issubset(scores.columns)
    assert scores["k_obs"].eq("K_exponential_disk").all()
    assert scores["scored_formula_shell"].eq("K_exponential_disk").all()
    assert int(scores["promotion_status"].eq("K_OBS_DIRECT").sum()) == 1
    assert int(scores["promotion_status"].eq("K_OBS_TO_K_READOUT_PROXY").sum()) == 3
    assert int(scores["readout_proxy_overlay_not_scored"].sum()) == 3
    assert scores["accepted_formula_family"].eq("K_exponential_disk").all()
    assert scores["primary_amplitude_policy"].eq("leave_one_galaxy_out_beta_all13").all()
    assert not scores["endpoint_scores_computed"].any()
    assert not scores["full_endpoint_manifest_row_created"].any()
    assert "p0_codex_source_review_pilot_not_endpoint" in set(scores["claim_boundary"])

    row = summary.iloc[0]
    assert row["pilot_decision"] == "P0_CODEX_SOURCE_REVIEW_PILOT_COMPLETE_NOT_ENDPOINT"
    assert int(row["n_galaxies"]) == 4
    assert int(row["n_distinct_k_readout"]) == 4
    assert int(row["n_k_obs_direct"]) == 1
    assert int(row["n_k_readout_proxy_promotions"]) == 3
    assert int(row["n_readout_proxy_overlay_not_scored"]) == 3
    assert abs(float(row["primary_beats_tpg_v6_fraction"]) - 0.75) < 1.0e-12
    assert abs(float(row["primary_beats_mond_fraction"]) - 0.25) < 1.0e-12
    assert abs(float(row["formula_shell_beats_tpg_v6_fraction"]) - 1.0) < 1.0e-12
    assert abs(float(row["formula_shell_beats_mond_fraction"]) - 0.25) < 1.0e-12
    assert bool(row["full_endpoint_manifest_rows_created"]) is False
    assert bool(row["endpoint_scores_computed"]) is False
    report = (ROOT / "reports" / "p0_codex_source_review_pilot.md").read_text(
        encoding="utf-8"
    )
    assert "not launch the frozen 175-galaxy endpoint" in report
    assert "MOND remains a hard baseline" in report
    assert "not an endpoint result" in report
    assert "The score table now separates `k_obs`, `k_readout`" in report
    assert "not yet scored with their readout-proxy shell" in report


def test_p0_review_pipeline_status_dashboard_summarizes_codex_review_chain():
    status = pd.read_csv(DATA / "p0_review_pipeline_status.csv")
    summary = pd.read_csv(DATA / "p0_review_pipeline_status_summary.csv")
    assert len(status) == 13
    assert {
        "external_imaging_request_manifest",
        "skyview_availability_audit",
        "skyview_preview_images",
        "visual_review_template",
        "visual_review_completion_gate",
        "visual_review_handoff",
        "visual_review_response_intake",
        "response_to_manifest_promotion_gate",
        "missing_data_source_acquisition_plan",
        "dustpedia_hi_phangs_source_evidence",
        "source_assisted_review_response_draft",
        "p0_codex_accepted_label_manifest",
        "requested_source_family_availability",
    } == set(status["stage"])
    blocked = status[status["stage_status"].str.startswith("BLOCKED")]
    assert len(blocked) == 2
    assert {
        "visual_review_completion_gate",
        "source_assisted_review_response_draft",
    } == set(blocked["stage"])
    assert not status["endpoint_scores_computed"].any()
    assert status["p0_codex_source_review_labels_created"].any()
    assert not status["full_endpoint_labels_created"].any()
    assert "p0_review_pipeline_status_not_label_not_endpoint" in set(
        status["claim_boundary"]
    )

    row = summary.iloc[0]
    assert row["pipeline_decision"] == "P0_CODEX_SOURCE_REVIEW_LABELS_READY_FULL_ENDPOINT_BLOCKED"
    assert int(row["n_stages"]) == 13
    assert int(row["n_blocked_stages"]) == 2
    assert bool(row["endpoint_scores_computed"]) is False
    assert bool(row["p0_codex_source_review_labels_created"]) is True
    assert bool(row["full_endpoint_labels_created"]) is False
    report = (ROOT / "reports" / "p0_review_pipeline_status_dashboard.md").read_text(
        encoding="utf-8"
    )
    assert "status dashboard only" in report
    assert "P0 source-reviewed labels may exist" in report
    assert "computes no endpoint scores" in report
    form = (ROOT / "reports" / "p0_review_pipeline_status_dashboard.html").read_text(
        encoding="utf-8"
    )
    assert "P0_CODEX_SOURCE_REVIEW_LABELS_READY_FULL_ENDPOINT_BLOCKED" in form
    assert "response_to_manifest_promotion_gate" in form
    assert "missing_data_source_acquisition_plan" in form
    assert "dustpedia_hi_phangs_source_evidence" in form
    assert "source_assisted_review_response_draft" in form
    assert "p0_codex_accepted_label_manifest" in form
    assert "requested_source_family_availability" in form
    assert "creates no full endpoint labels" in form


def test_synthetic_fixture_is_not_mistaken_for_empirical_result():
    demo = pd.read_csv(DATA / "synthetic_forward_gate_demo.csv")
    matched = float(demo.loc[demo["condition"] == "matched_family", "rms"].iloc[0])
    wrong = float(demo.loc[demo["condition"] == "wrong_family_mean", "rms"].iloc[0])
    shuffled = float(demo.loc[demo["condition"] == "shuffled_K_median", "rms"].iloc[0])
    assert matched < wrong
    assert matched < shuffled
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "protocol fixtures" in readme
    assert "not an empirical matched-family endpoint result" in readme


def test_s4g75_direct_kernel_promotions_preserve_claim_boundaries():
    measurements = pd.read_csv(DATA / "s4g75_direct_kernel_measurements.csv")
    assert len(measurements) == 15
    direct = measurements[measurements["direct_measurement_status"].str.startswith("DIRECT_")]
    assert set(direct["galaxy"]) == {"NGC5907", "NGC5985"}

    ngc5907 = direct[direct["galaxy"] == "NGC5907"].iloc[0]
    assert ngc5907["kernel_parameter_filled"] == "thickness_h_over_rs"
    assert abs(float(ngc5907["dimensionless_value"]) - 0.1733207190160832) < 1.0e-12

    ngc5985 = direct[direct["galaxy"] == "NGC5985"].iloc[0]
    assert ngc5985["kernel_parameter_filled"] == "compact_support_radius_kpc"
    assert abs(float(ngc5985["value_kpc"]) - 0.735239339935394) < 1.0e-12

    promoted = pd.read_csv(DATA / "s4g75_promoted_kernel_observable_fill.csv")
    overrides = promoted[
        promoted["promotion_override_status"] == "DIRECT_KERNEL_MEASUREMENT_OVERRIDE"
    ]
    assert set(overrides["galaxy"]) == {"NGC5907", "NGC5985"}

    gate = pd.read_csv(DATA / "s4g75_kernel_ready_endpoint_subset_status.csv")
    counts = dict(zip(gate["kernel_promotion_status"], gate["n_galaxies"]))
    assert counts == {
        "KERNEL_PROXY_ONLY": 7,
        "KERNEL_READY_CONDITIONAL": 6,
        "KERNEL_READY_STRICT": 2,
    }

    tail = pd.read_csv(DATA / "s4g75_tail_rhi_promotion_attempt.csv")
    assert len(tail) == 6
    assert set(tail["promotion_attempt_status"]) == {
        "THEOREM_CONDITIONAL_RHI_UPPER_CUTOFF_CANDIDATE"
    }
    assert not tail["strict_kernel_ready"].any()
    assert not tail["endpoint_scores_allowed"].any()
    assert not tail["endpoint_scores_computed"].any()

    ledger = pd.read_csv(DATA / "s4g75_remaining_kernel_acquisition_ledger.csv")
    assert len(ledger) == 13
    assert int((ledger["blocker_class"] == "SCALE_TAIL_TRANSITION_MISSING").sum()) == 6
    assert int((ledger["blocker_class"] == "VERTICAL_KERNEL_MISSING").sum()) == 7
    assert set(
        ledger.loc[
            ledger["acquisition_priority"]
            == "P0_EDGE_ON_VERTICAL_GEOMETRY_LITERATURE_SEARCH",
            "galaxy",
        ]
    ) == {"NGC2683", "NGC3972"}
    assert not ledger["strict_kernel_ready"].any()
    assert not ledger["endpoint_scores_allowed"].any()
    assert not ledger["endpoint_scores_computed"].any()

    literature = pd.read_csv(DATA / "s4g75_literature_kernel_source_hits.csv")
    ngc2683_hit = literature[literature["galaxy"] == "NGC2683"].iloc[0]
    assert (
        ngc2683_hit["literature_status"]
        == "DIRECT_LITERATURE_FLARE_PROFILE_READY_MAPPING_REQUIRED"
    )
    assert "flare_H_start_kpc=0.5" in ngc2683_hit["numeric_kernel_fields"]
    assert (
        ngc2683_hit["endpoint_mapping_status"]
        == "MAPPING_REQUIRED_PROFILE_TO_THICK_FLARED_EXECUTABLE_KERNEL"
    )
    assert not literature["strict_kernel_ready"].any()
    assert not literature["endpoint_scores_allowed"].any()
    assert not literature["endpoint_scores_computed"].any()

    vertical_search = pd.read_csv(DATA / "s4g75_vertical_source_search_audit.csv")
    assert set(vertical_search["galaxy"]) == {"NGC2683", "NGC3972", "NGC4088"}
    assert not vertical_search["endpoint_scores_allowed"].any()
    assert not vertical_search["endpoint_scores_computed"].any()
    ngc3972_search = vertical_search[vertical_search["galaxy"] == "NGC3972"]
    assert "HI_MORPHOLOGY_SOURCE_READY_VERTICAL_KERNEL_NOT_EXTRACTED" in set(
        ngc3972_search["source_status"]
    )
    ngc4088_search = vertical_search[vertical_search["galaxy"] == "NGC4088"]
    assert "WHISP_WARP_ASYMMETRY_SOURCE_READY_PROFILE_NOT_EXTRACTED" in set(
        ngc4088_search["source_status"]
    )
    assert not ngc4088_search["direct_profile_extracted"].any()

    vertical_summary = pd.read_csv(DATA / "s4g75_vertical_source_search_summary.csv")
    direct_profile_by_galaxy = dict(
        zip(vertical_summary["galaxy"], vertical_summary["any_direct_profile"])
    )
    assert direct_profile_by_galaxy["NGC2683"]
    assert not direct_profile_by_galaxy["NGC3972"]
    assert not direct_profile_by_galaxy["NGC4088"]

    ngc4088_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_warp_asymmetry_extraction_gate.csv"
    )
    ngc4088_row = ngc4088_gate.iloc[0]
    assert ngc4088_row["galaxy"] == "NGC4088"
    assert ngc4088_row["extraction_status"] == (
        "OBJECT_WARP_EVIDENCE_READY_PROFILE_KERNEL_BLOCKED"
    )
    assert abs(float(ngc4088_row["source_native_inclination_deg"]) - 69.0) < 1.0e-12
    assert abs(float(ngc4088_row["source_native_hi_diameter_arcmin"]) - 8.5) < 1.0e-12
    assert bool(ngc4088_row["closure_source_development_allowed"]) is True
    assert bool(ngc4088_row["closure_source_endpoint_allowed"]) is False
    assert bool(ngc4088_row["endpoint_scores_allowed"]) is False
    assert "theta_warp_R_or_PA_R_profile" in ngc4088_row["missing_for_profile_kernel"]

    ngc4088_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_warp_asymmetry_extraction_summary.csv"
    )
    assert int(ngc4088_summary["missing_profile_kernel_observable_count"].iloc[0]) == 5
    assert not ngc4088_summary["endpoint_scores_allowed"].any()

    ngc4088_prekernel = pd.read_csv(
        DATA / "s4g75_ngc4088_warp_prekernel_observables.csv"
    )
    prekernel_values = dict(
        zip(ngc4088_prekernel["observable"], ngc4088_prekernel["value"])
    )
    assert abs(prekernel_values["R_HI_from_WHISP_diameter_kpc"] - 22.25295929988883) < 1.0e-12
    assert abs(prekernel_values["R_HI_over_SPARC_Rdisk"] - 8.625178023212725) < 1.0e-12
    assert abs(prekernel_values["R_HI_over_S4G_scale_radius"] - 6.834638436291303) < 1.0e-12
    assert prekernel_values["qualitative_warp_asymmetry_score"] == 1.0
    assert not ngc4088_prekernel["endpoint_scores_allowed"].any()
    assert not ngc4088_prekernel["endpoint_scores_computed"].any()

    ngc4088_prekernel_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_warp_prekernel_observable_summary.csv"
    )
    assert (
        ngc4088_prekernel_summary["profile_kernel_status"].iloc[0]
        == "PREKERNEL_READY_PROFILE_KERNEL_BLOCKED"
    )
    assert (
        abs(
            float(
                ngc4088_prekernel_summary[
                    "whisp_vs_sparc_rhi_fractional_difference"
                ].iloc[0]
            )
            - 0.00013300224219456346
        )
        < 1.0e-15
    )
    assert not ngc4088_prekernel_summary["endpoint_scores_allowed"].any()

    ngc4088_mapping = pd.read_csv(
        DATA / "s4g75_ngc4088_warp_closure_mapping_rule.csv"
    )
    mapping_row = ngc4088_mapping.iloc[0]
    assert mapping_row["mapping_status"] == (
        "FORMULA_DEVELOPMENT_SHELL_PROFILE_ONSET_BLOCKED"
    )
    assert mapping_row["dimensional_status"] == "DIMENSIONLESS_BASIS_ONLY"
    assert "C_warp" in mapping_row["basis_formula"]
    assert not bool(mapping_row["uses_vobs_or_residual"])
    assert not bool(mapping_row["endpoint_scores_allowed"])

    ngc4088_basis = pd.read_csv(DATA / "s4g75_ngc4088_warp_closure_basis_grid.csv")
    assert len(ngc4088_basis) == 30
    assert not ngc4088_basis["uses_vobs_or_residual"].any()
    assert not ngc4088_basis["endpoint_scores_allowed"].any()
    inner = ngc4088_basis[
        ngc4088_basis["x_R_over_RHI"] <= ngc4088_basis["x_warp_onset_control"]
    ]
    assert (inner["basis_value"] == 0.0).all()
    outer = ngc4088_basis[ngc4088_basis["x_R_over_RHI"] == 1.0]
    assert (outer["basis_value"] == outer["q_warp"]).all()

    ngc4088_mapping_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_warp_closure_mapping_summary.csv"
    )
    assert int(ngc4088_mapping_summary["n_basis_grid_rows"].iloc[0]) == 30
    assert (
        ngc4088_mapping_summary["required_source_native_onset"].iloc[0]
        == "warp_onset_radius_or_PA_profile"
    )
    assert not ngc4088_mapping_summary["endpoint_scores_allowed"].any()

    ngc4088_onset_protocol = pd.read_csv(
        DATA / "s4g75_ngc4088_warp_onset_extraction_protocol.csv"
    )
    accepted_routes = set(ngc4088_onset_protocol["accepted_source_class"])
    assert accepted_routes == {
        "RADIAL_PA_PROFILE",
        "RADIAL_WARP_ANGLE_PROFILE",
        "CHANNEL_MAP_DIGITIZATION",
        "TEXT_ONLY_QUALITATIVE_WARP",
    }
    text_only = ngc4088_onset_protocol[
        ngc4088_onset_protocol["accepted_source_class"] == "TEXT_ONLY_QUALITATIVE_WARP"
    ].iloc[0]
    assert text_only["onset_definition"] == "not accepted for x_w"
    assert text_only["dimension_check"] == "insufficient dimensional information"
    assert not ngc4088_onset_protocol["endpoint_allowed_after_extraction"].any()

    ngc4088_onset_status = pd.read_csv(DATA / "s4g75_ngc4088_warp_onset_status.csv")
    status_row = ngc4088_onset_status.iloc[0]
    assert status_row["current_source_status"] == "WARP_PRESENT_ONSET_NOT_EXTRACTED"
    assert not bool(status_row["x_warp_onset_available"])
    assert not bool(status_row["uses_vobs_or_residual"])
    assert not bool(status_row["endpoint_scores_allowed"])

    ngc4088_onset_summary = pd.read_csv(DATA / "s4g75_ngc4088_warp_onset_summary.csv")
    assert int(ngc4088_onset_summary["n_accepted_source_classes"].iloc[0]) == 3
    assert (
        ngc4088_onset_summary["protocol_status"].iloc[0]
        == "RESIDUAL_BLIND_EXTRACTION_PROTOCOL_READY_ONSET_MISSING"
    )
    assert not ngc4088_onset_summary["endpoint_scores_allowed"].any()

    ngc4088_digitization = pd.read_csv(
        DATA / "s4g75_ngc4088_digitization_target_manifest.csv"
    )
    assert len(ngc4088_digitization) == 2
    assert set(ngc4088_digitization["digitization_route"]) == {
        "CHANNEL_MAP_DIGITIZATION",
        "PV_OR_CONTINUATION_CROSS_CHECK",
    }
    assert ngc4088_digitization["page_render_available"].all()
    assert not ngc4088_digitization["x_warp_onset_available"].any()
    assert not ngc4088_digitization["endpoint_scores_allowed"].any()
    primary_digitization = ngc4088_digitization[
        ngc4088_digitization["digitization_route"] == "CHANNEL_MAP_DIGITIZATION"
    ].iloc[0]
    assert int(primary_digitization["source_pdf_page"]) == 76
    assert primary_digitization["rendered_page_png"].endswith("ngc4088_page_76-076.png")
    assert "onset_radius_arcmin" in primary_digitization["required_measurement_outputs"]

    ngc4088_digitization_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_digitization_target_summary.csv"
    )
    assert int(ngc4088_digitization_summary["n_digitization_targets"].iloc[0]) == 2
    assert (
        ngc4088_digitization_summary["manifest_status"].iloc[0]
        == "DIGITIZATION_TARGET_READY_XW_NOT_EXTRACTED"
    )
    assert not ngc4088_digitization_summary["endpoint_scores_allowed"].any()

    ngc4088_worksheet = pd.read_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_worksheet.csv"
    )
    assert len(ngc4088_worksheet) == 24
    assert int((ngc4088_worksheet["panel_status"] == "MEASUREMENT_TARGET").sum()) == 23
    assert set(ngc4088_worksheet["panel_status"]) == {
        "MEASUREMENT_TARGET",
        "NON_TARGET_EDGE_PANEL",
    }
    assert not ngc4088_worksheet["uses_vobs_or_residual"].any()
    assert not ngc4088_worksheet["x_warp_onset_available"].any()
    assert not ngc4088_worksheet["endpoint_scores_allowed"].any()
    assert not ngc4088_worksheet["endpoint_scores_computed"].any()
    measurement_fields = [
        "measurement_inner_axis_px",
        "measurement_outer_ridge_axis_px",
        "measurement_onset_radius_arcmin",
        "measurement_uncertainty_arcmin",
    ]
    measurement_targets = ngc4088_worksheet[
        ngc4088_worksheet["panel_status"] == "MEASUREMENT_TARGET"
    ]
    for field in measurement_fields:
        assert measurement_targets[field].fillna("").eq("").all()

    ngc4088_worksheet_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_worksheet_summary.csv"
    )
    worksheet_row = ngc4088_worksheet_summary.iloc[0]
    assert int(worksheet_row["n_panel_rows"]) == 24
    assert int(worksheet_row["n_measurement_targets"]) == 23
    assert int(worksheet_row["n_empty_measurement_fields"]) == 92
    assert worksheet_row["worksheet_status"] == "PANEL_WORKSHEET_READY_MEASUREMENTS_EMPTY"
    assert not bool(worksheet_row["x_warp_onset_available"])
    assert not bool(worksheet_row["endpoint_scores_allowed"])
    assert (ROOT / worksheet_row["overlay_png"]).exists()

    ngc4088_protocol = pd.read_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_protocol.csv"
    )
    assert len(ngc4088_protocol) == 6
    assert set(ngc4088_protocol["rule_id"]) == {
        "SOURCE_LOCK",
        "INNER_AXIS",
        "OUTER_AXES_BY_SIDE",
        "ONSET_BY_SIDE",
        "SIDE_COMBINATION",
        "UNCERTAINTY_AND_CROSSCHECK",
    }
    assert "rotation residual" in ";".join(ngc4088_protocol["forbidden_inputs"])

    ngc4088_response = pd.read_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_response_template.csv"
    ).iloc[0]
    assert ngc4088_response["response_status"] == "MANUAL_FIRST_PASS_COMPLETE"
    assert abs(float(ngc4088_response["inner_disk_axis_pa_deg"]) - 229.0) < 1.0e-12
    assert (
        abs(float(ngc4088_response["outer_ridge_axis_side_a_pa_deg"]) - 319.0)
        < 1.0e-12
    )
    assert (
        abs(float(ngc4088_response["outer_ridge_axis_side_b_pa_deg"]) - 229.0)
        < 1.0e-12
    )
    assert abs(float(ngc4088_response["onset_radius_side_a_arcmin"]) - 1.2) < 1.0e-12
    assert abs(float(ngc4088_response["onset_radius_side_b_arcmin"]) - 1.6) < 1.0e-12
    assert ngc4088_response["side_combination_rule_applied"] == "MIN_SIDE"
    assert bool(ngc4088_response["accepted_x_w_available"]) is True
    assert bool(ngc4088_response["endpoint_scores_allowed"]) is False

    ngc4088_response_validation = pd.read_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_response_validation.csv"
    ).iloc[0]
    assert (
        ngc4088_response_validation["validation_status"]
        == "READY_FOR_XW_CONVERSION_AUDIT"
    )
    assert int(ngc4088_response_validation["n_missing_required_fields"]) == 0
    assert bool(ngc4088_response_validation["accepted_x_w_available"]) is True
    assert bool(ngc4088_response_validation["endpoint_scores_allowed"]) is False

    ngc4088_xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    assert ngc4088_xw["conversion_status"] == "XW_READY_FOR_MAPPING_RULE"
    assert abs(float(ngc4088_xw["hi_radius_arcmin"]) - 4.25) < 1.0e-12
    assert abs(float(ngc4088_xw["combined_onset_arcmin"]) - 1.2) < 1.0e-12
    assert abs(float(ngc4088_xw["x_warp_onset"]) - 0.2823529411764706) < 1.0e-12
    assert abs(float(ngc4088_xw["x_warp_uncertainty"]) - 0.07058823529411765) < 1.0e-12
    assert bool(ngc4088_xw["accepted_for_mapping_rule"]) is True
    assert bool(ngc4088_xw["endpoint_scores_allowed"]) is False

    ngc4088_filled = pd.read_csv(
        DATA / "s4g75_ngc4088_filled_warp_closure_mapping.csv"
    ).iloc[0]
    assert (
        ngc4088_filled["mapping_status"]
        == "FILLED_SOURCE_BASIS_PROFILE_NORMALIZATION_OPEN"
    )
    assert abs(float(ngc4088_filled["filled_x_warp_onset"]) - 0.2823529411764706) < 1.0e-12
    assert bool(ngc4088_filled["accepted_for_mapping_rule"]) is True
    assert bool(ngc4088_filled["endpoint_scores_allowed"]) is False

    ngc4088_filled_profile = pd.read_csv(
        DATA / "s4g75_ngc4088_filled_warp_closure_profile.csv"
    )
    assert len(ngc4088_filled_profile) == 16
    assert set(ngc4088_filled_profile["turn_on_power_control"]) == {1.0, 2.0}
    onset_rows = ngc4088_filled_profile[
        (
            ngc4088_filled_profile["x_R_over_RHI"]
            == ngc4088_filled_profile["filled_x_warp_onset"]
        )
    ]
    assert len(onset_rows) == 2
    assert (onset_rows["filled_basis_value"] == 0.0).all()
    outer_rows = ngc4088_filled_profile[ngc4088_filled_profile["x_R_over_RHI"] == 1.0]
    assert (outer_rows["filled_basis_value"] == outer_rows["q_warp"]).all()
    assert not ngc4088_filled_profile["endpoint_scores_allowed"].any()

    ngc4088_norm_constants = pd.read_csv(
        DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_constants.csv"
    )
    constants = dict(
        zip(ngc4088_norm_constants["constant_name"], ngc4088_norm_constants["constant_value"])
    )
    assert abs(constants["q_warp"] - 1.0) < 1.0e-12
    assert abs(constants["c_warp_candidate"] - 0.2823529411764706) < 1.0e-12
    assert abs(constants["velocity_scale_candidate"] - 29480.89) < 1.0e-9
    assert abs(constants["onset_over_rdisk"] - 2.4353443830247694) < 1.0e-9
    assert set(ngc4088_norm_constants["proof_status"]) == {
        "THEORY_CONDITIONAL",
        "SOURCE_NATIVE_QUALITATIVE_GATE",
        "XW_FILLED_SOURCE_FRACTION",
        "SOURCE_CATALOG_SCALE_CANDIDATE",
        "DERIVED_FROM_FILLED_ONSET",
    }

    ngc4088_norm_profile = pd.read_csv(
        DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_profile.csv"
    )
    assert len(ngc4088_norm_profile) == 16
    assert set(ngc4088_norm_profile["normalization_status"]) == {
        "THEORY_CONDITIONAL_FILLED_SOURCE_RULE"
    }
    assert abs(
        float(ngc4088_norm_profile["normalization_prefactor_km2_s2"].iloc[0])
        - 8324.016
    ) < 1.0e-9
    assert not ngc4088_norm_profile["accepted_for_endpoint"].any()

    ngc4088_norm_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_summary.csv"
    )
    assert len(ngc4088_norm_summary) == 2
    assert set(ngc4088_norm_summary["turn_on_power_control"]) == {1.0, 2.0}
    assert (
        abs(ngc4088_norm_summary["max_delta_v2_candidate"] - 8324.016) < 1.0e-9
    ).all()
    assert not ngc4088_norm_summary["accepted_for_endpoint"].any()

    ngc4088_preflight = pd.read_csv(
        DATA / "s4g75_ngc4088_readout_preflight_profile.csv"
    )
    assert len(ngc4088_preflight) == 12
    assert not ngc4088_preflight["uses_vobs_for_generation"].any()
    assert not ngc4088_preflight["endpoint_scores_allowed"].any()
    assert not ngc4088_preflight["endpoint_scores_computed"].any()
    assert (ngc4088_preflight["delta_v2_warp_candidate_p1"] >= 0.0).all()
    assert (ngc4088_preflight["delta_v2_warp_candidate_p2"] >= 0.0).all()
    assert (
        ngc4088_preflight["v_warp_candidate_p1"]
        >= ngc4088_preflight["vn"] - 1.0e-12
    ).all()
    assert (
        ngc4088_preflight["v_warp_candidate_p2"]
        >= ngc4088_preflight["vn"] - 1.0e-12
    ).all()

    ngc4088_preflight_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_readout_preflight_summary.csv"
    ).iloc[0]
    assert int(ngc4088_preflight_summary["n_points"]) == 12
    assert (
        ngc4088_preflight_summary["profile_status"]
        == "PREDECLARED_READOUT_EXPORT_NOT_ENDPOINT"
    )
    assert abs(float(ngc4088_preflight_summary["max_delta_v2_p1"]) - 7921.121953) < 1.0e-6
    assert abs(float(ngc4088_preflight_summary["max_delta_v2_p2"]) - 7630.509854) < 1.0e-6
    assert abs(float(ngc4088_preflight_summary["max_v_candidate_p1"]) - 190.380771) < 1.0e-6
    assert abs(float(ngc4088_preflight_summary["max_v_candidate_p2"]) - 189.581582) < 1.0e-6
    assert bool(ngc4088_preflight_summary["endpoint_scores_allowed"]) is False

    ngc4088_norm_formula = pd.read_csv(
        DATA / "s4g75_ngc4088_physical_normalization_formula.csv"
    ).iloc[0]
    assert ngc4088_norm_formula["formula_id"] == "NGC4088-WARP-DELTA-V2-CANDIDATE-001"
    assert "x_w Vflat^2 C_warp" in ngc4088_norm_formula["candidate_formula"]
    assert (
        ngc4088_norm_formula["proof_status"]
        == "FORMULA_CONDITIONAL_NOT_TAU_SIDE_LAW"
    )
    assert (
        abs(float(ngc4088_norm_formula["normalization_prefactor_km2_s2"]) - 8324.016)
        < 1.0e-9
    )

    ngc4088_norm_law_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_physical_normalization_law_gate.csv"
    )
    assert len(ngc4088_norm_law_gate) == 9
    norm_law_status = dict(
        zip(ngc4088_norm_law_gate["gate_id"], ngc4088_norm_law_gate["gate_status"])
    )
    assert {
        gate_id for gate_id, status in norm_law_status.items() if status == "PASS"
    } == {
        "DIMENSIONAL_CONSISTENCY",
        "PREFACTOR_REPRODUCED",
        "SOURCE_ONSET_SUPPRESSION",
        "POSITIVE_WARP_ORIENTATION",
        "RESIDUAL_BLIND_EXPORT",
    }
    assert {
        gate_id for gate_id, status in norm_law_status.items() if status == "FORMULA_CONDITIONAL"
    } == {"FORMULA_LEVEL_CANDIDATE"}
    assert {
        gate_id for gate_id, status in norm_law_status.items() if status == "BLOCKED"
    } == {
        "TAU_SIDE_VARIATIONAL_OR_CLOSURE_DERIVATION",
        "SCALE_UNIQUENESS",
        "POPULATION_TRANSFER",
    }
    assert not ngc4088_norm_law_gate["endpoint_scores_allowed"].any()

    ngc4088_norm_law_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_physical_normalization_law_summary.csv"
    ).iloc[0]
    assert int(ngc4088_norm_law_summary["n_gates"]) == 9
    assert int(ngc4088_norm_law_summary["n_pass"]) == 5
    assert int(ngc4088_norm_law_summary["n_formula_conditional"]) == 1
    assert int(ngc4088_norm_law_summary["n_blocked"]) == 3
    assert (
        ngc4088_norm_law_summary["law_status"]
        == "FORMULA_CONDITIONAL_PHYSICAL_LAW_BLOCKED"
    )
    assert bool(ngc4088_norm_law_summary["endpoint_scores_allowed"]) is False

    ngc4088_scale_uniqueness = pd.read_csv(
        DATA / "s4g75_ngc4088_scale_uniqueness_audit.csv"
    )
    assert len(ngc4088_scale_uniqueness) == 5
    assert set(ngc4088_scale_uniqueness["scale_id"]) == {
        "CURRENT_XW_VFLAT2",
        "XW_MEDIAN_VN2",
        "XW_MEDIAN_VV62",
        "CLOSURE_FRACTION_MEDIAN_VN2",
        "XW_CLOSURE_FRACTION_MEDIAN_VN2",
    }
    assert (ngc4088_scale_uniqueness["scale_value_km2_s2"] > 0.0).all()
    assert not ngc4088_scale_uniqueness["uses_vobs_or_residual"].any()
    assert not ngc4088_scale_uniqueness["endpoint_scores_allowed"].any()
    current_scale = ngc4088_scale_uniqueness[
        ngc4088_scale_uniqueness["scale_id"] == "CURRENT_XW_VFLAT2"
    ].iloc[0]
    assert abs(float(current_scale["scale_value_km2_s2"]) - 8324.016) < 1.0e-9
    assert current_scale["selection_status"] == "SELECTED_CANDIDATE_NOT_UNIQUE"

    ngc4088_scale_uniqueness_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_scale_uniqueness_summary.csv"
    ).iloc[0]
    assert int(ngc4088_scale_uniqueness_summary["n_scale_candidates"]) == 5
    assert int(ngc4088_scale_uniqueness_summary["n_dimensionally_valid"]) == 5
    assert int(ngc4088_scale_uniqueness_summary["n_residual_blind"]) == 5
    assert (
        ngc4088_scale_uniqueness_summary["scale_uniqueness_decision"]
        == "BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES"
    )
    assert bool(ngc4088_scale_uniqueness_summary["endpoint_scores_allowed"]) is False

    ngc4088_scale_selection_criteria = pd.read_csv(
        DATA / "s4g75_ngc4088_tau_side_scale_selection_criteria.csv"
    )
    assert len(ngc4088_scale_selection_criteria) == 5
    assert set(ngc4088_scale_selection_criteria["criterion_id"]) == {
        "C1_RESIDUAL_BLIND",
        "C2_SOURCE_ONSET_COUPLED",
        "C3_ASYMPTOTIC_READOUT_CARRIER",
        "C4_NO_EXTERNAL_CLOSURE_COMPARATOR",
        "C5_MINIMAL_SINGLE_SOURCE_FACTOR",
    }

    ngc4088_scale_selection_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_tau_side_scale_selection_gate.csv"
    )
    assert len(ngc4088_scale_selection_gate) == 5
    selected_scale = ngc4088_scale_selection_gate[
        ngc4088_scale_selection_gate["selection_gate_status"]
        == "SELECTED_BY_MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE"
    ]
    assert set(selected_scale["scale_id"]) == {"CURRENT_XW_VFLAT2"}
    assert int(selected_scale.iloc[0]["n_selection_criteria_passed"]) == 5
    assert not ngc4088_scale_selection_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_scale_selection_gate["endpoint_scores_allowed"].any()
    failed_by_scale = dict(
        zip(
            ngc4088_scale_selection_gate["scale_id"],
            ngc4088_scale_selection_gate["failed_criteria"],
        )
    )
    assert failed_by_scale["CURRENT_XW_VFLAT2"] == "none"
    assert failed_by_scale["XW_MEDIAN_VN2"] == "C3_ASYMPTOTIC_READOUT_CARRIER"
    assert "C4_NO_EXTERNAL_CLOSURE_COMPARATOR" in failed_by_scale["XW_MEDIAN_VV62"]
    assert "C5_MINIMAL_SINGLE_SOURCE_FACTOR" in failed_by_scale[
        "XW_CLOSURE_FRACTION_MEDIAN_VN2"
    ]

    ngc4088_scale_selection_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_tau_side_scale_selection_summary.csv"
    ).iloc[0]
    assert (
        ngc4088_scale_selection_summary["selection_principle"]
        == "MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE"
    )
    assert int(ngc4088_scale_selection_summary["n_candidates"]) == 5
    assert int(ngc4088_scale_selection_summary["n_selected_candidates"]) == 1
    assert ngc4088_scale_selection_summary["selected_scale_ids"] == "CURRENT_XW_VFLAT2"
    assert (
        ngc4088_scale_selection_summary["selection_status"]
        == "THEORY_SELECTION_CONDITIONAL_CURRENT_ONLY"
    )
    assert (
        ngc4088_scale_selection_summary["law_status_after_selection"]
        == "SELECTION_RULE_CONDITIONAL_NOT_DERIVED_LAW"
    )
    assert bool(ngc4088_scale_selection_summary["endpoint_scores_allowed"]) is False

    ngc4088_scale_derivation_skeleton = pd.read_csv(
        DATA / "s4g75_ngc4088_tau_side_scale_derivation_skeleton.csv"
    ).iloc[0]
    assert ngc4088_scale_derivation_skeleton["selected_scale_id"] == "CURRENT_XW_VFLAT2"
    assert "x_w * Vflat^2" in ngc4088_scale_derivation_skeleton["conditional_statement"]
    assert (
        ngc4088_scale_derivation_skeleton["current_status"]
        == "DERIVATION_SKELETON_NOT_PROOF"
    )

    ngc4088_scale_derivation_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_tau_side_scale_derivation_gate.csv"
    )
    assert len(ngc4088_scale_derivation_gate) == 7
    derivation_status = dict(
        zip(
            ngc4088_scale_derivation_gate["gate_id"],
            ngc4088_scale_derivation_gate["gate_status"],
        )
    )
    assert {
        gate_id for gate_id, status in derivation_status.items() if status == "PASS"
    } == {"G1_DIMENSIONAL_LIMIT"}
    assert {
        gate_id
        for gate_id, status in derivation_status.items()
        if status == "FORMULA_CONDITIONAL"
    } == {
        "G2_SOURCE_ONSET_LOCALITY",
        "G4_EXTERNAL_COMPARATOR_AUTONOMY",
        "G5_MINIMAL_SOURCE_FACTOR_RULE",
    }
    assert {
        gate_id for gate_id, status in derivation_status.items() if status == "BLOCKED"
    } == {
        "G3_ASYMPTOTIC_CARRIER_DOMINANCE",
        "G6_TAU_SIDE_CLOSURE_FUNCTIONAL",
        "G7_POPULATION_TRANSFER",
    }
    assert not ngc4088_scale_derivation_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_scale_derivation_gate["endpoint_scores_allowed"].any()

    ngc4088_scale_derivation_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_tau_side_scale_derivation_summary.csv"
    ).iloc[0]
    assert int(ngc4088_scale_derivation_summary["n_gates"]) == 7
    assert int(ngc4088_scale_derivation_summary["n_pass"]) == 1
    assert int(ngc4088_scale_derivation_summary["n_formula_conditional"]) == 3
    assert int(ngc4088_scale_derivation_summary["n_blocked"]) == 3
    assert (
        ngc4088_scale_derivation_summary["derivation_status"]
        == "DERIVATION_BLOCKED_SELECTION_RULE_AUDITED"
    )
    assert (
        ngc4088_scale_derivation_summary["law_status_after_derivation_gate"]
        == "NOT_DERIVED_TAU_SIDE_LAW"
    )
    assert bool(ngc4088_scale_derivation_summary["endpoint_scores_allowed"]) is False

    ngc4088_asymptotic_carrier = pd.read_csv(
        DATA / "s4g75_ngc4088_asymptotic_carrier_candidate.csv"
    ).iloc[0]
    assert ngc4088_asymptotic_carrier["selected_scale_id"] == "CURRENT_XW_VFLAT2"
    assert (
        ngc4088_asymptotic_carrier["carrier_id"]
        == "VFLAT2_ASYMPTOTIC_CARRIER_CANDIDATE"
    )
    assert abs(float(ngc4088_asymptotic_carrier["carrier_value_km2_s2"]) - 29480.89) < 1.0e-9
    assert ngc4088_asymptotic_carrier["unit"] == "km2_s2"
    assert (
        ngc4088_asymptotic_carrier["current_interpretation"]
        == "SOURCE_CATALOG_SCALE_CANDIDATE_NOT_DERIVED_CARRIER"
    )

    ngc4088_asymptotic_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_asymptotic_carrier_dominance_gate.csv"
    )
    assert len(ngc4088_asymptotic_gate) == 8
    asymptotic_status = dict(
        zip(ngc4088_asymptotic_gate["gate_id"], ngc4088_asymptotic_gate["gate_status"])
    )
    assert {
        gate_id for gate_id, status in asymptotic_status.items() if status == "PASS"
    } == {
        "A1_CATALOG_ASYMPTOTIC_SCALE_AVAILABLE",
        "A2_DIMENSIONAL_CARRIER",
        "A3_POINT_SAMPLED_MEDIANS_REJECTED",
        "A4_EXTERNAL_COMPARATOR_REJECTED",
    }
    assert {
        gate_id
        for gate_id, status in asymptotic_status.items()
        if status == "FORMULA_CONDITIONAL"
    } == {"A5_ASYMPTOTIC_READOUT_INTERPRETATION"}
    assert {
        gate_id for gate_id, status in asymptotic_status.items() if status == "BLOCKED"
    } == {
        "A6_TAU_CLOSURE_DERIVES_VFLAT",
        "A7_UNIQUENESS_AGAINST_OTHER_ASYMPTOTIC_CARRIERS",
        "A8_POPULATION_TRANSFER",
    }
    assert not ngc4088_asymptotic_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_asymptotic_gate["endpoint_scores_allowed"].any()

    ngc4088_asymptotic_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_asymptotic_carrier_dominance_summary.csv"
    ).iloc[0]
    assert int(ngc4088_asymptotic_summary["n_gates"]) == 8
    assert int(ngc4088_asymptotic_summary["n_pass"]) == 4
    assert int(ngc4088_asymptotic_summary["n_formula_conditional"]) == 1
    assert int(ngc4088_asymptotic_summary["n_blocked"]) == 3
    assert (
        ngc4088_asymptotic_summary["dominance_status"]
        == "ASYMPTOTIC_CARRIER_DOMINANCE_NOT_DERIVED"
    )
    assert (
        ngc4088_asymptotic_summary["law_status"]
        == "VFLAT2_SOURCE_CANDIDATE_NOT_TAU_SIDE_CARRIER_PROOF"
    )
    assert bool(ngc4088_asymptotic_summary["endpoint_scores_allowed"]) is False

    ngc4088_closure_functional = pd.read_csv(
        DATA / "s4g75_ngc4088_closure_functional_requirement.csv"
    ).iloc[0]
    assert (
        ngc4088_closure_functional["functional_id"]
        == "NGC4088_WARP_ASYMMETRY_CLOSURE_FUNCTIONAL_REQUIREMENT"
    )
    assert "J_tau[lambda_w]" in ngc4088_closure_functional["required_form"]
    assert "lambda_w = sigma_warp q_warp x_w Vflat^2" in ngc4088_closure_functional[
        "solved_scale_if_derived"
    ]
    assert (
        ngc4088_closure_functional["current_status"]
        == "FUNCTIONAL_REQUIREMENT_NOT_CONSTRUCTED"
    )

    ngc4088_closure_functional_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_closure_functional_requirement_gate.csv"
    )
    assert len(ngc4088_closure_functional_gate) == 8
    functional_status = dict(
        zip(
            ngc4088_closure_functional_gate["gate_id"],
            ngc4088_closure_functional_gate["gate_status"],
        )
    )
    assert {
        gate_id for gate_id, status in functional_status.items() if status == "PASS"
    } == {
        "F1_SOURCE_BASIS_AVAILABLE",
        "F2_DIMENSIONFUL_CARRIER_CANDIDATE_AVAILABLE",
    }
    assert {
        gate_id
        for gate_id, status in functional_status.items()
        if status == "FORMULA_CONDITIONAL"
    } == {
        "F3_FUNCTIONAL_VARIABLE_DECLARED",
        "F7_COMPARATOR_AUTONOMY_DERIVED",
    }
    assert {
        gate_id for gate_id, status in functional_status.items() if status == "BLOCKED"
    } == {
        "F4_CLOSURE_COST_DEFINED",
        "F5_EULER_CONDITION_DERIVED",
        "F6_ASYMPTOTIC_CARRIER_TERM_DERIVED",
        "F8_POPULATION_TRANSFER_REQUIRED",
    }
    assert not ngc4088_closure_functional_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_closure_functional_gate["endpoint_scores_allowed"].any()

    ngc4088_closure_functional_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_closure_functional_requirement_summary.csv"
    ).iloc[0]
    assert int(ngc4088_closure_functional_summary["n_gates"]) == 8
    assert int(ngc4088_closure_functional_summary["n_pass"]) == 2
    assert int(ngc4088_closure_functional_summary["n_formula_conditional"]) == 2
    assert int(ngc4088_closure_functional_summary["n_blocked"]) == 4
    assert (
        ngc4088_closure_functional_summary["functional_status"]
        == "CLOSURE_FUNCTIONAL_REQUIREMENT_SPECIFIED_NOT_DERIVED"
    )
    assert (
        ngc4088_closure_functional_summary["law_status"]
        == "NO_TAU_SIDE_EULER_CLOSURE_DERIVATION_YET"
    )
    assert bool(ngc4088_closure_functional_summary["endpoint_scores_allowed"]) is False

    ngc4088_euler_ansatz = pd.read_csv(
        DATA / "s4g75_ngc4088_minimal_euler_ansatz.csv"
    ).iloc[0]
    assert ngc4088_euler_ansatz["ansatz_id"] == "MINIMAL_QUADRATIC_TARGET_EULER_ANSATZ"
    assert "J_min(lambda_w)" in ngc4088_euler_ansatz["functional_ansatz"]
    assert "dJ_min/dlambda_w" in ngc4088_euler_ansatz["stationarity_equation"]
    assert abs(float(ngc4088_euler_ansatz["solved_lambda_km2_s2"]) - 8324.016) < 1.0e-9
    assert (
        ngc4088_euler_ansatz["proof_status"]
        == "EULER_SOLVES_TARGET_GIVEN_ANSATZ"
    )

    ngc4088_euler_gate = pd.read_csv(DATA / "s4g75_ngc4088_minimal_euler_ansatz_gate.csv")
    assert len(ngc4088_euler_gate) == 7
    euler_status = dict(zip(ngc4088_euler_gate["gate_id"], ngc4088_euler_gate["gate_status"]))
    assert {
        gate_id for gate_id, status in euler_status.items() if status == "PASS"
    } == {
        "E1_DIMENSIONAL_TARGET_VALID",
        "E2_STATIONARITY_ALGEBRA",
        "E7_ENDPOINT_BLINDNESS",
    }
    assert {
        gate_id for gate_id, status in euler_status.items() if status == "FORMULA_CONDITIONAL"
    } == {
        "E3_CONVEXITY",
        "E6_NONTRIVIAL_SOURCE_COUPLING",
    }
    assert {
        gate_id for gate_id, status in euler_status.items() if status == "BLOCKED"
    } == {
        "E4_TARGET_TERM_TAU_ORIGIN",
        "E5_WEIGHT_OR_STIFFNESS_DERIVATION",
    }
    assert not ngc4088_euler_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_euler_gate["endpoint_scores_allowed"].any()

    ngc4088_euler_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_minimal_euler_ansatz_summary.csv"
    ).iloc[0]
    assert int(ngc4088_euler_summary["n_gates"]) == 7
    assert int(ngc4088_euler_summary["n_pass"]) == 3
    assert int(ngc4088_euler_summary["n_formula_conditional"]) == 2
    assert int(ngc4088_euler_summary["n_blocked"]) == 2
    assert (
        ngc4088_euler_summary["euler_status"]
        == "EULER_CONDITION_SOLVED_GIVEN_TARGET_ANSATZ"
    )
    assert (
        ngc4088_euler_summary["law_status"]
        == "TARGET_FUNCTIONAL_NOT_TAU_SIDE_DERIVED"
    )
    assert bool(ngc4088_euler_summary["endpoint_scores_allowed"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc4088_b2_source_load_closure_functional_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    source_load_functional = pd.read_csv(
        DATA / "ngc4088_b2_source_load_closure_functional.csv"
    ).iloc[0]
    assert source_load_functional["functional_id"] == "B2_SOURCE_LOAD_CLOSURE_FUNCTIONAL"
    assert "J_load[lambda_w]" in source_load_functional["functional"]
    assert "dJ_load/dlambda_w" in source_load_functional["euler_equation"]
    assert (
        source_load_functional["mathematical_status"]
        == "EULER_DERIVED_FROM_CONDITIONAL_SOURCE_LOAD_FUNCTIONAL"
    )
    assert source_load_functional["tau_side_law_status"] == "SOURCE_LOAD_AND_CARRIER_ORIGIN_OPEN"
    assert bool(source_load_functional["formula_freeze_alignment_pass"]) is True
    assert abs(float(source_load_functional["numeric_lambda_w_km2_s2"]) - 8795.11175237) < 1.0e-5

    source_load_gates = pd.read_csv(
        DATA / "ngc4088_b2_source_load_closure_functional_gate.csv"
    )
    assert len(source_load_gates) == 8
    source_load_status = dict(
        zip(source_load_gates["gate_id"], source_load_gates["gate_status"])
    )
    assert {
        gate_id for gate_id, status in source_load_status.items() if status == "PASS"
    } == {
        "SL1_KERNEL_IS_RESIDUAL_BLIND_AND_DIMENSIONLESS",
        "SL2_SOURCE_LOAD_ALIGNED_TO_FREEZE",
        "SL3_EULER_STATIONARITY",
        "SL4_ZERO_SOURCE_LIMIT",
        "SL5_INACTIVE_WINDOW_LIMIT",
    }
    assert {
        gate_id for gate_id, status in source_load_status.items() if status == "OPEN"
    } == {
        "SL6_SOURCE_LOAD_ORIGIN",
        "SL7_ASYMPTOTIC_CARRIER_ORIGIN",
        "SL8_CROSS_TERM_BOUND",
    }
    assert not source_load_gates["endpoint_scores_allowed"].any()
    assert not source_load_gates["uses_vobs_or_residual"].any()

    source_load_summary = pd.read_csv(
        DATA / "ngc4088_b2_source_load_closure_functional_summary.csv"
    ).iloc[0]
    assert source_load_summary["closure_functional_status"] == (
        "SOURCE_LOAD_CLOSURE_FUNCTIONAL_CONSTRUCTED_CONDITIONALLY"
    )
    assert int(source_load_summary["n_pass"]) == 5
    assert int(source_load_summary["n_open"]) == 3
    assert bool(source_load_summary["law_level_closed"]) is False
    assert bool(source_load_summary["endpoint_scores_allowed"]) is False
    assert bool(source_load_summary["uses_vobs_or_residual"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc4088_b2_frozen_asymptotic_carrier_theorem_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    frozen_carrier_theorem = pd.read_csv(
        DATA / "ngc4088_b2_frozen_asymptotic_carrier_theorem.csv"
    ).iloc[0]
    assert frozen_carrier_theorem["theorem_id"] == (
        "FROZEN_MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_THEOREM"
    )
    assert frozen_carrier_theorem["theorem_status"] == (
        "CONDITIONAL_CARRIER_THEOREM_FOR_FROZEN_PROTOCOL"
    )
    assert frozen_carrier_theorem["law_status"] == "FINAL_TAU_SIDE_CARRIER_PROOF_OPEN"
    assert bool(frozen_carrier_theorem["formula_freeze_alignment_pass"]) is True
    assert abs(float(frozen_carrier_theorem["carrier_value_km2_s2"]) - 29480.89) < 1.0e-9
    assert abs(float(frozen_carrier_theorem["lambda_tau_km2_s2"]) - 8795.11175237) < 1.0e-5

    frozen_carrier_criteria = pd.read_csv(
        DATA / "ngc4088_b2_frozen_asymptotic_carrier_criteria.csv"
    )
    assert len(frozen_carrier_criteria) == 8
    frozen_carrier_status = dict(
        zip(frozen_carrier_criteria["criterion_id"], frozen_carrier_criteria["criterion_status"])
    )
    assert {
        criterion_id
        for criterion_id, status in frozen_carrier_status.items()
        if status == "PASS"
    } == {
        "FC1_RESIDUAL_BLIND",
        "FC2_SOURCE_NATIVE_ASYMPTOTIC",
        "FC3_SOURCE_ONSET_COUPLED",
        "FC4_NO_EXTERNAL_COMPARATOR",
        "FC5_MINIMAL_FACTORIZATION",
        "FC6_FREEZE_ALIGNMENT",
    }
    assert frozen_carrier_status["FC7_ALTERNATIVE_CARRIER_EXCLUSION"] == "CONDITIONAL"
    assert frozen_carrier_status["FC8_POPULATION_TRANSFER"] == "OPEN_FOR_CLAIMS"
    assert not frozen_carrier_criteria["endpoint_scores_allowed"].any()
    assert not frozen_carrier_criteria["uses_vobs_or_residual"].any()

    frozen_carrier_summary = pd.read_csv(
        DATA / "ngc4088_b2_frozen_asymptotic_carrier_summary.csv"
    ).iloc[0]
    assert frozen_carrier_summary["frozen_carrier_theorem_status"] == (
        "FROZEN_VFLAT2_CARRIER_CONDITIONAL_THEOREM_LAW_PROOF_OPEN"
    )
    assert int(frozen_carrier_summary["n_pass"]) == 6
    assert int(frozen_carrier_summary["n_conditional"]) == 1
    assert int(frozen_carrier_summary["n_open_for_claims"]) == 1
    assert bool(frozen_carrier_summary["law_level_closed"]) is False
    assert bool(frozen_carrier_summary["endpoint_scores_allowed"]) is False
    assert bool(frozen_carrier_summary["uses_vobs_or_residual"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc4088_b2_population_transfer_preflight_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    population_cases = pd.read_csv(
        DATA / "ngc4088_b2_population_transfer_preflight_cases.csv"
    )
    assert len(population_cases) == 7
    assert not population_cases["endpoint_scores_allowed"].any()
    assert not population_cases["uses_endpoint_scores_or_residual"].any()
    case_status = dict(
        zip(population_cases["galaxy"], population_cases["population_transfer_status"])
    )
    assert case_status["NGC4088"] == "REFERENCE_SINGLE_GALAXY_CONDITIONAL_THEOREM"
    assert case_status["NGC4013"] == "PARTIAL_ANALOGUE_NOT_EXACT_B2_TRANSFER"
    assert case_status["NGC5907"] == "PARTIAL_ANALOGUE_NOT_EXACT_B2_TRANSFER"
    assert case_status["NGC7331"] == "CAVEATED_PARTIAL_ANALOGUE_NOT_EXACT_B2_TRANSFER"

    population_summary = pd.read_csv(
        DATA / "ngc4088_b2_population_transfer_preflight_summary.csv"
    ).iloc[0]
    assert population_summary["population_transfer_preflight_status"] == (
        "POPULATION_TRANSFER_PREFLIGHT_BUILT_EXACT_TRANSFER_BLOCKED_ANALOGUE_LANE_AVAILABLE"
    )
    assert int(population_summary["n_reference_exact_protocol"]) == 1
    assert int(population_summary["n_exact_transfer_ready_excluding_reference"]) == 0
    assert int(population_summary["n_partial_analogues"]) == 3
    assert int(population_summary["n_blocked_acquisition_controls"]) == 3
    assert bool(population_summary["endpoint_scores_allowed"]) is False
    assert bool(population_summary["uses_vobs_or_residual"]) is False
    assert bool(population_summary["population_claim_allowed"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc4088_b2_exact_transfer_candidate_manifest.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    exact_candidates = pd.read_csv(DATA / "ngc4088_b2_exact_transfer_candidates.csv")
    assert len(exact_candidates) == 5
    assert not exact_candidates["endpoint_scores_allowed"].any()
    assert not exact_candidates["uses_vobs_or_residual"].any()
    exact_status = dict(zip(exact_candidates["galaxy"], exact_candidates["candidate_status"]))
    assert exact_status["NGC4088"] == "REFERENCE_EXACT_PROTOCOL_NOT_INDEPENDENT_TRANSFER"
    assert exact_status["NGC7331"] == "PARTIAL_EXACT_TRANSFER_CANDIDATE_SOURCE_GAPS"
    assert exact_status["NGC4013"] == "ANALOGUE_WITH_ONSET_CONTEXT_NOT_EXACT_TRANSFER"
    requirements = pd.read_csv(DATA / "ngc4088_b2_exact_transfer_requirements.csv")
    assert len(requirements) == 5
    assert set(requirements["required_field"]) == {
        "x_w",
        "q_warp",
        "sigma_warp",
        "Vflat",
        "epsilon_cross_inputs",
    }

    exact_summary = pd.read_csv(
        DATA / "ngc4088_b2_exact_transfer_candidate_summary.csv"
    ).iloc[0]
    assert exact_summary["exact_transfer_candidate_manifest_status"] == (
        "EXACT_TRANSFER_CANDIDATE_MANIFEST_BUILT_NO_READY_INDEPENDENT_CASE"
    )
    assert int(exact_summary["n_reference_rows"]) == 1
    assert int(exact_summary["n_exact_transfer_ready"]) == 0
    assert int(exact_summary["n_partial_or_analogue_candidates"]) == 3
    assert bool(exact_summary["endpoint_scores_allowed"]) is False
    assert bool(exact_summary["uses_vobs_or_residual"]) is False
    assert bool(exact_summary["population_claim_allowed"]) is False

    for script_name in [
        "scripts/build_ngc7331_qwarp_observable_choice_review_packet.py",
        "scripts/build_ngc7331_qwarp_source_only_review_response.py",
        "scripts/run_ngc7331_qwarp_observable_choice_review_intake.py",
        "scripts/build_ngc7331_b2_exact_transfer_upgrade_gate.py",
    ]:
        subprocess.run(
            ["python", script_name],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    n7331_fields = pd.read_csv(DATA / "ngc7331_b2_exact_transfer_upgrade_fields.csv")
    field_status = dict(zip(n7331_fields["required_b2_field"], n7331_fields["field_status"]))
    assert field_status["x_w"] == "SOURCE_ONSET_AVAILABLE_REPLAY_ONLY"
    assert field_status["Vflat"] == "SOURCE_CATALOG_AVAILABLE"
    assert field_status["q_warp"] == "SOURCE_ONLY_Q_WARP_INTERVAL_CARRIED"
    assert field_status["sigma_warp"] == "MOM1_SIGN_CONTEXT_CARRIED_TO_FORMULA_FREEZE"
    assert field_status["epsilon_cross_inputs"] == "CONSERVATIVE_EPSILON_CROSS_BOUND_CARRIED"
    assert not n7331_fields["endpoint_scores_allowed"].any()
    assert not n7331_fields["uses_vobs_or_residual"].any()

    n7331_gate = pd.read_csv(DATA / "ngc7331_b2_exact_transfer_upgrade_gate.csv")
    gate_status = dict(zip(n7331_gate["gate_id"], n7331_gate["gate_status"]))
    assert gate_status["N7331_ETG1_XW_ONSET"] == "PASS_REPLAY_ONLY"
    assert gate_status["N7331_ETG2_VFLAT_CARRIER"] == "PASS"
    assert gate_status["N7331_ETG3_Q_WARP"] == "PASS_INTERVAL_CARRIED"
    assert gate_status["N7331_ETG4_SIGMA_WARP"] == "PASS_CONTEXT_CARRIED"
    assert gate_status["N7331_ETG5_EPSILON_CROSS"] == "PASS_BOUND_CARRIED"
    assert not n7331_gate["endpoint_scores_allowed"].any()
    assert not n7331_gate["uses_vobs_or_residual"].any()

    n7331_worklist = pd.read_csv(DATA / "ngc7331_b2_exact_transfer_upgrade_worklist.csv")
    assert set(n7331_worklist["missing_field"]) == {
        "none_at_input_gate",
        "point_q_warp_not_selected",
        "endpoint_score_not_allowed_yet",
    }

    n7331_summary = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_upgrade_summary.csv"
    ).iloc[0]
    assert n7331_summary["exact_transfer_upgrade_status"] == (
        "NGC7331_EXACT_TRANSFER_UPGRADE_FORMULA_FREEZE_INPUT_READY_NOT_ENDPOINT"
    )
    assert bool(n7331_summary["x_w_available"]) is True
    assert bool(n7331_summary["vflat_available"]) is True
    assert bool(n7331_summary["q_warp_available"]) is True
    assert bool(n7331_summary["sigma_warp_available"]) is True
    assert bool(n7331_summary["epsilon_cross_inputs_available"]) is True
    assert int(n7331_summary["n_pass_like"]) == 7
    assert int(n7331_summary["n_blocked"]) == 0
    assert bool(n7331_summary["formula_freeze_allowed"]) is True
    assert bool(n7331_summary["endpoint_scores_allowed"]) is False
    assert bool(n7331_summary["uses_vobs_or_residual"]) is False
    assert bool(n7331_summary["population_claim_allowed"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc7331_b2_exact_transfer_formula_freeze_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    n7331_freeze_manifest = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_formula_freeze_manifest.csv"
    ).iloc[0]
    assert n7331_freeze_manifest["formula_id"] == (
        "NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1"
    )
    assert n7331_freeze_manifest["readout_family"] == (
        "K_warp_history_exact_b2_transfer_interval"
    )
    assert abs(float(n7331_freeze_manifest["q_warp_min"]) - 0.0079404475812108) < 1e-15
    assert abs(float(n7331_freeze_manifest["q_warp_max"]) - 0.2057957876154617) < 1e-15
    assert bool(n7331_freeze_manifest["formula_frozen_before_endpoint_scoring"]) is True
    assert bool(n7331_freeze_manifest["endpoint_scores_allowed"]) is False
    assert bool(n7331_freeze_manifest["uses_vobs_or_residual_in_construction"]) is False

    n7331_freeze_grid = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_formula_freeze_kernel_grid.csv"
    )
    assert len(n7331_freeze_grid) == 36
    assert "vobs" not in set(n7331_freeze_grid.columns)
    assert not any(column.startswith("residual_") for column in n7331_freeze_grid.columns)
    assert not n7331_freeze_grid["endpoint_scores_allowed"].any()
    assert not n7331_freeze_grid["uses_vobs_or_residual_in_construction"].any()
    inactive = n7331_freeze_grid[
        n7331_freeze_grid["x_R_over_RHI"]
        <= n7331_freeze_grid["x_w_formula_freeze"]
    ]
    assert (inactive["delta_v2_min_km2_s2"].abs() < 1e-12).all()
    assert (inactive["delta_v2_max_km2_s2"].abs() < 1e-12).all()

    n7331_freeze_gate = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_formula_freeze_gate.csv"
    )
    n7331_freeze_gate_status = dict(
        zip(n7331_freeze_gate["gate_id"], n7331_freeze_gate["gate_status"])
    )
    assert n7331_freeze_gate_status["N7331_B2FF1_UPGRADE_INPUT_READY"] == "PASS"
    assert n7331_freeze_gate_status["N7331_B2FF2_Q_INTERVAL_CARRIED"] == (
        "PASS_INTERVAL_CARRIED"
    )
    assert n7331_freeze_gate_status["N7331_B2FF3_SIGN_BRANCH"] == "PASS_CAVEATED"
    assert n7331_freeze_gate_status["N7331_B2FF4_EPSILON_CROSS"] == "PASS_CAVEATED"
    assert n7331_freeze_gate_status["N7331_B2FF5_DIMENSIONS_AND_LIMITS"] == "PASS"
    assert n7331_freeze_gate_status["N7331_B2FF6_ENDPOINT_BLINDNESS"] == "PASS"
    assert n7331_freeze_gate_status["N7331_B2FF7_Q_PLACEMENT_CAVEAT"] == (
        "PASS_CAVEATED"
    )
    assert not n7331_freeze_gate["endpoint_scores_allowed"].any()
    assert not n7331_freeze_gate["uses_vobs_or_residual_in_construction"].any()

    n7331_freeze_summary = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_formula_freeze_summary.csv"
    ).iloc[0]
    assert n7331_freeze_summary["formula_freeze_status"] == (
        "NGC7331_EXACT_B2_TRANSFER_INTERVAL_FORMULA_FREEZE_READY_NOT_SCORE"
    )
    assert int(n7331_freeze_summary["n_blocked"]) == 0
    assert bool(n7331_freeze_summary["formula_frozen_before_endpoint_scoring"]) is True
    assert bool(n7331_freeze_summary["endpoint_scores_allowed"]) is False
    assert bool(n7331_freeze_summary["uses_vobs_or_residual_in_construction"]) is False

    subprocess.run(
        [
            "python",
            "scripts/run_ngc7331_b2_exact_transfer_interval_control_audit.py",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    n7331_interval_points = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_interval_control_points.csv"
    )
    assert len(n7331_interval_points) == 36
    assert set(
        [
            "vobs",
            "v_exact_b2_min_km_s",
            "v_exact_b2_max_km_s",
            "v_exact_b2_min_cross_caveated_km_s",
            "v_exact_b2_max_cross_caveated_km_s",
        ]
    ).issubset(set(n7331_interval_points.columns))
    assert not n7331_interval_points["point_q_selected_from_residual"].any()
    assert not n7331_interval_points["construction_used_vobs"].any()
    assert n7331_interval_points["scoring_used_vobs"].all()

    n7331_interval_scores = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_interval_control_scores.csv"
    ).iloc[0]
    assert n7331_interval_scores["model_role"] == "source_frozen_interval_readout"
    assert 0.0 <= float(n7331_interval_scores["coverage_fraction"]) <= 1.0
    assert (
        0.0
        <= float(n7331_interval_scores["coverage_fraction_cross_caveated"])
        <= 1.0
    )
    assert bool(n7331_interval_scores["construction_used_vobs"]) is False
    assert bool(n7331_interval_scores["scoring_used_vobs"]) is True

    n7331_interval_baselines = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_interval_control_baselines.csv"
    )
    assert set(n7331_interval_baselines["model_id"]) == {
        "NEWTONIAN_vn",
        "TPG_V6_v_v6",
        "MOND_v_mond",
        "EXPONENTIAL_DISK_CARRIER",
    }
    assert not n7331_interval_baselines["construction_used_vobs"].any()
    assert n7331_interval_baselines["scoring_used_vobs"].all()

    n7331_interval_summary = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_interval_control_summary.csv"
    ).iloc[0]
    assert n7331_interval_summary["audit_status"] == (
        "NGC7331_EXACT_B2_INTERVAL_CONTROL_AUDIT_COMPLETE_NOT_POINT_ENDPOINT"
    )
    assert int(n7331_interval_summary["n_points"]) == 36
    assert bool(n7331_interval_summary["construction_used_vobs"]) is False
    assert bool(n7331_interval_summary["scoring_used_vobs"]) is True
    assert bool(n7331_interval_summary["endpoint_scores_allowed"]) is True
    assert bool(n7331_interval_summary["point_q_selected_from_residual"]) is False
    assert n7331_interval_summary["claim_boundary"] == (
        "ngc7331_b2_exact_transfer_interval_control_audit_not_point_endpoint"
    )

    subprocess.run(
        ["python", "scripts/build_ngc7331_b2_exact_transfer_source_packet.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    source_requirements = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_source_packet_requirements.csv"
    )
    assert set(source_requirements["required_b2_field"]) == {
        "q_warp",
        "sigma_warp",
        "epsilon_cross_inputs",
    }
    assert not source_requirements["endpoint_scores_allowed"].any()
    assert not source_requirements["uses_vobs_or_residual"].any()

    source_templates = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_source_packet_templates.csv"
    )
    assert len(source_templates) == 9
    assert set(source_templates["required_b2_field"]) == {
        "q_warp",
        "sigma_warp",
        "epsilon_cross_inputs",
    }
    assert set(source_templates["review_status"]) == {"MEASUREMENT_PENDING"}
    assert not source_templates["endpoint_scores_allowed"].any()
    assert not source_templates["uses_vobs_or_residual"].any()

    source_packet_gate = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_source_packet_gate.csv"
    )
    source_gate_status = dict(zip(source_packet_gate["gate_id"], source_packet_gate["gate_status"]))
    assert source_gate_status["N7331_B2SP1_PACKET_SCOPE"] == "PASS"
    assert source_gate_status["N7331_B2SP2_XW_VFLAT_CONTEXT"] == "PASS_CONTEXT"
    assert source_gate_status["N7331_B2SP3_Q_WARP_TEMPLATE"] == "BLOCKED_MEASUREMENT_PENDING"
    assert source_gate_status["N7331_B2SP4_SIGMA_TEMPLATE"] == "BLOCKED_REVIEW_PENDING"
    assert source_gate_status["N7331_B2SP5_EPSILON_TEMPLATE"] == "BLOCKED_MEASUREMENT_PENDING"
    assert source_gate_status["N7331_B2SP6_ENDPOINT_BLINDNESS"] == "PASS"
    assert not source_packet_gate["endpoint_scores_allowed"].any()
    assert not source_packet_gate["uses_vobs_or_residual"].any()

    source_packet_summary = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_source_packet_summary.csv"
    ).iloc[0]
    assert source_packet_summary["source_packet_status"] == (
        "NGC7331_EXACT_TRANSFER_SOURCE_PACKET_BUILT_MEASUREMENTS_PENDING"
    )
    assert int(source_packet_summary["n_requirements"]) == 3
    assert int(source_packet_summary["n_templates"]) == 9
    assert int(source_packet_summary["n_pass_like"]) == 3
    assert int(source_packet_summary["n_blocked"]) == 3
    assert bool(source_packet_summary["q_warp_packet_ready"]) is True
    assert bool(source_packet_summary["sigma_warp_packet_ready"]) is True
    assert bool(source_packet_summary["epsilon_cross_packet_ready"]) is True
    assert bool(source_packet_summary["q_warp_measurement_accepted"]) is False
    assert bool(source_packet_summary["sigma_warp_frozen"]) is False
    assert bool(source_packet_summary["epsilon_cross_bound_closed"]) is False
    assert bool(source_packet_summary["formula_freeze_allowed"]) is False
    assert bool(source_packet_summary["endpoint_scores_allowed"]) is False
    assert bool(source_packet_summary["uses_vobs_or_residual"]) is False
    assert bool(source_packet_summary["population_claim_allowed"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc7331_b2_exact_transfer_source_evidence_review.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    n7331_evidence = pd.read_csv(DATA / "ngc7331_b2_exact_transfer_source_evidence.csv")
    assert len(n7331_evidence) == 4
    assert set(n7331_evidence["supports_field"]).issuperset(
        {"q_warp", "sigma_warp;epsilon_cross_inputs", "epsilon_cross_inputs"}
    )
    assert not n7331_evidence["endpoint_scores_allowed"].any()
    assert not n7331_evidence["uses_vobs_or_residual"].any()

    n7331_decisions = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_source_evidence_decisions.csv"
    )
    decision_status = dict(
        zip(n7331_decisions["required_b2_field"], n7331_decisions["review_decision"])
    )
    assert decision_status["q_warp"] == "CONTEXT_READY_NUMERIC_Q_WARP_BLOCKED"
    assert decision_status["sigma_warp"] == "SIGN_RULE_BLOCKED_COMPLEX_WARP"
    assert decision_status["epsilon_cross_inputs"] == (
        "BOUND_BLOCKED_CROSS_TERMS_LIKELY_RELEVANT"
    )
    assert not n7331_decisions["endpoint_scores_allowed"].any()
    assert not n7331_decisions["uses_vobs_or_residual"].any()

    n7331_evidence_gate = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_source_evidence_gate.csv"
    )
    evidence_gate_status = dict(
        zip(n7331_evidence_gate["gate_id"], n7331_evidence_gate["gate_status"])
    )
    assert evidence_gate_status["N7331_B2ER1_SOURCE_CONTEXT_AVAILABLE"] == "PASS"
    assert evidence_gate_status["N7331_B2ER2_Q_WARP_PROMOTION"] == (
        "BLOCKED_NUMERIC_AMPLITUDE_MISSING"
    )
    assert evidence_gate_status["N7331_B2ER3_SIGMA_PROMOTION"] == "BLOCKED_SIGN_AMBIGUOUS"
    assert evidence_gate_status["N7331_B2ER4_EPSILON_PROMOTION"] == "BLOCKED_BOUND_MISSING"
    assert evidence_gate_status["N7331_B2ER5_ENDPOINT_BLINDNESS"] == "PASS"
    assert not n7331_evidence_gate["endpoint_scores_allowed"].any()
    assert not n7331_evidence_gate["uses_vobs_or_residual"].any()

    n7331_evidence_summary = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_source_evidence_summary.csv"
    ).iloc[0]
    assert n7331_evidence_summary["source_evidence_review_status"] == (
        "NGC7331_SOURCE_EVIDENCE_REVIEW_BUILT_EXACT_TRANSFER_STILL_BLOCKED"
    )
    assert int(n7331_evidence_summary["n_evidence_rows"]) == 4
    assert int(n7331_evidence_summary["n_blocked"]) == 3
    assert bool(n7331_evidence_summary["q_warp_promoted"]) is False
    assert bool(n7331_evidence_summary["sigma_warp_promoted"]) is False
    assert bool(n7331_evidence_summary["epsilon_cross_promoted"]) is False
    assert bool(n7331_evidence_summary["complex_warp_context_confirmed"]) is True
    assert bool(n7331_evidence_summary["cross_terms_must_be_carried_or_bounded"]) is True
    assert bool(n7331_evidence_summary["formula_freeze_allowed"]) is False
    assert bool(n7331_evidence_summary["endpoint_scores_allowed"]) is False
    assert bool(n7331_evidence_summary["uses_vobs_or_residual"]) is False
    assert bool(n7331_evidence_summary["population_claim_allowed"]) is False

    things_manifest = pd.read_csv(DATA / "ngc7331_things_hi_product_manifest.csv")
    assert len(things_manifest) == 6
    assert things_manifest["local_cache_exists"].all()
    assert things_manifest["sha256"].notna().all()
    assert not things_manifest["endpoint_scores_allowed"].any()
    assert not things_manifest["uses_vobs_or_residual"].any()

    subprocess.run(
        ["python", "scripts/build_ngc7331_things_hi_product_audit.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    things_audit = pd.read_csv(DATA / "ngc7331_things_hi_product_audit.csv")
    assert len(things_audit) == 6
    assert set(things_audit["audit_status"]) == {"PASS_FITS_READABLE"}
    assert set(things_audit["shape"]) == {"1x1x1024x1024"}
    assert not things_audit["endpoint_scores_allowed"].any()
    assert not things_audit["uses_vobs_or_residual"].any()

    things_audit_summary = pd.read_csv(
        DATA / "ngc7331_things_hi_product_audit_summary.csv"
    ).iloc[0]
    assert things_audit_summary["things_hi_product_audit_status"] == (
        "NGC7331_THINGS_HI_PRODUCTS_AUDITED_WORKSHEET_READY"
    )
    assert int(things_audit_summary["n_readable"]) == 6
    assert bool(things_audit_summary["worksheet_ready"]) is True
    assert bool(things_audit_summary["q_warp_measurement_ready"]) is False
    assert bool(things_audit_summary["formula_freeze_allowed"]) is False
    assert bool(things_audit_summary["endpoint_scores_allowed"]) is False
    assert bool(things_audit_summary["uses_vobs_or_residual"]) is False
    assert bool(things_audit_summary["population_claim_allowed"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc7331_b2_hi_warp_acquisition_route.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    hi_sources = pd.read_csv(DATA / "ngc7331_b2_hi_warp_source_candidates.csv")
    assert len(hi_sources) == 4
    source_status = dict(zip(hi_sources["source_id"], hi_sources["source_status"]))
    assert source_status["N7331_HI_SRC1_BOSMA_NED_21CM"] == (
        "PRIMARY_CONTEXT_SOURCE_FIGURE_DIGITIZATION_CANDIDATE"
    )
    assert source_status["N7331_HI_SRC2_THINGS_DATA_PRODUCTS"] == (
        "PUBLIC_DATA_ROUTE_CACHED_AND_AUDITED_WORKSHEET_READY"
    )
    assert not hi_sources["endpoint_scores_allowed"].any()
    assert not hi_sources["uses_vobs_or_residual"].any()

    hi_routes = pd.read_csv(DATA / "ngc7331_b2_hi_warp_extraction_routes.csv")
    assert len(hi_routes) == 4
    route_status = dict(zip(hi_routes["route_id"], hi_routes["current_route_status"]))
    assert route_status["N7331_HI_ROUTE1_THINGS_MOMENT_MAP_EXTRACTION"] == (
        "PREFERRED_ROUTE_SOURCE_PRODUCTS_CACHED_WORKSHEET_READY"
    )
    assert route_status["N7331_HI_ROUTE2_BOSMA_FIGURE_DIGITIZATION"] == (
        "FALLBACK_ROUTE_FIGURE_CACHE_OR_SCREENSHOT_PENDING"
    )
    assert not hi_routes["endpoint_scores_allowed"].any()
    assert not hi_routes["uses_vobs_or_residual"].any()

    hi_acquisition_gate = pd.read_csv(DATA / "ngc7331_b2_hi_warp_acquisition_gate.csv")
    hi_gate_status = dict(zip(hi_acquisition_gate["gate_id"], hi_acquisition_gate["gate_status"]))
    assert hi_gate_status["N7331_HIAG1_SOURCE_CANDIDATES_IDENTIFIED"] == "PASS"
    assert hi_gate_status["N7331_HIAG2_SOURCE_NATIVE_HI_PRODUCT_CACHED"] == "PASS"
    assert hi_gate_status["N7331_HIAG3_Q_WARP_MEASURABLE"] == "BLOCKED_EXTRACTION_PENDING"
    assert hi_gate_status["N7331_HIAG4_SIGMA_SIGN_REVIEW"] == "BLOCKED_SIGN_REVIEW_PENDING"
    assert hi_gate_status["N7331_HIAG5_ENDPOINT_BLINDNESS"] == "PASS"
    assert not hi_acquisition_gate["endpoint_scores_allowed"].any()
    assert not hi_acquisition_gate["uses_vobs_or_residual"].any()

    hi_acquisition_summary = pd.read_csv(
        DATA / "ngc7331_b2_hi_warp_acquisition_summary.csv"
    ).iloc[0]
    assert hi_acquisition_summary["hi_warp_acquisition_status"] == (
        "NGC7331_HI_WARP_ACQUISITION_ROUTE_SOURCE_PRODUCTS_CACHED_WORKSHEET_READY"
    )
    assert int(hi_acquisition_summary["n_source_candidates"]) == 4
    assert int(hi_acquisition_summary["n_extraction_routes"]) == 4
    assert hi_acquisition_summary["preferred_next_route"] == (
        "THINGS_QWARP_SIGN_CROSS_TERM_WORKSHEET"
    )
    assert hi_acquisition_summary["fallback_next_route"] == (
        "BOSMA_FIGURE_DIGITIZATION_WORKSHEET"
    )
    assert bool(hi_acquisition_summary["q_warp_measurement_ready"]) is False
    assert bool(hi_acquisition_summary["sigma_warp_sign_ready"]) is False
    assert bool(hi_acquisition_summary["epsilon_cross_bound_ready"]) is False
    assert bool(hi_acquisition_summary["formula_freeze_allowed"]) is False
    assert bool(hi_acquisition_summary["endpoint_scores_allowed"]) is False
    assert bool(hi_acquisition_summary["uses_vobs_or_residual"]) is False
    assert bool(hi_acquisition_summary["population_claim_allowed"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc7331_things_qwarp_measurement_worksheet.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    qwarp_geometry = pd.read_csv(DATA / "ngc7331_things_qwarp_measurement_geometry.csv")
    assert len(qwarp_geometry) == 1
    qgeom = qwarp_geometry.iloc[0]
    assert bool(qgeom["endpoint_scores_allowed"]) is False
    assert bool(qgeom["uses_vobs_or_residual"]) is False
    assert qgeom["pa_status"] == "PENDING_SOURCE_MEASUREMENT_OR_LITERATURE_VALUE"
    assert float(qgeom["rhi_pix"]) > float(qgeom["warp_onset_pix"]) > 0

    qwarp_worksheet = pd.read_csv(DATA / "ngc7331_things_qwarp_measurement_worksheet.csv")
    assert len(qwarp_worksheet) == 7
    assert set(qwarp_worksheet["status"]) == {"MEASUREMENT_PENDING"}
    assert not qwarp_worksheet["endpoint_scores_allowed"].any()
    assert not qwarp_worksheet["uses_vobs_or_residual"].any()

    qwarp_gate = pd.read_csv(DATA / "ngc7331_things_qwarp_measurement_gate.csv")
    qwarp_gate_status = dict(zip(qwarp_gate["gate_id"], qwarp_gate["gate_status"]))
    assert qwarp_gate_status["N7331_QWG1_THINGS_PRODUCTS_AUDITED"] == "PASS"
    assert qwarp_gate_status["N7331_QWG2_GEOMETRY_SCALES_DEFINED"] == "PASS"
    assert qwarp_gate_status["N7331_QWG3_PA_REFERENCE"] == "BLOCKED_MEASUREMENT_PENDING"
    assert qwarp_gate_status["N7331_QWG4_Q_WARP_RESPONSE"] == "BLOCKED_MEASUREMENT_PENDING"
    assert qwarp_gate_status["N7331_QWG5_ENDPOINT_BLINDNESS"] == "PASS"
    assert not qwarp_gate["endpoint_scores_allowed"].any()
    assert not qwarp_gate["uses_vobs_or_residual"].any()

    qwarp_summary = pd.read_csv(DATA / "ngc7331_things_qwarp_measurement_summary.csv").iloc[0]
    assert qwarp_summary["qwarp_worksheet_status"] == (
        "NGC7331_THINGS_QWARP_WORKSHEET_READY_MEASUREMENT_PENDING"
    )
    assert int(qwarp_summary["n_measurement_targets"]) == 7
    assert bool(qwarp_summary["things_products_audited"]) is True
    assert bool(qwarp_summary["geometry_defined"]) is True
    assert bool(qwarp_summary["pa_reference_frozen"]) is False
    assert bool(qwarp_summary["q_warp_measurement_ready"]) is False
    assert bool(qwarp_summary["sigma_warp_sign_ready"]) is False
    assert bool(qwarp_summary["epsilon_cross_bound_ready"]) is False
    assert bool(qwarp_summary["formula_freeze_allowed"]) is False
    assert bool(qwarp_summary["endpoint_scores_allowed"]) is False
    assert bool(qwarp_summary["uses_vobs_or_residual"]) is False
    assert bool(qwarp_summary["population_claim_allowed"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc7331_things_qwarp_first_pass_measurement.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    qwarp_first_pass = pd.read_csv(DATA / "ngc7331_things_qwarp_first_pass_measurements.csv")
    assert len(qwarp_first_pass) == 2
    assert set(qwarp_first_pass["product_id"]) == {"NA_MOM0", "RO_MOM0"}
    assert (qwarp_first_pass["q_warp_first_pass"] > 0).all()
    assert set(qwarp_first_pass["measurement_status"]) == {
        "FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED"
    }
    assert not qwarp_first_pass["endpoint_scores_allowed"].any()
    assert not qwarp_first_pass["uses_vobs_or_residual"].any()

    qwarp_response = pd.read_csv(DATA / "ngc7331_things_qwarp_first_pass_response.csv").iloc[0]
    assert qwarp_response["response_status"] == "FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED"
    assert float(qwarp_response["q_warp_first_pass"]) > 0.0
    assert pd.isna(qwarp_response["sigma_warp_sign"])
    assert pd.isna(qwarp_response["epsilon_cross_bound_or_interval"])
    assert bool(qwarp_response["formula_freeze_allowed"]) is False
    assert bool(qwarp_response["endpoint_scores_allowed"]) is False
    assert bool(qwarp_response["uses_vobs_or_residual"]) is False

    qwarp_first_pass_gate = pd.read_csv(DATA / "ngc7331_things_qwarp_first_pass_gate.csv")
    qwarp_first_pass_gate_status = dict(
        zip(qwarp_first_pass_gate["gate_id"], qwarp_first_pass_gate["gate_status"])
    )
    assert qwarp_first_pass_gate_status["N7331_QWFP1_SOURCE_PRODUCTS"] == "PASS"
    assert (
        qwarp_first_pass_gate_status["N7331_QWFP2_SOURCE_NATIVE_PA"]
        == "FIRST_PASS_REVIEW_REQUIRED"
    )
    assert (
        qwarp_first_pass_gate_status["N7331_QWFP3_QWARP_MEASUREMENT"]
        == "FIRST_PASS_REVIEW_REQUIRED"
    )
    assert qwarp_first_pass_gate_status["N7331_QWFP4_SIGN_AND_CROSS_TERMS"] == (
        "BLOCKED_REVIEW_REQUIRED"
    )
    assert qwarp_first_pass_gate_status["N7331_QWFP5_ENDPOINT_BLINDNESS"] == "PASS"
    assert not qwarp_first_pass_gate["endpoint_scores_allowed"].any()
    assert not qwarp_first_pass_gate["uses_vobs_or_residual"].any()

    qwarp_first_pass_summary = pd.read_csv(
        DATA / "ngc7331_things_qwarp_first_pass_summary.csv"
    ).iloc[0]
    assert qwarp_first_pass_summary["qwarp_first_pass_status"] == (
        "NGC7331_THINGS_QWARP_FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED"
    )
    assert int(qwarp_first_pass_summary["n_products_measured"]) == 2
    assert bool(qwarp_first_pass_summary["sign_ready"]) is False
    assert bool(qwarp_first_pass_summary["epsilon_cross_ready"]) is False
    assert bool(qwarp_first_pass_summary["formula_freeze_allowed"]) is False
    assert bool(qwarp_first_pass_summary["endpoint_scores_allowed"]) is False
    assert bool(qwarp_first_pass_summary["uses_vobs_or_residual"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc7331_things_qwarp_measurement_sensitivity_audit.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    qwarp_sensitivity = pd.read_csv(DATA / "ngc7331_things_qwarp_measurement_sensitivity.csv")
    assert len(qwarp_sensitivity) == 10
    assert set(qwarp_sensitivity["product_id"]) == {"NA_MOM0", "RO_MOM0"}
    assert (qwarp_sensitivity["q_envelope_p80"] > qwarp_sensitivity["q_centroid"]).all()
    assert not qwarp_sensitivity["endpoint_scores_allowed"].any()
    assert not qwarp_sensitivity["uses_vobs_or_residual"].any()

    qwarp_sensitivity_summary = pd.read_csv(
        DATA / "ngc7331_things_qwarp_measurement_sensitivity_summary.csv"
    ).iloc[0]
    assert qwarp_sensitivity_summary["sensitivity_status"] == (
        "CENTROID_STABLE_BUT_ENVELOPE_STRONGER_REVIEW_REQUIRED"
    )
    assert float(qwarp_sensitivity_summary["q_envelope_p80_mean_min"]) > (
        2.0 * float(qwarp_sensitivity_summary["q_centroid_mean_max"])
    )
    assert bool(qwarp_sensitivity_summary["formula_freeze_allowed"]) is False
    assert bool(qwarp_sensitivity_summary["endpoint_scores_allowed"]) is False
    assert bool(qwarp_sensitivity_summary["uses_vobs_or_residual"]) is False

    qwarp_sensitivity_gate = pd.read_csv(
        DATA / "ngc7331_things_qwarp_measurement_sensitivity_gate.csv"
    )
    qwarp_sensitivity_gate_status = dict(
        zip(qwarp_sensitivity_gate["gate_id"], qwarp_sensitivity_gate["gate_status"])
    )
    assert qwarp_sensitivity_gate_status["N7331_QWS1_CENTROID_STABILITY"] == (
        "REVIEW_REQUIRED"
    )
    assert qwarp_sensitivity_gate_status["N7331_QWS2_ENVELOPE_STRENGTH"] == (
        "REVIEW_REQUIRED"
    )
    assert qwarp_sensitivity_gate_status["N7331_QWS3_ENDPOINT_BLINDNESS"] == "PASS"
    assert not qwarp_sensitivity_gate["endpoint_scores_allowed"].any()
    assert not qwarp_sensitivity_gate["uses_vobs_or_residual"].any()

    subprocess.run(
        ["python", "scripts/build_ngc7331_things_mom1_sign_cross_review.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    mom1_measurements = pd.read_csv(DATA / "ngc7331_things_mom1_sign_cross_measurements.csv")
    assert len(mom1_measurements) == 2
    assert set(mom1_measurements["product_prefix"]) == {"NATURAL", "ROBUST"}
    assert mom1_measurements["inner_outer_receding_orientation_same"].all()
    assert (mom1_measurements["f_pa"] < 0.1).all()
    assert not mom1_measurements["endpoint_scores_allowed"].any()
    assert not mom1_measurements["uses_vobs_or_residual"].any()

    mom1_response = pd.read_csv(DATA / "ngc7331_things_mom1_sign_cross_response.csv").iloc[0]
    assert mom1_response["receding_side_consensus"] == "CONSISTENT"
    assert bool(mom1_response["inner_outer_receding_orientation_same_all"]) is True
    assert mom1_response["sigma_warp_sign_status"] == (
        "KINEMATIC_CONTEXT_AVAILABLE_SIGN_NOT_FROZEN"
    )
    assert mom1_response["epsilon_cross_status"] == (
        "CANDIDATE_BOUND_REVIEW_REQUIRED_NOT_CLOSED"
    )
    assert float(mom1_response["epsilon_cross_candidate_bound"]) > 0.0
    assert bool(mom1_response["formula_freeze_allowed"]) is False
    assert bool(mom1_response["endpoint_scores_allowed"]) is False
    assert bool(mom1_response["uses_vobs_or_residual"]) is False

    mom1_gate = pd.read_csv(DATA / "ngc7331_things_mom1_sign_cross_gate.csv")
    mom1_gate_status = dict(zip(mom1_gate["gate_id"], mom1_gate["gate_status"]))
    assert mom1_gate_status["N7331_MOM1SC1_PRODUCTS"] == "PASS"
    assert mom1_gate_status["N7331_MOM1SC2_KINEMATIC_ORIENTATION"] == "REVIEW_REQUIRED"
    assert mom1_gate_status["N7331_MOM1SC3_EPSILON_CROSS"] == (
        "CANDIDATE_BOUND_REVIEW_REQUIRED"
    )
    assert mom1_gate_status["N7331_MOM1SC4_FORMULA_FREEZE"] == "BLOCKED"
    assert mom1_gate_status["N7331_MOM1SC5_ENDPOINT_BLINDNESS"] == "PASS"
    assert not mom1_gate["endpoint_scores_allowed"].any()
    assert not mom1_gate["uses_vobs_or_residual"].any()

    mom1_summary = pd.read_csv(DATA / "ngc7331_things_mom1_sign_cross_summary.csv").iloc[0]
    assert mom1_summary["mom1_sign_cross_status"] == (
        "NGC7331_THINGS_MOM1_SIGN_CROSS_REVIEW_BUILT_FREEZE_BLOCKED"
    )
    assert int(mom1_summary["n_products_measured"]) == 2
    assert bool(mom1_summary["sigma_warp_sign_ready"]) is False
    assert bool(mom1_summary["epsilon_cross_bound_ready"]) is False
    assert bool(mom1_summary["formula_freeze_allowed"]) is False
    assert bool(mom1_summary["endpoint_scores_allowed"]) is False
    assert bool(mom1_summary["uses_vobs_or_residual"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc7331_qwarp_observable_choice_review_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    qchoice_candidates = pd.read_csv(DATA / "ngc7331_qwarp_observable_choice_candidates.csv")
    assert set(qchoice_candidates["candidate_observable"]) == {
        "CENTROID_RIDGE_SHIFT",
        "OUTER_ENVELOPE_P80_SUPPORT",
    }
    assert (
        qchoice_candidates.loc[
            qchoice_candidates["candidate_observable"].eq("OUTER_ENVELOPE_P80_SUPPORT"),
            "q_warp_candidate",
        ].iloc[0]
        > qchoice_candidates.loc[
            qchoice_candidates["candidate_observable"].eq("CENTROID_RIDGE_SHIFT"),
            "q_warp_candidate",
        ].iloc[0]
    )
    assert set(qchoice_candidates["formula_freeze_recommendation"]) == {
        "DO_NOT_FREEZE_WITHOUT_REVIEW"
    }
    assert not qchoice_candidates["endpoint_scores_allowed"].any()
    assert not qchoice_candidates["uses_vobs_or_residual"].any()

    qchoice_gate = pd.read_csv(DATA / "ngc7331_qwarp_observable_choice_gate.csv")
    qchoice_gate_status = dict(zip(qchoice_gate["gate_id"], qchoice_gate["gate_status"]))
    assert qchoice_gate_status["N7331_QCHOICE1_SOURCE_NATIVE_Q_EXISTS"] == (
        "PASS_REVIEW_INPUT_AVAILABLE"
    )
    assert qchoice_gate_status["N7331_QCHOICE2_OBSERVABLE_UNIQUENESS"] == (
        "BLOCKED_OBSERVABLE_CHOICE_NOT_UNIQUE"
    )
    assert qchoice_gate_status["N7331_QCHOICE3_MOM1_CONTEXT"] == (
        "PASS_REVIEW_INPUT_AVAILABLE"
    )
    assert qchoice_gate_status["N7331_QCHOICE4_EPSILON_INTERVAL"] == (
        "BLOCKED_INTERVAL_NOT_ACCEPTED"
    )
    assert qchoice_gate_status["N7331_QCHOICE5_FORMULA_FREEZE"] == "BLOCKED"
    assert qchoice_gate_status["N7331_QCHOICE6_ENDPOINT_BLINDNESS"] == "PASS"
    assert not qchoice_gate["endpoint_scores_allowed"].any()
    assert not qchoice_gate["uses_vobs_or_residual"].any()

    qchoice_summary = pd.read_csv(DATA / "ngc7331_qwarp_observable_choice_summary.csv").iloc[0]
    assert qchoice_summary["observable_choice_status"] == (
        "NGC7331_QWARP_OBSERVABLE_CHOICE_REVIEW_GATE_BUILT_FREEZE_BLOCKED"
    )
    assert float(qchoice_summary["q_envelope_to_centroid_ratio"]) > 10.0
    assert bool(qchoice_summary["mom1_context_available"]) is True
    assert bool(qchoice_summary["sigma_warp_sign_ready"]) is False
    assert bool(qchoice_summary["epsilon_cross_bound_ready"]) is False
    assert bool(qchoice_summary["formula_freeze_allowed"]) is False
    assert bool(qchoice_summary["endpoint_scores_allowed"]) is False
    assert bool(qchoice_summary["uses_vobs_or_residual"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc7331_qwarp_observable_choice_review_packet.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    qreview_packet = pd.read_csv(DATA / "ngc7331_qwarp_observable_choice_review_packet.csv")
    assert len(qreview_packet) == 1
    packet_row = qreview_packet.iloc[0]
    assert packet_row["review_status"] == "REVIEW_PACKET_READY_RESPONSE_PENDING"
    assert "vobs" in packet_row["forbidden_inputs"]
    assert "endpoint_score" in packet_row["forbidden_inputs"]
    assert "required_S_tau_diagnostic" in packet_row["forbidden_inputs"]
    assert bool(packet_row["formula_freeze_allowed_now"]) is False
    assert bool(packet_row["endpoint_scores_allowed"]) is False
    assert bool(packet_row["uses_vobs_or_residual"]) is False

    qreview_options = pd.read_csv(DATA / "ngc7331_qwarp_observable_choice_review_options.csv")
    assert set(qreview_options["review_option"]) == {
        "ACCEPT_CENTROID",
        "ACCEPT_ENVELOPE",
        "CARRY_INTERVAL",
        "REJECT_Q_FREEZE",
    }
    assert not qreview_options["endpoint_scores_allowed"].any()
    assert not qreview_options["uses_vobs_or_residual"].any()

    qreview_response = pd.read_csv(
        DATA / "ngc7331_qwarp_observable_choice_review_response_template.csv"
    ).iloc[0]
    assert qreview_response["review_decision"] == "PENDING_INDEPENDENT_REVIEW"
    assert bool(qreview_response["formula_freeze_allowed_after_review"]) is False
    assert bool(qreview_response["endpoint_scores_allowed"]) is False
    assert bool(qreview_response["uses_vobs_or_residual"]) is False

    qreview_gate = pd.read_csv(DATA / "ngc7331_qwarp_observable_choice_review_packet_gate.csv")
    qreview_gate_status = dict(zip(qreview_gate["gate_id"], qreview_gate["gate_status"]))
    assert qreview_gate_status["N7331_QPACK1_PACKET_SCOPE"] == "PASS"
    assert qreview_gate_status["N7331_QPACK2_SOURCE_INPUTS"] == "PASS"
    assert qreview_gate_status["N7331_QPACK3_MOM1_CONTEXT"] == "PASS_CONTEXT"
    assert qreview_gate_status["N7331_QPACK4_RESPONSE"] == "BLOCKED_RESPONSE_PENDING"
    assert qreview_gate_status["N7331_QPACK5_FORMULA_FREEZE"] == "BLOCKED"
    assert qreview_gate_status["N7331_QPACK6_ENDPOINT_BLINDNESS"] == "PASS"
    assert not qreview_gate["endpoint_scores_allowed"].any()
    assert not qreview_gate["uses_vobs_or_residual"].any()

    qreview_summary = pd.read_csv(
        DATA / "ngc7331_qwarp_observable_choice_review_packet_summary.csv"
    ).iloc[0]
    assert qreview_summary["review_packet_status"] == (
        "NGC7331_QWARP_OBSERVABLE_CHOICE_REVIEW_PACKET_READY_RESPONSE_PENDING"
    )
    assert int(qreview_summary["n_review_options"]) == 4
    assert bool(qreview_summary["response_pending"]) is True
    assert bool(qreview_summary["formula_freeze_allowed"]) is False
    assert bool(qreview_summary["endpoint_scores_allowed"]) is False
    assert bool(qreview_summary["uses_vobs_or_residual"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc7331_qwarp_source_only_review_response.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    qresponse = pd.read_csv(
        DATA / "ngc7331_qwarp_observable_choice_review_response_template.csv"
    ).iloc[0]
    assert qresponse["review_decision"] == "CARRY_INTERVAL"
    assert "0.0079404475812108" in qresponse["accepted_q_warp_interval"]
    assert "0.2057957876154617" in qresponse["accepted_q_warp_interval"]
    assert qresponse["forbidden_inputs_used"] == "none"
    assert bool(qresponse["formula_freeze_allowed_after_review"]) is True
    assert bool(qresponse["endpoint_scores_allowed"]) is False
    assert bool(qresponse["uses_vobs_or_residual"]) is False

    qresponse_summary = pd.read_csv(
        DATA / "ngc7331_qwarp_source_only_review_response_summary.csv"
    ).iloc[0]
    assert qresponse_summary["review_response_status"] == (
        "NGC7331_QWARP_SOURCE_ONLY_REVIEW_RESPONSE_FILLED_INTERVAL_CARRIED"
    )
    assert qresponse_summary["review_decision"] == "CARRY_INTERVAL"
    assert bool(qresponse_summary["formula_freeze_allowed_after_review"]) is True
    assert bool(qresponse_summary["endpoint_scores_allowed"]) is False
    assert bool(qresponse_summary["uses_vobs_or_residual"]) is False

    subprocess.run(
        ["python", "scripts/run_ngc7331_qwarp_observable_choice_review_intake.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    qintake_validation = pd.read_csv(
        DATA / "ngc7331_qwarp_observable_choice_review_intake_validation.csv"
    ).iloc[0]
    assert bool(qintake_validation["response_pending"]) is False
    assert bool(qintake_validation["decision_allowed"]) is True
    assert bool(qintake_validation["q_decision_valid"]) is True
    assert bool(qintake_validation["sources_clean"]) is True
    assert bool(qintake_validation["forbidden_clean"]) is True
    assert bool(qintake_validation["sign_ready"]) is True
    assert bool(qintake_validation["epsilon_ready"]) is True
    assert bool(qintake_validation["formula_freeze_allowed"]) is True
    assert bool(qintake_validation["endpoint_scores_allowed"]) is False
    assert bool(qintake_validation["uses_vobs_or_residual"]) is False

    qintake_gate = pd.read_csv(DATA / "ngc7331_qwarp_observable_choice_review_intake_gate.csv")
    qintake_gate_status = dict(zip(qintake_gate["gate_id"], qintake_gate["gate_status"]))
    assert qintake_gate_status["N7331_QINT1_RESPONSE_PRESENT"] == "PASS"
    assert qintake_gate_status["N7331_QINT2_ALLOWED_DECISION"] == "PASS"
    assert qintake_gate_status["N7331_QINT3_FORBIDDEN_INPUTS"] == "PASS"
    assert qintake_gate_status["N7331_QINT4_SOURCE_INPUTS"] == "PASS"
    assert qintake_gate_status["N7331_QINT5_Q_VALUE_OR_INTERVAL"] == "PASS"
    assert qintake_gate_status["N7331_QINT6_SIGN_EPSILON"] == "PASS"
    assert qintake_gate_status["N7331_QINT7_FORMULA_FREEZE"] == "PASS"
    assert qintake_gate_status["N7331_QINT8_ENDPOINT_BLINDNESS"] == "PASS"
    assert not qintake_gate["endpoint_scores_allowed"].any()
    assert not qintake_gate["uses_vobs_or_residual"].any()

    qintake_summary = pd.read_csv(
        DATA / "ngc7331_qwarp_observable_choice_review_intake_summary.csv"
    ).iloc[0]
    assert qintake_summary["review_intake_status"] == (
        "NGC7331_QWARP_REVIEW_INTAKE_FORMULA_FREEZE_INPUT_READY_NOT_ENDPOINT"
    )
    assert bool(qintake_summary["response_pending"]) is False
    assert bool(qintake_summary["formula_freeze_allowed"]) is True
    assert bool(qintake_summary["endpoint_scores_allowed"]) is False
    assert bool(qintake_summary["uses_vobs_or_residual"]) is False

    subprocess.run(
        ["python", "scripts/build_ngc4088_b2_source_load_origin_derivation_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    source_load_origin_factors = pd.read_csv(
        DATA / "ngc4088_b2_source_load_origin_factors.csv"
    )
    assert len(source_load_origin_factors) == 5
    factor_status = dict(
        zip(source_load_origin_factors["factor_id"], source_load_origin_factors["factor_status"])
    )
    assert factor_status["SLF3_ONSET_SUPPORT"] == "SOURCE_FROZEN_CAVEATED_ACCEPTED"
    assert factor_status["SLF4_ASYMPTOTIC_CARRIER"] == "SOURCE_CATALOG_CANDIDATE_LAW_OPEN"
    lambda_factor = source_load_origin_factors[
        source_load_origin_factors["factor_id"] == "SLF5_SOURCE_LOAD_PRODUCT"
    ].iloc[0]
    assert abs(float(lambda_factor["value"]) - 8795.11175237) < 1.0e-5

    source_load_origin_gates = pd.read_csv(DATA / "ngc4088_b2_source_load_origin_gate.csv")
    assert len(source_load_origin_gates) == 8
    source_load_origin_status = dict(
        zip(source_load_origin_gates["gate_id"], source_load_origin_gates["gate_status"])
    )
    assert source_load_origin_status["SLO1_FREEZE_ALIGNMENT"] == "PASS"
    assert source_load_origin_status["SLO2_DIMENSION_AND_LIMITS"] == "PASS"
    assert source_load_origin_status["SLO3_CLOSURE_FUNCTIONAL_STATIONARITY"] == "PASS"
    assert source_load_origin_status["SLO4_ONSET_SOURCE_ACCEPTANCE"] == "PASS_CAVEATED"
    assert source_load_origin_status["SLO5_STRENGTH_AND_SIGN_LAW"] == "FORMULA_CONDITIONAL"
    assert source_load_origin_status["SLO6_ASYMPTOTIC_CARRIER_THEOREM"] == (
        "CONDITIONAL_CARRIER_THEOREM"
    )
    assert source_load_origin_status["SLO7_CROSS_TERM_SUPPRESSION_BOUND"] == "PARTIAL"
    assert source_load_origin_status["SLO8_POPULATION_TRANSFER"] == "OPEN_FOR_CLAIMS"
    assert not source_load_origin_gates["endpoint_scores_allowed"].any()
    assert not source_load_origin_gates["uses_vobs_or_residual"].any()

    source_load_origin_summary = pd.read_csv(
        DATA / "ngc4088_b2_source_load_origin_summary.csv"
    ).iloc[0]
    assert source_load_origin_summary["source_load_origin_status"] == (
        "SOURCE_LOAD_ORIGIN_PARTIALLY_GROUNDED_CARRIER_AND_CROSS_OPEN"
    )
    assert int(source_load_origin_summary["n_pass_like"]) == 4
    assert int(source_load_origin_summary["n_formula_conditional"]) == 1
    assert int(source_load_origin_summary["n_partial"]) == 1
    assert int(source_load_origin_summary["n_conditional_carrier_theorem"]) == 1
    assert int(source_load_origin_summary["n_open_or_open_for_claims"]) == 1
    assert bool(source_load_origin_summary["law_level_closed"]) is False
    assert bool(source_load_origin_summary["endpoint_scores_allowed"]) is False
    assert bool(source_load_origin_summary["uses_vobs_or_residual"]) is False

    subprocess.run(
        [
            "python",
            "scripts/build_ngc4088_b2_closure_asymptotic_conditional_derivation_gate.py",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    conditional_theorem = pd.read_csv(
        DATA / "ngc4088_b2_closure_asymptotic_conditional_theorem.csv"
    ).iloc[0]
    assert (
        conditional_theorem["theorem_id"]
        == "B2_CLOSURE_ASYMPTOTIC_CONDITIONAL_DERIVATION"
    )
    assert (
        conditional_theorem["mathematical_status"]
        == "ALGEBRAICALLY_DERIVED_GIVEN_TARGET_FUNCTIONAL"
    )
    assert conditional_theorem["tau_side_law_status"] == "FORMULA_CONDITIONAL_PREMISES_OPEN"
    assert bool(conditional_theorem["formula_freeze_alignment_pass"]) is True
    assert abs(float(conditional_theorem["numeric_lambda_w_km2_s2"]) - 8795.11175237) < 1.0e-5
    assert not bool(conditional_theorem["endpoint_scores_allowed"])
    assert not bool(conditional_theorem["uses_vobs_or_residual"])

    conditional_conditions = pd.read_csv(
        DATA / "ngc4088_b2_closure_asymptotic_conditions.csv"
    )
    assert len(conditional_conditions) == 7
    condition_status = dict(
        zip(conditional_conditions["condition_id"], conditional_conditions["current_status"])
    )
    assert condition_status["B2D1_SOURCE_FREEZE_ALIGNMENT"] == "PASS"
    assert condition_status["B2D2_DIMENSIONAL_AND_LIMIT_CHECK"] == "PASS"
    assert condition_status["B2D3_EULER_STATIONARITY_GIVEN_TARGET"] == (
        "FORMULA_CONDITIONAL_PASS"
    )
    assert condition_status["B2D4_CLOSURE_FUNCTIONAL_ORIGIN"] == (
        "CONDITIONAL_FUNCTIONAL_CONSTRUCTED"
    )
    assert condition_status["B2D5_ASYMPTOTIC_CARRIER_ORIGIN"] == (
        "CONDITIONAL_CARRIER_THEOREM"
    )
    assert condition_status["B2D6_SEPARABILITY_AND_CROSS_TERM_BOUND"] == (
        "PARTIAL_SOURCE_BOUND"
    )
    assert condition_status["B2D7_POPULATION_TRANSFER"] == "OPEN_FOR_CLAIMS"
    assert not conditional_conditions["endpoint_scores_allowed"].any()
    assert not conditional_conditions["uses_vobs_or_residual"].any()

    conditional_summary = pd.read_csv(
        DATA / "ngc4088_b2_closure_asymptotic_summary.csv"
    ).iloc[0]
    assert conditional_summary["b2_conditional_derivation_status"] == (
        "B2_CONDITIONAL_THEOREM_ALIGNED_TO_FREEZE_MANIFEST_LAW_PREMISES_OPEN"
    )
    assert bool(conditional_summary["formula_freeze_alignment_pass"]) is True
    assert int(conditional_summary["n_conditions"]) == 7
    assert int(conditional_summary["n_pass_or_formula_conditional_pass"]) == 5
    assert int(conditional_summary["n_open_law_premises"]) == 3
    assert bool(conditional_summary["law_level_closed"]) is False
    assert bool(conditional_summary["endpoint_scores_allowed"]) is False
    assert bool(conditional_summary["uses_vobs_or_residual"]) is False

    ngc4088_target_factors = pd.read_csv(
        DATA / "s4g75_ngc4088_target_functional_origin_factors.csv"
    )
    assert len(ngc4088_target_factors) == 6
    factor_status = dict(
        zip(ngc4088_target_factors["factor_id"], ngc4088_target_factors["origin_status"])
    )
    assert factor_status["X_WARP_ONSET"] == "SOURCE_MEASURED_ONSET_FRACTION"
    assert (
        factor_status["VFLAT2_CARRIER"]
        == "SOURCE_CATALOG_SCALE_CANDIDATE_NOT_DERIVED_CARRIER"
    )
    assert factor_status["MULTIPLICATIVE_COUPLING"] == "TARGET_COMPOSITE_FORMULA_CONDITIONAL"
    assert factor_status["QUADRATIC_TARGET_PENALTY"] == "TARGET_PENALTY_NOT_TAU_SIDE_DERIVED"
    coupling = ngc4088_target_factors[
        ngc4088_target_factors["factor_id"] == "MULTIPLICATIVE_COUPLING"
    ].iloc[0]
    assert abs(float(coupling["factor_value"]) - 8324.016) < 1.0e-9
    assert coupling["unit"] == "km2_s2"

    ngc4088_target_origin_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_target_functional_origin_gate.csv"
    )
    assert len(ngc4088_target_origin_gate) == 7
    target_origin_status = dict(
        zip(
            ngc4088_target_origin_gate["gate_id"],
            ngc4088_target_origin_gate["gate_status"],
        )
    )
    assert {
        gate_id for gate_id, status in target_origin_status.items() if status == "PASS"
    } == {
        "T1_SOURCE_FACTORS_AVAILABLE",
        "T2_DIMENSIONAL_PRODUCT_VALID",
        "T7_ENDPOINT_BLINDNESS",
    }
    assert {
        gate_id
        for gate_id, status in target_origin_status.items()
        if status == "FORMULA_CONDITIONAL"
    } == {
        "T3_ONSET_FACTOR_SOURCE_GROUNDED",
        "T4_ASYMPTOTIC_CARRIER_SOURCE_GROUNDED",
    }
    assert {
        gate_id for gate_id, status in target_origin_status.items() if status == "BLOCKED"
    } == {
        "T5_MULTIPLICATIVE_COUPLING_DERIVED",
        "T6_QUADRATIC_PENALTY_DERIVED",
    }
    assert not ngc4088_target_origin_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_target_origin_gate["endpoint_scores_allowed"].any()

    ngc4088_target_origin_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_target_functional_origin_summary.csv"
    ).iloc[0]
    assert int(ngc4088_target_origin_summary["n_factors"]) == 6
    assert int(ngc4088_target_origin_summary["n_gates"]) == 7
    assert int(ngc4088_target_origin_summary["n_pass"]) == 3
    assert int(ngc4088_target_origin_summary["n_formula_conditional"]) == 2
    assert int(ngc4088_target_origin_summary["n_blocked"]) == 2
    assert (
        ngc4088_target_origin_summary["target_origin_status"]
        == "SOURCE_FACTORS_AVAILABLE_COUPLING_NOT_DERIVED"
    )
    assert (
        ngc4088_target_origin_summary["law_status"]
        == "TARGET_TERM_NOT_TAU_SIDE_DERIVED"
    )
    assert bool(ngc4088_target_origin_summary["endpoint_scores_allowed"]) is False

    ngc4088_coupling_theorem = pd.read_csv(
        DATA / "s4g75_ngc4088_multiplicative_coupling_theorem.csv"
    ).iloc[0]
    assert (
        ngc4088_coupling_theorem["theorem_id"]
        == "CONDITIONAL_SEPARABLE_SOURCE_READOUT_PRODUCT"
    )
    assert (
        ngc4088_coupling_theorem["proof_status"]
        == "FORMULA_DERIVED_GIVEN_SEPARABILITY_ASSUMPTIONS"
    )
    assert abs(float(ngc4088_coupling_theorem["derived_product_value_km2_s2"]) - 8324.016) < 1.0e-9

    ngc4088_coupling_assumptions = pd.read_csv(
        DATA / "s4g75_ngc4088_multiplicative_coupling_assumptions.csv"
    )
    assert len(ngc4088_coupling_assumptions) == 6
    assumption_status = dict(
        zip(
            ngc4088_coupling_assumptions["assumption_id"],
            ngc4088_coupling_assumptions["assumption_status"],
        )
    )
    assert assumption_status["S1_FACTOR_SEPARABILITY"] == "ASSUMPTION_NOT_DERIVED"
    assert assumption_status["S6_NO_CROSS_TERMS_AT_FIRST_ORDER"] == "ASSUMPTION_NOT_DERIVED"
    assert assumption_status["S5_ASYMPTOTIC_CARRIER"] == "SOURCE_CATALOG_CANDIDATE_NOT_DERIVED"

    ngc4088_coupling_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_multiplicative_coupling_separability_gate.csv"
    )
    assert len(ngc4088_coupling_gate) == 7
    coupling_status = dict(zip(ngc4088_coupling_gate["gate_id"], ngc4088_coupling_gate["gate_status"]))
    assert {
        gate_id for gate_id, status in coupling_status.items() if status == "PASS"
    } == {
        "M1_PRODUCT_ALGEBRA",
        "M2_DIMENSIONAL_CONSISTENCY",
    }
    assert {
        gate_id for gate_id, status in coupling_status.items() if status == "FORMULA_CONDITIONAL"
    } == {
        "M3_SEPARABILITY_ASSUMPTION",
        "M4_SOURCE_FACTOR_GROUNDING",
        "M5_CARRIER_GROUNDING",
    }
    assert {
        gate_id for gate_id, status in coupling_status.items() if status == "BLOCKED"
    } == {
        "M6_NO_CROSS_TERMS",
        "M7_POPULATION_TRANSFER",
    }
    assert not ngc4088_coupling_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_coupling_gate["endpoint_scores_allowed"].any()

    ngc4088_coupling_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_multiplicative_coupling_separability_summary.csv"
    ).iloc[0]
    assert int(ngc4088_coupling_summary["n_assumptions"]) == 6
    assert int(ngc4088_coupling_summary["n_gates"]) == 7
    assert int(ngc4088_coupling_summary["n_pass"]) == 2
    assert int(ngc4088_coupling_summary["n_formula_conditional"]) == 3
    assert int(ngc4088_coupling_summary["n_blocked"]) == 2
    assert (
        ngc4088_coupling_summary["coupling_status"]
        == "CONDITIONAL_PRODUCT_DERIVED_IF_SEPARABLE"
    )
    assert (
        ngc4088_coupling_summary["law_status"]
        == "SEPARABILITY_AND_CROSS_TERM_SUPPRESSION_NOT_DERIVED"
    )
    assert bool(ngc4088_coupling_summary["endpoint_scores_allowed"]) is False

    ngc4088_cross_model = pd.read_csv(DATA / "s4g75_ngc4088_cross_term_model.csv").iloc[0]
    assert ngc4088_cross_model["model_id"] == "LEADING_PRODUCT_PLUS_EPSILON_CROSS"
    assert "epsilon_cross" in ngc4088_cross_model["extended_formula"]
    assert abs(float(ngc4088_cross_model["lambda0_km2_s2"]) - 8324.016) < 1.0e-9
    assert (
        ngc4088_cross_model["proof_status"]
        == "LEADING_ORDER_ONLY_UNTIL_CROSS_TERMS_SUPPRESSED"
    )

    ngc4088_cross_ledger = pd.read_csv(DATA / "s4g75_ngc4088_cross_term_ledger.csv")
    assert len(ngc4088_cross_ledger) == 4
    assert set(ngc4088_cross_ledger["term_status"]) == {"NOT_DERIVED"}
    assert {
        "CROSS_ORIENTATION_STRENGTH",
        "CROSS_ONSET_STRENGTH",
        "CROSS_ONSET_CARRIER",
        "CROSS_GEOMETRY_MEMORY",
    } == set(ngc4088_cross_ledger["term_id"])

    ngc4088_cross_gate = pd.read_csv(DATA / "s4g75_ngc4088_cross_term_suppression_gate.csv")
    assert len(ngc4088_cross_gate) == 7
    cross_status = dict(zip(ngc4088_cross_gate["gate_id"], ngc4088_cross_gate["gate_status"]))
    assert {
        gate_id for gate_id, status in cross_status.items() if status == "PASS"
    } == {
        "X1_LEADING_PRODUCT_AVAILABLE",
        "X2_DIMENSIONAL_EXTENSION_VALID",
        "X4_ZERO_CROSS_TERM_LIMIT",
        "X7_ENDPOINT_BLINDNESS",
    }
    assert {
        gate_id for gate_id, status in cross_status.items() if status == "FORMULA_CONDITIONAL"
    } == {"X3_CROSS_TERM_PARAMETER_DECLARED"}
    assert {
        gate_id for gate_id, status in cross_status.items() if status == "BLOCKED"
    } == {
        "X5_CROSS_TERM_SUPPRESSION_DERIVED",
        "X6_SOURCE_BOUND_AVAILABLE",
    }
    assert not ngc4088_cross_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_cross_gate["endpoint_scores_allowed"].any()

    ngc4088_cross_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_cross_term_suppression_summary.csv"
    ).iloc[0]
    assert int(ngc4088_cross_summary["n_cross_terms"]) == 4
    assert int(ngc4088_cross_summary["n_gates"]) == 7
    assert int(ngc4088_cross_summary["n_pass"]) == 4
    assert int(ngc4088_cross_summary["n_formula_conditional"]) == 1
    assert int(ngc4088_cross_summary["n_blocked"]) == 2
    assert ngc4088_cross_summary["cross_term_status"] == "CROSS_TERMS_DECLARED_NOT_SUPPRESSED"
    assert (
        ngc4088_cross_summary["law_status"]
        == "LEADING_PRODUCT_ONLY_UNTIL_EPSILON_CROSS_BOUND"
    )
    assert bool(ngc4088_cross_summary["endpoint_scores_allowed"]) is False

    ngc4088_epsilon_observables = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_source_observables.csv"
    )
    assert len(ngc4088_epsilon_observables) == 5
    epsilon_observable_status = dict(
        zip(
            ngc4088_epsilon_observables["observable_id"],
            ngc4088_epsilon_observables["availability_status"],
        )
    )
    assert (
        epsilon_observable_status["O1_ORIENTATION_MISMATCH"]
        == "AVAILABLE_FIRST_PASS_NOT_INDEPENDENTLY_REVIEWED"
    )
    assert (
        epsilon_observable_status["O4_SOURCE_STRENGTH_AMPLITUDE"]
        == "MISSING_QUANTITATIVE_SOURCE_AMPLITUDE"
    )
    assert (
        epsilon_observable_status["O5_MEMORY_HISTORY_PROXY"]
        == "MISSING_HISTORY_MEMORY_SOURCE_PROXY"
    )
    epsilon_values = dict(
        zip(ngc4088_epsilon_observables["observable_id"], ngc4088_epsilon_observables["current_value"])
    )
    assert abs(float(epsilon_values["O1_ORIENTATION_MISMATCH"]) - 90.0) < 1.0e-12
    assert abs(float(epsilon_values["O2_SIDE_ASYMMETRY"]) - 0.4) < 1.0e-12
    assert abs(float(epsilon_values["O3_ONSET_UNCERTAINTY_FRACTION"]) - 0.25) < 1.0e-12

    ngc4088_epsilon_protocol = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_bound_protocol.csv"
    ).iloc[0]
    assert (
        ngc4088_epsilon_protocol["protocol_id"]
        == "EPSILON_CROSS_RESIDUAL_BLIND_SOURCE_BOUND_PROTOCOL"
    )
    assert "epsilon_cross" in ngc4088_epsilon_protocol["bound_form"]
    assert "vobs" in ngc4088_epsilon_protocol["forbidden_inputs"]
    assert (
        ngc4088_epsilon_protocol["current_status"]
        == "BOUND_FORM_DECLARED_NUMERIC_BOUND_BLOCKED"
    )

    ngc4088_epsilon_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_source_bound_gate.csv"
    )
    assert len(ngc4088_epsilon_gate) == 7
    epsilon_gate_status = dict(
        zip(ngc4088_epsilon_gate["gate_id"], ngc4088_epsilon_gate["gate_status"])
    )
    assert {
        gate_id for gate_id, status in epsilon_gate_status.items() if status == "PASS"
    } == {
        "B1_BOUND_FORM_DECLARED",
        "B2_ENDPOINT_BLINDNESS",
        "B7_CROSS_TERM_GATE_CONNECTION",
    }
    assert {
        gate_id
        for gate_id, status in epsilon_gate_status.items()
        if status == "FORMULA_CONDITIONAL"
    } == {"B3_PARTIAL_SOURCE_OBSERVABLES_AVAILABLE"}
    assert {
        gate_id for gate_id, status in epsilon_gate_status.items() if status == "BLOCKED"
    } == {
        "B4_QUANTITATIVE_Q_WARP_AVAILABLE",
        "B5_MEMORY_PROXY_AVAILABLE",
        "B6_BOUND_COEFFICIENTS_DERIVED",
    }
    assert not ngc4088_epsilon_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_epsilon_gate["endpoint_scores_allowed"].any()

    ngc4088_epsilon_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_source_bound_summary.csv"
    ).iloc[0]
    assert int(ngc4088_epsilon_summary["n_observables"]) == 5
    assert int(ngc4088_epsilon_summary["n_available_observables"]) == 3
    assert int(ngc4088_epsilon_summary["n_missing_observables"]) == 2
    assert int(ngc4088_epsilon_summary["n_pass"]) == 3
    assert int(ngc4088_epsilon_summary["n_formula_conditional"]) == 1
    assert int(ngc4088_epsilon_summary["n_blocked"]) == 3
    assert (
        ngc4088_epsilon_summary["bound_status"]
        == "SOURCE_BOUND_PROTOCOL_PARTIAL_NUMERIC_BOUND_BLOCKED"
    )
    assert (
        ngc4088_epsilon_summary["epsilon_cross_status"]
        == "SYMBOLIC_UNBOUNDED_UNTIL_Q_AND_MEMORY_READY"
    )
    assert bool(ngc4088_epsilon_summary["endpoint_scores_allowed"]) is False

    ngc4088_qwarp_protocol = pd.read_csv(
        DATA / "s4g75_ngc4088_qwarp_measurement_protocol.csv"
    ).iloc[0]
    assert (
        ngc4088_qwarp_protocol["protocol_id"]
        == "QWARP_CHANNEL_MAP_SOURCE_STRENGTH_PROTOCOL"
    )
    assert "outer_asymmetry_extent" in ngc4088_qwarp_protocol["definition"]
    assert "vobs" in ngc4088_qwarp_protocol["forbidden_inputs"]
    assert (
        ngc4088_qwarp_protocol["current_status"]
        == "PROTOCOL_READY_MEASUREMENT_RESPONSE_EMPTY"
    )

    ngc4088_qwarp_fields = pd.read_csv(DATA / "s4g75_ngc4088_qwarp_measurement_fields.csv")
    assert len(ngc4088_qwarp_fields) == 5
    assert {
        "outer_asymmetry_extent_px",
        "local_disk_reference_extent_px",
        "panel_source_weight",
        "side_label",
        "review_flag",
    } == set(ngc4088_qwarp_fields["field_name"])
    assert ngc4088_qwarp_fields["required"].all()

    ngc4088_qwarp_response = pd.read_csv(
        DATA / "s4g75_ngc4088_qwarp_measurement_response_template.csv"
    ).iloc[0]
    assert ngc4088_qwarp_response["response_status"] == "MEASUREMENT_EMPTY"
    assert pd.isna(ngc4088_qwarp_response["q_warp_measured"])
    assert pd.isna(ngc4088_qwarp_response["q_warp_uncertainty"])
    assert int(ngc4088_qwarp_response["n_panel_measurements_required"]) == 23
    assert bool(ngc4088_qwarp_response["endpoint_scores_allowed"]) is False

    ngc4088_qwarp_gate = pd.read_csv(DATA / "s4g75_ngc4088_qwarp_measurement_gate.csv")
    assert len(ngc4088_qwarp_gate) == 6
    qwarp_status = dict(zip(ngc4088_qwarp_gate["gate_id"], ngc4088_qwarp_gate["gate_status"]))
    assert {
        gate_id for gate_id, status in qwarp_status.items() if status == "PASS"
    } == {
        "Q1_PROTOCOL_DEFINED",
        "Q2_SOURCE_IMAGES_AVAILABLE",
        "Q3_PANEL_WORKSHEET_READY",
        "Q6_ENDPOINT_BLINDNESS",
    }
    assert {
        gate_id for gate_id, status in qwarp_status.items() if status == "BLOCKED"
    } == {
        "Q4_RESPONSE_FILLED",
        "Q5_INDEPENDENT_REVIEW",
    }
    assert not ngc4088_qwarp_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_qwarp_gate["endpoint_scores_allowed"].any()

    ngc4088_qwarp_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_qwarp_measurement_summary.csv"
    ).iloc[0]
    assert int(ngc4088_qwarp_summary["n_measurement_fields"]) == 5
    assert int(ngc4088_qwarp_summary["n_panel_measurements_required"]) == 23
    assert int(ngc4088_qwarp_summary["n_pass"]) == 4
    assert int(ngc4088_qwarp_summary["n_blocked"]) == 2
    assert ngc4088_qwarp_summary["q_warp_status"] == "QWARP_PROTOCOL_READY_MEASUREMENT_BLOCKED"
    assert (
        ngc4088_qwarp_summary["epsilon_cross_impact"]
        == "UNBLOCKS_Q_COMPONENT_AFTER_MEASUREMENT_AND_REVIEW"
    )
    assert bool(ngc4088_qwarp_summary["endpoint_scores_allowed"]) is False

    ngc4088_memory_protocol = pd.read_csv(
        DATA / "s4g75_ngc4088_memory_history_proxy_protocol.csv"
    ).iloc[0]
    assert (
        ngc4088_memory_protocol["protocol_id"]
        == "NGC4088_WARP_MEMORY_HISTORY_SOURCE_PROXY_PROTOCOL"
    )
    assert "weighted_source_score" in ngc4088_memory_protocol["proxy_definition"]
    assert "rotation-inferred family" in ngc4088_memory_protocol["forbidden_inputs"]
    assert ngc4088_memory_protocol["current_status"] == "PROTOCOL_READY_RESPONSE_EMPTY"

    ngc4088_memory_components = pd.read_csv(
        DATA / "s4g75_ngc4088_memory_history_proxy_components.csv"
    )
    assert len(ngc4088_memory_components) == 4
    assert set(ngc4088_memory_components["component_id"]) == {
        "H1_WARP_PERSISTENCE",
        "H2_HI_LOPSIDEDNESS",
        "H3_OUTER_DISK_ASYMMETRY",
        "H4_INTERACTION_CONTEXT",
    }
    assert (
        ngc4088_memory_components["availability_status"]
        .value_counts()
        .to_dict()
    ) == {
        "MEASUREMENT_REQUIRED": 3,
        "SOURCE_REVIEW_REQUIRED": 1,
    }

    ngc4088_memory_response = pd.read_csv(
        DATA / "s4g75_ngc4088_memory_history_proxy_response_template.csv"
    ).iloc[0]
    assert ngc4088_memory_response["response_status"] == "MEASUREMENT_EMPTY"
    assert pd.isna(ngc4088_memory_response["m_history_warp"])
    assert pd.isna(ngc4088_memory_response["m_history_uncertainty"])
    assert int(ngc4088_memory_response["n_components_measured"]) == 0
    assert int(ngc4088_memory_response["n_components_required"]) == 4
    assert bool(ngc4088_memory_response["source_ready_whisp"]) is True
    assert bool(ngc4088_memory_response["uses_rotation_inferred_proxy"]) is False
    assert bool(ngc4088_memory_response["uses_vobs_or_residual"]) is False
    assert bool(ngc4088_memory_response["endpoint_scores_allowed"]) is False

    ngc4088_memory_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_memory_history_proxy_gate.csv"
    )
    assert len(ngc4088_memory_gate) == 6
    memory_status = dict(
        zip(ngc4088_memory_gate["gate_id"], ngc4088_memory_gate["gate_status"])
    )
    assert {
        gate_id for gate_id, status in memory_status.items() if status == "PASS"
    } == {
        "H1_PROTOCOL_DEFINED",
        "H2_SOURCE_LANE_AVAILABLE",
        "H3_INVERSE_PROXY_EXCLUDED",
    }
    assert {
        gate_id for gate_id, status in memory_status.items() if status == "BLOCKED"
    } == {
        "H4_COMPONENT_MEASUREMENTS_FILLED",
        "H5_INDEPENDENT_REVIEW",
    }
    assert {
        gate_id for gate_id, status in memory_status.items() if status == "FORMULA_CONDITIONAL"
    } == {
        "H6_EPSILON_BOUND_CONNECTION",
    }
    assert not ngc4088_memory_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_memory_gate["endpoint_scores_allowed"].any()

    ngc4088_memory_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_memory_history_proxy_summary.csv"
    ).iloc[0]
    assert int(ngc4088_memory_summary["n_components"]) == 4
    assert int(ngc4088_memory_summary["n_components_measured"]) == 0
    assert bool(ngc4088_memory_summary["source_ready_whisp"]) is True
    assert int(ngc4088_memory_summary["n_gates"]) == 6
    assert int(ngc4088_memory_summary["n_pass"]) == 3
    assert int(ngc4088_memory_summary["n_formula_conditional"]) == 1
    assert int(ngc4088_memory_summary["n_blocked"]) == 2
    assert (
        ngc4088_memory_summary["memory_proxy_status"]
        == "MEMORY_PROTOCOL_READY_MEASUREMENT_BLOCKED"
    )
    assert (
        ngc4088_memory_summary["epsilon_cross_impact"]
        == "UNBLOCKS_MEMORY_COMPONENT_AFTER_MEASUREMENT_AND_REVIEW"
    )
    assert bool(ngc4088_memory_summary["uses_vobs_or_residual"]) is False
    assert bool(ngc4088_memory_summary["endpoint_scores_allowed"]) is False

    ngc4088_qwarp_first_pass = pd.read_csv(
        DATA / "s4g75_ngc4088_qwarp_first_pass_response.csv"
    ).iloc[0]
    assert ngc4088_qwarp_first_pass["response_id"] == "QWARP_FIRST_PASS_SOURCE_RESPONSE_V1"
    assert abs(float(ngc4088_qwarp_first_pass["q_warp_measured"]) - 1.0) < 1.0e-12
    assert abs(float(ngc4088_qwarp_first_pass["q_warp_uncertainty"]) - 0.25) < 1.0e-12
    assert int(ngc4088_qwarp_first_pass["n_panels_used"]) == 23
    assert (
        ngc4088_qwarp_first_pass["response_status"]
        == "FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED"
    )
    assert bool(ngc4088_qwarp_first_pass["accepted_for_numeric_bound"]) is False
    assert bool(ngc4088_qwarp_first_pass["uses_vobs_or_residual"]) is False
    assert bool(ngc4088_qwarp_first_pass["endpoint_scores_allowed"]) is False

    ngc4088_memory_first_pass_components = pd.read_csv(
        DATA / "s4g75_ngc4088_memory_history_first_pass_components.csv"
    )
    assert len(ngc4088_memory_first_pass_components) == 4
    assert int(ngc4088_memory_first_pass_components["component_value"].notna().sum()) == 3
    assert set(
        ngc4088_memory_first_pass_components.loc[
            ngc4088_memory_first_pass_components["component_value"].notna(),
            "component_value",
        ]
    ) == {1.0}
    assert "SOURCE_REVIEW_REQUIRED" in set(
        ngc4088_memory_first_pass_components["component_status"]
    )
    assert not ngc4088_memory_first_pass_components["uses_vobs_or_residual"].any()
    assert not ngc4088_memory_first_pass_components["endpoint_scores_allowed"].any()

    ngc4088_memory_first_pass = pd.read_csv(
        DATA / "s4g75_ngc4088_memory_history_first_pass_response.csv"
    ).iloc[0]
    assert (
        ngc4088_memory_first_pass["response_id"]
        == "NGC4088_MEMORY_HISTORY_FIRST_PASS_RESPONSE_V1"
    )
    assert abs(float(ngc4088_memory_first_pass["m_history_warp"]) - 1.0) < 1.0e-12
    assert abs(float(ngc4088_memory_first_pass["m_history_uncertainty"]) - 0.25) < 1.0e-12
    assert int(ngc4088_memory_first_pass["n_components_measured"]) == 3
    assert (
        ngc4088_memory_first_pass["response_status"]
        == "PARTIAL_FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED"
    )
    assert bool(ngc4088_memory_first_pass["accepted_for_numeric_bound"]) is False
    assert bool(ngc4088_memory_first_pass["uses_rotation_inferred_proxy"]) is False
    assert bool(ngc4088_memory_first_pass["uses_vobs_or_residual"]) is False
    assert bool(ngc4088_memory_first_pass["endpoint_scores_allowed"]) is False

    ngc4088_first_pass_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_first_pass_source_response_fill_gate.csv"
    )
    first_pass_status = dict(
        zip(ngc4088_first_pass_gate["gate_id"], ngc4088_first_pass_gate["gate_status"])
    )
    assert {
        gate_id for gate_id, status in first_pass_status.items() if status == "FORMULA_CONDITIONAL"
    } == {"FP1_Q_SOURCE_FILL_AVAILABLE", "FP2_MEMORY_SOURCE_FILL_AVAILABLE"}
    assert {
        gate_id for gate_id, status in first_pass_status.items() if status == "PASS"
    } == {"FP3_ENDPOINT_BLINDNESS"}
    assert {
        gate_id for gate_id, status in first_pass_status.items() if status == "BLOCKED"
    } == {"FP4_NUMERIC_BOUND_AUTHORIZATION"}

    ngc4088_first_pass_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_first_pass_source_response_fill_summary.csv"
    ).iloc[0]
    assert (
        ngc4088_first_pass_summary["fill_status"]
        == "FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED"
    )
    assert abs(float(ngc4088_first_pass_summary["q_warp_measured"]) - 1.0) < 1.0e-12
    assert abs(float(ngc4088_first_pass_summary["m_history_warp"]) - 1.0) < 1.0e-12
    assert int(ngc4088_first_pass_summary["n_memory_components_measured"]) == 3
    assert bool(ngc4088_first_pass_summary["accepted_for_numeric_bound"]) is False
    assert bool(ngc4088_first_pass_summary["uses_vobs_or_residual"]) is False
    assert bool(ngc4088_first_pass_summary["endpoint_scores_allowed"]) is False

    ngc4088_h4_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_h4_interaction_context_review_summary.csv"
    ).iloc[0]
    assert (
        ngc4088_h4_summary["h4_review_status"]
        == "H4_INTERACTION_CONTEXT_ACCEPTED_SOURCE_REVIEWED"
    )
    assert abs(float(ngc4088_h4_summary["accepted_h4_interaction_context"]) - 1.0) < 1.0e-12
    assert bool(ngc4088_h4_summary["uses_vobs_or_residual"]) is False
    assert bool(ngc4088_h4_summary["endpoint_scores_allowed"]) is False

    ngc4088_source_review = pd.read_csv(
        DATA / "s4g75_ngc4088_source_response_independent_review.csv"
    )
    assert len(ngc4088_source_review) == 2
    assert set(ngc4088_source_review["review_target"]) == {
        "q_warp_measured",
        "m_history_warp",
    }
    assert ngc4088_source_review["accepted_for_numeric_bound"].all()
    assert set(
        ngc4088_source_review["review_status"]
    ) == {"ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND"}
    assert not ngc4088_source_review["uses_vobs_or_residual"].any()
    assert not ngc4088_source_review["endpoint_scores_allowed"].any()

    ngc4088_source_review_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_source_response_independent_review_gate.csv"
    )
    assert len(ngc4088_source_review_gate) == 5
    assert set(ngc4088_source_review_gate["gate_status"]) == {"PASS"}
    assert not ngc4088_source_review_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_source_review_gate["endpoint_scores_allowed"].any()

    ngc4088_source_review_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_source_response_independent_review_summary.csv"
    ).iloc[0]
    assert (
        ngc4088_source_review_summary["source_review_status"]
        == "SOURCE_RESPONSES_ACCEPTED_FOR_PROTOCOL_BOUND"
    )
    assert bool(
        ngc4088_source_review_summary["numeric_bound_source_authorization"]
    ) is True
    assert abs(float(ngc4088_source_review_summary["accepted_q_warp_measured"]) - 1.0) < 1.0e-12
    assert abs(float(ngc4088_source_review_summary["accepted_m_history_warp"]) - 1.0) < 1.0e-12

    ngc4088_frozen_bi = pd.read_csv(
        DATA / "s4g75_ngc4088_bi_frozen_coefficients.csv"
    )
    assert len(ngc4088_frozen_bi) == 4
    assert set(ngc4088_frozen_bi["coefficient_id"]) == {
        "B_PA",
        "B_R",
        "B_q",
        "B_mem",
    }
    assert set(ngc4088_frozen_bi["frozen_value"]) == {1.0}
    assert set(ngc4088_frozen_bi["freeze_status"]) == {
        "FROZEN_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT"
    }
    assert set(ngc4088_frozen_bi["derivation_status"]) == {
        "PROTOCOL_BOUND_NOT_FINAL_TAU_SIDE_DERIVATION"
    }
    assert not ngc4088_frozen_bi["uses_vobs_or_residual"].any()
    assert not ngc4088_frozen_bi["endpoint_scores_allowed"].any()

    ngc4088_bi_freeze_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_bi_coefficient_freeze_rule_gate.csv"
    )
    assert len(ngc4088_bi_freeze_gate) == 5
    assert set(ngc4088_bi_freeze_gate["gate_status"]) == {"PASS"}
    assert not ngc4088_bi_freeze_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_bi_freeze_gate["endpoint_scores_allowed"].any()

    ngc4088_bi_freeze_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_bi_coefficient_freeze_rule_summary.csv"
    ).iloc[0]
    assert (
        ngc4088_bi_freeze_summary["freeze_rule_status"]
        == "BI_COEFFICIENTS_FROZEN_PROTOCOL_BOUND_READY"
    )
    assert bool(
        ngc4088_bi_freeze_summary["numeric_bound_coefficient_authorization"]
    ) is True

    ngc4088_sharp_bi = pd.read_csv(
        DATA / "s4g75_ngc4088_bi_sharp_coefficients.csv"
    )
    assert len(ngc4088_sharp_bi) == 4
    assert set(ngc4088_sharp_bi["coefficient_id"]) == {
        "B_PA",
        "B_R",
        "B_q",
        "B_mem",
    }
    assert set(ngc4088_sharp_bi["sharp_value"]) == {0.5}
    assert set(ngc4088_sharp_bi["sharp_status"]) == {
        "SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT"
    }
    assert set(ngc4088_sharp_bi["derivation_status"]) == {
        "FORMULA_CONDITIONAL_NOT_FINAL_TAU_SIDE_AMPLITUDE_DERIVATION"
    }
    assert not ngc4088_sharp_bi["uses_vobs_or_residual"].any()
    assert not ngc4088_sharp_bi["endpoint_scores_allowed"].any()

    ngc4088_sharp_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_bi_sharp_coefficient_bound_rule_summary.csv"
    ).iloc[0]
    assert (
        ngc4088_sharp_summary["sharp_rule_status"]
        == "BI_COEFFICIENTS_SHARPENED_PROTOCOL_BOUND_READY"
    )
    assert bool(
        ngc4088_sharp_summary["numeric_bound_coefficient_authorization"]
    ) is True

    ngc4088_input_obligations = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_input_review_obligations.csv"
    )
    assert len(ngc4088_input_obligations) == 6
    assert set(ngc4088_input_obligations["obligation_class"]) == {
        "SOURCE_MEASUREMENT",
        "COEFFICIENT_RULE",
    }
    assert set(
        ngc4088_input_obligations.loc[
            ngc4088_input_obligations["obligation_class"] == "SOURCE_MEASUREMENT",
            "required_input",
        ]
    ) == {"q_warp_measured", "m_history_warp"}
    assert set(
        ngc4088_input_obligations.loc[
            ngc4088_input_obligations["obligation_class"] == "COEFFICIENT_RULE",
            "required_input",
        ]
    ) == {"B_PA", "B_R", "B_q", "B_mem"}
    assert "ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND" in set(
        ngc4088_input_obligations["current_status"]
    )
    assert "SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT" in set(
        ngc4088_input_obligations["current_status"]
    )
    assert not ngc4088_input_obligations["uses_vobs_or_residual"].any()
    assert not ngc4088_input_obligations["endpoint_scores_allowed"].any()

    ngc4088_input_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_input_review_gate.csv"
    )
    assert len(ngc4088_input_gate) == 5
    input_status = dict(zip(ngc4088_input_gate["gate_id"], ngc4088_input_gate["gate_status"]))
    assert {
        gate_id for gate_id, status in input_status.items() if status == "PASS"
    } == {
        "EIN1_Q_PROTOCOL_READY",
        "EIN2_MEMORY_PROTOCOL_READY",
        "EIN3_COEFFICIENT_RULES_DECLARED",
        "EIN4_NUMERIC_BOUND_AUTHORIZED",
        "EIN5_ENDPOINT_BLINDNESS",
    }
    assert not {gate_id for gate_id, status in input_status.items() if status == "BLOCKED"}
    assert not ngc4088_input_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_input_gate["endpoint_scores_allowed"].any()

    ngc4088_input_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_input_review_summary.csv"
    ).iloc[0]
    assert (
        ngc4088_input_summary["packet_id"]
        == "NGC4088_EPSILON_CROSS_INPUT_REVIEW_PACKET"
    )
    assert int(ngc4088_input_summary["n_obligations"]) == 6
    assert int(ngc4088_input_summary["n_source_measurement_obligations"]) == 2
    assert int(ngc4088_input_summary["n_coefficient_rule_obligations"]) == 4
    assert int(ngc4088_input_summary["n_pass"]) == 5
    assert int(ngc4088_input_summary["n_blocked"]) == 0
    assert (
        ngc4088_input_summary["input_review_status"]
        == "INPUT_REVIEW_PACKET_NUMERIC_PROTOCOL_BOUND_READY"
    )
    assert (
        ngc4088_input_summary["next_required_action"]
        == "evaluate_numeric_epsilon_cross_protocol_bound"
    )
    assert bool(ngc4088_input_summary["uses_vobs_or_residual"]) is False
    assert bool(ngc4088_input_summary["endpoint_scores_allowed"]) is False

    ngc4088_bi_features = pd.read_csv(
        DATA / "s4g75_ngc4088_bi_feature_normalization.csv"
    )
    assert len(ngc4088_bi_features) == 4
    assert set(ngc4088_bi_features["feature_symbol"]) == {"f_PA", "f_R", "f_q", "f_mem"}
    feature_by_symbol = dict(
        zip(ngc4088_bi_features["feature_symbol"], ngc4088_bi_features["feature_value"])
    )
    assert abs(float(feature_by_symbol["f_PA"]) - 0.5) < 1.0e-12
    assert abs(float(feature_by_symbol["f_R"]) - 0.25) < 1.0e-12
    assert abs(float(feature_by_symbol["f_q"]) - 1.0) < 1.0e-12
    assert abs(float(feature_by_symbol["f_mem"]) - 1.0) < 1.0e-12
    status_by_feature = dict(
        zip(ngc4088_bi_features["feature_symbol"], ngc4088_bi_features["status"])
    )
    assert status_by_feature["f_PA"] == "ACCEPTED_FROM_FROZEN_DIGITIZATION_VALIDATION"
    assert status_by_feature["f_R"] == "ACCEPTED_FROM_FROZEN_DIGITIZATION_VALIDATION"
    assert status_by_feature["f_q"] == "ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND"
    assert status_by_feature["f_mem"] == "ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND"
    assert set(ngc4088_bi_features["unit"]) == {"dimensionless"}
    assert not ngc4088_bi_features["uses_vobs_or_residual"].any()
    assert not ngc4088_bi_features["endpoint_scores_allowed"].any()

    ngc4088_bi_coefficients = pd.read_csv(
        DATA / "s4g75_ngc4088_bi_coefficient_obligations.csv"
    )
    assert len(ngc4088_bi_coefficients) == 4
    assert set(ngc4088_bi_coefficients["coefficient_id"]) == {
        "B_PA",
        "B_R",
        "B_q",
        "B_mem",
    }
    assert set(ngc4088_bi_coefficients["unit"]) == {"dimensionless"}
    assert set(ngc4088_bi_coefficients["status"]) == {
        "SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT"
    }
    assert set(ngc4088_bi_coefficients["current_value"]) == {0.5}
    assert set(ngc4088_bi_coefficients["active_coefficient_source"]) == {
        "second_order_remainder_half_bound"
    }
    assert "endpoint residuals" in ";".join(ngc4088_bi_coefficients["forbidden_origin"])
    assert not ngc4088_bi_coefficients["uses_vobs_or_residual"].any()
    assert not ngc4088_bi_coefficients["endpoint_scores_allowed"].any()

    ngc4088_bi_gate = pd.read_csv(DATA / "s4g75_ngc4088_bi_coefficient_rule_gate.csv")
    assert len(ngc4088_bi_gate) == 6
    bi_status = dict(zip(ngc4088_bi_gate["gate_id"], ngc4088_bi_gate["gate_status"]))
    assert {
        gate_id for gate_id, status in bi_status.items() if status == "PASS"
    } == {
        "BI1_DIMENSIONLESS_FORM",
        "BI2_FEATURE_NORMALIZATION_DECLARED",
        "BI3_COEFFICIENT_ORIGIN_RESTRICTED",
        "BI4_COEFFICIENT_VALUES_AVAILABLE",
        "BI5_NUMERIC_BOUND_READY",
        "BI6_ENDPOINT_BLINDNESS",
    }
    assert not {gate_id for gate_id, status in bi_status.items() if status == "BLOCKED"}
    assert not ngc4088_bi_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_bi_gate["endpoint_scores_allowed"].any()

    ngc4088_bi_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_bi_coefficient_rule_summary.csv"
    ).iloc[0]
    assert (
        ngc4088_bi_summary["rule_id"]
        == "NGC4088_EPSILON_CROSS_BI_COEFFICIENT_RULE_GATE"
    )
    assert int(ngc4088_bi_summary["n_features"]) == 4
    assert int(ngc4088_bi_summary["n_available_features"]) == 4
    assert int(ngc4088_bi_summary["n_coefficients"]) == 4
    assert int(ngc4088_bi_summary["n_available_coefficients"]) == 4
    assert int(ngc4088_bi_summary["n_pass"]) == 6
    assert int(ngc4088_bi_summary["n_blocked"]) == 0
    assert (
        ngc4088_bi_summary["coefficient_rule_status"]
        == "FEATURE_NORMALIZATION_AND_B_VALUES_READY_PROTOCOL_BOUND"
    )
    assert (
        ngc4088_bi_summary["numeric_bound_status"]
        == "NUMERIC_EPSILON_PROTOCOL_BOUND_READY"
    )
    assert (
        ngc4088_bi_summary["source_response_status"]
        == "SOURCE_RESPONSES_ACCEPTED_FOR_PROTOCOL_BOUND"
    )
    assert bool(ngc4088_bi_summary["uses_vobs_or_residual"]) is False
    assert bool(ngc4088_bi_summary["endpoint_scores_allowed"]) is False

    ngc4088_bound_terms = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_bound_terms.csv"
    )
    assert len(ngc4088_bound_terms) == 4
    assert set(ngc4088_bound_terms["term_expression"]) == {
        "0.5*B_PA",
        "0.25*B_R",
        "1*B_q",
        "1*B_mem",
    }
    term_values = sorted(float(value) for value in ngc4088_bound_terms["term_numeric_value"])
    assert all(
        abs(value - expected) < 1.0e-12
        for value, expected in zip(term_values, [0.125, 0.25, 0.5, 0.5])
    )
    assert abs(float(ngc4088_bound_terms["term_numeric_value"].sum()) - 1.375) < 1.0e-12
    assert set(ngc4088_bound_terms["unit"]) == {"dimensionless"}
    assert set(ngc4088_bound_terms["term_status"]) == {
        "TERM_NUMERIC_PROTOCOL_BOUND_READY"
    }
    assert not ngc4088_bound_terms["uses_vobs_or_residual"].any()
    assert not ngc4088_bound_terms["endpoint_scores_allowed"].any()

    ngc4088_bound_expression = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_bound_expression.csv"
    ).iloc[0]
    assert (
        ngc4088_bound_expression["bound_expression"]
        == "|epsilon_cross| <= 0.5*B_PA + 0.25*B_R + 1*B_q + 1*B_mem"
    )
    assert (
        ngc4088_bound_expression["known_feature_subexpression"]
        == "0.5*B_PA + 0.25*B_R + 1*B_q + 1*B_mem"
    )
    assert ngc4088_bound_expression["blocked_feature_subexpression"] == "none"
    assert abs(float(ngc4088_bound_expression["numeric_bound_value"]) - 1.375) < 1.0e-12
    assert (
        ngc4088_bound_expression["expression_status"]
        == "NUMERIC_EPSILON_PROTOCOL_BOUND_READY_CAVEATED"
    )
    assert bool(ngc4088_bound_expression["uses_vobs_or_residual"]) is False
    assert bool(ngc4088_bound_expression["endpoint_scores_allowed"]) is False

    ngc4088_bound_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_bound_expression_summary.csv"
    ).iloc[0]
    assert int(ngc4088_bound_summary["n_terms"]) == 4
    assert int(ngc4088_bound_summary["n_terms_with_feature_values"]) == 4
    assert int(ngc4088_bound_summary["n_terms_numeric"]) == 4
    assert int(ngc4088_bound_summary["n_blocked_terms"]) == 0
    assert (
        ngc4088_bound_summary["bound_expression_status"]
        == "NUMERIC_EPSILON_PROTOCOL_BOUND_READY_CAVEATED"
    )
    assert (
        ngc4088_bound_summary["numeric_bound_status"]
        == "NUMERIC_EPSILON_PROTOCOL_BOUND_AVAILABLE"
    )
    assert (
        ngc4088_bound_summary["next_required_action"]
        == "numeric_protocol_bound_ready_interpret_with_caveats"
    )
    assert bool(ngc4088_bound_summary["uses_vobs_or_residual"]) is False
    assert bool(ngc4088_bound_summary["endpoint_scores_allowed"]) is False

    ngc4088_locality = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_locality_bound_summary.csv"
    ).iloc[0]
    assert (
        ngc4088_locality["locality_bound_status"]
        == "LOCALITY_EPSILON_BOUND_READY_SIGN_STABLE"
    )
    assert abs(float(ngc4088_locality["numeric_bound_value"]) - 0.6875) < 1.0e-12
    assert abs(float(ngc4088_locality["linear_sharp_bound_reference"]) - 1.375) < 1.0e-12
    assert int(ngc4088_locality["n_warn"]) == 0
    assert int(ngc4088_locality["n_blocked"]) == 0
    assert bool(ngc4088_locality["uses_vobs_or_residual"]) is False
    assert bool(ngc4088_locality["endpoint_scores_allowed"]) is False

    ngc4088_locality_terms = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_locality_bound_terms.csv"
    )
    assert set(ngc4088_locality_terms["term_expression"]) == {
        "0.5*f_PA*f_R",
        "0.5*f_R*f_q",
        "0.5*f_q*f_mem",
    }
    assert abs(float(ngc4088_locality_terms["term_numeric_value"].sum()) - 0.6875) < 1.0e-12
    assert not ngc4088_locality_terms["uses_vobs_or_residual"].any()
    assert not ngc4088_locality_terms["endpoint_scores_allowed"].any()

    ngc4088_sensitivity = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_readout_sensitivity_summary.csv"
    ).iloc[0]
    assert abs(float(ngc4088_sensitivity["numeric_epsilon_cross_bound"]) - 0.6875) < 1.0e-12
    assert abs(float(ngc4088_sensitivity["linear_sharp_bound_reference"]) - 1.375) < 1.0e-12
    assert ngc4088_sensitivity["active_bound_source"] == "adjacent_locality_chain_bound"
    assert (
        ngc4088_sensitivity["sensitivity_status"]
        == "CROSS_TERM_BOUND_MODERATE"
    )
    assert int(ngc4088_sensitivity["n_warn"]) == 0
    assert bool(ngc4088_sensitivity["uses_vobs_or_residual"]) is False
    assert bool(ngc4088_sensitivity["endpoint_scores_allowed"]) is False

    ngc4088_sensitivity_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_readout_sensitivity_gate.csv"
    )
    assert set(ngc4088_sensitivity_gate["gate_status"]) == {"PASS"}
    assert not ngc4088_sensitivity_gate["uses_vobs_or_residual"].any()
    assert not ngc4088_sensitivity_gate["endpoint_scores_allowed"].any()

    ngc4088_promotion_gate = pd.read_csv(
        DATA / "s4g75_ngc4088_readout_promotion_gate.csv"
    )
    assert len(ngc4088_promotion_gate) == 8
    gate_status = dict(
        zip(ngc4088_promotion_gate["gate_id"], ngc4088_promotion_gate["gate_status"])
    )
    assert {
        gate_id for gate_id, status in gate_status.items() if status == "PASS"
    } == {
        "SOURCE_ONSET_READY",
        "DIMENSIONAL_CARRIER_READY",
        "SOURCE_BASIS_SANITY",
        "RESIDUAL_BLIND_GENERATION",
        "ENDPOINT_SCORE_GUARD",
    }
    assert {
        gate_id for gate_id, status in gate_status.items() if status == "BLOCKED"
    } == {
        "INDEPENDENT_DIGITIZATION_REVIEW",
        "PHYSICAL_NORMALIZATION_LAW",
        "POPULATION_GENERALIZATION",
    }
    assert not ngc4088_promotion_gate["endpoint_authorizing"].any()

    ngc4088_promotion_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_readout_promotion_summary.csv"
    ).iloc[0]
    assert int(ngc4088_promotion_summary["n_gates"]) == 8
    assert int(ngc4088_promotion_summary["n_passed_gates"]) == 5
    assert int(ngc4088_promotion_summary["n_blocked_gates"]) == 3
    assert (
        ngc4088_promotion_summary["readout_promotion_decision"]
        == "PROMOTION_BLOCKED_PREFLIGHT_READY"
    )
    assert bool(ngc4088_promotion_summary["endpoint_scores_allowed"]) is False

    flare_summary = pd.read_csv(DATA / "s4g75_ngc2683_flare_profile_mapping_summary.csv")
    flare_row = flare_summary.iloc[0]
    assert flare_row["galaxy"] == "NGC2683"
    assert int(flare_row["n_rotation_points"]) == 11
    assert int(flare_row["n_profile_mapped_points"]) == 7
    assert int(flare_row["n_unmapped_post_saturation_points"]) == 4
    assert abs(float(flare_row["current_scalar_h_over_rs_proxy"]) - 0.202408) < 1.0e-6
    assert float(flare_row["mapped_profile_h_over_rs_max"]) > 1.8
    assert bool(flare_row["endpoint_scores_allowed"]) is False
    assert bool(flare_row["endpoint_scores_computed"]) is False

    flare_gate = pd.read_csv(DATA / "s4g75_ngc2683_flare_profile_mapping_gate.csv")
    assert set(flare_gate["mapping_status"]) == {
        "PROFILE_MAPPED",
        "MAPPING_REQUIRED_AFTER_22_KPC",
    }
    assert not flare_gate["strict_kernel_ready"].any()
    assert not flare_gate["endpoint_scores_allowed"].any()
    assert not flare_gate["endpoint_scores_computed"].any()

    profile_summary = pd.read_csv(
        DATA / "s4g75_ngc2683_profile_aware_kernel_preflight_summary.csv"
    )
    assert set(profile_summary["policy"]) == {
        "mapped_only_source_profile_policy",
        "hybrid_profile_mapped_scalar_unmapped_policy",
    }
    mapped_policy = profile_summary[
        profile_summary["policy"] == "mapped_only_source_profile_policy"
    ].iloc[0]
    assert int(mapped_policy["n_points"]) == 7
    assert int(mapped_policy["n_profile_points_exceeding_current_clip"]) == 3
    assert float(mapped_policy["profile_minus_scalar_rmse"]) > 0
    assert float(mapped_policy["unclipped_profile_minus_scalar_rmse"]) > float(
        mapped_policy["profile_minus_scalar_rmse"]
    )
    assert bool(mapped_policy["accepted_endpoint_ready"]) is False
    assert bool(mapped_policy["endpoint_scores_allowed"]) is False

    profile_points = pd.read_csv(
        DATA / "s4g75_ngc2683_profile_aware_kernel_preflight_points.csv"
    )
    assert int(profile_points["profile_h_over_rs_exceeds_current_clip"].sum()) == 3
    assert "unclipped_profile_v_K_thick_flared" in set(profile_points.columns)
    assert not profile_points["accepted_endpoint_ready"].any()
    assert not profile_points["endpoint_scores_allowed"].any()

    hr_summary = pd.read_csv(DATA / "s4g75_ngc2683_hr_profile_kernel_prototype_summary.csv")
    assert set(hr_summary["post22_policy"]) == {
        "post22_hold_plateau_upper",
        "post22_linear_taper_to_inner_height",
    }
    assert (hr_summary["hr_profile_minus_scalar_rmse"] > 0).all()
    assert not hr_summary["accepted_endpoint_ready"].any()
    assert not hr_summary["endpoint_scores_allowed"].any()

    closure_summary = pd.read_csv(
        DATA / "s4g75_ngc2683_flare_closure_source_prototype_summary.csv"
    )
    assert set(closure_summary["closure_policy"]) == {
        "flare_gradient_source",
        "flare_gradient_plus_ring_offset_source",
    }
    assert (closure_summary["closure_source_minus_scalar_rmse"] < 0).all()
    assert not closure_summary["accepted_endpoint_ready"].any()
    assert not closure_summary["endpoint_scores_allowed"].any()

    sensitivity = pd.read_csv(DATA / "s4g75_ngc2683_closure_source_sensitivity.csv")
    assert len(sensitivity) == 12
    assert (sensitivity["closure_source_minus_scalar_rmse"] < 0).all()
    assert sensitivity["closure_source_minus_scalar_rmse"].min() < -0.35
    assert not sensitivity["accepted_endpoint_ready"].any()
    assert not sensitivity["endpoint_scores_allowed"].any()

    generalization = pd.read_csv(DATA / "s4g75_closure_source_generalization_gate.csv")
    status_by_galaxy = dict(zip(generalization["galaxy"], generalization["generalization_status"]))
    assert status_by_galaxy["NGC2683"] == "PROFILE_CLOSURE_SOURCE_READY_PROTOTYPE_ONLY"
    assert status_by_galaxy["NGC3972"] == "EDGE_ON_VERTICAL_PROFILE_SEARCH_REQUIRED"
    assert status_by_galaxy["NGC4088"] == "HIGH_INCLINATION_WARP_FLARE_SEARCH_REQUIRED"
    assert "vertical_search_statuses" in set(generalization.columns)
    assert "WHISP_WARP_ASYMMETRY_SOURCE_READY_PROFILE_NOT_EXTRACTED" in generalization.loc[
        generalization["galaxy"] == "NGC4088", "vertical_search_statuses"
    ].iloc[0]
    assert set(
        generalization.loc[
            generalization["generalization_status"] == "INSUFFICIENT_VERTICAL_PROFILE_SUPPORT",
            "galaxy",
        ]
    ) == {"NGC0024", "NGC3726", "NGC3949", "NGC4389"}
    assert not generalization["closure_source_endpoint_allowed"].any()
    assert not generalization["endpoint_scores_allowed"].any()

    bridge = (ROOT / "docs" / "tau_core_gravity_bridge_central.md").read_text(
        encoding="utf-8"
    )
    assert "stable direct-source" in bridge
    assert "acquisition manifest" in bridge
    assert "not strict kernel readiness" in bridge
    assert "remaining kernel acquisition ledger" in bridge
    assert "flare-profile-to-readout-kernel mapping" in bridge
    assert "profile-aware vertical-kernel" in bridge
    assert "H(R)" in bridge
    assert "thick/flared readout kernel" in bridge
    assert "not just clipping" in bridge
    assert "old damping family is not enough" in bridge
    assert "closure source rather than as scalar" in bridge
    assert "damping" in bridge
    assert "all twelve improve" in bridge
    assert "authorized for closure-source endpoint scoring" in bridge
    assert "vertical source-search audit" in bridge
    assert "strongly distorted disk" in bridge
    assert "asymmetric warp" in bridge
    assert "warp/asymmetry profile-extraction lane" in bridge
    assert "NGC4088 warp/asymmetry extraction gate" in bridge
    assert "formula-development target" in bridge
    assert "endpoint-scoring row" in bridge
    assert "pre-kernel normalization step" in bridge
    assert "R_HI = 22.253 kpc" in bridge
    assert "R_HI/Rdisk = 8.63" in bridge
    assert "C_warp(x; x_w, p)" in bridge
    assert "source-native onset control" in bridge
    assert "onset extraction protocol" in bridge
    assert "A text-only warp statement is explicitly insufficient" in bridge
    assert "digitization target manifest" in bridge
    assert "ngc4088_page_76-076.png" in bridge
    assert "channel-map digitization worksheet" in bridge
    assert "panel-level measurement targets" in bridge
    assert "ngc4088_page_76_channel_maps_roi_worksheet_overlay.png" in bridge
    assert "frozen channel-map digitization protocol" in bridge
    assert "x_w = R_warp/R_HI = 0.282353" in bridge
    assert "FILLED_SOURCE_BASIS_NOT_ENDPOINT" in bridge
    assert "kernel-to-velocity normalization" in bridge
    assert "final 4D readout law remain" in bridge
    assert "8324.016 km^2/s^2" in bridge
    assert "THEORY_CONDITIONAL_FILLED_SOURCE_RULE" in bridge
    assert "PREDECLARED_READOUT_EXPORT_NOT_ENDPOINT" in bridge
    assert "FORMULA_CONDITIONAL_PHYSICAL_LAW_BLOCKED" in bridge
    assert "TAU_SIDE_VARIATIONAL_OR_CLOSURE_DERIVATION" in bridge
    assert "MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE" in bridge
    assert "THEORY_SELECTION_CONDITIONAL_CURRENT_ONLY" in bridge
    assert "SELECTION_RULE_CONDITIONAL_NOT_DERIVED_LAW" in bridge
    assert "CURRENT_XW_VFLAT2" in bridge
    assert "DERIVATION_SKELETON_NOT_PROOF" in bridge
    assert "DERIVATION_BLOCKED_SELECTION_RULE_AUDITED" in bridge
    assert "NOT_DERIVED_TAU_SIDE_LAW" in bridge
    assert "asymptotic carrier dominance" in bridge
    assert "ASYMPTOTIC_CARRIER_DOMINANCE_NOT_DERIVED" in bridge
    assert "VFLAT2_SOURCE_CANDIDATE_NOT_TAU_SIDE_CARRIER_PROOF" in bridge
    assert "source-catalog carrier candidate" in bridge
    assert "CLOSURE_FUNCTIONAL_REQUIREMENT_SPECIFIED_NOT_DERIVED" in bridge
    assert "NO_TAU_SIDE_EULER_CLOSURE_DERIVATION_YET" in bridge
    assert "J_tau[lambda_w]" in bridge
    assert "EULER_CONDITION_SOLVED_GIVEN_TARGET_ANSATZ" in bridge
    assert "TARGET_FUNCTIONAL_NOT_TAU_SIDE_DERIVED" in bridge
    assert "J_min(lambda_w)" in bridge
    assert "SOURCE_FACTORS_AVAILABLE_COUPLING_NOT_DERIVED" in bridge
    assert "TARGET_TERM_NOT_TAU_SIDE_DERIVED" in bridge
    assert "sigma_warp q_warp x_w Vflat^2 = 8324.016 km^2/s^2" in bridge
    assert "CONDITIONAL_PRODUCT_DERIVED_IF_SEPARABLE" in bridge
    assert "SEPARABILITY_AND_CROSS_TERM_SUPPRESSION_NOT_DERIVED" in bridge
    assert "CROSS_TERMS_DECLARED_NOT_SUPPRESSED" in bridge
    assert "LEADING_PRODUCT_ONLY_UNTIL_EPSILON_CROSS_BOUND" in bridge
    assert "epsilon_cross" in bridge
    assert "SOURCE_BOUND_PROTOCOL_PARTIAL_NUMERIC_BOUND_BLOCKED" in bridge
    assert "SYMBOLIC_UNBOUNDED_UNTIL_Q_AND_MEMORY_READY" in bridge
    assert "90 degree" in bridge
    assert "0.4 arcmin" in bridge
    assert "0.25 onset" in bridge
    assert "QWARP_PROTOCOL_READY_MEASUREMENT_BLOCKED" in bridge
    assert "q_warp_measured = clipped_mean" in bridge
    assert "MEMORY_PROTOCOL_READY_MEASUREMENT_BLOCKED" in bridge
    assert "UNBLOCKS_MEMORY_COMPONENT_AFTER_MEASUREMENT_AND_REVIEW" in bridge
    assert "weighted_source_score" in bridge
    assert "rotation-inferred family" in bridge
    assert "SCALE_UNIQUENESS" in bridge
    assert "BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES" in bridge
    assert "x_w * median_r(v_n^2) = 6038.611" in bridge
    assert "190.381 km/s" in bridge
    assert "PROMOTION_BLOCKED_PREFLIGHT_READY" in bridge
    assert "PHYSICAL_NORMALIZATION_LAW" in bridge
    assert "POPULATION_GENERALIZATION" in bridge
    assert "without residual-blind profile or bound extraction" in bridge


def test_figures_and_arxiv_source_package_are_valid():
    for name in [
        "fig01_morphology_family_registry",
        "fig02_forward_gate_score_schema",
        "fig03_forward_readout_gate_flow",
    ]:
        assert (ROOT / "figures" / f"{name}.svg").exists()
        assert (SOURCE / "figures" / f"{name}.pdf").exists()

    archive_path = ROOT / "arxiv_submission_source.zip"
    assert archive_path.exists()
    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "main.pdf" not in names
    assert "figures/fig01_morphology_family_registry.pdf" in names
    assert not any(name.endswith((".aux", ".log", ".out", ".toc", ".blg", ".bbl")) for name in names)


def test_build_arxiv_source_script_runs():
    result = subprocess.run(
        ["python", "scripts/build_arxiv_source.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "arxiv_submission_source.zip" in result.stdout


def test_ngc5907_projection_accepted_endpoint_gate_and_score():
    subprocess.run(
        ["python", "scripts/build_ngc5907_projection_accepted_endpoint_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/run_ngc5907_projection_accepted_endpoint.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    gate = pd.read_csv(DATA / "ngc5907_projection_accepted_endpoint_gate.csv")
    summary = pd.read_csv(DATA / "ngc5907_projection_accepted_endpoint_summary.csv").iloc[0]
    scores = pd.read_csv(DATA / "ngc5907_projection_accepted_endpoint_scores.csv").iloc[0]

    assert set(gate["gate_status"]) == {"PASS"}
    assert bool(summary["endpoint_scores_allowed"]) is True
    assert summary["accepted_endpoint_freeze_status"] == "ACCEPTED_ENDPOINT_FREEZE_READY"
    assert scores["accepted_endpoint_status"] == "ACCEPTED_ENDPOINT_PRELIMINARY_CONTROL_RESULT"
    assert bool(scores["endpoint_scores_allowed"]) is True
    assert abs(float(scores["rmse_projection_accepted"]) - 15.495197149438468) < 1.0e-12
    assert float(scores["rmse_projection_accepted"]) < float(scores["rmse_tpg_v6"])
    assert float(scores["rmse_projection_accepted"]) < float(scores["rmse_mond"])
    assert float(scores["rmse_projection_accepted"]) < float(
        scores["rmse_generic_promoted_thick_flared"]
    )
    report = (ROOT / "reports" / "ngc5907_projection_accepted_endpoint.md").read_text(
        encoding="utf-8"
    )
    assert "universal physical validation" in report


def test_ngc5907_accepted_endpoint_wrong_family_control_audit():
    subprocess.run(
        ["python", "scripts/run_ngc5907_accepted_endpoint_control_audit.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(DATA / "ngc5907_accepted_endpoint_control_summary.csv").iloc[0]
    candidates = pd.read_csv(DATA / "ngc5907_accepted_endpoint_control_candidates.csv")

    assert summary["accepted_endpoint_control_status"] == (
        "PASSED_SINGLE_GALAXY_WRONG_FAMILY_CONTROL"
    )
    assert bool(summary["accepted_beats_all_wrong_families"]) is True
    assert int(summary["accepted_rank_among_family_labels"]) == 1
    assert int(summary["n_family_label_candidates"]) == 5
    assert abs(float(summary["accepted_rmse"]) - 15.495197149438468) < 1.0e-12
    assert float(summary["accepted_minus_wrong_mean"]) < 0.0
    assert float(summary["accepted_minus_family_label_null_mean"]) < 0.0

    accepted_row = candidates[
        candidates["candidate_id"] == "accepted_K_projection_dominated"
    ].iloc[0]
    assert int(accepted_row["rank_all_candidates"]) == 1
    wrong = candidates[candidates["candidate_role"].str.startswith("wrong_family")]
    assert (accepted_row["rmse"] < wrong["rmse"]).all()


def test_ngc5907_projection_radial_zone_audit_preserves_inner_limit():
    subprocess.run(
        ["python", "scripts/run_ngc5907_projection_radial_zone_audit.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(DATA / "ngc5907_projection_radial_zone_summary.csv").iloc[0]
    zones = pd.read_csv(DATA / "ngc5907_projection_radial_zone_scores.csv")

    assert summary["outer_lane_status"] == (
        "ACCEPTED_PROJECTION_ENDPOINT_IS_OUTER_LANE_NOT_FULL_PROFILE"
    )
    assert int(summary["inner_n_points"]) == 4
    assert float(summary["inner_projection_kernel_mean"]) == 0.0
    assert float(summary["inner_projection_minus_tpg_rmse"]) == 0.0

    inner = zones[zones["radial_zone"] == "inner_pre_projection_window"].iloc[0]
    transition = zones[zones["radial_zone"] == "transition_projection_window"].iloc[0]
    outer = zones[zones["radial_zone"] == "outer_full_projection_window"].iloc[0]

    assert abs(float(inner["rmse_projection_accepted"]) - 32.51595420139793) < 1.0e-5
    assert float(transition["rmse_projection_accepted"]) < float(transition["rmse_tpg_v6"])
    assert float(outer["rmse_projection_accepted"]) < float(outer["rmse_tpg_v6"])
    assert "inner mismatch is outside this endpoint lane" in str(inner["zone_interpretation"])


def test_ngc4013_warp_overlay_preflight_blocks_endpoint_scoring():
    subprocess.run(
        ["python", "scripts/acquire_ngc4013_compact_overlay_sources.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_overlay_preflight_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(DATA / "ngc4013_warp_overlay_preflight_summary.csv").iloc[0]
    gates = pd.read_csv(DATA / "ngc4013_warp_overlay_preflight_gate.csv")
    fields = pd.read_csv(DATA / "ngc4013_warp_overlay_preflight_fields.csv")

    source_summary = pd.read_csv(DATA / "ngc4013_compact_overlay_source_summary.csv").iloc[0]
    assert source_summary["compact_lane_decision"] == "COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED"
    assert bool(source_summary["has_s4g_bulge_component"]) is False
    assert abs(float(source_summary["s4g_edge_disk_h_over_r"]) - 0.232931727) < 1.0e-9

    assert summary["preflight_status"] == (
        "COMPACT_REJECTED_WARP_OVERLAY_PREFLIGHT_READY_FORMULA_BLOCKED"
    )
    assert summary["current_manifest_family"] == "K_compact_finite"
    assert summary["preflight_subfamily_candidate"] == "K_warp_vertical_overlay_candidate"
    assert int(summary["best_existing_family_rank_of_current"]) == 4
    assert int(summary["n_blocked"]) == 1
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert set(gates.loc[gates["gate_status"] == "BLOCKED", "gate_id"]) == {
        "N4013_PG7_ENDPOINT_FREEZE_BLOCKED",
    }
    assert not gates["endpoint_scores_allowed"].any()
    assert "line_of_sight_warp_onset" in set(fields["observable"])
    assert "final_hi_scaleheight_central" in set(fields["observable"])


def test_ngc4013_warp_vertical_overlay_formula_shell_is_not_endpoint():
    subprocess.run(
        ["python", "scripts/acquire_ngc4013_compact_overlay_sources.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_overlay_preflight_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_vertical_overlay_formula_derivation.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_formula_summary.csv").iloc[0]
    manifest = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_formula_manifest.csv").iloc[0]
    blockers = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_formula_blockers.csv")
    steps = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_formula_derivation_steps.csv")

    assert summary["formula_id"] == "NGC4013_WARP_VERTICAL_OVERLAY_V1"
    assert summary["derivation_status"] == "FORMULA_SHELL_DERIVED_ENDPOINT_FREEZE_BLOCKED"
    assert abs(float(summary["gamma_overlay_upper"]) - 0.21646586345381524) < 1.0e-12
    assert int(summary["n_endpoint_blockers"]) == 3
    assert bool(summary["endpoint_scores_allowed"]) is False

    assert manifest["solved_response_formula"] == (
        "v_wvo^2(R)=v_TPG^2(R)*(1-Gamma_wvo*K_wvo(R))"
    )
    assert "W_warp" in manifest["kernel_formula"]
    assert manifest["sign_rule"] == "attenuation_not_added_gravity"
    assert bool(manifest["uses_vobs_or_residual_in_derivation"]) is False
    assert bool(manifest["formula_frozen_for_endpoint"]) is False
    assert bool(manifest["endpoint_scores_allowed"]) is False

    assert set(blockers["blocker_id"]) == {
        "B1_OUTER_WARP_WINDOW",
        "B2_LAG_TO_KERNEL_MAP",
        "B3_WEIGHT_RULE",
    }
    assert not blockers["endpoint_scores_allowed"].any()
    assert set(steps["status"]).issuperset(
        {"SOURCE_DERIVED_BOUND", "ENDPOINT_BLOCKED", "FORMULA_CONDITIONAL"}
    )


def test_ngc4013_warp_vertical_overlay_freezes_formula_but_blocks_endpoint_label():
    subprocess.run(
        ["python", "scripts/acquire_ngc4013_compact_overlay_sources.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_overlay_preflight_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_vertical_overlay_formula_derivation.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_vertical_overlay_endpoint_freeze_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_summary.csv").iloc[0]
    manifest = pd.read_csv(
        DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_manifest.csv"
    ).iloc[0]
    gates = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_gate.csv")
    kernel = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_kernel_grid.csv")

    assert summary["formula_freeze_status"] == "FORMULA_FREEZE_PROTOCOL_READY_LABEL_BLOCKED"
    assert abs(float(summary["r_warp_kpc"]) - 10.0) < 1.0e-12
    assert abs(float(summary["r_outer_kpc"]) - 11.2) < 1.0e-12
    assert abs(float(summary["r_lag_start_kpc"]) - 5.8) < 1.0e-12
    assert abs(float(summary["r_lag_zero_kpc"]) - 11.2) < 1.0e-12
    assert int(summary["n_blocked"]) == 1
    assert bool(summary["endpoint_scores_allowed"]) is False

    assert bool(manifest["formula_frozen_before_endpoint_scoring"]) is True
    assert bool(manifest["accepted_replacement_label_promoted"]) is False
    assert bool(manifest["uses_vobs_or_residual_in_construction"]) is False
    assert manifest["weight_rule"] == "uniform_over_three_source_supported_channels"
    assert abs(float(manifest["omega_z"]) - 1.0 / 3.0) < 1.0e-12
    assert abs(float(manifest["omega_ec"]) - 1.0 / 3.0) < 1.0e-12
    assert abs(float(manifest["omega_lag"]) - 1.0 / 3.0) < 1.0e-12

    blocked = gates.loc[gates["gate_status"] == "BLOCKED"].iloc[0]
    assert blocked["gate_id"] == "N4013_EFG6_REPLACEMENT_LABEL_PROMOTION"
    assert not gates["endpoint_scores_allowed"].any()
    assert not kernel["endpoint_scores_allowed"].any()
    assert (kernel["K_wvo"] >= 0.0).all()
    assert (kernel["K_wvo"] <= 1.0).all()
    assert float(kernel.loc[kernel["r_kpc"] == 0.0, "K_wvo"].iloc[0]) == 0.0


def test_ngc4013_warp_vertical_overlay_replacement_label_gate_allows_caveated_endpoint():
    subprocess.run(
        ["python", "scripts/acquire_ngc4013_compact_overlay_sources.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_overlay_preflight_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_vertical_overlay_formula_derivation.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_vertical_overlay_endpoint_freeze_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_vertical_overlay_replacement_label_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(
        DATA / "ngc4013_warp_vertical_overlay_replacement_label_summary.csv"
    ).iloc[0]
    gates = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_replacement_label_gate.csv")
    fields = pd.read_csv(
        DATA / "ngc4013_warp_vertical_overlay_replacement_label_source_fields.csv"
    )

    assert summary["rejected_label"] == "K_true_compact"
    assert summary["accepted_replacement_label"] == "K_warp_vertical_overlay_candidate"
    assert summary["label_promotion_status"] == (
        "CAVEATED_REPLACEMENT_LABEL_PROMOTED_ENDPOINT_SCORE_ALLOWED"
    )
    assert int(summary["n_blocked"]) == 0
    assert bool(summary["accepted_replacement_label_promoted"]) is True
    assert bool(summary["endpoint_scores_allowed"]) is True

    assert not gates["gate_status"].eq("BLOCKED").any()
    assert gates["endpoint_scores_allowed"].all()
    assert "N4013_RLG5_FORMULA_FREEZE_PROTOCOL_READY" in set(gates["gate_id"])
    assert "PASS_CAVEATED" in set(gates["gate_status"])
    assert {
        "compact_lane_decision",
        "line_of_sight_warp_onset",
        "s4g_edge_disk_h_over_r",
        "extended_component_mass_fraction",
        "rotational_lag_profile",
    }.issubset(set(fields["field_name"]))


def test_ngc4013_warp_vertical_overlay_caveated_endpoint_runs_after_gate():
    subprocess.run(
        ["python", "scripts/acquire_ngc4013_compact_overlay_sources.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_overlay_preflight_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_vertical_overlay_formula_derivation.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_vertical_overlay_endpoint_freeze_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_warp_vertical_overlay_replacement_label_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/run_ngc4013_warp_vertical_overlay_endpoint.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    scores = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_scores.csv").iloc[0]
    points = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_points.csv")

    assert scores["endpoint_status"] == "CAVEATED_ENDPOINT_PRELIMINARY_CONTROL_RESULT"
    assert bool(scores["endpoint_scores_allowed"]) is True
    assert abs(float(scores["rmse_warp_vertical_overlay"]) - 11.4504954) < 1.0e-6
    assert float(scores["rmse_warp_vertical_overlay"]) < float(scores["rmse_tpg_v6"])
    assert float(scores["rmse_warp_vertical_overlay"]) < float(scores["rmse_mond"])
    assert float(scores["rmse_warp_vertical_overlay"]) < float(
        scores["rmse_original_compact_family"]
    )
    assert int(scores["n_points"]) == 36
    assert points["endpoint_scores_allowed"].all()
    assert (points["K_wvo"] >= 0.0).all()
    assert (points["K_wvo"] <= 1.0).all()
    assert (points["wvo_attenuation"] >= 0.0).all()


def test_ngc4013_warp_vertical_overlay_controls_preserve_wrong_family_negative_result():
    subprocess.run(
        ["python", "scripts/run_ngc4013_warp_vertical_overlay_control_audit.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_control_summary.csv").iloc[0]
    candidates = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_control_candidates.csv")

    assert summary["control_status"] == (
        "NEGATIVE_RESULT_MATCHED_DOES_NOT_BEAT_ALL_WRONG_FAMILIES"
    )
    assert bool(summary["matched_beats_all_wrong_families"]) is False
    assert abs(float(summary["matched_rmse"]) - 11.4504954) < 1.0e-6
    assert float(summary["matched_minus_wrong_mean"]) < 0.0
    assert float(summary["matched_minus_wrong_best"]) > 0.0
    assert int(summary["matched_rank_among_family_labels"]) == 3
    assert candidates.loc[candidates["candidate_id"] == "wrong_K_exponential_disk", "rmse"].iloc[
        0
    ] < float(summary["matched_rmse"])


def test_ngc4013_warp_vertical_overlay_radial_zone_audit_localizes_improvement():
    subprocess.run(
        ["python", "scripts/run_ngc4013_warp_vertical_overlay_radial_zone_audit.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(
        DATA / "ngc4013_warp_vertical_overlay_radial_zone_summary.csv"
    ).iloc[0]
    zones = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_radial_zone_scores.csv")

    assert summary["outer_lane_status"] == (
        "WARP_VERTICAL_OVERLAY_ENDPOINT_IS_OUTER_LANE_NOT_FULL_PROFILE"
    )
    assert int(summary["inner_n_points"]) == 7
    assert float(summary["inner_K_wvo_mean"]) == 0.0
    assert abs(float(summary["inner_wvo_minus_tpg_rmse"])) < 1.0e-12
    assert float(summary["active_window_weighted_wvo_minus_tpg_rmse"]) < 0.0

    transition = zones.loc[zones["radial_zone"] == "transition_warp_window"].iloc[0]
    outer = zones.loc[zones["radial_zone"] == "outer_overlay_window"].iloc[0]
    assert float(transition["rmse_warp_vertical_overlay"]) < float(transition["rmse_tpg_v6"])
    assert float(outer["rmse_warp_vertical_overlay"]) < float(outer["rmse_tpg_v6"])


def test_ngc4013_expdisk_wvo_mixed_readout_remains_diagnostic_only():
    subprocess.run(
        ["python", "scripts/build_ngc4013_expdisk_warp_vertical_overlay_hypothesis_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/run_ngc4013_expdisk_warp_vertical_overlay_diagnostic.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(DATA / "ngc4013_expdisk_wvo_hypothesis_summary.csv").iloc[0]
    gates = pd.read_csv(DATA / "ngc4013_expdisk_wvo_hypothesis_gate.csv")
    scores = pd.read_csv(DATA / "ngc4013_expdisk_wvo_diagnostic_scores.csv").iloc[0]

    assert summary["hypothesis_status"] == "DIAGNOSTIC_ONLY_MIXED_READOUT_HYPOTHESIS"
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["diagnostic_scores_allowed"]) is True
    assert "BLOCKED_FOR_ENDPOINT" in set(gates["gate_status"])

    assert scores["diagnostic_status"] == "DIAGNOSTIC_ONLY_NOT_ENDPOINT"
    assert bool(scores["endpoint_scores_allowed"]) is False
    assert bool(scores["diagnostic_scores_allowed"]) is True
    assert abs(float(scores["rmse_expdisk_wvo_diagnostic"]) - 10.614758) < 1.0e-6
    assert float(scores["rmse_expdisk_wvo_diagnostic"]) < float(scores["rmse_exponential_disk"])
    assert float(scores["rmse_expdisk_wvo_diagnostic"]) < float(
        scores["rmse_warp_vertical_overlay"]
    )


def test_ngc4013_mixed_source_rule_has_source_support_but_blocks_endpoint_promotion():
    subprocess.run(
        ["python", "scripts/build_mixed_readout_source_selection_rule.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["python", "scripts/build_ngc4013_mixed_source_rule_audit.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(DATA / "ngc4013_mixed_source_rule_summary.csv").iloc[0]
    evidence = pd.read_csv(DATA / "ngc4013_mixed_source_rule_evidence.csv")
    gates = pd.read_csv(DATA / "ngc4013_mixed_source_rule_gate.csv")

    assert summary["source_support_status"] == (
        "SOURCE_SUPPORTED_MIXED_HYPOTHESIS_FORMULA_FREEZE_BLOCKED"
    )
    assert bool(summary["smooth_disk_source_supported"]) is True
    assert bool(summary["overlay_source_supported"]) is True
    assert bool(summary["compact_only_rejected"]) is True
    assert bool(summary["general_mixed_source_rule_pass"]) is True
    assert bool(summary["diagnostic_score_used_as_label_input"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["diagnostic_scores_allowed"]) is True
    assert int(summary["n_endpoint_blockers"]) == 1

    diagnostic = evidence.loc[evidence["evidence_id"] == "E8_DIAGNOSTIC_RMSE_SIGNAL"].iloc[0]
    assert bool(diagnostic["endpoint_label_input_allowed"]) is False
    msr5 = gates.loc[gates["gate_id"] == "MSR5_GENERAL_SOURCE_RULE"].iloc[0]
    assert msr5["gate_status"] == "PASS_FORMULA_FREEZE_REQUIRED"


def test_mixed_readout_source_selection_rule_is_predeclared_not_endpoint():
    subprocess.run(
        ["python", "scripts/build_mixed_readout_source_selection_rule.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    protocol = pd.read_csv(DATA / "mixed_readout_source_selection_protocol.csv")
    cases = pd.read_csv(DATA / "mixed_readout_source_selection_cases.csv")
    summary = pd.read_csv(DATA / "mixed_readout_source_selection_summary.csv").iloc[0]

    assert summary["rule_status"] == "MIXED_SOURCE_RULE_PREDECLARED_NOT_ENDPOINT"
    assert int(summary["n_cases_evaluated"]) == 1
    assert int(summary["n_source_rule_pass"]) == 1
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["diagnostic_scores_used_as_label_input"]) is False
    assert summary["next_required_gate"] == "mixed_readout_formula_freeze_gate"

    ngc4013 = cases.loc[cases["galaxy"] == "NGC4013"].iloc[0]
    assert ngc4013["case_status"] == "MIXED_SOURCE_RULE_PASS_FORMULA_FREEZE_REQUIRED"
    assert bool(ngc4013["source_rule_pass"]) is True
    assert bool(ngc4013["formula_freeze_required"]) is True
    assert bool(ngc4013["endpoint_scores_allowed"]) is False

    forbidden = " ".join(protocol["forbidden_inputs"].astype(str))
    assert "vobs residuals" in forbidden
    assert "RMSE ranks" in forbidden
    assert "mixed diagnostic RMSE as label evidence" in forbidden


def test_ngc4013_expdisk_wvo_formula_freeze_is_prospective_not_retroactive_endpoint():
    for script in [
        "scripts/build_mixed_readout_source_selection_rule.py",
        "scripts/build_ngc4013_expdisk_wvo_formula_freeze_gate.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_summary.csv").iloc[0]
    manifest = pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_manifest.csv").iloc[0]
    gates = pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_gate.csv")

    assert summary["formula_freeze_status"] == (
        "MIXED_FORMULA_FREEZE_READY_NOT_RETROACTIVE_ENDPOINT"
    )
    assert bool(summary["source_rule_pass"]) is True
    assert bool(summary["overlay_formula_frozen"]) is True
    assert bool(summary["uses_vobs_or_residual_in_construction"]) is False
    assert bool(summary["retrospective_endpoint_scores_allowed"]) is False
    assert bool(summary["prospective_endpoint_protocol_ready"]) is True

    assert manifest["formula_text"] == (
        "v_mix^2(R)=v_K_exponential_disk^2(R)*(1-Gamma_wvo*K_wvo(R))"
    )
    assert manifest["dimension_check"].startswith("PASS")
    assert manifest["inactive_window_limit"] == "K_wvo=0 implies v_mix=v_K_exponential_disk"
    assert bool(manifest["uses_vobs_or_residual_in_construction"]) is False

    retro = gates.loc[gates["gate_id"] == "MXF6_RETROACTIVE_ENDPOINT_STATUS"].iloc[0]
    assert retro["gate_status"] == "BLOCKED_RETROACTIVE_ENDPOINT"


def test_ngc4013_frozen_mixed_protocol_score_is_recorded_not_endpoint():
    for script in [
        "scripts/build_mixed_readout_source_selection_rule.py",
        "scripts/build_ngc4013_expdisk_wvo_formula_freeze_gate.py",
        "scripts/run_ngc4013_expdisk_wvo_frozen_protocol_audit.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    scores = pd.read_csv(DATA / "ngc4013_expdisk_wvo_frozen_protocol_scores.csv").iloc[0]
    points = pd.read_csv(DATA / "ngc4013_expdisk_wvo_frozen_protocol_points.csv")

    assert scores["protocol_audit_status"] == (
        "FROZEN_PROTOCOL_SCORE_RECORDED_NOT_RETROACTIVE_ENDPOINT"
    )
    assert bool(scores["retrospective_endpoint_scores_allowed"]) is False
    assert bool(scores["prospective_endpoint_protocol_ready"]) is True
    assert abs(float(scores["rmse_expdisk_wvo_frozen_protocol"]) - 10.614758) < 1.0e-6
    assert float(scores["rmse_expdisk_wvo_frozen_protocol"]) < float(
        scores["rmse_exponential_disk"]
    )
    assert float(scores["rmse_expdisk_wvo_frozen_protocol"]) < float(
        scores["rmse_warp_vertical_overlay"]
    )
    assert "v_expdisk_wvo_frozen" in points.columns
    assert bool(points["retrospective_endpoint_scores_allowed"].any()) is False


def test_ngc4013_mixed_accepted_endpoint_blocker_preserves_protocol_boundary():
    for script in [
        "scripts/build_mixed_readout_source_selection_rule.py",
        "scripts/build_ngc4013_expdisk_wvo_formula_freeze_gate.py",
        "scripts/run_ngc4013_expdisk_wvo_frozen_protocol_audit.py",
        "scripts/build_mixed_readout_population_validation_gate.py",
        "scripts/run_mixed_readout_population_endpoint.py",
        "scripts/run_mixed_readout_population_control_audit.py",
        "scripts/build_ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_gate.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(
        DATA / "ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_summary.csv"
    ).iloc[0]
    gates = pd.read_csv(DATA / "ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_gate.csv")

    assert summary["blocker_status"] == (
        "MIXED_ACCEPTED_ENDPOINT_BLOCKED_RETROACTIVE_PROTOCOL_READY"
    )
    assert bool(summary["source_rule_ready"]) is True
    assert bool(summary["formula_frozen_for_future_scoring"]) is True
    assert bool(summary["endpoint_blind_construction"]) is True
    assert bool(summary["prior_diagnostic_dependency"]) is True
    assert bool(summary["retrospective_endpoint_scores_allowed"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert abs(float(summary["frozen_protocol_rmse_km_s"]) - 10.6147582888) < 1.0e-6
    assert abs(float(summary["best_local_baseline_rmse_km_s"]) - 10.8802070820) < 1.0e-6
    assert abs(float(summary["wrong_mixed_mean_rmse_km_s"]) - 12.1321374835) < 1.0e-6
    assert abs(float(summary["wrong_mixed_best_rmse_km_s"]) - 11.3670075315) < 1.0e-6
    assert bool(summary["matched_beats_all_wrong_mixed_families"]) is True
    assert int(summary["n_blocked"]) == 2
    assert gates["endpoint_scores_allowed"].eq(False).all()
    assert "BLOCKED_RETROACTIVE_ENDPOINT" in set(gates["gate_status"])
    assert "BLOCKED_REPLAY_REQUIRED" in set(gates["gate_status"])


def test_ngc4013_retrospective_caveat_closure_gate_formalizes_path_without_endpoint_rewrite():
    for script in [
        "scripts/build_mixed_readout_source_selection_rule.py",
        "scripts/build_ngc4013_expdisk_wvo_formula_freeze_gate.py",
        "scripts/run_ngc4013_expdisk_wvo_frozen_protocol_audit.py",
        "scripts/build_mixed_readout_population_validation_gate.py",
        "scripts/build_mixed_readout_candidate_acquisition_queue.py",
        "scripts/run_mixed_readout_population_endpoint.py",
        "scripts/run_mixed_readout_population_control_audit.py",
        "scripts/build_ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_gate.py",
        "scripts/build_mixed_readout_population_expansion_gate.py",
        "scripts/build_ngc4013_retrospective_caveat_closure_gate.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "ngc4013_retrospective_caveat_closure_summary.csv").iloc[0]
    gates = pd.read_csv(DATA / "ngc4013_retrospective_caveat_closure_gates.csv")
    analogues = pd.read_csv(DATA / "ngc4013_retrospective_caveat_analogue_candidates.csv")
    report = (ROOT / "reports/ngc4013_retrospective_caveat_closure_gate.md").read_text(
        encoding="utf-8"
    )

    assert summary["closure_gate_status"] == (
        "NGC4013_RETROSPECTIVE_CAVEAT_CLOSURE_PATH_FORMALIZED_NOT_CLOSED"
    )
    assert bool(summary["source_rule_transferable"]) is True
    assert bool(summary["formula_freeze_transferable"]) is True
    assert bool(summary["control_signal_recorded"]) is True
    assert bool(summary["retrospective_endpoint_score_forbidden"]) is True
    assert int(summary["exact_non_ngc4013_analogue_ready_count"]) == 0
    assert summary["nearest_analogue_candidate"] == "NGC4088"
    assert bool(summary["nearest_analogue_freeze_allowed_now"]) is False
    assert bool(summary["endpoint_status_changed"]) is False
    assert bool(summary["endpoint_scores_recomputed"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False

    assert "BLOCKED_RETROACTIVE_ENDPOINT" in set(gates["gate_status"])
    assert "BLOCKED_FUTURE_ANALOGUE_REQUIRED" in set(gates["gate_status"])
    assert gates["endpoint_scores_allowed"].eq(False).all()
    assert gates["uses_vobs_or_residual"].eq(False).all()
    assert "NGC4088" in set(analogues["galaxy"])
    assert analogues["endpoint_scores_allowed"].eq(False).all()
    assert "not closed" in report
    assert "does not change the endpoint status" in report


def test_remaining_caveat_closure_roadmap_updates_after_ngc7331_replay_without_scoring():
    for script in [
        "scripts/build_four_case_endpoint_status_summary.py",
        "scripts/build_four_case_caveat_reduction_audit.py",
        "scripts/build_ngc4013_retrospective_caveat_closure_gate.py",
        "scripts/run_ngc7331_v2_v3_replay_holdout_endpoint.py",
        "scripts/build_ngc4013_predeclared_replay_holdout_gate.py",
        "scripts/build_ngc4088_remaining_caveat_action_gate.py",
        "scripts/build_remaining_caveat_closure_roadmap.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "remaining_caveat_closure_roadmap_summary.csv").iloc[0]
    roadmap = pd.read_csv(DATA / "remaining_caveat_closure_roadmap.csv")
    audit = pd.read_csv(DATA / "remaining_caveat_closure_roadmap_audit.csv")
    report = (ROOT / "reports/remaining_caveat_closure_roadmap.md").read_text(
        encoding="utf-8"
    )

    assert summary["roadmap_status"] == (
        "REMAINING_CAVEAT_CLOSURE_ROADMAP_UPDATED_AFTER_NGC4088_ACTION_GATE_NOT_ENDPOINT"
    )
    assert int(summary["n_cases"]) == 4
    assert int(summary["n_replay_ready_without_new_source"]) == 0
    assert int(summary["n_replay_completed_without_v1_update"]) == 1
    assert int(summary["n_predeclared_replay_gates_built_without_endpoint"]) == 1
    assert int(summary["n_remaining_caveat_action_gates_built_without_endpoint"]) == 1
    assert int(summary["n_retrospective_or_population_blocked"]) == 3
    assert int(summary["n_source_or_law_blocked"]) == 0
    assert bool(summary["endpoint_statuses_changed"]) is False
    assert bool(summary["endpoint_scores_recomputed"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert bool(summary["uses_replay_endpoint_summary"]) is True
    assert bool(summary["uses_predeclared_replay_gate_summary"]) is True
    assert bool(summary["uses_remaining_caveat_action_summary"]) is True
    assert bool(summary["v1_endpoint_updated"]) is False
    assert summary["next_recommended_gate"] == (
        "B2_SOURCE_LOAD_ORIGIN_AND_ASYMPTOTIC_CARRIER_DERIVATION_FOR_NGC4088"
    )

    assert set(roadmap["galaxy"]) == {"NGC4013", "NGC5907", "NGC7331", "NGC4088"}
    ngc4088 = roadmap.loc[roadmap["galaxy"].eq("NGC4088")].iloc[0]
    assert ngc4088["remaining_caveat_class"] == (
        "B2_B3_LAW_LEVEL_OPEN_B1_PROVENANCE_UPGRADE_OPTIONAL"
    )
    assert ngc4088["next_gate"] == "B2_SOURCE_LOAD_ORIGIN_AND_ASYMPTOTIC_CARRIER_DERIVATION"
    assert bool(ngc4088["endpoint_scores_allowed_now"]) is False
    ngc7331 = roadmap.loc[roadmap["galaxy"].eq("NGC7331")].iloc[0]
    assert ngc7331["remaining_caveat_class"] == "BROAD_WINDOW_REPLAY_REDUCED_V1_NOT_UPDATED"
    assert ngc7331["priority"] == "P2_POPULATION_SCALE"
    assert ngc7331["next_gate"] == "POPULATION_REPLAY_OR_SOURCE_ANALOGUE_CONFIRMATION"
    assert bool(ngc7331["can_close_without_new_endpoint_data"]) is False
    assert bool(ngc7331["endpoint_scores_allowed_now"]) is False
    ngc4013 = roadmap.loc[roadmap["galaxy"].eq("NGC4013")].iloc[0]
    assert ngc4013["remaining_caveat_class"] == (
        "PREDECLARED_REPLAY_GATE_BUILT_FUTURE_DATA_REQUIRED"
    )
    assert ngc4013["next_gate"] == "FUTURE_UNINSPECTED_HOLDOUT_OR_SOURCE_SELECTED_ANALOGUE"
    assert bool(ngc4013["can_close_without_new_endpoint_data"]) is False
    assert audit["endpoint_status_changed"].eq(False).all()
    assert audit["endpoint_scores_recomputed"].eq(False).all()
    assert audit["uses_vobs_or_residual_in_reduction"].eq(False).all()
    assert "not an endpoint score" in report
    assert "NGC7331 replay path" in report
    assert "NGC4088 remaining-caveat action gate" in report
    assert "The next scientific action is therefore B2 law-level work" in report


def test_ngc4013_predeclared_replay_holdout_gate_blocks_same_curve_replay():
    for script in [
        "scripts/build_four_case_endpoint_status_summary.py",
        "scripts/build_four_case_caveat_reduction_audit.py",
        "scripts/build_ngc4013_retrospective_caveat_closure_gate.py",
        "scripts/build_ngc4013_predeclared_replay_holdout_gate.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "ngc4013_predeclared_replay_holdout_summary.csv").iloc[0]
    gates = pd.read_csv(DATA / "ngc4013_predeclared_replay_holdout_gates.csv")
    routes = pd.read_csv(DATA / "ngc4013_predeclared_replay_holdout_routes.csv")
    report = (ROOT / "reports/ngc4013_predeclared_replay_holdout_gate.md").read_text(
        encoding="utf-8"
    )

    assert summary["predeclared_replay_gate_status"] == (
        "NGC4013_PREDECLARED_REPLAY_HOLDOUT_GATE_BUILT_ENDPOINT_STILL_BLOCKED"
    )
    assert bool(summary["source_rule_transferable"]) is True
    assert bool(summary["formula_manifest_transferable"]) is True
    assert bool(summary["prospective_endpoint_protocol_ready"]) is True
    assert bool(summary["existing_score_quarantined"]) is True
    assert bool(summary["same_curve_replay_allowed"]) is False
    assert bool(summary["future_holdout_route_defined"]) is True
    assert bool(summary["future_analogue_route_defined"]) is True
    assert int(summary["exact_non_ngc4013_analogue_ready_count"]) == 0
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["endpoint_scores_recomputed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert summary["next_required_gate"] == (
        "FUTURE_UNINSPECTED_HOLDOUT_OR_SOURCE_SELECTED_ANALOGUE"
    )

    assert gates["endpoint_scores_allowed"].eq(False).all()
    assert gates["uses_vobs_or_residual"].eq(False).all()
    assert "PASS_SCORE_QUARANTINED" in set(gates["gate_status"])
    assert "BLOCKED_ENDPOINT_SCORE_NOT_ALLOWED_NOW" in set(gates["gate_status"])
    same_curve = routes.loc[routes["route_id"].eq("R1_SAME_CURVE_REPLAY")].iloc[0]
    assert same_curve["route_status"] == "BLOCKED_RETROSPECTIVE_CURVE_ALREADY_INSPECTED"
    assert bool(same_curve["allowed_future_use"]) is False
    assert routes["endpoint_scores_allowed_now"].eq(False).all()
    assert "does not score a rotation curve" in report
    assert "same-curve replay is explicitly" in report


def test_ngc4088_remaining_caveat_action_gate_prioritizes_b2_law_derivation():
    for script in [
        "scripts/build_ngc4088_b1_whisp_promotion_review.py",
        "scripts/build_ngc4088_b2_physical_normalization_derivation_synthesis.py",
        "scripts/build_ngc4088_b2_source_load_closure_functional_gate.py",
        "scripts/build_ngc4088_b2_frozen_asymptotic_carrier_theorem_gate.py",
        "scripts/build_ngc4088_b2_source_load_origin_derivation_gate.py",
        "scripts/build_ngc4088_b2_closure_asymptotic_conditional_derivation_gate.py",
        "scripts/build_ngc4088_b3_scale_uniqueness_resolution_synthesis.py",
        "scripts/build_ngc4088_warp_history_formula_freeze_gate.py",
        "scripts/build_ngc4088_formula_freeze_readiness_dashboard.py",
        "scripts/build_ngc4088_warp_history_accepted_endpoint_gate.py",
        "scripts/run_ngc4088_warp_history_accepted_endpoint.py",
        "scripts/build_ngc4088_remaining_caveat_action_gate.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "ngc4088_remaining_caveat_action_summary.csv").iloc[0]
    actions = pd.read_csv(DATA / "ngc4088_remaining_caveat_actions.csv")
    report = (ROOT / "reports/ngc4088_remaining_caveat_action_gate.md").read_text(
        encoding="utf-8"
    )

    assert summary["action_gate_status"] == (
        "NGC4088_REMAINING_CAVEAT_ACTION_GATE_BUILT_NOT_ENDPOINT"
    )
    assert bool(summary["endpoint_ready"]) is True
    assert bool(summary["endpoint_scored"]) is True
    assert bool(summary["b1_formula_freeze_closed_caveated"]) is True
    assert bool(summary["b1_direct_hi_product_cached"]) is False
    assert bool(summary["b2_protocol_ready_law_level_open"]) is True
    assert summary["b2_conditional_derivation_status"] == (
        "B2_CONDITIONAL_THEOREM_ALIGNED_TO_FREEZE_MANIFEST_LAW_PREMISES_OPEN"
    )
    assert bool(summary["b2_formula_freeze_alignment_pass"]) is True
    assert bool(summary["b2_conditional_law_level_closed"]) is False
    assert bool(summary["b3_protocol_unique_law_level_open"]) is True
    assert bool(summary["endpoint_scores_allowed_by_this_gate"]) is False
    assert bool(summary["endpoint_status_changed"]) is False
    assert bool(summary["endpoint_scores_recomputed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert summary["next_recommended_caveat_action"] == (
        "B2_SOURCE_LOAD_ORIGIN_AND_ASYMPTOTIC_CARRIER_DERIVATION"
    )
    b2 = actions.loc[actions["action_id"].eq("A2_B2_CLOSURE_FUNCTIONAL_DERIVATION")].iloc[0]
    assert bool(b2["law_level_blocking_now"]) is True
    assert b2["current_status"] == (
        "B2_CONDITIONAL_THEOREM_ALIGNED_TO_FREEZE_MANIFEST_LAW_PREMISES_OPEN"
    )
    assert "source-load origin" in b2["next_action"]
    assert "Vflat^2" in b2["next_action"]
    b1 = actions.loc[actions["action_id"].eq("A1_DIRECT_HI_PROVENANCE_UPGRADE")].iloc[0]
    assert bool(b1["formula_freeze_blocking_now"]) is False
    assert "provenance upgrade" in b1["next_action"]
    assert actions["endpoint_scores_allowed"].eq(False).all()
    assert actions["uses_vobs_or_residual"].eq(False).all()
    assert "not another endpoint score" in report
    assert "primary theory action is B2" in report


def test_ngc7331_v2_v3_replay_holdout_endpoint_reduces_replay_caveat_without_v1_update():
    for script in [
        "scripts/build_ngc7331_fractional_warp_onset_source_gate.py",
        "scripts/build_ngc7331_fractional_onset_v2_replay_freeze_gate.py",
        "scripts/build_mixed_kernel_observable_separation_gate.py",
        "scripts/build_mixed_kernel_sharpening_preflight.py",
        "scripts/build_mixed_kernel_sharpened_replay_freeze.py",
        "scripts/run_ngc7331_v2_v3_replay_holdout_endpoint.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "ngc7331_v2_v3_replay_holdout_endpoint_summary.csv").iloc[0]
    scores = pd.read_csv(DATA / "ngc7331_v2_v3_replay_holdout_endpoint_scores.csv")
    gates = pd.read_csv(DATA / "ngc7331_v2_v3_replay_holdout_endpoint_gates.csv")
    points = pd.read_csv(DATA / "ngc7331_v2_v3_replay_holdout_endpoint_points.csv")
    report = (ROOT / "reports/ngc7331_v2_v3_replay_holdout_endpoint.md").read_text(
        encoding="utf-8"
    )

    assert summary["endpoint_status"] == (
        "NGC7331_V2_V3_REPLAY_HOLDOUT_PRELIMINARY_CONTROL_RESULT"
    )
    assert int(summary["n_points"]) == 36
    assert abs(float(summary["v1_reference_rmse_km_s"]) - 22.255666) < 1.0e-6
    assert abs(float(summary["v2_fractional_onset_rmse_km_s"]) - 22.732383) < 1.0e-6
    assert abs(float(summary["v3_source_sharpened_rmse_km_s"]) - 22.130849) < 1.0e-6
    assert abs(float(summary["best_baseline_rmse_km_s"]) - 23.472977) < 1.0e-6
    assert abs(float(summary["wrong_projection_sharpened_rmse_km_s"]) - 22.906398) < 1.0e-6
    assert bool(summary["v3_beats_v1_reference"]) is True
    assert bool(summary["v3_beats_v2_fractional_onset"]) is True
    assert bool(summary["v3_beats_best_baseline"]) is True
    assert bool(summary["v3_beats_wrong_projection_control"]) is True
    assert bool(summary["current_v1_endpoint_updated"]) is False
    assert bool(summary["construction_used_vobs"]) is False
    assert bool(summary["scoring_used_vobs"]) is True

    assert scores.iloc[0]["model_id"] == "TAU_NGC7331_V3_SOURCE_SHARPENED_REPLAY"
    assert gates["current_v1_endpoint_updated"].eq(False).all()
    assert gates["uses_vobs_or_residual_in_construction"].eq(False).all()
    assert points["current_v1_endpoint_updated"].eq(False).all()
    assert "does not update the accepted" in report
    assert "not a retroactive update" in report


def test_mixed_population_validation_gate_is_ready_before_endpoint_scoring():
    for script in [
        "scripts/build_mixed_readout_source_selection_rule.py",
        "scripts/build_ngc4013_expdisk_wvo_formula_freeze_gate.py",
        "scripts/run_ngc4013_expdisk_wvo_frozen_protocol_audit.py",
        "scripts/build_ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_gate.py",
        "scripts/build_mixed_readout_candidate_acquisition_queue.py",
        "scripts/build_ngc5907_expdisk_projection_mixed_formula_freeze_gate.py",
        "scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py",
        "scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.py",
        "scripts/build_mixed_readout_population_validation_gate.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "mixed_readout_population_validation_summary.csv").iloc[0]
    cases = pd.read_csv(DATA / "mixed_readout_population_validation_cases.csv")
    endpoints = pd.read_csv(DATA / "mixed_readout_population_validation_endpoints.csv")
    protocol = pd.read_csv(DATA / "mixed_readout_population_validation_protocol.csv")

    assert summary["validation_gate_status"] == "MIXED_POPULATION_VALIDATION_READY"
    assert int(summary["n_source_rule_positive_mixed_cases"]) == 3
    assert int(summary["n_prospective_protocol_ready_cases"]) == 3
    assert int(summary["min_independent_prospective_cases_required"]) == 3
    assert bool(summary["endpoint_scores_run"]) is False

    ngc4013 = cases.loc[cases["galaxy"] == "NGC4013"].iloc[0]
    assert bool(ngc4013["source_rule_pass"]) is True
    assert bool(ngc4013["prospective_protocol_ready"]) is True
    assert bool(ngc4013["retrospective_endpoint_allowed"]) is False
    ngc5907 = cases.loc[cases["galaxy"] == "NGC5907"].iloc[0]
    assert bool(ngc5907["source_rule_pass"]) is True
    assert bool(ngc5907["prospective_protocol_ready"]) is True
    assert bool(ngc5907["retrospective_endpoint_allowed"]) is False
    ngc7331 = cases.loc[cases["galaxy"] == "NGC7331"].iloc[0]
    assert bool(ngc7331["source_rule_pass"]) is True
    assert bool(ngc7331["prospective_protocol_ready"]) is True
    assert bool(ngc7331["retrospective_endpoint_allowed"]) is False
    assert ngc7331["population_validation_use"] == (
        "caveated_prospective_protocol_case_only_not_validation"
    )

    assert set(endpoints["status"]) == {"NOT_RUN_POPULATION_ENDPOINT"}
    assert "MPG6_NEGATIVE_CONTROL" in set(protocol["gate_id"])


def test_mixed_readout_population_endpoint_scores_frozen_manifests_only():
    for script in [
        "scripts/build_mixed_readout_source_selection_rule.py",
        "scripts/build_ngc4013_expdisk_wvo_formula_freeze_gate.py",
        "scripts/build_mixed_readout_candidate_acquisition_queue.py",
        "scripts/build_ngc5907_expdisk_projection_mixed_formula_freeze_gate.py",
        "scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py",
        "scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.py",
        "scripts/build_mixed_readout_population_validation_gate.py",
        "scripts/run_mixed_readout_population_endpoint.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "mixed_readout_population_endpoint_summary.csv").iloc[0]
    scores = pd.read_csv(DATA / "mixed_readout_population_endpoint_scores.csv")
    points = pd.read_csv(DATA / "mixed_readout_population_endpoint_points.csv")

    assert summary["endpoint_status"] == "MIXED_POPULATION_ENDPOINT_PRELIMINARY_CONTROL_RESULT"
    assert int(summary["n_cases_scored"]) == 3
    assert int(summary["n_fresh_prospective_cases"]) == 2
    assert int(summary["n_caveated_cases"]) == 1
    assert bool(summary["construction_used_vobs"]) is False
    assert bool(summary["scoring_used_vobs"]) is True
    assert "not population validation" in summary["claim_status"]

    assert set(scores["galaxy"]) == {"NGC4013", "NGC5907", "NGC7331"}
    assert scores["construction_used_vobs"].eq(False).all()
    assert scores["scoring_used_vobs"].eq(True).all()
    assert scores["beats_newton"].eq(True).all()
    assert scores["beats_tpg_v6"].eq(True).all()
    assert scores["beats_mond"].eq(True).all()
    assert scores["beats_exponential_disk_carrier"].eq(True).all()

    ngc4013 = scores.loc[scores["galaxy"].eq("NGC4013")].iloc[0]
    ngc5907 = scores.loc[scores["galaxy"].eq("NGC5907")].iloc[0]
    ngc7331 = scores.loc[scores["galaxy"].eq("NGC7331")].iloc[0]
    assert ngc4013["mixed_case_status"] == "RETROSPECTIVE_REFERENCE_FROZEN_PROTOCOL_SCORED"
    assert ngc5907["mixed_case_status"] == "FRESH_PROSPECTIVE_MIXED_PROTOCOL_SCORED"
    assert ngc7331["mixed_case_status"] == (
        "CAVEATED_FRESH_PROSPECTIVE_MIXED_PROTOCOL_SCORED"
    )
    assert ngc7331["mixed_case_caveat"] == "broad_outer_window_no_numeric_warp_onset"
    assert abs(float(summary["mean_rmse_mixed_population"]) - 16.414319) < 1.0e-6
    assert points["claim_boundary"].eq("mixed_readout_population_endpoint_preliminary_control").all()


def test_mixed_readout_population_wrong_label_control_passes_small_n_audit():
    for script in [
        "scripts/build_mixed_readout_source_selection_rule.py",
        "scripts/build_ngc4013_expdisk_wvo_formula_freeze_gate.py",
        "scripts/build_mixed_readout_candidate_acquisition_queue.py",
        "scripts/build_ngc5907_expdisk_projection_mixed_formula_freeze_gate.py",
        "scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py",
        "scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.py",
        "scripts/build_mixed_readout_population_validation_gate.py",
        "scripts/run_mixed_readout_population_endpoint.py",
        "scripts/run_mixed_readout_population_control_audit.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "mixed_readout_population_control_summary.csv").iloc[0]
    by_galaxy = pd.read_csv(DATA / "mixed_readout_population_control_by_galaxy.csv")
    permutations = pd.read_csv(DATA / "mixed_readout_population_shuffled_label_permutations.csv")
    matrix = pd.read_csv(DATA / "mixed_readout_population_control_matrix.csv")

    assert summary["control_status"] == "PASSED_3CASE_WRONG_LABEL_AND_SHUFFLED_CONTROL"
    assert int(summary["n_galaxies"]) == 3
    assert int(summary["n_formula_labels"]) == 3
    assert int(summary["n_matched_beats_all_wrong_labels"]) == 3
    assert int(summary["matched_permutation_rank"]) == 1
    assert bool(summary["construction_used_vobs"]) is False
    assert bool(summary["scoring_used_vobs"]) is True
    assert abs(float(summary["mean_matched_rmse"]) - 16.414319) < 1.0e-6
    assert abs(float(summary["mean_wrong_label_rmse"]) - 17.286791) < 1.0e-6
    assert abs(float(summary["best_shuffled_mean_rmse"]) - 16.710332) < 1.0e-6
    assert "small-N" in summary["claim_status"]

    assert by_galaxy["matched_beats_all_wrong_labels"].eq(True).all()
    assert by_galaxy["matched_rank_within_galaxy"].eq(1).all()
    assert len(matrix) == 9
    assert set(matrix["label_assignment_role"]) == {"matched", "wrong_label_control"}
    matched = permutations.loc[permutations["assignment_role"].eq("matched_diagonal")].iloc[0]
    assert int(matched["rank_by_mean_rmse"]) == 1
    assert len(permutations.loc[permutations["assignment_role"].eq("shuffled_label_null")]) == 5


def test_mixed_readout_replay_holdout_endpoint_preserves_negative_specificity_result():
    for script in [
        "scripts/build_mixed_readout_source_selection_rule.py",
        "scripts/build_mixed_readout_candidate_acquisition_queue.py",
        "scripts/build_ngc5907_expdisk_projection_mixed_formula_freeze_gate.py",
        "scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py",
        "scripts/build_ngc7331_fractional_warp_onset_source_gate.py",
        "scripts/build_ngc7331_fractional_onset_v2_replay_freeze_gate.py",
        "scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.py",
        "scripts/build_mixed_readout_population_validation_gate.py",
        "scripts/run_mixed_readout_replay_holdout_endpoint.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "mixed_readout_replay_holdout_endpoint_summary.csv").iloc[0]
    scores = pd.read_csv(DATA / "mixed_readout_replay_holdout_endpoint_scores.csv")
    by_galaxy = pd.read_csv(DATA / "mixed_readout_replay_holdout_control_by_galaxy.csv")
    permutations = pd.read_csv(DATA / "mixed_readout_replay_holdout_shuffled_permutations.csv")
    points = pd.read_csv(DATA / "mixed_readout_replay_holdout_endpoint_points.csv")

    assert summary["endpoint_status"] == "MIXED_REPLAY_HOLDOUT_2CASE_PRELIMINARY_RESULT"
    assert int(summary["n_cases_scored"]) == 2
    assert summary["ngc4013_excluded_reason"] == (
        "retrospective_reference_protocol_not_fresh_replay_holdout"
    )
    assert int(summary["n_beats_newton"]) == 2
    assert int(summary["n_beats_tpg_v6"]) == 2
    assert int(summary["n_beats_mond"]) == 2
    assert int(summary["n_beats_exponential_disk_carrier"]) == 2
    assert int(summary["n_matched_beats_all_wrong_labels"]) == 0
    assert int(summary["matched_permutation_rank"]) == 2
    assert bool(summary["construction_used_vobs"]) is False
    assert bool(summary["scoring_used_vobs"]) is True
    assert "small-N" in summary["claim_status"]

    assert set(scores["galaxy"]) == {"NGC5907", "NGC7331"}
    assert scores["beats_newton"].eq(True).all()
    assert scores["beats_tpg_v6"].eq(True).all()
    assert scores["beats_mond"].eq(True).all()
    assert scores["beats_exponential_disk_carrier"].eq(True).all()
    ngc7331 = scores.loc[scores["galaxy"].eq("NGC7331")].iloc[0]
    assert ngc7331["case_status"] == "V2_REPLAY_FRACTIONAL_ONSET_HOLDOUT_SCORED"
    assert ngc7331["applied_formula_id"] == "NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1"
    assert abs(float(ngc7331["rmse_mixed_replay_holdout"]) - 22.732383) < 1.0e-6

    assert by_galaxy["matched_beats_all_wrong_labels"].eq(False).all()
    assert by_galaxy["matched_rank_within_galaxy"].eq(2).all()
    matched = permutations.loc[permutations["assignment_role"].eq("matched_diagonal")].iloc[0]
    assert int(matched["rank_by_mean_rmse"]) == 2
    assert points["claim_boundary"].eq(
        "mixed_readout_replay_holdout_endpoint_small_n_not_validation"
    ).all()


def test_mixed_kernel_observable_separation_gate_is_source_side_only():
    for script in [
        "scripts/build_ngc5907_expdisk_projection_mixed_formula_freeze_gate.py",
        "scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py",
        "scripts/build_ngc7331_fractional_warp_onset_source_gate.py",
        "scripts/build_ngc7331_fractional_onset_v2_replay_freeze_gate.py",
        "scripts/build_mixed_kernel_observable_separation_gate.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "mixed_kernel_observable_separation_summary.csv").iloc[0]
    fingerprints = pd.read_csv(DATA / "mixed_kernel_observable_separation_fingerprints.csv")
    matrix = pd.read_csv(DATA / "mixed_kernel_observable_separation_matrix.csv")
    report = (ROOT / "reports" / "mixed_kernel_observable_separation_gate.md").read_text(
        encoding="utf-8"
    )

    assert summary["gate_status"] == "SOURCE_KERNEL_OBSERVABLE_SEPARATION_PASS"
    assert summary["diagnostic_status"] == "DIAGNOSTIC_ONLY_NOT_ENDPOINT"
    assert int(summary["cases_audited"]) == 2
    assert int(summary["matched_source_rank_first"]) == 2
    assert float(summary["min_source_similarity_margin"]) > 0.5
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["endpoint_score_inputs_read"]) is False
    assert summary["bridge_interpretation"] == (
        "source_fields_separate_lanes_kernel_mapping_needs_sharpening"
    )

    assert set(fingerprints["galaxy"]) == {"NGC5907", "NGC7331"}
    assert fingerprints["uses_vobs_or_residual"].eq(False).all()
    assert fingerprints["endpoint_scores_allowed"].eq(False).all()
    assert set(matrix["prototype_formula"]) == {
        "K_expdisk_projection_mixed",
        "K_expdisk_vertical_outer_warp_v2",
    }
    assert matrix.loc[matrix["is_matched_formula"], "rank_within_galaxy"].eq(1).all()
    assert "SOURCE_KERNEL_OBSERVABLE_SEPARATION_PASS" in report
    assert "current source-to-kernel map" in report
    assert "not an endpoint score" in report


def test_mixed_kernel_sharpening_preflight_reduces_kernel_shape_similarity():
    for script in [
        "scripts/build_ngc5907_expdisk_projection_mixed_formula_freeze_gate.py",
        "scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py",
        "scripts/build_ngc7331_fractional_warp_onset_source_gate.py",
        "scripts/build_ngc7331_fractional_onset_v2_replay_freeze_gate.py",
        "scripts/build_mixed_kernel_observable_separation_gate.py",
        "scripts/build_mixed_kernel_sharpening_preflight.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "mixed_kernel_sharpening_preflight_summary.csv").iloc[0]
    formulas = pd.read_csv(DATA / "mixed_kernel_sharpening_preflight_formulas.csv")
    profiles = pd.read_csv(DATA / "mixed_kernel_sharpening_preflight_profiles.csv")
    report = (ROOT / "reports" / "mixed_kernel_sharpening_preflight.md").read_text(
        encoding="utf-8"
    )

    assert summary["preflight_status"] == (
        "SOURCE_KERNEL_SHARPENING_PREFLIGHT_READY_NOT_ENDPOINT"
    )
    assert summary["diagnostic_status"] == "DIAGNOSTIC_ONLY_NOT_ENDPOINT"
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["endpoint_score_inputs_read"]) is False
    assert float(summary["current_kernel_cross_similarity"]) > 0.98
    assert float(summary["source_sharpened_kernel_cross_similarity"]) < 0.70
    assert float(summary["kernel_shape_separation_gain"]) > 0.30
    assert float(summary["projection_edge_exponent"]) > 2.0
    assert float(summary["vertical_decay"]) > 2.0

    assert set(formulas["formula_label"]) == {
        "K_projection_source_sharpened",
        "K_vertical_outer_warp_source_sharpened",
    }
    assert formulas["dimension_check"].str.startswith("PASS").all()
    assert formulas["endpoint_scores_allowed"].eq(False).all()
    assert profiles["uses_vobs_or_residual"].eq(False).all()
    assert profiles["endpoint_scores_allowed"].eq(False).all()
    assert "SOURCE_KERNEL_SHARPENING_PREFLIGHT_READY_NOT_ENDPOINT" in report
    assert "not a fit improvement claim" in report
    assert "No observed velocity, residual, RMSE, or endpoint rank" in report


def test_mixed_kernel_sharpened_replay_holdout_repairs_two_case_specificity():
    for script in [
        "scripts/build_ngc5907_expdisk_projection_mixed_formula_freeze_gate.py",
        "scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py",
        "scripts/build_ngc7331_fractional_warp_onset_source_gate.py",
        "scripts/build_ngc7331_fractional_onset_v2_replay_freeze_gate.py",
        "scripts/build_mixed_kernel_observable_separation_gate.py",
        "scripts/build_mixed_kernel_sharpening_preflight.py",
        "scripts/build_mixed_kernel_sharpened_replay_freeze.py",
        "scripts/run_mixed_kernel_sharpened_replay_holdout_endpoint.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    freeze = pd.read_csv(DATA / "mixed_kernel_sharpened_replay_freeze_summary.csv").iloc[0]
    manifest = pd.read_csv(DATA / "mixed_kernel_sharpened_replay_freeze_manifest.csv")
    summary = pd.read_csv(
        DATA / "mixed_kernel_sharpened_replay_holdout_endpoint_summary.csv"
    ).iloc[0]
    scores = pd.read_csv(DATA / "mixed_kernel_sharpened_replay_holdout_endpoint_scores.csv")
    by_galaxy = pd.read_csv(
        DATA / "mixed_kernel_sharpened_replay_holdout_control_by_galaxy.csv"
    )
    permutations = pd.read_csv(
        DATA / "mixed_kernel_sharpened_replay_holdout_shuffled_permutations.csv"
    )
    points = pd.read_csv(DATA / "mixed_kernel_sharpened_replay_holdout_endpoint_points.csv")

    assert freeze["freeze_status"] == "SHARPENED_REPLAY_FREEZE_READY_NOT_SCORED"
    assert int(freeze["n_formulas_frozen"]) == 2
    assert bool(freeze["uses_vobs_or_residual_in_construction"]) is False
    assert bool(freeze["endpoint_scores_allowed_by_this_gate"]) is False
    assert manifest["formula_frozen_before_sharpened_replay_scoring"].eq(True).all()
    assert manifest["uses_vobs_or_residual_in_construction"].eq(False).all()
    assert manifest["endpoint_scores_allowed_by_this_gate"].eq(False).all()

    assert summary["endpoint_status"] == (
        "SHARPENED_REPLAY_HOLDOUT_2CASE_PRELIMINARY_CONTROL_RESULT"
    )
    assert int(summary["n_cases_scored"]) == 2
    assert bool(summary["construction_used_vobs"]) is False
    assert bool(summary["scoring_used_vobs"]) is True
    assert int(summary["n_beats_newton"]) == 2
    assert int(summary["n_beats_tpg_v6"]) == 2
    assert int(summary["n_beats_mond"]) == 2
    assert int(summary["n_beats_exponential_disk_carrier"]) == 2
    assert int(summary["n_matched_beats_all_wrong_labels"]) == 2
    assert int(summary["matched_permutation_rank"]) == 1
    assert abs(float(summary["mean_rmse_mixed_sharpened_replay"]) - 19.224343) < 1.0e-6
    assert abs(float(summary["matched_minus_best_shuffled"])) < 1.0e-12
    assert "not population validation" in summary["claim_status"]

    assert set(scores["galaxy"]) == {"NGC5907", "NGC7331"}
    assert scores["beats_newton"].eq(True).all()
    assert scores["beats_tpg_v6"].eq(True).all()
    assert scores["beats_mond"].eq(True).all()
    assert scores["beats_exponential_disk_carrier"].eq(True).all()
    assert by_galaxy["matched_beats_all_wrong_labels"].eq(True).all()
    assert by_galaxy["matched_rank_within_galaxy"].eq(1).all()
    matched = permutations.loc[permutations["assignment_role"].eq("matched_diagonal")].iloc[0]
    assert int(matched["rank_by_mean_rmse"]) == 1
    assert points["claim_boundary"].eq(
        "mixed_kernel_sharpened_replay_holdout_endpoint_small_n_not_validation"
    ).all()


def test_four_case_caveat_reduction_audit_reduces_three_caveats_without_status_rewrite():
    for script in [
        "scripts/build_mixed_kernel_sharpened_replay_freeze.py",
        "scripts/run_mixed_kernel_sharpened_replay_holdout_endpoint.py",
        "scripts/build_ngc4088_formula_freeze_readiness_dashboard.py",
        "scripts/build_four_case_endpoint_status_summary.py",
        "scripts/build_four_case_caveat_reduction_audit.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "four_case_caveat_reduction_summary.csv").iloc[0]
    cases = pd.read_csv(DATA / "four_case_caveat_reduction_cases.csv")
    report = (ROOT / "reports" / "four_case_caveat_reduction_audit.md").read_text(
        encoding="utf-8"
    )

    assert summary["audit_status"] == "FOUR_CASE_CAVEAT_REDUCTION_AUDIT_COMPLETE"
    assert int(summary["n_cases"]) == 4
    assert int(summary["n_caveats_reduced"]) == 3
    assert int(summary["n_caveats_isolated_not_removed"]) == 1
    assert bool(summary["sharpened_replay_specificity_pass"]) is True
    assert bool(summary["endpoint_statuses_changed"]) is False
    assert bool(summary["endpoint_scores_recomputed"]) is False
    assert bool(summary["population_validation_claim"]) is False

    by_galaxy = cases.set_index("galaxy")
    assert by_galaxy.loc["NGC4013", "caveat_reduction_status"] == (
        "RETROSPECTIVE_CAVEAT_ISOLATED_NOT_REMOVED"
    )
    assert bool(by_galaxy.loc["NGC4013", "caveat_reduced"]) is False
    assert by_galaxy.loc["NGC5907", "caveat_reduction_status"] == (
        "PRIOR_PROJECTION_CAVEAT_REDUCED_TO_CONTROL_CONTEXT"
    )
    assert by_galaxy.loc["NGC7331", "caveat_reduction_status"] == (
        "BROAD_WINDOW_CAVEAT_REDUCED_FOR_REPLAY_NOT_RETROACTIVE_ENDPOINT"
    )
    assert by_galaxy.loc["NGC4088", "caveat_reduction_status"] == (
        "B1_PROVENANCE_CAVEAT_REDUCED_LAW_LEVEL_CAVEATS_REMAIN"
    )
    assert cases["endpoint_status_changed"].eq(False).all()
    assert cases["endpoint_scores_recomputed"].eq(False).all()
    assert cases["uses_vobs_or_residual_in_reduction"].eq(False).all()
    assert "Three caveats are reduced, not erased" in report


def test_mixed_readout_population_expansion_gate_identifies_ngc4088_but_blocks_freeze():
    for script in [
        "scripts/run_mixed_readout_population_endpoint.py",
        "scripts/run_mixed_readout_population_control_audit.py",
        "scripts/build_mixed_readout_population_expansion_gate.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "mixed_readout_population_expansion_summary.csv").iloc[0]
    candidates = pd.read_csv(DATA / "mixed_readout_population_expansion_candidates.csv")
    obligations = pd.read_csv(DATA / "mixed_readout_population_expansion_obligations.csv")

    assert summary["expansion_gate_status"] == (
        "NEXT_MIXED_CASE_IDENTIFIED_FORMULA_FREEZE_BLOCKED"
    )
    assert bool(summary["three_case_control_passed"]) is True
    assert summary["next_primary_galaxy"] == "NGC4088"
    assert bool(summary["next_primary_formula_freeze_allowed_now"]) is False
    assert int(summary["n_formula_freeze_allowed_now"]) == 0
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual_in_selection"]) is False

    ngc4088 = candidates.loc[candidates["galaxy"].eq("NGC4088")].iloc[0]
    assert ngc4088["expansion_gate_status"] == (
        "FORMULA_FREEZE_BLOCKED_SOURCE_PROTOCOL_CLOSEST"
    )
    assert bool(ngc4088["has_numeric_source_onset"]) is True
    assert bool(ngc4088["has_q_memory_review"]) is True
    assert bool(ngc4088["has_epsilon_bound"]) is True
    assert "PHYSICAL_NORMALIZATION_LAW" in ngc4088["main_blockers"]
    assert "BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES" in ngc4088["main_blockers"]
    assert "x_w=0.282353" in ngc4088["source_evidence_summary"]
    assert bool(ngc4088["formula_freeze_allowed_now"]) is False

    assert obligations["gate_status"].eq("PASS").all()
    assert "EXP3_NGC4088_NOT_PROMOTED" in set(obligations["gate_id"])


def test_ngc4088_mixed_formula_freeze_blocker_resolution_plan_is_not_endpoint():
    for script in [
        "scripts/run_mixed_readout_population_endpoint.py",
        "scripts/run_mixed_readout_population_control_audit.py",
        "scripts/build_mixed_readout_population_expansion_gate.py",
        "scripts/build_ngc4088_mixed_formula_freeze_blocker_resolution_plan.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(
        DATA / "ngc4088_mixed_formula_freeze_blocker_resolution_summary.csv"
    ).iloc[0]
    blockers = pd.read_csv(
        DATA / "ngc4088_mixed_formula_freeze_blocker_resolution_plan.csv"
    )
    supports = pd.read_csv(DATA / "ngc4088_mixed_formula_freeze_protocol_supports.csv")

    assert summary["resolution_plan_status"] == (
        "NGC4088_FORMULA_FREEZE_BLOCKER_RESOLUTION_PLAN_CREATED"
    )
    assert summary["galaxy"] == "NGC4088"
    assert int(summary["n_formula_freeze_blockers"]) == 3
    assert int(summary["n_population_claim_blockers"]) == 1
    assert int(summary["n_protocol_ready_supports"]) == 3
    assert bool(summary["formula_freeze_allowed_now"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert summary["scale_derivation_status"] == (
        "DERIVATION_BLOCKED_SELECTION_RULE_AUDITED"
    )

    blocker_ids = set(blockers["blocker_id"])
    assert "B1_INDEPENDENT_XW_DIGITIZATION_REVIEW" in blocker_ids
    assert "B2_PHYSICAL_NORMALIZATION_LAW" in blocker_ids
    assert "B3_SCALE_UNIQUENESS" in blocker_ids
    assert "B4_POPULATION_GENERALIZATION" in blocker_ids
    assert blockers["endpoint_scores_allowed_after_this_alone"].eq(False).all()
    assert supports["support_id"].eq("S1_BREAKTHROUGH_PROTOCOL_CHAIN").any()


def test_ngc4088_independent_xw_digitization_review_packet_keeps_b1_blocked():
    subprocess.run(
        ["python", "scripts/build_ngc4088_independent_xw_digitization_review_packet.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(
        DATA / "ngc4088_independent_xw_digitization_review_summary.csv"
    ).iloc[0]
    packet = pd.read_csv(DATA / "ngc4088_independent_xw_digitization_review_packet.csv")
    obligations = pd.read_csv(
        DATA / "ngc4088_independent_xw_digitization_review_obligations.csv"
    )
    response = pd.read_csv(
        DATA / "ngc4088_independent_xw_digitization_review_response_template.csv"
    ).iloc[0]

    assert summary["review_status"] == (
        "INDEPENDENT_XW_REVIEW_PACKET_READY_RESPONSE_PENDING"
    )
    assert summary["b1_resolution_status"] == (
        "B1_NOT_RESOLVED_INDEPENDENT_REVIEW_PENDING"
    )
    assert bool(summary["formula_freeze_allowed_now"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert float(summary["first_pass_x_w"]) > 0
    assert float(summary["acceptance_tolerance_x_w"]) > 0
    assert packet["forbidden_inputs"].str.contains("vobs").any()
    assert obligations["obligation_status"].isin(["READY", "PENDING"]).all()
    assert obligations["endpoint_scores_allowed"].eq(False).all()
    assert response["independent_reviewer_id"] == "PENDING_INDEPENDENT_REVIEW"


def test_ngc4088_b1_frozen_image_repeat_attempt_is_inconclusive_not_endpoint():
    subprocess.run(
        ["python", "scripts/build_ngc4088_b1_frozen_image_repeat_attempt.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(DATA / "ngc4088_b1_frozen_image_repeat_summary.csv").iloc[0]
    panel_geometry = pd.read_csv(
        DATA / "ngc4088_b1_frozen_image_repeat_panel_geometry.csv"
    )
    obligations = pd.read_csv(DATA / "ngc4088_b1_frozen_image_repeat_obligations.csv")

    assert summary["repeat_attempt_status"] == (
        "FROZEN_IMAGE_REPEAT_ATTEMPT_COMPLETE_INCONCLUSIVE"
    )
    assert summary["b1_resolution_status"] == (
        "B1_NOT_RESOLVED_IMAGE_REPEAT_INCONCLUSIVE"
    )
    assert bool(summary["accepted_x_w_from_repeat_available"]) is False
    assert bool(summary["formula_freeze_allowed_now"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert int(summary["n_panels_analyzed"]) > 0
    assert int(summary["n_elongated_components"]) > 0

    assert len(panel_geometry) > 0
    assert panel_geometry["uses_vobs_or_residual"].eq(False).all()
    assert panel_geometry["endpoint_scores_allowed"].eq(False).all()
    assert "B1R2_SOURCE_NATIVE_RADIAL_CALIBRATION" in set(obligations["obligation_id"])
    assert obligations["endpoint_scores_allowed"].eq(False).all()


def test_ngc4088_b1_source_native_radial_calibration_packet_keeps_xw_unaccepted():
    for script in [
        "scripts/build_ngc4088_b1_frozen_image_repeat_attempt.py",
        "scripts/build_ngc4088_b1_source_native_radial_calibration_packet.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(
        DATA / "ngc4088_b1_source_native_radial_calibration_summary.csv"
    ).iloc[0]
    formulas = pd.read_csv(
        DATA / "ngc4088_b1_source_native_radial_calibration_formulas.csv"
    )
    routes = pd.read_csv(DATA / "ngc4088_b1_source_native_radial_calibration_routes.csv")

    assert summary["calibration_packet_status"] == (
        "B1_SOURCE_NATIVE_RADIAL_CALIBRATION_PACKET_CREATED"
    )
    assert summary["radial_calibration_acceptance_status"] == (
        "RADIAL_CALIBRATION_NOT_ACCEPTED"
    )
    assert summary["b1_resolution_status"] == "B1_NOT_RESOLVED_RADIAL_CALIBRATION_OPEN"
    assert float(summary["first_pass_x_w"]) > 0
    assert bool(summary["accepted_x_w_for_formula_freeze"]) is False
    assert bool(summary["formula_freeze_allowed_now"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False

    assert "x_w" in set(formulas["quantity"])
    assert formulas["endpoint_scores_allowed"].eq(False).all()
    assert "RC1_INDEPENDENT_REVIEWER_DIRECT_ARCMIN" in set(routes["route_id"])
    assert "RC2_FROZEN_IMAGE_REPEAT_WITH_RADIAL_TICK_CALIBRATION" in set(
        routes["route_id"]
    )
    assert routes["uses_vobs_or_residual"].eq(False).all()


def test_ngc4088_b1_original_hi_data_acquisition_audit_keeps_b1_open():
    subprocess.run(
        ["python", "scripts/build_ngc4088_b1_original_hi_data_acquisition_audit.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(
        DATA / "ngc4088_b1_original_hi_data_acquisition_summary.csv"
    ).iloc[0]
    candidates = pd.read_csv(
        DATA / "ngc4088_b1_original_hi_data_source_candidates.csv"
    )
    attempts = pd.read_csv(
        DATA / "ngc4088_b1_original_hi_data_acquisition_attempts.csv"
    )

    assert summary["original_hi_data_audit_status"] == (
        "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE_AUDITED_NO_DIRECT_PRODUCT_CACHED"
    )
    assert summary["b1_resolution_status"] == "B1_NOT_RESOLVED_ORIGINAL_DATA_ROUTE_OPEN"
    assert bool(summary["direct_source_native_product_cached"]) is False
    assert bool(summary["whisp_direct_page_found"]) is True
    assert bool(summary["whisp_graphical_overview_cached"]) is True
    assert bool(summary["formula_freeze_allowed_now"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert int(summary["n_source_candidates_audited"]) >= 3

    assert "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE" in set(candidates["route_id"])
    assert candidates["endpoint_scores_allowed"].eq(False).all()
    assert attempts["uses_vobs_or_residual"].eq(False).all()
    assert attempts["endpoint_scores_allowed"].eq(False).all()
    assert attempts["direct_source_native_product_cached"].eq(False).all()
    assert attempts["product_status"].eq("WHISP_GRAPHICAL_OVERVIEW_CACHED_REVIEW_REQUIRED").any()


def test_ngc4088_b1_whisp_overview_extraction_packet_is_review_ready_not_endpoint():
    for script in [
        "scripts/build_ngc4088_b1_original_hi_data_acquisition_audit.py",
        "scripts/build_ngc4088_b1_whisp_overview_extraction_review_packet.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "ngc4088_b1_whisp_overview_extraction_summary.csv").iloc[0]
    packet = pd.read_csv(DATA / "ngc4088_b1_whisp_overview_extraction_packet.csv").iloc[0]
    panels = pd.read_csv(DATA / "ngc4088_b1_whisp_overview_extraction_panels.csv")
    obligations = pd.read_csv(DATA / "ngc4088_b1_whisp_overview_extraction_obligations.csv")
    response = pd.read_csv(DATA / "ngc4088_b1_whisp_overview_extraction_response_template.csv").iloc[0]

    assert summary["whisp_overview_extraction_status"] == (
        "WHISP_OVERVIEW_EXTRACTION_PACKET_READY_RESPONSE_PENDING"
    )
    assert summary["b1_resolution_status"] == (
        "B1_NOT_RESOLVED_WHISP_OVERVIEW_REVIEW_PENDING"
    )
    assert bool(summary["whisp_graphical_overview_cached"]) is True
    assert bool(summary["accepted_x_w_for_formula_freeze"]) is False
    assert bool(summary["formula_freeze_allowed_now"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False

    assert packet["primary_axis"] == "Offset from center (arcmin)"
    assert "P3_POSITION_VELOCITY_MAJOR_AXIS" in set(panels["panel_id"])
    assert panels["endpoint_scores_allowed"].eq(False).all()
    assert obligations["endpoint_scores_allowed"].eq(False).all()
    assert obligations["status"].isin(["PASS", "PENDING"]).all()
    assert response["x_w_review"] == "PENDING_WHISP_OVERVIEW_REVIEW"


def test_ngc4088_b1_whisp_overview_frozen_extraction_attempt_agrees_but_not_accepted():
    for script in [
        "scripts/build_ngc4088_b1_original_hi_data_acquisition_audit.py",
        "scripts/build_ngc4088_b1_whisp_overview_extraction_review_packet.py",
        "scripts/build_ngc4088_b1_whisp_overview_frozen_extraction_attempt.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(
        DATA / "ngc4088_b1_whisp_overview_frozen_extraction_summary.csv"
    ).iloc[0]
    components = pd.read_csv(
        DATA / "ngc4088_b1_whisp_overview_frozen_extraction_components.csv"
    )
    response = pd.read_csv(
        DATA / "ngc4088_b1_whisp_overview_frozen_extraction_response.csv"
    ).iloc[0]
    obligations = pd.read_csv(
        DATA / "ngc4088_b1_whisp_overview_frozen_extraction_obligations.csv"
    )

    assert summary["frozen_extraction_attempt_status"] == (
        "FROZEN_WHISP_OVERVIEW_EXTRACTION_ATTEMPT_COMPLETE_AGREES_WITH_FIRST_PASS"
    )
    assert summary["b1_resolution_status"] == (
        "B1_NOT_RESOLVED_FROZEN_EXTRACTION_PROMOTION_REVIEW_REQUIRED"
    )
    assert bool(summary["agrees_with_first_pass_within_tolerance"]) is True
    assert bool(summary["accepted_x_w_for_formula_freeze"]) is False
    assert bool(summary["formula_freeze_allowed_now"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert float(summary["x_w_review"]) > 0

    selected = components[components["selected_for_response"]]
    assert len(selected) == 2
    assert selected["component_side"].nunique() == 2
    assert response["reviewer_or_method_id"] == (
        "FROZEN_SCRIPT_WHISP_OVERVIEW_SATURATION_COMPONENT_CENTROID_V1"
    )
    assert obligations["endpoint_scores_allowed"].eq(False).all()


def test_ngc4088_b1_whisp_promotion_review_promotes_source_consistency_only():
    for script in [
        "scripts/build_ngc4088_b1_original_hi_data_acquisition_audit.py",
        "scripts/build_ngc4088_b1_whisp_overview_extraction_review_packet.py",
        "scripts/build_ngc4088_b1_whisp_overview_frozen_extraction_attempt.py",
        "scripts/build_ngc4088_b1_whisp_promotion_review.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "ngc4088_b1_whisp_promotion_review_summary.csv").iloc[0]
    gates = pd.read_csv(DATA / "ngc4088_b1_whisp_promotion_review_gates.csv")

    assert summary["promotion_review_status"] == (
        "B1_CAVEATED_XW_ACCEPTED_FOR_FORMULA_FREEZE_NOT_ENDPOINT"
    )
    assert summary["b1_resolution_status"] == (
        "B1_RESOLVED_CAVEATED_WHISP_GRAPHICAL_XW"
    )
    assert bool(summary["source_consistency_promoted"]) is True
    assert float(summary["x_w_source_consistency_value"]) > 0
    assert bool(summary["accepted_x_w_for_formula_freeze"]) is True
    assert bool(summary["formula_freeze_allowed_now"]) is True
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert "FORMULA_FREEZE_ACCEPTANCE" in set(gates["review_gate"])
    assert gates["endpoint_scores_allowed"].eq(False).all()
    assert gates["uses_vobs_or_residual"].eq(False).all()


def test_ngc4088_b2_physical_normalization_synthesis_keeps_law_open():
    subprocess.run(
        ["python", "scripts/build_ngc4088_b2_physical_normalization_derivation_synthesis.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(
        DATA / "ngc4088_b2_physical_normalization_synthesis_summary.csv"
    ).iloc[0]
    formula = pd.read_csv(DATA / "ngc4088_b2_physical_normalization_formula_status.csv")
    components = pd.read_csv(DATA / "ngc4088_b2_physical_normalization_components.csv")
    obligations = pd.read_csv(DATA / "ngc4088_b2_physical_normalization_obligations.csv")

    assert summary["b2_synthesis_status"] == (
        "B2_FORMULA_CONDITIONAL_DERIVATION_SYNTHESIZED_LAW_STILL_OPEN"
    )
    assert summary["formula_quality"] == "DIMENSIONALLY_VALID_RESIDUAL_BLIND_EXECUTABLE"
    assert summary["law_quality"] == "NOT_DERIVED_TAU_SIDE_PHYSICAL_NORMALIZATION_LAW"
    assert summary["formula_freeze_alignment_status"] == "ALIGNED_TO_FORMULA_FREEZE_MANIFEST"
    assert summary["normalization_source"] == "FORMULA_FREEZE_MANIFEST_REVIEW_ACCEPTED_XW"
    assert abs(float(summary["numeric_lambda_w_km2_s2"]) - 8795.11175237) < 1.0e-5
    assert abs(float(summary["first_pass_lambda_w_km2_s2"]) - 8324.016) < 1.0e-9
    assert bool(summary["formula_freeze_allowed_now"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert "sigma_warp q_warp x_w Vflat^2" in formula.iloc[0]["lambda_w_conditional"]
    assert bool(formula.iloc[0]["formula_freeze_alignment_pass"]) is True
    assert formula.iloc[0]["normalization_source"] == "FORMULA_FREEZE_MANIFEST_REVIEW_ACCEPTED_XW"
    assert abs(float(formula.iloc[0]["numeric_lambda_w_km2_s2"]) - 8795.11175237) < 1.0e-5
    assert abs(float(formula.iloc[0]["first_pass_lambda_w_km2_s2"]) - 8324.016) < 1.0e-9
    assert len(components) == int(summary["n_components"])
    assert obligations["obligation_status"].str.startswith("OPEN").all()
    assert obligations["endpoint_scores_allowed"].eq(False).all()


def test_ngc4088_b3_scale_uniqueness_synthesis_is_conditional_only():
    subprocess.run(
        ["python", "scripts/build_ngc4088_b3_scale_uniqueness_resolution_synthesis.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(DATA / "ngc4088_b3_scale_uniqueness_synthesis_summary.csv").iloc[0]
    candidates = pd.read_csv(DATA / "ngc4088_b3_scale_uniqueness_candidate_resolution.csv")
    obligations = pd.read_csv(DATA / "ngc4088_b3_scale_uniqueness_obligations.csv")

    assert summary["b3_synthesis_status"] == (
        "B3_CONDITIONAL_UNIQUE_SCALE_SELECTED_LAW_LEVEL_UNIQUENESS_OPEN"
    )
    assert summary["initial_uniqueness_decision"] == "BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES"
    assert summary["selected_scale_ids"] == "CURRENT_XW_VFLAT2"
    assert int(summary["n_initial_residual_blind_scales"]) == 5
    assert int(summary["n_selected_by_protocol_rule"]) == 1
    assert bool(summary["conditional_uniqueness_resolved"]) is True
    assert bool(summary["law_level_uniqueness_resolved"]) is False
    assert bool(summary["formula_freeze_allowed_now"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert len(candidates) == 5
    assert candidates["uses_vobs_or_residual"].eq(False).all()
    assert obligations["endpoint_scores_allowed"].eq(False).all()
    assert "B3O5_LAW_LEVEL_UNIQUENESS" in set(obligations["obligation_id"])


def test_ngc4088_formula_freeze_readiness_dashboard_keeps_endpoint_blocked():
    for script in [
        "scripts/build_ngc4088_mixed_formula_freeze_blocker_resolution_plan.py",
        "scripts/build_ngc4088_independent_xw_digitization_review_packet.py",
        "scripts/build_ngc4088_b1_frozen_image_repeat_attempt.py",
        "scripts/build_ngc4088_b1_source_native_radial_calibration_packet.py",
        "scripts/build_ngc4088_b1_original_hi_data_acquisition_audit.py",
        "scripts/build_ngc4088_b1_whisp_overview_extraction_review_packet.py",
        "scripts/build_ngc4088_b1_whisp_overview_frozen_extraction_attempt.py",
        "scripts/build_ngc4088_b1_whisp_promotion_review.py",
        "scripts/build_ngc4088_b2_physical_normalization_derivation_synthesis.py",
        "scripts/build_ngc4088_b3_scale_uniqueness_resolution_synthesis.py",
        "scripts/build_ngc4088_warp_history_formula_freeze_gate.py",
        "scripts/build_ngc4088_formula_freeze_readiness_dashboard.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "ngc4088_formula_freeze_readiness_summary.csv").iloc[0]
    dashboard = pd.read_csv(DATA / "ngc4088_formula_freeze_readiness_dashboard.csv")
    freeze_summary = pd.read_csv(
        DATA / "ngc4088_warp_history_formula_freeze_summary.csv"
    ).iloc[0]
    freeze_manifest = pd.read_csv(
        DATA / "ngc4088_warp_history_formula_freeze_manifest.csv"
    ).iloc[0]
    freeze_grid = pd.read_csv(DATA / "ngc4088_warp_history_formula_freeze_kernel_grid.csv")
    freeze_gate = pd.read_csv(DATA / "ngc4088_warp_history_formula_freeze_gate.csv")

    assert summary["dashboard_status"] == (
        "NGC4088_FORMULA_FREEZE_READINESS_DASHBOARD_CREATED"
    )
    assert summary["galaxy"] == "NGC4088"
    assert summary["b1_status"] == "B1_NOT_RESOLVED_INDEPENDENT_REVIEW_PENDING"
    assert summary["b1_repeat_status"] == (
        "FROZEN_IMAGE_REPEAT_ATTEMPT_COMPLETE_INCONCLUSIVE"
    )
    assert summary["b1_radial_calibration_status"] == "RADIAL_CALIBRATION_NOT_ACCEPTED"
    assert summary["b1_original_data_route_status"] == (
        "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE_AUDITED_NO_DIRECT_PRODUCT_CACHED"
    )
    assert summary["b1_whisp_overview_extraction_status"] == (
        "WHISP_OVERVIEW_EXTRACTION_PACKET_READY_RESPONSE_PENDING"
    )
    assert summary["b1_whisp_frozen_extraction_status"] == (
        "FROZEN_WHISP_OVERVIEW_EXTRACTION_ATTEMPT_COMPLETE_AGREES_WITH_FIRST_PASS"
    )
    assert bool(summary["b1_whisp_frozen_agrees_with_first_pass"]) is True
    assert summary["b1_whisp_promotion_status"] == (
        "B1_CAVEATED_XW_ACCEPTED_FOR_FORMULA_FREEZE_NOT_ENDPOINT"
    )
    assert bool(summary["b1_source_consistency_promoted"]) is True
    assert float(summary["b1_x_w_source_consistency_value"]) > 0
    assert bool(summary["b1_accepted_x_w_for_formula_freeze"]) is True
    assert summary["b2_status"] == (
        "B2_FORMULA_CONDITIONAL_DERIVATION_SYNTHESIZED_LAW_STILL_OPEN"
    )
    assert summary["b3_status"] == (
        "B3_CONDITIONAL_UNIQUE_SCALE_SELECTED_LAW_LEVEL_UNIQUENESS_OPEN"
    )
    assert summary["warp_history_formula_freeze_status"] == (
        "NGC4088_WARP_HISTORY_FORMULA_FREEZE_READY_LAW_CAVEATED_NOT_SCORE"
    )
    assert abs(float(summary["warp_history_lambda_w_km2_s2"]) - 8795.11175237) < 1.0e-5
    assert float(summary["warp_history_turn_on_power_frozen"]) == 1.0
    assert bool(summary["b2_law_level_open"]) is True
    assert bool(summary["b3_law_level_open"]) is True
    assert int(summary["n_local_blockers"]) == 3
    assert int(summary["n_resolved_local_blockers"]) == 3
    assert bool(summary["formula_freeze_allowed_now"]) is True
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["uses_vobs_or_residual"]) is False
    assert summary["readiness_decision"] == "FORMULA_FREEZE_READY_ENDPOINT_GATE_REQUIRED"

    assert freeze_summary["formula_freeze_status"] == (
        "NGC4088_WARP_HISTORY_FORMULA_FREEZE_READY_LAW_CAVEATED_NOT_SCORE"
    )
    assert bool(freeze_summary["formula_frozen_before_endpoint_scoring"]) is True
    assert bool(freeze_summary["prospective_endpoint_protocol_ready"]) is True
    assert bool(freeze_summary["endpoint_scores_allowed"]) is False
    assert abs(float(freeze_summary["x_w_formula_freeze"]) - 0.298333) < 1.0e-6
    assert abs(float(freeze_summary["lambda_w_km2_s2"]) - 8795.11175237) < 1.0e-5
    assert float(freeze_summary["turn_on_power_frozen"]) == 1.0
    assert freeze_manifest["carrier"] == "v_Newtonian_baryonic"
    assert "p=2 remains a sensitivity/control branch only" in freeze_manifest[
        "turn_on_power_sensitivity_control"
    ]
    assert "vobs" not in set(freeze_grid.columns)
    assert freeze_grid["uses_vobs_or_residual_in_construction"].eq(False).all()
    assert freeze_grid["endpoint_scores_allowed"].eq(False).all()
    assert freeze_gate["gate_status"].str.startswith("PASS").all()
    assert freeze_gate["endpoint_scores_allowed"].eq(False).all()

    assert set(dashboard["blocker_id"]) == {
        "B1_INDEPENDENT_XW_DIGITIZATION_REVIEW",
        "B2_PHYSICAL_NORMALIZATION_LAW",
        "B3_SCALE_UNIQUENESS",
    }
    assert bool(dashboard.loc[
        dashboard["blocker_id"].eq("B1_INDEPENDENT_XW_DIGITIZATION_REVIEW"),
        "resolved_for_formula_freeze",
    ].iloc[0]) is True
    assert dashboard["resolved_for_formula_freeze"].eq(True).all()
    assert dashboard["endpoint_scores_allowed"].eq(False).all()
    assert dashboard["uses_vobs_or_residual"].eq(False).all()


def test_ngc4088_warp_history_accepted_endpoint_scores_from_frozen_manifest():
    for script in [
        "scripts/build_ngc4088_mixed_formula_freeze_blocker_resolution_plan.py",
        "scripts/build_ngc4088_independent_xw_digitization_review_packet.py",
        "scripts/build_ngc4088_b1_frozen_image_repeat_attempt.py",
        "scripts/build_ngc4088_b1_source_native_radial_calibration_packet.py",
        "scripts/build_ngc4088_b1_original_hi_data_acquisition_audit.py",
        "scripts/build_ngc4088_b1_whisp_overview_extraction_review_packet.py",
        "scripts/build_ngc4088_b1_whisp_overview_frozen_extraction_attempt.py",
        "scripts/build_ngc4088_b1_whisp_promotion_review.py",
        "scripts/build_ngc4088_b2_physical_normalization_derivation_synthesis.py",
        "scripts/build_ngc4088_b3_scale_uniqueness_resolution_synthesis.py",
        "scripts/build_ngc4088_warp_history_formula_freeze_gate.py",
        "scripts/build_ngc4088_formula_freeze_readiness_dashboard.py",
        "scripts/build_ngc4088_warp_history_accepted_endpoint_gate.py",
        "scripts/run_ngc4088_warp_history_accepted_endpoint.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    gate_summary = pd.read_csv(
        DATA / "ngc4088_warp_history_accepted_endpoint_gate_summary.csv"
    ).iloc[0]
    manifest = pd.read_csv(DATA / "ngc4088_warp_history_accepted_endpoint_manifest.csv").iloc[0]
    gate = pd.read_csv(DATA / "ngc4088_warp_history_accepted_endpoint_gate.csv")
    endpoint_summary = pd.read_csv(
        DATA / "ngc4088_warp_history_accepted_endpoint_summary.csv"
    ).iloc[0]
    scores = pd.read_csv(DATA / "ngc4088_warp_history_accepted_endpoint_scores.csv")
    points = pd.read_csv(DATA / "ngc4088_warp_history_accepted_endpoint_points.csv")

    assert gate_summary["accepted_endpoint_freeze_status"] == (
        "CAVEATED_ACCEPTED_ENDPOINT_FREEZE_READY"
    )
    assert bool(gate_summary["endpoint_scores_allowed"]) is True
    assert bool(manifest["formula_frozen_before_endpoint_scoring"]) is True
    assert bool(manifest["uses_vobs_or_residual_in_construction"]) is False
    assert bool(manifest["posthoc_retuning_allowed"]) is False
    assert bool(manifest["endpoint_scores_allowed"]) is True
    assert gate["gate_status"].str.startswith("PASS").all()
    assert gate["endpoint_scores_allowed"].eq(True).all()

    assert endpoint_summary["endpoint_status"] == (
        "CAVEATED_ACCEPTED_ENDPOINT_PRELIMINARY_CONTROL_RESULT"
    )
    assert int(endpoint_summary["n_points"]) == 12
    assert abs(float(endpoint_summary["rmse_warp_history_accepted"]) - 11.6190379890) < 1.0e-6
    assert abs(float(endpoint_summary["best_baseline_rmse_km_s"]) - 25.3962893015) < 1.0e-6
    assert abs(float(endpoint_summary["wrong_family_mean_rmse_km_s"]) - 41.8579350143) < 1.0e-6
    assert abs(float(endpoint_summary["wrong_family_best_rmse_km_s"]) - 37.8699965618) < 1.0e-6
    assert int(endpoint_summary["matched_rank_among_all_models"]) == 1
    assert bool(endpoint_summary["matched_beats_all_baselines"]) is True
    assert bool(endpoint_summary["matched_beats_all_wrong_families"]) is True
    assert bool(endpoint_summary["construction_used_vobs"]) is False
    assert bool(endpoint_summary["scoring_used_vobs"]) is True

    matched = scores[scores["model_id"].eq("TAU_NGC4088_WARP_HISTORY_ACCEPTED")].iloc[0]
    assert matched["model_role"] == "matched_frozen_readout"
    assert abs(float(matched["rmse_km_s"]) - 11.6190379890) < 1.0e-6
    assert scores.sort_values("rmse_km_s")["model_id"].iloc[0] == (
        "TAU_NGC4088_WARP_HISTORY_ACCEPTED"
    )
    assert points["construction_used_vobs"].eq(False).all()
    assert points["scoring_used_vobs"].eq(True).all()
    assert points["endpoint_scores_allowed"].eq(True).all()


def test_ngc5907_expdisk_projection_mixed_accepted_endpoint_promotes_cleanly():
    for script in [
        "scripts/build_mixed_readout_source_selection_rule.py",
        "scripts/build_mixed_readout_candidate_acquisition_queue.py",
        "scripts/build_ngc5907_projection_freeze_gate.py",
        "scripts/build_ngc5907_projection_accepted_endpoint_gate.py",
        "scripts/build_ngc5907_expdisk_projection_mixed_formula_freeze_gate.py",
        "scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py",
        "scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.py",
        "scripts/build_ngc5907_expdisk_projection_mixed_accepted_endpoint_gate.py",
        "scripts/run_ngc5907_expdisk_projection_mixed_accepted_endpoint.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    gate_summary = pd.read_csv(
        DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_gate_summary.csv"
    ).iloc[0]
    manifest = pd.read_csv(
        DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_manifest.csv"
    ).iloc[0]
    endpoint_summary = pd.read_csv(
        DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_summary.csv"
    ).iloc[0]
    scores = pd.read_csv(DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_scores.csv")
    points = pd.read_csv(DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_points.csv")

    assert gate_summary["accepted_endpoint_freeze_status"] == (
        "ACCEPTED_MIXED_ENDPOINT_FREEZE_READY"
    )
    assert bool(gate_summary["endpoint_scores_allowed"]) is True
    assert bool(gate_summary["previous_projection_endpoint_used_as_mixed_evidence"]) is False
    assert bool(manifest["formula_frozen_before_endpoint_scoring"]) is True
    assert bool(manifest["uses_vobs_or_residual_in_construction"]) is False
    assert bool(manifest["posthoc_retuning_allowed"]) is False

    assert endpoint_summary["endpoint_status"] == (
        "ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT"
    )
    assert int(endpoint_summary["n_points"]) == 19
    assert abs(float(endpoint_summary["rmse_mixed_accepted"]) - 16.3725318404) < 1.0e-6
    assert abs(float(endpoint_summary["best_baseline_rmse_km_s"]) - 16.7855099855) < 1.0e-6
    assert abs(float(endpoint_summary["wrong_mixed_mean_rmse_km_s"]) - 17.0551660068) < 1.0e-6
    assert abs(float(endpoint_summary["wrong_mixed_best_rmse_km_s"]) - 16.8479888950) < 1.0e-6
    assert int(endpoint_summary["matched_rank_among_all_models"]) == 1
    assert bool(endpoint_summary["matched_beats_all_baselines"]) is True
    assert bool(endpoint_summary["matched_beats_all_wrong_mixed_families"]) is True
    assert bool(endpoint_summary["previous_projection_endpoint_used_as_mixed_evidence"]) is False
    assert bool(endpoint_summary["construction_used_vobs"]) is False
    assert bool(endpoint_summary["scoring_used_vobs"]) is True

    assert scores.sort_values("rmse_km_s")["model_id"].iloc[0] == (
        "TAU_NGC5907_EXPDISK_PROJECTION_MIXED_ACCEPTED"
    )
    assert points["construction_used_vobs"].eq(False).all()
    assert points["scoring_used_vobs"].eq(True).all()
    assert points["endpoint_scores_allowed"].eq(True).all()


def test_ngc7331_fractional_warp_onset_source_gate_is_replay_only():
    for script in [
        "scripts/build_mixed_readout_source_selection_rule.py",
        "scripts/build_mixed_readout_candidate_acquisition_queue.py",
        "scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py",
        "scripts/build_ngc7331_fractional_warp_onset_source_gate.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "ngc7331_fractional_warp_onset_source_summary.csv").iloc[0]
    fields = pd.read_csv(DATA / "ngc7331_fractional_warp_onset_source_fields.csv")
    gates = pd.read_csv(DATA / "ngc7331_fractional_warp_onset_source_gate.csv")
    report = (ROOT / "reports" / "ngc7331_fractional_warp_onset_source_gate.md").read_text(
        encoding="utf-8"
    )

    assert summary["source_gate_status"] == (
        "FRACTIONAL_WARP_ONSET_SOURCE_READY_REPLAY_REQUIRED"
    )
    assert bool(summary["previous_outer_warp_numeric_onset_available"]) is False
    assert bool(summary["fractional_warp_onset_available"]) is True
    assert abs(float(summary["approx_warp_onset_arcmin"]) - 3.375) < 1.0e-9
    assert abs(float(summary["approx_warp_onset_kpc"]) - 14.431691) < 1.0e-6
    assert abs(float(summary["approx_warp_onset_over_Rdisk"]) - 2.874839) < 1.0e-6
    assert abs(float(summary["approx_warp_onset_over_RHI"]) - 0.534309) < 1.0e-6
    assert bool(summary["formula_update_allowed_for_current_endpoint"]) is False
    assert bool(summary["replay_or_holdout_required"]) is True
    assert bool(summary["uses_vobs_or_residual_in_construction"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False

    assert set(fields["field_id"]) == {
        "N7331_FW1_HOLMBERG_SIZE",
        "N7331_FW2_FRACTIONAL_WARP_ONSET",
        "N7331_FW3_APPROX_ONSET_KPC",
    }
    assert fields["uses_vobs_or_residual"].eq(False).all()
    assert fields["endpoint_scores_allowed"].eq(False).all()
    assert "BLOCKED_REPLAY_REQUIRED" in set(gates["gate_status"])
    assert gates["uses_vobs_or_residual"].eq(False).all()
    assert gates["endpoint_scores_allowed"].eq(False).all()
    assert "not a post-hoc improvement" in report
    assert "predeclared replay/holdout lane" in report


def test_ngc7331_fractional_onset_v2_replay_freeze_is_not_scored_endpoint():
    for script in [
        "scripts/build_mixed_readout_source_selection_rule.py",
        "scripts/build_mixed_readout_candidate_acquisition_queue.py",
        "scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py",
        "scripts/build_ngc7331_fractional_warp_onset_source_gate.py",
        "scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.py",
        "scripts/build_ngc7331_fractional_onset_v2_replay_freeze_gate.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "ngc7331_fractional_onset_v2_replay_freeze_summary.csv").iloc[0]
    manifest = pd.read_csv(
        DATA / "ngc7331_fractional_onset_v2_replay_freeze_manifest.csv"
    ).iloc[0]
    gates = pd.read_csv(DATA / "ngc7331_fractional_onset_v2_replay_freeze_gate.csv")
    v1 = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_manifest.csv"
    ).iloc[0]
    report = (
        ROOT / "reports" / "ngc7331_fractional_onset_v2_replay_freeze_gate.md"
    ).read_text(encoding="utf-8")

    assert summary["v2_replay_freeze_status"] == "V2_REPLAY_PROTOCOL_READY_NOT_SCORED"
    assert summary["parent_v1_formula_id"] == (
        "NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1"
    )
    assert abs(float(summary["v1_window_inner_kpc"]) - 5.02) < 1.0e-9
    assert abs(float(summary["v2_window_inner_kpc"]) - 14.431691) < 1.0e-6
    assert abs(float(summary["v2_window_outer_kpc"]) - 27.01) < 1.0e-9
    assert int(summary["n_replay_blocked"]) == 1
    assert bool(summary["uses_vobs_or_residual_in_construction"]) is False
    assert bool(summary["formula_update_allowed_for_current_endpoint"]) is False
    assert bool(summary["v2_replay_scores_allowed_by_this_gate"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False

    assert manifest["formula_id"] == "NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1"
    assert manifest["formula_version"] == "V2_REPLAY_FRACTIONAL_ONSET"
    assert abs(float(manifest["r_window_inner_kpc"]) - 14.431691) < 1.0e-6
    assert abs(float(manifest["v1_broad_window_inner_kpc"]) - 5.02) < 1.0e-9
    assert bool(manifest["formula_frozen_before_replay_scoring"]) is True
    assert bool(manifest["v2_replay_scores_allowed_by_this_gate"]) is False
    assert bool(manifest["current_v1_endpoint_scores_allowed_by_this_gate"]) is False
    assert bool(manifest["uses_vobs_or_residual_in_construction"]) is False

    assert abs(float(v1["r_window_inner_kpc"]) - 5.02) < 1.0e-9
    assert "BLOCKED_REPLAY_REQUIRED" in set(gates["gate_status"])
    assert gates["endpoint_scores_allowed"].eq(False).all()
    assert gates["uses_vobs_or_residual"].eq(False).all()
    assert "already scored NGC7331 V1 accepted endpoint" in report
    assert "predeclared replay or holdout script" in report


def test_ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_preserves_caveat():
    for script in [
        "scripts/build_mixed_readout_source_selection_rule.py",
        "scripts/build_mixed_readout_candidate_acquisition_queue.py",
        "scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py",
        "scripts/build_ngc7331_fractional_warp_onset_source_gate.py",
        "scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.py",
        "scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_gate.py",
        "scripts/run_ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    gate_summary = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_gate_summary.csv"
    ).iloc[0]
    manifest = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_manifest.csv"
    ).iloc[0]
    endpoint_summary = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_summary.csv"
    ).iloc[0]
    scores = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_scores.csv"
    )
    points = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_points.csv"
    )

    assert gate_summary["accepted_endpoint_freeze_status"] == (
        "CAVEATED_ACCEPTED_MIXED_ENDPOINT_FREEZE_READY"
    )
    assert int(gate_summary["n_gates"]) == 6
    assert int(gate_summary["n_blocked"]) == 0
    assert int(gate_summary["n_caveated"]) == 2
    assert bool(gate_summary["endpoint_scores_allowed"]) is True
    assert bool(gate_summary["outer_warp_numeric_onset_available"]) is False
    assert bool(gate_summary["broad_outer_window_caveat_attached"]) is True
    assert bool(manifest["formula_frozen_before_endpoint_scoring"]) is True
    assert bool(manifest["uses_vobs_or_residual_in_construction"]) is False
    assert bool(manifest["posthoc_retuning_allowed"]) is False
    assert bool(manifest["outer_warp_numeric_onset_available"]) is False
    assert bool(manifest["broad_outer_window_caveat_attached"]) is True

    assert endpoint_summary["endpoint_status"] == (
        "CAVEATED_ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT"
    )
    assert int(endpoint_summary["n_points"]) == 36
    assert abs(float(endpoint_summary["rmse_mixed_accepted"]) - 22.2556656512) < 1.0e-6
    assert abs(float(endpoint_summary["best_baseline_rmse_km_s"]) - 23.4729768913) < 1.0e-6
    assert abs(float(endpoint_summary["wrong_mixed_mean_rmse_km_s"]) - 22.6730706096) < 1.0e-6
    assert abs(float(endpoint_summary["wrong_mixed_best_rmse_km_s"]) - 22.6682499470) < 1.0e-6
    assert int(endpoint_summary["matched_rank_among_all_models"]) == 1
    assert bool(endpoint_summary["matched_beats_all_baselines"]) is True
    assert bool(endpoint_summary["matched_beats_all_wrong_mixed_families"]) is True
    assert bool(endpoint_summary["outer_warp_numeric_onset_available"]) is False
    assert bool(endpoint_summary["broad_outer_window_caveat_attached"]) is True
    assert bool(endpoint_summary["construction_used_vobs"]) is False
    assert bool(endpoint_summary["scoring_used_vobs"]) is True

    assert scores.sort_values("rmse_km_s")["model_id"].iloc[0] == (
        "TAU_NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_ACCEPTED"
    )
    assert points["construction_used_vobs"].eq(False).all()
    assert points["scoring_used_vobs"].eq(True).all()
    assert points["endpoint_scores_allowed"].eq(True).all()


def test_four_case_endpoint_status_summary_keeps_evidence_packets_separate():
    for script in [
        "scripts/build_mixed_readout_source_selection_rule.py",
        "scripts/build_ngc4013_expdisk_wvo_formula_freeze_gate.py",
        "scripts/build_mixed_readout_candidate_acquisition_queue.py",
        "scripts/build_ngc5907_projection_freeze_gate.py",
        "scripts/build_ngc5907_projection_accepted_endpoint_gate.py",
        "scripts/build_ngc5907_expdisk_projection_mixed_formula_freeze_gate.py",
        "scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py",
        "scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.py",
        "scripts/build_mixed_readout_population_validation_gate.py",
        "scripts/run_mixed_readout_population_endpoint.py",
        "scripts/run_mixed_readout_population_control_audit.py",
        "scripts/build_ngc5907_expdisk_projection_mixed_accepted_endpoint_gate.py",
        "scripts/run_ngc5907_expdisk_projection_mixed_accepted_endpoint.py",
        "scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_gate.py",
        "scripts/run_ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint.py",
        "scripts/build_ngc4088_mixed_formula_freeze_blocker_resolution_plan.py",
        "scripts/build_ngc4088_independent_xw_digitization_review_packet.py",
        "scripts/build_ngc4088_b1_frozen_image_repeat_attempt.py",
        "scripts/build_ngc4088_b1_source_native_radial_calibration_packet.py",
        "scripts/build_ngc4088_b1_original_hi_data_acquisition_audit.py",
        "scripts/build_ngc4088_b1_whisp_overview_extraction_review_packet.py",
        "scripts/build_ngc4088_b1_whisp_overview_frozen_extraction_attempt.py",
        "scripts/build_ngc4088_b1_whisp_promotion_review.py",
        "scripts/build_ngc4088_b2_physical_normalization_derivation_synthesis.py",
        "scripts/build_ngc4088_b3_scale_uniqueness_resolution_synthesis.py",
        "scripts/build_ngc4088_warp_history_formula_freeze_gate.py",
        "scripts/build_ngc4088_formula_freeze_readiness_dashboard.py",
        "scripts/build_ngc4088_warp_history_accepted_endpoint_gate.py",
        "scripts/run_ngc4088_warp_history_accepted_endpoint.py",
        "scripts/build_four_case_endpoint_status_summary.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    cases = pd.read_csv(DATA / "four_case_endpoint_status_cases.csv")
    summary = pd.read_csv(DATA / "four_case_endpoint_status_summary.csv").iloc[0]
    report = (ROOT / "reports" / "four_case_endpoint_status_summary.md").read_text(
        encoding="utf-8"
    )

    assert summary["summary_status"] == (
        "FOUR_INSPECTED_CASES_HETEROGENEOUS_PRELIMINARY_EVIDENCE"
    )
    assert int(summary["n_inspected_cases"]) == 4
    assert int(summary["n_three_case_mixed_packet"]) == 3
    assert int(summary["n_additional_caveated_endpoint"]) == 1
    assert int(summary["n_accepted_single_galaxy_endpoints"]) == 3
    assert int(summary["n_matched_beats_best_baseline"]) == 4
    assert int(summary["n_matched_beats_all_wrong_families"]) == 4
    assert bool(summary["construction_used_vobs"]) is False
    assert bool(summary["scoring_used_vobs"]) is True
    assert "not a uniform population validation" in summary["claim_boundary"]

    assert set(cases["galaxy"]) == {"NGC4013", "NGC5907", "NGC7331", "NGC4088"}
    assert cases["evidence_packet"].str.contains("three_case|inside_three_case").sum() == 3
    ngc5907 = cases.loc[cases["galaxy"].eq("NGC5907")].iloc[0]
    assert ngc5907["endpoint_status"] == "ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT"
    assert ngc5907["evidence_packet"] == (
        "accepted_mixed_single_galaxy_endpoint_inside_three_case_packet"
    )
    ngc7331 = cases.loc[cases["galaxy"].eq("NGC7331")].iloc[0]
    assert ngc7331["endpoint_status"] == (
        "CAVEATED_ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT"
    )
    assert ngc7331["evidence_packet"] == (
        "caveated_accepted_mixed_single_galaxy_endpoint_inside_three_case_packet"
    )
    assert "broad outer window" in ngc7331["case_caveat"]
    assert (
        cases["evidence_packet"].eq("additional_caveated_single_galaxy_endpoint").sum()
        == 1
    )
    assert cases["matched_beats_best_baseline"].eq(True).all()
    assert cases["matched_beats_all_wrong_families"].eq(True).all()
    assert "heterogeneous" in report
    assert "not yet population validation" in report


def test_ngc4183_tilted_ring_review_handoff_is_residual_blind_and_not_endpoint():
    for script in [
        "scripts/build_ngc4183_mixed_overlay_source_audit.py",
        "scripts/build_ngc4183_mixed_overlay_observable_sheet.py",
        "scripts/build_ngc4183_projection_outer_warp_label_gate.py",
        "scripts/build_ngc4183_projection_outer_warp_formula_derivation.py",
        "scripts/build_ngc4183_projection_gamma_coefficient_gate.py",
        "scripts/build_ngc4183_tilted_ring_orientation_profile_extraction.py",
        "scripts/build_ngc4183_projection_gamma_upper_bound_gate.py",
        "scripts/build_ngc4183_weak_projection_control_preflight.py",
        "scripts/build_ngc4183_tilted_ring_independent_review_packet.py",
        "scripts/build_ngc4183_visual_review_readiness_gate.py",
        "scripts/build_ngc4183_tilted_ring_review_handoff.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "ngc4183_tilted_ring_review_handoff_summary.csv").iloc[0]
    tasks = pd.read_csv(DATA / "ngc4183_tilted_ring_review_handoff_tasks.csv")
    fields = pd.read_csv(DATA / "ngc4183_tilted_ring_review_handoff_response_fields.csv")
    report = (ROOT / "reports" / "ngc4183_tilted_ring_review_handoff.md").read_text(
        encoding="utf-8"
    )

    assert summary["handoff_status"] == (
        "NGC4183_TILTED_RING_REVIEW_HANDOFF_READY_RESPONSE_REQUIRED"
    )
    assert int(summary["n_tasks"]) == 5
    assert int(summary["n_visual_sources"]) == 3
    assert int(summary["n_required_response_fields"]) == 7
    assert bool(summary["response_received"]) is False
    assert bool(summary["formula_freeze_allowed"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["construction_reads_vobs"]) is False

    assert tasks["may_use_vobs"].eq(False).all()
    assert tasks["may_freeze_formula"].eq(False).all()
    assert tasks["may_score_endpoint"].eq(False).all()
    assert tasks["forbidden_inputs"].str.contains("observed rotation residuals").all()
    assert tasks["forbidden_inputs"].str.contains("endpoint score").all()
    assert set(tasks["review_item"]) == {
        "source_identity",
        "radius_series",
        "orientation_series",
        "velocity_columns_not_endpoint",
        "upper_bound_conclusion",
    }

    required = fields.loc[fields["required_for_freeze"]]
    assert set(required["field"]) == {
        "source_identity_decision",
        "radius_series_decision",
        "orientation_series_decision",
        "velocity_columns_decision",
        "upper_bound_conclusion_decision",
        "review_verdict",
        "may_freeze_null_control_after_review",
    }
    assert "not fill the response" in report
    assert "not an endpoint score" in report
    assert "rotation residuals" in report


def test_ngc4183_tilted_ring_review_response_intake_blocks_blank_template():
    pd.DataFrame(
        [
            {
                "reviewer": "independent_reviewer",
                "date": "YYYY-MM-DD",
                "source_identity_decision": "",
                "radius_series_decision": "",
                "orientation_series_decision": "",
                "velocity_columns_decision": "",
                "upper_bound_conclusion_decision": "",
                "corrections": "",
                "review_verdict": "",
                "may_freeze_null_control_after_review": False,
            }
        ]
    ).to_csv(
        DATA / "ngc4183_tilted_ring_independent_review_response_template.csv",
        index=False,
    )

    for script in [
        "scripts/build_ngc4183_mixed_overlay_source_audit.py",
        "scripts/build_ngc4183_mixed_overlay_observable_sheet.py",
        "scripts/build_ngc4183_projection_outer_warp_label_gate.py",
        "scripts/build_ngc4183_projection_outer_warp_formula_derivation.py",
        "scripts/build_ngc4183_projection_gamma_coefficient_gate.py",
        "scripts/build_ngc4183_tilted_ring_orientation_profile_extraction.py",
        "scripts/build_ngc4183_projection_gamma_upper_bound_gate.py",
        "scripts/build_ngc4183_weak_projection_control_preflight.py",
        "scripts/build_ngc4183_tilted_ring_independent_review_packet.py",
        "scripts/build_ngc4183_tilted_ring_review_response_intake.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "ngc4183_tilted_ring_review_response_summary.csv").iloc[0]
    intake = pd.read_csv(DATA / "ngc4183_tilted_ring_review_response_intake.csv").iloc[0]
    gates = pd.read_csv(DATA / "ngc4183_tilted_ring_review_response_gates.csv")
    report = (
        ROOT / "reports" / "ngc4183_tilted_ring_review_response_intake.md"
    ).read_text(encoding="utf-8")

    assert summary["review_response_intake_status"] == (
        "NGC4183_TILTED_RING_REVIEW_RESPONSE_MISSING_OR_BLOCKED"
    )
    assert bool(summary["response_received"]) is False
    assert bool(summary["all_required_accepted"]) is False
    assert bool(summary["formula_freeze_allowed"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert summary["next_gate"] == "fill_independent_review_response"

    assert "source_identity_decision" in intake["missing_response_fields"]
    assert "orientation_series_decision" in intake["missing_response_fields"]
    assert bool(intake["may_freeze_null_control_after_review"]) is False
    assert bool(intake["formula_freeze_allowed"]) is False
    assert gates.loc[
        gates["gate_id"].eq("N4183_RI_G1_RESPONSE_RECEIVED"), "gate_status"
    ].iloc[0] == "BLOCKED"
    assert gates.loc[
        gates["gate_id"].eq("N4183_RI_G2_REQUIRED_ACCEPTANCE"), "gate_status"
    ].iloc[0] == "BLOCKED"
    assert gates.loc[
        gates["gate_id"].eq("N4183_RI_G4_NULL_CONTROL_FREEZE"), "gate_status"
    ].iloc[0] == "BLOCKED"
    assert gates["formula_freeze_allowed"].eq(False).all()
    assert gates["endpoint_scores_allowed"].eq(False).all()
    assert "response template still blank" in report
    assert "required accept/correct decisions missing" in report


def test_ngc4183_codex_internal_review_response_fills_but_does_not_freeze():
    for script in [
        "scripts/build_ngc4183_mixed_overlay_source_audit.py",
        "scripts/build_ngc4183_mixed_overlay_observable_sheet.py",
        "scripts/build_ngc4183_projection_outer_warp_label_gate.py",
        "scripts/build_ngc4183_projection_outer_warp_formula_derivation.py",
        "scripts/build_ngc4183_projection_gamma_coefficient_gate.py",
        "scripts/build_ngc4183_tilted_ring_orientation_profile_extraction.py",
        "scripts/build_ngc4183_projection_gamma_upper_bound_gate.py",
        "scripts/build_ngc4183_weak_projection_control_preflight.py",
        "scripts/build_ngc4183_tilted_ring_independent_review_packet.py",
        "scripts/build_ngc4183_codex_internal_review_response.py",
        "scripts/build_ngc4183_tilted_ring_review_response_intake.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    codex = pd.read_csv(DATA / "ngc4183_codex_internal_review_response_summary.csv").iloc[0]
    response = pd.read_csv(
        DATA / "ngc4183_tilted_ring_independent_review_response_template.csv"
    ).iloc[0]
    intake = pd.read_csv(DATA / "ngc4183_tilted_ring_review_response_intake.csv").iloc[0]
    summary = pd.read_csv(DATA / "ngc4183_tilted_ring_review_response_summary.csv").iloc[0]
    gates = pd.read_csv(DATA / "ngc4183_tilted_ring_review_response_gates.csv")
    report = (ROOT / "reports" / "ngc4183_codex_internal_review_response.md").read_text(
        encoding="utf-8"
    )

    assert codex["codex_internal_review_status"] == (
        "NGC4183_CODEX_INTERNAL_REVIEW_RESPONSE_FILLED_NOT_INDEPENDENT"
    )
    assert bool(codex["response_is_independent"]) is False
    assert bool(codex["formula_freeze_allowed"]) is False
    assert response["reviewer"] == "codex_internal_source_review_not_independent"
    for field in [
        "source_identity_decision",
        "radius_series_decision",
        "orientation_series_decision",
        "velocity_columns_decision",
        "upper_bound_conclusion_decision",
    ]:
        assert response[field] == "ACCEPT"

    assert summary["review_response_intake_status"] == (
        "NGC4183_TILTED_RING_REVIEW_RESPONSE_ACCEPTED_INTERNAL_FREEZE_BLOCKED"
    )
    assert bool(summary["reviewer_is_independent"]) is False
    assert bool(summary["response_received"]) is True
    assert bool(summary["all_required_accepted"]) is True
    assert bool(summary["formula_freeze_allowed"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert intake["reviewer"] == "codex_internal_source_review_not_independent"
    assert bool(intake["reviewer_is_independent"]) is False
    independent_gate = gates.loc[gates["gate_id"].eq("N4183_RI_G3_INDEPENDENT_REVIEWER")].iloc[0]
    assert independent_gate["gate_status"] == "BLOCKED"
    assert "not an independent review" in report


def test_ngc4183_independent_source_review_can_be_accepted_without_freeze_authorization():
    for script in [
        "scripts/build_ngc4183_mixed_overlay_source_audit.py",
        "scripts/build_ngc4183_mixed_overlay_observable_sheet.py",
        "scripts/build_ngc4183_projection_outer_warp_label_gate.py",
        "scripts/build_ngc4183_projection_outer_warp_formula_derivation.py",
        "scripts/build_ngc4183_projection_gamma_coefficient_gate.py",
        "scripts/build_ngc4183_tilted_ring_orientation_profile_extraction.py",
        "scripts/build_ngc4183_projection_gamma_upper_bound_gate.py",
        "scripts/build_ngc4183_weak_projection_control_preflight.py",
        "scripts/build_ngc4183_tilted_ring_independent_review_packet.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    pd.DataFrame(
        [
            {
                "reviewer": "external_source_reviewer_v1",
                "date": "2026-06-05",
                "source_identity_decision": "ACCEPT",
                "radius_series_decision": "ACCEPT",
                "orientation_series_decision": "ACCEPT",
                "velocity_columns_decision": "ACCEPT",
                "upper_bound_conclusion_decision": "ACCEPT",
                "corrections": (
                    "No source-transcription correction. Table 4 and the context page support "
                    "the extracted 10..241 arcsec radius series, constant i=82 deg, PA=346..349 "
                    "deg, and preserved missing approaching-side entries at 229/241 arcsec."
                ),
                "review_verdict": "INDEPENDENT_SOURCE_REVIEW_ACCEPTED_SOURCE_ONLY_FREEZE_NOT_AUTHORIZED",
                "may_freeze_null_control_after_review": False,
            }
        ]
    ).to_csv(
        DATA / "ngc4183_tilted_ring_independent_review_response_template.csv",
        index=False,
    )

    subprocess.run(
        ["python", "scripts/build_ngc4183_tilted_ring_review_response_intake.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = pd.read_csv(DATA / "ngc4183_tilted_ring_review_response_summary.csv").iloc[0]
    intake = pd.read_csv(DATA / "ngc4183_tilted_ring_review_response_intake.csv").iloc[0]
    gates = pd.read_csv(DATA / "ngc4183_tilted_ring_review_response_gates.csv")

    assert summary["review_response_intake_status"] == (
        "NGC4183_TILTED_RING_REVIEW_RESPONSE_ACCEPTED_INDEPENDENT_SOURCE_ONLY_FREEZE_BLOCKED"
    )
    assert bool(summary["reviewer_is_independent"]) is True
    assert bool(summary["response_received"]) is True
    assert bool(summary["all_required_accepted"]) is True
    assert bool(summary["formula_freeze_allowed"]) is False
    assert summary["next_gate"] == "review_freeze_authorization_or_preserve_source_only_block"
    assert intake["reviewer"] == "external_source_reviewer_v1"
    assert bool(intake["reviewer_is_independent"]) is True
    assert bool(intake["formula_freeze_allowed"]) is False
    assert gates.loc[
        gates["gate_id"].eq("N4183_RI_G3_INDEPENDENT_REVIEWER"), "gate_status"
    ].iloc[0] == "PASS"
    assert gates.loc[
        gates["gate_id"].eq("N4183_RI_G4_NULL_CONTROL_FREEZE"), "gate_status"
    ].iloc[0] == "BLOCKED"


def test_ngc4183_null_control_downstream_chain_stays_blocked_without_review():
    for script in [
        "scripts/build_ngc4183_mixed_overlay_source_audit.py",
        "scripts/build_ngc4183_mixed_overlay_observable_sheet.py",
        "scripts/build_ngc4183_projection_outer_warp_label_gate.py",
        "scripts/build_ngc4183_projection_outer_warp_formula_derivation.py",
        "scripts/build_ngc4183_projection_gamma_coefficient_gate.py",
        "scripts/build_ngc4183_tilted_ring_orientation_profile_extraction.py",
        "scripts/build_ngc4183_projection_gamma_upper_bound_gate.py",
        "scripts/build_ngc4183_weak_projection_control_preflight.py",
        "scripts/build_ngc4183_tilted_ring_independent_review_packet.py",
        "scripts/build_ngc4183_codex_internal_review_response.py",
        "scripts/build_ngc4183_visual_review_readiness_gate.py",
        "scripts/build_ngc4183_tilted_ring_review_response_intake.py",
        "scripts/build_readout_lane_freeze_gate.py",
        "scripts/build_ngc4183_null_control_freeze_readiness_gate.py",
        "scripts/build_ngc4183_null_control_formula_freeze_gate.py",
        "scripts/build_ngc4183_accepted_null_control_gate.py",
        "scripts/build_ngc4183_control_promotion_roadmap.py",
        "scripts/run_ngc4183_weak_projection_null_control_scoring_gate.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    readiness = pd.read_csv(DATA / "ngc4183_null_control_freeze_readiness_summary.csv").iloc[0]
    freeze = pd.read_csv(DATA / "ngc4183_null_control_formula_freeze_summary.csv").iloc[0]
    accepted = pd.read_csv(DATA / "ngc4183_accepted_null_control_summary.csv").iloc[0]
    scoring = pd.read_csv(
        DATA / "ngc4183_weak_projection_null_control_scoring_summary.csv"
    ).iloc[0]
    scoring_gates = pd.read_csv(
        DATA / "ngc4183_weak_projection_null_control_scoring_gates.csv"
    )

    assert readiness["null_control_freeze_readiness_status"] == (
        "NGC4183_NULL_CONTROL_FREEZE_BLOCKED_REVIEW_REQUIRED"
    )
    assert bool(readiness["weak_control_preflight_pass"]) is True
    assert bool(readiness["review_accepts_freeze"]) is False
    assert bool(readiness["formula_freeze_allowed"]) is False
    assert bool(readiness["endpoint_scores_allowed"]) is False

    assert freeze["null_control_formula_freeze_status"] == (
        "NGC4183_NULL_CONTROL_FORMULA_FREEZE_BLOCKED_REVIEW_REQUIRED"
    )
    assert bool(freeze["formula_freeze_allowed"]) is False
    assert bool(freeze["endpoint_scores_allowed"]) is False

    assert accepted["accepted_null_control_gate_status"] == (
        "NGC4183_ACCEPTED_NULL_CONTROL_BLOCKED_FORMULA_NOT_FROZEN"
    )
    assert bool(accepted["accepted_control_allowed"]) is False
    assert bool(accepted["endpoint_scores_allowed"]) is False

    assert scoring["scoring_gate_status"] == (
        "NGC4183_WEAK_PROJECTION_NULL_CONTROL_SCORING_BLOCKED_PRE_ACCEPTANCE"
    )
    assert bool(scoring["accepted_control_allowed"]) is False
    assert bool(scoring["formula_freeze_allowed"]) is False
    assert bool(scoring["construction_reads_vobs"]) is False
    assert bool(scoring["scoring_reads_vobs"]) is False
    assert bool(scoring["endpoint_scores_allowed"]) is False
    assert scoring_gates["endpoint_scores_allowed"].eq(False).all()


def test_ngc4183_control_status_dashboard_identifies_review_response_blocker():
    for script in [
        "scripts/build_ngc4183_mixed_overlay_source_audit.py",
        "scripts/build_ngc4183_mixed_overlay_observable_sheet.py",
        "scripts/build_ngc4183_projection_outer_warp_label_gate.py",
        "scripts/build_ngc4183_projection_outer_warp_formula_derivation.py",
        "scripts/build_ngc4183_projection_gamma_coefficient_gate.py",
        "scripts/build_ngc4183_tilted_ring_orientation_profile_extraction.py",
        "scripts/build_ngc4183_projection_gamma_upper_bound_gate.py",
        "scripts/build_ngc4183_preendpoint_decision_synthesis.py",
        "scripts/build_ngc4183_weak_projection_control_preflight.py",
        "scripts/build_ngc4183_tilted_ring_independent_review_packet.py",
        "scripts/build_ngc4183_tilted_ring_review_handoff.py",
        "scripts/build_ngc4183_codex_internal_review_response.py",
        "scripts/build_ngc4183_tilted_ring_review_response_intake.py",
        "scripts/build_ngc4183_visual_review_readiness_gate.py",
        "scripts/build_readout_lane_freeze_gate.py",
        "scripts/build_ngc4183_null_control_freeze_readiness_gate.py",
        "scripts/build_ngc4183_null_control_formula_freeze_gate.py",
        "scripts/build_ngc4183_accepted_null_control_gate.py",
        "scripts/build_ngc4183_control_promotion_roadmap.py",
        "scripts/run_ngc4183_weak_projection_null_control_scoring_gate.py",
        "scripts/build_ngc4183_control_status_dashboard.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    summary = pd.read_csv(DATA / "ngc4183_control_status_dashboard_summary.csv").iloc[0]
    stages = pd.read_csv(DATA / "ngc4183_control_status_dashboard_stages.csv")
    report = (ROOT / "reports" / "ngc4183_control_status_dashboard.md").read_text(
        encoding="utf-8"
    )
    html = (ROOT / "reports" / "ngc4183_control_status_dashboard.html").read_text(
        encoding="utf-8"
    )

    assert summary["dashboard_status"] == "NGC4183_CONTROL_STATUS_DASHBOARD_BUILT_NOT_ENDPOINT"
    assert int(summary["n_stages"]) == 11
    assert int(summary["n_pass_or_ready_stages"]) == 6
    assert int(summary["n_blocked_stages"]) == 5
    assert summary["first_blocking_stage"] == "review_response_intake"
    assert summary["first_blocking_status"] == (
        "NGC4183_TILTED_RING_REVIEW_RESPONSE_ACCEPTED_INTERNAL_FREEZE_BLOCKED"
    )
    assert summary["next_required_action"] == "obtain_independent_review_response"
    assert bool(summary["formula_freeze_allowed"]) is False
    assert bool(summary["endpoint_scores_allowed"]) is False
    assert bool(summary["construction_reads_vobs"]) is False
    assert bool(summary["scoring_reads_vobs"]) is False

    assert set(stages["stage_id"]) == {
        "source_audit",
        "tilted_ring_profile",
        "projection_gamma_upper_bound",
        "weak_projection_control_preflight",
        "independent_review_packet",
        "review_handoff",
        "review_response_intake",
        "freeze_readiness",
        "formula_freeze",
        "accepted_null_control",
        "scoring_gate",
    }
    assert stages["endpoint_scores_allowed"].eq(False).all()
    assert stages["construction_reads_vobs"].eq(False).all()
    assert "not a formula freeze and not an endpoint score" in report
    assert "first blocking stage is the" in report
    assert "NGC4183 Control Status Dashboard" in html
    assert "review_response_intake" in html
    assert "Endpoint scores allowed" in html
    assert "False" in html


def test_ngc4183_authorized_null_control_endpoint_runs_as_interval_branch():
    for script in [
        "scripts/build_ngc4183_mixed_overlay_source_audit.py",
        "scripts/build_ngc4183_mixed_overlay_observable_sheet.py",
        "scripts/build_ngc4183_projection_outer_warp_label_gate.py",
        "scripts/build_ngc4183_projection_outer_warp_formula_derivation.py",
        "scripts/build_ngc4183_projection_gamma_coefficient_gate.py",
        "scripts/build_ngc4183_tilted_ring_orientation_profile_extraction.py",
        "scripts/build_ngc4183_projection_gamma_upper_bound_gate.py",
        "scripts/build_ngc4183_preendpoint_decision_synthesis.py",
        "scripts/build_ngc4183_weak_projection_control_preflight.py",
        "scripts/build_ngc4183_tilted_ring_independent_review_packet.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    pd.DataFrame(
        [
            {
                "reviewer": "external_source_reviewer_v1",
                "date": "2026-06-05",
                "source_identity_decision": "ACCEPT",
                "radius_series_decision": "ACCEPT",
                "orientation_series_decision": "ACCEPT",
                "velocity_columns_decision": "ACCEPT",
                "upper_bound_conclusion_decision": "ACCEPT",
                "corrections": "Independent source review accepted; freeze authorized.",
                "review_verdict": "INDEPENDENT_SOURCE_REVIEW_ACCEPTED_FREEZE_AUTHORIZED",
                "may_freeze_null_control_after_review": True,
            }
        ]
    ).to_csv(
        DATA / "ngc4183_tilted_ring_independent_review_response_template.csv",
        index=False,
    )

    for script in [
        "scripts/build_ngc4183_tilted_ring_review_response_intake.py",
        "scripts/build_ngc4183_visual_review_readiness_gate.py",
        "scripts/build_readout_lane_freeze_gate.py",
        "scripts/build_ngc4183_null_control_freeze_readiness_gate.py",
        "scripts/build_ngc4183_null_control_formula_freeze_gate.py",
        "scripts/build_ngc4183_accepted_null_control_gate.py",
        "scripts/run_ngc4183_weak_projection_null_control_scoring_gate.py",
        "scripts/run_ngc4183_weak_projection_null_control_accepted_endpoint.py",
        "scripts/build_ngc4183_control_promotion_roadmap.py",
        "scripts/run_ngc4183_weak_projection_null_control_scoring_gate.py",
        "scripts/build_ngc4183_control_status_dashboard.py",
    ]:
        subprocess.run(
            ["python", script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    endpoint = pd.read_csv(
        DATA / "ngc4183_weak_projection_null_control_accepted_endpoint_summary.csv"
    ).iloc[0]
    scoring = pd.read_csv(
        DATA / "ngc4183_weak_projection_null_control_scoring_summary.csv"
    ).iloc[0]
    roadmap = pd.read_csv(DATA / "ngc4183_control_promotion_roadmap_summary.csv").iloc[0]
    dashboard = pd.read_csv(DATA / "ngc4183_control_status_dashboard_summary.csv").iloc[0]

    assert endpoint["endpoint_status"] == (
        "NGC4183_ACCEPTED_NULL_CONTROL_INTERVAL_ENDPOINT_COMPLETE"
    )
    assert bool(endpoint["construction_used_vobs"]) is False
    assert bool(endpoint["scoring_used_vobs"]) is True
    assert bool(endpoint["endpoint_scores_allowed"]) is True

    assert scoring["scoring_gate_status"] == (
        "NGC4183_ACCEPTED_NULL_CONTROL_INTERVAL_ENDPOINT_COMPLETE"
    )
    assert bool(scoring["accepted_control_allowed"]) is True
    assert bool(scoring["formula_freeze_allowed"]) is True
    assert bool(scoring["construction_reads_vobs"]) is False
    assert bool(scoring["scoring_reads_vobs"]) is True
    assert bool(scoring["endpoint_scores_allowed"]) is True
    assert scoring["primary_blocker"] == "none"

    assert roadmap["control_roadmap_status"] == (
        "NGC4183_CONTROL_PROMOTION_ROADMAP_READY_FOR_SCORING_IMPLEMENTATION"
    ) or roadmap["control_roadmap_status"] == (
        "NGC4183_CONTROL_PROMOTION_ROADMAP_SCORING_COMPLETE_PRELIMINARY_CONTROL"
    )
    assert dashboard["first_blocking_stage"] in {"scoring_gate", "none"}
