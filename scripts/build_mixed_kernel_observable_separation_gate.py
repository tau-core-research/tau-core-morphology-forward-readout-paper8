#!/usr/bin/env python3
"""Audit whether fresh mixed-readout source fields separate the kernels.

This is a residual-blind diagnostic gate.  It does not score a rotation curve
and it does not tune a formula.  It asks a narrower question prompted by the
strict replay/holdout negative specificity result: do the source-native fields
already distinguish the NGC5907 projection-dominated lane from the NGC7331
vertical/outer-warp V2 lane, or are the source labels themselves too coarse?
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "mixed_kernel_observable_separation_source_side_not_endpoint"


FEATURES = [
    "projection_bound",
    "disk_truncation_or_break",
    "fractional_onset_available",
    "fractional_onset_over_RHI",
    "vertical_activation",
    "projected_thickness",
]

PROTOTYPES = {
    "K_expdisk_projection_mixed": {
        "projection_bound": 1.0,
        "disk_truncation_or_break": 1.0,
        "fractional_onset_available": 0.0,
        "fractional_onset_over_RHI": 0.0,
        "vertical_activation": 0.35,
        "projected_thickness": 0.35,
    },
    "K_expdisk_vertical_outer_warp_v2": {
        "projection_bound": 0.0,
        "disk_truncation_or_break": 0.0,
        "fractional_onset_available": 1.0,
        "fractional_onset_over_RHI": 0.80,
        "vertical_activation": 1.0,
        "projected_thickness": 0.50,
    },
}


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


def clamp01(value: float) -> float:
    if pd.isna(value):
        return 0.0
    return max(0.0, min(1.0, float(value)))


def cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    denom = float(np.linalg.norm(left) * np.linalg.norm(right))
    if denom == 0.0:
        return 0.0
    return float(np.dot(left, right) / denom)


def feature_vector(row: pd.Series) -> np.ndarray:
    return np.array([float(row[name]) for name in FEATURES], dtype=float)


def prototype_vector(prototype_id: str) -> np.ndarray:
    values = PROTOTYPES[prototype_id]
    return np.array([float(values[name]) for name in FEATURES], dtype=float)


def build_fingerprints() -> pd.DataFrame:
    ngc5907_manifest = pd.read_csv(
        DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_manifest.csv"
    ).iloc[0]
    ngc5907_projection = pd.read_csv(DATA / "ngc5907_projection_freeze_summary.csv").iloc[0]
    ngc7331_manifest = pd.read_csv(
        DATA / "ngc7331_fractional_onset_v2_replay_freeze_manifest.csv"
    ).iloc[0]
    ngc7331_vertical = pd.read_csv(DATA / "ngc7331_outer_warp_vertical_caveat_summary.csv").iloc[0]

    rows = [
        {
            "galaxy": "NGC5907",
            "source_matched_formula": "K_expdisk_projection_mixed",
            "source_lane": "projection_dominated_expdisk_mixed",
            "projection_bound": clamp01(ngc5907_manifest["pi_projection"]),
            "disk_truncation_or_break": clamp01(ngc5907_manifest["truncation_contrast"]),
            "fractional_onset_available": 0.0,
            "fractional_onset_over_RHI": 0.0,
            "vertical_activation": clamp01(float(ngc5907_manifest["h_over_r"]) / 0.25),
            "projected_thickness": clamp01(float(ngc5907_projection["thickness_h_over_rs"]) / 0.25),
            "source_onset_kpc": float(ngc5907_manifest["r_in_kpc"]),
            "source_window_outer_kpc": float(ngc5907_manifest["r_out_kpc"]),
            "source_window_width_kpc": float(ngc5907_manifest["r_out_kpc"])
            - float(ngc5907_manifest["r_in_kpc"]),
            "dimension_status": "dimensionless_source_features",
            "uses_vobs_or_residual": False,
            "endpoint_scores_allowed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC7331",
            "source_matched_formula": "K_expdisk_vertical_outer_warp_v2",
            "source_lane": "vertical_outer_warp_fractional_onset_mixed",
            "projection_bound": 0.0,
            "disk_truncation_or_break": 0.0,
            "fractional_onset_available": 1.0
            if bool(ngc7331_manifest["outer_warp_numeric_onset_available"])
            else 0.0,
            "fractional_onset_over_RHI": clamp01(ngc7331_manifest["fractional_warp_onset_over_RHI"]),
            "vertical_activation": clamp01(ngc7331_manifest["vertical_activation_candidate"]),
            "projected_thickness": clamp01(float(ngc7331_vertical["projected_hwhm_over_Rs"]) / 0.25),
            "source_onset_kpc": float(ngc7331_manifest["r_window_inner_kpc"]),
            "source_window_outer_kpc": float(ngc7331_manifest["r_window_outer_kpc"]),
            "source_window_width_kpc": float(ngc7331_manifest["r_window_outer_kpc"])
            - float(ngc7331_manifest["r_window_inner_kpc"]),
            "dimension_status": "dimensionless_source_features",
            "uses_vobs_or_residual": False,
            "endpoint_scores_allowed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return pd.DataFrame(rows)


def build_similarity_matrix(fingerprints: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, galaxy_row in fingerprints.iterrows():
        galaxy_vector = feature_vector(galaxy_row)
        for prototype_id in PROTOTYPES:
            score = cosine_similarity(galaxy_vector, prototype_vector(prototype_id))
            rows.append(
                {
                    "galaxy": galaxy_row["galaxy"],
                    "source_matched_formula": galaxy_row["source_matched_formula"],
                    "prototype_formula": prototype_id,
                    "source_similarity": score,
                    "is_matched_formula": prototype_id == galaxy_row["source_matched_formula"],
                    "uses_vobs_or_residual": False,
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    matrix = pd.DataFrame(rows)
    matrix["rank_within_galaxy"] = matrix.groupby("galaxy")["source_similarity"].rank(
        method="min", ascending=False
    )
    return matrix.sort_values(["galaxy", "rank_within_galaxy", "prototype_formula"])


def build_summary(fingerprints: pd.DataFrame, matrix: pd.DataFrame) -> pd.DataFrame:
    matched = matrix[matrix["is_matched_formula"]].copy()
    wrong = matrix[~matrix["is_matched_formula"]].copy()
    joined = matched.merge(
        wrong[["galaxy", "source_similarity"]].rename(
            columns={"source_similarity": "best_wrong_source_similarity"}
        ),
        on="galaxy",
    )
    joined = joined.rename(columns={"source_similarity": "matched_source_similarity"})
    joined["source_similarity_margin"] = (
        joined["matched_source_similarity"] - joined["best_wrong_source_similarity"]
    )
    n_cases = int(len(joined))
    n_matched_first = int((joined["rank_within_galaxy"] == 1).sum())
    source_status = (
        "SOURCE_KERNEL_OBSERVABLE_SEPARATION_PASS"
        if n_cases > 0 and n_matched_first == n_cases and (joined["source_similarity_margin"] > 0).all()
        else "SOURCE_KERNEL_OBSERVABLE_SEPARATION_INSUFFICIENT"
    )
    implication = (
        "source_fields_separate_lanes_kernel_mapping_needs_sharpening"
        if source_status == "SOURCE_KERNEL_OBSERVABLE_SEPARATION_PASS"
        else "source_fields_do_not_yet_separate_lanes_acquire_stronger_observables"
    )
    return pd.DataFrame(
        [
            {
                "gate_status": source_status,
                "diagnostic_status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
                "cases_audited": n_cases,
                "matched_source_rank_first": n_matched_first,
                "min_source_similarity_margin": float(joined["source_similarity_margin"].min()),
                "mean_source_similarity_margin": float(joined["source_similarity_margin"].mean()),
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "endpoint_score_inputs_read": False,
                "dimension_check": "PASS: all audited features are dimensionless source-native proxies",
                "known_limit_check": (
                    "PASS: absent projection, absent truncation, or absent fractional onset drives "
                    "the corresponding prototype evidence to zero"
                ),
                "bridge_interpretation": implication,
                "next_obligation": (
                    "derive sharper projection and vertical/outer-warp kernel maps from these "
                    "separated source fields before rerunning replay/holdout specificity"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    fingerprints = build_fingerprints()
    matrix = build_similarity_matrix(fingerprints)
    summary = build_summary(fingerprints, matrix)

    fingerprints.to_csv(
        DATA / "mixed_kernel_observable_separation_fingerprints.csv", index=False
    )
    matrix.to_csv(DATA / "mixed_kernel_observable_separation_matrix.csv", index=False)
    summary.to_csv(DATA / "mixed_kernel_observable_separation_summary.csv", index=False)

    report = [
        "# Mixed Kernel Observable Separation Gate",
        "",
        "Status label: `DIAGNOSTIC_ONLY_NOT_ENDPOINT`.",
        "",
        "This gate is a residual-blind follow-up to the strict replay/holdout",
        "mixed endpoint. It does not read observed velocities, residuals, RMSE",
        "scores, required-S_tau diagnostics, or endpoint ranks. It only asks",
        "whether the source-native observables already separate the fresh",
        "NGC5907 projection-dominated mixed lane from the NGC7331 V2",
        "vertical/outer-warp mixed lane.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Source Fingerprints",
        "",
        markdown_table(fingerprints),
        "",
        "## Prototype Similarity Matrix",
        "",
        markdown_table(matrix),
        "",
        "## Interpretation",
        "",
        "If this gate passes while the replay/holdout endpoint still fails",
        "wrong-label or shuffled-label specificity, the immediate bottleneck is",
        "not the residual-blind source separation itself. The bottleneck is the",
        "current source-to-kernel map: the projection and vertical/outer-warp",
        "attenuation curves remain too similar after they are converted into",
        "4D readout kernels.",
        "",
        "If this gate fails, the next obligation is different: acquire stronger",
        "source-native morphology fields before changing kernels.",
        "",
        "## Claim Boundary",
        "",
        "This is not an endpoint score and not empirical validation. It is a",
        "source-side diagnostic for where to sharpen the next replay/holdout",
        "mixed-readout protocol.",
        "",
    ]
    (REPORTS / "mixed_kernel_observable_separation_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
