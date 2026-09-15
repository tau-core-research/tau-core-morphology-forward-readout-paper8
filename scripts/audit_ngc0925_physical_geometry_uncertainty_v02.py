#!/usr/bin/env python3
"""Freeze the independent NGC925 geometry errors without endpoint access.

Schmidt et al. (2016) publish the NGC925 inclination and position-angle
profiles as vector paths with vertical error bars derived from a 100-step
residual-rescrambling Monte Carlo.  This script reads only the cached paper
source and the earlier de Blok source-geometry freeze.  It never reads a
HALOGAS image or velocity product.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data/external/literature/ngc0925_schmidt2016_geometry_uncertainty_v01"
SOURCE_TAR = SOURCE_DIR / "arxiv_1601.01689_source.tar.gz"
SOURCE_TEX = SOURCE_DIR / "Radialinflows.tex"
SOURCE_PDF = SOURCE_DIR / "fig19_NGC925.pdf"
SOURCE_SVG = SOURCE_DIR / "fig19_NGC925_pdftocairo_26.04.0.svg"
DEBLOK_CSV = ROOT / "data/derived/ngc0925_signed_descriptor_source_geometry_freeze_v01_points.csv"

OUT_CSV = ROOT / "data/derived/ngc0925_physical_geometry_uncertainty_v02_points.csv"
OUT_COMPARISON = ROOT / "data/derived/ngc0925_physical_geometry_uncertainty_v02_comparison.csv"
OUT_JSON = ROOT / "data/derived/ngc0925_physical_geometry_uncertainty_v02.json"
OUT_SHA = ROOT / "data/derived/ngc0925_physical_geometry_uncertainty_v02.sha256"
REPORT = ROOT / "reports/ngc0925_physical_geometry_uncertainty_v02.md"

EXPECTED_SHA256 = {
    "arxiv_1601.01689_source.tar.gz": "abc5f465b7cbcb21502a7dd1292aaeb5d374ec4a8563e22a96d88cee81e998d4",
    "Radialinflows.tex": "d569ca904c49cd03b00f2aa77fa9828e47dcec35ba935d967784b9ee9af42f5a",
    "fig19_NGC925.pdf": "16b9236c8a05f1e3d9afa19fad415d6c530c999065a2c1f7a85304bd63bf8f8b",
    "fig19_NGC925_pdftocairo_26.04.0.svg": "1ae5bf309eca492c03951876b1c1bde07701ce91e2dc9e1e5be83c06e7959713",
}

# Audited vector-axis anchors in the immutable SVG.  The SVG path coordinates
# precede its y-axis reflection, so numerical values increase with path y.
X0, X1 = 60.480469, 451.246094
R0_ARCSEC, R1_ARCSEC = 0.0, 450.0
I_Y0, I_Y1 = 330.195312, 354.324219
I0_DEG, I1_DEG = 50.0, 55.0
PA_Y0, PA_Y1 = 328.792969, 362.652344
PA0_DEG, PA1_DEG = 270.0, 275.0
RED = "rgb(100%, 0%, 0%)"
GREEN = "rgb(0%, 50.195312%, 0%)"

PATH_RE = re.compile(
    r'<path[^>]*stroke="(?P<colour>rgb\([^"]+\))"[^>]*'
    r'd="M (?P<x1>[0-9.]+) (?P<y1>[0-9.]+) L '
    r'(?P<x2>[0-9.]+) (?P<y2>[0-9.]+)'
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def calibrated(value: float, p0: float, p1: float, v0: float, v1: float) -> float:
    return v0 + (value - p0) * (v1 - v0) / (p1 - p0)


def extract_vertical_bars(svg: str, colour: str, y0: float, y1: float, v0: float, v1: float) -> list[dict]:
    rows = []
    for match in PATH_RE.finditer(svg):
        if match["colour"] != colour:
            continue
        x_a, y_a, x_b, y_b = map(
            float, (match["x1"], match["y1"], match["x2"], match["y2"])
        )
        if abs(x_a - x_b) > 1e-6 or not (X0 < x_a < X1):
            continue
        radius = calibrated(x_a, X0, X1, R0_ARCSEC, R1_ARCSEC)
        # Data centres lie on the source's 27-arcsec grid.  This rejects the
        # legend marker and same-colour paths in the other panels.
        nearest = 27.0 * round(radius / 27.0)
        if not (20.0 < radius < 430.0 and abs(radius - nearest) < 0.01):
            continue
        centre_y = 0.5 * (y_a + y_b)
        value = calibrated(centre_y, y0, y1, v0, v1)
        sigma = abs(calibrated(y_b, y0, y1, v0, v1) - calibrated(y_a, y0, y1, v0, v1)) / 2.0
        rows.append({"radius_arcsec": nearest, "value_deg": value, "sigma_deg": sigma})
    rows.sort(key=lambda row: row["radius_arcsec"])
    assert len(rows) == 15
    assert [row["radius_arcsec"] for row in rows] == [27.0 * i for i in range(1, 16)]
    return rows


def main() -> None:
    for path in (SOURCE_TAR, SOURCE_TEX, SOURCE_PDF, SOURCE_SVG):
        assert sha256(path) == EXPECTED_SHA256[path.name]

    tex = SOURCE_TEX.read_text()
    required_source_statements = [
        "We repeat this procedure 100  times",
        "running up to 2500 iterations and found that 100 is sufficient",
        "keep the ring centres fixed",
        "offsets of the order of 5'' and 10'' are no longer noticeable outside of 100'' and 200''",
        "solid body rotation makes it impossible to disentangle inclination and rotation",
        "inferred disk geometry inside of 250'' may be incorrect",
        "Outside of this radius, however, our fit results should be robust",
    ]
    for statement in required_source_statements:
        assert statement in tex

    svg = SOURCE_SVG.read_text()
    inclination = extract_vertical_bars(svg, RED, I_Y0, I_Y1, I0_DEG, I1_DEG)
    pa = extract_vertical_bars(svg, GREEN, PA_Y0, PA_Y1, PA0_DEG, PA1_DEG)
    assert [row["radius_arcsec"] for row in inclination] == [row["radius_arcsec"] for row in pa]

    rows = []
    for inc, angle in zip(inclination, pa):
        radius = inc["radius_arcsec"]
        rows.append(
            {
                "radius_arcsec": f"{radius:.1f}",
                "inclination_deg": f"{inc['value_deg']:.6f}",
                "inclination_mc_sigma_deg": f"{inc['sigma_deg']:.6f}",
                "position_angle_deg": f"{angle['value_deg']:.6f}",
                "position_angle_mc_sigma_deg": f"{angle['sigma_deg']:.6f}",
                "source_identifiability": "nonidentifiable_solid_body" if radius < 250.0 else "source_claimed_robust_outer",
            }
        )

    with DEBLOK_CSV.open() as handle:
        deblok = list(csv.DictReader(handle))
    deblok_r = np.array([float(row["radius_arcsec"]) for row in deblok])
    deblok_i = np.array([float(row["inclination_deg"]) for row in deblok])
    deblok_pa = np.array([float(row["position_angle_receding_deg"]) for row in deblok])
    deblok_pa_lo = np.array([float(row["position_angle_digitization_p05_deg"]) for row in deblok])
    deblok_pa_hi = np.array([float(row["position_angle_digitization_p95_deg"]) for row in deblok])

    comparisons = []
    for row in rows:
        radius = float(row["radius_arcsec"])
        if radius > deblok_r.max():
            continue
        inc = float(row["inclination_deg"])
        inc_sigma = float(row["inclination_mc_sigma_deg"])
        angle = float(row["position_angle_deg"])
        angle_sigma = float(row["position_angle_mc_sigma_deg"])
        db_i = float(np.interp(radius, deblok_r, deblok_i))
        db_pa = float(np.interp(radius, deblok_r, deblok_pa))
        db_lo = float(np.interp(radius, deblok_r, deblok_pa_lo))
        db_hi = float(np.interp(radius, deblok_r, deblok_pa_hi))
        comparisons.append(
            {
                "radius_arcsec": f"{radius:.1f}",
                "source_identifiability": row["source_identifiability"],
                "deblok_inclination_deg": f"{db_i:.6f}",
                "schmidt_inclination_deg": f"{inc:.6f}",
                "inclination_abs_gap_deg": f"{abs(db_i-inc):.6f}",
                "inclination_gap_over_schmidt_mc_sigma": f"{abs(db_i-inc)/inc_sigma:.6f}",
                "deblok_pa_deg": f"{db_pa:.6f}",
                "deblok_pa_digitization_p05_deg": f"{db_lo:.6f}",
                "deblok_pa_digitization_p95_deg": f"{db_hi:.6f}",
                "schmidt_pa_deg": f"{angle:.6f}",
                "pa_abs_gap_deg": f"{abs(db_pa-angle):.6f}",
                "pa_gap_over_schmidt_mc_sigma": f"{abs(db_pa-angle)/angle_sigma:.6f}",
                "one_sigma_pa_intervals_overlap": str(not (angle + angle_sigma < db_lo or angle - angle_sigma > db_hi)).lower(),
            }
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with OUT_COMPARISON.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(comparisons[0]))
        writer.writeheader()
        writer.writerows(comparisons)

    outer = [row for row in comparisons if row["source_identifiability"] == "source_claimed_robust_outer"]
    assert len(outer) == 1 and float(outer[0]["radius_arcsec"]) == 270.0
    payload = {
        "status": "PHYSICAL_MC_ACQUIRED_GEOMETRY_IDENTIFIABILITY_FAIL_ENDPOINT_BLOCKED",
        "galaxy": "NGC0925",
        "source": {
            "citation": "Schmidt et al. 2016, MNRAS 457, 2642, Figure 19 and Sections 3.4, 4.1, 5.10",
            "arxiv": "1601.01689",
            "sha256": EXPECTED_SHA256,
            "svg_derivation": "pdftocairo 26.04.0 -svg; byte-identical regeneration verified locally from the cached vector PDF",
        },
        "uncertainty_model": {
            "kind": "source-published residual-rescrambling Monte Carlo marginal standard deviations",
            "iterations": 100,
            "convergence_check_max_iterations": 2500,
            "cross_ring_covariance_published": False,
            "joint_inclination_pa_covariance_published": False,
        },
        "geometry": {
            "ring_count": len(rows),
            "ring_centres_arcsec": [float(row["radius_arcsec"]) for row in rows],
            "ring_width_arcsec": 43.2,
            "centre_treatment": "fixed after an inner-disk fit; source-specific centre covariance and alternative-centre weights are not published",
            "generic_centre_sensitivity": "5-arcsec and 10-arcsec offsets become unnoticeable beyond about 100 and 200 arcsec in the authors' tests",
        },
        "identifiability": {
            "inner_boundary_arcsec": 250.0,
            "inner_verdict": "source-declared inclination/rotation non-identifiability under nearly solid-body rotation",
            "outer_verdict": "authors state their fit should be robust outside 250 arcsec",
            "overlap_with_deblok_max_arcsec": float(deblok_r.max()),
            "outer_robust_independent_comparison_ring_count": len(outer),
        },
        "cross_source_comparison": {
            "purpose": "pre-endpoint nuisance compatibility audit, not a global significance test",
            "outer_270_arcsec_inclination_gap_deg": float(outer[0]["inclination_abs_gap_deg"]),
            "outer_270_arcsec_inclination_gap_over_schmidt_mc_sigma": float(outer[0]["inclination_gap_over_schmidt_mc_sigma"]),
            "outer_270_arcsec_pa_gap_deg": float(outer[0]["pa_abs_gap_deg"]),
            "outer_270_arcsec_pa_gap_over_schmidt_mc_sigma": float(outer[0]["pa_gap_over_schmidt_mc_sigma"]),
            "outer_270_arcsec_one_sigma_pa_intervals_overlap": outer[0]["one_sigma_pa_intervals_overlap"] == "true",
            "interpretation": "The normalized gaps divide only by Schmidt marginal MC errors; de Blok physical covariance and cross-source systematics are unavailable, so they are diagnostics rather than cross-source significances.",
        },
        "endpoint_pixels_read": False,
        "endpoint_allowed": False,
        "next_decision": "Test a prospectively frozen R>=250 arcsec outer-only descriptor for source/beam support; otherwise demote NGC925 and advance to the next unopened candidate.",
        "remaining_blockers": [
            "a cross-source-compatible geometry law or a source-justified outer-only restriction",
            "source-specific centre alternatives and weights",
            "cross-ring and joint inclination/position-angle covariance or a conservative nuisance construction",
            "HALOGAS beam blocks, common-footprint mask, solver tolerance, and wrong-family controls",
        ],
        "claim_boundary": "This audit acquires physical marginal MC errors and proves a source-side identifiability failure for the inner geometry. It is not an endpoint score, a global covariance, a Tau q_R selection, parent-morphology evidence, Nature occupation, or dark-matter-replacement evidence.",
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n")

    digest_lines = []
    for path in (OUT_CSV, OUT_COMPARISON, OUT_JSON):
        digest_lines.append(f"{sha256(path)}  {path.relative_to(ROOT)}")
    OUT_SHA.write_text("\n".join(digest_lines) + "\n")

    REPORT.write_text(
        "# NGC925 physical geometry-uncertainty audit v02\n\n"
        f"Status: `{payload['status']}`.\n\n"
        "Schmidt et al. (2016) supply an independent THINGS tilted-ring analysis. Its Figure 19 "
        "is vector-valued, so the 15 inclination and 15 position-angle points and their vertical "
        "error bars are extracted from exact paths rather than raster pixels. The error bars are "
        "physical marginal standard deviations from 100 residual-rescrambling Monte Carlo fits; "
        "the authors checked convergence with runs as long as 2500 iterations. Cross-ring and joint "
        "inclination/position-angle covariance were not published.\n\n"
        "The source itself declares the geometry inside 250 arcsec non-identifiable because the "
        "nearly solid-body rotation does not separate inclination from rotation speed. Consequently "
        "the inner error bars cannot repair or validate the earlier de Blok descriptor. Only the "
        "270-arcsec Schmidt ring lies both in the source-claimed robust outer region and within the "
        "15--291 arcsec de Blok extraction. There the inclination gap is "
        f"`{float(outer[0]['inclination_abs_gap_deg']):.3f} deg` "
        f"(`{float(outer[0]['inclination_gap_over_schmidt_mc_sigma']):.2f}` Schmidt marginal MC sigmas), "
        f"and the PA gap is `{float(outer[0]['pa_abs_gap_deg']):.3f} deg` "
        f"(`{float(outer[0]['pa_gap_over_schmidt_mc_sigma']):.2f}` such sigmas); the respective PA "
        "one-sigma intervals do not overlap. These ratios are not cross-source significances because "
        "the de Blok physical covariance and cross-source systematics are unavailable.\n\n"
        "The correct preflight verdict is therefore not 'uncertainty closed'. NGC925 remains endpoint-"
        "blocked pending a prospectively frozen outer-only support test or demotion to a nonconfirmatory "
        "case. The paper's generic 5/10-arcsec centre-offset tests inform sensitivity bounds but do not "
        "supply source-specific centre alternatives or weights. No HALOGAS endpoint pixel is read.\n"
    )
    print("NGC0925_PHYSICAL_GEOMETRY_UNCERTAINTY_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
