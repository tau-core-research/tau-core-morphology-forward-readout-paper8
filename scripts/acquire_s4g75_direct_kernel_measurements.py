#!/usr/bin/env python3
"""Extract direct S4G kernel measurements for S4G75 acquisition rows.

This pass uses already acquired S4G Table 7 decomposition rows and SPARC
distances to fill direct kernel measurements where the source table contains
the actual kernel parameter.  It deliberately reads the stable direct-source
acquisition manifest rather than the current conditional-promotion table, so
already promoted rows remain present under repeated reproduction runs.  It
leaves HI-extent-only tail rows conditional, because RHI is not a direct
outer-transition profile.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_direct_kernel_measurement_extraction_not_endpoint"
ARCSEC_TO_KPC_PER_MPC = 0.004848136811


PROMOTION_GATE_BY_DRIVER = {
    "compact_support_candidate": "COMPACT-COMPONENT-SUPPORT-PROMOTION",
    "thickness_h_over_rs_candidate": "EDGE-DISK-TO-VERTICAL-KERNEL-PROMOTION",
    "tail_inner_cutoff_candidate": "TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION",
}


def finite(value: object) -> bool:
    try:
        return pd.notna(value) and float(value) > 0
    except (TypeError, ValueError):
        return False


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


def s4g_name(galaxy: str) -> str:
    return galaxy.upper()


def extract_measurements() -> tuple[pd.DataFrame, pd.DataFrame]:
    manifest = pd.read_csv(DATA / "s4g75_direct_source_native_acquisition_manifest.csv")
    s4g = pd.read_csv(DATA / "external_s4g_table7.csv")
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv").rename(columns={"Galaxy": "galaxy"})
    rows = []
    for _, req in manifest.iterrows():
        galaxy = req["galaxy"]
        distance = float(sparc.loc[sparc["galaxy"] == galaxy, "D_Mpc"].iloc[0])
        kpc_per_arcsec = distance * ARCSEC_TO_KPC_PER_MPC
        table_rows = s4g.loc[s4g["Name"].str.upper() == s4g_name(galaxy)]
        driver = req["observable_driver_type"]
        base = {
            "galaxy": galaxy,
            "formula_family": req["formula_family"],
            "observable_driver_type": driver,
            "promotion_gate": PROMOTION_GATE_BY_DRIVER.get(driver, "NO_PROMOTION_GATE_DEFINED"),
            "distance_mpc": distance,
            "kpc_per_arcsec": kpc_per_arcsec,
            "source_table": "S4G_Table7",
            "endpoint_scores_allowed": False,
            "endpoint_scores_computed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        }

        if driver == "compact_support_candidate":
            bulge = table_rows.loc[table_rows["C"].astype(str).str.upper() == "B"]
            if not bulge.empty and finite(bulge.iloc[0]["Re"]):
                re_arcsec = float(bulge.iloc[0]["Re"])
                rows.append(
                    {
                        **base,
                        "direct_measurement_status": "DIRECT_S4G_BULGE_RE_READY",
                        "kernel_parameter_filled": "compact_support_radius_kpc",
                        "value_arcsec": re_arcsec,
                        "value_kpc": re_arcsec * kpc_per_arcsec,
                        "secondary_value_arcsec": None,
                        "secondary_value_kpc": None,
                        "dimensionless_value": None,
                        "source_component": "B:sersic_Re",
                        "promotion_interpretation": (
                            "S4G Sersic bulge effective radius directly constrains a compact support candidate"
                        ),
                    }
                )
            else:
                rows.append(
                    {
                        **base,
                        "direct_measurement_status": "NO_DIRECT_COMPACT_RADIUS_IN_S4G_TABLE7",
                        "kernel_parameter_filled": "compact_support_radius_kpc",
                        "value_arcsec": None,
                        "value_kpc": None,
                        "secondary_value_arcsec": None,
                        "secondary_value_kpc": None,
                        "dimensionless_value": None,
                        "source_component": "",
                        "promotion_interpretation": "no S4G bulge Re found",
                    }
                )
            continue

        if driver == "thickness_h_over_rs_candidate":
            edgedisk = table_rows.loc[table_rows["C"].astype(str).str.upper() == "Z"]
            if not edgedisk.empty and finite(edgedisk.iloc[0]["hz2"]) and finite(edgedisk.iloc[0]["hr2"]):
                hz_arcsec = float(edgedisk.iloc[0]["hz2"])
                hr_arcsec = float(edgedisk.iloc[0]["hr2"])
                rows.append(
                    {
                        **base,
                        "direct_measurement_status": "DIRECT_S4G_EDGEDISK_HZ_HR_READY",
                        "kernel_parameter_filled": "thickness_h_over_rs",
                        "value_arcsec": hz_arcsec,
                        "value_kpc": hz_arcsec * kpc_per_arcsec,
                        "secondary_value_arcsec": hr_arcsec,
                        "secondary_value_kpc": hr_arcsec * kpc_per_arcsec,
                        "dimensionless_value": hz_arcsec / hr_arcsec,
                        "source_component": "Z:edgedisk_hz2_over_hr2",
                        "promotion_interpretation": (
                            "S4G edge-disk hz2/hr2 directly constrains the vertical kernel ratio"
                        ),
                    }
                )
            else:
                rows.append(
                    {
                        **base,
                        "direct_measurement_status": "NO_DIRECT_VERTICAL_KERNEL_IN_S4G_TABLE7",
                        "kernel_parameter_filled": "thickness_h_over_rs",
                        "value_arcsec": None,
                        "value_kpc": None,
                        "secondary_value_arcsec": None,
                        "secondary_value_kpc": None,
                        "dimensionless_value": None,
                        "source_component": "",
                        "promotion_interpretation": "no S4G edge-disk hz2/hr2 found",
                    }
                )
            continue

        if driver == "tail_inner_cutoff_candidate":
            rows.append(
                {
                    **base,
                    "direct_measurement_status": "NO_DIRECT_OUTER_TRANSITION_IN_S4G_TABLE7",
                    "kernel_parameter_filled": "tail_inner_radius_kpc;tail_cutoff_radius_kpc",
                    "value_arcsec": None,
                    "value_kpc": None,
                    "secondary_value_arcsec": None,
                    "secondary_value_kpc": None,
                    "dimensionless_value": None,
                    "source_component": "",
                    "promotion_interpretation": (
                        "S4G Table 7 does not provide the HI/outer-disk transition profile required by the tail kernel"
                    ),
                }
            )
            continue
    measurements = pd.DataFrame(rows)
    summary = (
        measurements.groupby(
            ["observable_driver_type", "direct_measurement_status", "kernel_parameter_filled"],
            as_index=False,
        )
        .agg(
            n_galaxies=("galaxy", "count"),
            galaxies=("galaxy", lambda values: ";".join(values)),
        )
    )
    summary["claim_boundary"] = CLAIM_BOUNDARY
    return measurements, summary


def write_report(measurements: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    ready = measurements["direct_measurement_status"].str.startswith("DIRECT_")
    lines = [
        "# S4G75 Direct Kernel Measurement Extraction",
        "",
        "This report extracts direct S4G Table 7 kernel measurements for the "
        "stable S4G75 direct-source acquisition manifest. It does not use "
        "endpoint residuals and does not rerun scores.",
        "",
        "## Verdict",
        "",
        f"Acquisition-manifest rows checked: {len(measurements)}.",
        f"Direct kernel measurements found: {int(ready.sum())}.",
        f"Rows still missing direct kernel measurements: {int((~ready).sum())}.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Galaxy-Level Measurements",
        "",
        markdown_table(
            measurements[
                [
                    "galaxy",
                    "formula_family",
                    "observable_driver_type",
                    "direct_measurement_status",
                    "kernel_parameter_filled",
                    "value_kpc",
                    "secondary_value_kpc",
                    "dimensionless_value",
                    "source_component",
                    "promotion_interpretation",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "A direct S4G decomposition parameter can support kernel promotion only "
        "for the matching kernel. Bulge Re can support compact finite-source; "
        "edge-disk hz/hr can support thick/flared. This pass does not promote "
        "RHI-only scale-tail rows because S4G Table 7 does not supply their "
        "outer transition profile.",
        "",
    ]
    (REPORTS / "s4g75_direct_kernel_measurement_extraction.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    measurements, summary = extract_measurements()
    measurements.to_csv(DATA / "s4g75_direct_kernel_measurements.csv", index=False)
    summary.to_csv(DATA / "s4g75_direct_kernel_measurement_summary.csv", index=False)
    write_report(measurements, summary)
    print(f"wrote {DATA / 's4g75_direct_kernel_measurements.csv'}")
    print(f"wrote {DATA / 's4g75_direct_kernel_measurement_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_direct_kernel_measurement_extraction.md'}")


if __name__ == "__main__":
    main()
