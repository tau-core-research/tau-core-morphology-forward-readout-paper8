#!/usr/bin/env python3
"""Build the P0 residual-blind visual review template.

The template consumes the rendered SkyView preview manifest and produces
reviewer-fillable artefacts.  It intentionally does not classify the images,
does not emit accepted morphology labels, and does not compute endpoint scores.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FORM = REPORTS / "p0_visual_review_form.html"
REPORT = REPORTS / "p0_visual_review_template.md"

CLAIM_BOUNDARY = "p0_visual_review_template_not_accepted_label_not_endpoint"
PENDING = "TO_BE_FILLED_RESIDUAL_BLIND"

REVIEW_FIELDS = [
    (
        "reviewer_id",
        "text",
        "Reviewer identifier. Must be filled before any endpoint score is inspected.",
    ),
    (
        "review_timestamp_utc",
        "datetime",
        "UTC timestamp of the residual-blind visual review.",
    ),
    (
        "present_day_morphology_label",
        "controlled_text",
        "Residual-blind present-day morphology label from images/catalogues only.",
    ),
    (
        "outer_disk_lsb_tail_evidence",
        "yes_no_uncertain",
        "Evidence for outer disk, low-surface-brightness extension, scale tail, or diffuse outskirts.",
    ),
    (
        "hi_extent_or_asymmetry_evidence",
        "yes_no_uncertain",
        "Evidence from HI extent/asymmetry sources when available.",
    ),
    (
        "bar_m2_evidence",
        "yes_no_uncertain",
        "Evidence for bar or m=2 structure. Velocity-field support should be noted separately.",
    ),
    (
        "edge_projection_caveat",
        "yes_no_uncertain",
        "Inclination, edge-on, or projection caveat affecting visual morphology.",
    ),
    (
        "vertical_flare_warp_evidence",
        "yes_no_uncertain",
        "Evidence for thick, flared, warped, or vertically extended disk structure.",
    ),
    (
        "compact_bulge_evidence",
        "yes_no_uncertain",
        "Evidence for compact source, central concentration, or bulge-dominated support.",
    ),
    (
        "ring_resonance_evidence",
        "yes_no_uncertain",
        "Evidence for ring or resonance morphology.",
    ),
    (
        "morphological_memory_history_proxy_judgment",
        "controlled_text",
        "Residual-blind judgment about whether current morphology may be an incomplete proxy for readout-relevant history.",
    ),
    (
        "review_confidence",
        "low_medium_high",
        "Reviewer confidence based on source quality, not endpoint performance.",
    ),
    (
        "residual_blind_family_recommendation",
        "controlled_text",
        "Candidate morphology-readout family recommendation for future endpoint use; must not use residuals.",
    ),
    (
        "review_sources_used",
        "semicolon_list",
        "Source panels/catalogues used by the reviewer.",
    ),
    (
        "review_notes",
        "free_text",
        "Short residual-blind notes and caveats.",
    ),
]

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


def build_template_rows(
    previews: pd.DataFrame, requests: pd.DataFrame, queue: pd.DataFrame
) -> pd.DataFrame:
    rows = []
    for galaxy, group in previews.groupby("galaxy"):
        request = requests.loc[requests["galaxy"] == galaxy].iloc[0]
        queue_row = queue.loc[queue["galaxy"] == galaxy].iloc[0]
        rendered = group.loc[group["preview_status"] == "PREVIEW_RENDERED"]
        row = {
            "galaxy": galaxy,
            "inspection_priority_tier": queue_row["inspection_priority_tier"],
            "inspection_priority_score": int(queue_row["inspection_priority_score"]),
            "inspection_focus": request["inspection_focus"],
            "suggested_fov_arcmin": float(request["suggested_fov_arcmin"]),
            "preview_surveys_available": ";".join(sorted(rendered["survey"])),
            "preview_png_paths": ";".join(sorted(rendered["preview_png_path"])),
            "external_source_urls": ";".join(
                [
                    request["ned_url"],
                    request["simbad_url"],
                    request["skyview_dss2_red_url"],
                    request["skyview_2mass_ks_url"],
                    request["skyview_wise_w1_url"],
                ]
            ),
            "accepted_label_output_allowed": False,
            "endpoint_scores_allowed": False,
            "image_classification_performed": False,
            "forbidden_inputs": ";".join(FORBIDDEN_INPUTS),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for field, _, _ in REVIEW_FIELDS:
            row[field] = PENDING
        rows.append(row)
    return pd.DataFrame(rows).sort_values("galaxy").reset_index(drop=True)


def build_schema() -> pd.DataFrame:
    rows = []
    for field, value_type, description in REVIEW_FIELDS:
        rows.append(
            {
                "field": field,
                "value_type": value_type,
                "initial_value": PENDING,
                "residual_blind_required": True,
                "may_use_endpoint_scores": False,
                "description": description,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def image_panels(paths: str) -> str:
    panels = []
    for path in str(paths).split(";"):
        label = Path(path).stem.replace("_", " ")
        panels.append(
            f"""
            <figure>
              <img src="../{escape(path)}" alt="{escape(label)}" />
              <figcaption>{escape(label)}</figcaption>
            </figure>
            """
        )
    return "\n".join(panels)


def field_list() -> str:
    items = []
    for field, value_type, description in REVIEW_FIELDS:
        items.append(
            f"""
            <label>
              <span>{escape(field)} <small>{escape(value_type)}</small></span>
              <textarea placeholder="{escape(PENDING)}"></textarea>
              <em>{escape(description)}</em>
            </label>
            """
        )
    return "\n".join(items)


def write_html(template: pd.DataFrame) -> None:
    cards = []
    for _, row in template.iterrows():
        cards.append(
            f"""
            <section class="card">
              <header>
                <h2>{escape(row['galaxy'])}</h2>
                <p>{escape(row['inspection_focus'])}</p>
              </header>
              <div class="panels">{image_panels(row['preview_png_paths'])}</div>
              <h3>Residual-Blind Review Fields</h3>
              <div class="fields">{field_list()}</div>
            </section>
            """
        )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Paper 8 P0 Visual Review Template</title>
  <style>
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f6f6f2;
      color: #1f2933;
    }}
    main {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    .notice {{ max-width: 980px; line-height: 1.5; margin: 0 0 24px; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 18px;
    }}
    .card {{
      background: #fff;
      border: 1px solid #d9d9d0;
      border-radius: 8px;
      padding: 18px;
    }}
    h2 {{ margin: 0 0 4px; font-size: 22px; }}
    header p {{ margin: 0 0 14px; color: #52616b; line-height: 1.4; }}
    h3 {{ margin: 18px 0 10px; font-size: 14px; text-transform: uppercase; color: #52616b; }}
    .panels {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
    }}
    figure {{ margin: 0; border: 1px solid #e3e3dc; border-radius: 6px; overflow: hidden; background: #fafaf7; }}
    img {{ width: 100%; aspect-ratio: 1 / 1; object-fit: cover; display: block; }}
    figcaption {{ font-size: 12px; padding: 6px; color: #52616b; }}
    .fields {{ display: grid; gap: 10px; }}
    label span {{ display: block; font-weight: 600; font-size: 13px; }}
    small {{ color: #667085; font-weight: 500; }}
    textarea {{
      width: 100%;
      min-height: 36px;
      resize: vertical;
      border: 1px solid #d7d7d0;
      border-radius: 6px;
      padding: 8px;
      box-sizing: border-box;
      background: #fbfbf8;
    }}
    em {{ display: block; margin-top: 3px; color: #667085; font-size: 12px; font-style: normal; line-height: 1.35; }}
    footer {{ margin-top: 24px; color: #52616b; line-height: 1.5; }}
  </style>
</head>
<body>
  <main>
    <h1>Paper 8 P0 Visual Review Template</h1>
    <p class="notice">
      This form embeds the P0 SkyView preview panels for residual-blind human review.
      It is a template only: all review fields remain <code>{PENDING}</code>.
      It does not produce accepted morphology labels, does not classify images,
      and does not compute endpoint scores. Claim boundary:
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
    FORM.write_text(html, encoding="utf-8")


def write_report(template: pd.DataFrame, schema: pd.DataFrame) -> None:
    compact = template[
        [
            "galaxy",
            "inspection_priority_tier",
            "inspection_priority_score",
            "preview_surveys_available",
            "present_day_morphology_label",
            "morphological_memory_history_proxy_judgment",
            "residual_blind_family_recommendation",
            "claim_boundary",
        ]
    ]
    lines = [
        "# P0 Visual Review Template",
        "",
        "This report records the residual-blind visual review template generated",
        "from the P0 SkyView preview panels. The template is a reviewer-fillable",
        "source layer only. It is not an accepted morphology manifest, not an",
        "image classification, and not an endpoint score.",
        "",
        "## Review Template Rows",
        "",
        markdown_table(compact),
        "",
        "## Review Field Schema",
        "",
        markdown_table(schema[["field", "value_type", "initial_value", "may_use_endpoint_scores"]]),
        "",
        "## Forbidden Inputs",
        "",
        "\n".join(f"- {item}" for item in FORBIDDEN_INPUTS),
        "",
        "## Claim Boundary",
        "",
        "All review fields are initialized as residual-blind placeholders. The",
        "template must be filled before endpoint residual gains, required-S_tau",
        "diagnostics, best-fit readout families, MOND/RAR/TGP comparison scores,",
        "or post-hoc family switching are inspected.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_visual_review_template() -> tuple[pd.DataFrame, pd.DataFrame]:
    previews = pd.read_csv(DATA / "p0_skyview_preview_image_manifest.csv")
    requests = pd.read_csv(DATA / "p0_external_imaging_request_manifest.csv")
    queue = pd.read_csv(DATA / "morphology_inspection_queue.csv")
    rendered = previews.loc[previews["preview_status"] == "PREVIEW_RENDERED"].copy()
    if rendered.empty:
        raise RuntimeError("No rendered P0 preview images found.")
    template = build_template_rows(rendered, requests, queue)
    schema = build_schema()
    template.to_csv(DATA / "p0_visual_review_template.csv", index=False)
    schema.to_csv(DATA / "p0_visual_review_field_schema.csv", index=False)
    write_html(template)
    write_report(template, schema)
    return template, schema


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    build_visual_review_template()
    print("PAPER8_P0_VISUAL_REVIEW_TEMPLATE_COMPLETE")


if __name__ == "__main__":
    main()
