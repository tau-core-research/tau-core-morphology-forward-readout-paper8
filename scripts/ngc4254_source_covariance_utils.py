#!/usr/bin/env python3
"""Beam-matching utilities for the NGC4254 source-only map products."""

from __future__ import annotations

import math
import re

import numpy as np
from scipy.signal import fftconvolve


FWHM_TO_SIGMA = 1.0 / (2.0 * math.sqrt(2.0 * math.log(2.0)))


def aips_clean_beam_from_header(header) -> tuple[float, float, float]:
    """Read an AIPS CLEAN beam from standard cards or FITS HISTORY.

    Returns major/minor FWHM in arcseconds and position angle in degrees.
    """

    if all(header.get(key) is not None for key in ("BMAJ", "BMIN", "BPA")):
        return (
            float(header["BMAJ"]) * 3600.0,
            float(header["BMIN"]) * 3600.0,
            float(header["BPA"]),
        )
    pattern = re.compile(
        r"CLEAN\s+BMAJ=\s*([0-9.Ee+-]+)\s+BMIN=\s*([0-9.Ee+-]+)\s+BPA=\s*([0-9.Ee+-]+)"
    )
    history = header.get("HISTORY", [])
    lines = [history] if isinstance(history, str) else list(history)
    for line in lines:
        match = pattern.search(str(line))
        if match:
            return (
                float(match.group(1)) * 3600.0,
                float(match.group(2)) * 3600.0,
                float(match.group(3)),
            )
    raise ValueError("No AIPS CLEAN BMAJ/BMIN/BPA beam found in FITS header")


def beam_covariance_pixels(
    fwhm_major_arcsec: float,
    fwhm_minor_arcsec: float,
    pa_deg_east_of_north: float,
    pixel_scale_arcsec: float,
) -> np.ndarray:
    """Return the Gaussian beam covariance in ``(x_pixel, y_pixel)`` order.

    The NGC4254 VIVA grid has increasing x toward west. Position angle is the
    astronomical east-of-north convention, so the major-axis pixel vector is
    ``(-sin(PA), cos(PA))``.
    """

    values = (
        fwhm_major_arcsec,
        fwhm_minor_arcsec,
        pixel_scale_arcsec,
    )
    if not all(math.isfinite(value) and value > 0.0 for value in values):
        raise ValueError("Beam widths and pixel scale must be finite and positive")
    if fwhm_major_arcsec < fwhm_minor_arcsec:
        raise ValueError("The major-axis FWHM must not be smaller than the minor axis")

    pa = math.radians(pa_deg_east_of_north)
    major = np.array([-math.sin(pa), math.cos(pa)], dtype=float)
    minor = np.array([math.cos(pa), math.sin(pa)], dtype=float)
    sigma_major = fwhm_major_arcsec * FWHM_TO_SIGMA / pixel_scale_arcsec
    sigma_minor = fwhm_minor_arcsec * FWHM_TO_SIGMA / pixel_scale_arcsec
    return (
        sigma_major**2 * np.outer(major, major)
        + sigma_minor**2 * np.outer(minor, minor)
    )


def gaussian_kernel_from_covariance(
    covariance_xy_pixels: np.ndarray,
    truncate_sigma: float = 5.0,
) -> np.ndarray:
    """Build a normalized 2D Gaussian kernel from an x/y covariance matrix."""

    covariance = np.asarray(covariance_xy_pixels, dtype=float)
    if covariance.shape != (2, 2):
        raise ValueError("Gaussian covariance must be a 2x2 matrix")
    if not np.allclose(covariance, covariance.T, atol=1.0e-12):
        raise ValueError("Gaussian covariance must be symmetric")
    eigenvalues = np.linalg.eigvalsh(covariance)
    if float(np.min(eigenvalues)) <= 0.0:
        raise ValueError("Gaussian covariance must be positive definite")
    if not math.isfinite(truncate_sigma) or truncate_sigma <= 0.0:
        raise ValueError("Kernel truncation must be finite and positive")

    radius = max(1, int(math.ceil(truncate_sigma * math.sqrt(float(np.max(eigenvalues))))))
    y, x = np.mgrid[-radius : radius + 1, -radius : radius + 1]
    coordinates = np.stack([x, y], axis=-1)
    exponent = np.einsum(
        "...i,ij,...j->...", coordinates, np.linalg.inv(covariance), coordinates
    )
    kernel = np.exp(-0.5 * exponent)
    kernel /= float(np.sum(kernel))
    return kernel


