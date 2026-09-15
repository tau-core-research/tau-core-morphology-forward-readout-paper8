#!/usr/bin/env python3
"""Digitize the source-published NGC925 adopted geometry without endpoint access.

The source figure is a JPEG embedded as ASCIIHex/DCT data in the cached EPS.
This script extracts that immutable raster in memory, traces the thick adopted
inclination and PA curves, and keeps raster/calibration uncertainty distinct
from the unpublished physical tilted-ring covariance.  The table value
``i=66 deg`` is a summary value, not a constant radial model.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data/external/literature/ngc0925_signed_geometry_source_v01"
EPS = SOURCE_DIR / "deblok2008_figuur68_ngc925.ps"
TEX = SOURCE_DIR / "deblok2008_deblok_astroph.tex"
OUT_CSV = ROOT / "data/derived/ngc0925_signed_descriptor_source_geometry_freeze_v01_points.csv"
OUT_JSON = ROOT / "data/derived/ngc0925_signed_descriptor_source_geometry_freeze_v01.json"
OUT_SHA = ROOT / "data/derived/ngc0925_signed_descriptor_source_geometry_freeze_v01.sha256"
REPORT = ROOT / "reports/ngc0925_signed_descriptor_source_geometry_freeze_v01.md"

EXPECTED_EPS_SHA256 = "ed3b8e197e523531b5b9e77c9a58f8f7a5e275c4cc3f30ff773977e64fa0b2a0"
EXPECTED_TEX_SHA256 = "6c76c8d95dc671727370a44d7e040fa17e752971f2ad8c8b053438b998caa199"

# Pixel anchors audited on the immutable 561 x 756 JPEG, not on a rescaled render.
R_X0, R_X1 = 309, 510
R0_ARCSEC, R1_ARCSEC = 0.0, 300.0
PA_PANEL_Y0, PA_PANEL_Y1 = 627, 698
PA_TICK_Y0, PA_TICK_Y1 = 647, 688
PA0_DEG, PA1_DEG = 300.0, 260.0
I_PANEL_Y0, I_PANEL_Y1 = 557, 627
I_TICK_Y0, I_TICK_Y1 = 565, 619
I0_DEG, I1_DEG = 80.0, 20.0
TRACE_X_MARGIN_LEFT, TRACE_X_MARGIN_RIGHT = 6, 5
TRACE_Y_MARGIN_TOP, TRACE_Y_MARGIN_BOTTOM = 6, 5
NOMINAL_SMOOTHNESS = 10.0
RING_RADII_ARCSEC = np.arange(15.0, 292.0, 3.0)


def sha256_bytes(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def extract_embedded_jpeg(eps_bytes: bytes) -> bytes:
    text = eps_bytes.decode("ascii")
    start = text.index("FFD8")
    stop = text.rindex("FFD9>") + 4
    return bytes.fromhex("".join(text[start:stop].split()))


def trace_dark_continuous_curve(
    image: np.ndarray,
    x0: int,
    x1: int,
    y0: int,
    y1: int,
    smoothness: float,
) -> tuple[np.ndarray, np.ndarray]:
    xs = np.arange(x0 + TRACE_X_MARGIN_LEFT, x1 - TRACE_X_MARGIN_RIGHT + 1)
    low = y0 + TRACE_Y_MARGIN_TOP
    high = y1 - TRACE_Y_MARGIN_BOTTOM
    intensity = np.stack([image[low : high + 1, x] for x in xs], axis=1)
    cost = np.full(intensity.shape, np.inf)
    previous = np.zeros(intensity.shape, dtype=np.int16)
    cost[:, 0] = intensity[:, 0]

    for column in range(1, len(xs)):
        for row in range(intensity.shape[0]):
            lower = max(0, row - 3)
            upper = min(intensity.shape[0], row + 4)
            candidates = np.arange(lower, upper)
            transition = cost[lower:upper, column - 1] + smoothness * np.abs(candidates - row)
            best = int(np.argmin(transition))
            cost[row, column] = intensity[row, column] + transition[best]
            previous[row, column] = candidates[best]

    rows = np.empty(len(xs), dtype=int)
    rows[-1] = int(np.argmin(cost[:, -1]))
    for column in range(len(xs) - 1, 0, -1):
        rows[column - 1] = previous[rows[column], column]
    return xs, rows + low


def calibrate(
    xs: np.ndarray,
    ys: np.ndarray,
    x0: int,
    x1: int,
    y0: int,
    y1: int,
    value0: float,
    value1: float,
) -> tuple[np.ndarray, np.ndarray]:
    radius = R0_ARCSEC + (xs - x0) * (R1_ARCSEC - R0_ARCSEC) / (x1 - x0)
    value = value0 + (ys - y0) * (value1 - value0) / (y1 - y0)
    return radius, value


def main() -> None:
    eps_bytes = EPS.read_bytes()
    tex_bytes = TEX.read_bytes()
    assert sha256_bytes(eps_bytes) == EXPECTED_EPS_SHA256
    assert sha256_bytes(tex_bytes) == EXPECTED_TEX_SHA256

    tex = tex_bytes.decode()
    assert "PA is defined as the angle measured counter-clockwise" in tex
    assert "between the\nnorth direction on the sky and the major axis of the receding half" in tex
    assert "NGC 925  & 02 27 16.5 & +33 34 43.5" in tex
    assert "9.2 & 3.0 & 546.3 & 66.0 & 286.6" in tex

    jpeg = extract_embedded_jpeg(eps_bytes)
    image = np.asarray(Image.open(io.BytesIO(jpeg)).convert("L"), dtype=float)
    assert image.shape == (756, 561)

    xs, ys = trace_dark_continuous_curve(
        image, R_X0, R_X1, PA_PANEL_Y0, PA_PANEL_Y1, NOMINAL_SMOOTHNESS
    )
    radius, pa = calibrate(xs, ys, R_X0, R_X1, PA_TICK_Y0, PA_TICK_Y1, PA0_DEG, PA1_DEG)
    nominal = np.interp(RING_RADII_ARCSEC, radius, pa)

    ixs, iys = trace_dark_continuous_curve(
        image, R_X0, R_X1, I_PANEL_Y0, I_PANEL_Y1, NOMINAL_SMOOTHNESS
    )
    i_radius, inclination = calibrate(
        ixs, iys, R_X0, R_X1, I_TICK_Y0, I_TICK_Y1, I0_DEG, I1_DEG
    )
    nominal_i = np.interp(RING_RADII_ARCSEC, i_radius, inclination)

    pa_ensemble = []
    i_ensemble = []
    for dx0 in (-1, 0, 1):
        for dx1 in (-1, 0, 1):
            for dy0 in (-1, 0, 1):
                for dy1 in (-1, 0, 1):
                    for smoothness in (5.0, 8.0, 10.0, 12.0, 15.0, 20.0):
                        tx, ty = trace_dark_continuous_curve(
                            image,
                            R_X0 + dx0,
                            R_X1 + dx1,
                            PA_PANEL_Y0,
                            PA_PANEL_Y1,
                            smoothness,
                        )
                        tr, tp = calibrate(
                            tx,
                            ty,
                            R_X0 + dx0,
                            R_X1 + dx1,
                            PA_TICK_Y0 + dy0,
                            PA_TICK_Y1 + dy1,
                            PA0_DEG,
                            PA1_DEG,
                        )
                        pa_ensemble.append(np.interp(RING_RADII_ARCSEC, tr, tp))
                        itx, ity = trace_dark_continuous_curve(
                            image,
                            R_X0 + dx0,
                            R_X1 + dx1,
                            I_PANEL_Y0,
                            I_PANEL_Y1,
                            smoothness,
                        )
                        itr, iti = calibrate(
                            itx,
                            ity,
                            R_X0 + dx0,
                            R_X1 + dx1,
                            I_TICK_Y0 + dy0,
                            I_TICK_Y1 + dy1,
                            I0_DEG,
                            I1_DEG,
                        )
                        i_ensemble.append(np.interp(RING_RADII_ARCSEC, itr, iti))
    pa_ensemble_array = np.asarray(pa_ensemble)
    lower = np.quantile(pa_ensemble_array, 0.05, axis=0)
    upper = np.quantile(pa_ensemble_array, 0.95, axis=0)
    i_ensemble_array = np.asarray(i_ensemble)
    i_lower = np.quantile(i_ensemble_array, 0.05, axis=0)
    i_upper = np.quantile(i_ensemble_array, 0.95, axis=0)

    rows = []
    for r, inc, inc_lo, inc_hi, p, lo, hi in zip(
        RING_RADII_ARCSEC, nominal_i, i_lower, i_upper, nominal, lower, upper
    ):
        rows.append(
            {
                "radius_arcsec": f"{r:.1f}",
                "inclination_deg": f"{inc:.3f}",
                "inclination_digitization_p05_deg": f"{inc_lo:.3f}",
                "inclination_digitization_p95_deg": f"{inc_hi:.3f}",
                "position_angle_receding_deg": f"{p:.3f}",
                "position_angle_digitization_p05_deg": f"{lo:.3f}",
                "position_angle_digitization_p95_deg": f"{hi:.3f}",
                "position_angle_approaching_deg": f"{(p + 180.0) % 360.0:.3f}",
            }
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "status": "SOURCE_GEOMETRY_DIGITIZATION_COMPLETE_ENDPOINT_BLOCKED_PHYSICAL_UNCERTAINTY",
        "galaxy": "NGC0925",
        "source": {
            "citation": "de Blok et al. 2008, AJ 136, 2648, Figure 68 and Table 2",
            "arxiv": "0810.2100v2",
            "eps_sha256": EXPECTED_EPS_SHA256,
            "tex_sha256": EXPECTED_TEX_SHA256,
            "embedded_jpeg_sha256": sha256_bytes(jpeg),
            "embedded_jpeg_shape_yx": [756, 561],
        },
        "source_constants": {
            "centre_ra_j2000": "02 27 16.5",
            "centre_dec_j2000": "+33 34 43.5",
            "systemic_velocity_km_s": 546.3,
            "ring_spacing_arcsec": 3.0,
            "published_mean_inclination_deg": 66.0,
            "published_mean_position_angle_deg": 286.6,
        },
        "digitization": {
            "radius_axis_pixels": [R_X0, R_X1],
            "radius_axis_arcsec": [R0_ARCSEC, R1_ARCSEC],
            "pa_panel_pixels": [PA_PANEL_Y0, PA_PANEL_Y1],
            "pa_tick_anchor_pixels": [PA_TICK_Y0, PA_TICK_Y1],
            "pa_tick_anchor_deg": [PA0_DEG, PA1_DEG],
            "inclination_panel_pixels": [I_PANEL_Y0, I_PANEL_Y1],
            "inclination_tick_anchor_pixels": [I_TICK_Y0, I_TICK_Y1],
            "inclination_tick_anchor_deg": [I0_DEG, I1_DEG],
            "nominal_smoothness_penalty": NOMINAL_SMOOTHNESS,
            "ensemble_size": len(pa_ensemble),
            "sampled_radius_min_arcsec": float(RING_RADII_ARCSEC.min()),
            "sampled_radius_max_arcsec": float(RING_RADII_ARCSEC.max()),
            "sampled_ring_count": len(rows),
            "digitized_mean_pa_deg": float(np.mean(nominal)),
            "digitized_mean_inclination_deg": float(np.mean(nominal_i)),
            "absolute_difference_from_published_mean_pa_deg": float(abs(np.mean(nominal) - 286.6)),
            "absolute_difference_from_published_mean_inclination_deg": float(abs(np.mean(nominal_i) - 66.0)),
            "maximum_90pct_digitization_width_deg": float(np.max(upper - lower)),
            "maximum_inclination_90pct_digitization_width_deg": float(np.max(i_upper - i_lower)),
            "meaning": "The interval quantifies raster trace and axis-anchor sensitivity only; it is not a physical tilted-ring uncertainty.",
        },
        "signed_side_convention": {
            "receding": "PA(R), measured counter-clockwise from north to the receding major axis",
            "approaching": "PA(R)+180 deg modulo 360 deg",
        },
        "endpoint_pixels_read": False,
        "endpoint_allowed": False,
        "remaining_blockers": [
            "source-published or independently justified physical i(R)/PA(R) uncertainty and covariance",
            "source-frozen centre alternatives and their weights",
            "HALOGAS beam/covariance blocks and common-footprint mask",
            "solver convergence tolerance and wrong-family geometries",
        ],
        "claim_boundary": "This is a reproducible source-figure digitization and signed-geometry partial freeze. It is not an endpoint score, a Tau q_R selection, a parent-morphology detection, Nature occupation, or dark-matter-replacement evidence.",
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n")

    digest_lines = []
    for path in (OUT_CSV, OUT_JSON):
        digest_lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT)}")
    OUT_SHA.write_text("\n".join(digest_lines) + "\n")

    REPORT.write_text(
        "# NGC925 signed source-geometry partial freeze v01\n\n"
        f"Status: `{summary['status']}`.\n\n"
        "The cached de Blok et al. (2008) EPS contains one 561 x 756 grayscale JPEG. The script "
        "extracts that raster directly, rather than digitizing a rescaled PDF screenshot. It uses the source "
        "Table 2 value `i=66.0 deg` and traces the thick adopted PA curve in Figure 68. The source definition "
        "makes PA the counter-clockwise sky angle from north to the receding major axis, so the approaching "
        "axis is fixed at `PA+180 deg` modulo 360 degrees.\n\n"
        f"The nominal 3-arcsec table contains `{len(rows)}` rings from `{RING_RADII_ARCSEC.min():.0f}` to "
        f"`{RING_RADII_ARCSEC.max():.0f}` arcsec. Its mean digitized PA is "
        f"`{np.mean(nominal):.3f} deg`, within `{abs(np.mean(nominal)-286.6):.3f} deg` of the independently "
        "printed mean `286.6 deg`. The adopted inclination curve is traced separately; its mean is "
        f"`{np.mean(nominal_i):.3f} deg`, rather than incorrectly treating the printed `66.0 deg` summary "
        "as a constant radial law. A 486-member axis-anchor and path-smoothness ensemble supplies a raster "
        f"sensitivity envelope; its largest PA and inclination 90% widths are "
        f"`{np.max(upper-lower):.3f} deg` and `{np.max(i_upper-i_lower):.3f} deg`.\n\n"
        "This envelope is not a physical uncertainty model. The paper does not supply a machine-readable "
        "ring covariance for the adopted geometry, and NGC925 has a bar, a reported inclination trend, and "
        "known tilted-ring degeneracy in its nearly solid-body region. Endpoint access therefore remains "
        "blocked until physical orientation uncertainty/covariance, centre alternatives, common footprint, "
        "beam blocks, solver tolerance, and wrong-family controls are frozen. No HALOGAS endpoint pixel is "
        "read by this script.\n"
    )
    print("NGC0925_SIGNED_DESCRIPTOR_SOURCE_GEOMETRY_PARTIAL_FREEZE_COMPLETE")


if __name__ == "__main__":
    main()
