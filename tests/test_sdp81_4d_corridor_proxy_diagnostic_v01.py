from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from freeze_sdp81_4d_corridor_proxy_diagnostic_v01 import build_proxy  # noqa: E402


def test_proxy_is_source_only_contractive_and_not_physical() -> None:
    descriptor = json.loads(
        (ROOT / "data/derived/sdp81_standard_corridor_descriptor_v01.json").read_text()
    )
    model = build_proxy(descriptor)
    assert model["status"] == "DIAGNOSTIC_ONLY_NOT_ENDPOINT"
    assert model["physical_endpoint_authorized"] is False
    assert model["diagnostic_run_allowed"] is True
    assert model["inputs"]["spectral_or_velocity_endpoint_read"] is False
    assert len(model["compiled_paths"]) == 4
    assert model["checks_passed"] == model["checks_total"]
    for record in model["compiled_paths"]:
        transfer = np.asarray(record["selected_transfer"])
        assert transfer.shape == (5, 5)
        assert np.linalg.eigvalsh(transfer).min() > 0.0
        assert np.linalg.svd(transfer, compute_uv=False).max() < 1.0


def test_freeze_script_reproduces_checked_artifact() -> None:
    subprocess.run(
        [sys.executable, str(SCRIPTS / "freeze_sdp81_4d_corridor_proxy_diagnostic_v01.py")],
        cwd=ROOT,
        check=True,
    )
    model = json.loads(
        (ROOT / "data/derived/sdp81_4d_corridor_proxy_diagnostic_freeze_v01.json").read_text()
    )
    assert model["checks_passed"] == 8
    assert model["checks_total"] == 8


def test_preserved_score_is_negative_and_not_a_physical_endpoint() -> None:
    score = json.loads(
        (ROOT / "data/derived/sdp81_4d_corridor_proxy_diagnostic_score_v01.json").read_text()
    )
    assert score["status"] == "DIAGNOSTIC_ONLY_NOT_ENDPOINT"
    assert score["physical_endpoint_authorized"] is False
    assert score["verdict"] == "FIXED_4D_PROXY_NOT_PREFERRED"
    assert score["scores"]["matched_beats_lossless"] is False
    assert score["scores"]["matched_beats_wrong_median"] is False
    assert score["descriptive_permutation_fraction_not_worse"] > 0.5
