import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def test_ngc2541_halogas_endpoint_and_claim_boundary() -> None:
    endpoint_dir = ROOT / "data/external/literature/ngc2541_halogas_independent_endpoint_v01"
    assert md5(endpoint_dir / "NGC2541-HR_mom0m.fits") == "fc6149afc34a6fb0d5bcd7b13cb21aa4"
    assert md5(endpoint_dir / "NGC2541-HR_mom1m.fits") == "290a53d6bcaf372bb0d4b508dad6df64"

    result = json.loads((ROOT / "data/derived/ngc2541_halogas_independent_side_consistency_endpoint_v01.json").read_text())
    robustness = json.loads((ROOT / "data/derived/ngc2541_halogas_side_consistency_robustness_v01.json").read_text())
    rings = pd.read_csv(ROOT / "data/derived/ngc2541_halogas_independent_side_consistency_endpoint_v01_rings.csv")

    assert result["free_parameters"] == 0
    assert result["endpoint_hashes_verified"] is True
    assert result["n_common_eligible_rings"] == 23
    assert result["delta_mean_variable_minus_fixed_kms"] < 0
    assert "cannot select a Tau q_R" in result["claim_boundary"]
    assert robustness["bootstrap_95pct_ci_kms"][0] < 0 < robustness["bootstrap_95pct_ci_kms"][1]
    assert robustness["one_sided_sign_flip_p"] > 0.05
    assert robustness["leave_one_out_direction_always_improves"] is True
    assert set(rings.geometry) == {"fixed", "variable"}
