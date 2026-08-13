#!/usr/bin/env python3
"""Freeze velocity-independent S4G photometric geometry for NGC4254."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

S4G_GLOBAL_PATH = DATA / "external_s4g_galaxies.csv"
S4G_COMPONENT_PATH = DATA / "external_s4g_table7.csv"
LEGACY_WINDOW_PATH = DATA / "ngc4254_common_mode_geometry_freeze_v01.json"
JSON_PATH = DATA / "ngc4254_s4g_photometric_geometry_freeze_v02.json"
REPORT_PATH = REPORTS / "ngc4254_s4g_photometric_geometry_freeze_v02.md"

STATUS = "SOURCE_ONLY_S4G_PHOTOMETRIC_GEOMETRY_FROZEN"
S4G_CATALOG_URL = "https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/ApJS/219/4/galaxies"
S4G_PUBLISHED_TABLE_URL = "https://www.oulu.fi/astronomy/S4G_PIPELINE4/s4g_p4_table1.pdf"
S4G_PA_ERROR_DEG = 5.9
S4G_ELLIPTICITY_ERROR = 0.015
CLAIM_BOUNDARY = (
    "velocity-independent photometric geometry freeze; not a parent role identity, "
    "channel/time signal, dynamical inclination proof, or endpoint score"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def thin_disk_inclination(axis_ratio: float) -> float:
    if not 0.0 < axis_ratio <= 1.0:
        raise ValueError(f"Invalid projected axis ratio: {axis_ratio}")
    return math.degrees(math.acos(axis_ratio))


def finite_thickness_inclination(axis_ratio: float, q0: float) -> float:
    if not 0.0 <= q0 < axis_ratio <= 1.0:
        raise ValueError("Finite-thickness inclination requires 0 <= q0 < q <= 1")
    cos2 = (axis_ratio**2 - q0**2) / (1.0 - q0**2)
    return math.degrees(math.acos(math.sqrt(cos2)))


def main() -> None:
    global_catalog = pd.read_csv(S4G_GLOBAL_PATH)
    selected = global_catalog.loc[global_catalog["Name"].eq("NGC4254")]
    if len(selected) != 1:
        raise ValueError(f"Expected one NGC4254 S4G global row, found {len(selected)}")
    row = selected.iloc[0]
    if str(row["Flag"]).lower() != "ok":
        raise ValueError("The selected S4G global geometry is not flagged ok")

    components = pd.read_csv(S4G_COMPONENT_PATH)
    disk_rows = components.loc[
        components["Name"].eq("NGC4254")
        & components["C"].eq("D")
        & components["Fn"].eq("expdisk")
    ].copy()
    if len(disk_rows) != 2:
        raise ValueError(f"Expected two NGC4254 S4G disk components, found {len(disk_rows)}")

    legacy = json.loads(LEGACY_WINDOW_PATH.read_text(encoding="utf-8"))
    if legacy.get("velocity_pixels_read_during_freeze") is not False:
        raise ValueError("Inherited radial windows do not certify endpoint-unread freezing")

    ellipticity = float(row["Ell"])
    axis_ratio = 1.0 - ellipticity
    primary_inclination = thin_disk_inclination(axis_ratio)
    thickness_q0 = 0.2
    thickness_inclination = finite_thickness_inclination(axis_ratio, thickness_q0)
    low_ellipticity = ellipticity - S4G_ELLIPTICITY_ERROR
    high_ellipticity = ellipticity + S4G_ELLIPTICITY_ERROR

    component_controls = []
    for index, component in disk_rows.reset_index(drop=True).iterrows():
        component_controls.append(
            {
                "name": f"s4g_disk_component_{index + 1}",
                "position_angle_deg_east_of_north": float(component["PA3"]),
                "axis_ratio": float(component["q3"]),
                "thin_disk_inclination_deg": thin_disk_inclination(float(component["q3"])),
                "scale_length_arcsec": float(component["hr3"]),
                "flux_fraction": float(component["f3"]),
            }
        )

    manifest = {
        "schema": "ngc4254_s4g_photometric_geometry_freeze_v02",
        "status": STATUS,
        "galaxy": "NGC4254",
        "center_icrs_deg": [float(row["_RA"]), float(row["_DE"])],
        "position_angle_deg_east_of_north": float(row["PA"]),
        "ellipticity": ellipticity,
        "axis_ratio": axis_ratio,
        "inclination_deg": primary_inclination,
        "inclination_rule": "thin circular disk: i=acos(1-Ell)",
        "s4g_global_fit": {
            "flag": str(row["Flag"]),
            "source_radial_range_arcsec": [float(row["Rmin"]), float(row["Rmax"])],
            "position_angle_error_deg": S4G_PA_ERROR_DEG,
            "ellipticity_error": S4G_ELLIPTICITY_ERROR,
            "global_sersic_axis_ratio": float(row["q"]),
            "global_sersic_position_angle_deg": float(row["PA1"]),
            "catalog_url": S4G_CATALOG_URL,
            "published_table_url": S4G_PUBLISHED_TABLE_URL,
        },
        "photometric_geometry_controls": [
            {
                "name": "s4g_global_pa_minus_1sigma",
                "position_angle_deg_east_of_north": float(row["PA"])
                - S4G_PA_ERROR_DEG,
                "axis_ratio": axis_ratio,
                "inclination_deg": primary_inclination,
            },
            {
                "name": "s4g_global_pa_plus_1sigma",
                "position_angle_deg_east_of_north": float(row["PA"])
                + S4G_PA_ERROR_DEG,
                "axis_ratio": axis_ratio,
                "inclination_deg": primary_inclination,
            },
            {
                "name": "s4g_global_ellipticity_minus_1sigma",
                "position_angle_deg_east_of_north": float(row["PA"]),
                "ellipticity": low_ellipticity,
                "axis_ratio": 1.0 - low_ellipticity,
                "inclination_deg": thin_disk_inclination(1.0 - low_ellipticity),
            },
            {
                "name": "s4g_global_ellipticity_plus_1sigma",
                "position_angle_deg_east_of_north": float(row["PA"]),
                "ellipticity": high_ellipticity,
                "axis_ratio": 1.0 - high_ellipticity,
                "inclination_deg": thin_disk_inclination(1.0 - high_ellipticity),
            },
            {
                "name": "s4g_global_finite_thickness_q0_0p2",
                "position_angle_deg_east_of_north": float(row["PA"]),
                "axis_ratio": axis_ratio,
                "intrinsic_thickness_q0": thickness_q0,
                "inclination_deg": thickness_inclination,
            },
            *component_controls,
        ],
        "radial_edges_arcsec": legacy["radial_edges_arcsec"],
        "radial_window_provenance": (
            "inherited unchanged from the endpoint-unread v01 protocol; geometry values are not inherited"
        ),
        "velocity_pixels_read_during_freeze": False,
        "velocity_or_residual_inputs": [],
        "freeze_complete": True,
        "geometry_endpoint_independent": True,
        "full_endpoint_ready": False,
        "inputs": {
            "s4g_global_catalog": str(S4G_GLOBAL_PATH.relative_to(ROOT)),
            "s4g_global_catalog_sha256": sha256(S4G_GLOBAL_PATH),
            "s4g_component_catalog": str(S4G_COMPONENT_PATH.relative_to(ROOT)),
            "s4g_component_catalog_sha256": sha256(S4G_COMPONENT_PATH),
            "legacy_radial_window_manifest": str(LEGACY_WINDOW_PATH.relative_to(ROOT)),
            "legacy_radial_window_manifest_sha256": sha256(LEGACY_WINDOW_PATH),
        },
        "legacy_kinematic_comparison_not_selected": {
            "center_icrs_deg": legacy["center_icrs_deg"],
            "position_angle_deg_east_of_north": legacy["position_angle_deg_east_of_north"],
            "inclination_deg": legacy["inclination_deg"],
            "delta_position_angle_deg": float(row["PA"])
            - float(legacy["position_angle_deg_east_of_north"]),
            "delta_inclination_deg": primary_inclination
            - float(legacy["inclination_deg"]),
        },
        "known_limitations": [
            "photometric inclination assumes an intrinsically circular disk",
            "NGC4254 is morphologically asymmetric and its two S4G disk components have different PAs",
            "the q0=0.2 thickness correction and both disk components are mandatory sensitivity controls",
            "radial windows are inherited from an endpoint-unread protocol rather than newly selected from S4G",
            "beam covariance and physical FFL source/gain construction remain separate",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }

    report = f"""# NGC4254 S4G Photometric Geometry Freeze v02

