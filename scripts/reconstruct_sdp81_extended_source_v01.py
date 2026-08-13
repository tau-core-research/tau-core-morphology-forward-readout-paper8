#!/usr/bin/env python3
"""Fit one beam-convolved extended source morphology to four SDP.81 q1 paths."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.wcs import FITSFixedWarning
from lenstronomy.LensModel.lens_model import LensModel
from lenstronomy.Util.param_util import phi_q2_ellipticity, shear_polar2cartesian
from scipy.optimize import lsq_linear


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
IMAGE = ROOT / (
    "data/external/literature/sdp81_multipath_channel/"
    "SDP81_Band7_ReferenceImages/SDP81_band7_11exec.contR1.image.fits"
)
OUT = DATA / "sdp81_extended_source_reconstruction_v01.json"
COEFF = DATA / "sdp81_extended_source_coefficients_v01.csv"
REPORT = ROOT / "reports/sdp81_extended_source_reconstruction_v01.md"

GRID_SIDE = 7
SOURCE_EXTENT_ARCSEC = 0.12
SOURCE_SIGMA_ARCSEC = 0.020
IMAGE_RADIUS_ARCSEC = 0.15
RIDGE_FRACTION = 1e-3


def build_lens(frozen: dict) -> tuple[LensModel, list[dict]]:
    model = frozen["models"]["inoue_best_fit"]
    e1, e2 = phi_q2_ellipticity(
        np.deg2rad(90.0 + model["ellipticity_pa_deg_ccw_from_north"]),
        model["axis_ratio_q"],
    )
    gamma1, gamma2 = shear_polar2cartesian(
        np.deg2rad(model["external_shear_pa_deg_ccw_from_north"]),
        model["external_shear_gamma"],
    )
    cx, cy = model["lens_center_arcsec_relative_to_G"]
    return LensModel(["SIE", "SHEAR"]), [
        {
            "theta_E": model["einstein_radius_b_arcsec"],
            "e1": e1,
            "e2": e2,
            "center_x": cx,
            "center_y": cy,
        },
        {
            "gamma1": gamma1,
            "gamma2": gamma2,
            "ra_0": 0.0,
            "dec_0": 0.0,
        },
    ]


def source_grid() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    axis = np.linspace(-SOURCE_EXTENT_ARCSEC, SOURCE_EXTENT_ARCSEC, GRID_SIDE)
    x, y = np.meshgrid(axis, axis)
    return axis, x.ravel(), y.ravel()


def smoothness_matrix(side: int) -> np.ndarray:
    rows = []
    for y in range(side):
        for x in range(side):
            index = y * side + x
            if x + 1 < side:
                row = np.zeros(side * side)
                row[index] = 1.0
                row[index + 1] = -1.0
                rows.append(row)
            if y + 1 < side:
                row = np.zeros(side * side)
                row[index] = 1.0
                row[index + side] = -1.0
                rows.append(row)
    return np.asarray(rows)


def gaussian_design(
    east: np.ndarray,
    north: np.ndarray,
    source_x: np.ndarray,
    source_y: np.ndarray,
    jacobian: np.ndarray,
    beam_covariance: np.ndarray,
) -> np.ndarray:
    inverse_jacobian = np.linalg.inv(jacobian)
    pre_covariance = (
        SOURCE_SIGMA_ARCSEC**2
        * inverse_jacobian
        @ inverse_jacobian.T
    )
    convolved_covariance = pre_covariance + beam_covariance
    inverse_covariance = np.linalg.inv(convolved_covariance)
    amplitude = np.sqrt(
        abs(np.linalg.det(pre_covariance)) / np.linalg.det(convolved_covariance)
    )
    source_offsets = np.column_stack((source_x, source_y))
    image_centers = source_offsets @ inverse_jacobian.T
    points = np.column_stack((east, north))
    delta = points[:, None, :] - image_centers[None, :, :]
    exponent = np.einsum(
        "nki,ij,nkj->nk", delta, inverse_covariance, delta, optimize=True
    )
    return amplitude * np.exp(-0.5 * exponent)


def fit_nonnegative(
    designs: list[np.ndarray],
    observations: list[np.ndarray],
    shared_source: bool,
) -> tuple[float, list[float], np.ndarray]:
    source_count = GRID_SIDE**2
    if shared_source:
        source_blocks = 1
        source_columns = source_count
    else:
        source_blocks = len(designs)
        source_columns = source_count * source_blocks
    row_count = sum(len(values) for values in observations)
    matrix = np.zeros((row_count, source_columns + len(designs)))
    target = np.concatenate(observations)
    start = 0
    for path_index, design in enumerate(designs):
        stop = start + len(design)
        source_start = 0 if shared_source else path_index * source_count
        matrix[start:stop, source_start : source_start + source_count] = design
        matrix[start:stop, source_columns + path_index] = 1.0
        start = stop

    smooth = smoothness_matrix(GRID_SIDE)
    scale = RIDGE_FRACTION * np.linalg.norm(matrix[:, :source_columns], ord=2)
    regularizer = np.zeros(
        (smooth.shape[0] * source_blocks, source_columns + len(designs))
    )
    for block in range(source_blocks):
        first = block * smooth.shape[0]
        regularizer[first : first + smooth.shape[0], block * source_count : (block + 1) * source_count] = (
            scale * smooth
        )
    augmented_matrix = np.vstack((matrix, regularizer))
    augmented_target = np.concatenate((target, np.zeros(len(regularizer))))
    lower = np.concatenate((np.zeros(source_columns), np.full(len(designs), -np.inf)))
    upper = np.full(source_columns + len(designs), np.inf)
    solution = lsq_linear(
        augmented_matrix,
        augmented_target,
        bounds=(lower, upper),
        lsmr_tol="auto",
        max_iter=500,
    ).x
    prediction = matrix @ solution
    residual = target - prediction
    relative_residual = float(np.linalg.norm(residual) / np.linalg.norm(target))
    path_residuals = []
    start = 0
    for values in observations:
        stop = start + len(values)
        path_residuals.append(
            float(
                np.linalg.norm(residual[start:stop])
                / np.linalg.norm(target[start:stop])
            )
        )
        start = stop
    return relative_residual, path_residuals, solution


def main() -> None:
    frozen = json.loads(
        (DATA / "sdp81_lens_operator_freeze_v01.json").read_text(encoding="utf-8")
    )
    registration = json.loads(
        (DATA / "sdp81_image_g_wcs_registration_v01.json").read_text(encoding="utf-8")
    )
    lens, kwargs = build_lens(frozen)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        with fits.open(IMAGE) as hdul:
            image = np.squeeze(hdul[0].data).astype(float)
            header = hdul[0].header

    pixel_arcsec = abs(float(header["CDELT1"])) * 3600.0
    beam_major = float(header["BMAJ"]) * 3600.0
    beam_minor = float(header["BMIN"]) * 3600.0
    beam_pa = np.deg2rad(float(header.get("BPA", 0.0)))
    rotation = np.array(
        [[np.sin(beam_pa), np.cos(beam_pa)], [np.cos(beam_pa), -np.sin(beam_pa)]]
    )
    beam_sigma = np.diag(
        [(beam_major / 2.354820045) ** 2, (beam_minor / 2.354820045) ** 2]
    )
    beam_covariance = rotation @ beam_sigma @ rotation.T

    _, source_x, source_y = source_grid()
    designs = []
    observations = []
    jacobian_determinants = []
    for path in registration["q1_paths"]:
        x0 = path["pixel_x_zero_based"]
        y0 = path["pixel_y_zero_based"]
        radius_pixels = int(np.ceil(IMAGE_RADIUS_ARCSEC / pixel_arcsec))
        cx, cy = round(x0), round(y0)
        yy, xx = np.mgrid[
            cy - radius_pixels : cy + radius_pixels + 1,
            cx - radius_pixels : cx + radius_pixels + 1,
        ]
        lens_x = (xx - x0) * pixel_arcsec
        north = (yy - y0) * pixel_arcsec
        mask = lens_x**2 + north**2 <= IMAGE_RADIUS_ARCSEC**2
        f_xx, f_xy, f_yx, f_yy = lens.hessian(
            path["lens_x_west_offset_arcsec"],
            path["north_offset_arcsec"],
            kwargs,
        )
        jacobian = np.array(
            [[1.0 - f_xx, -f_xy], [-f_yx, 1.0 - f_yy]]
        )
        jacobian_determinants.append(float(np.linalg.det(jacobian)))
        designs.append(
            gaussian_design(
                lens_x[mask],
                north[mask],
                source_x,
                source_y,
                jacobian,
                beam_covariance,
            )
        )
        observations.append(image[yy, xx][mask])

    common_residual, common_path_residuals, common_solution = fit_nonnegative(
        designs, observations, shared_source=True
    )
    independent_residual, independent_path_residuals, _ = fit_nonnegative(
        designs, observations, shared_source=False
    )
    source_coefficients = common_solution[: GRID_SIDE**2]
    coefficient_rows = [
        {
            "source_x_arcsec_relative_to_q1": float(x),
            "source_y_arcsec_relative_to_q1": float(y),
            "nonnegative_intensity_coefficient": float(value),
        }
        for x, y, value in zip(source_x, source_y, source_coefficients)
    ]
    import csv

    with COEFF.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(coefficient_rows[0]))
        writer.writeheader()
        writer.writerows(coefficient_rows)

    common_to_independent_excess = (
        common_residual**2 - independent_residual**2
    ) / independent_residual**2
    promoted = bool(
        common_residual < 0.5
        and max(common_path_residuals) < 0.65
        and common_to_independent_excess < 0.5
    )
    result = {
        "schema": "tau_core.paper8.sdp81-extended-source-reconstruction.v01",
        "model": {
            "source_grid_side": GRID_SIDE,
            "source_basis_count": GRID_SIDE**2,
            "source_extent_arcsec": SOURCE_EXTENT_ARCSEC,
            "source_gaussian_sigma_arcsec": SOURCE_SIGMA_ARCSEC,
            "image_radius_arcsec": IMAGE_RADIUS_ARCSEC,
            "beam_convolution": True,
            "nonnegative_source": True,
            "smoothness_ridge_fraction": RIDGE_FRACTION,
        },
        "path_count": len(designs),
        "jacobian_determinants": jacobian_determinants,
        "common_source_relative_residual": common_residual,
        "common_source_path_relative_residuals": common_path_residuals,
        "independent_source_relative_residual": independent_residual,
        "independent_source_path_relative_residuals": independent_path_residuals,
        "common_vs_independent_squared_residual_excess": common_to_independent_excess,
        "common_extended_source_promoted": promoted,
        "promotion_rule": (
            "common residual < 0.5, every path residual < 0.65, and common squared "
            "residual no more than 50% above independent-path source fits"
        ),
        "body_covector_materialized": False,
        "time_covector_identified": False,
        "time_score_authorized": False,
        "verdict": (
            "COMMON_BEAM_CONVOLVED_EXTENDED_SOURCE_SUPPORTED"
            if promoted
            else "COMMON_BEAM_CONVOLVED_EXTENDED_SOURCE_NOT_YET_SUPPORTED"
        ),
        "claim_boundary": (
            "Fixed-basis local source-morphology reconstruction only; not a unique "
            "body map, time covector, channel innovation, or Tau Core detection."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 extended source reconstruction v01\n\n"
        f"Verdict: `{result['verdict']}`\n\n"
        f"The shared beam-convolved source fit has relative residual "
        f"`{common_residual:.3f}` versus `{independent_residual:.3f}` for four "
        "independent path-specific source fits. The common-source squared-residual "
        f"excess is `{common_to_independent_excess:.3f}`.\n\n"
        "This fixed-basis reconstruction tests whether extended morphology repairs "
        "the failed local-gradient approximation. It does not identify an observer-"
        "time covector.\n",
        encoding="utf-8",
    )
    print(result["verdict"])


if __name__ == "__main__":
    main()
