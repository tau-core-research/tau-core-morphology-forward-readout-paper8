#!/usr/bin/env python3
"""Audit whether NGC4254 supports a resolved 2D dark-discrepancy field."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import map_coordinates


ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data/external/literature/ngc4254_phangs_tracer_velocity"
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/ngc4254_dark_discrepancy_2d_resolution_audit_v01.md"
HI_BEAM_MAJOR_ARCSEC = 0.010473 * 3600.0
HI_BEAM_MINOR_ARCSEC = 0.0091517 * 3600.0


def sample_mask(source: np.ndarray, source_wcs: WCS, target_wcs: WCS, shape: tuple[int, int]) -> np.ndarray:
    yy, xx = np.indices(shape, dtype=float)
    ra, dec = target_wcs.pixel_to_world_values(xx, yy)
    sx, sy = source_wcs.world_to_pixel_values(ra, dec)
    return map_coordinates(source.astype(float), [sy, sx], order=0, mode="constant", cval=0.0) > 0.5


def main() -> None:
    common_path = DATA / "ngc4254_phangs_common_tracer_velocity_field_v01.fits"
    hi_path = EXT / "ngc4254.viva.mom0.fits"
    with fits.open(common_path) as h:
        common = np.asarray(h["COMMON_VEL"].data, float)
        common_mask = np.asarray(h["COMMON_MASK"].data, bool)
        common_wcs = WCS(h["COMMON_VEL"].header, naxis=2)
        pixel_arcsec = abs(float(h["COMMON_VEL"].header["CDELT1"])) * 3600.0
    with fits.open(hi_path) as h:
        hi = np.asarray(h[0].data, float)
        hi_header = h[0].header.copy()
        hi_header["CUNIT1"] = "deg"
        hi_header["CUNIT2"] = "deg"
        hi_wcs = WCS(hi_header, naxis=2)
    hi_support = sample_mask(np.isfinite(hi) & (hi > 0), hi_wcs, common_wcs, common.shape)
    overlap = common_mask & hi_support & np.isfinite(common)
    area_arcsec2 = float(overlap.sum()) * pixel_arcsec**2
    beam_area_arcsec2 = math.pi / (4.0 * math.log(2.0)) * HI_BEAM_MAJOR_ARCSEC * HI_BEAM_MINOR_ARCSEC
    independent_beams = area_arcsec2 / beam_area_arcsec2
    harmonic_allowed = independent_beams >= 25
    result = {
        "schema": "ngc4254_dark_discrepancy_2d_resolution_audit_v01",
        "status": (
            "NGC4254_FIVE_ZONE_2D_DARK_DISCREPANCY_RESOLUTION_READY"
            if harmonic_allowed else
            "NGC4254_RADIAL_ONLY_DARK_DISCREPANCY_READY_2D_HARMONIC_RESOLUTION_BLOCKED"
        ),
        "hi_beam_major_arcsec": HI_BEAM_MAJOR_ARCSEC,
        "hi_beam_minor_arcsec": HI_BEAM_MINOR_ARCSEC,
        "beam_provenance": "VIVA FITS HISTORY AIPS CLEAN BMAJ/BMIN",
        "common_grid_pixel_arcsec": pixel_arcsec,
        "overlap_area_arcsec2": area_arcsec2,
        "independent_hi_beams_in_common_support": independent_beams,
        "minimum_beams_for_five_zone_m0_m1_m2_model": 25,
        "five_zone_harmonic_model_allowed": harmonic_allowed,
        "coarse_radial_profile_allowed": independent_beams >= 10,
        "fine_scale_channel_claim_allowed": False,
        "required_common_resolution": "VIVA HI beam",
        "claim_boundary": "resolution/readiness audit; no baryonic gravity, dark discrepancy, morphology, or channel result",
    }
    (DATA / "ngc4254_dark_discrepancy_2d_resolution_audit_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    REPORT.write_text(
        "# NGC4254 2D dark-discrepancy resolution audit\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The VIVA H I beam is `{HI_BEAM_MAJOR_ARCSEC:.1f} x {HI_BEAM_MINOR_ARCSEC:.1f}` "
        f"arcsec. The common H I/CO/H-alpha support contains approximately "
        f"`{independent_beams:.1f}` independent H I beams. This "
        f"{'passes' if harmonic_allowed else 'fails'} the declared 25-beam gate for a "
        "five-zone `m=0,1,2` diagnostic. A coarse radial discrepancy profile remains "
        "allowed, but angular channel attribution does not.\n",
        encoding="utf-8",
    )
    print(result["status"], independent_beams)


if __name__ == "__main__":
    main()
