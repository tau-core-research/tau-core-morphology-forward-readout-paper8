#!/usr/bin/env python3
"""Run the source-frozen NGC2541 HALOGAS side-consistency endpoint."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS
import astropy.units as u


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data/protocols/ngc2541_halogas_independent_side_consistency_endpoint_v01.json"
GEOMETRY = ROOT / "data/derived/ngc2541_signed_descriptor_source_geometry_freeze_v01_points.csv"
ENDPOINT_DIR = ROOT / "data/external/literature/ngc2541_halogas_independent_endpoint_v01"
MOM0 = ENDPOINT_DIR / "NGC2541-HR_mom0m.fits"
MOM1 = ENDPOINT_DIR / "NGC2541-HR_mom1m.fits"
OUT_JSON = ROOT / "data/derived/ngc2541_halogas_independent_side_consistency_endpoint_v01.json"
OUT_CSV = ROOT / "data/derived/ngc2541_halogas_independent_side_consistency_endpoint_v01_rings.csv"
REPORT = ROOT / "reports/ngc2541_halogas_independent_side_consistency_endpoint_v01.md"


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_map(path: Path) -> tuple[np.ndarray, fits.Header]:
    with fits.open(path, memmap=True) as hdul:
        data = np.asarray(hdul[0].data, dtype=float).squeeze()
        header = hdul[0].header.copy()
    if data.ndim != 2:
        raise RuntimeError(f"expected a 2D moment map, got {data.shape}")
    return data, header


def geometry_from_normals(n_w: np.ndarray, n_n: np.ndarray, n_los: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    inc = np.degrees(np.arccos(np.clip(n_los, -1.0, 1.0)))
    normal_pa = np.degrees(np.arctan2(-n_w, n_n)) % 360.0
    major_pa = (normal_pa + 90.0) % 180.0
    return inc, major_pa


def disk_coordinates(east: np.ndarray, north: np.ndarray, inc_deg: np.ndarray, pa_deg: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    pa = np.radians(pa_deg)
    inc = np.radians(inc_deg)
    major = east * np.sin(pa) + north * np.cos(pa)
    minor = -east * np.cos(pa) + north * np.sin(pa)
    radius = np.hypot(major, minor / np.cos(inc))
    cos_theta = np.divide(major, radius, out=np.zeros_like(radius), where=radius > 0)
    return radius, cos_theta


def ring_summary(radius: np.ndarray, cos_theta: np.ndarray, velocity: np.ndarray, inc_deg: np.ndarray,
                 valid: np.ndarray, centres: np.ndarray, edges: np.ndarray, label: str, minimum: int) -> pd.DataFrame:
    speed = (velocity - 559.5) / (np.sin(np.radians(inc_deg)) * cos_theta)
    rows = []
    for centre, lo, hi in zip(centres, edges[:-1], edges[1:]):
        base = valid & (radius >= lo) & (radius < hi) & (np.abs(cos_theta) >= 0.8) & np.isfinite(speed)
        pos = speed[base & (cos_theta > 0)]
        neg = speed[base & (cos_theta < 0)]
        # The sign reversal in cos(theta) makes both sides positive for circular rotation.
        eligible = len(pos) >= minimum and len(neg) >= minimum
        vp = float(np.median(pos)) if len(pos) else math.nan
        vn = float(np.median(neg)) if len(neg) else math.nan
        rows.append({
            "geometry": label,
            "radius_arcsec": float(centre),
            "n_positive_side_pixels": int(len(pos)),
            "n_negative_side_pixels": int(len(neg)),
            "positive_side_speed_kms": vp,
            "negative_side_speed_kms": vn,
            "absolute_side_difference_kms": abs(vp - vn) if eligible else math.nan,
            "eligible": bool(eligible),
        })
    return pd.DataFrame(rows)


def main() -> None:
    protocol = json.loads(PROTOCOL.read_text())
    for path, key in [(MOM0, "moment0_md5"), (MOM1, "moment1_md5")]:
        if not path.exists() or md5(path) != protocol["independent_endpoint"][key]:
            raise RuntimeError(f"missing or hash-mismatched frozen endpoint: {path.name}")

    mom0, header0 = load_map(MOM0)
    mom1, header1 = load_map(MOM1)
    if mom0.shape != mom1.shape:
        raise RuntimeError("moment-map shapes differ")
    w0 = WCS(header0).celestial
    w1 = WCS(header1).celestial
    if not w0.wcs.compare(w1.wcs):
        raise RuntimeError("moment-map celestial WCS differs")

    yy, xx = np.indices(mom0.shape)
    sky = w0.pixel_to_world(xx, yy)
    centre = SkyCoord("08h14m40.07s", "+49d03m41.2s", frame="icrs")
    # Astropy may expose the FITS celestial WCS as FK5 rather than ICRS.  This
    # is a coordinate-frame compatibility conversion, not an endpoint-derived
    # calibration change.
    centre = centre.transform_to(sky.frame)
    east, north = centre.spherical_offsets_to(sky)
    east = east.to_value(u.arcsec)
    north = north.to_value(u.arcsec)
    valid = np.isfinite(mom0) & (mom0 > 0) & np.isfinite(mom1)

    source = pd.read_csv(GEOMETRY)
    centres = source["radius_arcsec"].to_numpy(float)
    inc_nodes, pa_nodes = geometry_from_normals(
        source["n_w_unit"].to_numpy(float),
        source["n_n_unit"].to_numpy(float),
        source["n_los_unit"].to_numpy(float),
    )
    edges = np.r_[30.0, (centres[:-1] + centres[1:]) / 2.0, 590.0]

    fixed_inc = np.full(mom0.shape, 66.3)
    fixed_pa = np.full(mom0.shape, 171.2)
    fixed_r, fixed_cos = disk_coordinates(east, north, fixed_inc, fixed_pa)

    variable_r = np.hypot(east, north)
    for _ in range(4):
        variable_inc = np.interp(variable_r, centres, inc_nodes, left=inc_nodes[0], right=inc_nodes[-1])
        unwrapped_pa = np.degrees(np.unwrap(np.radians(pa_nodes * 2.0))) / 2.0
        variable_pa = np.interp(variable_r, centres, unwrapped_pa, left=unwrapped_pa[0], right=unwrapped_pa[-1])
        variable_r, variable_cos = disk_coordinates(east, north, variable_inc, variable_pa)

    minimum = int(protocol["estimator"]["minimum_pixels_per_side_ring"])
    fixed = ring_summary(fixed_r, fixed_cos, mom1, fixed_inc, valid, centres, edges, "fixed", minimum)
    variable = ring_summary(variable_r, variable_cos, mom1, variable_inc, valid, centres, edges, "variable", minimum)
    rings = pd.concat([fixed, variable], ignore_index=True)
    common = fixed[fixed.eligible].merge(variable[variable.eligible], on="radius_arcsec", suffixes=("_fixed", "_variable"))
    if common.empty:
        raise RuntimeError("no common eligible rings under the frozen protocol")
    f = common["absolute_side_difference_kms_fixed"].to_numpy(float)
    v = common["absolute_side_difference_kms_variable"].to_numpy(float)
    result = {
        "schema": protocol["schema"],
        "status": "POST_OPEN_DESCRIPTIVE_MOMENT1_SIDE_SYMMETRY_DIAGNOSTIC",
        "n_common_eligible_rings": int(len(common)),
        "fixed_mean_absolute_side_difference_kms": float(np.mean(f)),
        "variable_mean_absolute_side_difference_kms": float(np.mean(v)),
        "delta_mean_variable_minus_fixed_kms": float(np.mean(v) - np.mean(f)),
        "fixed_median_absolute_side_difference_kms": float(np.median(f)),
        "variable_median_absolute_side_difference_kms": float(np.median(v)),
        "fraction_common_rings_improved": float(np.mean(v < f)),
        "primary_metric_direction_met": bool(np.mean(v) < np.mean(f)),
        "free_parameters": 0,
        "endpoint_hashes_verified": True,
        "claim_boundary": "Independent map input, but calibration-centre and footprint sensitivity demote this to a descriptive moment-1 side-symmetry diagnostic; it cannot select a Tau q_R, parent morphology, dark-matter replacement, or Nature occupation.",
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    rings.to_csv(OUT_CSV, index=False)
    OUT_JSON.write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# NGC2541 independent HALOGAS side-consistency endpoint v01\n\n"
        + "| status | common rings | fixed mean | variable mean | delta | improved fraction | primary direction met |\n"
        + "| --- | ---: | ---: | ---: | ---: | ---: | --- |\n"
        + f"| {result['status']} | {result['n_common_eligible_rings']} | "
        + f"{result['fixed_mean_absolute_side_difference_kms']:.6f} | "
        + f"{result['variable_mean_absolute_side_difference_kms']:.6f} | "
        + f"{result['delta_mean_variable_minus_fixed_kms']:.6f} | "
        + f"{result['fraction_common_rings_improved']:.6f} | {result['primary_metric_direction_met']} |\n\n"
        + protocol["claim_boundary"] + "\n"
    )
    print("NGC2541_HALOGAS_INDEPENDENT_SIDE_CONSISTENCY_ENDPOINT_COMPLETE")


if __name__ == "__main__":
    main()
