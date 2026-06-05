#!/usr/bin/env python3
"""Build the NGC4088 residual-blind source-review packet.

This packet separates literature-supported facts, first-pass internal
digitization fields, and still-blocked promotion inputs for the
K_warp_history_coupled readout subfamily. It is not an endpoint scorer.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
LITERATURE = ROOT / "data" / "external" / "literature"
CLAIM_BOUNDARY = "ngc4088_source_review_packet_not_endpoint"


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


def build_literature_fields() -> pd.DataFrame:
    rows = [
        {
            "field_id": "VS2001_PA_INCLINATION_HI_SIZE",
            "observable": "global_hi_geometry",
            "value": "PA=231deg; inclination=69deg; HI_diameter=8.5arcmin",
            "source": "Verheijen_Sancisi_2001_Ursa_Major_HI",
            "source_file": "2001_verheijen_sancisi_ursa_major_hi.txt",
            "source_line_refs": "11368-11500",
            "support_status": "ACCEPTED_LITERATURE_SOURCE_FIELD",
            "promotion_use": "supports geometry normalization and projection context; not sufficient for warp-onset acceptance",
        },
        {
            "field_id": "VS2001_STRONG_DISTORTION",
            "observable": "strong_optical_kinematic_distortion",
            "value": "strongly_distorted_disk",
            "source": "Verheijen_Sancisi_2001_Ursa_Major_HI",
            "source_file": "2001_verheijen_sancisi_ursa_major_hi.txt",
            "source_line_refs": "11498-11509;7201-7210",
            "support_status": "ACCEPTED_LITERATURE_SOURCE_FIELD",
            "promotion_use": "supports warp/history-coupled review and rejects quiet-thick-disk interpretation",
        },
        {
            "field_id": "VS2001_PV_ASYMMETRY",
            "observable": "pv_asymmetry",
            "value": "strong_position_velocity_asymmetry",
            "source": "Verheijen_Sancisi_2001_Ursa_Major_HI",
            "source_file": "2001_verheijen_sancisi_ursa_major_hi.txt",
            "source_line_refs": "11500-11505;7211-7224",
            "support_status": "ACCEPTED_LITERATURE_SOURCE_FIELD",
            "promotion_use": "supports HI asymmetry/history layer; not a numeric q_warp amplitude by itself",
        },
        {
            "field_id": "VS2001_ASYMMETRIC_WARP",
            "observable": "asymmetric_warp_and_side_pa_change",
            "value": "warp_asymmetric; PA changes more in southern than northern part",
            "source": "Verheijen_Sancisi_2001_Ursa_Major_HI",
            "source_file": "2001_verheijen_sancisi_ursa_major_hi.txt",
            "source_line_refs": "11503-11509",
            "support_status": "ACCEPTED_LITERATURE_SOURCE_FIELD",
            "promotion_use": "supports warp-asymmetry source review; numeric onset and q_warp still require measurement/review",
        },
        {
            "field_id": "VS2001_COMPANION_CONTEXT",
            "observable": "near_companion_context",
            "value": "NGC4085 located 10arcmin south",
            "source": "Verheijen_Sancisi_2001_Ursa_Major_HI",
            "source_file": "2001_verheijen_sancisi_ursa_major_hi.txt",
            "source_line_refs": "11511-11515",
            "support_status": "ACCEPTED_LITERATURE_SOURCE_FIELD",
            "promotion_use": "supports morphology-memory/history context; does not fix epsilon_cross numeric bound",
        },
    ]
    df = pd.DataFrame(rows)
    df["source_path"] = df["source_file"].map(lambda name: str(LITERATURE / name))
    df["source_exists"] = df["source_path"].map(lambda path: Path(path).exists())
    df["endpoint_scores_allowed"] = False
    df["claim_boundary"] = CLAIM_BOUNDARY
    return df


def build_gate_decisions() -> pd.DataFrame:
    xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    qwarp = pd.read_csv(DATA / "s4g75_ngc4088_qwarp_first_pass_response.csv").iloc[0]
    memory = pd.read_csv(DATA / "s4g75_ngc4088_memory_history_first_pass_response.csv").iloc[0]
    h4 = pd.read_csv(DATA / "s4g75_ngc4088_h4_interaction_context_review_summary.csv").iloc[0]
    eps = pd.read_csv(DATA / "s4g75_ngc4088_epsilon_cross_source_bound_summary.csv").iloc[0]
    rows = [
        {
            "gate_id": "G1_WARP_ONSET",
            "needed_observable": "x_warp_onset_value",
            "current_value": xw["x_warp_onset"],
            "current_status": "PROTOCOL_NUMERIC_READY_REVIEW_REQUIRED",
            "decision": "SOURCE_REVIEW_READY_NOT_ACCEPTED",
            "reason": "channel-map digitization validates dimensionally, but independent source review is still required before accepted-manifest promotion",
        },
        {
            "gate_id": "G2_Q_WARP",
            "needed_observable": "q_warp_measured_first_pass",
            "current_value": qwarp["q_warp_measured"],
            "current_status": qwarp["response_status"],
            "decision": "SOURCE_REVIEW_REQUIRED",
            "reason": "first-pass q_warp comes from internal digitization response and is not yet independently accepted",
        },
        {
            "gate_id": "G3_MEMORY_HISTORY",
            "needed_observable": "m_history_warp_first_pass",
            "current_value": memory["m_history_warp"],
            "current_status": memory["response_status"],
            "decision": "SOURCE_REVIEW_REQUIRED",
            "reason": "memory/history response is partly filled, but one required component remains unaccepted",
        },
        {
            "gate_id": "G4_INTERACTION_CONTEXT",
            "needed_observable": "h4_interaction_context",
            "current_value": h4["accepted_h4_interaction_context"],
            "current_status": h4["h4_review_status"],
            "decision": "ACCEPTED_SUPPORT_FIELD",
            "reason": "interaction/history context is source-reviewed and can support the subfamily, but cannot alone promote it",
        },
        {
            "gate_id": "G5_EPSILON_CROSS_BOUND",
            "needed_observable": "epsilon_cross_numeric_bound",
            "current_value": "blocked",
            "current_status": eps["epsilon_cross_status"],
            "decision": "BLOCKED_UNTIL_G2_G3_ACCEPTED",
            "reason": "numeric epsilon_cross bound depends on accepted q_warp and accepted memory/history inputs",
        },
    ]
    df = pd.DataFrame(rows)
    df["endpoint_scores_allowed"] = False
    df["claim_boundary"] = CLAIM_BOUNDARY
    return df


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    lit = build_literature_fields()
    gates = build_gate_decisions()
    lit.to_csv(DATA / "ngc4088_source_review_literature_fields.csv", index=False)
    gates.to_csv(DATA / "ngc4088_source_review_gate_decisions.csv", index=False)
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "proposed_readout_subfamily": "K_warp_history_coupled",
                "n_literature_fields": len(lit),
                "n_accepted_literature_fields": int(
                    lit["support_status"].eq("ACCEPTED_LITERATURE_SOURCE_FIELD").sum()
                ),
                "n_gate_decisions": len(gates),
                "n_accepted_support_fields": int(gates["decision"].eq("ACCEPTED_SUPPORT_FIELD").sum()),
                "n_review_required": int(gates["decision"].str.contains("REVIEW", na=False).sum()),
                "n_blocked": int(gates["decision"].str.contains("BLOCKED", na=False).sum()),
                "accepted_subfamily_label_promoted": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(DATA / "ngc4088_source_review_packet_summary.csv", index=False)
    report = [
        "# NGC4088 Source-Review Packet",
        "",
        "This packet separates accepted literature facts from first-pass internal",
        "digitization fields for the K_warp_history_coupled readout subfamily.",
        "It does not score rotation endpoints and does not promote an accepted",
        "subfamily label.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Literature Fields",
        "",
        markdown_table(
            lit[
                [
                    "field_id",
                    "observable",
                    "value",
                    "source_line_refs",
                    "support_status",
                    "promotion_use",
                    "claim_boundary",
                ]
            ]
        ),
        "",
        "## Gate Decisions",
        "",
        markdown_table(
            gates[
                [
                    "gate_id",
                    "needed_observable",
                    "current_value",
                    "current_status",
                    "decision",
                    "reason",
                    "claim_boundary",
                ]
            ]
        ),
        "",
        "## Verdict",
        "",
        "The literature layer strongly supports a warp/history-coupled review for",
        "NGC4088. It does not yet authorize endpoint-safe subfamily use. The",
        "remaining promotion blockers are independent review of x_warp, q_warp,",
        "and memory/history, followed by a rerun of the epsilon_cross bound.",
        "",
    ]
    (REPORTS / "ngc4088_source_review_packet.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
