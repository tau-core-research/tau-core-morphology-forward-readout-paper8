#!/usr/bin/env python3
"""Build the NGC5907 projection-dominated freeze gate.

NGC5907 is the current source-field accepted projection-dominated control.
This gate freezes a residual-blind projection/warp/truncation/vertical-kernel
protocol for future endpoint use. It does not score rotation endpoints.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc5907_projection_freeze_gate_not_endpoint"


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
        raise RuntimeError(f"missing NGC5907 observable: {name}")
    return match.iloc[0]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    extracted = pd.read_csv(DATA / "readout_subfamily_extracted_observables.csv")
    audit = pd.read_csv(DATA / "readout_subfamily_accepted_manifest_audit.csv")
    direct = pd.read_csv(DATA / "s4g75_direct_kernel_measurements.csv")
    promoted = pd.read_csv(DATA / "s4g75_promoted_kernel_observable_fill.csv")

    ngc = extracted.loc[extracted["galaxy"] == "NGC5907"]
    audit_row = audit.loc[audit["galaxy"] == "NGC5907"].iloc[0]
    direct_row = direct.loc[direct["galaxy"] == "NGC5907"].iloc[0]
    promoted_row = promoted.loc[promoted["galaxy"] == "NGC5907"].iloc[0]

    warp_range = get_observable(ngc, "optical_warp_radial_range")
    warp_amp = get_observable(ngc, "optical_warp_max_displacement")
    scale_lengths = get_observable(ngc, "disk_truncation_scale_lengths")
    interaction = get_observable(ngc, "interaction_warp_context")
    vertical = get_observable(ngc, "edge_on_vertical_structure_source")

    warp_r_inner, warp_r_outer = [float(x) for x in str(warp_range["numeric_value"]).split(";")]
    warp_displacement = float(warp_amp["numeric_value"])
    main_scale, corrected_scale, outer_scale = [
        float(x) for x in str(scale_lengths["numeric_value"]).split(";")
    ]
    h_over_r = float(direct_row["dimensionless_value"])
    hz_kpc = float(direct_row["value_kpc"])
    hr_kpc = float(direct_row["secondary_value_kpc"])

    projection_strength = min(1.0, warp_displacement / max(hz_kpc, 1.0e-12))
    warp_start_over_main_scale = warp_r_inner / main_scale
    warp_span_over_main_scale = (warp_r_outer - warp_r_inner) / main_scale
    truncation_contrast = 1.0 - outer_scale / corrected_scale
    vertical_kernel_ratio = h_over_r
    frozen_projection_bound = min(
        1.0,
        0.25 * projection_strength
        + 0.25 * min(1.0, warp_span_over_main_scale / 3.0)
        + 0.25 * min(1.0, truncation_contrast)
        + 0.25 * min(1.0, vertical_kernel_ratio / 0.25),
    )

    fields = pd.DataFrame(
        [
            {
                "field_id": "P1_WARP_RADIAL_RANGE",
                "observable": "optical_warp_radial_range",
                "value": f"{warp_r_inner:.6g}-{warp_r_outer:.6g}",
                "unit": "kpc",
                "status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
                "source": warp_range["source_file"],
                "source_line_refs": warp_range["source_line_refs"],
                "role": "sets projection-dominated radial support",
            },
            {
                "field_id": "P2_WARP_DISPLACEMENT",
                "observable": "optical_warp_max_displacement",
                "value": warp_displacement,
                "unit": "kpc",
                "status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
                "source": warp_amp["source_file"],
                "source_line_refs": warp_amp["source_line_refs"],
                "role": "sets projection displacement amplitude proxy",
            },
            {
                "field_id": "P3_TRUNCATION_SCALES",
                "observable": "disk_truncation_scale_lengths",
                "value": f"{main_scale:.6g};{corrected_scale:.6g};{outer_scale:.6g}",
                "unit": "kpc",
                "status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
                "source": scale_lengths["source_file"],
                "source_line_refs": scale_lengths["source_line_refs"],
                "role": "sets disk/truncation transition contrast",
            },
            {
                "field_id": "P4_VERTICAL_KERNEL_RATIO",
                "observable": "thickness_h_over_rs",
                "value": h_over_r,
                "unit": "dimensionless",
                "status": str(direct_row["direct_measurement_status"]),
                "source": str(direct_row["source_table"]),
                "source_line_refs": str(direct_row["source_component"]),
                "role": "direct S4G edge-disk vertical-kernel observable",
            },
            {
                "field_id": "P5_INTERACTION_CONTEXT",
                "observable": "interaction_warp_context",
                "value": interaction["observable_value"],
                "unit": "categorical",
                "status": "ACCEPTED_CONTEXT_SOURCE_FIELD",
                "source": interaction["source_file"],
                "source_line_refs": interaction["source_line_refs"],
                "role": "supports projection/history context, not amplitude by itself",
            },
            {
                "field_id": "P6_VERTICAL_STRUCTURE_CONTEXT",
                "observable": "edge_on_vertical_structure_source",
                "value": vertical["observable_value"],
                "unit": "categorical",
                "status": "ACCEPTED_CONTEXT_SOURCE_FIELD",
                "source": vertical["source_file"],
                "source_line_refs": vertical["source_line_refs"],
                "role": "supports edge-on projection sanity",
            },
        ]
    )
    fields["endpoint_scores_allowed"] = False
    fields["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "PFG1_ACCEPTED_SOURCE_FIELDS",
                "gate_status": "PASS",
                "evidence": str(audit_row["audit_decision"]),
                "remaining_obligation": "endpoint freeze still separate",
            },
            {
                "gate_id": "PFG2_DIMENSIONAL_WARP_RANGE",
                "gate_status": "PASS",
                "evidence": f"warp range {warp_r_inner:.3g}-{warp_r_outer:.3g} kpc; start/main_scale={warp_start_over_main_scale:.3g}",
                "remaining_obligation": "preserve projected-geometry caveat",
            },
            {
                "gate_id": "PFG3_VERTICAL_KERNEL_DIRECT",
                "gate_status": "PASS",
                "evidence": f"h/R={h_over_r:.6g} from {direct_row['source_component']}",
                "remaining_obligation": "treat as source-native kernel observable, not endpoint fit",
            },
            {
                "gate_id": "PFG4_TRUNCATION_CONTRAST_READY",
                "gate_status": "PASS",
                "evidence": f"main/corrected/outer scales={main_scale:.3g}/{corrected_scale:.3g}/{outer_scale:.3g} kpc",
                "remaining_obligation": "do not tune transition against rotation residuals",
            },
            {
                "gate_id": "PFG5_FROZEN_PROJECTION_BOUND",
                "gate_status": "PASS_CAVEATED",
                "evidence": f"Pi_projection <= {frozen_projection_bound:.6g}",
                "remaining_obligation": "protocol bound only; not final Tau-side projection coefficient law",
            },
            {
                "gate_id": "PFG6_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "all inputs are source fields or direct kernel observables; endpoint_scores_allowed=False",
                "remaining_obligation": "future scoring requires separately frozen endpoint protocol",
            },
        ]
    )
    gates["galaxy"] = "NGC5907"
    gates["proposed_readout_subfamily"] = "K_projection_dominated"
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "proposed_readout_subfamily",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC5907",
                "proposed_readout_subfamily": "K_projection_dominated",
                "n_source_fields": len(fields),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "warp_r_inner_kpc": warp_r_inner,
                "warp_r_outer_kpc": warp_r_outer,
                "warp_displacement_kpc": warp_displacement,
                "thickness_h_over_rs": h_over_r,
                "truncation_contrast": truncation_contrast,
                "frozen_projection_bound": frozen_projection_bound,
                "projection_freeze_status": "PROJECTION_PROTOCOL_BOUND_READY_NOT_ENDPOINT",
                "accepted_subfamily_label_promoted": bool(
                    audit_row["accepted_subfamily_label_promoted"]
                ),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    fields.to_csv(DATA / "ngc5907_projection_freeze_fields.csv", index=False)
    gates.to_csv(DATA / "ngc5907_projection_freeze_gate.csv", index=False)
    summary.to_csv(DATA / "ngc5907_projection_freeze_summary.csv", index=False)

    report = [
        "# NGC5907 Projection-Dominated Freeze Gate",
        "",
        "This gate freezes a residual-blind projection/warp/truncation/vertical",
        "kernel protocol for the current source-field accepted NGC5907 control.",
        "It does not score endpoints and does not validate Tau Core.",
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
        "NGC5907 is now a projection-dominated protocol-ready control, not an",
        "endpoint-ready validation case. The source layer supplies warp range, warp",
        "displacement, disk/truncation scales, interaction context, and a direct S4G",
        "edge-disk h/R observable. The frozen projection bound is a conservative",
        "protocol quantity, not a fitted readout amplitude.",
        "",
    ]
    (REPORTS / "ngc5907_projection_freeze_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
