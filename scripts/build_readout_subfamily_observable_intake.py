#!/usr/bin/env python3
"""Build a first-pass readout-subfamily observable intake manifest.

This layer proposes readout-relevant subfamilies from residual-blind source
observables and proxy caveats. It does not use endpoint scores and it does not
promote accepted labels.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "readout_subfamily_observable_intake_not_endpoint_not_accepted_label"


FIELD_ROWS = [
    {
        "field": "warp_onset_or_outer_bend",
        "accepted_source_path": "HI velocity field; optical/IR outer-disk warp review; source-extracted warp onset",
        "proxy_source_path": "manifest_caveat; inclination/projection caveat; NGC4088 source-bound warp lane",
        "used_for_subfamilies": "K_warp_history_coupled;K_flared_outer_disk;K_projection_dominated",
        "forbidden_source": "rotation residual shape; best-fitting Tau branch",
    },
    {
        "field": "hi_asymmetry_or_tail_support",
        "accepted_source_path": "HI maps/asymmetry indices; resolved HI radius and outer profile",
        "proxy_source_path": "SPARC RHI/MHI; gas-rich/irregular flag; literature source hits",
        "used_for_subfamilies": "K_smooth_n2_tail;K_disturbed_outer_tail;K_warp_history_coupled",
        "forbidden_source": "outer rotation residual improvement",
    },
    {
        "field": "projection_safety",
        "accepted_source_path": "inclination uncertainty; dust lane/projection review; velocity-field sanity check",
        "proxy_source_path": "SPARC inclination; inc_bin; manifest_caveat",
        "used_for_subfamilies": "K_projection_dominated;K_clean_expdisk;K_thick_regular",
        "forbidden_source": "bad model fit after deprojection",
    },
    {
        "field": "clean_disk_support",
        "accepted_source_path": "S4G/SPARC disk scale and no bar/ring/warp caveat from residual-blind review",
        "proxy_source_path": "type_bin; scale_radius_proxy_kpc; manifest_caveat",
        "used_for_subfamilies": "K_clean_expdisk",
        "forbidden_source": "readout family inferred from rotation endpoint",
    },
    {
        "field": "bar_core_overlay_support",
        "accepted_source_path": "S4G component decomposition; bar/core/nuclear support",
        "proxy_source_path": "mean_bulge; max_bulge; p0 source review caveats where available",
        "used_for_subfamilies": "K_expdisk_overlay;K_compact_plus_disk;K_true_compact",
        "forbidden_source": "residual peak/ring chosen from fit",
    },
    {
        "field": "vertical_or_flare_support",
        "accepted_source_path": "edge-on thickness; flare gradient; vertical profile; HI warp/flare evidence",
        "proxy_source_path": "thickness_h_over_rs_proxy; inc_bin; vertical_geometry_proxy_only caveat",
        "used_for_subfamilies": "K_thick_regular;K_flared_outer_disk;K_warp_history_coupled",
        "forbidden_source": "endpoint-selected damping factor",
    },
    {
        "field": "morphology_history_memory_support",
        "accepted_source_path": "residual-blind interaction/environment/history review",
        "proxy_source_path": "morphological_memory_history_proxy flags; source-side interaction evidence",
        "used_for_subfamilies": "K_warp_history_coupled;K_disturbed_outer_tail;K_expdisk_overlay",
        "forbidden_source": "rotation-inferred family as accepted label",
    },
]


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


def caveats(row: pd.Series) -> set[str]:
    return {
        token.strip()
        for token in str(row.get("manifest_caveat", "")).split(";")
        if token.strip() and token.strip() != "none"
    }


def flags(row: pd.Series) -> set[str]:
    return {
        token.strip()
        for token in str(row.get("source_memory_proxy_flags", "")).split(";")
        if token.strip()
    }


def choose_subfamily(row: pd.Series) -> tuple[str, str, str, str]:
    family = str(row["formula_family"])
    cv = caveats(row)
    fl = flags(row)
    inc = float(row.get("inclination_deg", 0.0))
    mean_bulge = float(row.get("mean_bulge", 0.0))
    max_bulge = float(row.get("max_bulge", 0.0))
    mean_gas = float(row.get("mean_gas", 0.0))
    mean_log_sbdisk = float(row.get("mean_log_sbdisk", 99.0))
    confidence = float(row.get("manifest_confidence", 0.0))

    if family == "K_thick_flared":
        if row["galaxy"] == "NGC4088":
            return (
                "K_warp_history_coupled",
                "source-bound warp/history lane already exists for NGC4088",
                "warp onset/asymmetry; HI disturbance; interaction/history; epsilon_cross bound",
                "diagnostic_subfamily_not_accepted",
            )
        if inc >= 84 or "edge_projection_caveat" in cv:
            return (
                "K_projection_dominated",
                "edge-on or projection-sensitive thick/flared morphology",
                "projection/deprojection audit; dust lane review; velocity-field sanity check",
                "proxy_only",
            )
        if "vertical_geometry_proxy_only" in cv:
            return (
                "K_thick_regular",
                "vertical proxy exists but no accepted flare/warp source",
                "direct vertical scale or flare-gradient source",
                "proxy_only",
            )
        return (
            "K_flared_outer_disk",
            "thick/flared parent without projection-dominant caveat",
            "outer flare gradient; HI extent; vertical profile",
            "proxy_only",
        )

    if family == "K_scale_tail_spiral":
        if "rotation_current_proxy_mismatch" in fl or "gas_rich_late_or_irregular" in fl:
            if mean_gas >= 0.30 and mean_log_sbdisk <= 1.0:
                return (
                    "K_disturbed_outer_tail",
                    "gas-rich diffuse/irregular source proxy suggests tail/history sensitivity",
                    "HI asymmetry maps; outer-tail transition radius; environment review",
                    "proxy_only",
                )
        return (
            "K_smooth_n2_tail",
            "scale-tail parent with available smooth n=2 shell",
            "HI radius/profile transition and stable tail support",
            "proxy_only",
        )

    if family == "K_exponential_disk":
        if cv or "rotation_current_proxy_mismatch" in fl or max_bulge > 0.05:
            return (
                "K_expdisk_overlay",
                "exponential disk has caveat, bulge/core/projection, or memory mismatch proxy",
                "bar/core/projection/history overlay source review",
                "proxy_only",
            )
        if confidence >= 0.9:
            return (
                "K_clean_expdisk",
                "clean high-confidence exponential disk proxy",
                "external disk-family audit and stable scale source",
                "proxy_only",
            )
        return (
            "K_expdisk_overlay",
            "exponential parent but confidence/caveat not strong enough for clean disk",
            "clean-disk audit plus caveat resolution",
            "proxy_only",
        )

    if family == "K_compact_finite":
        if mean_bulge >= 0.10 or max_bulge >= 0.20:
            return (
                "K_true_compact",
                "bulge/core support is high enough for compact-dominant proxy",
                "compact support radius and bulge/core decomposition",
                "proxy_only",
            )
        return (
            "K_compact_plus_disk",
            "compact parent but extended disk likely remains readout-relevant",
            "bulge-to-disk decomposition plus disk/tail overlay source",
            "proxy_only",
        )

    return (
        "K_unknown_subfamily",
        "parent family not in first-pass subfamily selector",
        "manual residual-blind source review",
        "blocked",
    )


def build_manifest() -> pd.DataFrame:
    atlas = pd.read_csv(DATA / "multigalaxy_fit_inspection_summary.csv")
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    memory = pd.read_csv(DATA / "morphological_memory_history_proxy.csv")
    cols = [
        "galaxy",
        "split",
        "formula_family",
        "manifest_confidence",
        "manifest_caveat",
        "type_bin",
        "inc_bin",
        "inclination_deg",
        "mean_gas",
        "mean_bulge",
        "max_bulge",
        "mean_log_sbdisk",
        "scale_radius_proxy_kpc",
        "tail_inner_radius_proxy_kpc",
        "tail_cutoff_radius_proxy_kpc",
        "compact_support_radius_proxy_kpc",
        "thickness_h_over_rs_proxy",
    ]
    base = atlas[["galaxy"]].merge(manifest[cols], on="galaxy", how="left")
    base = base.merge(
        memory[
            [
                "galaxy",
                "rotation_inferred_family",
                "source_memory_proxy_flags",
                "memory_history_proxy_class",
            ]
        ],
        on="galaxy",
        how="left",
    )
    rows = []
    for _, row in base.iterrows():
        subfamily, reason, missing, status = choose_subfamily(row)
        rows.append(
            {
                **row.to_dict(),
                "proposed_readout_subfamily": subfamily,
                "subfamily_selection_reason": reason,
                "missing_for_acceptance": missing,
                "subfamily_status": status,
                "uses_vobs_for_selection": False,
                "endpoint_scores_computed": False,
                "accepted_label": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows).sort_values("galaxy")


def build_gate(manifest: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "gate_id": "SOI1_SCHEMA_DEFINED",
            "gate_status": "PASS",
            "evidence": "subfamily observable fields and forbidden sources are recorded",
            "remaining_obligation": "none",
        },
        {
            "gate_id": "SOI2_FIRST_PASS_MANIFEST_POPULATED",
            "gate_status": "PASS" if len(manifest) > 0 else "BLOCKED",
            "evidence": f"{len(manifest)} atlas galaxies receive first-pass subfamily proposals",
            "remaining_obligation": "extend to larger source-rich set",
        },
        {
            "gate_id": "SOI3_NO_ENDPOINT_SELECTION",
            "gate_status": "PASS" if not manifest["uses_vobs_for_selection"].any() else "FAIL",
            "evidence": "subfamily choices use manifest/source proxy fields, not vobs scores",
            "remaining_obligation": "preserve this boundary during audit",
        },
        {
            "gate_id": "SOI4_ACCEPTED_SOURCE_READY",
            "gate_status": "PENDING",
            "evidence": "all rows remain first-pass/proxy-only or diagnostic; no accepted subfamily labels promoted",
            "remaining_obligation": "fill accepted residual-blind observables per missing_for_acceptance",
        },
    ]
    df = pd.DataFrame(rows)
    df["endpoint_scores_allowed"] = False
    df["claim_boundary"] = CLAIM_BOUNDARY
    return df


def write_report(fields: pd.DataFrame, manifest: pd.DataFrame, gate: pd.DataFrame) -> None:
    summary = (
        manifest.groupby(["formula_family", "proposed_readout_subfamily", "subfamily_status"], as_index=False)
        .agg(n_galaxies=("galaxy", "nunique"))
        .sort_values(["formula_family", "proposed_readout_subfamily"])
    )
    lines = [
        "# Readout-Subfamily Observable Intake",
        "",
        "This first-pass intake proposes readout-relevant subfamilies from",
        "residual-blind manifest/source fields. It is not an accepted label layer",
        "and it does not compute endpoint scores.",
        "",
        "## Gate Status",
        "",
        markdown_table(gate),
        "",
        "## Observable Fields",
        "",
        markdown_table(fields),
        "",
        "## First-Pass Subfamily Summary",
        "",
        markdown_table(summary),
        "",
        "## First-Pass Manifest",
        "",
        markdown_table(
            manifest[
                [
                    "galaxy",
                    "formula_family",
                    "proposed_readout_subfamily",
                    "subfamily_selection_reason",
                    "missing_for_acceptance",
                    "subfamily_status",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "The intake is a residual-blind proposal layer. It is designed to be",
        "audited before endpoint scoring. The next step is to replace proxy reasons",
        "with accepted source observables such as HI asymmetry, warp onset, bar/core",
        "decomposition, vertical flare, and projection-safety evidence.",
        "",
    ]
    (REPORTS / "readout_subfamily_observable_intake.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    fields = pd.DataFrame(FIELD_ROWS)
    fields["claim_boundary"] = CLAIM_BOUNDARY
    manifest = build_manifest()
    gate = build_gate(manifest)
    fields.to_csv(DATA / "readout_subfamily_observable_fields.csv", index=False)
    manifest.to_csv(DATA / "readout_subfamily_observable_intake_manifest.csv", index=False)
    gate.to_csv(DATA / "readout_subfamily_observable_intake_gate.csv", index=False)
    write_report(fields, manifest, gate)
    print(gate.to_string(index=False))
    print(manifest[["galaxy", "formula_family", "proposed_readout_subfamily", "subfamily_status"]].to_string(index=False))


if __name__ == "__main__":
    main()
