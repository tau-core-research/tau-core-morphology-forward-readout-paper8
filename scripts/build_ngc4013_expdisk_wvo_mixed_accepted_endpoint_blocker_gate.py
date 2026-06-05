#!/usr/bin/env python3
"""Build the NGC4013 accepted mixed-endpoint blocker gate."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_not_score"


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

    freeze = pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_summary.csv").iloc[0]
    manifest = pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_manifest.csv").iloc[0]
    audit_scores = pd.read_csv(DATA / "ngc4013_expdisk_wvo_frozen_protocol_scores.csv").iloc[0]
    control = pd.read_csv(DATA / "mixed_readout_population_control_by_galaxy.csv")
    control_row = control.loc[control["galaxy"].eq("NGC4013")].iloc[0]

    source_rule_ready = bool(freeze["source_rule_pass"])
    formula_frozen = bool(freeze["overlay_formula_frozen"])
    endpoint_blind = not bool(freeze["uses_vobs_or_residual_in_construction"])
    prospective_ready = bool(freeze["prospective_endpoint_protocol_ready"])
    retroactive_blocker = not bool(freeze["retrospective_endpoint_scores_allowed"])
    prior_diagnostic_dependency = True
    endpoint_scores_allowed = False

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4013_MAEB1_SOURCE_RULE_READY",
                "gate_status": "PASS" if source_rule_ready else "BLOCKED",
                "evidence": str(freeze["mixed_readout_candidate"]),
                "remaining_obligation": "none at source-rule level",
            },
            {
                "gate_id": "N4013_MAEB2_FORMULA_FROZEN_BEFORE_FUTURE_SCORING",
                "gate_status": "PASS" if formula_frozen and prospective_ready else "BLOCKED",
                "evidence": str(freeze["formula_freeze_status"]),
                "remaining_obligation": "may be reused only prospectively or in a predeclared replay lane",
            },
            {
                "gate_id": "N4013_MAEB3_ENDPOINT_BLIND_CONSTRUCTION",
                "gate_status": "PASS" if endpoint_blind else "BLOCKED",
                "evidence": "frozen manifest construction uses source rule and WVO freeze manifest only",
                "remaining_obligation": "scoring must remain separate",
            },
            {
                "gate_id": "N4013_MAEB4_RETROACTIVE_ENDPOINT_BLOCKER",
                "gate_status": "BLOCKED_RETROACTIVE_ENDPOINT",
                "evidence": "mixed expdisk+WVO lane was developed after NGC4013 wrong-family/control inspection",
                "remaining_obligation": "do not promote the existing NGC4013 mixed score to accepted endpoint evidence",
            },
            {
                "gate_id": "N4013_MAEB5_REPLAY_OR_HOLDOUT_REQUIREMENT",
                "gate_status": "BLOCKED_REPLAY_REQUIRED",
                "evidence": "accepted endpoint would require a predeclared replay protocol, new source-frozen galaxy, or holdout rule fixed before scoring",
                "remaining_obligation": "define prospective replay/holdout lane before any accepted NGC4013 mixed endpoint claim",
            },
        ]
    )
    gates["galaxy"] = "NGC4013"
    gates["formula_id"] = str(freeze["formula_id"])
    gates["endpoint_scores_allowed"] = endpoint_scores_allowed
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "formula_id",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "formula_id": str(freeze["formula_id"]),
                "blocker_status": "MIXED_ACCEPTED_ENDPOINT_BLOCKED_RETROACTIVE_PROTOCOL_READY",
                "source_rule_ready": source_rule_ready,
                "formula_frozen_for_future_scoring": bool(formula_frozen and prospective_ready),
                "endpoint_blind_construction": endpoint_blind,
                "prior_diagnostic_dependency": prior_diagnostic_dependency,
                "retrospective_endpoint_scores_allowed": False,
                "endpoint_scores_allowed": endpoint_scores_allowed,
                "frozen_protocol_rmse_km_s": float(
                    audit_scores["rmse_expdisk_wvo_frozen_protocol"]
                ),
                "best_local_baseline_rmse_km_s": float(
                    min(
                        audit_scores["rmse_newton"],
                        audit_scores["rmse_tpg_v6"],
                        audit_scores["rmse_mond"],
                        audit_scores["rmse_exponential_disk"],
                    )
                ),
                "wrong_mixed_mean_rmse_km_s": float(control_row["wrong_mean_rmse"]),
                "wrong_mixed_best_rmse_km_s": float(control_row["wrong_best_rmse"]),
                "matched_beats_all_wrong_mixed_families": bool(
                    control_row["matched_beats_all_wrong_labels"]
                ),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_blocked": int(gates["gate_status"].str.startswith("BLOCKED").sum()),
                "next_required_action": "predeclare replay/holdout endpoint lane or use this formula only on future source-selected cases",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates.to_csv(DATA / "ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_gate.csv", index=False)
    summary.to_csv(
        DATA / "ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_summary.csv",
        index=False,
    )

    report = [
        "# NGC4013 Mixed Accepted-Endpoint Blocker Gate",
        "",
        "This gate records why the strong NGC4013 exponential-disk + WVO mixed",
        "curve cannot be promoted to an accepted single-galaxy endpoint in the",
        "current package, despite being source-frozen and endpoint-blind at formula",
        "construction level.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Interpretation",
        "",
        "The formula is useful and prospective-ready, but the existing NGC4013 score",
        "is retrospective because the mixed branch was developed after inspecting the",
        "NGC4013 wrong-family/control context. Therefore it remains a frozen-reference",
        "row rather than an accepted endpoint row. Promotion requires a predeclared",
        "replay/holdout lane or application to future source-selected cases.",
        "",
    ]
    (REPORTS / "ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
