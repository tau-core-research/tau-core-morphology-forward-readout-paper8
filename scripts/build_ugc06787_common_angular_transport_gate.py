#!/usr/bin/env python3
"""Audit distance conventions and freeze the UGC06787 angular transport rule."""

from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
ARCSEC_PER_RADIAN = 206265.0


def kpc_per_arcsec(distance_mpc: float) -> float:
    return distance_mpc * 1000.0 / ARCSEC_PER_RADIAN


def implied_distance_mpc(kpc_per_arcsec_value: float) -> float:
    return kpc_per_arcsec_value * ARCSEC_PER_RADIAN / 1000.0


def main() -> None:
    with (DATA / "ghasp_sparc_side_rotation_points_v01.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        points = [row for row in csv.DictReader(handle) if row["galaxy"] == "UGC06787"]
    with (DATA / "external_sparc_master_table.csv").open(newline="", encoding="utf-8") as handle:
        sparc = next(row for row in csv.DictReader(handle) if row["Galaxy"] == "UGC06787")
    whisp = json.loads((DATA / "ugc06787_whisp_hi_source_v01.json").read_text())

    ghasp_pairs = [
        (float(row["radius_kpc"]), float(row["radius_arcsec"]))
        for row in points
        if float(row["radius_kpc"]) > 0 and float(row["radius_arcsec"]) > 0
    ]
    if not ghasp_pairs:
        raise RuntimeError("UGC06787 GHASP angular radii unavailable")

    ratios = [radius_kpc / radius_arcsec for radius_kpc, radius_arcsec in ghasp_pairs]
    ghasp_scale = statistics.median(ratios)
    ghasp_distance = implied_distance_mpc(ghasp_scale)
    sparc_distance = float(sparc["D_Mpc"])
    # The WHISP overview prints 16 Mpc; this value is source-visible and frozen.
    whisp_distance = 16.0
    max_ghasp_arcsec = max(radius_arcsec for _, radius_arcsec in ghasp_pairs)
    result = {
        "schema": "ugc06787_common_angular_transport_gate_v01",
        "status": "UGC06787_ANGULAR_FIRST_TRANSPORT_RULE_FROZEN_WORLD_AXIS_CALIBRATION_OPEN",
        "galaxy": "UGC06787",
        "n_ghasp_points": len(points),
        "ghasp_native_max_radius_arcsec": max_ghasp_arcsec,
        "ghasp_median_kpc_per_arcsec": ghasp_scale,
        "ghasp_implied_distance_mpc": ghasp_distance,
        "whisp_printed_distance_mpc": whisp_distance,
        "sparc_distance_mpc": sparc_distance,
        "kpc_per_arcsec": {
            "ghasp_implied": ghasp_scale,
            "whisp_16_mpc": kpc_per_arcsec(whisp_distance),
            "sparc_21p3_mpc": kpc_per_arcsec(sparc_distance),
        },
        "distance_spread_max_over_min": max(ghasp_distance, whisp_distance, sparc_distance)
        / min(ghasp_distance, whisp_distance, sparc_distance),
        "transport_rule": "compare GHASP native angular radius r2 to WHISP source-figure angular axes before choosing one physical distance conversion",
        "kpc_transport_allowed": False,
        "whisp_world_axis_calibration_ready": False,
        "common_hi_halpha_angular_transport_ready": False,
        "physical_a_row_constructed": False,
        "endpoint_access": False,
        "claim_boundary": "source-side scale audit only; no residual access, no calibrated WHISP WCS, no common beam/radial operator, and no channel test",
    }
    (DATA / "ugc06787_common_angular_transport_gate_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    (REPORTS / "ugc06787_common_angular_transport_gate_v01.md").write_text(
        f"""# UGC06787 Common Angular Transport Gate v0.1

**Status:** `{result['status']}`

Three source packets use materially different physical-distance conventions:

| source | distance or implied distance | kpc/arcsec |
| --- | ---: | ---: |
| GHASP native `r/r2` median | {ghasp_distance:.3f} Mpc | {ghasp_scale:.6f} |
| WHISP overview | {whisp_distance:.3f} Mpc | {kpc_per_arcsec(whisp_distance):.6f} |
| SPARC master | {sparc_distance:.3f} Mpc | {kpc_per_arcsec(sparc_distance):.6f} |

The largest distance is `{result['distance_spread_max_over_min']:.3f}` times
the smallest. A direct kpc merge would therefore create a scale mismatch that
could masquerade as a radial channel effect.

The transport rule is frozen as:

```text
GHASP native angular radius r2
<-> WHISP source-figure angular axes
first;

one declared distance conversion
only after angular support and geometry agree.
```

GHASP reaches `{max_ghasp_arcsec:.1f}` arcsec on its available approaching
side. The WHISP graphical panel still needs an explicit source-axis pixel to
sky calibration before common angular overlap can be computed.

No endpoint residual was opened. No physical `A_p` row is constructed.
""",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
