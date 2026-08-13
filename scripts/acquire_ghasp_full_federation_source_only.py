#!/usr/bin/env python3
"""Federate GHASP VI/VII and rank SPARC H I-Halpha probes source-only."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import urllib.request
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
EXTERNAL = ROOT / "data" / "external" / "catalogs" / "ghasp"
REPORTS = ROOT / "reports"
WHISP_LISTING = (
    ROOT
    / "data"
    / "external"
    / "literature"
    / "ngc4088_source_native_hi_route"
    / "whisp_listing_by_name.html"
)
BASE = "https://cdsarc.cds.unistra.fr/ftp/J/MNRAS"
SOURCES = {
    "vi_readme": f"{BASE}/388/500/ReadMe",
    "vi_points": f"{BASE}/388/500/tablef.dat",
    "vii_readme": f"{BASE}/390/466/ReadMe",
    "vii_aliases": f"{BASE}/390/466/tableb1.dat",
    "vii_metadata": f"{BASE}/390/466/tableb3.dat",
    "vii_points": f"{BASE}/390/466/tablef.dat",
}


def normalize_name(value: str) -> str:
    name = re.sub(r"[^A-Z0-9]", "", value.upper())
    match = re.fullmatch(r"(UGC|NGC|IC)0*(\d+)([A-Z]?)", name)
    if not match:
        return name
    return f"{match.group(1)}{int(match.group(2))}{match.group(3)}"


def fetch(url: str, path: Path) -> str:
    text = urllib.request.urlopen(url, timeout=60).read().decode("utf-8")
    path.write_text(text, encoding="utf-8")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_aliases(path: Path) -> tuple[dict[str, set[str]], dict[str, str]]:
    aliases: dict[str, set[str]] = {}
    ugc_by_name: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        primary = normalize_name(line[0:9])
        values = {primary}
        ugc = line[10:15].strip()
        ngc = line[17:21].strip()
        if ugc:
            ugc_name = f"UGC{int(ugc)}"
            values.add(ugc_name)
            ugc_by_name[primary] = ugc_name
        if ngc:
            values.add(f"NGC{int(ngc)}{line[21:22].strip().upper()}")
        aliases[primary] = values
    return aliases, ugc_by_name


def parse_metadata(path: Path) -> dict[str, dict[str, str]]:
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        rows[normalize_name(line[0:9])] = {
            "ghasp_d25_arcsec": line[61:65].strip(),
            "ghasp_d25_error_arcsec": line[66:68].strip(),
            "ghasp_hi_facility": line[92:93].strip(),
            "ghasp_hi_reference": line[94:97].strip(),
        }
    return rows


def parse_points(path: Path, release: str) -> list[dict[str, object]]:
    if release == "VI":
        slices = (slice(0, 9), slice(10, 15), slice(16, 20), slice(21, 26),
                  slice(27, 31), slice(32, 35), slice(36, 39), slice(40, 42), 43)
    else:
        slices = (slice(0, 8), slice(9, 14), slice(15, 19), slice(20, 25),
                  slice(26, 30), slice(31, 34), slice(35, 38), slice(39, 41), 42)
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        name, radius, radius_error, radius_arcsec, radius_error_arcsec, velocity, velocity_error, n_bins, side_index = slices
        rows.append(
            {
                "ghasp_release": release,
                "ghasp_name": line[name].strip(),
                "ghasp_key": normalize_name(line[name]),
                "radius_kpc": float(line[radius]),
                "radius_error_kpc": float(line[radius_error]),
                "radius_arcsec": float(line[radius_arcsec]),
                "radius_error_arcsec": float(line[radius_error_arcsec]),
                "velocity_km_s": int(line[velocity]),
                "velocity_error_km_s": int(line[velocity_error]),
                "n_velocity_bins": int(line[n_bins]),
                "side": line[side_index].strip(),
            }
        )
    return rows


class WhispParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.href: str | None = None
        self.text: list[str] = []
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self.href = dict(attrs).get("href")
            self.text = []

    def handle_data(self, data: str) -> None:
        if self.href is not None:
            self.text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.href is not None:
            self.links.append(("".join(self.text).strip(), self.href))
            self.href = None


def parse_whisp_listing(path: Path) -> dict[str, str]:
    parser = WhispParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    pages = {}
    for label, href in parser.links:
        match = re.fullmatch(r"UGC\s+(\d+)\s*", label, re.IGNORECASE)
        if match:
            pages[f"UGC{int(match.group(1))}"] = href
    return pages


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    paths = {key: EXTERNAL / f"{key}.txt" for key in SOURCES}
    hashes = {key: fetch(url, paths[key]) for key, url in SOURCES.items()}

    aliases, ugc_by_name = parse_aliases(paths["vii_aliases"])
    metadata = parse_metadata(paths["vii_metadata"])
    points = parse_points(paths["vi_points"], "VI") + parse_points(
        paths["vii_points"], "VII"
    )
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in points:
        grouped[str(row["ghasp_key"])].append(row)
    release_curve_count = sum(
        len({str(row["ghasp_key"]) for row in points if row["ghasp_release"] == release})
        for release in ("VI", "VII")
    )
    if release_curve_count != 175 or len(grouped) != 173:
        raise RuntimeError(
            "Expected 175 release-specific curves for 173 identities, got "
            f"{release_curve_count} and {len(grouped)}"
        )

    with (DATA / "external_sparc_master_table.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        sparc_rows = list(csv.DictReader(handle))
    sparc_by_name = {normalize_name(row["Galaxy"]): row for row in sparc_rows}
    whisp_pages = parse_whisp_listing(WHISP_LISTING)

    federation_rows = []
    candidate_rows = []
    for ghasp_key, galaxy_points in sorted(grouped.items()):
        alias_set = aliases.get(ghasp_key, {ghasp_key})
        matches = sorted(alias_set.intersection(sparc_by_name))
        for point in galaxy_points:
            federation_rows.append(
                {
                    **point,
                    "aliases": ";".join(sorted(alias_set)),
                    "sparc_match": sparc_by_name[matches[0]]["Galaxy"] if matches else "",
                    "source_url": SOURCES[f"{str(point['ghasp_release']).lower()}_points"],
                    "endpoint_access": False,
                    "claim_boundary": "source acquisition only; not an endpoint score",
                }
            )
        if not matches:
            continue

        sparc = sparc_by_name[matches[0]]
        sides = [str(row["side"]) for row in galaxy_points]
        n_approaching = sides.count("a")
        n_receding = sides.count("r")
        both_sides = n_approaching > 0 and n_receding > 0
        min_side = min(n_approaching, n_receding)
        meta = metadata[ghasp_key]
        ugc = ugc_by_name.get(ghasp_key, ghasp_key if ghasp_key.startswith("UGC") else "")
        whisp_href = whisp_pages.get(ugc, "")
        inclination = float(sparc["Inc_deg"])
        inclination_error = float(sparc["e_Inc_deg"])
        distance = float(sparc["D_Mpc"])
        distance_error = float(sparc["e_D_Mpc"])
        fractional_distance_error = distance_error / distance if distance else float("inf")
        max_radius_arcsec = max(float(row["radius_arcsec"]) for row in galaxy_points)
        d25_arcsec = float(meta["ghasp_d25_arcsec"] or 0)
        angular_coverage = max_radius_arcsec / d25_arcsec if d25_arcsec else 0.0

        score_parts = {
            "both_halpha_sides": 4 if both_sides else 0,
            "at_least_10_each_side": 2 if min_side >= 10 else 0,
            "at_least_20_each_side": 1 if min_side >= 20 else 0,
            "at_least_50_points": 2 if len(galaxy_points) >= 50 else 0,
            "at_least_100_points": 1 if len(galaxy_points) >= 100 else 0,
            "whisp_overview_page": 3 if whisp_href else 0,
            "ghasp_whisp_reference": 1 if meta["ghasp_hi_facility"] == "W" else 0,
            "moderate_inclination": 1 if 30 <= inclination <= 75 else 0,
            "inclination_error_le_5deg": 1 if inclination_error <= 5 else 0,
            "fractional_distance_error_le_20pct": 1 if fractional_distance_error <= 0.2 else 0,
            "halpha_coverage_ge_0p3_d25": 1 if angular_coverage >= 0.3 else 0,
            "halpha_coverage_ge_0p5_d25": 1 if angular_coverage >= 0.5 else 0,
        }
        candidate_rows.append(
            {
                "galaxy": sparc["Galaxy"],
                "ghasp_name": galaxy_points[0]["ghasp_name"],
                "ghasp_release": galaxy_points[0]["ghasp_release"],
                "aliases": ";".join(sorted(alias_set)),
                "n_halpha_points": len(galaxy_points),
                "n_approaching": n_approaching,
                "n_receding": n_receding,
                "both_halpha_sides": both_sides,
                "halpha_max_radius_arcsec": max_radius_arcsec,
                "ghasp_d25_arcsec": d25_arcsec,
                "halpha_max_radius_over_d25": round(angular_coverage, 4),
                "ghasp_hi_facility": meta["ghasp_hi_facility"],
                "ghasp_hi_reference": meta["ghasp_hi_reference"],
                "whisp_overview_available": bool(whisp_href),
                "whisp_relative_url": whisp_href,
                "sparc_inclination_deg": inclination,
                "sparc_inclination_error_deg": inclination_error,
                "sparc_distance_mpc": distance,
                "sparc_distance_error_mpc": distance_error,
                "sparc_fractional_distance_error": round(fractional_distance_error, 4),
                "source_only_score": sum(score_parts.values()),
                "score_components": ";".join(
                    key for key, value in score_parts.items() if value
                ),
                "selection_uses_vobs_or_residual": False,
                "endpoint_access": False,
                "candidate_status": "SOURCE_ACQUISITION_ONLY",
            }
        )

    candidate_rows.sort(
        key=lambda row: (
            -int(row["source_only_score"]),
            -int(row["n_halpha_points"]),
            str(row["galaxy"]),
        )
    )
    for rank, row in enumerate(candidate_rows, 1):
        row["source_only_rank"] = rank
    candidate_rows = [
        {"source_only_rank": row.pop("source_only_rank"), **row}
        for row in candidate_rows
    ]
    write_csv(DATA / "ghasp_full_federation_side_points_v01.csv", federation_rows)
    write_csv(
        DATA / "ghasp_sparc_source_only_candidate_federation_v01.csv",
        candidate_rows,
    )

    eligible = [
        row
        for row in candidate_rows
        if row["both_halpha_sides"] and row["whisp_overview_available"]
    ]
    result = {
        "schema": "ghasp_sparc_source_only_candidate_federation_v01",
        "status": "GHASP_FULL_FEDERATION_SOURCE_ONLY_CANDIDATES_RANKED_NOT_ENDPOINT",
        "source_catalogs": ["J/MNRAS/388/500", "J/MNRAS/390/466"],
        "source_urls": SOURCES,
        "source_sha256": hashes,
        "ghasp_point_rows": len(points),
        "ghasp_release_specific_rotation_curves": release_curve_count,
        "ghasp_rotation_curve_galaxies": len(grouped),
        "sparc_overlap_galaxies": len(candidate_rows),
        "both_side_overlap_galaxies": sum(
            bool(row["both_halpha_sides"]) for row in candidate_rows
        ),
        "whisp_overview_overlap_galaxies": sum(
            bool(row["whisp_overview_available"]) for row in candidate_rows
        ),
        "eligible_both_side_whisp_galaxies": len(eligible),
        "top_source_only_candidate": eligible[0]["galaxy"],
        "top_source_only_candidates": [row["galaxy"] for row in eligible[:5]],
        "ranking_inputs": [
            "Halpha side counts and total source-point count",
            "Halpha angular support divided by GHASP D25",
            "WHISP overview availability and GHASP H I reference",
            "SPARC inclination geometry and quoted source uncertainties",
        ],
        "selection_uses_vobs_or_residual": False,
        "endpoint_access": False,
        "physical_a_row_constructed": False,
        "claim_boundary": "candidate acquisition and source-only ranking; no common-coordinate transport, channel observable, residual test, or Tau Core validation",
    }
    (DATA / "ghasp_sparc_source_only_candidate_federation_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    top_rows = "\n".join(
        f"| {row['source_only_rank']} | {row['galaxy']} | {row['n_halpha_points']} | "
        f"{row['n_approaching']} / {row['n_receding']} | {row['halpha_max_radius_over_d25']:.2f} | "
        f"{row['whisp_overview_available']} | {row['sparc_inclination_deg']:.0f} | {row['source_only_score']} |"
        for row in eligible[:10]
    )
    (REPORTS / "ghasp_sparc_source_only_candidate_federation_v01.md").write_text(
        f"""# GHASP-SPARC Source-Only Candidate Federation v0.1

