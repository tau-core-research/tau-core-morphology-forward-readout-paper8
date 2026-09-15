#!/usr/bin/env python3
"""Post-open nuisance audit of the NGC2541 HALOGAS calibration endpoint."""

from __future__ import annotations

import json
import math
from pathlib import Path

import astropy.units as u
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS


ROOT = Path(__file__).resolve().parents[1]
GEOMETRY = ROOT / "data/derived/ngc2541_signed_descriptor_source_geometry_freeze_v01_points.csv"
ENDPOINT = ROOT / "data/external/literature/ngc2541_halogas_independent_endpoint_v01"
MOM0 = ENDPOINT / "NGC2541-HR_mom0m.fits"
MOM1 = ENDPOINT / "NGC2541-HR_mom1m.fits"
OUT_JSON = ROOT / "data/derived/ngc2541_halogas_calibration_nuisance_v02.json"
OUT_CSV = ROOT / "data/derived/ngc2541_halogas_calibration_nuisance_v02_scenarios.csv"
REPORT = ROOT / "reports/ngc2541_halogas_side_consistency_nuisance_audit_v02.md"

VSYS_KMS = 559.5
MINIMUM_PIXELS = 8
NED_CENTRE = SkyCoord("08h14m40.07s", "+49d03m41.2s", frame="icrs")
JOZSA_FITTED_CENTRE = SkyCoord("08h14m40.83s", "+49d03m33.6s", frame="icrs")


def load_map(path: Path) -> tuple[np.ndarray, fits.Header]:
    with fits.open(path, memmap=True) as hdul:
        return np.asarray(hdul[0].data, dtype=float).squeeze(), hdul[0].header.copy()


