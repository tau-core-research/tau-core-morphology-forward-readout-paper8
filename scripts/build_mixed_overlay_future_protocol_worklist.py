#!/usr/bin/env python3
"""Build future protocol worklist for mixed-overlay readout tests.

NGC4013 is now a prospective-only mixed-overlay protocol template, not a
validation case. This worklist selects future galaxies that could test the
same lane discipline without using endpoint residuals.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "mixed_overlay_future_protocol_worklist_not_endpoint"


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    lane_freeze = pd.read_csv(DATA / "readout_lane_freeze_assignments.csv")
    mixed_expansion = pd.read_csv(DATA / "mixed_readout_population_expansion_candidates.csv")
    acquisition = pd.read_csv(DATA / "s4g75_direct_source_native_acquisition_manifest.csv")
    missing = pd.read_csv(DATA / "readout_subfamily_missing_source_worklist.csv")
    ngc4013_replay = pd.read_csv(
        DATA / "ngc4013_mixed_overlay_prospective_replay_summary.csv"
    ).iloc[0]

    rows = [
        {
            "galaxy": "NGC4013",
            "protocol_role": "TEMPLATE_PROSPECTIVE_ONLY_NOT_VALIDATION",
            "candidate_lane": "L_mixed_overlay",
            "candidate_readout": "K_expdisk_warp_vertical_overlay",
            "priority": "REFERENCE_TEMPLATE",
            "source_status": "SOURCE_FREEZE_AND_FORMULA_FREEZE_PASS_CAVEATED",
            "score_status": "REPLAY_RECORDED_NOT_VALIDATION",
            "ready_for_future_scoring": False,
            "needed_next_action": "repeat protocol on future predeclared galaxies",
            "source_basis": "smooth disk carrier + warp/vertical/lag overlay source fields",
            "blocking_reason": "same galaxy already inspected diagnostically",
        }
    ]

    def add_row(
        galaxy: str,
        protocol_role: str,
        candidate_lane: str,
        candidate_readout: str,
        priority: str,
        source_status: str,
        needed_next_action: str,
        source_basis: str,
        blocking_reason: str,
    ) -> None:
        rows.append(
            {
                "galaxy": galaxy,
                "protocol_role": protocol_role,
                "candidate_lane": candidate_lane,
                "candidate_readout": candidate_readout,
                "priority": priority,
                "source_status": source_status,
                "score_status": "NOT_SCORED",
                "ready_for_future_scoring": False,
                "needed_next_action": needed_next_action,
                "source_basis": source_basis,
                "blocking_reason": blocking_reason,
            }
        )

    expansion_by_galaxy = {
        str(row["galaxy"]): row for _, row in mixed_expansion.iterrows()
    }
    acquisition_by_galaxy = {
        str(row["galaxy"]): row for _, row in acquisition.iterrows()
    }
    missing_by_galaxy = {
        galaxy: group for galaxy, group in missing.groupby("galaxy")
    }

    if "NGC4183" in expansion_by_galaxy:
        row = expansion_by_galaxy["NGC4183"]
        add_row(
            "NGC4183",
            "PRIMARY_FRESH_MIXED_OVERLAY_ACQUISITION_TARGET",
            "L_mixed_overlay",
            str(row["candidate_readout"]),
            "P0",
            str(row["source_side_strength"]),
            "acquire galaxy-specific bar/core/projection/history overlay observables",
            str(row["source_evidence_summary"]),
            str(row["main_blockers"]),
        )

    for galaxy in ["NGC0024", "NGC2683", "NGC3726", "NGC3949"]:
        source_row = acquisition_by_galaxy.get(galaxy)
        missing_rows = missing_by_galaxy.get(galaxy, pd.DataFrame())
        needed = (
            ";".join(missing_rows["needed_observable_or_review"].astype(str).tolist())
            if not missing_rows.empty
            else "vertical/projection source observables"
        )
        add_row(
            galaxy,
            "SECONDARY_VERTICAL_OVERLAY_ACQUISITION_TARGET",
            "L_mixed_overlay",
            "K_expdisk_thick_flared_overlay_review",
            "P1",
            str(source_row["acquisition_status"]) if source_row is not None else "SOURCE_ACQUISITION_REQUIRED",
            "acquire direct vertical/thickness/flare/warp/projection source fields",
            str(source_row["required_observables"]) if source_row is not None else needed,
            needed,
        )

    if "NGC4088" in expansion_by_galaxy:
        row = expansion_by_galaxy["NGC4088"]
        add_row(
            "NGC4088",
            "ADDED_OR_MIXED_WARP_HISTORY_PROTOCOL_BLOCKED",
            "L_added_source_or_L_mixed_overlay",
            str(row["candidate_readout"]),
            "P1_BLOCKED",
            str(row["source_side_strength"]),
            str(row["next_required_gate"]),
            str(row["source_evidence_summary"]),
            str(row["main_blockers"]),
        )

    if "NGC5907" in lane_freeze["galaxy"].values:
        lane = lane_freeze.loc[lane_freeze["galaxy"].eq("NGC5907")].iloc[0]
        add_row(
            "NGC5907",
            "NEGATIVE_CONTROL_FOR_ADDED_MIXED_CONFUSION",
            str(lane["frozen_lane"]),
            "K_projection_dominated",
            "CONTROL",
            str(lane["lane_freeze_status"]),
            "do not use as standalone mixed-overlay population template unless projection-specific",
            str(lane["source_evidence"]),
            str(lane["blocked_formula_shells"]),
        )

    worklist = pd.DataFrame(rows)
    worklist["uses_vobs_or_residual_in_selection"] = False
    worklist["endpoint_scores_allowed"] = False
    worklist["claim_boundary"] = CLAIM_BOUNDARY

    priority_order = {
        "REFERENCE_TEMPLATE": 0,
        "P0": 1,
        "P1": 2,
        "P1_BLOCKED": 3,
        "CONTROL": 4,
    }
    worklist["sort_priority"] = worklist["priority"].map(priority_order).fillna(9)
    worklist = worklist.sort_values(["sort_priority", "galaxy"]).drop(
        columns=["sort_priority"]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "MOFPW_G1_TEMPLATE_AVAILABLE",
                "gate_status": "PASS",
                "evidence": str(ngc4013_replay["prospective_replay_gate_status"]),
                "remaining_obligation": "do not count template as validation",
            },
            {
                "gate_id": "MOFPW_G2_PRIMARY_FRESH_TARGET",
                "gate_status": "PASS_CAVEATED",
                "evidence": "NGC4183 has SPARC scale but needs galaxy-specific overlay observables",
                "remaining_obligation": "source acquisition before any formula freeze",
            },
            {
                "gate_id": "MOFPW_G3_SECONDARY_VERTICAL_TARGETS",
                "gate_status": "PASS_CAVEATED",
                "evidence": "bulk S4G/DustPedia/HI source targets exist",
                "remaining_obligation": "direct source-native observables still missing",
            },
            {
                "gate_id": "MOFPW_G4_NO_ENDPOINT_SCORING",
                "gate_status": "PASS",
                "evidence": "worklist uses only source/gate metadata",
                "remaining_obligation": "separate source acquisition and formula freeze before scoring",
            },
        ]
    )
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "worklist_status": "MIXED_OVERLAY_FUTURE_PROTOCOL_WORKLIST_COMPLETE_NOT_ENDPOINT",
                "template_galaxy": "NGC4013",
                "primary_fresh_target": "NGC4183",
                "n_candidates": len(worklist),
                "n_primary_fresh_targets": int(
                    worklist["protocol_role"].eq(
                        "PRIMARY_FRESH_MIXED_OVERLAY_ACQUISITION_TARGET"
                    ).sum()
                ),
                "n_secondary_acquisition_targets": int(
                    worklist["protocol_role"].eq(
                        "SECONDARY_VERTICAL_OVERLAY_ACQUISITION_TARGET"
                    ).sum()
                ),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual_in_selection": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    worklist.to_csv(DATA / "mixed_overlay_future_protocol_worklist.csv", index=False)
    gates.to_csv(DATA / "mixed_overlay_future_protocol_worklist_gates.csv", index=False)
    summary.to_csv(DATA / "mixed_overlay_future_protocol_worklist_summary.csv", index=False)

    report = f"""# Mixed Overlay Future Protocol Worklist

Status: `{summary.iloc[0]['worklist_status']}`

This worklist turns NGC4013 into a prospective-only template and identifies
future galaxies where the mixed-overlay lane can be tested without using the
template score as validation.

## Summary

{markdown_table(summary)}

## Worklist

{markdown_table(worklist)}

## Gates

{markdown_table(gates)}

## Interpretation

The next scientifically clean move is not to keep reusing NGC4013. NGC4013
defines the protocol shape. NGC4183 is the primary fresh acquisition target
because it already has a smooth-disk scale but lacks galaxy-specific overlay
activation fields. The secondary targets are vertical/projection acquisition
cases that can broaden the mixed-overlay lane after source-native observables
are filled.

## Claim Boundary

`{CLAIM_BOUNDARY}`
"""
    (REPORTS / "mixed_overlay_future_protocol_worklist.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))
    print(worklist[["galaxy", "protocol_role", "priority", "needed_next_action"]].to_string(index=False))


if __name__ == "__main__":
    main()
