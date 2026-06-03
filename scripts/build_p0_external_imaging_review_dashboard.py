#!/usr/bin/env python3
"""Build a local P0 external imaging review dashboard.

The dashboard is an offline HTML launch page for residual-blind image and
catalogue review.  It links to external services but does not download,
classify, or interpret images.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
DASHBOARD = REPORTS / "p0_external_imaging_review_dashboard.html"

CLAIM_BOUNDARY = "p0_imaging_review_dashboard_not_morphology_label_not_endpoint"


def link(url: str, label: str) -> str:
    return f'<a href="{escape(url)}" target="_blank" rel="noreferrer">{escape(label)}</a>'


def source_chips(items: str) -> str:
    return "".join(f"<span>{escape(item)}</span>" for item in str(items).split(";"))


def row_card(row: pd.Series) -> str:
    links = " ".join(
        [
            link(row["ned_url"], "NED"),
            link(row["simbad_url"], "SIMBAD"),
            link(row["skyview_dss2_red_url"], "DSS2 Red"),
            link(row["skyview_2mass_ks_url"], "2MASS-K"),
            link(row["skyview_wise_w1_url"], "WISE W1"),
        ]
    )
    checklist = [
        "present-day morphology label",
        "outer-disk / LSB / tail evidence",
        "HI extent or asymmetry evidence",
        "projection, edge-on, flare, or warp caveat",
        "bar / m=2 evidence if requested",
        "morphological memory/history proxy judgment",
        "residual-blind family recommendation for future endpoint",
    ]
    checklist_html = "".join(
        f"<li><label><input type=\"checkbox\" /> {escape(item)}</label></li>"
        for item in checklist
    )
    return f"""
    <section class="card">
      <header>
        <h2>{escape(row['galaxy'])}</h2>
        <p class="tag">{escape(row['inspection_focus'])}</p>
      </header>
      <dl class="meta">
        <div><dt>RA</dt><dd>{float(row['ra_deg']):.5f}</dd></div>
        <div><dt>Dec</dt><dd>{float(row['dec_deg']):.5f}</dd></div>
        <div><dt>FOV</dt><dd>{float(row['suggested_fov_arcmin']):.3f} arcmin</dd></div>
        <div><dt>Inclination</dt><dd>{float(row['sparc_inclination_deg']):.1f} deg</dd></div>
        <div><dt>S4G components</dt><dd>{escape(str(row['s4g_model_components']))}</dd></div>
      </dl>
      <div class="links">{links}</div>
      <h3>Requested Observables</h3>
      <div class="chips">{source_chips(row['requested_external_sources'])}</div>
      <h3>Blank Review Checklist</h3>
      <ul class="checklist">{checklist_html}</ul>
    </section>
    """


def build_dashboard() -> pd.DataFrame:
    manifest = pd.read_csv(DATA / "p0_external_imaging_request_manifest.csv")
    manifest = manifest.sort_values("galaxy").reset_index(drop=True)
    cards = "\n".join(row_card(row) for _, row in manifest.iterrows())
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Paper 8 P0 External Imaging Review Dashboard</title>
  <style>
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #1f2933;
      background: #f7f7f4;
    }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 30px;
    }}
    .notice {{
      max-width: 900px;
      margin: 0 0 24px;
      line-height: 1.5;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
    }}
    .card {{
      background: #fff;
      border: 1px solid #d7d7d0;
      border-radius: 8px;
      padding: 18px;
      box-shadow: 0 1px 2px rgba(0,0,0,.04);
    }}
    h2 {{
      margin: 0 0 4px;
      font-size: 22px;
    }}
    h3 {{
      margin: 16px 0 8px;
      font-size: 14px;
      text-transform: uppercase;
      letter-spacing: .04em;
      color: #52616b;
    }}
    .tag {{
      margin: 0;
      color: #52616b;
      line-height: 1.4;
    }}
    .meta {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin: 16px 0;
    }}
    .meta div {{
      border-top: 1px solid #ecece7;
      padding-top: 8px;
    }}
    dt {{
      font-size: 12px;
      color: #6b7280;
    }}
    dd {{
      margin: 2px 0 0;
      font-weight: 600;
    }}
    .links {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    a, .chips span {{
      display: inline-block;
      padding: 6px 8px;
      border: 1px solid #c7d2da;
      border-radius: 6px;
      color: #0f4c81;
      background: #f4f9fc;
      text-decoration: none;
      font-size: 13px;
    }}
    .chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .checklist {{
      padding-left: 20px;
      line-height: 1.75;
    }}
    footer {{
      margin-top: 24px;
      color: #52616b;
      font-size: 13px;
    }}
  </style>
</head>
<body>
  <main>
    <h1>Paper 8 P0 External Imaging Review Dashboard</h1>
    <p class="notice">
      This is a residual-blind review launch page. It links to external image and
      catalogue sources for the four P0 morphology-inspection targets. This dashboard does not classify images, does not produce accepted morphology labels, and does not compute endpoint scores. Claim boundary: <code>{CLAIM_BOUNDARY}</code>.
    </p>
    <div class="grid">
      {cards}
    </div>
    <footer>
      Forbidden inputs: endpoint residual gain, required-S_tau as a label input,
      best-fit readout family as accepted morphology evidence, and post-hoc
      family switching after endpoint scoring.
    </footer>
  </main>
</body>
</html>
"""
    DASHBOARD.write_text(html, encoding="utf-8")
    index = pd.DataFrame(
        [
            {
                "dashboard_path": str(DASHBOARD.relative_to(ROOT)),
                "n_galaxies": len(manifest),
                "galaxies": ";".join(manifest["galaxy"]),
                "claim_boundary": CLAIM_BOUNDARY,
                "accepted_label_output_allowed": False,
                "endpoint_scores_allowed": False,
            }
        ]
    )
    index.to_csv(DATA / "p0_external_imaging_review_dashboard_index.csv", index=False)
    return index


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    build_dashboard()
    print("PAPER8_P0_EXTERNAL_IMAGING_REVIEW_DASHBOARD_COMPLETE")


if __name__ == "__main__":
    main()