**Status:** `{STATUS}`

**Claim boundary:** {CLAIM_BOUNDARY}.

## Primary Geometry

The primary geometry is selected directly from the unique `Flag=ok` NGC4254
row in the local S4G global catalog:

| quantity | frozen value |
|---|---:|
| center RA | {manifest['center_icrs_deg'][0]:.8f} deg |
| center Dec | {manifest['center_icrs_deg'][1]:.8f} deg |
| photometric PA | {manifest['position_angle_deg_east_of_north']:.3f} deg east of north |
| photometric PA uncertainty | {S4G_PA_ERROR_DEG:.3f} deg |
| ellipticity | {ellipticity:.6f} |
| ellipticity uncertainty | {S4G_ELLIPTICITY_ERROR:.6f} |
| axis ratio | {axis_ratio:.6f} |
| thin-disk inclination | {primary_inclination:.6f} deg |
| outer-isophote range | {float(row['Rmin']):.0f}--{float(row['Rmax']):.0f} arcsec |

The inclination follows `i=acos(1-Ell)`. No velocity map, rotation curve,
fitted residual, or dark-discrepancy label is read.

The field meanings and units are those of the official S4G Pipeline 4
`galaxies` table. The published Table 1 gives the NGC4254 uncertainties used
below.

## Mandatory Controls

