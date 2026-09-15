import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ngc4062_freeze_precedes_reproducible_negative_endpoint():
    subprocess.run(
        [sys.executable, "scripts/freeze_ngc4062_halogas_confirmatory_endpoint_v01.py"],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        [sys.executable, "scripts/run_ngc4062_halogas_confirmatory_endpoint_v01.py"],
        cwd=ROOT,
        check=True,
    )
    freeze = json.loads((ROOT / "data/derived/ngc4062_halogas_confirmatory_freeze_v01.json").read_text())
    result = json.loads((ROOT / "data/derived/ngc4062_halogas_confirmatory_endpoint_v01.json").read_text())

    assert freeze["pixel_values_opened_during_freeze"] is False
    assert freeze["common_radii_arcsec"] == [42.0, 84.0]
    assert freeze["source_geometry"]["halogas_3dbarolo"] == {
        "median_inclination_deg": 67.1,
        "median_pa_deg": 100.1,
    }
    assert result["status"] == "NGC4062_CONFIRMATORY_ENDPOINT_FAIL"
    assert result["confirmatory_pass"] is False
    assert result["gates"]["hr_rejects_zero"] is False
    assert result["gates"]["lr_rejects_zero"] is False
    assert result["gates"]["hr_lr_gls_sign_agreement"] is True
    assert result["gates"]["all_twelve_nuisance_scores_preserve_sign"] is False
    assert abs(result["outputs"]["HR"]["primary_score"]["gls_mean_z"]) < 1.0
    assert abs(result["outputs"]["LR"]["primary_score"]["gls_mean_z"]) < 1.0
    assert "not a Tau detection" in result["claim_boundary"]
