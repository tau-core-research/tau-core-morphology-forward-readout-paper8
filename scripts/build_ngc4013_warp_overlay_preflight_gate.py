#!/usr/bin/env python3
"""Build an NGC4013 warp/overlay preflight gate.

NGC4013 is not endpoint-ready. Existing residual-blind source fields pressure
the current compact-only proxy toward a disk/warp/vertical-overlay review. This
script records that pressure and freezes the missing obligations before any
endpoint scoring or formula promotion.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4013_warp_overlay_preflight_not_endpoint"


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


def get_observable(rows: pd.DataFrame, name: str) -> pd.Series:
    match = rows.loc[rows["observable_name"] == name]
    if match.empty:
        raise RuntimeError(f"missing NGC4013 observable: {name}")
    return match.iloc[0]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    extracted = pd.read_csv(DATA / "readout_subfamily_extracted_observables.csv")
    audit = pd.read_csv(DATA / "readout_subfamily_accepted_manifest_audit.csv")
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    scores = pd.read_csv(DATA / "s4g75_promoted_kernel_endpoint_scores.csv")
    source_summary_path = DATA / "ngc4013_compact_overlay_source_summary.csv"
    source_summary = (
        pd.read_csv(source_summary_path).iloc[0] if source_summary_path.exists() else None
    )

    rows = extracted.loc[extracted["galaxy"] == "NGC4013"]
    audit_row = audit.loc[audit["galaxy"] == "NGC4013"].iloc[0]
    manifest_row = manifest.loc[manifest["galaxy"] == "NGC4013"].iloc[0]
    score_row = scores.loc[scores["galaxy"] == "NGC4013"].iloc[0]

    overlay = get_observable(rows, "compact_only_overlay_flag")
    onset = get_observable(rows, "line_of_sight_warp_onset")
    scaleheight = get_observable(rows, "final_hi_scaleheight_central")
    lag = get_observable(rows, "rotational_lag_profile")

    warp_onset_kpc = float(onset["numeric_value"])
    central_hi_scaleheight_pc = float(scaleheight["numeric_value"])
    central_hi_scaleheight_kpc = central_hi_scaleheight_pc / 1000.0
    scale_radius_proxy_kpc = float(manifest_row["scale_radius_proxy_kpc"])
    h_over_rs_central = central_hi_scaleheight_kpc / scale_radius_proxy_kpc
    s4g_edge_h_over_r = (
        float(source_summary["s4g_edge_disk_h_over_r"]) if source_summary is not None else float("nan")
    )
    compact_lane_decision = (
        str(source_summary["compact_lane_decision"])
        if source_summary is not None
        else "COMPACT_ENDPOINT_UNRESOLVED_SOURCE_ACQUISITION_REQUIRED"
    )

    fields = pd.DataFrame(
        [
            {
                "field_id": "N4013_F1_OVERLAY_PRESSURE",
                "observable": "compact_only_overlay_flag",
                "value": overlay["observable_value"],
                "numeric_value": "",
                "unit": "categorical",
                "status": "RECLASSIFICATION_PRESSURE_SOURCE_FIELD",
                "source": overlay["source_file"],
                "source_line_refs": overlay["source_line_refs"],
                "role": "blocks compact-only endpoint use and motivates warp/overlay review",
            },
            {
                "field_id": "N4013_F2_WARP_ONSET",
                "observable": "line_of_sight_warp_onset",
                "value": warp_onset_kpc,
                "numeric_value": warp_onset_kpc,
                "unit": "kpc",
                "status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
                "source": onset["source_file"],
                "source_line_refs": onset["source_line_refs"],
                "role": "sets first-pass inner support for a future warp/overlay window",
            },
            {
                "field_id": "N4013_F3_CENTRAL_HI_SCALEHEIGHT",
                "observable": "final_hi_scaleheight_central",
                "value": central_hi_scaleheight_pc,
                "numeric_value": central_hi_scaleheight_kpc,
                "unit": "kpc",
                "status": "ACCEPTED_NUMERIC_SOURCE_FIELD_CENTRAL_ONLY",
                "source": scaleheight["source_file"],
                "source_line_refs": scaleheight["source_line_refs"],
                "role": "supplies central vertical kernel proxy, not full radial vertical profile",
            },
            {
                "field_id": "N4013_F4_ROTATIONAL_LAG",
                "observable": "rotational_lag_profile",
                "value": lag["observable_value"],
                "numeric_value": "",
                "unit": "profile_context",
                "status": "ACCEPTED_CONTEXT_SOURCE_FIELD",
                "source": lag["source_file"],
                "source_line_refs": lag["source_line_refs"],
                "role": "supports disk-halo/vertical-overlay readout review",
            },
        ]
    )
    fields["endpoint_scores_allowed"] = False
    fields["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4013_PG1_CURRENT_COMPACT_LABEL_FAILS_AUDIT",
                "gate_status": "PASS",
                "evidence": f"audit decision={audit_row['audit_decision']}; matched compact rank={int(score_row['matched_family_rank'])}",
                "remaining_obligation": "do not use compact-only label for endpoint promotion",
            },
            {
                "gate_id": "N4013_PG2_WARP_OVERLAY_SOURCE_PRESSURE",
                "gate_status": "PASS",
                "evidence": str(overlay["observable_value"]),
                "remaining_obligation": "define an explicit replacement readout subfamily",
            },
            {
                "gate_id": "N4013_PG3_WARP_ONSET_AVAILABLE",
                "gate_status": "PASS",
                "evidence": f"line-of-sight warp onset near {warp_onset_kpc:.3g} kpc",
                "remaining_obligation": "outer warp/projection window still missing",
            },
            {
                "gate_id": "N4013_PG4_VERTICAL_KERNEL_PARTIAL",
                "gate_status": "PASS_CAVEATED",
                "evidence": f"central HI scaleheight={central_hi_scaleheight_kpc:.3g} kpc; h/Rs proxy={h_over_rs_central:.5f}",
                "remaining_obligation": "radial vertical profile or endpoint-freeze vertical rule required",
            },
            {
                "gate_id": "N4013_PG5_ROTATIONAL_LAG_CONTEXT",
                "gate_status": "PASS_CAVEATED",
                "evidence": str(lag["observable_value"]),
                "remaining_obligation": "lag profile must be mapped into a source-side readout kernel before scoring",
            },
            {
                "gate_id": "N4013_PG6_COMPACT_LANE_SOURCE_REVIEW",
                "gate_status": "PASS",
                "evidence": compact_lane_decision,
                "remaining_obligation": "compact endpoint lane rejected unless later independent compact support evidence overturns this review",
            },
            {
                "gate_id": "N4013_PG7_ENDPOINT_FREEZE_BLOCKED",
                "gate_status": "BLOCKED",
                "evidence": "no full source-frozen warp/projection radial window and no accepted overlay formula",
                "remaining_obligation": "freeze replacement subfamily formula before any endpoint score",
            },
        ]
    )
    gates["galaxy"] = "NGC4013"
    gates["preflight_subfamily_candidate"] = "K_warp_vertical_overlay_candidate"
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "preflight_subfamily_candidate",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "current_manifest_family": str(manifest_row["formula_family"]),
                "preflight_subfamily_candidate": "K_warp_vertical_overlay_candidate",
                "current_matched_rmse": float(score_row["rmse_matched_family"]),
                "best_existing_family": str(score_row["best_family"]),
                "best_existing_family_rank_of_current": int(score_row["matched_family_rank"]),
                "warp_onset_kpc": warp_onset_kpc,
                "central_hi_scaleheight_kpc": central_hi_scaleheight_kpc,
                "central_h_over_rs_proxy": h_over_rs_central,
                "s4g_edge_disk_h_over_r": s4g_edge_h_over_r,
                "compact_lane_decision": compact_lane_decision,
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "preflight_status": "COMPACT_REJECTED_WARP_OVERLAY_PREFLIGHT_READY_FORMULA_BLOCKED",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    fields.to_csv(DATA / "ngc4013_warp_overlay_preflight_fields.csv", index=False)
    gates.to_csv(DATA / "ngc4013_warp_overlay_preflight_gate.csv", index=False)
    summary.to_csv(DATA / "ngc4013_warp_overlay_preflight_summary.csv", index=False)

    report = [
        "# NGC4013 Warp/Overlay Preflight Gate",
        "",
        "This gate does not score an endpoint. It records that residual-blind",
        "source evidence pressures the current compact-only label toward a",
        "warp/vertical-overlay readout review.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Source Fields",
        "",
        markdown_table(fields),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Interpretation",
        "",
        "NGC4013 is not an accepted endpoint row. The current compact-only lane",
        "performs poorly against the wrong-family controls, and the source layer",
        "contains direct warp, scaleheight, rotational-lag, and negative compact",
        "support evidence. The correct next step is a replacement warp/vertical",
        "overlay readout subfamily and formula-freeze protocol, not endpoint",
        "scoring.",
        "",
    ]
    (REPORTS / "ngc4013_warp_overlay_preflight_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
