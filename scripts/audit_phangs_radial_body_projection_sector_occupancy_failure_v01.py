#!/usr/bin/env python3
"""Diagnose the frozen sector-occupancy failure without rescoring."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales
from scipy.ndimage import gaussian_filter

from acquire_phangs_radial_body_projection_confirmatory_packet_v01 import CONFIG, CONFIRMATORY
from build_phangs_population_channel_preregistration_v01 import GEOMETRY
from build_phangs_radial_body_projection_development_preflight_v01 import disk_coordinates
from run_phangs_radial_body_projection_confirmatory_endpoint_v01 import (
    EXTERNAL,
    MAX_VELOCITY_ERROR,
    MIN_FLUX_SNR,
    N_SECTORS,
    SAMPLE,
    sample_to_wcs,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
ENDPOINT = DATA / "phangs_radial_body_projection_confirmatory_endpoint_v01.json"
OUTPUT = DATA / "phangs_radial_body_projection_sector_occupancy_failure_v01.json"
REPORT = ROOT / "reports/phangs_radial_body_projection_sector_occupancy_failure_v01.md"


def occupancy(galaxy: str, center: tuple[float, float]) -> dict[str, object]:
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
        header = hdul[0].header.copy()
        co_wcs = WCS(header, naxis=2)
    with fits.open(eco_path, memmap=True) as hdul:
        co_error = np.squeeze(np.asarray(hdul[0].data, dtype=float))

    co_beam = math.sqrt(float(header["BMAJ"]) * float(header["BMIN"])) * 3600.0
    muse_pixel = float(np.mean(np.abs(proj_plane_pixel_scales(muse_wcs))) * 3600.0)
    sigma = math.sqrt(max(co_beam**2 - float(CONFIG[galaxy]["muse_psf_arcsec"])**2, 0.0)) / 2.354820045 / muse_pixel
    valid_flux = np.isfinite(flux) & np.isfinite(velocity) & (flux > 0)
    numerator = gaussian_filter(np.where(valid_flux, flux * velocity, 0.0), sigma)
    denominator = gaussian_filter(np.where(valid_flux, flux, 0.0), sigma)
    smoothed = np.divide(numerator, denominator, out=np.full_like(numerator, np.nan), where=denominator > 0)
    ha_velocity = sample_to_wcs(smoothed, muse_wcs, co_wcs, co_velocity.shape)
    ha_error = sample_to_wcs(evelocity, muse_wcs, co_wcs, co_velocity.shape)
    ha_flux = sample_to_wcs(flux, muse_wcs, co_wcs, co_velocity.shape)
    ha_eflux = sample_to_wcs(eflux, muse_wcs, co_wcs, co_velocity.shape)
    radius, theta = disk_coordinates(co_wcs, co_velocity.shape, center, *GEOMETRY[galaxy])
    snr = ha_flux / ha_eflux
    mask = (
        np.isfinite(co_velocity) & np.isfinite(co_error) & (co_error > 0)
        & (co_error <= MAX_VELOCITY_ERROR) & np.isfinite(ha_velocity)
        & np.isfinite(ha_error) & (ha_error > 0) & (ha_error <= MAX_VELOCITY_ERROR)
        & np.isfinite(snr) & (snr >= MIN_FLUX_SNR) & (np.abs(ha_velocity) < 450.0)
    )
    co_pixel = float(np.mean(np.abs(proj_plane_pixel_scales(co_wcs))) * 3600.0)
    stride = max(1, int(math.ceil(co_beam / co_pixel)))
    yy, xx = np.indices(co_velocity.shape)
    independent = mask & ((xx % stride) == 0) & ((yy % stride) == 0)
    edges = np.quantile(radius[independent], np.linspace(0.0, 1.0, 6))
    zones = []
    for zone in range(5):
        select = independent & (radius >= edges[zone]) & (
            radius <= edges[zone + 1] if zone == 4 else radius < edges[zone + 1]
        )
        sector = np.floor(((theta[select] + np.pi) % (2 * np.pi)) / (2 * np.pi) * N_SECTORS).astype(int)
        counts = np.bincount(sector, minlength=N_SECTORS)
        zones.append({
            "zone": zone,
            "independent_pixels": int(select.sum()),
            "occupied_sector_count": int(np.sum(counts > 0)),
            "missing_sectors": np.flatnonzero(counts == 0).tolist(),
            "sector_counts": counts.tolist(),
        })
    return {
        "beam_independent_pixels": int(independent.sum()),
        "beam_stride_pixels": stride,
        "zones": zones,
        "all_12_sectors_in_every_zone": all(zone["occupied_sector_count"] == 12 for zone in zones),
    }


def main() -> None:
    endpoint = json.loads(ENDPOINT.read_text(encoding="utf-8"))
    if endpoint["status"] != "CONFIRMATORY_ENDPOINT_OPENED_NONIDENTIFIABLE_GATE_FAILURE":
        raise RuntimeError("This diagnostic is authorized only after the frozen endpoint gate failure")
    import pandas as pd

    sample = pd.read_csv(SAMPLE, skiprows=[1]).set_index("Name")
    galaxies = {}
    for galaxy in CONFIRMATORY:
        center = (float(sample.loc[galaxy, "R.A."]), float(sample.loc[galaxy, "Dec."]))
        galaxies[galaxy] = occupancy(galaxy, center)
    result = {
        "schema": "phangs_radial_body_projection_sector_occupancy_failure_v01",
        "status": "FROZEN_12_SECTOR_GATE_FAILS_FINITE_FOOTPRINT_DIAGNOSTIC_ONLY",
        "galaxies": galaxies,
        "same_endpoint_rescoring_allowed": False,
        "post_open_gate_relaxation_allowed": False,
        "future_protocol_candidate": (
            "predeclare a footprint-adaptive spatial block jackknife on a new untouched cohort, "
            "with block count and covariance-rank gates frozen before acquisition"
        ),
        "claim_boundary": (
            "post-open support-geometry diagnosis only; not a repaired endpoint, score, body-orthogonal "
            "signal, channel, time, quantum, Tau, or dark-sector result"
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# PHANGS radial body-projection sector-occupancy failure v01", "",
        f"Status: `{result['status']}`", "",
    ]
    for galaxy, audit in galaxies.items():
        occupied = [zone["occupied_sector_count"] for zone in audit["zones"]]
        lines.append(f"- `{galaxy}`: occupied sectors by radial zone `{occupied}`.")
    lines.extend([
        "", "The fixed twelve-sector rule is incompatible with the finite common-support footprints. "
        "This is a diagnostic of the preserved non-identifiability result, not authorization to "
        "relax and rescore the opened cohort.",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(result["status"])
    for galaxy, audit in galaxies.items():
        print(galaxy, [zone["occupied_sector_count"] for zone in audit["zones"]])


if __name__ == "__main__":
    main()
