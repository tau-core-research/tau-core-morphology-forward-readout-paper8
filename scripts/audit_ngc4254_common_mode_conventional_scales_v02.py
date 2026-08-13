#!/usr/bin/env python3
"""Quantify conventional scale bounds for the NGC4254 common-mode preflight."""

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
C = 299792.458


def main() -> None:
    sides = pd.read_csv(DATA / "ngc4254_common_mode_side_spectra_v01.csv")
    profile = pd.read_csv(DATA / "ngc4254_common_mode_multitracer_profile_v01.csv")
    # Conservative orbital scale from the largest side displacement about each
    # tracer's annular midpoint. This does not fit a channel component.
    side_mid = 0.5 * (sides.z_plus + sides.z_minus)
    beta_orb = np.maximum(np.abs(sides.z_plus - side_mid), np.abs(sides.z_minus - side_mid))
    vmax = float(C * beta_orb.max())
    transverse_bound = vmax**2 / (2 * C)
    gravitational_scale_bound = vmax**2 / C
    discrepancy = np.abs(profile.q_co_minus_halpha) * C
    result = {
        "schema": "ngc4254_common_mode_conventional_scales_v02",
        "maximum_inferred_side_orbital_scale_km_s": vmax,
        "transverse_doppler_upper_scale_km_s": transverse_bound,
        "gravitational_redshift_order_scale_km_s": gravitational_scale_bound,
        "combined_relativistic_order_scale_km_s": transverse_bound + gravitational_scale_bound,
        "observed_co_halpha_difference_km_s": {
            "minimum": float(discrepancy.min()),
            "maximum": float(discrepancy.max()),
        },
        "relativistic_scale_can_explain_tracer_difference": bool(
            transverse_bound + gravitational_scale_bound >= discrepancy.min()
        ),
        "co_moment2_or_cube_available": False,
        "asymmetric_drift_closed": False,
        "noncircular_streaming_closed": False,
        "geometry_perturbation_closed": False,
        "full_spatial_covariance_closed": False,
        "next_required_data": [
            "PHANGS-ALMA CO cube or matched moment-2/equivalent-width product",
            "matched Halpha line-profile rather than moment-1 only",
            "source-frozen center/PA/inclination perturbation replay",
            "beam-correlated annulus covariance",
        ],
        "common_channel_detected": False,
        "claim_boundary": (
            "order-of-magnitude conventional baseline audit; relativistic terms are too small, "
            "but gas dynamics, geometry, line formation, and covariance remain open"
        ),
    }
    (DATA / "ngc4254_common_mode_conventional_scales_v02.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    (ROOT / "reports/ngc4254_common_mode_conventional_scales_v02.md").write_text(
        "# NGC4254 common-mode conventional-scale audit v02\n\n"
        f"The largest paired orbital scale is `{vmax:.2f} km/s`. Its transverse-Doppler "
        f"scale is at most `{transverse_bound:.3f} km/s`, and the order-of-magnitude "
        f"galactic gravitational-redshift scale is `{gravitational_scale_bound:.3f} km/s`. "
        f"Their sum (`{transverse_bound + gravitational_scale_bound:.3f} km/s`) is far "
        f"below the observed CO-Halpha difference (`{discrepancy.min():.2f}-"
        f"{discrepancy.max():.2f} km/s`).\n\n"
        "This excludes those two small relativistic scales as a complete explanation, not "
        "ordinary gas dynamics. The local packet has no CO cube/moment-2 product, so "
        "asymmetric drift, non-circular streaming, line-profile mixing, geometry "
        "perturbations, and full spatial covariance remain open. No channel signal is detected.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
