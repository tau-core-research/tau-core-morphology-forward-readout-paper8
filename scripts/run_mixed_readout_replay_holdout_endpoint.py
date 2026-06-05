#!/usr/bin/env python3
"""Run the strict mixed-readout replay/holdout endpoint.

This endpoint scores only fresh replay/holdout mixed protocols:

- NGC5907 uses the source-frozen exponential-disk/projection mixed formula.
- NGC7331 uses the V2 fractional-onset replay freeze manifest.

NGC4013 is intentionally excluded because it is a retrospective frozen
reference protocol, not a fresh replay/holdout case. Observed velocities are
read only in the scoring block.
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
CLAIM_BOUNDARY = "mixed_readout_replay_holdout_endpoint_small_n_not_validation"
CASE_ORDER = ["NGC5907", "NGC7331"]
FORMULA_LABELS = {
    "NGC5907": "K_expdisk_projection_overlay",
    "NGC7331": "K_expdisk_vertical_outer_warp_fractional_onset_v2",
}

sys.path.insert(0, str(ROOT / "scripts"))
import run_mixed_readout_population_endpoint as population_endpoint  # noqa: E402
import run_source_native_readout_formula_endpoint as src  # noqa: E402
import run_s4g75_promoted_kernel_endpoint_stress_test as promoted  # noqa: E402


def rmse(obs: pd.Series, pred: pd.Series) -> float:
    return float(np.sqrt(np.mean(np.square(pred.to_numpy() - obs.to_numpy()))))


def smoothstep(x: np.ndarray) -> np.ndarray:
    clipped = np.clip(x, 0.0, 1.0)
    return clipped * clipped * (3.0 - 2.0 * clipped)


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


def build_generic_predictions() -> pd.DataFrame:
    points, _labels = src.load_points()
    points = promoted.apply_promoted_observables(points)
    points = src.add_bridge_formula_kernels(points)
    amplitudes = src.fit_amplitudes(points)
    return src.add_predictions(points, amplitudes)


def add_ngc5907_formula(sub: pd.DataFrame, manifest: pd.Series) -> pd.DataFrame:
    out = sub.sort_values("r").reset_index(drop=True).copy()
    r = out["r"].to_numpy(dtype=float)
    r_in = float(manifest["r_in_kpc"])
    r_out = float(manifest["r_out_kpc"])
    truncation_contrast = float(manifest["truncation_contrast"])
    gamma = float(manifest["gamma_projection"])

    x = (r - r_in) / max(r_out - r_in, 1.0e-9)
    window = smoothstep(x)
    kernel = window * (1.0 + truncation_contrast * window) / (1.0 + truncation_contrast)
    attenuation = np.clip(gamma * kernel, 0.0, 0.95)
    v2_carrier = out["v_K_exponential_disk"].to_numpy(dtype=float) ** 2
    out["mixed_kernel"] = kernel
    out["mixed_attenuation"] = attenuation
    out["v_mixed_replay_holdout"] = np.sqrt(np.maximum(v2_carrier * (1.0 - attenuation), 0.0))
    out["applied_formula_source"] = "NGC5907"
    out["applied_formula_label"] = FORMULA_LABELS["NGC5907"]
    out["applied_formula_id"] = str(manifest["formula_id"])
    return out


def add_ngc7331_v2_formula(sub: pd.DataFrame, manifest: pd.Series) -> pd.DataFrame:
    out = sub.sort_values("r").reset_index(drop=True).copy()
    r = out["r"].to_numpy(dtype=float)
    r_inner = float(manifest["r_window_inner_kpc"])
    r_outer = float(manifest["r_window_outer_kpc"])
    projected_hwhm_over_rs = float(manifest["projected_hwhm_over_Rs"])
    gamma = float(manifest["gamma_vow"])

    x = (r - r_inner) / max(r_outer - r_inner, 1.0e-9)
    w_outer = smoothstep(x)
    k_vertical = 0.5 / (1.0 + r / max(r_inner, 1.0e-9)) + 0.5 * projected_hwhm_over_rs
    kernel = w_outer * k_vertical
    attenuation = np.clip(gamma * kernel, 0.0, 0.95)
    v2_carrier = out["v_K_exponential_disk"].to_numpy(dtype=float) ** 2
    out["mixed_kernel"] = kernel
    out["mixed_attenuation"] = attenuation
    out["v_mixed_replay_holdout"] = np.sqrt(np.maximum(v2_carrier * (1.0 - attenuation), 0.0))
    out["applied_formula_source"] = "NGC7331"
    out["applied_formula_label"] = FORMULA_LABELS["NGC7331"]
    out["applied_formula_id"] = str(manifest["formula_id"])
    return out


def apply_formula(points: pd.DataFrame, galaxy: str, formula_source: str, manifest: pd.Series) -> pd.DataFrame:
    sub = points.loc[points["galaxy"].eq(galaxy)].copy()
    if formula_source == "NGC5907":
        out = add_ngc5907_formula(sub, manifest)
    elif formula_source == "NGC7331":
        out = add_ngc7331_v2_formula(sub, manifest)
    else:  # pragma: no cover
        raise ValueError(f"unknown formula source: {formula_source}")
    out["galaxy"] = galaxy
    out["label_assignment_role"] = "matched" if galaxy == formula_source else "wrong_label_control"
    return out


def score_case(sub: pd.DataFrame) -> dict[str, object]:
    mixed = rmse(sub["vobs"], sub["v_mixed_replay_holdout"])
    return {
        "galaxy": str(sub["galaxy"].iloc[0]),
        "n_points": len(sub),
        "rmse_newton": rmse(sub["vobs"], sub["vn"]),
        "rmse_tpg_v6": rmse(sub["vobs"], sub["v_v6"]),
        "rmse_mond": rmse(sub["vobs"], sub["v_mond"]),
        "rmse_exponential_disk_carrier": rmse(sub["vobs"], sub["v_K_exponential_disk"]),
        "rmse_mixed_replay_holdout": mixed,
        "mixed_minus_newton": mixed - rmse(sub["vobs"], sub["vn"]),
        "mixed_minus_tpg_v6": mixed - rmse(sub["vobs"], sub["v_v6"]),
        "mixed_minus_mond": mixed - rmse(sub["vobs"], sub["v_mond"]),
        "mixed_minus_exponential_disk_carrier": mixed
        - rmse(sub["vobs"], sub["v_K_exponential_disk"]),
        "beats_newton": mixed < rmse(sub["vobs"], sub["vn"]),
        "beats_tpg_v6": mixed < rmse(sub["vobs"], sub["v_v6"]),
        "beats_mond": mixed < rmse(sub["vobs"], sub["v_mond"]),
        "beats_exponential_disk_carrier": mixed < rmse(sub["vobs"], sub["v_K_exponential_disk"]),
        "applied_formula_source": str(sub["applied_formula_source"].iloc[0]),
        "applied_formula_label": str(sub["applied_formula_label"].iloc[0]),
        "applied_formula_id": str(sub["applied_formula_id"].iloc[0]),
        "case_status": (
            "FRESH_PROSPECTIVE_MIXED_PROTOCOL_REPLAY_HOLDOUT_SCORED"
            if str(sub["galaxy"].iloc[0]) == "NGC5907"
            else "V2_REPLAY_FRACTIONAL_ONSET_HOLDOUT_SCORED"
        ),
        "construction_used_vobs": False,
        "scoring_used_vobs": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    validation = pd.read_csv(DATA / "mixed_readout_population_validation_summary.csv").iloc[0]
    if validation["validation_gate_status"] != "MIXED_POPULATION_VALIDATION_READY":
        raise RuntimeError("mixed population validation gate is not ready")

    manifests = {
        "NGC5907": pd.read_csv(
            DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_manifest.csv"
        ).iloc[0],
        "NGC7331": pd.read_csv(
            DATA / "ngc7331_fractional_onset_v2_replay_freeze_manifest.csv"
        ).iloc[0],
    }
    if bool(manifests["NGC5907"].get("uses_vobs_or_residual_in_construction", False)):
        raise RuntimeError("NGC5907 replay/holdout manifest is not endpoint-blind")
    if bool(manifests["NGC7331"].get("uses_vobs_or_residual_in_construction", False)):
        raise RuntimeError("NGC7331 V2 replay manifest is not endpoint-blind")
    if not bool(manifests["NGC7331"].get("replay_or_holdout_required", False)):
        raise RuntimeError("NGC7331 V2 manifest should remain replay/holdout-only")

    points = build_generic_predictions()
    matched_points = [
        apply_formula(points, "NGC5907", "NGC5907", manifests["NGC5907"]),
        apply_formula(points, "NGC7331", "NGC7331", manifests["NGC7331"]),
    ]
    matched_all = pd.concat(matched_points, ignore_index=True)
    scores = pd.DataFrame([score_case(sub) for sub in matched_points])

    matrix_rows = []
    control_points = []
    for galaxy in CASE_ORDER:
        for formula_source in CASE_ORDER:
            sub = apply_formula(points, galaxy, formula_source, manifests[formula_source])
            control_points.append(sub)
            matrix_rows.append(
                {
                    "galaxy": galaxy,
                    "applied_formula_source": formula_source,
                    "applied_formula_label": FORMULA_LABELS[formula_source],
                    "label_assignment_role": "matched"
                    if galaxy == formula_source
                    else "wrong_label_control",
                    "rmse": rmse(sub["vobs"], sub["v_mixed_replay_holdout"]),
                    "construction_used_vobs": False,
                    "scoring_used_vobs": True,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    matrix = pd.DataFrame(matrix_rows)
    matrix["rank_within_galaxy"] = matrix.groupby("galaxy")["rmse"].rank(method="min").astype(int)

    permutation_rows = []
    for perm in itertools.permutations(CASE_ORDER):
        assignment = dict(zip(CASE_ORDER, perm))
        selected = []
        for galaxy, formula_source in assignment.items():
            selected.append(
                matrix.loc[
                    matrix["galaxy"].eq(galaxy)
                    & matrix["applied_formula_source"].eq(formula_source)
                ].iloc[0]
            )
        selected_df = pd.DataFrame(selected)
        is_matched = all(galaxy == assignment[galaxy] for galaxy in CASE_ORDER)
        permutation_rows.append(
            {
                "assignment_id": ";".join(
                    f"{galaxy}->{assignment[galaxy]}" for galaxy in CASE_ORDER
                ),
                "assignment_role": "matched_diagonal" if is_matched else "shuffled_label_null",
                "mean_rmse": float(selected_df["rmse"].mean()),
                "sum_rmse": float(selected_df["rmse"].sum()),
                "n_matched_labels": sum(galaxy == assignment[galaxy] for galaxy in CASE_ORDER),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    permutations = pd.DataFrame(permutation_rows).sort_values("mean_rmse").reset_index(drop=True)
    permutations["rank_by_mean_rmse"] = permutations["mean_rmse"].rank(method="min").astype(int)

    per_galaxy_rows = []
    for galaxy in CASE_ORDER:
        sub = matrix.loc[matrix["galaxy"].eq(galaxy)]
        matched = sub.loc[sub["label_assignment_role"].eq("matched")].iloc[0]
        wrong = sub.loc[sub["label_assignment_role"].eq("wrong_label_control")]
        per_galaxy_rows.append(
            {
                "galaxy": galaxy,
                "matched_rmse": float(matched["rmse"]),
                "wrong_best_rmse": float(wrong["rmse"].min()),
                "matched_minus_wrong_best": float(matched["rmse"] - wrong["rmse"].min()),
                "matched_rank_within_galaxy": int(matched["rank_within_galaxy"]),
                "matched_beats_all_wrong_labels": bool((matched["rmse"] < wrong["rmse"]).all()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    per_galaxy = pd.DataFrame(per_galaxy_rows)
    matched_perm = permutations.loc[permutations["assignment_role"].eq("matched_diagonal")].iloc[0]
    shuffled = permutations.loc[permutations["assignment_role"].eq("shuffled_label_null")]

    summary = pd.DataFrame(
        [
            {
                "endpoint_status": "MIXED_REPLAY_HOLDOUT_2CASE_PRELIMINARY_RESULT",
                "n_cases_scored": len(scores),
                "case_set": "NGC5907_fresh_prospective;NGC7331_v2_fractional_onset_replay",
                "ngc4013_excluded_reason": "retrospective_reference_protocol_not_fresh_replay_holdout",
                "mean_rmse_mixed_replay_holdout": float(scores["rmse_mixed_replay_holdout"].mean()),
                "mean_rmse_newton": float(scores["rmse_newton"].mean()),
                "mean_rmse_tpg_v6": float(scores["rmse_tpg_v6"].mean()),
                "mean_rmse_mond": float(scores["rmse_mond"].mean()),
                "mean_rmse_exponential_disk_carrier": float(
                    scores["rmse_exponential_disk_carrier"].mean()
                ),
                "n_beats_newton": int(scores["beats_newton"].sum()),
                "n_beats_tpg_v6": int(scores["beats_tpg_v6"].sum()),
                "n_beats_mond": int(scores["beats_mond"].sum()),
                "n_beats_exponential_disk_carrier": int(
                    scores["beats_exponential_disk_carrier"].sum()
                ),
                "n_matched_beats_all_wrong_labels": int(
                    per_galaxy["matched_beats_all_wrong_labels"].sum()
                ),
                "matched_permutation_rank": int(matched_perm["rank_by_mean_rmse"]),
                "best_shuffled_mean_rmse": float(shuffled["mean_rmse"].min()),
                "matched_minus_best_shuffled": float(
                    matched_perm["mean_rmse"] - shuffled["mean_rmse"].min()
                ),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "claim_boundary": CLAIM_BOUNDARY,
                "claim_status": (
                    "two-case replay/holdout endpoint; encouraging if matched labels win, "
                    "but still small-N and not population validation"
                ),
            }
        ]
    )

    points_out = matched_all[
        [
            "galaxy",
            "r",
            "vobs",
            "errv",
            "vn",
            "v_v6",
            "v_mond",
            "v_K_exponential_disk",
            "mixed_kernel",
            "mixed_attenuation",
            "v_mixed_replay_holdout",
            "applied_formula_source",
            "applied_formula_label",
            "applied_formula_id",
            "label_assignment_role",
        ]
    ].copy()
    points_out["construction_used_vobs"] = False
    points_out["scoring_used_vobs"] = True
    points_out["claim_boundary"] = CLAIM_BOUNDARY

    pd.concat(control_points, ignore_index=True).to_csv(
        DATA / "mixed_readout_replay_holdout_control_points.csv", index=False
    )
    points_out.to_csv(DATA / "mixed_readout_replay_holdout_endpoint_points.csv", index=False)
    scores.to_csv(DATA / "mixed_readout_replay_holdout_endpoint_scores.csv", index=False)
    summary.to_csv(DATA / "mixed_readout_replay_holdout_endpoint_summary.csv", index=False)
    matrix.to_csv(DATA / "mixed_readout_replay_holdout_control_matrix.csv", index=False)
    per_galaxy.to_csv(DATA / "mixed_readout_replay_holdout_control_by_galaxy.csv", index=False)
    permutations.to_csv(DATA / "mixed_readout_replay_holdout_shuffled_permutations.csv", index=False)

    report = [
        "# Mixed Readout Replay/Holdout Endpoint",
        "",
        "This endpoint scores the strict fresh replay/holdout subset. NGC4013 is",
        "excluded because it is a retrospective frozen reference protocol. NGC7331",
        "uses the V2 fractional-onset replay freeze manifest rather than the V1",
        "broad-window endpoint manifest.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        "## Matched vs Wrong Labels",
        "",
        markdown_table(per_galaxy),
        "",
        "## Shuffled Label Permutations",
        "",
        markdown_table(permutations),
        "",
        "## Claim Boundary",
        "",
        "This is a two-case replay/holdout endpoint. It is not population validation,",
        "not a universal baseline-superiority claim, and not a replacement for the",
        "larger predeclared population test.",
        "",
    ]
    (REPORTS / "mixed_readout_replay_holdout_endpoint.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))
    print(scores.to_string(index=False))
    print(per_galaxy.to_string(index=False))


if __name__ == "__main__":
    main()
