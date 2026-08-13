#!/usr/bin/env python3
"""Compare source-frozen UGC08490 H I and H-alpha readouts on beam-scale radii."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/ugc08490_hi_halpha_channel_diagnostic_v01.md"
RADII = np.array([30.0, 60.0, 90.0])
ANNULUS_HALF_WIDTH = 15.0
INCLINATION_DEG = 53.0
MIN_ABS_COS_THETA = 0.65


def weighted_median(values: np.ndarray, weights: np.ndarray) -> float:
    order = np.argsort(values)
    values, weights = values[order], weights[order]
    return float(values[np.searchsorted(np.cumsum(weights), weights.sum() / 2)])


def main() -> None:
    pixels = pd.read_csv(DATA / "ugc08490_whisp_30arcsec_velocity_pixels_v01.csv")
    center = json.loads((DATA / "ugc08490_whisp_external_center_freeze_v01.json").read_text())[
        "center_source_pixels_by_panel"
    ]["30arcsec"]
    axis = json.loads((DATA / "ugc08490_whisp_angular_axis_preflight_v01.json").read_text())
    ra_scale = axis["ra_seconds_of_time_per_pixel"] * 15 * math.cos(math.radians(58.6765))
    dec_scale = axis["dec_arcmin_per_pixel"] * 60
    pixels["east_arcsec"] = (pixels.source_x - center[0]) * ra_scale
    pixels["north_arcsec"] = (pixels.source_y - center[1]) * dec_scale

    side_centers = {}
    for side in ("approaching", "receding"):
        part = pixels[pixels.systemic_relation.eq(side)]
        side_centers[side] = np.array([part.east_arcsec.mean(), part.north_arcsec.mean()])
    major_unit = side_centers["receding"] - side_centers["approaching"]
    major_unit /= np.linalg.norm(major_unit)
    minor_unit = np.array([-major_unit[1], major_unit[0]])
    xy = pixels[["east_arcsec", "north_arcsec"]].to_numpy()
    pixels["major_arcsec"] = xy @ major_unit
    pixels["minor_arcsec"] = xy @ minor_unit
    cos_i = math.cos(math.radians(INCLINATION_DEG))
    sin_i = math.sin(math.radians(INCLINATION_DEG))
    pixels["disk_radius_arcsec"] = np.sqrt(
        pixels.major_arcsec**2 + (pixels.minor_arcsec / cos_i) ** 2
    )
    pixels["abs_cos_theta"] = np.abs(pixels.major_arcsec / pixels.disk_radius_arcsec)
    pixels["rotation_km_s"] = (
        np.abs(pixels.velocity_bin_center_km_s - 204.0) / (sin_i * pixels.abs_cos_theta)
    )
    usable = pixels[
        pixels.systemic_relation.ne("systemic_ambiguous")
        & pixels.abs_cos_theta.ge(MIN_ABS_COS_THETA)
    ].copy()

    ghasp = pd.read_csv(DATA / "ghasp_full_federation_side_points_v01.csv")
    ghasp = ghasp[ghasp.sparc_match.eq("UGC08490")].copy()
    side_support = {
        side: {
            "minimum_usable_radius_arcsec": float(part.disk_radius_arcsec.min()),
            "maximum_usable_radius_arcsec": float(part.disk_radius_arcsec.max()),
            "usable_pixels": int(len(part)),
        }
        for side, part in usable.groupby("systemic_relation")
    }
    halpha_max = float(ghasp.radius_arcsec.max())
    common_two_side_support = all(
        side in side_support and side_support[side]["minimum_usable_radius_arcsec"] <= halpha_max
        for side in ("approaching", "receding")
    )
    rows = []
    for radius in RADII:
        hi = usable[np.abs(usable.disk_radius_arcsec - radius) < ANNULUS_HALF_WIDTH]
        for side, side_code in {"approaching": "a", "receding": "r"}.items():
            hi_side = hi[hi.systemic_relation.eq(side)]
            if hi_side.empty:
                continue
            weights = hi_side.abs_cos_theta.to_numpy() ** 2
            hi_velocity = weighted_median(hi_side.rotation_km_s.to_numpy(), weights)
            source = ghasp[ghasp.side.eq(side_code)].sort_values("radius_arcsec")
            ha_velocity = float(np.interp(radius, source.radius_arcsec, source.velocity_km_s))
            ha_error = float(np.interp(radius, source.radius_arcsec, source.velocity_error_km_s))
            hi_quant_error = float(
                hi_side.velocity_quantization_half_width_km_s.iloc[0]
                / (sin_i * MIN_ABS_COS_THETA)
            )
            rows.append({
                "radius_arcsec": radius, "side": side,
                "hi_rotation_km_s": hi_velocity,
                "hi_graphical_error_floor_km_s": hi_quant_error,
                "hi_selected_pixels": len(hi_side),
                "halpha_rotation_km_s": ha_velocity, "halpha_error_km_s": ha_error,
                "hi_minus_halpha_km_s": hi_velocity - ha_velocity,
                "endpoint_access": False,
            })
    profile = pd.DataFrame(rows)
    profile.to_csv(DATA / "ugc08490_hi_halpha_channel_profile_v01.csv", index=False)
    rms = float(np.sqrt(np.mean(profile.hi_minus_halpha_km_s**2))) if common_two_side_support else None
    median_offset = float(profile.hi_minus_halpha_km_s.median()) if common_two_side_support else None
    result = {
        "schema": "ugc08490_hi_halpha_channel_diagnostic_v01",
        "status": "NEGATIVE_RESULT_PRESERVED",
        "galaxy": "UGC08490 / NGC5204",
        "geometry": {
            "center": "external SIMBAD center transported to printed B1950 axes",
            "position_angle_rule": "line joining source-side approaching/receding WHISP color centroids",
            "inclination_deg": INCLINATION_DEG,
            "inclination_source": "WHISP printed overview",
            "minimum_abs_cos_theta": MIN_ABS_COS_THETA,
            "radii_arcsec": RADII.tolist(), "annulus_half_width_arcsec": ANNULUS_HALF_WIDTH,
        },
        "hi_usable_radial_support_by_side": side_support,
        "halpha_max_radius_arcsec": halpha_max,
        "common_two_side_radial_support": common_two_side_support,
        "one_side_audit_points": len(profile), "matched_two_side_points": 0,
        "median_hi_minus_halpha_km_s": median_offset,
        "rms_hi_minus_halpha_km_s": rms,
        "kernel_specific_channel_test_allowed": False,
        "endpoint_access": False,
        "claim_boundary": (
            "the color-quantized WHISP figure has no two-sided usable H I support inside "
            "the H-alpha radial range; no same-body channel comparison is identified"
        ),
    }
    (DATA / "ugc08490_hi_halpha_channel_diagnostic_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    REPORT.write_text(
        "# UGC08490 H I-Halpha channel diagnostic v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "The source-frozen 30 arcsec WHISP graphical velocity field was compared with "
        "the two GHASP Halpha sides at 30, 60, and 90 arcsec. Geometry was fixed without "
        "reading a rotation residual.\n\n"
        "The graphical velocity bins do not provide both H I sides inside the Halpha "
        "support. The receding side starts beyond the available Halpha radius after the "
        "frozen deprojection, so no matched two-side statistic is reported.\n\n"
        "This is a preserved negative measurement-path result, not evidence for a Tau Core channel term. "
        "A FITS cube or a published numerical H I rotation table is required before a "
        "kernel-specific comparison can be promoted.\n",
        encoding="utf-8",
    )
    print(result["status"], f"two_side_support={common_two_side_support}")


if __name__ == "__main__":
    main()
