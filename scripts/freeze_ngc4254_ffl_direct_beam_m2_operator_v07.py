#!/usr/bin/env python3
"""Audit a direct beam-resolved morphology-phase operator for NGC4254.

This source-only v07 removes the sparse annulus-by-role cells from v06.  The
frozen v06 `beam_mode=1` radial eigenvector is interpolated to pixels and applied directly
to axisymmetry-subtracted observer-path, stellar, and gas source fields.  The
m=2 construction is the candidate and m=1 is processed identically as an
alternative-family specificity control.  No velocity or residual endpoint is
opened.
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
from freeze_ngc4254_ffl_morphology_phase_roles_v06 import (
    angular_role_resolution,
    beam_modes,
    disk_coordinates,
    morphology_phase,
    phase_distance_rad,
    role_index,
)
from ngc4254_source_covariance_utils import (
    beam_covariance_pixels,
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
V06_PATH = DATA / "ngc4254_ffl_morphology_phase_roles_v06.json"

SYSTEMATICS_PATH = DATA / "ngc4254_ffl_direct_beam_m2_systematics_v07.csv"
MEASUREMENT_PATH = DATA / "ngc4254_ffl_direct_beam_m2_measurement_v07.csv"
SUMMARY_PATH = DATA / "ngc4254_ffl_direct_beam_m2_summary_v07.csv"
JSON_PATH = DATA / "ngc4254_ffl_direct_beam_m2_operator_v07.json"
REPORT_PATH = REPORTS / "ngc4254_ffl_direct_beam_m2_operator_v07.md"

STATUS = "SOURCE_ONLY_DIRECT_BEAM_M2_OPERATOR_AUDIT_COMPLETE_NO_ENDPOINT"
CLAIM_BOUNDARY = (
    "finite source-only 4D-inverse audit of a direct beam-weighted m=2 role "
    "operator with an identically processed m=1 alternative-family control; "
    "not a parent-derived role, physical q_det, complete covariance, channel/"
    "time/quantum signal, dark-matter replacement, or endpoint score"
)
HARMONICS = (1, 2)
TARGET_HARMONIC = 2
CONTROL_HARMONIC = 1
V06_SURVIVING_BEAM_MODE_INDEX = 1
PHASE_STABILITY_LIMIT_DEG = 22.5
ROLE_EDGE_PERTURBATION_DEG = 0.5
H2_CONVERSION_FACTORS = (0.7, 1.0, 1.3)
RANDOM_SEED = 425407
N_DRAWS = 256
MEASUREMENT_SCENARIOS = (
    "star_only",
    "co_independent_only",
    "star_plus_co_independent",
    "star_co_plus_hi_ctl49",
)
PRIMARY_MEASUREMENT_SCENARIO = "star_plus_co_independent"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def centered(values: np.ndarray) -> np.ndarray:
    return values - float(np.mean(values))


def radial_residual(
    values: np.ndarray,
    finite: np.ndarray,
    radius: np.ndarray,
    edges: list[float],
) -> tuple[np.ndarray, np.ndarray]:
    medians = []
    for radius_lo, radius_hi in zip(edges[:-1], edges[1:]):
        annulus = finite & (radius >= radius_lo) & (radius < radius_hi)
        if np.count_nonzero(annulus) == 0:
            raise ValueError(f"Empty radial baseline annulus {radius_lo:g}-{radius_hi:g}")
        medians.append(float(np.median(values[annulus])))
    midpoints = 0.5 * (np.asarray(edges[:-1]) + np.asarray(edges[1:]))
    baseline = np.interp(radius, midpoints, medians)
    residual = np.full(values.shape, np.nan, dtype=float)
    residual[finite] = values[finite] - baseline[finite]
    return residual, np.asarray(medians, dtype=float)


def direct_role_vector(
    residual: np.ndarray,
    support: np.ndarray,
    roles: np.ndarray,
    radial_weights: np.ndarray,
) -> np.ndarray:
    values = []
    for role in range(4):
        mask = support & (roles == role)
        denominator = float(np.sum(np.abs(radial_weights[mask])))
        if denominator <= 0.0:
            raise ValueError(f"Role {role} has zero direct radial-weight norm")
        values.append(float(np.sum(radial_weights[mask] * residual[mask]) / denominator))
    return centered(np.asarray(values, dtype=float))


def candidate_row(
    geometry: dict[str, object],
    star: np.ndarray,
    h2: np.ndarray,
    hi: np.ndarray,
    wcs: WCS,
    harmonic: int,
    radial_mode: np.ndarray,
    *,
    h2_scale: float = 1.0,
    anchor_offset_rad: float = 0.0,
) -> tuple[dict[str, object], dict[str, object]]:
    if star.shape != h2.shape or star.shape != hi.shape:
        raise ValueError("Source fields do not share one grid")
    edges = [float(value) for value in geometry["radial_edges_arcsec"]]
    midpoints = 0.5 * (np.asarray(edges[:-1]) + np.asarray(edges[1:]))
    if radial_mode.shape != midpoints.shape:
        raise ValueError("Radial beam mode does not match inherited annuli")

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
    support = finite & (radius >= edges[0]) & (radius < edges[-1])
    anchor, amplitude, flux_anchor, estimator_difference = morphology_phase(
        star, radius, theta, edges, harmonic
    )
    used_anchor = anchor + anchor_offset_rad
    roles = role_index(theta, used_anchor)
    counts = np.asarray(
        [np.count_nonzero(support & (roles == role)) for role in range(4)], dtype=int
    )
    if np.any(counts == 0):
        raise ValueError(f"m={harmonic} has an empty direct full-support role")

    log_star = np.full(star.shape, np.nan, dtype=float)
    log_gas = np.full(gas.shape, np.nan, dtype=float)
    log_star[finite] = np.log(star[finite])
    log_gas[finite] = np.log(gas[finite])
    path_residual, path_profile = radial_residual(path, finite, radius, edges)
    star_residual, star_profile = radial_residual(log_star, finite, radius, edges)
    gas_residual, gas_profile = radial_residual(log_gas, finite, radius, edges)
    pixel_weights = np.interp(radius, midpoints, radial_mode)

    u = direct_role_vector(path_residual, support, roles, pixel_weights)
    v = direct_role_vector(star_residual, support, roles, pixel_weights)
    eta = direct_role_vector(gas_residual, support, roles, pixel_weights)
    u_es = E_S_BASIS.T @ u
    v_es = E_S_BASIS.T @ v
    eta_es = E_S_BASIS.T @ eta
    normal = np.cross(u_es, v_es)
    normal_norm = float(np.linalg.norm(normal))
    tangent_norm = float(np.linalg.norm(u_es)) * float(np.linalg.norm(v_es))
    if normal_norm == 0.0 or tangent_norm == 0.0:
        raise ValueError(f"m={harmonic} direct operator has dependent tangents")

    row = {
        "harmonic": harmonic,
        "q_shape_proxy": float(np.dot(normal, eta_es) / normal_norm),
        "delta_uv": normal_norm / tangent_norm,
        "determinant_norm": normal_norm,
        "minimum_role_pixels": int(np.min(counts)),
        "role_0_pixels": int(counts[0]),
        "role_1_pixels": int(counts[1]),
        "role_2_pixels": int(counts[2]),
        "role_3_pixels": int(counts[3]),
    }
    diagnostics = {
        "phase_anchor_rad": anchor,
        "phase_anchor_deg": math.degrees(anchor),
        "phase_amplitude": amplitude,
        "flux_phase_anchor_deg": math.degrees(flux_anchor),
        "phase_estimator_difference_deg": math.degrees(estimator_difference),
        "path_radial_profile": path_profile.tolist(),
        "log_stellar_radial_profile": star_profile.tolist(),
        "log_gas_radial_profile": gas_profile.tolist(),
        "u_role_vector": u.tolist(),
        "v_role_vector": v.tolist(),
        "eta_role_vector": eta.tolist(),
    }
    return row, diagnostics


def source_systematic_audit(
    geometry: dict[str, object],
    star_controls: dict[str, np.ndarray],
    h2: np.ndarray,
    hi: np.ndarray,
    wcs: WCS,
    radial_mode: np.ndarray,
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
                    row, diagnostics = candidate_row(
                        scenario_geometry,
                        star,
                        h2,
                        hi,
                        wcs,
                        harmonic,
                        radial_mode,
                        h2_scale=h2_factor,
                    )
                    records.append(
                        {
                            "geometry_variant": variant["variant"],
                            "stellar_psf_scenario": psf_name,
                            "h2_conversion_factor": h2_factor,
                            **row,
                            "phase_anchor_deg": diagnostics["phase_anchor_deg"],
                            "phase_amplitude": diagnostics["phase_amplitude"],
                            "flux_phase_anchor_deg": diagnostics["flux_phase_anchor_deg"],
                            "phase_estimator_difference_deg": diagnostics[
                                "phase_estimator_difference_deg"
                            ],
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
    radial_mode: np.ndarray,
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
        _, diagnostics = candidate_row(
            geometry, star0, h20, hi0, wcs, harmonic, radial_mode
        )
        baseline_phase[harmonic] = math.radians(diagnostics["phase_anchor_deg"])

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
        h2_draw, h2_clip = positive_field(h20 + uncertainty["H2_IND"] * z_h2, common)
        hi_draw, hi_clip = positive_field(hi0 + uncertainty["HI_CTL49"] * z_hi, common)
        fields = {
            "star_only": (star_draw, h20, hi0),
            "co_independent_only": (star0, h2_draw, hi0),
            "star_plus_co_independent": (star_draw, h2_draw, hi0),
            "star_co_plus_hi_ctl49": (star_draw, h2_draw, hi_draw),
        }
        for scenario in MEASUREMENT_SCENARIOS:
            star, h2, hi = fields[scenario]
            for harmonic in HARMONICS:
                row, diagnostics = candidate_row(
                    geometry, star, h2, hi, wcs, harmonic, radial_mode
                )
                phase_delta = math.degrees(
                    phase_distance_rad(
                        math.radians(diagnostics["phase_anchor_deg"]),
                        baseline_phase[harmonic],
                        harmonic,
                    )
                )
                records.append(
                    {
                        "scenario": scenario,
                        "draw": draw,
                        **row,
                        "phase_anchor_deg": diagnostics["phase_anchor_deg"],
                        "phase_amplitude": diagnostics["phase_amplitude"],
                        "phase_delta_from_baseline_deg": phase_delta,
                        "star_clipped_fraction": star_clip if "star" in scenario else 0.0,
                        "h2_clipped_fraction": h2_clip if "co" in scenario else 0.0,
                        "hi_clipped_fraction": hi_clip if "hi_ctl49" in scenario else 0.0,
                    }
                )
    return pd.DataFrame.from_records(records), baseline_phase


def summarize(
    systematics: pd.DataFrame,
    measurement: pd.DataFrame,
    baseline: dict[int, float],
    baseline_phase: dict[int, float],
    beam_area_pixels: float,
    minimum_required_role_pixels: int,
    role_resolution: dict[str, object],
) -> pd.DataFrame:
    rows = []
    primary = measurement.loc[
        measurement["scenario"].eq(PRIMARY_MEASUREMENT_SCENARIO)
    ]
    for harmonic in HARMONICS:
        source = systematics.loc[systematics["harmonic"].eq(harmonic)]
        measured = primary.loc[primary["harmonic"].eq(harmonic)]
        baseline_q = baseline[harmonic]
        q_source = source["q_shape_proxy"].to_numpy(dtype=float)
        q_measured = measured["q_shape_proxy"].to_numpy(dtype=float)
        sign_probability = float(
            np.mean(q_measured > 0.0)
            if baseline_q > 0.0
            else np.mean(q_measured < 0.0)
        )
        source_phase_deltas = np.asarray(
            [
                math.degrees(
                    phase_distance_rad(
                        math.radians(value), baseline_phase[harmonic], harmonic
                    )
                )
                for value in source["phase_anchor_deg"].to_numpy(dtype=float)
            ],
            dtype=float,
        )
        source_sign = bool(np.all(np.sign(q_source) == np.sign(baseline_q)))
        source_phase = float(np.max(source_phase_deltas)) <= PHASE_STABILITY_LIMIT_DEG
        measurement_sign = sign_probability >= 0.95
        measurement_phase_p95 = float(
            np.percentile(measured["phase_delta_from_baseline_deg"], 95.0)
        )
        measurement_phase = measurement_phase_p95 <= PHASE_STABILITY_LIMIT_DEG
        minimum_pixels = int(source["minimum_role_pixels"].min())
        support_gate = minimum_pixels >= minimum_required_role_pixels
        rank = int(role_resolution[f"m{harmonic}"]["relative_role_algebraic_rank"])
        rank_gate = rank == 3
        own_gate = bool(
            source_sign
            and source_phase
            and measurement_sign
            and measurement_phase
            and support_gate
            and rank_gate
        )
        rows.append(
            {
                "harmonic": harmonic,
                "family_role": "target_m2" if harmonic == 2 else "alternative_m1_control",
                "baseline_q_shape_proxy": baseline_q,
                "source_q_min": float(np.min(q_source)),
                "source_q_max": float(np.max(q_source)),
                "source_sign_stable": source_sign,
                "source_phase_max_delta_deg": float(np.max(source_phase_deltas)),
                "source_phase_stable": source_phase,
                "measurement_q_p025": float(np.percentile(q_measured, 2.5)),
                "measurement_q_median": float(np.median(q_measured)),
                "measurement_q_p975": float(np.percentile(q_measured, 97.5)),
                "measurement_baseline_sign_probability": sign_probability,
                "measurement_sign_stable_95": measurement_sign,
                "measurement_phase_p95_delta_deg": measurement_phase_p95,
                "measurement_phase_stable": measurement_phase,
                "minimum_role_pixels_source_systematics": minimum_pixels,
                "gaussian_beam_area_pixels": beam_area_pixels,
                "minimum_required_role_pixels": minimum_required_role_pixels,
                "full_role_beam_support_gate": support_gate,
                "relative_role_algebraic_rank": rank,
                "relative_role_rank3_gate": rank_gate,
                "passes_own_internal_gates": own_gate,
                "minimum_delta_uv_source_systematics": float(source["delta_uv"].min()),
            }
        )
    return pd.DataFrame.from_records(rows)


def linear_zero_crossings(midpoints: np.ndarray, vector: np.ndarray) -> list[float]:
    crossings = []
    for x0, x1, y0, y1 in zip(
        midpoints[:-1], midpoints[1:], vector[:-1], vector[1:]
    ):
        if y0 == 0.0:
            crossings.append(float(x0))
        elif y0 * y1 < 0.0:
            crossings.append(float(x0 - y0 * (x1 - x0) / (y1 - y0)))
    return crossings


def main() -> None:
    geometry = json.loads(GEOMETRY_PATH.read_text())
    uncertainty_meta = json.loads(UNCERTAINTY_META_PATH.read_text())
    v06 = json.loads(V06_PATH.read_text())
    if geometry.get("velocity_or_residual_inputs"):
        raise ValueError("Geometry freeze declares forbidden endpoint inputs")
    if uncertainty_meta["inputs"]["velocity_or_residual_inputs"]:
        raise ValueError("Uncertainty fields declare forbidden endpoint inputs")
    if v06["result"]["physical_role_chart_promoted"]:
        raise ValueError("v06 unexpectedly promotes a physical role chart")

    beam_matrix, beam_eigenvalues, beam_eigenvectors = beam_modes()
    radial_mode = np.asarray(
        beam_eigenvectors[:, V06_SURVIVING_BEAM_MODE_INDEX], dtype=float
    )
    edges = [float(value) for value in geometry["radial_edges_arcsec"]]
    midpoints = 0.5 * (np.asarray(edges[:-1]) + np.asarray(edges[1:]))

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

    pixel_scale_arcsec = (
        math.sqrt(abs(float(np.linalg.det(wcs.pixel_scale_matrix)))) * 3600.0
    )
    beam_area_arcsec2 = math.pi * target_beam[0] * target_beam[1] / (4.0 * math.log(2.0))
    beam_area_pixels = beam_area_arcsec2 / pixel_scale_arcsec**2
    minimum_required_role_pixels = int(math.ceil(beam_area_pixels))

    systematics = source_systematic_audit(
        geometry, star_controls, h20, hi0, wcs, radial_mode
    )
    expected_systematic_rows = 8 * 3 * 3 * len(HARMONICS)
    if len(systematics) != expected_systematic_rows:
        raise ValueError("Incomplete source-systematic Cartesian product")
    systematics.to_csv(SYSTEMATICS_PATH, index=False, float_format="%.10g")

    baseline = {}
    baseline_diagnostics = {}
    edge_sensitivity = {}
    scale_invariance = {}
    for harmonic in HARMONICS:
        row, diagnostics = candidate_row(
            geometry, star0, h20, hi0, wcs, harmonic, radial_mode
        )
        baseline[harmonic] = float(row["q_shape_proxy"])
        baseline_diagnostics[harmonic] = {**row, **diagnostics}
        edge_values = []
        for offset_deg in (-ROLE_EDGE_PERTURBATION_DEG, ROLE_EDGE_PERTURBATION_DEG):
            controlled, _ = candidate_row(
                geometry,
                star0,
                h20,
                hi0,
                wcs,
                harmonic,
                radial_mode,
                anchor_offset_rad=math.radians(offset_deg),
            )
            edge_values.append(abs(float(controlled["q_shape_proxy"]) - baseline[harmonic]))
        edge_sensitivity[harmonic] = float(max(edge_values))
        scale_values = []
        for scale in (0.5, 2.0):
            controlled, _ = candidate_row(
                geometry, scale * star0, h20, hi0, wcs, harmonic, radial_mode
            )
            scale_values.append(abs(float(controlled["q_shape_proxy"]) - baseline[harmonic]))
        scale_invariance[harmonic] = float(max(scale_values))

    shifted_theta = np.linspace(0.0, 2.0 * math.pi, 1000, endpoint=False)
    rotation_covariance = bool(
        np.array_equal(
            role_index(shifted_theta, 0.37),
            role_index(shifted_theta + 0.91, 0.37 + 0.91),
        )
    )
    role_resolution = angular_role_resolution(
        geometry, star0, h20, hi0, wcs, common, target_beam
    )

    measurement, baseline_phase = measurement_audit(
        geometry,
        star0,
        h20,
        hi0,
        wcs,
        common,
        uncertainty,
        radial_mode,
        target_beam,
    )
    expected_measurement_rows = N_DRAWS * len(MEASUREMENT_SCENARIOS) * len(HARMONICS)
    if len(measurement) != expected_measurement_rows:
        raise ValueError("Incomplete measurement Cartesian product")
    measurement.to_csv(MEASUREMENT_PATH, index=False, float_format="%.10g")

    summary = summarize(
        systematics,
        measurement,
        baseline,
        baseline_phase,
        beam_area_pixels,
        minimum_required_role_pixels,
        role_resolution,
    )
    m2_pass = bool(
        summary.loc[summary["harmonic"].eq(TARGET_HARMONIC), "passes_own_internal_gates"].iloc[0]
    )
    m1_pass = bool(
        summary.loc[summary["harmonic"].eq(CONTROL_HARMONIC), "passes_own_internal_gates"].iloc[0]
    )
    family_specificity_pass = bool(m2_pass and not m1_pass)
    summary["family_specificity_gate"] = False
    summary.loc[summary["harmonic"].eq(TARGET_HARMONIC), "family_specificity_gate"] = family_specificity_pass
    summary["survives_v07_selection"] = False
    summary.loc[summary["harmonic"].eq(TARGET_HARMONIC), "survives_v07_selection"] = family_specificity_pass
    summary.to_csv(SUMMARY_PATH, index=False, float_format="%.10g")

    if family_specificity_pass:
        candidate_status = "DIRECT_BEAM_M2_SOURCE_CANDIDATE_SURVIVES_INTERNAL_SPECIFICITY_GATE"
    elif m2_pass and m1_pass:
        candidate_status = "M2_AND_M1_BOTH_PASS_NO_INTERNAL_FAMILY_SPECIFICITY"
    else:
        candidate_status = "DIRECT_BEAM_M2_SOURCE_CANDIDATE_FAILS_INTERNAL_GATES"

    manifest = {
        "schema": "ngc4254_ffl_direct_beam_m2_operator_v07",
        "status": STATUS,
        "candidate_status": candidate_status,
        "galaxy": "NGC4254",
        "construction": {
            "target_family": "stellar_m2_phase_four-role chart",
            "alternative_family_control": "stellar_m1_phase four-role chart processed identically",
            "phase_estimator": "annulus-median-subtracted log-stellar contrast over inherited 5-65 arcsec support",
            "direct_operator": "axisymmetry-subtracted pixel fields weighted by the linearly interpolated frozen v06 beam_mode=1 radial eigenvector, normalized within each full-support role",
            "sparse_annulus_role_cells_used": False,
            "radial_midpoints_arcsec": midpoints.tolist(),
            "v06_surviving_beam_mode_index": V06_SURVIVING_BEAM_MODE_INDEX,
            "radial_beam_mode_1": radial_mode.tolist(),
            "radial_weight_zero_crossings_arcsec": linear_zero_crossings(midpoints, radial_mode),
            "beam_mode_1_eigenvalue": float(
                beam_eigenvalues[V06_SURVIVING_BEAM_MODE_INDEX]
            ),
            "phase_stability_limit_deg": PHASE_STABILITY_LIMIT_DEG,
            "phase_limit_reason": "half of one pi/2 role-sector width",
            "role_edge_perturbation_deg": ROLE_EDGE_PERTURBATION_DEG,
            "beam_support_rule": "each full angular role must contain at least one Gaussian beam area in source pixels",
            "gaussian_beam_area_arcsec2": beam_area_arcsec2,
            "gaussian_beam_area_pixels": beam_area_pixels,
            "minimum_required_role_pixels": minimum_required_role_pixels,
            "relative_role_rank_rule": "algebraic rank must equal the full three-dimensional relative-role space",
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
            "v06_source_role_audit": str(V06_PATH.relative_to(ROOT)),
            "v06_source_role_audit_sha256": sha256(V06_PATH),
            "velocity_or_residual_inputs": [],
        },
        "source_systematic_audit": {
            "n_rows": len(systematics),
            "n_scenarios_per_harmonic": 72,
            "geometry_variants": 8,
            "stellar_psf_controls": 3,
            "h2_conversion_controls": 3,
        },
        "measurement_audit": {
            "random_seed": RANDOM_SEED,
            "n_draws": N_DRAWS,
            "scenarios": list(MEASUREMENT_SCENARIOS),
            "primary_gate_scenario": PRIMARY_MEASUREMENT_SCENARIO,
            "n_rows": len(measurement),
            "hi_role": "robust1 49-channel control only",
        },
        "baseline": {
            f"m{harmonic}": values for harmonic, values in baseline_diagnostics.items()
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
                for harmonic, values in baseline_diagnostics.items()
            },
            "angular_role_beam_screen": role_resolution,
            "beam_overlap_is_complete_covariance": False,
        },
        "result": {
            "m2_passes_own_internal_gates": m2_pass,
            "m1_alternative_control_passes_own_internal_gates": m1_pass,
            "m2_family_specificity_pass": family_specificity_pass,
            "source_candidate_survives_v07": family_specificity_pass,
            "physical_role_chart_promoted": False,
            "physical_q_det_constructed": False,
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
            "complete_source_systematic_product": len(systematics) == expected_systematic_rows,
            "complete_measurement_product": len(measurement) == expected_measurement_rows,
            "all_q_values_finite": bool(
                np.isfinite(systematics["q_shape_proxy"]).all()
                and np.isfinite(measurement["q_shape_proxy"]).all()
            ),
            "sparse_annulus_role_cells_eliminated": True,
            "target_and_control_share_operator": True,
            "endpoint_scored": False,
        },
        "known_limitations": [
            "m=2 and m=1 remain finite source-coordinate families, not parent-derived role identities",
            "the radial weight comes from a support-overlap beam screen, not a complete nonlinear q covariance",
            "one-beam pixel support is a resolution floor, not proof of independent role information",
            "the stellar measurement modes remain a conditional P5 uncertainty reconstruction",
            "the H I measurement layer remains a robust-1 control for a robust-5 moment map",
            "family specificity in one galaxy would not establish universality",
            "passing source gates would not construct physical eta, q_det, determinant transport, or a terminal map",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }

    table_rows = []
    for row in summary.itertuples():
        table_rows.append(
            "| "
            f"m={int(row.harmonic)} | {row.family_role} | {row.baseline_q_shape_proxy:+.6f} | "
            f"{row.source_q_min:+.6f}, {row.source_q_max:+.6f} | "
            f"{row.source_phase_max_delta_deg:.2f} | "
            f"{row.measurement_q_p025:+.6f}, {row.measurement_q_p975:+.6f} | "
            f"{row.measurement_baseline_sign_probability:.3f} | "
            f"{row.measurement_phase_p95_delta_deg:.2f} | "
            f"{int(row.minimum_role_pixels_source_systematics)} | "
            f"{'PASS' if row.passes_own_internal_gates else 'FAIL'} |"
        )
    report = f"""# NGC4254 Direct Beam-Resolved m=2 Operator Audit v07

