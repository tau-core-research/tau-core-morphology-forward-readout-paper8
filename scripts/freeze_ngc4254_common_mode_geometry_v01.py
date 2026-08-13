#!/usr/bin/env python3
"""Freeze the NGC4254 common-mode geometry before evaluating velocity pixels."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/ngc4254_common_mode_geometry_freeze_v01.md"


def main() -> None:
    freeze = {
        "schema": "ngc4254_common_mode_geometry_freeze_v01",
        "galaxy": "NGC4254",
        "center_icrs_deg": [184.7067, 14.4168],
        "position_angle_deg_east_of_north": 68.1,
        "inclination_deg": 34.4,
        "geometry_source": "existing source-frozen PHANGS Halpha kinematic geometry",
        "muse_input_psf_fwhm_arcsec": 0.89,
        "target_resolution": "native PHANGS-ALMA CO beam; flux-weighted MUSE smoothing",
        "major_axis_half_wedge_deg": 30.0,
        "radial_edges_arcsec": [5.0, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0],
        "reference_annulus_arcsec": [5.0, 15.0],
        "side_rule": "sign of source-frozen deprojected major-axis coordinate",
        "quality": {
            "minimum_halpha_flux_snr": 5.0,
            "maximum_halpha_velocity_error_km_s": 10.0,
            "maximum_co_velocity_error_km_s": 10.0,
            "absolute_halpha_relative_velocity_limit_km_s": 450.0,
            "beam_independent_subsampling": True,
        },
        "spectral_transport": {
            "muse": "z=(v_reference_barycentric+v_relative)/c",
            "co": "subtract frozen BARYCENT-to-LSRK direction correction from radio velocity, then z=u/(1-u)",
            "barycentric_to_lsrk_direction_correction_km_s": 3.586395393549658,
            "empirical_intertracer_offset_allowed": False,
        },
        "statistics": {
            "log_g_spec": "0.5*(log(1+z_plus)+log(1+z_minus))",
            "radial_contrast": "log_g_spec(R)-log_g_spec(reference_annulus)",
            "common_mode": "inverse-variance CO/Halpha radial contrast",
            "tracer_control": "CO radial contrast minus Halpha radial contrast",
        },
        "standard_null_controls": [
            "zero radial common mode",
            "CO-Halpha tracer difference",
            "approaching/receding sampling balance",
            "line-width and fit-quality sensitivity",
            "center/PA/inclination perturbation reserved for v02",
            "ordinary gravitational and transverse-Doppler scale audit",
        ],
        "velocity_pixels_read_during_freeze": False,
        "freeze_complete": True,
        "claim_boundary": "pre-endpoint geometry and statistic freeze; no channel or time signal",
    }
    path = DATA / "ngc4254_common_mode_geometry_freeze_v01.json"
    path.write_text(json.dumps(freeze, indent=2) + "\n")
    REPORT.write_text(
        "# NGC4254 common-mode geometry freeze v01\n\n"
        "The source-frozen center, `PA=68.1 deg`, `i=34.4 deg`, a `+/-30 deg` "
        "major-axis wedge, six fixed `10 arcsec` annuli from `5` to `65 arcsec`, "
        "and the innermost annulus as reference are frozen before velocity pixels "
        "are evaluated. MUSE is smoothed to the native CO beam. No empirical "
        "inter-tracer velocity offset is allowed.\n\n"
        "**Claim boundary:** pre-endpoint geometry/statistic freeze only.\n"
    )


if __name__ == "__main__":
    main()
