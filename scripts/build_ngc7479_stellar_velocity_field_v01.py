#!/usr/bin/env python3
"""Build an endpoint-blind NGC7479 stellar velocity field from COMING+S4G."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import gammainc, iv, kv


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "ngc7479_stellar_velocity_field_v01.md"
G = 4.30091e-6  # kpc (km/s)^2 / Msun
DISTANCE_MPC = 32.0
MSTAR = 1.07e11
MSTAR_ERROR = 0.03e11
F_BULGE, F_DISK, F_BAR = 0.083, 0.680, 0.238
F_SUM = F_BULGE + F_DISK + F_BAR
RD_ARCSEC = 37.28
RE_BULGE_ARCSEC = 1.16
N_BULGE = 1.007
RBAR_ARCSEC = 81.6


def arcsec_to_kpc(value: float) -> float:
    return value * DISTANCE_MPC * 1e3 / 206265.0


def disk_v2(radius: np.ndarray, mass: float, scale: float) -> np.ndarray:
    y = radius / (2.0 * scale)
    sigma0 = mass / (2.0 * np.pi * scale**2)
    return 4.0 * np.pi * G * sigma0 * scale * y**2 * (iv(0, y) * kv(0, y) - iv(1, y) * kv(1, y))


def sersic_enclosed_fraction(radius: np.ndarray, re: float, n: float) -> np.ndarray:
    bn = 2.0 * n - 1.0 / 3.0 + 0.009876 / n
    return gammainc(2.0 * n, bn * (radius / re) ** (1.0 / n))


def bar_enclosed_fraction(radius: np.ndarray, rbar: float, power: float) -> np.ndarray:
    return np.minimum((radius / rbar) ** power, 1.0)


def main() -> None:
    endpoint = pd.read_csv(DATA / "ngc7479_hi_rotation_endpoint_v01.csv")
    radius = endpoint.radius_kpc_at_source_distance.to_numpy(float)
    fractions = np.array([F_BULGE, F_DISK, F_BAR]) / F_SUM
    mbulge, mdisk, mbar = MSTAR * fractions
    rd, re, rbar = map(arcsec_to_kpc, [RD_ARCSEC, RE_BULGE_ARCSEC, RBAR_ARCSEC])
    v2_disk = disk_v2(radius, mdisk, rd)
    v2_bulge = G * mbulge * sersic_enclosed_fraction(radius, re, N_BULGE) / radius
    v2_bar = G * mbar * bar_enclosed_fraction(radius, rbar, 2.0) / radius
    v2_bar_lo = G * mbar * bar_enclosed_fraction(radius, rbar, 3.0) / radius
    v2_bar_hi = G * mbar * bar_enclosed_fraction(radius, rbar, 1.0) / radius
    vstar = np.sqrt(v2_disk + v2_bulge + v2_bar)
    vlo = np.sqrt(v2_disk + v2_bulge + v2_bar_lo)
    vhi = np.sqrt(v2_disk + v2_bulge + v2_bar_hi)
    out = endpoint[["galaxy", "radius_arcsec", "radius_kpc_at_source_distance"]].copy()
    out["vstar_disk_km_s"] = np.sqrt(v2_disk)
    out["vstar_bulge_km_s"] = np.sqrt(v2_bulge)
    out["vstar_bar_primary_km_s"] = np.sqrt(v2_bar)
    out["vstar_total_primary_km_s"] = vstar
    out["vstar_total_bar_envelope_low_km_s"] = np.minimum(vlo, vhi)
    out["vstar_total_bar_envelope_high_km_s"] = np.maximum(vlo, vhi)
    out["uses_rotation_endpoint_in_construction"] = False
    out.to_csv(DATA / "ngc7479_stellar_velocity_field_v01.csv", index=False)
    payload = {
        "schema": "tau_core_ngc7479_stellar_velocity_field_v01",
        "status": "ENDPOINT_BLIND_STELLAR_VELOCITY_FIELD_CONSTRUCTED_GAS_OPEN",
        "stellar_mass_msun": MSTAR,
        "stellar_mass_error_msun": MSTAR_ERROR,
        "stellar_mass_source": "Salak et al. 2019 Table 3, WISE 3.4 micron mass",
        "s4g_component_fractions_raw": {"bulge": F_BULGE, "disk": F_DISK, "bar": F_BAR},
        "s4g_fraction_sum": F_SUM,
        "component_fractions_renormalized": {"bulge": float(fractions[0]), "disk": float(fractions[1]), "bar": float(fractions[2])},
        "disk_scale_kpc": rd,
        "bulge_re_kpc": re,
        "bar_radius_kpc_s4g": rbar,
        "primary_bar_enclosure_power": 2.0,
        "bar_enclosure_sensitivity_powers": [1.0, 3.0],
        "dimension_check": "G*M/R gives velocity squared; Bessel and enclosed fractions are dimensionless",
        "uses_rotation_endpoint_or_dark_discrepancy_in_construction": False,
        "stellar_velocity_field_ready": True,
        "gas_velocity_field_ready": False,
        "baryonic_velocity_field_ready": False,
        "endpoint_scoring_allowed": False,
        "claim_boundary": "axisymmetrized stellar predictor with frozen bar-shape sensitivity; not a unique barred potential reconstruction",
    }
    (DATA / "ngc7479_stellar_velocity_field_v01.json").write_text(json.dumps(payload, indent=2) + "\n")
    REPORT.write_text(
        "# NGC7479 stellar velocity field v01\n\n"
        f"Status: `{payload['status']}`\n\n"
        "The stellar normalization is the endpoint-blind WISE mass `Mstar=(1.07+/-0.03)e11 Msun`. S4G flux fractions split it into bulge, exponential disk, and bar components. "
        "The disk uses the exact thin exponential-disk Bessel expression; the bulge uses a spherical Sersic enclosed mass; the bar uses a frozen axisymmetrized enclosed-mass power `p=2`, with `p=1,3` sensitivity bounds.\n\n"
        "No observed rotation velocity or dark-discrepancy residual enters construction. The stellar field is ready, while the gas field and combined baryonic field remain open.\n"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
