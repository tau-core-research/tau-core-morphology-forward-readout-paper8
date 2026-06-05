#!/usr/bin/env python3
"""Build the S4G75 closure-source generalization gate.

The NGC2683 flare closure-source prototype improved a local stress diagnostic,
but it must not be generalized automatically.  This gate records which S4G75
thick/flared rows have enough source support to enter a profile-aware vertical
closure-source development lane.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_closure_source_generalization_gate_not_endpoint"


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


def classify(row: pd.Series) -> tuple[str, str, str]:
    galaxy = row["galaxy"]
    inc = float(row["inclination_deg"])
    source_hit = str(row.get("literature_status", ""))
    if galaxy == "NGC2683" and source_hit == "DIRECT_LITERATURE_FLARE_PROFILE_READY_MAPPING_REQUIRED":
        return (
            "PROFILE_CLOSURE_SOURCE_READY_PROTOTYPE_ONLY",
            "direct flare profile exists; closure-source prototype improves NGC2683 stress diagnostic",
            "develop and predeclare a population-level H(R)/warp closure-source kernel before endpoint use",
        )
    if inc >= 75:
        return (
            "EDGE_ON_VERTICAL_PROFILE_SEARCH_REQUIRED",
            "high inclination makes a vertical/warp source search plausible, but no direct profile is recorded",
            "perform residual-blind literature/data extraction for vertical scale, flare, warp, or gas-plane thickness",
        )
    if inc >= 65:
        return (
            "HIGH_INCLINATION_WARP_FLARE_SEARCH_REQUIRED",
            "inclination is high enough for flare/warp evidence to matter, but direct source profile is missing",
            "search resolved HI/kinematic/warp literature before closure-source promotion",
        )
    return (
        "INSUFFICIENT_VERTICAL_PROFILE_SUPPORT",
        "current source support does not provide a direct vertical or flare profile",
        "keep as proxy/theorem-development row; do not use closure-source endpoint kernel",
    )


def clean_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value)


def build_gate() -> tuple[pd.DataFrame, pd.DataFrame]:
    ledger = pd.read_csv(DATA / "s4g75_remaining_kernel_acquisition_ledger.csv")
    literature = pd.read_csv(DATA / "s4g75_literature_kernel_source_hits.csv")
    search_summary = pd.read_csv(DATA / "s4g75_vertical_source_search_summary.csv")
    sensitivity = pd.read_csv(DATA / "s4g75_ngc2683_closure_source_sensitivity.csv")
    best_delta = float(sensitivity["closure_source_minus_scalar_rmse"].min())
    improved_count = int((sensitivity["closure_source_minus_scalar_rmse"] < 0).sum())
    thick = ledger.loc[ledger["formula_family"] == "K_thick_flared"].copy()
    thick = thick.merge(
        literature[
            [
                "galaxy",
                "literature_status",
                "source_authors_year",
                "source_url",
                "endpoint_mapping_status",
            ]
        ],
        on="galaxy",
        how="left",
        validate="one_to_one",
    )
    thick = thick.merge(
        search_summary[
            [
                "galaxy",
                "n_source_checks",
                "any_direct_profile",
                "statuses",
                "kernel_relevance",
            ]
        ].rename(
            columns={
                "statuses": "vertical_search_statuses",
                "kernel_relevance": "vertical_search_relevance",
            }
        ),
        on="galaxy",
        how="left",
        validate="one_to_one",
    )
    rows = []
    for _, row in thick.iterrows():
        status, reason, next_action = classify(row)
        rows.append(
            {
                "galaxy": row["galaxy"],
                "formula_family": row["formula_family"],
                "source_priority": row["source_priority"],
                "inclination_deg": row["inclination_deg"],
                "blocker_class": row["blocker_class"],
                "literature_status": row["literature_status"],
                "source_authors_year": row["source_authors_year"],
                "source_url": row["source_url"],
                "vertical_source_checks": int(row["n_source_checks"])
                if pd.notna(row["n_source_checks"])
                else 0,
                "vertical_search_direct_profile": bool(row["any_direct_profile"])
                if pd.notna(row["any_direct_profile"])
                else False,
                "vertical_search_statuses": clean_text(row.get("vertical_search_statuses", "")),
                "vertical_search_relevance": clean_text(row.get("vertical_search_relevance", "")),
                "generalization_status": status,
                "generalization_reason": reason,
                "next_action": next_action,
                "ngc2683_sensitivity_grid_points": len(sensitivity),
                "ngc2683_sensitivity_improved_points": improved_count,
                "ngc2683_best_delta_rmse": best_delta,
                "closure_source_endpoint_allowed": False,
                "endpoint_scores_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    gate = pd.DataFrame(rows)
    summary = (
        gate.groupby(["generalization_status"], as_index=False)
        .agg(
            n_galaxies=("galaxy", "count"),
            galaxies=("galaxy", lambda values: ";".join(values)),
            median_inclination=("inclination_deg", "median"),
        )
    )
    summary["claim_boundary"] = CLAIM_BOUNDARY
    return gate, summary


def write_report(gate: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# S4G75 Closure-Source Generalization Gate",
        "",
        "This gate prevents the NGC2683 closure-source prototype from being "
        "generalized automatically. It records which thick/flared rows are ready "
        "for profile-aware closure-source development and which still need data.",
        "",
        "## Verdict",
        "",
        markdown_table(summary),
        "",
        "Only NGC2683 is currently profile-source ready, and even there the status "
        "is prototype-only. No S4G75 row is authorized for closure-source endpoint "
        "scoring by this gate.",
        "",
        "## Galaxy-Level Gate",
        "",
        markdown_table(
            gate[
                [
                    "galaxy",
                    "inclination_deg",
                    "literature_status",
                    "vertical_source_checks",
                    "vertical_search_statuses",
                    "generalization_status",
                    "generalization_reason",
                    "next_action",
                    "closure_source_endpoint_allowed",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "The NGC2683 sensitivity result is a formula-development signal. A "
        "population-level closure-source endpoint requires predeclared source "
        "criteria, direct profile extraction for additional galaxies, and a fixed "
        "kernel rule before endpoint scoring.",
        "",
    ]
    (REPORTS / "s4g75_closure_source_generalization_gate.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    gate, summary = build_gate()
    gate.to_csv(DATA / "s4g75_closure_source_generalization_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_closure_source_generalization_summary.csv", index=False)
    write_report(gate, summary)
    print(f"wrote {DATA / 's4g75_closure_source_generalization_gate.csv'}")
    print(f"wrote {DATA / 's4g75_closure_source_generalization_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_closure_source_generalization_gate.md'}")


if __name__ == "__main__":
    main()
