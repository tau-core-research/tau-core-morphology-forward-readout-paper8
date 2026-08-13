#!/usr/bin/env python3
"""Audit morphology-phase four-role charts for the NGC4254 FFL inverse.

This source-only v06 replaces sky-PA quadrants by roles anchored to either the
stellar m=1 or m=2 phase.  It projects the six inherited annular role vectors
onto the first two modes of the already frozen H I beam-overlap matrix, then
tests the finite v03 source-systematic family and the v05 partial measurement
model without opening any velocity or residual endpoint.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS

from freeze_ngc4254_ffl_determinant_photometric_v02 import (
    geometry_variants,
    variant_geometry,
)
from freeze_ngc4254_ffl_determinant_source_vectors_v01 import E_S_BASIS
from ngc4254_source_covariance_utils import (
    beam_covariance_pixels,
    beam_overlap_correlation,
    gaussian_kernel_from_covariance,
)
from propagate_ngc4254_ffl_partial_measurement_covariance_v05 import (
    correlated_standard,
    positive_field,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

GEOMETRY_PATH = DATA / "ngc4254_s4g_photometric_geometry_freeze_v02.json"
COMMON_PATH = DATA / "ngc4254_common_hi_resolution_source_cube_v03.fits"
BEAM_PATH = DATA / "ngc4254_ffl_determinant_beam_overlap_correlation_v02.csv"
UNCERTAINTY_PATH = DATA / "ngc4254_measurement_uncertainty_fields_v05.fits"
UNCERTAINTY_META_PATH = DATA / "ngc4254_measurement_uncertainty_fields_v05.json"

SYSTEMATICS_PATH = DATA / "ngc4254_ffl_morphology_phase_role_systematics_v06.csv"
MEASUREMENT_PATH = DATA / "ngc4254_ffl_morphology_phase_role_measurement_v06.csv"
SUMMARY_PATH = DATA / "ngc4254_ffl_morphology_phase_role_summary_v06.csv"
JSON_PATH = DATA / "ngc4254_ffl_morphology_phase_roles_v06.json"
REPORT_PATH = REPORTS / "ngc4254_ffl_morphology_phase_roles_v06.md"

STATUS = "SOURCE_ONLY_MORPHOLOGY_PHASE_ROLE_AUDIT_COMPLETE_NO_ENDPOINT"
CLAIM_BOUNDARY = (
    "finite source-only audit of m=1/m=2 phase-anchored inverse role charts; "
    "not a parent role identification, physical q_det, complete covariance, "
    "channel/time/quantum signal, dark-matter replacement, or endpoint score"
)
HARMONICS = (1, 2)
N_BEAM_MODES = 2
PHASE_STABILITY_LIMIT_DEG = 22.5
ROLE_EDGE_PERTURBATION_DEG = 0.5
H2_CONVERSION_FACTORS = (0.7, 1.0, 1.3)
RANDOM_SEED = 425406
N_DRAWS = 256
MEASUREMENT_SCENARIOS = (
    "star_only",
    "co_independent_only",
    "star_plus_co_independent",
    "star_co_plus_hi_ctl49",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def centered(values: np.ndarray) -> np.ndarray:
    return values - float(np.mean(values))


def phase_distance_rad(first: float, second: float, harmonic: int) -> float:
    return abs(float(np.angle(np.exp(1j * harmonic * (first - second))))) / harmonic


def role_index(theta: np.ndarray, anchor: float) -> np.ndarray:
    return np.floor(np.mod(theta - anchor, 2.0 * math.pi) / (0.5 * math.pi)).astype(int)


def beam_modes() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    table = pd.read_csv(BEAM_PATH)
    n = int(max(table["row_radial_index"].max(), table["column_radial_index"].max())) + 1
    matrix = np.zeros((n, n), dtype=float)
    matrix[
        table["row_radial_index"].to_numpy(dtype=int),
        table["column_radial_index"].to_numpy(dtype=int),
    ] = table["beam_overlap_correlation_proxy"].to_numpy(dtype=float)
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    for index in range(eigenvectors.shape[1]):
        vector = eigenvectors[:, index]
        pivot = int(np.argmax(np.abs(vector)))
        if vector[pivot] < 0.0:
            eigenvectors[:, index] = -vector
    return matrix, eigenvalues, eigenvectors


def disk_coordinates(
    geometry: dict[str, object], shape: tuple[int, int], wcs: WCS
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    y, x = np.indices(shape, dtype=float)
    ra, dec = wcs.pixel_to_world_values(x, y)
    ra0, dec0 = (float(value) for value in geometry["center_icrs_deg"])
    pa = math.radians(float(geometry["position_angle_deg_east_of_north"]))
    inclination = math.radians(float(geometry["inclination_deg"]))
    east = (ra - ra0) * math.cos(math.radians(dec0)) * 3600.0
    north = (dec - dec0) * 3600.0
    major = east * math.sin(pa) + north * math.cos(pa)
    minor = -east * math.cos(pa) + north * math.sin(pa)
    deprojected_minor = minor / math.cos(inclination)
    radius = np.hypot(major, deprojected_minor)
    theta = np.mod(np.arctan2(deprojected_minor, major), 2.0 * math.pi)
    path = math.sin(inclination) * np.sin(theta)
    return radius, theta, path


def morphology_phase(
    star: np.ndarray,
    radius: np.ndarray,
    theta: np.ndarray,
    edges: list[float],
    harmonic: int,
) -> tuple[float, float, float, float]:
    finite = np.isfinite(star) & np.isfinite(radius) & np.isfinite(theta) & (star > 0.0)
    log_star = np.full(star.shape, np.nan, dtype=float)
    log_star[finite] = np.log(star[finite])
    contrast = np.full(star.shape, np.nan, dtype=float)
    for radius_lo, radius_hi in zip(edges[:-1], edges[1:]):
        annulus = finite & (radius >= radius_lo) & (radius < radius_hi)
        if np.count_nonzero(annulus) == 0:
            raise ValueError(f"Empty phase annulus {radius_lo:g}-{radius_hi:g}")
        contrast[annulus] = log_star[annulus] - float(np.median(log_star[annulus]))
    support = finite & np.isfinite(contrast) & (radius >= edges[0]) & (radius < edges[-1])
    denominator = float(np.sum(np.abs(contrast[support])))
    if denominator == 0.0:
        raise ValueError("Stellar morphology contrast has zero phase norm")
    coefficient = np.sum(
        contrast[support] * np.exp(1j * harmonic * theta[support])
    ) / denominator
    anchor = float(np.angle(coefficient) / harmonic)

    flux = star[support]
    angular = np.exp(1j * harmonic * theta[support])
    flux_coefficient = np.sum(flux * angular) / np.sum(flux) - np.mean(angular)
    flux_anchor = float(np.angle(flux_coefficient) / harmonic)
    estimator_difference = phase_distance_rad(anchor, flux_anchor, harmonic)
    return anchor, float(abs(coefficient)), flux_anchor, estimator_difference


def candidate_rows(
    geometry: dict[str, object],
    star: np.ndarray,
    h2: np.ndarray,
    hi: np.ndarray,
    wcs: WCS,
    harmonic: int,
    radial_eigenvectors: np.ndarray,
    *,
    h2_scale: float = 1.0,
    anchor_offset_rad: float = 0.0,
) -> tuple[list[dict[str, object]], dict[str, float]]:
    if star.shape != h2.shape or star.shape != hi.shape:
        raise ValueError("Source fields do not share one grid")
    edges = [float(value) for value in geometry["radial_edges_arcsec"]]
    radius, theta, path = disk_coordinates(geometry, star.shape, wcs)
    gas = h2_scale * h2 + hi
    finite = (
        np.isfinite(star)
        & np.isfinite(gas)
        & np.isfinite(radius)
        & np.isfinite(theta)
        & (star > 0.0)
        & (gas > 0.0)
    )
    anchor, amplitude, flux_anchor, estimator_difference = morphology_phase(
        star, radius, theta, edges, harmonic
    )
    used_anchor = anchor + anchor_offset_rad
    roles = role_index(theta, used_anchor)

    u_annuli = []
    v_annuli = []
    eta_annuli = []
    counts_annuli = []
    for radius_lo, radius_hi in zip(edges[:-1], edges[1:]):
        annulus = finite & (radius >= radius_lo) & (radius < radius_hi)
        counts = np.asarray(
            [np.count_nonzero(annulus & (roles == role)) for role in range(4)],
            dtype=int,
        )
        if np.any(counts == 0):
            raise ValueError(
                f"m={harmonic} phase chart has an empty role in {radius_lo:g}-{radius_hi:g} arcsec"
            )
        u = np.asarray(
            [np.median(path[annulus & (roles == role)]) for role in range(4)],
            dtype=float,
        )
        v = np.log(
            np.asarray(
                [np.median(star[annulus & (roles == role)]) for role in range(4)],
                dtype=float,
            )
        )
        eta = np.log(
            np.asarray(
                [np.median(gas[annulus & (roles == role)]) for role in range(4)],
                dtype=float,
            )
        )
        u_annuli.append(centered(u))
        v_annuli.append(centered(v))
        eta_annuli.append(centered(eta))
        counts_annuli.append(counts)

    u_annuli_array = np.asarray(u_annuli, dtype=float)
    v_annuli_array = np.asarray(v_annuli, dtype=float)
    eta_annuli_array = np.asarray(eta_annuli, dtype=float)
    rows = []
    for beam_mode in range(N_BEAM_MODES):
        radial_weights = radial_eigenvectors[:, beam_mode]
        u = radial_weights @ u_annuli_array
        v = radial_weights @ v_annuli_array
        eta = radial_weights @ eta_annuli_array
        u_es = E_S_BASIS.T @ u
        v_es = E_S_BASIS.T @ v
        eta_es = E_S_BASIS.T @ eta
        normal = np.cross(u_es, v_es)
        normal_norm = float(np.linalg.norm(normal))
        if normal_norm == 0.0:
            raise ValueError(f"m={harmonic} beam mode {beam_mode} has dependent tangents")
        conditioning = normal_norm / (
            float(np.linalg.norm(u_es)) * float(np.linalg.norm(v_es))
        )
        q_shape = float(np.dot(normal, eta_es) / normal_norm)
        rows.append(
            {
                "harmonic": harmonic,
                "beam_mode": beam_mode,
                "q_shape_proxy": q_shape,
                "delta_uv": float(conditioning),
                "determinant_norm": normal_norm,
                "minimum_role_pixels": int(np.min(counts_annuli)),
            }
        )
    phase = {
        "phase_anchor_rad": anchor,
        "phase_anchor_deg": math.degrees(anchor),
        "phase_amplitude": amplitude,
        "flux_phase_anchor_deg": math.degrees(flux_anchor),
        "phase_estimator_difference_deg": math.degrees(estimator_difference),
    }
    return rows, phase


def source_systematic_audit(
    geometry: dict[str, object],
    star_controls: dict[str, np.ndarray],
    h2: np.ndarray,
    hi: np.ndarray,
    wcs: WCS,
    eigenvectors: np.ndarray,
) -> pd.DataFrame:
    records = []
    variants = [
        row
        for row in geometry_variants(geometry)
        if row["variant_class"] in ("photometric_primary", "photometric_control")
    ]
    for variant in variants:
        scenario_geometry = variant_geometry(geometry, variant)
        for psf_name, star in star_controls.items():
            for h2_factor in H2_CONVERSION_FACTORS:
                for harmonic in HARMONICS:
                    rows, phase = candidate_rows(
                        scenario_geometry,
                        star,
                        h2,
                        hi,
                        wcs,
                        harmonic,
                        eigenvectors,
                        h2_scale=h2_factor,
                    )
                    for row in rows:
                        records.append(
                            {
                                "geometry_variant": variant["variant"],
                                "stellar_psf_scenario": psf_name,
                                "h2_conversion_factor": h2_factor,
                                **row,
                                **phase,
                            }
                        )
    return pd.DataFrame.from_records(records)


def measurement_audit(
    geometry: dict[str, object],
    star0: np.ndarray,
    h20: np.ndarray,
    hi0: np.ndarray,
    wcs: WCS,
    common: np.ndarray,
    uncertainty: dict[str, np.ndarray],
    eigenvectors: np.ndarray,
    target_beam: tuple[float, float, float],
) -> tuple[pd.DataFrame, dict[int, float]]:
    pixel_scale_arcsec = (
        math.sqrt(abs(float(np.linalg.det(wcs.pixel_scale_matrix)))) * 3600.0
    )
    beam_covariance = beam_covariance_pixels(*target_beam, pixel_scale_arcsec)
    kernel = gaussian_kernel_from_covariance(beam_covariance)
    rng = np.random.default_rng(RANDOM_SEED)
    baseline_phase = {}
    for harmonic in HARMONICS:
        _, phase = candidate_rows(
            geometry, star0, h20, hi0, wcs, harmonic, eigenvectors
        )
        baseline_phase[harmonic] = math.radians(phase["phase_anchor_deg"])

    records = []
    for draw in range(N_DRAWS):
        z_star = correlated_standard(rng, star0.shape, kernel, common)
        z_h2 = correlated_standard(rng, star0.shape, kernel, common)
        z_hi = correlated_standard(rng, star0.shape, kernel, common)
        coherent = rng.standard_normal(4)
        star_draw, star_clip = positive_field(
            star0
            + uncertainty["STAR_PIX"] * z_star
            + coherent[0] * uncertainty["STAR_SKY1"]
            + coherent[1] * uncertainty["STAR_SKY2"]
            + coherent[2] * uncertainty["STAR_ICA1"]
            + coherent[3] * uncertainty["STAR_ICA2"],
            common,
        )
        h2_draw, h2_clip = positive_field(
            h20 + uncertainty["H2_IND"] * z_h2, common
        )
        hi_draw, hi_clip = positive_field(
            hi0 + uncertainty["HI_CTL49"] * z_hi, common
        )
        fields = {
            "star_only": (star_draw, h20, hi0),
            "co_independent_only": (star0, h2_draw, hi0),
            "star_plus_co_independent": (star_draw, h2_draw, hi0),
            "star_co_plus_hi_ctl49": (star_draw, h2_draw, hi_draw),
        }
        for scenario in MEASUREMENT_SCENARIOS:
            star, h2, hi = fields[scenario]
            for harmonic in HARMONICS:
                rows, phase = candidate_rows(
                    geometry, star, h2, hi, wcs, harmonic, eigenvectors
                )
                phase_delta = math.degrees(
                    phase_distance_rad(
                        math.radians(phase["phase_anchor_deg"]),
                        baseline_phase[harmonic],
                        harmonic,
                    )
                )
                for row in rows:
                    records.append(
                        {
                            "scenario": scenario,
                            "draw": draw,
                            **row,
                            **phase,
                            "phase_delta_from_baseline_deg": phase_delta,
                            "star_clipped_fraction": star_clip if "star" in scenario else 0.0,
                            "h2_clipped_fraction": h2_clip if "co" in scenario else 0.0,
                            "hi_clipped_fraction": hi_clip if "hi_ctl49" in scenario else 0.0,
                        }
                    )
    return pd.DataFrame.from_records(records), baseline_phase


def angular_role_resolution(
    geometry: dict[str, object],
    star: np.ndarray,
    h2: np.ndarray,
    hi: np.ndarray,
    wcs: WCS,
    common: np.ndarray,
    target_beam: tuple[float, float, float],
) -> dict[str, object]:
    radius, theta, _ = disk_coordinates(geometry, star.shape, wcs)
    edges = [float(value) for value in geometry["radial_edges_arcsec"]]
    pixel_scale_arcsec = (
        math.sqrt(abs(float(np.linalg.det(wcs.pixel_scale_matrix)))) * 3600.0
    )
    beam_covariance = beam_covariance_pixels(*target_beam, pixel_scale_arcsec)
    output = {}
    for harmonic in HARMONICS:
        anchor, _, _, _ = morphology_phase(star, radius, theta, edges, harmonic)
        roles = role_index(theta, anchor)
        valid = (
            common
            & np.isfinite(star)
            & np.isfinite(h2)
            & np.isfinite(hi)
            & (radius >= edges[0])
            & (radius < edges[-1])
        )
        masks = []
        counts = []
        for role in range(4):
            mask = valid & (roles == role)
            count = int(np.count_nonzero(mask))
            if count == 0:
                raise ValueError(f"m={harmonic} has an empty full-support angular role")
            counts.append(count)
            masks.append(mask.astype(float) / count)
        correlation, eigenvalues, effective_rank = beam_overlap_correlation(
            masks, beam_covariance
        )
        relative = E_S_BASIS.T @ correlation @ E_S_BASIS
        relative = 0.5 * (relative + relative.T)
        relative_eigenvalues = np.linalg.eigvalsh(relative)[::-1]
        relative_effective_rank = float(
            np.sum(relative_eigenvalues) ** 2 / np.sum(relative_eigenvalues**2)
        )
        output[f"m{harmonic}"] = {
            "role_pixel_counts": counts,
            "role_beam_overlap_correlation": correlation.tolist(),
            "full_role_eigenvalues": eigenvalues.tolist(),
            "full_role_participation_rank": effective_rank,
            "relative_role_eigenvalues": relative_eigenvalues.tolist(),
            "relative_role_participation_rank": relative_effective_rank,
            "relative_role_algebraic_rank": int(
                np.count_nonzero(relative_eigenvalues > 1.0e-10)
            ),
            "is_complete_role_covariance": False,
        }
    return output


def source_driver_summary(systematics: pd.DataFrame) -> dict[str, object]:
    output = {}
    for harmonic in HARMONICS:
        for beam_mode in range(N_BEAM_MODES):
            candidate = systematics.loc[
                systematics["harmonic"].eq(harmonic)
                & systematics["beam_mode"].eq(beam_mode)
            ]
            controls = {
                "geometry_only": candidate.loc[
                    candidate["stellar_psf_scenario"].eq("psf_0arcsec_primary")
                    & candidate["h2_conversion_factor"].eq(1.0)
                ],
                "stellar_psf_only": candidate.loc[
                    candidate["geometry_variant"].eq("s4g_global_thin_primary")
                    & candidate["h2_conversion_factor"].eq(1.0)
                ],
                "h2_conversion_only": candidate.loc[
                    candidate["geometry_variant"].eq("s4g_global_thin_primary")
                    & candidate["stellar_psf_scenario"].eq("psf_0arcsec_primary")
                ],
            }
            baseline = float(
                candidate.loc[
                    candidate["geometry_variant"].eq("s4g_global_thin_primary")
                    & candidate["stellar_psf_scenario"].eq("psf_0arcsec_primary")
                    & candidate["h2_conversion_factor"].eq(1.0),
                    "q_shape_proxy",
                ].iloc[0]
            )
            output[f"m{harmonic}_beam{beam_mode}"] = {
                name: {
                    "n": int(len(values)),
                    "q_min": float(values["q_shape_proxy"].min()),
                    "q_max": float(values["q_shape_proxy"].max()),
                    "sign_stable": bool(
                        np.all(np.sign(values["q_shape_proxy"]) == np.sign(baseline))
                    ),
                }
                for name, values in controls.items()
            }
    return output


def summarize(
    systematics: pd.DataFrame,
    measurement: pd.DataFrame,
    baseline: dict[tuple[int, int], float],
    baseline_phase: dict[int, float],
) -> pd.DataFrame:
    rows = []
    primary_measurement = measurement.loc[
        measurement["scenario"].eq("star_plus_co_independent")
    ]
    for harmonic in HARMONICS:
        primary_phase = baseline_phase[harmonic]
        for beam_mode in range(N_BEAM_MODES):
            source = systematics.loc[
                systematics["harmonic"].eq(harmonic)
                & systematics["beam_mode"].eq(beam_mode)
            ]
            measured = primary_measurement.loc[
                primary_measurement["harmonic"].eq(harmonic)
                & primary_measurement["beam_mode"].eq(beam_mode)
            ]
            q_source = source["q_shape_proxy"].to_numpy(dtype=float)
            q_measured = measured["q_shape_proxy"].to_numpy(dtype=float)
            baseline_q = baseline[(harmonic, beam_mode)]
            baseline_sign_probability = float(
                np.mean(q_measured > 0.0)
                if baseline_q > 0.0
                else np.mean(q_measured < 0.0)
            )
            source_phase_deltas = np.asarray(
                [
                    math.degrees(
                        phase_distance_rad(
                            math.radians(value), primary_phase, harmonic
                        )
                    )
                    for value in source["phase_anchor_deg"].to_numpy(dtype=float)
                ]
            )
            source_sign_stable = bool(np.all(np.sign(q_source) == np.sign(baseline_q)))
            measurement_sign_stable = baseline_sign_probability >= 0.95
            source_phase_stable = float(np.max(source_phase_deltas)) <= PHASE_STABILITY_LIMIT_DEG
            measurement_phase_p95 = float(
                np.percentile(measured["phase_delta_from_baseline_deg"], 95.0)
            )
            measurement_phase_stable = measurement_phase_p95 <= PHASE_STABILITY_LIMIT_DEG
            rows.append(
                {
                    "harmonic": harmonic,
                    "beam_mode": beam_mode,
                    "baseline_q_shape_proxy": baseline_q,
                    "source_q_min": float(np.min(q_source)),
                    "source_q_max": float(np.max(q_source)),
                    "source_sign_stable": source_sign_stable,
                    "source_phase_max_delta_deg": float(np.max(source_phase_deltas)),
                    "source_phase_stable": source_phase_stable,
                    "measurement_q_p025": float(np.percentile(q_measured, 2.5)),
                    "measurement_q_median": float(np.median(q_measured)),
                    "measurement_q_p975": float(np.percentile(q_measured, 97.5)),
                    "measurement_baseline_sign_probability": baseline_sign_probability,
                    "measurement_sign_stable_95": measurement_sign_stable,
                    "measurement_phase_p95_delta_deg": measurement_phase_p95,
                    "measurement_phase_stable": measurement_phase_stable,
                    "passes_both_separate_gates": bool(
                        source_sign_stable
                        and measurement_sign_stable
                        and source_phase_stable
                        and measurement_phase_stable
                    ),
                    "minimum_delta_uv_source_systematics": float(source["delta_uv"].min()),
                    "minimum_role_pixels_source_systematics": int(
                        source["minimum_role_pixels"].min()
                    ),
                }
            )
    return pd.DataFrame.from_records(rows)


def main() -> None:
    geometry = json.loads(GEOMETRY_PATH.read_text())
    uncertainty_meta = json.loads(UNCERTAINTY_META_PATH.read_text())
    if geometry.get("velocity_or_residual_inputs"):
        raise ValueError("Geometry freeze declares forbidden endpoint inputs")
    if uncertainty_meta["inputs"]["velocity_or_residual_inputs"]:
        raise ValueError("Uncertainty fields declare forbidden endpoint inputs")

    beam_matrix, eigenvalues, eigenvectors = beam_modes()
    with fits.open(COMMON_PATH) as hdul:
        wcs = WCS(hdul["SIGMA_STAR"].header, naxis=2)
        target_beam = (
            float(hdul["SIGMA_STAR"].header["BMAJ"]) * 3600.0,
            float(hdul["SIGMA_STAR"].header["BMIN"]) * 3600.0,
            float(hdul["SIGMA_STAR"].header["BPA"]),
        )
        star_controls = {
            "psf_0arcsec_primary": np.asarray(hdul["STAR_P00"].data, dtype=float),
            "psf_2arcsec_control": np.asarray(hdul["STAR_P20"].data, dtype=float),
            "psf_4arcsec_control": np.asarray(hdul["STAR_P40"].data, dtype=float),
        }
        star0 = star_controls["psf_0arcsec_primary"]
        h20 = np.asarray(hdul["SIGMA_H2"].data, dtype=float)
        hi0 = np.asarray(hdul["SIGMA_HI"].data, dtype=float)
    with fits.open(UNCERTAINTY_PATH) as hdul:
        common = np.asarray(hdul["COMMON"].data, dtype=bool)
        uncertainty = {
            name: np.asarray(hdul[name].data, dtype=float)
            for name in (
                "STAR_PIX",
                "STAR_SKY1",
                "STAR_SKY2",
                "STAR_ICA1",
                "STAR_ICA2",
                "H2_IND",
                "HI_CTL49",
            )
        }
    for values in (*star_controls.values(), h20, hi0):
        values[~common] = np.nan

    systematics = source_systematic_audit(
        geometry, star_controls, h20, hi0, wcs, eigenvectors
    )
    expected_systematic_rows = 8 * 3 * 3 * len(HARMONICS) * N_BEAM_MODES
    if len(systematics) != expected_systematic_rows:
        raise ValueError("Incomplete source-systematic Cartesian product")
    systematics.to_csv(SYSTEMATICS_PATH, index=False, float_format="%.10g")

    baseline = {}
    baseline_phase_metrics = {}
    edge_sensitivity = {}
    scale_invariance = {}
    for harmonic in HARMONICS:
        rows, phase = candidate_rows(
            geometry, star0, h20, hi0, wcs, harmonic, eigenvectors
        )
        baseline_phase_metrics[harmonic] = phase
        for row in rows:
            baseline[(harmonic, int(row["beam_mode"]))] = float(row["q_shape_proxy"])
        edge_values = []
        for offset_deg in (-ROLE_EDGE_PERTURBATION_DEG, ROLE_EDGE_PERTURBATION_DEG):
            controlled, _ = candidate_rows(
                geometry,
                star0,
                h20,
                hi0,
                wcs,
                harmonic,
                eigenvectors,
                anchor_offset_rad=math.radians(offset_deg),
            )
            edge_values.extend(
                abs(
                    float(row["q_shape_proxy"])
                    - baseline[(harmonic, int(row["beam_mode"]))]
                )
                for row in controlled
            )
        edge_sensitivity[harmonic] = float(max(edge_values))
        scale_differences = []
        for scale in (0.5, 2.0):
            controlled, _ = candidate_rows(
                geometry, scale * star0, h20, hi0, wcs, harmonic, eigenvectors
            )
            scale_differences.extend(
                abs(
                    float(row["q_shape_proxy"])
                    - baseline[(harmonic, int(row["beam_mode"]))]
                )
                for row in controlled
            )
        scale_invariance[harmonic] = float(max(scale_differences))

    shifted_theta = np.linspace(0.0, 2.0 * math.pi, 1000, endpoint=False)
    rotation_covariance = bool(
        np.array_equal(
            role_index(shifted_theta, 0.37),
            role_index(shifted_theta + 0.91, 0.37 + 0.91),
        )
    )

    measurement, baseline_phase = measurement_audit(
        geometry,
        star0,
        h20,
        hi0,
        wcs,
        common,
        uncertainty,
        eigenvectors,
        target_beam,
    )
    expected_measurement_rows = (
        N_DRAWS * len(MEASUREMENT_SCENARIOS) * len(HARMONICS) * N_BEAM_MODES
    )
    if len(measurement) != expected_measurement_rows:
        raise ValueError("Incomplete measurement Cartesian product")
    measurement.to_csv(MEASUREMENT_PATH, index=False, float_format="%.10g")

    summary = summarize(systematics, measurement, baseline, baseline_phase)
    summary.to_csv(SUMMARY_PATH, index=False, float_format="%.10g")
    passing = summary.loc[summary["passes_both_separate_gates"]]
    role_resolution = angular_role_resolution(
        geometry, star0, h20, hi0, wcs, common, target_beam
    )
    driver_summary = source_driver_summary(systematics)
    candidate_status = (
        "AT_LEAST_ONE_INTERNAL_SOURCE_ROLE_CANDIDATE_SURVIVES"
        if len(passing)
        else "NO_PHASE_ROLE_CANDIDATE_SURVIVES_BOTH_INTERNAL_GATES"
    )

    manifest = {
        "schema": "ngc4254_ffl_morphology_phase_roles_v06",
        "status": STATUS,
        "candidate_status": candidate_status,
        "galaxy": "NGC4254",
        "construction": {
            "role_anchor_candidates": ["stellar_m1_phase", "stellar_m2_phase"],
            "phase_estimator": "annulus-median-subtracted log-stellar contrast over inherited 5-65 arcsec support",
            "role_rule": "four ordered pi/2 sectors measured from the source-derived phase anchor",
            "radial_projection": "first two eigenvectors of the frozen six-annulus H I beam-overlap correlation screen",
            "phase_stability_limit_deg": PHASE_STABILITY_LIMIT_DEG,
            "phase_limit_reason": "half of one pi/2 role-sector width",
            "role_edge_perturbation_deg": ROLE_EDGE_PERTURBATION_DEG,
            "beam_eigenvalues": eigenvalues.tolist(),
            "beam_mode_vectors": eigenvectors[:, :N_BEAM_MODES].T.tolist(),
            "top_two_trace_fraction": float(np.sum(eigenvalues[:2]) / np.sum(eigenvalues)),
            "beam_overlap_is_complete_covariance": False,
        },
        "inputs": {
            "geometry": str(GEOMETRY_PATH.relative_to(ROOT)),
            "geometry_sha256": sha256(GEOMETRY_PATH),
            "common_source_cube": str(COMMON_PATH.relative_to(ROOT)),
            "common_source_cube_sha256": sha256(COMMON_PATH),
            "beam_overlap": str(BEAM_PATH.relative_to(ROOT)),
            "beam_overlap_sha256": sha256(BEAM_PATH),
            "uncertainty_fields": str(UNCERTAINTY_PATH.relative_to(ROOT)),
            "uncertainty_fields_sha256": sha256(UNCERTAINTY_PATH),
            "velocity_or_residual_inputs": [],
        },
        "source_systematic_audit": {
            "n_rows": len(systematics),
            "n_scenarios_per_harmonic_mode": 72,
            "geometry_variants": 8,
            "stellar_psf_controls": 3,
            "h2_conversion_controls": 3,
            "driver_summary": driver_summary,
        },
        "measurement_audit": {
            "random_seed": RANDOM_SEED,
            "n_draws": N_DRAWS,
            "scenarios": list(MEASUREMENT_SCENARIOS),
            "n_rows": len(measurement),
            "hi_role": "robust1 49-channel control only",
        },
        "baseline_phase_metrics": {
            f"m{harmonic}": values for harmonic, values in baseline_phase_metrics.items()
        },
        "validation": {
            "global_stellar_scale_max_q_change": {
                f"m{key}": value for key, value in scale_invariance.items()
            },
            "role_rotation_covariance_exact": rotation_covariance,
            "half_degree_role_edge_max_q_change": {
                f"m{key}": value for key, value in edge_sensitivity.items()
            },
            "independent_flux_phase_estimator_difference_deg": {
                f"m{harmonic}": values["phase_estimator_difference_deg"]
                for harmonic, values in baseline_phase_metrics.items()
            },
            "top_two_beam_trace_fraction": float(
                np.sum(eigenvalues[:2]) / np.sum(eigenvalues)
            ),
            "angular_role_beam_screen": role_resolution,
        },
        "result": {
            "passing_harmonic_beam_modes": [
                {
                    "harmonic": int(row.harmonic),
                    "beam_mode": int(row.beam_mode),
                }
                for row in passing.itertuples()
            ],
            "n_passing_candidates": int(len(passing)),
            "physical_role_chart_promoted": False,
            "endpoint_scoring_allowed": False,
        },
        "outputs": {
            "systematics": str(SYSTEMATICS_PATH.relative_to(ROOT)),
            "systematics_sha256": sha256(SYSTEMATICS_PATH),
            "measurement": str(MEASUREMENT_PATH.relative_to(ROOT)),
            "measurement_sha256": sha256(MEASUREMENT_PATH),
            "summary": str(SUMMARY_PATH.relative_to(ROOT)),
            "summary_sha256": sha256(SUMMARY_PATH),
            "report": str(REPORT_PATH.relative_to(ROOT)),
        },
        "audit_checks": {
            "source_only": True,
            "velocity_or_residual_inputs_empty": True,
            "fixed_random_seed": True,
            "complete_source_systematic_product": len(systematics)
            == expected_systematic_rows,
            "complete_measurement_product": len(measurement)
            == expected_measurement_rows,
            "all_q_values_finite": bool(
                np.isfinite(systematics["q_shape_proxy"]).all()
                and np.isfinite(measurement["q_shape_proxy"]).all()
            ),
            "beam_mode_signs_frozen_by_largest_component": True,
            "endpoint_scored": False,
        },
        "known_limitations": [
            "m=1 and m=2 are finite source-coordinate candidates, not parent-derived role identities",
            "the beam eigenvectors diagonalize a support-overlap correlation screen, not the complete nonlinear q covariance",
            "individual inherited annulus-role cells can contain as few as three map pixels; beam-mode projection and Monte Carlo propagation do not make those cells independent measurements",
            "the stellar measurement modes remain a conditional P5 uncertainty reconstruction",
            "the H I measurement layer remains a robust-1 control for a robust-5 moment map",
            "passing internal source gates would not construct physical eta, q_det, curvatures, determinant transport, or a terminal map",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    JSON_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    table_rows = []
    for row in summary.itertuples():
        table_rows.append(
            "| "
            f"m={int(row.harmonic)} | {int(row.beam_mode)} | "
            f"{row.baseline_q_shape_proxy:+.6f} | "
            f"{row.source_q_min:+.6f}, {row.source_q_max:+.6f} | "
            f"{row.source_phase_max_delta_deg:.2f} | "
            f"{row.measurement_q_p025:+.6f}, {row.measurement_q_p975:+.6f} | "
            f"{row.measurement_baseline_sign_probability:.3f} | "
            f"{row.measurement_phase_p95_delta_deg:.2f} | "
            f"{'PASS' if row.passes_both_separate_gates else 'FAIL'} |"
        )
    report = f"""# NGC4254 Morphology-Phase Four-Role Audit v06

