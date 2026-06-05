#!/usr/bin/env python3
"""Build the NGC7331 exact-transfer upgrade gate for the NGC4088 B2 law.

This gate checks whether NGC7331 can be promoted from a useful outer-warp
analogue to an exact transfer candidate for

    Lambda_tau = sigma_warp q_warp x_w Vflat^2.

It is source-side only. It does not score the rotation curve and does not use
endpoint residuals.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint"


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


def b(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    sparc_row = sparc.loc[sparc["Galaxy"].eq(GALAXY)].iloc[0]
    onset_summary = pd.read_csv(DATA / "ngc7331_fractional_warp_onset_source_summary.csv").iloc[0]
    onset_fields = pd.read_csv(DATA / "ngc7331_fractional_warp_onset_source_fields.csv")
    outer_fields = pd.read_csv(DATA / "ngc7331_outer_warp_vertical_caveat_fields.csv")
    exact_manifest = pd.read_csv(DATA / "ngc4088_b2_exact_transfer_candidates.csv")
    exact_row = exact_manifest.loc[exact_manifest["galaxy"].eq(GALAXY)].iloc[0]
    intake_path = DATA / "ngc7331_qwarp_observable_choice_review_intake_summary.csv"
    response_path = DATA / "ngc7331_qwarp_observable_choice_review_response_template.csv"
    intake = pd.read_csv(intake_path).iloc[0] if intake_path.exists() else None
    response = pd.read_csv(response_path).iloc[0] if response_path.exists() else None
    intake_ready = (
        intake is not None
        and str(intake["review_intake_status"])
        == "NGC7331_QWARP_REVIEW_INTAKE_FORMULA_FREEZE_INPUT_READY_NOT_ENDPOINT"
        and b(intake["formula_freeze_allowed"])
    )
    q_interval = str(response["accepted_q_warp_interval"]) if response is not None else ""
    epsilon_decision = str(response["epsilon_cross_decision"]) if response is not None else ""
    sign_decision = str(response["sign_convention_decision"]) if response is not None else ""

    vflat = float(sparc_row["Vflat_kms"])
    x_w = float(onset_summary["approx_warp_onset_over_RHI"])
    lambda_if_unit_q_sigma = x_w * vflat**2

    fields = pd.DataFrame(
        [
            {
                "field_id": "N7331_ET1_XW",
                "required_b2_field": "x_w",
                "field_status": "SOURCE_ONSET_AVAILABLE_REPLAY_ONLY",
                "value": x_w,
                "unit": "dimensionless",
                "source_basis": "Bosma/NED fractional Holmberg onset converted with SPARC distance and R_HI",
                "source_status": str(onset_summary["source_gate_status"]),
                "exact_transfer_use": "available for future exact transfer formula-freeze only; not retroactive V1 update",
            },
            {
                "field_id": "N7331_ET2_Q_WARP",
                "required_b2_field": "q_warp",
                "field_status": (
                    "SOURCE_ONLY_Q_WARP_INTERVAL_CARRIED"
                    if intake_ready
                    else "MISSING_EXACT_Q_WARP_REVIEW"
                ),
                "value": q_interval if intake_ready else pd.NA,
                "unit": "dimensionless",
                "source_basis": (
                    "source-only review carries full THINGS centroid/envelope q_warp interval"
                    if intake_ready
                    else "no accepted source-native warp-strength review analogous to NGC4088 q_warp"
                ),
                "source_status": (
                    "FORMULA_FREEZE_INPUT_READY_INTERVAL_CARRIED"
                    if intake_ready
                    else "MISSING"
                ),
                "exact_transfer_use": (
                    "available for exact B2 freeze as an explicit interval, not a scalar point"
                    if intake_ready
                    else "blocks exact B2 source-load freeze"
                ),
            },
            {
                "field_id": "N7331_ET3_SIGMA_WARP",
                "required_b2_field": "sigma_warp",
                "field_status": (
                    "MOM1_SIGN_CONTEXT_CARRIED_TO_FORMULA_FREEZE"
                    if intake_ready
                    else "OUTER_WARP_CONTEXT_AVAILABLE_SIGN_RULE_NOT_FROZEN"
                ),
                "value": sign_decision if intake_ready else pd.NA,
                "unit": "dimensionless_sign",
                "source_basis": "; ".join(
                    outer_fields.loc[
                        outer_fields["observable"].str.contains("warp", case=False, na=False),
                        "status",
                    ].astype(str)
                ),
                "source_status": (
                    "FORMULA_FREEZE_INPUT_READY_SIGN_CONTEXT_CARRIED"
                    if intake_ready
                    else "CONTEXT_AVAILABLE_NOT_EXACT_SIGN_RULE"
                ),
                "exact_transfer_use": (
                    "available as carried sign-context input; exact formula must state sign convention"
                    if intake_ready
                    else "blocks exact B2 source-load freeze until orientation/sign convention is source-frozen"
                ),
            },
            {
                "field_id": "N7331_ET4_VFLAT",
                "required_b2_field": "Vflat",
                "field_status": "SOURCE_CATALOG_AVAILABLE",
                "value": vflat,
                "unit": "km_s",
                "source_basis": "SPARC external master table",
                "source_status": "ACCEPTED_CATALOG_FIELD",
                "exact_transfer_use": "available carrier input",
            },
            {
                "field_id": "N7331_ET5_EPSILON_CROSS",
                "required_b2_field": "epsilon_cross_inputs",
                "field_status": (
                    "CONSERVATIVE_EPSILON_CROSS_BOUND_CARRIED"
                    if intake_ready
                    else "MISSING_EXACT_CROSS_TERM_OBSERVABLES"
                ),
                "value": epsilon_decision if intake_ready else pd.NA,
                "unit": "dimensionless_bound_inputs",
                "source_basis": (
                    "source-only review carries conservative MOM1/q-observable ambiguity bound"
                    if intake_ready
                    else "no accepted side-asymmetry, orientation mismatch, q/memory, and locality packet for exact B2 bound"
                ),
                "source_status": (
                    "FORMULA_FREEZE_INPUT_READY_BOUND_CARRIED"
                    if intake_ready
                    else "MISSING"
                ),
                "exact_transfer_use": (
                    "available for exact B2 freeze as an explicit uncertainty/cross-term caveat"
                    if intake_ready
                    else "blocks exact B2 source-load freeze or must be carried as explicit uncertainty"
                ),
            },
            {
                "field_id": "N7331_ET6_UNIT_Q_SIGMA_LAMBDA_PREVIEW",
                "required_b2_field": "lambda_preview_not_formula",
                "field_status": "DERIVED_PREVIEW_NOT_FORMULA_FREEZE",
                "value": lambda_if_unit_q_sigma,
                "unit": "km2_s2",
                "source_basis": "x_w * Vflat^2 assuming q=sigma=1 only as a diagnostic preview",
                "source_status": "NOT_A_FREEZE_INPUT",
                "exact_transfer_use": "for dimensional preview only; must not be scored or called a formula",
            },
        ]
    )
    fields["galaxy"] = GALAXY
    fields["endpoint_scores_allowed"] = False
    fields["uses_vobs_or_residual"] = False
    fields["claim_boundary"] = CLAIM_BOUNDARY
    fields = fields[
        [
            "galaxy",
            "field_id",
            "required_b2_field",
            "field_status",
            "value",
            "unit",
            "source_basis",
            "source_status",
            "exact_transfer_use",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_ETG1_XW_ONSET",
                "gate_status": "PASS_REPLAY_ONLY",
                "evidence": f"x_w={x_w:.6g} from fractional outer-warp onset gate",
                "remaining_obligation": "use only in future exact-transfer freeze/replay, not retroactive V1 endpoint update",
            },
            {
                "gate_id": "N7331_ETG2_VFLAT_CARRIER",
                "gate_status": "PASS",
                "evidence": f"SPARC Vflat={vflat:.6g} km/s",
                "remaining_obligation": "none at source-catalog carrier field level",
            },
            {
                "gate_id": "N7331_ETG3_Q_WARP",
                "gate_status": "PASS_INTERVAL_CARRIED" if intake_ready else "BLOCKED",
                "evidence": (
                    f"q_warp interval carried: {q_interval}"
                    if intake_ready
                    else "no exact q_warp source-strength review is accepted"
                ),
                "remaining_obligation": (
                    "carry q interval into exact-transfer formula freeze"
                    if intake_ready
                    else "measure or bound q_warp from source-native H I warp amplitude/asymmetry"
                ),
            },
            {
                "gate_id": "N7331_ETG4_SIGMA_WARP",
                "gate_status": "PASS_CONTEXT_CARRIED" if intake_ready else "BLOCKED",
                "evidence": (
                    sign_decision
                    if intake_ready
                    else "outer-warp context exists, but exact added-readout/attenuation sign rule is not frozen"
                ),
                "remaining_obligation": (
                    "state the exact added-readout/attenuation sign in the freeze gate"
                    if intake_ready
                    else "freeze orientation/sign rule from source-side warp/readout geometry"
                ),
            },
            {
                "gate_id": "N7331_ETG5_EPSILON_CROSS",
                "gate_status": "PASS_BOUND_CARRIED" if intake_ready else "BLOCKED",
                "evidence": (
                    epsilon_decision
                    if intake_ready
                    else "no exact cross-term source-observable packet exists"
                ),
                "remaining_obligation": (
                    "carry conservative epsilon_cross caveat into exact-transfer formula freeze"
                    if intake_ready
                    else "build side-asymmetry, orientation mismatch, memory/history, and locality packet"
                ),
            },
            {
                "gate_id": "N7331_ETG6_DIMENSION_PREVIEW",
                "gate_status": "PASS_NOT_FREEZE",
                "evidence": "x_w * Vflat^2 has velocity-squared units",
                "remaining_obligation": "do not score the preview lambda without q/sigma/cross-term freeze",
            },
            {
                "gate_id": "N7331_ETG7_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "all fields are source-side or catalog-side; no vobs residuals are read",
                "remaining_obligation": "keep any future scoring in a separate endpoint script",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    if intake_ready:
        work_items = [
            {
                "work_item": "W1_EXACT_TRANSFER_FORMULA_FREEZE_GATE",
                "missing_field": "none_at_input_gate",
                "preferred_source": "validated q interval, MOM1 sign context, and conservative epsilon_cross bound",
                "acceptance_rule": "freeze exact-transfer formula without reading vobs or endpoint residuals",
            },
            {
                "work_item": "W2_INTERVAL_PROPAGATION",
                "missing_field": "point_q_warp_not_selected",
                "preferred_source": "CARRY_INTERVAL source-only review response",
                "acceptance_rule": "carry q_warp interval rather than collapsing to a scalar unless a future source theorem selects one observable",
            },
            {
                "work_item": "W3_ENDPOINT_GATE_AFTER_FREEZE",
                "missing_field": "endpoint_score_not_allowed_yet",
                "preferred_source": "future formula-freeze manifest",
                "acceptance_rule": "only a separate endpoint gate may read vobs after the freeze manifest is fixed",
            },
        ]
    else:
        work_items = [
            {
                "work_item": "W1_Q_WARP_SOURCE_STRENGTH_REVIEW",
                "missing_field": "q_warp",
                "preferred_source": "source-native H I warp map or literature warp-amplitude/asymmetry measurement",
                "acceptance_rule": "numeric or bounded q_warp fixed before endpoint scoring",
            },
            {
                "work_item": "W2_SIGMA_WARP_SIGN_RULE",
                "missing_field": "sigma_warp",
                "preferred_source": "source-side orientation/readout geometry and whether the outer warp implies added-readout or attenuation",
                "acceptance_rule": "sign convention frozen without using rotation residuals",
            },
            {
                "work_item": "W3_EPSILON_CROSS_PACKET",
                "missing_field": "epsilon_cross_inputs",
                "preferred_source": "orientation mismatch, side asymmetry, memory/history context, and locality observables",
                "acceptance_rule": "closed bound or explicitly carried uncertainty interval",
            },
        ]
    worklist = pd.DataFrame(work_items)
    worklist["galaxy"] = GALAXY
    worklist["endpoint_scores_allowed"] = False
    worklist["uses_vobs_or_residual"] = False
    worklist["claim_boundary"] = CLAIM_BOUNDARY
    worklist = worklist[
        [
            "galaxy",
            "work_item",
            "missing_field",
            "preferred_source",
            "acceptance_rule",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    pass_like = {
        "PASS",
        "PASS_REPLAY_ONLY",
        "PASS_NOT_FREEZE",
        "PASS_INTERVAL_CARRIED",
        "PASS_CONTEXT_CARRIED",
        "PASS_BOUND_CARRIED",
    }
    n_blocked = int(gates["gate_status"].eq("BLOCKED").sum())
    formula_freeze_allowed = intake_ready and n_blocked == 0
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "exact_transfer_upgrade_status": (
                    "NGC7331_EXACT_TRANSFER_UPGRADE_FORMULA_FREEZE_INPUT_READY_NOT_ENDPOINT"
                    if formula_freeze_allowed
                    else "NGC7331_EXACT_TRANSFER_UPGRADE_GATE_BUILT_FORMULA_FREEZE_BLOCKED"
                ),
                "source_candidate_status_from_manifest": str(exact_row["candidate_status"]),
                "x_w_available": True,
                "vflat_available": True,
                "q_warp_available": intake_ready,
                "sigma_warp_available": intake_ready,
                "epsilon_cross_inputs_available": intake_ready,
                "unit_q_sigma_lambda_preview_km2_s2": lambda_if_unit_q_sigma,
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].isin(pass_like).sum()),
                "n_blocked": n_blocked,
                "formula_freeze_allowed": formula_freeze_allowed,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "population_claim_allowed": False,
                "next_required_action": (
                    "build exact B2 transfer formula-freeze gate carrying q interval and epsilon caveat"
                    if formula_freeze_allowed
                    else "fill q_warp, sigma_warp, and epsilon_cross source packets before "
                    "any exact B2 transfer formula freeze"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    fields.to_csv(DATA / "ngc7331_b2_exact_transfer_upgrade_fields.csv", index=False)
    gates.to_csv(DATA / "ngc7331_b2_exact_transfer_upgrade_gate.csv", index=False)
    worklist.to_csv(DATA / "ngc7331_b2_exact_transfer_upgrade_worklist.csv", index=False)
    summary.to_csv(DATA / "ngc7331_b2_exact_transfer_upgrade_summary.csv", index=False)

    report = [
        "# NGC7331 B2 Exact Transfer Upgrade Gate",
        "",
        "This gate checks whether NGC7331 can move from outer-warp analogue to",
        "exact NGC4088-style B2 source-load transfer. It is not an endpoint score.",
        "",
        "## Fields",
        "",
        markdown_table(fields),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Worklist",
        "",
        markdown_table(worklist),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        (
            "NGC7331 has now cleared the response-pending source-input blocker: "
            "q_warp is carried as a THINGS centroid/envelope interval, MOM1 supplies "
            "orientation context, and epsilon_cross is carried as a conservative "
            "source-side caveat. This is formula-freeze input readiness, not an "
            "endpoint result; a separate exact-transfer formula-freeze gate must "
            "still be built before any scoring."
            if formula_freeze_allowed
            else "NGC7331 is a real upgrade target because the residual-blind fractional "
            "outer-warp onset and SPARC Vflat carrier are available. It is not yet an "
            "exact B2 transfer case: q_warp, sigma_warp, and epsilon_cross source "
            "packets remain missing. The preview x_w Vflat^2 scale is dimensional "
            "bookkeeping only and must not be scored as a frozen formula."
        ),
        "",
    ]
    (REPORTS / "ngc7331_b2_exact_transfer_upgrade_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
