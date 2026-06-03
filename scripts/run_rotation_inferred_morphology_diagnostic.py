#!/usr/bin/env python3
"""Infer morphology-family preferences from rotation-curve scores.

This is an inverse diagnostic.  It asks which Tau Core readout family the
rotation curve would choose if the family were inferred from the score table.
It must not be used as a residual-blind morphology label for the Paper 8
endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

FAMILIES = [
    "K_compact_finite",
    "K_scale_tail_spiral",
    "K_exponential_disk",
    "K_thick_flared",
]


def infer_margin(row: pd.Series) -> tuple[str, float, int]:
    values = [(family, float(row[f"rmse_{family}"])) for family in FAMILIES]
    ranked = sorted(values, key=lambda item: item[1])
    best_family, best_rmse = ranked[0]
    second_rmse = ranked[1][1]
    matched_rank = [family for family, _ in ranked].index(row["formula_family"]) + 1
    return best_family, second_rmse - best_rmse, matched_rank


def confidence_from_margin(margin: float, best_rmse: float) -> str:
    denom = max(best_rmse, 1.0e-9)
    rel = margin / denom
    if rel >= 0.25:
        return "HIGH"
    if rel >= 0.10:
        return "MEDIUM"
    return "LOW"


def build_diagnostic() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    scores = pd.read_csv(DATA / "source_native_readout_formula_scores_by_galaxy.csv")
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    external = pd.read_csv(DATA / "exponential_disk_family_label_audit.csv")
    rows = []
    for _, row in scores.iterrows():
        inferred, margin, matched_rank = infer_margin(row)
        best_rmse = float(row[f"rmse_{inferred}"])
        rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "predeclared_formula_family": row["formula_family"],
                "rotation_inferred_family": inferred,
                "rotation_inferred_best_rmse": best_rmse,
                "rotation_inferred_margin_to_second": margin,
                "rotation_inferred_confidence": confidence_from_margin(margin, best_rmse),
                "predeclared_family_rank_by_rotation": matched_rank,
                "matches_predeclared_family": inferred == row["formula_family"],
                "rmse_tpg_v6": row["rmse_tpg_v6"],
                "rmse_mond": row["rmse_mond"],
                "rotation_inferred_beats_tpg_v6": best_rmse < row["rmse_tpg_v6"],
                "rotation_inferred_beats_mond": best_rmse < row["rmse_mond"],
                "claim_boundary": (
                    "inverse_rotation_diagnostic_not_residual_blind_label_not_endpoint"
                ),
            }
        )
    diagnostic = pd.DataFrame(rows).merge(
        manifest[
            [
                "galaxy",
                "manifest_confidence",
                "manifest_caveat",
                "type_bin",
                "inclination_deg",
                "distance_frac_error",
            ]
        ],
        on="galaxy",
        how="left",
        validate="one_to_one",
    )
    diagnostic = diagnostic.merge(
        external[
            [
                "galaxy",
                "external_family_label",
                "external_family_label_status",
                "narrow_dry_run_lane",
            ]
        ],
        on="galaxy",
        how="left",
    )
    diagnostic["matches_external_expdisk_label"] = (
        diagnostic["external_family_label"].notna()
        & (
            diagnostic["rotation_inferred_family"]
            == diagnostic["external_family_label"]
        )
    )
    summary = (
        diagnostic.groupby(
            ["predeclared_formula_family", "rotation_inferred_family"],
            as_index=False,
        )
        .agg(
            n_galaxies=("galaxy", "size"),
            n_matches_predeclared=("matches_predeclared_family", "sum"),
            median_margin=("rotation_inferred_margin_to_second", "median"),
        )
        .sort_values(["predeclared_formula_family", "rotation_inferred_family"])
    )
    external_summary = (
        diagnostic[diagnostic["external_family_label"].notna()]
        .groupby(
            [
                "external_family_label",
                "external_family_label_status",
                "rotation_inferred_family",
            ],
            as_index=False,
        )
        .agg(
            n_galaxies=("galaxy", "size"),
            n_matches_external=("matches_external_expdisk_label", "sum"),
            median_margin=("rotation_inferred_margin_to_second", "median"),
        )
        .sort_values(["external_family_label_status", "rotation_inferred_family"])
    )
    return diagnostic, summary, external_summary


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(
    diagnostic: pd.DataFrame, summary: pd.DataFrame, external_summary: pd.DataFrame
) -> None:
    match_rate = float(diagnostic["matches_predeclared_family"].mean())
    external = diagnostic[diagnostic["external_family_label"].notna()]
    external_match = float(external["matches_external_expdisk_label"].mean())
    inferred_counts = (
        diagnostic.groupby("rotation_inferred_family", as_index=False)
        .size()
        .rename(columns={"size": "n_galaxies"})
        .sort_values("rotation_inferred_family")
    )
    lines = [
        "# Rotation-Inferred Morphology Diagnostic",
        "",
        "This inverse diagnostic asks which Tau Core readout family is preferred by",
        "the rotation-curve score table. It intentionally violates the residual-blind",
        "direction required for the main Paper 8 endpoint, so it is a hypothesis",
        "generator only.",
        "This inverse diagnostic is a hypothesis generator only.",
        "",
        "## Verdict",
        "",
        f"Rotation-inferred family matches the predeclared proxy family in {match_rate:.3f} of rows.",
        f"For the 13 externally supported exponential-disk rows, it matches the external label in {external_match:.3f} of rows.",
        "",
        "This is useful for model development and subtype discovery, but it must not",
        "be used as accepted morphology evidence.",
        "",
        "## Inferred Family Counts",
        "",
        markdown_table(inferred_counts),
        "",
        "## Predeclared vs Rotation-Inferred Summary",
        "",
        markdown_table(summary),
        "",
        "## External Exponential-Disk Rows",
        "",
        markdown_table(external_summary),
        "",
        "## Claim Boundary",
        "",
        "This diagnostic is not residual-blind, not an endpoint score, and not a",
        "validation of Tau Core. It can suggest morphology-subtype splits to test",
        "later with external labels.",
        "It must not be used as accepted morphology evidence.",
    ]
    (REPORTS / "rotation_inferred_morphology_diagnostic.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    diagnostic, summary, external_summary = build_diagnostic()
    diagnostic.to_csv(DATA / "rotation_inferred_morphology_diagnostic.csv", index=False)
    summary.to_csv(DATA / "rotation_inferred_morphology_summary.csv", index=False)
    external_summary.to_csv(
        DATA / "rotation_inferred_external_expdisk_summary.csv", index=False
    )
    write_report(diagnostic, summary, external_summary)
    print("PAPER8_ROTATION_INFERRED_MORPHOLOGY_DIAGNOSTIC_COMPLETE")


if __name__ == "__main__":
    main()
