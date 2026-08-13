#!/usr/bin/env python3
"""Freeze a source-only determinant-line proxy for NGC4254.

This script deliberately reads no velocity field, rotation curve, fitted
residual, or dark-discrepancy label. It constructs a four-role inverse proxy
from inherited frozen geometry and source-side baryonic surface-density maps.
The inherited geometry has a kinematic provenance, which remains an explicit
independence limitation for a later endpoint.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

GEOMETRY_PATH = DATA / "ngc4254_common_mode_geometry_freeze_v01.json"
FIELDS_PATH = DATA / "ngc4254_baryonic_surface_density_fields_v01.fits"
CSV_PATH = DATA / "ngc4254_ffl_determinant_source_vectors_v01.csv"
JSON_PATH = DATA / "ngc4254_ffl_determinant_source_freeze_v01.json"
REPORT_PATH = REPORTS / "ngc4254_ffl_determinant_source_freeze_v01.md"

STATUS = "SOURCE_ONLY_FFL_DETERMINANT_PROXY_FROZEN_NOT_ENDPOINT_READY"
CLAIM_BOUNDARY = (
    "source-only four-role inverse proxy; not a parent role identification, "
    "physical channel/time/quantum signal, dark-matter replacement, or endpoint score"
)

# Columns are a fixed oriented orthonormal basis of E_S = 1^perp in R^4.
E_S_BASIS = np.array(
    [
        [1.0 / math.sqrt(2.0), 1.0 / math.sqrt(6.0), 1.0 / math.sqrt(12.0)],
        [-1.0 / math.sqrt(2.0), 1.0 / math.sqrt(6.0), 1.0 / math.sqrt(12.0)],
        [0.0, -2.0 / math.sqrt(6.0), 1.0 / math.sqrt(12.0)],
        [0.0, 0.0, -3.0 / math.sqrt(12.0)],
    ],
    dtype=float,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def centered(values: np.ndarray) -> np.ndarray:
    return values - float(np.mean(values))


def vector_columns(prefix: str, values: np.ndarray) -> dict[str, float]:
    return {f"{prefix}_q{index}": float(value) for index, value in enumerate(values)}


def load_source_fields() -> tuple[np.ndarray, np.ndarray, np.ndarray, WCS]:
    with fits.open(FIELDS_PATH) as hdul:
        star_hdu = hdul["SIGMA_STAR"]
        star = np.asarray(star_hdu.data, dtype=float)
        h2 = np.asarray(hdul["SIGMA_H2"].data, dtype=float)
        hi = np.asarray(hdul["SIGMA_HI"].data, dtype=float)
        wcs = WCS(star_hdu.header, naxis=2)
    if star.shape != h2.shape or star.shape != hi.shape:
        raise ValueError("Source-side surface-density fields do not share one grid")
    return star, h2, hi, wcs


def build_rows_from_fields(
    geometry: dict[str, object],
    star: np.ndarray,
    h2: np.ndarray,
    hi: np.ndarray,
    wcs: WCS,
    *,
    star_scale: float = 1.0,
    h2_scale: float = 1.0,
    hi_scale: float = 1.0,
) -> list[dict[str, object]]:
    """Construct determinant rows from already selected source-side fields."""

    if star.shape != h2.shape or star.shape != hi.shape:
        raise ValueError("Source-side surface-density fields do not share one grid")
    scales = (star_scale, h2_scale, hi_scale)
    if not all(math.isfinite(value) and value > 0.0 for value in scales):
        raise ValueError("Source conversion scales must be finite and positive")
    star = np.asarray(star, dtype=float) * star_scale
    gas = np.asarray(h2, dtype=float) * h2_scale + np.asarray(hi, dtype=float) * hi_scale

    y_pixels, x_pixels = np.indices(star.shape, dtype=float)
    ra_deg, dec_deg = wcs.pixel_to_world_values(x_pixels, y_pixels)

    ra0, dec0 = (float(value) for value in geometry["center_icrs_deg"])
    pa = math.radians(float(geometry["position_angle_deg_east_of_north"]))
    inclination = math.radians(float(geometry["inclination_deg"]))
    cos_i = math.cos(inclination)

    east = (ra_deg - ra0) * math.cos(math.radians(dec0)) * 3600.0
    north = (dec_deg - dec0) * 3600.0
    major = east * math.sin(pa) + north * math.cos(pa)
    minor = -east * math.cos(pa) + north * math.sin(pa)
    deprojected_minor = minor / cos_i
    radius = np.hypot(major, deprojected_minor)
    theta = np.mod(np.arctan2(deprojected_minor, major), 2.0 * math.pi)
    quadrant = np.floor(theta / (0.5 * math.pi)).astype(int)

    finite_source = (
        np.isfinite(star)
        & np.isfinite(gas)
        & np.isfinite(radius)
        & np.isfinite(theta)
        & (star > 0.0)
        & (gas > 0.0)
    )
    path_field = math.sin(inclination) * np.sin(theta)
    edges = [float(value) for value in geometry["radial_edges_arcsec"]]

    rows: list[dict[str, object]] = []
    for radial_index, (radius_lo, radius_hi) in enumerate(zip(edges[:-1], edges[1:])):
        annulus = finite_source & (radius >= radius_lo) & (radius < radius_hi)
        counts = np.array(
            [np.count_nonzero(annulus & (quadrant == index)) for index in range(4)],
            dtype=int,
        )
        if np.any(counts == 0):
            raise ValueError(
                f"Annulus {radius_lo:g}-{radius_hi:g} arcsec lacks a populated quadrant"
            )

        u_raw = np.array(
            [np.median(path_field[annulus & (quadrant == index)]) for index in range(4)]
        )
        v_raw = np.log(
            np.array(
                [np.median(star[annulus & (quadrant == index)]) for index in range(4)]
            )
        )
        eta_raw = np.log(
            np.array(
                [np.median(gas[annulus & (quadrant == index)]) for index in range(4)]
            )
        )

        u = centered(u_raw)
        v = centered(v_raw)
        eta = centered(eta_raw)
        u_es = E_S_BASIS.T @ u
        v_es = E_S_BASIS.T @ v
        eta_es = E_S_BASIS.T @ eta
        determinant_normal = np.cross(u_es, v_es)
        determinant_norm = float(np.linalg.norm(determinant_normal))
        if determinant_norm == 0.0:
            raise ValueError(
                f"Annulus {radius_lo:g}-{radius_hi:g} has dependent source tangents"
            )

        conditioning = determinant_norm / (
            float(np.linalg.norm(u_es)) * float(np.linalg.norm(v_es))
        )
        q_shape_proxy = float(np.dot(determinant_normal, eta_es) / determinant_norm)
        eta_plane_fraction = float(
            np.linalg.norm(
                eta_es
                - determinant_normal
                * np.dot(determinant_normal, eta_es)
                / determinant_norm**2
            )
            / np.linalg.norm(eta_es)
        )

        row: dict[str, object] = {
            "galaxy": "NGC4254",
            "radial_index": radial_index,
            "radius_lo_arcsec": radius_lo,
            "radius_hi_arcsec": radius_hi,
            "radius_mid_arcsec": 0.5 * (radius_lo + radius_hi),
            "n_pixels_total": int(np.sum(counts)),
            "determinant_norm": determinant_norm,
            "delta_uv": float(conditioning),
            "q_shape_proxy": q_shape_proxy,
            "eta_in_uv_plane_fraction": eta_plane_fraction,
            "source_vector_computable": True,
            "physical_amplitude_ready": False,
            "endpoint_scored": False,
        }
        row.update({f"n_pixels_q{index}": int(value) for index, value in enumerate(counts)})
        row.update(vector_columns("u_path_centered", u))
        row.update(vector_columns("v_star_log_centered", v))
        row.update(vector_columns("eta_gas_log_centered", eta))
        rows.append(row)

    return rows


def build_rows(geometry: dict[str, object]) -> list[dict[str, object]]:
    star, h2, hi, wcs = load_source_fields()
    return build_rows_from_fields(geometry, star, h2, hi, wcs)


def write_report(rows: list[dict[str, object]], manifest: dict[str, object]) -> None:
    table_lines = [
        "| annulus (arcsec) | quadrant pixels | Delta_uv | q_shape proxy | gas-shape fraction in span(u,v) |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        counts = "/".join(str(row[f"n_pixels_q{index}"]) for index in range(4))
        table_lines.append(
            "| "
            f"{row['radius_lo_arcsec']:.0f}-{row['radius_hi_arcsec']:.0f} | "
            f"{counts} | {row['delta_uv']:.6f} | {row['q_shape_proxy']:+.6f} | "
            f"{row['eta_in_uv_plane_fraction']:.6f} |"
        )

    report = f"""# NGC4254 Source-Only FFL Determinant Proxy Freeze v01

