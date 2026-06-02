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
        ROOT / "scripts/run_manifest_confidence_diagnostics.py",
        ROOT / "scripts/run_amplitude_policy_diagnostics.py",
        ROOT / "scripts/run_amplitude_shrinkage_path.py",
        ROOT / "scripts/run_train_selected_shrinkage_diagnostic.py",
        ROOT / "scripts/run_family_breakdown_diagnostics.py",
        ROOT / "scripts/run_family_observable_quality_diagnostics.py",
        ROOT / "scripts/run_predeclared_quality_gate_diagnostics.py",
        ROOT / "scripts/run_quality_gate_shuffled_null_diagnostics.py",
        ROOT / "scripts/run_endpoint_decision_matrix.py",
        ROOT / "scripts/build_predeclared_endpoint_protocol.py",
        ROOT / "scripts/build_readiness_upgrade_audit.py",
        ROOT / "scripts/build_morphology_observable_intake_schema.py",
        ROOT / "scripts/run_morphology_observable_gap_audit.py",
        ROOT / "scripts/build_arxiv_source.py",
        ROOT / "scripts/reproduce.py",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == []


def test_manuscript_contains_forward_gate_and_claim_boundaries():
    source = (SOURCE / "main.tex").read_text(encoding="utf-8")
    assert "MORPHOLOGY-MATCHED-FORWARD-READOUT-GATE" in source
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
    forbidden_phrases = [
        "We prove Tau Core",
        "This paper demonstrates Tau Core has beaten MOND/RAR",
        "MOND and RAR are superseded",
        "we derive a universal galaxy law",
    ]
    for phrase in forbidden_phrases:
        assert phrase not in source


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
