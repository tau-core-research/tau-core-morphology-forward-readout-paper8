#!/usr/bin/env python3
"""Score the frozen NGC4254 CO/Halpha common spectral mode."""

from __future__ import annotations

import json
import math
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
C = 299792.458


def reproject(data, source_wcs, target_wcs, shape):
    yy, xx = np.indices(shape, dtype=float)
    ra, dec = target_wcs.pixel_to_world_values(xx, yy)
    sx, sy = source_wcs.world_to_pixel_values(ra, dec)
    return map_coordinates(data, [sy, sx], order=1, mode="constant", cval=np.nan)


def weighted_side(values, errors, select):
    variance = errors[select] ** 2
    weight = 1.0 / variance
    mean = float(np.sum(weight * values[select]) / np.sum(weight))
    formal = float(np.sqrt(1.0 / np.sum(weight)))
    scatter = float(np.nanstd(values[select], ddof=1) / np.sqrt(select.sum()))
    return mean, max(formal, scatter), int(select.sum())


def main() -> None:
    freeze = json.loads((DATA / "ngc4254_common_mode_geometry_freeze_v01.json").read_text())
    if not freeze["freeze_complete"] or freeze["velocity_pixels_read_during_freeze"]:
        raise RuntimeError("Invalid pre-endpoint freeze")
    muse = EXT / "NGC4254_MAPS_copt_0.89asec.fits"
    co = EXT / "group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_mom1wprior.fits"
    eco = EXT / "group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_emom1wprior.fits"
    with fits.open(muse, memmap=True) as h:
        flux = np.asarray(h["HA6562_FLUX"].data, float)
        eflux = np.asarray(h["HA6562_FLUX_ERR"].data, float)
        hvel = np.asarray(h["HA6562_VEL"].data, float)
        ehvel = np.asarray(h["HA6562_VEL_ERR"].data, float)
        mwcs = WCS(h["HA6562_VEL"].header, naxis=2)
        pix = abs(float(h["HA6562_VEL"].header["CD1_1"])) * 3600
        vref = float(h[0].header["REDSHIFT"])
    with fits.open(co, memmap=True) as h:
        cvel = np.squeeze(np.asarray(h[0].data, float))
        ch = h[0].header.copy()
        cwcs = WCS(ch, naxis=2)
        beam = math.sqrt(float(ch["BMAJ"]) * float(ch["BMIN"])) * 3600
    with fits.open(eco, memmap=True) as h:
        ecvel = np.squeeze(np.asarray(h[0].data, float))

    sigma = math.sqrt(max(beam**2 - freeze["muse_input_psf_fwhm_arcsec"] ** 2, 0)) / 2.35482 / pix
    valid = np.isfinite(flux) & np.isfinite(hvel) & (flux > 0) & (np.abs(hvel) < 450)
    sf = gaussian_filter(np.where(valid, flux, 0.0), sigma)
    sv = gaussian_filter(np.where(valid, flux * hvel, 0.0), sigma)
    hvel = reproject(np.divide(sv, sf, out=np.full_like(sv, np.nan), where=sf > 0), mwcs, cwcs, cvel.shape)
    ehvel = reproject(ehvel, mwcs, cwcs, cvel.shape)
    flux = reproject(flux, mwcs, cwcs, cvel.shape)
    eflux = reproject(eflux, mwcs, cwcs, cvel.shape)

    yy, xx = np.indices(cvel.shape, dtype=float)
    ra, dec = cwcs.pixel_to_world_values(xx, yy)
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
    q = freeze["quality"]
    mask = (
        wedge & np.isfinite(cvel) & np.isfinite(ecvel) & (ecvel > 0)
        & (ecvel <= q["maximum_co_velocity_error_km_s"])
        & np.isfinite(hvel) & np.isfinite(ehvel) & (ehvel > 0)
        & (ehvel <= q["maximum_halpha_velocity_error_km_s"])
        & np.isfinite(flux) & np.isfinite(eflux) & (eflux > 0)
        & (flux / eflux >= q["minimum_halpha_flux_snr"])
    )
    beam_pix = max(1, int(math.ceil(beam / (abs(float(ch["CDELT1"])) * 3600))))
    mask &= (xx.astype(int) % beam_pix == 0) & (yy.astype(int) % beam_pix == 0)

    correction = freeze["spectral_transport"]["barycentric_to_lsrk_direction_correction_km_s"]
    z_co = ((cvel - correction) / C) / (1.0 - (cvel - correction) / C)
    z_ha = (vref + hvel) / C
    ez_co = ecvel / C / np.maximum(1.0 - (cvel - correction) / C, 1e-6) ** 2
    ez_ha = ehvel / C
    rows = []
    edges = freeze["radial_edges_arcsec"]
    for tracer, zmap, ezmap in (("CO", z_co, ez_co), ("Halpha", z_ha, ez_ha)):
        for i, (lo, hi) in enumerate(zip(edges[:-1], edges[1:])):
            ann = mask & (radius >= lo) & (radius < hi)
            plus = ann & (major > 0)
            minus = ann & (major < 0)
            if min(plus.sum(), minus.sum()) < 3:
                continue
            zp, ep, npixp = weighted_side(zmap, ezmap, plus)
            zm, em, npixm = weighted_side(zmap, ezmap, minus)
            logg = 0.5 * (math.log1p(zp) + math.log1p(zm))
            elog = 0.5 * math.sqrt((ep / (1 + zp)) ** 2 + (em / (1 + zm)) ** 2)
            rows.append({"tracer": tracer, "annulus": i, "r_lo_arcsec": lo, "r_hi_arcsec": hi,
                         "n_plus": npixp, "n_minus": npixm, "z_plus": zp, "z_minus": zm,
                         "log_g_spec": logg, "sigma_log_g_spec": elog})
    frame = pd.DataFrame(rows)
    contrasts = []
    for tracer, group in frame.groupby("tracer"):
        ref = group[group.annulus.eq(0)].iloc[0]
        for _, row in group.iterrows():
            if row.annulus == 0:
                continue
            contrasts.append({"tracer": tracer, "annulus": int(row.annulus),
                              "r_mid_arcsec": 0.5 * (row.r_lo_arcsec + row.r_hi_arcsec),
                              "delta_log_g": float(row.log_g_spec - ref.log_g_spec),
                              "sigma_delta": float(math.hypot(row.sigma_log_g_spec, ref.sigma_log_g_spec))})
    contrast = pd.DataFrame(contrasts)
    merged = contrast.pivot(index="annulus", columns="tracer", values=["delta_log_g", "sigma_delta"])
    summary_rows = []
    for annulus, row in merged.iterrows():
        coq, haq = row[("delta_log_g", "CO")], row[("delta_log_g", "Halpha")]
        ecoq, ehaq = row[("sigma_delta", "CO")], row[("sigma_delta", "Halpha")]
        wco, wha = 1 / ecoq**2, 1 / ehaq**2
        common = (wco * coq + wha * haq) / (wco + wha)
        ecommon = math.sqrt(1 / (wco + wha))
        diff = coq - haq
        ediff = math.hypot(ecoq, ehaq)
        summary_rows.append({"annulus": int(annulus), "r_mid_arcsec": float(contrast[contrast.annulus.eq(annulus)].r_mid_arcsec.iloc[0]),
                             "q_co": coq, "q_halpha": haq, "q_common": common, "sigma_common": ecommon,
                             "q_co_minus_halpha": diff, "sigma_difference": ediff})
    summary = pd.DataFrame(summary_rows)
    common_chi2 = float(np.sum((summary.q_common / summary.sigma_common) ** 2))
    diff_chi2 = float(np.sum((summary.q_co_minus_halpha / summary.sigma_difference) ** 2))
    result = {
        "schema": "ngc4254_common_mode_multitracer_v01",
        "status": "COMMON_MODE_METHOD_PREFLIGHT_SCORED",
        "n_radial_contrasts": len(summary),
        "common_zero_chi2": common_chi2,
        "common_zero_dof": len(summary),
        "common_zero_p": float(chi2.sf(common_chi2, len(summary))),
        "tracer_agreement_chi2": diff_chi2,
        "tracer_agreement_dof": len(summary),
        "tracer_agreement_p": float(chi2.sf(diff_chi2, len(summary))),
        "maximum_absolute_common_z": float(np.max(np.abs(summary.q_common / summary.sigma_common))),
        "standard_physical_baseline_complete": False,
        "full_spatial_covariance_complete": False,
        "common_channel_detected": False,
        "effective_time_readout_detected": False,
        "claim_boundary": "opened two-tracer method preflight with conservative side scatter; not a channel/time/Tau detection",
    }
    frame.to_csv(DATA / "ngc4254_common_mode_side_spectra_v01.csv", index=False)
    summary.to_csv(DATA / "ngc4254_common_mode_multitracer_profile_v01.csv", index=False)
    (DATA / "ngc4254_common_mode_multitracer_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    (ROOT / "reports/ngc4254_common_mode_multitracer_v01.md").write_text(
        "# NGC4254 common-mode multitracer preflight v01\n\n"
        f"Five radial contrasts give common-mode `chi2={common_chi2:.2f}` for `{len(summary)}` dof "
        f"(`p={result['common_zero_p']:.4g}`), while CO-Halpha agreement gives "
        f"`chi2={diff_chi2:.2f}` (`p={result['tracer_agreement_p']:.4g}`). Maximum absolute "
        f"common-bin significance is `{result['maximum_absolute_common_z']:.2f}`.\n\n"
        "This opened method preflight uses conservative side scatter but not a complete spatial "
        "covariance or conventional gravitational/transverse-Doppler baseline. It cannot detect "
        "a common channel or effective time readout.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
