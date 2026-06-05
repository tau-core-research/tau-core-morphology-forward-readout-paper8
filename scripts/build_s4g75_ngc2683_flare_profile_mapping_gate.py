#!/usr/bin/env python3
"""Build a residual-blind flare-profile mapping gate for NGC2683.

The literature source for NGC2683 gives a radial HI flare profile, while the
current executable thick/flared readout shell uses a scalar h/Rs proxy.  This
gate records the source-native profile and the exact points where it can be
mapped without endpoint residuals.  It deliberately does not authorize endpoint
scoring, because the profile-to-kernel readout rule is not implemented yet.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
TPG_RESULTS = Path("/Users/jolcsak/Projects/TPG/results/tau_core_projection_v1")
CLAIM_BOUNDARY = "s4g75_ngc2683_flare_profile_mapping_gate_not_endpoint"
GALAXY = "NGC2683"

SOURCE_URL = "https://arxiv.org/abs/1512.07058"
SOURCE_LABEL = "Vollmer_Nehlig_Ibata_2016_NGC2683_HI_flare"

H_START_KPC = 0.5
R_START_KPC = 9.0
H_MAX_KPC = 4.0
R_MAX_KPC = 15.0
R_SAT_END_KPC = 22.0
RING_VERTICAL_OFFSET_KPC = 1.3


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


def flare_height(radius_kpc: float) -> tuple[float | None, str, str]:
    if radius_kpc < R_START_KPC:
        return H_START_KPC, "INNER_THIN_DISK_HEIGHT_REPRESENTATIVE", "PROFILE_MAPPED"
    if radius_kpc <= R_MAX_KPC:
        scale = (R_MAX_KPC - R_START_KPC) / math.log(H_MAX_KPC / H_START_KPC)
        height = H_START_KPC * math.exp((radius_kpc - R_START_KPC) / scale)
        return height, "EXPONENTIAL_FLARE_RISE", "PROFILE_MAPPED"
    if radius_kpc <= R_SAT_END_KPC:
        return H_MAX_KPC, "SATURATED_FLARE_PLATEAU", "PROFILE_MAPPED"
    return None, "POST_SATURATION_DECREASE_UNSPECIFIED", "MAPPING_REQUIRED_AFTER_22_KPC"


def build_gate() -> tuple[pd.DataFrame, pd.DataFrame]:
    points = pd.read_csv(TPG_RESULTS / "tau_rotation_curve_frozen_proxy_runner_v0_points.csv")
    fill = pd.read_csv(DATA / "s4g75_promoted_kernel_observable_fill.csv")
    hit = pd.read_csv(DATA / "s4g75_literature_kernel_source_hits.csv")

    galaxy_points = points.loc[points["galaxy"] == GALAXY].copy()
    row = fill.loc[fill["galaxy"] == GALAXY].iloc[0]
    source_hit = hit.loc[hit["galaxy"] == GALAXY].iloc[0]
    scale_radius = float(row["scale_radius_kpc"])
    scalar_proxy = float(row["thickness_h_over_rs"])
    profile_scale = (R_MAX_KPC - R_START_KPC) / math.log(H_MAX_KPC / H_START_KPC)

    rows = []
    for _, point in galaxy_points.iterrows():
        radius = float(point["r"])
        height, region, status = flare_height(radius)
        mapped = height is not None
        rows.append(
            {
                "galaxy": GALAXY,
                "radius_kpc": radius,
                "vobs": point["vobs"],
                "split": point["split"],
                "scale_radius_kpc": scale_radius,
                "current_scalar_h_over_rs_proxy": scalar_proxy,
                "flare_height_kpc": height,
                "flare_h_over_rs_profile": height / scale_radius if mapped else None,
                "mapping_region": region,
                "mapping_status": status,
                "source_label": SOURCE_LABEL,
                "source_url": SOURCE_URL,
                "source_literature_status": source_hit["literature_status"],
                "source_numeric_kernel_fields": source_hit["numeric_kernel_fields"],
                "profile_exponential_scale_kpc": profile_scale,
                "ring_vertical_offset_kpc": RING_VERTICAL_OFFSET_KPC,
                "strict_kernel_ready": False,
                "endpoint_scores_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    gate = pd.DataFrame(rows)
    mapped = gate.loc[gate["mapping_status"] == "PROFILE_MAPPED"]
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "n_rotation_points": len(gate),
                "n_profile_mapped_points": len(mapped),
                "n_unmapped_post_saturation_points": int(
                    (gate["mapping_status"] == "MAPPING_REQUIRED_AFTER_22_KPC").sum()
                ),
                "scale_radius_kpc": scale_radius,
                "current_scalar_h_over_rs_proxy": scalar_proxy,
                "mapped_profile_h_over_rs_min": mapped["flare_h_over_rs_profile"].min(),
                "mapped_profile_h_over_rs_median": mapped["flare_h_over_rs_profile"].median(),
                "mapped_profile_h_over_rs_max": mapped["flare_h_over_rs_profile"].max(),
                "profile_exponential_scale_kpc": profile_scale,
                "endpoint_scores_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return gate, summary


def write_report(gate: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    row = summary.iloc[0]
    lines = [
        "# NGC2683 Flare-Profile Mapping Gate",
        "",
        "This gate maps the source-native NGC2683 HI flare profile onto the "
        "rotation-curve radii without using endpoint residuals. It does not "
        "authorize endpoint scoring.",
        "",
        "## Source Profile",
        "",
        f"Source: {SOURCE_LABEL}, {SOURCE_URL}.",
        "",
        "The source profile used here is:",
        "",
        "```text",
        "H(R) = 0.5 kpc for the inner representative region before R = 9 kpc",
        "H(R) rises exponentially from 0.5 kpc at R = 9 kpc to 4 kpc at R = 15 kpc",
        "H(R) remains 4 kpc until R = 22 kpc",
        "after R = 22 kpc the source says the flare decreases but does not provide a single executable formula",
        "outer ring vertical offset = 1.3 kpc",
        "```",
        "",
        "## Verdict",
        "",
        f"Rotation points checked: {int(row['n_rotation_points'])}.",
        f"Profile-mapped points: {int(row['n_profile_mapped_points'])}.",
        f"Unmapped post-saturation points: {int(row['n_unmapped_post_saturation_points'])}.",
        "",
        "The direct profile is stronger than the old scalar proxy, but it is not "
        "yet an endpoint override. The missing step is a residual-blind "
        "profile-to-thick/flared-kernel readout rule.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Point-Level Mapping",
        "",
        markdown_table(
            gate[
                [
                    "radius_kpc",
                    "current_scalar_h_over_rs_proxy",
                    "flare_height_kpc",
                    "flare_h_over_rs_profile",
                    "mapping_region",
                    "mapping_status",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "The NGC2683 literature source provides a direct flare profile. This pass "
        "does not convert it into an accepted scalar h/Rs value and does not "
        "score an endpoint. Radii beyond 22 kpc remain unmapped because the "
        "source states a decrease but does not provide a unique executable "
        "post-saturation profile.",
        "",
    ]
    (REPORTS / "s4g75_ngc2683_flare_profile_mapping_gate.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    gate, summary = build_gate()
    gate.to_csv(DATA / "s4g75_ngc2683_flare_profile_mapping_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc2683_flare_profile_mapping_summary.csv", index=False)
    write_report(gate, summary)
    print(f"wrote {DATA / 's4g75_ngc2683_flare_profile_mapping_gate.csv'}")
    print(f"wrote {DATA / 's4g75_ngc2683_flare_profile_mapping_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_ngc2683_flare_profile_mapping_gate.md'}")


if __name__ == "__main__":
    main()
