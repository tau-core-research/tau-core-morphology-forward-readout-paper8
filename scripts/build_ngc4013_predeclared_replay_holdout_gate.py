#!/usr/bin/env python3
"""Build the NGC4013 predeclared replay/holdout eligibility gate.

This gate does not score a rotation curve. It converts the retrospective
NGC4013 caveat into explicit future-use rules: which parts of the mixed
protocol can be transferred, which score remains quarantined, and which
future routes could make the protocol endpoint-eligible.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4013_predeclared_replay_holdout_gate_not_endpoint"


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


def require_row(path: Path) -> pd.Series:
    if not path.exists():
        raise FileNotFoundError(path)
    table = pd.read_csv(path)
    if table.empty:
        raise ValueError(f"{path} is empty")
    return table.iloc[0]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    closure = require_row(DATA / "ngc4013_retrospective_caveat_closure_summary.csv")
    freeze = require_row(DATA / "ngc4013_expdisk_wvo_formula_freeze_summary.csv")
    manifest = require_row(DATA / "ngc4013_expdisk_wvo_formula_freeze_manifest.csv")
    blocker = require_row(
        DATA / "ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_summary.csv"
    )
    analogues = pd.read_csv(DATA / "ngc4013_retrospective_caveat_analogue_candidates.csv")

    exact_analogue_count = int(closure["exact_non_ngc4013_analogue_ready_count"])
    source_transferable = bool(closure["source_rule_transferable"])
    formula_transferable = bool(closure["formula_freeze_transferable"])
    retrospective_forbidden = bool(closure["retrospective_endpoint_score_forbidden"])
    prospective_protocol_ready = bool(freeze["prospective_endpoint_protocol_ready"])

    route_rows = [
        {
            "route_id": "R1_SAME_CURVE_REPLAY",
            "route_status": "BLOCKED_RETROSPECTIVE_CURVE_ALREADY_INSPECTED",
            "allowed_future_use": False,
            "endpoint_scores_allowed_now": False,
            "reason": (
                "the existing NGC4013 rotation curve and controls have already been inspected; "
                "rescoring the same curve cannot remove the retrospective caveat"
            ),
            "required_next_input": "none; route is protocol-forbidden",
        },
        {
            "route_id": "R2_PREDECLARED_NEW_HOLDOUT",
            "route_status": "FUTURE_ONLY_REQUIRES_UNINSPECTED_HOLDOUT_DATA",
            "allowed_future_use": True,
            "endpoint_scores_allowed_now": False,
            "reason": (
                "the frozen source rule and formula may be applied only if the holdout target "
                "is declared before endpoint residuals or score ranks are inspected"
            ),
            "required_next_input": "new uninspected NGC4013-compatible holdout target or data release",
        },
        {
            "route_id": "R3_SOURCE_SELECTED_ANALOGUE",
            "route_status": (
                "BLOCKED_NO_EXACT_ANALOGUE_READY"
                if exact_analogue_count == 0
                else "READY_EXACT_ANALOGUE_AVAILABLE"
            ),
            "allowed_future_use": exact_analogue_count > 0,
            "endpoint_scores_allowed_now": False,
            "reason": (
                "no non-NGC4013 galaxy currently has the same expdisk+WVO source-rule readiness"
                if exact_analogue_count == 0
                else "at least one exact source-selected analogue is available"
            ),
            "required_next_input": "promote an exact non-NGC4013 source-selected analogue",
        },
        {
            "route_id": "R4_POPULATION_REPLAY",
            "route_status": "FUTURE_ONLY_POPULATION_PROTOCOL",
            "allowed_future_use": True,
            "endpoint_scores_allowed_now": False,
            "reason": (
                "the NGC4013 protocol can be one predeclared member of a future population replay, "
                "but not a standalone retroactive endpoint"
            ),
            "required_next_input": "predeclared population packet with source-selected rows",
        },
    ]
    routes = pd.DataFrame(route_rows)
    routes["claim_boundary"] = CLAIM_BOUNDARY

    gate_rows = [
        {
            "gate_id": "N4013_PRH1_SOURCE_RULE_TRANSFER",
            "gate_status": "PASS" if source_transferable else "BLOCKED",
            "evidence": str(closure["closure_gate_status"]),
            "remaining_obligation": "future route must read the source rule unchanged",
        },
        {
            "gate_id": "N4013_PRH2_FORMULA_MANIFEST_TRANSFER",
            "gate_status": "PASS" if formula_transferable and prospective_protocol_ready else "BLOCKED",
            "evidence": str(freeze["formula_freeze_status"]),
            "remaining_obligation": "future route must read the frozen formula manifest unchanged",
        },
        {
            "gate_id": "N4013_PRH3_RETROSPECTIVE_SCORE_QUARANTINE",
            "gate_status": "PASS_SCORE_QUARANTINED" if retrospective_forbidden else "BLOCKED",
            "evidence": str(blocker["blocker_status"]),
            "remaining_obligation": "do not use the existing NGC4013 score as accepted endpoint evidence",
        },
        {
            "gate_id": "N4013_PRH4_EXACT_ANALOGUE_AVAILABILITY",
            "gate_status": (
                "BLOCKED_FUTURE_ANALOGUE_REQUIRED"
                if exact_analogue_count == 0
                else "PASS_EXACT_ANALOGUE_AVAILABLE"
            ),
            "evidence": f"exact_non_ngc4013_analogue_ready_count={exact_analogue_count}",
            "remaining_obligation": "source-select a non-NGC4013 analogue before analogue endpoint scoring",
        },
        {
            "gate_id": "N4013_PRH5_NO_CURRENT_ENDPOINT_SCORE",
            "gate_status": "BLOCKED_ENDPOINT_SCORE_NOT_ALLOWED_NOW",
            "evidence": "this gate does not read vobs and does not score a curve",
            "remaining_obligation": "endpoint scoring requires a future predeclared route",
        },
    ]
    gates = pd.DataFrame(gate_rows)
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "predeclared_replay_gate_status": (
                    "NGC4013_PREDECLARED_REPLAY_HOLDOUT_GATE_BUILT_ENDPOINT_STILL_BLOCKED"
                ),
                "source_rule_transferable": source_transferable,
                "formula_manifest_transferable": formula_transferable,
                "prospective_endpoint_protocol_ready": prospective_protocol_ready,
                "existing_score_quarantined": retrospective_forbidden,
                "same_curve_replay_allowed": False,
                "future_holdout_route_defined": True,
                "future_analogue_route_defined": True,
                "exact_non_ngc4013_analogue_ready_count": exact_analogue_count,
                "endpoint_scores_allowed": False,
                "endpoint_scores_recomputed": False,
                "uses_vobs_or_residual": False,
                "uses_existing_score_summary_as_diagnostic_context": True,
                "next_required_gate": "FUTURE_UNINSPECTED_HOLDOUT_OR_SOURCE_SELECTED_ANALOGUE",
                "formula_id": str(manifest["formula_id"]),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    summary.to_csv(DATA / "ngc4013_predeclared_replay_holdout_summary.csv", index=False)
    gates.to_csv(DATA / "ngc4013_predeclared_replay_holdout_gates.csv", index=False)
    routes.to_csv(DATA / "ngc4013_predeclared_replay_holdout_routes.csv", index=False)

    report = [
        "# NGC4013 Predeclared Replay/Holdout Gate",
        "",
        "This gate converts the NGC4013 retrospective caveat into explicit future-use",
        "rules. It does not score a rotation curve and does not change the endpoint",
        "status.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Future Routes",
        "",
        markdown_table(routes),
        "",
        "## Analogue Snapshot",
        "",
        markdown_table(analogues),
        "",
        "## Interpretation",
        "",
        "Status: the NGC4013 source rule and frozen expdisk+WVO formula are transferable,",
        "but the existing score remains quarantined. A same-curve replay is explicitly",
        "blocked because the NGC4013 curve and controls have already been inspected.",
        "The admissible routes are future-only: a genuinely predeclared uninspected",
        "holdout target, a source-selected non-NGC4013 analogue, or a predeclared",
        "population replay packet. Therefore this gate narrows the caveat but does",
        "not close it.",
        "",
    ]
    (REPORTS / "ngc4013_predeclared_replay_holdout_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
