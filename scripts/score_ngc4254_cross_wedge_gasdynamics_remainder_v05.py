#!/usr/bin/env python3
"""Predict the NGC4254 major-axis tracer difference from off-wedge harmonics."""

import json
import math
import os
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.stats import chi2


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
EXT = ROOT / "data/external/literature/ngc4254_phangs_tracer_velocity"


def sample(data, source_wcs, target_wcs, shape):
    yy, xx = np.indices(shape, dtype=float)
    ra, dec = target_wcs.pixel_to_world_values(xx, yy)
    sx, sy = source_wcs.world_to_pixel_values(ra, dec)
    return map_coordinates(data, [sy, sx], order=1, mode="constant", cval=np.nan)


def fit(design, values, variance):
    weight = 1 / variance
    normal = design.T @ (weight[:, None] * design)
    covariance = np.linalg.pinv(normal)
    coefficient = covariance @ design.T @ (weight * values)
    return coefficient, covariance


def main():
    freeze = json.loads((DATA / "ngc4254_common_mode_geometry_freeze_v01.json").read_text())
    sensitivity_id = os.environ.get("TC_SENSITIVITY_ID", "nominal")
    pa_offset = float(os.environ.get("TC_PA_OFFSET_DEG", "0"))
    inc_offset = float(os.environ.get("TC_INC_OFFSET_DEG", "0"))
    east_offset = float(os.environ.get("TC_CENTER_EAST_OFFSET_ARCSEC", "0"))
    north_offset = float(os.environ.get("TC_CENTER_NORTH_OFFSET_ARCSEC", "0"))
    wedge_half = float(os.environ.get("TC_WEDGE_HALF_DEG", freeze["major_axis_half_wedge_deg"]))
    observed = pd.read_csv(DATA / "ngc4254_common_mode_multitracer_profile_v01.csv")
    with fits.open(EXT / "NGC4254_MAPS_copt_0.89asec.fits", memmap=True) as h:
        flux = np.asarray(h["HA6562_FLUX"].data, float)
        eflux = np.asarray(h["HA6562_FLUX_ERR"].data, float)
        hvel = np.asarray(h["HA6562_VEL"].data, float)
        ehvel = np.asarray(h["HA6562_VEL_ERR"].data, float)
        hwcs = WCS(h["HA6562_VEL"].header, naxis=2)
        pix = abs(float(h["HA6562_VEL"].header["CD1_1"])) * 3600
    co_path = next(EXT.glob("*co21_mom1wprior.fits"))
    eco_path = next(EXT.glob("*co21_emom1wprior.fits"))
    with fits.open(co_path, memmap=True) as h:
        cvel = np.squeeze(np.asarray(h[0].data, float)); header = h[0].header.copy(); cwcs = WCS(header, naxis=2)
        beam = math.sqrt(float(header["BMAJ"]) * float(header["BMIN"])) * 3600
    with fits.open(eco_path, memmap=True) as h:
        ecvel = np.squeeze(np.asarray(h[0].data, float))
    sigma = math.sqrt(max(beam**2 - freeze["muse_input_psf_fwhm_arcsec"]**2, 0)) / 2.35482 / pix
    valid = np.isfinite(flux) & np.isfinite(hvel) & (flux > 0) & (np.abs(hvel) < 450)
    sf = gaussian_filter(np.where(valid, flux, 0), sigma)
    sv = gaussian_filter(np.where(valid, flux * hvel, 0), sigma)
    hvel = sample(np.divide(sv, sf, out=np.full_like(sv, np.nan), where=sf > 0), hwcs, cwcs, cvel.shape)
    ehvel = sample(ehvel, hwcs, cwcs, cvel.shape)
    flux = sample(flux, hwcs, cwcs, cvel.shape); eflux = sample(eflux, hwcs, cwcs, cvel.shape)
    yy, xx = np.indices(cvel.shape, dtype=float)
    ra, dec = cwcs.pixel_to_world_values(xx, yy)
    cra, cdec = freeze["center_icrs_deg"]
    cra += east_offset / (3600 * math.cos(math.radians(cdec)))
    cdec += north_offset / 3600
    east = (ra - cra) * math.cos(math.radians(cdec)) * 3600
    north = (dec - cdec) * 3600
    pa = math.radians(freeze["position_angle_deg_east_of_north"] + pa_offset)
    major = east * math.sin(pa) + north * math.cos(pa)
    minor = -east * math.cos(pa) + north * math.sin(pa)
    disky = minor / math.cos(math.radians(freeze["inclination_deg"] + inc_offset))
    radius = np.hypot(major, disky); theta = np.arctan2(disky, major)
    q = freeze["quality"]
    mask = (
        np.isfinite(cvel) & np.isfinite(ecvel) & (ecvel > 0) & (ecvel <= q["maximum_co_velocity_error_km_s"])
        & np.isfinite(hvel) & np.isfinite(ehvel) & (ehvel > 0) & (ehvel <= q["maximum_halpha_velocity_error_km_s"])
        & np.isfinite(flux) & np.isfinite(eflux) & (eflux > 0) & (flux / eflux >= q["minimum_halpha_flux_snr"])
    )
    beam_pix = max(1, int(math.ceil(beam / (abs(float(header["CDELT1"])) * 3600))))
    mask &= (xx.astype(int) % beam_pix == 0) & (yy.astype(int) % beam_pix == 0)
    contrast = cvel - hvel
    variance = ecvel**2 + ehvel**2
    wedge = np.abs(np.sin(theta)) <= math.sin(math.radians(wedge_half))
    edges = freeze["radial_edges_arcsec"]
    rows = []
    for annulus, (lo, hi) in enumerate(zip(edges[:-1], edges[1:])):
        radial = mask & (radius >= lo) & (radius < hi)
        train = radial & ~wedge
        test = radial & wedge
        design = np.column_stack([np.ones(train.sum()), np.cos(theta[train]), np.sin(theta[train]),
                                  np.cos(2*theta[train]), np.sin(2*theta[train])])
        coefficient, covariance = fit(design, contrast[train], variance[train])
        test_design = np.column_stack([np.ones(test.sum()), np.cos(theta[test]), np.sin(theta[test]),
                                       np.cos(2*theta[test]), np.sin(2*theta[test])])
        prediction = test_design @ coefficient
        plus = major[test] > 0; minus = major[test] < 0
        pred_even = 0.5 * (float(np.mean(prediction[plus])) + float(np.mean(prediction[minus])))
        obs_values = contrast[test]
        obs_even = 0.5 * (float(np.mean(obs_values[plus])) + float(np.mean(obs_values[minus])))
        residual = obs_values - prediction
        residual_even = 0.5 * (float(np.mean(residual[plus])) + float(np.mean(residual[minus])))
        sem = 0.5 * math.hypot(float(np.std(residual[plus], ddof=1)/math.sqrt(plus.sum())),
                               float(np.std(residual[minus], ddof=1)/math.sqrt(minus.sum())))
        rows.append({"annulus": annulus, "r_mid_arcsec": (lo+hi)/2, "n_train": int(train.sum()),
                     "n_test": int(test.sum()), "observed_even_contrast_km_s": obs_even,
                     "predicted_even_contrast_km_s": pred_even, "residual_even_km_s": residual_even,
                     "sigma_residual_even_km_s": sem})
    frame = pd.DataFrame(rows)
    ref = frame.iloc[0]
    radial = frame.iloc[1:].copy()
    radial["residual_radial_contrast_km_s"] = radial.residual_even_km_s - ref.residual_even_km_s
    radial["sigma_residual_radial_km_s"] = np.hypot(radial.sigma_residual_even_km_s, ref.sigma_residual_even_km_s)
    stat = float(np.sum((radial.residual_radial_contrast_km_s / radial.sigma_residual_radial_km_s)**2))
    result = {
        "schema": "ngc4254_cross_wedge_gasdynamics_remainder_v05",
        "sensitivity_id": sensitivity_id,
        "geometry_offsets": {"pa_deg": pa_offset, "inclination_deg": inc_offset,
                             "center_east_arcsec": east_offset, "center_north_arcsec": north_offset,
                             "wedge_half_deg": wedge_half},
        "training_region": "outside frozen +/-30 deg major-axis wedge",
        "heldout_region": "inside frozen major-axis wedge used by G_spec",
        "harmonic_basis": "m0+m1+m2 independently in each frozen annulus",
        "n_heldout_radial_contrasts": len(radial),
        "residual_zero_chi2": stat, "residual_zero_dof": len(radial),
        "residual_zero_p": float(chi2.sf(stat, len(radial))),
        "maximum_absolute_residual_km_s": float(radial.residual_radial_contrast_km_s.abs().max()),
        "endpoint_independent_source_body_prediction": False,
        "spatial_holdout_nuisance_prediction": True,
        "common_channel_remainder_identified": False,
        "claim_boundary": "cross-wedge gas-dynamic nuisance prediction; same endpoint field, not source-side Tau prediction",
    }
    suffix = "" if sensitivity_id == "nominal" else f"_{sensitivity_id}"
    frame.to_csv(DATA / f"ngc4254_cross_wedge_gasdynamics_profile_v05{suffix}.csv", index=False)
    (DATA / f"ngc4254_cross_wedge_gasdynamics_remainder_v05{suffix}.json").write_text(json.dumps(result, indent=2)+"\n")
    if sensitivity_id == "nominal":
      (ROOT / "reports/ngc4254_cross_wedge_gasdynamics_remainder_v05.md").write_text(
        "# NGC4254 cross-wedge gas-dynamics remainder v05\n\n"
        f"Off-wedge `m0+m1+m2` fits predict the held-out major-axis wedge. Five radial "
        f"residual contrasts give `chi2={stat:.2f}/5` (`p={result['residual_zero_p']:.4g}`); "
        f"maximum absolute residual is `{result['maximum_absolute_residual_km_s']:.2f} km/s`.\n\n"
        "This is a spatial holdout nuisance test using the same endpoint field, not an independent "
        "source-body prediction. Any surviving residual remains unqualified as a channel signal.\n"
      )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
