#!/usr/bin/env python3
"""Freeze endpoint-blind S4G morphology features for attribution testing."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
SPLIT_SALT = "tau-core-s4g-optical-attribution-v01"
HOLDOUT_THRESHOLD = 25

SOURCE_FILES = {
    "sparc_source": DATA / "external_sparc_master_table.csv",
    "s4g_crossmatch": DATA / "external_s4g_sparc_observable_candidates.csv",
    "s4g_global": DATA / "external_s4g_galaxies.csv",
}

FORBIDDEN_TOKENS = (
    "vobs",
    "residual",
    "rmse",
    "endpoint",
    "score",
    "mond",
    "tpg",
    "required_s_tau",
)

BASELINE_FEATURES = [
    "sparc_t_type",
    "log_distance_mpc",
    "inclination_deg",
    "log_l36",
    "log_reff_kpc",
    "log_sbeff",
    "log_rdisk_kpc",
    "log_sbdisk",
    "log_mhi",
    "log_rhi_kpc",
]

MORPHOLOGY_FEATURES = [
    "log_s4g_scale_to_sparc_rdisk",
    "s4g_bar_present",
    "s4g_bar_to_disk_scale",
    "s4g_component_bulge",
    "s4g_component_disk",
    "s4g_component_edge_disk",
    "s4g_component_nucleus",
    "s4g_component_bar",
    "s4g_model_quality",
    "s4g_global_sersic_n",
    "s4g_global_axis_ratio_q",
    "s4g_global_ellipticity",
    "log_s4g_global_re_to_disk_scale",
    "s4g_global_tmag",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_log(value: object) -> float:
    if pd.isna(value) or float(value) <= 0:
        return math.nan
    return math.log(float(value))


def component_flag(value: object, token: str) -> int:
    if pd.isna(value):
        return 0
    return int(token in {part.strip() for part in str(value).split(";")})


def split_for(galaxy: str) -> str:
    digest = hashlib.sha256(f"{SPLIT_SALT}:{galaxy}".encode()).hexdigest()
    return "holdout" if int(digest[:8], 16) % 100 < HOLDOUT_THRESHOLD else "train"


def main() -> None:
    for name, path in SOURCE_FILES.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing {name}: {path}")
        lowered = path.name.lower()
        if any(token in lowered for token in FORBIDDEN_TOKENS):
            raise RuntimeError(f"Forbidden endpoint-like source path: {path}")

    sparc = pd.read_csv(SOURCE_FILES["sparc_source"])
    cross = pd.read_csv(SOURCE_FILES["s4g_crossmatch"])
    global_s4g = pd.read_csv(SOURCE_FILES["s4g_global"])

    cross = cross.loc[
        (cross["s4g_match_status"] == "S4G_MATCHED")
        & cross["scale_radius_kpc"].notna()
        & cross["s4g_model_components"].notna()
        & cross["s4g_model_quality_values"].notna()
    ].copy()
    merged = cross.merge(
        sparc,
        left_on="galaxy",
        right_on="Galaxy",
        how="inner",
        validate="one_to_one",
    ).merge(
        global_s4g,
        left_on="s4g_name",
        right_on="Name",
        how="left",
        validate="one_to_one",
        suffixes=("", "_s4g_global"),
    )

    out = pd.DataFrame({"galaxy": merged["galaxy"].astype(str)})
    out["split"] = out["galaxy"].map(split_for)
    out["source_family"] = "S4G_3P6UM_PIPELINE4_PLUS_GLOBAL_PROFILE"
    out["endpoint_blind"] = True
    out["retrospective_lock"] = True

    out["sparc_t_type"] = merged["T"].astype(float)
    out["log_distance_mpc"] = merged["D_Mpc"].map(safe_log)
    out["inclination_deg"] = merged["Inc_deg"].astype(float)
    out["log_l36"] = merged["L36_1e9Lsun"].map(safe_log)
    out["log_reff_kpc"] = merged["Reff_kpc"].map(safe_log)
    out["log_sbeff"] = merged["SBeff_Lsun_pc2"].map(safe_log)
    out["log_rdisk_kpc"] = merged["Rdisk_kpc"].map(safe_log)
    out["log_sbdisk"] = merged["SBdisk_Lsun_pc2"].map(safe_log)
    out["log_mhi"] = merged["MHI_1e9Msun"].map(safe_log)
    out["log_rhi_kpc"] = merged["RHI_kpc"].map(safe_log)

    scale_ratio = merged["scale_radius_kpc"] / merged["Rdisk_kpc"]
    out["log_s4g_scale_to_sparc_rdisk"] = scale_ratio.map(safe_log)
    out["s4g_bar_present"] = merged["bar_radius_kpc"].notna().astype(int)
    out["s4g_bar_to_disk_scale"] = (
        merged["bar_radius_kpc"] / merged["scale_radius_kpc"]
    )
    out["s4g_component_bulge"] = merged["s4g_model_components"].map(
        lambda value: component_flag(value, "B")
    )
    out["s4g_component_disk"] = merged["s4g_model_components"].map(
        lambda value: component_flag(value, "D")
    )
    out["s4g_component_edge_disk"] = merged["s4g_model_components"].map(
        lambda value: component_flag(value, "Z")
    )
    out["s4g_component_nucleus"] = merged["s4g_model_components"].map(
        lambda value: component_flag(value, "N")
    )
    out["s4g_component_bar"] = merged["s4g_model_components"].map(
        lambda value: component_flag(value, "BAR")
    )
    out["s4g_model_quality"] = merged["s4g_model_quality_values"].astype(float)
    out["s4g_global_sersic_n"] = pd.to_numeric(merged["n"], errors="coerce")
    out["s4g_global_axis_ratio_q"] = pd.to_numeric(merged["q"], errors="coerce")
    out["s4g_global_ellipticity"] = pd.to_numeric(merged["Ell"], errors="coerce")
    out["log_s4g_global_re_to_disk_scale"] = (
        pd.to_numeric(merged["Re"], errors="coerce")
        / merged["s4g_disk_scale_arcsec"]
    ).map(safe_log)
    out["s4g_global_tmag"] = pd.to_numeric(merged["Tmag"], errors="coerce")

    baseline_missingness_features = []
    morphology_missingness_features = []
    for feature in BASELINE_FEATURES + MORPHOLOGY_FEATURES:
        if out[feature].isna().any():
            missing_name = f"{feature}__missing"
            out[missing_name] = out[feature].isna().astype(int)
            if feature in BASELINE_FEATURES:
                baseline_missingness_features.append(missing_name)
            else:
                morphology_missingness_features.append(missing_name)

    out = out.sort_values("galaxy").reset_index(drop=True)
    output_csv = DATA / "s4g_optical_morphology_attribution_source_features_v02.csv"
    out.to_csv(output_csv, index=False)

    manifest = {
        "schema": "s4g_optical_morphology_attribution_freeze_v02",
        "status": "SOURCE_ONLY_RETROSPECTIVE_LOCK_V02_READY",
        "source_only": True,
        "endpoint_access": False,
        "retrospective_lock": True,
        "prospective_validation": False,
        "split_salt": SPLIT_SALT,
        "holdout_threshold_percent": HOLDOUT_THRESHOLD,
        "n_rows": int(len(out)),
        "n_train": int((out["split"] == "train").sum()),
        "n_holdout": int((out["split"] == "holdout").sum()),
        "baseline_features": BASELINE_FEATURES,
        "morphology_features": MORPHOLOGY_FEATURES,
        "baseline_missingness_features": baseline_missingness_features,
        "morphology_missingness_features": morphology_missingness_features,
        "imputation": "training_median_per_feature",
        "standardization": "training_mean_and_population_sd",
        "model": "ridge_linear_fixed_lambda_1",
        "primary_target": "log_tpg_v6_velocity_rmse",
        "primary_metric": "holdout_mean_squared_error_reduction",
        "controls": [
            "log_newtonian_baryonic_velocity_rmse_target",
            "morphology_row_shuffle_1000",
            "morphology_column_permutation_1000",
            "baseline_plus_missingness_only",
        ],
        "promotion_rule": (
            "positive holdout MSE reduction; row-shuffle p<=0.05; column-shuffle "
            "p<=0.05; observed reduction above both null 95th percentiles; "
            "larger proportional gain than on the Newtonian control target"
        ),
        "claim_boundary": (
            "retrospective locked prevalidation only; not independent external "
            "replication, shared-parent proof, or M_tau attribution"
        ),
        "v01_coverage_failure": (
            "Paper 1 publication endpoint joined only 33 of 76 frozen source rows; "
            "v02 switches by coverage rule to the Paper 8 full-population paired "
            "TPG-v6/Newtonian RMSE endpoint before any v02 scoring"
        ),
        "input_sha256": {name: sha256(path) for name, path in SOURCE_FILES.items()},
        "output_sha256": sha256(output_csv),
        "forbidden_tokens": FORBIDDEN_TOKENS,
    }
    manifest_path = DATA / "s4g_optical_morphology_attribution_freeze_v02.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / "s4g_optical_morphology_attribution_freeze_v02.md"
    report_path.write_text(
        "\n".join(
            [
                "# S4G Optical Morphology Attribution Freeze v0.2",
                "",
                "**Status:** `SOURCE_ONLY_RETROSPECTIVE_LOCK_V02_READY`",
                "",
                "This freeze reads no observed velocity, residual, score, RMSE,",
                "MOND/TPG, or endpoint artifact. It fixes the source rows, feature",
                "sets, split, imputation, standardization, model, metrics, controls,",
                "and promotion rule before the separate scorer is run.",
                "",
                f"- rows: `{len(out)}`",
                f"- train: `{(out['split'] == 'train').sum()}`",
                f"- holdout: `{(out['split'] == 'holdout').sum()}`",
                f"- baseline features: `{len(BASELINE_FEATURES)}`",
                f"- morphology features: `{len(MORPHOLOGY_FEATURES)}`",
                f"- baseline missingness flags: `{len(baseline_missingness_features)}`",
                f"- morphology missingness flags: `{len(morphology_missingness_features)}`",
                "",
                "The split is deterministic from galaxy name and a frozen salt.",
                "Because SPARC endpoints have been analyzed elsewhere in the program,",
                "this is a retrospective lock, not a prospective blind validation.",
                "The v0.1 endpoint covered only 33/76 frozen rows; v0.2 uses the",
                "full-population paired TPG-v6/Newtonian RMSE endpoint by a coverage rule.",
                "",
                "No endpoint scoring is performed by this script.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(manifest["status"])
    print(output_csv)
    print(manifest_path)
    print(report_path)


if __name__ == "__main__":
    main()
