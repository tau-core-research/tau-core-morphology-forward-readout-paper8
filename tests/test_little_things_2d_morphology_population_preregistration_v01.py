import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"


def test_little_things_population_freeze_is_velocity_blind_and_nonlabel_selected() -> None:
    result = json.loads(
        (DATA / "little_things_2d_morphology_population_preregistration_v01.json")
        .read_text(encoding="utf-8")
    )
    assert result["status"] == "SOURCE_POPULATION_FROZEN_MOM0_ONLY_ACQUISITION_ALLOWED"
    assert result["population_rule"].startswith("all 40 galaxies")
    assert len(result["rows"]) == 40
    assert result["counts"] == {
        "EXCLUDED_PUBLISHED_SUPPORT_LT_10_BEAMS_PER_RH": 9,
        "EXCLUDED_SOURCE_GEOMETRY": 6,
        "PROVISIONAL_SOURCE_CANDIDATE": 19,
        "SOURCE_MOM0_SUPPORT_PENDING": 6,
    }
    assert result["velocity_product_acquisition_allowed"] is False
    assert result["velocity_pixels_opened"] is False
    assert result["tau_endpoint_allowed"] is False


def test_little_things_population_freeze_hash_and_operator_shape() -> None:
    result = json.loads(
        (DATA / "little_things_2d_morphology_population_preregistration_v01.json")
        .read_text(encoding="utf-8")
    )
    cohort = ROOT / result["cohort_csv"]
    assert hashlib.sha256(cohort.read_bytes()).hexdigest() == result["cohort_csv_sha256"]
    design = result["test_design"]
    assert "exactly two" in result["cross_validation"]["rank"]
    assert "never 2J" in design["velocity_target"]
    assert "global_phase_rotation_pi_over_2" not in design["wrong_templates"]
    assert "same two-quadrature target subspace" in design["forbidden_wrong_template"]
    assert result["source_gates"]["minimum_published_or_measured_beams_per_source_radius"] == 10.0


def test_little_things_acquisition_contains_source_maps_only() -> None:
    acquisition_path = DATA / "little_things_2d_morphology_source_acquisition_v01.json"
    if not acquisition_path.exists():
        return
    result = json.loads(acquisition_path.read_text(encoding="utf-8"))
    assert result["requested_count"] == 25
    assert result["velocity_products_downloaded"] is False
    assert result["velocity_pixels_read"] is False
    assert result["endpoint_scoring_allowed"] is False
    ledger = (ROOT / result["ledger"]).read_text(encoding="utf-8").upper()
    assert "MOM1" not in ledger
    assert "MOM2" not in ledger
    assert "ICL001" not in ledger


def test_little_things_source_preflight_keeps_velocity_closed() -> None:
    path = DATA / "little_things_2d_morphology_source_preflight_v01.json"
    if not path.exists():
        return
    result = json.loads(path.read_text(encoding="utf-8"))
    assert result["source_map_count"] == 25
    assert result["support_pass_count"] >= 19
    assert result["support_pass_count"] + result["support_fail_count"] == 25
    assert result["operator_calibration_complete"] is False
    assert result["velocity_product_acquisition_allowed"] is False
    assert result["velocity_pixels_opened"] is False
    assert result["tau_endpoint_allowed"] is False
    assert len(result["cross_galaxy_derangement"]) == result["support_pass_count"]
    assert all(
        result["cross_galaxy_derangement"][galaxy] != galaxy
        for galaxy in result["passing_galaxies"]
    )


def test_little_things_operator_calibration_has_two_target_dimensions() -> None:
    path = DATA / "little_things_2d_morphology_operator_calibration_v01.json"
    if not path.exists():
        return
    result = json.loads(path.read_text(encoding="utf-8"))
    assert result["velocity_pixels_opened"] is False
    assert result["endpoint_scoring_allowed"] is False
    assert result["tau_endpoint_allowed"] is False
    assert result["global_phase_wrong_template_forbidden"] is True
    assert result["galaxy_count"] >= 19
    assert all(row["target_rank"] == 2 for row in result["results"])
    assert all(len(row["fold_checks"]) == 8 for row in result["results"])
    assert result["population_operator_gate_pass"] is True
    assert result["operator_pass_count"] == 20
    assert result["operator_failing_galaxies"] == ["M81dwA", "Mrk178"]
    assert result["velocity_product_acquisition_allowed"] is True


def test_little_things_frozen_endpoint_preserves_negative_result() -> None:
    endpoint = json.loads(
        (DATA / "little_things_2d_morphology_population_endpoint_v01.json").read_text(encoding="utf-8")
    )
    assert endpoint["status"] == "CONVENTIONAL_MORPHOLOGY_SENSITIVITY_NOT_DEMONSTRATED"
    assert endpoint["scored_galaxy_count"] == 20
    assert endpoint["mean_specificity"] < 0
    assert endpoint["median_specificity"] < 0
    assert endpoint["positive_fraction"] == 0.25
    assert endpoint["exact_one_sided_sign_flip_p"] > 0.95
    assert endpoint["tau_endpoint_scored"] is False
    assert endpoint["parent_loss_inferred"] is False
    assert endpoint["gravity_or_dark_matter_claim_allowed"] is False


def test_little_things_post_open_robustness_does_not_replace_endpoint() -> None:
    robustness = json.loads(
        (DATA / "little_things_2d_morphology_endpoint_robustness_v01.json").read_text(encoding="utf-8")
    )
    assert robustness["audit_class"] == "post-open robustness; not a replacement endpoint"
    assert robustness["all_leave_one_out_primary_means_negative"] is True
    assert robustness["all_target_valid_fractions_one"] is True
    assert robustness["global_phase_rotation_is_invalid_negative_control"] is True
    assert robustness["global_phase_rotation_projector_delta"] < 1e-12
    assert robustness["primary_endpoint_changed"] is False
