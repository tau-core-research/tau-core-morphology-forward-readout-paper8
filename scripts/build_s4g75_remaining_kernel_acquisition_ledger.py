#!/usr/bin/env python3
"""Build the S4G75 remaining kernel-source acquisition ledger.

This ledger starts after the strict S4G Table 7 promotions.  It records the
remaining non-strict rows, the direct source-native observable still required,
and the admissible acquisition/theorem route.  It is deliberately not an
endpoint and does not use residual scores to choose a path.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_remaining_kernel_acquisition_ledger_not_endpoint"
WANG_2014_URL = "https://arxiv.org/abs/1401.8164"


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


def classify_row(row: pd.Series) -> dict[str, object]:
    driver = row["observable_driver_type"]
    inc = float(row["Inc_deg"])
    if driver == "tail_inner_cutoff_candidate":
        return {
            "blocker_class": "SCALE_TAIL_TRANSITION_MISSING",
            "direct_kernel_observable_needed": (
                "outer_disk_break_radius_kpc; truncation_radius_kpc; "
                "HI_radial_profile_transition_radius_kpc; tail_inner_radius_kpc; "
                "tail_cutoff_radius_kpc"
            ),
            "primary_acquisition_lane": "HI_PROFILE_OR_OUTER_DISK_TRANSITION_EXTRACTION",
            "direct_source_targets": (
                "resolved HI radial surface-density profile; optical/IR outer-disk "
                "break or truncation profile; source-native transition radius"
            ),
            "fallback_theorem_route": "RHI_CONSERVATIVE_UPPER_CUTOFF_THEOREM",
            "theorem_support_status": "THEOREM_CONDITIONAL_RHI_UPPER_CUTOFF_CANDIDATE",
            "external_context": (
                "Wang et al. 2014 reports homogeneous outer HI profiles and an "
                "outer exponential scale of about 0.18 R1; useful context only, "
                "not a galaxy-specific direct transition measurement."
            ),
            "external_context_url": WANG_2014_URL,
            "next_action": (
                "search the SPARC HI reference and resolved HI/outer-disk profile "
                "sources for a residual-blind transition/break/truncation radius; "
                "otherwise keep RHI only as a theorem-conditional upper cutoff"
            ),
            "acquisition_priority": "P0_DIRECT_TRANSITION_SEARCH"
            if row["source_priority"] == "P0_DIRECT_SOURCE_NATIVE_REQUIRED"
            else "P1_DIRECT_TRANSITION_OR_THEOREM_SEARCH",
        }

    if driver == "thickness_h_over_rs_candidate":
        if inc >= 75:
            priority = "P0_EDGE_ON_VERTICAL_GEOMETRY_LITERATURE_SEARCH"
            lane = "EDGE_ON_VERTICAL_DECOMPOSITION_OR_WARP_EXTRACTION"
        elif inc >= 65:
            priority = "P1_HIGH_INCLINATION_FLARE_WARP_SEARCH"
            lane = "FLARE_WARP_OR_GAS_PLANE_THICKNESS_EXTRACTION"
        else:
            priority = "P2_NON_EDGE_ON_PROXY_REVIEW"
            lane = "KINEMATIC_OR_MULTI_BAND_THICKNESS_PROXY_REVIEW"
        return {
            "blocker_class": "VERTICAL_KERNEL_MISSING",
            "direct_kernel_observable_needed": (
                "vertical_scale_height_kpc; h_over_Rs; flare_radius_kpc; "
                "warp_radius_kpc; gas_plane_thickness_or_warp"
            ),
            "primary_acquisition_lane": lane,
            "direct_source_targets": (
                "edge-on disk decomposition; vertical light profile; flare/warp "
                "measurement; gas-plane thickness from resolved HI/kinematics"
            ),
            "fallback_theorem_route": "EDGE_DISK_OR_INCLINATION_TO_VERTICAL_KERNEL_THEOREM",
            "theorem_support_status": "NO_ACCEPTED_VERTICAL_KERNEL_THEOREM_YET",
            "external_context": (
                "S4G/SPARC/HI coverage is useful context, but not a measured "
                "vertical kernel unless a vertical scale, flare, warp, or gas-plane "
                "thickness parameter is source-native."
            ),
            "external_context_url": "",
            "next_action": (
                "search source-native decompositions and resolved gas/warp studies "
                "for a measured or bounded vertical kernel; do not promote from "
                "inclination or generic disk-component naming alone"
            ),
            "acquisition_priority": priority,
        }

    return {
        "blocker_class": "UNCLASSIFIED_KERNEL_BLOCKER",
        "direct_kernel_observable_needed": row.get("required_observables", ""),
        "primary_acquisition_lane": "REVIEW_REQUIRED",
        "direct_source_targets": "",
        "fallback_theorem_route": "NO_ROUTE_DEFINED",
        "theorem_support_status": "NO_THEOREM_DEFINED",
        "external_context": "",
        "external_context_url": "",
        "next_action": "define a driver-specific acquisition rule",
        "acquisition_priority": "P2_REVIEW_REQUIRED",
    }


def build_ledger() -> tuple[pd.DataFrame, pd.DataFrame]:
    gate = pd.read_csv(DATA / "s4g75_kernel_ready_promotion_gate.csv")
    rows = []
    remaining = gate[gate["kernel_promotion_status"] != "KERNEL_READY_STRICT"].copy()
    for _, row in remaining.iterrows():
        details = classify_row(row)
        rows.append(
            {
                "galaxy": row["galaxy"],
                "formula_family": row["formula_family"],
                "source_priority": row["source_priority"],
                "observable_driver_type": row["observable_driver_type"],
                "kernel_promotion_status": row["kernel_promotion_status"],
                "kernel_specific_source_status": row["kernel_specific_source_status"],
                "inclination_deg": row["Inc_deg"],
                "rdisk_kpc": row["Rdisk_kpc"],
                "rhi_kpc": row["RHI_kpc"],
                "sparc_hi_ref": row["Ref"],
                "dustpedia_status": row["dustpedia_status"],
                "phangs_status": row["phangs_status"],
                "s4g_model_components": row["s4g_model_components"],
                "s4g_disk_component_source": row["s4g_disk_component_source"],
                **details,
                "strict_kernel_ready": False,
                "endpoint_scores_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    ledger = pd.DataFrame(rows)
    summary = (
        ledger.groupby(
            [
                "formula_family",
                "blocker_class",
                "primary_acquisition_lane",
                "fallback_theorem_route",
            ],
            as_index=False,
        )
        .agg(
            n_galaxies=("galaxy", "count"),
            galaxies=("galaxy", lambda values: ";".join(values)),
            p0_count=("source_priority", lambda s: int((s == "P0_DIRECT_SOURCE_NATIVE_REQUIRED").sum())),
            p1_count=("source_priority", lambda s: int((s == "P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE").sum())),
        )
    )
    summary["claim_boundary"] = CLAIM_BOUNDARY
    return ledger, summary


def write_report(ledger: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# S4G75 Remaining Kernel Acquisition Ledger",
        "",
        "This ledger records the remaining non-strict S4G75 kernel blockers after "
        "direct S4G Table 7 extraction. It is residual-blind and does not compute "
        "or authorize endpoint scores.",
        "",
        "## Verdict",
        "",
        f"Remaining non-strict rows: {len(ledger)}.",
        f"Scale-tail transition blockers: {int((ledger['blocker_class'] == 'SCALE_TAIL_TRANSITION_MISSING').sum())}.",
        f"Vertical-kernel blockers: {int((ledger['blocker_class'] == 'VERTICAL_KERNEL_MISSING').sum())}.",
        "",
        "The scale-tail rows have RHI support but still lack galaxy-specific direct "
        "outer transition measurements. The thick/flared rows need vertical "
        "scale, flare, warp, or gas-plane thickness observables; inclination or "
        "generic disk-component naming is not enough.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Galaxy-Level Ledger",
        "",
        markdown_table(
            ledger[
                [
                    "galaxy",
                    "formula_family",
                    "source_priority",
                    "blocker_class",
                    "acquisition_priority",
                    "inclination_deg",
                    "rhi_kpc",
                    "sparc_hi_ref",
                    "dustpedia_status",
                    "phangs_status",
                    "direct_kernel_observable_needed",
                    "primary_acquisition_lane",
                    "fallback_theorem_route",
                    "theorem_support_status",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "Rows in this ledger are not strict kernel-ready. They can become strict "
        "only through direct source-native kernel measurements or an accepted "
        "residual-blind Tau-side promotion theorem. Endpoint improvement cannot "
        "satisfy the missing source/kernel condition.",
        "",
    ]
    (REPORTS / "s4g75_remaining_kernel_acquisition_ledger.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    ledger, summary = build_ledger()
    ledger.to_csv(DATA / "s4g75_remaining_kernel_acquisition_ledger.csv", index=False)
    summary.to_csv(DATA / "s4g75_remaining_kernel_acquisition_summary.csv", index=False)
    write_report(ledger, summary)
    print(f"wrote {DATA / 's4g75_remaining_kernel_acquisition_ledger.csv'}")
    print(f"wrote {DATA / 's4g75_remaining_kernel_acquisition_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_remaining_kernel_acquisition_ledger.md'}")


if __name__ == "__main__":
    main()
