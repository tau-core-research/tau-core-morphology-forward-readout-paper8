#!/usr/bin/env python3
"""Clarify the NGC4013 retrospective caveat closure path.

This gate does not try to erase the retrospective caveat.  It records what is
already transferable from NGC4013, what is still forbidden, and which
source-selected analogues could reduce the caveat in a future replay/holdout
or prospective endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4013_retrospective_caveat_closure_gate_not_endpoint"


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


def first_existing(row: pd.Series, columns: tuple[str, ...]) -> str:
    for column in columns:
        if column in row.index:
            return str(row[column])
    raise KeyError(f"none of the expected columns were found: {columns}")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    blocker = pd.read_csv(
        DATA / "ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_summary.csv"
    ).iloc[0]
    source_rule = pd.read_csv(DATA / "ngc4013_mixed_source_rule_summary.csv").iloc[0]
    freeze = pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_summary.csv").iloc[0]
    control = pd.read_csv(DATA / "mixed_readout_population_control_by_galaxy.csv")
    queue = pd.read_csv(DATA / "mixed_readout_candidate_acquisition_queue.csv")
    expansion = pd.read_csv(DATA / "mixed_readout_population_expansion_candidates.csv")

    n4013_control = control.loc[control["galaxy"].eq("NGC4013")].iloc[0]
    exact_analogue_ready = queue.loc[
        (~queue["galaxy"].eq("NGC4013"))
        & queue["candidate_mixed_readout"].eq("K_expdisk_warp_vertical_overlay")
        & queue["source_rule_candidate"].eq(True)
        & queue["has_numeric_warp_activation"].eq(True)
        & queue["has_numeric_vertical_activation"].eq(True)
    ].copy()

    analogue_rows = []
    for _, row in expansion.iterrows():
        analogue_rows.append(
            {
                "galaxy": row["galaxy"],
                "candidate_readout": row["candidate_readout"],
                "analogue_class": (
                    "closest_warp_history_not_same_protocol"
                    if row["galaxy"] == "NGC4088"
                    else "source_acquisition_candidate"
                ),
                "source_side_strength": row["source_side_strength"],
                "formula_freeze_allowed_now": bool(row["formula_freeze_allowed_now"]),
                "main_blockers": row["main_blockers"],
                "next_required_gate": row["next_required_gate"],
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    analogues = pd.DataFrame(analogue_rows)

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4013_RCC1_SOURCE_RULE_TRANSFERABLE",
                "gate_status": "PASS",
                "evidence": first_existing(
                    source_rule, ("source_rule_status", "source_support_status")
                ),
                "remaining_obligation": "none for protocol transfer",
            },
            {
                "gate_id": "N4013_RCC2_FORMULA_FREEZE_TRANSFERABLE",
                "gate_status": "PASS",
                "evidence": str(freeze["formula_freeze_status"]),
                "remaining_obligation": "future use must read the frozen manifest unchanged",
            },
            {
                "gate_id": "N4013_RCC3_CONTROL_SIGNAL_RECORDED",
                "gate_status": "PASS_DIAGNOSTIC",
                "evidence": (
                    f"matched rank={int(n4013_control['matched_rank_within_galaxy'])}; "
                    "matched-minus-best-wrong="
                    f"{float(n4013_control['matched_minus_wrong_best']):.6g}"
                ),
                "remaining_obligation": "diagnostic/control score cannot be used to accept the old endpoint",
            },
            {
                "gate_id": "N4013_RCC4_RETROACTIVE_SCORE_FORBIDDEN",
                "gate_status": "BLOCKED_RETROACTIVE_ENDPOINT",
                "evidence": str(blocker["blocker_status"]),
                "remaining_obligation": "do not promote the existing NGC4013 score to accepted endpoint evidence",
            },
            {
                "gate_id": "N4013_RCC5_EXACT_ANALOGUE_NOT_READY",
                "gate_status": "BLOCKED_FUTURE_ANALOGUE_REQUIRED"
                if exact_analogue_ready.empty
                else "PASS_EXACT_ANALOGUE_READY",
                "evidence": f"exact non-NGC4013 source-rule analogue ready count={len(exact_analogue_ready)}",
                "remaining_obligation": (
                    "acquire or promote a future source-selected analogue before claiming retrospective-caveat reduction"
                ),
            },
        ]
    )
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "closure_gate_status": "NGC4013_RETROSPECTIVE_CAVEAT_CLOSURE_PATH_FORMALIZED_NOT_CLOSED",
                "source_rule_transferable": True,
                "formula_freeze_transferable": True,
                "control_signal_recorded": True,
                "retrospective_endpoint_score_forbidden": True,
                "exact_non_ngc4013_analogue_ready_count": len(exact_analogue_ready),
                "nearest_analogue_candidate": "NGC4088",
                "nearest_analogue_freeze_allowed_now": False,
                "endpoint_status_changed": False,
                "endpoint_scores_recomputed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates.to_csv(DATA / "ngc4013_retrospective_caveat_closure_gates.csv", index=False)
    analogues.to_csv(DATA / "ngc4013_retrospective_caveat_analogue_candidates.csv", index=False)
    summary.to_csv(DATA / "ngc4013_retrospective_caveat_closure_summary.csv", index=False)

    report = [
        "# NGC4013 Retrospective Caveat Closure Gate",
        "",
        "This gate formalizes the closure path for the NGC4013 retrospective",
        "caveat. It does not change the endpoint status and does not score a",
        "curve.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Analogue Candidates",
        "",
        markdown_table(analogues),
        "",
        "## Interpretation",
        "",
        "Status: the retrospective caveat is formalized, but it is not closed.",
        "",
        "NGC4013's mixed protocol is transferable: the source rule is ready, the",
        "formula is frozen, and the control signal is recorded. The caveat is not",
        "closed; it is only formalized because the score was inspected before accepted endpoint",
        "promotion. The current package has no exact non-NGC4013 analogue with the",
        "same source-rule readiness. NGC4088 is the closest source-bound analogue,",
        "but its warp/history lane is not the same protocol and remains caveated.",
        "",
    ]
    (REPORTS / "ngc4013_retrospective_caveat_closure_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
