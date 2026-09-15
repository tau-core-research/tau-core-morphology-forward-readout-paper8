#!/usr/bin/env python3
"""Audit an outer-only NGC925 route using source information only."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HEALD = ROOT / "data/external/literature/halogas_dr1_confirmatory_pool_v01/heald2011_15938.tex"
GEOMETRY = ROOT / "data/derived/ngc0925_physical_geometry_uncertainty_v02_points.csv"
GEOMETRY_AUDIT = ROOT / "data/derived/ngc0925_physical_geometry_uncertainty_v02.json"
OUT_CSV = ROOT / "data/derived/ngc0925_outer_only_source_support_v01.csv"
OUT_JSON = ROOT / "data/derived/ngc0925_outer_only_source_support_v01.json"
OUT_SHA = ROOT / "data/derived/ngc0925_outer_only_source_support_v01.sha256"
REPORT = ROOT / "reports/ngc0925_outer_only_source_support_v01.md"

EXPECTED_HEALD_SHA256 = "6985ce18fd7978f16a921a3b7df6444ab0fc66c02dacb359a780d0d221d53017"
BEAMS = {
    "uniform": (22.2, 12.6),
    "robust_0": (25.3, 13.9),
    "30_arcsec_taper": (37.9, 33.2),
}
MIN_BEAM_AREAS_PER_SIDE_CELL = 2.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assert sha256(HEALD) == EXPECTED_HEALD_SHA256
    text = HEALD.read_text()
    assert "NGC~925  & uniform             & $22.2\\times12.6$" in text
    assert "complicated stream of gas stripped during a minor merger" in text
    assert "twisting of the isovelocity contours" in text
    assert "A large amount of anomalous \\HI\\ emission is clearly visible" in text

    audit = json.loads(GEOMETRY_AUDIT.read_text())
    assert audit["endpoint_pixels_read"] is False
    with GEOMETRY.open() as handle:
        geometry = [row for row in csv.DictReader(handle) if float(row["radius_arcsec"]) >= 250.0]
    assert [float(row["radius_arcsec"]) for row in geometry] == [270.0, 297.0, 324.0, 351.0, 378.0, 405.0]

    rows = []
    for row in geometry:
        radius = float(row["radius_arcsec"])
        inclination = float(row["inclination_deg"])
        width = 43.2
        projected_half_annulus = math.pi * radius * width * math.cos(math.radians(inclination))
        for weighting, (major, minor) in BEAMS.items():
            beam_area = math.pi * major * minor / (4.0 * math.log(2.0))
            capacity = projected_half_annulus / beam_area
            rows.append(
                {
                    "radius_arcsec": f"{radius:.1f}",
                    "inclination_deg": f"{inclination:.6f}",
                    "beam_weighting": weighting,
                    "beam_major_arcsec": f"{major:.1f}",
                    "beam_minor_arcsec": f"{minor:.1f}",
                    "full_projected_half_annulus_beam_areas": f"{capacity:.6f}",
                    "maximum_mask_loss_fraction_before_two_beam_failure": f"{1.0-MIN_BEAM_AREAS_PER_SIDE_CELL/capacity:.6f}",
                }
            )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    minimum_capacity = min(float(row["full_projected_half_annulus_beam_areas"]) for row in rows)
    summary = {
        "status": "OUTER_GEOMETRIC_CAPACITY_PASS_TERMINAL_CLEANLINESS_FAIL_ENDPOINT_BLOCKED",
        "galaxy": "NGC0925",
        "prospective_radial_rule": "use only published Schmidt ring centres R>=250 arcsec; first retained centre is 270 arcsec",
        "retained_ring_count": len(geometry),
        "retained_radii_arcsec": [float(row["radius_arcsec"]) for row in geometry],
        "published_beam_scenarios_arcsec": BEAMS,
        "minimum_full_half_annulus_capacity_beam_areas": minimum_capacity,
        "geometric_capacity_gate": "passes before masking for all three published pilot-cube beams",
        "mask_occupancy_gate": "not testable without endpoint pixels; the full-area calculation is only an upper capacity bound",
        "terminal_cleanliness_gate": "fails the current source-only readiness test because the same outer disk is source-described as a minor-merger stream with twisted isovelocity contours, warp/spiral ambiguity, and anomalous HI",
        "signed_pa_gate": "open; Schmidt defines a sky-plane major-axis PA and rotation sense but the cached text does not explicitly state which PA ray is receding",
        "disposition": "demote from first clean confirmatory acquisition target; retain only as a preregistered disturbed-system robustness or stronger-terminal case",
        "next_source_target": "NGC4062",
        "endpoint_pixels_read": False,
        "endpoint_allowed": False,
        "claim_boundary": "The outer annuli have adequate ideal geometric beam capacity, but this neither certifies masked support nor removes known standard-physics terminal contamination. No Tau or parent-morphology inference follows.",
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n")
    OUT_SHA.write_text(
        "\n".join(f"{sha256(path)}  {path.relative_to(ROOT)}" for path in (OUT_CSV, OUT_JSON)) + "\n"
    )
    REPORT.write_text(
        "# NGC925 outer-only source-support audit v01\n\n"
        f"Status: `{summary['status']}`.\n\n"
        "The source-authored identifiability boundary leaves six Schmidt ring centres from 270 to "
        "405 arcsec. Their ideal projected half-annulus capacity is at least "
        f"`{minimum_capacity:.2f}` synthesized-beam areas even under the broadest published 30-arcsec-"
        "taper beam, so an outer-only route is not geometrically impossible before masking. This is "
        "an upper capacity bound, not a masked-cell pass.\n\n"
        "The route nevertheless fails the current clean-terminal source gate. Heald et al. describe "
        "the same outer disk as a complicated minor-merger gas stream, with twisted isovelocity contours, "
        "warp/spiral ambiguity, and substantial anomalous HI. A moment-1 side-consistency score could "
        "therefore absorb standard disturbed-gas kinematics. NGC925 is demoted from the first clean "
        "confirmatory acquisition target and retained only for a prospectively defined disturbed-system "
        "robustness stratum or a stronger velocity-cube terminal. NGC4062 becomes the next source target. "
        "No HALOGAS endpoint pixel was read.\n"
    )
    print("NGC0925_OUTER_ONLY_SOURCE_SUPPORT_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
