#!/usr/bin/env python3
"""Build the S4G75 direct source-native kernel-observable acquisition manifest.

The manifest is downstream of the filled-kernel delta-driver audit.  It turns
the diagnostic P0/P1 targets into residual-blind source tasks, without creating
accepted labels and without recomputing endpoint scores.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_direct_source_native_acquisition_manifest_not_endpoint"

SOURCE_URLS = {
    "S4G": "https://irsa.ipac.caltech.edu/data/SPITZER/S4G/overview.html",
    "NED_NEDD": "https://ned.ipac.caltech.edu/",
    "DustPedia": "https://arxiv.org/abs/1708.05335",
    "HI_SURVEYS": "THINGS; LITTLE_THINGS; WALLABY; HALOGAS; SPARC HI fields",
    "PHANGS": "https://www.phangs.org/home/data",
}

TARGET_SPECS = {
    "tail_inner_cutoff_candidate": {
        "required_source_families": "HI_SURVEYS;DustPedia;S4G;NED_NEDD",
        "required_observables": (
            "outer_disk_break_radius_kpc; HI_radial_profile_or_RHI_kpc; "
            "tail_inner_radius_kpc; tail_cutoff_radius_kpc; truncation_radius_kpc"
        ),
        "source_task": (
            "measure or cite direct outer-disk/HI transition support rather "
            "than using the predeclared disk-to-HI formula candidate alone"
        ),
    },
    "compact_support_candidate": {
        "required_source_families": "S4G;DustPedia;NED_NEDD",
        "required_observables": (
            "bulge_or_compact_component_radius_kpc; compact_light_support_kpc; "
            "central_component_decomposition_flag"
        ),
        "source_task": (
            "measure or cite a compact component support radius instead of "
            "using SPARC Reff as a formula-conditional support proxy"
        ),
    },
    "thickness_h_over_rs_candidate": {
        "required_source_families": "S4G;DustPedia;HI_SURVEYS;PHANGS;NED_NEDD",
        "required_observables": (
            "vertical_scale_height_kpc; h_over_Rs; flare_or_warp_radius_kpc; "
            "edge_on_thickness_evidence; gas_plane_thickness_or_warp"
        ),
        "source_task": (
            "measure or cite direct vertical geometry, flare, warp, or "
            "edge-on thickness evidence instead of inclination+HI proxy only"
        ),
    },
}


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


def source_urls(families: str) -> str:
    return "; ".join(SOURCE_URLS[source] for source in families.split(";"))


def build_manifest() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    audit = pd.read_csv(DATA / "s4g75_filled_kernel_delta_drivers.csv")
    rows = []
    for _, row in audit.iterrows():
        driver = row["observable_driver_type"]
        spec = TARGET_SPECS.get(driver)
        if spec is None:
            continue
        rows.append(
            {
                "galaxy": row["galaxy"],
                "formula_family": row["formula_family"],
                "observable_driver_type": driver,
                "source_priority": row["source_priority"],
                "repair_priority": row["repair_priority"],
                "driver_outcome": row["driver_outcome"],
                "required_source_families": spec["required_source_families"],
                "source_urls_or_catalogs": source_urls(spec["required_source_families"]),
                "required_observables": spec["required_observables"],
                "source_task": spec["source_task"],
                "delta_matched_rmse": row["filled_minus_old_matched_rmse"],
                "delta_vs_tpg": row["filled_minus_old_matched_minus_tpg"],
                "delta_vs_mond": row["filled_minus_old_matched_minus_mond"],
                "endpoint_blocker": row["endpoint_blocker"],
                "acquisition_status": "TO_BE_ACQUIRED_OR_DIRECTLY_MEASURED_RESIDUAL_BLIND",
                "accepted_label_output_allowed": False,
                "endpoint_scores_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    manifest = pd.DataFrame(rows).sort_values(
        ["source_priority", "observable_driver_type", "galaxy"]
    )
    source_summary = (
        manifest.assign(
            source_family=manifest["required_source_families"].str.split(";")
        )
        .explode("source_family")
        .groupby(["source_family", "source_priority"], as_index=False)
        .agg(
            n_tasks=("galaxy", "count"),
            n_galaxies=("galaxy", "nunique"),
            galaxies=("galaxy", lambda values: ";".join(sorted(set(values)))),
        )
    )
    source_summary["url_or_catalog"] = source_summary["source_family"].map(SOURCE_URLS)
    source_summary["acquisition_status"] = "TO_BE_ACQUIRED_OR_DIRECTLY_MEASURED_RESIDUAL_BLIND"
    source_summary["claim_boundary"] = CLAIM_BOUNDARY

    family_summary = (
        manifest.groupby(
            ["formula_family", "observable_driver_type", "source_priority"],
            as_index=False,
        )
        .agg(
            n_galaxies=("galaxy", "count"),
            galaxies=("galaxy", lambda values: ";".join(values)),
            median_delta_matched_rmse=("delta_matched_rmse", "median"),
            median_delta_vs_tpg=("delta_vs_tpg", "median"),
            median_delta_vs_mond=("delta_vs_mond", "median"),
        )
    )
    family_summary["claim_boundary"] = CLAIM_BOUNDARY
    return manifest, source_summary, family_summary


def write_report(
    manifest: pd.DataFrame,
    source_summary: pd.DataFrame,
    family_summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    p0 = manifest.loc[manifest["source_priority"] == "P0_DIRECT_SOURCE_NATIVE_REQUIRED"]
    p1 = manifest.loc[manifest["source_priority"] == "P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE"]
    lines = [
        "# S4G75 Direct Source-Native Acquisition Manifest",
        "",
        "This manifest converts the filled-kernel delta-driver audit into concrete "
        "residual-blind source tasks. It does not create accepted labels and does "
        "not rerun endpoint scores.",
        "",
        "## Verdict",
        "",
        f"Total source tasks: {len(manifest)}.",
        f"P0 direct source-native tasks: {len(p0)}.",
        f"P1 promote/confirm source-native tasks: {len(p1)}.",
        "",
        "P0 tasks are the rows where formula-conditional filled observables "
        "worsened baseline transfer. P1 tasks are rows where filled observables "
        "helped but still require source-native confirmation or a stronger "
        "Tau-side promotion rule.",
        "",
        "## Family Summary",
        "",
        markdown_table(family_summary),
        "",
        "## Source Family Summary",
        "",
        markdown_table(source_summary),
        "",
        "## Galaxy-Level Acquisition Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Claim Boundary",
        "",
        "The manifest is an acquisition queue. It may be used to fetch or measure "
        "direct morphology kernel observables, but it cannot define accepted "
        "readout labels or endpoint wins without a later residual-blind audit.",
        "",
    ]
    (REPORTS / "s4g75_direct_source_native_acquisition_manifest.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    manifest, source_summary, family_summary = build_manifest()
    manifest.to_csv(DATA / "s4g75_direct_source_native_acquisition_manifest.csv", index=False)
    source_summary.to_csv(
        DATA / "s4g75_direct_source_native_acquisition_source_summary.csv",
        index=False,
    )
    family_summary.to_csv(
        DATA / "s4g75_direct_source_native_acquisition_family_summary.csv",
        index=False,
    )
    write_report(manifest, source_summary, family_summary)
    print(f"wrote {DATA / 's4g75_direct_source_native_acquisition_manifest.csv'}")
    print(f"wrote {DATA / 's4g75_direct_source_native_acquisition_source_summary.csv'}")
    print(f"wrote {DATA / 's4g75_direct_source_native_acquisition_family_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_direct_source_native_acquisition_manifest.md'}")


if __name__ == "__main__":
    main()
