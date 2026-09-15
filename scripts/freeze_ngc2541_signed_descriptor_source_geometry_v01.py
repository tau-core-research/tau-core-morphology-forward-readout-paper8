#!/usr/bin/env python3
"""Freeze the residual-blind signed tilted-ring descriptor for NGC2541."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "external" / "literature" / "jozsa2007_ngc2541_table6_orientation_v01.csv"
PDF = ROOT / "data" / "external" / "literature" / "ugc08490_ngc5204_warp" / "gentile2007_warped_disks.pdf"
DATA = ROOT / "data" / "derived"
OUT_POINTS = DATA / "ngc2541_signed_descriptor_source_geometry_freeze_v01_points.csv"
OUT_JSON = DATA / "ngc2541_signed_descriptor_source_geometry_freeze_v01.json"
OUT_SHA = DATA / "ngc2541_signed_descriptor_source_geometry_freeze_v01.sha256"
REPORT = ROOT / "reports" / "ngc2541_signed_descriptor_source_geometry_freeze_v01.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def unit_rows(values: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(values, axis=1)
    if np.any(norms <= 0.0):
        raise RuntimeError("zero spin normal in source table")
    return values / norms[:, None]


def markdown_table(frame: pd.DataFrame) -> str:
    display = frame.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.8g}")
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    source = pd.read_csv(RAW)
    required = {
        "radius_arcsec", "inclination_deg", "pa_deg", "n_w", "n_n", "n_los",
        "tip_deg", "lon_deg",
    }
    if not required.issubset(source.columns) or len(source) != 29:
        raise RuntimeError("unexpected NGC2541 source-only orientation table")
    if not source["radius_arcsec"].is_monotonic_increasing:
        raise RuntimeError("source radii are not ordered")

    raw_normals = source[["n_w", "n_n", "n_los"]].to_numpy(float)
    normals = unit_rows(raw_normals)
    source_norm_error = np.abs(np.linalg.norm(raw_normals, axis=1) - 1.0)

    # These ranges are published in Jozsa (2007), Table 4.  The published
    # inner-plane range begins at 30 arcsec.  The paper separately flags its
    # first two plotted points as possible non-circular-motion fit artefacts;
    # neither statement is used to extend the frozen support inward.
    inner_mask = source["radius_arcsec"].between(30.0, 240.0)
    outer_mask = source["radius_arcsec"].between(300.0, 590.0)
    support_mask = source["radius_arcsec"].between(30.0, 590.0)
    n_inner = unit_rows(normals[inner_mask].mean(axis=0, keepdims=True))[0]
    n_outer = unit_rows(normals[outer_mask].mean(axis=0, keepdims=True))[0]
    cross = np.cross(n_inner, n_outer)
    separation_sine = float(np.linalg.norm(cross))
    if separation_sine <= 1.0e-6:
        raise RuntimeError("inner and outer source planes are not distinct")
    c_axis = cross / separation_sine
    basis = np.vstack((n_inner, n_outer, c_axis))
    basis_condition = float(np.linalg.cond(basis))
    decoder_jacobian = np.linalg.inv(basis) @ np.diag([-1.0, -1.0, 1.0])

    support = source.loc[support_mask].copy()
    n_support = normals[support_mask]
    d_inner = 1.0 - n_support @ n_inner
    d_outer = 1.0 - n_support @ n_outer
    chi = n_support @ c_axis
    descriptor = np.column_stack((d_inner, d_outer, chi))
    decoded = np.vstack(
        [np.linalg.solve(basis, np.array([1.0 - d[0], 1.0 - d[1], d[2]])) for d in descriptor]
    )
    decoder_error = float(np.max(np.linalg.norm(decoded - n_support, axis=1)))
    jacobian_error = float(np.max(np.abs(decoder_jacobian - np.linalg.inv(basis) @ np.diag([-1.0, -1.0, 1.0]))))

    reference_i_deg = 66.3
    sin2_reference = float(np.sin(np.deg2rad(reference_i_deg)) ** 2)
    projection_ratio_sq = (1.0 - n_support[:, 2] ** 2) / sin2_reference
    terminal_covectors = np.column_stack(
        (
            np.zeros(len(n_support)),
            np.zeros(len(n_support)),
            -2.0 * n_support[:, 2] / sin2_reference,
        )
    )
    composite = terminal_covectors @ decoder_jacobian
    eps = 1.0e-6
    finite_difference = np.empty_like(composite)
    for row_index, d_hat in enumerate(descriptor):
        for column in range(3):
            step = np.zeros(3)
            step[column] = eps
            n_plus = np.linalg.solve(basis, np.array([1.0 - d_hat[0] - step[0], 1.0 - d_hat[1] - step[1], d_hat[2] + step[2]]))
            n_minus = np.linalg.solve(basis, np.array([1.0 - d_hat[0] + step[0], 1.0 - d_hat[1] + step[1], d_hat[2] - step[2]]))
            g_plus = (1.0 - n_plus[2] ** 2) / sin2_reference
            g_minus = (1.0 - n_minus[2] ** 2) / sin2_reference
            finite_difference[row_index, column] = (g_plus - g_minus) / (2.0 * eps)
    chain_error = float(np.max(np.abs(composite - finite_difference)))

    out = support[[
        "radius_arcsec", "inclination_deg", "e_inclination_deg", "pa_deg", "e_pa_deg",
        "tip_deg", "e_tip_deg", "lon_deg", "e_lon_deg",
    ]].copy()
    out["n_w_unit"] = n_support[:, 0]
    out["n_n_unit"] = n_support[:, 1]
    out["n_los_unit"] = n_support[:, 2]
    out["d_inner"] = d_inner
    out["d_outer"] = d_outer
    out["chi"] = chi
    out["projection_ratio_sq_reference_sensitivity"] = projection_ratio_sq
    out["endpoint_values_used"] = False
    out.to_csv(OUT_POINTS, index=False, float_format="%.12g")

    result = {
        "schema": "tau_core_ngc2541_signed_descriptor_source_geometry_freeze_v01",
        "status": "SOURCE_GEOMETRY_READY_TERMINAL_CALIBRATION_AND_UNTOUCHED_ENDPOINT_BLOCKED",
        "galaxy": "NGC2541",
        "alias": "UGC4284",
        "source": {
            "citation": "Jozsa 2007, A&A 468, 731, online Table 6 and Table 4",
            "pdf_sha256": sha256(PDF),
            "orientation_table_sha256": sha256(RAW),
            "approaching_side": "NE",
            "reference_inclination_deg": reference_i_deg,
            "reference_pa_deg": 261.2,
            "inner_plane_range_arcsec": [30.0, 240.0],
            "outer_plane_range_arcsec": [300.0, 590.0],
            "excluded_inner_reason": "published inner-plane range begins at 30 arcsec; paper separately flags its first two plotted points as possible non-circular-motion fit artefacts",
        },
        "descriptor": {
            "definition": "D_hat=(1-n_inner dot n,1-n_outer dot n,c dot n)",
            "decoder": "N(D_hat)=A^-1(1-d_inner,1-d_outer,chi)^T",
            "jacobian": "J_OS=D_Dhat N=A^-1 diag(-1,-1,+1)",
            "inner_normal": n_inner.tolist(),
            "outer_normal": n_outer.tolist(),
            "transverse_axis": c_axis.tolist(),
            "basis_condition_number": basis_condition,
            "maximum_decoder_error": decoder_error,
            "maximum_source_rounding_norm_error": float(source_norm_error.max()),
            "n_support_rings": int(len(out)),
        },
        "reference_projection_sensitivity": {
            "formula": "G_ref=(1-n_los^2)/sin(i_ref)^2",
            "terminal_covector": "P_R=(0,0,-2*n_los/sin(i_ref)^2)",
            "chain": "D_Dhat G_ref=P_R J_OS",
            "maximum_finite_difference_error": chain_error,
            "minimum_ratio_sq": float(projection_ratio_sq.min()),
            "maximum_ratio_sq": float(projection_ratio_sq.max()),
            "status": "SOURCE_FROZEN_ALGEBRAIC_SENSITIVITY_ONLY",
        },
        "physical_terminal_branch": {
            "status": "BLOCKED_PENDING_ENDPOINT_CALIBRATION",
            "reason": "oriented normals do not prove that an eventual endpoint used one fixed 66.3-degree inclination reduction",
        },
        "integrability": {
            "pathwise_finite_profile": "available after one source-owned anchor for any L1 pullback on this radial chain",
            "ambient_descriptor_exactness": "not established by one radial chain; no independent cycles",
            "normalization": "must be source-owned and fixed before endpoint access",
        },
        "endpoint_values_used": False,
        "endpoint_scoring_allowed": False,
        "free_parameters": 0,
        "claim_boundary": (
            "Complete source-owned signed geometry and a reference-projection sensitivity Jacobian only. "
            "No Tau-specific q_R, physical terminal calibration, Nature occupation, or galaxy score is derived."
        ),
    }
    if decoder_error >= 1.0e-10 or jacobian_error != 0.0 or chain_error >= 1.0e-8:
        raise RuntimeError("signed-descriptor reconstruction or chain-rule audit failed")
    OUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    OUT_SHA.write_text(f"{sha256(OUT_JSON)}  {OUT_JSON.name}\n", encoding="utf-8")

    summary = pd.DataFrame([{
        "status": result["status"],
        "n_support_rings": len(out),
        "basis_condition_number": basis_condition,
        "maximum_decoder_error": decoder_error,
        "chain_rule_max_error": chain_error,
        "reference_projection_ratio_min": projection_ratio_sq.min(),
        "reference_projection_ratio_max": projection_ratio_sq.max(),
        "endpoint_values_used": False,
        "endpoint_scoring_allowed": False,
    }])
    REPORT.write_text(
        "# NGC2541 / UGC4284 signed-descriptor source freeze v01\n\n"
        + markdown_table(summary)
        + "\n\nThe freeze uses only the radius and orientation columns of Jozsa (2007) "
        "Table 6 plus the source-published inner/outer ranges. Rotation velocity, "
        "SPARC residuals and baseline scores are not used.\n\n"
        "The complete signed descriptor reconstructs the unit ring normals and "
        "passes `D_Dhat G_ref=P_R J_OS`. The latter is only a fixed-reference "
        "projection sensitivity. Physical scoring remains blocked until an untouched "
        "endpoint and its inclination-reduction provenance are frozen.\n",
        encoding="utf-8",
    )
    print("NGC2541_SIGNED_DESCRIPTOR_SOURCE_GEOMETRY_FREEZE_PASS")


if __name__ == "__main__":
    main()
