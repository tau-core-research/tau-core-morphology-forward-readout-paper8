#!/usr/bin/env python3
"""Build the S4G75 promoted kernel-observable fill table.

This table starts from the previous residual-blind filled candidates and
overrides only rows with direct source-native S4G kernel measurements.  It keeps
the original filled table intact as a control.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_promoted_kernel_observable_fill_not_endpoint"


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


def build_promoted_fill() -> tuple[pd.DataFrame, pd.DataFrame]:
    fill = pd.read_csv(DATA / "s4g75_kernel_observable_fill.csv")
    direct = pd.read_csv(DATA / "s4g75_direct_kernel_measurements.csv")
    out = fill.copy()
    out["promotion_override_status"] = "NO_DIRECT_KERNEL_OVERRIDE"
    out["promotion_override_source"] = ""
    out["promotion_override_previous_value"] = None
    out["promotion_override_new_value"] = None

    for _, row in direct.iterrows():
        if not str(row["direct_measurement_status"]).startswith("DIRECT_"):
            continue
        mask = out["galaxy"] == row["galaxy"]
        if not mask.any():
            continue
        if row["kernel_parameter_filled"] == "compact_support_radius_kpc":
            previous = out.loc[mask, "compact_support_radius_kpc"].iloc[0]
            out.loc[mask, "compact_support_radius_kpc"] = row["value_kpc"]
            out.loc[mask, "compact_observable_status"] = row["direct_measurement_status"]
        elif row["kernel_parameter_filled"] == "thickness_h_over_rs":
            previous = out.loc[mask, "thickness_h_over_rs"].iloc[0]
            out.loc[mask, "thickness_h_over_rs"] = row["dimensionless_value"]
            out.loc[mask, "thickness_observable_status"] = row["direct_measurement_status"]
        else:
            continue
        out.loc[mask, "promotion_override_status"] = "DIRECT_KERNEL_MEASUREMENT_OVERRIDE"
        out.loc[mask, "promotion_override_source"] = row["source_component"]
        out.loc[mask, "promotion_override_previous_value"] = previous
        out.loc[mask, "promotion_override_new_value"] = (
            row["dimensionless_value"]
            if row["kernel_parameter_filled"] == "thickness_h_over_rs"
            else row["value_kpc"]
        )
        out.loc[mask, "accepted_endpoint_ready"] = True
        out.loc[mask, "kernel_observable_provenance"] = (
            out.loc[mask, "kernel_observable_provenance"].astype(str)
            + ";direct_kernel_measurement_from_S4G_Table7:"
            + str(row["source_component"])
        )
    out["claim_boundary"] = CLAIM_BOUNDARY

    summary = (
        out.groupby(
            [
                "formula_family",
                "promotion_override_status",
                "compact_observable_status",
                "thickness_observable_status",
                "tail_observable_status",
            ],
            as_index=False,
        )
        .agg(
            n_galaxies=("galaxy", "count"),
            galaxies=("galaxy", lambda values: ";".join(values)),
        )
    )
    summary["claim_boundary"] = CLAIM_BOUNDARY
    return out, summary


def write_report(promoted: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    overrides = promoted.loc[promoted["promotion_override_status"] == "DIRECT_KERNEL_MEASUREMENT_OVERRIDE"]
    lines = [
        "# S4G75 Promoted Kernel-Observable Fill",
        "",
        "This table keeps the original filled-kernel candidates as a control and "
        "overrides only rows where S4G Table 7 supplies a direct source-native "
        "kernel measurement. It is not an endpoint result.",
        "",
        "## Verdict",
        "",
        f"Rows with direct kernel overrides: {len(overrides)}.",
        "",
        "## Override Rows",
        "",
        markdown_table(
            overrides[
                [
                    "galaxy",
                    "formula_family",
                    "promotion_override_source",
                    "promotion_override_previous_value",
                    "promotion_override_new_value",
                    "compact_support_radius_kpc",
                    "thickness_h_over_rs",
                ]
            ]
        ),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "Only direct S4G Table 7 kernel measurements are promoted. Scale-tail "
        "RHI-only rows remain conditional because no direct outer-transition "
        "profile has been supplied.",
        "",
    ]
    (REPORTS / "s4g75_promoted_kernel_observable_fill.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    promoted, summary = build_promoted_fill()
    promoted.to_csv(DATA / "s4g75_promoted_kernel_observable_fill.csv", index=False)
    summary.to_csv(DATA / "s4g75_promoted_kernel_observable_fill_summary.csv", index=False)
    write_report(promoted, summary)
    print(f"wrote {DATA / 's4g75_promoted_kernel_observable_fill.csv'}")
    print(f"wrote {DATA / 's4g75_promoted_kernel_observable_fill_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_promoted_kernel_observable_fill.md'}")


if __name__ == "__main__":
    main()
