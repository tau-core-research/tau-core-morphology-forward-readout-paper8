#!/usr/bin/env python3
"""Audit source-normalization failure modes by inclusion lane.

This diagnostic compares the source-native hard-family signal to the Tau-side
evidence-measure L2 normalization on the same galaxies.  It does not tune the
normalization rule and does not select an endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "source_normalization_failure_modes_by_lane_not_endpoint"


def classify(row: pd.Series) -> tuple[str, str]:
    tau_weak = (not bool(row["tau_beats_tpg_v6"])) and (not bool(row["tau_beats_mond"]))
    hard_specific = bool(row["hard_beats_wrong_mean"])
    cancellation_ratio = abs(float(row["net_signed_source_strength_v2"])) / max(
        abs(float(row["positive_component_strength_v2"]))
        + abs(float(row["negative_component_strength_v2"])),
        1e-9,
    )
    has_proxy = bool(row["has_proxy_component"])
    projection_caveat = row["allowed_use"] == "support_lane_projection_caveat"
    closure = float(row["closure_fraction_c"])

    if hard_specific and tau_weak and projection_caveat:
        return (
            "PROJECTION_SCALE_NORMALIZATION_FAILURE",
            "family specificity survives, but Tau evidence L2 fails in projection-caveated lane",
        )
    if hard_specific and tau_weak and cancellation_ratio < 0.35:
        return (
            "SIGNED_COMPONENT_CANCELLATION_FAILURE",
            "positive and negative source components strongly cancel",
        )
    if hard_specific and tau_weak and has_proxy:
        return (
            "PROXY_GATE_OR_COMPONENT_WEIGHT_FAILURE",
            "Tau evidence L2 depends on proxy/partial components in a weak baseline case",
        )
    if hard_specific and tau_weak and (closure < 0.25 or closure > 0.85):
        return (
            "CLOSURE_FRACTION_SCALE_FAILURE",
            "closure fraction is near an extreme in a weak baseline case",
        )
    if hard_specific and not tau_weak:
        return (
            "SPECIFICITY_AND_BASELINE_PARTLY_TRANSFER",
            "family specificity partly transfers to baseline comparison",
        )
    if not hard_specific and tau_weak:
        return (
            "NO_SPECIFICITY_AND_BASELINE_WEAK",
            "both family specificity and Tau evidence baseline comparison are weak",
        )
    return (
        "OTHER_NORMALIZATION_DIAGNOSTIC",
        "mixed normalization behavior",
    )


def build_audit() -> tuple[pd.DataFrame, pd.DataFrame]:
    lanes = pd.read_csv(DATA / "inclusion_lane_expansion_audit.csv")
    hard = pd.read_csv(DATA / "source_native_readout_formula_scores_by_galaxy.csv")
    tau = pd.read_csv(DATA / "tau_side_evidence_measure_l2_endpoint_scores.csv")
    galaxy_rule = pd.read_csv(DATA / "tau_side_evidence_measure_l2_galaxy_rule.csv")
    components = pd.read_csv(DATA / "tau_side_evidence_measure_l2_component_rule.csv")

    proxy_by_galaxy = (
        components.groupby("galaxy")
        .agg(
            has_proxy_component=("e_tau_status", lambda values: bool((values == "E_TAU_PROXY_PRODUCT_CANDIDATE").any())),
            n_proxy_components=("e_tau_status", lambda values: int((values == "E_TAU_PROXY_PRODUCT_CANDIDATE").sum())),
            median_e_tau_gate=("e_tau_gate", "median"),
        )
        .reset_index()
    )

    table = lanes.merge(
        hard[
            [
                "galaxy",
                "split",
                "matched_beats_wrong_mean",
                "matched_minus_wrong_mean",
                "matched_beats_tpg_v6",
                "matched_beats_mond",
                "matched_minus_tpg_v6",
                "matched_minus_mond",
            ]
        ],
        on=["galaxy", "split"],
        how="left",
        validate="one_to_one",
    ).merge(
        tau[
            [
                "galaxy",
                "source_norm_beats_tpg_v6",
                "source_norm_beats_mond",
                "source_norm_minus_tpg_v6",
                "source_norm_minus_mond",
            ]
        ],
        on="galaxy",
        how="left",
        validate="one_to_one",
    ).merge(
        galaxy_rule[
            [
                "galaxy",
                "closure_fraction_c",
                "net_signed_source_strength_v2",
                "positive_component_strength_v2",
                "negative_component_strength_v2",
            ]
        ],
        on="galaxy",
        how="left",
        validate="one_to_one",
    ).merge(proxy_by_galaxy, on="galaxy", how="left", validate="one_to_one")

    rows = []
    for _, row in table.iterrows():
        status, reason = classify(
            pd.Series(
                {
                    **row.to_dict(),
                    "hard_beats_wrong_mean": row["matched_beats_wrong_mean"],
                    "tau_beats_tpg_v6": row["source_norm_beats_tpg_v6"],
                    "tau_beats_mond": row["source_norm_beats_mond"],
                }
            )
        )
        denom = abs(float(row["positive_component_strength_v2"])) + abs(
            float(row["negative_component_strength_v2"])
        )
        rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "formula_family": row["formula_family"],
                "inclusion_lane": row["inclusion_lane"],
                "allowed_use": row["allowed_use"],
                "hard_beats_wrong_mean": bool(row["matched_beats_wrong_mean"]),
                "hard_minus_wrong_mean": row["matched_minus_wrong_mean"],
                "tau_beats_tpg_v6": bool(row["source_norm_beats_tpg_v6"]),
                "tau_beats_mond": bool(row["source_norm_beats_mond"]),
                "tau_minus_tpg_v6": row["source_norm_minus_tpg_v6"],
                "tau_minus_mond": row["source_norm_minus_mond"],
                "closure_fraction_c": row["closure_fraction_c"],
                "net_signed_source_strength_v2": row["net_signed_source_strength_v2"],
                "positive_component_strength_v2": row["positive_component_strength_v2"],
                "negative_component_strength_v2": row["negative_component_strength_v2"],
                "signed_cancellation_ratio": abs(float(row["net_signed_source_strength_v2"]))
                / max(denom, 1e-9),
                "has_proxy_component": bool(row["has_proxy_component"]),
                "n_proxy_components": int(row["n_proxy_components"]),
                "median_e_tau_gate": row["median_e_tau_gate"],
                "failure_mode": status,
                "failure_reason": reason,
                "endpoint_scores_computed": False,
                "uses_vobs_or_residual_for_classification": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    audit = pd.DataFrame(rows).sort_values(["split", "inclusion_lane", "failure_mode", "galaxy"])
    summary = summarize(audit)
    return audit, summary


def summarize(audit: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (split, lane, allowed_use, failure_mode), sub in audit.groupby(
        ["split", "inclusion_lane", "allowed_use", "failure_mode"]
    ):
        rows.append(
            {
                "split": split,
                "inclusion_lane": lane,
                "allowed_use": allowed_use,
                "failure_mode": failure_mode,
                "n_galaxies": int(len(sub)),
                "hard_beats_wrong_fraction": float(sub["hard_beats_wrong_mean"].mean()),
                "tau_beats_tpg_v6_fraction": float(sub["tau_beats_tpg_v6"].mean()),
                "tau_beats_mond_fraction": float(sub["tau_beats_mond"].mean()),
                "median_tau_minus_tpg_v6": float(sub["tau_minus_tpg_v6"].median()),
                "median_tau_minus_mond": float(sub["tau_minus_mond"].median()),
                "median_signed_cancellation_ratio": float(sub["signed_cancellation_ratio"].median()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows).sort_values(["split", "inclusion_lane", "allowed_use", "failure_mode"])


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


def write_report(audit: pd.DataFrame, summary: pd.DataFrame) -> None:
    holdout_projection = summary.loc[
        (summary["split"] == "holdout")
        & (summary["allowed_use"] == "support_lane_projection_caveat")
    ]
    lines = [
        "# Source-Normalization Failure Modes By Lane",
        "",
        "This diagnostic compares morphology-family specificity with Tau evidence",
        "L2 baseline behavior. It does not tune the normalization rule and does",
        "not select an endpoint.",
        "",
        "## Holdout Projection-Caveat Failure Modes",
        "",
        markdown_table(holdout_projection),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "Failure mode labels are diagnostic. They do not use endpoint residuals to",
        "change any gate, family, sign, or normalization constant.",
    ]
    (REPORTS / "source_normalization_failure_modes_by_lane.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    audit, summary = build_audit()
    audit.to_csv(DATA / "source_normalization_failure_modes_by_lane.csv", index=False)
    summary.to_csv(DATA / "source_normalization_failure_modes_by_lane_summary.csv", index=False)
    write_report(audit, summary)
    print("PAPER8_SOURCE_NORMALIZATION_FAILURE_MODES_BY_LANE_COMPLETE")


if __name__ == "__main__":
    main()
