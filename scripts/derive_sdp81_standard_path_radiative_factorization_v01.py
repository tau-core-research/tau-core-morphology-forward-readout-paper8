#!/usr/bin/env python3
"""Derive the endpoint-blind standard path/radiative factorization for SDP.81.

The script reads only the frozen smooth-lens model and the already registered
q1 image positions.  It does not open continuum or line pixels, and in
particular it does not inspect the sealed CO(10-9) FITS member.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
NUMBA_CACHE = Path("/private/tmp/tau_core_numba_cache")
NUMBA_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("NUMBA_CACHE_DIR", str(NUMBA_CACHE))
sys.path.insert(0, str(ROOT / "scripts"))
from reconstruct_sdp81_extended_source_v01 import (  # noqa: E402
    SOURCE_SIGMA_ARCSEC,
    build_lens,
    source_grid,
)


DATA = ROOT / "data/derived"
LENS_FREEZE = DATA / "sdp81_lens_operator_freeze_v01.json"
REGISTRATION = DATA / "sdp81_image_g_wcs_registration_v01.json"
OUT = DATA / "sdp81_standard_path_radiative_factorization_v01.json"
REPORT = ROOT / "reports/sdp81_standard_path_radiative_factorization_v01.md"

APERTURE_RADIUS_ARCSEC = 0.12
QUADRATURE_STEP_ARCSEC = 0.005


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def helmert_zero_sum_basis(channel_count: int) -> np.ndarray:
    basis = np.zeros((channel_count, channel_count - 1), dtype=float)
    for column in range(channel_count - 1):
        scale = np.sqrt((column + 1) * (column + 2))
        basis[: column + 1, column] = 1.0 / scale
        basis[column + 1, column] = -(column + 1) / scale
    return basis


def path_functional(
    lens,
    kwargs: list[dict],
    image_x: float,
    image_y: float,
    beta_center: tuple[float, float],
    source_x: np.ndarray,
    source_y: np.ndarray,
) -> tuple[np.ndarray, int]:
    axis = np.arange(
        -APERTURE_RADIUS_ARCSEC,
        APERTURE_RADIUS_ARCSEC + 0.5 * QUADRATURE_STEP_ARCSEC,
        QUADRATURE_STEP_ARCSEC,
    )
    dx, dy = np.meshgrid(axis, axis)
    mask = dx**2 + dy**2 <= APERTURE_RADIUS_ARCSEC**2
    theta_x = image_x + dx[mask]
    theta_y = image_y + dy[mask]
    beta_x, beta_y = lens.ray_shooting(theta_x, theta_y, kwargs)
    beta_x = beta_x[:, None] - beta_center[0]
    beta_y = beta_y[:, None] - beta_center[1]
    design = np.exp(
        -0.5
        * (
            (beta_x - source_x[None, :]) ** 2
            + (beta_y - source_y[None, :]) ** 2
        )
        / SOURCE_SIGMA_ARCSEC**2
    )
    return design.sum(axis=0) * QUADRATURE_STEP_ARCSEC**2, int(mask.sum())


def main() -> None:
    frozen = json.loads(LENS_FREEZE.read_text(encoding="utf-8"))
    registration = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    lens, kwargs = build_lens(frozen)
    beta_center = tuple(
        frozen["models"]["inoue_best_fit"]["source_positions_arcsec"]["q1"]
    )
    _, source_x, source_y = source_grid()

    rows = []
    sample_counts = []
    for path in registration["q1_paths"]:
        row, count = path_functional(
            lens,
            kwargs,
            float(path["lens_x_west_offset_arcsec"]),
            float(path["north_offset_arcsec"]),
            beta_center,
            source_x,
            source_y,
        )
        rows.append(row)
        sample_counts.append(count)
    path_matrix = np.asarray(rows)
    row_norms = np.linalg.norm(path_matrix, axis=1)
    normalized = path_matrix / row_norms[:, None]
    singular_values = np.linalg.svd(normalized, compute_uv=False)
    rank = int(np.linalg.matrix_rank(normalized, tol=1.0e-10))
    cosine = normalized @ normalized.T

    # STRAD-T1 separable-source control.  If S_nk(Z)=p_n f_k(Z), then
    # every achromatic path contributes only one common scalar gain, which
    # centered log-channel coordinates remove exactly.
    radius2 = source_x**2 + source_y**2
    spatial_template = np.exp(-0.5 * radius2 / 0.055**2)
    spatial_template /= spatial_template.sum()
    baseline_spectrum = np.asarray([1.0, 1.2, 1.5, 1.35, 1.1, 0.85])
    basis = helmert_zero_sum_basis(6)
    separable_jacobians = []
    baseline_fluxes = []
    for row in path_matrix:
        gain = float(row @ spatial_template)
        flux = gain * baseline_spectrum
        raw = gain * np.diag(baseline_spectrum) @ basis
        j_log = basis.T @ np.diag(1.0 / flux) @ raw
        baseline_fluxes.append(flux)
        separable_jacobians.append(j_log)
    separable_spread = max(
        float(np.linalg.norm(a - b, ord="fro"))
        for a in separable_jacobians
        for b in separable_jacobians
    )

    # Same standard lens reduct, but a spatially varying derivative for each
    # spectral mode.  This is a countermodel to any inference that pathwise
    # centered-log differences uniquely identify parent loss.
    centers = [0, 6, 24, 42, 48]
    derivative_templates = []
    for center in centers:
        dx = source_x - source_x[center]
        dy = source_y - source_y[center]
        q = np.exp(-0.5 * (dx**2 + dy**2) / 0.035**2)
        q /= q.sum()
        derivative_templates.append(q)
    derivative_templates = np.column_stack(derivative_templates)
    coupled_jacobians = []
    for row, flux in zip(path_matrix, baseline_fluxes):
        mode_gains = row @ derivative_templates
        raw = np.diag(baseline_spectrum) @ basis @ np.diag(mode_gains)
        coupled_jacobians.append(basis.T @ np.diag(1.0 / flux) @ raw)
    coupled_spread = max(
        float(np.linalg.norm(a - b, ord="fro"))
        for a in coupled_jacobians
        for b in coupled_jacobians
    )

    checks = {
        "four_registered_standard_paths": path_matrix.shape == (4, 49),
        "all_path_functionals_finite_nonzero": bool(
            np.all(np.isfinite(path_matrix)) and np.all(row_norms > 0.0)
        ),
        "path_matrix_rank_is_four": rank == 4,
        "per_channel_spatial_nullity_is_45": 49 - rank == 45,
        "centered_log_separable_gain_cancels": separable_spread < 1.0e-12,
        "spatial_spectral_coupling_can_create_path_dependence": coupled_spread > 1.0e-3,
        "no_spectral_or_velocity_endpoint_read": True,
        "no_co109_header_or_pixel_read": True,
    }
    result = {
        "schema": "tau-core.paper8.sdp81-standard-path-radiative-factorization.v01",
        "status": (
            "STANDARD_PATH_FUNCTIONAL_DERIVED_RADIATIVE_MIXED_JET_OPEN"
            if all(checks.values())
            else "STANDARD_PATH_FACTORIZATION_AUDIT_FAILED"
        ),
        "scientific_role": (
            "endpoint-blind separation of standard lens/aperture transport from the "
            "source radiative mixed jet; not a parent transfer"
        ),
        "source_provenance": [
            {"artifact": str(LENS_FREEZE.relative_to(ROOT)), "sha256": sha256(LENS_FREEZE)},
            {"artifact": str(REGISTRATION.relative_to(ROOT)), "sha256": sha256(REGISTRATION)},
        ],
        "discretized_forward_law": (
            "F_i,k(Z)=sum_n L_i,n S_n,k(Z); "
            "[D_Z Phi_i]_k,a=sum_n L_i,n [D_Z S]_n,k,a"
        ),
        "typed_boundary": {
            "L_i": "ordinary 4D smooth-lens plus aperture surface-brightness functional",
            "D_Z_S": "source radiative mixed jet from five parent/body modes to 49x6 source emission coefficients",
            "parent_loss_identified_by_L_i": False,
        },
        "quadrature": {
            "aperture_radius_arcsec": APERTURE_RADIUS_ARCSEC,
            "step_arcsec": QUADRATURE_STEP_ARCSEC,
            "samples_per_path": sample_counts,
            "beam_convolution_included": False,
            "spectral_response_included": False,
        },
        "standard_path_functional_arcsec2": path_matrix.tolist(),
        "normalized_path_functional": normalized.tolist(),
        "normalized_singular_values": singular_values.tolist(),
        "rank": rank,
        "per_channel_spatial_nullity": 49 - rank,
        "path_cosine_similarity": cosine.tolist(),
        "separable_source_control": {
            "maximum_pairwise_centered_log_jacobian_spread": separable_spread,
            "all_paths_reduce_to_identity": all(
                np.allclose(jacobian, np.eye(5), atol=1.0e-12, rtol=0.0)
                for jacobian in separable_jacobians
            ),
        },
        "spatial_spectral_countermodel": {
            "maximum_pairwise_centered_log_jacobian_spread": coupled_spread,
            "same_standard_lens_and_aperture_reduct": True,
            "parent_loss_present": False,
        },
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "remaining_object": (
            "a source-owned CO(10-9) radiative mixed jet D_Z S, plus the frozen "
            "CO(10-9) beam/spectral response and noise covariance"
        ),
        "claim_boundary": (
            "The standard four-path geometry is now an explicit linear functional. "
            "It neither supplies the parent mixed jet nor identifies path differences "
            "as parent loss. Spatial-spectral source structure is a complete standard-"
            "physics alternative and must be propagated as a control."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 standard path/radiative factorization v01\n\n"
        f"Status: `{result['status']}`. Checks: `{result['checks_passed']}/"
        f"{result['checks_total']}`. No spectral endpoint or sealed CO(10-9) "
        "header/pixels were read.\n\n"
        "For source coefficients $S_{nk}(Z)$ and the ordinary smooth-lens plus "
        "aperture functional $L_{in}$,\n\n"
        "$$F_{ik}(Z)=\\sum_n L_{in}S_{nk}(Z),\\qquad "
        "[D_Z\\Phi_i]_{ka}=\\sum_n L_{in}[D_ZS]_{nka}. $$\n\n"
        f"The normalized four-by-49 path matrix has rank `{rank}`, leaving a "
        f"`{49-rank}`-dimensional spatial null per channel. In the separable "
        f"control the maximum pathwise centered-log Jacobian spread is "
        f"`{separable_spread:.3e}`; common path gain cancels exactly. In the "
        "same-lens spatial--spectral countermodel it is "
        f"`{coupled_spread:.3e}` without parent loss.\n\n"
        "Therefore a nontrivial multipath spectral difference is not by itself "
        "evidence for parent attenuation. The remaining physical object is a "
        "source-owned CO(10-9) radiative mixed jet $D_ZS$, followed by the frozen "
        "line-specific beam/spectral response and covariance.\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
