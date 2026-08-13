#!/usr/bin/env python3
"""Register the published SDP.81 image-G coordinate on the ALMA Band-7 WCS."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord, SkyOffsetFrame
from astropy.io import fits
from astropy.wcs import FITSFixedWarning, WCS


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
FREEZE = DATA / "sdp81_lens_operator_freeze_v01.json"
GEOMETRY = DATA / "sdp81_lens_operator_geometry_validation_v01.json"
IMAGE = ROOT / (
    "data/external/literature/sdp81_multipath_channel/"
    "SDP81_Band7_ReferenceImages/SDP81_band7_11exec.contR1.image.fits"
)
OUT = DATA / "sdp81_image_g_wcs_registration_v01.json"
REPORT = ROOT / "reports/sdp81_image_g_wcs_registration_v01.md"


def main() -> None:
    frozen = json.loads(FREEZE.read_text(encoding="utf-8"))
    geometry = json.loads(GEOMETRY.read_text(encoding="utf-8"))
    g_icrs = frozen["coordinates"]["image_G_icrs_j2000"]
    g = SkyCoord(
        g_icrs["ra_hms"],
        g_icrs["dec_dms"],
        unit=(u.hourangle, u.deg),
        frame="icrs",
    )

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        with fits.open(IMAGE) as hdul:
            image = np.squeeze(hdul[0].data).astype(float)
            header = hdul[0].header
            wcs = WCS(header).celestial
            beam_major_arcsec = float(header["BMAJ"]) * 3600.0
            beam_minor_arcsec = float(header["BMIN"]) * 3600.0

    gx, gy = (float(value) for value in wcs.world_to_pixel(g))
    ix, iy = round(gx), round(gy)
    radius_pixels = 60
    cutout = image[
        iy - radius_pixels : iy + radius_pixels + 1,
        ix - radius_pixels : ix + radius_pixels + 1,
    ]
    peak_index = int(np.nanargmax(cutout))
    peak_y_local, peak_x_local = np.unravel_index(peak_index, cutout.shape)
    peak_x = ix - radius_pixels + int(peak_x_local)
    peak_y = iy - radius_pixels + int(peak_y_local)
    peak_sky = wcs.pixel_to_world(peak_x, peak_y)
    peak_offset_arcsec = float(g.separation(peak_sky).arcsec)

    offset_frame = SkyOffsetFrame(origin=g)
    q1_rows = []
    for path_index, (lens_x_arcsec, north_arcsec) in enumerate(
        geometry["image_positions_arcsec_relative_to_G"]["q1"], start=1
    ):
        sky = SkyCoord(
            lon=-lens_x_arcsec * u.arcsec,
            lat=north_arcsec * u.arcsec,
            frame=offset_frame,
        ).transform_to("icrs")
        px, py = (float(value) for value in wcs.world_to_pixel(sky))
        q1_rows.append(
            {
                "path_index": path_index,
                "lens_x_west_offset_arcsec": lens_x_arcsec,
                "north_offset_arcsec": north_arcsec,
                "ra_deg": float(sky.ra.deg),
                "dec_deg": float(sky.dec.deg),
                "pixel_x_zero_based": px,
                "pixel_y_zero_based": py,
            }
        )

    tolerance_arcsec = 1.5 * beam_major_arcsec
    counterpart_consistent = peak_offset_arcsec <= tolerance_arcsec
    result = {
        "schema": "tau_core.paper8.sdp81-image-g-wcs-registration.v01",
        "status": (
            "IMAGE_G_WCS_ANCHOR_OPERATIONAL_WITH_BEAM_SCALE_SYSTEMATIC"
            if counterpart_consistent
            else "IMAGE_G_WCS_COUNTERPART_VALIDATION_FAILED"
        ),
        "anchor": {
            "source": frozen["coordinates"]["image_G_icrs_j2000"]["source"],
            "ra_hms": g_icrs["ra_hms"],
            "dec_dms": g_icrs["dec_dms"],
            "pixel_x_zero_based": gx,
            "pixel_y_zero_based": gy,
        },
        "local_compact_peak": {
            "pixel_x_zero_based": peak_x,
            "pixel_y_zero_based": peak_y,
            "separation_from_published_g_arcsec": peak_offset_arcsec,
            "beam_major_arcsec": beam_major_arcsec,
            "beam_minor_arcsec": beam_minor_arcsec,
            "acceptance_tolerance_arcsec": tolerance_arcsec,
            "counterpart_consistent_within_tolerance": counterpart_consistent,
        },
        "q1_paths": q1_rows,
        "lens_x_convention": (
            "positive lens-model x is westward RA offset; WCS sky-offset longitude "
            "therefore uses -x"
        ),
        "q1_path_count": len(q1_rows),
        "absolute_wcs_registration_operational": counterpart_consistent,
        "body_covector_pullback_materialized": False,
        "pathwise_sensitivity_requirement": (
            "repeat extraction over at least the published-coordinate to local-peak "
            "offset and the frozen smooth-lens family"
        ),
        "claim_boundary": (
            "Operational image-plane WCS registration with beam-scale systematic; "
            "not a body covector, time predictor, channel effect, or Tau detection."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 image-G WCS registration v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The published image-G coordinate maps to pixel `({gx:.3f}, {gy:.3f})`. "
        f"The nearest local compact peak is offset by `{peak_offset_arcsec:.4f}` "
        f"arcsec; the declared 1.5-beam-major tolerance is `{tolerance_arcsec:.4f}` "
        "arcsec. The four q1 image positions are now represented in the absolute "
        "Band-7 WCS.\n\n"
        "This closes the coordinate-anchor portion of the path geometry only. A "
        "body-derived covector and its ray-traced pullback remain absent.\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
