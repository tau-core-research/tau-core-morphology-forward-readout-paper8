#!/usr/bin/env python3
"""Build a deprojected NGC4579 H I profile and disk-gravity field from VIVA."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
SOURCE = ROOT / "data" / "external" / "literature" / "ngc4579_viva_hi" / "ngc4579.mom0.fits"
REPORT = ROOT / "reports" / "ngc4579_viva_hi_gravity_v01.md"
G = 4.30091e-6
DISTANCE_MPC = 16.5
PA_DEG = 90.3
INCLINATION_DEG = 38.7
BEAM_MAJOR_DEG = 1.1789e-2
BEAM_MINOR_DEG = 9.5861e-3
HELIUM = 1.36
RING_WIDTH_KPC = 1.0
SOFTENING_KPC = [0.1, 0.3, 0.5]


def ring_velocity_squared(radius: np.ndarray, ring_radius: np.ndarray, ring_mass: np.ndarray, softening: float) -> np.ndarray:
    theta = np.linspace(0.0, 2.0 * np.pi, 720, endpoint=False)
    result = np.zeros_like(radius)
    for a, mass in zip(ring_radius, ring_mass):
        if mass <= 0.0:
            continue
        denominator = (
            radius[:, None] ** 2 + a**2 - 2.0 * radius[:, None] * a * np.cos(theta)[None, :] + softening**2
        ) ** 1.5
        radial_kernel = np.mean((radius[:, None] - a * np.cos(theta)[None, :]) / denominator, axis=1)
        result += G * mass * radius * radial_kernel
    return result


def main() -> None:
    with fits.open(SOURCE, memmap=False) as hdul:
        image = hdul[0].data.astype(float)
        header = hdul[0].header
    blank_floor = float(np.min(image[image > 0.0]))
    signal = image > blank_floor * 1.01
    yy, xx = np.indices(image.shape)
    dx_arcsec = (xx + 1.0 - header["CRPIX1"]) * header["CDELT1"] * 3600.0 * np.cos(np.deg2rad(header["CRVAL2"]))
    dy_arcsec = (yy + 1.0 - header["CRPIX2"]) * header["CDELT2"] * 3600.0
    pa = np.deg2rad(PA_DEG)
    major_arcsec = dx_arcsec * np.sin(pa) + dy_arcsec * np.cos(pa)
    minor_arcsec = -dx_arcsec * np.cos(pa) + dy_arcsec * np.sin(pa)
    radius_arcsec = np.sqrt(major_arcsec**2 + (minor_arcsec / np.cos(np.deg2rad(INCLINATION_DEG))) ** 2)
    radius_kpc_pixels = radius_arcsec * DISTANCE_MPC * 1e3 / 206265.0

    pixel_area_deg2 = abs(header["CDELT1"] * header["CDELT2"])
    beam_area_deg2 = np.pi / (4.0 * np.log(2.0)) * BEAM_MAJOR_DEG * BEAM_MINOR_DEG
    pixel_flux = np.where(signal, image * pixel_area_deg2 / beam_area_deg2, 0.0)
    pixel_hi_mass = 2.356e5 * DISTANCE_MPC**2 * pixel_flux
    pixel_gas_mass = HELIUM * pixel_hi_mass
    max_radius = np.ceil(radius_kpc_pixels[signal].max() / RING_WIDTH_KPC) * RING_WIDTH_KPC
    edges = np.arange(0.0, max_radius + RING_WIDTH_KPC, RING_WIDTH_KPC)
    centers = 0.5 * (edges[:-1] + edges[1:])
    rows = []
    cumulative = 0.0
    for lo, hi, center in zip(edges[:-1], edges[1:], centers):
        mask = signal & (radius_kpc_pixels >= lo) & (radius_kpc_pixels < hi)
        mass = float(pixel_gas_mass[mask].sum())
        cumulative += mass
        area = np.pi * (hi**2 - lo**2)
        rows.append({
            "radius_inner_kpc": lo, "radius_outer_kpc": hi, "radius_kpc": center,
            "hi_plus_helium_mass_msun": mass, "cumulative_hi_plus_helium_mass_msun": cumulative,
            "surface_density_msun_kpc2": mass / area, "n_signal_pixels": int(mask.sum())
        })
    profile = pd.DataFrame(rows)
    radius_eval = np.arange(0.1, 15.0001, 0.05)
    gravity = pd.DataFrame({"radius_kpc": radius_eval})
    for softening in SOFTENING_KPC:
        v2 = ring_velocity_squared(
            radius_eval, profile.radius_kpc.to_numpy(float), profile.hi_plus_helium_mass_msun.to_numpy(float), softening
        )
        gravity[f"v2_hi_helium_disk_h{softening:.1f}_km2_s2"] = v2
        gravity[f"signed_v_hi_helium_disk_h{softening:.1f}_km_s"] = np.sign(v2) * np.sqrt(np.abs(v2))
    gravity["uses_halpha_endpoint_or_dark_discrepancy"] = False
    profile.to_csv(DATA / "ngc4579_viva_hi_radial_profile_v01.csv", index=False)
    gravity.to_csv(DATA / "ngc4579_viva_hi_gravity_v01.csv", index=False)
    total_flux = float(pixel_flux.sum())
    result = {
        "schema": "tau_core_ngc4579_viva_hi_gravity_v01",
        "status": "CALIBRATED_HI_DISK_GRAVITY_READY_MOLECULAR_GAS_OPEN",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "image_shape": list(image.shape), "bunit": header["BUNIT"].strip(),
        "pixel_arcsec": abs(header["CDELT1"]) * 3600.0,
        "beam_arcsec": [BEAM_MAJOR_DEG * 3600.0, BEAM_MINOR_DEG * 3600.0],
        "blank_floor_jy_beam_km_s": blank_floor, "signal_pixels": int(signal.sum()),
        "integrated_hi_flux_jy_km_s": total_flux,
        "hi_mass_msun": float(pixel_hi_mass.sum()),
        "hi_plus_helium_mass_msun": float(pixel_gas_mass.sum()),
        "geometry": {"distance_mpc": DISTANCE_MPC, "pa_deg": PA_DEG, "inclination_deg": INCLINATION_DEG},
        "ring_width_kpc": RING_WIDTH_KPC, "vertical_softening_sensitivities_kpc": SOFTENING_KPC,
        "gravity_method": "axisymmetric finite-thickness ring angular integration with signed radial v-squared contribution",
        "inner_outward_ring_force_preserved": True,
        "uses_spherical_enclosed_mass_proxy": False,
        "construction_uses_halpha_endpoint_or_dark_discrepancy": False,
        "hi_gravity_ready": True, "molecular_gas_gravity_ready": False,
        "combined_gas_gravity_ready": False, "scoring_allowed": False,
        "claim_boundary": "calibrated VIVA H I plus helium disk gravity; molecular gas still required"
    }
    (DATA / "ngc4579_viva_hi_gravity_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# NGC4579 VIVA H I gravity v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The checksum-frozen calibrated moment-0 map gives `{total_flux:.3f} Jy km/s`, `M_HI={result['hi_mass_msun']:.3e} M_sun`, and H I+helium mass `{result['hi_plus_helium_mass_msun']:.3e} M_sun`. The map is deprojected with source geometry and binned into 1-kpc rings. Gravity is computed by axisymmetric ring angular integration with `h=0.1,0.3,0.5 kpc`, not by spherical enclosed mass.\n\n"
        "No Halpha endpoint value enters construction. Molecular-gas gravity remains open, so combined baryonic scoring is forbidden.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
