#!/usr/bin/env python3
"""Build and alias-audit the first untouched refined-body source cohort."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
from astroquery.simbad import Simbad


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "refined_body_source_cohort_v01.md"
CATALOGS = ("DDO", "UGC", "NGC", "IC", "F", "HARO")


ROWS = [
    # Candidate membership is source-side only. Hole/dispersion fields still require extraction.
    ("DDO 43", "K_scale_tail_turbulent_holey", "LITTLE THINGS", "https://doi.org/10.1088/0004-6256/149/6/180"),
    ("DDO 46", "K_scale_tail_turbulent_holey", "LITTLE THINGS", "https://doi.org/10.1088/0004-6256/149/6/180"),
    ("DDO 47", "K_scale_tail_turbulent_holey", "LITTLE THINGS", "https://doi.org/10.1088/0004-6256/149/6/180"),
    ("DDO 52", "K_scale_tail_turbulent_holey", "LITTLE THINGS", "https://doi.org/10.1088/0004-6256/149/6/180"),
    ("DDO 53", "K_scale_tail_turbulent_holey", "LITTLE THINGS", "https://doi.org/10.1088/0004-6256/149/6/180"),
    ("NGC 4449", "K_disturbed_tidal_history", "resolved HI stream system", "https://doi.org/10.1088/0004-637X/706/1/516"),
    ("NGC 4656", "K_disturbed_tidal_history", "HI tidal interaction system", "https://doi.org/10.1086/307001"),
    ("NGC 4631", "K_disturbed_tidal_history", "HI tidal interaction system", "https://doi.org/10.1086/307001"),
    ("NGC 1512", "K_disturbed_tidal_history", "HI companion interaction system", "https://doi.org/10.1086/308819"),
    ("NGC 4490", "K_disturbed_tidal_history", "HI tidal interaction system", "https://doi.org/10.1088/0004-637X/706/1/516"),
    ("UGC 2459", "K_warped_asymmetric_disturbed_disk", "edge-on HI warp survey", "https://doi.org/10.1051/0004-6361:20020976"),
    ("UGC 2082", "K_warped_asymmetric_disturbed_disk", "edge-on HI warp survey", "https://doi.org/10.1051/0004-6361:20020976"),
    ("UGC 7321", "K_warped_asymmetric_disturbed_disk", "edge-on HI warp survey", "https://doi.org/10.1051/0004-6361:20020976"),
    ("NGC 4565", "K_warped_asymmetric_disturbed_disk", "edge-on HI warp survey", "https://doi.org/10.1051/0004-6361:20020976"),
    ("UGC 3137", "K_warped_asymmetric_disturbed_disk", "edge-on HI warp survey", "https://doi.org/10.1051/0004-6361:20020976"),
    ("NGC 613", "K_bar_dominated_non_circular", "COMING Fourier velocity field", "https://doi.org/10.1093/pasj/psz004"),
    ("NGC 4303", "K_bar_dominated_non_circular", "COMING Fourier velocity field", "https://doi.org/10.1093/pasj/psz004"),
    ("NGC 4579", "K_bar_dominated_non_circular", "COMING Fourier velocity field", "https://doi.org/10.1093/pasj/psz004"),
    ("NGC 5248", "K_bar_dominated_non_circular", "COMING Fourier velocity field", "https://doi.org/10.1093/pasj/psz004"),
    ("NGC 7479", "K_bar_dominated_non_circular", "COMING Fourier velocity field", "https://doi.org/10.1093/pasj/psz004"),
]


def keys(value: str) -> set[str]:
    text = str(value).upper().replace("_", " ").replace("-", " ")
    out: set[str] = set()
    for cat in CATALOGS:
        for num in re.findall(rf"\b{cat}\s*0*(\d+)\b", text):
            out.add(f"{cat}{int(num)}")
    return out


def main() -> None:
    historical = pd.read_csv(DATA / "external_sparc_master_table.csv")
    historical_keys = set().union(*(keys(x) for x in historical.Galaxy))
    results = []
    for galaxy, family, source, url in ROWS:
        ids: list[str] = []
        status = "OK"
        try:
            table = Simbad.query_objectids(galaxy)
            ids = [] if table is None else [str(x) for x in table["id"]]
        except Exception as exc:
            status = f"QUERY_FAILED:{type(exc).__name__}"
        alias_keys = set().union(keys(galaxy), *(keys(x) for x in ids))
        overlaps = sorted(alias_keys & historical_keys)
        results.append(
            {
                "galaxy": galaxy,
                "family": family,
                "source_program": source,
                "source_url": url,
                "simbad_status": status,
                "alias_keys": ";".join(sorted(alias_keys)),
                "historical_overlap_keys": ";".join(overlaps),
                "alias_independent": not overlaps and status == "OK",
                "source_fields_complete": False,
                "rotation_endpoint_acquired": False,
                "endpoint_eligible": False,
            }
        )

    frame = pd.DataFrame(results)
    frame.to_csv(DATA / "refined_body_source_cohort_v01.csv", index=False)
    counts = frame.groupby("family").agg(
        nominated=("galaxy", "size"),
        alias_independent=("alias_independent", "sum"),
    )
    payload = {
        "schema": "tau_core_refined_body_source_cohort_v01",
        "status": "SOURCE_COHORT_NOMINATED_FIELD_EXTRACTION_OPEN",
        "n_nominated": len(frame),
        "n_alias_independent": int(frame.alias_independent.sum()),
        "n_alias_overlaps": int((frame.historical_overlap_keys != "").sum()),
        "n_query_failures": int((frame.simbad_status != "OK").sum()),
        "family_counts": counts.to_dict(orient="index"),
        "source_fields_complete": False,
        "endpoint_scoring_allowed": False,
        "claim_boundary": "source-acquisition cohort only; nomination is not classification, formula freeze, or endpoint evidence",
    }
    (DATA / "refined_body_source_cohort_v01.json").write_text(json.dumps(payload, indent=2) + "\n")

    overlap = frame.loc[frame.historical_overlap_keys != "", ["galaxy", "historical_overlap_keys"]]
    lines = [
        "# Refined body source cohort v01",
        "",
        f"Status: `{payload['status']}`",
        "",
        f"Nominated: `{len(frame)}`; SIMBAD alias-independent from the historical SPARC set: `{payload['n_alias_independent']}`; physical overlaps: `{payload['n_alias_overlaps']}`; query failures: `{payload['n_query_failures']}`.",
        "",
        "This is a source-acquisition cohort. No row is endpoint eligible until the required source-native fields and an independent rotation endpoint are acquired and frozen.",
        "",
        "## Family counts",
        "",
    ]
    for family, row in counts.iterrows():
        lines.append(f"- `{family}`: {int(row.nominated)} nominated, {int(row.alias_independent)} alias-independent.")
    lines.extend(["", "## Alias exclusions", ""])
    if overlap.empty:
        lines.append("No physical overlap was found by the current identifier audit.")
    else:
        for row in overlap.itertuples(index=False):
            lines.append(f"- `{row.galaxy}` overlaps historical key(s) `{row.historical_overlap_keys}` and is excluded.")
    lines.extend(
        [
            "",
            "## Next acquisition gate",
            "",
            "Extract the preregistered source fields for each alias-independent row. Replace excluded or incomplete rows before opening any rotation data. The final manifest must retain at least five complete independent galaxies per family.",
            "",
        ]
    )
    REPORT.write_text("\n".join(lines))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
