#!/usr/bin/env python3
"""Record source-native COMING bar fields without opening rotation endpoints."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "coming_bar_source_fields_v01.md"
SOURCE_URL = "https://doi.org/10.1093/pasj/psz004"


# Values transcribed from Salak et al. (2019), Table 2. The paper adopts a
# conservative 10 percent uncertainty for the deprojected bar semimajor axis.
ROWS = [
    ("NGC 613", "SB(rs)b", 10.3, 1.0, 0.75, 0.11, "SB", "profile_in_figure_not_numeric_table"),
    ("NGC 4303", "SAB(rs)bc", 2.97, 0.30, 1.22, 0.20, "SAB", "profile_in_figure_not_numeric_table"),
    ("NGC 4579", "SB(rs)a", 3.62, 0.36, 1.37, 0.19, "SB", "central_outlier_Delta_2p9_profile_not_frozen"),
    ("NGC 5248", "SAB(s)bc", 1.78, 0.18, 1.61, 0.27, "SAB", "bar_length_literature_ambiguity"),
    ("NGC 7479", "SB(rs)b", 10.2, 1.0, 1.09, None, "SB", "bar_region_residual_about_20_km_s_qualitative"),
]


def main() -> None:
    records = []
    for galaxy, morphology, bar_kpc, bar_err, ratio, ratio_err, strength, caveat in ROWS:
        records.append(
            {
                "galaxy": galaxy,
                "family": "K_bar_dominated_non_circular",
                "morphology": morphology,
                "bar_class": strength,
                "deprojected_bar_radius_kpc": bar_kpc,
                "deprojected_bar_radius_error_kpc": bar_err,
                "reversal_over_bar_radius": ratio,
                "reversal_over_bar_radius_error": ratio_err,
                "active_zone_inner_kpc": 0.0,
                "active_zone_outer_kpc": bar_kpc,
                "active_zone_rule": "0 <= R <= source_deprojected_bar_radius",
                "harmonic_non_circular_profile_status": caveat,
                "source_url": SOURCE_URL,
                "uses_vobs_or_dark_discrepancy_residual": False,
                "classification_source_supported": True,
                "source_fields_complete": False,
                "endpoint_eligible": False,
            }
        )
    frame = pd.DataFrame(records)
    frame.to_csv(DATA / "coming_bar_source_fields_v01.csv", index=False)
    payload = {
        "schema": "tau_core_coming_bar_source_fields_v01",
        "status": "BAR_CLASS_AND_ACTIVE_ZONE_FROZEN_HARMONIC_PROFILE_OPEN",
        "n_galaxies": len(frame),
        "n_classification_source_supported": int(frame.classification_source_supported.sum()),
        "n_active_zones_frozen": int(frame.active_zone_outer_kpc.notna().sum()),
        "n_source_fields_complete": int(frame.source_fields_complete.sum()),
        "construction_uses_vobs_or_dark_discrepancy_residual": False,
        "endpoint_scoring_allowed": False,
        "remaining_blocker": "acquire or residual-blindly digitize the published radial non-circular harmonic profiles with uncertainty and provenance",
        "claim_boundary": "bar morphology and source-active zones only; no Tau kernel success or channel effect is measured",
    }
    (DATA / "coming_bar_source_fields_v01.json").write_text(json.dumps(payload, indent=2) + "\n")
    lines = [
        "# COMING bar source fields v01",
        "",
        f"Status: `{payload['status']}`",
        "",
        "Salak et al. provide independent infrared bar classifications, deprojected bar semimajor axes, and radial-velocity reversal coordinates. These freeze the family label and the first active-zone rule without access to a dark-discrepancy endpoint.",
        "",
        "| Galaxy | Class | Bar radius (kpc) | Rr/abar | Frozen active zone | Caveat |",
        "| --- | --- | ---: | ---: | --- | --- |",
    ]
    for row in frame.itertuples(index=False):
        lines.append(
            f"| {row.galaxy} | {row.bar_class} | {row.deprojected_bar_radius_kpc:.2f} | {row.reversal_over_bar_radius:.2f} | 0-Rbar | {row.harmonic_non_circular_profile_status} |"
        )
    lines.extend(
        [
            "",
            "The five classifications and radial windows are frozen. The preregistered harmonic-profile field is not yet complete: most per-galaxy profiles are graphical, NGC 4579 has a documented central outlier, and NGC 5248 has a bar-length ambiguity. Endpoint scoring therefore remains closed.",
            "",
        ]
    )
    REPORT.write_text("\n".join(lines))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
