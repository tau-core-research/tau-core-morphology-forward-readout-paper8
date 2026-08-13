import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / "data/derived" / name).read_text(encoding="utf-8"))


def test_global_s4g_morphology_does_not_predict_outer_discrepancy():
    result = read("s4g_dark_discrepancy_morphology_endpoint_v01.json")
    assert result["n_holdout"] == 20
    assert result["mse_reduction"] < 0
    assert result["morphology_information_candidate"] is False
    assert result["channel_origin_identified"] is False


def test_d1p5_multitracer_candidate_is_not_replicated():
    result = read("dark_discrepancy_zone_multitracer_channel_audit_v01.json")
    assert result["galaxies"]["NGC3726"]["post_d1p5"]["chi2_zero_p"] <= 0.05
    assert result["galaxies"]["NGC4559"]["post_d1p5"]["chi2_zero_p"] > 0.05
    assert result["zero_contrast_rejected_in_both_galaxies"] is False
    assert result["d2_zone_covered_in_both_galaxies"] is False
    assert result["channel_information_candidate"] is False


def test_disturbance_atlas_keeps_unknown_path_explicit():
    atlas = read("sparc_lightcone_disturbance_atlas_v01.json")
    assert atlas["n_galaxies"] == 75
    assert atlas["path_class_counts"] == {"PX": 75}
    assert "foreground objects" in atlas["path_data_requirements"][0]


def test_local_candidate_is_source_disturbed_and_path_unknown():
    result = read("dark_discrepancy_channel_disturbance_classification_v01.json")
    assert result["classified_results"]["NGC3726"]["combined_class"] == "S3-PX-O0"
    assert result["classified_results"]["NGC4559"]["combined_class"] == "S0-PX-O0"
    assert result["candidate_clean_source_replication"] is False
    assert result["candidate_clean_path_replication"] is False


def test_simbad_path_proxy_is_not_population_signal():
    census = read("sparc_simbad_lightcone_foregrounds_v01.json")
    assert census["n_query_ok"] == 75
    assert census["path_class_counts"]["P0"] == 68
    result = read("sparc_path_disturbance_dark_discrepancy_test_v01.json")
    assert result["mse_reduction"] > 0
    assert result["shuffle"]["p"] > 0.05
    assert result["path_information_candidate"] is False
    assert result["physical_channel_detected"] is False


def test_tau_kernel_gain_is_not_modulated_by_preliminary_path_proxy():
    result = read("tau_kernel_path_modulation_test_v01.json")
    assert result["n_galaxies"] == 75
    assert result["permutation"]["two_sided_p"] > 0.05
    assert result["fisher_two_sided_p"] > 0.05
    assert result["path_modulation_candidate"] is False


def test_kernel_provenance_keeps_channel_content_unidentified():
    result = read("tau_kernel_body_channel_provenance_audit_v01.json")
    assert result["shape_and_scale_layer"]["uses_observed_rotation_endpoint"] is False
    assert result["amplitude_layer"]["uses_observed_rotation_endpoint"] is True
    assert result["identifiability"]["physical_path_channel_separable_from_amplitude"] is False
    assert result["identifiability"]["tracer_specific_channel_kernel_measured"] is False


def test_same_body_tracer_amplitude_difference_is_not_kernel_specific():
    result = read("same_body_tracer_effective_kernel_amplitude_test_v01.json")
    assert result["two_sigma_difference_in_all_galaxy_resolution_tests"] is True
    assert result["tau_kernel_shape_wins_all_equal_parameter_controls"] is False
    assert result["kernel_embedded_channel_information_candidate"] is False
    assert result["kernel_after_multiplicative_scale_candidate_all_tests"] is False
    assert result["physical_channel_detected"] is False


