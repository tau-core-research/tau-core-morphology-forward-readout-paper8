#!/usr/bin/env python3
"""Reconstruct a sensitivity-bounded HI radial proxy from the embedded map."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data" / "external" / "literature" / "ngc7479_baryonic_endpoint"
IMAGE = EXT / "pdfimages" / "p5-001.png"
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "ngc7479_hi_radial_proxy_v01.md"
M_HI = 8.58e9
HELIUM = 1.36
DISTANCE_MPC = 32.0
INCLINATION_DEG = 51.0
PA_DEG = 22.0


def main() -> None:
    gray = np.asarray(Image.open(IMAGE).convert("L"), dtype=float)
    height, width = gray.shape
    # Figure bounds: RA 23:02:36 to 23:02:16, Dec +12:06:30 to +12:00:00.
    cos_dec = np.cos(np.deg2rad(12.05))
    sx = 20.0 * 15.0 * cos_dec / width
    sy = 390.0 / height
    cx = (36.0 - 26.52) / 20.0 * width
    cy = (390.0 - 187.9) / 390.0 * height
    yy, xx = np.indices(gray.shape)
    east = -(xx - cx) * sx
    north = -(yy - cy) * sy
    pa = np.deg2rad(PA_DEG)
    major = east * np.sin(pa) + north * np.cos(pa)
    minor = east * np.cos(pa) - north * np.sin(pa)
    radius_arcsec = np.sqrt(major**2 + (minor / np.cos(np.deg2rad(INCLINATION_DEG))) ** 2)
    radius_kpc = radius_arcsec * DISTANCE_MPC * 1e3 / 206265.0
    bins = np.arange(0.0, np.ceil(radius_kpc.max()) + 2.0, 1.0)
    rows = []
    for floor in (0.0, 4.0, 8.0):
        raw = np.maximum(255.0 - gray - floor, 0.0)
        # Exclude a narrow image border where page extraction can introduce edges.
        raw[:2, :] = raw[-2:, :] = raw[:, :2] = raw[:, -2:] = 0.0
        mass_pixel = raw / raw.sum() * M_HI
        shell_mass, _ = np.histogram(radius_kpc, bins=bins, weights=mass_pixel)
        enclosed = np.cumsum(shell_mass) * HELIUM
        centers = 0.5 * (bins[:-1] + bins[1:])
        for r, shell, enc in zip(centers, shell_mass * HELIUM, enclosed):
            rows.append(
                {
                    "grayscale_floor": floor,
                    "radius_kpc": r,
                    "gas_shell_mass_msun_with_helium": shell,
                    "gas_enclosed_mass_msun_with_helium": enc,
                }
            )
    frame = pd.DataFrame(rows)
    frame.to_csv(DATA / "ngc7479_hi_radial_proxy_v01.csv", index=False)
    payload = {
        "schema": "tau_core_ngc7479_hi_radial_proxy_v01",
        "status": "PUBLICATION_RASTER_GAS_PROXY_RECONSTRUCTED_NOT_FITS_GRADE",
        "image_sha256": hashlib.sha256(IMAGE.read_bytes()).hexdigest(),
        "image_shape": [height, width],
        "pixel_scale_arcsec": [sx, sy],
        "center_pixel": [cx, cy],
        "geometry": {"inclination_deg": INCLINATION_DEG, "position_angle_deg": PA_DEG, "distance_mpc": DISTANCE_MPC},
        "hi_mass_normalization_msun": M_HI,
        "helium_factor": HELIUM,
        "grayscale_floor_sensitivities": [0.0, 4.0, 8.0],
        "mass_conservation_relative_error_max": float(
            max(abs(g.gas_shell_mass_msun_with_helium.sum() / (M_HI * HELIUM) - 1.0) for _, g in frame.groupby("grayscale_floor"))
        ),
        "uses_rotation_endpoint_or_dark_discrepancy": False,
        "strict_radial_gas_profile_ready": False,
        "diagnostic_gas_profile_ready": True,
        "endpoint_scoring_allowed": False,
        "remaining_blocker": "recover the calibrated digital moment-0/FITS product or validate publication grayscale linearity against it",
        "claim_boundary": "mass-normalized publication-raster proxy only; not a precision gas gravitational field",
    }
    (DATA / "ngc7479_hi_radial_proxy_v01.json").write_text(json.dumps(payload, indent=2) + "\n")
    REPORT.write_text(
        "# NGC7479 H I radial proxy v01\n\n"
        f"Status: `{payload['status']}`\n\n"
        "The embedded 174x207 grayscale moment-0 image is isolated from the PDF, registered with the published coordinate bounds and kinematic centre, deprojected at `i=51 deg`, `PA=22 deg`, and normalized to the published H I mass. Three grayscale-floor sensitivities are preserved.\n\n"
        "The proxy conserves total H I+helium mass but publication grayscale linearity is not proven. It is suitable for pipeline diagnostics only; precision endpoint scoring remains blocked until the calibrated digital moment-0/FITS product is recovered or validates this reconstruction.\n"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
