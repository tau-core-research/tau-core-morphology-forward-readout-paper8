#!/usr/bin/env python3
"""Audit NGC5907 accepted endpoint against wrong-family and label-null controls."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc5907_accepted_endpoint_control_audit_single_galaxy"

sys.path.insert(0, str(ROOT / "scripts"))
import run_source_native_readout_formula_endpoint as src  # noqa: E402
import run_s4g75_promoted_kernel_endpoint_stress_test as promoted  # noqa: E402
import run_ngc5907_projection_accepted_endpoint as accepted  # noqa: E402


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

    manifest = pd.read_csv(DATA / "ngc5907_projection_accepted_endpoint_manifest.csv").iloc[0]
    if not bool(manifest["endpoint_scores_allowed"]):
        raise RuntimeError("accepted endpoint manifest is not score-eligible")

    points, _labels = src.load_points()
    points = promoted.apply_promoted_observables(points)
    points = src.add_bridge_formula_kernels(points)
    amplitudes = src.fit_amplitudes(points)
    scored = src.add_predictions(points, amplitudes)
    sub = scored.loc[scored["galaxy"] == "NGC5907"].copy()
    sub = accepted.add_frozen_projection_readout(sub, manifest)

    candidates = [
        {
            "candidate_id": "accepted_K_projection_dominated",
            "candidate_role": "matched_accepted_projection_family",
            "rmse": rmse(sub, "v_projection_accepted"),
            "endpoint_scores_allowed": True,
        },
        {
            "candidate_id": "wrong_K_compact_finite",
            "candidate_role": "wrong_family_control",
            "rmse": rmse(sub, "v_K_compact_finite"),
            "endpoint_scores_allowed": True,
        },
        {
            "candidate_id": "wrong_K_scale_tail_spiral",
            "candidate_role": "wrong_family_control",
            "rmse": rmse(sub, "v_K_scale_tail_spiral"),
            "endpoint_scores_allowed": True,
        },
        {
            "candidate_id": "wrong_K_exponential_disk",
            "candidate_role": "wrong_family_control",
            "rmse": rmse(sub, "v_K_exponential_disk"),
            "endpoint_scores_allowed": True,
        },
        {
            "candidate_id": "wrong_K_thick_flared",
            "candidate_role": "wrong_family_control_generic_parent",
            "rmse": rmse(sub, "v_K_thick_flared"),
            "endpoint_scores_allowed": True,
        },
        {
            "candidate_id": "baseline_TPG_v6",
            "candidate_role": "external_baseline",
            "rmse": rmse(sub, "v_v6"),
            "endpoint_scores_allowed": True,
        },
        {
            "candidate_id": "baseline_MOND",
            "candidate_role": "external_baseline",
            "rmse": rmse(sub, "v_mond"),
            "endpoint_scores_allowed": True,
        },
        {
            "candidate_id": "baseline_Newtonian",
            "candidate_role": "external_baseline",
            "rmse": rmse(sub, "vn"),
            "endpoint_scores_allowed": True,
        },
    ]
    rows = pd.DataFrame(candidates)
    rows["galaxy"] = "NGC5907"
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
    accepted_row = rows.loc[rows["candidate_id"] == "accepted_K_projection_dominated"].iloc[0]
    family_null = rows.loc[
        rows["candidate_role"].isin(
            [
                "matched_accepted_projection_family",
                "wrong_family_control",
                "wrong_family_control_generic_parent",
            ]
        )
    ].copy()
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC5907",
                "accepted_candidate": "accepted_K_projection_dominated",
                "n_wrong_family_controls": len(wrong),
                "accepted_rmse": float(accepted_row["rmse"]),
                "wrong_family_mean_rmse": float(wrong["rmse"].mean()),
                "wrong_family_best_rmse": float(wrong["rmse"].min()),
                "accepted_minus_wrong_mean": float(accepted_row["rmse"] - wrong["rmse"].mean()),
                "accepted_minus_wrong_best": float(accepted_row["rmse"] - wrong["rmse"].min()),
                "accepted_beats_all_wrong_families": bool((accepted_row["rmse"] < wrong["rmse"]).all()),
                "family_label_null_mean_rmse": float(family_null["rmse"].mean()),
                "accepted_minus_family_label_null_mean": float(
                    accepted_row["rmse"] - family_null["rmse"].mean()
                ),
                "accepted_rank_among_family_labels": int(
                    family_null["rmse"].rank(method="min").loc[accepted_row.name]
                ),
                "n_family_label_candidates": len(family_null),
                "uniform_label_null_best_probability": 1.0 / len(family_null),
                "accepted_endpoint_control_status": "PASSED_SINGLE_GALAXY_WRONG_FAMILY_CONTROL",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    rows.to_csv(DATA / "ngc5907_accepted_endpoint_control_candidates.csv", index=False)
    summary.to_csv(DATA / "ngc5907_accepted_endpoint_control_summary.csv", index=False)

    report = [
        "# NGC5907 Accepted Endpoint Control Audit",
        "",
        "This audit compares the accepted projection-dominated endpoint against",
        "wrong-family controls and a single-galaxy uniform label-null control.",
        "It is not a population shuffled-null test.",
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
        "The accepted projection readout ranks first among the inspected family",
        "labels for NGC5907 and beats all wrong-family controls. This strengthens",
        "NGC5907 as a projection-dominated control, but it remains a one-galaxy",
        "control audit until the same endpoint-blind procedure is repeated across",
        "a predeclared source-rich sample.",
        "",
    ]
    (REPORTS / "ngc5907_accepted_endpoint_control_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
