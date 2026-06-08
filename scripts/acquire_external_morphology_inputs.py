#!/usr/bin/env python3
"""Acquire available external SPARC/S4G morphology inputs."""

from __future__ import annotations

import re
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from astroquery.vizier import Vizier


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
EXTERNAL = ROOT / "data" / "external"
REPORTS = ROOT / "reports"

SPARC_URL = "https://astroweb.case.edu/SPARC/SPARC_Lelli2016c.mrt"
S4G_CATALOG = "J/ApJS/219/4"
SPARC_TO_S4G_ALIAS_OVERRIDES = {
    "UGC08286": "NGC5023",
}


SPARC_COLUMNS = [
    "Galaxy",
    "T",
    "D_Mpc",
    "e_D_Mpc",
    "f_D",
    "Inc_deg",
    "e_Inc_deg",
    "L36_1e9Lsun",
    "e_L36_1e9Lsun",
    "Reff_kpc",
    "SBeff_Lsun_pc2",
    "Rdisk_kpc",
    "SBdisk_Lsun_pc2",
    "MHI_1e9Msun",
    "RHI_kpc",
    "Vflat_kms",
    "e_Vflat_kms",
    "Q",
    "Ref",
]


def ensure_dirs() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (EXTERNAL / "sparc").mkdir(parents=True, exist_ok=True)
    (EXTERNAL / "s4g").mkdir(parents=True, exist_ok=True)


