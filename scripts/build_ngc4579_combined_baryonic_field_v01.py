#!/usr/bin/env python3
"""Build NGC4579 molecular-gas gravity and the combined baryonic field."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
SOURCE = ROOT / "data" / "external" / "literature" / "ngc4579_coming_co" / "NGC4579_12CO_RADEC.mom0.fits"
REPORT = ROOT / "reports" / "ngc4579_combined_baryonic_field_v01.md"
G = 4.30091e-6
DISTANCE_MPC = 16.5
PA_DEG = 90.3
INCLINATION_DEG = 38.7
RING_WIDTH_KPC = 1.0
ALPHA_CO = [3.2, 4.35, 5.5]
SOFTENING_KPC = [0.1, 0.3, 0.5]


def ring_v2(radius: np.ndarray, ring_radius: np.ndarray, ring_mass: np.ndarray, softening: float) -> np.ndarray:
    theta = np.linspace(0.0, 2.0 * np.pi, 720, endpoint=False)
    result = np.zeros_like(radius)
    for a, mass in zip(ring_radius, ring_mass):
        if mass <= 0.0:
            continue
        denominator = (
            radius[:, None] ** 2 + a**2 - 2.0 * radius[:, None] * a * np.cos(theta)[None, :] + softening**2
        ) ** 1.5
        result += G * mass * radius * np.mean(
            (radius[:, None] - a * np.cos(theta)[None, :]) / denominator, axis=1
        )
    return result


def main() -> None:
    with fits.open(SOURCE, memmap=False) as hdul:
        image = hdul[0].data.astype(float)
        header = hdul[0].header
    signal = np.isfinite(image) & (image > 0.0)
    yy, xx = np.indices(image.shape)
    dx_arcsec = (xx + 1.0 - header["CRPIX1"]) * header["CDELT1"] * 3600.0 * np.cos(np.deg2rad(header["CRVAL2"]))
    dy_arcsec = (yy + 1.0 - header["CRPIX2"]) * header["CDELT2"] * 3600.0
    pa = np.deg2rad(PA_DEG)
    major = dx_arcsec * np.sin(pa) + dy_arcsec * np.cos(pa)
    minor = -dx_arcsec * np.cos(pa) + dy_arcsec * np.sin(pa)
    radius_pix = np.sqrt(major**2 + (minor / np.cos(np.deg2rad(INCLINATION_DEG))) ** 2)
    radius_pix *= DISTANCE_MPC * 1e3 / 206265.0
    pixel_kpc = abs(header["CDELT1"]) * 3600.0 * DISTANCE_MPC * 1e3 / 206265.0
    pixel_area_pc2 = pixel_kpc**2 * 1e6
    max_radius = np.ceil(radius_pix[signal].max() / RING_WIDTH_KPC) * RING_WIDTH_KPC
    edges = np.arange(0.0, max_radius + RING_WIDTH_KPC, RING_WIDTH_KPC)
    centers = 0.5 * (edges[:-1] + edges[1:])
    rows = []
    for lo, hi, center in zip(edges[:-1], edges[1:], centers):
        mask = signal & (radius_pix >= lo) & (radius_pix < hi)
        row = {"radius_inner_kpc": lo, "radius_outer_kpc": hi, "radius_kpc": center, "n_signal_pixels": int(mask.sum())}
        for alpha in ALPHA_CO:
            row[f"molecular_plus_helium_mass_alpha{alpha:.2f}_msun"] = float((image[mask] * alpha * pixel_area_pc2).sum())
        rows.append(row)
    profile = pd.DataFrame(rows)
    profile.to_csv(DATA / "ngc4579_coming_co_radial_profile_v01.csv", index=False)

    stellar = pd.read_csv(DATA / "ngc4579_stellar_velocity_field_v01.csv")
    hi = pd.read_csv(DATA / "ngc4579_viva_hi_gravity_v01.csv")
    radius = stellar.radius_kpc.to_numpy(float)
    out = stellar[["radius_kpc", "vstar_total_primary_km_s"]].copy()
    out["v2_star_primary_km2_s2"] = out.vstar_total_primary_km_s**2
    for alpha in ALPHA_CO:
        masses = profile[f"molecular_plus_helium_mass_alpha{alpha:.2f}_msun"].to_numpy(float)
        for softening in SOFTENING_KPC:
            v2_h2 = ring_v2(radius, centers, masses, softening)
            v2_hi = hi[f"v2_hi_helium_disk_h{softening:.1f}_km2_s2"].to_numpy(float)
            out[f"v2_h2_alpha{alpha:.2f}_h{softening:.1f}_km2_s2"] = v2_h2
            total = out.v2_star_primary_km2_s2.to_numpy(float) + v2_hi + v2_h2
            out[f"vbar_alpha{alpha:.2f}_h{softening:.1f}_km_s"] = np.sqrt(np.maximum(total, 0.0))
    out["uses_halpha_endpoint_or_dark_discrepancy"] = False
    out.to_csv(DATA / "ngc4579_combined_baryonic_field_v01.csv", index=False)
    total_masses = {
        f"alpha_{alpha:.2f}": float(profile[f"molecular_plus_helium_mass_alpha{alpha:.2f}_msun"].sum())
        for alpha in ALPHA_CO
    }
    result = {
        "schema": "tau_core_ngc4579_combined_baryonic_field_v01",
        "status": "ENDPOINT_BLIND_STELLAR_HI_H2_BARYONIC_FIELD_READY",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "co_bunit": header["BUNIT"], "co_signal_pixels": int(signal.sum()),
        "alpha_co_sensitivities_msun_pc2_per_k_km_s": ALPHA_CO,
        "molecular_plus_helium_mass_msun": total_masses,
        "published_reference_molecular_plus_helium_mass_msun": 2.93e9,
        "primary_alpha_co": 4.35, "primary_vertical_softening_kpc": 0.3,
        "gravity_method": "signed axisymmetric finite-thickness ring integration for HI and H2",
        "construction_uses_halpha_endpoint_or_dark_discrepancy": False,
        "stellar_field_ready": True, "hi_gravity_ready": True,
        "molecular_gas_gravity_ready": True, "combined_baryonic_field_ready": True,
        "halpha_endpoint_ready": False, "scoring_allowed": False,
        "claim_boundary": "endpoint-blind baryonic predictor ready; Halpha endpoint access remains required"
    }
    (DATA / "ngc4579_combined_baryonic_field_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# NGC4579 combined baryonic field v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The checksum-frozen COMING moment-0 map yields H2+helium masses `{total_masses}` under the frozen alpha_CO sensitivity. Stellar, H I and H2 radial forces are combined at signed `v^2` level using finite-thickness disk rings.\n\n"
        "No Halpha endpoint or dark-discrepancy value enters construction. The baryonic field is ready, but scoring remains closed until the prospective Halpha endpoint is acquired.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
