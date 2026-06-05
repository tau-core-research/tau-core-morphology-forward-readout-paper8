#!/usr/bin/env python3
"""Build the NGC4088 warp-onset extraction protocol.

The closure mapping shell needs x_w = R_warp / R_HI.  This protocol defines
which residual-blind source-native measurements can supply x_w and records that
NGC4088 remains onset-blocked until one of those measurements is extracted.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_ngc4088_warp_onset_extraction_protocol_not_endpoint"


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


def build_protocol() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    prekernel = pd.read_csv(DATA / "s4g75_ngc4088_warp_prekernel_observables.csv")
    prekernel_values = dict(zip(prekernel["observable"], prekernel["value"]))
    r_hi_kpc = float(prekernel_values["R_HI_from_WHISP_diameter_kpc"])
    rules = pd.DataFrame(
        [
            {
                "accepted_source_class": "RADIAL_PA_PROFILE",
                "source_observable": "PA(R) from tilted-ring HI model or digitized source-native PA profile",
                "onset_definition": "first R where |PA(R)-PA_inner| exceeds predeclared PA threshold for contiguous outer bins",
                "dimension_check": "x_w = R_onset_kpc / R_HI_kpc must satisfy 0 < x_w < 1",
                "residual_blind_requirement": "PA profile and threshold are selected without Vobs residuals",
                "endpoint_allowed_after_extraction": False,
            },
            {
                "accepted_source_class": "RADIAL_WARP_ANGLE_PROFILE",
                "source_observable": "theta_warp(R) or inclination/line-of-nodes warp profile from HI model",
                "onset_definition": "first R where theta_warp(R) exceeds predeclared angle threshold for contiguous outer bins",
                "dimension_check": "x_w = R_onset_kpc / R_HI_kpc must satisfy 0 < x_w < 1",
                "residual_blind_requirement": "warp profile and threshold are selected without Vobs residuals",
                "endpoint_allowed_after_extraction": False,
            },
            {
                "accepted_source_class": "CHANNEL_MAP_DIGITIZATION",
                "source_observable": "digitized channel-map ridge or major-axis bend from source figure",
                "onset_definition": "first R where outer ridge departs from inner disk PA beyond predeclared angular tolerance",
                "dimension_check": "requires angular-to-kpc conversion using source distance; then 0 < x_w < 1",
                "residual_blind_requirement": "digitization protocol, tolerance, and side-combination rule are frozen before scoring",
                "endpoint_allowed_after_extraction": False,
            },
            {
                "accepted_source_class": "TEXT_ONLY_QUALITATIVE_WARP",
                "source_observable": "text says warp/asymmetry is present but gives no radial onset",
                "onset_definition": "not accepted for x_w",
                "dimension_check": "insufficient dimensional information",
                "residual_blind_requirement": "may support development lane only",
                "endpoint_allowed_after_extraction": False,
            },
        ]
    )
    rules["claim_boundary"] = CLAIM_BOUNDARY
    status = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "R_HI_kpc_for_normalization": r_hi_kpc,
                "current_best_source_class": "TEXT_ONLY_QUALITATIVE_WARP_PLUS_GLOBAL_HI_GEOMETRY",
                "current_source_status": "WARP_PRESENT_ONSET_NOT_EXTRACTED",
                "x_warp_onset_available": False,
                "x_warp_onset_value": "",
                "acceptable_next_routes": "RADIAL_PA_PROFILE;RADIAL_WARP_ANGLE_PROFILE;CHANNEL_MAP_DIGITIZATION",
                "blocked_reason": "no source-native radial onset or PA/theta profile has been extracted",
                "closure_mapping_status": "MAPPING_RULE_DEFINED_ONSET_BLOCKED",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "n_accepted_source_classes": 3,
                "x_warp_onset_available": False,
                "R_HI_kpc_for_normalization": r_hi_kpc,
                "protocol_status": "RESIDUAL_BLIND_EXTRACTION_PROTOCOL_READY_ONSET_MISSING",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return rules, status, summary


def write_report(rules: pd.DataFrame, status: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Warp-Onset Extraction Protocol",
        "",
        "This protocol defines how the missing NGC4088 warp-onset control "
        "`x_w = R_warp/R_HI` may be supplied without using rotation residuals.",
        "",
        "## Verdict",
        "",
        "The mapping shell is ready, but the onset is not. NGC4088 has global HI "
        "geometry and qualitative warp/asymmetry evidence, yet no accepted "
        "source-native radial onset. The next admissible step is a PA profile, "
        "warp-angle profile, or frozen channel-map digitization.",
        "",
        "## Accepted Source Classes",
        "",
        markdown_table(rules),
        "",
        "## Current NGC4088 Status",
        "",
        markdown_table(status),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "A text-only warp statement is not enough to compute `x_w`. Even after "
        "`x_w` is extracted, endpoint scoring remains blocked until amplitude "
        "normalization and the 4D readout map are fixed residual-blind.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_warp_onset_extraction_protocol.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    rules, status, summary = build_protocol()
    rules.to_csv(DATA / "s4g75_ngc4088_warp_onset_extraction_protocol.csv", index=False)
    status.to_csv(DATA / "s4g75_ngc4088_warp_onset_status.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_warp_onset_summary.csv", index=False)
    write_report(rules, status, summary)
    print(f"wrote {DATA / 's4g75_ngc4088_warp_onset_extraction_protocol.csv'}")
    print(f"wrote {DATA / 's4g75_ngc4088_warp_onset_status.csv'}")
    print(f"wrote {DATA / 's4g75_ngc4088_warp_onset_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_ngc4088_warp_onset_extraction_protocol.md'}")


if __name__ == "__main__":
    main()
