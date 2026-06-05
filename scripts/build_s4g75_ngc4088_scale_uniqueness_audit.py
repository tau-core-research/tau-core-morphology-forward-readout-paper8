#!/usr/bin/env python3
"""Audit scale uniqueness for the NGC4088 warp/asymmetry readout candidate.

This is not an endpoint comparison.  It enumerates residual-blind,
dimensionally valid delta-v-squared scale carriers so the theory can see
whether the current x_w Vflat^2 choice is unique or still a convention.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import run_source_native_readout_formula_endpoint as src


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_scale_uniqueness_audit_not_endpoint"


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


def build_audit() -> tuple[pd.DataFrame, pd.DataFrame]:
    points, _labels = src.load_points()
    ngc = points.loc[points["galaxy"] == GALAXY].copy()
    xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    constants = pd.read_csv(DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_constants.csv")
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    sparc_row = sparc.loc[sparc["Galaxy"] == GALAXY].iloc[0]

    x_w = float(xw["x_warp_onset"])
    vflat2 = float(sparc_row["Vflat_kms"]) ** 2
    median_vn2 = float(np.median(ngc["vn"].to_numpy(dtype=float) ** 2))
    median_vv62 = float(np.median(ngc["v_v6"].to_numpy(dtype=float) ** 2))
    closure_num = np.maximum(
        ngc["v_v6"].to_numpy(dtype=float) ** 2 - ngc["vn"].to_numpy(dtype=float) ** 2,
        0.0,
    )
    closure_fraction = float(np.median(closure_num) / max(median_vv62, 1.0e-12))
    current_prefactor = float(
        constants.loc[
            constants["constant_name"] == "c_warp_candidate", "constant_value"
        ].iloc[0]
    ) * float(
        constants.loc[
            constants["constant_name"] == "velocity_scale_candidate", "constant_value"
        ].iloc[0]
    )

    rows = [
        {
            "scale_id": "CURRENT_XW_VFLAT2",
            "scale_formula": "x_w * Vflat^2",
            "scale_value_km2_s2": x_w * vflat2,
            "source_status": "CURRENT_FORMULA_CONDITIONAL_CANDIDATE",
            "uses_vobs_or_residual": False,
            "selection_status": "SELECTED_CANDIDATE_NOT_UNIQUE",
            "tau_side_obligation": "derive why onset fraction times catalog flat-speed carrier is selected",
        },
        {
            "scale_id": "XW_MEDIAN_VN2",
            "scale_formula": "x_w * median_r(v_n^2)",
            "scale_value_km2_s2": x_w * median_vn2,
            "source_status": "RESIDUAL_BLIND_BARYONIC_SCALE_ALTERNATIVE",
            "uses_vobs_or_residual": False,
            "selection_status": "ALTERNATIVE_NOT_SELECTED",
            "tau_side_obligation": "rule out if flat-speed carrier is required rather than baryonic readout carrier",
        },
        {
            "scale_id": "XW_MEDIAN_VV62",
            "scale_formula": "x_w * median_r(v_v6^2)",
            "scale_value_km2_s2": x_w * median_vv62,
            "source_status": "RESIDUAL_BLIND_TPG_CLOSURE_SCALE_ALTERNATIVE",
            "uses_vobs_or_residual": False,
            "selection_status": "ALTERNATIVE_NOT_SELECTED",
            "tau_side_obligation": "rule out if external TPG-like closure carrier is not allowed as Tau-side normalizer",
        },
        {
            "scale_id": "CLOSURE_FRACTION_MEDIAN_VN2",
            "scale_formula": "c_g * median_r(v_n^2)",
            "scale_value_km2_s2": closure_fraction * median_vn2,
            "source_status": "TAU_SOURCE_NORMALIZATION_RULE_ALTERNATIVE",
            "uses_vobs_or_residual": False,
            "selection_status": "ALTERNATIVE_NOT_SELECTED",
            "tau_side_obligation": "decide whether NGC4088 warp lane must use local closure fraction instead of x_w",
        },
        {
            "scale_id": "XW_CLOSURE_FRACTION_MEDIAN_VN2",
            "scale_formula": "x_w * c_g * median_r(v_n^2)",
            "scale_value_km2_s2": x_w * closure_fraction * median_vn2,
            "source_status": "COMPOSITE_ONSET_CLOSURE_SCALE_ALTERNATIVE",
            "uses_vobs_or_residual": False,
            "selection_status": "ALTERNATIVE_NOT_SELECTED",
            "tau_side_obligation": "derive or reject a two-factor onset-plus-closure carrier",
        },
    ]
    audit = pd.DataFrame(rows)
    audit["galaxy"] = GALAXY
    audit["current_prefactor_ratio"] = audit["scale_value_km2_s2"] / current_prefactor
    audit["endpoint_scores_allowed"] = False
    audit["claim_boundary"] = CLAIM_BOUNDARY
    audit = audit[
        [
            "galaxy",
            "scale_id",
            "scale_formula",
            "scale_value_km2_s2",
            "current_prefactor_ratio",
            "source_status",
            "uses_vobs_or_residual",
            "selection_status",
            "tau_side_obligation",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    dimensionally_valid = audit["scale_value_km2_s2"].gt(0.0).all()
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "n_scale_candidates": len(audit),
                "n_dimensionally_valid": int(audit["scale_value_km2_s2"].gt(0.0).sum()),
                "n_residual_blind": int((~audit["uses_vobs_or_residual"]).sum()),
                "current_scale_id": "CURRENT_XW_VFLAT2",
                "current_prefactor_km2_s2": current_prefactor,
                "scale_uniqueness_decision": (
                    "BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES"
                    if dimensionally_valid and len(audit) > 1
                    else "SCALE_UNIQUENESS_NOT_AUDITED"
                ),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return audit, summary


def write_report(audit: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Scale-Uniqueness Audit",
        "",
        "This audit enumerates residual-blind, dimensionally valid scale carriers",
        "for the NGC4088 warp/asymmetry readout lane. It does not compare any",
        "scale to observed velocities.",
        "",
        "## Verdict",
        "",
        "The current `x_w * Vflat^2` carrier is a valid selected candidate, but it",
        "is not unique at theory level. Several residual-blind alternatives exist,",
        "so `SCALE_UNIQUENESS` remains blocked until a Tau-side principle selects",
        "or rejects them without endpoint residual tuning.",
        "",
        "## Scale Candidates",
        "",
        markdown_table(audit),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "This is a theory audit, not a performance diagnostic. The listed scales",
        "must not be selected by endpoint scores.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_scale_uniqueness_audit.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    audit, summary = build_audit()
    audit.to_csv(DATA / "s4g75_ngc4088_scale_uniqueness_audit.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_scale_uniqueness_summary.csv", index=False)
    write_report(audit, summary)
    print("PAPER8_NGC4088_SCALE_UNIQUENESS_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
