#!/usr/bin/env python3
"""Build a consolidated NGC4183 weak-projection control status dashboard.

The dashboard is a coordination artifact. It reads existing source/review/
freeze/accepted/scoring gates and does not create a new formula, fill review
responses, or score an endpoint.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_control_status_dashboard_not_endpoint"
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


def read_first(path: Path) -> pd.Series:
    if not path.exists():
        raise FileNotFoundError(path)
    table = pd.read_csv(path)
    if table.empty:
        raise ValueError(f"empty summary: {path}")
    return table.iloc[0]


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def report_href(report_path: object) -> str:
    path = ROOT / str(report_path)
    return path.resolve().as_uri() if path.exists() else "#"


def stage(
    stage_order: int,
    stage_id: str,
    status: object,
    gate_pass: bool,
    next_gate: object,
    report_path: str,
    evidence: str,
    formula_freeze_allowed: bool = False,
    endpoint_scores_allowed: bool = False,
    construction_reads_vobs: bool = False,
    scoring_reads_vobs: bool = False,
) -> dict[str, object]:
    return {
        "stage_order": stage_order,
        "stage_id": stage_id,
        "stage_status": str(status),
        "gate_pass": gate_pass,
        "next_gate": str(next_gate),
        "evidence": evidence,
        "report_path": report_path,
        "formula_freeze_allowed": formula_freeze_allowed,
        "endpoint_scores_allowed": endpoint_scores_allowed,
        "construction_reads_vobs": construction_reads_vobs,
        "scoring_reads_vobs": scoring_reads_vobs,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    source = read_first(DATA / "ngc4183_mixed_overlay_source_audit_summary.csv")
    profile = read_first(DATA / "ngc4183_tilted_ring_orientation_profile_summary.csv")
    gamma = read_first(DATA / "ngc4183_projection_gamma_upper_bound_summary.csv")
    weak = read_first(DATA / "ngc4183_weak_projection_control_summary.csv")
    packet = read_first(DATA / "ngc4183_tilted_ring_independent_review_summary.csv")
    handoff = read_first(DATA / "ngc4183_tilted_ring_review_handoff_summary.csv")
    intake = read_first(DATA / "ngc4183_tilted_ring_review_response_summary.csv")
    readiness = read_first(DATA / "ngc4183_null_control_freeze_readiness_summary.csv")
    formula = read_first(DATA / "ngc4183_null_control_formula_freeze_summary.csv")
    accepted = read_first(DATA / "ngc4183_accepted_null_control_summary.csv")
    scoring = read_first(DATA / "ngc4183_weak_projection_null_control_scoring_summary.csv")
    roadmap = read_first(DATA / "ngc4183_control_promotion_roadmap_summary.csv")

    stages = pd.DataFrame(
        [
            stage(
                1,
                "source_audit",
                source["source_audit_status"],
                "LOCAL_SOURCE_PRESENT" in str(source["source_audit_status"]),
                source["next_gate"],
                "reports/ngc4183_mixed_overlay_source_audit.md",
                "local Verheijen-Sancisi source cache present",
            ),
            stage(
                2,
                "tilted_ring_profile",
                profile["tilted_ring_profile_status"],
                "EXTRACTED" in str(profile["tilted_ring_profile_status"]),
                profile["next_gate"],
                "reports/ngc4183_tilted_ring_orientation_profile_extraction.md",
                (
                    f"n={int(profile['n_rings'])}; max Delta PA="
                    f"{float(profile['max_abs_pa_drift_deg']):.6g} deg"
                ),
            ),
            stage(
                3,
                "projection_gamma_upper_bound",
                gamma["upper_bound_gate_status"],
                "DERIVED" in str(gamma["upper_bound_gate_status"]),
                gamma["next_gate"],
                "reports/ngc4183_projection_gamma_upper_bound_gate.md",
                f"gamma_bound<={float(gamma['gamma_projection_upper_bound']):.8f}",
            ),
            stage(
                4,
                "weak_projection_control_preflight",
                weak["weak_control_preflight_status"],
                str(weak["recommended_role"]) == "WEAK_PROJECTION_NULL_CONTROL_AFTER_REVIEW",
                weak["next_gate"],
                "reports/ngc4183_weak_projection_control_preflight.md",
                (
                    f"max |Delta v|/v="
                    f"{float(weak['max_velocity_fractional_change']):.8f}"
                ),
            ),
            stage(
                5,
                "independent_review_packet",
                packet["review_packet_status"],
                "PACKET_CREATED" in str(packet["review_packet_status"]),
                packet["next_gate"],
                "reports/ngc4183_tilted_ring_independent_review_packet.md",
                f"n_review_items={int(packet['n_review_items'])}",
            ),
            stage(
                6,
                "review_handoff",
                handoff["handoff_status"],
                "HANDOFF_READY" in str(handoff["handoff_status"]),
                handoff["next_gate"],
                "reports/ngc4183_tilted_ring_review_handoff.md",
                (
                    f"n_tasks={int(handoff['n_tasks'])}; "
                    f"n_visual_sources={int(handoff['n_visual_sources'])}"
                ),
                construction_reads_vobs=truthy(handoff["construction_reads_vobs"]),
            ),
            stage(
                7,
                "review_response_intake",
                intake["review_response_intake_status"],
                truthy(intake["formula_freeze_allowed"]),
                intake["next_gate"],
                "reports/ngc4183_tilted_ring_review_response_intake.md",
                (
                    f"response_received={truthy(intake['response_received'])}; "
                    f"all_required_accepted={truthy(intake['all_required_accepted'])}"
                ),
                formula_freeze_allowed=truthy(intake["formula_freeze_allowed"]),
                endpoint_scores_allowed=truthy(intake["endpoint_scores_allowed"]),
            ),
            stage(
                8,
                "freeze_readiness",
                readiness["null_control_freeze_readiness_status"],
                truthy(readiness["formula_freeze_allowed"]),
                readiness["next_gate"],
                "reports/ngc4183_null_control_freeze_readiness_gate.md",
                f"review_accepts_freeze={truthy(readiness['review_accepts_freeze'])}",
                formula_freeze_allowed=truthy(readiness["formula_freeze_allowed"]),
                endpoint_scores_allowed=truthy(readiness["endpoint_scores_allowed"]),
            ),
            stage(
                9,
                "formula_freeze",
                formula["null_control_formula_freeze_status"],
                truthy(formula["formula_freeze_allowed"]),
                formula["next_gate"],
                "reports/ngc4183_null_control_formula_freeze_gate.md",
                f"gamma_bound={float(formula['gamma_bound']):.8f}",
                formula_freeze_allowed=truthy(formula["formula_freeze_allowed"]),
                endpoint_scores_allowed=truthy(formula["endpoint_scores_allowed"]),
            ),
            stage(
                10,
                "accepted_null_control",
                accepted["accepted_null_control_gate_status"],
                truthy(accepted["accepted_control_allowed"]),
                accepted["next_gate"],
                "reports/ngc4183_accepted_null_control_gate.md",
                f"frozen_lane={accepted['frozen_lane']}",
                endpoint_scores_allowed=truthy(accepted["endpoint_scores_allowed"]),
            ),
            stage(
                11,
                "scoring_gate",
                scoring["scoring_gate_status"],
                truthy(scoring["endpoint_scores_allowed"]),
                scoring["next_gate"],
                "reports/ngc4183_weak_projection_null_control_scoring_gate.md",
                f"primary_blocker={scoring['primary_blocker']}",
                formula_freeze_allowed=truthy(scoring["formula_freeze_allowed"]),
                endpoint_scores_allowed=truthy(scoring["endpoint_scores_allowed"]),
                construction_reads_vobs=truthy(scoring["construction_reads_vobs"]),
                scoring_reads_vobs=truthy(scoring["scoring_reads_vobs"]),
            ),
        ]
    )

    blocking = stages.loc[~stages["gate_pass"]]
    if blocking.empty:
        first_blocker = None
        first_stage = "none"
        first_status = "none"
        first_next_gate = "none"
        next_required_action = "none"
        dashboard_status = "NGC4183_CONTROL_STATUS_DASHBOARD_SCORED_PRELIMINARY_CONTROL"
    else:
        first_blocker = blocking.sort_values("stage_order").iloc[0]
        first_stage = first_blocker["stage_id"]
        first_status = first_blocker["stage_status"]
        first_next_gate = first_blocker["next_gate"]
        next_required_action = str(first_blocker["next_gate"])
        dashboard_status = "NGC4183_CONTROL_STATUS_DASHBOARD_BUILT_NOT_ENDPOINT"
    summary = pd.DataFrame(
        [
            {
                "dashboard_status": dashboard_status,
                "galaxy": GALAXY,
                "n_stages": len(stages),
                "n_pass_or_ready_stages": int(stages["gate_pass"].sum()),
                "n_blocked_stages": int((~stages["gate_pass"]).sum()),
                "first_blocking_stage": first_stage,
                "first_blocking_status": first_status,
                "first_blocking_next_gate": first_next_gate,
                "gamma_projection_upper_bound": float(gamma["gamma_projection_upper_bound"]),
                "max_velocity_fractional_change": float(
                    weak["max_velocity_fractional_change"]
                ),
                "formula_freeze_allowed": bool(stages["formula_freeze_allowed"].any()),
                "endpoint_scores_allowed": bool(stages["endpoint_scores_allowed"].any()),
                "construction_reads_vobs": bool(stages["construction_reads_vobs"].any()),
                "scoring_reads_vobs": bool(stages["scoring_reads_vobs"].any()),
                "roadmap_status": str(roadmap["control_roadmap_status"]),
                "claim_boundary": CLAIM_BOUNDARY,
                "next_required_action": next_required_action,
            }
        ]
    )

    stages.to_csv(DATA / "ngc4183_control_status_dashboard_stages.csv", index=False)
    summary.to_csv(DATA / "ngc4183_control_status_dashboard_summary.csv", index=False)

    if blocking.empty:
        interpretation_lines = [
            "The source-side pipeline predicted a near-carrier weak-projection case,",
            "and that branch has now been carried through accepted source review,",
            "freeze, accepted-control promotion, and interval-control scoring.",
            "The result remains a preliminary single-galaxy control endpoint, not",
            "a point-fit validation and not population validation.",
        ]
    else:
        interpretation_lines = [
            "The source-side pipeline predicts a near-carrier weak-projection case",
            "with a very small projection bound. An accepted independent source",
            "review can be present, but the first blocking stage is the",
            "review-response intake whenever freeze authorization is still absent.",
            "Formula freeze, accepted-control promotion, and scoring remain blocked.",
        ]

    report = [
        "# NGC4183 Control Status Dashboard",
        "",
        f"Status: `{summary.iloc[0]['dashboard_status']}`",
        "",
        "This dashboard consolidates the NGC4183 weak-projection/null-control",
        "path. It is not a formula freeze and not an endpoint score.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Stage Chain",
        "",
        markdown_table(stages),
        "",
        "## Interpretation",
        "",
        *interpretation_lines,
        "",
    ]
    (REPORTS / "ngc4183_control_status_dashboard.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    stage_cards = []
    for _, row in stages.sort_values("stage_order").iterrows():
        css_class = "pass" if truthy(row["gate_pass"]) else "blocked"
        label = "PASS/READY" if truthy(row["gate_pass"]) else "BLOCKED"
        stage_cards.append(
            f"""
            <section class="stage {css_class}">
              <div class="stage-head">
                <span class="badge">{escape(label)}</span>
                <h2>{int(row['stage_order'])}. {escape(str(row['stage_id']))}</h2>
              </div>
              <p><strong>Status:</strong> <code>{escape(str(row['stage_status']))}</code></p>
              <p><strong>Evidence:</strong> {escape(str(row['evidence']))}</p>
              <p><strong>Next gate:</strong> <code>{escape(str(row['next_gate']))}</code></p>
              <p><a href="{escape(report_href(row['report_path']))}">Open source report</a></p>
            </section>
            """
        )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>NGC4183 Control Status Dashboard</title>
  <style>
    body {{
      margin: 32px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #172026;
      background: #f5f7f8;
    }}
    header, .summary, .stage {{
      background: #fff;
      border: 1px solid #d8dee4;
      border-radius: 8px;
      padding: 18px;
      margin-bottom: 16px;
    }}
    h1, h2 {{ margin-top: 0; }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
    }}
    .metric {{
      border: 1px solid #e4e9ef;
      border-radius: 8px;
      padding: 12px;
      background: #fbfcfd;
    }}
    .metric strong {{
      display: block;
      font-size: 12px;
      color: #52606d;
      margin-bottom: 6px;
    }}
    .stage-head {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 8px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.02em;
    }}
    .pass .badge {{ background: #dff6e7; color: #126b35; }}
    .blocked .badge {{ background: #ffe6df; color: #9a3412; }}
    code {{
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }}
    a {{ color: #0b5cad; }}
  </style>
</head>
<body>
  <header>
    <h1>NGC4183 Control Status Dashboard</h1>
    <p>Status: <code>{escape(str(summary.iloc[0]['dashboard_status']))}</code></p>
    <p>This dashboard is not a formula freeze and not an endpoint score.</p>
  </header>
  <section class="summary">
    <h2>Summary</h2>
    <div class="summary-grid">
      <div class="metric"><strong>Stages</strong>{int(summary.iloc[0]['n_stages'])}</div>
      <div class="metric"><strong>Ready</strong>{int(summary.iloc[0]['n_pass_or_ready_stages'])}</div>
      <div class="metric"><strong>Blocked</strong>{int(summary.iloc[0]['n_blocked_stages'])}</div>
      <div class="metric"><strong>First blocker</strong>{escape(str(summary.iloc[0]['first_blocking_stage']))}</div>
      <div class="metric"><strong>Next action</strong>{escape(str(summary.iloc[0]['next_required_action']))}</div>
      <div class="metric"><strong>gamma bound</strong>{float(summary.iloc[0]['gamma_projection_upper_bound']):.8f}</div>
      <div class="metric"><strong>max |Delta v|/v</strong>{float(summary.iloc[0]['max_velocity_fractional_change']):.8f}</div>
      <div class="metric"><strong>Endpoint scores allowed</strong>{escape(str(summary.iloc[0]['endpoint_scores_allowed']))}</div>
    </div>
  </section>
  {''.join(stage_cards)}
</body>
</html>
"""
    (REPORTS / "ngc4183_control_status_dashboard.html").write_text(
        html, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
