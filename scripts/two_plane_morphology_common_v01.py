#!/usr/bin/env python3
"""Source-only spherical geometry utilities for tilted-ring body proxies."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "radius_arcsec",
    "radius_kpc_source",
    "radius_kpc_error",
    "sigma_hi_msun_pc2",
    "sigma_hi_error",
    "inclination_deg",
    "inclination_error_deg",
    "pa_deg",
    "pa_error_deg",
    "n_w",
    "n_w_error",
    "n_n",
    "n_n_error",
    "n_los",
    "n_los_error",
    "tip_deg",
    "tip_error_deg",
    "lon_deg",
    "lon_error_deg",
}

FORBIDDEN_ENDPOINT_FRAGMENTS = (
    "vobs",
    "vrot",
    "residual",
    "sparc",
    "rotation_model",
)


def load_source_geometry(path: Path) -> pd.DataFrame:
    """Load a source table and reject endpoint-bearing schemas."""

    frame = pd.read_csv(path)
    missing = sorted(REQUIRED_COLUMNS - set(frame.columns))
    if missing:
        raise ValueError(f"missing source geometry columns: {missing}")
    lowered = [column.lower() for column in frame.columns]
    forbidden = [
        column
        for column in lowered
        if any(fragment in column for fragment in FORBIDDEN_ENDPOINT_FRAGMENTS)
    ]
    if forbidden:
        raise ValueError(f"endpoint-bearing columns are forbidden: {forbidden}")
    if not np.all(np.diff(frame["radius_arcsec"].to_numpy(dtype=float)) > 0.0):
        raise ValueError("source radii must be strictly increasing")
    if not np.isfinite(frame.select_dtypes(include=[np.number]).to_numpy()).all():
        raise ValueError("source geometry contains non-finite numeric values")
    return frame


def orientation_normal(inclination_deg: np.ndarray, pa_deg: np.ndarray) -> np.ndarray:
    """Return (west, north, line-of-sight) unit normals from tilted-ring angles."""

    inclination = np.deg2rad(np.asarray(inclination_deg, dtype=float))
    pa = np.deg2rad(np.asarray(pa_deg, dtype=float))
    normals = np.column_stack(
        (
            np.sin(inclination) * np.sin(pa),
            -np.sin(inclination) * np.cos(pa),
            np.cos(inclination),
        )
    )
    return unit_rows(normals)


def unit_rows(vectors: np.ndarray) -> np.ndarray:
    values = np.asarray(vectors, dtype=float)
    norms = np.linalg.norm(values, axis=-1, keepdims=True)
    if np.any(norms <= 0.0):
        raise ValueError("zero vector cannot define a plane orientation")
    return values / norms


def angle_deg(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    left = np.asarray(a, dtype=float)
    right = np.asarray(b, dtype=float)
    dots = np.sum(left * right, axis=-1)
    return np.rad2deg(np.arccos(np.clip(dots, -1.0, 1.0)))


def chordal_mean(normals: np.ndarray, weights: np.ndarray | None = None) -> np.ndarray:
    values = unit_rows(normals)
    if weights is None:
        mean = np.sum(values, axis=0)
    else:
        w = np.asarray(weights, dtype=float)
        if w.ndim != 1 or len(w) != len(values) or np.any(w < 0.0) or not np.any(w > 0.0):
            raise ValueError("weights must be a nonnegative nonzero vector")
        mean = np.sum(values * w[:, None], axis=0)
    return unit_rows(mean[None, :])[0]


def slerp(a: np.ndarray, b: np.ndarray, fraction: float) -> np.ndarray:
    """Shortest great-circle interpolation between two unit normals."""

    if not 0.0 <= fraction <= 1.0:
        raise ValueError("fraction must lie in [0, 1]")
    left = unit_rows(np.asarray(a, dtype=float)[None, :])[0]
    right = unit_rows(np.asarray(b, dtype=float)[None, :])[0]
    dot = float(np.clip(np.dot(left, right), -1.0, 1.0))
    if dot < -1.0 + 1.0e-12:
        raise ValueError("antipodal planes do not select a unique shortest geodesic")
    theta = math.acos(dot)
    if theta < 1.0e-12:
        return left.copy()
    sin_theta = math.sin(theta)
    value = (
        math.sin((1.0 - fraction) * theta) / sin_theta * left
        + math.sin(fraction * theta) / sin_theta * right
    )
    return unit_rows(value[None, :])[0]


def connection_diagnostics(radii_kpc: np.ndarray, normals: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return adjacent great-circle angle and angular gradient at each row."""

    radii = np.asarray(radii_kpc, dtype=float)
    values = unit_rows(normals)
    segment_angle = np.full(len(radii), np.nan, dtype=float)
    segment_gradient = np.full(len(radii), np.nan, dtype=float)
    for index in range(1, len(radii)):
        delta_r = radii[index] - radii[index - 1]
        if delta_r <= 0.0:
            raise ValueError("radii must be strictly increasing")
        segment_angle[index] = float(angle_deg(values[index], values[index - 1]))
        segment_gradient[index] = segment_angle[index] / delta_r
    return segment_angle, segment_gradient


