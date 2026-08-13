#!/usr/bin/env python3
"""Test 2D CO/H-alpha tracer innovation in a frozen harmonic field basis."""

from __future__ import annotations

import json
import math
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.stats import chi2


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
GALAXIES = {
    "NGC3351": {
        "slug": "ngc3351", "center": (160.9906, 11.7037), "pa": 193.0, "inclination": 41.0,
        "muse_psf": 1.05, "muse": "NGC3351_MAPS_copt_1.05asec.fits",
        "co": "group.uid___A001_X2fb_X27c.lp_schinner.ngc3351_12m7mtp_co21_mom1wprior.fits",
        "eco": "group.uid___A001_X2fb_X27c.lp_schinner.ngc3351_12m7mtp_co21_emom1wprior.fits",
        "morphology_control": "strongly_barred",
    },
    "NGC4254": {
        "slug": "ngc4254", "center": (184.7067, 14.4168), "pa": 68.1, "inclination": 34.4,
        "muse_psf": 0.89, "muse": "NGC4254_MAPS_copt_0.89asec.fits",
        "co": "group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_mom1wprior.fits",
        "eco": "group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_emom1wprior.fits",
        "morphology_control": "unbarred_lopsided_environmentally_disturbed",
    },
    "NGC3627": {
        "slug": "ngc3627", "center": (170.0625, 12.9916), "pa": 173.1, "inclination": 57.3,
        "muse_psf": 1.05, "muse": "NGC3627_MAPS_copt_1.05asec.fits",
        "co": "group.uid___A001_X2fb_X286.lp_schinner.ngc3627_12m7mtp_co21_mom1wprior.fits",
        "eco": "group.uid___A001_X2fb_X286.lp_schinner.ngc3627_12m7mtp_co21_emom1wprior.fits",
        "morphology_control": "barred_interacting_disturbed",
        "replication_role": "source-frozen morphology-complex stress control",
    },
    "NGC4535": {
        "slug": "ngc4535", "center": (188.5846, 8.197973), "pa": 179.7, "inclination": 44.7,
        "muse_psf": 0.56, "muse": "NGC4535_MAPS_copt_0.56asec.fits",
        "co": "group.uid___A001_X2fb_X2cc.lp_schinner.ngc4535_12m7mtp_co21_mom1wprior.fits",
        "eco": "group.uid___A001_X2fb_X2cc.lp_schinner.ngc4535_12m7mtp_co21_emom1wprior.fits",
        "morphology_control": "barred_spiral_no_prefrozen_m1_nuisance",
        "replication_role": "source-frozen barred-galaxy morphology-orthogonal replication",
    },
    "IC5332": {
        "slug": "ic5332", "center": (353.6145, -36.1011), "pa": 74.4, "inclination": 26.9,
        "muse_psf": 0.87, "muse": "IC5332_MAPS_copt_0.87asec.fits",
        "co": "group.uid___A001_X2fe_X2bb.lp_schinner.ic5332_12m7mtp_co21_mom1wprior.fits",
        "eco": "group.uid___A001_X2fe_X2bb.lp_schinner.ic5332_12m7mtp_co21_emom1wprior.fits",
        "morphology_control": "nonbarred_population_m2_test",
        "replication_role": "preregistered confirmatory population endpoint",
    },
    "NGC4321": {
        "slug": "ngc4321", "center": (185.7289, 15.8223), "pa": 156.2, "inclination": 38.5,
        "muse_psf": 1.16, "muse": "NGC4321_MAPS_copt_1.16asec.fits",
        "co": "group.uid___A001_X2fb_X2b8.lp_schinner.ngc4321_12m7mtp_co21_mom1wprior.fits",
        "eco": "group.uid___A001_X2fb_X2b8.lp_schinner.ngc4321_12m7mtp_co21_emom1wprior.fits",
        "morphology_control": "nonbarred_population_m2_test",
        "replication_role": "preregistered confirmatory population endpoint",
    },
}
N_RADIAL_ZONES = 5
MAX_VELOCITY_ERROR = 10.0
MIN_FLUX_SNR = 5.0
ERROR_FLOORS_KM_S = (0.0, 1.0, 3.0, 5.0, 10.0)
N_AZIMUTH_JACKKNIFE_SECTORS = 12


