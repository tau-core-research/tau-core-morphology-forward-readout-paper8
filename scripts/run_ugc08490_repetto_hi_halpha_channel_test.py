#!/usr/bin/env python3
"""Test the published UGC08490 H I profile against GHASP H-alpha at common radii."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/ugc08490_repetto_hi_halpha_channel_test_v01.md"


def main() -> None:
    hi = pd.read_csv(DATA / "ugc08490_repetto_hi_vector_profile_v01.csv")
    ha = pd.read_csv(DATA / "ghasp_full_federation_side_points_v01.csv")
    ha = ha[ha.sparc_match.eq("UGC08490")]
    side_maxima = ha.groupby("side").radius_arcsec.max()
    max_radius = min(float(hi.radius_arcsec.max()), float(side_maxima.min()))
    common = hi[(hi.radius_arcsec >= 5) & (hi.radius_arcsec <= max_radius)].copy()
    side_profiles = []
    for side in ("a", "r"):
        source = ha[ha.side.eq(side)].sort_values("radius_arcsec")
        side_profiles.append(np.interp(common.radius_arcsec, source.radius_arcsec, source.velocity_km_s))
    common["halpha_side_mean_km_s"] = np.mean(side_profiles, axis=0)
    common["hi_minus_halpha_km_s"] = common.hi_rotation_km_s - common.halpha_side_mean_km_s
    # A pure multiplicative tracer calibration is the minimal wrong-channel control.
    scale = float(np.dot(common.halpha_side_mean_km_s, common.hi_rotation_km_s) /
                  np.dot(common.halpha_side_mean_km_s, common.halpha_side_mean_km_s))
    common["scaled_halpha_km_s"] = scale * common.halpha_side_mean_km_s
    common["hi_minus_scaled_halpha_km_s"] = common.hi_rotation_km_s - common.scaled_halpha_km_s
    common.to_csv(DATA / "ugc08490_repetto_hi_halpha_common_profile_v01.csv", index=False)
    raw_rms = float(np.sqrt(np.mean(common.hi_minus_halpha_km_s**2)))
    scaled_rms = float(np.sqrt(np.mean(common.hi_minus_scaled_halpha_km_s**2)))
    result = {
        "schema": "ugc08490_repetto_hi_halpha_channel_test_v01",
        "status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
        "n_common_points": len(common), "common_radius_arcsec": [float(common.radius_arcsec.min()), max_radius],
        "both_halpha_sides_covered_without_extrapolation": True,
        "raw_rms_km_s": raw_rms, "multiplicative_halpha_scale": scale,
        "scale_control_rms_km_s": scaled_rms,
        "rms_reduction_fraction": 1 - scaled_rms / raw_rms,
        "tau_kernel_tested": False, "physical_channel_detected": False,
        "endpoint_access": False,
        "claim_boundary": (
            "same-body figure-derived H I versus published H-alpha diagnostic; a tracer difference "
            "does not identify observer-path, time, quantum, or Tau-kernel origin"
        ),
    }
    (DATA / "ugc08490_repetto_hi_halpha_channel_test_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    REPORT.write_text(
        "# UGC08490 published H I-Halpha channel test v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The Repetto et al. vector figure supplies {len(hi)} observed H I points; "
        f"{len(common)} lie in the common GHASP Halpha range. Raw RMS tracer difference is "
        f"`{raw_rms:.2f} km/s`. A pure multiplicative Halpha scale of `{scale:.4f}` gives "
        f"`{scaled_rms:.2f} km/s` RMS.\n\n"
        "This measures tracer/readout disagreement but does not identify its physical origin. "
        "The next gate is a frozen Tau-kernel-versus-scale shape comparison.\n",
        encoding="utf-8",
    )
    print(result["status"], f"n={len(common)}", f"raw={raw_rms:.2f}", f"scaled={scaled_rms:.2f}")


if __name__ == "__main__":
    main()
