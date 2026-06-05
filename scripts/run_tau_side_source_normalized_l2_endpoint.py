#!/usr/bin/env python3
"""Run a residual-blind Tau-side source-normalized L2 endpoint preflight.

The normalization rule is source-side only:

    normalized_shape_gK(r) = kernel_gK(r) / median_r |kernel_gK(r)|
    c_g = median_r max(v_v6^2 - v_n^2, 0) / median_r v_v6^2
    delta v_gK^2(r) = sigma_K * e_gK * w_gK * c_g * median_r(v_n^2)
                      * normalized_shape_gK(r)

where w_gK are residual-blind L2 intake weights, e_gK are residual-blind
source-evidence gates, and sigma_K is a predeclared readout-orientation sign.

No vobs, endpoint residual, required S_tau, best-family choice, or holdout
selection enters the normalization.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import run_source_native_readout_formula_endpoint as source_native


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FAMILIES = source_native.FORMULA_FAMILIES
CLAIM_BOUNDARY = "tau_side_source_normalization_formula_conditional_not_validation"
DERIVATION_CONSTANTS_PATH = DATA / "tau_side_source_normalization_derivation_constants.csv"


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    points, _ = source_native.load_points()
    points = source_native.add_bridge_formula_kernels(points)
    weights = pd.read_csv(DATA / "morphology_information_gain_l2_weight_intake_candidates.csv")
    component_audit = pd.read_csv(
        DATA / "morphology_information_gain_l2_weight_freeze_component_audit.csv"
    )
    return points, weights, component_audit


def load_normalization_constants() -> tuple[dict[str, float], dict[str, float], dict[str, str]]:
    if not DERIVATION_CONSTANTS_PATH.exists():
        raise FileNotFoundError(
            "Missing tau_side_source_normalization_derivation_constants.csv; "
            "run scripts/build_tau_side_source_normalization_derivation_audit.py first."
        )
    constants = pd.read_csv(DERIVATION_CONSTANTS_PATH)
    orientation_rows = constants.loc[constants["constant_type"] == "orientation_sign"]
    gate_rows = constants.loc[constants["constant_type"] == "evidence_gate"]
    orientation_sign = {
        row["constant_key"]: float(row["constant_value"]) for _, row in orientation_rows.iterrows()
    }
    evidence_gate = {
        row["constant_key"]: float(row["constant_value"]) for _, row in gate_rows.iterrows()
    }
    proof_status = {
        row["constant_key"]: row["proof_status"] for _, row in constants.iterrows()
    }
    missing_families = sorted(set(FAMILIES) - set(orientation_sign))
    required_gates = {
        "SOURCE_CANDIDATE_COMPACT_READY",
        "SOURCE_CANDIDATE_HI_TAIL_READY",
        "SOURCE_CANDIDATE_S4G_SCALE_READY",
        "SOURCE_CANDIDATE_VELOCITY_FIELD_READY",
        "PROXY_OR_PARTIAL_SOURCE_ONLY",
        "MISSING_SOURCE_SUPPORT",
    }
    missing_gates = sorted(required_gates - set(evidence_gate))
    if missing_families or missing_gates:
        raise ValueError(
            "Incomplete source-normalization derivation constants: "
            f"missing_families={missing_families}, missing_gates={missing_gates}"
        )
    return orientation_sign, evidence_gate, proof_status


def kernel_scale(values: pd.Series) -> float:
    clean = values.abs().replace([np.inf, -np.inf], np.nan).dropna()
    if clean.empty:
        return 1.0
    scale = float(clean.median())
    return scale if scale > 1.0e-12 else 1.0


def source_scales(points: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for galaxy, sub in points.groupby("galaxy"):
        vn2 = sub["vn"].pow(2)
        vv62 = sub["v_v6"].pow(2).clip(lower=1.0e-12)
        closure_num = np.maximum(vv62.to_numpy() - vn2.to_numpy(), 0.0)
        closure_fraction = float(np.median(closure_num) / np.median(vv62))
        row = {
            "galaxy": galaxy,
            "source_vn2_median": float(vn2.median()),
            "closure_fraction_c": float(np.clip(closure_fraction, 0.0, 1.0)),
        }
        for family in FAMILIES:
            row[f"kernel_scale_{family}"] = kernel_scale(sub[f"kernel_{family}"])
        rows.append(row)
    return pd.DataFrame(rows)


def component_evidence_map(component_audit: pd.DataFrame) -> dict[tuple[str, str], str]:
    return {
        (row["galaxy"], row["component_family"]): row["component_evidence_status"]
        for _, row in component_audit.iterrows()
    }


def build_component_rule(
    weights: pd.DataFrame, scales: pd.DataFrame, component_audit: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    orientation_sign, evidence_gate, proof_status = load_normalization_constants()
    evidence = component_evidence_map(component_audit)
    table = weights.merge(scales, on="galaxy", how="left", validate="one_to_one")
    component_rows = []
    galaxy_rows = []
    for _, row in table.iterrows():
        active_strengths = {}
        for family in FAMILIES:
            status = evidence.get((row["galaxy"], family), "MISSING_SOURCE_SUPPORT")
            gate = evidence_gate.get(status, evidence_gate["MISSING_SOURCE_SUPPORT"])
            weight = float(row[f"w_{family}"])
            signed_strength = (
                orientation_sign[family]
                * gate
                * weight
                * float(row["closure_fraction_c"])
                * float(row["source_vn2_median"])
            )
            beta = signed_strength / float(row[f"kernel_scale_{family}"])
            active_strengths[family] = signed_strength
            component_rows.append(
                {
                    "galaxy": row["galaxy"],
                    "split": row["split"],
                    "component_family": family,
                    "intake_weight": weight,
                    "component_evidence_status": status,
                    "evidence_gate": gate,
                    "orientation_sign": orientation_sign[family],
                    "orientation_sign_proof_status": proof_status[family],
                    "evidence_gate_proof_status": proof_status.get(
                        status, proof_status["MISSING_SOURCE_SUPPORT"]
                    ),
                    "closure_fraction_c": float(row["closure_fraction_c"]),
                    "source_vn2_median": float(row["source_vn2_median"]),
                    "kernel_scale": float(row[f"kernel_scale_{family}"]),
                    "signed_source_strength_v2": signed_strength,
                    "beta_source_normalized": beta,
                    "uses_vobs_or_residual": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        galaxy_rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "dominant_intake_family": row["dominant_intake_family"],
                "closure_fraction_c": float(row["closure_fraction_c"]),
                "source_vn2_median": float(row["source_vn2_median"]),
                "net_signed_source_strength_v2": float(sum(active_strengths.values())),
                "positive_component_strength_v2": float(
                    sum(value for value in active_strengths.values() if value > 0.0)
                ),
                "negative_component_strength_v2": float(
                    sum(value for value in active_strengths.values() if value < 0.0)
                ),
                "normalization_rule_status": "THEORY_CONDITIONAL_RESIDUAL_BLIND_SOURCE_RULE",
                "endpoint_freeze_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(component_rows), pd.DataFrame(galaxy_rows)


def add_predictions(points: pd.DataFrame, component_rule: pd.DataFrame) -> pd.DataFrame:
    beta = {
        (row["galaxy"], row["component_family"]): float(row["beta_source_normalized"])
        for _, row in component_rule.iterrows()
    }
    out = points.copy()
    delta_v2 = np.zeros(len(out), dtype=float)
    for idx, row in out.iterrows():
        galaxy = row["galaxy"]
        total = 0.0
        for family in FAMILIES:
            total += beta.get((galaxy, family), 0.0) * float(row[f"kernel_{family}"])
        delta_v2[idx] = total
    out["delta_v2_tau_source_normalized_l2"] = delta_v2
    out["v_tau_source_normalized_l2"] = np.sqrt(
        np.maximum(out["v_v6"].pow(2).to_numpy() + delta_v2, 0.0)
    )
    return out


def rmse(df: pd.DataFrame, pred_col: str) -> float:
    return float(((df[pred_col] - df["vobs"]).pow(2).mean()) ** 0.5)


def score(scored: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    old = pd.read_csv(DATA / "morphology_information_gain_l2_weight_intake_endpoint_scores.csv")[
        ["galaxy", "rmse_l2_weight_intake"]
    ]
    for galaxy, sub in scored.groupby("galaxy"):
        rows.append(
            {
                "galaxy": galaxy,
                "split": sub["split"].iloc[0],
                "n_points": int(len(sub)),
                "rmse_tau_source_normalized_l2": rmse(sub, "v_tau_source_normalized_l2"),
                "rmse_tpg_v6": rmse(sub, "v_v6"),
                "rmse_mond": rmse(sub, "v_mond"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    scores = pd.DataFrame(rows).merge(old, on="galaxy", how="left", validate="one_to_one")
    scores["source_norm_minus_old_l2_intake"] = (
        scores["rmse_tau_source_normalized_l2"] - scores["rmse_l2_weight_intake"]
    )
    scores["source_norm_minus_tpg_v6"] = scores["rmse_tau_source_normalized_l2"] - scores["rmse_tpg_v6"]
    scores["source_norm_minus_mond"] = scores["rmse_tau_source_normalized_l2"] - scores["rmse_mond"]
    scores["source_norm_beats_old_l2_intake"] = scores["source_norm_minus_old_l2_intake"] < 0
    scores["source_norm_beats_tpg_v6"] = scores["source_norm_minus_tpg_v6"] < 0
    scores["source_norm_beats_mond"] = scores["source_norm_minus_mond"] < 0

    summary_rows = []
    for split, sub in scores.groupby("split"):
        summary_rows.append(
            {
                "split": split,
                "n_galaxies": int(len(sub)),
                "median_rmse_tau_source_normalized_l2": float(
                    sub["rmse_tau_source_normalized_l2"].median()
                ),
                "beats_old_l2_intake_fraction": float(
                    sub["source_norm_beats_old_l2_intake"].mean()
                ),
                "beats_tpg_v6_fraction": float(sub["source_norm_beats_tpg_v6"].mean()),
                "beats_mond_fraction": float(sub["source_norm_beats_mond"].mean()),
                "median_source_norm_minus_old_l2_intake": float(
                    sub["source_norm_minus_old_l2_intake"].median()
                ),
                "median_source_norm_minus_tpg_v6": float(
                    sub["source_norm_minus_tpg_v6"].median()
                ),
                "median_source_norm_minus_mond": float(sub["source_norm_minus_mond"].median()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return scores.sort_values(["split", "galaxy"]), pd.DataFrame(summary_rows).sort_values("split")


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


def write_report(summary: pd.DataFrame, galaxy_rule: pd.DataFrame) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    lines = [
        "# Tau-Side Source-Normalized L2 Endpoint Preflight",
        "",
        "This run implements a residual-blind, theory-conditional Tau-side",
        "source-normalization rule. It uses no observed velocity endpoint, no",
        "rotation residual, no required-S_tau diagnostic, and no best-family",
        "selection. It is not yet an accepted physical normalization law.",
        "This is not an accepted physical normalization law.",
        "",
        "## Normalization Rule",
        "",
        "```text",
        "normalized_shape_gK(r) = kernel_gK(r) / median_r |kernel_gK(r)|",
        "c_g = median_r max(v_v6^2 - v_n^2, 0) / median_r v_v6^2",
        "delta v_gK^2(r) = sigma_K e_gK w_gK c_g median_r(v_n^2) normalized_shape_gK(r)",
        "```",
        "",
        "The signs are predeclared: compact/tail positive, exponential/thick",
        "negative. These signs and evidence gates are loaded from the",
        "Tau-side source-normalization derivation manifest, not selected from",
        "endpoint residuals. The manifest marks the orientation signs as",
        "theory-conditional bridge derivations and the proxy attenuation as the",
        "coarse executable representative of the conservative Tau-side",
        "readout-admission product, not an empirical fit.",
        "",
        "## Holdout Verdict",
        "",
        f"- Holdout galaxies: {int(holdout['n_galaxies'])}",
        f"- Beats old L2 intake endpoint: {holdout['beats_old_l2_intake_fraction']:.3f}",
        f"- Beats TPG/v6: {holdout['beats_tpg_v6_fraction']:.3f}",
        f"- Beats MOND: {holdout['beats_mond_fraction']:.3f}",
        f"- Median source-normalized-minus-old-L2 RMSE: {holdout['median_source_norm_minus_old_l2_intake']:.6g}",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Rule Scale Summary",
        "",
        markdown_table(
            galaxy_rule.groupby("split")
            .agg(
                n_galaxies=("galaxy", "count"),
                median_closure_fraction=("closure_fraction_c", "median"),
                median_source_vn2=("source_vn2_median", "median"),
                median_net_signed_strength=("net_signed_source_strength_v2", "median"),
            )
            .reset_index()
        ),
        "",
        "## Claim Boundary",
        "",
        "This is a theory-conditional source-normalization candidate. A positive",
        "or negative endpoint result here is not validation. The weakest step is",
        "source-native promotion of the orientation signs plus accepted",
        "per-galaxy evidence assignments before endpoint freeze.",
    ]
    (REPORTS / "tau_side_source_normalized_l2_endpoint.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points, weights, component_audit = load_inputs()
    scales = source_scales(points)
    component_rule, galaxy_rule = build_component_rule(weights, scales, component_audit)
    scored = add_predictions(points, component_rule)
    scores, summary = score(scored)

    component_rule.to_csv(DATA / "tau_side_source_normalization_component_rule.csv", index=False)
    galaxy_rule.to_csv(DATA / "tau_side_source_normalization_galaxy_rule.csv", index=False)
    scores.to_csv(DATA / "tau_side_source_normalized_l2_endpoint_scores.csv", index=False)
    summary.to_csv(DATA / "tau_side_source_normalized_l2_endpoint_summary.csv", index=False)
    write_report(summary, galaxy_rule)
    print("PAPER8_TAU_SIDE_SOURCE_NORMALIZED_L2_ENDPOINT_COMPLETE")


if __name__ == "__main__":
    main()