def geometry_from_normals(source: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    n_w = source["n_w_unit"].to_numpy(float)
    n_n = source["n_n_unit"].to_numpy(float)
    n_los = source["n_los_unit"].to_numpy(float)
    inclination = np.degrees(np.arccos(np.clip(n_los, -1.0, 1.0)))
    normal_pa = np.degrees(np.arctan2(-n_w, n_n)) % 360.0
    major_pa = (normal_pa + 90.0) % 180.0
    unwrapped_major_pa = np.degrees(np.unwrap(np.radians(2.0 * major_pa))) / 2.0
    return inclination, unwrapped_major_pa


def disk_coordinates(
    east: np.ndarray,
    north: np.ndarray,
    inclination_deg: np.ndarray,
    major_pa_deg: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    pa = np.radians(major_pa_deg)
    inclination = np.radians(inclination_deg)
    major = east * np.sin(pa) + north * np.cos(pa)
    minor = -east * np.cos(pa) + north * np.sin(pa)
    radius = np.hypot(major, minor / np.cos(inclination))
    cos_theta = np.divide(major, radius, out=np.zeros_like(radius), where=radius > 0.0)
    return radius, cos_theta


def variable_geometry(
    east: np.ndarray,
    north: np.ndarray,
    centres: np.ndarray,
    inclination_nodes: np.ndarray,
    pa_nodes: np.ndarray,
    iterations: int,
    diagnostic_mask: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, float]]:
    radius = np.hypot(east, north)
    for _ in range(iterations):
        inclination = np.interp(
            radius, centres, inclination_nodes, left=inclination_nodes[0], right=inclination_nodes[-1]
        )
        pa = np.interp(radius, centres, pa_nodes, left=pa_nodes[0], right=pa_nodes[-1])
        radius, cos_theta = disk_coordinates(east, north, inclination, pa)

    next_inclination = np.interp(
        radius, centres, inclination_nodes, left=inclination_nodes[0], right=inclination_nodes[-1]
    )
    next_pa = np.interp(radius, centres, pa_nodes, left=pa_nodes[0], right=pa_nodes[-1])
    next_radius, _ = disk_coordinates(east, north, next_inclination, next_pa)
    support = diagnostic_mask & (radius >= 30.0) & (radius < 590.0)
    step = np.abs(next_radius[support] - radius[support])
    diagnostic = {
        "median_next_step_arcsec": float(np.median(step)),
        "p95_next_step_arcsec": float(np.quantile(step, 0.95)),
        "maximum_next_step_arcsec": float(np.max(step)),
    }
    return radius, cos_theta, inclination, diagnostic


def common_pixel_ring_summary(
    fixed_radius: np.ndarray,
    fixed_cos: np.ndarray,
    fixed_inclination: np.ndarray,
    variable_radius: np.ndarray,
    variable_cos: np.ndarray,
    variable_inclination: np.ndarray,
    velocity: np.ndarray,
    valid: np.ndarray,
    centres: np.ndarray,
    edges: np.ndarray,
) -> tuple[pd.DataFrame, dict[str, float]]:
    fixed_speed = (velocity - VSYS_KMS) / (np.sin(np.radians(fixed_inclination)) * fixed_cos)
    variable_speed = (velocity - VSYS_KMS) / (np.sin(np.radians(variable_inclination)) * variable_cos)
    rows: list[dict[str, float | int | bool]] = []
    for centre, lo, hi in zip(centres, edges[:-1], edges[1:]):
        fixed_selection = (
            valid & (fixed_radius >= lo) & (fixed_radius < hi) & (np.abs(fixed_cos) >= 0.8)
        )
        variable_selection = (
            valid & (variable_radius >= lo) & (variable_radius < hi) & (np.abs(variable_cos) >= 0.8)
        )
        common = fixed_selection & variable_selection & (np.sign(fixed_cos) == np.sign(variable_cos))
        positive = common & (fixed_cos > 0.0)
        negative = common & (fixed_cos < 0.0)
        eligible = int(positive.sum()) >= MINIMUM_PIXELS and int(negative.sum()) >= MINIMUM_PIXELS
        fixed_difference = math.nan
        variable_difference = math.nan
        if eligible:
            fixed_difference = abs(float(np.median(fixed_speed[positive]) - np.median(fixed_speed[negative])))
            variable_difference = abs(
                float(np.median(variable_speed[positive]) - np.median(variable_speed[negative]))
            )
        rows.append(
            {
                "radius_arcsec": float(centre),
                "n_common_positive_pixels": int(positive.sum()),
                "n_common_negative_pixels": int(negative.sum()),
                "fixed_absolute_side_difference_kms": fixed_difference,
                "variable_absolute_side_difference_kms": variable_difference,
                "eligible": bool(eligible),
            }
        )
    frame = pd.DataFrame(rows)
    eligible = frame[frame["eligible"]]
    fixed = eligible["fixed_absolute_side_difference_kms"].to_numpy(float)
    variable = eligible["variable_absolute_side_difference_kms"].to_numpy(float)
    delta = variable - fixed
    score = {
        "n_common_eligible_rings": int(len(eligible)),
        "fixed_mean_absolute_side_difference_kms": float(np.mean(fixed)),
        "variable_mean_absolute_side_difference_kms": float(np.mean(variable)),
        "delta_mean_variable_minus_fixed_kms": float(np.mean(delta)),
        "fraction_common_rings_improved": float(np.mean(delta < 0.0)),
    }
    return frame, score


def markdown_table(frame: pd.DataFrame) -> str:
    columns = list(frame.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in frame.iterrows():
        values = []
        for column in columns:
            value = row[column]
            values.append(f"{value:.6f}" if isinstance(value, (float, np.floating)) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def main() -> None:
    mom0, header0 = load_map(MOM0)
    mom1, header1 = load_map(MOM1)
    if mom0.shape != mom1.shape:
        raise RuntimeError("moment-map shapes differ")
    wcs0 = WCS(header0).celestial
    wcs1 = WCS(header1).celestial
    if not wcs0.wcs.compare(wcs1.wcs):
        raise RuntimeError("moment-map celestial WCS differs")

    yy, xx = np.indices(mom0.shape)
    sky = wcs0.pixel_to_world(xx, yy)
    valid = np.isfinite(mom0) & (mom0 > 0.0) & np.isfinite(mom1)
    source = pd.read_csv(GEOMETRY)
    centres = source["radius_arcsec"].to_numpy(float)
    edges = np.r_[30.0, (centres[:-1] + centres[1:]) / 2.0, 590.0]
    inclination_nodes, pa_nodes = geometry_from_normals(source)

    centre_cases = {
        "NED": NED_CENTRE,
        "JOZSA_FITTED": JOZSA_FITTED_CENTRE,
        "NED_E_PLUS_4_ARCSEC": NED_CENTRE.spherical_offsets_by(4.0 * u.arcsec, 0.0 * u.arcsec),
        "NED_E_MINUS_4_ARCSEC": NED_CENTRE.spherical_offsets_by(-4.0 * u.arcsec, 0.0 * u.arcsec),
        "NED_N_PLUS_4_ARCSEC": NED_CENTRE.spherical_offsets_by(0.0 * u.arcsec, 4.0 * u.arcsec),
        "NED_N_MINUS_4_ARCSEC": NED_CENTRE.spherical_offsets_by(0.0 * u.arcsec, -4.0 * u.arcsec),
    }
    scenario_rows: list[dict[str, float | int | str]] = []
    convergence: dict[str, dict[str, dict[str, float]]] = {}
    for centre_name, centre_icrs in centre_cases.items():
        centre = centre_icrs.transform_to(sky.frame)
        east, north = centre.spherical_offsets_to(sky)
        east = east.to_value(u.arcsec)
        north = north.to_value(u.arcsec)
        fixed_inclination = np.full(mom0.shape, 66.3)
        fixed_pa = np.full(mom0.shape, 171.2)
        fixed_radius, fixed_cos = disk_coordinates(east, north, fixed_inclination, fixed_pa)
        convergence[centre_name] = {}
        for iterations in (4, 20):
            variable_radius, variable_cos, variable_inclination, solver_diagnostic = variable_geometry(
                east, north, centres, inclination_nodes, pa_nodes, iterations, valid
            )
            _, score = common_pixel_ring_summary(
                fixed_radius,
                fixed_cos,
                fixed_inclination,
                variable_radius,
                variable_cos,
                variable_inclination,
                mom1,
                valid,
                centres,
                edges,
            )
            convergence[centre_name][str(iterations)] = solver_diagnostic
            scenario_rows.append(
                {
                    "centre_case": centre_name,
                    "iterations": iterations,
                    "footprint": "COMMON_SKY_PIXEL_INTERSECTION",
                    **score,
                    **solver_diagnostic,
                }
            )

    scenarios = pd.DataFrame(scenario_rows)
    pixel_area_deg2 = float(abs(np.linalg.det(wcs0.pixel_scale_matrix)))
    beam_area_deg2 = float(np.pi * header0["BMAJ"] * header0["BMIN"] / (4.0 * np.log(2.0)))
    pixels_per_beam = beam_area_deg2 / pixel_area_deg2
    spacings = np.diff(centres)
    directions = np.sign(scenarios["delta_mean_variable_minus_fixed_kms"].to_numpy(float))
    result = {
        "schema": "tau_core_ngc2541_halogas_calibration_nuisance_v02",
        "status": "POST_OPEN_DESCRIPTIVE_DIAGNOSTIC_CALIBRATION_UNSTABLE",
        "endpoint": "NGC2541 HALOGAS DR1 HR moment-0/moment-1",
        "systemic_velocity_kms_held_fixed": VSYS_KMS,
        "footprint_rule": "fixed and variable estimators use the identical sky pixels in each ring and side",
        "centre_cases": list(centre_cases),
        "ned_to_jozsa_fitted_centre_separation_arcsec": float(
            NED_CENTRE.separation(JOZSA_FITTED_CENTRE).to_value(u.arcsec)
        ),
        "solver_iterations_compared": [4, 20],
        "nuisance_direction_contains_improvement_and_worsening": bool(np.any(directions < 0) and np.any(directions > 0)),
        "calibration_direction_stable": bool(np.all(directions < 0) or np.all(directions > 0)),
        "beam_correlation_audit": {
            "beam_major_arcsec": float(header0["BMAJ"] * 3600.0),
            "beam_minor_arcsec": float(header0["BMIN"] * 3600.0),
            "pixel_scale_arcsec": float(np.sqrt(pixel_area_deg2) * 3600.0),
            "pixels_per_gaussian_beam": float(pixels_per_beam),
            "minimum_pixels_per_side_ring_in_v01": MINIMUM_PIXELS,
            "minimum_pixels_in_beams": float(MINIMUM_PIXELS / pixels_per_beam),
            "minimum_ring_spacing_arcsec": float(spacings.min()),
            "median_ring_spacing_arcsec": float(np.median(spacings)),
            "ring_spacing_below_beam_major_present": bool(np.any(spacings < header0["BMAJ"] * 3600.0)),
            "consequence": "pixel counts and adjacent rings cannot be treated as independent samples",
        },
        "source_uncertainty_limitation": {
            "maximum_inclination_error_deg": float(source["e_inclination_deg"].max()),
            "maximum_pa_error_deg": float(source["e_pa_deg"].max()),
            "propagated_in_v02": False,
            "covariance_available_in_source_table": False,
            "consequence": "the source ring geometry is frozen but not known exactly; this audit cannot form a physical confidence interval",
        },
        "moment1_limitation": (
            "Moment-1 is an intensity-weighted line-of-sight velocity. It is not a thin-disc circular-speed "
            "measurement and can be biased by line-of-sight warp overlap and slower extraplanar gas."
        ),
        "statistical_claim": (
            "The scenario deltas are descriptive nuisance checks. Correlated pixels/rings and unpropagated "
            "source uncertainty prohibit interpreting them as independent-sample significance."
        ),
        "claim_boundary": (
            "Post-open standard-calibration diagnostic only. The sign of the small mean change is unstable "
            "under source-relevant centre choices; no Tau q_R, physical calibration law, Nature occupation, "
            "or dark-matter-replacement evidence follows."
        ),
        "convergence_diagnostics": convergence,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    scenarios.to_csv(OUT_CSV, index=False, float_format="%.12g")
    OUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    display = scenarios[
        [
            "centre_case",
            "iterations",
            "n_common_eligible_rings",
            "fixed_mean_absolute_side_difference_kms",
            "variable_mean_absolute_side_difference_kms",
            "delta_mean_variable_minus_fixed_kms",
            "fraction_common_rings_improved",
            "median_next_step_arcsec",
            "p95_next_step_arcsec",
        ]
    ]
    REPORT.write_text(
        "# NGC2541 HALOGAS calibration nuisance audit v02\n\n"
        f"Status: `{result['status']}`. All rows use the common fixed/variable sky-pixel intersection.\n\n"
        + markdown_table(display)
        + "\n\nThe NED-centred directional change is not stable under the source-published "
        "Józsa fitted kinematic centre or under four-arcsecond cardinal centre shifts. "
        "The four-iteration solver also lacks a demonstrated convergence tolerance.\n\n"
        f"The HR beam contains `{pixels_per_beam:.6f}` map pixels, whereas the v01 gate accepted "
        f"only `{MINIMUM_PIXELS}` pixels (`{MINIMUM_PIXELS / pixels_per_beam:.6f}` beams) per side. "
        "Some source-ring spacings are below the synthesized beam, so pixel and ring independence "
        "must not be assumed.\n\n"
        "Published inclination/PA uncertainties and their covariance are not propagated. The moment-1 "
        "terminal is intensity-weighted and remains vulnerable to warp overlap and extraplanar-gas bias.\n\n"
        + result["claim_boundary"]
        + "\n",
        encoding="utf-8",
    )
    print("NGC2541_HALOGAS_CALIBRATION_NUISANCE_V02_COMPLETE")


if __name__ == "__main__":
    main()
