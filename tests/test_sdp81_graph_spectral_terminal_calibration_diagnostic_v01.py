from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from freeze_sdp81_graph_spectral_terminal_calibration_diagnostic_v01 import (  # noqa: E402
    build_freeze,
)


def test_graph_spectral_freeze_is_endpoint_blind_and_canonical() -> None:
    base = json.loads(
        (ROOT / "data/derived/sdp81_4d_corridor_proxy_diagnostic_freeze_v01.json").read_text()
    )
    model = build_freeze(base)
    assert model["inputs"]["spectral_or_velocity_endpoint_read"] is False
    assert model["physical_endpoint_authorized"] is False
    assert model["diagnostic_run_allowed"] is True
    assert model["checks_passed"] == model["checks_total"] == 10
    eigenvalues = np.asarray(model["canonical_graph_eigenvalues"])
    assert np.all(np.diff(eigenvalues) > 0.0)
    assert max(model["commutator_norms"].values()) < 1e-12
    assert len(model["mode_assignment_ensemble"]) == 120


def test_commutation_does_not_select_stiffness_assignment() -> None:
    base = json.loads(
        (ROOT / "data/derived/sdp81_4d_corridor_proxy_diagnostic_freeze_v01.json").read_text()
    )
    model = build_freeze(base)
    monotone = np.asarray(model["candidates"]["wr_t19_graph_monotone_half"]["generator"])
    reverse = np.asarray(model["candidates"]["wr_t19_graph_reverse_half"]["generator"])
    laplacian = np.asarray(model["normalized_path_graph_laplacian"])
    assert not np.allclose(monotone, reverse)
    assert np.allclose(monotone @ laplacian, laplacian @ monotone)
    assert np.allclose(reverse @ laplacian, laplacian @ reverse)


def test_channel_space_operator_is_coordinate_basis_invariant() -> None:
    base = json.loads(
        (ROOT / "data/derived/sdp81_4d_corridor_proxy_diagnostic_freeze_v01.json").read_text()
    )
    model = build_freeze(base)
    basis = np.asarray(model["helmert_basis"])
    generator = np.asarray(
        model["candidates"]["wr_t19_graph_monotone_half"]["generator"]
    )
    # A deterministic orthogonal relabelling of centered coordinates must not
    # alter the induced six-channel operator.
    trial = np.arange(1.0, 26.0).reshape(5, 5)
    rotation, _ = np.linalg.qr(trial)
    rotated_basis = basis @ rotation
    rotated_generator = rotation.T @ generator @ rotation
    assert np.allclose(
        basis @ generator @ basis.T,
        rotated_basis @ rotated_generator @ rotated_basis.T,
    )


def test_retrospective_result_preserves_negative_assignment_result() -> None:
    score = json.loads(
        (ROOT / "data/derived/sdp81_graph_spectral_terminal_calibration_diagnostic_score_v01.json").read_text()
    )
    assert score["status"] == "RETROSPECTIVE_DIAGNOSTIC_ONLY_NOT_ENDPOINT"
    assert score["verdict"] == "CANONICAL_BASIS_DERIVED_MONOTONE_ASSIGNMENT_NOT_SUPPORTED"
    assert score["checks_passed"] == score["checks_total"] == 11
    assert score["physical_endpoint_authorized"] is False
    assert score["confirmatory_prediction"] is False
    assert score["monotone_summary"]["exact_assignment_rank_p_value_range"] == [
        0.375,
        0.4166666666666667,
    ]
    assert score["reverse_summary"]["exact_assignment_rank_p_value_range"] == [
        0.08333333333333333,
        0.3333333333333333,
    ]
    assert score["mode_assignment_summary"]["monotone_rank_range_of_120"] == [39, 81]
    assert score["mode_assignment_summary"]["reverse_rank_range_of_120"] == [55, 97]
    assert score["mode_assignment_summary"]["distinct_best_assignment_count"] == 3
