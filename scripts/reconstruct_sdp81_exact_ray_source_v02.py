#!/usr/bin/env python3
"""Fit one extended SDP.81 source with exact nonlinear lens ray shooting."""

from __future__ import annotations

import csv
import json
import sys
import warnings
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.wcs import FITSFixedWarning
from scipy.signal import fftconvolve


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from reconstruct_sdp81_extended_source_v01 import (  # noqa: E402
    GRID_SIDE,
    IMAGE_RADIUS_ARCSEC,
    SOURCE_SIGMA_ARCSEC,
    build_lens,
    fit_nonnegative,
    source_grid,
)


DATA = ROOT / "data/derived"
IMAGE = ROOT / (
    "data/external/literature/sdp81_multipath_channel/"
    "SDP81_Band7_ReferenceImages/SDP81_band7_11exec.contR1.image.fits"
)
OUT = DATA / "sdp81_exact_ray_source_reconstruction_v02.json"
COEFF = DATA / "sdp81_exact_ray_source_coefficients_v02.csv"
REPORT = ROOT / "reports/sdp81_exact_ray_source_reconstruction_v02.md"


def beam_kernel(
    pixel_arcsec: float,
    beam_major: float,
    beam_minor: float,
    beam_pa_deg: float,
) -> np.ndarray:
    sigma_major = beam_major / 2.354820045
    sigma_minor = beam_minor / 2.354820045
    angle = np.deg2rad(beam_pa_deg)
    major = np.array([np.sin(angle), np.cos(angle)])
    minor = np.array([np.cos(angle), -np.sin(angle)])
    covariance = (
        sigma_major**2 * np.outer(major, major)
        + sigma_minor**2 * np.outer(minor, minor)
    )
    inverse = np.linalg.inv(covariance)
    radius_pixels = int(np.ceil(4.0 * sigma_major / pixel_arcsec))
    yy, xx = np.mgrid[
        -radius_pixels : radius_pixels + 1,
        -radius_pixels : radius_pixels + 1,
    ]
    east = -xx * pixel_arcsec
    north = yy * pixel_arcsec
    points = np.stack((east, north), axis=-1)
    exponent = np.einsum("...i,ij,...j->...", points, inverse, points)
    kernel = np.exp(-0.5 * exponent)
    return kernel / kernel.sum()


def exact_path_design(
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
    for center_x, center_y in zip(source_x, source_y):
        unconvolved = np.exp(
            -0.5
            * (
                (beta_x - center_x) ** 2
                + (beta_y - center_y) ** 2
            )
            / SOURCE_SIGMA_ARCSEC**2
        )
        columns.append(fftconvolve(unconvolved, kernel, mode="same"))
    return np.stack(columns, axis=-1)


def main() -> None:
    frozen = json.loads(
        (DATA / "sdp81_lens_operator_freeze_v01.json").read_text(encoding="utf-8")
    )
    registration = json.loads(
        (DATA / "sdp81_image_g_wcs_registration_v01.json").read_text(encoding="utf-8")
    )
    lens, kwargs = build_lens(frozen)
    beta_center = tuple(
        frozen["models"]["inoue_best_fit"]["source_positions_arcsec"]["q1"]
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        with fits.open(IMAGE) as hdul:
            image = np.squeeze(hdul[0].data).astype(float)
            header = hdul[0].header

    pixel_arcsec = abs(float(header["CDELT1"])) * 3600.0
    kernel = beam_kernel(
        pixel_arcsec,
        float(header["BMAJ"]) * 3600.0,
        float(header["BMIN"]) * 3600.0,
        float(header.get("BPA", 0.0)),
    )
    _, source_x, source_y = source_grid()
    designs = []
    observations = []
    pixel_counts = []
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
        full_design = exact_path_design(
            lens,
            kwargs,
            path["lens_x_west_offset_arcsec"] + lens_x,
            path["north_offset_arcsec"] + north,
            beta_center,
            source_x,
            source_y,
            kernel,
        )
        designs.append(full_design[mask])
        observations.append(image[yy, xx][mask])
        pixel_counts.append(int(mask.sum()))

    common_residual, common_path_residuals, common_solution = fit_nonnegative(
        designs, observations, shared_source=True
    )
    independent_residual, independent_path_residuals, _ = fit_nonnegative(
        designs, observations, shared_source=False
    )
    excess = (
        common_residual**2 - independent_residual**2
    ) / independent_residual**2
    promoted = bool(
        common_residual < 0.5
        and max(common_path_residuals) < 0.65
        and excess < 0.5
    )
    rows = [
        {
            "source_x_arcsec_relative_to_q1": float(x),
            "source_y_arcsec_relative_to_q1": float(y),
            "nonnegative_intensity_coefficient": float(value),
        }
        for x, y, value in zip(
            source_x, source_y, common_solution[: GRID_SIDE**2]
        )
    ]
    with COEFF.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    result = {
        "schema": "tau_core.paper8.sdp81-exact-ray-source-reconstruction.v02",
        "mapping": "exact lenstronomy ray_shooting plus image-plane ALMA beam convolution",
        "path_count": len(designs),
        "pixels_per_path": pixel_counts,
        "source_basis_count": GRID_SIDE**2,
        "common_source_relative_residual": common_residual,
        "common_source_path_relative_residuals": common_path_residuals,
        "independent_source_relative_residual": independent_residual,
        "independent_source_path_relative_residuals": independent_path_residuals,
        "common_vs_independent_squared_residual_excess": excess,
        "common_extended_source_promoted": promoted,
        "promotion_rule": (
            "common residual < 0.5, every path residual < 0.65, and common squared "
            "residual no more than 50% above independent-path source fits"
        ),
        "body_covector_materialized": False,
        "time_covector_identified": False,
        "time_score_authorized": False,
        "verdict": (
            "EXACT_RAY_COMMON_EXTENDED_SOURCE_SUPPORTED"
            if promoted
            else "EXACT_RAY_COMMON_EXTENDED_SOURCE_NOT_YET_SUPPORTED"
        ),
        "claim_boundary": (
            "Fixed-basis exact-ray morphology reconstruction; not a unique body map, "
            "time covector, channel innovation, or Tau Core detection."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 exact-ray source reconstruction v02\n\n"
        f"Verdict: `{result['verdict']}`\n\n"
        f"The exact-ray common-source residual is `{common_residual:.3f}` versus "
        f"`{independent_residual:.3f}` for independent path sources. The squared-"
        f"residual excess is `{excess:.3f}`.\n\n"
        "This replaces the local-Jacobian rendering while preserving the frozen "
        "source basis, positivity, beam model, apertures, and promotion rule.\n",
        encoding="utf-8",
    )
    print(result["verdict"])


if __name__ == "__main__":
    main()
