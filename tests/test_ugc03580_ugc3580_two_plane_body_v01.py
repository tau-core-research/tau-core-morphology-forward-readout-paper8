from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from two_plane_morphology_common_v01 import load_source_geometry, slerp  # noqa: E402


def test_ugc03580_two_plane_body_reproducibility() -> None:
    scripts = [
        "scripts/build_ugc03580_ugc3580_two_plane_body_v01.py",
        "scripts/audit_ugc03580_ugc3580_two_plane_body_reproducibility_v01.py",
    ]
    for script in scripts:
        subprocess.run([sys.executable, script], cwd=ROOT, check=True, capture_output=True)

    summary = json.loads(
        (ROOT / "data/derived/ugc03580_ugc3580_two_plane_body_v01.json").read_text(encoding="utf-8")
    )
    audit = json.loads(
        (ROOT / "data/derived/ugc03580_ugc3580_two_plane_body_reproducibility_audit_v01.json").read_text(
            encoding="utf-8"
        )
    )
    assert summary["status"] == "SOURCE_ACQUISITION_ONLY"
    assert summary["endpoint_allowed"] is False
    assert summary["readout_formula_selected"] is False
    assert summary["validation"]["table4_reproduction_within_one_published_sigma"] is True
    assert audit["status"] == "REPRODUCIBILITY_AUDIT_PASS"
    assert audit["checks_passed"] == audit["checks_total"]


def test_slerp_limits_and_antipodal_degeneracy() -> None:
    north = np.array([0.0, 0.0, 1.0])
    east = np.array([1.0, 0.0, 0.0])
    assert np.allclose(slerp(north, north, 0.37), north)
    assert np.allclose(slerp(north, east, 0.0), north)
    assert np.allclose(slerp(north, east, 1.0), east)
    assert np.isclose(np.linalg.norm(slerp(north, east, 0.5)), 1.0)
    with pytest.raises(ValueError, match="antipodal"):
        slerp(north, -north, 0.5)


def test_source_loader_rejects_endpoint_column(tmp_path: Path) -> None:
    source = ROOT / "data/external/literature/ugc08490_ngc5204_warp/ugc3580_table6_geometry_v01.csv"
    frame = pd.read_csv(source)
    frame["vobs_km_s"] = 0.0
    contaminated = tmp_path / "contaminated.csv"
    frame.to_csv(contaminated, index=False)
    with pytest.raises(ValueError, match="endpoint-bearing"):
        load_source_geometry(contaminated)
