#!/usr/bin/env python3
"""Build a reviewer handoff for the NGC4183 tilted-ring source check.

The handoff turns the independent review packet into concrete residual-blind
review tasks. It does not fill the response, freeze a formula, or score an
endpoint.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_tilted_ring_review_handoff_not_endpoint"
GALAXY = "NGC4183"


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


def file_uri(path: str) -> str:
    return Path(path).resolve().as_uri()


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    review_items = pd.read_csv(DATA / "ngc4183_tilted_ring_independent_review_items.csv")
    visual_sources = pd.read_csv(
        DATA / "ngc4183_tilted_ring_independent_review_visual_sources.csv"
    )
    readiness = pd.read_csv(DATA / "ngc4183_visual_review_readiness_summary.csv").iloc[0]
    response = pd.read_csv(
        DATA / "ngc4183_tilted_ring_independent_review_response_template.csv"
    )
    weak = pd.read_csv(DATA / "ngc4183_weak_projection_control_summary.csv").iloc[0]

    tasks = []
    for index, row in review_items.iterrows():
        tasks.append(
            {
                "task_id": f"N4183_HANDOFF_T{index + 1}",
                "galaxy": GALAXY,
                "review_item": row["review_item"],
                "task": row["review_question"],
                "current_pipeline_value": row["current_value"],
                "required_response": row["required_response"],
                "allowed_sources": (
                    "local Verheijen-Sancisi PDF page/crop; local OCR excerpt; "
                    "extracted tilted-ring CSV for transcription comparison"
                ),
                "forbidden_inputs": (
                    "observed rotation residuals; endpoint score; baseline comparison; "
                    "best-fit Tau readout family; post-hoc formula retuning"
                ),
                "may_use_vobs": False,
                "may_freeze_formula": False,
                "may_score_endpoint": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    tasks_df = pd.DataFrame(tasks)

    response_fields = pd.DataFrame(
        [
            {
                "response_file": str(
                    DATA / "ngc4183_tilted_ring_independent_review_response_template.csv"
                ),
                "field": column,
                "current_value": "" if pd.isna(response.iloc[0][column]) else response.iloc[0][column],
                "required_for_freeze": column
                in {
                    "source_identity_decision",
                    "radius_series_decision",
                    "orientation_series_decision",
                    "velocity_columns_decision",
                    "upper_bound_conclusion_decision",
                    "review_verdict",
                    "may_freeze_null_control_after_review",
                },
                "accepted_values_or_rule": (
                    "must be True only after all source transcription decisions accept or correct"
                    if column == "may_freeze_null_control_after_review"
                    else "accept/reject/correct or reviewer note"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for column in response.columns
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "handoff_status": "NGC4183_TILTED_RING_REVIEW_HANDOFF_READY_RESPONSE_REQUIRED",
                "galaxy": GALAXY,
                "visual_review_readiness_status": str(readiness["visual_review_readiness_status"]),
                "weak_control_preflight_status": str(weak["weak_control_preflight_status"]),
                "n_tasks": len(tasks_df),
                "n_visual_sources": len(visual_sources),
                "n_required_response_fields": int(response_fields["required_for_freeze"].sum()),
                "response_received": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "construction_reads_vobs": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": "independent_reviewer_fills_response_template",
            }
        ]
    )

    tasks_df.to_csv(DATA / "ngc4183_tilted_ring_review_handoff_tasks.csv", index=False)
    response_fields.to_csv(
        DATA / "ngc4183_tilted_ring_review_handoff_response_fields.csv", index=False
    )
    summary.to_csv(DATA / "ngc4183_tilted_ring_review_handoff_summary.csv", index=False)

    report = [
        "# NGC4183 Tilted-Ring Review Handoff",
        "",
        f"Status: `{summary.iloc[0]['handoff_status']}`",
        "",
        "This handoff is for residual-blind independent source review. It does",
        "not fill the response, freeze a formula, or authorize endpoint scoring.",
        "It is not an endpoint score.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Review Tasks",
        "",
        markdown_table(tasks_df),
        "",
        "## Response Fields",
        "",
        markdown_table(response_fields),
        "",
        "## Visual Sources",
        "",
        markdown_table(visual_sources),
        "",
        "## Freeze Rule",
        "",
        "The null-control formula may be reconsidered for freeze only if the",
        "independent reviewer accepts or corrects the source identity, radius",
        "series, orientation series, and upper-bound conclusion without using",
        "rotation residuals or endpoint scores.",
        "",
    ]
    (REPORTS / "ngc4183_tilted_ring_review_handoff.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    image_cards = []
    for _, row in visual_sources.iterrows():
        path = str(row["path"])
        if Path(path).exists():
            image_html = f'<img src="{escape(file_uri(path))}" alt="{escape(row["visual_source_id"])}" />'
        else:
            image_html = "<p><strong>Missing local visual source.</strong></p>"
        image_cards.append(
            f"""
            <section class="card">
              <h2>{escape(row['visual_source_id'])}</h2>
              <p><strong>Role:</strong> {escape(row['role'])}</p>
              <p><strong>Review use:</strong> {escape(row['review_use'])}</p>
              <p><code>{escape(path)}</code></p>
              {image_html}
            </section>
            """
        )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>NGC4183 Tilted-Ring Review Handoff</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      margin: 32px;
      color: #172026;
      background: #f6f7f8;
    }}
    header, .card {{
      background: white;
      border: 1px solid #d8dee4;
      border-radius: 8px;
      padding: 18px;
      margin-bottom: 18px;
    }}
    h1, h2 {{ margin-top: 0; }}
    table {{
      border-collapse: collapse;
      width: 100%;
      background: white;
      margin-bottom: 18px;
    }}
    th, td {{
      border: 1px solid #d8dee4;
      padding: 8px;
      vertical-align: top;
      font-size: 13px;
    }}
    img {{
      max-width: 100%;
      border: 1px solid #d8dee4;
      background: #fff;
    }}
    code {{ white-space: pre-wrap; }}
  </style>
</head>
<body>
  <header>
    <h1>NGC4183 Tilted-Ring Review Handoff</h1>
    <p>Status: <code>{escape(summary.iloc[0]['handoff_status'])}</code></p>
    <p>This page is a source-review handoff. It is not a formula freeze and not an endpoint score.</p>
  </header>
  <section class="card">
    <h2>Reviewer Contract</h2>
    <p>Use only the listed source visuals, OCR excerpt, and extracted profile for transcription review.
    Do not use observed rotation residuals, endpoint scores, or best-fit readout outcomes.</p>
  </section>
  {''.join(image_cards)}
</body>
</html>
"""
    (REPORTS / "ngc4183_tilted_ring_review_handoff.html").write_text(
        html, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
