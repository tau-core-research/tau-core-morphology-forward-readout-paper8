#!/usr/bin/env python3
"""Build source-evidence matrix for readout-subfamily promotion.

This script audits which residual-blind source observables are already present
for the first-pass subfamily proposals and which source families should be
queried next. It does not score endpoints and does not accept labels.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "readout_subfamily_source_evidence_matrix_not_endpoint"


SOURCE_REQUESTS = {
    "K_disturbed_outer_tail": [
        ("hi_radius_mass", "SPARC master table", "MHI_1e9Msun;RHI_kpc"),
        ("hi_asymmetry_map", "HI surveys / THINGS / LITTLE THINGS / WHISP / literature", "HI asymmetry or tail map"),
        ("outer_tail_transition", "HI profile or deep optical/IR outer disk", "tail inner/cutoff radius"),
        ("environment_history", "NED/SIMBAD/literature", "interaction or companion evidence"),
    ],
    "K_smooth_n2_tail": [
        ("hi_radius_mass", "SPARC master table", "MHI_1e9Msun;RHI_kpc"),
        ("outer_tail_transition", "HI profile or deep optical/IR outer disk", "tail inner/cutoff radius"),
        ("smooth_tail_stability", "HI/optical profile review", "smooth non-disturbed outer tail"),
    ],
    "K_true_compact": [
        ("compact_support_radius", "S4G/NED/SIMBAD/decomposition", "compact support radius or bulge/core scale"),
        ("bulge_core_decomposition", "S4G Pipeline4 or literature", "B/N/component evidence"),
        ("disk_overlay_check", "S4G/SPARC/literature", "extended disk influence check"),
    ],
    "K_compact_plus_disk": [
        ("compact_support_radius", "S4G/NED/SIMBAD/decomposition", "compact support radius or bulge/core scale"),
        ("disk_scale", "S4G/SPARC", "disk scale radius"),
        ("overlay_balance", "decomposition review", "compact-vs-disk dominance"),
    ],
    "K_expdisk_overlay": [
        ("disk_scale", "S4G/SPARC", "disk scale radius"),
        ("bar_core_projection_history_overlay", "S4G/NED/SIMBAD/HI/projection review", "overlay type and strength"),
        ("clean_disk_rejection_reason", "source review", "why K_clean_expdisk is insufficient"),
    ],
    "K_clean_expdisk": [
        ("disk_scale", "S4G/SPARC", "disk scale radius"),
        ("clean_disk_label", "S4G/source review", "no strong bar/ring/warp/projection caveat"),
    ],
    "K_projection_dominated": [
        ("projection_geometry", "SPARC/S4G/dust lane/velocity field", "inclination/projection/deprojection support"),
        ("velocity_field_sanity", "HI/PHANGS/literature", "non-1D projection audit"),
        ("vertical_or_warp_source", "S4G/HI/literature", "separate true vertical/warp support from projection"),
    ],
    "K_thick_regular": [
        ("vertical_scale_or_thickness", "edge-on morphology/S4G/literature", "accepted thickness or h/rs"),
        ("low_warp_asymmetry", "HI/projection review", "absence of warp/history dominance"),
        ("projection_safety", "SPARC/S4G/literature", "projection not dominant"),
    ],
    "K_warp_history_coupled": [
        ("warp_onset", "HI velocity field / outer disk review", "warp onset radius"),
        ("warp_asymmetry", "HI maps/literature", "warp or lopsided asymmetry"),
        ("interaction_history", "NED/SIMBAD/literature", "interaction or morphology-memory evidence"),
        ("epsilon_cross_bound", "Tau Core source-bound protocol", "bounded cross-coupling interval"),
    ],
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


def has_value(value: object) -> bool:
    return pd.notna(value) and str(value) != ""


def evidence_status(
    galaxy: str,
    evidence_id: str,
    accepted_row: pd.Series,
    sparc_row: pd.Series | None,
    intake_row: pd.Series,
) -> tuple[str, str, str]:
    if evidence_id == "hi_radius_mass":
        if sparc_row is not None and (
            has_value(sparc_row.get("MHI_1e9Msun")) or has_value(sparc_row.get("RHI_kpc"))
        ):
            return "SOURCE_READY_CONTEXT_ONLY", "SPARC HI mass/radius present", "needs resolved HI asymmetry/profile for subfamily acceptance"
        return "MISSING", "no SPARC HI mass/radius row found", "query SPARC/NED/HI survey"

    if evidence_id in {"disk_scale", "compact_support_radius"}:
        field = "scale_radius_kpc" if evidence_id == "disk_scale" else "compact_support_radius_kpc"
        if has_value(accepted_row.get(field)):
            return "ACCEPTED_FIELD_READY", f"{field} present in accepted manifest", "family/subfamily label audit still needed"
        if evidence_id == "compact_support_radius" and (
            float(intake_row.get("mean_bulge", 0.0)) > 0.1
            or float(intake_row.get("max_bulge", 0.0)) > 0.2
        ):
            return "PROXY_SUPPORT_ONLY", "bulge/core proxy present", "extract compact support radius from decomposition/literature"
        return "MISSING", f"{field} missing", "query S4G/NED/decomposition"

    if evidence_id == "bulge_core_decomposition":
        if float(intake_row.get("mean_bulge", 0.0)) > 0.1 or float(intake_row.get("max_bulge", 0.0)) > 0.2:
            return "PROXY_SUPPORT_ONLY", "bulge/core proxy present from manifest", "promote with S4G/literature component evidence"
        return "MISSING", "no bulge/core proxy support", "query S4G/NED decomposition"

    if evidence_id in {"projection_geometry", "projection_safety"}:
        inc = float(intake_row.get("inclination_deg", 0.0))
        caveat = str(intake_row.get("manifest_caveat", ""))
        if inc >= 84 or "edge" in caveat or "projection" in caveat:
            return "PROXY_SUPPORT_ONLY", f"projection-sensitive inclination/caveat present: inc={inc}", "needs residual-blind projection review or velocity field"
        return "SOURCE_READY_CONTEXT_ONLY", f"inclination context present: inc={inc}", "needs explicit projection-safety acceptance"

    if evidence_id in {"vertical_scale_or_thickness", "vertical_or_warp_source"}:
        if has_value(accepted_row.get("thickness_h_over_rs")):
            return "ACCEPTED_FIELD_READY", "thickness_h_over_rs present", "audit vertical source provenance"
        if has_value(intake_row.get("thickness_h_over_rs_proxy")):
            return "PROXY_SUPPORT_ONLY", "thickness_h_over_rs proxy present", "promote with direct vertical/flare/warp source"
        return "MISSING", "vertical/thickness field missing", "query edge-on/HI/literature vertical source"

    if evidence_id == "epsilon_cross_bound":
        path = DATA / "s4g75_ngc4088_epsilon_cross_locality_bound_summary.csv"
        if galaxy == "NGC4088" and path.exists():
            return "SOURCE_BOUND_READY_FOR_DIAGNOSTIC", "NGC4088 epsilon_cross locality bound exists", "not accepted endpoint; repeat source-bound derivation for more galaxies"
        return "MISSING", "no source-bound epsilon_cross derivation for this galaxy", "run source-bound epsilon protocol"

    if evidence_id in {"warp_onset", "warp_asymmetry", "interaction_history"}:
        if galaxy == "NGC4088":
            return "SOURCE_BOUND_PARTIAL", "NGC4088 targeted warp/history protocol exists", f"accept {evidence_id} from independent HI/literature review"
        return "MISSING", f"{evidence_id} not available in local accepted source table", "query HI/NED/SIMBAD/literature"

    if evidence_id in {
        "hi_asymmetry_map",
        "outer_tail_transition",
        "environment_history",
        "smooth_tail_stability",
        "bar_core_projection_history_overlay",
        "clean_disk_rejection_reason",
        "clean_disk_label",
        "velocity_field_sanity",
        "low_warp_asymmetry",
        "disk_overlay_check",
        "overlay_balance",
    }:
        return "MISSING_OR_REVIEW_REQUIRED", f"{evidence_id} requires source review", "query/review listed source family before endpoint use"

    return "MISSING", "unrecognized evidence id", "manual audit"


def build_matrix() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    intake = pd.read_csv(DATA / "readout_subfamily_observable_intake_manifest.csv")
    accepted = pd.read_csv(DATA / "accepted_morphology_manifest.csv")
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    accepted_map = {row["galaxy"]: row for _, row in accepted.iterrows()}
    sparc_map = {row["Galaxy"]: row for _, row in sparc.iterrows()}
    rows = []
    for _, intake_row in intake.iterrows():
        galaxy = str(intake_row["galaxy"])
        subfamily = str(intake_row["proposed_readout_subfamily"])
        accepted_row = accepted_map.get(galaxy, pd.Series(dtype=object))
        sparc_row = sparc_map.get(galaxy)
        for evidence_id, source_family, target_field in SOURCE_REQUESTS.get(subfamily, []):
            status, current_evidence, next_action = evidence_status(
                galaxy, evidence_id, accepted_row, sparc_row, intake_row
            )
            rows.append(
                {
                    "galaxy": galaxy,
                    "parent_family": intake_row["formula_family"],
                    "proposed_readout_subfamily": subfamily,
                    "evidence_id": evidence_id,
                    "target_field": target_field,
                    "preferred_source_family": source_family,
                    "evidence_status": status,
                    "current_evidence": current_evidence,
                    "next_action": next_action,
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    matrix = pd.DataFrame(rows)
    summary = (
        matrix.groupby(["proposed_readout_subfamily", "evidence_status"], as_index=False)
        .agg(n_items=("evidence_id", "size"), n_galaxies=("galaxy", "nunique"))
        .sort_values(["proposed_readout_subfamily", "evidence_status"])
    )
    by_galaxy = (
        matrix.groupby(["galaxy", "proposed_readout_subfamily"], as_index=False)
        .agg(
            n_evidence_items=("evidence_id", "size"),
            n_accepted_ready=("evidence_status", lambda s: int((s == "ACCEPTED_FIELD_READY").sum())),
            n_source_context_ready=("evidence_status", lambda s: int(s.astype(str).str.contains("SOURCE").sum())),
            n_proxy_only=("evidence_status", lambda s: int(s.astype(str).str.contains("PROXY").sum())),
            n_missing_or_review=("evidence_status", lambda s: int(s.astype(str).str.contains("MISSING|REVIEW").sum())),
        )
        .sort_values("galaxy")
    )
    by_galaxy["subfamily_acceptance_status"] = by_galaxy.apply(
        lambda row: (
            "READY_FOR_INDEPENDENT_SUBFAMILY_REVIEW"
            if row["n_missing_or_review"] == 0 and row["n_accepted_ready"] > 0
            else "SOURCE_ACQUISITION_REQUIRED"
        ),
        axis=1,
    )
    by_galaxy["endpoint_scores_allowed"] = False
    by_galaxy["claim_boundary"] = CLAIM_BOUNDARY
    return matrix, summary, by_galaxy


def write_report(matrix: pd.DataFrame, summary: pd.DataFrame, by_galaxy: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    priority = matrix[
        matrix["evidence_status"].astype(str).str.contains("MISSING|REVIEW|PROXY")
    ][
        [
            "galaxy",
            "proposed_readout_subfamily",
            "evidence_id",
            "preferred_source_family",
            "evidence_status",
            "next_action",
        ]
    ]
    lines = [
        "# Readout-Subfamily Source Evidence Matrix",
        "",
        "This matrix audits which source observables are already present for the",
        "first-pass readout-subfamily proposals and which source families must be",
        "queried next. It does not score endpoints or accept subfamily labels.",
        "",
        "## By Galaxy",
        "",
        markdown_table(by_galaxy),
        "",
        "## Evidence Status Summary",
        "",
        markdown_table(summary),
        "",
        "## Acquisition / Review Priorities",
        "",
        markdown_table(priority),
        "",
        "## Full Evidence Matrix",
        "",
        markdown_table(matrix),
        "",
        "## Claim Boundary",
        "",
        "Accepted source evidence is still incomplete. SPARC/S4G provide useful",
        "scale and HI context for several rows, but subfamily acceptance requires",
        "additional residual-blind evidence such as resolved HI asymmetry, warp",
        "onset, compact support, vertical flare, projection safety, or overlay",
        "decomposition. No endpoint labels are promoted here.",
        "",
    ]
    (REPORTS / "readout_subfamily_source_evidence_matrix.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    matrix, summary, by_galaxy = build_matrix()
    matrix.to_csv(DATA / "readout_subfamily_source_evidence_matrix.csv", index=False)
    summary.to_csv(DATA / "readout_subfamily_source_evidence_summary.csv", index=False)
    by_galaxy.to_csv(DATA / "readout_subfamily_source_evidence_by_galaxy.csv", index=False)
    write_report(matrix, summary, by_galaxy)
    print(by_galaxy.to_string(index=False))
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
