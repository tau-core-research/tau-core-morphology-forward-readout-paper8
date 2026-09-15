from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_sdp81_4d_corridor_proxy_covariance_robustness_v01 import (  # noqa: E402
    log_mode_covariances,
)


def test_delta_method_covariance_is_positive_and_scale_invariant() -> None:
    rng = np.random.default_rng(20260902)
    raw = rng.normal(size=(6, 6))
    covariance = raw @ raw.T + 0.2 * np.eye(6)
    basis = np.linalg.qr(np.column_stack([np.ones(6), rng.normal(size=(6, 5))]))[0][:, 1:]
    fluxes = np.asarray([[1.0, 1.2, 0.9, 1.4, 1.1, 1.3]])
    first = log_mode_covariances(fluxes, basis, covariance)[0]
    scale = 7.0
    second = log_mode_covariances(scale * fluxes, basis, scale**2 * covariance)[0]
    assert np.linalg.eigvalsh(first).min() > 0.0
    assert np.allclose(first, second)


def test_preserved_covariance_result_is_diagnostic_and_inconclusive() -> None:
    result = json.loads(
        (ROOT / "data/derived/sdp81_4d_corridor_proxy_covariance_robustness_v01.json").read_text()
    )
    assert result["status"] == "DIAGNOSTIC_ONLY_NOT_ENDPOINT"
    assert result["physical_endpoint_authorized"] is False
    assert result["checks_passed"] == result["checks_total"] == 6
    assert result["summary"]["matched_beats_lossless_geometries"] < 9
    assert result["summary"]["matched_beats_every_wrong_assignment_geometries"] == 0
    assert result["summary"]["frozen_unit_scale_is_posthoc_best_geometries"] < 9
    assert result["summary"]["posthoc_retuning_allowed"] is False
