#!/usr/bin/env python3
"""Build P0 morphology inspection packets.

The packets are residual-blind review templates for the highest-priority
morphology inspection targets.  They summarize existing source context and leave
the actual morphology/history observations blank for a future external audit.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
PACKET_DIR = REPORTS / "p0_morphology_packets"

CLAIM_BOUNDARY = "p0_morphology_packets_not_accepted_label_not_endpoint"


def safe_text(value: object) -> str:
    if pd.isna(value):
        return "MISSING"
    return str(value)


def source_links(galaxy: str) -> str:
    query = galaxy.replace(" ", "+")
    ned = f"https://ned.ipac.caltech.edu/byname?objname={query}"
    simbad = f"https://simbad.cds.unistra.fr/simbad/sim-id?Ident={query}"
    legacy = f"https://www.legacysurvey.org/viewer?object={query}"
    return f"[NED]({ned}); [SIMBAD]({simbad}); [Legacy Survey viewer]({legacy})"


def packet_markdown(row: pd.Series) -> str:
    galaxy = row["galaxy"]
    requested = str(row["requested_external_sources"]).split(";")
    lines = [
        f"# P0 Morphology Inspection Packet: {galaxy}",
        "",
        "This packet is a residual-blind morphology/history review template.",
        "It must not be filled using endpoint residual gains, required-S_tau",
        "diagnostics, or best-fit readout-family choices.",
        "",
        "## Existing Context",
        "",
        f"- Inspection tier: `{row['inspection_priority_tier']}`",
        f"- Inspection score: `{row['inspection_priority_score']}`",
        f"- Inspection focus: `{row['inspection_focus']}`",
        f"- Current proxy family: `{row['current_proxy_family']}`",
        f"- Rotation-inferred family: `{row['rotation_inferred_family']}`",
        f"- Rotation-inferred confidence: `{row['rotation_inferred_confidence']}`",
        f"- Memory/history proxy class: `{row['memory_history_proxy_class']}`",
        f"- Source flags: `{row['source_memory_proxy_flags']}`",
        f"- External family label: `{safe_text(row['external_family_label'])}`",
        f"- External family mismatch: `{row['external_family_mismatch']}`",
        f"- S4G match status: `{safe_text(row['s4g_match_status'])}`",
        f"- S4G model components: `{safe_text(row['s4g_model_components'])}`",
        f"- Scale radius kpc: `{safe_text(row['scale_radius_kpc'])}`",
        f"- Bar radius kpc: `{safe_text(row['bar_radius_kpc'])}`",
        f"- Observable provenance: `{safe_text(row['observable_provenance'])}`",
        "",
        "## Suggested External Lookup Links",
        "",
        source_links(str(galaxy)),
        "",
        "## Requested Residual-Blind Observables",
        "",
    ]
    lines.extend(f"- `{item}`" for item in requested)
    lines.extend(
        [
            "",
            "## Blank Review Fields",
            "",
            "- Reviewer:",
            "- Review date:",
            "- Imaging/decomposition sources used:",
            "- Present-day morphology label:",
            "- Present-day morphology confidence:",
            "- Outer disk / LSB / tail evidence:",
            "- HI extent or asymmetry evidence:",
            "- Bar / m=2 evidence:",
            "- Edge-on / projection caveat:",
            "- Vertical thickness / flare / warp evidence:",
            "- Bulge / compact-core evidence:",
            "- Morphological memory/history proxy judgment:",
            "- Memory/history proxy confidence:",
            "- Residual-blind family label recommended for future endpoint:",
            "- Caveats:",
            "",
            "## Forbidden Inputs",
            "",
            "- endpoint residual gain",
            "- required-S_tau diagnostic as label input",
            "- best-fit readout family as accepted morphology evidence",
            "- post-hoc family switching after seeing endpoint scores",
            "",
            "## Claim Boundary",
            "",
            "This packet is not an accepted morphology label, not empirical validation,",
            "and not an endpoint score. It is a source-collection and manual-review",
            "template only.",
            "",
            f"Claim boundary: `{CLAIM_BOUNDARY}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_packets() -> tuple[pd.DataFrame, pd.DataFrame]:
    queue = pd.read_csv(DATA / "morphology_inspection_queue.csv")
    p0 = queue.loc[queue["inspection_priority_tier"] == "P0"].copy()
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    packet_rows = []
    for _, row in p0.iterrows():
        packet_path = PACKET_DIR / f"{row['galaxy']}.md"
        packet_path.write_text(packet_markdown(row), encoding="utf-8")
        packet_rows.append(
            {
                "galaxy": row["galaxy"],
                "packet_path": str(packet_path.relative_to(ROOT)),
                "inspection_focus": row["inspection_focus"],
                "requested_external_sources": row["requested_external_sources"],
                "current_proxy_family": row["current_proxy_family"],
                "rotation_inferred_family": row["rotation_inferred_family"],
                "s4g_match_status": row["s4g_match_status"],
                "packet_status": "PENDING_RESIDUAL_BLIND_EXTERNAL_REVIEW",
                "accepted_label_output_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    index = pd.DataFrame(packet_rows).sort_values("galaxy")
    source_need = (
        index.assign(source=index["requested_external_sources"].str.split(";"))
        .explode("source")
        .groupby("source", as_index=False)
        .agg(n_packets=("galaxy", "size"))
        .sort_values(["n_packets", "source"], ascending=[False, True])
    )
    return index, source_need


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(index: pd.DataFrame, source_need: pd.DataFrame) -> None:
    lines = [
        "# P0 Morphology Inspection Packets",
        "",
        "This index collects the four P0 morphology inspection packets produced from",
        "the morphology inspection queue. The packets are manual residual-blind",
        "review templates, not accepted labels.",
        "",
        "## Packet Index",
        "",
        markdown_table(index),
        "",
        "## Requested Source Types",
        "",
        markdown_table(source_need),
        "",
        "## Claim Boundary",
        "",
        "These packets are not endpoint scores, not accepted morphology evidence,",
        "and not validation of Tau Core. They are the first concrete audit sheets",
        "for checking whether present-day morphology, projection, or history/memory",
        "observables can explain the current-shape/readout mismatch candidates.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_morphology_inspection_packets.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    index, source_need = build_packets()
    index.to_csv(DATA / "p0_morphology_inspection_packet_index.csv", index=False)
    source_need.to_csv(DATA / "p0_morphology_inspection_source_needs.csv", index=False)
    write_report(index, source_need)
    print("PAPER8_P0_MORPHOLOGY_INSPECTION_PACKETS_COMPLETE")


if __name__ == "__main__":
    main()
