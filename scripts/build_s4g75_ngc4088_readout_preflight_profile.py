#!/usr/bin/env python3
"""Export an NGC4088-specific readout preflight profile.

This script evaluates the filled NGC4088 warp closure-source normalization
candidate on the local SPARC/TPG point radii. It is a profile export only:
no amplitude fitting, no endpoint score, and no validation claim are made.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import run_source_native_readout_formula_endpoint as src


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_ngc4088_readout_preflight_profile_not_endpoint"
GALAXY = "NGC4088"


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.6g}")
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def build_profile() -> tuple[pd.DataFrame, pd.DataFrame]:
    points, _labels = src.load_points()
    ngc = points.loc[points["galaxy"] == GALAXY].copy().sort_values("r").reset_index(drop=True)
    candidate = pd.read_csv(
        DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_profile.csv"
    )

    # Use the gentler p=1 branch as the first preflight export and carry p=2
    # alongside it as an explicit sensitivity column.
    p1 = candidate.loc[candidate["turn_on_power_control"] == 1.0].copy()
    p2 = candidate.loc[candidate["turn_on_power_control"] == 2.0].copy()
    r_hi_kpc = float(p1["radius_kpc_candidate"].max())

    def interp_delta(sub: pd.DataFrame, radii: pd.Series) -> np.ndarray:
        return np.interp(
            radii.to_numpy(dtype=float),
            sub["radius_kpc_candidate"].to_numpy(dtype=float),
            sub["delta_v2_warp_candidate"].to_numpy(dtype=float),
            left=0.0,
            right=float(sub["delta_v2_warp_candidate"].iloc[-1]),
        )

    ngc["x_R_over_RHI"] = ngc["r"] / r_hi_kpc
    ngc["delta_v2_warp_candidate_p1"] = interp_delta(p1, ngc["r"])
    ngc["delta_v2_warp_candidate_p2"] = interp_delta(p2, ngc["r"])
    ngc["v_warp_candidate_p1"] = np.sqrt(
        np.maximum(ngc["vn"].to_numpy(dtype=float) ** 2 + ngc["delta_v2_warp_candidate_p1"], 0.0)
    )
    ngc["v_warp_candidate_p2"] = np.sqrt(
        np.maximum(ngc["vn"].to_numpy(dtype=float) ** 2 + ngc["delta_v2_warp_candidate_p2"], 0.0)
    )
    ngc["uses_vobs_for_generation"] = False
    ngc["endpoint_scores_allowed"] = False
    ngc["endpoint_scores_computed"] = False
    ngc["claim_boundary"] = CLAIM_BOUNDARY

    export = ngc[
        [
            "galaxy",
            "split",
            "r",
            "x_R_over_RHI",
            "vn",
            "v_v6",
            "v_mond",
            "vobs",
            "delta_v2_warp_candidate_p1",
            "delta_v2_warp_candidate_p2",
            "v_warp_candidate_p1",
            "v_warp_candidate_p2",
            "uses_vobs_for_generation",
            "endpoint_scores_allowed",
            "endpoint_scores_computed",
            "claim_boundary",
        ]
    ].copy()

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "n_points": len(export),
                "r_hi_kpc": r_hi_kpc,
                "max_delta_v2_p1": float(export["delta_v2_warp_candidate_p1"].max()),
                "max_delta_v2_p2": float(export["delta_v2_warp_candidate_p2"].max()),
                "max_v_candidate_p1": float(export["v_warp_candidate_p1"].max()),
                "max_v_candidate_p2": float(export["v_warp_candidate_p2"].max()),
                "profile_status": "PREDECLARED_READOUT_EXPORT_NOT_ENDPOINT",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return export, summary


def write_report(export: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# NGC4088 Readout Preflight Profile",
        "",
        "This report exports the NGC4088-specific readout candidate on the local",
        "SPARC/TPG point radii. It is not a fit or endpoint score.",
        "",
        "## Verdict",
        "",
        "The filled NGC4088 source-side lane can now be evaluated as a concrete",
        "radial candidate profile. This is still a profile export only: it does not",
        "decide whether the law is correct or whether it beats any baseline.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## First Rows",
        "",
        markdown_table(export.head(12)),
        "",
        "## Claim Boundary",
        "",
        "The observed velocity columns are carried only as contextual source-package",
        "fields. They are not used to generate the candidate profile in this",
        "artifact, and this report does not compute an endpoint score or a fit",
        "quality judgment.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_readout_preflight_profile.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    export, summary = build_profile()
    export.to_csv(DATA / "s4g75_ngc4088_readout_preflight_profile.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_readout_preflight_summary.csv", index=False)
    write_report(export, summary)
    print("PAPER8_NGC4088_READOUT_PREFLIGHT_PROFILE_COMPLETE")


if __name__ == "__main__":
    main()
