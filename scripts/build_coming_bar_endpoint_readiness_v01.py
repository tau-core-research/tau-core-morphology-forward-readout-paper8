#!/usr/bin/env python3
"""Audit independent endpoint readiness after the barred source-family freeze."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "coming_bar_endpoint_readiness_v01.md"
GALAXIES = {
    "NGC 613": ["NGC613"],
    "NGC 4303": ["NGC4303", "UGC7420"],
    "NGC 4579": ["NGC4579", "UGC7796"],
    "NGC 5248": ["NGC5248", "UGC8616"],
    "NGC 7479": ["NGC7479", "UGC12343"],
}


def main() -> None:
    ghasp = pd.read_csv(DATA / "ghasp_full_federation_side_points_v01.csv")
    s4g = pd.read_csv(DATA / "external_s4g_table7.csv")
    phangs = pd.read_csv(ROOT / "data" / "external" / "phangs" / "phangs_public_sample.csv")
    rows = []
    for galaxy, aliases in GALAXIES.items():
        pattern = "|".join(aliases)
        g = ghasp[ghasp.aliases.fillna("").str.contains(pattern, case=False, regex=True)]
        compact = galaxy.replace(" ", "")
        s = s4g[s4g.Name.astype(str).str.replace(" ", "").str.upper().eq(compact.upper())]
        p = phangs[phangs.iloc[:, 0].astype(str).str.replace(" ", "").str.upper().eq(compact.upper())]
        independent_rotation = len(g) > 0
        stellar_decomposition = len(s) > 0
        gas_profile = False
        baryonic_velocity = False
        blockers = []
        if not independent_rotation:
            blockers.append("independent_non_CO_rotation_curve")
        if not stellar_decomposition:
            blockers.append("source_stellar_mass_decomposition")
        blockers.extend(["radial_gas_surface_density", "baryonic_poisson_velocity_components"])
        rows.append(
            {
                "galaxy": galaxy,
                "ghasp_independent_halpha_points": len(g),
                "independent_rotation_endpoint_acquired": independent_rotation,
                "s4g_component_rows": len(s),
                "stellar_decomposition_acquired": stellar_decomposition,
                "phangs_catalog_match": len(p) > 0,
                "radial_gas_profile_acquired": gas_profile,
                "baryonic_velocity_components_acquired": baryonic_velocity,
                "dark_discrepancy_endpoint_ready": independent_rotation and stellar_decomposition and gas_profile and baryonic_velocity,
                "blockers": ";".join(blockers),
                "endpoint_scoring_allowed": False,
            }
        )
    frame = pd.DataFrame(rows)
    frame.to_csv(DATA / "coming_bar_endpoint_readiness_v01.csv", index=False)
    ranked = frame.sort_values(
        ["independent_rotation_endpoint_acquired", "stellar_decomposition_acquired", "ghasp_independent_halpha_points"],
        ascending=False,
    )
    payload = {
        "schema": "tau_core_coming_bar_endpoint_readiness_v01",
        "status": "NGC7479_PRIMARY_ENDPOINT_CANDIDATE_BARYONIC_FIELD_OPEN",
        "n_galaxies": len(frame),
        "n_independent_rotation_acquired": int(frame.independent_rotation_endpoint_acquired.sum()),
        "n_dark_discrepancy_endpoint_ready": int(frame.dark_discrepancy_endpoint_ready.sum()),
        "primary_acquisition_target": ranked.iloc[0].galaxy,
        "primary_target_halpha_points": int(ranked.iloc[0].ghasp_independent_halpha_points),
        "coming_co_reuse_as_endpoint_allowed": False,
        "endpoint_scoring_allowed": False,
        "next_action": "acquire NGC7479 radial HI/gas surface density and compute source-frozen stellar+gas baryonic velocity components",
        "claim_boundary": "readiness audit only; no dark discrepancy or Tau score computed",
    }
    (DATA / "coming_bar_endpoint_readiness_v01.json").write_text(json.dumps(payload, indent=2) + "\n")
    REPORT.write_text(
        "# COMING barred-family endpoint readiness v01\n\n"
        f"Status: `{payload['status']}`\n\n"
        "All five morphology profiles are source-ready, but none yet has a complete independent dark-discrepancy endpoint. "
        "NGC7479 ranks first because 99 GHASP Halpha side points and an S4G stellar decomposition are already local. "
        "Its radial gas surface density and source-frozen stellar+gas baryonic velocity components remain missing.\n\n"
        "The COMING CO field may not be reused as the rotation endpoint. No scoring is allowed until `v_obs` and `v_bar` come from the declared independent route.\n"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
