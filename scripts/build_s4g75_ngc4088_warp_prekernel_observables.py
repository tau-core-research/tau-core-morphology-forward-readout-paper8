#!/usr/bin/env python3
"""Build residual-blind NGC4088 warp/asymmetry pre-kernel observables.

This step converts source-native WHISP/SPARC quantities into dimensionless
pre-kernel observables.  It is a consistency and formula-development layer, not
an endpoint kernel: the radial warp/asymmetry profile is still missing.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_ngc4088_warp_prekernel_observables_not_endpoint"


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


def angular_radius_kpc(diameter_arcmin: float, distance_mpc: float) -> float:
    radius_rad = math.radians(diameter_arcmin / 2.0 / 60.0)
    return 1000.0 * distance_mpc * math.tan(radius_rad)


def build_observables() -> tuple[pd.DataFrame, pd.DataFrame]:
    gate = pd.read_csv(DATA / "s4g75_ngc4088_warp_asymmetry_extraction_gate.csv").iloc[0]
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    s4g = pd.read_csv(DATA / "external_s4g_sparc_observable_candidates.csv")
    sparc_row = sparc.loc[sparc["Galaxy"] == "NGC4088"].iloc[0]
    s4g_row = s4g.loc[s4g["galaxy"] == "NGC4088"].iloc[0]

    hi_radius_from_whisp_kpc = angular_radius_kpc(
        float(gate["source_native_hi_diameter_arcmin"]),
        float(sparc_row["D_Mpc"]),
    )
    sparc_rhi_kpc = float(sparc_row["RHI_kpc"])
    sparc_rdisk_kpc = float(sparc_row["Rdisk_kpc"])
    s4g_scale_radius_kpc = float(s4g_row["scale_radius_kpc"])
    hi_consistency_fraction = (
        hi_radius_from_whisp_kpc - sparc_rhi_kpc
    ) / sparc_rhi_kpc
    rows = [
        {
            "galaxy": "NGC4088",
            "observable": "R_HI_from_WHISP_diameter_kpc",
            "value": hi_radius_from_whisp_kpc,
            "unit": "kpc",
            "source": "Verheijen_Sancisi_2001_HI_diameter_x_SPARC_distance",
            "interpretation": "source-native HI radial extent reconstructed from angular diameter",
        },
        {
            "galaxy": "NGC4088",
            "observable": "R_HI_over_SPARC_Rdisk",
            "value": hi_radius_from_whisp_kpc / sparc_rdisk_kpc,
            "unit": "dimensionless",
            "source": "WHISP_HI_diameter;SPARC_Rdisk",
            "interpretation": "outer HI extent normalized by SPARC disk scale",
        },
        {
            "galaxy": "NGC4088",
            "observable": "R_HI_over_S4G_scale_radius",
            "value": hi_radius_from_whisp_kpc / s4g_scale_radius_kpc,
            "unit": "dimensionless",
            "source": "WHISP_HI_diameter;S4G_scale_radius",
            "interpretation": "outer HI extent normalized by S4G disk scale",
        },
        {
            "galaxy": "NGC4088",
            "observable": "WHISP_vs_SPARC_RHI_fractional_difference",
            "value": hi_consistency_fraction,
            "unit": "dimensionless",
            "source": "WHISP_HI_diameter;SPARC_RHI",
            "interpretation": "catalog consistency check, not a fitted parameter",
        },
        {
            "galaxy": "NGC4088",
            "observable": "qualitative_warp_asymmetry_score",
            "value": (
                float(bool(gate["warp_presence_flag"]))
                + float(bool(gate["pv_asymmetry_flag"]))
                + float(bool(gate["pa_asymmetry_flag"]))
            )
            / 3.0,
            "unit": "dimensionless",
            "source": "Verheijen_Sancisi_2001_qualitative_flags",
            "interpretation": "binary evidence score for formula development only",
        },
    ]
    obs = pd.DataFrame(rows)
    obs["endpoint_scores_allowed"] = False
    obs["endpoint_scores_computed"] = False
    obs["claim_boundary"] = CLAIM_BOUNDARY
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "n_prekernel_observables": len(obs),
                "hi_radius_from_whisp_kpc": hi_radius_from_whisp_kpc,
                "sparc_rhi_kpc": sparc_rhi_kpc,
                "whisp_vs_sparc_rhi_fractional_difference": hi_consistency_fraction,
                "profile_kernel_status": "PREKERNEL_READY_PROFILE_KERNEL_BLOCKED",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return obs, summary


def write_report(obs: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Warp Pre-Kernel Observables",
        "",
        "This report normalizes source-native NGC4088 warp/asymmetry evidence into "
        "dimensionless pre-kernel observables. It does not construct an endpoint "
        "closure-source kernel.",
        "",
        "## Verdict",
        "",
        "The WHISP HI diameter combined with the SPARC distance reconstructs the "
        "outer HI scale consistently with SPARC RHI. This supports a "
        "residual-blind normalization layer for a future warp/asymmetry readout. "
        "The radial warp profile and closure-source mapping remain missing.",
        "",
        "## Observables",
        "",
        markdown_table(obs[["observable", "value", "unit", "source", "interpretation"]]),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "These are pre-kernel observables for formula development. They are not "
        "accepted kernel observables and cannot be used for endpoint scoring "
        "until a residual-blind radial warp/asymmetry profile and mapping rule "
        "are supplied.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_warp_prekernel_observables.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    obs, summary = build_observables()
    obs.to_csv(DATA / "s4g75_ngc4088_warp_prekernel_observables.csv", index=False)
    summary.to_csv(
        DATA / "s4g75_ngc4088_warp_prekernel_observable_summary.csv",
        index=False,
    )
    write_report(obs, summary)
    print(f"wrote {DATA / 's4g75_ngc4088_warp_prekernel_observables.csv'}")
    print(f"wrote {DATA / 's4g75_ngc4088_warp_prekernel_observable_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_ngc4088_warp_prekernel_observables.md'}")


if __name__ == "__main__":
    main()
