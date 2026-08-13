#!/usr/bin/env python3
"""Run the frozen retrospective UGC07323 two-side channel-law preflight."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
SPARC = ROOT / "data" / "external" / "sparc" / "UGC07323_rotmod.dat"
REPORT = ROOT / "reports" / "ugc07323_oriented_channel_compatibility_v01.md"
C_KM_S = 299792.458


def inverse_q(vobs: np.ndarray, vbar: np.ndarray) -> np.ndarray:
    beta_obs = vobs / C_KM_S
    beta_bar = vbar / C_KM_S
    delta = (beta_obs - beta_bar) / (1.0 - beta_obs * beta_bar)
    return np.arctanh(delta)


def main() -> None:
    freeze = json.loads((DATA / "ugc07323_oriented_channel_compatibility_freeze_v01.json").read_text())
    sides = pd.read_csv(DATA / "ghasp_full_federation_side_points_v01.csv")
    sides = sides[sides.ghasp_key.eq("UGC7323") & sides.velocity_km_s.gt(0)].copy()
    approaching = sides[sides.side.eq("a")].sort_values("radius_kpc")
    receding = sides[sides.side.eq("r")].sort_values("radius_kpc")

    sparc = pd.read_csv(
        SPARC, comment="#", sep=r"\s+",
        names=["radius_kpc", "vobs_sparc", "vobs_error", "vgas", "vdisk", "vbul", "sbdisk", "sbbul"],
    )
    vbar2 = np.sign(sparc.vgas) * sparc.vgas**2 + 0.5 * sparc.vdisk**2 + 0.7 * sparc.vbul**2
    sparc["vbar_km_s"] = np.sqrt(np.maximum(vbar2, 0.0))
    lo = max(approaching.radius_kpc.min(), receding.radius_kpc.min())
    hi = min(approaching.radius_kpc.max(), receding.radius_kpc.max())
    common = sparc[sparc.radius_kpc.between(lo, hi)].copy()

    r = common.radius_kpc.to_numpy(float)
    vbar = common.vbar_km_s.to_numpy(float)
    for label, frame in (("approaching", approaching), ("receding", receding)):
        velocity = np.interp(r, frame.radius_kpc, frame.velocity_km_s)
        error = np.interp(r, frame.radius_kpc, frame.velocity_error_km_s)
        q = inverse_q(velocity, vbar)
        q_hi = inverse_q(velocity + error, vbar)
        q_lo = inverse_q(np.maximum(velocity - error, 0.0), vbar)
        common[f"v_{label}_km_s"] = velocity
        common[f"v_{label}_error_km_s"] = error
        common[f"q_{label}"] = q
        common[f"q_{label}_error"] = 0.5 * np.abs(q_hi - q_lo)

    qa = common.q_approaching.to_numpy(float)
    qr = common.q_receding.to_numpy(float)
    sa = common.q_approaching_error.to_numpy(float)
    sr = common.q_receding_error.to_numpy(float)
    variance = np.maximum(sa**2 + sr**2, 1e-30)
    difference = qa - qr
    q_common = 0.5 * (qa + qr)
    q_contrast = 0.5 * difference
    common["q_common"] = q_common
    common["q_side_contrast"] = q_contrast
    common["cq_common_km_s_equivalent"] = C_KM_S * q_common
    common["cq_side_contrast_km_s_equivalent"] = C_KM_S * q_contrast
    common.to_csv(DATA / "ugc07323_oriented_channel_compatibility_points_v01.csv", index=False)

    chi2 = float(np.sum(difference**2 / variance))
    weighted_mean_difference = float(np.sum(difference / variance) / np.sum(1.0 / variance))
    weighted_mean_difference_error = float(np.sqrt(1.0 / np.sum(1.0 / variance)))
    result = {
        "schema": "tau_core_ugc07323_oriented_channel_compatibility_v01",
        "status": "RETROSPECTIVE_ORIENTED_LAW_COMPATIBILITY_PREFLIGHT_COMPLETE",
        "freeze_status": freeze["status"], "fitted_parameters": 0,
        "n_common_radii": int(len(common)),
        "common_radius_range_kpc": [float(r.min()), float(r.max())],
        "side_compatibility": {
            "chi2": chi2, "degrees_of_freedom": int(len(common)),
            "chi2_per_point": chi2 / len(common),
            "weighted_mean_q_approaching_minus_receding": weighted_mean_difference,
            "weighted_mean_difference_error": weighted_mean_difference_error,
            "weighted_mean_difference_z": weighted_mean_difference / weighted_mean_difference_error,
        },
        "cq_common_km_s_equivalent": {
            "median": float(np.median(C_KM_S * q_common)),
            "minimum": float(np.min(C_KM_S * q_common)),
            "maximum": float(np.max(C_KM_S * q_common)),
        },
        "cq_side_contrast_km_s_equivalent": {
            "median_absolute": float(np.median(np.abs(C_KM_S * q_contrast))),
            "maximum_absolute": float(np.max(np.abs(C_KM_S * q_contrast))),
        },
        "common_oriented_load_compatible_with_both_sides": bool(chi2 / len(common) <= 2.0),
        "source_native_morphology_body_ready": False,
        "sparc_baryonic_covariance_included": False,
        "dark_halo_degeneracy_removed": False,
        "physical_channel_detected": False,
        "claim_boundary": freeze["claim_boundary"]
    }
    (DATA / "ugc07323_oriented_channel_compatibility_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# UGC07323 oriented-channel compatibility v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The zero-parameter inverse law yields `{len(common)}` common radii over `{result['common_radius_range_kpc']}` kpc. "
        f"Approaching/receding q compatibility has chi2 per point `{result['side_compatibility']['chi2_per_point']:.3f}` and weighted mean-difference z "
        f"`{result['side_compatibility']['weighted_mean_difference_z']:.3f}`. Median common `c q` equivalent is "
        f"`{result['cq_common_km_s_equivalent']['median']:.2f} km/s`; median absolute side contrast is "
        f"`{result['cq_side_contrast_km_s_equivalent']['median_absolute']:.2f} km/s`.\n\n"
        "This is retrospective compatibility only. A shared dark halo or conventional dynamics produces the same common-load pattern; "
        "the morphology body is not source-ready and baryonic covariance is absent.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
