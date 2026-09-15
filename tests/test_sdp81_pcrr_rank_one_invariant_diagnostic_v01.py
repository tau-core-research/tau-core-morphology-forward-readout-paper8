from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from freeze_sdp81_pcrr_rank_one_invariant_diagnostic_v01 import build_freeze  # noqa: E402
from run_sdp81_pcrr_rank_one_invariant_diagnostic_v01 import singular_statistics  # noqa: E402


def test_freeze_is_depth_free_endpoint_blind_and_fail_closed() -> None:
    model = build_freeze()
    assert model["status"] == "SOURCE_METHOD_FROZEN_RETROSPECTIVE_DIAGNOSTIC_ONLY"
    assert model["physical_endpoint_authorized"] is False
    assert model["diagnostic_run_allowed"] is True
    assert model["checks_passed"] == model["checks_total"] == 7
    assert model["checks"]["no_fermat_or_parent_depth_input"] is True


def test_singular_statistic_recovers_exact_rank_one() -> None:
    matrix = np.outer(np.asarray([1.0, -2.0, 0.5]), np.arange(1.0, 6.0))
    stats = singular_statistics(matrix)
    assert np.isclose(stats["rank_one_energy_fraction"], 1.0)
    assert np.isclose(stats["rank_one_residual_fraction"], 0.0)


def test_preserved_result_is_compatible_but_not_detected() -> None:
    result = json.loads(
        (ROOT / "data/derived/sdp81_pcrr_rank_one_invariant_diagnostic_score_v01.json").read_text()
    )
    assert result["verdict"] == "RANK_ONE_COMPATIBLE_NOT_DETECTED_NOT_IDENTIFYING"
    assert result["physical_endpoint_authorized"] is False
    assert result["confirmatory_prediction"] is False
    assert result["checks_passed"] == result["checks_total"] == 6
    assert result["summary"]["rank_zero_rejected_geometries"] == 0
    assert result["summary"]["rank_one_rejected_geometries"] == 0
