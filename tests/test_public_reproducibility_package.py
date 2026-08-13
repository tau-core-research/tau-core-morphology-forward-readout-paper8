import json
import hashlib
import math
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
        ROOT / "scripts/reproduce.py",
        ROOT / "scripts/generate_paper8_artifacts.py",
        ROOT / "scripts/audit_paper8_foundations.py",
        ROOT / "scripts/run_source_native_readout_formula_endpoint.py",
        ROOT / "scripts/run_source_native_carrier_robustness.py",
        ROOT / "arxiv_submission_source.zip",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert not missing


def test_paper1_source_boundary_is_explicit():
    reproduce = (ROOT / "scripts" / "reproduce.py").read_text(encoding="utf-8")
    assert "Paper 9 repository" in reproduce
    assert "PAPER8_INTERNAL_PREFLIGHT_REPRODUCTION_COMPLETE" in reproduce
    assert "build_arxiv_projection_enriched_source.py" not in reproduce


def test_headline_artifacts_are_present():
    required = [
        DATA / "source_native_readout_formula_endpoint_summary.csv",
        DATA / "source_native_readout_formula_robustness_summary.csv",
        DATA / "source_native_carrier_robustness_summary.csv",
        DATA / "accepted_morphology_manifest.csv",
        DATA / "narrow_accepted_exponential_disk_population_endpoint_summary.csv",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert not missing

    summary = pd.read_csv(DATA / "source_native_readout_formula_endpoint_summary.csv")
    assert not summary.empty


def test_arxiv_source_package_contains_latex_sources():
    zip_path = ROOT / "arxiv_submission_source.zip"
    assert zip_path.exists()
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "main.pdf" not in names


def test_s4g_optical_morphology_attribution_negative_result_is_preserved():
    freeze_path = DATA / "s4g_optical_morphology_attribution_freeze_v02.json"
    result_path = DATA / "s4g_optical_morphology_attribution_endpoint_v02.json"
    assert freeze_path.exists()
    assert result_path.exists()

    import json

    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert freeze["source_only"] is True
    assert freeze["endpoint_access"] is False
    assert freeze["n_rows"] == 76
    assert freeze["n_train"] == 56
    assert freeze["n_holdout"] == 20
    assert result["status"] == (
        "RETROSPECTIVE_S4G_OPTICAL_MORPHOLOGY_INCREMENTAL_SIGNAL_FAIL"
    )
    assert result["projection_target"]["mse_reduction"] < 0
    assert result["nulls"]["row_shuffle_p"] > 0.05
    assert result["nulls"]["column_shuffle_p"] > 0.05
    assert not all(result["gates"].values())


def test_specific_attribution_routes_are_preserved():
    import json

    theta = json.loads(
        (DATA / "ungc_theta1_environment_attribution_endpoint_v01.json").read_text(
            encoding="utf-8"
        )
    )
    lopsidedness = json.loads(
        (DATA / "s4g_lopsidedness_source_coverage_v01.json").read_text(
            encoding="utf-8"
        )
    )
    asymmetry_freeze = json.loads(
        (DATA / "s4g_stellar_asymmetry_attribution_freeze_v01.json").read_text(
            encoding="utf-8"
        )
    )
    asymmetry = json.loads(
        (DATA / "s4g_stellar_asymmetry_attribution_endpoint_v01.json").read_text(
            encoding="utf-8"
        )
    )

    assert theta["status"] == "RETROSPECTIVE_UNGC_THETA1_ENVIRONMENT_SIGNAL_FAIL"
    assert theta["shuffle"]["p"] > 0.05
    assert lopsidedness["status"] == "SOURCE_COVERAGE_INSUFFICIENT_NOT_ENDPOINT"
    assert lopsidedness["unique_matches"] == 1
    assert asymmetry_freeze["endpoint_access"] is False
    assert asymmetry_freeze["n_rows"] == 75
    assert asymmetry_freeze["source_channel_concordance_gate"] is True
    assert asymmetry["status"] == "RETROSPECTIVE_S4G_STELLAR_ASYMMETRY_SIGNAL_FAIL"
    assert asymmetry["tpg_3p6_primary"]["mse_reduction"] < 0
    assert asymmetry["tpg_4p5_replication"]["mse_reduction"] < 0
    assert not all(asymmetry["gates"].values())


def test_disk_break_dynamic_onset_pilot_is_small_n_diagnostic():
    import json

    freeze = json.loads(
        (DATA / "s4g_disk_break_dynamic_onset_freeze_v01.json").read_text(
            encoding="utf-8"
        )
    )
    result = json.loads(
        (DATA / "s4g_disk_break_dynamic_onset_alignment_v01.json").read_text(
            encoding="utf-8"
        )
    )

    assert freeze["source_only"] is True
    assert freeze["endpoint_access"] is False
    assert freeze["n_source_rows"] == 7
    assert freeze["population_claim_allowed"] is False
    assert result["status"] == (
        "DIAGNOSTIC_ONLY_S4G_DISK_BREAK_DYNAMIC_ONSET_SMALL_N"
    )
    primary = result["metrics"]["d2p0_primary"]
    assert primary["n_paired"] == 5
    assert primary["permutation_p_lower_is_better"] > 0.05
    assert result["population_claim_allowed"] is False


def test_ngc7331_clock_channel_parity_pilot_preserves_boundary():
    import json

    freeze = json.loads(
        (DATA / "ngc7331_things_clock_channel_parity_freeze_v01.json").read_text(
            encoding="utf-8"
        )
    )
    result = json.loads(
        (DATA / "ngc7331_things_clock_channel_parity_v01.json").read_text(
            encoding="utf-8"
        )
    )

    assert freeze["source_only"] is True
    assert freeze["mom1_values_opened_by_freeze"] is False
    assert freeze["endpoint_access"] is False
    assert result["status"] == (
        "SIMPLE_COMMON_MULTIPLICATIVE_CLOCK_CHANNEL_INCOMPATIBLE_SINGLE_GALAXY"
    )
    for product in ("NATURAL", "ROBUST"):
        metrics = result["product_metrics"][product]
        assert metrics["outer_median_even_over_odd"] < 0.05
        assert metrics["outer_median_abs_odd_km_s"] > 100
    assert result["predicted_to_observed_even_ratio"] > 1.0e4
    differential = result["differential_observer_path_channel"]
    assert differential["status"] == "KINEMATIC_SCALE_ESTIMATE_NOT_PATH_CHANNEL_TEST"
    assert 2.0e-4 < differential["required_delta"] < 4.0e-4
    assert "does not test a differential" in result["model_scope"]


def test_observer_channel_collective_probe_atlas_preserves_identifiability_boundary():
    import json

    atlas = json.loads(
        (DATA / "observer_channel_collective_probe_atlas_v01.json").read_text(
            encoding="utf-8"
        )
    )
    assert atlas["status"] == "COLLECTIVE_PROBE_ATLAS_BUILT_NO_INJECTIVE_A_MATRIX"
    assert atlas["n_rows"] == 12
    assert atlas["n_constructed_a_rows"] == 0
    assert atlas["collective_injectivity_test_allowed"] is False
    assert atlas["sigma_min_a_available"] is False
    assert atlas["phangs_alma_sparc_overlap"] == ["NGC2903", "NGC3521"]
    assert atlas["phangs_muse_sparc_overlap"] == []
    assert atlas["ghasp_sparc_overlap_count"] == 26
    assert atlas["ghasp_both_side_overlap_count"] == 25
    assert atlas["ghasp_whisp_overview_overlap_count"] == 21
    assert atlas["ghasp_top_source_only_candidate"] == "NGC3726"
    assert atlas["ghasp_legacy_exact_primary_name_overlap"] == ["UGC06787"]
    assert atlas["ngc3726_hi_halpha_two_side_source_support"] is True
    assert atlas["ngc3726_whisp_fits_acquired"] is False
    assert atlas["ugc06787_whisp_graphical_hi_acquired"] is True
    assert atlas["ugc06787_whisp_fits_acquired"] is False

    ghasp = json.loads(
        (DATA / "ghasp_sparc_probe_crossmatch_v01.json").read_text(encoding="utf-8")
    )
    assert ghasp["status"] == (
        "GHASP_SPARC_ONE_OBJECT_HALPHA_SOURCE_ACQUIRED_SINGLE_SIDE_ONLY_HI_FIELD_OPEN"
    )
    assert ghasp["overlap_galaxies"] == ["UGC06787"]
    assert ghasp["collective_a_row_constructed"] is False

    federation = json.loads(
        (DATA / "ghasp_sparc_source_only_candidate_federation_v01.json").read_text(
            encoding="utf-8"
        )
    )
    assert federation["status"] == (
        "GHASP_FULL_FEDERATION_SOURCE_ONLY_CANDIDATES_RANKED_NOT_ENDPOINT"
    )
    assert federation["ghasp_point_rows"] == 9713
    assert federation["ghasp_release_specific_rotation_curves"] == 175
    assert federation["ghasp_rotation_curve_galaxies"] == 173
    assert federation["sparc_overlap_galaxies"] == 26
    assert federation["both_side_overlap_galaxies"] == 25
    assert federation["top_source_only_candidate"] == "NGC3726"
    assert federation["selection_uses_vobs_or_residual"] is False
    assert federation["physical_a_row_constructed"] is False

    ngc3726 = json.loads(
        (DATA / "ngc3726_whisp_graphical_side_preflight_v01.json").read_text(
            encoding="utf-8"
        )
    )
    assert ngc3726["status"] == (
        "NGC3726_HI_HALPHA_TWO_SIDE_SOURCE_SUPPORT_CONFIRMED_COMMON_TRANSPORT_OPEN"
    )
    assert ngc3726["both_hi_velocity_sides_present"] is True
    assert ngc3726["both_halpha_sides_present"] is True
    assert ngc3726["world_coordinate_transport_ready"] is False
    assert ngc3726["physical_a_row_constructed"] is False

    transport = json.loads(
        (DATA / "ngc3726_hi_halpha_angular_transport_freeze_v01.json").read_text(
            encoding="utf-8"
        )
    )
    channel = json.loads(
        (DATA / "ngc3726_hi_halpha_channel_preflight_v01.json").read_text(
            encoding="utf-8"
        )
    )
    assert transport["velocity_values_opened_during_freeze"] is False
    assert transport["common_radii_arcsec"] == [40.0, 60.0, 80.0, 100.0, 120.0, 140.0]
    assert channel["status"] == (
        "NGC3726_TWO_TRACER_ODD_CONTRAST_NULL_NOT_REJECTED_PATTERN_DIAGNOSTIC"
    )
    assert channel["primary_odd_contrast"]["chi2_zero_p"] > 0.05
    assert channel["primary_odd_contrast"]["pearson_halpha_hi_odd"] > 0.8
    assert abs(channel["primary_odd_contrast"]["gls_mean_z"]) < 1.0
    assert channel["observer_channel_detected"] is False
    assert channel["sparc_endpoint_opened"] is False

    ngc4559 = json.loads(
        (DATA / "ngc4559_halogas_moment_sources_v01.json").read_text(
            encoding="utf-8"
        )
    )
    assert ngc4559["status"] == (
        "NGC4559_HALOGAS_HR_LR_MOMENT0_MOMENT1_FITS_ACQUIRED_PIXELS_UNOPENED"
    )
    assert ngc4559["source_only_rank"] == 2
    assert ngc4559["n_products"] == 4
    assert ngc4559["pixel_values_opened"] is False
    assert ngc4559["cube_downloaded"] is False
    assert ngc4559["sparc_endpoint_opened"] is False

    ngc4559_freeze = json.loads(
        (DATA / "ngc4559_halogas_extraction_freeze_v01.json").read_text(
            encoding="utf-8"
        )
    )
    ngc4559_result = json.loads(
        (DATA / "ngc4559_halogas_hi_halpha_replication_v01.json").read_text(
            encoding="utf-8"
        )
    )
    assert ngc4559_freeze["pixel_values_opened_during_freeze"] is False
    assert ngc4559_freeze["common_radii_arcsec"] == [42.0, 84.0, 126.0, 168.0]
    assert ngc4559_result["status"] == (
        "NGC4559_HALOGAS_HI_HALPHA_REPLICATION_NOT_POSITIVE"
    )
    assert ngc4559_result["maps"]["HR"]["summary"]["chi2_zero_p"] > 0.05
    assert ngc4559_result["maps"]["LR"]["summary"]["chi2_zero_p"] > 0.05
    assert ngc4559_result["hr_lr_same_sign_radius_fraction"] == 1.0
    assert ngc4559_result["all_replication_gates_pass"] is False
    assert ngc4559_result["observer_channel_detected"] is False

    ngc3893 = json.loads(
        (DATA / "ngc3893_replication_eligibility_v01.json").read_text(
            encoding="utf-8"
        )
    )
    assert ngc3893["status"] == (
        "NGC3893_DISTURBED_CONTROL_PRIMARY_REPLICATION_BLOCKED"
    )
    assert ngc3893["source_only_rank"] == 3
    assert ngc3893["primary_replication_eligible"] is False
    assert ngc3893["channel_statistic_run"] is False
    assert ngc3893["counts_as_negative_channel_test"] is False
    assert ngc3893["evidence"]["interaction_and_non_circular_motion"] is True
    assert ngc3893["evidence"]["dedicated_curve_symmetry_targeted"] is True
    assert ngc3893["next_clean_candidate"] == "UGC08490"

    whisp = json.loads(
        (DATA / "ugc06787_whisp_hi_source_v01.json").read_text(encoding="utf-8")
    )
    assert whisp["status"] == (
        "WHISP_UGC06787_GRAPHICAL_HI_VELOCITY_FIELD_ACQUIRED_FITS_OPEN"
    )
    assert whisp["graphical_velocity_field_acquired"] is True
    assert whisp["source_coordinate_fits_acquired"] is False
    assert whisp["physical_a_row_constructed"] is False

    preflight = json.loads(
        (DATA / "ugc06787_whisp_graphical_velocity_preflight_v01.json").read_text(
            encoding="utf-8"
        )
    )
    assert preflight["status"] == (
        "WHISP_UGC06787_60ARCSEC_GRAPHICAL_VELOCITY_DIGITIZED_WORLD_TRANSPORT_OPEN"
    )
    assert preflight["both_hi_velocity_sides_present"] is True
    assert preflight["raw_exact_palette_pixels"] == 2578
    assert preflight["exact_palette_pixels"] == 2511
    assert preflight["connected_component_sizes"][0] == 2511
    assert preflight["world_coordinate_transport_ready"] is False
    assert preflight["halpha_common_radial_transport_ready"] is False
    assert preflight["physical_a_row_constructed"] is False

    angular = json.loads(
        (DATA / "ugc06787_common_angular_transport_gate_v01.json").read_text(
            encoding="utf-8"
        )
    )
    assert angular["status"] == (
        "UGC06787_ANGULAR_FIRST_TRANSPORT_RULE_FROZEN_WORLD_AXIS_CALIBRATION_OPEN"
    )
    assert angular["ghasp_native_max_radius_arcsec"] == 173.7
    assert angular["distance_spread_max_over_min"] > 1.2
    assert angular["kpc_transport_allowed"] is False
    assert angular["common_hi_halpha_angular_transport_ready"] is False

    axis = json.loads(
        (DATA / "ugc06787_whisp_angular_axis_preflight_v01.json").read_text(
            encoding="utf-8"
        )
    )
    assert axis["status"] == (
        "WHISP_UGC06787_SOURCE_AXIS_PROXY_CALIBRATED_CENTER_AND_WCS_OPEN"
    )
    assert axis["source_axis_proxy_ready"] is True
    assert axis["formal_wcs_ready"] is False
    assert axis["ghasp_support_inside_both_hi_proxy_maxima"] is True
    assert axis["common_hi_halpha_angular_transport_ready"] is False


def test_little_things_prospective_kernel_score_artifacts():
    extraction = json.loads(
        (DATA / "little_things_baryonic_vector_extraction_v01.json").read_text()
    )
    score = json.loads(
        (DATA / "little_things_prospective_kernel_score_v01.json").read_text()
    )
    assert extraction["n_quality_pass"] >= 20
    assert score["prospective_formula_retuning"] is False
    assert score["primary"]["n_galaxies"] == 14
    assert score["primary"]["n_points"] == 313
    assert score["primary_matched_family_rank1_fraction"] == 0.5


def test_theory_completed_scale_tail_kernel_v02():
    result = json.loads(
        (DATA / "theory_completed_scale_tail_kernel_v02.json").read_text()
    )
    assert result["selected_feature"] == "phi_tail_bounded"
    assert result["eta_units"] == "dimensionless"
    assert result["little_things_is_prospective_for_v02"] is False
    assert result["time_operator_identified"] is False
    assert result["quantum_operator_identified"] is False


def test_little_things_lightcone_capacity_score():
    result = json.loads(
        (DATA / "little_things_lightcone_capacity_score_v01.json").read_text()
    )
    assert result["status"] == "DIAGNOSTIC_ONLY_NOT_ENDPOINT"
    assert result["eta_source"].endswith("no LITTLE THINGS refit")
    assert result["primary"]["n_galaxies"] == 14
    assert result["measured_channel_finite_dimensional"] is True
    assert result["primary_capacity"]["all_sampled_modes_retained"] is True
    assert result["raw_null_propagation_claimed_compact"] is False
    assert result["physical_time_operator_identified"] is False


def test_little_things_oscc_capacity_scoring_v02():
    result = json.loads(
        (DATA / "little_things_oscc_capacity_scoring_v02.json").read_text()
    )
    assert result["status"] == "DIAGNOSTIC_ONLY_NOT_ENDPOINT"
    assert result["eta_refit"] is False
    assert result["primary"]["n_galaxies"] == 14
    assert result["capacity_modifies_prediction_directly"] is False
    assert result["physical_parent_cost_metric_derived"] is False
    assert result["time_operator_identified"] is False
    assert result["quantum_operator_identified"] is False


def test_joint_channel_component_measurement_v01():
    result = json.loads(
        (DATA / "joint_channel_component_measurement_v01.json").read_text()
    )
    assert result["status"] == "SAME_BODY_PRECISION_GAIN_MEASURED_DISTINCT_MODE_AND_FULL_ORIGIN_BLOCKED"
    assert result["same_body_tracer_delta_i_computed"] is True
    assert result["same_body_distinct_tracer_mode_detected"] is False
    assert result["full_joint_channel_delta_i_computable"] is False
    assert result["physical_channel_detected"] is False
    assert result["quantum_channel_status"] == "unmeasured"


def test_same_body_joint_conditional_information_v01():
    result = json.loads(
        (DATA / "same_body_joint_conditional_information_v01.json").read_text()
    )
    assert result["galaxies"] == 2
    assert result["channel_pairs"] == 3
    assert result["positive_incremental_information_all_sensitivities"]["hi_given_halpha"] is True
    assert result["positive_incremental_information_all_sensitivities"]["halpha_given_hi"] is True
    assert result["stacked_rank_increment"] == 0
    assert result["shared_source_innovation_null_rejected"] is False
    assert result["distinct_tracer_source_mode_detected"] is False
    assert result["physical_channel_detected"] is False


def test_ngc3351_phangs_tracer_velocity_field_rank_test():
    source = json.loads((DATA / "ngc3351_phangs_tracer_velocity_fields_v01.json").read_text())
    result = json.loads((DATA / "ngc3351_phangs_tracer_velocity_field_rank_test_v01.json").read_text())
    assert source["status"] == "SOURCE_NATIVE_2D_TRACER_VELOCITY_FIELDS_ACQUIRED"
    assert result["beam_independent_pixels"] >= 50
    assert result["construction_uses_rotation_residual"] is False
    assert result["time_channel_identified"] is False
    assert result["quantum_channel_identified"] is False


def test_ngc4254_phangs_tracer_velocity_field_control():
    source = json.loads((DATA / "ngc4254_phangs_tracer_velocity_fields_v01.json").read_text())
    result = json.loads((DATA / "ngc4254_phangs_tracer_velocity_field_rank_test_v01.json").read_text())
    assert source["status"] == "SOURCE_NATIVE_2D_TRACER_VELOCITY_FIELDS_ACQUIRED"
    assert result["galaxy"] == "NGC4254"
    assert result["morphology_control"] == "unbarred_lopsided_environmentally_disturbed"
    assert result["beam_independent_pixels"] > 5000
    assert result["sector_jackknife_max_absolute_mode_z"] < 3.0
    assert result["construction_uses_rotation_residual"] is False
    assert result["time_channel_identified"] is False
    assert result["quantum_channel_identified"] is False


def test_ngc3627_phangs_tracer_velocity_field_stress_control():
    source = json.loads((DATA / "ngc3627_phangs_tracer_velocity_fields_v01.json").read_text())
    result = json.loads((DATA / "ngc3627_phangs_tracer_velocity_field_rank_test_v01.json").read_text())
    assert source["status"] == "SOURCE_NATIVE_2D_TRACER_VELOCITY_FIELDS_ACQUIRED"
    assert source["source_side_selection"]["role"].startswith("independent")
    assert result["galaxy"] == "NGC3627"
    assert result["morphology_control"] == "barred_interacting_disturbed"
    assert result["beam_independent_pixels"] > 3000
    assert result["sector_jackknife_max_absolute_mode_z"] < 3.0
    assert result["construction_uses_rotation_residual"] is False
    assert result["time_channel_identified"] is False
    assert result["quantum_channel_identified"] is False


def test_ngc4535_phangs_morphology_orthogonal_replication():
    source = json.loads((DATA / "ngc4535_phangs_tracer_velocity_fields_v01.json").read_text())
    result = json.loads((DATA / "ngc4535_phangs_tracer_velocity_field_rank_test_v01.json").read_text())
    assert source["status"] == "SOURCE_NATIVE_2D_TRACER_VELOCITY_FIELDS_ACQUIRED"
    assert source["source_side_selection"]["role"].startswith("independent barred")
    assert result["morphology_control"] == "barred_spiral_no_prefrozen_m1_nuisance"
    assert result["beam_independent_pixels"] > 1500
    assert result["sector_jackknife_max_absolute_mode_z"] < 3.0
    assert result["construction_uses_rotation_residual"] is False
    assert result["time_channel_identified"] is False
    assert result["quantum_channel_identified"] is False


def test_phangs_morphology_orthogonal_tracer_field_test():
    result = json.loads((DATA / "phangs_morphology_orthogonal_tracer_field_test_v01.json").read_text())
    assert result["status"] == "ELIGIBLE_THREE_GALAXY_MORPHOLOGY_ORTHOGONAL_NULL_REPLICATED"
    assert result["matched_orthogonal_p"] > 0.1
    assert result["wrong_family_residual_p"] > 0.1
    assert result["shared_universal_angular_mode_identifiable"] is False
    ngc3627 = next(row for row in result["galaxies"] if row["galaxy"] == "NGC3627")
    assert ngc3627["low_order_orthogonal_mode_identifiable"] is False
    assert ngc3627["contributes_to_common_orthogonal_test"] is False
    assert result["ngc3627_replication_verdict"].startswith("NEGATIVE_RESULT_PRESERVED")
    ngc4535 = next(row for row in result["galaxies"] if row["galaxy"] == "NGC4535")
    assert ngc4535["low_order_orthogonal_mode_identifiable"] is True
    assert ngc4535["matched_orthogonal_p"] > 0.1
    assert result["ngc4535_replication_verdict"].startswith("NEGATIVE_RESULT_PRESERVED")


def test_phangs_population_channel_preregistration_boundary():
    result = json.loads((DATA / "phangs_population_channel_preregistration_v01.json").read_text())
    frame = pd.read_csv(DATA / "phangs_population_channel_preregistration_v01.csv")
    assert result["status"] == "SOURCE_FROZEN_POPULATION_TEST_PREREGISTERED_ENDPOINTS_CLOSED"
    assert result["population_size"] == 19
    assert result["eligible_galaxies"] == ["IC5332", "NGC4254", "NGC4321"]
    assert result["legacy_open_pilots"] == ["NGC4254"]
    assert result["confirmatory_unopened_galaxies"] == ["IC5332", "NGC4321"]
    assert result["endpoint_opened"] is False
    assert result["construction_uses_tracer_contrast"] is False
    assert result["construction_uses_rotation_residual"] is False
    eligible = frame[frame.population_test_eligible]
    assert set(eligible.nuisance_modes) == {"m0+m1"}
    assert set(eligible.retained_test_mode) == {"m2"}


def test_phangs_confirmatory_population_sources_and_rank_outputs():
    for galaxy, slug in (("IC5332", "ic5332"), ("NGC4321", "ngc4321")):
        source = json.loads((DATA / f"{slug}_phangs_tracer_velocity_fields_v01.json").read_text())
        rank = json.loads((DATA / f"{slug}_phangs_tracer_velocity_field_rank_test_v01.json").read_text())
        assert source["source_side_selection"]["role"] == "preregistered confirmatory population endpoint"
        assert rank["galaxy"] == galaxy
        assert rank["beam_independent_pixels"] >= 50
        assert rank["construction_uses_rotation_residual"] is False
        assert rank["time_channel_identified"] is False
        assert rank["quantum_channel_identified"] is False


def test_phangs_population_label_audit_demotes_numerical_pass():
    labels = json.loads((DATA / "phangs_population_morphology_label_audit_v01.json").read_text())
    result = json.loads((DATA / "phangs_population_channel_test_v01.json").read_text())
    ngc4321 = next(row for row in labels["rows"] if row["galaxy"] == "NGC4321")
    ic5332 = next(row for row in labels["rows"] if row["galaxy"] == "IC5332")
    assert labels["confirmatory_label_integrity_pass"] is False
    assert labels["replacement_endpoint_allowed"] is False
    assert ngc4321["verdict"] == "NONBARRED_LABEL_CONTRADICTED"
    assert ngc4321["phangs_co_bar_class"] == "C"
    assert ic5332["verdict"] == "BAR_ABSENCE_NOT_PROVED"
    assert result["numerical_gate_passed"] is True
    assert result["confirmatory_morphology_label_integrity_pass"] is False
    assert result["promotion_gate_passed"] is False
    assert result["body_increment_score_open_allowed"] is False
    assert result["global_retained_m2_p"] < 0.01
    assert all(row["retained_m2_p"] < 0.05 for row in result["confirmatory_galaxies"])
    assert result["global_wrong_family_m1_p"] < 0.01
    assert result["time_channel_identified"] is False
    assert result["quantum_channel_identified"] is False
    assert result["construction_uses_rotation_residual"] is False


def test_phangs_source_certified_nuisance_atlas_closes_low_order_lane():
    m1 = json.loads((DATA / "phangs_radial_m1_source_coverage_v01.json").read_text())
    atlas = json.loads(
        (DATA / "phangs_source_certified_morphology_nuisance_atlas_v02.json").read_text()
    )
    frame = pd.read_csv(DATA / "phangs_source_certified_morphology_nuisance_atlas_v02.csv")
    assert m1["population_size"] == 19
    assert m1["catalog_match_count"] == 4
    assert m1["radial_m1_null_certified_count"] == 0
    assert atlas["status"] == "NO_UNTOUCHED_LOW_ORDER_ENDPOINT_AFTER_MULTI_SOURCE_NUISANCE_UNION"
    assert atlas["untouched_low_order_endpoint_count"] == 0
    assert atlas["m2_clean_source_certified_bodies"] == ["NGC4254"]
    assert set(atlas["cross_tracer_bar_conflicts"]) == {"NGC1385", "NGC5068"}
    assert not frame.untouched_endpoint_eligible.any()
    assert not frame.m1_clean_source_certified.any()
    assert atlas["construction_uses_velocity_contrast"] is False
    assert atlas["construction_uses_rotation_residual"] is False


def test_phangs_radial_body_projection_preregistration_is_unopened():
    result = json.loads(
        (DATA / "phangs_radial_body_projection_preregistration_v01.json").read_text()
    )
    frame = pd.read_csv(DATA / "phangs_radial_body_projection_preregistration_v01.csv")
    assert result["status"] == "HIGHER_DIMENSIONAL_BODY_PROJECTION_ENDPOINTS_FROZEN_UNOPENED"
    assert result["confirmatory_untouched"] == ["NGC1300", "NGC1385", "NGC1512", "NGC5068"]
    assert len(result["pipeline_development_no_claim"]) == 6
    assert result["radial_zones"] == 5
    assert "dimension 20" in result["terminal_vector"]
    assert "20-by-at-most-8" in result["body_nuisance_matrix"]
    assert result["endpoint_opened"] is False
    assert result["construction_uses_velocity_contrast"] is False
    assert result["construction_uses_rotation_residual"] is False
    assert not frame.velocity_contrast_opened.any()


def test_dark_discrepancy_is_primary_endpoint_not_tracer_contrast():
    result = json.loads((DATA / "dark_discrepancy_primary_endpoint_gate_v01.json").read_text())
    assert result["primary_target"].startswith("Delta_DM")
    assert "nuisance calibration" in result["tracer_contrast_role"]
    assert all(v["common_co_halpha_velocity_field"] for v in result["phangs_2d_readiness"].values())
    assert all(v["stellar_mass_surface_density_field"] for v in result["phangs_2d_readiness"].values())
    assert result["phangs_2d_readiness"]["NGC4254"]["atomic_hi_surface_density_field"] is True
    assert result["phangs_2d_readiness"]["NGC3351"]["atomic_hi_surface_density_field"] is False
    assert not any(v["dark_discrepancy_field_open_allowed"] for v in result["phangs_2d_readiness"].values())

    resolution = json.loads((DATA / "ngc4254_dark_discrepancy_2d_resolution_audit_v01.json").read_text())
    assert resolution["independent_hi_beams_in_common_support"] > 10
    assert resolution["independent_hi_beams_in_common_support"] < 25
    assert resolution["coarse_radial_profile_allowed"] is True
    assert resolution["five_zone_harmonic_model_allowed"] is False
    assert resolution["fine_scale_channel_claim_allowed"] is False

    baryons = json.loads((DATA / "ngc4254_baryonic_surface_density_fields_v01.json").read_text())
    assert baryons["n_radial_bins"] == 12
    assert baryons["gravity_field_solved"] is False

    discrepancy = json.loads((DATA / "ngc4254_radial_dark_discrepancy_v01.json").read_text())
    assert discrepancy["n_observed_radial_bins"] == 11
    assert discrepancy["outer_nominal_median_ratio"] > 1.0
    assert discrepancy["outer_all_models_ratio_range"][0] > 1.0
    assert discrepancy["two_dimensional_attribution_allowed"] is False
    assert discrepancy["tau_morphology_detected"] is False
    assert discrepancy["channel_detected"] is False

    kernel = json.loads((DATA / "ngc4254_dark_discrepancy_tau_kernel_score_v01.json").read_text())
    assert kernel["ngc4254_parameters_fitted"] is False
    assert kernel["nominal_rmse_km_s"]["tpg_v6"] < kernel["nominal_rmse_km_s"]["newton"]
    assert kernel["nominal_rmse_km_s"]["tpg_v6"] < kernel["nominal_rmse_km_s"]["mond"]
    assert kernel["model_win_counts"]["tpg_v6"] > kernel["model_win_counts"]["mond"]
    assert kernel["tau_kernel_origin_identified"] is False
    assert kernel["channel_origin_identified"] is False

    onset = json.loads((DATA / "ngc4254_dark_discrepancy_onset_v01.json").read_text())
    assert onset["target"].startswith("vobs^2-vbar^2")
    assert onset["q05_above_unity_onset_kpc"] > onset["nominal_sustained_onset_kpc"]
    assert abs(onset["robust_onset_minus_h2_hi_kpc"]) < 1.0
    assert onset["s4g_disk_break_inside_kinematic_coverage"] is False
    assert onset["tau_morphology_detected"] is False
    assert onset["channel_detected"] is False

    control = json.loads((DATA / "ngc7331_dark_discrepancy_onset_control_v01.json").read_text())
    assert control["target"].startswith("vobs^2-vbar^2")
    assert control["three_sigma_sustained_onset_kpc"] < control["source_frozen_warp_onset_kpc"]
    assert control["simple_universal_morphology_onset_alignment_supported"] is False
    assert control["tau_morphology_detected"] is False
    assert control["channel_detected"] is False

    interaction = json.loads((DATA / "dark_discrepancy_morphology_channel_interaction_v01.json").read_text())
    assert interaction["target"].startswith("log outer3 vobs^2/vbar^2")
    assert interaction["interaction_mse_reduction_vs_additive"] < 0
    assert interaction["interaction_information_candidate"] is False
    assert interaction["physical_channel_detected"] is False

    continuous = json.loads((DATA / "continuous_channel_dark_discrepancy_interaction_v01.json").read_text())
    assert continuous["target"].startswith("log outer3 vobs^2/vbar^2")
    assert continuous["interaction_mse_reduction"] < 0
    assert continuous["interaction_information_candidate"] is False
    assert continuous["physical_channel_detected"] is False

    multipath = json.loads((DATA / "sdp81_multipath_channel_source_audit_v01.json").read_text())
    assert multipath["preflight_band4"]["n_spectral_channels"] == 119
    assert multipath["published_endpoint_band6"]["line"] == "CO(8-7)"
    assert multipath["published_endpoint_band6"]["n_spectral_channels"] == 100
    assert "not the published CO(8-7)" in multipath["lens_registration_band7"]["line_in_archive"]
    assert multipath["same_source_multiple_null_paths"] is True
    assert multipath["pathwise_comparison_allowed"] is False
    assert "lens operator" in multipath["blocker"]

    lens = json.loads((DATA / "sdp81_lens_operator_freeze_v01.json").read_text())
    assert lens["status"] == "PARAMETERS_FROZEN_IMAGE_G_WCS_REGISTRATION_OPEN"
    assert len(lens["models"]) == 3
    assert lens["models"]["inoue_best_fit"]["axis_ratio_q"] == 0.83
    assert len(lens["promotion_gates"]) == 4

    geometry = json.loads(
        (DATA / "sdp81_lens_operator_geometry_validation_v01.json").read_text()
    )
    assert geometry["image_multiplicities"] == {"q1": 4, "d1": 2, "d2": 2}
    assert geometry["multiplicity_pass"] is True
    assert geometry["published_configuration_pass"] is True
    assert geometry["image_G_wcs_registration_complete"] is False
    assert geometry["pathwise_cube_comparison_allowed"] is False

    score = json.loads((DATA / "sdp81_q1_multipath_spectral_score_v01.json").read_text())
    assert score["path_count"] == 4
    assert score["n_sensitivity_runs"] == 36
    assert score["rolling_six_channel_positive_flux_windows"] > 5
    assert 0 <= score["published_endpoint_empirical_upper_tail_fraction"] <= 1
    assert score["physical_significance_computed"] is False
    assert score["channel_origin_identified"] is False

    selection = json.loads(
        (DATA / "joint_readout_body_dominant_baseline_selection_v01.json").read_text()
    )
    assert selection["independent_test_family_count"] == 5
    assert selection["no_positive_channel_test"] is True
    assert selection["nonconventional_channel_default"] == "Delta_Oc = 0"

    body = json.loads((DATA / "body_only_newtonian_kernel_score_v01.json").read_text())
    assert body["nonconventional_channel_parameters"] == 0
    assert body["tpg_used_in_fit_or_prediction"] is False
    assert body["n_holdout_galaxies"] > 30
    assert 0 <= body["matched_vs_wrong"]["shuffle_p_mean_delta"] <= 1

    freeze = json.loads((DATA / "body_amplitude_law_freeze_v01.json").read_text())
    assert freeze["uses_vobs_or_residual"] is False
    assert freeze["channel_coordinates"] == []
    amplitude = json.loads((DATA / "body_amplitude_law_score_v01.json").read_text())
    assert amplitude["n_holdout_galaxies"] == body["n_holdout_galaxies"]
    assert amplitude["selected_ridge_alpha_train_cv"] in freeze["ridge_alpha_grid"]

    local_freeze = json.loads(
        (DATA / "local_kernel_invariant_response_freeze_v01.json").read_text()
    )
    assert local_freeze["uses_vobs_or_residual"] is False
    local = json.loads((DATA / "local_kernel_invariant_response_score_v01.json").read_text())
    assert local["channel_coordinates_used"] == []
    assert local["n_holdout_galaxies"] == body["n_holdout_galaxies"]

    shape_freeze = json.loads((DATA / "local_kernel_shape_response_freeze_v01.json").read_text())
    assert shape_freeze["uses_vobs_or_residual"] is False
    shape = json.loads((DATA / "local_kernel_shape_response_score_v01.json").read_text())
    assert shape["channel_coordinates_used"] == []
    assert shape["n_holdout_galaxies"] == body["n_holdout_galaxies"]

    failure_channel = json.loads(
        (DATA / "body_failure_channel_stratification_v01.json").read_text()
    )
    assert failure_channel["n_body_failures"] + failure_channel["n_body_successes"] == failure_channel["n_overlap_holdout"]
    assert failure_channel["physical_channel_detected"] is False

    signed_freeze = json.loads(
        (DATA / "signed_kernel_transition_response_freeze_v01.json").read_text()
    )
    assert signed_freeze["uses_vobs_or_residual"] is False
    signed = json.loads((DATA / "signed_kernel_transition_response_score_v01.json").read_text())
    assert signed["channel_coordinates_used"] == []
    assert signed["n_holdout_galaxies"] == body["n_holdout_galaxies"]

    onset_freeze = json.loads(
        (DATA / "kernel_curvature_onset_response_freeze_v01.json").read_text()
    )
    assert onset_freeze["uses_vobs_or_residual"] is False
    onset = json.loads((DATA / "kernel_curvature_onset_response_score_v01.json").read_text())
    assert onset["channel_coordinates_used"] == []
    assert onset["n_holdout_galaxies"] == body["n_holdout_galaxies"]

    bc_freeze = json.loads((DATA / "body_conditioned_bounded_channel_freeze_v01.json").read_text())
    assert bc_freeze["uses_vobs_or_residual"] is False
    assert "not OSCC" in bc_freeze["capacity_claim"]
    bc = json.loads((DATA / "body_conditioned_bounded_channel_score_v01.json").read_text())
    assert bc["physical_capacity_measured"] is False
    assert bc["physical_channel_detected"] is False

    atlas = json.loads((DATA / "body_success_morphology_channel_atlas_v01.json").read_text())
    assert sum(atlas["counts"].values()) == body["n_holdout_galaxies"]
    assert atlas["physical_channel_detected"] is False
    assert atlas["retuning_allowed"] is False

    readiness = json.loads((DATA / "body_failure_source_readiness_v01.json").read_text())
    assert readiness["n_failures"] == atlas["counts"]["body_failure"]
    assert readiness["n_refined_source_ready"] == 0
    assert readiness["rescoring_allowed"] is False

    p0_review = json.loads(
        (DATA / "p0_body_failure_source_reclassification_review_v01.json").read_text()
    )
    assert p0_review["n_p0"] == 4
    assert p0_review["n_high_pressure"] == 4
    assert p0_review["inspected_holdout_rescoring_allowed"] is False

    alias_audit = json.loads(
        (DATA / "little_things_alias_independence_audit_v01.json").read_text()
    )
    assert alias_audit["ddo50_ugc04305_overlap_confirmed"] is True
    assert alias_audit["n_missed_by_exact_name"] >= 1

    corrected = json.loads(
        (DATA / "little_things_alias_corrected_kernel_score_v01.json").read_text()
    )
    assert "DDO_50" in corrected["excluded_alias_overlaps"]
    assert corrected["prospective_claim_allowed"] is False

    prereg = json.loads(
        (DATA / "refined_body_subfamily_preregistration_v01.json").read_text()
    )
    assert prereg["status"] == "SOURCE_ACQUISITION_ONLY"
    assert prereg["construction_uses_vobs_or_rotation_residual"] is False
    assert prereg["inspected_motivating_objects_endpoint_eligible"] is False
    assert prereg["alias_resolution_required_before_sample_freeze"] is True
    assert prereg["minimum_independent_galaxies_per_family"] >= 5
    assert len(prereg["families"]) == 4
    assert prereg["endpoint_scoring_allowed"] is False
    assert prereg["channel_handoff_rule"].startswith("fit no nonconventional channel")

    cohort = json.loads((DATA / "refined_body_source_cohort_v01.json").read_text())
    assert cohort["n_nominated"] == 20
    assert len(cohort["family_counts"]) == 4
    assert all(row["nominated"] == 5 for row in cohort["family_counts"].values())
    assert cohort["source_fields_complete"] is False
    assert cohort["endpoint_scoring_allowed"] is False

    bars = json.loads((DATA / "coming_bar_source_fields_v01.json").read_text())
    assert bars["n_galaxies"] == 5
    assert bars["n_classification_source_supported"] == 5
    assert bars["n_active_zones_frozen"] == 5
    assert bars["n_source_fields_complete"] == 0
    assert bars["construction_uses_vobs_or_dark_discrepancy_residual"] is False
    assert bars["endpoint_scoring_allowed"] is False

    vector_source = json.loads(
        (DATA / "coming_vector_profile_source_audit_v01.json").read_text()
    )
    assert vector_source["journal_doi"] == "10.1093/pasj/psz004"
    assert vector_source["numeric_profile_table_present"] is False
    assert vector_source["required_vector_files_complete"] is True
    assert vector_source["uses_dark_discrepancy_endpoint"] is False
    assert vector_source["profile_values_frozen"] is False
    assert vector_source["endpoint_scoring_allowed"] is False

    markers = json.loads((DATA / "coming_vector_marker_centers_v01.json").read_text())
    assert markers["n_galaxies"] == 5
    assert markers["n_markers"] == 57
    assert markers["marker_count_gate_pass"] is True
    assert markers["marker_counts"]["NGC 613"] == 13
    assert markers["delta_axis_calibrated"] is True
    assert markers["ngc4579_clipped_outlier_restored_as_separate_point"] is True
    assert markers["physical_delta_amplitudes_frozen"] is True
    assert markers["radial_r_over_abar_calibrated"] is True
    assert markers["central_value_profiles_frozen"] is True
    assert markers["n_points_with_vector_errors"] == 56
    assert markers["physical_profiles_frozen"] is False
    assert markers["uses_dark_discrepancy_endpoint"] is False
    assert markers["endpoint_scoring_allowed"] is False

    reverse = json.loads(
        (DATA / "coming_profile_reverse_render_validation_v01.json").read_text()
    )
    assert reverse["n_visible_points"] == 56
    assert reverse["visible_marker_roundtrip_pass"] is True
    assert reverse["visible_error_roundtrip_pass"] is True
    assert reverse["clipped_ngc4579_outlier_present"] is True
    assert reverse["clipped_ngc4579_outlier_uncertainty_available"] is False
    assert reverse["source_profile_gate_complete"] is False
    assert reverse["endpoint_scoring_allowed"] is False

    bar_completion = json.loads(
        (DATA / "coming_bar_family_completion_v01.json").read_text()
    )
    assert bar_completion["n_candidates"] == 5
    scale = json.loads((DATA / "ngc5248_bar_scale_resolution_v01.json").read_text())
    assert scale["selection_uses_rotation_endpoint_or_dark_discrepancy"] is False
    assert scale["post_score_scale_switch_allowed"] is False
    assert scale["source_scale_resolved_for_primary_protocol"] is True
    assert bar_completion["n_source_ready"] == 5
    assert bar_completion["blocked_galaxies"] == []
    assert bar_completion["ngc4579_outlier_policy_source_frozen"] is True
    assert bar_completion["minimum_five_ready_met"] is True
    assert bar_completion["family_source_gate_complete"] is True
    assert bar_completion["endpoint_scoring_allowed"] is False

    endpoint_ready = json.loads(
        (DATA / "coming_bar_endpoint_readiness_v01.json").read_text()
    )
    assert endpoint_ready["n_galaxies"] == 5
    assert endpoint_ready["n_independent_rotation_acquired"] >= 1
    assert endpoint_ready["primary_acquisition_target"] == "NGC 7479"
    assert endpoint_ready["primary_target_halpha_points"] == 99
    assert endpoint_ready["coming_co_reuse_as_endpoint_allowed"] is False
    assert endpoint_ready["n_dark_discrepancy_endpoint_ready"] == 0
    assert endpoint_ready["endpoint_scoring_allowed"] is False

    ngc7479_hi = json.loads((DATA / "ngc7479_hi_endpoint_source_v01.json").read_text())
    assert ngc7479_hi["n_rotation_points"] == 10
    assert ngc7479_hi["independent_of_coming_co_morphology"] is True
    assert ngc7479_hi["hi_moment0_map_published"] is True
    assert ngc7479_hi["numeric_radial_hi_surface_density_profile_published"] is False
    assert ngc7479_hi["stellar_ml_1p35_route_endpoint_calibrated_and_primary_forbidden"] is True
    assert ngc7479_hi["dark_discrepancy_ready"] is False
    assert ngc7479_hi["endpoint_scoring_allowed"] is False

    stellar = json.loads((DATA / "ngc7479_stellar_velocity_field_v01.json").read_text())
    assert abs(stellar["s4g_fraction_sum"] - 1.001) < 1e-9
    assert stellar["uses_rotation_endpoint_or_dark_discrepancy_in_construction"] is False
    assert stellar["stellar_velocity_field_ready"] is True
    assert stellar["gas_velocity_field_ready"] is False
    assert stellar["baryonic_velocity_field_ready"] is False
    assert stellar["endpoint_scoring_allowed"] is False

    gas_proxy = json.loads((DATA / "ngc7479_hi_radial_proxy_v01.json").read_text())
    assert gas_proxy["image_shape"] == [207, 174]
    assert gas_proxy["uses_rotation_endpoint_or_dark_discrepancy"] is False
    assert gas_proxy["mass_conservation_relative_error_max"] < 1e-6
    assert gas_proxy["strict_radial_gas_profile_ready"] is False
    assert gas_proxy["diagnostic_gas_profile_ready"] is True
    assert gas_proxy["endpoint_scoring_allowed"] is False

    diagnostic_score = json.loads((DATA / "ngc7479_diagnostic_bar_scoring_v01.json").read_text())
    assert diagnostic_score["fitted_parameters"] == 0
    assert diagnostic_score["uses_endpoint_to_select_morphology_scale_or_amplitude"] is False
    assert diagnostic_score["n_endpoint_points"] == 10
    assert diagnostic_score["n_gas_sensitivities"] == 3
    assert diagnostic_score["strict_physical_score_allowed"] is False
    assert diagnostic_score["tau_morphology_detected"] is False
    assert diagnostic_score["channel_detected"] is False

    cumulative = json.loads(
        (DATA / "ngc7479_cumulative_morphology_scoring_v01.json").read_text()
    )
    assert cumulative["fitted_parameters"] == 0
    assert cumulative["n_endpoint_points"] == 10
    assert cumulative["n_gas_sensitivities"] == 3
    assert cumulative["prospective"] is False
    assert cumulative["strict_physical_score_allowed"] is False
    assert cumulative["tau_morphology_detected"] is False
    assert cumulative["channel_detected"] is False

    reliability_capacity = json.loads(
        (DATA / "ngc7479_reliability_capacity_scoring_v01.json").read_text()
    )
    assert reliability_capacity["fitted_parameters"] == 0
    assert reliability_capacity["n_endpoint_points"] == 10
    assert reliability_capacity["n_gas_sensitivities"] == 3
    assert reliability_capacity["prospective"] is False
    assert reliability_capacity["strict_physical_score_allowed"] is False
    assert reliability_capacity["tau_morphology_detected"] is False
    assert reliability_capacity["channel_detected"] is False

    inflow_capacity = json.loads(
        (DATA / "ngc7479_inflow_limited_capacity_scoring_v01.json").read_text()
    )
    assert inflow_capacity["fitted_parameters"] == 0
    assert inflow_capacity["n_endpoint_points"] == 10
    assert inflow_capacity["n_gas_sensitivities"] == 3
    assert all(0.0 <= c <= 1.0 for c in inflow_capacity["source_capacities"].values())
    assert inflow_capacity["prospective"] is False
    assert inflow_capacity["strict_physical_score_allowed"] is False
    assert inflow_capacity["tau_morphology_detected"] is False
    assert inflow_capacity["channel_detected"] is False

    modal_capacity = json.loads(
        (DATA / "ngc7479_modal_capacity_scoring_v01.json").read_text()
    )
    assert modal_capacity["fitted_endpoint_parameters"] == 0
    assert modal_capacity["basis_order"] == 2
    assert modal_capacity["n_endpoint_points"] == 10
    assert modal_capacity["n_gas_sensitivities"] == 3
    for source in modal_capacity["source_mode_diagnostics"].values():
        assert len(source["modal_capacities"]) == 3
        assert all(0.0 <= c <= 1.0 for c in source["modal_capacities"])
        assert 0.0 <= source["total_capacity"] <= 1.0
    assert modal_capacity["prospective"] is False
    assert modal_capacity["strict_physical_score_allowed"] is False
    assert modal_capacity["tau_morphology_detected"] is False
    assert modal_capacity["channel_detected"] is False

    multicoordinate = json.loads(
        (DATA / "coming_multicoordinate_source_descriptor_v01.json").read_text()
    )
    assert multicoordinate["n_galaxies"] == 5
    assert multicoordinate["n_core_descriptor_complete"] == 5
    assert multicoordinate["construction_uses_rotation_endpoint_or_dark_discrepancy"] is False
    assert multicoordinate["formula_scoring_allowed"] is False

    ngc4303_intake = json.loads(
        (DATA / "ngc4303_prospective_endpoint_intake_freeze_v01.json").read_text()
    )
    assert ngc4303_intake["selection_reads_ngc4303_rotation_values"] is False
    assert ngc4303_intake["selection_reads_ngc4303_dark_discrepancy"] is False
    assert ngc4303_intake["endpoint_values_opened"] is False
    assert ngc4303_intake["scoring_allowed"] is False

    ngc4303_endpoint = json.loads(
        (DATA / "ngc4303_phangs_rotation_endpoint_v01.json").read_text()
    )
    assert ngc4303_endpoint["n_points"] == 43
    assert ngc4303_endpoint["paper_unreliable_fit_marker"] is False
    assert ngc4303_endpoint["strictly_independent_tracer_from_coming"] is False
    assert ngc4303_endpoint["endpoint_values_now_open"] is True
    assert ngc4303_endpoint["new_operator_selection_on_ngc4303_allowed"] is False
    assert ngc4303_endpoint["strict_endpoint_scoring_allowed"] is False

    ngc4579_freeze = json.loads(
        (DATA / "ngc4579_halpha_prospective_replication_freeze_v01.json").read_text()
    )
    assert ngc4579_freeze["target_selection_reads_halpha_rotation_values"] is False
    assert ngc4579_freeze["prefrozen_operator"]["frozen_before_halpha_endpoint_open"] is True
    assert ngc4579_freeze["halpha_endpoint_values_opened"] is False
    assert ngc4579_freeze["scoring_allowed"] is False

    ngc4579_access = json.loads(
        (DATA / "ngc4579_halpha_source_access_audit_v01.json").read_text()
    )
    assert ngc4579_access["ngc4579_in_published_sample"] is True
    assert ngc4579_access["ngc4303_in_published_sample"] is False
    assert ngc4579_access["halpha_rotation_values_opened"] is True
    assert ngc4579_access["prospective_status_preserved"] is True
    assert ngc4579_access["scoring_allowed"] is False

    ngc4579_endpoint = json.loads(
        (DATA / "ngc4579_halpha_pv_endpoint_v01.json").read_text()
    )
    assert ngc4579_endpoint["both_sides_quality_gate_pass"] is False
    assert ngc4579_endpoint["post_bar_side_counts"].get("receding", 0) == 0
    assert ngc4579_endpoint["reverse_render_visual_acceptance"] is False
    assert ngc4579_endpoint["scoring_allowed"] is False

    ngc4579_numeric = json.loads(
        (DATA / "ngc4579_sings_halpha_modal_capacity_replay_v01.json").read_text()
    )
    assert ngc4579_numeric["fitted_endpoint_parameters"] == 0
    assert ngc4579_numeric["n_source_points"] == 35
    assert ngc4579_numeric["n_post_bar_points"] == 20
    assert ngc4579_numeric["source_sides_individually_available"] is False
    assert ngc4579_numeric["side_disagreement_retained_in_source_final_error"] is True
    assert ngc4579_numeric["all_matched_beat_newton"] is True
    assert ngc4579_numeric["all_matched_beat_wrong_mean"] is True
    assert ngc4579_numeric["all_matched_beat_best_wrong"] is True
    assert ngc4579_numeric["physical_channel_detected"] is False

    ngc4579_gap = json.loads(
        (DATA / "ngc4579_morphology_amplitude_shape_gap_v01.json").read_text()
    )
    assert ngc4579_gap["source_support_counts"] == {"inside": 12, "beyond": 8}
    assert ngc4579_gap["median_q_response_fraction"][1] < 0.25
    assert ngc4579_gap["post_open_scale_only_factor"][0] > 4.0
    assert ngc4579_gap["new_formula_selection_allowed"] is False
    assert ngc4579_gap["physical_channel_detected"] is False

    ngc4579_side_search = json.loads(
        (DATA / "ngc4579_side_resolved_halpha_source_search_v01.json").read_text()
    )
    assert ngc4579_side_search["even_common_amplitude_test_available"] is True
    assert ngc4579_side_search["orientation_odd_time_channel_test_available"] is False
    assert ngc4579_side_search["page_links_fits_or_cube"] is False

    ngc4579_side_gate = json.loads(
        (DATA / "ngc4579_sings_side_resolved_gate_v01.json").read_text()
    )
    assert ngc4579_side_gate["figure_c2_visual_series_count"] == 1
    assert ngc4579_side_gate["n_side_error_dominates_formal_error"] == 19
    assert ngc4579_side_gate["side_values_algebraically_reconstructed"] is False
    assert ngc4579_side_gate["signed_orientation_odd_information_available"] is False
    assert ngc4579_side_gate["odd_channel_scoring_allowed"] is False

    ugc08490_oriented = json.loads(
        (DATA / "ugc08490_oriented_channel_compatibility_v01.json").read_text()
    )
    assert ugc08490_oriented["fitted_parameters"] == 0
    assert ugc08490_oriented["n_common_radii"] == 7
    assert ugc08490_oriented["side_compatibility"]["chi2_per_point"] > 4.0
    assert abs(ugc08490_oriented["side_compatibility"]["weighted_mean_difference_z"]) < 2.0
    assert ugc08490_oriented["common_oriented_load_compatible_with_both_sides"] is False
    assert ugc08490_oriented["physical_channel_detected"] is False

    ugc08490_covariance = json.loads(
        (DATA / "ugc08490_oriented_channel_covariance_audit_v02.json").read_text()
    )
    assert ugc08490_covariance["covariance_rank"] == 7
    assert ugc08490_covariance["gls_side_compatibility"]["chi2_per_effective_dof"] > 5.0
    assert ugc08490_covariance["leave_one_radius_out"]["minimum_chi2_per_effective_dof"] > 4.0
    assert ugc08490_covariance["common_reciprocal_load_compatible"] is False
    assert ugc08490_covariance["physical_channel_detected"] is False

    ugc08490_warp = json.loads(
        (DATA / "ugc08490_ngc5204_warp_body_v01.json").read_text()
    )
    assert ugc08490_warp["n_tilted_rings"] == 24
    assert ugc08490_warp["warp_onset"]["radius_kpc_source"] == 3.13
    assert ugc08490_warp["ghasp_preflight_overlaps_warp_onset"] is False
    assert ugc08490_warp["outer_warp_can_explain_current_inner_side_incompatibility"] is False
    assert ugc08490_warp["endpoint_values_used_for_body_construction"] is False
    assert ugc08490_warp["same_tracer_inner_context"]["independent_body_coordinate"] is False
    assert ugc08490_warp["same_tracer_inner_context"]["central_ring_radius_arcsec_approx"] == 30.0

    ugc07323_body = json.loads((DATA / "ugc07323_ngc4242_body_freeze_v01.json").read_text())
    assert ugc07323_body["radial_window_freeze_allowed"] is False
    assert ugc07323_body["body_conditioned_side_function_allowed"] is False

    ugc07323_oriented = json.loads(
        (DATA / "ugc07323_oriented_channel_compatibility_v01.json").read_text()
    )
    assert ugc07323_oriented["fitted_parameters"] == 0
    assert ugc07323_oriented["n_common_radii"] == 8
    assert ugc07323_oriented["common_oriented_load_compatible_with_both_sides"] is False

    ugc07323_covariance = json.loads(
        (DATA / "ugc07323_oriented_channel_covariance_audit_v02.json").read_text()
    )
    assert ugc07323_covariance["gls_side_compatibility"]["chi2_per_effective_dof"] > 4.5
    assert ugc07323_covariance["leave_one_radius_out"]["minimum_chi2_per_effective_dof"] > 3.9
    assert ugc07323_covariance["common_reciprocal_load_compatible"] is False
    assert ugc07323_covariance["physical_channel_detected"] is False

    ngc4579_stellar = json.loads(
        (DATA / "ngc4579_stellar_velocity_field_v01.json").read_text()
    )
    assert abs(sum(ngc4579_stellar["s4g_component_fractions"].values()) - 1.0) < 1e-12
    assert ngc4579_stellar["construction_uses_halpha_endpoint_or_dark_discrepancy"] is False
    assert ngc4579_stellar["stellar_field_ready"] is True
    assert ngc4579_stellar["gas_field_ready"] is False
    assert ngc4579_stellar["baryonic_field_ready"] is False
    assert ngc4579_stellar["scoring_allowed"] is False

    ngc4579_hi = json.loads((DATA / "ngc4579_viva_hi_gravity_v01.json").read_text())
    assert ngc4579_hi["uses_spherical_enclosed_mass_proxy"] is False
    assert ngc4579_hi["inner_outward_ring_force_preserved"] is True
    assert ngc4579_hi["construction_uses_halpha_endpoint_or_dark_discrepancy"] is False
    assert ngc4579_hi["hi_gravity_ready"] is True
    assert ngc4579_hi["combined_gas_gravity_ready"] is False
    assert ngc4579_hi["scoring_allowed"] is False

    ngc4579_baryonic = json.loads(
        (DATA / "ngc4579_combined_baryonic_field_v01.json").read_text()
    )
    primary_mass = ngc4579_baryonic["molecular_plus_helium_mass_msun"]["alpha_4.35"]
    reference_mass = ngc4579_baryonic["published_reference_molecular_plus_helium_mass_msun"]
    assert abs(primary_mass / reference_mass - 1.0) < 0.01
    assert ngc4579_baryonic["construction_uses_halpha_endpoint_or_dark_discrepancy"] is False
    assert ngc4579_baryonic["combined_baryonic_field_ready"] is True
    assert ngc4579_baryonic["halpha_endpoint_ready"] is False
    assert ngc4579_baryonic["scoring_allowed"] is False


def test_tpg_v6_motivation_ablation():
    result = json.loads((DATA / "tpg_v6_motivation_ablation.json").read_text())
    selected = result["generalized_dtl_train_selected"]
    assert selected["gamma"] == 1.0
    assert selected["beta"] == 1.0
    assert abs(result["cosmology_alpha_holdout_delta_km_s"]) < 0.05
    assert result["alpha_status"].startswith("SPARC-calibrated")


def test_common_mode_multitracer_source_audit_is_preflight_only():
    result = json.loads(
        (DATA / "common_mode_multitracer_source_audit_v01.json").read_text()
    )
    assert result["primary_candidate"] == "NGC4254"
    assert result["replication_candidate"] == "NGC3351"
    assert len(result["records"]) == 2
    assert all(row["absolute_reconstruction_possible"] for row in result["records"])
    assert not any(row["spectral_frames_match"] for row in result["records"])
    assert all(row["frame_transform_frozen"] for row in result["records"])
    assert not any(row["cross_tracer_common_mode_ready"] for row in result["records"])
    assert not any(row["endpoint_scored"] for row in result["records"])
    assert len(result["freeze_before_scoring"]) == 8

    freeze = json.loads((DATA / "ngc4254_common_mode_geometry_freeze_v01.json").read_text())
    assert freeze["velocity_pixels_read_during_freeze"] is False
    assert freeze["spectral_transport"]["empirical_intertracer_offset_allowed"] is False

    score = json.loads((DATA / "ngc4254_common_mode_multitracer_v01.json").read_text())
    assert score["n_radial_contrasts"] == 5
    assert score["tracer_agreement_p"] < 1e-5
    assert score["standard_physical_baseline_complete"] is False
    assert score["common_channel_detected"] is False
    assert score["effective_time_readout_detected"] is False

    scales = json.loads(
        (DATA / "ngc4254_common_mode_conventional_scales_v02.json").read_text()
    )
    assert scales["combined_relativistic_order_scale_km_s"] < 0.05
    assert scales["observed_co_halpha_difference_km_s"]["minimum"] > 3.8
    assert scales["relativistic_scale_can_explain_tracer_difference"] is False
    assert scales["asymmetric_drift_closed"] is False
    assert scales["common_channel_detected"] is False

    linewidth = json.loads(
        (DATA / "ngc4254_linewidth_tracer_difference_v03.json").read_text()
    )
    assert linewidth["co_linewidth_data_blocker_removed"] is True
    assert linewidth["n_nonreference_annuli"] == 5
    assert linewidth["pressure_support_correction_derived"] is False
    assert linewidth["common_channel_detected"] is False

    gas = json.loads((DATA / "ngc4254_common_mode_gas_dynamics_v04.json").read_text())
    assert gas["sectors"]["axisymmetric_m0"]["p"] > 0.05
    assert gas["sectors"]["combined_nonaxisymmetric_m1_m2"]["p"] < 0.01
    assert gas["nonaxisymmetric_tracer_structure_detected"] is True
    assert gas["gas_dynamics_fully_explains_common_mode"] is False
    assert gas["common_channel_remainder_identified"] is False

    remainder = json.loads(
        (DATA / "ngc4254_cross_wedge_gasdynamics_remainder_v05.json").read_text()
    )
    assert remainder["spatial_holdout_nuisance_prediction"] is True
    assert remainder["endpoint_independent_source_body_prediction"] is False
    assert remainder["maximum_absolute_residual_km_s"] > 4.5
    assert remainder["common_channel_remainder_identified"] is False

    geometry = json.loads(
        (DATA / "ngc4254_cross_wedge_geometry_sensitivity_v06.json").read_text()
    )
    assert geometry["maximum_absolute_residual_range_km_s"][0] < 1.8
    assert geometry["maximum_absolute_residual_range_km_s"][1] > 7.5
    assert geometry["all_formal_residual_tests_p_below_0_01"] is False
    assert geometry["common_channel_remainder_identified"] is False

    replication_freeze = json.loads(
        (DATA / "ngc3351_common_mode_geometry_freeze_v01.json").read_text()
    )
    assert replication_freeze["velocity_pixels_read_during_freeze"] is False
    assert replication_freeze["replication_settings_changed_after_ngc4254"] is False
    replication = json.loads((DATA / "ngc3351_common_mode_multitracer_v01.json").read_text())
    assert replication["n_radial_contrasts"] == 2
    assert replication["common_zero_p"] > 0.05
    assert replication["tracer_agreement_p"] < 0.01
    assert replication["common_channel_detected"] is False

    optical = json.loads((DATA / "ngc4254_optical_line_common_mode_v07.json").read_text())
    assert optical["n_line_annulus_controls"] == 20
    assert optical["all_optical_vs_halpha_p"] < 1e-4
    assert optical["per_line_vs_halpha"]["HB4861"]["p"] > 0.99
    assert optical["per_line_vs_halpha"]["OIII5006"]["p"] < 1e-4
    assert optical["optical_line_common_mode_consistent"] is False
    assert optical["common_channel_detected"] is False

    multipath = json.loads((DATA / "sdp81_q1_multipath_centroid_v02.json").read_text())
    assert multipath["path_count"] == 4
    assert multipath["nominal"]["centroid_path_std_km_s"] > 8.0
    assert multipath["empirical_upper_tail_fraction"] > 0.6
    assert multipath["differential_magnification_line_shape_control_complete"] is False
    assert multipath["multipath_common_channel_detected"] is False

    matrix = json.loads((DATA / "common_channel_exclusion_matrix_v01.json").read_text())
    assert len(matrix["rows"]) == 5
    assert matrix["all_universal_scalar_gates_pass"] is False
    assert all(row["gate_pass"] is False for row in matrix["rows"])
    assert matrix["physical_channel_detected"] is False
    assert matrix["dark_matter_replacement_supported"] is False

    cross_transition_freeze = json.loads(
        (DATA / "sdp81_q1_cross_transition_rank_freeze_v01.json").read_text()
    )
    assert cross_transition_freeze["cube_flux_opened_during_freeze"] is False
    assert cross_transition_freeze["readouts"] == ["CO(5-4)", "CO(8-7)"]
    cross_transition = json.loads((DATA / "sdp81_q1_cross_transition_rank_v02.json").read_text())
    assert cross_transition["nominal"]["centered_path_cosine"] > 0.8
    assert cross_transition["two_sided_permutation_p"] == 1 / 24
    assert cross_transition["sign_stable_across_all_sensitivity_runs"] is True
    assert cross_transition["projected_cross_transition_rank_promoted"] is False
    assert cross_transition["mode_selective_channel_detected"] is False

    projected = json.loads((DATA / "sdp81_q1_projected_innovation_v03.json").read_text())
    assert projected["observed_is_most_rank_one_permutation"] is True
    assert projected["nominal"]["orthogonal_energy_fraction"] < 0.09
    assert projected["sensitivity_orthogonal_energy_fraction_range"][0] < 0.03
    assert projected["sensitivity_orthogonal_energy_fraction_range"][1] > 0.27
    assert projected["shared_parent_lens_mode_supported"] is True
    assert projected["projected_channel_innovation_detected"] is False


def test_alpha_0360_independence_audit():
    result = json.loads((DATA / "alpha_0360_independence_audit.json").read_text())
    external = result["little_things"]
    assert external["n_galaxies"] == 14
    assert external["canonical_0_360_inside_interval"] is True
    etg = result["atlas3d_etg"]
    assert etg["n_galaxies"] == 16
    assert etg["n_points"] == 32
    assert etg["canonical_0_360_inside_interval"] is True
    assert result["counts"]["completed_first_principles_derivations"] == 0


def test_ngc4254_ffl_common_resolution_source_boundary():
    from astropy.io import fits

    cube_path = DATA / "ngc4254_common_hi_resolution_source_cube_v03.fits"
    cube_meta = json.loads(
        (DATA / "ngc4254_common_hi_resolution_source_cube_v03.json").read_text()
    )
    result = json.loads((DATA / "ngc4254_ffl_source_systematics_v03.json").read_text())
    scenarios = pd.read_csv(DATA / "ngc4254_ffl_source_systematic_scenarios_v03.csv")
    drivers = pd.read_csv(DATA / "ngc4254_ffl_source_systematic_driver_summary_v03.csv")

    assert cube_meta["inputs"]["velocity_or_residual_inputs"] == []
    assert math.isclose(cube_meta["target_beam"]["major_arcsec"], 37.7028)
    assert math.isclose(cube_meta["target_beam"]["minor_arcsec"], 32.94612)
    assert cube_meta["target_beam"]["pa_deg_east_of_north"] == 42.4
    assert cube_meta["complete_measurement_covariance_ready"] is False
    with fits.open(cube_path) as hdul:
        hdul.verify("exception")
        assert {"STAR_P00", "STAR_P20", "STAR_P40", "SIGMA_GAS"}.issubset(
            {hdu.name for hdu in hdul}
        )

    assert len(scenarios) == 72 * 6
    assert scenarios.groupby("radial_index").size().eq(72).all()
    assert result["summary"]["systematic_sign_stable_radial_indices"] == [5]
    assert result["summary"]["beam_matching_primary_sign_change_radial_indices"] == [0]
    assert 1.74 < result["summary"]["beam_overlap_participation_effective_rank"] < 1.76
    assert result["covariance_boundary"]["diagonal_six_row_likelihood_allowed"] is False
    assert result["complete_measurement_covariance_ready"] is False
    assert result["endpoint_scoring_authorized"] is False
    assert result["audit_checks"]["stellar_global_scale_cancels_in_centered_log_shape"] is True

    geometry = drivers.loc[drivers["driver"].eq("geometry_only")]
    psf_h2 = drivers.loc[
        drivers["driver"].isin(["stellar_psf_only", "h2_conversion_only"])
    ]
    assert (~geometry["sign_stable"]).sum() == 5
    assert psf_h2["sign_stable"].all()

    v01_manifest = json.loads(
        (DATA / "ngc4254_ffl_determinant_source_freeze_v01.json").read_text()
    )
    digest = hashlib.sha256(
        (DATA / "ngc4254_ffl_determinant_source_vectors_v01.csv").read_bytes()
    ).hexdigest()
    assert digest == v01_manifest["outputs"]["row_table_sha256"]


def test_ngc4254_ffl_partial_measurement_boundary():
    from astropy.io import fits

    acquisition = json.loads(
        (DATA / "ngc4254_ffl_uncertainty_source_acquisition_v04.json").read_text()
    )
    fields = json.loads(
        (DATA / "ngc4254_measurement_uncertainty_fields_v05.json").read_text()
    )
    propagation = json.loads(
        (DATA / "ngc4254_ffl_partial_measurement_covariance_v05.json").read_text()
    )
    samples = pd.read_csv(DATA / "ngc4254_ffl_partial_measurement_samples_v05.csv")
    summary = pd.read_csv(DATA / "ngc4254_ffl_partial_measurement_summary_v05.csv")

    assert acquisition["source_products_acquired"] == 21
    assert acquisition["co_error_map_matches_frozen_moment0_grid"] is True
    assert acquisition["hi_public_cube_is_exact_parent_of_frozen_moment0"] is False
    assert acquisition["endpoint_scoring_allowed"] is False

    with fits.open(DATA / "ngc4254_measurement_uncertainty_fields_v05.fits") as hdul:
        hdul.verify("exception")
        names = {hdu.name for hdu in hdul}
        assert {
            "STAR_PIX",
            "STAR_SKY1",
            "STAR_SKY2",
            "STAR_ICA1",
            "STAR_ICA2",
            "H2_IND",
            "H2_CORR",
            "HI_CTL01",
            "HI_CTL10",
            "HI_CTL49",
        }.issubset(names)
    assert fields["audit_checks"]["all_fields_finite_on_common_mask"] is True
    assert fields["hi"]["exact_robust5_uncertainty_ready"] is False
    assert fields["complete_measurement_covariance_ready"] is False
    assert fields["endpoint_scoring_allowed"] is False

    assert len(samples) == 7 * 256 * 6
    assert samples["q_shape_proxy"].notna().all()
    primary = propagation["primary_measurement_result"]
    assert primary["conditionally_sign_stable_annuli_95"] == [0, 1, 2, 3]
    assert primary["co_only_conditionally_sign_stable_annuli_95"] == [0, 1, 2, 3, 4, 5]
    assert primary["v03_source_systematic_sign_stable_annuli"] == [5]
    assert primary["annuli_passing_both_separate_robustness_checks"] == []
    assert primary["maximum_absolute_baseline_shift_from_v03_due_to_one_pixel_mask_refinement"] < 1e-10
    assert propagation["hi49_control_result"]["median_std_change_vs_no_hi_control"] < 0.002
    assert propagation["audit_checks"]["endpoint_scored"] is False
    assert propagation["endpoint_scoring_allowed"] is False
    assert summary.groupby("scenario").size().eq(6).all()


def test_ngc4254_ffl_morphology_phase_role_boundary():
    result = json.loads(
        (DATA / "ngc4254_ffl_morphology_phase_roles_v06.json").read_text()
    )
    systematics = pd.read_csv(
        DATA / "ngc4254_ffl_morphology_phase_role_systematics_v06.csv"
    )
    measurement = pd.read_csv(
        DATA / "ngc4254_ffl_morphology_phase_role_measurement_v06.csv"
    )
    summary = pd.read_csv(DATA / "ngc4254_ffl_morphology_phase_role_summary_v06.csv")

    assert len(systematics) == 8 * 3 * 3 * 2 * 2
    assert len(measurement) == 256 * 4 * 2 * 2
    assert len(summary) == 4
    assert result["inputs"]["velocity_or_residual_inputs"] == []
    assert result["construction"]["phase_stability_limit_deg"] == 22.5
    assert 0.958 < result["construction"]["top_two_trace_fraction"] < 0.959
    assert result["validation"]["role_rotation_covariance_exact"] is True
    assert max(
        result["validation"]["global_stellar_scale_max_q_change"].values()
    ) < 1e-12

    assert result["candidate_status"] == (
        "AT_LEAST_ONE_INTERNAL_SOURCE_ROLE_CANDIDATE_SURVIVES"
    )
    assert result["result"]["passing_harmonic_beam_modes"] == [
        {"beam_mode": 1, "harmonic": 2}
    ]
    assert result["result"]["physical_role_chart_promoted"] is False
    assert result["result"]["endpoint_scoring_allowed"] is False
    passing = summary.loc[summary["passes_both_separate_gates"]]
    assert passing[["harmonic", "beam_mode"]].to_numpy().tolist() == [[2, 1]]
    assert passing["source_q_min"].iloc[0] > 0.0
    assert passing["measurement_baseline_sign_probability"].iloc[0] > 0.95

    role_screen = result["validation"]["angular_role_beam_screen"]["m2"]
    assert role_screen["relative_role_algebraic_rank"] == 3
    assert role_screen["relative_role_participation_rank"] > 2.8
    assert min(role_screen["role_pixel_counts"]) > 100
    assert result["audit_checks"]["endpoint_scored"] is False


def test_ngc4254_ffl_direct_beam_m2_operator_boundary():
    result = json.loads(
        (DATA / "ngc4254_ffl_direct_beam_m2_operator_v07.json").read_text()
    )
    systematics = pd.read_csv(
        DATA / "ngc4254_ffl_direct_beam_m2_systematics_v07.csv"
    )
    measurement = pd.read_csv(
        DATA / "ngc4254_ffl_direct_beam_m2_measurement_v07.csv"
    )
    summary = pd.read_csv(DATA / "ngc4254_ffl_direct_beam_m2_summary_v07.csv")

    assert len(systematics) == 8 * 3 * 3 * 2
    assert len(measurement) == 256 * 4 * 2
    assert len(summary) == 2
    assert result["inputs"]["velocity_or_residual_inputs"] == []
    assert result["construction"]["v06_surviving_beam_mode_index"] == 1
    assert result["construction"]["sparse_annulus_role_cells_used"] is False
    assert 35.0 < result["construction"]["radial_weight_zero_crossings_arcsec"][0] < 35.2
    assert result["construction"]["minimum_required_role_pixels"] == 57
    assert result["validation"]["role_rotation_covariance_exact"] is True
    assert max(
        result["validation"]["global_stellar_scale_max_q_change"].values()
    ) < 1e-12

    assert result["candidate_status"] == (
        "DIRECT_BEAM_M2_SOURCE_CANDIDATE_SURVIVES_INTERNAL_SPECIFICITY_GATE"
    )
    assert result["result"]["m2_passes_own_internal_gates"] is True
    assert result["result"]["m1_alternative_control_passes_own_internal_gates"] is False
    assert result["result"]["m2_family_specificity_pass"] is True
    assert result["result"]["physical_role_chart_promoted"] is False
    assert result["result"]["physical_q_det_constructed"] is False
    assert result["result"]["endpoint_scoring_allowed"] is False

    m2 = summary.loc[summary["harmonic"].eq(2)].iloc[0]
    m1 = summary.loc[summary["harmonic"].eq(1)].iloc[0]
    assert bool(m2["passes_own_internal_gates"]) is True
    assert bool(m2["survives_v07_selection"]) is True
    assert bool(m1["passes_own_internal_gates"]) is False
    assert m2["source_q_min"] > 0.0
    assert m2["measurement_q_p025"] > 0.0
    assert m2["minimum_role_pixels_source_systematics"] >= 57
    assert result["audit_checks"]["sparse_annulus_role_cells_eliminated"] is True
    assert result["audit_checks"]["endpoint_scored"] is False


def test_ngc4254_ffl_terminal_identifiability_no_go_boundary():
    result = json.loads(
        (DATA / "ngc4254_ffl_terminal_identifiability_v08.json").read_text()
    )

    assert result["status"] == (
        "SOURCE_ONLY_TERMINAL_IDENTIFIABILITY_NO_GO_PROVED_NO_ENDPOINT"
    )
    assert result["inputs"]["velocity_or_residual_inputs"] == []
    assert result["source_result"]["q_shape_proxy_baseline"] > 0.0
    assert result["source_result"]["q_shape_proxy_source_range"][0] > 0.0
    theorem = result["single_terminal_theorem"]
    assert theorem["single_terminal_free_gain_saturated"] is True
    assert theorem["identity_checks"] == 10000
    assert theorem["maximum_reconstruction_error"] < 1e-12
    no_go = result["factorization_no_go"]
    assert no_go["named_readouts_are_independent_by_name"] is False
    assert no_go["one_scalar_source_proxy_separates_components"] is False
    assert result["result"]["morphology_source_coordinate_robust"] is True
    assert result["result"]["single_terminal_physical_test_ready"] is False
    assert result["result"]["channel_presence_detected"] is False
    assert result["result"]["channel_components_identifiable"] is False
    assert result["result"]["endpoint_scoring_allowed"] is False
    assert result["audit_checks"]["endpoint_scored"] is False


def test_ngc4254_ffl_primitive_curvature_identifiability_no_go_boundary():
    result = json.loads(
        (DATA / "ngc4254_ffl_primitive_curvature_identifiability_v09.json").read_text()
    )

    assert result["status"] == (
        "SOURCE_STATE_DOES_NOT_IDENTIFY_PRIMITIVE_FFL_CURVATURES_PROVED_NO_ENDPOINT"
    )
    assert result["inputs"]["velocity_or_residual_inputs"] == []
    countermodel = result["stationary_state_countermodel"]
    assert countermodel["shared_action_value_at_state"] == 0.0
    assert countermodel["shared_first_variation_at_state"] == 0.0
    assert countermodel["different_second_variations"] is True
    witness = result["finite_witness"]
    assert len(witness["models"]) == 4
    assert witness["same_q_shape_in_every_model"] is True
    assert witness["all_conditional_gains_distinct"] is True
    covariance = result["measurement_covariance_no_go"]
    assert covariance["not_equal_without_bridge"] is True
    assert covariance["v05_or_v07_covariance_can_define_kappa_X_kappa_Y"] is False
    assert result["result"]["robust_source_shape_retained"] is True
    assert result["result"]["primitive_curvatures_identified"] is False
    assert result["result"]["physical_gain_identified"] is False
    assert result["result"]["measurement_covariance_promoted_to_parent_hessian"] is False
    assert result["result"]["endpoint_scoring_allowed"] is False
    assert result["audit_checks"]["endpoint_scored"] is False


def test_morphology_conditioned_channel_novelty_boundary():
    result = json.loads(
        (DATA / "morphology_conditioned_channel_novelty_audit_v01.json").read_text()
    )

    assert result["status"] == (
        "NO_CURRENT_CHANNEL_CANDIDATE_PASSES_MORPHOLOGY_CONDITIONED_NOVELTY_RULE"
    )
    witness = result["finite_witnesses"]
    assert witness["duplicate_readout_positive_conditional_information_bits"] > 0.0
    assert witness["duplicate_readout_rank_increment"] == 0
    assert witness["transverse_readout_rank_increment"] == 1
    assert result["candidate_count"] == 6
    assert result["population_label_integrity_pass"] is False
    assert result["promotion_pass_count"] == 0
    assert all(not row["promotion_pass"] for row in result["current_candidates"])
    assert result["time_status"].startswith("not identified")
    assert "residual-based" in result["claim_boundary"]


def test_phangs_radial_body_projection_development_preflight_boundary():
    acquisition = json.loads(
        (DATA / "phangs_radial_body_projection_development_source_acquisition_v01.json").read_text()
    )
    preflight = json.loads(
        (DATA / "phangs_radial_body_projection_development_preflight_v01.json").read_text()
    )
    coverage = pd.read_csv(
        DATA / "phangs_radial_body_projection_development_source_coverage_v01.csv"
    )

    assert acquisition["velocity_products_acquired"] == 0
    assert acquisition["velocity_contrast_opened"] is False
    assert acquisition["rotation_residual_opened"] is False
    assert acquisition["confirmatory_products_requested"] is False
    assert acquisition["source_body_blocked"] == ["NGC1365"]
    assert len(acquisition["source_body_ready"]) == 5
    assert coverage.source_body_ready.sum() == 5

    assert preflight["velocity_contrast_opened"] is False
    assert preflight["rotation_residual_opened"] is False
    assert preflight["confirmatory_products_opened"] is False
    assert preflight["endpoint_score_computed"] is False
    assert preflight["all_ready_galaxies_pass_rank_gate"] is True
    assert len(preflight["galaxies"]) == 5
    for metrics in preflight["galaxies"].values():
        assert metrics["shape"] == [20, 8]
        assert metrics["rank"] == 8
        assert metrics["projected_complement_dimension"] == 12
        assert metrics["rank_gate_ge_4_complement"] is True
        assert metrics["center_inside_both_sources"] is True
        assert metrics["condition_number_nonzero"] < 20.0
    assert "final endpoint matrices must be reevaluated" in preflight["radial_coordinate_boundary"]


def test_phangs_radial_body_projection_terminal_edge_replay_boundary():
    acquisition = json.loads(
        (DATA / "phangs_radial_body_projection_development_terminal_acquisition_v01.json").read_text()
    )
    replay = json.loads(
        (DATA / "phangs_radial_body_projection_development_terminal_edge_replay_v01.json").read_text()
    )
    operator = json.loads(
        (DATA / "phangs_radial_body_projection_operator_audit_v01.json").read_text()
    )

    assert acquisition["status"] == "DEVELOPMENT_TERMINAL_FIELDS_ACQUIRED_HASH_FROZEN"
    assert acquisition["hashes_frozen_in_script"] is True
    assert acquisition["confirmatory_galaxies_opened"] == []
    assert acquisition["body_projection_score_computed"] is False
    assert acquisition["endpoint_scoring_allowed"] is False

    assert replay["status"] == "DEVELOPMENT_TERMINAL_EDGE_BODY_MATRIX_RANK_GATE_PASSES"
    assert replay["velocity_values_used_only_for_common_support"] is True
    assert replay["velocity_contrast_constructed"] is False
    assert replay["terminal_coefficients_fitted"] is False
    assert replay["body_projection_score_computed"] is False
    assert replay["confirmatory_galaxies_opened"] == []
    assert replay["all_development_galaxies_pass_rank_gate"] is True
    for metrics in replay["galaxies"].values():
        assert metrics["beam_independent_pixels"] >= 50
        assert metrics["rank"] == 8
        assert metrics["projected_complement_dimension"] == 12
        assert metrics["condition_number_nonzero"] < 20.0

    assert operator["status"] == "COVARIANCE_WEIGHTED_BODY_PROJECTOR_IDENTITIES_PASS"
    assert operator["all_operator_checks_pass"] is True
    assert operator["rank_relative_svd_tolerance"] == 1.0e-10
    assert operator["velocity_contrast_used"] is False
    assert operator["terminal_coefficients_used"] is False
    assert operator["confirmatory_galaxies_opened"] == []
    assert operator["endpoint_score_computed"] is False
    for metrics in operator["galaxies"].values():
        assert metrics["projection_rank"] == 12
        assert metrics["projected_covariance_rank"] == 12
        assert metrics["annihilation_max_abs"] < 1.0e-10
        assert metrics["idempotence_max_abs"] < 1.0e-10
        assert metrics["weighted_self_adjoint_max_abs"] < 1.0e-10
        assert abs(metrics["body_vector_q"]) < 1.0e-10


def test_phangs_radial_body_projection_holdout_identifiability_no_go():
    result = json.loads(
        (DATA / "phangs_radial_body_projection_holdout_identifiability_v01.json").read_text()
    )
    assert result["status"] == (
        "CURRENT_PROJECTION_PACKET_DOES_NOT_IDENTIFY_GROUPED_HOLDOUT_BODY_INCREMENT"
    )
    assert result["verdict"] == "PROVEN_FINITE_LINEAR_NO_GO"
    assert all(result["checks"].values())
    assert result["derived_results"]["projection_q_can_test_body_orthogonal_innovation"] is True
    assert result["derived_results"]["source_matrix_alone_predicts_body_terminal"] is False
    assert result["derived_results"]["free_per_body_complement_is_predictive_model"] is False
    assert result["derived_results"]["grouped_holdout_gain_identified_by_current_packet"] is False
    assert result["velocity_contrast_used"] is False
    assert result["terminal_coefficients_used"] is False
    assert result["confirmatory_galaxies_opened"] == []
    assert result["endpoint_score_computed"] is False
    for witness in result["witnesses"].values():
        assert witness["source_rank"] == 8
        assert witness["complement_dimension"] == 12
        assert witness["combined_span_rank"] == 20


def test_phangs_radial_body_projection_normalization_gauge():
    result = json.loads(
        (DATA / "phangs_radial_body_projection_normalization_gauge_v01.json").read_text()
    )
    assert result["status"] == "RAW_SOURCE_AMPLITUDE_GAUGE_RECOVERED_SOURCE_SIDE"
    assert result["all_checks_pass"] is True
    assert result["endpoint_opened"] is False
    assert result["score_computed"] is False
    assert len(result["galaxies"]) == 5
    for galaxy in result["galaxies"].values():
        assert galaxy["minimum_raw_column_norm"] > 0.0
        assert all(galaxy["checks"].values())


def test_phangs_radial_body_projection_rank4_source_shadow():
    result = json.loads(
        (DATA / "phangs_radial_body_projection_rank4_source_shadow_v01.json").read_text()
    )
    assert result["status"] == "SOURCE_ONLY_OPTIMAL_RANK4_BODY_SHADOW_QUANTIFIED"
    assert result["velocity_contrast_opened"] is False
    assert result["endpoint_score_computed"] is False
    assert len(result["galaxies"]) == 5
    assert result["summary"]["minimum_rank4_energy_fraction"] > 0.86
    assert result["summary"]["minimum_sigma4_over_sigma5"] > 1.0
    for galaxy in result["galaxies"].values():
        assert galaxy["source_matrix_rank"] == 8
        assert galaxy["rank4_subspace_unique_in_euclidean_source_metric"] is True
        assert galaxy["rank4_projector_idempotence_error"] < 1.0e-10


def test_phangs_radial_body_projection_scoring_contract_is_frozen_unopened():
    result = json.loads(
        (DATA / "phangs_radial_body_projection_scoring_contract_v01.json").read_text()
    )
    assert result["status"] == "ONE_SHOT_BODY_ORTHOGONAL_Q_SCORING_CONTRACT_FROZEN_UNOPENED"
    assert result["all_synthetic_checks_pass"] is True
    assert result["jackknife_assembly_audit"]["all_gates_pass"] is True
    assert result["jackknife_assembly_audit"]["zone_block_ranks"] == [4, 4, 4, 4, 4]
    assert result["jackknife_assembly_audit"]["assembled_rank"] == 20
    assert result["projection_and_score"]["relative_svd_tolerance"] == 1.0e-10
    assert result["decision_covariance"]["azimuth_sectors"] == 12
    assert result["decision_rule"]["global_p_below"] == 0.01
    assert result["decision_rule"]["minimum_individual_detections_of_four"] == 3
    assert result["promotion_boundary"]["one_shot_q_can_detect_body_orthogonal_tracer_structure"] is True
    assert result["promotion_boundary"]["grouped_body_increment_available"] is False
    assert result["velocity_contrast_used"] is False
    assert result["terminal_coefficients_used"] is False
    assert result["confirmatory_galaxies_opened"] == []
    assert result["endpoint_score_computed"] is False
    assert result["decision_truth_table"] == {
        "global_and_three_individual": True,
        "global_without_replication": False,
        "replication_without_global": False,
    }
    for audit in result["synthetic_audit"].values():
        assert all(audit["checks"].values())
        assert abs(audit["pure_body"]["q"]) < 1.0e-10
        assert audit["pure_body"]["dof"] == 12
        assert audit["transverse_injection"]["q"] > 0.0


def test_phangs_radial_body_projection_confirmatory_gate_failure_is_preserved():
    acquisition = json.loads(
        (DATA / "phangs_radial_body_projection_confirmatory_acquisition_v01.json").read_text()
    )
    endpoint = json.loads(
        (DATA / "phangs_radial_body_projection_confirmatory_endpoint_v01.json").read_text()
    )
    diagnostic = json.loads(
        (DATA / "phangs_radial_body_projection_sector_occupancy_failure_v01.json").read_text()
    )
    assert acquisition["status"] == "CONFIRMATORY_PACKET_ACQUIRED_HASH_FROZEN_VALUES_UNOPENED"
    assert acquisition["products_total"] == 24
    assert len(acquisition["source_hashes_sha256"]) == 24
    assert acquisition["terminal_pixel_values_opened"] is False
    assert acquisition["endpoint_score_computed"] is False

    assert endpoint["status"] == "CONFIRMATORY_ENDPOINT_OPENED_NONIDENTIFIABLE_GATE_FAILURE"
    assert set(endpoint["eligibility_failures"]) == {"NGC1300", "NGC1385", "NGC1512", "NGC5068"}
    assert endpoint["individual_scores_released"] is False
    assert endpoint["aggregate_score_computed"] is False
    assert endpoint["replacement_or_repair_allowed"] is False

    assert diagnostic["status"] == "FROZEN_12_SECTOR_GATE_FAILS_FINITE_FOOTPRINT_DIAGNOSTIC_ONLY"
    assert diagnostic["same_endpoint_rescoring_allowed"] is False
    assert diagnostic["post_open_gate_relaxation_allowed"] is False
    expected = {
        "NGC1300": [12, 11, 12, 12, 9],
        "NGC1385": [12, 12, 12, 12, 9],
        "NGC1512": [12, 12, 12, 12, 8],
        "NGC5068": [12, 12, 11, 10, 6],
    }
    for galaxy, counts in expected.items():
        assert [zone["occupied_sector_count"] for zone in diagnostic["galaxies"][galaxy]["zones"]] == counts


def test_phangs_radial_body_projection_same_family_cohort_is_exhausted():
    result = json.loads(
        (DATA / "phangs_radial_body_projection_cohort_exhaustion_v01.json").read_text()
    )
    assert result["status"] == "PHANGS_MUSE_SAME_FAMILY_CONFIRMATORY_COHORT_EXHAUSTED"
    assert result["all_checks_pass"] is True
    assert result["untouched_same_family_candidates"] == []
    assert result["same_sample_relabel_or_replacement_allowed"] is False
    assert sum(result["disposition_counts"].values()) == 19
    assert result["disposition_counts"] == {
        "CURRENT_CONFIRMATORY_VALUES_OPENED": 4,
        "CURRENT_METHOD_DEVELOPMENT_VALUES_OPENED": 5,
        "GEOMETRY_GATE_FAILED": 2,
        "PRIOR_ENDPOINT_ALREADY_OPENED": 6,
        "SOURCE_BLOCKED_NO_MATCHING_BROAD_CO_MOMENT0": 1,
        "SOURCE_BODY_DESCRIPTION_INCOMPLETE": 1,
    }