**Status:** `{STATUS}`

**Candidate verdict:** `{candidate_status}`

**Claim boundary:** {CLAIM_BOUNDARY}.

## Frozen Construction

The v06 `m=2`, `beam_mode=1` source candidate is tested without retaining any
annulus-by-role cell. The corresponding six-component radial beam eigenvector
is linearly interpolated onto source pixels. Observer-path, log-stellar, and
log-gas fields are each stripped of an all-role radial median baseline; their
remaining pixels are then projected directly within the four morphology-phase
roles and centered before the inherited `E_S` determinant proxy is evaluated.

The `m=1` phase family receives exactly the same operator and gates. It is an
alternative-family specificity control, not an asserted physically wrong
family. The `m=2` selection survives only if `m=2` passes and `m=1` does not.

## Finite Audit

| family | role | baseline q | 72-source range | max source phase shift (deg) | measurement 95% q | P(baseline sign) | measurement phase p95 (deg) | min role pixels | own gates |
|---:|---|---:|---:|---:|---:|---:|---:|---:|:---:|
{chr(10).join(table_rows)}

Passing the own-family gate requires stable source and measurement sign,
source and measurement phase shifts below `{PHASE_STABILITY_LIMIT_DEG}` degrees,
all three relative role directions in the beam screen, and at least one full
Gaussian beam area per angular role. Here one beam is
`{beam_area_pixels:.3f}` pixels, so the frozen minimum is
`{minimum_required_role_pixels}` pixels.

