#!/usr/bin/env python3
"""Build the NGC4088 B2 population-transfer preflight gate.

This gate asks whether the frozen NGC4088 source-load/carrier theorem can be
treated as a population result.  It deliberately does not score curves.  It
separates the exact warp/history source-load protocol from looser mixed
overlay/projection analogues already present in Paper 8.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_b2_population_transfer_preflight_gate_not_endpoint"


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


def read_first(path: str) -> pd.Series:
    table_path = DATA / path
    if not table_path.exists():
        raise FileNotFoundError(table_path)
    table = pd.read_csv(table_path)
    if table.empty:
        raise ValueError(f"{table_path} is empty")
    return table.iloc[0]


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    frozen_carrier = read_first("ngc4088_b2_frozen_asymptotic_carrier_summary.csv")
    n4013 = read_first("ngc4013_expdisk_wvo_formula_freeze_summary.csv")
    n5907 = read_first("ngc5907_expdisk_projection_mixed_formula_freeze_summary.csv")
    n7331 = read_first("ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_summary.csv")
    mixed_population = pd.read_csv(DATA / "mixed_readout_population_validation_cases.csv")
    blocked_controls = mixed_population[
        mixed_population["population_validation_use"].eq("negative_or_acquisition_control")
    ].copy()

    cases = [
        {
            "galaxy": "NGC4088",
            "case_role": "reference_exact_protocol",
            "candidate_protocol": "K_warp_history_caveated_protocol",
            "source_protocol_status": str(
                frozen_carrier["frozen_carrier_theorem_status"]
            ),
            "exact_b2_source_load_protocol": True,
            "same_carrier_rule_available": True,
            "formula_frozen_before_scoring": True,
            "uses_endpoint_scores_or_residual": False,
            "population_transfer_status": "REFERENCE_SINGLE_GALAXY_CONDITIONAL_THEOREM",
            "remaining_obligation": (
                "repeat exact source-load/carrier gate on independent warp/history "
                "galaxies before population claims"
            ),
        },
        {
            "galaxy": "NGC4013",
            "case_role": "prospective_mixed_overlay_analogue",
            "candidate_protocol": str(n4013["formula_id"]),
            "source_protocol_status": str(n4013["formula_freeze_status"]),
            "exact_b2_source_load_protocol": False,
            "same_carrier_rule_available": False,
            "formula_frozen_before_scoring": False,
            "uses_endpoint_scores_or_residual": False,
            "population_transfer_status": "PARTIAL_ANALOGUE_NOT_EXACT_B2_TRANSFER",
            "remaining_obligation": (
                "derive separate mixed carrier-plus-overlay carrier rule or acquire "
                "exact warp/history source-load fields"
            ),
        },
        {
            "galaxy": "NGC5907",
            "case_role": "prospective_projection_mixed_analogue",
            "candidate_protocol": str(n5907["formula_id"]),
            "source_protocol_status": str(n5907["formula_freeze_status"]),
            "exact_b2_source_load_protocol": False,
            "same_carrier_rule_available": False,
            "formula_frozen_before_scoring": boolish(
                n5907["prospective_mixed_protocol_ready"]
            ),
            "uses_endpoint_scores_or_residual": False,
            "population_transfer_status": "PARTIAL_ANALOGUE_NOT_EXACT_B2_TRANSFER",
            "remaining_obligation": (
                "projection-dominated mixed carrier is useful control evidence, not "
                "the NGC4088 warp/history source-load theorem"
            ),
        },
        {
            "galaxy": "NGC7331",
            "case_role": "caveated_outer_warp_mixed_analogue",
            "candidate_protocol": str(n7331["formula_id"]),
            "source_protocol_status": str(n7331["formula_freeze_status"]),
            "exact_b2_source_load_protocol": False,
            "same_carrier_rule_available": False,
            "formula_frozen_before_scoring": boolish(
                n7331["prospective_mixed_protocol_ready"]
            ),
            "uses_endpoint_scores_or_residual": False,
            "population_transfer_status": "CAVEATED_PARTIAL_ANALOGUE_NOT_EXACT_B2_TRANSFER",
            "remaining_obligation": (
                "broad outer-window caveat and missing numeric onset block exact "
                "B2 transfer use"
            ),
        },
    ]

    for _, row in blocked_controls.iterrows():
        cases.append(
            {
                "galaxy": str(row["galaxy"]),
                "case_role": "blocked_acquisition_control",
                "candidate_protocol": str(row["candidate_mixed_readout"]),
                "source_protocol_status": str(row["formula_freeze_status"]),
                "exact_b2_source_load_protocol": False,
                "same_carrier_rule_available": False,
                "formula_frozen_before_scoring": False,
                "uses_endpoint_scores_or_residual": False,
                "population_transfer_status": "BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING",
                "remaining_obligation": str(row["reason"]),
            }
        )

    case_table = pd.DataFrame(cases)
    case_table["endpoint_scores_allowed"] = False
    case_table["claim_boundary"] = CLAIM_BOUNDARY

    exact_transfer_ready = case_table[
        case_table["exact_b2_source_load_protocol"]
        & case_table["same_carrier_rule_available"]
        & ~case_table["case_role"].eq("reference_exact_protocol")
    ]
    partial_analogues = case_table[
        case_table["population_transfer_status"].str.contains("ANALOGUE")
    ]
    blocked = case_table[
        case_table["population_transfer_status"].str.contains("BLOCKED")
    ]

    summary = pd.DataFrame(
        [
            {
                "population_transfer_preflight_status": (
                    "POPULATION_TRANSFER_PREFLIGHT_BUILT_EXACT_TRANSFER_BLOCKED_ANALOGUE_LANE_AVAILABLE"
                ),
                "n_cases": len(case_table),
                "n_reference_exact_protocol": int(
                    case_table["case_role"].eq("reference_exact_protocol").sum()
                ),
                "n_exact_transfer_ready_excluding_reference": len(exact_transfer_ready),
                "n_partial_analogues": len(partial_analogues),
                "n_blocked_acquisition_controls": len(blocked),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "law_level_closed": False,
                "population_claim_allowed": False,
                "next_required_action": (
                    "acquire or predeclare at least two independent exact warp/history "
                    "source-load cases with x_w, q_warp, sigma_warp, Vflat, and cross-term "
                    "source observables frozen before scoring"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    case_table.to_csv(DATA / "ngc4088_b2_population_transfer_preflight_cases.csv", index=False)
    summary.to_csv(DATA / "ngc4088_b2_population_transfer_preflight_summary.csv", index=False)

    report = [
        "# NGC4088 B2 Population-Transfer Preflight Gate",
        "",
        "This gate asks whether the frozen NGC4088 B2 source-load/carrier theorem",
        "has already transferred to a population. It does not score rotations and",
        "does not use endpoint residuals.",
        "",
        "## Cases",
        "",
        markdown_table(case_table),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        "The package now has one exact reference case, NGC4088, with a frozen",
        "`Vflat^2` conditional carrier theorem. NGC4013, NGC5907, and NGC7331",
        "are useful mixed overlay/projection analogues, but they are not exact",
        "transfers of the NGC4088 warp/history source-load protocol. Therefore",
        "the population-transfer lane is explicitly built but remains blocked for",
        "claims until independent exact warp/history cases are source-frozen.",
        "",
    ]
    (REPORTS / "ngc4088_b2_population_transfer_preflight_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
