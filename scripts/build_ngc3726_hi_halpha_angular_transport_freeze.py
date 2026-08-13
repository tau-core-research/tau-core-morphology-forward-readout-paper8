#!/usr/bin/env python3
"""Freeze residual-blind NGC3726 H I-Halpha angular transport and statistic."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
HI_POINTS = DATA / "ngc3726_uma_hi_side_rotation_points_v01.csv"
HALPHA_POINTS = DATA / "ghasp_full_federation_side_points_v01.csv"
SOURCE = DATA / "ngc3726_uma_hi_rotation_source_v01.json"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bracket(radii: list[float], target: float) -> tuple[float, float, float, float]:
    lower = max(radius for radius in radii if radius <= target)
    upper = min(radius for radius in radii if radius >= target)
    if lower == upper:
        return lower, upper, 1.0, 0.0
    upper_weight = (target - lower) / (upper - lower)
    return lower, upper, 1.0 - upper_weight, upper_weight


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    if source["status"] != "NGC3726_SOURCE_NATIVE_HI_SIDE_ROTATION_ACQUIRED_GEOMETRY_COMPATIBLE":
        raise RuntimeError("NGC3726 H I geometry source gate is not passed")
    hi = list(csv.DictReader(HI_POINTS.open(newline="", encoding="utf-8")))
    halpha = [
        row
        for row in csv.DictReader(HALPHA_POINTS.open(newline="", encoding="utf-8"))
        if row["sparc_match"] == "NGC3726"
    ]
    radii_by_side = {
        side: sorted(float(row["radius_arcsec"]) for row in halpha if row["side"] == side)
        for side in ("a", "r")
    }
    halpha_max = min(max(radii_by_side["a"]), max(radii_by_side["r"]))
    common_hi = [
        row
        for row in hi
        if float(row["radius_arcsec"]) <= halpha_max
    ]
    freeze_rows = []
    for row in common_hi:
        target = float(row["radius_arcsec"])
        a0, a1, aw0, aw1 = bracket(radii_by_side["a"], target)
        r0, r1, rw0, rw1 = bracket(radii_by_side["r"], target)
        freeze_rows.append(
            {
                "radius_arcsec": target,
                "hi_inclination_deg": float(row["inclination_deg"]),
                "hi_receding_pa_deg": float(row["receding_pa_deg"]),
                "halpha_approaching_lower_radius_arcsec": a0,
                "halpha_approaching_upper_radius_arcsec": a1,
                "halpha_approaching_lower_weight": aw0,
                "halpha_approaching_upper_weight": aw1,
                "halpha_receding_lower_radius_arcsec": r0,
                "halpha_receding_upper_radius_arcsec": r1,
                "halpha_receding_lower_weight": rw0,
                "halpha_receding_upper_weight": rw1,
                "endpoint_access": False,
            }
        )
    if [row["radius_arcsec"] for row in freeze_rows] != [40.0, 60.0, 80.0, 100.0, 120.0, 140.0]:
        raise RuntimeError("Unexpected NGC3726 common angular support")

    path = DATA / "ngc3726_hi_halpha_angular_transport_freeze_v01.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(freeze_rows[0]))
        writer.writeheader()
        writer.writerows(freeze_rows)
    metadata = source["metadata"]
    result = {
        "schema": "ngc3726_hi_halpha_angular_transport_freeze_v01",
        "status": "NGC3726_HI_HALPHA_ANGULAR_TRANSPORT_AND_ODD_CONTRAST_FROZEN",
        "galaxy": "NGC3726",
        "construction_blind_to": [
            "SPARC vobs and rotation residuals",
            "H I-Halpha velocity differences",
            "baseline model scores",
            "required Tau channel amplitudes",
        ],
        "input_sha256": {
            "hi_points": file_hash(HI_POINTS),
            "halpha_points": file_hash(HALPHA_POINTS),
            "geometry_source": file_hash(SOURCE),
        },
        "common_radius_unit": "arcsec",
        "common_radii_arcsec": [row["radius_arcsec"] for row in freeze_rows],
        "n_common_radii": len(freeze_rows),
        "halpha_interpolation": "side-separate linear interpolation in angular radius using frozen brackets and weights",
        "projection_rule": "u_tracer_side(R)=Vrot_tracer_side(R)*sin(inclination_tracer(R))",
        "halpha_inclination_deg": metadata["ghasp_kinematic_inclination_deg"],
        "halpha_inclination_error_deg": metadata["ghasp_kinematic_inclination_error_deg"],
        "hi_inclination_error_deg_inner": metadata["hi_adopted_inclination_error_deg"],
        "odd_statistic": "O_tracer(R)=u_receding(R)-u_approaching(R)",
        "even_statistic": "E_tracer(R)=[u_receding(R)+u_approaching(R)]/2",
        "primary_channel_contrast": "Delta_O(R)=O_Halpha(R)-O_HI(R)",
        "secondary_tracer_offset": "Delta_E(R)=E_Halpha(R)-E_HI(R)",
        "uncertainty_rule": "symmetrize quoted side errors; interpolate in quadrature; propagate shared inclination error analytically; combine tracer errors in quadrature",
        "primary_null": "Delta_O(R)=0 on common support within propagated uncertainty",
        "selection_uses_vobs_or_residual": False,
        "velocity_values_opened_during_freeze": False,
        "endpoint_access": False,
        "physical_a_row_constructed": False,
        "claim_boundary": "predeclared two-tracer angular statistic only; any nonzero result remains compatible with conventional tracer, geometry, beam, and non-circular-motion systematics",
    }
    (DATA / "ngc3726_hi_halpha_angular_transport_freeze_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    (REPORTS / "ngc3726_hi_halpha_angular_transport_freeze_v01.md").write_text(
        f"""# NGC3726 H I-Halpha Angular Transport Freeze v0.1

**Status:** `{result['status']}`

Six H I radii (`40, 60, 80, 100, 120, 140 arcsec`) lie inside the two-sided
GHASP Halpha support. Separate approaching and receding interpolation brackets
and weights are frozen before tracer velocity differences are evaluated.

The comparison returns both published deprojected curves to line-of-sight
equivalents, `u=Vrot sin(i)`. The primary statistic is the cross-tracer
side-odd contrast

```text
Delta_O = (u_rec-u_app)_Halpha - (u_rec-u_app)_HI.
```

The secondary statistic compares side-even means. Quoted measurement errors
and shared inclination uncertainties are propagated. SPARC `vobs`, rotation
residuals, baseline scores, and required Tau amplitudes are not read by this
freeze.

A nonzero `Delta_O` will be a two-tracer discrepancy diagnostic, not by itself
an observer-channel detection. Beam smearing, gas-phase structure,
non-circular motion, center choice, and remaining geometry differences stay
as conventional alternatives.
""",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
