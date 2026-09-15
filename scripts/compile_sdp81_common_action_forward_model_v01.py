#!/usr/bin/env python3
"""Compile a physical common-action packet into frozen SDP.81 transfers.

This script is source-only.  It never opens the CO spectral endpoint.  In the
current repository the physical manifest is absent, so the expected result is
fail-closed while retaining an executable compiler for a future sourced packet.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
GATE = DATA / "sdp81_parent_path_lift_gate_v01.json"
PHYSICAL_MANIFEST = DATA / "sdp81_parent_lift_physical_source_manifest_v01.json"
OUT = DATA / "sdp81_common_action_forward_model_v01.json"
REPORT = ROOT / "reports/sdp81_common_action_forward_model_v01.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def symmetric_invsqrt(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(matrix)
    if float(values.min()) <= 0.0:
        raise ValueError("matrix must be positive definite")
    return vectors @ np.diag(values ** -0.5) @ vectors.T


def helmert_zero_sum_basis(channel_count: int) -> np.ndarray:
    """Deterministic orthonormal basis for centered log-channel coordinates."""
    if channel_count < 2:
        raise ValueError("at least two channels are required")
    basis = np.zeros((channel_count, channel_count - 1), dtype=float)
    for column in range(channel_count - 1):
        scale = np.sqrt((column + 1) * (column + 2))
        basis[: column + 1, column] = 1.0 / scale
        basis[column + 1, column] = -(column + 1) / scale
    return basis


def compile_transfer(
    hessian: np.ndarray,
    source_dim: int,
    observer_dim: int,
    lift_dim: int,
    interior_dim: int,
    semantics: str,
) -> dict[str, Any]:
    """Apply the CSCR-T32v nested-Schur construction to one path Hessian."""
    boundary_dim = source_dim + observer_dim
    expected_dim = boundary_dim + lift_dim + interior_dim
    if hessian.shape != (expected_dim, expected_dim):
        raise ValueError("common Hessian has the wrong declared dimension")
    if not np.allclose(hessian, hessian.T, atol=1.0e-10, rtol=0.0):
        raise ValueError("common Hessian is not symmetric")
    if float(np.linalg.eigvalsh(hessian).min()) <= 0.0:
        raise ValueError("common Hessian is not positive definite")
    if semantics not in {"fixed_lift", "relaxed_lift"}:
        raise ValueError("transfer semantics must be fixed_lift or relaxed_lift")

    b = slice(0, boundary_dim)
    u = slice(boundary_dim, boundary_dim + lift_dim)
    i = slice(boundary_dim + lift_dim, expected_dim)
    h_bb = hessian[b, b]
    h_bu = hessian[b, u]
    h_bi = hessian[b, i]
    h_uu = hessian[u, u]
    h_ui = hessian[u, i]
    h_ii = hessian[i, i]
    h_ii_inv = np.linalg.inv(h_ii)

    h_p_eff = h_uu - h_ui @ h_ii_inv @ h_ui.T
    s_fixed = h_bb - h_bi @ h_ii_inv @ h_bi.T
    h_bu_eff = h_bu - h_bi @ h_ii_inv @ h_ui.T
    relaxation = h_bu_eff @ np.linalg.solve(h_p_eff, h_bu_eff.T)
    s_relaxed = s_fixed - relaxation
    selected = s_fixed if semantics == "fixed_lift" else s_relaxed

    s_ss = selected[:source_dim, :source_dim]
    s_so = selected[:source_dim, source_dim:]
    s_oo = selected[source_dim:, source_dim:]
    transfer = -symmetric_invsqrt(s_oo) @ s_so.T @ symmetric_invsqrt(s_ss)
    singular_values = np.linalg.svd(transfer, compute_uv=False)
    return {
        "effective_lift_hessian": h_p_eff.tolist(),
        "fixed_boundary_hessian": s_fixed.tolist(),
        "relaxed_boundary_hessian": s_relaxed.tolist(),
        "relaxation_correction": relaxation.tolist(),
        "selected_transfer": transfer.tolist(),
        "maximum_transfer_singular_value": float(singular_values.max()),
        "minimum_common_hessian_eigenvalue": float(np.linalg.eigvalsh(hessian).min()),
        "minimum_effective_lift_eigenvalue": float(np.linalg.eigvalsh(h_p_eff).min()),
        "minimum_selected_boundary_eigenvalue": float(np.linalg.eigvalsh(selected).min()),
        "minimum_relaxation_eigenvalue": float(np.linalg.eigvalsh(relaxation).min()),
    }


def validate_calibration(manifest: dict[str, Any], mode_dim: int, path_ids: list[str]) -> dict[str, Any]:
    calibration = manifest.get("terminal_calibration", {})
    basis = np.asarray(calibration.get("centered_log_channel_basis", []), dtype=float)
    covariances = calibration.get("mode_noise_covariance_by_path", {})
    expected_basis = helmert_zero_sum_basis(mode_dim + 1)
    if basis.shape != expected_basis.shape:
        raise ValueError("terminal channel basis has the wrong shape")
    if not np.allclose(basis.T @ basis, np.eye(mode_dim), atol=1.0e-10):
        raise ValueError("terminal channel basis is not orthonormal")
    if not np.allclose(np.ones(mode_dim + 1) @ basis, 0.0, atol=1.0e-10):
        raise ValueError("terminal channel basis does not remove common gain")
    covariance_out: dict[str, list[list[float]]] = {}
    for path_id in path_ids:
        covariance = np.asarray(covariances.get(path_id, []), dtype=float)
        if covariance.shape != (mode_dim, mode_dim):
            raise ValueError(f"noise covariance missing or malformed for {path_id}")
        if not np.allclose(covariance, covariance.T, atol=1.0e-10):
            raise ValueError(f"noise covariance is not symmetric for {path_id}")
        if float(np.linalg.eigvalsh(covariance).min()) <= 0.0:
            raise ValueError(f"noise covariance is not positive for {path_id}")
        covariance_out[path_id] = covariance.tolist()
    return {"centered_log_channel_basis": basis.tolist(), "mode_noise_covariance_by_path": covariance_out}


def audit_loo_identifiability(
    compiled_paths: list[dict[str, Any]], calibration: dict[str, Any]
) -> dict[str, Any]:
    """Require every three-path training set to identify all source modes."""
    folds = []
    path_ids = [record["path_id"] for record in compiled_paths]
    mode_dim = len(compiled_paths[0]["selected_transfer"])
    for held_out, held_out_id in enumerate(path_ids):
        fisher = np.zeros((mode_dim, mode_dim), dtype=float)
        stacked = []
        for index, record in enumerate(compiled_paths):
            if index == held_out:
                continue
            transfer = np.asarray(record["selected_transfer"], dtype=float)
            covariance = np.asarray(
                calibration["mode_noise_covariance_by_path"][record["path_id"]],
                dtype=float,
            )
            fisher += transfer.T @ np.linalg.inv(covariance) @ transfer
            stacked.append(transfer)
        stacked_matrix = np.vstack(stacked)
        eigenvalues = np.linalg.eigvalsh(fisher)
        rank = int(np.linalg.matrix_rank(stacked_matrix, tol=1.0e-10))
        condition = float(eigenvalues.max() / eigenvalues.min()) if eigenvalues.min() > 0 else float("inf")
        folds.append(
            {
                "held_out_path_id": held_out_id,
                "stacked_transfer_rank": rank,
                "source_mode_dimension": mode_dim,
                "minimum_fisher_eigenvalue": float(eigenvalues.min()),
                "fisher_condition_number": condition,
                "identifiable": rank == mode_dim and eigenvalues.min() > 1.0e-12 and condition < 1.0e12,
            }
        )
    return {"folds": folds, "all_folds_identifiable": all(fold["identifiable"] for fold in folds)}


def main() -> None:
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    source_only = {
        "parent_path_gate_present": GATE.is_file(),
        "parent_path_gate_source_checks_pass": gate.get("source_checks_passed") == gate.get("source_checks_total") == 8,
        "spectral_or_velocity_endpoint_read": False,
    }
    status = "FORMULA_SHELL_DERIVED_ENDPOINT_BLOCKED"
    blocker = "physical common-action manifest absent"
    compiled_paths: list[dict[str, Any]] = []
    calibration: dict[str, Any] | None = None
    endpoint_authorized = False
    manifest_hash = None
    semantics = None
    loo_identifiability = None

    if PHYSICAL_MANIFEST.is_file():
        manifest = json.loads(PHYSICAL_MANIFEST.read_text(encoding="utf-8"))
        manifest_hash = sha256(PHYSICAL_MANIFEST)
        semantics = manifest.get("transfer_semantics")
        dimensions = manifest.get("dimensions", {})
        source_dim = int(dimensions.get("source_mode", 0))
        observer_dim = int(dimensions.get("observer_mode", 0))
        lift_dim = int(dimensions.get("parent_lift", 0))
        interior_dim = int(dimensions.get("internal_channel", 0))
        path_ids = gate.get("observed_4d_path_keys", [])
        try:
            if not gate.get("endpoint_authorized", False):
                raise ValueError("parent-path physical gate is not authorized")
            if source_dim != observer_dim or source_dim != 5:
                raise ValueError("the frozen six-channel score requires 5 centered log modes")
            path_records = {record.get("path_id"): record for record in manifest.get("common_action_paths", [])}
            if set(path_records) != set(path_ids):
                raise ValueError("common-action path set does not match the four observed incidences")
            calibration = validate_calibration(manifest, source_dim, path_ids)
            for path_id in path_ids:
                hessian = np.asarray(path_records[path_id].get("common_postbody_hessian", []), dtype=float)
                compiled = compile_transfer(
                    hessian, source_dim, observer_dim, lift_dim, interior_dim, semantics
                )
                if compiled["maximum_transfer_singular_value"] >= 1.0:
                    raise ValueError(f"compiled transfer is not contractive for {path_id}")
                compiled_paths.append({"path_id": path_id, **compiled})
            loo_identifiability = audit_loo_identifiability(compiled_paths, calibration)
            if not loo_identifiability["all_folds_identifiable"]:
                raise ValueError("three-path training transfers do not identify all source modes")
            status = "FORMULA_FROZEN_ENDPOINT_AUTHORIZED_RETROSPECTIVE_ONLY"
            blocker = None
            endpoint_authorized = True
        except (KeyError, TypeError, ValueError, np.linalg.LinAlgError) as exc:
            blocker = str(exc)

    result = {
        "schema": "tau-core.paper8.sdp81-common-action-forward-model.v01",
        "status": status,
        "scientific_role": "source-only common-action to fixed/relaxed transfer compiler",
        "inputs": {
            "parent_path_gate": str(GATE.relative_to(ROOT)),
            "parent_path_gate_sha256": sha256(GATE),
            "physical_manifest": str(PHYSICAL_MANIFEST.relative_to(ROOT)) if PHYSICAL_MANIFEST.is_file() else None,
            "physical_manifest_sha256": manifest_hash,
            "spectral_or_velocity_endpoint_read": False,
        },
        "source_checks": source_only,
        "transfer_semantics": semantics,
        "compiled_paths": compiled_paths,
        "terminal_calibration": calibration,
        "leave_one_path_out_identifiability": loo_identifiability,
        "endpoint_extraction_freeze": {
            "line": "CO(8-7)",
            "channels_one_based": [47, 48, 49, 50, 51, 52],
            "aperture_radius_arcsec": 0.12,
            "registration_dx_mas": 0.0,
            "registration_dy_mas": 0.0,
            "observable": "five-dimensional centered log spectral shape",
        },
        "endpoint_authorized": endpoint_authorized,
        "retrospective_only": True,
        "blocker": blocker,
        "score_contract": {
            "primary": "leave-one-path-out generalized least-squares prediction of a common source-mode vector",
            "baseline": "lossless identity transfer",
            "wrong_family": "all non-identity permutations of path-to-transfer assignment",
            "metrics": ["held-out Mahalanobis chi2", "held-out Euclidean mode RMSE"],
            "no_post_endpoint_retuning": True,
        },
        "claim_boundary": (
            "Compilation derives transfer matrices only from an independently physical, "
            "gate-authorized common-action manifest. The present absent manifest blocks "
            "endpoint access. Any future SDP.81 score is retrospective because the spectral "
            "cube was opened before this common-action formula freeze; it cannot be reported "
            "as a novel Tau prediction or Nature occupation proof."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 common-action forward-model compiler v01\n\n"
        f"Status: `{status}`.\n\n"
        "The source-only compiler reads no spectral or velocity endpoint. It is ready "
        "to reduce one physically authorized `(B,u,I)` common Hessian per path into "
        "the selected fixed-lift or relaxed-lift transfer and a five-mode centered-log "
        "terminal calibration.\n\n"
        f"Current blocker: `{blocker}`. Endpoint authorized: `{endpoint_authorized}`. "
        "The physical manifest is absent, so no CO cube was opened and no score was emitted.\n\n"
        "Even after future authorization the SDP.81 result will be retrospective: the "
        "spectral endpoint predates this formula freeze. The first confirmatory claim "
        "requires a new untouched multipath endpoint.\n",
        encoding="utf-8",
    )
    print(status)


if __name__ == "__main__":
    main()
