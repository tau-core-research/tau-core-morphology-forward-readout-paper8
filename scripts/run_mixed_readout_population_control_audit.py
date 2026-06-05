#!/usr/bin/env python3
"""Audit the mixed-population endpoint against wrong mixed-readout labels.

The audit applies each frozen mixed formula shell to each of the three scored
galaxies, then evaluates all one-to-one formula-label permutations. Formula
parameters remain frozen; observed velocities are used only for scoring.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "mixed_readout_population_wrong_label_control_audit"

sys.path.insert(0, str(ROOT / "scripts"))
import run_mixed_readout_population_endpoint as endpoint  # noqa: E402


FORMULA_ORDER = ["NGC4013", "NGC5907", "NGC7331"]
FORMULA_LABELS = {
    "NGC4013": "K_expdisk_warp_vertical_overlay",
    "NGC5907": "K_expdisk_projection_overlay",
    "NGC7331": "K_expdisk_vertical_outer_warp_overlay",
}


def rmse(obs: pd.Series, pred: pd.Series) -> float:
    return float(np.sqrt(np.mean(np.square(pred.to_numpy() - obs.to_numpy()))))


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


def apply_formula_to_galaxy(
    points: pd.DataFrame, galaxy: str, formula_source: str, manifest: pd.Series
) -> pd.DataFrame:
    """Apply one frozen formula shell to a target galaxy without reading vobs."""
    sub = points.loc[points["galaxy"].eq(galaxy)].sort_values("r").reset_index(drop=True).copy()
    original_galaxy = sub["galaxy"].copy()
    if formula_source == "NGC4013":
        manifest = manifest.copy()
        sub["galaxy"] = "NGC4013"
        out = endpoint.add_ngc4013_mixed(sub, manifest)
    elif formula_source == "NGC5907":
        manifest = manifest.copy()
        sub["galaxy"] = "NGC5907"
        out = endpoint.add_ngc5907_mixed(sub, manifest)
    elif formula_source == "NGC7331":
        manifest = manifest.copy()
        sub["galaxy"] = "NGC7331"
        out = endpoint.add_ngc7331_mixed(sub, manifest)
    else:  # pragma: no cover
        raise ValueError(f"unknown formula source: {formula_source}")
    out["galaxy"] = original_galaxy.to_numpy()
    out["applied_formula_source"] = formula_source
    out["applied_formula_label"] = FORMULA_LABELS[formula_source]
    out["label_assignment_role"] = "matched" if galaxy == formula_source else "wrong_label_control"
    return out


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    endpoint_summary = pd.read_csv(DATA / "mixed_readout_population_endpoint_summary.csv").iloc[0]
    if endpoint_summary["endpoint_status"] != "MIXED_POPULATION_ENDPOINT_PRELIMINARY_CONTROL_RESULT":
        raise RuntimeError("mixed-population endpoint must be scored before control audit")

    points = endpoint.build_generic_predictions()
    manifests = {
        "NGC4013": pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_manifest.csv").iloc[0],
        "NGC5907": pd.read_csv(
            DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_manifest.csv"
        ).iloc[0],
        "NGC7331": pd.read_csv(
            DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_manifest.csv"
        ).iloc[0],
    }

    matrix_rows = []
    point_rows = []
    for galaxy in FORMULA_ORDER:
        for formula_source in FORMULA_ORDER:
            sub = apply_formula_to_galaxy(points, galaxy, formula_source, manifests[formula_source])
            point_rows.append(sub)
            score = rmse(sub["vobs"], sub["v_mixed_population"])
            matrix_rows.append(
                {
                    "galaxy": galaxy,
                    "applied_formula_source": formula_source,
                    "applied_formula_label": FORMULA_LABELS[formula_source],
                    "label_assignment_role": "matched"
                    if galaxy == formula_source
                    else "wrong_label_control",
                    "rmse": score,
                    "construction_used_vobs": False,
                    "scoring_used_vobs": True,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    matrix = pd.DataFrame(matrix_rows)
    matrix["rank_within_galaxy"] = matrix.groupby("galaxy")["rmse"].rank(method="min").astype(int)

    permutation_rows = []
    for perm in itertools.permutations(FORMULA_ORDER):
        assignment = dict(zip(FORMULA_ORDER, perm))
        selected = []
        for galaxy, formula_source in assignment.items():
            row = matrix.loc[
                matrix["galaxy"].eq(galaxy)
                & matrix["applied_formula_source"].eq(formula_source)
            ].iloc[0]
            selected.append(row)
        selected_df = pd.DataFrame(selected)
        is_matched = all(galaxy == assignment[galaxy] for galaxy in FORMULA_ORDER)
        permutation_rows.append(
            {
                "assignment_id": ";".join(
                    f"{galaxy}->{assignment[galaxy]}" for galaxy in FORMULA_ORDER
                ),
                "assignment_role": "matched_diagonal" if is_matched else "shuffled_label_null",
                "mean_rmse": float(selected_df["rmse"].mean()),
                "sum_rmse": float(selected_df["rmse"].sum()),
                "n_matched_labels": sum(galaxy == assignment[galaxy] for galaxy in FORMULA_ORDER),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    permutations = pd.DataFrame(permutation_rows).sort_values("mean_rmse").reset_index(drop=True)
    permutations["rank_by_mean_rmse"] = permutations["mean_rmse"].rank(method="min").astype(int)

    matched_rows = matrix.loc[matrix["label_assignment_role"].eq("matched")]
    wrong_rows = matrix.loc[matrix["label_assignment_role"].eq("wrong_label_control")]
    matched_perm = permutations.loc[permutations["assignment_role"].eq("matched_diagonal")].iloc[0]
    shuffled = permutations.loc[permutations["assignment_role"].eq("shuffled_label_null")]
    per_galaxy = []
    for galaxy in FORMULA_ORDER:
        sub = matrix.loc[matrix["galaxy"].eq(galaxy)]
        matched = sub.loc[sub["label_assignment_role"].eq("matched")].iloc[0]
        wrong = sub.loc[sub["label_assignment_role"].eq("wrong_label_control")]
        per_galaxy.append(
            {
                "galaxy": galaxy,
                "matched_rmse": float(matched["rmse"]),
                "wrong_mean_rmse": float(wrong["rmse"].mean()),
                "wrong_best_rmse": float(wrong["rmse"].min()),
                "matched_minus_wrong_mean": float(matched["rmse"] - wrong["rmse"].mean()),
                "matched_minus_wrong_best": float(matched["rmse"] - wrong["rmse"].min()),
                "matched_rank_within_galaxy": int(matched["rank_within_galaxy"]),
                "matched_beats_all_wrong_labels": bool((matched["rmse"] < wrong["rmse"]).all()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    per_galaxy_summary = pd.DataFrame(per_galaxy)

    summary = pd.DataFrame(
        [
            {
                "control_status": (
                    "PASSED_3CASE_WRONG_LABEL_AND_SHUFFLED_CONTROL"
                    if bool(per_galaxy_summary["matched_beats_all_wrong_labels"].all())
                    and int(matched_perm["rank_by_mean_rmse"]) == 1
                    else "NEGATIVE_OR_PARTIAL_WRONG_LABEL_CONTROL_RESULT"
                ),
                "n_galaxies": len(FORMULA_ORDER),
                "n_formula_labels": len(FORMULA_ORDER),
                "mean_matched_rmse": float(matched_rows["rmse"].mean()),
                "mean_wrong_label_rmse": float(wrong_rows["rmse"].mean()),
                "matched_minus_wrong_label_mean": float(
                    matched_rows["rmse"].mean() - wrong_rows["rmse"].mean()
                ),
                "n_matched_beats_all_wrong_labels": int(
                    per_galaxy_summary["matched_beats_all_wrong_labels"].sum()
                ),
                "matched_permutation_mean_rmse": float(matched_perm["mean_rmse"]),
                "best_shuffled_mean_rmse": float(shuffled["mean_rmse"].min()),
                "matched_minus_best_shuffled": float(
                    matched_perm["mean_rmse"] - shuffled["mean_rmse"].min()
                ),
                "matched_permutation_rank": int(matched_perm["rank_by_mean_rmse"]),
                "n_shuffled_permutations": len(shuffled),
                "uniform_shuffled_best_probability": 1.0 / len(permutations),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "claim_boundary": CLAIM_BOUNDARY,
                "claim_status": (
                    "wrong-label control on three frozen formula shells; "
                    "still small-N and not population validation"
                ),
            }
        ]
    )

    points_out = pd.concat(point_rows, ignore_index=True)[
        [
            "galaxy",
            "r",
            "vobs",
            "errv",
            "v_K_exponential_disk",
            "mixed_kernel",
            "mixed_attenuation",
            "v_mixed_population",
            "applied_formula_source",
            "applied_formula_label",
            "label_assignment_role",
        ]
    ].copy()
    points_out["construction_used_vobs"] = False
    points_out["scoring_used_vobs"] = True
    points_out["claim_boundary"] = CLAIM_BOUNDARY

    matrix.to_csv(DATA / "mixed_readout_population_control_matrix.csv", index=False)
    permutations.to_csv(DATA / "mixed_readout_population_shuffled_label_permutations.csv", index=False)
    per_galaxy_summary.to_csv(
        DATA / "mixed_readout_population_control_by_galaxy.csv", index=False
    )
    summary.to_csv(DATA / "mixed_readout_population_control_summary.csv", index=False)
    points_out.to_csv(DATA / "mixed_readout_population_control_points.csv", index=False)

    report = [
        "# Mixed Readout Population Wrong-Label Control Audit",
        "",
        "This audit applies each frozen mixed formula shell to each of the three",
        "scored galaxies, then evaluates all one-to-one formula-label shuffles.",
        "The construction reads frozen manifests only; observed velocities are",
        "used only for scoring.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Per-Galaxy Matched vs Wrong Labels",
        "",
        markdown_table(per_galaxy_summary),
        "",
        "## Formula Matrix",
        "",
        markdown_table(matrix.sort_values(["galaxy", "rmse"])),
        "",
        "## Label Permutations",
        "",
        markdown_table(permutations.sort_values("mean_rmse")),
        "",
        "## Claim Boundary",
        "",
        "This is a small-N wrong-label control, not a population validation. It",
        "tests whether the source-matched frozen mixed formula labels beat the",
        "available wrong mixed labels within the three-case packet.",
        "",
    ]
    (REPORTS / "mixed_readout_population_control_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(per_galaxy_summary.to_string(index=False))


if __name__ == "__main__":
    main()
