#!/usr/bin/env python3
"""Audit radial zones for the NGC4013 warp/vertical-overlay endpoint."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4013_warp_vertical_overlay_radial_zone_audit_not_full_profile_solution"


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


def zone_for_radius(radius: float, r_warp: float, r_outer: float) -> str:
    if radius < r_warp:
        return "inner_pre_warp_window"
    if radius < r_outer:
        return "transition_warp_window"
    return "outer_overlay_window"


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    points = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_points.csv")
    manifest = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_manifest.csv").iloc[0]
    r_warp = float(manifest["r_warp_kpc"])
    r_outer = float(manifest["r_outer_kpc"])

    points = points.copy()
    points["radial_zone"] = points["r"].map(
        lambda value: zone_for_radius(float(value), r_warp, r_outer)
    )
    points["wvo_minus_tpg"] = points["v_wvo_endpoint"] - points["v_v6"]
    points["wvo_residual"] = points["v_wvo_endpoint"] - points["vobs"]
    points["tpg_residual"] = points["v_v6"] - points["vobs"]

    rows = []
    for zone, sub in points.groupby("radial_zone", sort=False):
        rows.append(
            {
                "galaxy": "NGC4013",
                "radial_zone": zone,
                "r_min_kpc": float(sub["r"].min()),
                "r_max_kpc": float(sub["r"].max()),
                "n_points": int(len(sub)),
                "mean_K_wvo": float(sub["K_wvo"].mean()),
                "mean_wvo_attenuation": float(sub["wvo_attenuation"].mean()),
                "rmse_tpg_v6": rmse(sub, "v_v6"),
                "rmse_warp_vertical_overlay": rmse(sub, "v_wvo_endpoint"),
                "wvo_minus_tpg_rmse": rmse(sub, "v_wvo_endpoint") - rmse(sub, "v_v6"),
                "mean_abs_wvo_shift_kms": float(sub["wvo_minus_tpg"].abs().mean()),
                "zone_interpretation": {
                    "inner_pre_warp_window": "warp/overlay kernel inactive; this endpoint does not address inner structure",
                    "transition_warp_window": "source warp window turns on between R_w and R_o",
                    "outer_overlay_window": "warp/vertical-overlay kernel active; endpoint lane should act here",
                }[zone],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    zone_scores = pd.DataFrame(rows)

    inner = zone_scores.loc[zone_scores["radial_zone"] == "inner_pre_warp_window"].iloc[0]
    active = zone_scores.loc[
        zone_scores["radial_zone"].isin(["transition_warp_window", "outer_overlay_window"])
    ]
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "r_warp_kpc": r_warp,
                "r_outer_kpc": r_outer,
                "inner_n_points": int(inner["n_points"]),
                "inner_K_wvo_mean": float(inner["mean_K_wvo"]),
                "inner_rmse_warp_vertical_overlay": float(inner["rmse_warp_vertical_overlay"]),
                "inner_rmse_tpg_v6": float(inner["rmse_tpg_v6"]),
                "inner_wvo_minus_tpg_rmse": float(inner["wvo_minus_tpg_rmse"]),
                "active_window_points": int(active["n_points"].sum()),
                "active_window_weighted_wvo_minus_tpg_rmse": float(
                    (active["wvo_minus_tpg_rmse"] * active["n_points"]).sum()
                    / active["n_points"].sum()
                ),
                "outer_lane_status": "WARP_VERTICAL_OVERLAY_ENDPOINT_IS_OUTER_LANE_NOT_FULL_PROFILE",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    points.to_csv(DATA / "ngc4013_warp_vertical_overlay_radial_zone_points.csv", index=False)
    zone_scores.to_csv(
        DATA / "ngc4013_warp_vertical_overlay_radial_zone_scores.csv", index=False
    )
    summary.to_csv(
        DATA / "ngc4013_warp_vertical_overlay_radial_zone_summary.csv", index=False
    )

    report = [
        "# NGC4013 Warp/Vertical-Overlay Radial-Zone Audit",
        "",
        "This audit separates the caveated NGC4013 endpoint into inner, transition,",
        "and outer radial zones. It preserves whether the source-windowed readout",
        "acts only where its source morphology is active.",
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
        f"Before the source-frozen warp onset \(R={r_warp:.3g}\,{{\\rm kpc}}\),",
        "the warp/vertical-overlay kernel is inactive and the curve equals the TPG",
        "carrier. Improvement outside that window supports the source-lane reading;",
        "a remaining inner mismatch would require a separately frozen inner",
        "disk/core/readout component.",
        "",
    ]
    (REPORTS / "ngc4013_warp_vertical_overlay_radial_zone_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print()
    print(zone_scores.to_string(index=False))


if __name__ == "__main__":
    main()