def test_raw_effective_beta_path_signal_fails_robustness():
    raw = read("effective_kernel_amplitude_path_information_test_v01.json")
    assert raw["shuffle"]["p"] <= 0.05
    audit = read("effective_kernel_amplitude_path_robustness_v01.json")
    assert audit["variants"]["signed_log"]["mse_reduction"] < 0
    assert audit["variants"]["winsor_5_95"]["mse_reduction"] < 0
    assert audit["variants"]["exclude_compact_family"]["mse_reduction"] < 0
    assert audit["variants"]["scale_invariant_fractional_kernel_load"]["mse_reduction"] < 0
    assert audit["variants"]["scale_invariant_fractional_kernel_load"]["shuffle_p"] > 0.05
    assert audit["path_information_candidate_promoted"] is False


def test_ugc08490_source_packet_is_endpoint_blind_and_radially_supported():
    source = read("ugc08490_whisp_hi_source_v01.json")
    assert source["graphical_velocity_field_acquired"] is True
    assert source["source_coordinate_fits_acquired"] is False
    velocity = read("ugc08490_whisp_graphical_velocity_preflight_v01.json")
    assert velocity["both_hi_velocity_sides_present"] is True
    assert velocity["kernel_measurement_allowed"] is False
    axis = read("ugc08490_whisp_angular_axis_preflight_v01.json")
    assert axis["ghasp_support_inside_both_hi_proxy_maxima"] is True
    assert axis["endpoint_access"] is False


def test_ugc08490_channel_diagnostic_preserves_claim_boundary():
    result = read("ugc08490_hi_halpha_channel_diagnostic_v01.json")
    profile = pd.read_csv(ROOT / "data/derived/ugc08490_hi_halpha_channel_profile_v01.csv")
    assert result["status"] == "NEGATIVE_RESULT_PRESERVED"
    assert result["kernel_specific_channel_test_allowed"] is False
    assert result["endpoint_access"] is False
    assert result["common_two_side_radial_support"] is False
    assert set(profile["side"]) == {"approaching"}
    assert (profile["hi_selected_pixels"] > 0).all()


def test_ugc08490_vector_hi_route_stays_diagnostic():
    source = read("ugc08490_repetto_hi_figure_source_v01.json")
    profile = read("ugc08490_repetto_hi_vector_profile_v01.json")
    result = read("ugc08490_repetto_hi_halpha_channel_test_v01.json")
    assert source["vector_figure_acquired"] is True
    assert source["source_native_numeric_table_acquired"] is False
    assert profile["n_points"] >= 60
    assert result["n_common_points"] == 14
    assert result["both_halpha_sides_covered_without_extrapolation"] is True
    assert result["tau_kernel_tested"] is False
    assert result["physical_channel_detected"] is False
    assert result["endpoint_access"] is False


def test_ugc08490_scale_is_not_promoted_past_inclination_control():
    result = read("ugc08490_tracer_scale_origin_audit_v01.json")
    assert result["scale_differs_from_unity_in_point_bootstrap"] is True
    assert result["measured_scale_inside_inclination_prediction_interval"] is True
    assert abs(result["residual_scale_after_inclination_harmonization"] - 1) < 0.05
    assert result["tau_core_scale_candidate_promoted"] is False
    assert result["physical_channel_detected"] is False


def test_composite_kernel_scoring_replay_keeps_origin_unresolved():
    result = read("composite_tau_kernel_scoring_replay_v01.json")
    assert result["verdicts"]["matched_kernel_family_specificity_signal"] is True
    assert result["verdicts"]["universal_baseline_superiority"] is False
    assert result["verdicts"]["time_operator_identified"] is False
    assert result["verdicts"]["quantum_operator_identified"] is False
    assert result["verdicts"]["physical_channel_origin_identified"] is False


def test_little_things_prospective_sample_is_not_scored_without_baryonic_profiles():
    result = read("little_things_prospective_scoring_source_v01.json")
    assert result["source_native_numeric_rotation_curves"] is True
    assert result["n_exact_name_new_vs_historical_175"] > 0
    assert result["source_native_radial_baryonic_velocity_components"] is False
    assert result["prospective_scoring_allowed"] is False
    assert result["endpoint_access"] is False
