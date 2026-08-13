#!/usr/bin/env python3
"""Freeze the external SIMBAD center on the printed WHISP B1950 axes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
ICRS = {"ra_deg": 202.40211666666664, "dec_deg": 58.41873055555556}
B1950 = {"ra_h": 13, "ra_m": 27, "ra_s": 43.95673432049165,
         "dec_d": 58, "dec_m": 40, "dec_s": 35.30635042275776}


def main() -> None:
    axis = json.loads((DATA / "ugc08490_whisp_angular_axis_preflight_v01.json").read_text())
    ra_value = B1950["ra_m"] * 60 + B1950["ra_s"]
    dec_value = B1950["dec_m"] + B1950["dec_s"] / 60
    ra0 = axis["ra_tick_anchors"]; dec0 = axis["dec_tick_anchors"]
    ra_slope = axis["ra_seconds_of_time_per_pixel"]
    dec_slope = axis["dec_arcmin_per_pixel"]
    ra_intercept = sum(y - ra_slope*x for x,y in ra0) / len(ra0)
    dec_intercept = sum(y - dec_slope*x for x,y in dec0) / len(dec0)
    center = [(ra_value-ra_intercept)/ra_slope, (dec_value-dec_intercept)/dec_slope]
    panel_centers = {
        "60arcsec": center,
        "30arcsec": [center[0] - 220.0, center[1]],
        "full_resolution": [center[0] - 440.0, center[1]],
    }
    payload = {
        "schema": "ugc08490_whisp_external_center_freeze_v01",
        "status": "UGC08490_EXTERNAL_CENTER_FROZEN_ON_PRINTED_B1950_AXES",
        "source": "SIMBAD UGC 8490 / NGC 5204 coordinate",
        "source_url": "https://simbad.cds.unistra.fr/simbad/sim-id?Ident=UGC+8490",
        "icrs_coordinate_deg": ICRS, "fk4_b1950_coordinate": B1950,
        "center_source_pixels": center,
        "center_source_pixels_by_panel": panel_centers,
        "horizontal_panel_spacing_pixels": 220.0,
        "conversion": "Astropy ICRS to FK4 B1950; printed-axis linear calibration",
        "center_selected_from_velocity_or_endpoint": False,
        "allowed_next_use": "freeze beam-scale radial annuli and side geometry",
        "endpoint_access": False,
        "claim_boundary": "external center on printed graphical axes; not formal FITS WCS",
    }
    (DATA / "ugc08490_whisp_external_center_freeze_v01.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["status"])


if __name__ == "__main__":
    main()
