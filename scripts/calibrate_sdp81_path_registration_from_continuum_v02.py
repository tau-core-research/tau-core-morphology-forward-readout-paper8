#!/usr/bin/env python3
"""Run the one allowed expanded-grid SDP.81 continuum registration audit."""

from __future__ import annotations

import calibrate_sdp81_path_registration_from_continuum_v01 as calibration


calibration.SHIFT_GRID_MAS = [
    -80.0,
    -60.0,
    -40.0,
    -20.0,
    0.0,
    20.0,
    40.0,
    60.0,
    80.0,
]
calibration.SCHEMA = "tau_core.paper8.sdp81-continuum-path-registration.v02"
calibration.OUT = calibration.DATA / "sdp81_continuum_path_registration_v02.json"
calibration.REPORT = (
    calibration.ROOT / "reports/sdp81_continuum_path_registration_v02.md"
)


if __name__ == "__main__":
    calibration.main()
