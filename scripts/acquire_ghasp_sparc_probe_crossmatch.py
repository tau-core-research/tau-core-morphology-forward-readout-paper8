#!/usr/bin/env python3
"""Acquire GHASP side-resolved Halpha rotation points and crossmatch SPARC."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
EXTERNAL = ROOT / "data" / "external" / "catalogs" / "ghasp"
REPORTS = ROOT / "reports"
URL = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/MNRAS/388/500/tablef&-out.all"


def normalize_name(value: str) -> str:
    name = re.sub(r"[^A-Z0-9]", "", value.upper())
    match = re.fullmatch(r"(UGC|NGC|IC)0*(\d+)", name)
    return f"{match.group(1)}{int(match.group(2))}" if match else name


def parse_vizier_tsv(text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    start = next(index for index, line in enumerate(lines) if line.startswith("recno\tName\t"))
    rows = []
    for row in csv.DictReader(io.StringIO("\n".join(lines[start:])), delimiter="\t"):
        if not row.get("Name") or row["Name"].strip() == "---------":
            continue
        if not row.get("Vrot", "").strip().lstrip("-").isdigit():
            continue
        rows.append({key: value.strip() for key, value in row.items()})
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    raw_path = EXTERNAL / "J_MNRAS_388_500_tablef.tsv"
    text = urllib.request.urlopen(URL, timeout=60).read().decode("utf-8")
    raw_path.write_text(text, encoding="utf-8")
    raw_sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
    ghasp_rows = parse_vizier_tsv(text)

    with (DATA / "external_sparc_master_table.csv").open(newline="", encoding="utf-8") as handle:
        sparc_rows = list(csv.DictReader(handle))
    sparc_by_name = {normalize_name(row["Galaxy"]): row for row in sparc_rows}

    matched_points = []
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in ghasp_rows:
        key = normalize_name(row["Name"])
        if key not in sparc_by_name:
            continue
        sparc = sparc_by_name[key]
        point = {
            "galaxy": sparc["Galaxy"],
            "ghasp_name": row["Name"],
            "radius_kpc": row["r"],
            "radius_error_kpc": row["e_r"],
            "radius_arcsec": row["r2"],
            "radius_error_arcsec": row["e_r2"],
            "velocity_km_s": row["Vrot"],
            "velocity_error_km_s": row["e_Vrot"],
            "side": row["Side"],
            "n_velocity_bins": row["NBins"],
            "source_url": URL,
            "endpoint_access": False,
            "claim_boundary": "source-side Halpha probe acquisition only",
        }
        matched_points.append(point)
        grouped[sparc["Galaxy"]].append(row)

    summary_rows = []
    for galaxy, rows in sorted(grouped.items()):
        sparc = next(row for row in sparc_rows if row["Galaxy"] == galaxy)
        sides = sorted({row["Side"] for row in rows})
        radii = [float(row["r"]) for row in rows]
        summary_rows.append(
            {
                "galaxy": galaxy,
                "ghasp_name": rows[0]["Name"],
                "n_points": len(rows),
                "n_approaching": sum(row["Side"] == "a" for row in rows),
                "n_receding": sum(row["Side"] == "r" for row in rows),
                "both_sides_present": set(sides) == {"a", "r"},
                "radius_min_kpc": min(radii),
                "radius_max_kpc": max(radii),
                "sparc_rdisk_kpc": sparc["Rdisk_kpc"],
                "sparc_rhi_kpc": sparc["RHI_kpc"],
                "sparc_reference": sparc["Ref"],
                "hi_velocity_field_status": "NOT_ACQUIRED",
                "probe_status": "HALPHA_SINGLE_SIDE_SOURCE_ACQUIRED_HI_COSPATIAL_FIELD_OPEN",
                "endpoint_access": False,
            }
        )

    if not matched_points or not summary_rows:
        raise RuntimeError("GHASP-SPARC crossmatch unexpectedly empty")
    write_csv(DATA / "ghasp_sparc_side_rotation_points_v01.csv", matched_points)
    write_csv(DATA / "ghasp_sparc_probe_crossmatch_v01.csv", summary_rows)

    result = {
        "schema": "ghasp_sparc_probe_crossmatch_v01",
        "status": "GHASP_SPARC_ONE_OBJECT_HALPHA_SOURCE_ACQUIRED_SINGLE_SIDE_ONLY_HI_FIELD_OPEN",
        "source_url": URL,
        "source_catalog": "J/MNRAS/388/500/tablef",
        "raw_path": str(raw_path.relative_to(ROOT)),
        "raw_sha256": raw_sha256,
        "ghasp_rows": len(ghasp_rows),
        "ghasp_galaxies": len({normalize_name(row["Name"]) for row in ghasp_rows}),
        "sparc_galaxies": len(sparc_rows),
        "overlap_galaxies": [row["galaxy"] for row in summary_rows],
        "overlap_points": len(matched_points),
        "endpoint_access": False,
        "collective_a_row_constructed": False,
        "claim_boundary": "source acquisition and identity/radial coverage only; no H I-Halpha common-parent transport, A_p row, residual test, or Tau Core claim",
    }
    (DATA / "ghasp_sparc_probe_crossmatch_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    rows_text = "\n".join(
        f"| {row['galaxy']} | {row['n_points']} | {row['n_approaching']} | {row['n_receding']} | {row['radius_min_kpc']:.2f} | {row['radius_max_kpc']:.2f} | {row['hi_velocity_field_status']} |"
        for row in summary_rows
    )
    (REPORTS / "ghasp_sparc_probe_crossmatch_v01.md").write_text(
        f"""# GHASP-SPARC Halpha Probe Crossmatch v0.1

**Status:** `{result['status']}`

The VizieR `J/MNRAS/388/500/tablef` source contains side-labelled GHASP Halpha
rotation points for 93 galaxies. Exact normalized-name crossmatch against the
local 175-galaxy SPARC master table yields one object.

| galaxy | points | approaching | receding | R min kpc | R max kpc | H I field |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
{rows_text}

This promotes `OC-P02` from a generic source idea to a one-object Halpha
acquisition route. The overlap supplies only approaching-side rows, so it does
not yet create a parity pair or a co-spatial H I-Halpha probe row. The matched
source-native H I velocity field, a receding-side ionized-gas control, and
common geometry/radial transport remain open.

No observed rotation residual was used in acquisition or crossmatching.
""",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
