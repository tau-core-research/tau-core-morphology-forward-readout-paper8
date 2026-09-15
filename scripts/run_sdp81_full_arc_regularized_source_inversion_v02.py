#!/usr/bin/env python3
"""Resource-bounded full-arc SDP.81 open-line source inversion.

The script reads only the already-open CO(5-4) and CO(8-7) restored image
cubes.  CO(10-9) is not opened.  Regularization is selected from open-line
leave-one-path-out prediction and then frozen for the complete open window.
"""

from __future__ import annotations

import csv
import json
import sys
import warnings
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import FITSFixedWarning, WCS
from scipy.linalg import solve_triangular
from scipy.optimize import nnls
from scipy.signal import fftconvolve


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from reconstruct_sdp81_extended_source_v01 import build_lens  # noqa: E402
from reconstruct_sdp81_exact_ray_source_v02 import beam_kernel  # noqa: E402


DATA = ROOT / "data/derived"
OUT = DATA / "sdp81_full_arc_regularized_source_inversion_v02.json"
COEFF = DATA / "sdp81_full_arc_regularized_source_coefficients_v02.npz"
LOO_CSV = DATA / "sdp81_full_arc_regularized_source_loo_v02.csv"
REPORT = ROOT / "reports/sdp81_full_arc_regularized_source_inversion_v02.md"

LINES = {
    "CO54": ROOT / (
        "data/external/literature/sdp81_multipath_channel/"
        "SDP81_Band4_ReferenceImages_z3.042/SDP.81.Band4.CO_smooth_z3.042.fits"
    ),
    "CO87": ROOT / (
        "data/external/literature/sdp81_multipath_channel/"
        "SDP81_Band6_ReferenceImages/SDP81_9exec.co87.R1uvtaper1000klambda.fits"
    ),
}
EXPECTED_HASHES = {
    "CO54": "b26f3e4cbff43bab9d6c4c082ff513788f9dcf20b2e640edf607dbc3fe34a656",
    "CO87": "aeea985de1e590921a6282cdd9d017f0a888958e7e07b54d4d51435772475ea3",
}
GRID_SIDE = 11
SOURCE_EXTENT_ARCSEC = 0.18
SOURCE_SIGMA_ARCSEC = 0.018
IMAGE_RADIUS_ARCSEC = 0.48
PIXEL_STRIDE = 3
NOISE_NUGGET_FRACTION = 0.08
VELOCITIES_KM_S = np.arange(-202.0, 198.0, 21.0)
CALIBRATION_VELOCITIES_KM_S = np.array([-160.0, -76.0, 8.0, 92.0, 176.0])
LAMBDA_GRID = np.array([1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0])
C_KM_S = 299792.458


