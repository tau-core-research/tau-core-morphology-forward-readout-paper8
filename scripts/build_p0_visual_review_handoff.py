#!/usr/bin/env python3
"""Build a reviewer handoff package for the P0 visual review.

The handoff translates the blocked visual review completion gate into concrete
reviewer tasks.  It does not classify images, does not promote accepted labels,
and does not compute endpoint scores.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "p0_visual_review_handoff_not_label_not_endpoint"

FORBIDDEN_INPUTS = [
    "endpoint residual gain",
    "required-S_tau diagnostic as a label input",
    "best-fit Tau Core readout family",
    "MOND/RAR/TGP comparison score",
    "post-hoc family switching after endpoint scoring",
]


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def allowed_sources(row: pd.Series) -> str:
    sources = [
        "local SkyView preview panels",
        "NED",
        "SIMBAD",
        "SkyView DSS2 Red",
        "SkyView 2MASS-K",
        "SkyView WISE W1",
    ]
    if "bar_m2_component" in str(row["inspection_focus"]):
        sources.append("bar-length or velocity-field support if acquired before scoring")
    if "edge_on_projection_degeneracy" in str(row["inspection_focus"]):
        sources.append("projection/inclination caveat sources")
    return ";".join(sources)


def build_tasks(template: pd.DataFrame, completion: pd.DataFrame) -> pd.DataFrame:
    rows = []
    completion = completion.set_index("galaxy")
    for _, row in template.iterrows():
        gate = completion.loc[row["galaxy"]]
        rows.append(
            {
                "galaxy": row["galaxy"],
                "review_status": gate["completion_status"],
                "n_pending_review_fields": int(gate["n_pending_review_fields"]),
                "required_review_fields": gate["pending_review_fields"],
                "preview_png_paths": row["preview_png_paths"],
                "allowed_sources": allowed_sources(row),
                "forbidden_inputs": ";".join(FORBIDDEN_INPUTS),
                "handoff_action": "fill residual-blind review fields before accepted-manifest audit",
                "accepted_manifest_promotion_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows).sort_values("galaxy").reset_index(drop=True)


def image_panel(paths: str) -> str:
    figures = []
    for path in str(paths).split(";"):
        label = Path(path).stem.replace("_", " ")
        figures.append(
            f"""
            <figure>
              <img src="../{escape(path)}" alt="{escape(label)}" />
              <figcaption>{escape(label)}</figcaption>
            </figure>
            """
        )
    return "\n".join(figures)


def write_html(tasks: pd.DataFrame) -> None:
    cards = []
    for _, row in tasks.iterrows():
        required = "".join(
            f"<li>{escape(field)}</li>"
            for field in str(row["required_review_fields"]).split(";")
        )
        allowed = "".join(
            f"<li>{escape(source)}</li>"
            for source in str(row["allowed_sources"]).split(";")
        )
        cards.append(
            f"""
            <section class="card">
              <h2>{escape(row['galaxy'])}</h2>
              <p class="status">{escape(row['review_status'])}</p>
              <div class="panels">{image_panel(row['preview_png_paths'])}</div>
              <h3>Required Residual-Blind Fields</h3>
              <ol>{required}</ol>
              <h3>Allowed Sources</h3>
              <ul>{allowed}</ul>
            </section>
            """
        )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Paper 8 P0 Visual Review Handoff</title>
  <style>
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f6f6f2;
      color: #1f2933;
    }}
    main {{
      max-width: 1220px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    .notice {{ max-width: 940px; line-height: 1.5; margin-bottom: 24px; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 18px;
    }}
    .card {{
      background: #fff;
      border: 1px solid #d7d7d0;
      border-radius: 8px;
      padding: 18px;
    }}
    h2 {{ margin: 0 0 6px; font-size: 22px; }}
    .status {{
      display: inline-block;
      margin: 0 0 14px;
      padding: 5px 8px;
      border-radius: 6px;
      background: #fff4dc;
      border: 1px solid #e8c36a;
      color: #624b00;
      font-size: 13px;
      font-weight: 700;
    }}
    .panels {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
    }}
    figure {{
      margin: 0;
      overflow: hidden;
      border: 1px solid #e0e0da;
      border-radius: 6px;
      background: #fafaf8;
    }}
    img {{ width: 100%; aspect-ratio: 1 / 1; object-fit: cover; display: block; }}
    figcaption {{ padding: 6px; color: #52616b; font-size: 12px; }}
    h3 {{ margin: 18px 0 8px; font-size: 14px; color: #52616b; text-transform: uppercase; }}
    li {{ line-height: 1.55; }}
    footer {{ margin-top: 24px; color: #52616b; line-height: 1.5; }}
  </style>
</head>
<body>
  <main>
    <h1>Paper 8 P0 Visual Review Handoff</h1>
    <p class="notice">
      This handoff package converts the blocked P0 visual review completion gate
      into concrete reviewer tasks. It is not an accepted morphology manifest,
      not an image classification, and not an endpoint score. Claim boundary:
      <code>{CLAIM_BOUNDARY}</code>.
    </p>
    <div class="grid">
      {''.join(cards)}
    </div>
    <footer>
      Forbidden inputs: {escape('; '.join(FORBIDDEN_INPUTS))}.
    </footer>
  </main>
</body>
</html>
"""
    (REPORTS / "p0_visual_review_handoff.html").write_text(html, encoding="utf-8")


def write_report(tasks: pd.DataFrame, summary: pd.DataFrame) -> None:
    compact = tasks[
        [
            "galaxy",
            "review_status",
            "n_pending_review_fields",
            "accepted_manifest_promotion_allowed",
            "endpoint_scores_computed",
            "claim_boundary",
        ]
    ]
    lines = [
        "# P0 Visual Review Handoff",
        "",
        "This handoff translates the blocked P0 visual review completion gate into",
        "concrete residual-blind reviewer tasks. It is a source-review handoff, not",
        "an accepted morphology manifest, not an image classification, and not an",
        "endpoint score.",
        "",
        "This handoff is not an accepted morphology manifest and not an endpoint score.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Handoff Tasks",
        "",
        markdown_table(compact),
        "",
        "## Forbidden Inputs",
        "",
        "\n".join(f"- {item}" for item in FORBIDDEN_INPUTS),
        "",
        "## Claim Boundary",
        "",
        "The handoff may be used to collect residual-blind human review evidence.",
        "It cannot promote labels, run endpoint scores, or compare Tau Core to",
        "MOND/RAR/TGP/Newtonian baselines.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_visual_review_handoff.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    template = pd.read_csv(DATA / "p0_visual_review_template.csv")
    completion = pd.read_csv(DATA / "p0_visual_review_completion_gate.csv")
    tasks = build_tasks(template, completion)
    summary = pd.DataFrame(
        [
            {
                "handoff_status": "READY_FOR_RESIDUAL_BLIND_HUMAN_REVIEW",
                "n_galaxies": len(tasks),
                "n_blocked_review_rows": int(
                    (tasks["review_status"] == "BLOCKED_VISUAL_REVIEW_PENDING").sum()
                ),
                "n_pending_review_fields_total": int(tasks["n_pending_review_fields"].sum()),
                "accepted_manifest_promotion_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    tasks.to_csv(DATA / "p0_visual_review_handoff_tasks.csv", index=False)
    summary.to_csv(DATA / "p0_visual_review_handoff_summary.csv", index=False)
    write_html(tasks)
    write_report(tasks, summary)
    print("PAPER8_P0_VISUAL_REVIEW_HANDOFF_COMPLETE")


if __name__ == "__main__":
    main()
