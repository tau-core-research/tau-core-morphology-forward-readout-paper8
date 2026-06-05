#!/usr/bin/env python3
"""Audit radial zones for the accepted NGC5907 projection endpoint."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc5907_projection_radial_zone_audit_not_full_profile_solution"


def rmse(df: pd.DataFrame, pred_col: str) -> float:
    return float(((df[pred_col] - df["vobs"]).pow(2).mean()) ** 0.5)


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
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def zone_for_radius(radius: float, r_in: float, r_out: float) -> str:
    if radius < r_in:
        return "inner_pre_projection_window"
    if radius < r_out:
        return "transition_projection_window"
    return "outer_full_projection_window"


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    points = pd.read_csv(DATA / "ngc5907_projection_accepted_endpoint_points.csv")
    manifest = pd.read_csv(DATA / "ngc5907_projection_accepted_endpoint_manifest.csv").iloc[0]
    r_in = float(manifest["r_in_kpc"])
    r_out = float(manifest["r_out_kpc"])
    points = points.copy()
    points["radial_zone"] = points["r"].map(lambda value: zone_for_radius(float(value), r_in, r_out))
    points["projection_minus_tpg"] = points["v_projection_accepted"] - points["v_v6"]
    points["projection_residual"] = points["v_projection_accepted"] - points["vobs"]
    points["tpg_residual"] = points["v_v6"] - points["vobs"]

    rows = []
    for zone, sub in points.groupby("radial_zone", sort=False):
        rows.append(
            {
                "galaxy": "NGC5907",
                "radial_zone": zone,
                "r_min_kpc": float(sub["r"].min()),
                "r_max_kpc": float(sub["r"].max()),
                "n_points": int(len(sub)),
                "mean_projection_kernel": float(sub["projection_kernel"].mean()),
                "rmse_tpg_v6": rmse(sub, "v_v6"),
                "rmse_projection_accepted": rmse(sub, "v_projection_accepted"),
                "projection_minus_tpg_rmse": rmse(sub, "v_projection_accepted")
                - rmse(sub, "v_v6"),
                "mean_abs_projection_shift_kms": float(sub["projection_minus_tpg"].abs().mean()),
                "zone_interpretation": {
                    "inner_pre_projection_window": "projection kernel inactive; inner mismatch is outside this endpoint lane",
                    "transition_projection_window": "source-windowed projection kernel turns on",
                    "outer_full_projection_window": "projection kernel fully active",
                }[zone],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    zone_scores = pd.DataFrame(rows)

    inner = zone_scores.loc[
        zone_scores["radial_zone"] == "inner_pre_projection_window"
    ].iloc[0]
    active = zone_scores.loc[
        zone_scores["radial_zone"].isin(
            ["transition_projection_window", "outer_full_projection_window"]
        )
    ]
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC5907",
                "r_in_kpc": r_in,
                "r_out_kpc": r_out,
                "inner_n_points": int(inner["n_points"]),
                "inner_projection_kernel_mean": float(inner["mean_projection_kernel"]),
                "inner_rmse_projection_accepted": float(inner["rmse_projection_accepted"]),
                "inner_rmse_tpg_v6": float(inner["rmse_tpg_v6"]),
                "inner_projection_minus_tpg_rmse": float(inner["projection_minus_tpg_rmse"]),
                "active_window_points": int(active["n_points"].sum()),
                "active_window_weighted_projection_minus_tpg_rmse": float(
                    (active["projection_minus_tpg_rmse"] * active["n_points"]).sum()
                    / active["n_points"].sum()
                ),
                "outer_lane_status": "ACCEPTED_PROJECTION_ENDPOINT_IS_OUTER_LANE_NOT_FULL_PROFILE",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    points.to_csv(DATA / "ngc5907_projection_radial_zone_points.csv", index=False)
    zone_scores.to_csv(DATA / "ngc5907_projection_radial_zone_scores.csv", index=False)
    summary.to_csv(DATA / "ngc5907_projection_radial_zone_summary.csv", index=False)

    report = [
        "# NGC5907 Projection Radial-Zone Audit",
        "",
        "This audit separates the accepted projection endpoint into inner, transition,",
        "and outer radial zones. It preserves the negative result that the inner",
        "profile mismatch is not addressed by the frozen projection lane.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Zone Scores",
        "",
        markdown_table(zone_scores),
        "",
        "## Interpretation",
        "",
        "The accepted projection endpoint is an outer/projection-lane control. Before",
        f"the source-frozen warp onset \(R={r_in:.3g}\,{{\\rm kpc}}\), the projection",
        "kernel is inactive, so the accepted projection curve is identical to the",
        "TPG carrier. The large inner mismatch is therefore a documented limitation,",
        "not a hidden fitting success. A full-profile NGC5907 model would require a",
        "separately frozen inner disk/core/readout component before scoring.",
        "",
    ]
    (REPORTS / "ngc5907_projection_radial_zone_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print()
    print(zone_scores.to_string(index=False))


if __name__ == "__main__":
    main()
