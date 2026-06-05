#!/usr/bin/env python3
"""Build a consolidated four-case endpoint status summary.

The summary deliberately keeps the evidence categories separate: three rows
come from the mixed-readout population/control packet, while NGC4088 is an
additional caveated single-galaxy accepted endpoint. NGC5907 and caveated
NGC7331 may also be promoted as single-galaxy mixed endpoint rows inside the
three-case packet when their endpoint-freeze gates exist.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


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

    mixed_scores = pd.read_csv(DATA / "mixed_readout_population_endpoint_scores.csv")
    mixed_control = pd.read_csv(DATA / "mixed_readout_population_control_by_galaxy.csv")
    ngc5907_accepted_summary_path = (
        DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_summary.csv"
    )
    ngc5907_accepted = (
        pd.read_csv(ngc5907_accepted_summary_path).iloc[0]
        if ngc5907_accepted_summary_path.exists()
        else None
    )
    ngc4013_blocker_path = (
        DATA / "ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_summary.csv"
    )
    ngc4013_blocker = (
        pd.read_csv(ngc4013_blocker_path).iloc[0]
        if ngc4013_blocker_path.exists()
        else None
    )
    ngc7331_accepted_summary_path = (
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_summary.csv"
    )
    ngc7331_accepted = (
        pd.read_csv(ngc7331_accepted_summary_path).iloc[0]
        if ngc7331_accepted_summary_path.exists()
        else None
    )
    ngc4088_summary = pd.read_csv(
        DATA / "ngc4088_warp_history_accepted_endpoint_summary.csv"
    ).iloc[0]
    ngc4088_scores = pd.read_csv(DATA / "ngc4088_warp_history_accepted_endpoint_scores.csv")

    rows: list[dict[str, object]] = []
    for _, row in mixed_scores.sort_values("galaxy").iterrows():
        control = mixed_control.loc[mixed_control["galaxy"].eq(row["galaxy"])].iloc[0]
        best_baseline = min(
            float(row["rmse_newton"]),
            float(row["rmse_tpg_v6"]),
            float(row["rmse_mond"]),
            float(row["rmse_exponential_disk_carrier"]),
        )
        endpoint_status = row["mixed_case_status"]
        evidence_packet = "three_case_mixed_readout_control"
        matched_rmse = float(row["rmse_mixed_population"])
        wrong_mean = float(control["wrong_mean_rmse"])
        wrong_best = float(control["wrong_best_rmse"])
        beats_best_baseline = matched_rmse < best_baseline
        beats_all_wrong = bool(control["matched_beats_all_wrong_labels"])
        claim_boundary = "small_N_mixed_control_not_population_validation"
        case_caveat = row["mixed_case_caveat"]
        if row["galaxy"] == "NGC4013" and ngc4013_blocker is not None:
            endpoint_status = ngc4013_blocker["blocker_status"]
            claim_boundary = "retrospective_frozen_reference_not_accepted_endpoint"
            case_caveat = (
                "mixed accepted endpoint blocked: protocol ready but retroactive; "
                "predeclared replay/holdout required"
            )
        if row["galaxy"] == "NGC5907" and ngc5907_accepted is not None:
            endpoint_status = ngc5907_accepted["endpoint_status"]
            evidence_packet = "accepted_mixed_single_galaxy_endpoint_inside_three_case_packet"
            matched_rmse = float(ngc5907_accepted["rmse_mixed_accepted"])
            best_baseline = float(ngc5907_accepted["best_baseline_rmse_km_s"])
            wrong_mean = float(ngc5907_accepted["wrong_mixed_mean_rmse_km_s"])
            wrong_best = float(ngc5907_accepted["wrong_mixed_best_rmse_km_s"])
            beats_best_baseline = bool(ngc5907_accepted["matched_beats_all_baselines"])
            beats_all_wrong = bool(ngc5907_accepted["matched_beats_all_wrong_mixed_families"])
            claim_boundary = "accepted_single_galaxy_mixed_control_not_population_validation"
            case_caveat = "prior projection endpoint not used as mixed-readout evidence"
        if row["galaxy"] == "NGC7331" and ngc7331_accepted is not None:
            endpoint_status = ngc7331_accepted["endpoint_status"]
            evidence_packet = (
                "caveated_accepted_mixed_single_galaxy_endpoint_inside_three_case_packet"
            )
            matched_rmse = float(ngc7331_accepted["rmse_mixed_accepted"])
            best_baseline = float(ngc7331_accepted["best_baseline_rmse_km_s"])
            wrong_mean = float(ngc7331_accepted["wrong_mixed_mean_rmse_km_s"])
            wrong_best = float(ngc7331_accepted["wrong_mixed_best_rmse_km_s"])
            beats_best_baseline = bool(ngc7331_accepted["matched_beats_all_baselines"])
            beats_all_wrong = bool(ngc7331_accepted["matched_beats_all_wrong_mixed_families"])
            claim_boundary = (
                "caveated_accepted_single_galaxy_mixed_control_not_population_validation"
            )
            case_caveat = (
                "broad outer window retained; numeric outer-warp onset unavailable"
            )
        rows.append(
            {
                "galaxy": row["galaxy"],
                "evidence_packet": evidence_packet,
                "endpoint_status": endpoint_status,
                "matched_formula_id": row["mixed_formula_id"],
                "matched_rmse_km_s": matched_rmse,
                "best_baseline_rmse_km_s": best_baseline,
                "wrong_family_mean_rmse_km_s": wrong_mean,
                "best_wrong_family_rmse_km_s": wrong_best,
                "matched_beats_best_baseline": beats_best_baseline,
                "matched_beats_all_wrong_families": beats_all_wrong,
                "claim_boundary": claim_boundary,
                "case_caveat": case_caveat,
            }
        )

    ngc4088_matched = ngc4088_scores.loc[
        ngc4088_scores["model_id"].eq("TAU_NGC4088_WARP_HISTORY_ACCEPTED")
    ].iloc[0]
    rows.append(
        {
            "galaxy": "NGC4088",
            "evidence_packet": "additional_caveated_single_galaxy_endpoint",
            "endpoint_status": ngc4088_summary["endpoint_status"],
            "matched_formula_id": ngc4088_summary["formula_id"],
            "matched_rmse_km_s": float(ngc4088_matched["rmse_km_s"]),
            "best_baseline_rmse_km_s": float(ngc4088_summary["best_baseline_rmse_km_s"]),
            "wrong_family_mean_rmse_km_s": float(
                ngc4088_summary["wrong_family_mean_rmse_km_s"]
            ),
            "best_wrong_family_rmse_km_s": float(ngc4088_summary["wrong_family_best_rmse_km_s"]),
            "matched_beats_best_baseline": bool(ngc4088_summary["matched_beats_all_baselines"]),
            "matched_beats_all_wrong_families": bool(
                ngc4088_summary["matched_beats_all_wrong_families"]
            ),
            "claim_boundary": "caveated_single_galaxy_endpoint_not_population_validation",
            "case_caveat": "B1 graphical-overview provenance plus B2/B3 law-level open",
        }
    )

    cases = pd.DataFrame(rows)
    summary = pd.DataFrame(
        [
            {
                "summary_status": "FOUR_INSPECTED_CASES_HETEROGENEOUS_PRELIMINARY_EVIDENCE",
                "n_inspected_cases": len(cases),
                "n_three_case_mixed_packet": int(
                    cases["evidence_packet"].str.contains("three_case|inside_three_case").sum()
                ),
                "n_additional_caveated_endpoint": int(
                    cases["evidence_packet"].eq(
                        "additional_caveated_single_galaxy_endpoint"
                    ).sum()
                ),
                "n_accepted_single_galaxy_endpoints": int(
                    (
                        cases["endpoint_status"].str.contains("ACCEPTED")
                        & ~cases["endpoint_status"].str.contains("BLOCKED")
                    ).sum()
                ),
                "n_matched_beats_best_baseline": int(
                    cases["matched_beats_best_baseline"].sum()
                ),
                "n_matched_beats_all_wrong_families": int(
                    cases["matched_beats_all_wrong_families"].sum()
                ),
                "mean_matched_rmse_km_s": float(cases["matched_rmse_km_s"].mean()),
                "claim_boundary": (
                    "four inspected cases, not a uniform population validation; "
                    "three-case mixed control with NGC5907 and caveated NGC7331 "
                    "accepted-mixed promotions plus one additional caveated accepted endpoint"
                ),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
            }
        ]
    )

    cases.to_csv(DATA / "four_case_endpoint_status_cases.csv", index=False)
    summary.to_csv(DATA / "four_case_endpoint_status_summary.csv", index=False)

    report = f"""# Four inspected endpoint cases status

Status: `{summary.iloc[0]['summary_status']}`

This report consolidates the four already inspected galaxies without turning
them into a uniform population-validation claim. Three cases belong to the
mixed-readout population/control packet; NGC5907 and caveated NGC7331 are
additionally promoted to mixed single-galaxy endpoint rows inside that packet,
while NGC4088 is an additional caveated warp/history accepted endpoint.

{markdown_table(cases)}

## Summary

{markdown_table(summary)}

Interpretation: the current package contains four inspected cases in which the
source- or morphology-matched Tau Core readout beats the best local baseline
and the inspected wrong-family controls. This is encouraging small-N evidence
for readout specificity, but it is not yet population validation because the
evidence packets are heterogeneous: NGC4013 remains retrospective, NGC7331 is
accepted only with a broad-window caveat, and NGC4088 carries explicit B1/B2/B3
caveats.
"""
    (REPORTS / "four_case_endpoint_status_summary.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
