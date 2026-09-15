import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
SCRIPT = ROOT / "scripts" / "run_inverse_required_rapidity_diagnostic_v01.py"
PREFIX = "inverse_required_rapidity_diagnostic_v01"
SUMMARY = DATA / f"{PREFIX}_summary.csv"
PAIRS = DATA / f"{PREFIX}_model_pair_tests.csv"
POINTS = DATA / f"{PREFIX}_points.csv"
AUDIT = DATA / f"{PREFIX}_audit.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_diagnostic() -> None:
    subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def test_inverse_required_rapidity_diagnostic_is_reproducible() -> None:
    run_diagnostic()
    first = {path: digest(path) for path in (SUMMARY, PAIRS, POINTS, AUDIT)}
    run_diagnostic()
    second = {path: digest(path) for path in (SUMMARY, PAIRS, POINTS, AUDIT)}
    assert first == second


def test_inverse_required_rapidity_claim_boundary_and_packet() -> None:
    result = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert result["status"] == "DIAGNOSTIC_ONLY_NOT_ENDPOINT"
    assert result["frozen_packet"]["n_points"] == 3389
    assert result["frozen_packet"]["n_galaxies"] == 175
    assert result["frozen_packet"]["n_train_galaxies"] == 131
    assert result["frozen_packet"]["n_holdout_galaxies"] == 44
    assert result["predictor_policy"]["holdout_used_for_tuning"] is False
    assert result["predictor_policy"]["forbidden_overlap"] == []
    assert result["claim_boundary"]["endpoint_allowed"] is False
    assert "physical q_tau(R)" in result["claim_boundary"]["not_derived"]
    assert "distance-dependent parent loss" in result["claim_boundary"]["not_derived"]


def test_inverse_required_rapidity_numerics_and_negative_distance_result() -> None:
    result = json.loads(AUDIT.read_text(encoding="utf-8"))
    numerics = result["known_limit_and_numerics"]
    assert numerics["equal_velocity_gives_zero_exactly"] is True
    assert max(numerics["maximum_exact_minus_linear_kms"].values()) < 1.0e-3
    assert max(numerics["maximum_change_using_c_300000_kms"].values()) < 1.0e-5

    summary = pd.read_csv(SUMMARY)
    assert len(summary) == 24
    combined = summary.loc[summary["model_id"] == "combined"].set_index("baseline_id")
    assert combined.loc["newtonian_baryonic", "rmse_ratio_to_zero"] < 0.5
    assert combined.loc["newtonian_baryonic", "paired_sign_flip_p_lower"] < 0.01
    assert 0.9 < combined.loc["tpg_v6", "rmse_ratio_to_zero"] < 1.05
    assert combined.loc["tpg_v6", "paired_sign_flip_p_lower"] > 0.05
    assert 0.85 < combined.loc["mond_fixed", "rmse_ratio_to_zero"] < 1.05
    assert combined.loc["mond_fixed", "paired_sign_flip_p_lower"] > 0.05

    pairs = pd.read_csv(PAIRS)
    distance = pairs.loc[
        pairs["comparison_id"] == "distance_added_to_morphology"
    ].set_index("baseline_id")
    for baseline in ("newtonian_baryonic", "tpg_v6", "mond_fixed"):
        assert distance.loc[baseline, "paired_sign_flip_p_lower"] > 0.05
        assert distance.loc[baseline, "bootstrap_ci_lower_kms"] <= 0.0
        assert distance.loc[baseline, "bootstrap_ci_upper_kms"] >= 0.0

    points = pd.read_csv(POINTS)
    assert len(points) == 3 * 3389
    assert points["baseline_id"].nunique() == 3
    assert "u_predicted_combined_kms" in points.columns
