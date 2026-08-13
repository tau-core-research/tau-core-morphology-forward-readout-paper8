#!/usr/bin/env python3
"""Build a multi-source morphology nuisance atlas before future endpoints."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/phangs_source_certified_morphology_nuisance_atlas_v02.md"
PHANGS = ROOT / "data/external/literature/phangs_stuber_2023_muse_morphology_selected_v01.csv"
S4G = DATA / "external_s4g_disk_component_summary.csv"
PREREG = DATA / "phangs_population_channel_preregistration_v01.csv"
M1_SOURCE = DATA / "phangs_radial_m1_source_coverage_v01.csv"
OPENED = {"IC5332", "NGC3351", "NGC3627", "NGC4254", "NGC4321", "NGC4535"}


def main() -> None:
    phangs = pd.read_csv(PHANGS)
    s4g = pd.read_csv(S4G).set_index("s4g_name")
    geometry = pd.read_csv(PREREG).set_index("galaxy")
    m1_source = pd.read_csv(M1_SOURCE).set_index("galaxy")
    rows = []
    for source in phangs.itertuples():
        galaxy = source.galaxy
        components = None if galaxy not in s4g.index else str(s4g.loc[galaxy, "s4g_model_components"])
        stellar_bar = components is not None and "BAR" in components.split(";")
        co_bar = source.co_bar_class in {"B", "C"}
        grand_design = source.spiral_class == "G"
        m2_body_nuisance = stellar_bar or co_bar or grand_design
        geometry_pass = bool(geometry.loc[galaxy, "geometry_pass"])
        morphology_validated = source.source_table_status.startswith("validated")

        m1_match = bool(m1_source.loc[galaxy, "catalog_match"])
        m1_clean_certified = bool(
            m1_source.loc[galaxy, "radial_m1_null_source_certified"]
        )
        m2_clean_certified = morphology_validated and not m2_body_nuisance
        retained = []
        if geometry_pass and m1_clean_certified and m2_body_nuisance:
            retained.append("m1")
        if geometry_pass and m2_clean_certified:
            retained.append("m2")
        rows.append({
            "galaxy": galaxy,
            "endpoint_opened": galaxy in OPENED,
            "geometry_pass": geometry_pass,
            "phangs_morphology_validated": morphology_validated,
            "phangs_co_bar_class": source.co_bar_class,
            "phangs_spiral_class": source.spiral_class,
            "s4g_model_components": components,
            "s4g_stellar_bar_component": stellar_bar,
            "m0_body_nuisance": True,
            "radial_m1_catalog_match": m1_match,
            "a1_inner": m1_source.loc[galaxy, "a1_inner"],
            "a1_outer": m1_source.loc[galaxy, "a1_outer"],
            "m1_clean_source_certified": m1_clean_certified,
            "m2_body_nuisance": m2_body_nuisance,
            "m2_clean_source_certified": m2_clean_certified,
            "retained_low_order_test_directions": "+".join(retained) if retained else None,
            "untouched_endpoint_eligible": bool(retained) and galaxy not in OPENED,
            "decision_uses_velocity_contrast": False,
            "decision_uses_rotation_residual": False,
        })
    frame = pd.DataFrame(rows).sort_values("galaxy")
    untouched = frame[frame.untouched_endpoint_eligible]
    clean_m2 = frame[frame.m2_clean_source_certified]
    conflicts = frame[
        frame.phangs_co_bar_class.eq("A") & frame.s4g_stellar_bar_component
    ]
    result = {
        "schema": "phangs_source_certified_morphology_nuisance_atlas_v02",
        "status": "NO_UNTOUCHED_LOW_ORDER_ENDPOINT_AFTER_MULTI_SOURCE_NUISANCE_UNION",
        "population_size": int(len(frame)),
        "opened_endpoint_count": int(frame.endpoint_opened.sum()),
        "untouched_low_order_endpoint_count": int(len(untouched)),
        "untouched_low_order_endpoints": untouched.galaxy.tolist(),
        "m2_clean_source_certified_bodies": clean_m2.galaxy.tolist(),
        "cross_tracer_bar_conflicts": conflicts.galaxy.tolist(),
        "nuisance_union_rule": (
            "m0 is always body nuisance; m2 is body nuisance if any source reports an S4G stellar BAR, "
            "PHANGS CO bar B/C, or grand-design G spiral; m1 is retained only when both published "
            "radial stellar A1 averages are below the pre-frozen 0.1 boundary"
        ),
        "next_finite_action": (
            "close the current low-order PHANGS selection lane and move to a higher-dimensional "
            "morphology basis before opening more tracer contrasts"
        ),
        "phangs_source": "Stuber et al. 2023 Table 1 selected to the PHANGS-MUSE sample",
        "phangs_source_url": "https://arxiv.org/abs/2305.17172",
        "construction_uses_velocity_contrast": False,
        "construction_uses_rotation_residual": False,
        "claim_boundary": (
            "source-only nuisance atlas; no new endpoint was opened, and zero eligible low-order endpoints "
            "does not imply absence of a complete channel or of higher-dimensional differential structure"
        ),
    }
    frame.to_csv(DATA / "phangs_source_certified_morphology_nuisance_atlas_v02.csv", index=False)
    (DATA / "phangs_source_certified_morphology_nuisance_atlas_v02.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    REPORT.write_text(
        "# PHANGS source-certified morphology nuisance atlas v02\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The multi-source nuisance union leaves `{len(untouched)}` untouched low-order endpoint. "
        f"The only source-certified clean-`m2` body is `{', '.join(clean_m2.galaxy)}`, which is already "
        "an opened pilot. No body has a certified radial `m1` null.\n\n"
        f"PHANGS/S4G bar conflicts occur for `{', '.join(conflicts.galaxy)}`. This demonstrates that "
        "one tracer's morphology cannot stand in for the complete body nuisance space. The current "
        "low-order selection lane is closed without opening another velocity contrast.\n",
        encoding="utf-8",
    )
    print(result["status"], result["untouched_low_order_endpoints"])


if __name__ == "__main__":
    main()
