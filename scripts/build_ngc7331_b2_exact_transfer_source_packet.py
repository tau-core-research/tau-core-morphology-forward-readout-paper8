#!/usr/bin/env python3
"""Build the NGC7331 source packet for exact B2 transfer inputs.

This is a residual-blind acquisition/review packet. It defines the missing
source-side measurements needed before an NGC4088-style B2 exact-transfer
formula can be frozen for NGC7331. It does not fill those measurements and
does not score the rotation curve.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_b2_exact_transfer_source_packet_not_endpoint"


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    upgrade_summary = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_upgrade_summary.csv"
    ).iloc[0]

    requirements = pd.DataFrame(
        [
            {
                "requirement_id": "N7331_B2_REQ_Q_WARP",
                "required_b2_field": "q_warp",
                "required_status": "accepted_numeric_or_bounded_dimensionless_source_strength",
                "source_class": "source-native H I warp map or literature warp amplitude/asymmetry",
                "acceptance_rule": (
                    "q_warp must be fixed from residual-blind outer-warp geometry; "
                    "allowed range is dimensionless and bounded before formula freeze"
                ),
                "blocks": "exact B2 source-load freeze",
            },
            {
                "requirement_id": "N7331_B2_REQ_SIGMA_WARP",
                "required_b2_field": "sigma_warp",
                "required_status": "accepted_sign_or_orientation_convention",
                "source_class": "orientation/readout geometry, side convention, and added-readout vs attenuation review",
                "acceptance_rule": (
                    "sigma_warp must be frozen from source-side geometry without using "
                    "endpoint residuals or baseline comparison"
                ),
                "blocks": "exact B2 source-load freeze",
            },
            {
                "requirement_id": "N7331_B2_REQ_EPSILON_CROSS",
                "required_b2_field": "epsilon_cross_inputs",
                "required_status": "accepted_bound_or_explicit_uncertainty_packet",
                "source_class": "side asymmetry, orientation mismatch, history/context, and locality observables",
                "acceptance_rule": (
                    "cross-term inputs must either close a residual-blind bound or be "
                    "carried as an explicit uncertainty interval"
                ),
                "blocks": "exact B2 source-load freeze or population-transfer claim",
            },
        ]
    )
    requirements["galaxy"] = GALAXY
    requirements["endpoint_scores_allowed"] = False
    requirements["uses_vobs_or_residual"] = False
    requirements["claim_boundary"] = CLAIM_BOUNDARY
    requirements = requirements[
        [
            "galaxy",
            "requirement_id",
            "required_b2_field",
            "required_status",
            "source_class",
            "acceptance_rule",
            "blocks",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    templates = pd.DataFrame(
        [
            {
                "template_id": "N7331_Q1_OUTER_WARP_EXTENT",
                "required_b2_field": "q_warp",
                "measurement_field": "outer_warp_extent_or_amplitude",
                "unit": "arcsec_or_kpc_or_dimensionless_ratio",
                "fill_rule": "measure source-native outer warp displacement, extent, or amplitude",
                "review_status": "MEASUREMENT_PENDING",
            },
            {
                "template_id": "N7331_Q2_LOCAL_DISK_REFERENCE",
                "required_b2_field": "q_warp",
                "measurement_field": "local_disk_reference_extent",
                "unit": "same_as_outer_warp_extent",
                "fill_rule": "use the same source frame as the outer-warp measurement",
                "review_status": "MEASUREMENT_PENDING",
            },
            {
                "template_id": "N7331_Q3_SIDE_WEIGHT",
                "required_b2_field": "q_warp",
                "measurement_field": "side_weight_or_reliability",
                "unit": "dimensionless",
                "fill_rule": "assign residual-blind side/panel reliability from source quality",
                "review_status": "MEASUREMENT_PENDING",
            },
            {
                "template_id": "N7331_S1_SIGN_CONVENTION",
                "required_b2_field": "sigma_warp",
                "measurement_field": "added_readout_or_attenuation",
                "unit": "sign_or_enum",
                "fill_rule": "freeze whether NGC7331 uses added-readout B2 sign or attenuation sign",
                "review_status": "MEASUREMENT_PENDING",
            },
            {
                "template_id": "N7331_S2_ORIENTATION_CONVENTION",
                "required_b2_field": "sigma_warp",
                "measurement_field": "orientation_side_convention",
                "unit": "text_plus_optional_angle",
                "fill_rule": "record which side/axis convention defines the sign",
                "review_status": "MEASUREMENT_PENDING",
            },
            {
                "template_id": "N7331_E1_ORIENTATION_MISMATCH",
                "required_b2_field": "epsilon_cross_inputs",
                "measurement_field": "orientation_mismatch_bound",
                "unit": "dimensionless_or_angle",
                "fill_rule": "bound source-side misalignment between ordinary disk and warp/readout layer",
                "review_status": "MEASUREMENT_PENDING",
            },
            {
                "template_id": "N7331_E2_SIDE_ASYMMETRY",
                "required_b2_field": "epsilon_cross_inputs",
                "measurement_field": "side_asymmetry_bound",
                "unit": "dimensionless",
                "fill_rule": "bound asymmetry between sides without rotation residuals",
                "review_status": "MEASUREMENT_PENDING",
            },
            {
                "template_id": "N7331_E3_HISTORY_CONTEXT",
                "required_b2_field": "epsilon_cross_inputs",
                "measurement_field": "history_or_memory_context",
                "unit": "categorical_or_dimensionless_proxy",
                "fill_rule": "record interaction/history context only if source-supported",
                "review_status": "MEASUREMENT_PENDING",
            },
            {
                "template_id": "N7331_E4_LOCALITY_ONSET_COUPLING",
                "required_b2_field": "epsilon_cross_inputs",
                "measurement_field": "locality_onset_coupling_bound",
                "unit": "dimensionless",
                "fill_rule": "bound whether cross terms remain local to the warp/onset lane",
                "review_status": "MEASUREMENT_PENDING",
            },
        ]
    )
    templates["galaxy"] = GALAXY
    templates["accepted_value"] = pd.NA
    templates["source_citation_or_cache"] = pd.NA
    templates["endpoint_scores_allowed"] = False
    templates["uses_vobs_or_residual"] = False
    templates["claim_boundary"] = CLAIM_BOUNDARY
    templates = templates[
        [
            "galaxy",
            "template_id",
            "required_b2_field",
            "measurement_field",
            "unit",
            "fill_rule",
            "accepted_value",
            "source_citation_or_cache",
            "review_status",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_B2SP1_PACKET_SCOPE",
                "gate_status": "PASS",
                "evidence": "q_warp, sigma_warp, and epsilon_cross source requirements are declared",
                "remaining_obligation": "none at packet-scope level",
            },
            {
                "gate_id": "N7331_B2SP2_XW_VFLAT_CONTEXT",
                "gate_status": "PASS_CONTEXT",
                "evidence": (
                    "upgrade gate has x_w and Vflat available; "
                    f"preview={float(upgrade_summary['unit_q_sigma_lambda_preview_km2_s2']):.6f} km^2/s^2"
                ),
                "remaining_obligation": "do not treat preview as formula or endpoint score",
            },
            {
                "gate_id": "N7331_B2SP3_Q_WARP_TEMPLATE",
                "gate_status": "BLOCKED_MEASUREMENT_PENDING",
                "evidence": "q_warp templates exist but no accepted measurement is filled",
                "remaining_obligation": "measure or bound q_warp from residual-blind H I/warp source",
            },
            {
                "gate_id": "N7331_B2SP4_SIGMA_TEMPLATE",
                "gate_status": "BLOCKED_REVIEW_PENDING",
                "evidence": "sigma_warp sign/orientation templates exist but convention is not frozen",
                "remaining_obligation": "freeze sign from source-side geometry",
            },
            {
                "gate_id": "N7331_B2SP5_EPSILON_TEMPLATE",
                "gate_status": "BLOCKED_MEASUREMENT_PENDING",
                "evidence": "epsilon_cross templates exist but no bound is filled",
                "remaining_obligation": "fill orientation, asymmetry, history, and locality inputs",
            },
            {
                "gate_id": "N7331_B2SP6_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "packet defines source templates only and reads no vobs/residual columns",
                "remaining_obligation": "keep endpoint scoring in a later separate script after formula freeze",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "source_packet_status": "NGC7331_EXACT_TRANSFER_SOURCE_PACKET_BUILT_MEASUREMENTS_PENDING",
                "n_requirements": len(requirements),
                "n_templates": len(templates),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].isin({"PASS", "PASS_CONTEXT"}).sum()),
                "n_blocked": int(gates["gate_status"].str.startswith("BLOCKED").sum()),
                "q_warp_packet_ready": True,
                "sigma_warp_packet_ready": True,
                "epsilon_cross_packet_ready": True,
                "q_warp_measurement_accepted": False,
                "sigma_warp_frozen": False,
                "epsilon_cross_bound_closed": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "population_claim_allowed": False,
                "next_required_action": (
                    "fill and independently review q_warp, sigma_warp, and epsilon_cross "
                    "source templates before exact B2 formula freeze"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    requirements.to_csv(
        DATA / "ngc7331_b2_exact_transfer_source_packet_requirements.csv", index=False
    )
    templates.to_csv(
        DATA / "ngc7331_b2_exact_transfer_source_packet_templates.csv", index=False
    )
    gates.to_csv(DATA / "ngc7331_b2_exact_transfer_source_packet_gate.csv", index=False)
    summary.to_csv(
        DATA / "ngc7331_b2_exact_transfer_source_packet_summary.csv", index=False
    )

    report = [
        "# NGC7331 B2 Exact Transfer Source Packet",
        "",
        "This packet turns the NGC7331 exact-transfer worklist into concrete",
        "residual-blind measurement and review templates. It does not fill the",
        "measurements, freeze a formula, or score the rotation curve.",
        "",
        "## Requirements",
        "",
        markdown_table(requirements),
        "",
        "## Measurement Templates",
        "",
        markdown_table(templates),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        "NGC7331 now has a concrete exact-transfer source-acquisition packet.",
        "The packet makes the next work narrow: fill q_warp, freeze sigma_warp,",
        "and close or explicitly carry epsilon_cross before any B2 formula freeze.",
        "The existing x_w Vflat^2 scale remains a dimensional preview only.",
        "",
    ]
    (REPORTS / "ngc7331_b2_exact_transfer_source_packet.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
