#!/usr/bin/env python3
"""Build printed-axis radial transport for the UGC08490 WHISP panel."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
RA_ANCHORS = [(566.0, 28 * 60 + 20.0), (615.5, 27 * 60 + 30.0), (664.5, 26 * 60 + 40.0)]
DEC_ANCHORS = [(546.5, 45.0), (603.5, 40.0), (660.5, 35.0)]


def fit(points):
    x = [p[0] for p in points]; y = [p[1] for p in points]
    xm = sum(x) / len(x); ym = sum(y) / len(y)
    slope = sum((a-xm)*(b-ym) for a,b in zip(x,y)) / sum((a-xm)**2 for a in x)
    intercept = ym - slope*xm
    return slope, intercept, max(abs(slope*a+intercept-b) for a,b in points)


def percentile(values, q):
    return float(pd.Series(values).quantile(q))


def main() -> None:
    pixels = pd.read_csv(DATA / "ugc08490_whisp_60arcsec_velocity_pixels_v01.csv")
    candidates = pd.read_csv(DATA / "ghasp_sparc_source_only_candidate_federation_v01.csv")
    ghasp_max = float(candidates.loc[candidates.galaxy.eq("UGC08490"), "halpha_max_radius_arcsec"].iloc[0])
    ra_slope, ra_intercept, ra_residual = fit(RA_ANCHORS)
    dec_slope, dec_intercept, dec_residual = fit(DEC_ANCHORS)

    def centroid(relation):
        sub = pixels.loc[pixels.systemic_relation.eq(relation)]
        return float(sub.source_x.mean()), float(sub.source_y.mean())
    systemic = centroid("systemic_ambiguous")
    approaching = centroid("approaching"); receding = centroid("receding")
    midpoint = ((approaching[0]+receding[0])/2, (approaching[1]+receding[1])/2)

    def radii(center):
        center_ra = ra_slope*center[0]+ra_intercept
        center_dec = dec_slope*center[1]+dec_intercept
        dra = (ra_slope*pixels.source_x+ra_intercept-center_ra)*15*math.cos(math.radians(58+center_dec/60))
        ddec = (dec_slope*pixels.source_y+dec_intercept-center_dec)*60
        return (dra**2+ddec**2)**0.5
    summaries = {}
    for name, center in (("systemic_color_centroid", systemic), ("side_centroid_midpoint", midpoint)):
        radius = radii(center)
        summaries[name] = {"center_source_pixels": list(center), "p50_arcsec": percentile(radius,.5),
                           "p95_arcsec": percentile(radius,.95), "max_arcsec": float(radius.max())}
    result = {
        "schema": "ugc08490_whisp_angular_axis_preflight_v01",
        "status": "WHISP_UGC08490_PRINTED_AXIS_PROXY_READY_COMMON_SUPPORT_PRESENT",
        "axis_epoch": "B1950_as_printed", "ra_tick_anchors": RA_ANCHORS,
        "dec_tick_anchors": DEC_ANCHORS, "anchor_pixel_uncertainty": 1.0,
        "ra_seconds_of_time_per_pixel": ra_slope, "dec_arcmin_per_pixel": dec_slope,
        "ra_anchor_max_residual_seconds": ra_residual, "dec_anchor_max_residual_arcmin": dec_residual,
        "center_proxy_radius_summary": summaries, "ghasp_max_radius_arcsec": ghasp_max,
        "ghasp_support_inside_both_hi_proxy_maxima": all(ghasp_max <= x["max_arcsec"] for x in summaries.values()),
        "formal_wcs_ready": False, "center_source_frozen": False,
        "beam_covariance_ready": False, "common_hi_halpha_radial_transport_ready": False,
        "kernel_measurement_allowed": False, "endpoint_access": False,
        "claim_boundary": (
            "printed-axis and two-center source proxy only; formal center, deprojection, beam "
            "covariance and common radial bin freeze remain open"
        ),
    }
    (DATA / "ugc08490_whisp_angular_axis_preflight_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