**Status:** `{STATUS}`

**Candidate verdict:** `{candidate_status}`

**Claim boundary:** {CLAIM_BOUNDARY}.

## Frozen Construction

The four ordered roles are no longer anchored to an externally imposed disk
position angle.  For each finite candidate, the stellar map supplies an `m=1`
or `m=2` phase from annulus-normalized log-intensity contrast, and the roles are
the four consecutive 90-degree sectors measured from that phase.  The same
source-derived anchor is used for the observer-path, stellar-body, and gas-shape
vectors.

The six inherited annular relative vectors are projected onto the first two
eigenvectors of the already frozen H I beam-overlap screen.  Their eigenvalues
are `{eigenvalues[0]:.6f}` and `{eigenvalues[1]:.6f}` and together carry
`{manifest['construction']['top_two_trace_fraction']:.4%}` of the matrix trace.
This does not turn the overlap screen into a complete covariance.

## Finite Audit

| anchor | beam mode | baseline q | 72-source range | max source phase shift (deg) | measurement 95% q | P(baseline sign) | measurement phase p95 (deg) | joint internal gate |
|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
{chr(10).join(table_rows)}

The phase limit is frozen at `{PHASE_STABILITY_LIMIT_DEG}` degrees, half one
role-sector width. Passing requires sign and phase stability under both the 72
source-systematic scenarios and the separate 256-draw stellar-plus-independent-
CO measurement model.

