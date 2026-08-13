#!/usr/bin/env python3
"""Compare frozen NGC4254 common-mode differences with line-width structure."""

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import map_coordinates
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
EXT = ROOT / "data/external/literature/ngc4254_phangs_tracer_velocity"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sample(data, source_wcs, target_wcs, shape):
    yy, xx = np.indices(shape, dtype=float)
    ra, dec = target_wcs.pixel_to_world_values(xx, yy)
    sx, sy = source_wcs.world_to_pixel_values(ra, dec)
    return map_coordinates(data, [sy, sx], order=1, mode="constant", cval=np.nan)


def main():
    freeze = json.loads((DATA / "ngc4254_common_mode_geometry_freeze_v01.json").read_text())
    profile = pd.read_csv(DATA / "ngc4254_common_mode_multitracer_profile_v01.csv")
    mom2_path = next(EXT.glob("*strict_mom2.fits"))
    ew_path = next(EXT.glob("*strict_ew.fits"))
    muse_path = EXT / "NGC4254_MAPS_copt_0.89asec.fits"
    with fits.open(mom2_path, memmap=True) as h:
        mom2 = np.squeeze(np.asarray(h[0].data, float)); header = h[0].header.copy(); wcs = WCS(header, naxis=2)
    with fits.open(ew_path, memmap=True) as h:
        ew = np.squeeze(np.asarray(h[0].data, float))
    with fits.open(muse_path, memmap=True) as h:
        hsigma = np.asarray(h["HA6562_SIGMA"].data, float)
        hesigma = np.asarray(h["HA6562_SIGMA_ERR"].data, float)
        hwcs = WCS(h["HA6562_SIGMA"].header, naxis=2)
    hsigma = sample(hsigma, hwcs, wcs, mom2.shape)
    hesigma = sample(hesigma, hwcs, wcs, mom2.shape)
    yy, xx = np.indices(mom2.shape, dtype=float)
    ra, dec = wcs.pixel_to_world_values(xx, yy)
    cra, cdec = freeze["center_icrs_deg"]
    east = (ra - cra) * math.cos(math.radians(cdec)) * 3600
    north = (dec - cdec) * 3600
    pa = math.radians(freeze["position_angle_deg_east_of_north"])
    major = east * math.sin(pa) + north * math.cos(pa)
    minor = -east * math.cos(pa) + north * math.sin(pa)
    disky = minor / math.cos(math.radians(freeze["inclination_deg"]))
    radius = np.hypot(major, disky)
    theta = np.arctan2(disky, major)
    wedge = np.abs(np.sin(theta)) <= math.sin(math.radians(freeze["major_axis_half_wedge_deg"]))
    rows = []
    edges = freeze["radial_edges_arcsec"]
    for annulus, (lo, hi) in enumerate(zip(edges[:-1], edges[1:])):
        select = wedge & (radius >= lo) & (radius < hi) & np.isfinite(mom2) & np.isfinite(ew)
        hselect = select & np.isfinite(hsigma) & np.isfinite(hesigma) & (hesigma > 0) & (hesigma < 10)
        rows.append({
            "annulus": annulus, "r_mid_arcsec": (lo + hi) / 2,
            "co_mom2_median_km_s": float(np.nanmedian(mom2[select])),
            "co_ew_median_km_s": float(np.nanmedian(ew[select])),
            "halpha_sigma_observed_median_km_s": float(np.nanmedian(hsigma[hselect])),
            "n_co": int(select.sum()), "n_halpha": int(hselect.sum()),
        })
    widths = pd.DataFrame(rows)
    joined = profile.merge(widths, on=["annulus", "r_mid_arcsec"])
    difference = np.abs(joined.q_co_minus_halpha) * 299792.458
    rho_m2, p_m2 = spearmanr(difference, joined.co_mom2_median_km_s)
    rho_ha, p_ha = spearmanr(difference, joined.halpha_sigma_observed_median_km_s)
    result = {
        "schema": "ngc4254_linewidth_tracer_difference_v03",
        "sources": {
            "co_strict_mom2": {"path": str(mom2_path.relative_to(ROOT)), "sha256": digest(mom2_path)},
            "co_strict_ew": {"path": str(ew_path.relative_to(ROOT)), "sha256": digest(ew_path)},
        },
        "n_nonreference_annuli": len(joined),
        "absolute_tracer_difference_vs_co_mom2_spearman": {"rho": float(rho_m2), "p": float(p_m2)},
        "absolute_tracer_difference_vs_halpha_observed_sigma_spearman": {"rho": float(rho_ha), "p": float(p_ha)},
        "co_linewidth_data_blocker_removed": True,
        "pressure_support_correction_derived": False,
        "reasons_not_corrected": [
            "five nonreference annuli only",
            "Halpha sigma includes instrumental and thermal broadening",
            "moment-2 and equivalent width do not uniquely determine asymmetric drift",
            "surface-density and anisotropy gradients are not yet propagated",
        ],
        "common_channel_detected": False,
        "claim_boundary": "linewidth association diagnostic, not a pressure correction or channel test",
    }
    joined.to_csv(DATA / "ngc4254_linewidth_tracer_difference_profile_v03.csv", index=False)
    (DATA / "ngc4254_linewidth_tracer_difference_v03.json").write_text(json.dumps(result, indent=2) + "\n")
    (ROOT / "reports/ngc4254_linewidth_tracer_difference_v03.md").write_text(
        "# NGC4254 line-width versus tracer-difference audit v03\n\n"
        f"The official PHANGS CO strict moment-2 and equivalent-width maps are now checksum-frozen. "
        f"Across five nonreference annuli, absolute CO-Halpha common-mode difference versus CO "
        f"moment-2 gives Spearman `rho={rho_m2:.3f}` (`p={p_m2:.3f}`); versus observed Halpha "
        f"sigma it gives `rho={rho_ha:.3f}` (`p={p_ha:.3f}`).\n\n"
        "With five bins and no fully corrected Halpha intrinsic dispersion or pressure-gradient model, "
        "this cannot derive an asymmetric-drift correction. It removes the CO-width acquisition blocker "
        "and supplies a conventional-physics diagnostic only.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
