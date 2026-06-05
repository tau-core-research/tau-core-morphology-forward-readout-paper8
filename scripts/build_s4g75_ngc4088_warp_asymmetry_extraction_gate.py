#!/usr/bin/env python3
"""Build the NGC4088 warp/asymmetry extraction gate.

The WHISP/Ursa Major source gives object-specific warp/asymmetry evidence for
NGC4088, but not yet a radial warp angle, flare height, or closure-source
profile.  This gate records the source-native observables that can be used for
formula development and the missing observables that block endpoint scoring.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
LITERATURE = ROOT / "data" / "external" / "literature"
CLAIM_BOUNDARY = "s4g75_ngc4088_warp_asymmetry_extraction_gate_not_endpoint"
SOURCE_TXT = LITERATURE / "2001_verheijen_sancisi_ursa_major_hi.txt"


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


def source_contains(pattern: str) -> bool:
    if not SOURCE_TXT.exists():
        return False
    return pattern in SOURCE_TXT.read_text(encoding="utf-8", errors="ignore")


def build_gate() -> tuple[pd.DataFrame, pd.DataFrame]:
    row = {
        "galaxy": "NGC4088",
        "formula_family": "K_thick_flared",
        "source_title": "The Ursa Major Cluster of Galaxies. IV: HI synthesis observations",
        "source_authors_year": "Verheijen & Sancisi 2001",
        "source_url": "https://www.aanda.org/articles/aa/pdf/2001/18/aa10469.pdf",
        "source_text_local": SOURCE_TXT.exists(),
        "source_text_contains_ngc4088": source_contains("NGC 4088"),
        "source_text_contains_strongly_distorted": source_contains("strongly\ndistorted")
        or source_contains("strongly distorted"),
        "source_text_contains_warp_asymmetric": source_contains("warp is\nasymmetric")
        or source_contains("warp is asymmetric"),
        "source_native_inclination_deg": 69.0,
        "source_native_position_angle_deg": 231.0,
        "source_native_hi_diameter_arcmin": 8.5,
        "source_native_hi_flux_jy_kms": 102.9,
        "source_native_w20_kms": 371.4,
        "source_native_w50_kms": 342.1,
        "warp_presence_flag": True,
        "pv_asymmetry_flag": True,
        "pa_asymmetry_flag": True,
        "extractable_now": (
            "inclination_deg;position_angle_deg;hi_diameter_arcmin;"
            "hi_flux_jy_kms;w20_kms;w50_kms;qualitative_warp_asymmetry_flags"
        ),
        "missing_for_profile_kernel": (
            "warp_onset_radius;theta_warp_R_or_PA_R_profile;vertical_height_H_R;"
            "radial_closure_source_profile;residual_blind_mapping_rule"
        ),
        "extraction_status": "OBJECT_WARP_EVIDENCE_READY_PROFILE_KERNEL_BLOCKED",
        "closure_source_development_allowed": True,
        "closure_source_endpoint_allowed": False,
        "endpoint_scores_allowed": False,
        "endpoint_scores_computed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gate = pd.DataFrame([row])
    missing = row["missing_for_profile_kernel"].split(";")
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "extractable_observable_count": len(row["extractable_now"].split(";")),
                "missing_profile_kernel_observable_count": len(missing),
                "closure_source_development_allowed": True,
                "closure_source_endpoint_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return gate, summary


def write_report(gate: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    row = gate.iloc[0]
    lines = [
        "# NGC4088 Warp/Asymmetry Extraction Gate",
        "",
        "This gate records what the WHISP/Ursa Major source can and cannot provide "
        "for the NGC4088 thick/flared closure-source branch.",
        "",
        "## Verdict",
        "",
        "NGC4088 now has object-specific warp/asymmetry evidence suitable for "
        "formula-development work. It is not endpoint-ready because the source "
        "does not yet provide a residual-blind radial warp, flare, or closure "
        "source profile.",
        "",
        "## Extractable Source-Native Observables",
        "",
        markdown_table(
            gate[
                [
                    "galaxy",
                    "source_native_inclination_deg",
                    "source_native_position_angle_deg",
                    "source_native_hi_diameter_arcmin",
                    "source_native_hi_flux_jy_kms",
                    "source_native_w20_kms",
                    "source_native_w50_kms",
                    "warp_presence_flag",
                    "pv_asymmetry_flag",
                    "pa_asymmetry_flag",
                ]
            ]
        ),
        "",
        "## Missing Profile-Kernel Observables",
        "",
        row["missing_for_profile_kernel"].replace(";", "\n"),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "The source permits a warp/asymmetry closure-source development lane, but "
        "not endpoint scoring. A usable readout kernel still needs a predeclared "
        "mapping from source-native warp/asymmetry observables to a radial "
        "closure-source profile.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_warp_asymmetry_extraction_gate.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    gate, summary = build_gate()
    gate.to_csv(DATA / "s4g75_ngc4088_warp_asymmetry_extraction_gate.csv", index=False)
    summary.to_csv(
        DATA / "s4g75_ngc4088_warp_asymmetry_extraction_summary.csv",
        index=False,
    )
    write_report(gate, summary)
    print(f"wrote {DATA / 's4g75_ngc4088_warp_asymmetry_extraction_gate.csv'}")
    print(f"wrote {DATA / 's4g75_ngc4088_warp_asymmetry_extraction_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_ngc4088_warp_asymmetry_extraction_gate.md'}")


if __name__ == "__main__":
    main()
