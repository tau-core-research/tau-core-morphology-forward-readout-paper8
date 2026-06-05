#!/usr/bin/env python3
"""Build the frozen NGC4088 channel-map digitization protocol and intake.

This protocol sits one step downstream of the worksheet.  It does not extract
`x_w` automatically and does not use endpoint scores.  Instead, it freezes the
allowed measurement logic and creates a residual-blind response template for a
later manual or image-analysis digitization pass.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

PENDING = "DIGITIZATION_RESPONSE_PENDING"
CLAIM_BOUNDARY = "s4g75_ngc4088_channel_map_digitization_protocol_not_endpoint"

REQUIRED_RESPONSE_FIELDS = [
    "digitizer_id",
    "digitization_timestamp_utc",
    "inner_disk_axis_definition",
    "inner_disk_axis_pa_deg",
    "outer_ridge_axis_side_a_pa_deg",
    "outer_ridge_axis_side_b_pa_deg",
    "onset_radius_side_a_arcmin",
    "onset_radius_side_b_arcmin",
    "side_combination_rule_applied",
    "xw_combined_arcmin",
    "uncertainty_arcmin",
    "crosscheck_page77_consistency",
    "source_images_used",
]

OPTIONAL_RESPONSE_FIELDS = [
    "digitization_notes",
]

FORBIDDEN_INPUTS = [
    "rotation residual",
    "endpoint score",
    "best-fit Tau family",
    "required-S_tau diagnostic",
    "post-hoc x_w chosen after endpoint scoring",
]


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
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def build_protocol() -> pd.DataFrame:
    rows = [
        {
            "protocol_step": 1,
            "rule_id": "SOURCE_LOCK",
            "instruction": "Use only the frozen ROI crop overlay plus the rendered Verheijen-Sancisi pages 76 and 77.",
            "allowed_inputs": "ROI worksheet overlay;page_76 PNG;page_77 PNG",
            "forbidden_inputs": "rotation residual;endpoint score;fit comparison",
            "output_field": "source_images_used",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_step": 2,
            "rule_id": "INNER_AXIS",
            "instruction": "Define one inner-disk axis from the central channel-map morphology before reading the outer bend.",
            "allowed_inputs": "central channel-map ridge/orientation only",
            "forbidden_inputs": "outer warp morphology used to redefine the inner axis",
            "output_field": "inner_disk_axis_definition;inner_disk_axis_pa_deg",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_step": 3,
            "rule_id": "OUTER_AXES_BY_SIDE",
            "instruction": "Measure outer ridge axes separately on the two sides of the disk.",
            "allowed_inputs": "outer ridge morphology by side",
            "forbidden_inputs": "single global axis replacing side-by-side outer measurements",
            "output_field": "outer_ridge_axis_side_a_pa_deg;outer_ridge_axis_side_b_pa_deg",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_step": 4,
            "rule_id": "ONSET_BY_SIDE",
            "instruction": "Record the first radial onset where the outer ridge departs from the inner axis on each side.",
            "allowed_inputs": "page 76 channel-map morphology;page 77 cross-check",
            "forbidden_inputs": "text-only warped/asymmetric label",
            "output_field": "onset_radius_side_a_arcmin;onset_radius_side_b_arcmin",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_step": 5,
            "rule_id": "SIDE_COMBINATION",
            "instruction": "Combine side measurements with a frozen rule: MIN_SIDE onset if both sides are measurable; otherwise use the measurable side and mark the other as missing.",
            "allowed_inputs": "measured side A/B onset radii only",
            "forbidden_inputs": "post-hoc side choice based on endpoint behavior",
            "output_field": "side_combination_rule_applied;xw_combined_arcmin",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_step": 6,
            "rule_id": "UNCERTAINTY_AND_CROSSCHECK",
            "instruction": "Report one predeclared uncertainty in arcmin and whether page 77 is consistent with the chosen onset.",
            "allowed_inputs": "digitization spread;page 77 continuation/PV context",
            "forbidden_inputs": "uncertainty tuned after scoring",
            "output_field": "uncertainty_arcmin;crosscheck_page77_consistency",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return pd.DataFrame(rows)


def build_response_template() -> pd.DataFrame:
    row = {
        "galaxy": "NGC4088",
        "digitization_route": "CHANNEL_MAP_DIGITIZATION",
        "response_status": "BLOCKED_RESPONSE_PENDING",
        "accepted_x_w_available": False,
        "endpoint_scores_allowed": False,
        "endpoint_scores_computed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    for field in REQUIRED_RESPONSE_FIELDS + OPTIONAL_RESPONSE_FIELDS:
        row[field] = PENDING
    return pd.DataFrame([row])


def load_or_initialize_response() -> pd.DataFrame:
    path = DATA / "s4g75_ngc4088_channel_map_digitization_response_template.csv"
    if path.exists():
        response = pd.read_csv(path)
        expected = {
            "galaxy",
            "digitization_route",
            "response_status",
            "accepted_x_w_available",
            "endpoint_scores_allowed",
            "endpoint_scores_computed",
            "claim_boundary",
            *REQUIRED_RESPONSE_FIELDS,
            *OPTIONAL_RESPONSE_FIELDS,
        }
        if expected.issubset(set(response.columns)):
            return response
    return build_response_template()


def build_schema() -> pd.DataFrame:
    rows = []
    for field in REQUIRED_RESPONSE_FIELDS:
        rows.append(
            {
                "field": field,
                "required_for_xw_candidate": True,
                "initial_value": PENDING,
                "may_use_endpoint_scores": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for field in OPTIONAL_RESPONSE_FIELDS:
        rows.append(
            {
                "field": field,
                "required_for_xw_candidate": False,
                "initial_value": PENDING,
                "may_use_endpoint_scores": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def validate_response(row: pd.Series) -> dict[str, object]:
    missing = [field for field in REQUIRED_RESPONSE_FIELDS if str(row[field]).strip() == PENDING]
    forbidden_hits = [
        item
        for item in FORBIDDEN_INPUTS
        if item.lower() in str(row.get("digitization_notes", "")).lower()
    ]
    if forbidden_hits:
        status = "BLOCKED_FORBIDDEN_INPUT_PRESENT"
    elif missing:
        status = "BLOCKED_DIGITIZATION_RESPONSE_PENDING"
    else:
        status = "READY_FOR_XW_CONVERSION_AUDIT"
    return {
        "galaxy": row["galaxy"],
        "validation_status": status,
        "n_required_fields": len(REQUIRED_RESPONSE_FIELDS),
        "n_missing_required_fields": len(missing),
        "missing_required_fields": ";".join(missing) if missing else "none",
        "forbidden_input_detected": bool(forbidden_hits),
        "forbidden_input_terms": ";".join(forbidden_hits) if forbidden_hits else "none",
        "accepted_x_w_available": status == "READY_FOR_XW_CONVERSION_AUDIT",
        "endpoint_scores_allowed": False,
        "endpoint_scores_computed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_report(
    protocol: pd.DataFrame,
    validation: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    compact = validation[
        [
            "galaxy",
            "validation_status",
            "n_missing_required_fields",
            "accepted_x_w_available",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]
    lines = [
        "# NGC4088 Channel-Map Digitization Protocol",
        "",
        "This report freezes the residual-blind measurement logic for the NGC4088",
        "channel-map route and creates a blank response intake for later manual or",
        "frozen image-analysis digitization. It does not extract `x_w`.",
        "",
        "## Verdict",
        "",
        "The protocol is frozen and the response template is ready, but the current",
        "package remains blocked because all required digitization fields are still",
        "pending.",
        "",
        "## Protocol Rules",
        "",
        markdown_table(protocol),
        "",
        "## Response Validation",
        "",
        markdown_table(compact),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Forbidden Inputs",
        "",
        "\n".join(f"- {item}" for item in FORBIDDEN_INPUTS),
        "",
        "## Claim Boundary",
        "",
        "A completed response would only authorize a later residual-blind",
        "`x_w` conversion audit. It would not by itself allow endpoint scoring or",
        "promote NGC4088 into a matched-family validation row.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_channel_map_digitization_protocol.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    protocol = build_protocol()
    response = load_or_initialize_response()
    schema = build_schema()
    validation = pd.DataFrame([validate_response(row) for _, row in response.iterrows()])
    response["accepted_x_w_available"] = (
        validation["validation_status"] == "READY_FOR_XW_CONVERSION_AUDIT"
    ).to_numpy()
    response["endpoint_scores_allowed"] = False
    response["endpoint_scores_computed"] = False
    blocked = validation[
        validation["validation_status"].isin(
            {"BLOCKED_DIGITIZATION_RESPONSE_PENDING", "BLOCKED_FORBIDDEN_INPUT_PRESENT"}
        )
    ]
    summary = pd.DataFrame(
        [
            {
                "digitization_protocol_decision": (
                    "READY_FOR_XW_CONVERSION_AUDIT"
                    if blocked.empty
                    else "BLOCKED_DIGITIZATION_RESPONSE_PENDING"
                ),
                "n_rows": len(response),
                "n_blocked_rows": len(blocked),
                "n_missing_required_fields_total": int(
                    validation["n_missing_required_fields"].sum()
                ),
                "accepted_x_w_available": blocked.empty,
                "endpoint_scores_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    protocol.to_csv(DATA / "s4g75_ngc4088_channel_map_digitization_protocol.csv", index=False)
    response.to_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_response_template.csv", index=False
    )
    schema.to_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_response_schema.csv", index=False
    )
    validation.to_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_response_validation.csv", index=False
    )
    summary.to_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_response_summary.csv", index=False
    )
    write_report(protocol, validation, summary)
    print("PAPER8_NGC4088_CHANNEL_MAP_DIGITIZATION_PROTOCOL_COMPLETE")


if __name__ == "__main__":
    main()
