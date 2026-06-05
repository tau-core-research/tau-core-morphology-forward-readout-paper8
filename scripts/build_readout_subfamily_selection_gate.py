#!/usr/bin/env python3
"""Build the Tau Core readout-subfamily selection gate.

The gate records why coarse 4D morphology families are not enough and lists
the residual-blind source observables required before a subfamily can be used
as an accepted forward-readout input.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "readout_subfamily_selection_gate_not_endpoint"


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


def build_registry() -> pd.DataFrame:
    rows = [
        {
            "parent_family": "K_thick_flared",
            "subfamily": "K_thick_regular",
            "readout_interpretation": "smooth vertically extended disk without strong warp/history coupling",
            "required_residual_blind_observables": "vertical scale height or edge-on thickness; low warp/asymmetry evidence; projection-safe inclination",
            "candidate_formula_layer": "thick/flared damped vertical kernel",
            "current_status": "candidate_subfamily_pending_source_rule",
        },
        {
            "parent_family": "K_thick_flared",
            "subfamily": "K_flared_outer_disk",
            "readout_interpretation": "outer disk flaring modulates vertical readout in the outskirts",
            "required_residual_blind_observables": "outer thickness/flare gradient; HI extent; projection caveat audit",
            "candidate_formula_layer": "radially varying thick/flared kernel",
            "current_status": "candidate_subfamily_pending_source_rule",
        },
        {
            "parent_family": "K_thick_flared",
            "subfamily": "K_warp_history_coupled",
            "readout_interpretation": "warp/history/background morphology layer cross-couples into the 4D readout",
            "required_residual_blind_observables": "warp onset; warp asymmetry; HI disturbance; interaction/memory evidence; epsilon_cross source bound",
            "candidate_formula_layer": "warp p1/p2 branch plus bounded epsilon_cross modulation",
            "current_status": "motivated_by_NGC4088_targeted_diagnostic_not_accepted_endpoint",
        },
        {
            "parent_family": "K_thick_flared",
            "subfamily": "K_projection_dominated",
            "readout_interpretation": "apparent thickness/flare is dominated by viewing/projection uncertainty",
            "required_residual_blind_observables": "edge-on geometry; inclination uncertainty; dust lane/projection flags; velocity-field sanity check",
            "candidate_formula_layer": "projection-corrected or endpoint-blocked thick/flared shell",
            "current_status": "control_or_blocker_subfamily",
        },
        {
            "parent_family": "K_scale_tail_spiral",
            "subfamily": "K_smooth_n2_tail",
            "readout_interpretation": "smooth source-tail branch with n=2 TGP-like asymptotic form",
            "required_residual_blind_observables": "HI radius; outer-disk/tail transition; stable tail support",
            "candidate_formula_layer": "n=2 scale-tail readout",
            "current_status": "candidate_subfamily_pending_source_rule",
        },
        {
            "parent_family": "K_scale_tail_spiral",
            "subfamily": "K_disturbed_outer_tail",
            "readout_interpretation": "asymmetric or environmentally disturbed outer tail",
            "required_residual_blind_observables": "HI asymmetry; outer lopsidedness; environment/interaction evidence",
            "candidate_formula_layer": "tail plus memory/asymmetry modulation",
            "current_status": "candidate_subfamily_pending_source_rule",
        },
        {
            "parent_family": "K_exponential_disk",
            "subfamily": "K_clean_expdisk",
            "readout_interpretation": "present-day exponential disk is a close proxy for readout-relevant morphology",
            "required_residual_blind_observables": "S4G/SPARC scale radius; no strong bar/ring/projection caveat; stable disk component",
            "candidate_formula_layer": "Freeman/Bessel exponential-disk shell",
            "current_status": "candidate_subfamily_pending_source_rule",
        },
        {
            "parent_family": "K_exponential_disk",
            "subfamily": "K_expdisk_overlay",
            "readout_interpretation": "exponential disk with bar, compact core, projection, or memory/history overlay",
            "required_residual_blind_observables": "bar/core/projection/history flags; overlay source support",
            "candidate_formula_layer": "exponential shell plus overlay component",
            "current_status": "candidate_subfamily_pending_source_rule",
        },
        {
            "parent_family": "K_compact_finite",
            "subfamily": "K_true_compact",
            "readout_interpretation": "compact finite source dominates the readout support",
            "required_residual_blind_observables": "bulge/core support; compact scale; limited extended disk influence",
            "candidate_formula_layer": "compact finite-source exterior response",
            "current_status": "candidate_subfamily_pending_source_rule",
        },
        {
            "parent_family": "K_compact_finite",
            "subfamily": "K_compact_plus_disk",
            "readout_interpretation": "compact core exists but extended disk/tail still controls part of readout",
            "required_residual_blind_observables": "bulge-to-disk decomposition; disk scale; compact support radius",
            "candidate_formula_layer": "compact shell plus disk/tail overlay",
            "current_status": "candidate_subfamily_pending_source_rule",
        },
    ]
    df = pd.DataFrame(rows)
    df["endpoint_scores_allowed"] = False
    df["claim_boundary"] = CLAIM_BOUNDARY
    return df


def build_ngc4088_case() -> pd.DataFrame:
    generic_path = DATA / "multigalaxy_fit_inspection_summary.csv"
    targeted_path = DATA / "s4g75_ngc4088_endpoint_fit_diagnostic_summary.csv"
    if not generic_path.exists() or not targeted_path.exists():
        return pd.DataFrame(
            [
                {
                    "galaxy": "NGC4088",
                    "case_status": "BLOCKED_INPUT_DIAGNOSTICS_MISSING",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        )
    generic = pd.read_csv(generic_path)
    targeted = pd.read_csv(targeted_path).iloc[0]
    row = generic[generic["galaxy"] == "NGC4088"].iloc[0]
    return pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "coarse_parent_family": row["formula_family"],
                "motivated_subfamily": "K_warp_history_coupled",
                "generic_tau_matched_rmse_kms": float(row["rmse_tau_matched"]),
                "best_generic_baseline_model": row["best_baseline_model"],
                "best_generic_baseline_rmse_kms": float(row["rmse_best_baseline"]),
                "targeted_warp_fixed_tau_rmse_kms": float(targeted["best_fixed_tau_rmse_kms"]),
                "targeted_warp_bounded_tau_rmse_kms": float(targeted["best_bounded_tau_rmse_kms"]),
                "diagnostic_delta_generic_minus_targeted_bounded_kms": float(
                    row["rmse_tau_matched"] - targeted["best_bounded_tau_rmse_kms"]
                ),
                "interpretation": "coarse_family_insufficient_correct_subfamily_matters",
                "endpoint_scores_allowed": False,
                "validation_claim_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def build_gate(case: pd.DataFrame) -> pd.DataFrame:
    has_ngc4088 = (
        not case.empty
        and "diagnostic_delta_generic_minus_targeted_bounded_kms" in case.columns
    )
    delta = (
        float(case["diagnostic_delta_generic_minus_targeted_bounded_kms"].iloc[0])
        if has_ngc4088
        else float("nan")
    )
    rows = [
        {
            "gate_id": "RSF1_COARSE_FAMILY_NOT_FINAL_READOUT",
            "gate_status": "PASS",
            "evidence": "K_obs and K_readout are already separated; 4D projected morphology is not automatically the Tau-side readout class",
            "remaining_obligation": "keep parent-family labels as handles, not final physical taxonomy",
        },
        {
            "gate_id": "RSF2_SUBFAMILY_MOTIVATED_BY_STRESS_CASE",
            "gate_status": "PASS" if has_ngc4088 and delta > 0 else "BLOCKED",
            "evidence": (
                f"NGC4088 generic family RMSE exceeds targeted warp bounded RMSE by {delta:.6g} km/s"
                if has_ngc4088
                else "NGC4088 diagnostic inputs missing"
            ),
            "remaining_obligation": "repeat on multiple warp/history-rich galaxies",
        },
        {
            "gate_id": "RSF3_RESIDUAL_BLIND_SUBFAMILY_OBSERVABLES",
            "gate_status": "PENDING",
            "evidence": "registry lists required source observables for each subfamily",
            "remaining_obligation": "fill accepted residual-blind subfamily observables before endpoint use",
        },
        {
            "gate_id": "RSF4_NO_ENDPOINT_SUBFAMILY_SELECTION",
            "gate_status": "PASS",
            "evidence": "best Tau family/subfamily rows remain diagnostic-only and are not promoted to accepted labels",
            "remaining_obligation": "freeze subfamily selection rule before future endpoint scoring",
        },
    ]
    df = pd.DataFrame(rows)
    df["endpoint_scores_allowed"] = False
    df["claim_boundary"] = CLAIM_BOUNDARY
    return df


def write_report(registry: pd.DataFrame, case: pd.DataFrame, gate: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Readout-Subfamily Selection Gate",
        "",
        "This gate records the next refinement implied by the multi-galaxy atlas:",
        "coarse projected 4D morphology families are useful handles, but they are",
        "not always the final Tau Core readout classes. A galaxy may require a",
        "readout-relevant subfamily selected by residual-blind source observables.",
        "",
        "## Gate Status",
        "",
        markdown_table(gate),
        "",
        "## NGC4088 Stress Case",
        "",
        markdown_table(case),
        "",
        "## Subfamily Registry",
        "",
        markdown_table(registry),
        "",
        "## Claim Boundary",
        "",
        "This is a protocol and taxonomy refinement, not an endpoint score. The",
        "NGC4088 comparison motivates the subfamily layer because the generic",
        "thick/flared family is weak while the targeted warp/history branch is",
        "strong. The subfamily cannot be accepted until selected by residual-blind",
        "observables and repeated on a larger matched set.",
        "",
    ]
    (REPORTS / "readout_subfamily_selection_gate.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    registry = build_registry()
    case = build_ngc4088_case()
    gate = build_gate(case)
    registry.to_csv(DATA / "readout_subfamily_registry.csv", index=False)
    case.to_csv(DATA / "readout_subfamily_ngc4088_case.csv", index=False)
    gate.to_csv(DATA / "readout_subfamily_selection_gate.csv", index=False)
    write_report(registry, case, gate)
    print(gate.to_string(index=False))
    print(case.to_string(index=False))


if __name__ == "__main__":
    main()
