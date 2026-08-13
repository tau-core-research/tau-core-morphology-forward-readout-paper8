#!/usr/bin/env python3
"""Open and score the four-galaxy PHANGS body-projection endpoint once."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales
from scipy.ndimage import gaussian_filter, map_coordinates

from acquire_phangs_radial_body_projection_confirmatory_packet_v01 import CONFIG, CONFIRMATORY
from build_phangs_population_channel_preregistration_v01 import GEOMETRY
from build_phangs_radial_body_projection_development_preflight_v01 import (
    S4G_PSF_FWHM_ARCSEC,
    disk_coordinates,
    embed,
    finite_difference,
    harmonic_profile,
    normalized_smooth,
    read_image,
)
from freeze_phangs_radial_body_projection_scoring_contract_v01 import (
    aggregate,
    assemble_decision_covariance,
    fit_modes,
    phase_rotate_pi_over_2,
    radial_reverse,
    score,
    sector_jackknife_block,
    stable_rank,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
EXTERNAL = ROOT / "data/external/literature/phangs_radial_body_projection_confirmatory_v01"
SAMPLE = ROOT / "data/external/phangs/phangs_public_sample.csv"
ACQUISITION = DATA / "phangs_radial_body_projection_confirmatory_acquisition_v01.json"
CONTRACT = DATA / "phangs_radial_body_projection_scoring_contract_v01.json"
OUTPUT = DATA / "phangs_radial_body_projection_confirmatory_endpoint_v01.json"
COEFFICIENTS = DATA / "phangs_radial_body_projection_confirmatory_coefficients_v01.csv"
MATRICES = DATA / "phangs_radial_body_projection_confirmatory_matrices_v01.npz"
REPORT = ROOT / "reports/phangs_radial_body_projection_confirmatory_endpoint_v01.md"

N_ZONES = 5
N_SECTORS = 12
MAX_VELOCITY_ERROR = 10.0
MIN_FLUX_SNR = 5.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sample_to_wcs(data: np.ndarray, source_wcs: WCS, target_wcs: WCS, shape: tuple[int, int]) -> np.ndarray:
    yy, xx = np.indices(shape, dtype=float)
    ra, dec = target_wcs.pixel_to_world_values(xx, yy)
    sx, sy = source_wcs.world_to_pixel_values(ra, dec)
    return map_coordinates(data, [sy, sx], order=1, mode="constant", cval=np.nan)


def source_matrix(
    galaxy: str, center: tuple[float, float], edges: np.ndarray, terminal_co_beam: float
) -> np.ndarray:
    directory = EXTERNAL / galaxy
    stellar, _, stellar_wcs = read_image(next(directory.glob("*.phot.1.fits")))
    source_mask, _, _ = read_image(next(directory.glob("*.1.final_mask.fits")))
    co, co_header, co_wcs = read_image(next(directory.glob("*broad_mom0.fits")))
    pa, inclination = GEOMETRY[galaxy]
    stellar_radius, stellar_theta = disk_coordinates(stellar_wcs, stellar.shape, center, pa, inclination)
    co_radius, co_theta = disk_coordinates(co_wcs, co.shape, center, pa, inclination)

    stellar_pixel = float(np.mean(np.abs(proj_plane_pixel_scales(stellar_wcs))) * 3600.0)
    co_pixel = float(np.mean(np.abs(proj_plane_pixel_scales(co_wcs))) * 3600.0)
    co_beam = math.sqrt(float(co_header["BMAJ"]) * float(co_header["BMIN"])) * 3600.0
    if abs(co_beam - terminal_co_beam) > 1.0e-6:
        raise RuntimeError("Source and terminal CO products disagree on the frozen beam")
    target_beam = max(S4G_PSF_FWHM_ARCSEC, co_beam)
    stellar_sigma = math.sqrt(max(target_beam**2 - S4G_PSF_FWHM_ARCSEC**2, 0.0)) / 2.35482 / stellar_pixel
    co_sigma = math.sqrt(max(target_beam**2 - co_beam**2, 0.0)) / 2.35482 / co_pixel

    stellar_valid = np.isfinite(stellar) & (source_mask == 0)
    outer = stellar_valid & (stellar_radius >= np.nanquantile(stellar_radius[stellar_valid], 0.8))
    stellar_signal = normalized_smooth(stellar - np.nanmedian(stellar[outer]), stellar_valid, stellar_sigma)
    co_finite = np.isfinite(co)
    co_noise = 1.4826 * float(np.nanmedian(np.abs(co[co_finite] - np.nanmedian(co[co_finite]))))
    co_support = co_finite & (co > 3.0 * co_noise)
    co_signal = normalized_smooth(co, co_finite, co_sigma)
    profiles = {
        "stellar_m1": harmonic_profile(
            stellar_signal, stellar_radius, stellar_theta,
            np.isfinite(stellar_signal) & (stellar_signal > 0), edges, 1,
        ),
        "stellar_m2": harmonic_profile(
            stellar_signal, stellar_radius, stellar_theta,
            np.isfinite(stellar_signal) & (stellar_signal > 0), edges, 2,
        ),
        "co_m1": harmonic_profile(co_signal, co_radius, co_theta, np.isfinite(co_signal) & co_support, edges, 1),
        "co_m2": harmonic_profile(co_signal, co_radius, co_theta, np.isfinite(co_signal) & co_support, edges, 2),
    }
    return np.column_stack([
        embed(profiles["stellar_m1"], 1),
        embed(finite_difference(profiles["stellar_m1"]), 1),
        embed(profiles["stellar_m2"], 2),
        embed(finite_difference(profiles["stellar_m2"]), 2),
        embed(profiles["co_m1"], 1),
        embed(finite_difference(profiles["co_m1"]), 1),
        embed(profiles["co_m2"], 2),
        embed(finite_difference(profiles["co_m2"]), 2),
    ])


def open_galaxy(galaxy: str, center: tuple[float, float]) -> dict[str, Any]:
    directory = EXTERNAL / galaxy
    maps_path = next(directory.glob("*_MAPS_copt_*.fits"))
    co_path = next(path for path in directory.glob("*_mom1wprior.fits") if "_emom1wprior" not in path.name)
    eco_path = next(directory.glob("*_emom1wprior.fits"))
    with fits.open(maps_path, memmap=True) as hdul:
        flux = np.asarray(hdul["HA6562_FLUX"].data, dtype=float)
        eflux = np.asarray(hdul["HA6562_FLUX_ERR"].data, dtype=float)
        velocity = np.asarray(hdul["HA6562_VEL"].data, dtype=float)
        evelocity = np.asarray(hdul["HA6562_VEL_ERR"].data, dtype=float)
        muse_wcs = WCS(hdul["HA6562_VEL"].header, naxis=2)
    with fits.open(co_path, memmap=True) as hdul:
        co_velocity = np.squeeze(np.asarray(hdul[0].data, dtype=float))
        co_header = hdul[0].header.copy()
        co_wcs = WCS(co_header, naxis=2)
    with fits.open(eco_path, memmap=True) as hdul:
        co_error = np.squeeze(np.asarray(hdul[0].data, dtype=float))

    muse_psf = float(CONFIG[galaxy]["muse_psf_arcsec"])
    co_beam = math.sqrt(float(co_header["BMAJ"]) * float(co_header["BMIN"])) * 3600.0
    muse_pixel = float(np.mean(np.abs(proj_plane_pixel_scales(muse_wcs))) * 3600.0)
    sigma_pixels = math.sqrt(max(co_beam**2 - muse_psf**2, 0.0)) / 2.354820045 / muse_pixel
    valid_flux = np.isfinite(flux) & np.isfinite(velocity) & (flux > 0)
    weighted_velocity = gaussian_filter(np.where(valid_flux, flux * velocity, 0.0), sigma_pixels)
    smoothed_flux = gaussian_filter(np.where(valid_flux, flux, 0.0), sigma_pixels)
    smoothed_velocity = np.divide(
        weighted_velocity, smoothed_flux, out=np.full_like(weighted_velocity, np.nan), where=smoothed_flux > 0
    )
    ha_velocity = sample_to_wcs(smoothed_velocity, muse_wcs, co_wcs, co_velocity.shape)
    ha_error = sample_to_wcs(evelocity, muse_wcs, co_wcs, co_velocity.shape)
    ha_flux = sample_to_wcs(flux, muse_wcs, co_wcs, co_velocity.shape)
    ha_eflux = sample_to_wcs(eflux, muse_wcs, co_wcs, co_velocity.shape)

    pa, inclination = GEOMETRY[galaxy]
    radius, theta = disk_coordinates(co_wcs, co_velocity.shape, center, pa, inclination)
    snr = ha_flux / ha_eflux
    mask = (
        np.isfinite(co_velocity) & np.isfinite(co_error) & (co_error > 0)
        & (co_error <= MAX_VELOCITY_ERROR) & np.isfinite(ha_velocity)
        & np.isfinite(ha_error) & (ha_error > 0) & (ha_error <= MAX_VELOCITY_ERROR)
        & np.isfinite(snr) & (snr >= MIN_FLUX_SNR) & (np.abs(ha_velocity) < 450.0)
    )
    co_pixel = float(np.mean(np.abs(proj_plane_pixel_scales(co_wcs))) * 3600.0)
    beam_pixels = max(1, int(math.ceil(co_beam / co_pixel)))
    yy, xx = np.indices(co_velocity.shape)
    independent = mask & ((xx % beam_pixels) == 0) & ((yy % beam_pixels) == 0)
    if int(independent.sum()) < 50:
        raise RuntimeError("Insufficient beam-independent common support")

    edges = np.quantile(radius[independent], np.linspace(0.0, 1.0, N_ZONES + 1))
    matrix = source_matrix(galaxy, center, edges, co_beam)
    if stable_rank(matrix) != 8:
        raise RuntimeError(f"Source matrix rank is {stable_rank(matrix)}, expected 8")

    offset = float(np.median((co_velocity - ha_velocity)[independent]))
    contrast = co_velocity - offset - ha_velocity
    variance = co_error**2 + ha_error**2
    terminal = []
    covariance_blocks = []
    rows = []
    for zone in range(N_ZONES):
        select = independent & (radius >= edges[zone]) & (
            radius <= edges[zone + 1] if zone == N_ZONES - 1 else radius < edges[zone + 1]
        )
        angle = theta[select]
        design = np.column_stack([
            np.ones(select.sum()), np.cos(angle), np.sin(angle), np.cos(2 * angle), np.sin(2 * angle)
        ])
        sectors = np.floor(((angle + np.pi) % (2 * np.pi)) / (2 * np.pi) * N_SECTORS).astype(int)
        coefficient = fit_modes(design, contrast[select], variance[select])
        covariance_blocks.append(
            sector_jackknife_block(design, contrast[select], variance[select], sectors)
        )
        terminal.extend(coefficient[1:5])
        for mode, value in zip(("m1_cos", "m1_sin", "m2_cos", "m2_sin"), coefficient[1:5]):
            rows.append({
                "galaxy": galaxy, "zone": zone, "mode": mode, "co_minus_halpha_km_s": float(value),
                "radius_min_arcsec": float(edges[zone]), "radius_max_arcsec": float(edges[zone + 1]),
                "n_independent_pixels": int(select.sum()), "occupied_sectors": int(len(np.unique(sectors))),
            })
    covariance = assemble_decision_covariance(covariance_blocks)
    terminal_array = np.asarray(terminal)
    primary = score(matrix, covariance, terminal_array)
    reverse = score(radial_reverse(matrix), covariance, terminal_array)
    phase = score(phase_rotate_pi_over_2(matrix), covariance, terminal_array)
    stellar_only = score(matrix[:, :4], covariance, terminal_array)
    co_only = score(matrix[:, 4:], covariance, terminal_array)
    if primary["projection_rank"] != 12 or primary["projected_covariance_rank"] != 12:
        raise RuntimeError("Projected endpoint rank gate failed")
    return {
        "matrix": matrix,
        "rows": rows,
        "metrics": {
            "beam_independent_pixels": int(independent.sum()),
            "co_beam_arcsec": co_beam,
            "muse_psf_arcsec": muse_psf,
            "velocity_zero_point_offset_km_s": offset,
            "radial_edges_arcsec": edges.tolist(),
            "source_rank": stable_rank(matrix),
            "primary": primary,
            "radial_reversal": reverse,
            "phase_rotation_pi_over_2": phase,
            "stellar_only_ablation": stellar_only,
            "co_only_ablation": co_only,
        },
    }


def main() -> None:
    acquisition = json.loads(ACQUISITION.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if acquisition["status"] != "CONFIRMATORY_PACKET_ACQUIRED_HASH_FROZEN_VALUES_UNOPENED":
        raise RuntimeError("Confirmatory packet is not frozen and unopened")
    if acquisition["confirmatory_galaxies"] != CONFIRMATORY or contract["confirmatory_galaxies_opened"]:
        raise RuntimeError("Confirmatory membership or opening boundary changed")
    for key, expected in acquisition["source_hashes_sha256"].items():
        if sha256(EXTERNAL / key) != expected:
            raise RuntimeError(f"Hash mismatch before endpoint opening: {key}")

    sample = pd.read_csv(SAMPLE, skiprows=[1]).set_index("Name")
    opened: dict[str, Any] = {}
    failures: dict[str, str] = {}
    for galaxy in CONFIRMATORY:
        center = (float(sample.loc[galaxy, "R.A."]), float(sample.loc[galaxy, "Dec."]))
        try:
            opened[galaxy] = open_galaxy(galaxy, center)
        except Exception as error:  # preserve all-body eligibility failures without a partial score
            failures[galaxy] = f"{type(error).__name__}: {error}"

    if failures:
        result = {
            "schema": "phangs_radial_body_projection_confirmatory_endpoint_v01",
            "status": "CONFIRMATORY_ENDPOINT_OPENED_NONIDENTIFIABLE_GATE_FAILURE",
            "galaxies_opened_once": CONFIRMATORY,
            "eligibility_failures": failures,
            "individual_scores_released": False,
            "aggregate_score_computed": False,
            "replacement_or_repair_allowed": False,
            "claim_boundary": "predeclared endpoint gate failure; not evidence for or against a body-orthogonal mode or physical channel",
        }
        OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        REPORT.write_text(
            "# PHANGS radial body-projection confirmatory endpoint v01\n\n"
            f"Status: `{result['status']}`\n\nAt least one frozen eligibility gate failed. No individual or aggregate "
            "score is released, and no galaxy replacement or post-open repair is allowed.\n",
            encoding="utf-8",
        )
        print(result["status"], failures)
        return

    primary_rows = [opened[galaxy]["metrics"]["primary"] for galaxy in CONFIRMATORY]
    reverse_rows = [opened[galaxy]["metrics"]["radial_reversal"] for galaxy in CONFIRMATORY]
    phase_rows = [opened[galaxy]["metrics"]["phase_rotation_pi_over_2"] for galaxy in CONFIRMATORY]
    primary_aggregate = aggregate(primary_rows)
    reverse_aggregate = aggregate(reverse_rows)
    phase_aggregate = aggregate(phase_rows)
    reverse_individual = sum(
        opened[g]["metrics"]["primary"]["q"] < opened[g]["metrics"]["radial_reversal"]["q"]
        for g in CONFIRMATORY
    )
    phase_individual = sum(
        opened[g]["metrics"]["primary"]["q"] < opened[g]["metrics"]["phase_rotation_pi_over_2"]["q"]
        for g in CONFIRMATORY
    )
    controls = {
        "radial_reversal": {
            "aggregate_q": reverse_aggregate["q"],
            "correct_q_strictly_lower_global": primary_aggregate["q"] < reverse_aggregate["q"],
            "correct_q_lower_individual_count": int(reverse_individual),
            "passes": bool(primary_aggregate["q"] < reverse_aggregate["q"] and reverse_individual >= 3),
        },
        "phase_rotation_pi_over_2": {
            "aggregate_q": phase_aggregate["q"],
            "correct_q_strictly_lower_global": primary_aggregate["q"] < phase_aggregate["q"],
            "correct_q_lower_individual_count": int(phase_individual),
            "passes": bool(primary_aggregate["q"] < phase_aggregate["q"] and phase_individual >= 3),
        },
    }
    detection = bool(
        primary_aggregate["primary_and_replication_thresholds_pass"]
        and controls["radial_reversal"]["passes"]
        and controls["phase_rotation_pi_over_2"]["passes"]
    )
    galaxy_results = {galaxy: opened[galaxy]["metrics"] for galaxy in CONFIRMATORY}
    result = {
        "schema": "phangs_radial_body_projection_confirmatory_endpoint_v01",
        "status": (
            "BODY_ORTHOGONAL_DIFFERENTIAL_TRACER_STRUCTURE_DETECTED"
            if detection else "NO_PREREGISTERED_BODY_ORTHOGONAL_DETECTION"
        ),
        "galaxies_opened_once": CONFIRMATORY,
        "all_frozen_eligibility_gates_pass": True,
        "galaxies": galaxy_results,
        "aggregate_primary": primary_aggregate,
        "geometric_controls": controls,
        "preregistered_detection": detection,
        "grouped_body_increment_identified": False,
        "physical_channel_identified": False,
        "time_component_identified": False,
        "quantum_component_identified": False,
        "dark_sector_identified": False,
        "chi_square_calibration": "approximate under frozen block-sector-jackknife covariance",
        "replacement_or_repair_allowed": False,
        "claim_boundary": (
            "one-shot source-frozen body-orthogonal differential tracer endpoint; even a positive "
            "result does not identify channel, time, quantum, Tau-parent, or dark-sector origin"
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    pd.DataFrame([row for galaxy in CONFIRMATORY for row in opened[galaxy]["rows"]]).to_csv(
        COEFFICIENTS, index=False
    )
    np.savez_compressed(MATRICES, **{galaxy: opened[galaxy]["matrix"] for galaxy in CONFIRMATORY})
    REPORT.write_text(
        "# PHANGS radial body-projection confirmatory endpoint v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The frozen four-body score gives `Q={primary_aggregate['q']:.3f}` for "
        f"`{primary_aggregate['dof']}` approximate chi-square degrees of freedom "
        f"(`p={primary_aggregate['p_chi_square_approximation']:.4g}`), with "
        f"`{primary_aggregate['individual_p_below_0_05']}/4` individual detections. "
        f"Radial-reversal control pass: `{controls['radial_reversal']['passes']}`; "
        f"phase-rotation control pass: `{controls['phase_rotation_pi_over_2']['passes']}`.\n\n"
        "This endpoint tests differential tracer structure outside the declared source-body span. "
        "It does not identify a physical channel or a time, quantum, Tau-parent, or dark-sector origin.\n",
        encoding="utf-8",
    )
    print(result["status"], primary_aggregate)


if __name__ == "__main__":
    main()
