#!/usr/bin/env python3
"""Freeze a source-only 4D corridor proxy for an SDP.81 sensitivity diagnostic.

This is deliberately not a Tau parent transfer.  It maps the conventional
relative Fermat coordinate through one fixed ordered-channel roughness
generator so that the already implemented common-source score can be tested
without manufacturing a physical parent-action manifest.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from compile_sdp81_common_action_forward_model_v01 import (
    audit_loo_identifiability,
    helmert_zero_sum_basis,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
DESCRIPTOR = DATA / "sdp81_standard_corridor_descriptor_v01.json"
OUT = DATA / "sdp81_4d_corridor_proxy_diagnostic_freeze_v01.json"
REPORT = ROOT / "reports/sdp81_4d_corridor_proxy_diagnostic_freeze_v01.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ordered_channel_generator(channel_count: int = 6) -> tuple[np.ndarray, np.ndarray]:
    """Return the Helmert basis and the unit-norm path-graph Laplacian on it."""
    basis = helmert_zero_sum_basis(channel_count)
    difference = np.zeros((channel_count - 1, channel_count), dtype=float)
    for row in range(channel_count - 1):
        difference[row, row] = -1.0
        difference[row, row + 1] = 1.0
    laplacian = difference.T @ difference
    reduced = basis.T @ laplacian @ basis
    reduced /= float(np.linalg.eigvalsh(reduced).max())
    return basis, reduced


def exp_symmetric(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(matrix)
    return vectors @ np.diag(np.exp(values)) @ vectors.T


def build_proxy(descriptor: dict) -> dict:
    paths = descriptor["paths"]
    span = float(descriptor["summary"]["relative_fermat_span_arcsec2"])
    if span <= 0.0 or len(paths) != 4:
        raise ValueError("the frozen comparator must contain four paths and positive span")
    basis, generator = ordered_channel_generator(6)
    mode_dim = generator.shape[0]
    compiled_paths = []
    for record in paths:
        relative_coordinate = float(record["relative_fermat_potential_arcsec2"]) / span
        # The common +1 origin makes every finite witness strictly contractive.
        # It is not a physical depth: because it is common and the generator is
        # shared, it is an invertible source reparameterization in the LOO score.
        proxy_depth = 1.0 + relative_coordinate
        transfer = exp_symmetric(-proxy_depth * generator)
        compiled_paths.append(
            {
                "path_id": record["path_id"],
                "relative_4d_fermat_coordinate": relative_coordinate,
                "proxy_depth": proxy_depth,
                "selected_transfer": transfer.tolist(),
                "maximum_transfer_singular_value": float(
                    np.linalg.svd(transfer, compute_uv=False).max()
                ),
            }
        )
    calibration = {
        "centered_log_channel_basis": basis.tolist(),
        "mode_noise_covariance_by_path": {
            record["path_id"]: np.eye(mode_dim).tolist() for record in compiled_paths
        },
        "covariance_status": (
            "identity sensitivity metric; values called Mahalanobis chi2 are not "
            "calibrated statistical chi-square variables"
        ),
    }
    identifiability = audit_loo_identifiability(compiled_paths, calibration)
    checks = {
        "standard_descriptor_is_source_only": descriptor["inputs"][
            "spectral_or_velocity_endpoint_read"
        ]
        is False,
        "direct_parent_identification_remains_forbidden": descriptor[
            "direct_parent_contraction_identification_allowed"
        ]
        is False,
        "four_paths": len(compiled_paths) == 4,
        "five_centered_log_modes": mode_dim == 5,
        "generator_is_positive_on_centered_modes": bool(
            np.linalg.eigvalsh(generator).min() > 0.0
        ),
        "all_proxy_transfers_are_strict_contractions": all(
            item["maximum_transfer_singular_value"] < 1.0 for item in compiled_paths
        ),
        "every_loo_fold_is_identifiable": identifiability["all_folds_identifiable"],
        "no_spectral_endpoint_read": True,
    }
    return {
        "schema": "tau-core.paper8.sdp81-4d-corridor-proxy-diagnostic-freeze.v01",
        "status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
        "scientific_role": (
            "retrospective sensitivity control for one fixed 4D-corridor proxy; "
            "not a Tau parent-distance or parent-action model"
        ),
        "inputs": {
            "standard_corridor_descriptor": str(DESCRIPTOR.relative_to(ROOT)),
            "standard_corridor_descriptor_sha256": sha256(DESCRIPTOR),
            "spectral_or_velocity_endpoint_read": False,
        },
        "proxy_definition": {
            "relative_coordinate": "r_i=(phi_i-min_j phi_j)/(max_j phi_j-min_j phi_j)",
            "ordered_channel_generator": "K=U^T D^T D U/lambda_max(D^T D)",
            "transfer": "C_i=exp[-(1+r_i)K]",
            "common_depth_origin_note": (
                "the +1 is a common invertible source reparameterization, not an "
                "identified physical depth"
            ),
        },
        "generator": generator.tolist(),
        "compiled_paths": compiled_paths,
        "terminal_calibration": calibration,
        "leave_one_path_out_identifiability": identifiability,
        "endpoint_extraction_freeze": {
            "line": "CO(8-7)",
            "channels_one_based": [47, 48, 49, 50, 51, 52],
            "aperture_radius_arcsec": 0.12,
            "registration_dx_mas": 0.0,
            "registration_dy_mas": 0.0,
            "observable": "five-dimensional centered log spectral shape",
        },
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "physical_endpoint_authorized": False,
        "diagnostic_run_allowed": all(checks.values()),
        "retrospective_only": True,
        "claim_boundary": (
            "The conventional 4D Fermat coordinate is used only as a proxy label. "
            "It is not retyped as parent distance, and the resulting contractions "
            "are not claimed to be Nature-owned Tau transfers. A score can reject or "
            "motivate this fixed proxy family only; it cannot validate Tau Core."
        ),
    }


def main() -> None:
    descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
    result = build_proxy(descriptor)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 fixed 4D-corridor proxy diagnostic freeze v01\n\n"
        f"Status: `{result['status']}`; checks: "
        f"`{result['checks_passed']}/{result['checks_total']}`.\n\n"
        "This source-only freeze maps the conventional relative Fermat coordinate "
        "through one normalized ordered-channel Laplacian. It reads no CO spectral "
        "endpoint and has no fitted coefficient. The construction is a sensitivity "
        "control, not a physical Tau parent transfer.\n\n"
        f"{result['claim_boundary']}\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
