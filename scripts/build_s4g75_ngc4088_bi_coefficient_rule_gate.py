#!/usr/bin/env python3
"""Build the NGC4088 B_i coefficient-rule gate for epsilon_cross.

The epsilon_cross source-bound protocol needs dimensionless B_i coefficients.
This gate fixes the residual-blind feature normalization side of the rule and
uses the sharp residual-blind coefficient protocol when present, otherwise
falling back to the conservative unit-bound freeze.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_bi_coefficient_rule_gate_not_endpoint"


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


def clipped(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def build_gate() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    response = pd.read_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_response_template.csv"
    ).iloc[0]
    validation = pd.read_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_response_validation.csv"
    ).iloc[0]
    xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    q_first_pass_path = DATA / "s4g75_ngc4088_qwarp_first_pass_response.csv"
    memory_first_pass_path = DATA / "s4g75_ngc4088_memory_history_first_pass_response.csv"
    source_review_path = DATA / "s4g75_ngc4088_source_response_independent_review.csv"
    frozen_coefficients_path = DATA / "s4g75_ngc4088_bi_frozen_coefficients.csv"
    sharp_coefficients_path = DATA / "s4g75_ngc4088_bi_sharp_coefficients.csv"
    q_first_pass = pd.read_csv(q_first_pass_path).iloc[0] if q_first_pass_path.exists() else None
    memory_first_pass = (
        pd.read_csv(memory_first_pass_path).iloc[0] if memory_first_pass_path.exists() else None
    )
    source_review = (
        pd.read_csv(source_review_path) if source_review_path.exists() else pd.DataFrame()
    )
    frozen_coefficients = (
        pd.read_csv(frozen_coefficients_path)
        if frozen_coefficients_path.exists()
        else pd.DataFrame()
    )
    sharp_coefficients = (
        pd.read_csv(sharp_coefficients_path)
        if sharp_coefficients_path.exists()
        else pd.DataFrame()
    )
    accepted_source_values = {}
    accepted_source_status = {}
    if not source_review.empty:
        for _, row in source_review.iterrows():
            if bool(row["accepted_for_numeric_bound"]):
                accepted_source_values[str(row["review_target"])] = float(row["accepted_value"])
                accepted_source_status[str(row["review_target"])] = str(row["review_status"])
    frozen_by_coefficient = {}
    frozen_status_by_coefficient = {}
    frozen_source_by_coefficient = {}
    if not frozen_coefficients.empty:
        for _, row in frozen_coefficients.iterrows():
            frozen_by_coefficient[str(row["coefficient_id"])] = float(row["frozen_value"])
            frozen_status_by_coefficient[str(row["coefficient_id"])] = str(row["freeze_status"])
            frozen_source_by_coefficient[str(row["coefficient_id"])] = "unit_Lipschitz_triangle_bound_default"
    if not sharp_coefficients.empty:
        for _, row in sharp_coefficients.iterrows():
            if str(row["sharp_status"]) == "SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT":
                frozen_by_coefficient[str(row["coefficient_id"])] = float(row["sharp_value"])
                frozen_status_by_coefficient[str(row["coefficient_id"])] = str(row["sharp_status"])
                frozen_source_by_coefficient[str(row["coefficient_id"])] = str(row["sharp_rule"])

    delta_pa = abs(
        float(response["outer_ridge_axis_side_a_pa_deg"])
        - float(response["inner_disk_axis_pa_deg"])
    )
    delta_r = abs(
        float(response["onset_radius_side_b_arcmin"])
        - float(response["onset_radius_side_a_arcmin"])
    )
    hi_radius = float(xw["hi_radius_arcmin"])
    onset_uncertainty_fraction = float(xw["x_warp_uncertainty"]) / float(
        xw["x_warp_onset"]
    )
    frozen_digitization_accepted = (
        str(validation["validation_status"]) == "READY_FOR_XW_CONVERSION_AUDIT"
        and bool(xw["accepted_for_mapping_rule"])
        and not bool(validation["forbidden_input_detected"])
    )
    frozen_feature_status = (
        "ACCEPTED_FROM_FROZEN_DIGITIZATION_VALIDATION"
        if frozen_digitization_accepted
        else "AVAILABLE_FIRST_PASS_NOT_INDEPENDENTLY_REVIEWED"
    )

    features = pd.DataFrame(
        [
            {
                "feature_id": "F_PA",
                "feature_symbol": "f_PA",
                "definition": "min(|Delta_PA_outer_inner| / 180 deg, 1)",
                "source_inputs": "Delta_PA_outer_inner",
                "feature_value": clipped(delta_pa / 180.0),
                "unit": "dimensionless",
                "status": frozen_feature_status,
            },
            {
                "feature_id": "F_R",
                "feature_symbol": "f_R",
                "definition": "min(max(|Delta_R_onset_sides| / R_HI, sigma_xw/xw), 1)",
                "source_inputs": "Delta_R_onset_sides; R_HI; sigma_xw_over_xw",
                "feature_value": clipped(max(delta_r / hi_radius, onset_uncertainty_fraction)),
                "unit": "dimensionless",
                "status": frozen_feature_status,
            },
            {
                "feature_id": "F_Q",
                "feature_symbol": "f_q",
                "definition": "q_warp_measured after residual-blind source review",
                "source_inputs": "q_warp_measured",
                "feature_value": (
                    accepted_source_values.get(
                        "q_warp_measured",
                        float(q_first_pass["q_warp_measured"]) if q_first_pass is not None else None,
                    )
                ),
                "unit": "dimensionless",
                "status": (
                    accepted_source_status.get(
                        "q_warp_measured",
                        "FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED"
                        if q_first_pass is not None
                        else "BLOCKED_QWARP_MEASUREMENT_EMPTY",
                    )
                ),
            },
            {
                "feature_id": "F_MEM",
                "feature_symbol": "f_mem",
                "definition": "morphological-history warp proxy after residual-blind source review",
                "source_inputs": "m_history_warp",
                "feature_value": (
                    accepted_source_values.get(
                        "m_history_warp",
                        float(memory_first_pass["m_history_warp"])
                        if memory_first_pass is not None
                        else None,
                    )
                ),
                "unit": "dimensionless",
                "status": (
                    accepted_source_status.get(
                        "m_history_warp",
                        "FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED"
                        if memory_first_pass is not None
                        else "BLOCKED_MEMORY_HISTORY_MEASUREMENT_EMPTY",
                    )
                ),
            },
        ]
    )
    features["galaxy"] = GALAXY
    features["uses_vobs_or_residual"] = False
    features["endpoint_scores_allowed"] = False
    features["claim_boundary"] = CLAIM_BOUNDARY
    features = features[
        [
            "galaxy",
            "feature_id",
            "feature_symbol",
            "definition",
            "source_inputs",
            "feature_value",
            "unit",
            "status",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    coefficients = pd.DataFrame(
        [
            {
                "coefficient_id": coefficient_id,
                "multiplies_feature": feature_symbol,
                "unit": "dimensionless",
                "allowed_origin": "Tau-side geometry derivation or predeclared residual-blind coefficient protocol",
                "current_value": frozen_by_coefficient.get(coefficient_id),
                "status": frozen_status_by_coefficient.get(
                    coefficient_id, "COEFFICIENT_VALUE_BLOCKED"
                ),
                "active_coefficient_source": frozen_source_by_coefficient.get(
                    coefficient_id, "none"
                ),
            }
            for coefficient_id, feature_symbol in [
                ("B_PA", "f_PA"),
                ("B_R", "f_R"),
                ("B_q", "f_q"),
                ("B_mem", "f_mem"),
            ]
        ]
    )
    coefficients["galaxy"] = GALAXY
    coefficients["forbidden_origin"] = "vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit"
    coefficients["uses_vobs_or_residual"] = False
    coefficients["endpoint_scores_allowed"] = False
    coefficients["claim_boundary"] = CLAIM_BOUNDARY
    coefficients = coefficients[
        [
            "galaxy",
            "coefficient_id",
            "multiplies_feature",
            "unit",
            "allowed_origin",
            "forbidden_origin",
            "current_value",
            "status",
            "active_coefficient_source",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    source_review_ready = {"q_warp_measured", "m_history_warp"}.issubset(
        set(accepted_source_values)
    )
    source_review_caveated = any("CAVEATED" in status for status in accepted_source_status.values())
    coefficients_ready = len(frozen_by_coefficient) == 4
    numeric_ready = source_review_ready and coefficients_ready

    gates = pd.DataFrame(
        [
            {
                "gate_id": "BI1_DIMENSIONLESS_FORM",
                "gate_status": "PASS",
                "evidence": "epsilon_cross, f_i, and B_i are all dimensionless",
                "remaining_obligation": "preserve dimensionless coefficient rule",
            },
            {
                "gate_id": "BI2_FEATURE_NORMALIZATION_DECLARED",
                "gate_status": "PASS",
                "evidence": "f_PA and f_R are normalized from source observables; f_q and f_mem use accepted q and caveated morphological-history source review if available",
                "remaining_obligation": "preserve source-review provenance",
            },
            {
                "gate_id": "BI3_COEFFICIENT_ORIGIN_RESTRICTED",
                "gate_status": "PASS",
                "evidence": "allowed and forbidden coefficient origins are explicit",
                "remaining_obligation": "derive or freeze coefficient values without endpoint residuals",
            },
            {
                "gate_id": "BI4_COEFFICIENT_VALUES_AVAILABLE",
                "gate_status": "PASS" if coefficients_ready else "BLOCKED",
                "evidence": (
                    "B_PA, B_R, B_q, and B_mem supplied by residual-blind protocol"
                    if coefficients_ready
                    else "B_PA, B_R, B_q, and B_mem are empty"
                ),
                "remaining_obligation": (
                    "derive the active protocol coefficients from Tau-side geometry before final physical claims"
                    if coefficients_ready
                    else "supply Tau-side derived or predeclared residual-blind B_i values"
                ),
            },
            {
                "gate_id": "BI5_NUMERIC_BOUND_READY",
                "gate_status": "PASS" if numeric_ready else "BLOCKED",
                "evidence": (
                    "accepted q/morphological-history source responses and residual-blind B_i values are available"
                    if numeric_ready
                    else "numeric bound needs accepted source responses and B_i values"
                ),
                "remaining_obligation": (
                    "evaluate numeric epsilon_cross protocol bound"
                    if numeric_ready
                    else "wait for independent source review and coefficient values"
                ),
            },
            {
                "gate_id": "BI6_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "rule forbids vobs and endpoint residuals",
                "remaining_obligation": "keep endpoint scoring separate",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    status_counts = gates["gate_status"].value_counts().to_dict()
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "rule_id": "NGC4088_EPSILON_CROSS_BI_COEFFICIENT_RULE_GATE",
                "n_features": len(features),
                "n_available_features": int(features["feature_value"].notna().sum()),
                "n_coefficients": len(coefficients),
                "n_available_coefficients": int(coefficients["current_value"].notna().sum()),
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "coefficient_rule_status": (
                    "FEATURE_NORMALIZATION_AND_B_VALUES_READY_PROTOCOL_BOUND"
                    if coefficients_ready
                    else "FEATURE_NORMALIZATION_READY_B_VALUES_BLOCKED"
                ),
                "numeric_bound_status": (
                    "NUMERIC_EPSILON_PROTOCOL_BOUND_READY"
                    if numeric_ready
                    else "NUMERIC_EPSILON_BOUND_BLOCKED"
                ),
                "source_response_status": (
                    "SOURCE_RESPONSES_ACCEPTED_CAVEATED_FOR_PROTOCOL_BOUND"
                    if source_review_ready and source_review_caveated
                    else "SOURCE_RESPONSES_ACCEPTED_FOR_PROTOCOL_BOUND"
                    if source_review_ready
                    else (
                        "FIRST_PASS_SOURCE_FEATURES_AVAILABLE_REVIEW_REQUIRED"
                        if q_first_pass is not None and memory_first_pass is not None
                        else "SOURCE_FEATURES_PARTLY_BLOCKED"
                    )
                ),
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return features, coefficients, gates, summary


def write_report(
    features: pd.DataFrame,
    coefficients: pd.DataFrame,
    gates: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 B_i Coefficient-Rule Gate",
        "",
        "This gate fixes the residual-blind feature-normalization side of the",
        "`epsilon_cross` bound. If a residual-blind sharpened coefficient rule",
        "is available, this gate carries it into the numeric-bound shell;",
        "otherwise it falls back to the conservative unit-bound freeze. Neither",
        "path uses endpoint residuals.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Feature Normalization",
        "",
        markdown_table(features),
        "",
        "## Coefficient Obligations",
        "",
        markdown_table(coefficients),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The feature definitions are dimensionless and residual-blind. Frozen",
        "or sharpened B_i values, when present, are protocol coefficients, not",
        "final Tau-side sharp-amplitude derivations.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_bi_coefficient_rule_gate.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    features, coefficients, gates, summary = build_gate()
    features.to_csv(DATA / "s4g75_ngc4088_bi_feature_normalization.csv", index=False)
    coefficients.to_csv(DATA / "s4g75_ngc4088_bi_coefficient_obligations.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_bi_coefficient_rule_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_bi_coefficient_rule_summary.csv", index=False)
    write_report(features, coefficients, gates, summary)
    print("PAPER8_NGC4088_BI_COEFFICIENT_RULE_GATE_COMPLETE")


if __name__ == "__main__":
    main()
