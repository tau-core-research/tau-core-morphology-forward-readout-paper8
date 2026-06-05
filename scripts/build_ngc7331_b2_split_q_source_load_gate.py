#!/usr/bin/env python3
"""Build the NGC7331 B2 split q/source-load theory gate.

This gate responds to the diagnostic finding that the transferred NGC4088 B2
formula uses q_warp both in the source-load amplitude and in the radial kernel.
It reformulates the B2 shell with two distinct quantities:

    q_shape  -- residual-blind morphology/kernel handle;
    mu_load  -- Tau-side source-load/readout coupling handle.

The gate is theory/pre-freeze only. It does not score endpoints and it does not
select mu_load from observed rotation residuals.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_b2_split_q_source_load_theory_gate_not_endpoint"


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

    freeze = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_formula_freeze_manifest.csv"
    ).iloc[0]
    role_summary = pd.read_csv(DATA / "ngc7331_b2_q_role_separation_summary.csv").iloc[0]
    q_review = pd.read_csv(
        DATA / "ngc7331_qwarp_source_only_review_response_summary.csv"
    ).iloc[0]
    mom1 = pd.read_csv(DATA / "ngc7331_things_mom1_sign_cross_summary.csv").iloc[0]
    vertical = pd.read_csv(
        DATA / "ngc7331_outer_warp_vertical_caveat_summary.csv"
    ).iloc[0]

    x_w = float(freeze["x_w_formula_freeze"])
    vflat = float(freeze["vflat_km_s"])
    source_scale = x_w * vflat**2
    q_shape_min = float(freeze["q_warp_min"])
    q_shape_max = float(freeze["q_warp_max"])
    epsilon_cross_bound = float(freeze["epsilon_cross_bound"])
    vertical_activation = float(vertical["vertical_activation_candidate"])

    formulas = pd.DataFrame(
        [
            {
                "branch_id": "B2_ORIGINAL_IDENTIFIED_Q",
                "formula_text": (
                    "Delta v^2 = sigma_warp q_shape x_w Vflat^2 "
                    "* q_shape ramp(x;x_w)"
                ),
                "effective_q_power": 2,
                "kernel_text": "K_shape = q_shape ramp",
                "source_load_text": "mu_load identified with q_shape",
                "ngc4088_limit": "recovers original protocol when q_shape=1",
                "ngc7331_status": "DIAGNOSTICALLY_REJECTED_FOR_TRANSFER",
                "theory_status": "FORMULA_CONDITIONAL_Q_ROLE_CONFLATED",
            },
            {
                "branch_id": "B2_SPLIT_UNIT_KERNEL_LOAD",
                "formula_text": (
                    "Delta v^2 = sigma_warp mu_load x_w Vflat^2 "
                    "* ramp(x;x_w)"
                ),
                "effective_q_power": 0,
                "kernel_text": "K_shape = ramp; q_shape carried as morphology evidence",
                "source_load_text": "mu_load independent Tau-side source-load handle",
                "ngc4088_limit": "recovers original protocol when q_shape=1 and mu_load=1",
                "ngc7331_status": "BEST_DIAGNOSTIC_SHAPE_REPAIR_NOT_ENDPOINT",
                "theory_status": "PREFERRED_NEXT_THEORY_BRANCH_MU_LOAD_OPEN",
            },
            {
                "branch_id": "B2_SPLIT_Q_KERNEL_LOAD",
                "formula_text": (
                    "Delta v^2 = sigma_warp mu_load x_w Vflat^2 "
                    "* q_shape ramp(x;x_w)"
                ),
                "effective_q_power": 1,
                "kernel_text": "K_shape = q_shape ramp",
                "source_load_text": "mu_load independent Tau-side source-load handle",
                "ngc4088_limit": "recovers original protocol when q_shape=1 and mu_load=1",
                "ngc7331_status": "POSSIBLE_BUT_REQUIRES_LARGE_MU_LOAD",
                "theory_status": "SECONDARY_BRANCH_MU_LOAD_AND_Q_KERNEL_ROLE_OPEN",
            },
        ]
    )
    formulas["galaxy"] = GALAXY
    formulas["dimension_check"] = (
        "PASS: x_w, q_shape, mu_load, sigma_warp, and ramp are dimensionless; "
        "Vflat^2 supplies km^2/s^2"
    )
    formulas["inactive_window_limit"] = "PASS: ramp=0 for x<=x_w"
    formulas["zero_source_limit"] = (
        "PASS if sigma_warp=0 or mu_load=0; original branch also zeroes if q_shape=0"
    )
    formulas["uses_vobs_or_residual_in_construction"] = False
    formulas["endpoint_scores_allowed"] = False
    formulas["claim_boundary"] = CLAIM_BOUNDARY

    source_candidates = pd.DataFrame(
        [
            {
                "candidate_id": "MU0_UNIT_ASYMPTOTIC_LOAD",
                "mu_load_rule": "mu_load = 1",
                "source_basis": (
                    "minimal source-load normalization after separating q_shape; "
                    "uses x_w Vflat^2 as carrier scale"
                ),
                "available_value": 1.0,
                "residual_blind": True,
                "freeze_status": "CANDIDATE_RULE_READY_NOT_LAW_DERIVED",
                "remaining_obligation": (
                    "derive why the split source-load coefficient is unity from "
                    "Tau-side closure/readout structure"
                ),
            },
            {
                "candidate_id": "MU_VERTICAL_OVERLAY_CONTEXT",
                "mu_load_rule": "mu_load = f(vertical_activation, projection_context)",
                "source_basis": (
                    "existing NGC7331 vertical/outer-warp caveat layer; "
                    f"vertical_activation_candidate={vertical_activation:.6g}"
                ),
                "available_value": vertical_activation,
                "residual_blind": True,
                "freeze_status": "CONTEXT_AVAILABLE_FUNCTION_NOT_DERIVED",
                "remaining_obligation": (
                    "derive the mapping from vertical/projection evidence to mu_load"
                ),
            },
            {
                "candidate_id": "MU_CROSS_CONTEXT_BOUND",
                "mu_load_rule": "mu_load interval widened by epsilon_cross",
                "source_basis": (
                    "MOM1 sign/cross review carries conservative bound "
                    f"epsilon_cross={epsilon_cross_bound:.6g}"
                ),
                "available_value": epsilon_cross_bound,
                "residual_blind": True,
                "freeze_status": "BOUND_AVAILABLE_NOT_PRIMARY_LOAD_RULE",
                "remaining_obligation": (
                    "keep as uncertainty/cross-term bound, not as primary source-load fit"
                ),
            },
            {
                "candidate_id": "MU_HI_SUPPORT_OR_HISTORY_COHERENCE",
                "mu_load_rule": "mu_load = F(HI support, warp coherence, history memory)",
                "source_basis": (
                    "scientifically motivated by bridge, but no accepted numeric "
                    "NGC7331 source observable is frozen yet"
                ),
                "available_value": pd.NA,
                "residual_blind": True,
                "freeze_status": "SOURCE_OBSERVABLE_MISSING",
                "remaining_obligation": (
                    "define and extract residual-blind support/coherence/history observable"
                ),
            },
        ]
    )
    source_candidates["galaxy"] = GALAXY
    source_candidates["endpoint_scores_allowed"] = False
    source_candidates["uses_vobs_or_residual"] = False
    source_candidates["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "B2S1_FAILURE_LOCALIZED",
                "gate_status": "PASS",
                "evidence": str(role_summary["audit_status"]),
                "remaining_obligation": "none for failure localization",
            },
            {
                "gate_id": "B2S2_Q_SHAPE_SOURCE_AVAILABLE",
                "gate_status": "PASS_INTERVAL",
                "evidence": str(q_review["q_warp_interval"]),
                "remaining_obligation": (
                    "rename/use as q_shape; do not identify with mu_load by default"
                ),
            },
            {
                "gate_id": "B2S3_DIMENSIONS_LIMITS",
                "gate_status": "PASS",
                "evidence": "split formulas are dimensionally valid and recover inactive window",
                "remaining_obligation": "none at dimensional/protocol level",
            },
            {
                "gate_id": "B2S4_MU_LOAD_SOURCE_ORIGIN",
                "gate_status": "OPEN",
                "evidence": "unit, vertical, cross, and HI/history candidates listed",
                "remaining_obligation": (
                    "derive or source-freeze mu_load before any endpoint freeze"
                ),
            },
            {
                "gate_id": "B2S5_SIGN_CONTEXT",
                "gate_status": "CARRIED_CAVEATED",
                "evidence": str(mom1["mom1_sign_cross_status"]),
                "remaining_obligation": "freeze sign convention independently if point branch is built",
            },
            {
                "gate_id": "B2S6_ENDPOINT_ELIGIBILITY",
                "gate_status": "BLOCKED",
                "evidence": "post-failure diagnostic only",
                "remaining_obligation": (
                    "new formula branch must be predeclared and frozen before scoring"
                ),
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "split_gate_status": "NGC7331_B2_SPLIT_Q_SOURCE_LOAD_THEORY_GATE_BUILT_ENDPOINT_BLOCKED",
                "recommended_next_branch": "B2_SPLIT_UNIT_KERNEL_LOAD",
                "source_scale_xw_vflat2_km2_s2": source_scale,
                "q_shape_interval": f"[{q_shape_min}, {q_shape_max}]",
                "mu_load_status": "OPEN_NOT_TAU_SIDE_DERIVED",
                "n_formula_branches": len(formulas),
                "n_mu_load_candidates": len(source_candidates),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].isin(["PASS", "PASS_INTERVAL", "CARRIED_CAVEATED"]).sum()),
                "n_open": int(gates["gate_status"].eq("OPEN").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_status": (
                    "theory reformulation only; q_shape/mu_load split required before "
                    "any future NGC7331 B2 point branch"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    formulas.to_csv(DATA / "ngc7331_b2_split_q_source_load_formulas.csv", index=False)
    source_candidates.to_csv(
        DATA / "ngc7331_b2_split_q_source_load_mu_candidates.csv", index=False
    )
    gates.to_csv(DATA / "ngc7331_b2_split_q_source_load_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_b2_split_q_source_load_summary.csv", index=False)

    report = [
        "# NGC7331 B2 split q/source-load theory gate",
        "",
        "This gate is built after the NGC7331 exact B2 interval-control failure",
        "and the q-role diagnostic. It does not score an endpoint. It rewrites",
        "the B2 shell so `q_shape` and `mu_load` are no longer identified by",
        "default.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Formula branches",
        "",
        markdown_table(formulas),
        "",
        "## Residual-blind mu_load candidates",
        "",
        markdown_table(source_candidates),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Verdict",
        "",
        "The current exact-transfer failure is best treated as a source-load",
        "role-confusion failure, not as proof that the B2 radial ramp is useless.",
        "The next admissible path is to derive or source-freeze an independent",
        "`mu_load` before scoring. The most economical theory branch is",
        "`B2_SPLIT_UNIT_KERNEL_LOAD`, but it remains blocked until `mu_load=1`",
        "or another source-load rule is derived from Tau-side closure/readout",
        "structure rather than endpoint residuals.",
        "",
    ]
    (REPORTS / "ngc7331_b2_split_q_source_load_theory_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
