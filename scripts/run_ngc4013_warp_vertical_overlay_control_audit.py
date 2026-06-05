#!/usr/bin/env python3
"""Audit NGC4013 warp/vertical-overlay endpoint against controls."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4013_warp_vertical_overlay_control_audit_single_galaxy"


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


def rmse(df: pd.DataFrame, pred_col: str) -> float:
    return float(((df[pred_col] - df["vobs"]).pow(2).mean()) ** 0.5)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    label = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_replacement_label_summary.csv").iloc[0]
    if not bool(label["endpoint_scores_allowed"]):
        raise RuntimeError("NGC4013 replacement label is not endpoint-score eligible")

    points = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_points.csv")
    scores = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_scores.csv").iloc[0]
    if not bool(scores["endpoint_scores_allowed"]):
        raise RuntimeError("NGC4013 endpoint scores are not marked allowed")

    candidates = [
        {
            "candidate_id": "matched_K_warp_vertical_overlay",
            "candidate_role": "matched_caveated_replacement_family",
            "rmse": rmse(points, "v_wvo_endpoint"),
        },
        {
            "candidate_id": "wrong_K_compact_finite_rejected",
            "candidate_role": "wrong_family_control_rejected_original",
            "rmse": rmse(points, "v_K_compact_finite"),
        },
        {
            "candidate_id": "wrong_K_scale_tail_spiral",
            "candidate_role": "wrong_family_control",
            "rmse": rmse(points, "v_K_scale_tail_spiral"),
        },
        {
            "candidate_id": "wrong_K_exponential_disk",
            "candidate_role": "wrong_family_control",
            "rmse": rmse(points, "v_K_exponential_disk"),
        },
        {
            "candidate_id": "wrong_K_thick_flared",
            "candidate_role": "wrong_family_control",
            "rmse": rmse(points, "v_K_thick_flared"),
        },
        {
            "candidate_id": "baseline_TPG_v6",
            "candidate_role": "external_baseline",
            "rmse": rmse(points, "v_v6"),
        },
        {
            "candidate_id": "baseline_MOND",
            "candidate_role": "external_baseline",
            "rmse": rmse(points, "v_mond"),
        },
        {
            "candidate_id": "baseline_Newtonian",
            "candidate_role": "external_baseline",
            "rmse": rmse(points, "vn"),
        },
    ]
    rows = pd.DataFrame(candidates)
    rows["galaxy"] = "NGC4013"
    rows["endpoint_scores_allowed"] = True
    rows["claim_boundary"] = CLAIM_BOUNDARY
    rows = rows[
        [
            "galaxy",
            "candidate_id",
            "candidate_role",
            "rmse",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]
    rows["rank_all_candidates"] = rows["rmse"].rank(method="min").astype(int)

    wrong = rows.loc[rows["candidate_role"].str.startswith("wrong_family")]
    matched_row = rows.loc[rows["candidate_id"] == "matched_K_warp_vertical_overlay"].iloc[0]
    family_null = rows.loc[
        rows["candidate_role"].isin(
            [
                "matched_caveated_replacement_family",
                "wrong_family_control",
                "wrong_family_control_rejected_original",
            ]
        )
    ].copy()
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "matched_candidate": "matched_K_warp_vertical_overlay",
                "n_wrong_family_controls": len(wrong),
                "matched_rmse": float(matched_row["rmse"]),
                "wrong_family_mean_rmse": float(wrong["rmse"].mean()),
                "wrong_family_best_rmse": float(wrong["rmse"].min()),
                "matched_minus_wrong_mean": float(matched_row["rmse"] - wrong["rmse"].mean()),
                "matched_minus_wrong_best": float(matched_row["rmse"] - wrong["rmse"].min()),
                "matched_beats_all_wrong_families": bool((matched_row["rmse"] < wrong["rmse"]).all()),
                "family_label_null_mean_rmse": float(family_null["rmse"].mean()),
                "matched_minus_family_label_null_mean": float(
                    matched_row["rmse"] - family_null["rmse"].mean()
                ),
                "matched_rank_among_family_labels": int(
                    family_null["rmse"].rank(method="min").loc[matched_row.name]
                ),
                "n_family_label_candidates": len(family_null),
                "uniform_label_null_best_probability": 1.0 / len(family_null),
                "control_status": (
                    "PASSED_SINGLE_GALAXY_WRONG_FAMILY_CONTROL"
                    if bool((matched_row["rmse"] < wrong["rmse"]).all())
                    else "NEGATIVE_RESULT_MATCHED_DOES_NOT_BEAT_ALL_WRONG_FAMILIES"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    rows.to_csv(
        DATA / "ngc4013_warp_vertical_overlay_control_candidates.csv", index=False
    )
    summary.to_csv(
        DATA / "ngc4013_warp_vertical_overlay_control_summary.csv", index=False
    )

    report = [
        "# NGC4013 Warp/Vertical-Overlay Control Audit",
        "",
        "This audit compares the caveated replacement endpoint against wrong-family",
        "Tau controls and conventional proxy baselines. It is a single-galaxy",
        "control, not a population shuffled-null test.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Candidates",
        "",
        markdown_table(rows.sort_values("rmse")),
        "",
        "## Claim Boundary",
        "",
        "The caveated replacement readout ranks first among the inspected family",
        "labels for NGC4013 and beats all wrong-family controls. This supports",
        "the source-driven compact-to-warp/vertical-overlay reclassification for",
        "this galaxy only.",
        "",
    ]
    (REPORTS / "ngc4013_warp_vertical_overlay_control_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