def fit_modes(design: np.ndarray, values: np.ndarray, variance: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if (
        not np.all(np.isfinite(design))
        or not np.all(np.isfinite(values))
        or not np.all(np.isfinite(variance))
        or np.any(variance <= 0)
    ):
        raise ValueError("Mode fit received non-finite data or non-positive variance")
    weight = 1.0 / variance
    # Accelerate-backed NumPy can retain benign FP flags across finite matmuls.
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        normal = design.T @ (weight[:, None] * design)
        right_hand_side = design.T @ (weight * values)
    if not np.all(np.isfinite(normal)) or not np.all(np.isfinite(right_hand_side)):
        raise FloatingPointError("Mode normal equation is non-finite")
    covariance = np.linalg.pinv(normal)
    coefficient = covariance @ right_hand_side
    if not np.all(np.isfinite(coefficient)) or not np.all(np.isfinite(covariance)):
        raise FloatingPointError("Mode solution is non-finite")
    return coefficient, covariance


def sector_jackknife_covariance(
    design: np.ndarray, values: np.ndarray, variance: np.ndarray, angle: np.ndarray
) -> tuple[np.ndarray, int]:
    sector = np.floor(((angle + np.pi) % (2 * np.pi)) / (2 * np.pi) * N_AZIMUTH_JACKKNIFE_SECTORS).astype(int)
    estimates = []
    for omitted in np.unique(sector):
        keep = sector != omitted
        if keep.sum() > design.shape[1]:
            estimates.append(fit_modes(design[keep], values[keep], variance[keep])[0])
    estimates = np.asarray(estimates)
    mean = estimates.mean(axis=0)
    covariance = (len(estimates) - 1) / len(estimates) * (estimates - mean).T @ (estimates - mean)
    return covariance, len(estimates)


def sample_to_wcs(data: np.ndarray, source_wcs: WCS, target_wcs: WCS, shape: tuple[int, int]) -> np.ndarray:
    yy, xx = np.indices(shape, dtype=float)
    ra, dec = target_wcs.pixel_to_world_values(xx, yy)
    sx, sy = source_wcs.world_to_pixel_values(ra, dec)
    return map_coordinates(data, [sy, sx], order=1, mode="constant", cval=np.nan)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--galaxy", choices=GALAXIES, default="NGC3351")
    args = parser.parse_args()
    galaxy = args.galaxy
    config = GALAXIES[galaxy]
    slug = config["slug"]
    ext = ROOT / f"data/external/literature/{slug}_phangs_tracer_velocity"
    report = ROOT / f"reports/{slug}_phangs_tracer_velocity_field_rank_test_v01.md"
    source = json.loads((DATA / f"{slug}_phangs_tracer_velocity_fields_v01.json").read_text())
    if source["status"] != "SOURCE_NATIVE_2D_TRACER_VELOCITY_FIELDS_ACQUIRED":
        raise RuntimeError("Tracer source gate is not ready")
    muse_path = ext / config["muse"]
    co_path = ext / config["co"]
    eco_path = ext / config["eco"]
    with fits.open(muse_path, memmap=True) as h:
        flux = np.asarray(h["HA6562_FLUX"].data, float)
        eflux = np.asarray(h["HA6562_FLUX_ERR"].data, float)
        velocity = np.asarray(h["HA6562_VEL"].data, float)
        evelocity = np.asarray(h["HA6562_VEL_ERR"].data, float)
        muse_wcs = WCS(h["HA6562_VEL"].header, naxis=2)
        pixel_arcsec = abs(float(h["HA6562_VEL"].header["CD1_1"])) * 3600
    with fits.open(co_path, memmap=True) as h:
        co_velocity = np.squeeze(np.asarray(h[0].data, float))
        co_header = h[0].header.copy()
        co_wcs = WCS(co_header, naxis=2)
        co_beam = math.sqrt(float(co_header["BMAJ"]) * float(co_header["BMIN"])) * 3600
    with fits.open(eco_path, memmap=True) as h:
        co_error = np.squeeze(np.asarray(h[0].data, float))

    extra_fwhm = math.sqrt(max(co_beam**2 - config["muse_psf"]**2, 0.0))
    sigma_pixels = extra_fwhm / 2.354820045 / pixel_arcsec
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

    yy, xx = np.indices(co_velocity.shape, dtype=float)
    ra, dec = co_wcs.pixel_to_world_values(xx, yy)
    center_ra, center_dec = config["center"]
    east = (ra - center_ra) * math.cos(math.radians(center_dec)) * 3600
    north = (dec - center_dec) * 3600
    pa = math.radians(config["pa"])
    major = east * math.sin(pa) + north * math.cos(pa)
    minor = -east * math.cos(pa) + north * math.sin(pa)
    disk_y = minor / math.cos(math.radians(config["inclination"]))
    radius = np.hypot(major, disk_y)
    theta = np.arctan2(disk_y, major)
    snr = ha_flux / ha_eflux
    mask = (
        np.isfinite(co_velocity) & np.isfinite(co_error) & (co_error > 0) & (co_error <= MAX_VELOCITY_ERROR)
        & np.isfinite(ha_velocity) & np.isfinite(ha_error) & (ha_error > 0) & (ha_error <= MAX_VELOCITY_ERROR)
        & np.isfinite(snr) & (snr >= MIN_FLUX_SNR) & (np.abs(ha_velocity) < 450)
    )
    beam_pixels = max(1, int(math.ceil(co_beam / (abs(float(co_header["CDELT1"])) * 3600))))
    independent = mask & ((xx.astype(int) % beam_pixels) == 0) & ((yy.astype(int) % beam_pixels) == 0)
    if independent.sum() < 50:
        raise RuntimeError("Insufficient beam-independent common tracer pixels")

    offset = float(np.median((co_velocity - ha_velocity)[independent]))
    contrast = co_velocity - offset - ha_velocity
    variance = co_error**2 + ha_error**2
    co_weight = np.divide(1.0, co_error**2, out=np.zeros_like(co_error), where=mask)
    ha_weight = np.divide(1.0, ha_error**2, out=np.zeros_like(ha_error), where=mask)
    total_weight = co_weight + ha_weight
    common_velocity = np.divide(
        co_weight * co_velocity + ha_weight * (ha_velocity + offset),
        total_weight, out=np.full_like(co_velocity, np.nan), where=total_weight > 0,
    )
    common_error = np.divide(
        1.0, np.sqrt(total_weight), out=np.full_like(co_velocity, np.nan), where=total_weight > 0,
    )
    radial_edges = np.quantile(radius[independent], np.linspace(0, 1, N_RADIAL_ZONES + 1))
    rows = []
    floor_rows = []
    zone_blocks = []
    global_chi2 = 0.0
    global_dof = 0
    jackknife_chi2 = 0.0
    jackknife_dof = 0
    for zone in range(N_RADIAL_ZONES):
        select = independent & (radius >= radial_edges[zone]) & (
            radius <= radial_edges[zone + 1] if zone == N_RADIAL_ZONES - 1 else radius < radial_edges[zone + 1]
        )
        angle = theta[select]
        design = np.column_stack([
            np.ones(select.sum()), np.cos(angle), np.sin(angle), np.cos(2 * angle), np.sin(2 * angle)
        ])
        coefficient, covariance = fit_modes(design, contrast[select], variance[select])
        jackknife_covariance, occupied_sectors = sector_jackknife_covariance(
            design, contrast[select], variance[select], angle
        )
        statistic = float(coefficient @ np.linalg.pinv(covariance) @ coefficient)
        global_chi2 += statistic
        global_dof += len(coefficient)
        jackknife_chi2 += float(coefficient @ np.linalg.pinv(jackknife_covariance) @ coefficient)
        jackknife_dof += int(np.linalg.matrix_rank(jackknife_covariance))
        zone_blocks.append({
            "zone": zone,
            "radius_min_arcsec": float(radial_edges[zone]),
            "radius_max_arcsec": float(radial_edges[zone + 1]),
            "mode_order": ["m0", "m1_cos", "m1_sin", "m2_cos", "m2_sin"],
            "coefficient_km_s": coefficient.tolist(),
            "sector_jackknife_covariance_km2_s2": jackknife_covariance.tolist(),
        })
        for mode, value, error, jk_error in zip(
            ("m0", "m1_cos", "m1_sin", "m2_cos", "m2_sin"), coefficient,
            np.sqrt(np.diag(covariance)), np.sqrt(np.diag(jackknife_covariance))
        ):
            rows.append({
                "zone": zone, "radius_min_arcsec": radial_edges[zone], "radius_max_arcsec": radial_edges[zone + 1],
                "n_independent_pixels": int(select.sum()), "mode": mode,
                "co_minus_halpha_km_s": float(value), "sigma_km_s": float(error),
                "z": float(value / error),
                "sector_jackknife_sigma_km_s": float(jk_error),
                "sector_jackknife_z": float(value / jk_error) if jk_error > 0 else None,
                "occupied_jackknife_sectors": occupied_sectors,
            })
        for floor in ERROR_FLOORS_KM_S:
            floor_coefficient, floor_covariance = fit_modes(
                design, contrast[select], variance[select] + floor**2
            )
            floor_rows.append({
                "zone": zone, "error_floor_km_s": floor,
                "chi2": float(floor_coefficient @ np.linalg.pinv(floor_covariance) @ floor_coefficient),
                "dof": len(floor_coefficient),
                "max_absolute_z": float(np.max(np.abs(floor_coefficient / np.sqrt(np.diag(floor_covariance))))),
            })
    mode_frame = pd.DataFrame(rows)
    floor_frame = pd.DataFrame(floor_rows)
    floor_summary = []
    for floor, group in floor_frame.groupby("error_floor_km_s"):
        statistic = float(group.chi2.sum())
        dof = int(group.dof.sum())
        floor_summary.append({
            "error_floor_km_s": float(floor), "global_chi2": statistic, "dof": dof,
            "p": float(chi2.sf(statistic, dof)), "max_absolute_mode_z": float(group.max_absolute_z.max()),
        })
    result = {
        "schema": f"{slug}_phangs_tracer_velocity_field_rank_test_v01",
        "status": "TWO_DIMENSIONAL_TRACER_INNOVATION_DIAGNOSTIC",
        "galaxy": galaxy,
        "morphology_control": config["morphology_control"],
        "replication_role": config.get("replication_role", "legacy source-frozen pilot"),
        "tracers": ["CO(2-1)", "H-alpha"],
        "common_quality_pixels": int(mask.sum()),
        "beam_independent_pixels": int(independent.sum()),
        "co_beam_arcsec": co_beam,
        "muse_input_psf_arcsec": config["muse_psf"],
        "velocity_zero_point_offset_km_s": offset,
        "common_velocity_field_fits": f"data/derived/{slug}_phangs_common_tracer_velocity_field_v01.fits",
        "harmonic_basis": "five radial zones times {m0,m1_cos,m1_sin,m2_cos,m2_sin}",
        "global_zero_innovation_chi2": global_chi2,
        "global_zero_innovation_dof": global_dof,
        "global_zero_innovation_p": float(chi2.sf(global_chi2, global_dof)),
        "max_absolute_mode_z": float(mode_frame.z.abs().max()),
        "formal_abs_z_ge_3_mode_count": int((mode_frame.z.abs() >= 3.0).sum()),
        "sector_jackknife_global_chi2_diagnostic": jackknife_chi2,
        "sector_jackknife_global_rank": jackknife_dof,
        "sector_jackknife_global_p_diagnostic": float(chi2.sf(jackknife_chi2, jackknife_dof)),
        "sector_jackknife_max_absolute_mode_z": float(mode_frame.sector_jackknife_z.abs().max()),
        "zone_mode_blocks": zone_blocks,
        "error_floor_sensitivity": floor_summary,
        "distinct_tracer_field_mode_candidate": bool(float(chi2.sf(global_chi2, global_dof)) < 0.01),
        "construction_uses_rotation_residual": False,
        "time_channel_identified": False,
        "quantum_channel_identified": False,
        "limitations": [
            "formal chi-square still uses diagonal per-pixel errors after beam-independent subsampling",
            "sector jackknife is a robustness diagnostic and does not estimate a complete spatial covariance matrix",
            "MUSE velocity-extension BUNIT metadata is incorrect in DR1 although values are documented as km/s",
            "global geometry is frozen from published H-alpha kinematics rather than refit",
            "gas phase, bar streaming, line formation and pressure support remain physical alternatives",
            "NGC3627 has source-known m1-like disturbance and m2-like bar structure, leaving no low-order morphology-orthogonal angular mode in this frozen basis" if galaxy == "NGC3627" else "the retained angular-family interpretation is supplied by the separate morphology-removal audit",
        ],
        "claim_boundary": "per-galaxy 2D CO/H-alpha field innovation diagnostic; a nonzero harmonic contrast is tracer-field structure, not observer-time, path, quantum, Tau Core, or dark-sector detection",
    }
    mode_frame.to_csv(DATA / f"{slug}_phangs_tracer_velocity_field_modes_v01.csv", index=False)
    floor_frame.to_csv(DATA / f"{slug}_phangs_tracer_velocity_field_error_floor_sensitivity_v01.csv", index=False)
    (DATA / f"{slug}_phangs_tracer_velocity_field_rank_test_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    common_header = co_header.copy()
    common_header["BUNIT"] = "km/s"
    common_header["TCROLE"] = "inverse-variance common CO/Halpha velocity"
    error_header = co_header.copy()
    error_header["BUNIT"] = "km/s"
    fits.HDUList([
        fits.PrimaryHDU(),
        fits.ImageHDU(common_velocity.astype(np.float32), header=common_header, name="COMMON_VEL"),
        fits.ImageHDU(common_error.astype(np.float32), header=error_header, name="COMMON_ERR"),
        fits.ImageHDU(mask.astype(np.uint8), header=co_header, name="COMMON_MASK"),
    ]).writeto(DATA / f"{slug}_phangs_common_tracer_velocity_field_v01.fits", overwrite=True)
    report.write_text(
        f"# {galaxy} PHANGS 2D tracer velocity-field rank test\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The common quality mask has `{result['common_quality_pixels']}` pixels and "
        f"`{result['beam_independent_pixels']}` beam-independent samples. The frozen 25-mode "
        f"innovation test gives `chi2={global_chi2:.2f}` for `{global_dof}` dof "
        f"(`p={result['global_zero_innovation_p']:.4g}`); maximum absolute single-mode "
        f"significance is `{result['max_absolute_mode_z']:.2f}`. A 12-sector spatial jackknife reduces "
        f"the maximum absolute mode significance to `{result['sector_jackknife_max_absolute_mode_z']:.2f}` "
        f"and gives a combined diagnostic `p={result['sector_jackknife_global_p_diagnostic']:.4g}`; "
        f"this is the preferred robustness diagnostic, while the formal chi-square is retained for "
        f"reproducibility. With a conservative `10 km/s` error floor the largest formal mode significance "
        f"is `{floor_summary[-1]['max_absolute_mode_z']:.2f}`.\n\n"
        "The test uses source-native CO and H-alpha velocity fields and no rotation residual. "
        "Any surviving contrast remains compatible with ordinary tracer and non-circular gas "
        "physics and does not identify time, path, quantum, or Tau origin.\n",
        encoding="utf-8",
    )
    print(result["status"], json.dumps({k: result[k] for k in ["beam_independent_pixels", "global_zero_innovation_p", "max_absolute_mode_z"]}))


if __name__ == "__main__":
    main()