The catalog `PA +/- 5.9 deg` and `Ell +/- 0.015` controls are retained in
addition to the primary. The finite-thickness control with `q0=0.2` gives
`i={thickness_inclination:.6f} deg`. The two S4G exponential-disk components
have `(PA,q,i)=({component_controls[0]['position_angle_deg_east_of_north']:.2f},
{component_controls[0]['axis_ratio']:.3f},
{component_controls[0]['thin_disk_inclination_deg']:.3f})` and
`({component_controls[1]['position_angle_deg_east_of_north']:.2f},
{component_controls[1]['axis_ratio']:.3f},
{component_controls[1]['thin_disk_inclination_deg']:.3f})`. They are retained
as source-side controls because NGC4254 is asymmetric; neither may be selected
or discarded using a terminal score.

## Comparison With The Retired Primary Geometry

The earlier kinematic geometry used `PA={legacy['position_angle_deg_east_of_north']:.3f}`
deg and `i={legacy['inclination_deg']:.3f} deg`. The new source-only primary
therefore changes PA by
`{manifest['legacy_kinematic_comparison_not_selected']['delta_position_angle_deg']:+.3f}`
deg and inclination by
`{manifest['legacy_kinematic_comparison_not_selected']['delta_inclination_deg']:+.3f}`
deg. The old values remain a provenance comparison only.

The six radial windows are inherited unchanged from the earlier protocol,
whose freeze certifies that no velocity pixel was read. This removes
kinematic dependence from center/PA/inclination, but full endpoint readiness
still requires the mandatory photometric controls, beam covariance, and the
physical FFL source/gain construction.
"""

    JSON_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(STATUS)
    print(
        f"PA={manifest['position_angle_deg_east_of_north']:.3f} "
        f"inclination={manifest['inclination_deg']:.6f}"
    )


if __name__ == "__main__":
    main()