## Validation

- A global stellar rescaling changes q by at most
  `{max(scale_invariance.values()):.3e}`.
- Simultaneously rotating theta and the morphology anchor leaves every role
  label unchanged: `{rotation_covariance}`.
- A +/-`{ROLE_EDGE_PERTURBATION_DEG}` degree role-edge perturbation changes q by
  at most `{max(edge_sensitivity.values()):.6g}`.
- The independent mask-corrected flux phase differs from the primary contrast
  phase by `m=1: {baseline_phase_metrics[1]['phase_estimator_difference_deg']:.2f}`
  degrees and `m=2: {baseline_phase_metrics[2]['phase_estimator_difference_deg']:.2f}`
  degrees. This is an estimator-consistency diagnostic, not a promotion gate.
- The `m=2` full-support role counts are
  `{role_resolution['m2']['role_pixel_counts']}`. Its three relative role
  eigenvalues are
  `{[round(value, 6) for value in role_resolution['m2']['relative_role_eigenvalues']]}`
  with participation rank
  `{role_resolution['m2']['relative_role_participation_rank']:.4f}/3`. Thus the
  beam screen does not collapse the candidate to one relative direction, but
  it is not a complete role covariance and does not authorize a diagonal
  four-role likelihood.
- Some inherited annulus-role cells contain only three map pixels. The radial
  eigenmode projection uses them as correlated source coordinates; it does not
  turn them into independent measurements. This remains a promotion blocker.

For the passing `m=2`, beam-mode-1 candidate, geometry-only, stellar-PSF-only,
and H2-conversion-only controls each preserve the baseline sign. The
measurement decomposition remains stellar-mode dominated; CO-only and the
robust-1 H I control do not select the candidate.

## Verdict

Passing internal harmonic/mode candidates:
`{manifest['result']['passing_harmonic_beam_modes']}`.

Even a passing candidate would remain a source-side inverse chart only. No
physical parent role, FFL eta, determinant transport, channel origin, time or
quantum terminal, dark-sector replacement, or endpoint score is identified.
"""
    REPORT_PATH.write_text(report)
    print(STATUS)
    print(candidate_status)
    print(f"passing={manifest['result']['passing_harmonic_beam_modes']}")


if __name__ == "__main__":
    main()