def download(url: str, path: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Paper8-data-acquisition/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            path.write_bytes(response.read())
    except Exception:
        if path.exists() and path.stat().st_size > 0:
            print(f"download failed; using cached file: {path}")
            return
        raise


def parse_sparc_mrt(path: Path) -> pd.DataFrame:
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.split()
        if len(parts) < len(SPARC_COLUMNS):
            continue
        try:
            int(parts[1])
            float(parts[2])
            float(parts[3])
            int(parts[4])
            float(parts[5])
        except ValueError:
            continue
        row = dict(zip(SPARC_COLUMNS, parts[: len(SPARC_COLUMNS)]))
        rows.append(row)
    df = pd.DataFrame(rows)
    numeric = [col for col in SPARC_COLUMNS if col not in {"Galaxy", "Ref"}]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def norm_variants(name: str) -> set[str]:
    base = re.sub(r"[^A-Z0-9]", "", str(name).upper())
    out = {base}
    out.add(re.sub(r"ESO(\d+)G(\d+)", r"ESO\1\2", base))
    match = re.match(r"([A-Z]+)0+(\d+)$", base)
    if match:
        out.add(match.group(1) + match.group(2))
    match = re.match(r"([A-Z]+)(\d+)$", base)
    if match:
        prefix, number = match.group(1), match.group(2)
        for width in [3, 4, 5]:
            out.add(prefix + number.zfill(width))
    return out


def acquire_s4g() -> tuple[pd.DataFrame, pd.DataFrame]:
    Vizier.ROW_LIMIT = -1
    catalogs = Vizier.get_catalogs(S4G_CATALOG)
    galaxies = catalogs["J/ApJS/219/4/galaxies"].to_pandas()
    table7 = catalogs["J/ApJS/219/4/table7"].to_pandas()
    return galaxies, table7


def best_s4g_match(name: str, s4g_names: dict[str, str]) -> str | None:
    override = SPARC_TO_S4G_ALIAS_OVERRIDES.get(str(name).upper())
    if override is not None:
        return override
    for variant in norm_variants(name):
        if variant in s4g_names:
            return s4g_names[variant]
    return None


def extract_disk_components(table7: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, group in table7.groupby("Name"):
        disk = group[(group["C"].astype(str).str.strip() == "D") & group["hr3"].notna()]
        edge = group[(group["C"].astype(str).str.strip() == "Z") & group["hr2"].notna()]
        bar = group[(group["C"].astype(str).str.strip() == "BAR") & group["Rbar"].notna()]
        if not disk.empty:
            disk_hr = float(disk.iloc[0]["hr3"])
            disk_component = "D:expdisk_hr3"
        elif not edge.empty:
            disk_hr = float(edge.iloc[0]["hr2"])
            disk_component = "Z:edgedisk_hr2"
        else:
            disk_hr = np.nan
            disk_component = "missing"
        rows.append(
            {
                "s4g_name": name,
                "s4g_disk_scale_arcsec": disk_hr,
                "s4g_disk_component_source": disk_component,
                "s4g_bar_radius_arcsec": float(bar.iloc[0]["Rbar"]) if not bar.empty else np.nan,
                "s4g_model_components": ";".join(group["C"].dropna().astype(str).unique()),
                "s4g_model_quality_values": ";".join(group["Q"].dropna().astype(str).unique()),
            }
        )
    return pd.DataFrame(rows)


def build_candidates(
    manifest: pd.DataFrame,
    sparc: pd.DataFrame,
    s4g_galaxies: pd.DataFrame,
    s4g_components: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    s4g_name_lookup: dict[str, str] = {}
    for name in s4g_galaxies["Name"]:
        for variant in norm_variants(name):
            s4g_name_lookup[variant] = name

    sparc_lookup = sparc.set_index("Galaxy")
    s4g_basic = s4g_galaxies.rename(columns={"Name": "s4g_name"})
    s4g_join = s4g_basic.merge(s4g_components, on="s4g_name", how="left")

    rows = []
    crossmatch_rows = []
    for _, item in manifest.iterrows():
        galaxy = item["galaxy"]
        s4g_name = best_s4g_match(galaxy, s4g_name_lookup)
        sparc_row = sparc_lookup.loc[galaxy] if galaxy in sparc_lookup.index else None
        s4g_row = (
            s4g_join.loc[s4g_join["s4g_name"] == s4g_name].iloc[0]
            if s4g_name is not None and (s4g_join["s4g_name"] == s4g_name).any()
            else None
        )
        d_mpc = float(sparc_row["D_Mpc"]) if sparc_row is not None else np.nan
        disk_arcsec = (
            float(s4g_row["s4g_disk_scale_arcsec"])
            if s4g_row is not None and pd.notna(s4g_row["s4g_disk_scale_arcsec"])
            else np.nan
        )
        scale_kpc = disk_arcsec * d_mpc / 206.265 if pd.notna(disk_arcsec) and pd.notna(d_mpc) else np.nan
        bar_arcsec = (
            float(s4g_row["s4g_bar_radius_arcsec"])
            if s4g_row is not None and pd.notna(s4g_row["s4g_bar_radius_arcsec"])
            else np.nan
        )
        bar_kpc = bar_arcsec * d_mpc / 206.265 if pd.notna(bar_arcsec) and pd.notna(d_mpc) else np.nan

        source_status = "S4G_MATCHED" if s4g_name is not None else "NO_S4G_MATCH"
        scale_status = "ACQUIRED_S4G_SPARC_DERIVED" if pd.notna(scale_kpc) else "MISSING"
        rows.append(
            {
                "galaxy": galaxy,
                "proxy_formula_family_for_scope": item["formula_family"],
                "sparc_distance_mpc": d_mpc,
                "sparc_rdisk_kpc": float(sparc_row["Rdisk_kpc"]) if sparc_row is not None else np.nan,
                "sparc_inclination_deg": float(sparc_row["Inc_deg"]) if sparc_row is not None else np.nan,
                "s4g_match_status": source_status,
                "s4g_name": s4g_name or "",
                "s4g_disk_scale_arcsec": disk_arcsec,
                "scale_radius_kpc": scale_kpc,
                "scale_radius_source": "S4G_Pipeline4_disk_scale_arcsec_x_SPARC_distance",
                "s4g_bar_radius_arcsec": bar_arcsec,
                "bar_radius_kpc": bar_kpc,
                "s4g_model_components": s4g_row["s4g_model_components"] if s4g_row is not None else "",
                "s4g_model_quality_values": s4g_row["s4g_model_quality_values"] if s4g_row is not None else "",
                "candidate_observable_status": scale_status,
                "observable_provenance": (
                    "SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4"
                    if s4g_name is not None
                    else "SPARC_Lelli2016c.mrt"
                ),
                "residual_blind_certification": "pre_endpoint_external_catalog_query",
                "claim_boundary": "candidate_source_observable_not_family_label_validation",
            }
        )
        crossmatch_rows.append(
            {
                "galaxy": galaxy,
                "proxy_formula_family_for_scope": item["formula_family"],
                "sparc_present": sparc_row is not None,
                "s4g_match_status": source_status,
                "ned_nedd_match_status": "TO_BE_CHECKED",
                "dustpedia_match_status": "TO_BE_CHECKED",
                "phangs_match_status": "TO_BE_CHECKED",
                "hi_survey_match_status": "TO_BE_CHECKED",
                "primary_morphology_source": "S4G" if s4g_name is not None else "TO_BE_ASSIGNED",
                "secondary_morphology_source": "DustPedia/NED_NEDD_TO_BE_CHECKED",
                "accepted_observable_collection_status": (
                    "PARTIAL_S4G_SCALE_CANDIDATE" if pd.notna(scale_kpc) else "NOT_STARTED"
                ),
                "crossmatch_notes": (
                    "S4G disk scale candidate acquired; family label still requires audit"
                    if pd.notna(scale_kpc)
                    else "No S4G disk scale candidate acquired"
                ),
            }
        )
    return pd.DataFrame(rows), pd.DataFrame(crossmatch_rows)


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(candidates: pd.DataFrame) -> None:
    total = len(candidates)
    matched = int((candidates["s4g_match_status"] == "S4G_MATCHED").sum())
    acquired_scale = int((candidates["candidate_observable_status"] == "ACQUIRED_S4G_SPARC_DERIVED").sum())
    by_family = (
        candidates.groupby("proxy_formula_family_for_scope", as_index=False)
        .agg(
            n_galaxies=("galaxy", "count"),
            n_s4g_matched=("s4g_match_status", lambda s: int((s == "S4G_MATCHED").sum())),
            n_scale_acquired=("candidate_observable_status", lambda s: int((s == "ACQUIRED_S4G_SPARC_DERIVED").sum())),
        )
    )
    lines = [
        "# External Morphology Input Acquisition",
        "",
        "This report records the first actual external-source acquisition for the",
        "Paper 8 accepted-observable path. It downloads SPARC Table 1 from the",
        "official SPARC site and S4G Pipeline 4 tables from VizieR/CDS through",
        "astroquery.",
        "",
        "## Verdict",
        "",
        f"SPARC master rows acquired: {total}.",
        f"S4G crossmatches acquired: {matched}.",
        f"S4G/SPARC-derived disk scale candidates acquired: {acquired_scale}.",
        "",
        "These are candidate source observables, not a completed accepted manifest.",
        "In particular, S4G disk scales can support `scale_radius_kpc` where matched,",
        "but `formula_family`, confidence/caveat, tail transition radii, thickness,",
        "and full provenance still require the accepted-source audit path.",
        "",
        "## Family Acquisition Summary",
        "",
        markdown_table(by_family),
        "",
        "## Claim Boundary",
        "",
        "This acquisition does not compute endpoint scores and does not validate Tau",
        "Core. It reduces the missing-input blocker by acquiring a source-native",
        "S4G/SPARC disk-scale candidate subset.",
    ]
    (REPORTS / "external_morphology_input_acquisition.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    ensure_dirs()
    sparc_raw = EXTERNAL / "sparc" / "SPARC_Lelli2016c.mrt"
    download(SPARC_URL, sparc_raw)
    sparc = parse_sparc_mrt(sparc_raw)
    s4g_galaxies, s4g_table7 = acquire_s4g()
    s4g_components = extract_disk_components(s4g_table7)

    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    candidates, crossmatch = build_candidates(manifest, sparc, s4g_galaxies, s4g_components)

    sparc.to_csv(DATA / "external_sparc_master_table.csv", index=False)
    s4g_galaxies.to_csv(DATA / "external_s4g_galaxies.csv", index=False)
    s4g_table7.to_csv(DATA / "external_s4g_table7.csv", index=False)
    s4g_components.to_csv(DATA / "external_s4g_disk_component_summary.csv", index=False)
    candidates.to_csv(DATA / "external_s4g_sparc_observable_candidates.csv", index=False)
    crossmatch.to_csv(DATA / "sparc_external_source_crossmatch_acquired.csv", index=False)
    write_report(candidates)
    print("PAPER8_EXTERNAL_MORPHOLOGY_INPUT_ACQUISITION_COMPLETE")


if __name__ == "__main__":
    main()
