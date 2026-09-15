#!/usr/bin/env python3
"""Freeze the source-only signed-descriptor projection control for UGC03580."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
BODY = DATA / "ugc03580_ugc3580_two_plane_body_v01.json"
BODY_POINTS = DATA / "ugc03580_ugc3580_two_plane_body_v01_points.csv"
SHELL = DATA / "ugc03580_ugc3580_two_plane_readout_shell_v01.json"
MASTER = DATA / "external_sparc_master_table.csv"
MANIFEST = DATA / "ugc03580_signed_descriptor_projection_control_freeze_v01.json"
MANIFEST_SHA = DATA / "ugc03580_signed_descriptor_projection_control_freeze_v01.sha256"
POINTS_OUT = DATA / "ugc03580_signed_descriptor_projection_control_freeze_v01_points.csv"
REPORT = ROOT / "reports" / "ugc03580_signed_descriptor_projection_control_freeze_v01.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def markdown_table(frame: pd.DataFrame) -> str:
    display = frame.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda x: f"{x:.8g}")
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[c]) for c in display.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    body = json.loads(BODY.read_text(encoding="utf-8"))
    shell = json.loads(SHELL.read_text(encoding="utf-8"))
    if body["status"] != "SOURCE_ACQUISITION_ONLY" or body["endpoint_allowed"]:
        raise RuntimeError("the upstream body is not source-only")
    if shell["status"] != "FORMULA_SHELL_DERIVED_ENDPOINT_BLOCKED":
        raise RuntimeError("unexpected upstream shell status")
    if shell["endpoint_values_used"] or shell["endpoint_allowed"]:
        raise RuntimeError("the upstream shell is endpoint-contaminated")

    master = pd.read_csv(MASTER)
    row = master.loc[master["Galaxy"].eq("UGC03580")]
    if len(row) != 1:
        raise RuntimeError("UGC03580 global calibration row is not unique")
    row = row.iloc[0]
    distance_mpc = float(row["D_Mpc"])
    global_inclination_deg = float(row["Inc_deg"])

    points = pd.read_csv(BODY_POINTS)
    points = points.loc[points["within_source_terminal_support"].astype(bool)].copy()
    inner = body["construction"]["inner_reference_plane"]
    outer = body["construction"]["outer_mean_plane"]
    n_inner = np.array([inner["n_w"], inner["n_n"], inner["n_los"]], dtype=float)
    n_outer = np.array([outer["n_w"], outer["n_n"], outer["n_los"]], dtype=float)
    transverse = np.cross(n_inner, n_outer)
    transverse /= np.linalg.norm(transverse)
    decoder_basis = np.vstack((n_inner, n_outer, transverse))
    decoder_jacobian = np.linalg.inv(decoder_basis) @ np.diag([-1.0, -1.0, 1.0])

    normals = points[["n_w_orientation", "n_n_orientation", "n_los_orientation"]].to_numpy(float)
    n_los = normals[:, 2]
    sin2_global = float(np.sin(np.deg2rad(global_inclination_deg)) ** 2)
    projection_ratio_sq = (1.0 - n_los**2) / sin2_global

    # Exact local chain rule for Dhat=(d_in,d_out,chi):
    # D_Dhat G = P_R J_OS with J_OS=D_Dhat N and
    # P_R=(0,0,-2 n_los/sin(i_global)^2).
    analytic = np.vstack(
        [np.array([0.0, 0.0, -2.0 * value / sin2_global]) @ decoder_jacobian for value in n_los]
    )
    eps = 1.0e-6
    numeric = np.empty_like(analytic)
    d_inner = 1.0 - normals @ n_inner
    d_outer = 1.0 - normals @ n_outer
    chi = normals @ transverse
    descriptor = np.column_stack((d_inner, d_outer, chi))
    for i, d_hat in enumerate(descriptor):
        for j in range(3):
            step = np.zeros(3)
            step[j] = eps
            n_plus = np.linalg.solve(
                decoder_basis, np.array([1.0, 1.0, 0.0]) + np.diag([-1.0, -1.0, 1.0]) @ (d_hat + step)
            )
            n_minus = np.linalg.solve(
                decoder_basis, np.array([1.0, 1.0, 0.0]) + np.diag([-1.0, -1.0, 1.0]) @ (d_hat - step)
            )
            g_plus = (1.0 - n_plus[2] ** 2) / sin2_global
            g_minus = (1.0 - n_minus[2] ** 2) / sin2_global
            numeric[i, j] = (g_plus - g_minus) / (2.0 * eps)
    chain_error = float(np.max(np.abs(analytic - numeric)))

    k1 = shell["scalar_registration_boundary"]["selected_witness"]
    k1_collision_projection_difference = abs(float(k1["projection_difference"]))
    if k1_collision_projection_difference <= 0.08:
        raise RuntimeError("the frozen K1 fibre counterexample disappeared")
    if chain_error >= 1.0e-8:
        raise RuntimeError("mixed-Hessian/terminal chain-rule audit failed")

    kpc_per_arcsec = distance_mpc * 1000.0 / 206265.0
    out = pd.DataFrame(
        {
            "radius_arcsec": points["radius_arcsec"].to_numpy(float),
            "radius_kpc_terminal_calibration": points["radius_arcsec"].to_numpy(float) * kpc_per_arcsec,
            "inclination_deg_source": points["inclination_deg"].to_numpy(float),
            "signed_chi": chi,
            "projection_ratio_sq": projection_ratio_sq,
            "projection_velocity_factor": np.sqrt(np.maximum(projection_ratio_sq, 0.0)),
            "endpoint_values_used": False,
        }
    )
    out.to_csv(POINTS_OUT, index=False, float_format="%.12g")

    result = {
        "schema": "tau_core_ugc03580_signed_descriptor_projection_control_freeze_v01",
        "status": "SOURCE_FROZEN_STANDARD_PROJECTION_CONTROL_READY_DIAGNOSTIC_ONLY",
        "galaxy": "UGC03580",
        "source_hashes": {
            "body": sha256(BODY),
            "body_points": sha256(BODY_POINTS),
            "readout_shell": sha256(SHELL),
            "global_calibration_table": sha256(MASTER),
        },
        "calibration": {
            "distance_mpc": distance_mpc,
            "global_inclination_deg": global_inclination_deg,
            "kpc_per_arcsec": kpc_per_arcsec,
            "source": "external_sparc_master_table.csv global fields only",
        },
        "descriptor": {
            "full_signed_descriptor": "D_hat=(d_in,d_out,chi)",
            "decoder": "N(D_hat)=A^-1(1-d_in,1-d_out,chi)^T",
            "scalar_K1_is_complete": False,
            "k1_collision_projection_difference": k1_collision_projection_difference,
        },
        "mixed_hessian_terminal_chain": {
            "response": "Gamma=J_OS=D_Dhat N for the frozen Bregman graph control",
            "terminal_covector": "P_R=D_N G_proj=(0,0,-2*n_los/sin(i_global)^2)",
            "composite": "D_Dhat G_proj=P_R J_OS",
            "maximum_finite_difference_error": chain_error,
            "nonzero_on_source_support": bool(np.max(np.linalg.norm(analytic, axis=1)) > 0.0),
        },
        "terminal_formula": {
            "projection_ratio_sq": "G_proj(R)=sin(i_source(R))^2/sin(i_global)^2",
            "reported_velocity_control": "v_pred_reported(R)=sqrt(G_proj(R))*v_carrier(R)",
            "free_parameters": 0,
            "post_freeze_retuning_allowed": False,
        },
        "support": {
            "minimum_kpc": float(out["radius_kpc_terminal_calibration"].min()),
            "maximum_kpc": float(out["radius_kpc_terminal_calibration"].max()),
            "n_source_rings": int(len(out)),
        },
        "endpoint_values_used": False,
        "endpoint_scoring_allowed": True,
        "score_status_limit": "DIAGNOSTIC_STANDARD_SYSTEMATICS_CONTROL_ONLY",
        "claim_boundary": (
            "A source-frozen standard tilted-ring projection control, not a Tau-specific "
            "q_R law, morphology-body occupation result, or dark-matter replacement. "
            "Application is valid only if the compared terminal used the declared fixed "
            "global-inclination reduction; otherwise it is a sensitivity control."
        ),
    }
    MANIFEST.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    MANIFEST_SHA.write_text(f"{sha256(MANIFEST)}  {MANIFEST.name}\n", encoding="utf-8")

    summary = pd.DataFrame([{
        "status": result["status"],
        "n_source_rings": len(out),
        "min_projection_ratio_sq": float(projection_ratio_sq.min()),
        "max_projection_ratio_sq": float(projection_ratio_sq.max()),
        "chain_rule_max_error": chain_error,
        "endpoint_values_used": False,
        "endpoint_scoring_allowed": True,
    }])
    REPORT.write_text(
        "# UGC03580 signed-descriptor projection-control freeze v01\n\n"
        + markdown_table(summary)
        + "\n\nThe complete signed two-plane descriptor is retained. The frozen "
        "Bregman graph control gives `Gamma=J_OS`, and the standard projection "
        "terminal obeys `D_Dhat G_proj=P_R J_OS`. No rotation endpoint was read.\n\n"
        "This is a zero-free-parameter standard-systematics control. It is not a "
        "Tau-specific radial law or evidence for parent morphology.\n",
        encoding="utf-8",
    )
    print("UGC03580_SIGNED_DESCRIPTOR_PROJECTION_FREEZE_PASS")


if __name__ == "__main__":
    main()
