#!/usr/bin/env python3
"""Build all-sample source expansion for the information-gain test.

The goal is to map the residual-blind source coverage currently available for
L2/L4 morphology-information levels. This is not an endpoint scorer and does
not promote accepted morphology labels.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
EXTERNAL = ROOT / "data" / "external"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "source_expansion_not_label_not_endpoint"


def norm_name(name: object) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(name).upper())


def name_variants(name: object) -> set[str]:
    raw = norm_name(name)
    out = {raw}

    ngc = re.match(r"NGC0*(\d+)$", raw)
    if ngc:
        number = ngc.group(1)
        out.update({"NGC" + number, "NGC" + number.zfill(3), "NGC" + number.zfill(4)})

    eso = re.match(r"ESO0*(\d+)G?0*(\d+)$", raw)
    if eso:
        field, number = eso.group(1), eso.group(2)
        out.update(
            {
                f"ESO{field}{number}",
                f"ESO{field}{number.zfill(3)}",
                f"ESO{field}G{number}",
                f"ESO{field}G{number.zfill(3)}",
            }
        )

    letter_number = re.match(r"([A-Z]+)0*(\d+)$", raw)
    if letter_number:
        prefix, number = letter_number.group(1), letter_number.group(2)
        out.update({prefix + number, prefix + number.zfill(3), prefix + number.zfill(4)})

    return out


def build_name_index(tables: dict[str, pd.DataFrame]) -> dict[str, set[str]]:
    index: dict[str, set[str]] = {}
    for table_name, table in tables.items():
        name_columns = [c for c in table.columns if c.lower() in {"name", "simbadname"}]
        names: set[str] = set()
        for column in name_columns:
            for value in table[column].dropna():
                names.update(name_variants(value))
        index[table_name] = names
    return index


def load_dustpedia_tables() -> dict[str, pd.DataFrame]:
    tables = {}
    for path in sorted((EXTERNAL / "dustpedia").glob("*.csv")):
        tables[path.stem] = pd.read_csv(path)
    return tables


def phangs_index() -> tuple[set[str], pd.DataFrame]:
    path = EXTERNAL / "phangs" / "phangs_public_sample.csv"
    if not path.exists():
        return set(), pd.DataFrame()
    sample = pd.read_csv(path)
    sample = sample.loc[sample["Name"].notna()].copy()
    names: set[str] = set()
    for value in sample["Name"]:
        names.update(name_variants(value))
    return names, sample


def bool_true(value: object) -> bool:
    return str(value).strip().upper() == "TRUE"


def build_expansion() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    s4g = pd.read_csv(DATA / "external_s4g_sparc_observable_candidates.csv")
    dust_tables = load_dustpedia_tables()
    dust_index = build_name_index(dust_tables)
    phangs_names, phangs = phangs_index()

    s4g_by_galaxy = s4g.set_index("galaxy")
    manifest_by_galaxy = manifest.set_index("galaxy")
    phangs_by_norm = {}
    if not phangs.empty:
        for _, row in phangs.iterrows():
            for variant in name_variants(row["Name"]):
                phangs_by_norm[variant] = row

    rows = []
    dust_rows = []
    for _, item in sparc.iterrows():
        galaxy = item["Galaxy"]
        variants = name_variants(galaxy)
        manifest_row = manifest_by_galaxy.loc[galaxy] if galaxy in manifest_by_galaxy.index else None
        s4g_row = s4g_by_galaxy.loc[galaxy] if galaxy in s4g_by_galaxy.index else None

        table_matches = {
            table_name: bool(variants & names) for table_name, names in dust_index.items()
        }
        for table_name, matched in table_matches.items():
            dust_rows.append(
                {
                    "galaxy": galaxy,
                    "dustpedia_table": table_name,
                    "match_status": "MATCHED_SOURCE_EVIDENCE" if matched else "NO_DIRECT_MATCH",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

        phangs_match = bool(variants & phangs_names)
        phangs_row = next((phangs_by_norm[v] for v in variants if v in phangs_by_norm), None)
        phangs_muse = bool_true(phangs_row["VLT/MUSE"]) if phangs_row is not None else False
        phangs_alma = bool_true(phangs_row["ALMA"]) if phangs_row is not None else False

        s4g_components = str(s4g_row["s4g_model_components"]) if s4g_row is not None else ""
        s4g_scale_ready = s4g_row is not None and pd.notna(s4g_row["scale_radius_kpc"])
        s4g_bar_ready = s4g_row is not None and pd.notna(s4g_row["bar_radius_kpc"])
        s4g_compact_ready = any(token in set(s4g_components.split(";")) for token in ["B", "N"])
        sparc_hi_ready = pd.notna(item["MHI_1e9Msun"]) and pd.notna(item["RHI_kpc"]) and float(item["RHI_kpc"]) > 0
        dust_any = any(table_matches.values())
        dust_hi = table_matches.get("J_A+A_623_A5_dp-hi", False)
        dust_physical = table_matches.get("J_A+A_631_A38_tablea1", False)
        dust_profile = table_matches.get("J_A+A_622_A132_fitw1", False) or table_matches.get(
            "J_A+A_622_A132_fither", False
        )

        rows.append(
            {
                "galaxy": galaxy,
                "split": manifest_row["split"] if manifest_row is not None else "",
                "formula_family": manifest_row["formula_family"] if manifest_row is not None else "",
                "sparc_hi_ready": sparc_hi_ready,
                "sparc_mhi_1e9_msun": item["MHI_1e9Msun"],
                "sparc_rhi_kpc": item["RHI_kpc"],
                "s4g_scale_ready": bool(s4g_scale_ready),
                "s4g_bar_ready": bool(s4g_bar_ready),
                "s4g_compact_component_ready": bool(s4g_compact_ready),
                "dustpedia_any_match": dust_any,
                "dustpedia_hi_match": dust_hi,
                "dustpedia_physical_match": dust_physical,
                "dustpedia_dust_profile_match": dust_profile,
                "phangs_sample_match": phangs_match,
                "phangs_muse_ready": phangs_muse,
                "phangs_alma_ready": phangs_alma,
                "q_tail_candidate": bool(sparc_hi_ready or dust_hi),
                "q_expdisk_scale_candidate": bool(s4g_scale_ready),
                "q_bar_candidate": bool(s4g_bar_ready),
                "q_compact_candidate": bool(s4g_compact_ready or dust_physical),
                "q_memory_candidate": bool(dust_any or sparc_hi_ready or phangs_match),
                "l4_velocity_field_candidate": bool(phangs_muse),
                "source_expansion_status": "RESIDUAL_BLIND_SOURCE_CANDIDATE",
                "accepted_label_output_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    expansion = pd.DataFrame(rows)
    dust_detail = pd.DataFrame(dust_rows)
    summary = summarize(expansion)
    return expansion, dust_detail, summary


def summarize(expansion: pd.DataFrame) -> pd.DataFrame:
    fields = [
        "sparc_hi_ready",
        "s4g_scale_ready",
        "s4g_bar_ready",
        "s4g_compact_component_ready",
        "dustpedia_any_match",
        "dustpedia_hi_match",
        "dustpedia_physical_match",
        "dustpedia_dust_profile_match",
        "phangs_sample_match",
        "phangs_muse_ready",
        "phangs_alma_ready",
        "q_tail_candidate",
        "q_expdisk_scale_candidate",
        "q_bar_candidate",
        "q_compact_candidate",
        "q_memory_candidate",
        "l4_velocity_field_candidate",
    ]
    rows = []
    for field in fields:
        rows.append(
            {
                "coverage_field": field,
                "n_galaxies": int(expansion[field].astype(bool).sum()),
                "fraction": float(expansion[field].astype(bool).mean()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda x: f"{x:.6g}")
        else:
            display[col] = display[col].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def write_report(expansion: pd.DataFrame, summary: pd.DataFrame) -> None:
    holdout = expansion.loc[expansion["split"] == "holdout"]
    holdout_summary = summarize(holdout) if len(holdout) else pd.DataFrame()
    lines = [
        "# Morphology Information Gain Source Expansion",
        "",
        "This all-sample source expansion maps residual-blind source coverage for",
        "the L2/L4 morphology-information-gain layers. It does not classify",
        "galaxies, does not promote accepted labels, and does not compute endpoint",
        "scores.",
        "",
        "## Full-Sample Coverage",
        "",
        markdown_table(summary),
        "",
        "## Holdout Coverage",
        "",
        markdown_table(holdout_summary),
        "",
        "## Claim Boundary",
        "",
        "These are source candidates only. L2 readout-state weights still require",
        "accepted morphology-memory, HI/tail, compact/core, bar, thickness/flare,",
        "and normalization rules before endpoint use.",
    ]
    (REPORTS / "morphology_information_gain_source_expansion.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    expansion, dust_detail, summary = build_expansion()
    expansion.to_csv(DATA / "morphology_information_gain_source_expansion.csv", index=False)
    dust_detail.to_csv(DATA / "morphology_information_gain_dustpedia_matches.csv", index=False)
    summary.to_csv(DATA / "morphology_information_gain_source_expansion_summary.csv", index=False)
    write_report(expansion, summary)
    print("PAPER8_MORPHOLOGY_INFORMATION_GAIN_SOURCE_EXPANSION_COMPLETE")


if __name__ == "__main__":
    main()
