#!/usr/bin/env python3
"""Audit which filled S4G75 kernel observables drive endpoint deltas.

This is a diagnostic, not a new endpoint.  It asks whether the concrete
residual-blind filled kernel candidates helped or hurt the existing S4G75
stress-test comparison, then maps the result to the next source-native
observable target.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_filled_kernel_delta_driver_audit_not_endpoint"


def fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def markdown_table(df: pd.DataFrame) -> str:
    columns = list(df.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(fmt(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def approx_zero(value: float, tol: float = 1.0e-12) -> bool:
    return abs(float(value)) <= tol


def observable_driver_type(row: pd.Series) -> str:
    family = row["formula_family"]
    if family == "K_scale_tail_spiral":
        return "tail_inner_cutoff_candidate"
    if family == "K_compact_finite":
        return "compact_support_candidate"
    if family == "K_thick_flared":
        return "thickness_h_over_rs_candidate"
    return "scale_only_or_not_filled"


def driver_outcome(row: pd.Series) -> str:
    matched_delta = float(row["filled_minus_old_matched_rmse"])
    wrong_delta = float(row["filled_minus_old_matched_minus_wrong"])
    tpg_delta = float(row["filled_minus_old_matched_minus_tpg"])
    mond_delta = float(row["filled_minus_old_matched_minus_mond"])

    if all(approx_zero(v) for v in [matched_delta, wrong_delta, tpg_delta, mond_delta]):
        return "FILLED_NO_EFFECT"
    if matched_delta < 0 and tpg_delta < 0 and mond_delta < 0:
        return "FILLED_IMPROVED_MATCHED_AND_BASELINES"
    if matched_delta < 0 and (tpg_delta < 0 or mond_delta < 0):
        return "FILLED_IMPROVED_PARTIAL_BASELINE_TRANSFER"
    if matched_delta < 0:
        return "FILLED_IMPROVED_MATCHED_RMSE_ONLY"
    if tpg_delta > 0 or mond_delta > 0:
        return "FILLED_WORSENED_BASELINE_TRANSFER"
    if wrong_delta > 0:
        return "FILLED_WEAKENED_WRONG_FAMILY_MARGIN"
    return "FILLED_MIXED_OR_SMALL_DELTA"


def source_native_target(row: pd.Series) -> str:
    family = row["formula_family"]
    if family == "K_scale_tail_spiral":
        return (
            "direct outer-disk/HI transition observable: HI radial profile, "
            "break radius, truncation radius, or source-native tail cutoff"
        )
    if family == "K_compact_finite":
        return (
            "direct compact support observable: bulge/component radius, "
            "central compact mass-light component, or decomposition support"
        )
    if family == "K_thick_flared":
        return (
            "direct vertical geometry observable: scale height, flare/warp "
            "profile, edge-on thickness, or gas-plane thickness"
        )
    return "direct source-native morphology kernel observable"


def source_priority(row: pd.Series) -> str:
    outcome = row["driver_outcome"]
    status_blob = ";".join(
        str(row.get(column, ""))
        for column in [
            "tail_observable_status",
            "compact_observable_status",
            "thickness_observable_status",
        ]
    )
    candidate_like = "FORMULA_CANDIDATE" in status_blob or "EDGE_DISK_CANDIDATE" in status_blob
    if outcome == "FILLED_WORSENED_BASELINE_TRANSFER" and candidate_like:
        return "P0_DIRECT_SOURCE_NATIVE_REQUIRED"
    if outcome in {
        "FILLED_IMPROVED_MATCHED_AND_BASELINES",
        "FILLED_IMPROVED_PARTIAL_BASELINE_TRANSFER",
    } and candidate_like:
        return "P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE"
    if outcome == "FILLED_NO_EFFECT":
        return "P2_NO_EFFECT_REVIEW"
    return "P1_PROMOTION_RULE_AUDIT_REQUIRED"


def build_audit() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    delta = pd.read_csv(DATA / "s4g75_filled_vs_proxy_delta.csv")
    fill = pd.read_csv(DATA / "s4g75_kernel_observable_fill.csv")
    review = pd.read_csv(DATA / "s4g75_holdout_repair_review_galaxy_summary.csv")
    failure = pd.read_csv(DATA / "s4g75_failure_mode_breakdown.csv")

    keep_delta = [
        "galaxy",
        "split",
        "formula_family",
        "old_rmse_matched_family",
        "rmse_tpg_v6",
        "rmse_mond",
        "filled_rmse_matched_family",
        "filled_minus_old_matched_rmse",
        "filled_minus_old_matched_minus_wrong",
        "filled_minus_old_matched_minus_tpg",
        "filled_minus_old_matched_minus_mond",
        "filled_improves_matched_rmse",
        "filled_improves_vs_wrong",
        "filled_improves_vs_tpg",
        "filled_improves_vs_mond",
    ]
    keep_fill = [
        "galaxy",
        "repair_priority",
        "scale_radius_status",
        "tail_inner_radius_kpc",
        "tail_cutoff_radius_kpc",
        "tail_observable_status",
        "compact_support_radius_kpc",
        "compact_observable_status",
        "thickness_h_over_rs",
        "thickness_observable_status",
        "kernel_observable_provenance",
    ]
    keep_review = [
        "galaxy",
        "manifest_caveat",
        "s4g_support_status",
        "audit_lane",
        "endpoint_blocker",
    ]
    keep_failure = [
        "galaxy",
        "failure_mode",
        "failure_reason",
        "repair_status",
        "projection_reason",
    ]

    audit = (
        fill[keep_fill]
        .merge(delta[keep_delta], on="galaxy", how="left", validate="one_to_one")
        .merge(review[keep_review], on="galaxy", how="left", validate="one_to_one")
        .merge(failure[keep_failure], on="galaxy", how="left", validate="one_to_one")
    )
    audit["observable_driver_type"] = audit.apply(observable_driver_type, axis=1)
    audit["driver_outcome"] = audit.apply(driver_outcome, axis=1)
    audit["source_native_target"] = audit.apply(source_native_target, axis=1)
    audit["source_priority"] = audit.apply(source_priority, axis=1)
    audit["claim_boundary"] = CLAIM_BOUNDARY

    audit = audit.sort_values(
        [
            "source_priority",
            "observable_driver_type",
            "repair_priority",
            "galaxy",
        ]
    )

    summary = (
        audit.groupby(
            [
                "formula_family",
                "observable_driver_type",
                "driver_outcome",
                "source_priority",
            ],
            dropna=False,
        )
        .agg(
            n_galaxies=("galaxy", "count"),
            median_delta_matched_rmse=("filled_minus_old_matched_rmse", "median"),
            median_delta_vs_wrong=("filled_minus_old_matched_minus_wrong", "median"),
            median_delta_vs_tpg=("filled_minus_old_matched_minus_tpg", "median"),
            median_delta_vs_mond=("filled_minus_old_matched_minus_mond", "median"),
            improves_matched_fraction=("filled_improves_matched_rmse", "mean"),
            improves_tpg_fraction=("filled_improves_vs_tpg", "mean"),
            improves_mond_fraction=("filled_improves_vs_mond", "mean"),
        )
        .reset_index()
    )
    summary["claim_boundary"] = CLAIM_BOUNDARY

    targets = (
        audit.groupby(
            [
                "formula_family",
                "observable_driver_type",
                "source_priority",
                "source_native_target",
            ],
            dropna=False,
        )
        .agg(
            n_galaxies=("galaxy", "count"),
            galaxies=("galaxy", lambda values: ";".join(values)),
            median_delta_matched_rmse=("filled_minus_old_matched_rmse", "median"),
            median_delta_vs_tpg=("filled_minus_old_matched_minus_tpg", "median"),
            median_delta_vs_mond=("filled_minus_old_matched_minus_mond", "median"),
        )
        .reset_index()
        .sort_values(["source_priority", "formula_family"])
    )
    targets["claim_boundary"] = CLAIM_BOUNDARY
    return audit, summary, targets


def write_report(audit: pd.DataFrame, summary: pd.DataFrame, targets: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    by_outcome = (
        audit.groupby(["driver_outcome", "source_priority"], dropna=False)
        .agg(
            n_galaxies=("galaxy", "count"),
            median_delta_matched_rmse=("filled_minus_old_matched_rmse", "median"),
            median_delta_vs_tpg=("filled_minus_old_matched_minus_tpg", "median"),
            median_delta_vs_mond=("filled_minus_old_matched_minus_mond", "median"),
        )
        .reset_index()
        .sort_values(["source_priority", "driver_outcome"])
    )
    top_rows = audit[
        [
            "galaxy",
            "formula_family",
            "repair_priority",
            "observable_driver_type",
            "driver_outcome",
            "source_priority",
            "filled_minus_old_matched_rmse",
            "filled_minus_old_matched_minus_tpg",
            "filled_minus_old_matched_minus_mond",
        ]
    ].copy()

    lines = [
        "# S4G75 Filled-Kernel Delta-Driver Audit",
        "",
        "This diagnostic splits the filled-kernel stress-test delta by formula "
        "family, observable type, and repair priority. It is not a new endpoint "
        "and does not change the accepted-claim status.",
        "",
        "## Main Reading",
        "",
        "The filled candidates preserve morphology-family specificity in the "
        "S4G75 endpoint, but they do not uniformly improve baseline transfer. "
        "The delta-driver split identifies where direct source-native kernel "
        "observables are needed before a baseline-superiority claim is allowed.",
        "",
        "## Outcome Summary",
        "",
        markdown_table(by_outcome),
        "",
        "## Driver Summary",
        "",
        markdown_table(summary),
        "",
        "## Direct Source-Native Observable Targets",
        "",
        markdown_table(targets),
        "",
        "## Galaxy-Level Delta Drivers",
        "",
        markdown_table(top_rows),
        "",
        "## Claim Boundary",
        "",
        "These rows are residual-blind diagnostics over already computed stress "
        "tests. They identify acquisition and promotion targets; they are not "
        "empirical validation and not accepted endpoint scoring.",
        "",
    ]
    (REPORTS / "s4g75_filled_kernel_delta_driver_audit.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    audit, summary, targets = build_audit()
    audit.to_csv(DATA / "s4g75_filled_kernel_delta_drivers.csv", index=False)
    summary.to_csv(DATA / "s4g75_filled_kernel_delta_driver_summary.csv", index=False)
    targets.to_csv(DATA / "s4g75_direct_source_native_observable_targets.csv", index=False)
    write_report(audit, summary, targets)
    print(f"wrote {DATA / 's4g75_filled_kernel_delta_drivers.csv'}")
    print(f"wrote {DATA / 's4g75_filled_kernel_delta_driver_summary.csv'}")
    print(f"wrote {DATA / 's4g75_direct_source_native_observable_targets.csv'}")
    print(f"wrote {REPORTS / 's4g75_filled_kernel_delta_driver_audit.md'}")


if __name__ == "__main__":
    main()