**Status:** `{result['status']}`

GHASP VI and VII jointly expose {len(points)} side-labelled Halpha rotation
points in {release_curve_count} release-specific curves for {len(grouped)}
distinct galaxies. UGC3382 and UGC11300 occur in both releases and both
provenance rows are retained. Alias-aware matching through the
203-object GHASP identity table yields {len(candidate_rows)} SPARC overlaps;
{result['both_side_overlap_galaxies']} have both Halpha sides and
{result['whisp_overview_overlap_galaxies']} have an exact public WHISP overview
entry. The earlier exact-primary-name match found only one overlap because it
missed UGC/NGC aliases.

## Blind source ranking

| rank | galaxy | Halpha points | approaching / receding | max R / D25 | WHISP page | inclination | score |
| ---: | --- | ---: | ---: | ---: | --- | ---: | ---: |
{top_rows}

The ranking uses only source availability, side balance, angular radial
coverage, and quoted geometry/uncertainty fields. It does not use SPARC
`vobs`, rotation residuals, required channel amplitudes, or baseline model
scores. The first acquisition target is **{eligible[0]['galaxy']}**; this is a
data-quality choice, not a physical result.

No row is yet a common-coordinate H I-Halpha observable. Direct source-native
H I products, WCS/center transport, beam matching, uncertainty covariance, and
the channel statistic must be frozen before any endpoint access.
""",
        encoding="utf-8",
    )
    print(result["status"])
    print("top candidates:", ", ".join(result["top_source_only_candidates"]))


if __name__ == "__main__":
    main()
