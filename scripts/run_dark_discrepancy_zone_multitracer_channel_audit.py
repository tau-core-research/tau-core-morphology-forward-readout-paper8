#!/usr/bin/env python3
"""Audit H I-Halpha channel contrast specifically beyond frozen D>=1.5 onsets."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2


ROOT = Path(__file__).resolve().parents[1]
TAU_ROOT = ROOT.parent
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
ATLAS = TAU_ROOT / (
    "tau-core-theory/source_material/tau_core_foundations/numerical_checks/"
    "tau_core_galactic_clock_channel_reparameterization_v01_galaxies.csv"
)
SOURCE_FEATURES = DATA / "s4g_optical_morphology_attribution_source_features_v02.csv"


def kpc_per_arcsec(distance_mpc: float) -> float:
    return distance_mpc * 1000.0 / 206265.0


def gls(values: np.ndarray, covariance: np.ndarray) -> dict[str, float]:
    inverse = np.linalg.pinv(covariance)
    ones = np.ones(len(values))
    variance = 1.0 / float(ones @ inverse @ ones)
    mean = variance * float(ones @ inverse @ values)
    chi2_zero = float(values @ inverse @ values)
    return {
        "n_post_onset": len(values),
        "gls_mean_km_s": mean,
        "gls_sigma_km_s": math.sqrt(variance),
        "gls_z": mean / math.sqrt(variance),
        "chi2_zero": chi2_zero,
        "chi2_zero_p": float(chi2.sf(chi2_zero, len(values))),
    }


def main() -> None:
    atlas = pd.read_csv(ATLAS).set_index("galaxy")
    features = pd.read_csv(SOURCE_FEATURES).set_index("galaxy")
    results = {}

    galaxy = "NGC3726"
    distance = math.exp(float(features.loc[galaxy, "log_distance_mpc"]))
    onset = float(atlas.loc[galaxy, "onset_radius_kpc_d1p5"])
    rows = pd.read_csv(DATA / "ngc3726_hi_halpha_channel_preflight_v01.csv")
    rows["radius_kpc"] = rows["radius_arcsec"] * kpc_per_arcsec(distance)
    post = rows.loc[rows["radius_kpc"].ge(onset)].copy()
    covariance = np.diag(post["delta_odd_measurement_sigma_km_s"].to_numpy() ** 2)
    results[galaxy] = {
        "distance_mpc": distance,
        "d1p5_onset_kpc": onset,
        "d1p5_onset_arcsec": onset / kpc_per_arcsec(distance),
        "d2p0_onset_kpc": float(atlas.loc[galaxy, "onset_radius_kpc_d2p0"]),
        "max_channel_radius_kpc": float(rows["radius_kpc"].max()),
        "covariance_scope": "quoted measurement diagonal; existing full-sample inclination covariance not persisted",
        "post_d1p5": gls(post["delta_odd_los_km_s"].to_numpy(), covariance),
    }

    galaxy = "NGC4559"
    distance = math.exp(float(features.loc[galaxy, "log_distance_mpc"]))
    onset = float(atlas.loc[galaxy, "onset_radius_kpc_d1p5"])
    score = json.loads((DATA / "ngc4559_halogas_hi_halpha_replication_v01.json").read_text())
    rows = pd.read_csv(DATA / "ngc4559_halogas_hi_halpha_replication_v01.csv")
    primary = rows.loc[rows["resolution"].eq("HR")].sort_values("radius_arcsec")
    radii_kpc = primary["radius_arcsec"].to_numpy() * kpc_per_arcsec(distance)
    select = radii_kpc >= onset
    covariance_full = np.asarray(score["maps"]["HR"]["covariance"], dtype=float)
    covariance = covariance_full[np.ix_(select, select)]
    values = primary["delta_odd_los_km_s"].to_numpy()[select]
    results[galaxy] = {
        "distance_mpc": distance,
        "d1p5_onset_kpc": onset,
        "d1p5_onset_arcsec": onset / kpc_per_arcsec(distance),
        "d2p0_onset_kpc": float(atlas.loc[galaxy, "onset_radius_kpc_d2p0"]),
        "max_channel_radius_kpc": float(radii_kpc.max()),
        "covariance_scope": "HALOGAS bootstrap plus geometry variants plus Halpha covariance",
        "post_d1p5": gls(values, covariance),
    }

    p_values = [entry["post_d1p5"]["chi2_zero_p"] for entry in results.values()]
    replicated = all(value <= 0.05 for value in p_values)
    d2_covered = all(
        entry["max_channel_radius_kpc"] >= entry["d2p0_onset_kpc"]
        for entry in results.values()
    )
    payload = {
        "schema": "dark_discrepancy_zone_multitracer_channel_audit_v01",
        "status": "DIAGNOSTIC_ONLY_D1P5_ZONE_MULTITRACER_CHANNEL_NOT_REPLICATED",
        "target_zone": "persistent SPARC mass discrepancy D>=1.5 onset and beyond",
        "retrospective_zone_audit": True,
        "galaxies": results,
        "zero_contrast_rejected_in_both_galaxies": replicated,
        "d2_zone_covered_in_both_galaxies": d2_covered,
        "channel_information_candidate": replicated,
        "claim_boundary": (
            "retrospective two-galaxy D>=1.5 zone audit; no replicated channel contrast, "
            "D>=2 coverage is incomplete, and no observer-time or quantum origin is identified"
        ),
    }
    (DATA / "dark_discrepancy_zone_multitracer_channel_audit_v01.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = []
    for name, entry in results.items():
        stat = entry["post_d1p5"]
        lines.append(
            f"| {name} | {entry['d1p5_onset_kpc']:.2f} | {stat['n_post_onset']} | "
            f"{stat['gls_mean_km_s']:.2f} +/- {stat['gls_sigma_km_s']:.2f} | "
            f"{stat['chi2_zero_p']:.4f} |"
        )
    (REPORTS / "dark_discrepancy_zone_multitracer_channel_audit_v01.md").write_text(
        "# Dark-Discrepancy-Zone Multitracer Channel Audit v0.1\n\n"
        f"**Status:** `{payload['status']}`\n\n"
        "| galaxy | D>=1.5 onset kpc | post-onset N | GLS contrast km/s | zero p |\n"
        "| --- | ---: | ---: | ---: | ---: |\n" + "\n".join(lines) + "\n\n"
        "This retrospective audit targets the dark-matter-like radial zone rather than "
        "a generic tracer difference. It does not find a replicated post-onset H I-Halpha "
        "odd contrast. The stronger D>=2 zone is not covered in both galaxies.\n",
        encoding="utf-8",
    )
    print(payload["status"])


if __name__ == "__main__":
    main()
