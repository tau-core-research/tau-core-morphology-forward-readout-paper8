#!/usr/bin/env python3
"""Build an endpoint-blind NGC4579 stellar velocity field from COMING+S4G."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import gammainc, iv, kv


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "ngc4579_stellar_velocity_field_v01.md"
G = 4.30091e-6
DISTANCE_MPC = 16.5
MSTAR = 6.90e10
MSTAR_ERROR = 0.16e10
F_BULGE, F_DISK, F_BAR = 0.113, 0.776, 0.111
RD_ARCSEC = 45.27
RE_BULGE_ARCSEC = 3.91
N_BULGE = 2.655
RBAR_ARCSEC = 45.0


def arcsec_to_kpc(value: float) -> float:
    return value * DISTANCE_MPC * 1e3 / 206265.0


def disk_v2(radius: np.ndarray, mass: float, scale: float) -> np.ndarray:
    y = radius / (2.0 * scale)
    sigma0 = mass / (2.0 * np.pi * scale**2)
    return 4.0 * np.pi * G * sigma0 * scale * y**2 * (
        iv(0, y) * kv(0, y) - iv(1, y) * kv(1, y)
    )


def sersic_fraction(radius: np.ndarray, re: float, n: float) -> np.ndarray:
    bn = 2.0 * n - 1.0 / 3.0 + 0.009876 / n
    return gammainc(2.0 * n, bn * (radius / re) ** (1.0 / n))


def bar_fraction(radius: np.ndarray, rbar: float, power: float) -> np.ndarray:
    return np.minimum((radius / rbar) ** power, 1.0)


def main() -> None:
    radius = np.arange(0.1, 15.0001, 0.05)
    fractions = np.array([F_BULGE, F_DISK, F_BAR])
    fractions /= fractions.sum()
    mbulge, mdisk, mbar = MSTAR * fractions
    rd, re, rbar = map(arcsec_to_kpc, [RD_ARCSEC, RE_BULGE_ARCSEC, RBAR_ARCSEC])
    v2_disk = disk_v2(radius, mdisk, rd)
    v2_bulge = G * mbulge * sersic_fraction(radius, re, N_BULGE) / radius
    v2_bar = G * mbar * bar_fraction(radius, rbar, 2.0) / radius
    v2_bar_lo = G * mbar * bar_fraction(radius, rbar, 3.0) / radius
    v2_bar_hi = G * mbar * bar_fraction(radius, rbar, 1.0) / radius
    out = pd.DataFrame({"radius_kpc": radius})
    out["vstar_disk_km_s"] = np.sqrt(v2_disk)
    out["vstar_bulge_km_s"] = np.sqrt(v2_bulge)
    out["vstar_bar_primary_km_s"] = np.sqrt(v2_bar)
    out["vstar_total_primary_km_s"] = np.sqrt(v2_disk + v2_bulge + v2_bar)
    vlo = np.sqrt(v2_disk + v2_bulge + v2_bar_lo)
    vhi = np.sqrt(v2_disk + v2_bulge + v2_bar_hi)
    out["vstar_total_bar_envelope_low_km_s"] = np.minimum(vlo, vhi)
    out["vstar_total_bar_envelope_high_km_s"] = np.maximum(vlo, vhi)
    out["uses_halpha_endpoint_or_dark_discrepancy"] = False
    out.to_csv(DATA / "ngc4579_stellar_velocity_field_v01.csv", index=False)
    result = {
        "schema": "tau_core_ngc4579_stellar_velocity_field_v01",
        "status": "ENDPOINT_BLIND_STELLAR_FIELD_READY_GAS_OPEN",
        "stellar_mass_msun": MSTAR, "stellar_mass_error_msun": MSTAR_ERROR,
        "stellar_mass_source": "Salak et al. 2019 barred-galaxy table; WISE 3.4 micron",
        "s4g_component_fractions": {"bulge": F_BULGE, "disk": F_DISK, "bar": F_BAR},
        "disk_scale_kpc": rd, "bulge_re_kpc": re, "bulge_sersic_n": N_BULGE,
        "bar_radius_kpc_s4g": rbar, "coming_bar_radius_kpc": 3.62,
        "primary_bar_enclosure_power": 2.0, "bar_sensitivity_powers": [1.0, 3.0],
        "radius_grid_kpc": [0.1, 15.0, 0.05],
        "construction_uses_halpha_endpoint_or_dark_discrepancy": False,
        "stellar_field_ready": True, "gas_field_ready": False,
        "baryonic_field_ready": False, "scoring_allowed": False,
        "claim_boundary": "axisymmetrized source-only stellar predictor; Halpha endpoint remains unopened"
    }
    (DATA / "ngc4579_stellar_velocity_field_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# NGC4579 stellar velocity field v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "The source-only WISE stellar mass and S4G bulge/disk/bar decomposition define an exact exponential-disk term, spherical Sersic bulge, and axisymmetrized bar with frozen shape envelope on a `0.1-15 kpc` grid. No Halpha endpoint or dark-discrepancy value enters construction.\n\n"
        "The stellar field is ready. Gas gravity and the combined baryonic field remain open; scoring is forbidden.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
