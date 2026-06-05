#!/usr/bin/env python3
"""Build the population validation gate for mixed 4D readouts.

This gate states the empirical proof target for mixed readouts. It does not
score rotations. It records which current rows are source-rule ready, which are
controls or acquisition candidates, and what endpoint conditions must pass
before a mixed-readout claim can be made.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "mixed_readout_population_validation_gate_not_endpoint"


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


def optional_row(path: Path) -> pd.Series | None:
    if not path.exists():
        return None
    df = pd.read_csv(path)
    if df.empty:
        return None
    return df.iloc[0]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    mixed_cases = pd.read_csv(DATA / "mixed_readout_source_selection_cases.csv")
    freeze_summary = pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_summary.csv").iloc[0]
    ngc5907_mixed_freeze = optional_row(
        DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_summary.csv"
    )
    ngc7331_mixed_freeze = optional_row(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_summary.csv"
    )
    accepted_audit = pd.read_csv(DATA / "readout_subfamily_accepted_manifest_audit.csv")

    protocol = pd.DataFrame(
        [
            {
                "gate_id": "MPG1_RESIDUAL_BLIND_LABEL",
                "required_condition": "mixed candidates are selected from source fields before rotation scoring",
                "pass_measure": "source_rule_pass=True and diagnostic scores excluded as label inputs",
                "failure_mode": "mixed label chosen from RMSE, required S_tau, or wrong-family result",
            },
            {
                "gate_id": "MPG2_FORMULA_FREEZE",
                "required_condition": "carrier, overlay kernel, sign, amplitude, and radial window are frozen before scoring",
                "pass_measure": "formula_freeze_status is ready and uses_vobs_or_residual_in_construction=False",
                "failure_mode": "formula ingredient changed after observing endpoint residuals",
            },
            {
                "gate_id": "MPG3_MATCHED_VS_PURE_CONTROLS",
                "required_condition": "mixed readout beats its pure carrier and pure overlay controls",
                "pass_measure": "RMSE_mixed < RMSE_pure_carrier and RMSE_mixed < RMSE_pure_overlay",
                "failure_mode": "mixed shell acts only as an over-flexible or redundant correction",
            },
            {
                "gate_id": "MPG4_MATCHED_VS_WRONG_AND_SHUFFLED",
                "required_condition": "mixed matched labels beat wrong-family and shuffled-label controls",
                "pass_measure": "Delta_mixed > 0 and correct-family rank improves against shuffled/null labels",
                "failure_mode": "improvement also appears under wrong or shuffled labels",
            },
            {
                "gate_id": "MPG5_BASELINE_COMPARISON",
                "required_condition": "mixed readout is compared with Newtonian, MOND/RAR, and TPG/RMOND-facing baselines",
                "pass_measure": "baseline competitiveness reported without claiming universal superiority unless population endpoint passes",
                "failure_mode": "baseline comparison omitted or overclaimed",
            },
            {
                "gate_id": "MPG6_NEGATIVE_CONTROL",
                "required_condition": "non-mixed source-control galaxies should not be systematically improved by the mixed formula",
                "pass_measure": "mixed-readout improvement concentrates in source-rule-positive cases",
                "failure_mode": "mixed formula improves everything, suggesting excess flexibility",
            },
        ]
    )
    protocol["claim_boundary"] = CLAIM_BOUNDARY

    current_cases = []
    for _, row in mixed_cases.iterrows():
        current_cases.append(
            {
                "galaxy": row["galaxy"],
                "case_role": "source_rule_positive_mixed_candidate",
                "candidate_mixed_readout": row["candidate_mixed_readout"],
                "source_rule_pass": bool(row["source_rule_pass"]),
                "formula_freeze_status": (
                    str(freeze_summary["formula_freeze_status"])
                    if row["galaxy"] == "NGC4013"
                    else "NOT_BUILT"
                ),
                "prospective_protocol_ready": (
                    bool(freeze_summary["prospective_endpoint_protocol_ready"])
                    if row["galaxy"] == "NGC4013"
                    else False
                ),
                "retrospective_endpoint_allowed": False,
                "population_validation_use": "prospective_protocol_case_only_not_validation",
                "reason": "source-rule and formula-freeze pass, but existing mixed score is not retroactive endpoint validation",
            }
        )

    if ngc5907_mixed_freeze is not None:
        current_cases.append(
            {
                "galaxy": "NGC5907",
                "case_role": "source_rule_positive_mixed_formula_freeze_candidate",
                "candidate_mixed_readout": str(ngc5907_mixed_freeze["mixed_readout_candidate"]),
                "source_rule_pass": bool(ngc5907_mixed_freeze["source_rule_candidate"]),
                "formula_freeze_status": str(ngc5907_mixed_freeze["formula_freeze_status"]),
                "prospective_protocol_ready": bool(
                    ngc5907_mixed_freeze["prospective_mixed_protocol_ready"]
                ),
                "retrospective_endpoint_allowed": False,
                "population_validation_use": "prospective_protocol_case_only_not_validation",
                "reason": "fresh mixed formula-freeze exists, but prior projection endpoint cannot be reused as mixed-readout evidence and no mixed endpoint score is run here",
            }
        )

    if ngc7331_mixed_freeze is not None:
        current_cases.append(
            {
                "galaxy": "NGC7331",
                "case_role": "caveated_source_rule_positive_mixed_formula_freeze_candidate",
                "candidate_mixed_readout": str(ngc7331_mixed_freeze["mixed_readout_candidate"]),
                "source_rule_pass": bool(ngc7331_mixed_freeze["source_rule_candidate"]),
                "formula_freeze_status": str(ngc7331_mixed_freeze["formula_freeze_status"]),
                "prospective_protocol_ready": bool(
                    ngc7331_mixed_freeze["prospective_mixed_protocol_ready"]
                ),
                "retrospective_endpoint_allowed": False,
                "population_validation_use": "caveated_prospective_protocol_case_only_not_validation",
                "reason": "caveated vertical/outer-warp mixed formula-freeze exists, but broad outer window must be reported and no mixed endpoint score is run here",
            }
        )

    control_rows = {
        "IC2574": "disturbed_tail_control_not_mixed",
        "UGC05716": "tail_asymmetry_candidate_control_not_mixed",
        "NGC4183": "expdisk_overlay_acquisition_candidate_context_only",
    }
    if ngc5907_mixed_freeze is None:
        control_rows["NGC5907"] = "projection_dominated_accepted_control_not_mixed"
    if ngc7331_mixed_freeze is None:
        control_rows["NGC7331"] = "vertical_thick_regular_caveated_control_not_mixed"
    for galaxy, role in control_rows.items():
        audit_row = accepted_audit.loc[accepted_audit["galaxy"].eq(galaxy)]
        audit_decision = str(audit_row.iloc[0]["audit_decision"]) if len(audit_row) else "NO_AUDIT_ROW"
        current_cases.append(
            {
                "galaxy": galaxy,
                "case_role": role,
                "candidate_mixed_readout": "not_source_rule_positive_mixed_case",
                "source_rule_pass": False,
                "formula_freeze_status": "NOT_APPLICABLE",
                "prospective_protocol_ready": False,
                "retrospective_endpoint_allowed": False,
                "population_validation_use": "negative_or_acquisition_control",
                "reason": audit_decision,
            }
        )

    cases = pd.DataFrame(current_cases)
    n_source_ready = int(cases["source_rule_pass"].sum())
    n_prospective_ready = int(cases["prospective_protocol_ready"].sum())
    min_independent_prospective_cases = 3
    validation_ready = n_prospective_ready >= min_independent_prospective_cases

    endpoints = pd.DataFrame(
        [
            {
                "endpoint_id": "DELTA_MIXED_PURE",
                "definition": "mean or median RMSE(best pure carrier/overlay control) - RMSE(matched mixed readout)",
                "pass_condition": "> 0 on predeclared mixed source-rule-positive cases",
                "status": "NOT_RUN_POPULATION_ENDPOINT",
            },
            {
                "endpoint_id": "DELTA_MIXED_WRONG",
                "definition": "RMSE(wrong-family mean) - RMSE(matched mixed readout)",
                "pass_condition": "> 0 and correct family rank improves",
                "status": "NOT_RUN_POPULATION_ENDPOINT",
            },
            {
                "endpoint_id": "SHUFFLED_MIXED_NULL",
                "definition": "matched-vs-shuffled improvement under randomized mixed labels",
                "pass_condition": "predeclared matched labels beat shuffled/null labels",
                "status": "NOT_RUN_POPULATION_ENDPOINT",
            },
            {
                "endpoint_id": "BASELINE_COMPETITIVENESS",
                "definition": "mixed readout versus Newtonian, MOND/RAR proxy, TPG/v6/RMOND-facing proxy",
                "pass_condition": "reported with caveats; no universal superiority claim unless population endpoint passes",
                "status": "NOT_RUN_POPULATION_ENDPOINT",
            },
            {
                "endpoint_id": "NON_MIXED_NEGATIVE_CONTROL",
                "definition": "apply mixed formula only as forbidden/control lane to non-mixed source-rule-negative galaxies",
                "pass_condition": "mixed improvement is not systematic in non-mixed controls",
                "status": "NOT_RUN_POPULATION_ENDPOINT",
            },
        ]
    )
    endpoints["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "validation_gate_status": (
                    "MIXED_POPULATION_VALIDATION_READY"
                    if validation_ready
                    else "MIXED_POPULATION_VALIDATION_BLOCKED_MORE_PROSPECTIVE_CASES_REQUIRED"
                ),
                "n_cases_listed": len(cases),
                "n_source_rule_positive_mixed_cases": n_source_ready,
                "n_prospective_protocol_ready_cases": n_prospective_ready,
                "min_independent_prospective_cases_required": min_independent_prospective_cases,
                "endpoint_scores_run": False,
                "diagnostic_scores_used_as_label_input": False,
                "current_claim": "NGC4013 supplies a frozen prospective mixed protocol, not population proof",
                "next_required_action": "acquire or promote at least two more residual-blind mixed candidates and freeze their formulas before scoring",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    if n_prospective_ready == 2:
        summary.loc[0, "current_claim"] = (
            "NGC4013 and NGC5907 supply frozen prospective mixed protocols, "
            "but no population proof and no mixed endpoint scoring here"
        )
        summary.loc[0, "next_required_action"] = (
            "acquire or promote at least one more residual-blind mixed candidate "
            "and freeze its formula before population scoring"
        )
    if n_prospective_ready >= min_independent_prospective_cases:
        summary.loc[0, "current_claim"] = (
            "NGC4013, NGC5907, and caveated NGC7331 supply frozen prospective "
            "mixed protocols, but no mixed endpoint scoring has been run here"
        )
        summary.loc[0, "next_required_action"] = (
            "run the predeclared mixed-population endpoints from unchanged "
            "frozen manifests, preserving NGC7331 broad-window caveats"
        )

    protocol.to_csv(DATA / "mixed_readout_population_validation_protocol.csv", index=False)
    cases.to_csv(DATA / "mixed_readout_population_validation_cases.csv", index=False)
    endpoints.to_csv(DATA / "mixed_readout_population_validation_endpoints.csv", index=False)
    summary.to_csv(DATA / "mixed_readout_population_validation_summary.csv", index=False)

    report = [
        "# Mixed Readout Population Validation Gate",
        "",
        "This gate states what would count as evidence for the mixed 4D readout",
        "program. It does not score rotations and does not promote NGC4013",
        "retroactively. It turns the proof idea into a predeclared population",
        "protocol.",
        "",
        "## Protocol",
        "",
        markdown_table(protocol),
        "",
        "## Current Cases And Controls",
        "",
        markdown_table(cases),
        "",
        "## Endpoints To Run After Freeze",
        "",
        markdown_table(endpoints),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "The current package still does not have enough independent prospective",
        "mixed protocols for population validation. Frozen protocol rows are",
        "formula-preparation results only; population scoring remains blocked",
        "until the minimum case count is reached and the scoring endpoints are",
        "run from unchanged frozen manifests.",
    ]
    (REPORTS / "mixed_readout_population_validation_gate.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
