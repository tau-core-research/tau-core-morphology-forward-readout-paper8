#!/usr/bin/env python3
"""Extract the independent NGC7479 HI endpoint and gas-source metadata."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data" / "external" / "literature" / "ngc7479_baryonic_endpoint"
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "ngc7479_hi_endpoint_source_v01.md"
PDF = EXT / "laine1998_hi.pdf"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    radii = list(range(40, 131, 10))
    velocities = [171.0, 191.7, 201.1, 208.0, 211.3, 215.9, 214.0, 214.5, 216.9, 216.9]
    errors = [8.3, 4.8, 4.0, 3.8, 5.4, 4.3, 4.6, 4.6, 5.4, 6.1]
    frame = pd.DataFrame(
        {
            "galaxy": "NGC 7479",
            "radius_arcsec": radii,
            "vrot_hi_km_s": velocities,
            "vrot_error_km_s": errors,
            "side_policy": "south_eastern_less_perturbed_side",
            "inclination_deg": 51.0,
            "position_angle_deg": 22.0,
            "distance_mpc_source": 32.0,
            "source_table": "Laine_and_Gottesman_1998_Table_5",
            "uses_coming_co_or_tau_residual": False,
        }
    )
    frame["radius_kpc_at_source_distance"] = frame.radius_arcsec * 32.0e3 / 206265.0
    frame.to_csv(DATA / "ngc7479_hi_rotation_endpoint_v01.csv", index=False)
    payload = {
        "schema": "tau_core_ngc7479_hi_endpoint_source_v01",
        "status": "INDEPENDENT_HI_ROTATION_ENDPOINT_AND_GAS_MAP_SOURCE_ACQUIRED",
        "source": "Laine and Gottesman 1998, MNRAS 297, 1041",
        "source_url": "https://adsabs.harvard.edu/pdf/1998MNRAS.297.1041L",
        "source_pdf_sha256": sha256(PDF),
        "n_rotation_points": len(frame),
        "rotation_radius_arcsec_range": [min(radii), max(radii)],
        "rotation_radius_kpc_range_at_source_distance": [float(frame.radius_kpc_at_source_distance.min()), float(frame.radius_kpc_at_source_distance.max())],
        "hi_mass_msun": 8.58e9,
        "hi_mass_error_msun": 0.30e9,
        "hi_moment0_map_published": True,
        "hi_moment0_beam_arcsec": [9.7, 7.4],
        "hi_column_density_rms_atoms_cm2": 7e19,
        "numeric_radial_hi_surface_density_profile_published": False,
        "independent_of_coming_co_morphology": True,
        "stellar_ml_1p35_route_endpoint_calibrated_and_primary_forbidden": True,
        "dark_discrepancy_ready": False,
        "endpoint_scoring_allowed": False,
        "remaining_blocker": "derive a residual-blind radial gas profile and independently normalized stellar gravitational velocity field",
        "claim_boundary": "independent observed endpoint acquired; baryonic prediction not yet complete",
    }
    (DATA / "ngc7479_hi_endpoint_source_v01.json").write_text(json.dumps(payload, indent=2) + "\n")
    REPORT.write_text(
        "# NGC7479 H I endpoint source v01\n\n"
        f"Status: `{payload['status']}`\n\n"
        "Laine and Gottesman Table 5 supplies ten independent H I rotation points from 40 to 130 arcsec using the less-perturbed south-eastern side. "
        "The same source reports `M_HI=(8.58+/-0.30)e9 Msun` and a calibrated moment-0 map at `9.7x7.4 arcsec` beam.\n\n"
        "No numeric radial H I surface-density table is published. The Quillen K-band `M/L~1.35` route is normalized to the observed rotation curve and is forbidden as the primary baryonic predictor. "
        "A residual-blind gas profile and independently normalized stellar field remain required before dark-discrepancy scoring.\n"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
