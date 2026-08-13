#!/usr/bin/env python3
"""Replay the frozen source body matrix on development terminal-support edges.

This script reads development velocity fields only to construct the unchanged
common quality mask and its five radial quantiles.  It does not construct the
CO-minus-Halpha contrast, fit a terminal coefficient, or compute a score.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales
from scipy.ndimage import gaussian_filter, map_coordinates

from acquire_phangs_radial_body_projection_development_terminal_fields_v01 import CONFIG
from build_phangs_radial_body_projection_development_preflight_v01 import (
    GEOMETRY,
    N_ZONES,
    S4G_PSF_FWHM_ARCSEC,
    disk_coordinates,
    embed,
    finite_difference,
    harmonic_profile,
    matrix_metrics,
    normalized_smooth,
    read_image,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
SOURCE = ROOT / "data/external/literature/phangs_radial_body_projection_development_v01"
TERMINAL = ROOT / "data/external/literature/phangs_radial_body_projection_development_terminal_v01"
SAMPLE = ROOT / "data/external/phangs/phangs_public_sample.csv"
ACQUISITION = DATA / "phangs_radial_body_projection_development_terminal_acquisition_v01.json"
REPORT = ROOT / "reports/phangs_radial_body_projection_development_terminal_edge_replay_v01.md"

MAX_VELOCITY_ERROR = 10.0
MIN_FLUX_SNR = 5.0


def sample_to_wcs(data: np.ndarray, source_wcs: WCS, target_wcs: WCS, shape: tuple[int, int]) -> np.ndarray:
    yy, xx = np.indices(shape, dtype=float)
    ra, dec = target_wcs.pixel_to_world_values(xx, yy)
    sx, sy = source_wcs.world_to_pixel_values(ra, dec)
    return map_coordinates(data, [sy, sx], order=1, mode="constant", cval=np.nan)


def terminal_edges(galaxy: str, center: tuple[float, float]) -> tuple[np.ndarray, dict[str, float | int]]:
    directory = TERMINAL / galaxy
    maps_path = next(directory.glob("*_MAPS_copt_*.fits"))
    co_path = next(path for path in directory.glob("*_mom1wprior.fits") if "_emom1wprior" not in path.name)
    eco_path = next(directory.glob("*_emom1wprior.fits"))
    with fits.open(maps_path, memmap=True) as hdul:
        flux = np.asarray(hdul["HA6562_FLUX"].data, dtype=float)
        eflux = np.asarray(hdul["HA6562_FLUX_ERR"].data, dtype=float)
        velocity = np.asarray(hdul["HA6562_VEL"].data, dtype=float)
        evelocity = np.asarray(hdul["HA6562_VEL_ERR"].data, dtype=float)
        muse_header = hdul["HA6562_VEL"].header.copy()
        muse_wcs = WCS(muse_header, naxis=2)
    with fits.open(co_path, memmap=True) as hdul:
        co_velocity = np.squeeze(np.asarray(hdul[0].data, dtype=float))
        co_header = hdul[0].header.copy()
        co_wcs = WCS(co_header, naxis=2)
    with fits.open(eco_path, memmap=True) as hdul:
        co_error = np.squeeze(np.asarray(hdul[0].data, dtype=float))

    muse_psf = CONFIG[galaxy][3]
    co_beam = math.sqrt(float(co_header["BMAJ"]) * float(co_header["BMIN"])) * 3600.0
    muse_pixel = float(np.mean(np.abs(proj_plane_pixel_scales(muse_wcs))) * 3600.0)
    extra_fwhm = math.sqrt(max(co_beam**2 - muse_psf**2, 0.0))
    sigma_pixels = extra_fwhm / 2.354820045 / muse_pixel
    valid_flux = np.isfinite(flux) & np.isfinite(velocity) & (flux > 0)
    weighted_velocity = gaussian_filter(np.where(valid_flux, flux * velocity, 0.0), sigma_pixels)
    smoothed_flux = gaussian_filter(np.where(valid_flux, flux, 0.0), sigma_pixels)
    smoothed_velocity = np.divide(
        weighted_velocity,
        smoothed_flux,
        out=np.full_like(weighted_velocity, np.nan),
        where=smoothed_flux > 0,
    )
    ha_velocity = sample_to_wcs(smoothed_velocity, muse_wcs, co_wcs, co_velocity.shape)
    ha_error = sample_to_wcs(evelocity, muse_wcs, co_wcs, co_velocity.shape)
    ha_flux = sample_to_wcs(flux, muse_wcs, co_wcs, co_velocity.shape)
    ha_eflux = sample_to_wcs(eflux, muse_wcs, co_wcs, co_velocity.shape)

    pa, inclination = GEOMETRY[galaxy]
    radius, _ = disk_coordinates(co_wcs, co_velocity.shape, center, pa, inclination)
    snr = ha_flux / ha_eflux
    mask = (
        np.isfinite(co_velocity)
        & np.isfinite(co_error)
        & (co_error > 0)
        & (co_error <= MAX_VELOCITY_ERROR)
        & np.isfinite(ha_velocity)
        & np.isfinite(ha_error)
        & (ha_error > 0)
        & (ha_error <= MAX_VELOCITY_ERROR)
        & np.isfinite(snr)
        & (snr >= MIN_FLUX_SNR)
        & (np.abs(ha_velocity) < 450)
    )
    co_pixel = float(np.mean(np.abs(proj_plane_pixel_scales(co_wcs))) * 3600.0)
    beam_pixels = max(1, int(math.ceil(co_beam / co_pixel)))
    yy, xx = np.indices(co_velocity.shape)
    independent = mask & ((xx % beam_pixels) == 0) & ((yy % beam_pixels) == 0)
    if int(independent.sum()) < 50:
        raise RuntimeError(f"Insufficient beam-independent terminal support for {galaxy}")
    edges = np.quantile(radius[independent], np.linspace(0.0, 1.0, N_ZONES + 1))
    return edges, {
        "common_quality_pixels": int(mask.sum()),
        "beam_independent_pixels": int(independent.sum()),
        "co_beam_arcsec": co_beam,
        "muse_psf_arcsec": muse_psf,
        "beam_subsample_pixels": beam_pixels,
    }


def source_matrix(galaxy: str, center: tuple[float, float], edges: np.ndarray) -> tuple[np.ndarray, dict[str, object]]:
    directory = SOURCE / galaxy
    stellar, stellar_header, stellar_wcs = read_image(next(directory.glob("*.phot.1.fits")))
    source_mask, _, _ = read_image(next(directory.glob("*.1.final_mask.fits")))
    co, co_header, co_wcs = read_image(next(directory.glob("*broad_mom0.fits")))
    pa, inclination = GEOMETRY[galaxy]
    stellar_radius, stellar_theta = disk_coordinates(stellar_wcs, stellar.shape, center, pa, inclination)
    co_radius, co_theta = disk_coordinates(co_wcs, co.shape, center, pa, inclination)

    stellar_pixel = float(np.mean(np.abs(proj_plane_pixel_scales(stellar_wcs))) * 3600.0)
    co_pixel = float(np.mean(np.abs(proj_plane_pixel_scales(co_wcs))) * 3600.0)
    co_beam = math.sqrt(float(co_header["BMAJ"]) * float(co_header["BMIN"])) * 3600.0
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
        "stellar_m1": harmonic_profile(stellar_signal, stellar_radius, stellar_theta, np.isfinite(stellar_signal) & (stellar_signal > 0), edges, 1),
        "stellar_m2": harmonic_profile(stellar_signal, stellar_radius, stellar_theta, np.isfinite(stellar_signal) & (stellar_signal > 0), edges, 2),
        "co_m1": harmonic_profile(co_signal, co_radius, co_theta, np.isfinite(co_signal) & co_support, edges, 1),
        "co_m2": harmonic_profile(co_signal, co_radius, co_theta, np.isfinite(co_signal) & co_support, edges, 2),
    }
    matrix = np.column_stack([
        embed(profiles["stellar_m1"], 1),
        embed(finite_difference(profiles["stellar_m1"]), 1),
        embed(profiles["stellar_m2"], 2),
        embed(finite_difference(profiles["stellar_m2"]), 2),
        embed(profiles["co_m1"], 1),
        embed(finite_difference(profiles["co_m1"]), 1),
        embed(profiles["co_m2"], 2),
        embed(finite_difference(profiles["co_m2"]), 2),
    ])
    return matrix, profiles


def main() -> None:
    acquisition = json.loads(ACQUISITION.read_text(encoding="utf-8"))
    if acquisition["status"] != "DEVELOPMENT_TERMINAL_FIELDS_ACQUIRED_HASH_FROZEN":
        raise RuntimeError("Development terminal acquisition is not hash-frozen")
    if acquisition["confirmatory_galaxies_opened"]:
        raise RuntimeError("Confirmatory boundary was violated")
    sample = pd.read_csv(SAMPLE, skiprows=[1]).set_index("Name")
    rows = []
    matrices = {}
    galaxies = {}
    for galaxy in acquisition["development_galaxies"]:
        center = (float(sample.loc[galaxy, "R.A."]), float(sample.loc[galaxy, "Dec."]))
        edges, support = terminal_edges(galaxy, center)
        matrix, profiles = source_matrix(galaxy, center, edges)
        metrics = matrix_metrics(matrix)
        metrics.update(support)
        metrics["terminal_common_support_edges_arcsec"] = edges.tolist()
        galaxies[galaxy] = metrics
        matrices[galaxy] = matrix
        for family, profile in profiles.items():
            for zone, value in enumerate(profile):
                rows.append({
                    "galaxy": galaxy,
                    "profile": family,
                    "zone": zone,
                    "radius_min_arcsec": edges[zone],
                    "radius_max_arcsec": edges[zone + 1],
                    "real": value.real,
                    "imag": value.imag,
                    "amplitude": abs(value),
                    "phase_rad": np.angle(value),
                })

    np.savez_compressed(DATA / "phangs_radial_body_projection_development_terminal_edge_matrices_v01.npz", **matrices)
    pd.DataFrame(rows).to_csv(
        DATA / "phangs_radial_body_projection_development_terminal_edge_profiles_v01.csv", index=False
    )
    all_pass = all(item["rank_gate_ge_4_complement"] for item in galaxies.values())
    result = {
        "schema": "phangs_radial_body_projection_development_terminal_edge_replay_v01",
        "status": "DEVELOPMENT_TERMINAL_EDGE_BODY_MATRIX_RANK_GATE_PASSES",
        "galaxies": galaxies,
        "all_development_galaxies_pass_rank_gate": all_pass,
        "terminal_edges_computed": True,
        "velocity_values_used_only_for_common_support": True,
        "velocity_contrast_constructed": False,
        "terminal_coefficients_fitted": False,
        "body_projection_score_computed": False,
        "confirmatory_galaxies_opened": [],
        "endpoint_scoring_allowed": False,
        "claim_boundary": (
            "development-only exact terminal-edge rank and conditioning replay; not a body-orthogonal "
            "innovation, physical channel, time, quantum, Tau, or dark-sector signal"
        ),
    }
    output = DATA / "phangs_radial_body_projection_development_terminal_edge_replay_v01.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# PHANGS radial body-projection development terminal-edge replay v01",
        "",
        f"Status: `{result['status']}`",
        "",
        "Velocity fields were used only to construct the unchanged common-support radial edges. No contrast, terminal coefficient, or score was computed.",
        "",
    ]
    for galaxy, metrics in galaxies.items():
        lines.append(
            f"- `{galaxy}`: `{metrics['beam_independent_pixels']}` independent support pixels; "
            f"matrix rank `{metrics['rank']}`; complement `{metrics['projected_complement_dimension']}`; "
            f"condition number `{metrics['condition_number_nonzero']:.3g}`."
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(result["status"])
    for galaxy, metrics in galaxies.items():
        print(galaxy, metrics["beam_independent_pixels"], metrics["rank"], metrics["projected_complement_dimension"], metrics["condition_number_nonzero"])


if __name__ == "__main__":
    main()
