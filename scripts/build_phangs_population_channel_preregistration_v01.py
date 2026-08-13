#!/usr/bin/env python3
"""Freeze the source-side PHANGS morphology-orthogonal population test."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/phangs_population_channel_preregistration_v01.md"
PHANGS = ROOT / "data/external/phangs/phangs_public_sample.csv"
S4G = DATA / "external_s4g_disk_component_summary.csv"

# Emsellem et al. (2022) / Lang et al. (2020) source geometry, frozen before
# opening NGC4321 or IC5332 tracer contrasts.
GEOMETRY = {
    "IC5332": (74.4, 26.9), "NGC0628": (20.7, 8.9), "NGC1087": (359.1, 42.9),
    "NGC1300": (278.0, 31.8), "NGC1365": (201.1, 55.4), "NGC1385": (181.3, 44.0),
    "NGC1433": (199.7, 28.6), "NGC1512": (261.9, 42.5), "NGC1566": (214.7, 29.5),
    "NGC1672": (134.3, 42.6), "NGC2835": (1.0, 41.3), "NGC3351": (193.2, 45.1),
    "NGC3627": (173.1, 57.3), "NGC4254": (68.1, 34.4), "NGC4303": (312.4, 23.5),
    "NGC4321": (156.2, 38.5), "NGC4535": (179.7, 44.7), "NGC5068": (342.4, 35.7),
    "NGC7496": (193.7, 35.9),
}


def normalized(value: object) -> str:
    text = re.sub(r"[^A-Z0-9]", "", str(value).upper())
    match = re.fullmatch(r"(NGC|IC)0*(\d+)", text)
    return text if match is None else match.group(1) + str(int(match.group(2)))


def main() -> None:
    phangs = pd.read_csv(PHANGS, skiprows=[1])
    phangs = phangs[phangs["VLT/MUSE"].astype(str).str.upper().eq("TRUE")].copy()
    components = pd.read_csv(S4G)
    component_lookup = {
        normalized(row.s4g_name): str(row.s4g_model_components)
        for row in components.itertuples()
    }
    opened = {"NGC4254", "NGC3351", "NGC3627", "NGC4535"}
    rows = []
    for row in phangs.itertuples():
        galaxy = str(row.Name)
        key = normalized(galaxy)
        pa, inclination = GEOMETRY[galaxy]
        model_components = component_lookup.get(key)
        geometry_pass = 25.0 <= inclination <= 70.0
        morphology_known = model_components is not None
        barred = morphology_known and "BAR" in model_components.split(";")
        eligible = geometry_pass and morphology_known and not barred
        if not geometry_pass:
            reason = "inclination_outside_frozen_25_to_70_deg_window"
        elif not morphology_known:
            reason = "source_side_s4g_decomposition_missing"
        elif barred:
            reason = "m2_is_body_nuisance_and_no_source_certified_m1_null_is_available"
        else:
            reason = "eligible_nonbarred_body_remove_m0_plus_m1_retain_m2"
        rows.append({
            "galaxy": galaxy,
            "position_angle_deg": pa,
            "inclination_deg": inclination,
            "s4g_model_components": model_components,
            "barred": bool(barred),
            "geometry_pass": bool(geometry_pass),
            "morphology_source_pass": bool(morphology_known),
            "population_test_eligible": bool(eligible),
            "nuisance_modes": "m0+m1" if eligible else None,
            "retained_test_mode": "m2" if eligible else None,
            "endpoint_role": "legacy_open_pilot" if galaxy in opened else ("confirmatory_unopened" if eligible else "excluded"),
            "decision_reason": reason,
            "selection_uses_tracer_contrast": False,
            "selection_uses_rotation_residual": False,
        })
    frame = pd.DataFrame(rows).sort_values("galaxy")
    eligible = frame[frame.population_test_eligible]
    confirmatory = eligible[eligible.endpoint_role.eq("confirmatory_unopened")]
    result = {
        "schema": "phangs_population_channel_preregistration_v01",
        "status": "SOURCE_FROZEN_POPULATION_TEST_PREREGISTERED_ENDPOINTS_CLOSED",
        "population_size": int(len(frame)),
        "eligible_galaxies": eligible.galaxy.tolist(),
        "legacy_open_pilots": eligible.loc[eligible.endpoint_role.eq("legacy_open_pilot"), "galaxy"].tolist(),
        "confirmatory_unopened_galaxies": confirmatory.galaxy.tolist(),
        "source_rule": "25<=inclination<=70 deg; S4G decomposition present; BAR absent; remove m0+m1 and test m2",
        "basis": "five radial zones times {m2_cos,m2_sin} from the unchanged PHANGS tracer-field operator",
        "primary_null": "all retained confirmatory m2 coefficients are zero under block sector-jackknife covariance",
        "promotion_rule": "global confirmatory p<0.01 and each confirmatory galaxy m2 p<0.05; only then permit a separately frozen body-increment score",
        "wrong_family_control": "m1 block evaluated without changing the m2 decision",
        "geometry_source": "Emsellem et al. 2022 table using Lang et al. 2020 CO geometry",
        "geometry_source_url": "https://academic.oup.com/view-large/555742476",
        "morphology_source": "S4G multicomponent decomposition summary frozen in the repository",
        "construction_uses_tracer_contrast": False,
        "construction_uses_rotation_residual": False,
        "endpoint_opened": False,
        "claim_boundary": "source-side population preregistration only; no channel, time, quantum, path, Tau, or dark-sector signal",
    }
    frame.to_csv(DATA / "phangs_population_channel_preregistration_v01.csv", index=False)
    (DATA / "phangs_population_channel_preregistration_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    REPORT.write_text(
        "# PHANGS population channel preregistration v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The source-only rule retains `{', '.join(result['eligible_galaxies'])}`. "
        f"`{', '.join(result['legacy_open_pilots'])}` is a legacy pilot; the unopened "
        f"confirmatory cohort is `{', '.join(result['confirmatory_unopened_galaxies'])}`.\n\n"
        "For every eligible nonbarred body, `m0+m1` is nuisance and `m2` is the sole "
        "test family. Promotion requires global confirmatory `p<0.01` and individual "
        "`m2 p<0.05` in both confirmatory galaxies. Failure preserves the null and "
        "does not authorize another post-result galaxy choice.\n",
        encoding="utf-8",
    )
    print(result["status"], result["confirmatory_unopened_galaxies"])


if __name__ == "__main__":
    main()
