#!/usr/bin/env python3
"""Build a residual-blind missing-source worklist for readout subfamilies.

The worklist is an acquisition and review planning artifact. It does not
promote labels and does not compute rotation endpoints.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "readout_subfamily_missing_source_worklist_not_endpoint"


SOURCE_HINTS = {
    "x_warp_onset_value": "HI velocity-field radial PA profile; radial warp-angle profile; channel-map digitization",
    "q_warp_measured_first_pass": "independent channel-map review or published warp/asymmetry amplitude",
    "m_history_warp_first_pass": "residual-blind interaction/environment/history review",
    "epsilon_cross_numeric_bound": "accepted q_warp plus accepted memory/history proxy, then source-bound protocol rerun",
    "outer_tail_transition_radius": "resolved HI radius/profile map; tail/envelope transition measurement",
    "hi_asymmetry_or_tail_measurement": "resolved HI asymmetry map or published lopsidedness/tail metric",
    "compact support radius and bulge/core decomposition": "S4G/NED/DustPedia decomposition; compact support radius source",
    "compact_support_radius": "S4G/NED/DustPedia decomposition; compact support radius source",
    "bulge_core_decomposition": "S4G component table or independent bulge/core decomposition",
    "bar_core_projection_history_overlay": "S4G bar/core decomposition plus NED/HI projection-history review",
    "bar/core/projection/history overlay source review": "S4G/NED/HI source review for bar, core, projection, and history overlays",
    "possible_outer_warp_caveat": "HI/projection review to confirm or reject outer-warp emission",
    "compact_only_overlay_flag": "reclassify against disk/warp overlay sources before endpoint use",
}


PRIORITY = {
    "NGC4088": 1,
    "NGC5907": 2,
    "IC2574": 3,
    "UGC05716": 4,
    "NGC4013": 5,
    "NGC7331": 6,
    "NGC4183": 7,
    "IC4202": 8,
    "UGC12506": 9,
}


def split_items(value: object) -> list[str]:
    if pd.isna(value) or str(value).strip() == "":
        return []
    return [item.strip() for item in str(value).split(";") if item.strip()]


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def add_rows(rows: list[dict[str, object]], audit_row: pd.Series, items: list[str], blocker_type: str) -> None:
    for item in items:
        if any(
            existing["galaxy"] == audit_row["galaxy"]
            and existing["needed_observable_or_review"] == item
            for existing in rows
        ):
            continue
        rows.append(
            {
                "priority_rank": PRIORITY.get(audit_row["galaxy"], 99),
                "galaxy": audit_row["galaxy"],
                "proposed_readout_subfamily": audit_row["proposed_readout_subfamily"],
                "audit_decision": audit_row["audit_decision"],
                "blocker_type": blocker_type,
                "needed_observable_or_review": item,
                "recommended_source_path": SOURCE_HINTS.get(item, "targeted residual-blind literature/source review"),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )


def main() -> None:
    audit = pd.read_csv(DATA / "readout_subfamily_accepted_manifest_audit.csv")
    rows: list[dict[str, object]] = []
    for _, audit_row in audit.iterrows():
        add_rows(
            rows,
            audit_row,
            split_items(audit_row.get("missing_required_observables")),
            "missing_required_observable",
        )
        add_rows(
            rows,
            audit_row,
            split_items(audit_row.get("blocked_observables")),
            "blocked_observable",
        )
        add_rows(
            rows,
            audit_row,
            split_items(audit_row.get("caveat_observables")),
            "caveat_to_resolve",
        )
        add_rows(
            rows,
            audit_row,
            split_items(audit_row.get("reclassification_pressure_observables")),
            "reclassification_review",
        )
        if audit_row["audit_decision"] == "ACCEPTED_SUBFAMILY_SOURCE_FIELDS_ENDPOINT_STILL_BLOCKED":
            rows.append(
                {
                    "priority_rank": PRIORITY.get(audit_row["galaxy"], 99),
                    "galaxy": audit_row["galaxy"],
                    "proposed_readout_subfamily": audit_row["proposed_readout_subfamily"],
                    "audit_decision": audit_row["audit_decision"],
                    "blocker_type": "endpoint_freeze_gate",
                    "needed_observable_or_review": "frozen endpoint protocol and source-native normalization gate",
                    "recommended_source_path": "no new rotation scoring; freeze predeclared endpoint-use rule",
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    worklist = pd.DataFrame(rows).sort_values(
        ["priority_rank", "galaxy", "blocker_type", "needed_observable_or_review"]
    )
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    worklist.to_csv(DATA / "readout_subfamily_missing_source_worklist.csv", index=False)
    summary = (
        worklist.groupby(["priority_rank", "galaxy", "proposed_readout_subfamily"], as_index=False)
        .agg(
            n_open_items=("needed_observable_or_review", "size"),
            blocker_types=("blocker_type", lambda s: ";".join(sorted(set(s)))),
        )
        .sort_values(["priority_rank", "galaxy"])
    )
    summary.to_csv(DATA / "readout_subfamily_missing_source_worklist_summary.csv", index=False)
    report = [
        "# Readout-Subfamily Missing-Source Worklist",
        "",
        "This worklist is generated from the accepted-manifest audit. It is an",
        "acquisition/review guide only: it does not score rotation endpoints and",
        "does not validate Tau Core.",
        "",
        "## Priority Summary",
        "",
        markdown_table(summary),
        "",
        "## Open Items",
        "",
        markdown_table(
            worklist[
                [
                    "priority_rank",
                    "galaxy",
                    "proposed_readout_subfamily",
                    "audit_decision",
                    "blocker_type",
                    "needed_observable_or_review",
                    "recommended_source_path",
                    "claim_boundary",
                ]
            ]
        ),
        "",
        "## Immediate Next Target",
        "",
        "NGC4088 remains the highest-priority case because the targeted warp/history",
        "diagnostic already has a strong shape signal, while accepted subfamily use",
        "is still blocked by source-review and numeric-bound requirements. The next",
        "source task is to promote or reject its first-pass warp onset, q-warp,",
        "memory/history, and epsilon-cross inputs without using the rotation endpoint.",
        "",
    ]
    (REPORTS / "readout_subfamily_missing_source_worklist.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
