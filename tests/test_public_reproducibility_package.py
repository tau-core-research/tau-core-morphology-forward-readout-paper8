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
        ROOT / "scripts/run_source_native_readout_formula_endpoint.py",
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
    assert labels["label_source"].str.contains("no residual endpoints").all()
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
    assert "not empirical validation" in report


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
