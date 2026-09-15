from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from freeze_sdp81_pcrr_source_hessian_diagnostic_v01 import build_freeze  # noqa: E402


def test_source_freeze_is_endpoint_blind_and_fail_closed() -> None:
    base = json.loads(
        (ROOT / "data/derived/sdp81_4d_corridor_proxy_diagnostic_freeze_v01.json").read_text()
    )
    model = build_freeze(base)
    assert model["inputs"]["spectral_or_velocity_endpoint_read"] is False
    assert model["physical_endpoint_authorized"] is False
    assert model["diagnostic_run_allowed"] is True
    assert model["checks_passed"] == model["checks_total"] == 8
    assert model["candidates"]["pcrr_half_laplacian"][
        "extra_terminal_alignment_assumption"
    ] is False
    assert model["candidates"]["wr_t19_aligned_half"][
        "extra_terminal_alignment_assumption"
    ] is True
    for candidate in model["candidates"].values():
        for transfer in candidate["transfers"]:
            matrix = np.asarray(transfer)
            assert np.linalg.eigvalsh(matrix).min() > 0.0
            assert np.linalg.svd(matrix, compute_uv=False).max() < 1.0


def test_preserved_score_keeps_physical_gate_closed() -> None:
    score = json.loads(
        (ROOT / "data/derived/sdp81_pcrr_source_hessian_diagnostic_score_v01.json").read_text()
    )
    primary = score["primary_summary"]
    assert score["status"] == "RETROSPECTIVE_DIAGNOSTIC_ONLY_NOT_ENDPOINT"
    assert score["physical_endpoint_authorized"] is False
    assert score["confirmatory_prediction"] is False
    assert score["checks_passed"] == score["checks_total"] == 7
    assert primary["matched_beats_lossless_geometries"] == 9
    assert primary["matched_beats_wrong_median_geometries"] == 9
    assert primary["matched_beats_every_wrong_assignment_geometries"] == 0
    assert primary["exact_assignment_p_le_0_05_geometries"] == 0
    assert primary["exact_assignment_rank_p_value_range"] == [0.375, 0.4166666666666667]
