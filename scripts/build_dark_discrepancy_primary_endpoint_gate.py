#!/usr/bin/env python3
"""Freeze the dark-discrepancy field as the primary Tau Core galaxy endpoint."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/dark_discrepancy_primary_endpoint_gate_v01.md"


def main() -> None:
    galaxies = {}
    for slug in ("ngc3351", "ngc4254"):
        common = DATA / f"{slug}_phangs_common_tracer_velocity_field_v01.fits"
        external = ROOT / f"data/external/literature/{slug}_phangs_tracer_velocity"
        galaxies[slug.upper()] = {
            "common_co_halpha_velocity_field": common.exists(),
            "co_molecular_intensity_field": any(external.glob("*broad_mom0.fits")),
            "stellar_mass_surface_density_field": any(external.glob("*.stellar.fits")),
            "atomic_hi_surface_density_field": any(external.glob("*viva*mom0.fits")),
            "two_dimensional_baryonic_gravity_field_ready": False,
            "dark_discrepancy_field_open_allowed": False,
        }
    morphology = json.loads((DATA / "s4g_dark_discrepancy_morphology_endpoint_v01.json").read_text())
    multitracer = json.loads((DATA / "dark_discrepancy_zone_multitracer_channel_audit_v01.json").read_text())
    result = {
        "schema": "dark_discrepancy_primary_endpoint_gate_v01",
        "status": "DARK_DISCREPANCY_PRIMARY_ENDPOINT_FROZEN_2D_BARYONIC_FIELDS_INCOMPLETE",
        "primary_target": "Delta_DM(R,theta)=v_common(R,theta)^2-v_baryon(R,theta)^2",
        "equivalent_acceleration_target": "Delta_g(R,theta)=g_common(R,theta)-g_baryon(R,theta)",
        "tau_core_attribution_order": [
            "source_morphology component inside Delta_DM",
            "observer-source path/channel component inside remaining Delta_DM",
            "shared or interaction component if source and channel are nonseparable",
        ],
        "tracer_contrast_role": "nuisance calibration for v_common only; never the primary Tau Core endpoint",
        "phangs_2d_readiness": galaxies,
        "existing_one_dimensional_evidence": {
            "global_s4g_morphology_status": morphology["status"],
            "global_s4g_morphology_holdout_mse_reduction": morphology["mse_reduction"],
            "dark_discrepancy_zone_multitracer_status": multitracer["status"],
        },
        "forbidden_shortcuts": [
            "treat CO-Halpha contrast as the dark discrepancy",
            "compute baryonic gravity without stellar and atomic-gas mass fields",
            "identify channel origin from a morphology-correlated residual",
        ],
        "next_required_acquisition": [
            "source-native HI surface-density maps or a documented central-footprint negligible-HI gate",
            "mass-conversion and vertical-thickness covariance",
        ],
        "claim_boundary": "endpoint architecture and readiness gate; no Tau Core morphology or channel detection",
    }
    (DATA / "dark_discrepancy_primary_endpoint_gate_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    REPORT.write_text(
        "# Dark-discrepancy primary endpoint gate\n\n"
        f"Status: `{result['status']}`\n\n"
        "The primary galaxy target is `Delta_DM(R,theta)=v_common^2-v_baryon^2`, "
        "the discrepancy conventionally attributed to dark matter. CO-Halpha contrast "
        "is retained only as nuisance calibration for `v_common`.\n\n"
        "NGC3351 and NGC4254 now have common tracer velocity fields, CO intensity, "
        "and S4G ICA-cleaned stellar maps. Their 2D endpoint remains closed because "
        "matched HI surface-density fields are absent. No partial baryonic model is scored.\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
