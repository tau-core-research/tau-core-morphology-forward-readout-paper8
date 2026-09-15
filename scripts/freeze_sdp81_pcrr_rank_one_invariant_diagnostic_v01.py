#!/usr/bin/env python3
"""Freeze the PCRR same-source rank-one diagnostic without endpoint access."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from compile_sdp81_common_action_forward_model_v01 import helmert_zero_sum_basis


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
OUT = DATA / "sdp81_pcrr_rank_one_invariant_diagnostic_freeze_v01.json"
REPORT = ROOT / "reports/sdp81_pcrr_rank_one_invariant_diagnostic_freeze_v01.md"


def build_freeze() -> dict:
    path_basis = helmert_zero_sum_basis(4)
    channel_basis = helmert_zero_sum_basis(6)
    checks = {
        "no_endpoint_read": True,
        "four_path_centered_dimension_is_three": path_basis.shape == (4, 3),
        "six_channel_centered_dimension_is_five": channel_basis.shape == (6, 5),
        "path_basis_is_orthonormal_and_centered": bool(
            np.allclose(path_basis.T @ path_basis, np.eye(3))
            and np.allclose(np.ones(4) @ path_basis, 0.0)
        ),
        "channel_basis_is_orthonormal_and_centered": bool(
            np.allclose(channel_basis.T @ channel_basis, np.eye(5))
            and np.allclose(np.ones(6) @ channel_basis, 0.0)
        ),
        "no_fermat_or_parent_depth_input": True,
        "physical_endpoint_remains_unauthorized": True,
    }
    return {
        "schema": "tau-core.paper8.sdp81-pcrr-rank-one-invariant-freeze.v01",
        "status": "SOURCE_METHOD_FROZEN_RETROSPECTIVE_DIAGNOSTIC_ONLY",
        "scientific_role": (
            "depth-free necessary-condition test of the conditional commuting "
            "same-source PCRR family"
        ),
        "source_provenance": {
            "repository": "tau-core-theory",
            "path": "docs/tau_core_cross_scale_clock_resolution_hypothesis_001.md",
            "label": "CSCR-T32d",
            "law": (
                "DC[log z]_in=-(eta_i-mean eta)(lambda_n-mean lambda)/2, "
                "hence rank DC[log z] <= 1"
            ),
            "status": "conditional theorem; physical eta and lambda remain open",
        },
        "endpoint_contract": {
            "path_count": 4,
            "channel_count": 6,
            "channels_one_based": [47, 48, 49, 50, 51, 52],
            "aperture_radius_arcsec": 0.12,
            "observable": "double-centered log spectral matrix",
        },
        "path_centering_basis": path_basis.tolist(),
        "channel_centering_basis": channel_basis.tolist(),
        "statistics": {
            "rank_one_energy_fraction": "sigma_1^2/sum_a sigma_a^2",
            "rank_one_residual_fraction": "sum_{a>1} sigma_a^2/sum_a sigma_a^2",
            "noise_null": "rank-zero Gaussian draws in projected log-mode covariance",
            "rank_one_gof": (
                "Gaussian draws about the observed best Frobenius rank-one matrix, "
                "with rank one refit by SVD on every draw"
            ),
            "bootstrap_draws_per_geometry": 4096,
            "random_seed_base": 20260902,
            "decision_threshold": 0.05,
        },
        "predeclared_interpretation": {
            "rank_zero_rejected_and_rank_one_not_rejected": (
                "rank-one interaction candidate, still non-identifying"
            ),
            "rank_zero_not_rejected": "rank-one component not detected above noise",
            "rank_one_rejected": "commuting scalar-depth PCRR specialization demoted",
        },
        "wrong_family_boundary": (
            "a nonlinear separable spectral filter is also rank one, while a "
            "path-by-mode calibration can create higher rank; rank one alone does "
            "not identify PCRR or Tau"
        ),
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "diagnostic_run_allowed": all(checks.values()),
        "physical_endpoint_authorized": False,
        "retrospective_only": True,
    }


def main() -> None:
    result = build_freeze()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 PCRR rank-one invariant diagnostic freeze v01\n\n"
        f"Status: `{result['status']}`; checks: "
        f"`{result['checks_passed']}/{result['checks_total']}`.\n\n"
        "The source-method freeze declares a basis-invariant SVD test of the "
        "double-centered four-path by six-channel log spectrum. It uses no "
        "Fermat or parent-depth input and reads no endpoint. Rank-zero and fitted "
        "rank-one Gaussian controls are fixed at 4096 draws per covariance "
        "geometry. Rank one is necessary but not sufficient for the conditional "
        "commuting PCRR family.\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
