#!/usr/bin/env python3
"""Build a morphology-memory/history proxy diagnostic layer.

The layer records cases where the current catalog/proxy morphology and the
rotation-inferred readout preference disagree.  It is a hypothesis generator
only: it is not residual-blind accepted morphology evidence and is not an
endpoint score.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = (
    "morphological_memory_proxy_not_accepted_label_not_endpoint_validation"
)


def join_flags(flags: list[str]) -> str:
    if not flags:
        return "none"
    return ";".join(sorted(set(flags)))


def source_flags(row: pd.Series) -> list[str]:
    flags: list[str] = []
    if float(row.get("mean_gas", 0.0)) >= 0.35 or row.get("type_bin") == "irregular_T_ge_9":
        flags.append("gas_rich_late_or_irregular")
    if float(row.get("mean_log_sbdisk", 99.0)) <= 0.75:
        flags.append("low_surface_brightness_or_diffuse")
    if float(row.get("mean_bulge", 0.0)) >= 0.10 or float(row.get("max_bulge", 0.0)) >= 0.20:
        flags.append("bulge_or_compact_core_memory")
    if "vertical_geometry_proxy_only" in str(row.get("manifest_caveat", "")):
        flags.append("vertical_geometry_proxy_only")
    if "large_distance_error" in str(row.get("manifest_caveat", "")):
        flags.append("distance_caveat")
    if "low_inclination" in str(row.get("manifest_caveat", "")):
        flags.append("inclination_caveat")
    return flags


def external_flags(row: pd.Series) -> list[str]:
    flags: list[str] = []
    caveat = str(row.get("external_family_label_caveat", ""))
    components = str(row.get("s4g_model_components", ""))
    if "bar" in caveat or "BAR" in components:
        flags.append("bar_component_caveat")
    if "edge" in caveat or "edgedisk" in caveat.lower() or "Z" in components.split(";"):
        flags.append("edge_or_projection_caveat")
    return flags


def classify_memory_proxy(row: pd.Series) -> str:
    current = row["current_proxy_family"]
    inferred = row["rotation_inferred_family"]
    has_external_expdisk = pd.notna(row.get("external_family_label"))

    if current == inferred and (
        not has_external_expdisk or bool(row["matches_external_family"])
    ):
        return "current_readout_consistent_no_memory_proxy_flag"
    if has_external_expdisk and inferred == "K_scale_tail_spiral":
        return "expdisk_current_with_scale_tail_readout_memory_candidate"
    if has_external_expdisk and inferred == "K_thick_flared":
        return "expdisk_current_with_vertical_projection_memory_candidate"
    if has_external_expdisk and inferred == "K_compact_finite":
        return "expdisk_current_with_compact_core_memory_candidate"
    if current == "K_scale_tail_spiral" and inferred == "K_exponential_disk":
        return "scale_tail_current_with_expdisk_readout_memory_candidate"
    if current == "K_exponential_disk" and inferred == "K_scale_tail_spiral":
        return "expdisk_proxy_with_scale_tail_readout_memory_candidate"
    if current == "K_thick_flared" and inferred != "K_thick_flared":
        return "thick_flared_proxy_with_alternate_readout_memory_candidate"
    if current == "K_compact_finite" and inferred != "K_compact_finite":
        return "compact_proxy_with_alternate_readout_memory_candidate"
    return "generic_current_vs_rotation_readout_mismatch_candidate"


def build_proxy() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    rotation = pd.read_csv(DATA / "rotation_inferred_morphology_diagnostic.csv")
    external = pd.read_csv(DATA / "exponential_disk_family_label_audit.csv")

    rows = manifest.merge(
        rotation[
            [
                "galaxy",
                "rotation_inferred_family",
                "rotation_inferred_confidence",
                "rotation_inferred_margin_to_second",
                "matches_predeclared_family",
                "predeclared_family_rank_by_rotation",
            ]
        ],
        on="galaxy",
        how="left",
        validate="one_to_one",
    ).merge(
        external[
            [
                "galaxy",
                "external_family_label",
                "external_family_label_status",
                "external_family_label_caveat",
                "narrow_dry_run_lane",
                "s4g_model_components",
            ]
        ],
        on="galaxy",
        how="left",
    )

    output_rows = []
    for _, row in rows.iterrows():
        flags = source_flags(row) + external_flags(row)
        current = row["formula_family"]
        inferred = row["rotation_inferred_family"]
        matches_current = bool(row["matches_predeclared_family"])
        matches_external = (
            pd.notna(row.get("external_family_label"))
            and inferred == row.get("external_family_label")
        )
        if not matches_current:
            flags.append("rotation_current_proxy_mismatch")
        if pd.notna(row.get("external_family_label")) and not matches_external:
            flags.append("rotation_external_family_mismatch")

        record = {
            "galaxy": row["galaxy"],
            "split": row["split"],
            "current_proxy_family": current,
            "rotation_inferred_family": inferred,
            "rotation_inferred_confidence": row["rotation_inferred_confidence"],
            "rotation_inferred_margin_to_second": row[
                "rotation_inferred_margin_to_second"
            ],
            "predeclared_family_rank_by_rotation": row[
                "predeclared_family_rank_by_rotation"
            ],
            "matches_current_proxy_family": matches_current,
            "external_family_label": row.get("external_family_label"),
            "external_family_label_status": row.get("external_family_label_status"),
            "external_family_present": pd.notna(row.get("external_family_label")),
            "matches_external_family": matches_external,
            "external_family_mismatch": (
                pd.notna(row.get("external_family_label")) and not matches_external
            ),
            "type_bin": row["type_bin"],
            "manifest_confidence": row["manifest_confidence"],
            "manifest_caveat": row["manifest_caveat"],
            "mean_gas": row["mean_gas"],
            "mean_bulge": row["mean_bulge"],
            "max_bulge": row["max_bulge"],
            "mean_log_sbdisk": row["mean_log_sbdisk"],
            "source_memory_proxy_flags": join_flags(flags),
            "proxy_status": (
                "SOURCE_PLUS_INVERSE_HYPOTHESIS"
                if not matches_current or pd.notna(row.get("external_family_label"))
                else "SOURCE_ONLY_CURRENT_PROXY_CONTEXT"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        record["memory_history_proxy_class"] = classify_memory_proxy(pd.Series(record))
        output_rows.append(record)

    proxy = pd.DataFrame(output_rows).sort_values("galaxy").reset_index(drop=True)
    summary = (
        proxy.groupby("memory_history_proxy_class", as_index=False)
        .agg(
            n_galaxies=("galaxy", "size"),
            n_rotation_current_mismatches=(
                "matches_current_proxy_family",
                lambda values: int((~values).sum()),
            ),
            n_external_rows=("external_family_label", lambda values: int(values.notna().sum())),
            n_external_mismatches=("external_family_mismatch", "sum"),
            median_rotation_margin=("rotation_inferred_margin_to_second", "median"),
        )
        .sort_values(["n_galaxies", "memory_history_proxy_class"], ascending=[False, True])
    )
    external_summary = (
        proxy[proxy["external_family_label"].notna()]
        .groupby(
            [
                "external_family_label",
                "memory_history_proxy_class",
                "rotation_inferred_family",
            ],
            as_index=False,
        )
        .agg(
            n_galaxies=("galaxy", "size"),
            n_matches_external=("matches_external_family", "sum"),
            median_margin=("rotation_inferred_margin_to_second", "median"),
        )
        .sort_values(["memory_history_proxy_class", "rotation_inferred_family"])
    )
    return proxy, summary, external_summary


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(
    proxy: pd.DataFrame, summary: pd.DataFrame, external_summary: pd.DataFrame
) -> None:
    total = len(proxy)
    current_mismatches = int((~proxy["matches_current_proxy_family"]).sum())
    external = proxy[proxy["external_family_label"].notna()]
    external_mismatches = int((~external["matches_external_family"]).sum())
    scale_tail_expdisk = int(
        (
            external["memory_history_proxy_class"]
            == "expdisk_current_with_scale_tail_readout_memory_candidate"
        ).sum()
    )
    thick_expdisk = int(
        (
            external["memory_history_proxy_class"]
            == "expdisk_current_with_vertical_projection_memory_candidate"
        ).sum()
    )
    lines = [
        "# Morphological Memory / History Proxy Diagnostic",
        "",
        "This diagnostic records a conservative proxy layer for the possibility that",
        "the currently observed morphology is not the full readout-relevant",
        "morphological state. A galaxy may have had a different earlier structure,",
        "or the Tau Core readout may encode an integrated morphology/history",
        "component rather than only the present catalog shape.",
        "",
        "The layer combines source-side morphology/context flags with the",
        "rotation-inferred readout-family diagnostic. Because the rotation-inferred",
        "component is not residual-blind, this is a hypothesis generator only.",
        "",
        "## Verdict",
        "",
        f"Current proxy family and rotation-inferred family disagree in {current_mismatches}/{total} rows.",
        f"Within the 13 externally supported exponential-disk rows, {external_mismatches}/13 do not infer the exponential-disk readout family.",
        f"Of those external exponential-disk rows, {scale_tail_expdisk} are scale-tail readout-memory candidates and {thick_expdisk} are vertical/projection readout-memory candidates.",
        "",
        "This is not evidence that the historical morphology is known. It is a",
        "reproducible triage layer for deciding where a future residual-blind",
        "history/memory observable should be collected.",
        "",
        "## Proxy Classes",
        "",
        markdown_table(summary),
        "",
        "## External Exponential-Disk Subset",
        "",
        markdown_table(external_summary),
        "",
        "## Claim Boundary",
        "",
        "This proxy is not an accepted morphology label and not an endpoint score.",
        "The morphological memory / history proxy is not an accepted morphology",
        "label, not an endpoint score, not empirical validation, and not proof that",
        "Tau Core has recovered galaxy history. It is a pre-endpoint hypothesis",
        "layer that marks possible current-shape/readout-history mismatches for",
        "future residual-blind testing.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "morphological_memory_history_proxy.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    proxy, summary, external_summary = build_proxy()
    proxy.to_csv(DATA / "morphological_memory_history_proxy.csv", index=False)
    summary.to_csv(DATA / "morphological_memory_history_proxy_summary.csv", index=False)
    external_summary.to_csv(
        DATA / "morphological_memory_history_proxy_external_expdisk.csv",
        index=False,
    )
    write_report(proxy, summary, external_summary)
    print("PAPER8_MORPHOLOGICAL_MEMORY_HISTORY_PROXY_COMPLETE")


if __name__ == "__main__":
    main()
