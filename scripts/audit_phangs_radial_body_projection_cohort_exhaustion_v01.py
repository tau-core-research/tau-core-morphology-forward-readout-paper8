#!/usr/bin/env python3
"""Audit whether any untouched same-family PHANGS endpoint remains."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
ATLAS = DATA / "phangs_source_certified_morphology_nuisance_atlas_v02.csv"
PREREGISTRATION = DATA / "phangs_radial_body_projection_preregistration_v01.json"
DEVELOPMENT = DATA / "phangs_radial_body_projection_development_terminal_acquisition_v01.json"
CONFIRMATORY = DATA / "phangs_radial_body_projection_confirmatory_endpoint_v01.json"
OUTPUT = DATA / "phangs_radial_body_projection_cohort_exhaustion_v01.json"
REPORT = ROOT / "reports/phangs_radial_body_projection_cohort_exhaustion_v01.md"


def main() -> None:
    atlas = pd.read_csv(ATLAS)
    preregistration = json.loads(PREREGISTRATION.read_text(encoding="utf-8"))
    development = json.loads(DEVELOPMENT.read_text(encoding="utf-8"))
    confirmatory = json.loads(CONFIRMATORY.read_text(encoding="utf-8"))
    development_opened = set(development["development_galaxies"])
    confirmatory_opened = set(confirmatory["galaxies_opened_once"])
    rows = []
    for row in atlas.itertuples(index=False):
        if bool(row.endpoint_opened):
            disposition = "PRIOR_ENDPOINT_ALREADY_OPENED"
        elif row.galaxy in development_opened:
            disposition = "CURRENT_METHOD_DEVELOPMENT_VALUES_OPENED"
        elif row.galaxy in confirmatory_opened:
            disposition = "CURRENT_CONFIRMATORY_VALUES_OPENED"
        elif row.galaxy == "NGC1365":
            disposition = "SOURCE_BLOCKED_NO_MATCHING_BROAD_CO_MOMENT0"
        elif not bool(row.geometry_pass):
            disposition = "GEOMETRY_GATE_FAILED"
        elif not bool(row.phangs_morphology_validated) or pd.isna(row.s4g_model_components):
            disposition = "SOURCE_BODY_DESCRIPTION_INCOMPLETE"
        else:
            disposition = "UNTOUCHED_SAME_FAMILY_CANDIDATE"
        rows.append({"galaxy": row.galaxy, "disposition": disposition})

    counts = pd.DataFrame(rows).disposition.value_counts().sort_index().to_dict()
    untouched = [row["galaxy"] for row in rows if row["disposition"] == "UNTOUCHED_SAME_FAMILY_CANDIDATE"]
    checks = {
        "atlas_has_19_galaxies": len(rows) == 19,
        "development_set_matches_preregistration": development_opened
        == set(preregistration["pipeline_development_no_claim"]) - {"NGC1365"},
        "confirmatory_set_matches_preregistration": confirmatory_opened
        == set(preregistration["confirmatory_untouched"]),
        "no_untouched_same_family_candidate": untouched == [],
        "all_galaxies_have_one_disposition": sum(counts.values()) == 19,
    }
    result = {
        "schema": "phangs_radial_body_projection_cohort_exhaustion_v01",
        "status": "PHANGS_MUSE_SAME_FAMILY_CONFIRMATORY_COHORT_EXHAUSTED",
        "galaxies": rows,
        "disposition_counts": counts,
        "untouched_same_family_candidates": untouched,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "same_sample_relabel_or_replacement_allowed": False,
        "finite_decision": (
            "close same-sample confirmatory search; future empirical validation requires an external "
            "survey or genuinely new public galaxies with the complete source and terminal product family"
        ),
        "theory_frontier": (
            "return to the source-derived body coefficient and low-dimensional complement law; do not "
            "use the exhausted sample to choose that law"
        ),
        "claim_boundary": (
            "cohort provenance and endpoint-availability audit; not evidence for or against morphology, "
            "channel, time, quantum, Tau, or dark-sector physics"
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# PHANGS radial body-projection cohort exhaustion v01", "",
        f"Status: `{result['status']}`", "",
        "No untouched same-family galaxy remains in the 19-object PHANGS-MUSE atlas.", "",
    ]
    for label, count in counts.items():
        lines.append(f"- `{label}`: `{count}`")
    lines.extend([
        "", "This closes same-sample endpoint replacement. A future empirical test requires an "
        "external or genuinely new cohort. The exhausted sample may not select a new covariance, "
        "body coefficient law, or complement law for confirmatory claims.",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(result["status"], counts)
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