**Status:** `{STATUS}`

**Claim boundary:** {CLAIM_BOUNDARY}.

## Purpose

This freeze asks only whether one endpoint-unread, four-role 4D inverse chart
can instantiate the determinant contraction before any terminal score. It does
not identify the parent role chart or infer the morphological body from a
readout. The formula and map extraction are blind to velocity pixels, but the
inherited center/PA/inclination values have a prior Halpha-kinematic provenance.

## Frozen Construction

- Four roles: the four deprojected disk quadrants fixed by the source-frozen
  center, position angle, and inclination.
- `u_OS`: centered quadrant medians of `sin(i) sin(theta)`, a geometry-only
  observer-source path proxy.
- `v_M`: centered log quadrant medians of stellar surface density, a
  stabilized-body shape proxy.
- `eta_shape`: centered log quadrant medians of `Sigma_H2 + Sigma_HI`, a
  source-side third-shape proxy.
- Radial windows: the already frozen 5--65 arcsec annuli. No annulus was added,
  removed, or moved using a velocity endpoint.
- Relative space: the fixed oriented orthonormal basis of
  `E_S = 1^perp subset R^4` recorded in the JSON manifest.

For each annulus the recorded scalar is

```text
q_shape_proxy = det(u_OS, v_M, eta_shape) / ||u_OS x v_M||.
```

