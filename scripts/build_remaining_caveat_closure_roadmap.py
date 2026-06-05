#!/usr/bin/env python3
"""Build the remaining four-case caveat closure roadmap.

The roadmap is not an endpoint score. It classifies the remaining caveats after
the four-case caveat-reduction and NGC4013 retrospective-closure gates, then
records which next gate could reduce each caveat without retroactive scoring.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "remaining_caveat_closure_roadmap_not_endpoint"


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


def require(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def optional_first_row(path: Path) -> pd.Series | None:
    if not path.exists():
        return None
    table = pd.read_csv(path)
    if table.empty:
        return None
    return table.iloc[0]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    four_cases = require(DATA / "four_case_caveat_reduction_cases.csv")
    n4013 = require(DATA / "ngc4013_retrospective_caveat_closure_summary.csv").iloc[0]
    n4013_predeclared = optional_first_row(
        DATA / "ngc4013_predeclared_replay_holdout_summary.csv"
    )
    n7331_v2 = require(DATA / "ngc7331_fractional_onset_v2_replay_freeze_summary.csv").iloc[0]
    n7331_replay = optional_first_row(
        DATA / "ngc7331_v2_v3_replay_holdout_endpoint_summary.csv"
    )
    n4088_readiness = require(DATA / "ngc4088_formula_freeze_readiness_summary.csv").iloc[0]
    n4088_action = optional_first_row(DATA / "ngc4088_remaining_caveat_action_summary.csv")
    n5907_gate = require(DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_gate_summary.csv").iloc[0]

    n7331_replay_done = (
        n7331_replay is not None
        and str(n7331_replay["endpoint_status"])
        == "NGC7331_V2_V3_REPLAY_HOLDOUT_PRELIMINARY_CONTROL_RESULT"
    )
    if n7331_replay_done:
        n7331_row = {
            "galaxy": "NGC7331",
            "remaining_caveat_class": "BROAD_WINDOW_REPLAY_REDUCED_V1_NOT_UPDATED",
            "current_status": str(n7331_replay["endpoint_status"]),
            "next_gate": "POPULATION_REPLAY_OR_SOURCE_ANALOGUE_CONFIRMATION",
            "closure_route": (
                "V3 replay reduces the broad-window caveat for the replay path; keep the "
                "accepted V1 endpoint unchanged and reduce further only by population replay "
                "or fresh source-selected analogues"
            ),
            "can_close_without_new_endpoint_data": False,
            "endpoint_scores_allowed_now": False,
            "priority": "P2_POPULATION_SCALE",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    else:
        n7331_row = {
            "galaxy": "NGC7331",
            "remaining_caveat_class": "BROAD_WINDOW_V1_CAVEAT",
            "current_status": str(n7331_v2["v2_replay_freeze_status"]),
            "next_gate": "V2_OR_V3_REPLAY_HOLDOUT_ENDPOINT",
            "closure_route": (
                "score a replay/holdout-only fractional-onset or source-sharpened window without "
                "altering the accepted V1 endpoint"
            ),
            "can_close_without_new_endpoint_data": True,
            "endpoint_scores_allowed_now": False,
            "priority": "P0_REPLAY_READY",
            "claim_boundary": CLAIM_BOUNDARY,
        }

    n4013_predeclared_done = (
        n4013_predeclared is not None
        and str(n4013_predeclared["predeclared_replay_gate_status"])
        == "NGC4013_PREDECLARED_REPLAY_HOLDOUT_GATE_BUILT_ENDPOINT_STILL_BLOCKED"
    )
    if n4013_predeclared_done:
        n4013_row = {
            "galaxy": "NGC4013",
            "remaining_caveat_class": "PREDECLARED_REPLAY_GATE_BUILT_FUTURE_DATA_REQUIRED",
            "current_status": str(n4013_predeclared["predeclared_replay_gate_status"]),
            "next_gate": "FUTURE_UNINSPECTED_HOLDOUT_OR_SOURCE_SELECTED_ANALOGUE",
            "closure_route": (
                "the frozen expdisk+WVO protocol is transferable, but the same-curve replay "
                "is blocked; reduce further only with future uninspected holdout data or an "
                "exact source-selected analogue"
            ),
            "can_close_without_new_endpoint_data": False,
            "endpoint_scores_allowed_now": False,
            "priority": "P2_POPULATION_SCALE",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    else:
        n4013_row = {
            "galaxy": "NGC4013",
            "remaining_caveat_class": "RETROSPECTIVE_PROTOCOL_CAVEAT",
            "current_status": str(n4013["closure_gate_status"]),
            "next_gate": "PREDECLARED_REPLAY_HOLDOUT_OR_FUTURE_SOURCE_ANALOGUE",
            "closure_route": (
                "run the frozen expdisk+WVO protocol only in a predeclared replay/holdout lane "
                "or on a future source-selected analogue"
            ),
            "can_close_without_new_endpoint_data": False,
            "endpoint_scores_allowed_now": False,
            "priority": "P1_PROTOCOL_ANALOGUE",
            "claim_boundary": CLAIM_BOUNDARY,
        }

    n4088_action_done = (
        n4088_action is not None
        and str(n4088_action["action_gate_status"])
        == "NGC4088_REMAINING_CAVEAT_ACTION_GATE_BUILT_NOT_ENDPOINT"
    )
    if n4088_action_done:
        n4088_row = {
            "galaxy": "NGC4088",
            "remaining_caveat_class": "B2_B3_LAW_LEVEL_OPEN_B1_PROVENANCE_UPGRADE_OPTIONAL",
            "current_status": str(n4088_action["action_gate_status"]),
            "next_gate": "B2_SOURCE_LOAD_ORIGIN_AND_ASYMPTOTIC_CARRIER_DERIVATION",
            "closure_route": (
                "endpoint is already caveated-control scored; B1 is formula-freeze closed with "
                "WHISP graphical provenance caveat; direct H I is a provenance upgrade, while "
                "the primary open theory gate is B2 source-load-origin/asymptotic-carrier derivation"
            ),
            "can_close_without_new_endpoint_data": False,
            "endpoint_scores_allowed_now": False,
            "priority": "P1_SOURCE_AND_THEORY",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    else:
        n4088_row = {
            "galaxy": "NGC4088",
            "remaining_caveat_class": "B1_PROVENANCE_PLUS_B2_B3_LAW_LEVEL",
            "current_status": str(n4088_readiness["readiness_decision"]),
            "next_gate": "DIRECT_HI_PRODUCT_OR_B2_B3_THEORY_CLOSURE",
            "closure_route": (
                "cache a direct source-coordinate H I product to reduce B1 provenance, and separately "
                "derive the B2 physical normalization and B3 law-level uniqueness"
            ),
            "can_close_without_new_endpoint_data": False,
            "endpoint_scores_allowed_now": False,
            "priority": "P1_SOURCE_AND_THEORY",
            "claim_boundary": CLAIM_BOUNDARY,
        }

    roadmap_rows = [
        n4013_row,
        n7331_row,
        n4088_row,
        {
            "galaxy": "NGC5907",
            "remaining_caveat_class": "SMALL_N_CONTROL_CONTEXT",
            "current_status": str(n5907_gate["accepted_endpoint_freeze_status"]),
            "next_gate": "POPULATION_REPLAY_OR_MORE_FRESH_ANALOGUES",
            "closure_route": (
                "do not change the accepted single-galaxy endpoint; reduce only by adding fresh "
                "source-selected population rows"
            ),
            "can_close_without_new_endpoint_data": False,
            "endpoint_scores_allowed_now": False,
            "priority": "P2_POPULATION_SCALE",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    roadmap = pd.DataFrame(roadmap_rows)

    priority_order = {
        "P0_REPLAY_READY": 0,
        "P1_PROTOCOL_ANALOGUE": 1,
        "P1_SOURCE_AND_THEORY": 2,
        "P2_POPULATION_SCALE": 3,
    }
    roadmap["priority_rank"] = roadmap["priority"].map(priority_order).astype(int)
    roadmap = roadmap.sort_values(["priority_rank", "galaxy"]).drop(columns=["priority_rank"])
    next_recommended_gate = (
        "B2_SOURCE_LOAD_ORIGIN_AND_ASYMPTOTIC_CARRIER_DERIVATION_FOR_NGC4088"
        if n7331_replay_done and n4013_predeclared_done and n4088_action_done
        else "NGC4088_DIRECT_HI_PRODUCT_OR_B2_B3_THEORY_CLOSURE"
        if n7331_replay_done and n4013_predeclared_done
        else "NGC4013_PREDECLARED_REPLAY_HOLDOUT_OR_FUTURE_SOURCE_ANALOGUE"
        if n7331_replay_done
        else "V2_OR_V3_REPLAY_HOLDOUT_ENDPOINT_FOR_NGC7331"
    )
    roadmap_status = (
        "REMAINING_CAVEAT_CLOSURE_ROADMAP_UPDATED_AFTER_NGC4088_ACTION_GATE_NOT_ENDPOINT"
        if n7331_replay_done and n4013_predeclared_done and n4088_action_done
        else
        "REMAINING_CAVEAT_CLOSURE_ROADMAP_UPDATED_AFTER_NGC7331_AND_NGC4013_GATES_NOT_ENDPOINT"
        if n7331_replay_done and n4013_predeclared_done
        else
        "REMAINING_CAVEAT_CLOSURE_ROADMAP_UPDATED_AFTER_NGC7331_REPLAY_NOT_ENDPOINT"
        if n7331_replay_done
        else "REMAINING_CAVEAT_CLOSURE_ROADMAP_READY_NOT_ENDPOINT"
    )

    summary = pd.DataFrame(
        [
            {
                "roadmap_status": roadmap_status,
                "n_cases": len(roadmap),
                "n_replay_ready_without_new_source": int(
                    roadmap["can_close_without_new_endpoint_data"].sum()
                ),
                "n_replay_completed_without_v1_update": int(n7331_replay_done),
                "n_predeclared_replay_gates_built_without_endpoint": int(
                    n4013_predeclared_done
                ),
                "n_remaining_caveat_action_gates_built_without_endpoint": int(
                    n4088_action_done
                ),
                "n_retrospective_or_population_blocked": int(
                    roadmap["remaining_caveat_class"].isin(
                        [
                            "RETROSPECTIVE_PROTOCOL_CAVEAT",
                            "SMALL_N_CONTROL_CONTEXT",
                            "BROAD_WINDOW_REPLAY_REDUCED_V1_NOT_UPDATED",
                            "PREDECLARED_REPLAY_GATE_BUILT_FUTURE_DATA_REQUIRED",
                        ]
                    ).sum()
                ),
                "n_source_or_law_blocked": int(
                    roadmap["remaining_caveat_class"].eq(
                        "B1_PROVENANCE_PLUS_B2_B3_LAW_LEVEL"
                    ).sum()
                ),
                "endpoint_statuses_changed": False,
                "endpoint_scores_recomputed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "uses_replay_endpoint_summary": bool(n7331_replay_done),
                "uses_predeclared_replay_gate_summary": bool(n4013_predeclared_done),
                "uses_remaining_caveat_action_summary": bool(n4088_action_done),
                "v1_endpoint_updated": False,
                "next_recommended_gate": next_recommended_gate,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    audit = four_cases[
        [
            "galaxy",
            "caveat_reduction_status",
            "caveat_reduced",
            "remaining_caveat",
            "endpoint_status_changed",
            "endpoint_scores_recomputed",
            "uses_vobs_or_residual_in_reduction",
        ]
    ].copy()
    audit["claim_boundary"] = CLAIM_BOUNDARY

    roadmap.to_csv(DATA / "remaining_caveat_closure_roadmap.csv", index=False)
    summary.to_csv(DATA / "remaining_caveat_closure_roadmap_summary.csv", index=False)
    audit.to_csv(DATA / "remaining_caveat_closure_roadmap_audit.csv", index=False)

    report = [
        "# Remaining Caveat Closure Roadmap",
        "",
        "This roadmap ranks the remaining caveats after the four-case caveat",
        "reduction audit. It is not an endpoint score and does not change any",
        "endpoint status.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Roadmap",
        "",
        markdown_table(roadmap),
        "",
        "## Prior Audit Snapshot",
        "",
        markdown_table(audit),
        "",
        "## Interpretation",
        "",
        (
            "The NGC7331 replay path, NGC4013 predeclared replay gate, and NGC4088 "
            "remaining-caveat action gate have all been built. NGC4088 is already "
            "a caveated accepted single-galaxy control endpoint; its B1 graphical "
            "WHISP x_w is closed for formula freeze but remains a provenance caveat. "
            "The next scientific action is therefore B2 law-level work: derive the "
            "Tau-side source-load origin, final carrier law/population transfer, "
            "and cross-term bound. The frozen Vflat^2 carrier theorem narrows the "
            "asymptotic-carrier part, but does not close the final Tau-side law; "
            "B3 law-level uniqueness then follows as the dependent caveat. No "
            "endpoint status is changed by this roadmap."
            if n7331_replay_done and n4013_predeclared_done and n4088_action_done
            else "The NGC7331 V2/V3 replay path has already been run, and the NGC4013 "
            "predeclared replay/holdout gate has been built. NGC7331 is no "
            "longer the next replay-ready step, and NGC4013 is no longer an "
            "unformalized retrospective caveat; its same-curve replay is explicitly "
            "blocked and future use requires uninspected holdout data or an exact "
            "source-selected analogue. The next currently actionable caveat path is "
            "NGC4088: it requires either a direct source-coordinate H I product for "
            "B1 or law-level B2/B3 derivations. NGC5907 is locally accepted; its "
            "remaining caveat is only the small-N population context."
            if n7331_replay_done and n4013_predeclared_done
            else "The NGC7331 V2/V3 replay path has already been run, so NGC7331 is no "
            "longer the next replay-ready step in this roadmap. The replay result "
            "reduces the broad-window caveat for the replay path only and leaves "
            "the accepted V1 endpoint unchanged. The next protocol-level caveat "
            "path is NGC4013: it requires a predeclared replay lane or a future "
            "source-selected analogue. NGC4088 still requires either a direct "
            "source-coordinate H I product for B1 or law-level B2/B3 derivations. "
            "NGC5907 is locally accepted; its remaining caveat is only the small-N "
            "population context."
            if n7331_replay_done
            else "The next executable caveat-reduction step is NGC7331 V2/V3 replay, because "
            "it already has a replay-only source window and does not require relabeling "
            "an already inspected endpoint. NGC4013 requires a predeclared replay lane "
            "or a future source-selected analogue. NGC4088 requires either a direct "
            "source-coordinate H I product for B1 or law-level B2/B3 derivations. "
            "NGC5907 is locally accepted; its remaining caveat is only the small-N "
            "population context."
        ),
        "",
    ]
    (REPORTS / "remaining_caveat_closure_roadmap.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
