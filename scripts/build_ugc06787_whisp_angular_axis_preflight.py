#!/usr/bin/env python3
"""Build a source-figure angular-axis proxy for the UGC06787 WHISP panel."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

# Major tick anchors read from the frozen WHISP source figure (B1950 axes).
RA_ANCHORS = [(566.0, 47 * 60 + 30.0), (615.5, 46 * 60 + 40.0), (664.5, 45 * 60 + 50.0)]
DEC_ANCHORS = [(546.5, 32.0), (603.5, 24.0), (660.5, 16.0)]
ANCHOR_PIXEL_UNCERTAINTY = 1.0


def fit_line(points: list[tuple[float, float]]) -> tuple[float, float, float]:
    x_mean = sum(x for x, _ in points) / len(points)
    y_mean = sum(y for _, y in points) / len(points)
    slope = sum((x - x_mean) * (y - y_mean) for x, y in points) / sum(
        (x - x_mean) ** 2 for x, _ in points
    )
    intercept = y_mean - slope * x_mean
    max_residual = max(abs((slope * x + intercept) - y) for x, y in points)
    return slope, intercept, max_residual


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round(fraction * (len(ordered) - 1))))
    return ordered[index]


def main() -> None:
    with (DATA / "ugc06787_whisp_60arcsec_velocity_pixels_v01.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle))
    angular_gate = json.loads(
        (DATA / "ugc06787_common_angular_transport_gate_v01.json").read_text()
    )

    ra_slope, ra_intercept, ra_residual = fit_line(RA_ANCHORS)
    dec_slope, dec_intercept, dec_residual = fit_line(DEC_ANCHORS)
    systemic_rows = [row for row in rows if row["systemic_relation"] == "systemic_ambiguous"]
    approaching_rows = [row for row in rows if row["systemic_relation"] == "approaching"]
    receding_rows = [row for row in rows if row["systemic_relation"] == "receding"]

    def mean_source(items: list[dict[str, str]]) -> tuple[float, float]:
        return (
            sum(float(row["source_x"]) for row in items) / len(items),
            sum(float(row["source_y"]) for row in items) / len(items),
        )

    systemic_center = mean_source(systemic_rows)
    approaching_center = mean_source(approaching_rows)
    receding_center = mean_source(receding_rows)
    side_midpoint = (
        0.5 * (approaching_center[0] + receding_center[0]),
        0.5 * (approaching_center[1] + receding_center[1]),
    )

    def angular_radius(row: dict[str, str], center: tuple[float, float]) -> float:
        x = float(row["source_x"])
        y = float(row["source_y"])
        center_ra_seconds = ra_slope * center[0] + ra_intercept
        center_dec_minutes = dec_slope * center[1] + dec_intercept
        ra_seconds = ra_slope * x + ra_intercept
        dec_minutes = dec_slope * y + dec_intercept
        projected_ra_arcsec = (ra_seconds - center_ra_seconds) * 15.0 * math.cos(
            math.radians(56.0 + center_dec_minutes / 60.0)
        )
        dec_arcsec = (dec_minutes - center_dec_minutes) * 60.0
        return math.hypot(projected_ra_arcsec, dec_arcsec)

    radius_sets = {
        "systemic_color_centroid": [angular_radius(row, systemic_center) for row in rows],
        "approaching_receding_centroid_midpoint": [angular_radius(row, side_midpoint) for row in rows],
    }
    radius_summary = {
        name: {
            "p50_arcsec": percentile(values, 0.50),
            "p95_arcsec": percentile(values, 0.95),
            "max_arcsec": max(values),
        }
        for name, values in radius_sets.items()
    }
    ghasp_max = float(angular_gate["ghasp_native_max_radius_arcsec"])
    result = {
        "schema": "ugc06787_whisp_angular_axis_preflight_v01",
        "status": "WHISP_UGC06787_SOURCE_AXIS_PROXY_CALIBRATED_CENTER_AND_WCS_OPEN",
        "axis_epoch": "B1950_as_printed",
        "ra_tick_anchors": RA_ANCHORS,
        "dec_tick_anchors": DEC_ANCHORS,
        "anchor_pixel_uncertainty": ANCHOR_PIXEL_UNCERTAINTY,
        "ra_seconds_of_hour_per_pixel": ra_slope,
        "dec_arcmin_per_pixel": dec_slope,
        "ra_anchor_max_residual_seconds_of_time": ra_residual,
        "dec_anchor_max_residual_arcmin": dec_residual,
        "center_proxies_source_pixels": {
            "systemic_color_centroid": list(systemic_center),
            "approaching_receding_centroid_midpoint": list(side_midpoint),
        },
        "radius_summary": radius_summary,
        "ghasp_max_radius_arcsec": ghasp_max,
        "ghasp_support_inside_both_hi_proxy_maxima": all(
            ghasp_max <= summary["max_arcsec"] for summary in radius_summary.values()
        ),
        "source_axis_proxy_ready": True,
        "formal_wcs_ready": False,
        "center_source_frozen": False,
        "beam_covariance_ready": False,
        "common_hi_halpha_angular_transport_ready": False,
        "physical_a_row_constructed": False,
        "endpoint_access": False,
        "claim_boundary": "manual printed-axis proxy with +/-1 pixel anchor uncertainty and two center proxies; not a FITS WCS, source-frozen center, beam-covariant radial map, or physical probe operator",
    }
    (DATA / "ugc06787_whisp_angular_axis_preflight_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    (REPORTS / "ugc06787_whisp_angular_axis_preflight_v01.md").write_text(
        f"""# UGC06787 WHISP Angular-Axis Preflight v0.1

**Status:** `{result['status']}`

Three printed B1950 major ticks on each axis were frozen with `+/-1` source
pixel reading uncertainty. Linear fits give:

```text
RA scale:  {ra_slope:.6f} seconds-of-time / pixel
Dec scale: {dec_slope:.6f} arcmin / pixel
```

The source graphic does not provide a machine-readable center. Two independent
source-only center proxies were therefore retained rather than choosing one
post hoc:

| center proxy | H I p50 radius | H I p95 radius | H I max radius |
| --- | ---: | ---: | ---: |
| systemic-color centroid | {radius_summary['systemic_color_centroid']['p50_arcsec']:.2f} | {radius_summary['systemic_color_centroid']['p95_arcsec']:.2f} | {radius_summary['systemic_color_centroid']['max_arcsec']:.2f} |
| approaching/receding midpoint | {radius_summary['approaching_receding_centroid_midpoint']['p50_arcsec']:.2f} | {radius_summary['approaching_receding_centroid_midpoint']['p95_arcsec']:.2f} | {radius_summary['approaching_receding_centroid_midpoint']['max_arcsec']:.2f} |

The GHASP approaching-side support reaches `{ghasp_max:.1f}` arcsec and lies
inside both graphical H I maximum-radius estimates. This establishes possible
angular support overlap, not a pointwise common radial transport.

Formal WCS, a source-frozen galaxy center, beam covariance, and the mapping of
GHASP approaching-side radii onto the WHISP side remain open. No endpoint
residual was opened and no physical `A_p` row is constructed.
""",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