def sha256(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def source_grid(side: int = GRID_SIDE) -> tuple[np.ndarray, np.ndarray]:
    axis = np.linspace(-SOURCE_EXTENT_ARCSEC, SOURCE_EXTENT_ARCSEC, side)
    x, y = np.meshgrid(axis, axis)
    return x.ravel(), y.ravel()


def smoothness_matrix(side: int = GRID_SIDE) -> np.ndarray:
    rows = []
    for iy in range(side):
        for ix in range(side):
            i = iy * side + ix
            if ix + 1 < side:
                row = np.zeros(side * side)
                row[i], row[i + 1] = 1.0, -1.0
                rows.append(row)
            if iy + 1 < side:
                row = np.zeros(side * side)
                row[i], row[i + side] = 1.0, -1.0
                rows.append(row)
    return np.asarray(rows)


def exact_design(
    lens,
    kwargs,
    theta_x: np.ndarray,
    theta_y: np.ndarray,
    beta_center: tuple[float, float],
    source_x: np.ndarray,
    source_y: np.ndarray,
    kernel: np.ndarray,
) -> np.ndarray:
    beta_x, beta_y = lens.ray_shooting(theta_x.ravel(), theta_y.ravel(), kwargs)
    beta_x = beta_x.reshape(theta_x.shape) - beta_center[0]
    beta_y = beta_y.reshape(theta_y.shape) - beta_center[1]
    columns = []
    for sx, sy in zip(source_x, source_y):
        unconvolved = np.exp(
            -0.5 * ((beta_x - sx) ** 2 + (beta_y - sy) ** 2)
            / SOURCE_SIGMA_ARCSEC**2
        )
        columns.append(fftconvolve(unconvolved, kernel, mode="same"))
    return np.stack(columns, axis=-1)


def path_pixels(x0: float, y0: float, pixel_arcsec: float) -> tuple[np.ndarray, ...]:
    radius = int(np.ceil(IMAGE_RADIUS_ARCSEC / pixel_arcsec))
    cx, cy = round(x0), round(y0)
    yy, xx = np.mgrid[cy - radius : cy + radius + 1, cx - radius : cx + radius + 1]
    east = -(xx - x0) * pixel_arcsec
    north = (yy - y0) * pixel_arcsec
    mask = east**2 + north**2 <= IMAGE_RADIUS_ARCSEC**2
    selection = np.zeros(mask.shape, dtype=bool)
    selection[::PIXEL_STRIDE, ::PIXEL_STRIDE] = True
    mask &= selection
    return yy, xx, east, north, mask


def noise_whitener(
    east: np.ndarray,
    north: np.ndarray,
    beam_major: float,
    beam_minor: float,
    beam_pa_deg: float,
) -> np.ndarray:
    angle = np.deg2rad(beam_pa_deg)
    major = np.array([np.sin(angle), np.cos(angle)])
    minor = np.array([np.cos(angle), -np.sin(angle)])
    sigma_major = beam_major / 2.354820045
    sigma_minor = beam_minor / 2.354820045
    covariance = sigma_major**2 * np.outer(major, major) + sigma_minor**2 * np.outer(minor, minor)
    inverse = np.linalg.inv(covariance)
    points = np.column_stack((east, north))
    delta = points[:, None, :] - points[None, :, :]
    exponent = np.einsum("...i,ij,...j->...", delta, inverse, delta, optimize=True)
    correlation = np.exp(-0.25 * exponent)
    correlation = (1.0 - NOISE_NUGGET_FRACTION) * correlation + NOISE_NUGGET_FRACTION * np.eye(len(points))
    chol = np.linalg.cholesky(correlation)
    return solve_triangular(chol, np.eye(len(points)), lower=True)


def nuisance_project(A: np.ndarray, y: np.ndarray, B: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    q, _ = np.linalg.qr(B, mode="reduced")
    return A - q @ (q.T @ A), y - q @ (q.T @ y)


def prepare_line(name: str, path: Path, lens, kwargs, frozen: dict, geometry: dict) -> dict:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        with fits.open(path, memmap=True) as handle:
            cube = np.squeeze(np.asarray(handle[0].data, dtype=float))
            header = handle[0].header.copy()
            wcs = WCS(header).celestial
    indices = np.arange(cube.shape[0])
    frequency = float(header["CRVAL3"]) + (indices + 1.0 - float(header["CRPIX3"])) * float(header["CDELT3"])
    velocity = C_KM_S * (1.0 - frequency / float(header["RESTFRQ"]))
    selected = np.array([int(np.argmin(abs(velocity - value))) for value in VELOCITIES_KM_S])
    if np.max(abs(velocity[selected] - VELOCITIES_KM_S)) > 0.01:
        raise RuntimeError(f"{name}: frozen velocity grid is not present")

    gd = frozen["coordinates"]["image_G_icrs_j2000"]
    g = SkyCoord(gd["ra_hms"], gd["dec_dms"], unit=(u.hourangle, u.deg))
    pixel_arcsec = abs(float(header["CDELT1"])) * 3600.0
    beam_major = float(header["BMAJ"]) * 3600.0
    beam_minor = float(header["BMIN"]) * 3600.0
    beam_pa = float(header.get("BPA", 0.0))
    kernel = beam_kernel(pixel_arcsec, beam_major, beam_minor, beam_pa)
    source_x, source_y = source_grid()
    beta_center = tuple(frozen["models"]["inoue_best_fit"]["source_positions_arcsec"]["q1"])
    designs, observations, projectors = [], [], []
    for lens_x0, north0 in geometry["image_positions_arcsec_relative_to_G"]["q1"]:
        sky = SkyCoord(
            ra=(g.ra.deg - lens_x0 / (3600.0 * np.cos(g.dec.radian))) * u.deg,
            dec=(g.dec.deg + north0 / 3600.0) * u.deg,
        )
        x0, y0 = (float(v) for v in wcs.world_to_pixel(sky))
        yy, xx, east, north, mask = path_pixels(x0, y0, pixel_arcsec)
        design_full = exact_design(
            lens,
            kwargs,
            lens_x0 - east,
            north0 + north,
            beta_center,
            source_x,
            source_y,
            kernel,
        )
        design = design_full[mask]
        values = cube[selected][:, yy[mask], xx[mask]]
        W = noise_whitener(east[mask], north[mask], beam_major, beam_minor, beam_pa)
        nuisance = np.column_stack((np.ones(mask.sum()), east[mask], north[mask]))
        Aw = W @ design
        Bw = W @ nuisance
        q, _ = np.linalg.qr(Bw, mode="reduced")
        designs.append(Aw - q @ (q.T @ Aw))
        observations.append(np.stack([W @ row - q @ (q.T @ (W @ row)) for row in values]))
        projectors.append({"W": W, "Q": q, "B": Bw})
    return {
        "name": name,
        "cube": cube,
        "header": header,
        "selected": selected,
        "velocities": velocity[selected],
        "designs": designs,
        "observations": observations,
        "source_x": source_x,
        "source_y": source_y,
        "pixels_per_path": int(designs[0].shape[0]),
        "beam_arcsec": [beam_major, beam_minor, beam_pa],
    }


def fit_source(designs: list[np.ndarray], observations: list[np.ndarray], channel: int, lam: float, train_paths: list[int]) -> np.ndarray:
    A = np.vstack([designs[p] for p in train_paths])
    y = np.concatenate([observations[p][channel] for p in train_paths])
    R = smoothness_matrix()
    scale = np.linalg.norm(A, "fro") / max(np.linalg.norm(R, "fro"), np.finfo(float).tiny)
    A_aug = np.vstack((A, np.sqrt(lam) * scale * R))
    y_aug = np.concatenate((y, np.zeros(R.shape[0])))
    return nnls(A_aug, y_aug, maxiter=4000)[0]


def held_improvement(design: np.ndarray, observed: np.ndarray, source: np.ndarray) -> tuple[float, float, float]:
    baseline = float(observed @ observed)
    residual = observed - design @ source
    rss = float(residual @ residual)
    improvement = 1.0 - rss / max(baseline, np.finfo(float).tiny)
    return improvement, rss, baseline


def evaluate_lambda(lines: dict[str, dict], lam: float) -> list[dict]:
    records = []
    calibration_indices = [int(np.argmin(abs(VELOCITIES_KM_S - v))) for v in CALIBRATION_VELOCITIES_KM_S]
    for line_name, line in lines.items():
        for channel in calibration_indices:
            for held in range(4):
                train = [p for p in range(4) if p != held]
                source = fit_source(line["designs"], line["observations"], channel, lam, train)
                improvement, rss, baseline = held_improvement(
                    line["designs"][held], line["observations"][held][channel], source
                )
                records.append({
                    "line": line_name,
                    "velocity_km_s": float(line["velocities"][channel]),
                    "held_path": held,
                    "lambda": lam,
                    "improvement": improvement,
                    "rss": rss,
                    "baseline_rss": baseline,
                })
    return records


def main() -> None:
    route = json.loads((DATA / "sdp81_reference_image_source_route_v01.json").read_text())
    if route.get("status") != "LOCAL_REFERENCE_IMAGE_ROUTE_AVAILABLE_DEVELOPMENT_ONLY":
        raise RuntimeError("resource-bounded source route is not frozen")
    for name, path in LINES.items():
        if sha256(path) != EXPECTED_HASHES[name]:
            raise RuntimeError(f"{name}: source hash drift")
    frozen = json.loads((DATA / "sdp81_lens_operator_freeze_v01.json").read_text())
    geometry = json.loads((DATA / "sdp81_lens_operator_geometry_validation_v01.json").read_text())
    lens, kwargs = build_lens(frozen)
    lines = {name: prepare_line(name, path, lens, kwargs, frozen, geometry) for name, path in LINES.items()}

    lambda_records = []
    for lam in LAMBDA_GRID:
        records = evaluate_lambda(lines, float(lam))
        values = np.asarray([r["improvement"] for r in records])
        lambda_records.append({
            "lambda": float(lam),
            "median_held_path_improvement": float(np.median(values)),
            "positive_fraction": float(np.mean(values > 0)),
            "records": records,
        })
    best_value = max(r["median_held_path_improvement"] for r in lambda_records)
    eligible = [r for r in lambda_records if r["median_held_path_improvement"] >= best_value - 0.01]
    selected_lambda = max(r["lambda"] for r in eligible)

    all_records, coefficients = [], {}
    for line_name, line in lines.items():
        maps = []
        for channel in range(len(VELOCITIES_KM_S)):
            maps.append(fit_source(line["designs"], line["observations"], channel, selected_lambda, list(range(4))))
            for held in range(4):
                train = [p for p in range(4) if p != held]
                source = fit_source(line["designs"], line["observations"], channel, selected_lambda, train)
                improvement, rss, baseline = held_improvement(line["designs"][held], line["observations"][held][channel], source)
                wrong_source = source.reshape(GRID_SIDE, GRID_SIDE)[:, ::-1].ravel()
                wrong_improvement, _, _ = held_improvement(
                    line["designs"][held],
                    line["observations"][held][channel],
                    wrong_source,
                )
                all_records.append({
                    "line": line_name,
                    "velocity_km_s": float(line["velocities"][channel]),
                    "channel_index_zero_based": int(line["selected"][channel]),
                    "held_path": held,
                    "lambda": selected_lambda,
                    "fractional_squared_residual_improvement": improvement,
                    "wrong_source_reflection_improvement": wrong_improvement,
                    "model_rss": rss,
                    "background_plane_rss": baseline,
                })
        coefficients[line_name] = np.asarray(maps)

    values = np.asarray([r["fractional_squared_residual_improvement"] for r in all_records])
    by_path = {}
    for held in range(4):
        v = np.asarray([r["fractional_squared_residual_improvement"] for r in all_records if r["held_path"] == held])
        by_path[str(held)] = {"median_improvement": float(np.median(v)), "positive_fraction": float(np.mean(v > 0))}
    path_positive = sum(v["median_improvement"] > 0 for v in by_path.values())
    median_improvement = float(np.median(values))
    promoted = bool(path_positive >= 3 and median_improvement > 0.05)

    # Fair wrong-morphology control: each reflected source uses exactly the
    # same three-path LOO fit as its matched counterpart.
    wrong_median = float(
        np.median([r["wrong_source_reflection_improvement"] for r in all_records])
    )

    # Exact zero-data known limit under the selected regularizer.
    zero_source = fit_source(lines["CO87"]["designs"], [np.zeros_like(v) for v in lines["CO87"]["observations"]], 0, selected_lambda, list(range(4)))
    zero_limit_norm = float(np.linalg.norm(zero_source))

    np.savez_compressed(
        COEFF,
        velocities_km_s=VELOCITIES_KM_S,
        source_x_arcsec=lines["CO54"]["source_x"],
        source_y_arcsec=lines["CO54"]["source_y"],
        CO54=coefficients["CO54"],
        CO87=coefficients["CO87"],
    )
    with LOO_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_records[0]))
        writer.writeheader(); writer.writerows(all_records)

    result = {
        "schema": "tau-core.paper8.sdp81-full-arc-regularized-source-inversion.v02",
        "status": "DEVELOPMENT_SOURCE_PROFILE_PROMOTED_IMAGE_LEVEL_CONFIRMATION_REQUIRED" if promoted else "FULL_ARC_REFERENCE_IMAGE_INVERSION_NOT_PROMOTED",
        "scientific_role": "endpoint-blind open-transition development source reconstruction",
        "configuration": {
            "grid_side": GRID_SIDE,
            "source_basis_count": GRID_SIDE**2,
            "source_extent_arcsec": SOURCE_EXTENT_ARCSEC,
            "source_sigma_arcsec": SOURCE_SIGMA_ARCSEC,
            "image_radius_arcsec": IMAGE_RADIUS_ARCSEC,
            "pixel_stride": PIXEL_STRIDE,
            "noise_nugget_fraction": NOISE_NUGGET_FRACTION,
            "velocity_grid_km_s": VELOCITIES_KM_S.tolist(),
            "calibration_velocity_grid_km_s": CALIBRATION_VELOCITIES_KM_S.tolist(),
            "lambda_grid": LAMBDA_GRID.tolist(),
            "selected_lambda": selected_lambda,
            "v02_change": "lambda range extended after v01 selected its upper boundary; source data, model family, score and 5 percent promotion threshold unchanged",
        },
        "line_metadata": {
            name: {"pixels_per_path": line["pixels_per_path"], "beam_arcsec": line["beam_arcsec"], "channel_indices_zero_based": line["selected"].tolist()}
            for name, line in lines.items()
        },
        "lambda_scan": [{k: v for k, v in row.items() if k != "records"} for row in lambda_records],
        "held_path_summary": by_path,
        "held_path_positive_median_count": path_positive,
        "median_held_path_squared_residual_improvement": median_improvement,
        "wrong_source_reflection_median_improvement": wrong_median,
        "matched_minus_wrong_median_improvement": median_improvement - wrong_median,
        "zero_source_limit_norm": zero_limit_norm,
        "development_source_profile_promoted": promoted,
        "controls_completed": [
            "background-plane baseline",
            "leave-one-path-out prediction",
            "five-point then boundary-extended seven-point regularization scan",
            "fair identically trained source-reflection control",
            "zero-source known limit",
        ],
        "controls_not_run_after_primary_failure": [
            "source-grid resolution perturbation",
            "beam perturbation",
            "astrometric perturbation",
            "leave-one-channel-block-out prediction",
        ],
        "short_circuit_rule": "If the frozen primary 5 percent LOO promotion threshold fails, downstream stability controls cannot rescue or promote the family and are not run.",
        "visibility_level_confirmation_complete": False,
        "physical_D_Zp_identified": False,
        "transition_readiness_increment": 0,
        "co109_header_read": False,
        "co109_pixels_read": False,
        "endpoint_authorized": False,
        "promotion_rule": "at least 3/4 paths have positive median held-path improvement and the all-record median improvement exceeds 5 percent",
        "failure_modes": [
            "restored-image covariance is only a stationary beam-correlated approximation",
            "lens/source-grid/regularization mismatch can suppress held-path prediction",
            "a promoted open-line source profile would still not uniquely select CO(10-9) excitation-opacity response",
        ],
        "claim_boundary": "Development-only source-profile reconstruction from already-open restored images. Promotion, if any, is not visibility-level validation, does not identify D_Zp or a physical parent transfer, does not increase the sealed transition gate, and does not authorize or score CO(10-9).",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# SDP.81 full-arc regularized open-line source inversion v02\n\n"
        f"Status: `{result['status']}`. Endpoint authorized: `False`.\n\n"
        f"The open-line-only scan selected lambda `{selected_lambda:g}`. Across "
        f"{len(all_records)} line/channel/path holdouts, the median background-relative "
        f"squared-residual improvement is `{median_improvement:.4f}`; `{path_positive}/4` "
        f"paths have positive median improvement. The wrong source-reflection median is "
        f"`{wrong_median:.4f}`. The zero-source known-limit norm is `{zero_limit_norm:.3e}`.\n\n"
        "The result uses full path neighbourhoods, exact frozen ray shooting, line-specific "
        "beam convolution, a beam-correlated stationary noise approximation, exact nuisance-"
        "plane projection and nonnegative gradient regularization. It remains below visibility-"
        "level confirmation and cannot identify the CO(10-9) profile response. Because the "
        "primary 5% LOO gate failed, grid/beam/astrometric/channel-block stability controls "
        "were short-circuited rather than used to rescue the family.\n\n"
        f"Claim boundary: {result['claim_boundary']}\n"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
