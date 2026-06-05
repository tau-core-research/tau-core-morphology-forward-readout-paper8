#!/usr/bin/env python3
"""Build residual-blind L2 readout-weight intake candidates.

This script converts the all-sample source-expansion layer into candidate
readout-component weights.  It is deliberately upstream of endpoint scoring:
the weights are not accepted Tau-side states, not promoted labels, and not fit
from rotation residuals.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "l2_weight_intake_candidate_not_endpoint_not_accepted_state"
FAMILIES = [
    "K_compact_finite",
    "K_scale_tail_spiral",
    "K_exponential_disk",
    "K_thick_flared",
]


def scale01(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)
    if values.notna().sum() == 0:
        return pd.Series(0.0, index=series.index)
    lo = float(values.quantile(0.10))
    hi = float(values.quantile(0.90))
    if hi <= lo:
        return pd.Series(0.0, index=series.index)
    return ((values.fillna(lo) - lo) / (hi - lo)).clip(0.0, 1.0)


def load_inputs() -> pd.DataFrame:
    expansion = pd.read_csv(DATA / "morphology_information_gain_source_expansion.csv")
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    s4g = pd.read_csv(DATA / "external_s4g_sparc_observable_candidates.csv")
    keep = [
        "galaxy",
        "manifest_confidence",
        "manifest_caveat",
        "inclination_deg",
        "mean_bulge",
        "max_bulge",
        "mean_gas",
        "mean_log_sbdisk",
        "scale_radius_proxy_kpc",
        "thickness_h_over_rs_proxy",
    ]
    out = expansion.merge(manifest[keep], on="galaxy", how="left", validate="one_to_one")
    out = out.merge(
        s4g[["galaxy", "scale_radius_kpc", "bar_radius_kpc", "s4g_model_components"]],
        on="galaxy",
        how="left",
        validate="one_to_one",
    )
    return out


def add_raw_signals(table: pd.DataFrame) -> pd.DataFrame:
    out = table.copy()
    rhi_strength = scale01(np.log1p(out["sparc_rhi_kpc"].clip(lower=0.0)))
    mhi_strength = scale01(np.log1p(out["sparc_mhi_1e9_msun"].clip(lower=0.0)))
    scale_strength = scale01(np.log1p(out["scale_radius_kpc"].fillna(out["scale_radius_proxy_kpc"])))
    bulge_strength = scale01(0.6 * out["mean_bulge"].fillna(0.0) + 0.4 * out["max_bulge"].fillna(0.0))
    thickness_strength = scale01(out["thickness_h_over_rs_proxy"].fillna(0.0))

    out["signal_K_scale_tail_spiral"] = np.where(
        out["q_tail_candidate"].astype(bool),
        0.25 + 0.35 * rhi_strength + 0.25 * mhi_strength + 0.15 * out["dustpedia_hi_match"].astype(float),
        0.0,
    )
    out["signal_K_exponential_disk"] = np.where(
        out["q_expdisk_scale_candidate"].astype(bool),
        0.55 + 0.25 * scale_strength + 0.20 * out["dustpedia_dust_profile_match"].astype(float),
        0.0,
    )
    out["signal_K_compact_finite"] = np.where(
        out["q_compact_candidate"].astype(bool),
        0.35
        + 0.35 * out["s4g_compact_component_ready"].astype(float)
        + 0.20 * out["dustpedia_physical_match"].astype(float)
        + 0.10 * bulge_strength,
        0.0,
    )
    out["signal_K_thick_flared"] = np.where(
        (out["thickness_h_over_rs_proxy"].fillna(0.0) >= 0.20)
        | (out["inclination_deg"].fillna(0.0) >= 70.0),
        0.20 + 0.35 * thickness_strength + 0.10 * (out["inclination_deg"].fillna(0.0) >= 70.0),
        0.0,
    )
    return out


def normalize_rows(table: pd.DataFrame) -> pd.DataFrame:
    rows = []
    signal_cols = {family: f"signal_{family}" for family in FAMILIES}
    for _, row in table.iterrows():
        signals = {family: max(float(row[col]), 0.0) for family, col in signal_cols.items()}
        total = sum(signals.values())
        if total > 0.0:
            weights = {family: value / total for family, value in signals.items()}
            status = "SOURCE_INFORMATIVE_WEIGHT_CANDIDATE"
        else:
            weights = {family: 1.0 / len(FAMILIES) for family in FAMILIES}
            status = "UNINFORMATIVE_EQUAL_FALLBACK"

        nonzero = [family for family, value in signals.items() if value > 0.0]
        dominant = max(FAMILIES, key=lambda family: weights[family])
        entropy = -sum(value * np.log(value) for value in weights.values() if value > 0.0)
        effective_components = float(np.exp(entropy))
        rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "coarse_formula_family": row["formula_family"],
                "weight_intake_status": status,
                "dominant_intake_family": dominant,
                "n_nonzero_source_components": len(nonzero),
                "nonzero_source_components": ";".join(nonzero),
                "weight_entropy": entropy,
                "effective_component_count": effective_components,
                "uses_endpoint_residuals": False,
                "accepted_label_output_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "thick_flared_weight_is_proxy_only": bool(row["signal_K_thick_flared"] > 0.0),
            }
            | {f"raw_{family}": signals[family] for family in FAMILIES}
            | {f"w_{family}": weights[family] for family in FAMILIES}
        )
    return pd.DataFrame(rows).sort_values(["split", "galaxy"])


def summarize(candidates: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split, sub in candidates.groupby("split", dropna=False):
        row = {
            "split": split,
            "n_galaxies": int(len(sub)),
            "source_informative_count": int(
                sub["weight_intake_status"].eq("SOURCE_INFORMATIVE_WEIGHT_CANDIDATE").sum()
            ),
            "uninformative_fallback_count": int(
                sub["weight_intake_status"].eq("UNINFORMATIVE_EQUAL_FALLBACK").sum()
            ),
            "mean_effective_component_count": float(sub["effective_component_count"].mean()),
            "median_effective_component_count": float(sub["effective_component_count"].median()),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for family in FAMILIES:
            row[f"dominant_{family}_count"] = int(sub["dominant_intake_family"].eq(family).sum())
            row[f"nonzero_{family}_count"] = int(sub[f"raw_{family}"].gt(0.0).sum())
            row[f"mean_w_{family}"] = float(sub[f"w_{family}"].mean())
        rows.append(row)
    return pd.DataFrame(rows).sort_values("split")


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda value: f"{value:.6g}")
        else:
            display[col] = display[col].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def write_report(candidates: pd.DataFrame, summary: pd.DataFrame) -> None:
    full = summary.loc[summary["split"] == "all"].iloc[0] if "all" in set(summary["split"]) else None
    lines = [
        "# L2 Readout-Weight Intake Candidates",
        "",
        "This preflight converts residual-blind source coverage into candidate",
        "readout-component weights for the morphology-information-gain path.",
        "It is an intake layer only: it does not create accepted labels, does not",
        "score rotation curves, and does not use endpoint residuals.",
        "",
        "## Full-Sample Verdict",
        "",
    ]
    if full is not None:
        lines.extend(
            [
                f"- Galaxies: {int(full['n_galaxies'])}",
                f"- Source-informative candidates: {int(full['source_informative_count'])}",
                f"- Uninformative fallbacks: {int(full['uninformative_fallback_count'])}",
                f"- Mean effective component count: {full['mean_effective_component_count']:.3f}",
                f"- Tail nonzero count: {int(full['nonzero_K_scale_tail_spiral_count'])}",
                f"- Exponential-disk nonzero count: {int(full['nonzero_K_exponential_disk_count'])}",
                f"- Compact nonzero count: {int(full['nonzero_K_compact_finite_count'])}",
                f"- Thick/flared nonzero count: {int(full['nonzero_K_thick_flared_count'])}",
                "",
            ]
        )
    lines.extend(
        [
            "## Summary",
            "",
            markdown_table(summary),
            "",
            "## Dominant Candidate Families",
            "",
            markdown_table(
                candidates.groupby(["split", "dominant_intake_family"])
                .size()
                .reset_index(name="n_galaxies")
            ),
            "",
            "## Claim Boundary",
            "",
            "These are weight-intake candidates, not accepted Tau-side readout",
            "states. The tail, exponential-disk, compact, and thick/flared signals",
            "come from currently available residual-blind source coverage and",
            "present-day morphology proxies. The thick/flared channel remains",
            "especially proxy-like because no dedicated source-native thickness",
            "or velocity-field layer is assembled here.",
            "Endpoint use requires a separate freeze-and-audit step.",
        ]
    )
    (REPORTS / "morphology_information_gain_l2_weight_intake.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    table = add_raw_signals(load_inputs())
    candidates = normalize_rows(table)
    all_summary = summarize(candidates.assign(split="all"))
    split_summary = summarize(candidates)
    summary = pd.concat([all_summary, split_summary], ignore_index=True)
    candidates.to_csv(DATA / "morphology_information_gain_l2_weight_intake_candidates.csv", index=False)
    summary.to_csv(DATA / "morphology_information_gain_l2_weight_intake_summary.csv", index=False)
    write_report(candidates, summary)
    print("PAPER8_L2_WEIGHT_INTAKE_CANDIDATES_COMPLETE")


if __name__ == "__main__":
    main()
