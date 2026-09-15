import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"


def test_inverse_parent_loss_artifacts_and_forward_identity():
    audit = json.loads(
        (DATA / "inverse_required_parent_loss_diagnostic_v01.json").read_text()
    )
    points = pd.read_csv(
        DATA / "inverse_required_parent_loss_diagnostic_v01_points.csv"
    )
    assert audit["status"] == "DIAGNOSTIC_ONLY_NOT_ENDPOINT"
    assert audit["endpoint_authorized"] is False
    assert audit["n_points"] == 3389
    assert audit["n_galaxies"] == 175
    reconstructed = points["v_baseline"] ** 2 / (1.0 - points["loss_required"])
    assert np.allclose(reconstructed, points["vobs"] ** 2, rtol=1e-12, atol=1e-8)
    assert np.allclose(
        points["kappa_required"], np.log(points["gain_required"]), rtol=1e-12
    )
    assert audit["checks"]["all_outputs_finite"] is True


def test_inverse_parent_loss_preserves_nonidentifiability_boundary():
    audit = json.loads(
        (DATA / "inverse_required_parent_loss_diagnostic_v01.json").read_text()
    )
    not_identified = " ".join(audit["identifiability"]["not_identified"])
    assert "parent morphology" in not_identified
    assert "Nature occupation" in not_identified
    assert "component shifts" in audit["identifiability"]["gauge_family"]