def max_slerp_norm_error(normals: np.ndarray, samples_per_segment: int = 17) -> float:
    values = unit_rows(normals)
    maximum = 0.0
    for left, right in zip(values[:-1], values[1:]):
        for fraction in np.linspace(0.0, 1.0, samples_per_segment):
            interpolated = slerp(left, right, float(fraction))
            maximum = max(maximum, abs(float(np.linalg.norm(interpolated)) - 1.0))
    return maximum


def radial_zone(radius_arcsec: float) -> str:
    if radius_arcsec <= 150.0:
        return "inner_reference_plane"
    if radius_arcsec < 240.0:
        return "transition"
    if radius_arcsec <= 375.0:
        return "outer_plane_support"
    return "beyond_source_terminal_support"


def plane_defect(normals: np.ndarray, plane: np.ndarray) -> np.ndarray:
    """Return the nonnegative chordal plane defect ``1 - n dot plane``."""

    values = unit_rows(np.asarray(normals, dtype=float))
    reference = unit_rows(np.asarray(plane, dtype=float)[None, :])[0]
    return 1.0 - np.clip(values @ reference, -1.0, 1.0)


def two_plane_barycentric_kernel(
    normals: np.ndarray,
    inner_plane: np.ndarray,
    outer_plane: np.ndarray,
    *,
    power: float = 1.0,
    separation_tolerance: float = 1.0e-12,
) -> np.ndarray:
    """Return a bounded source-coordinate between two oriented planes.

    The two-plane morphology is declared inactive when the reference planes
    coincide.  Otherwise the coordinate is

    ``d_inner**power / (d_inner**power + d_outer**power)``.

    This routine selects no terminal carrier, sign, or coupling strength.
    """

    if not math.isfinite(power) or power <= 0.0:
        raise ValueError("power must be finite and strictly positive")
    inner = unit_rows(np.asarray(inner_plane, dtype=float)[None, :])[0]
    outer = unit_rows(np.asarray(outer_plane, dtype=float)[None, :])[0]
    if 1.0 - float(np.clip(np.dot(inner, outer), -1.0, 1.0)) <= separation_tolerance:
        return np.zeros(len(np.asarray(normals)), dtype=float)
    d_inner = plane_defect(normals, inner)
    d_outer = plane_defect(normals, outer)
    numerator = np.power(d_inner, power)
    denominator = numerator + np.power(d_outer, power)
    if np.any(denominator <= 0.0):
        raise ValueError("nondegenerate two-plane defects must have positive sum")
    return np.clip(numerator / denominator, 0.0, 1.0)


def fixed_inclination_projection_ratio_sq(
    inclination_deg: np.ndarray,
    reference_inclination_deg: float,
) -> np.ndarray:
    """Standard circular-ring projection factor for a fixed-inclination reducer.

    If a line-of-sight circular speed from a ring of inclination ``i(R)`` is
    reduced with a fixed inclination ``i0``, the inferred squared speed is
    multiplied by ``[sin(i(R))/sin(i0)]**2``.  This is a conventional geometry
    control, not a Tau-specific readout law.
    """

    reference_sine = math.sin(math.radians(float(reference_inclination_deg)))
    if abs(reference_sine) <= 1.0e-12:
        raise ValueError("face-on reference cannot define a stable deprojection ratio")
    values = np.sin(np.deg2rad(np.asarray(inclination_deg, dtype=float))) / reference_sine
    return np.square(values)