`Delta_uv = ||u_OS x v_M||/(||u_OS|| ||v_M||)` is reported as a conditioning
diagnostic only. No conditioning threshold selects the rows.

## Frozen Rows

{chr(10).join(table_lines)}

## Provenance And Leakage Boundary

- Geometry input SHA-256: `{manifest['inputs']['geometry_freeze_sha256']}`
- Surface-density input SHA-256: `{manifest['inputs']['surface_density_fields_sha256']}`
- Velocity, rotation-curve, fitted-residual, and dark-discrepancy inputs read:
  **none**.
- The inherited geometry is source-frozen but was originally obtained from a
  PHANGS Halpha kinematic geometry. A later Halpha endpoint therefore requires
  an independently sourced morphology geometry or an explicit dependence
  control; a distinct held-out tracer remains another option.
- The surface-density file uses fixed stellar, CO-to-H2, and HI conversions;
  those assumptions are inherited rather than fitted here.

## What This Does Not Establish

The quadrant chart is a 4D inverse candidate, not a physical identification of
the parent roles. `eta_shape` is not yet the physical FFL terminal load, and
the missing `kappa_X/kappa_Y` normalization prevents a physical amplitude or
time-readout prediction. The approximately 37 arcsec HI beam also correlates
the narrower radial annuli, so the rows are not independent observations.

The freeze therefore establishes source-side computability only. It reports no
channel detection, no time or quantum signal, no dark-matter replacement, and
no endpoint validation.
"""
    REPORT_PATH.write_text(report, encoding="utf-8")


def main() -> None:
    geometry = json.loads(GEOMETRY_PATH.read_text(encoding="utf-8"))
    if not geometry.get("freeze_complete"):
        raise ValueError("The geometry source is not marked frozen")
    if geometry.get("velocity_pixels_read_during_freeze") is not False:
        raise ValueError("Geometry provenance does not certify velocity blindness")

    rows = build_rows(geometry)
    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(CSV_PATH, index=False, float_format="%.12g", lineterminator="\n")

    manifest: dict[str, object] = {
        "schema": "ngc4254_ffl_determinant_source_freeze_v01",
        "status": STATUS,
        "galaxy": "NGC4254",
        "construction_class": "source_only_4d_inverse_role_chart_proxy",
        "inputs": {
            "geometry_freeze": str(GEOMETRY_PATH.relative_to(ROOT)),
            "geometry_freeze_sha256": sha256(GEOMETRY_PATH),
            "surface_density_fields": str(FIELDS_PATH.relative_to(ROOT)),
            "surface_density_fields_sha256": sha256(FIELDS_PATH),
            "velocity_or_residual_inputs": [],
        },
        "role_chart": {
            "roles": ["Q0", "Q1", "Q2", "Q3"],
            "quadrant_rule": "floor(mod(atan2(minor/cos(i),major),2pi)/(pi/2))",
            "observer_source_tangent": "centered quadrant median of sin(i)*sin(theta)",
            "body_tangent": "centered log quadrant median of Sigma_star",
            "third_shape_proxy": "centered log quadrant median of Sigma_H2+Sigma_HI",
            "radial_edges_arcsec": geometry["radial_edges_arcsec"],
            "es_basis_columns": E_S_BASIS.tolist(),
            "orientation_policy": "fixed ordered Q0,Q1,Q2,Q3 pseudoform chart",
        },
        "formula": {
            "determinant_normal": "cross(E_S^T u_OS,E_S^T v_M)",
            "q_shape_proxy": "dot(determinant_normal,E_S^T eta_shape)/norm(determinant_normal)",
            "conditioning": "Delta_uv=norm(cross(u_OS,v_M))/(norm(u_OS)*norm(v_M))",
            "conditioning_selection_threshold": None,
        },
        "outputs": {
            "row_table": str(CSV_PATH.relative_to(ROOT)),
            "row_table_sha256": sha256(CSV_PATH),
            "report": str(REPORT_PATH.relative_to(ROOT)),
        },
        "summary": {
            "n_annuli": len(rows),
            "n_source_vector_computable": int(sum(bool(row["source_vector_computable"]) for row in rows)),
            "endpoint_scored": False,
            "physical_amplitude_ready": False,
            "source_extraction_viable": True,
        },
        "known_limitations": [
            "quadrant role chart is a 4D inverse candidate, not a parent role identity",
            "gas contrast is a source-side eta-shape proxy, not the physical FFL eta",
            "kappa_X/kappa_Y and the physical terminal gain remain unsourced",
            "the inherited center/PA/inclination geometry has prior Halpha-kinematic provenance",
            "the HI beam is about 37 arcsec and correlates the narrower annuli",
            "fixed baryonic conversion assumptions are inherited",
            "no endpoint or covariance score is present",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }

    # The report reads provenance from the manifest; the manifest then records
    # the deterministic report path without creating a self-hash cycle.
    write_report(rows, manifest)
    JSON_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(STATUS)
    print(f"rows={len(rows)} csv_sha256={manifest['outputs']['row_table_sha256']}")


if __name__ == "__main__":
    main()
