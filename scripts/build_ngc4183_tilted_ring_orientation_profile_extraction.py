#!/usr/bin/env python3
"""Extract an NGC4183 source-native tilted-ring orientation profile.

The values are transcribed from the locally cached Verheijen & Sancisi (2001)
OCR block for Table 4.  This extraction is residual-blind and is intended to
support an independent review before any formula freeze.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
SOURCE = ROOT / "data" / "external" / "literature" / "2001_verheijen_sancisi_ursa_major_hi.txt"
CLAIM_BOUNDARY = "ngc4183_tilted_ring_orientation_profile_extraction_not_endpoint"
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


def arcsec_to_kpc(radius_arcsec: float, distance_mpc: float) -> float:
    return radius_arcsec * distance_mpc * 1000.0 * math.pi / (180.0 * 3600.0)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    sparc_row = sparc.loc[sparc["Galaxy"].eq(GALAXY)].iloc[0]
    distance_mpc = float(sparc_row["D_Mpc"])
    rhi_kpc = float(pd.read_csv(DATA / "ngc4183_mixed_overlay_observable_sheet_summary.csv").iloc[0]["rhi_source_kpc"])

    # Table 4 OCR row pattern:
    # Rad(arcsec), Vrot_app, e_app, Vrot_rec, e_rec, Vrot_ave, e_ave, inc, PA.
    # Missing approaching/receding values near the edge are represented as NA.
    rows = [
        (10, 47, 10, 38, 15, 47, 10, 82, 346),
        (20, 71, 7, 61, 12, 66, 10, 82, 346),
        (30, 78, 7, 74, 10, 76, 7, 82, 346),
        (40, 88, 7, 84, 10, 86, 7, 82, 346),
        (50, 97, 7, 97, 7, 97, 7, 82, 346),
        (60, 100, 7, 99, 7, 99, 7, 82, 346),
        (70, 103, 7, 103, 7, 103, 7, 82, 346),
        (80, 106, 7, 107, 7, 107, 7, 82, 346),
        (90, 110, 7, 113, 7, 111, 7, 82, 346),
        (100, 112, 7, 117, 10, 114, 10, 82, 346),
        (110, 112, 7, 118, 10, 115, 10, 82, 346),
        (120, 108, 7, 114, 10, 111, 7, 82, 346),
        (130, 108, 7, 113, 10, 110, 7, 82, 347),
        (141, 111, 7, 112, 7, 111, 7, 82, 347),
        (151, 108, 7, 110, 7, 109, 7, 82, 347),
        (161, 106, 5, 109, 7, 108, 7, 82, 347),
        (172, 109, 7, 109, 7, 109, 7, 82, 347),
        (183, 112, 7, 110, 7, 111, 7, 82, 348),
        (194, 108, 5, 111, 8, 110, 8, 82, 348),
        (205, 106, 5, 111, 8, 109, 8, 82, 348),
        (217, 107, 7, 112, 8, 110, 8, 82, 348),
        (229, pd.NA, pd.NA, 112, 10, 112, 10, 82, 348),
        (241, pd.NA, pd.NA, 113, 13, 113, 10, 82, 349),
    ]

    profile = pd.DataFrame(
        rows,
        columns=[
            "radius_arcsec",
            "vrot_app_kms",
            "e_app_kms",
            "vrot_rec_kms",
            "e_rec_kms",
            "vrot_ave_kms",
            "e_ave_kms",
            "inclination_deg",
            "pa_deg",
        ],
    )
    profile["radius_kpc"] = profile["radius_arcsec"].map(
        lambda value: arcsec_to_kpc(float(value), distance_mpc)
    )
    profile["x_R_over_RHI"] = profile["radius_kpc"] / rhi_kpc
    profile["delta_pa_deg"] = profile["pa_deg"] - float(profile["pa_deg"].iloc[0])
    profile["delta_i_deg"] = profile["inclination_deg"] - float(profile["inclination_deg"].iloc[0])
    profile["twist_kernel_sin2_delta_pa"] = profile["delta_pa_deg"].map(
        lambda value: math.sin(math.radians(float(value))) ** 2
    )
    profile["inclination_kernel_sin2_delta_i"] = profile["delta_i_deg"].map(
        lambda value: math.sin(math.radians(float(value))) ** 2
    )
    profile["uses_vobs_or_residual"] = False
    profile["source_id"] = "VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI_TABLE4_OCR"
    profile["extraction_status"] = "OCR_TRANSCRIPTION_REVIEW_REQUIRED"

    max_pa_drift = float(profile["delta_pa_deg"].abs().max())
    max_i_drift = float(profile["delta_i_deg"].abs().max())
    max_twist_kernel = float(profile["twist_kernel_sin2_delta_pa"].max())
    max_radius_kpc = float(profile["radius_kpc"].max())

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_TR_G1_SOURCE_NATIVE_PROFILE_PRESENT",
                "gate_status": "PASS_REVIEW_REQUIRED",
                "evidence": "Table 4 OCR contains NGC4183 radial rings out to 241 arcsec",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "independent review against PDF/table image",
            },
            {
                "gate_id": "N4183_TR_G2_RADIAL_COVERAGE",
                "gate_status": "PASS",
                "evidence": f"max radius {max_radius_kpc:.3f} kpc, RHI {rhi_kpc:.3f} kpc",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "none for source profile extraction",
            },
            {
                "gate_id": "N4183_TR_G3_PROJECTION_LEVERAGE",
                "gate_status": "WEAK_SOURCE_LEVERAGE",
                "evidence": f"PA drift {max_pa_drift:.1f} deg; inclination drift {max_i_drift:.1f} deg",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "do not expect a large projection correction from this profile alone",
            },
            {
                "gate_id": "N4183_TR_G4_FREEZE",
                "gate_status": "BLOCKED",
                "evidence": "OCR extraction not independently reviewed",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "review source-native table or acquire machine-readable tilted-ring data",
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "tilted_ring_profile_status": "NGC4183_TILTED_RING_PROFILE_EXTRACTED_REVIEW_REQUIRED_NOT_FREEZE_READY",
                "galaxy": GALAXY,
                "n_rings": len(profile),
                "max_radius_arcsec": float(profile["radius_arcsec"].max()),
                "max_radius_kpc": max_radius_kpc,
                "rhi_kpc": rhi_kpc,
                "max_abs_pa_drift_deg": max_pa_drift,
                "max_abs_inclination_drift_deg": max_i_drift,
                "max_twist_kernel_sin2_delta_pa": max_twist_kernel,
                "profile_suggests_large_projection_correction": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": "independent_table_review_or_machine_readable_tilted_ring_acquisition",
            }
        ]
    )

    profile.to_csv(DATA / "ngc4183_tilted_ring_orientation_profile.csv", index=False)
    gates.to_csv(DATA / "ngc4183_tilted_ring_orientation_profile_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_tilted_ring_orientation_profile_summary.csv", index=False)

    report = f"""# NGC4183 Tilted-Ring Orientation Profile Extraction

Status: `{summary.iloc[0]["tilted_ring_profile_status"]}`

This extraction is residual-blind.  It transcribes the NGC4183 rows from the
locally cached Verheijen & Sancisi (2001) Table 4 OCR block.

## Summary

{markdown_table(summary)}

## Profile

{markdown_table(profile)}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Interpretation

The extracted source-native orientation profile has good radial coverage, but
it is nearly constant: inclination stays at 82 degrees and PA drifts only from
346 to 349 degrees.  That is useful negative/limiting evidence.  It supports
NGC4183 as an edge-on projection-caveated system, but it does not by itself
support a large projection correction or a numeric added warp-ramp.
"""
    (REPORTS / "ngc4183_tilted_ring_orientation_profile_extraction.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
