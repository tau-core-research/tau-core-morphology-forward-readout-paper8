#!/usr/bin/env python3
"""Build a residual-blind morphology-parameter manifest for Paper 8 preflights.

This is not the final hand-curated morphology catalog. It is a reproducible
available-data manifest that freezes the currently available proxy inputs:

    galaxy -> morphology family -> scale/cutoff/support/thickness parameters

The manifest is intentionally explicit about confidence and caveats so the
source-native bridge formula endpoint can consume a declared input table rather
than assigning labels internally.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
TPG_RESULTS = Path("/Users/jolcsak/Projects/TPG/results/tau_core_projection_v1")


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    points_path = TPG_RESULTS / "tau_rotation_curve_frozen_proxy_runner_v0_points.csv"
    meta_path = TPG_RESULTS / "tau_rotation_curve_projection_metadata_control_v0.csv"
    if not points_path.exists():
        raise FileNotFoundError(points_path)
    if not meta_path.exists():
        raise FileNotFoundError(meta_path)
    return pd.read_csv(points_path), pd.read_csv(meta_path)


def assign_family(row: pd.Series) -> str:
    if row["mean_bulge"] >= 0.10 or row["type_bin"] == "early_T_le_2":
        return "K_compact_finite"
    if row["type_bin"] == "irregular_T_ge_9" or (
        row["mean_gas"] >= 0.35 and row["mean_log_sbdisk"] <= 0.90
    ):
        return "K_scale_tail_spiral"
    if row["type_bin"] == "late_T_6_8":
        return "K_exponential_disk"
    return "K_thick_flared"


def confidence(row: pd.Series) -> tuple[float, str]:
    score = 1.0
    caveats: list[str] = []
    if row["n_points"] < 8:
        score -= 0.20
        caveats.append("few_rotation_points")
    if row["inc_bin"] == "inc_low_lt_40":
        score -= 0.20
        caveats.append("low_inclination")
    if row["distance_frac_error"] > 0.20:
        score -= 0.15
        caveats.append("large_distance_error")
    if row["inclination_error_deg"] > 10:
        score -= 0.10
        caveats.append("large_inclination_error")
    if row["formula_family"] == "K_thick_flared":
        score -= 0.10
        caveats.append("vertical_geometry_proxy_only")
    if row["formula_family"] in {"K_scale_tail_spiral", "K_exponential_disk"} and row["mean_log_sbdisk"] != row["mean_log_sbdisk"]:
        score -= 0.15
        caveats.append("missing_surface_brightness_proxy")
    score = max(0.05, min(1.0, score))
    return score, ";".join(caveats) if caveats else "none"


def build_manifest(points: pd.DataFrame, meta: pd.DataFrame) -> pd.DataFrame:
    stats = (
        points.groupby("galaxy")
        .agg(
            n_points=("r", "size"),
            r_min=("r", "min"),
            r_median=("r", "median"),
            r_max=("r", "max"),
            mean_gas=("total_gas_fraction", "mean"),
            mean_bulge=("bulge_frac", "mean"),
            max_bulge=("bulge_frac", "max"),
            mean_log_sbdisk=("log_sbdisk", "mean"),
            peak_log_sb=("log_sb_peak", "max"),
        )
        .reset_index()
    )
    manifest = stats.merge(
        meta[
            [
                "galaxy",
                "split",
                "role",
                "hub_type",
                "type_bin",
                "inc_bin",
                "distance_quality",
                "distance_frac_error",
                "inclination_deg",
                "inclination_error_deg",
            ]
        ],
        on="galaxy",
        how="left",
    )
    manifest["formula_family"] = manifest.apply(assign_family, axis=1)

    safe_median = manifest["r_median"].clip(lower=1.0e-6)
    safe_max = manifest["r_max"].clip(lower=safe_median + 1.0e-6)
    gas = manifest["mean_gas"].clip(lower=0.0)
    bulge = manifest["mean_bulge"].clip(lower=0.0)

    manifest["scale_radius_proxy_kpc"] = safe_median / 1.678
    manifest["tail_inner_radius_proxy_kpc"] = safe_median * 0.35
    manifest["tail_cutoff_radius_proxy_kpc"] = safe_max * (1.0 + 0.5 * gas)
    manifest["compact_support_radius_proxy_kpc"] = safe_median * (1.0 + bulge)
    manifest["thickness_h_over_rs_proxy"] = (0.08 + 0.45 * gas).clip(lower=0.05, upper=0.75)
    manifest["ring_radius_proxy_kpc"] = pd.NA
    manifest["ring_width_proxy_kpc"] = pd.NA
    manifest["bar_m2_proxy"] = pd.NA
    manifest["lopsided_m1_proxy"] = pd.NA
    manifest["amplitude_policy"] = "train_only_family_amplitude_preflight"
    manifest["parameter_source"] = (
        "available_data_proxy:r_median+r_max+type_bin+bulge_frac+gas_fraction+surface_brightness"
    )
    manifest["forbidden_inputs"] = "vobs_endpoint_residual_gain;required_S_tau;posthoc_family_choice"

    conf = manifest.apply(confidence, axis=1)
    manifest["manifest_confidence"] = [item[0] for item in conf]
    manifest["manifest_caveat"] = [item[1] for item in conf]
    columns = [
        "galaxy",
        "split",
        "role",
        "formula_family",
        "manifest_confidence",
        "manifest_caveat",
        "hub_type",
        "type_bin",
        "inc_bin",
        "distance_quality",
        "distance_frac_error",
        "inclination_deg",
        "inclination_error_deg",
        "n_points",
        "r_min",
        "r_median",
        "r_max",
        "mean_gas",
        "mean_bulge",
        "max_bulge",
        "mean_log_sbdisk",
        "peak_log_sb",
        "scale_radius_proxy_kpc",
        "tail_inner_radius_proxy_kpc",
        "tail_cutoff_radius_proxy_kpc",
        "compact_support_radius_proxy_kpc",
        "thickness_h_over_rs_proxy",
        "ring_radius_proxy_kpc",
        "ring_width_proxy_kpc",
        "bar_m2_proxy",
        "lopsided_m1_proxy",
        "amplitude_policy",
        "parameter_source",
        "forbidden_inputs",
    ]
    return manifest[columns].sort_values(["split", "galaxy"])


def write_report(manifest: pd.DataFrame) -> None:
    family_counts = (
        manifest.groupby(["split", "formula_family"])
        .size()
        .reset_index(name="n_galaxies")
        .sort_values(["split", "formula_family"])
    )
    confidence_summary = (
        manifest.groupby(["split", "formula_family"])
        .agg(
            n_galaxies=("galaxy", "count"),
            mean_confidence=("manifest_confidence", "mean"),
            median_confidence=("manifest_confidence", "median"),
        )
        .reset_index()
        .sort_values(["split", "formula_family"])
    )

    def markdown_table(df: pd.DataFrame) -> str:
        display = df.copy()
        for col in display.columns:
            if pd.api.types.is_float_dtype(display[col]):
                display[col] = display[col].map(lambda x: f"{x:.6g}")
            else:
                display[col] = display[col].astype(str)
        lines = [
            "| " + " | ".join(display.columns) + " |",
            "| " + " | ".join(["---"] * len(display.columns)) + " |",
        ]
        for _, row in display.iterrows():
            lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
        return "\n".join(lines)

    lines = [
        "# Morphology Parameter Manifest",
        "",
        "This manifest freezes the currently available residual-blind morphology",
        "parameters for Paper 8 preflights. It is an available-data proxy manifest,",
        "not the final hand-curated source-native morphology catalog.",
        "",
        "## Outputs",
        "",
        "- `data/derived/morphology_parameter_manifest.csv`",
        "- `data/derived/morphology_parameter_manifest_family_counts.csv`",
        "- `data/derived/morphology_parameter_manifest_confidence_summary.csv`",
        "",
        "## Family Counts",
        "",
        markdown_table(family_counts),
        "",
        "## Confidence Summary",
        "",
        markdown_table(confidence_summary),
        "",
        "## Claim Boundary",
        "",
        "The manifest does not use endpoint residual gains, required S_tau, or",
        "post-hoc family choice. Its weak point is that scale/cutoff/thickness",
        "parameters are still proxies extracted from available 1D data and metadata.",
    ]
    (REPORTS / "morphology_parameter_manifest.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    family_counts.to_csv(DATA / "morphology_parameter_manifest_family_counts.csv", index=False)
    confidence_summary.to_csv(DATA / "morphology_parameter_manifest_confidence_summary.csv", index=False)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points, meta = load_inputs()
    manifest = build_manifest(points, meta)
    manifest.to_csv(DATA / "morphology_parameter_manifest.csv", index=False)
    write_report(manifest)
    print("PAPER8_MORPHOLOGY_PARAMETER_MANIFEST_COMPLETE")


if __name__ == "__main__":
    main()
