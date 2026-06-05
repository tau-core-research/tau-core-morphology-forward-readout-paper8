#!/usr/bin/env python3
"""Fill the NGC4183 tilted-ring response with a non-independent Codex review.

This script records a local source/transcription review performed by Codex. It
is intentionally marked as non-independent and does not authorize formula
freeze. A later independent reviewer response is still required before
null-control promotion.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_codex_internal_review_response_not_independent_not_endpoint"


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    profile = pd.read_csv(DATA / "ngc4183_tilted_ring_orientation_profile_summary.csv").iloc[0]
    weak = pd.read_csv(DATA / "ngc4183_weak_projection_control_summary.csv").iloc[0]

    response = pd.DataFrame(
        [
            {
                "reviewer": "codex_internal_source_review_not_independent",
                "date": "2026-06-05",
                "source_identity_decision": "ACCEPT",
                "radius_series_decision": "ACCEPT",
                "orientation_series_decision": "ACCEPT",
                "velocity_columns_decision": "ACCEPT",
                "upper_bound_conclusion_decision": "ACCEPT",
                "corrections": (
                    "No correction from local visual review of the rendered Table 4 "
                    "page/crop. NGC4183 rows match the extracted radius series "
                    "10..241 arcsec, constant i=82 deg, and PA=346..349 deg. "
                    "Outer 229/241 arcsec rows have missing approaching-side "
                    "velocity entries, as represented in the extracted profile."
                ),
                "review_verdict": (
                    "INTERNAL_CODEX_SOURCE_REVIEW_ACCEPTS_TRANSCRIPTION_NOT_INDEPENDENT_"
                    "FREEZE_BLOCKED"
                ),
                "may_freeze_null_control_after_review": False,
            }
        ]
    )

    template_path = DATA / "ngc4183_tilted_ring_independent_review_response_template.csv"
    if template_path.exists():
        existing = pd.read_csv(template_path)
        existing_row = existing.iloc[0]
        existing_reviewer = str(existing_row.get("reviewer", "")).strip().lower()
        existing_verdict = str(existing_row.get("review_verdict", "")).strip()
        preserve_existing_template = bool(existing_reviewer) and existing_reviewer != "nan" and (
            "independent" in existing_verdict or "FREEZE_AUTHORIZED" in existing_verdict
        )
    else:
        preserve_existing_template = False

    summary = pd.DataFrame(
        [
            {
                "codex_internal_review_status": (
                    "NGC4183_CODEX_INTERNAL_REVIEW_RESPONSE_FILLED_NOT_INDEPENDENT"
                ),
                "reviewer": response.iloc[0]["reviewer"],
                "source_identity_decision": response.iloc[0]["source_identity_decision"],
                "radius_series_decision": response.iloc[0]["radius_series_decision"],
                "orientation_series_decision": response.iloc[0]["orientation_series_decision"],
                "upper_bound_conclusion_decision": response.iloc[0][
                    "upper_bound_conclusion_decision"
                ],
                "max_abs_pa_drift_deg": float(profile["max_abs_pa_drift_deg"]),
                "max_abs_inclination_drift_deg": float(
                    profile["max_abs_inclination_drift_deg"]
                ),
                "gamma_projection_upper_bound": float(
                    weak["gamma_projection_upper_bound"]
                ),
                "max_velocity_fractional_change": float(
                    weak["max_velocity_fractional_change"]
                ),
                "response_is_independent": False,
                "may_freeze_null_control_after_review": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": "independent_reviewer_response_still_required_for_freeze",
            }
        ]
    )

    if not preserve_existing_template:
        response.to_csv(template_path, index=False)
    response.to_csv(DATA / "ngc4183_codex_internal_review_response.csv", index=False)
    summary.to_csv(DATA / "ngc4183_codex_internal_review_response_summary.csv", index=False)

    report = f"""# NGC4183 Codex Internal Source Review Response

Status: `{summary.iloc[0]["codex_internal_review_status"]}`

This response records a Codex source/transcription review. It is not an independent review and does not authorize formula freeze or endpoint scoring.

## Summary

{markdown_table(summary)}

## Internal Response Draft

{markdown_table(response)}

## Template Write Policy

{"The existing independent response template was preserved." if preserve_existing_template else "No independent response was present, so the internal draft was written to the shared template."}

## Review Basis

- Local rendered Table 4 full page and focused NGC4183 crop.
- Extracted profile rows: `10..241 arcsec`, `n={int(profile["n_rings"])}`.
- Orientation series: `i=82 deg` throughout; `PA=346..349 deg`.
- Derived weak-control bound: `gamma_proj <= {float(weak["gamma_projection_upper_bound"]):.8f}`.

## Claim Boundary

This is useful as an internal consistency check only. A genuinely independent
review response is still required before null-control formula freeze can be
authorized.
"""
    (REPORTS / "ngc4183_codex_internal_review_response.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