def matching_kernel(
    target_covariance_xy_pixels: np.ndarray,
    native_covariance_xy_pixels: np.ndarray | None = None,
    truncate_sigma: float = 5.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the Gaussian kernel taking a native beam to a target beam."""

    target = np.asarray(target_covariance_xy_pixels, dtype=float)
    native = (
        np.zeros((2, 2), dtype=float)
        if native_covariance_xy_pixels is None
        else np.asarray(native_covariance_xy_pixels, dtype=float)
    )
    difference = 0.5 * ((target - native) + (target - native).T)
    kernel = gaussian_kernel_from_covariance(difference, truncate_sigma=truncate_sigma)
    return kernel, difference


def normalized_convolution(
    data: np.ndarray,
    kernel: np.ndarray,
    valid: np.ndarray | None = None,
    minimum_coverage: float = 0.5,
) -> tuple[np.ndarray, np.ndarray]:
    """Convolve finite data while normalizing over missing-map support."""

    values = np.asarray(data, dtype=float)
    if valid is None:
        support = np.isfinite(values)
    else:
        support = np.asarray(valid, dtype=bool) & np.isfinite(values)
    if support.shape != values.shape:
        raise ValueError("Data and validity mask shapes differ")
    if not 0.0 < minimum_coverage <= 1.0:
        raise ValueError("minimum_coverage must lie in (0,1]")

    numerator = fftconvolve(np.where(support, values, 0.0), kernel, mode="same")
    coverage = fftconvolve(support.astype(float), kernel, mode="same")
    output = np.full(values.shape, np.nan, dtype=float)
    keep = coverage >= minimum_coverage
    output[keep] = numerator[keep] / coverage[keep]
    return output, coverage


def beam_overlap_correlation(
    normalized_masks: list[np.ndarray],
    beam_covariance_xy_pixels: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float]:
    """Integrate the exact Gaussian beam autocorrelation over fixed masks."""

    if not normalized_masks:
        raise ValueError("At least one mask is required")
    autocorrelation_kernel = gaussian_kernel_from_covariance(
        2.0 * np.asarray(beam_covariance_xy_pixels, dtype=float)
    )
    convolved = [
        fftconvolve(np.asarray(mask, dtype=float), autocorrelation_kernel, mode="same")
        for mask in normalized_masks
    ]
    raw = np.zeros((len(normalized_masks), len(normalized_masks)), dtype=float)
    for row_index, row_mask in enumerate(normalized_masks):
        for column_index, column_blur in enumerate(convolved):
            raw[row_index, column_index] = float(np.sum(row_mask * column_blur))
    raw = 0.5 * (raw + raw.T)
    diagonal = np.sqrt(np.diag(raw))
    correlation = raw / np.outer(diagonal, diagonal)
    correlation = 0.5 * (correlation + correlation.T)
    eigenvalues = np.linalg.eigvalsh(correlation)[::-1]
    if not np.allclose(np.diag(correlation), 1.0, atol=1.0e-12):
        raise ValueError("Beam-overlap matrix does not have unit diagonal")
    if float(np.min(eigenvalues)) < -1.0e-10:
        raise ValueError("Beam-overlap matrix is not positive semidefinite")
    effective_rank = float(np.sum(eigenvalues) ** 2 / np.sum(eigenvalues**2))
    return correlation, eigenvalues, effective_rank
