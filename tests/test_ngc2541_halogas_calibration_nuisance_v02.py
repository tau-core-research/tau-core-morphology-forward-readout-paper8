import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def test_ngc2541_halogas_calibration_nuisance_v02() -> None:
    result = json.loads(
        (ROOT / "data/derived/ngc2541_halogas_calibration_nuisance_v02.json").read_text()
    )
    scenarios = pd.read_csv(
        ROOT / "data/derived/ngc2541_halogas_calibration_nuisance_v02_scenarios.csv"
    )

    assert result["status"] == "POST_OPEN_DESCRIPTIVE_DIAGNOSTIC_CALIBRATION_UNSTABLE"
    assert result["calibration_direction_stable"] is False
    assert result["nuisance_direction_contains_improvement_and_worsening"] is True
    assert result["beam_correlation_audit"]["minimum_pixels_in_beams"] < 1.0
    assert result["beam_correlation_audit"]["ring_spacing_below_beam_major_present"] is True
    assert result["source_uncertainty_limitation"]["propagated_in_v02"] is False
    assert set(scenarios["iterations"]) == {4, 20}
    assert set(scenarios["footprint"]) == {"COMMON_SKY_PIXEL_INTERSECTION"}
    assert {
        "NED",
        "JOZSA_FITTED",
        "NED_E_PLUS_4_ARCSEC",
        "NED_E_MINUS_4_ARCSEC",
        "NED_N_PLUS_4_ARCSEC",
        "NED_N_MINUS_4_ARCSEC",
    } == set(scenarios["centre_case"])
    fitted = scenarios[(scenarios.centre_case == "JOZSA_FITTED") & (scenarios.iterations == 20)]
    ned = scenarios[(scenarios.centre_case == "NED") & (scenarios.iterations == 20)]
    assert float(fitted.iloc[0].delta_mean_variable_minus_fixed_kms) > 0.0
    assert float(ned.iloc[0].delta_mean_variable_minus_fixed_kms) < 0.0
    assert "no Tau q_R" in result["claim_boundary"]
