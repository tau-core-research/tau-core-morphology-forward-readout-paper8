#!/usr/bin/env python3
"""Build a consolidated P0 residual-blind review pipeline status dashboard.

This dashboard summarizes the P0 source-to-review-to-promotion chain without
creating full endpoint labels and without computing endpoint scores.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "p0_review_pipeline_status_not_label_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def load_one(path: str) -> pd.DataFrame:
    return pd.read_csv(DATA / path)


def build_status_rows() -> pd.DataFrame:
    request_manifest = load_one("p0_external_imaging_request_manifest.csv")
    availability = load_one("p0_skyview_availability_summary.csv")
    preview = load_one("p0_skyview_preview_image_summary.csv")
    visual_template = load_one("p0_visual_review_template.csv")
    completion = load_one("p0_visual_review_completion_summary.csv")
    handoff = load_one("p0_visual_review_handoff_summary.csv")
    response = load_one("p0_visual_review_response_summary.csv")
    promotion = load_one("p0_response_to_manifest_promotion_summary.csv")
    source_plan = load_one("p0_missing_data_source_acquisition_summary.csv")
    source_evidence = load_one("p0_external_source_evidence_summary.csv")
    response_draft = load_one("p0_source_assisted_review_response_validation.csv")
    source_availability = load_one("p0_requested_source_family_availability_summary.csv")
    codex_labels = load_one("p0_codex_accepted_label_manifest_summary.csv")

    n_p0 = int(len(visual_template))
    rows = [
        {
            "stage": "external_imaging_request_manifest",
            "stage_status": "SOURCE_REQUEST_READY",
            "n_galaxies": int(request_manifest["galaxy"].nunique()),
            "n_blocked": 0,
            "endpoint_scores_computed": False,
            "next_action": "use source requests for residual-blind review",
        },
        {
            "stage": "skyview_availability_audit",
            "stage_status": "AVAILABLE_SOURCE_PREFLIGHT_COMPLETE",
            "n_galaxies": int(availability["n_galaxies"].max()),
            "n_blocked": 0,
            "endpoint_scores_computed": False,
            "next_action": "render source previews without image classification",
        },
        {
            "stage": "skyview_preview_images",
            "stage_status": "PREVIEW_SOURCE_MATERIAL_READY",
            "n_galaxies": n_p0,
            "n_blocked": 0,
            "endpoint_scores_computed": False,
            "next_action": "use previews only as residual-blind review source material",
        },
        {
            "stage": "visual_review_template",
            "stage_status": "REVIEW_TEMPLATE_READY",
            "n_galaxies": n_p0,
            "n_blocked": 0,
            "endpoint_scores_computed": False,
            "next_action": "fill review fields residual-blind",
        },
        {
            "stage": "visual_review_completion_gate",
            "stage_status": completion["visual_review_completion_decision"].iloc[0],
            "n_galaxies": int(completion["n_galaxies"].iloc[0]),
            "n_blocked": int(completion["n_blocked_rows"].iloc[0]),
            "endpoint_scores_computed": bool(completion["endpoint_scores_computed"].iloc[0]),
            "next_action": "complete residual-blind visual review fields",
        },
        {
            "stage": "visual_review_handoff",
            "stage_status": handoff["handoff_status"].iloc[0],
            "n_galaxies": int(handoff["n_galaxies"].iloc[0]),
            "n_blocked": int(handoff["n_blocked_review_rows"].iloc[0]),
            "endpoint_scores_computed": bool(handoff["endpoint_scores_computed"].iloc[0]),
            "next_action": "send handoff to residual-blind reviewer",
        },
        {
            "stage": "visual_review_response_intake",
            "stage_status": response["response_intake_decision"].iloc[0],
            "n_galaxies": int(response["n_galaxies"].iloc[0]),
            "n_blocked": int(response["n_blocked_rows"].iloc[0]),
            "endpoint_scores_computed": bool(response["endpoint_scores_computed"].iloc[0]),
            "next_action": "fill response template before independent manifest audit",
        },
        {
            "stage": "response_to_manifest_promotion_gate",
            "stage_status": promotion["promotion_gate_decision"].iloc[0],
            "n_galaxies": n_p0,
            "n_blocked": int(promotion["n_blocked_gates"].iloc[0]),
            "endpoint_scores_computed": bool(promotion["endpoint_scores_computed"].iloc[0]),
            "next_action": "do not promote labels until all promotion gates pass",
        },
        {
            "stage": "missing_data_source_acquisition_plan",
            "stage_status": "SOURCE_PLAN_READY",
            "n_galaxies": int(source_plan["n_p0_galaxies"].max()),
            "n_blocked": 0,
            "endpoint_scores_computed": bool(source_plan["endpoint_scores_computed"].any()),
            "next_action": "acquire S4G/NED/DustPedia/HI/PHANGS evidence residual-blind",
        },
        {
            "stage": "dustpedia_hi_phangs_source_evidence",
            "stage_status": "SOURCE_EVIDENCE_PARTIAL_REVIEW_REQUIRED",
            "n_galaxies": int(source_evidence["galaxy"].nunique()),
            "n_blocked": int(
                (source_evidence["dustpedia_status"] == "NO_DIRECT_DUSTPEDIA_MATCH").sum()
                + (source_evidence["phangs_status"] == "NO_PHANGS_SAMPLE_COVERAGE").sum()
            ),
            "endpoint_scores_computed": bool(source_evidence["endpoint_scores_computed"].any()),
            "next_action": "use source evidence for human residual-blind review only",
        },
        {
            "stage": "source_assisted_review_response_draft",
            "stage_status": "BLOCKED_DRAFT_NOT_ACCEPTED_REVIEW",
            "n_galaxies": int(response_draft["galaxy"].nunique()),
            "n_blocked": int((response_draft["draft_validation_status"] != "PASS").sum()),
            "endpoint_scores_computed": bool(response_draft["endpoint_scores_computed"].any()),
            "next_action": "human reviewer must convert draft into accepted-review response",
        },
        {
            "stage": "p0_codex_accepted_label_manifest",
            "stage_status": codex_labels["p0_label_manifest_decision"].iloc[0],
            "n_galaxies": int(codex_labels["n_galaxies"].iloc[0]),
            "n_blocked": int(codex_labels["n_blocked"].iloc[0]),
            "endpoint_scores_computed": bool(codex_labels["endpoint_scores_computed"].iloc[0]),
            "next_action": "keep P0 labels in audit lane; do not launch full endpoint manifest",
        },
        {
            "stage": "requested_source_family_availability",
            "stage_status": "SOURCE_AVAILABILITY_PREFLIGHT_COMPLETE",
            "n_galaxies": int(source_availability["n_p0_galaxies"].max()),
            "n_blocked": int(
                source_availability["n_to_be_queried"].sum()
                + source_availability.get("n_no_coverage", pd.Series(dtype=int)).sum()
                + source_availability.get("n_review_pending", pd.Series(dtype=int)).sum()
            ),
            "endpoint_scores_computed": bool(source_availability["endpoint_scores_computed"].any()),
            "next_action": "complete human review for matched evidence and record no-coverage blockers",
        },
    ]
    status = pd.DataFrame(rows)
    status["p0_codex_source_review_labels_created"] = (
        status["stage"].eq("p0_codex_accepted_label_manifest")
        & status["n_blocked"].eq(0)
    )
    status["full_endpoint_labels_created"] = False
    status["claim_boundary"] = CLAIM_BOUNDARY
    return status


def build_summary(status: pd.DataFrame) -> pd.DataFrame:
    blocked = status[status["stage_status"].str.startswith("BLOCKED")]
    p0_labels_ready = bool(status["p0_codex_source_review_labels_created"].any())
    if p0_labels_ready:
        decision = "P0_CODEX_SOURCE_REVIEW_LABELS_READY_FULL_ENDPOINT_BLOCKED"
    elif not blocked.empty:
        decision = "READY_FOR_RESIDUAL_BLIND_HUMAN_REVIEW_ONLY"
    else:
        decision = "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
    return pd.DataFrame(
        [
            {
                "pipeline_decision": decision,
                "n_stages": len(status),
                "n_blocked_stages": len(blocked),
                "endpoint_scores_computed": bool(status["endpoint_scores_computed"].any()),
                "p0_codex_source_review_labels_created": p0_labels_ready,
                "full_endpoint_labels_created": False,
                "next_action": (
                    "use P0 source-reviewed labels for audit only; full endpoint remains blocked"
                    if p0_labels_ready
                    else "complete residual-blind human review responses"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def write_report(status: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# P0 Residual-Blind Review Pipeline Status",
        "",
        "This report consolidates the P0 source-request, preview, visual-review,",
        "response-intake, response-to-manifest promotion, and P0 source-reviewed",
        "label-manifest gates. It is a status dashboard only: it creates no full",
        "endpoint labels and computes no endpoint scores.",
        "",
        "This is a status dashboard only: P0 source-reviewed labels may exist,",
        "but no full endpoint labels or endpoint scores are created.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Stage Status",
        "",
        markdown_table(
            status[
                [
                    "stage",
                    "stage_status",
                    "n_galaxies",
                    "n_blocked",
                    "p0_codex_source_review_labels_created",
                    "full_endpoint_labels_created",
                    "endpoint_scores_computed",
                    "next_action",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "The dashboard may be used to coordinate residual-blind review work. It does",
        "not launch full endpoint labels, does not run endpoint scores, and does",
        "not compare Tau Core to MOND/RAR/TGP/Newtonian baselines.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_review_pipeline_status_dashboard.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def write_html(status: pd.DataFrame, summary: pd.DataFrame) -> None:
    cards = []
    for _, row in status.iterrows():
        status_class = "blocked" if str(row["stage_status"]).startswith("BLOCKED") else "ready"
        cards.append(
            f"""
            <section class="card {status_class}">
              <h2>{escape(row['stage'])}</h2>
              <p class="status">{escape(row['stage_status'])}</p>
              <dl>
                <div><dt>Galaxies</dt><dd>{int(row['n_galaxies'])}</dd></div>
                <div><dt>Blocked</dt><dd>{int(row['n_blocked'])}</dd></div>
                <div><dt>P0 labels</dt><dd>{escape(str(row['p0_codex_source_review_labels_created']))}</dd></div>
                <div><dt>Endpoint labels</dt><dd>{escape(str(row['full_endpoint_labels_created']))}</dd></div>
                <div><dt>Endpoint scores</dt><dd>{escape(str(row['endpoint_scores_computed']))}</dd></div>
              </dl>
              <p>{escape(row['next_action'])}</p>
            </section>
            """
        )
    decision = summary["pipeline_decision"].iloc[0]
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Paper 8 P0 Review Pipeline Status</title>
  <style>
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #1f2933;
      background: #f6f6f2;
    }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    .notice {{ max-width: 920px; line-height: 1.5; margin-bottom: 24px; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
    }}
    .card {{
      background: #fff;
      border: 1px solid #d7d7d0;
      border-radius: 8px;
      padding: 16px;
    }}
    .card.blocked {{ border-color: #d49b5a; background: #fff9ed; }}
    h2 {{ margin: 0 0 6px; font-size: 18px; }}
    .status {{
      display: inline-block;
      padding: 5px 8px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 12px;
      background: #eef6f1;
      color: #22613a;
    }}
    .blocked .status {{ background: #fff0d8; color: #694600; }}
    dl {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
    }}
    dt {{ font-size: 12px; color: #667085; }}
    dd {{ margin: 2px 0 0; font-weight: 700; }}
    p {{ line-height: 1.45; }}
  </style>
</head>
<body>
  <main>
    <h1>Paper 8 P0 Review Pipeline Status</h1>
    <p class="notice">
      Pipeline decision: <strong>{escape(decision)}</strong>. This dashboard
      coordinates residual-blind review work only. P0 source-reviewed labels may
      exist, but it creates no full endpoint labels and computes no endpoint
      scores. Claim boundary:
      <code>{CLAIM_BOUNDARY}</code>.
    </p>
    <div class="grid">
      {''.join(cards)}
    </div>
  </main>
</body>
</html>
"""
    html = "\n".join(line.rstrip() for line in html.splitlines()) + "\n"
    (REPORTS / "p0_review_pipeline_status_dashboard.html").write_text(
        html, encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    status = build_status_rows()
    summary = build_summary(status)
    status.to_csv(DATA / "p0_review_pipeline_status.csv", index=False)
    summary.to_csv(DATA / "p0_review_pipeline_status_summary.csv", index=False)
    write_report(status, summary)
    write_html(status, summary)
    print("PAPER8_P0_REVIEW_PIPELINE_STATUS_DASHBOARD_COMPLETE")


if __name__ == "__main__":
    main()
