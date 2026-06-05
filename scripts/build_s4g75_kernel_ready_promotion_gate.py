#!/usr/bin/env python3
"""Build the S4G75 kernel-ready promotion gate.

The gate asks whether a source-rich filled kernel observable is constrained by
the same source-native morphology feature used by its formula family.  It does
not rerun endpoint scores and does not promote accepted labels.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_kernel_ready_promotion_gate_not_endpoint"


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


def promotion_decision(row: pd.Series) -> tuple[str, str, bool, bool]:
    driver = row["observable_driver_type"]
    status = row["kernel_specific_source_status"]
    direct_status = str(row.get("direct_measurement_status", ""))

    if direct_status.startswith("DIRECT_"):
        return (
            "KERNEL_READY_STRICT",
            f"{direct_status} supplies the source-native kernel parameter used by the formula family",
            True,
            True,
        )

    if driver == "tail_inner_cutoff_candidate":
        if status == "DIRECT_OUTER_DISK_TRANSITION_READY":
            return (
                "KERNEL_READY_STRICT",
                "direct outer-disk transition/break/truncation support constrains the tail kernel",
                True,
                True,
            )
        if status == "PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING":
            return (
                "KERNEL_READY_CONDITIONAL",
                "SPARC HI extent supports a tail cutoff candidate but does not directly constrain the transition profile",
                False,
                False,
            )
        return (
            "KERNEL_PROXY_ONLY",
            "tail kernel lacks direct HI/outer-disk transition support",
            False,
            False,
        )

    if driver == "compact_support_candidate":
        if status == "DIRECT_COMPACT_OR_BAR_SUPPORT_READY":
            return (
                "KERNEL_READY_STRICT",
                "direct compact/bar component support constrains the compact kernel",
                True,
                True,
            )
        if status in {
            "PARTIAL_COMPACT_COMPONENT_READY_RADIUS_MISSING",
            "PARTIAL_REFF_READY_COMPACT_RADIUS_MISSING",
        }:
            return (
                "KERNEL_READY_CONDITIONAL",
                "compact component or Reff support exists but direct compact-support radius is missing",
                False,
                False,
            )
        return (
            "KERNEL_PROXY_ONLY",
            "compact kernel lacks direct compact-component support",
            False,
            False,
        )

    if driver == "thickness_h_over_rs_candidate":
        if status == "DIRECT_VERTICAL_GEOMETRY_READY":
            return (
                "KERNEL_READY_STRICT",
                "direct vertical scale height/flare/warp evidence constrains the thick/flared kernel",
                True,
                True,
            )
        if status == "PARTIAL_EDGE_DISK_VERTICAL_EVIDENCE_READY":
            return (
                "KERNEL_READY_CONDITIONAL",
                "edge-disk component supports vertical geometry but does not yet provide a measured h/Rs or flare profile",
                False,
                False,
            )
        return (
            "KERNEL_PROXY_ONLY",
            "thick/flared kernel lacks direct vertical scale height, flare, warp, or gas-plane thickness evidence",
            False,
            False,
        )

    return (
        "KERNEL_PROXY_ONLY",
        "no kernel-specific promotion rule is available for this observable driver",
        False,
        False,
    )


def build_gate() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    availability = pd.read_csv(DATA / "s4g75_source_native_availability_audit.csv")
    measurements_path = DATA / "s4g75_direct_kernel_measurements.csv"
    if measurements_path.exists():
        measurements = pd.read_csv(measurements_path)[
            [
                "galaxy",
                "observable_driver_type",
                "direct_measurement_status",
                "kernel_parameter_filled",
                "value_kpc",
                "secondary_value_kpc",
                "dimensionless_value",
                "source_component",
            ]
        ]
        availability = availability.merge(
            measurements,
            on=["galaxy", "observable_driver_type"],
            how="left",
            validate="one_to_one",
        )
    else:
        availability["direct_measurement_status"] = "DIRECT_MEASUREMENT_TABLE_NOT_BUILT"
        availability["kernel_parameter_filled"] = ""
        availability["value_kpc"] = None
        availability["secondary_value_kpc"] = None
        availability["dimensionless_value"] = None
        availability["source_component"] = ""
    decisions = [promotion_decision(row) for _, row in availability.iterrows()]
    gate = availability.copy()
    gate["kernel_promotion_status"] = [item[0] for item in decisions]
    gate["kernel_promotion_reason"] = [item[1] for item in decisions]
    gate["kernel_ready"] = [item[2] for item in decisions]
    gate["endpoint_eligible_after_kernel_gate"] = [item[3] for item in decisions]
    gate["accepted_label_output_allowed"] = False
    gate["endpoint_scores_computed"] = False
    gate["claim_boundary"] = CLAIM_BOUNDARY

    summary = (
        gate.groupby(
            [
                "formula_family",
                "observable_driver_type",
                "source_priority",
                "kernel_promotion_status",
            ],
            as_index=False,
        )
        .agg(
            n_galaxies=("galaxy", "count"),
            galaxies=("galaxy", lambda values: ";".join(values)),
            endpoint_eligible_count=("endpoint_eligible_after_kernel_gate", "sum"),
            median_delta_matched_rmse=("delta_matched_rmse", "median"),
            median_delta_vs_tpg=("delta_vs_tpg", "median"),
            median_delta_vs_mond=("delta_vs_mond", "median"),
        )
    )
    summary["claim_boundary"] = CLAIM_BOUNDARY

    endpoint = (
        gate.groupby("kernel_promotion_status", as_index=False)
        .agg(
            n_galaxies=("galaxy", "count"),
            endpoint_eligible_count=("endpoint_eligible_after_kernel_gate", "sum"),
            p0_count=("source_priority", lambda s: int((s == "P0_DIRECT_SOURCE_NATIVE_REQUIRED").sum())),
            p1_count=("source_priority", lambda s: int((s == "P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE").sum())),
            galaxies=("galaxy", lambda values: ";".join(values)),
        )
        .sort_values("kernel_promotion_status")
    )
    endpoint["endpoint_subset_status"] = endpoint["endpoint_eligible_count"].map(
        lambda value: "RUNNABLE_STRICT_SUBSET" if value > 0 else "NO_STRICT_ENDPOINT_ROWS"
    )
    endpoint["claim_boundary"] = CLAIM_BOUNDARY
    return gate, summary, endpoint


def write_report(gate: pd.DataFrame, summary: pd.DataFrame, endpoint: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    strict_count = int(gate["endpoint_eligible_after_kernel_gate"].sum())
    conditional_count = int((gate["kernel_promotion_status"] == "KERNEL_READY_CONDITIONAL").sum())
    proxy_count = int((gate["kernel_promotion_status"] == "KERNEL_PROXY_ONLY").sum())
    lines = [
        "# S4G75 Kernel-Ready Promotion Gate",
        "",
        "This gate separates source-rich rows from kernel-ready rows. A row is "
        "strictly kernel-ready only when the source constrains the same "
        "morphology kernel used by the formula family. It is not an endpoint.",
        "",
        "## Verdict",
        "",
        f"Strict kernel-ready endpoint rows: {strict_count}.",
        f"Conditional kernel rows: {conditional_count}.",
        f"Proxy-only kernel rows: {proxy_count}.",
        "",
        "A strict S4G75 kernel-ready endpoint subset is not runnable yet if the "
        "strict count is zero. Conditional rows may guide acquisition and "
        "promotion work, but they must not be used as accepted endpoint rows.",
        "",
        "## Promotion Summary",
        "",
        markdown_table(summary),
        "",
        "## Endpoint Subset Status",
        "",
        markdown_table(endpoint),
        "",
        "## Galaxy-Level Gate",
        "",
        markdown_table(
            gate[
                [
                    "galaxy",
                    "formula_family",
                    "source_priority",
                    "observable_driver_type",
                    "kernel_specific_source_status",
                    "direct_measurement_status",
                    "kernel_parameter_filled",
                    "value_kpc",
                    "dimensionless_value",
                    "kernel_promotion_status",
                    "endpoint_eligible_after_kernel_gate",
                    "kernel_promotion_reason",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "The gate is deliberately conservative. Generic S4G/SPARC/HI source "
        "coverage is not enough. Endpoint eligibility requires direct or "
        "accepted-promoted evidence for the kernel observable actually used by "
        "the morphology formula family.",
        "",
    ]
    (REPORTS / "s4g75_kernel_ready_promotion_gate.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    gate, summary, endpoint = build_gate()
    gate.to_csv(DATA / "s4g75_kernel_ready_promotion_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_kernel_ready_promotion_summary.csv", index=False)
    endpoint.to_csv(DATA / "s4g75_kernel_ready_endpoint_subset_status.csv", index=False)
    write_report(gate, summary, endpoint)
    print(f"wrote {DATA / 's4g75_kernel_ready_promotion_gate.csv'}")
    print(f"wrote {DATA / 's4g75_kernel_ready_promotion_summary.csv'}")
    print(f"wrote {DATA / 's4g75_kernel_ready_endpoint_subset_status.csv'}")
    print(f"wrote {REPORTS / 's4g75_kernel_ready_promotion_gate.md'}")


if __name__ == "__main__":
    main()
