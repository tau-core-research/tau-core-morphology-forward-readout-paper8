#!/usr/bin/env python3
"""Fill concrete kernel-observable candidates for the S4G75 repair packet.

The filled values are residual-blind and source-constrained, but not all are
accepted direct measurements.  Direct S4G/SPARC fields are marked separately
from formula-conditional bridge candidates.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_kernel_observable_fill_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda value: f"{value:.6g}")
        else:
            display[col] = display[col].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def finite(value: object) -> bool:
    try:
        return pd.notna(value) and float(value) > 0
    except (TypeError, ValueError):
        return False


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def tail_values(row: pd.Series) -> tuple[float, float, str, str]:
    scale = float(row["scale_radius_kpc"])
    rhi = float(row["RHI_kpc"]) if finite(row["RHI_kpc"]) else 0.0
    rdisk = float(row["Rdisk_kpc"]) if finite(row["Rdisk_kpc"]) else scale
    if rhi > 0:
        cutoff = rhi
        inner = min(max(2.0 * scale, rdisk), 0.65 * cutoff)
        inner = max(inner, 1.05 * scale)
        status = "SOURCE_CONSTRAINED_FORMULA_CANDIDATE"
        provenance = "tail_cutoff_from_SPARC_RHI;tail_inner_from_predeclared_disk_to_HI_transition_rule"
    else:
        cutoff = 6.0 * scale
        inner = 2.0 * scale
        status = "FORMULA_CONDITIONAL_FALLBACK_NO_RHI"
        provenance = "tail_inner_cutoff_from_predeclared_scale_multiple_no_RHI"
    return inner, max(cutoff, inner * 1.25), status, provenance


def compact_support(row: pd.Series) -> tuple[float, str, str]:
    if finite(row["bar_radius_kpc"]):
        return (
            float(row["bar_radius_kpc"]),
            "SOURCE_DERIVED_COMPACT_PROXY_FROM_S4G_BAR_RADIUS",
            "S4G_bar_radius_kpc_used_as_compact_support_proxy",
        )
    if finite(row["Reff_kpc"]):
        return (
            float(row["Reff_kpc"]),
            "SOURCE_CONSTRAINED_FORMULA_CANDIDATE",
            "SPARC_Reff_used_as_compact_support_candidate_no_S4G_bulge_radius",
        )
    return (
        float(row["scale_radius_kpc"]),
        "FORMULA_CONDITIONAL_FALLBACK",
        "S4G_scale_radius_used_as_compact_support_fallback",
    )


def thickness_ratio(row: pd.Series) -> tuple[float, str, str]:
    inc = float(row["sparc_inclination_deg"])
    rhi = float(row["RHI_kpc"]) if finite(row["RHI_kpc"]) else 0.0
    scale = float(row["scale_radius_kpc"])
    hi_ratio = rhi / scale if rhi > 0 and scale > 0 else 0.0
    components = str(row.get("s4g_model_components", ""))
    disk_source = str(row.get("s4g_disk_component_source", ""))

    if "Z" in components or "edgedisk" in disk_source:
        value = 0.22
        return (
            value,
            "SOURCE_CONSTRAINED_EDGE_DISK_CANDIDATE",
            "S4G_edge_disk_component_supports_thick_flared_candidate_h_over_rs",
        )

    base = 0.08
    inc_boost = 0.06 if inc >= 75 else 0.03 if inc >= 65 else 0.0
    hi_boost = clamp(0.01 * hi_ratio, 0.0, 0.10)
    value = clamp(base + inc_boost + hi_boost, 0.08, 0.28)
    return (
        value,
        "SOURCE_CONSTRAINED_FORMULA_CANDIDATE",
        "predeclared_h_over_rs_from_inclination_and_HI_extent_no_direct_vertical_scale",
    )


def build_fill() -> tuple[pd.DataFrame, pd.DataFrame]:
    review = pd.read_csv(DATA / "s4g75_holdout_repair_review_galaxy_summary.csv")
    s4g = pd.read_csv(DATA / "external_s4g_sparc_observable_candidates.csv")
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv").rename(columns={"Galaxy": "galaxy"})
    audit = pd.read_csv(DATA / "accepted_morphology_manifest_audit.csv")

    table = (
        review.merge(
            s4g[
                [
                    "galaxy",
                    "bar_radius_kpc",
                    "s4g_model_components",
                    "s4g_disk_scale_arcsec",
                    "s4g_bar_radius_arcsec",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
        .merge(
            sparc[["galaxy", "Reff_kpc", "Rdisk_kpc", "MHI_1e9Msun", "RHI_kpc", "D_Mpc", "e_D_Mpc"]],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
        .merge(
            audit[["galaxy", "s4g_disk_component_source"]],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
    )

    rows = []
    for _, row in table.iterrows():
        scale_status = (
            "SOURCE_DERIVED_S4G_SPARC_SCALE"
            if finite(row["scale_radius_kpc"])
            else "MISSING_SCALE_SOURCE"
        )
        tail_inner = tail_cutoff = compact = thickness = None
        tail_status = compact_status = thickness_status = "NOT_APPLICABLE"
        tail_prov = compact_prov = thickness_prov = ""

        if row["formula_family"] == "K_scale_tail_spiral":
            tail_inner, tail_cutoff, tail_status, tail_prov = tail_values(row)
        if row["formula_family"] == "K_compact_finite":
            compact, compact_status, compact_prov = compact_support(row)
        if row["formula_family"] == "K_thick_flared":
            thickness, thickness_status, thickness_prov = thickness_ratio(row)

        distance_frac_error = (
            float(row["e_D_Mpc"]) / float(row["D_Mpc"])
            if finite(row["e_D_Mpc"]) and finite(row["D_Mpc"])
            else None
        )
        rows.append(
            {
                "galaxy": row["galaxy"],
                "split": "holdout",
                "formula_family": row["formula_family"],
                "repair_priority": row["repair_priority"],
                "scale_radius_kpc": row["scale_radius_kpc"],
                "scale_radius_status": scale_status,
                "tail_inner_radius_kpc": tail_inner,
                "tail_cutoff_radius_kpc": tail_cutoff,
                "tail_observable_status": tail_status,
                "compact_support_radius_kpc": compact,
                "compact_observable_status": compact_status,
                "thickness_h_over_rs": thickness,
                "thickness_observable_status": thickness_status,
                "sparc_rhi_kpc": row["RHI_kpc"],
                "sparc_rdisk_kpc": row["Rdisk_kpc"],
                "sparc_reff_kpc": row["Reff_kpc"],
                "sparc_inclination_deg": row["sparc_inclination_deg"],
                "distance_frac_error": distance_frac_error,
                "s4g_model_components": row["s4g_model_components"],
                "s4g_disk_component_source": row["s4g_disk_component_source"],
                "bar_radius_kpc": row["bar_radius_kpc"],
                "kernel_observable_provenance": ";".join(
                    part
                    for part in [
                        "scale_radius_from_S4G_Pipeline4_x_SPARC_distance"
                        if scale_status == "SOURCE_DERIVED_S4G_SPARC_SCALE"
                        else "",
                        tail_prov,
                        compact_prov,
                        thickness_prov,
                    ]
                    if part
                ),
                "accepted_endpoint_ready": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    fill = pd.DataFrame(rows).sort_values(["repair_priority", "formula_family", "galaxy"])
    status_cols = [
        "scale_radius_status",
        "tail_observable_status",
        "compact_observable_status",
        "thickness_observable_status",
    ]
    summary_rows = []
    for col in status_cols:
        for status, sub in fill.groupby(col):
            if status == "NOT_APPLICABLE":
                continue
            summary_rows.append(
                {
                    "observable_status_field": col,
                    "status": status,
                    "n_galaxies": int(len(sub)),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    summary = pd.DataFrame(summary_rows)
    return fill, summary


def write_report(fill: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# S4G75 Kernel-Observable Fill",
        "",
        "This table fills concrete kernel-observable candidates for the S4G75 "
        "holdout repair set using residual-blind S4G/SPARC/HI fields and "
        "predeclared bridge rules. It does not promote endpoint-ready accepted "
        "labels.",
        "",
        "## Status Summary",
        "",
        markdown_table(summary),
        "",
        "## Filled Kernel Observables",
        "",
        markdown_table(
            fill[
                [
                    "galaxy",
                    "formula_family",
                    "scale_radius_kpc",
                    "tail_inner_radius_kpc",
                    "tail_cutoff_radius_kpc",
                    "compact_support_radius_kpc",
                    "thickness_h_over_rs",
                    "tail_observable_status",
                    "compact_observable_status",
                    "thickness_observable_status",
                    "kernel_observable_provenance",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "Concrete means numerically filled. It does not mean accepted. Direct "
        "S4G/SPARC scale values are source-derived; tail, compact, and thickness "
        "fields are source-constrained or formula-conditional candidates unless "
        "a direct source-native morphology measurement is present.",
    ]
    (REPORTS / "s4g75_kernel_observable_fill.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    fill, summary = build_fill()
    fill.to_csv(DATA / "s4g75_kernel_observable_fill.csv", index=False)
    summary.to_csv(DATA / "s4g75_kernel_observable_fill_summary.csv", index=False)
    write_report(fill, summary)
    print("PAPER8_S4G75_KERNEL_OBSERVABLE_FILL_COMPLETE")
    print(fill.to_string(index=False))


if __name__ == "__main__":
    main()
