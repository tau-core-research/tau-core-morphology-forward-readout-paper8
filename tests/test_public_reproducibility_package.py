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
