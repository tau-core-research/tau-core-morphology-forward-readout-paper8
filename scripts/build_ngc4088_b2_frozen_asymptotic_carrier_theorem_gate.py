#!/usr/bin/env python3
"""Build the NGC4088 B2 frozen asymptotic-carrier theorem gate.

This gate works from the accepted formula-freeze manifest, not from the older
first-pass scale audit.  It records the conditional theorem under which
`Vflat^2` is the correct asymptotic carrier for the frozen warp/history source
load, while preserving that a final Tau-side proof remains open.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "ngc4088_b2_frozen_asymptotic_carrier_theorem_gate_not_endpoint"


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

    freeze = pd.read_csv(DATA / "ngc4088_warp_history_formula_freeze_manifest.csv").iloc[0]
    source_origin = pd.read_csv(DATA / "ngc4088_b2_source_load_origin_summary.csv").iloc[0]

    vflat = float(freeze["vflat_km_s"])
    vflat2 = vflat**2
    x_w = float(freeze["x_w_formula_freeze"])
    lambda_w = float(freeze["lambda_w_km2_s2"])
    reconstructed = float(freeze["sigma_warp"]) * float(freeze["q_warp"]) * x_w * vflat2
    alignment_pass = abs(reconstructed - lambda_w) < 1.0e-6

    theorem = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "theorem_id": "FROZEN_MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_THEOREM",
                "conditional_statement": (
                    "For a frozen warp/history source-load whose dimensionful "
                    "normalizer must be residual-blind, source-native, asymptotic, "
                    "non-comparator, and minimally factorized with the onset x_w, "
                    "the manifest carrier is Vflat^2 and the source load is "
                    "Lambda_tau = sigma_warp q_warp x_w Vflat^2."
                ),
                "carrier": "Vflat^2",
                "carrier_value_km2_s2": vflat2,
                "lambda_tau_km2_s2": reconstructed,
                "formula_freeze_lambda_w_km2_s2": lambda_w,
                "formula_freeze_alignment_pass": alignment_pass,
                "theorem_status": "CONDITIONAL_CARRIER_THEOREM_FOR_FROZEN_PROTOCOL",
                "law_status": "FINAL_TAU_SIDE_CARRIER_PROOF_OPEN",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    criteria = pd.DataFrame(
        [
            {
                "criterion_id": "FC1_RESIDUAL_BLIND",
                "criterion_status": "PASS",
                "evidence": "Vflat is a source/catalog value; no vobs residual or endpoint score is used",
                "law_obligation": "none at residual-blindness level",
            },
            {
                "criterion_id": "FC2_SOURCE_NATIVE_ASYMPTOTIC",
                "criterion_status": "PASS",
                "evidence": "Vflat is the manifest's source/catalog flat-speed asymptotic carrier",
                "law_obligation": "derive why the outer readout carrier must be the flat-speed carrier",
            },
            {
                "criterion_id": "FC3_SOURCE_ONSET_COUPLED",
                "criterion_status": "PASS",
                "evidence": "carrier enters only through x_w Vflat^2 in the frozen source-load",
                "law_obligation": "none at frozen source-load bookkeeping level",
            },
            {
                "criterion_id": "FC4_NO_EXTERNAL_COMPARATOR",
                "criterion_status": "PASS",
                "evidence": "the frozen manifest does not use TPG/v6, MOND, RAR, or Newtonian residual comparators as normalizers",
                "law_obligation": "derive comparator autonomy from Tau-side readout architecture",
            },
            {
                "criterion_id": "FC5_MINIMAL_FACTORIZATION",
                "criterion_status": "PASS",
                "evidence": "source-load uses one onset factor and one asymptotic carrier, not extra closure-fraction composites",
                "law_obligation": "derive minimal factorization or carry it as a protocol premise",
            },
            {
                "criterion_id": "FC6_FREEZE_ALIGNMENT",
                "criterion_status": "PASS" if alignment_pass else "BLOCKED",
                "evidence": "sigma*q*x_w*Vflat^2 reproduces the frozen lambda_w",
                "law_obligation": "none at arithmetic freeze-alignment level",
            },
            {
                "criterion_id": "FC7_ALTERNATIVE_CARRIER_EXCLUSION",
                "criterion_status": "CONDITIONAL",
                "evidence": "older first-pass audit rejects point medians and external comparators under the same selection logic",
                "law_obligation": "repeat alternative enumeration on the frozen manifest protocol or a predeclared sample",
            },
            {
                "criterion_id": "FC8_POPULATION_TRANSFER",
                "criterion_status": "OPEN_FOR_CLAIMS",
                "evidence": "single-galaxy frozen carrier theorem only",
                "law_obligation": "apply to a predeclared source-rich warp/history sample",
            },
        ]
    )
    criteria["galaxy"] = GALAXY
    criteria["endpoint_scores_allowed"] = False
    criteria["uses_vobs_or_residual"] = False
    criteria["claim_boundary"] = CLAIM_BOUNDARY
    criteria = criteria[
        [
            "galaxy",
            "criterion_id",
            "criterion_status",
            "evidence",
            "law_obligation",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    pass_like = {"PASS"}
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "frozen_carrier_theorem_status": (
                    "FROZEN_VFLAT2_CARRIER_CONDITIONAL_THEOREM_LAW_PROOF_OPEN"
                ),
                "carrier_value_km2_s2": vflat2,
                "lambda_tau_km2_s2": reconstructed,
                "formula_freeze_alignment_pass": alignment_pass,
                "source_load_origin_status": str(source_origin["source_load_origin_status"]),
                "n_criteria": len(criteria),
                "n_pass": int(criteria["criterion_status"].isin(pass_like).sum()),
                "n_conditional": int(criteria["criterion_status"].eq("CONDITIONAL").sum()),
                "n_open_for_claims": int(criteria["criterion_status"].eq("OPEN_FOR_CLAIMS").sum()),
                "law_level_closed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "derive comparator autonomy and minimal asymptotic carrier dominance "
                    "on a predeclared warp/history population"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    theorem.to_csv(DATA / "ngc4088_b2_frozen_asymptotic_carrier_theorem.csv", index=False)
    criteria.to_csv(DATA / "ngc4088_b2_frozen_asymptotic_carrier_criteria.csv", index=False)
    summary.to_csv(DATA / "ngc4088_b2_frozen_asymptotic_carrier_summary.csv", index=False)

    report = [
        "# NGC4088 B2 Frozen Asymptotic-Carrier Theorem Gate",
        "",
        "This gate records the conditional carrier theorem for the accepted",
        "formula-freeze manifest. It does not use endpoint velocities, residuals,",
        "or score ranks.",
        "",
        "## Conditional Theorem",
        "",
        markdown_table(theorem),
        "",
        "## Criteria",
        "",
        markdown_table(criteria),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        "`Vflat^2` is conditionally justified as the frozen protocol carrier under",
        "the minimal residual-blind source-onset asymptotic-carrier rule. This",
        "sharpens the B2 carrier premise, but it is not yet a final Tau-side law:",
        "alternative-carrier exclusion, comparator autonomy, and population",
        "transfer remain open.",
        "",
    ]
    (REPORTS / "ngc4088_b2_frozen_asymptotic_carrier_theorem_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