## Validation

- The radial mode crosses zero at
  `{[round(value, 4) for value in linear_zero_crossings(midpoints, radial_mode)]}`
  arcsec, implementing an inner-versus-outer contrast rather than six discrete
  annulus-role coordinates.
- Baseline full-role counts are `m=1:
  {baseline_diagnostics[1]['role_0_pixels'], baseline_diagnostics[1]['role_1_pixels'], baseline_diagnostics[1]['role_2_pixels'], baseline_diagnostics[1]['role_3_pixels']}`
  and `m=2:
  {baseline_diagnostics[2]['role_0_pixels'], baseline_diagnostics[2]['role_1_pixels'], baseline_diagnostics[2]['role_2_pixels'], baseline_diagnostics[2]['role_3_pixels']}`.
- A global stellar rescaling changes q by at most
  `{max(scale_invariance.values()):.3e}`.
- Simultaneously rotating theta and its morphology anchor preserves every role
  label exactly: `{rotation_covariance}`.
- A +/-`{ROLE_EDGE_PERTURBATION_DEG}` degree role-edge perturbation changes q by
  at most `{max(edge_sensitivity.values()):.6g}`.
- The independent flux-phase estimator differs from the primary phase by
  `m=1: {baseline_diagnostics[1]['phase_estimator_difference_deg']:.3f}` degrees
  and `m=2: {baseline_diagnostics[2]['phase_estimator_difference_deg']:.3f}`
  degrees.

## Verdict

`m=2` own gates: `{m2_pass}`. `m=1` alternative-control own gates: `{m1_pass}`.
The source-only family-specificity gate is therefore
`{family_specificity_pass}`.

This finite audit removes the sparse-cell blocker from the tested operator,
but it does not turn `q_shape_proxy` into physical `q_det`. No parent role,
complete channel, time or quantum terminal, dark-sector replacement, or
endpoint score is identified.
"""
    REPORT_PATH.write_text(report)
    JSON_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(STATUS)
    print(candidate_status)
    print(f"m2_pass={m2_pass} m1_control_pass={m1_pass} specificity={family_specificity_pass}")


if __name__ == "__main__":
    main()
