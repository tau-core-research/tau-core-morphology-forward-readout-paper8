#!/usr/bin/env python3
"""Build the NGC7331 outer-warp/vertical caveat gate.

This is a residual-blind source gate. It maps the existing Patra vertical
source fields into dimensionless h/Rs observables and records independent
outer-warp literature context. It does not score rotation curves.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc7331_outer_warp_vertical_caveat_gate_not_endpoint"


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
        raise RuntimeError(f"missing NGC7331 observable: {name}")
    return match.iloc[0]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    extracted = pd.read_csv(DATA / "readout_subfamily_extracted_observables.csv")
    audit = pd.read_csv(DATA / "readout_subfamily_accepted_manifest_audit.csv")
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    queue = pd.read_csv(DATA / "mixed_readout_candidate_acquisition_queue.csv")

    ngc = extracted.loc[extracted["galaxy"].eq("NGC7331")]
    audit_row = audit.loc[audit["galaxy"].eq("NGC7331")].iloc[0]
    sparc_row = sparc.loc[sparc["Galaxy"].eq("NGC7331")].iloc[0]
    queue_row = queue.loc[queue["galaxy"].eq("NGC7331")].iloc[0]

    scale_range = get_observable(ngc, "molecular_scaleheight_range")
    hwhm = get_observable(ngc, "edge_on_projected_hwhm")
    inc_review = get_observable(ngc, "inclination_review_range")
    warp_caveat = get_observable(ngc, "possible_outer_warp_caveat")

    h_min_pc, h_max_pc = [float(x) for x in str(scale_range["numeric_value"]).split(";")]
    h_mid_kpc = 0.5 * (h_min_pc + h_max_pc) / 1000.0
    h_min_kpc = h_min_pc / 1000.0
    h_max_kpc = h_max_pc / 1000.0
    projected_hwhm_kpc = float(hwhm["numeric_value"]) / 1000.0
    rdisk_kpc = float(sparc_row["Rdisk_kpc"])
    rhi_kpc = float(sparc_row["RHI_kpc"])

    intrinsic_h_over_rs_mid = h_mid_kpc / rdisk_kpc
    projected_hwhm_over_rs = projected_hwhm_kpc / rdisk_kpc
    projected_hwhm_over_rhi = projected_hwhm_kpc / rhi_kpc
    vertical_activation = min(1.0, 0.5 * intrinsic_h_over_rs_mid / 0.05 + 0.5 * projected_hwhm_over_rs / 0.15)

    # This is source context, not a numeric warp kernel. The Bosma review page
    # records NGC7331 as a case with an HI warp consistent in direct
    # distribution and tilted-ring/kinematic inference.
    bosma_url = "https://ned.ipac.caltech.edu/level5/March05/Bosma/Bosma5_5.html"
    bosma_context = (
        "Bosma review records NGC7331 as just edge-on enough to see the warp "
        "directly in the HI distribution and just face-on enough to infer it "
        "from kinematics; these are consistent with each other."
    )

    fields = pd.DataFrame(
        [
            {
                "field_id": "N7331_V1_MOLECULAR_SCALEHEIGHT_RANGE",
                "observable": "molecular_scaleheight_range",
                "value": f"{h_min_kpc:.6g}-{h_max_kpc:.6g}",
                "unit": "kpc",
                "status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
                "source": str(scale_range["source_file"]),
                "source_line_refs": str(scale_range["source_line_refs"]),
                "role": "sets intrinsic vertical thickness range",
            },
            {
                "field_id": "N7331_V2_EDGE_ON_PROJECTED_HWHM",
                "observable": "edge_on_projected_hwhm",
                "value": projected_hwhm_kpc,
                "unit": "kpc",
                "status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
                "source": str(hwhm["source_file"]),
                "source_line_refs": str(hwhm["source_line_refs"]),
                "role": "sets projected observable vertical thickness",
            },
            {
                "field_id": "N7331_V3_H_OVER_RS_INTRINSIC_MID",
                "observable": "intrinsic_h_over_Rs_mid",
                "value": intrinsic_h_over_rs_mid,
                "unit": "dimensionless",
                "status": "DERIVED_FROM_ACCEPTED_VERTICAL_SOURCE_AND_SPARC_RDISK",
                "source": "Patra2018NGC7331ScaleHeight + SPARC Rdisk",
                "source_line_refs": "scaleheight lines from Patra; Rdisk from SPARC metadata",
                "role": "dimensionless vertical kernel amplitude candidate",
            },
            {
                "field_id": "N7331_V4_PROJECTED_HWHM_OVER_RS",
                "observable": "projected_hwhm_over_Rs",
                "value": projected_hwhm_over_rs,
                "unit": "dimensionless",
                "status": "DERIVED_FROM_ACCEPTED_VERTICAL_SOURCE_AND_SPARC_RDISK",
                "source": "Patra2018NGC7331ScaleHeight + SPARC Rdisk",
                "source_line_refs": "edge-on HWHM lines from Patra; Rdisk from SPARC metadata",
                "role": "dimensionless projected-thickness overlay amplitude candidate",
            },
            {
                "field_id": "N7331_P1_INCLINATION_REVIEW",
                "observable": "inclination_review_range",
                "value": str(inc_review["observable_value"]),
                "unit": "deg",
                "status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
                "source": str(inc_review["source_file"]),
                "source_line_refs": str(inc_review["source_line_refs"]),
                "role": "projection-safety context",
            },
            {
                "field_id": "N7331_W1_OUTER_WARP_CAVEAT",
                "observable": "possible_outer_warp_caveat",
                "value": str(warp_caveat["observable_value"]),
                "unit": "categorical",
                "status": "CAVEAT_CONFIRMED_AS_OVERLAY_CONTEXT",
                "source": str(warp_caveat["source_file"]),
                "source_line_refs": str(warp_caveat["source_line_refs"]),
                "role": "blocks pure thick-regular acceptance; supports mixed outer-warp overlay review",
            },
            {
                "field_id": "N7331_W2_HI_WARP_CONTEXT",
                "observable": "outer_hi_warp_context",
                "value": "direct_and_kinematic_HI_warp_context_present",
                "unit": "categorical",
                "status": "CONTEXT_SOURCE_FIELD_REVIEW_READY",
                "source": bosma_url,
                "source_line_refs": "NED Level 5 Bosma warp discussion",
                "role": "supports outer-warp overlay context; no numeric warp radius extracted here",
            },
        ]
    )
    fields["endpoint_scores_allowed"] = False
    fields["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_CG1_SOURCE_QUEUE_CANDIDATE",
                "gate_status": "PASS_CAVEATED",
                "evidence": str(queue_row["candidate_priority"]),
                "remaining_obligation": "candidate source rule supports formula-freeze attempt only, not endpoint scoring",
            },
            {
                "gate_id": "N7331_CG2_VERTICAL_NUMERIC_MAPPING",
                "gate_status": "PASS",
                "evidence": f"intrinsic_h_over_Rs_mid={intrinsic_h_over_rs_mid:.6g}; projected_hwhm_over_Rs={projected_hwhm_over_rs:.6g}",
                "remaining_obligation": "treat projected HWHM as overlay observable, not intrinsic scaleheight",
            },
            {
                "gate_id": "N7331_CG3_OUTER_WARP_CAVEAT",
                "gate_status": "PASS_CAVEATED",
                "evidence": str(warp_caveat["observable_value"]),
                "remaining_obligation": "outer warp lacks numeric onset; may only define a broad outer-window caveat",
            },
            {
                "gate_id": "N7331_CG4_HI_WARP_CONTEXT",
                "gate_status": "PASS_CONTEXT_ONLY",
                "evidence": bosma_context,
                "remaining_obligation": "no endpoint kernel may use a fitted warp radius from this context alone",
            },
            {
                "gate_id": "N7331_CG5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "uses source fields, SPARC scale metadata, and literature context only",
                "remaining_obligation": "scoring must remain separate and formula must freeze before scoring",
            },
        ]
    )
    gates["galaxy"] = "NGC7331"
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
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
                "galaxy": "NGC7331",
                "candidate_mixed_readout": str(queue_row["candidate_mixed_readout"]),
                "audit_decision": str(audit_row["audit_decision"]),
                "rdisk_kpc": rdisk_kpc,
                "rhi_kpc": rhi_kpc,
                "intrinsic_h_mid_kpc": h_mid_kpc,
                "projected_hwhm_kpc": projected_hwhm_kpc,
                "intrinsic_h_over_Rs_mid": intrinsic_h_over_rs_mid,
                "projected_hwhm_over_Rs": projected_hwhm_over_rs,
                "projected_hwhm_over_RHI": projected_hwhm_over_rhi,
                "vertical_activation_candidate": vertical_activation,
                "outer_warp_context_present": True,
                "outer_warp_numeric_onset_available": False,
                "uses_vobs_or_residual_in_construction": False,
                "endpoint_scores_allowed": False,
                "formula_freeze_attempt_allowed": True,
                "caveat_gate_status": "CAVEAT_MAPPED_TO_MIXED_OVERLAY_CONTEXT_FORMULA_FREEZE_ALLOWED",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    fields.to_csv(DATA / "ngc7331_outer_warp_vertical_caveat_fields.csv", index=False)
    gates.to_csv(DATA / "ngc7331_outer_warp_vertical_caveat_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_outer_warp_vertical_caveat_summary.csv", index=False)

    report = [
        "# NGC7331 Outer-Warp / Vertical Caveat Gate",
        "",
        "This residual-blind gate maps the existing NGC7331 vertical source",
        "fields into dimensionless readout inputs and records that the outer-warp",
        "caveat should be treated as mixed-overlay context rather than ignored.",
        "It does not score rotation curves.",
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
        "## Claim Boundary",
        "",
        "This gate does not prove that the mixed NGC7331 readout fits the galaxy.",
        "It only allows a formula-freeze attempt: the vertical amplitudes are",
        "source-derived, while the outer-warp term is context/caveat-only until",
        "a numeric HI/projection onset is extracted.",
        "",
    ]
    (REPORTS / "ngc7331_outer_warp_vertical_caveat_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
