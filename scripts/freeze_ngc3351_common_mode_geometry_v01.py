#!/usr/bin/env python3
"""Freeze NGC3351 as the untouched replication of the NGC4254 protocol."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"


def main():
    freeze = {
        "schema": "ngc3351_common_mode_geometry_freeze_v01",
        "galaxy": "NGC3351",
        "protocol_parent": "ngc4254_common_mode_geometry_freeze_v01",
        "center_icrs_deg": [160.9906, 11.7037],
        "position_angle_deg_east_of_north": 193.0,
        "inclination_deg": 41.0,
        "geometry_source": "existing source-frozen PHANGS Halpha kinematic geometry",
        "muse_input_psf_fwhm_arcsec": 1.05,
        "target_resolution": "native PHANGS-ALMA CO beam; flux-weighted MUSE smoothing",
        "major_axis_half_wedge_deg": 30.0,
        "radial_edges_arcsec": [5.0, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0],
        "reference_annulus_arcsec": [5.0, 15.0],
        "quality": {"minimum_halpha_flux_snr": 5.0, "maximum_halpha_velocity_error_km_s": 10.0,
                    "maximum_co_velocity_error_km_s": 10.0,
                    "absolute_halpha_relative_velocity_limit_km_s": 450.0,
                    "beam_independent_subsampling": True},
        "spectral_transport": {
            "muse_reference_velocity_km_s": 774.736,
            "barycentric_to_lsrk_direction_correction_km_s": -3.7630557874444444,
            "empirical_intertracer_offset_allowed": False,
        },
        "geometry_sensitivity": {"pa_offset_deg": [-5, 5], "inclination_offset_deg": [-5, 5],
                                 "center_offsets_arcsec": [-1, 1], "wedge_half_deg": [20, 40]},
        "velocity_pixels_read_during_freeze": False,
        "replication_settings_changed_after_ngc4254": False,
        "freeze_complete": True,
        "claim_boundary": "untouched replication freeze; no NGC3351 velocity endpoint read",
    }
    (DATA / "ngc3351_common_mode_geometry_freeze_v01.json").write_text(json.dumps(freeze, indent=2)+"\n")
    (ROOT / "reports/ngc3351_common_mode_geometry_freeze_v01.md").write_text(
        "# NGC3351 common-mode replication freeze v01\n\n"
        "The NGC4254 six-annulus, `+/-30 deg` wedge, CO-resolution, quality-mask, "
        "spectral-transport, off-wedge nuisance, and geometry-sensitivity protocol is "
        "transferred unchanged. Only source-native NGC3351 center, PA, inclination, PSF, "
        "systemic reference, and fixed ICRS/LSRK direction correction differ. No velocity "
        "pixel was read during this freeze.\n"
    )


if __name__ == "__main__":
    main()
