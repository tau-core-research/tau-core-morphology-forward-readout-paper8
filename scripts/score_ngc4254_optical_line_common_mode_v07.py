#!/usr/bin/env python3
"""Test common-mode consistency across five NGC4254 MUSE emission lines."""

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
LINES = ["HB4861", "OIII5006", "HA6562", "NII6583", "SII6716"]


def sample(data, source_wcs, target_wcs, shape):
    yy, xx = np.indices(shape, dtype=float)
    ra, dec = target_wcs.pixel_to_world_values(xx, yy)
    sx, sy = source_wcs.world_to_pixel_values(ra, dec)
    return map_coordinates(data, [sy, sx], order=1, mode="constant", cval=np.nan)


def side_mean(z, ez, select):
    w = 1 / ez[select]**2
    mean = float(np.sum(w*z[select])/np.sum(w))
    scatter = float(np.nanstd(z[select], ddof=1)/np.sqrt(select.sum()))
    return mean, max(float(np.sqrt(1/np.sum(w))), scatter), int(select.sum())


def main():
    freeze = json.loads((DATA / "ngc4254_common_mode_geometry_freeze_v01.json").read_text())
    co_path = next(EXT.glob("*co21_mom1wprior.fits"))
    with fits.open(co_path, memmap=True) as h:
        target = np.squeeze(np.asarray(h[0].data, float)); header = h[0].header.copy(); twcs = WCS(header, naxis=2)
        beam = math.sqrt(float(header["BMAJ"])*float(header["BMIN"]))*3600
    with fits.open(EXT / "NGC4254_MAPS_copt_0.89asec.fits", memmap=True) as h:
        vref = float(h[0].header["REDSHIFT"])
        line_maps = {}
        for line in LINES:
            flux = np.asarray(h[f"{line}_FLUX"].data, float)
            eflux = np.asarray(h[f"{line}_FLUX_ERR"].data, float)
            vel = np.asarray(h[f"{line}_VEL"].data, float)
            evel = np.asarray(h[f"{line}_VEL_ERR"].data, float)
            wcs = WCS(h[f"{line}_VEL"].header, naxis=2)
            pix = abs(float(h[f"{line}_VEL"].header["CD1_1"]))*3600
            sigma = math.sqrt(max(beam**2-freeze["muse_input_psf_fwhm_arcsec"]**2, 0))/2.35482/pix
            valid = np.isfinite(flux)&np.isfinite(vel)&(flux>0)&(np.abs(vel)<450)
            sf = gaussian_filter(np.where(valid, flux, 0), sigma)
            sv = gaussian_filter(np.where(valid, flux*vel, 0), sigma)
            smoothed = np.divide(sv, sf, out=np.full_like(sv, np.nan), where=sf>0)
            line_maps[line] = (sample(smoothed,wcs,twcs,target.shape), sample(evel,wcs,twcs,target.shape),
                               sample(flux,wcs,twcs,target.shape), sample(eflux,wcs,twcs,target.shape))
    yy,xx=np.indices(target.shape,dtype=float); ra,dec=twcs.pixel_to_world_values(xx,yy)
    cra,cdec=freeze["center_icrs_deg"]
    east=(ra-cra)*math.cos(math.radians(cdec))*3600; north=(dec-cdec)*3600
    pa=math.radians(freeze["position_angle_deg_east_of_north"])
    major=east*math.sin(pa)+north*math.cos(pa); minor=-east*math.cos(pa)+north*math.sin(pa)
    disky=minor/math.cos(math.radians(freeze["inclination_deg"])); radius=np.hypot(major,disky)
    theta=np.arctan2(disky,major)
    wedge=np.abs(np.sin(theta))<=math.sin(math.radians(freeze["major_axis_half_wedge_deg"]))
    beam_pix=max(1,int(math.ceil(beam/(abs(float(header["CDELT1"]))*3600))))
    independent=(xx.astype(int)%beam_pix==0)&(yy.astype(int)%beam_pix==0)
    rows=[]; edges=freeze["radial_edges_arcsec"]
    for line,(vel,evel,flux,eflux) in line_maps.items():
        mask=wedge&independent&np.isfinite(vel)&np.isfinite(evel)&(evel>0)&(evel<=10)&np.isfinite(flux)&np.isfinite(eflux)&(eflux>0)&(flux/eflux>=5)
        z=(vref+vel)/C; ez=evel/C
        raw=[]
        for ann,(lo,hi) in enumerate(zip(edges[:-1],edges[1:])):
            ring=mask&(radius>=lo)&(radius<hi); plus=ring&(major>0); minus=ring&(major<0)
            if min(plus.sum(),minus.sum())<3: continue
            zp,ep,npixp=side_mean(z,ez,plus); zm,em,npixm=side_mean(z,ez,minus)
            logg=.5*(math.log1p(zp)+math.log1p(zm)); elog=.5*math.hypot(ep/(1+zp),em/(1+zm))
            raw.append((ann,(lo+hi)/2,logg,elog,npixp,npixm))
        if not raw or raw[0][0]!=0: continue
        ref=raw[0]
        for ann,rmid,logg,elog,npixp,npixm in raw[1:]:
            rows.append({"line":line,"annulus":ann,"r_mid_arcsec":rmid,"delta_common_km_s":(logg-ref[2])*C,
                         "sigma_common_km_s":math.hypot(elog,ref[3])*C,"n_plus":npixp,"n_minus":npixm})
    frame=pd.DataFrame(rows)
    ha=frame[frame.line.eq("HA6562")][["annulus","delta_common_km_s","sigma_common_km_s"]].rename(
        columns={"delta_common_km_s":"ha","sigma_common_km_s":"eha"})
    joined=frame.merge(ha,on="annulus")
    control=joined[~joined.line.eq("HA6562")].copy()
    control["difference_from_halpha_km_s"]=control.delta_common_km_s-control.ha
    control["sigma_difference_km_s"]=np.hypot(control.sigma_common_km_s,control.eha)
    stat=float(np.sum((control.difference_from_halpha_km_s/control.sigma_difference_km_s)**2)); dof=len(control)
    per_line={}
    for line,g in control.groupby("line"):
        x=float(np.sum((g.difference_from_halpha_km_s/g.sigma_difference_km_s)**2))
        per_line[line]={"chi2":x,"dof":len(g),"p":float(chi2.sf(x,len(g)))}
    result={"schema":"ngc4254_optical_line_common_mode_v07","lines":LINES,"n_line_annulus_controls":dof,
            "all_optical_vs_halpha_chi2":stat,"all_optical_vs_halpha_dof":dof,"all_optical_vs_halpha_p":float(chi2.sf(stat,dof)),
            "per_line_vs_halpha":per_line,"optical_line_common_mode_consistent":float(chi2.sf(stat,dof))>=0.01,
            "independent_readout_count":1,"co_comparison_repaired":False,"common_channel_detected":False,
            "claim_boundary":"same-instrument optical line-formation control; not independent multi-readout evidence"}
    frame.to_csv(DATA/"ngc4254_optical_line_common_mode_profile_v07.csv",index=False)
    (DATA/"ngc4254_optical_line_common_mode_v07.json").write_text(json.dumps(result,indent=2)+"\n")
    (ROOT/"reports/ngc4254_optical_line_common_mode_v07.md").write_text(
        "# NGC4254 optical-line common-mode control v07\n\n"
        f"Five MUSE emission-line velocity maps were replayed through the frozen geometry. "
        f"All non-Halpha line-annulus contrasts versus Halpha give `chi2={stat:.2f}/{dof}` "
        f"(`p={result['all_optical_vs_halpha_p']:.4g}`). Optical-line consistency at the "
        f"declared 1% gate is `{result['optical_line_common_mode_consistent']}`.\n\n"
        "These lines share one instrument and reduction family, so agreement would be a line-formation "
        "control rather than independent readout evidence. No CO discrepancy or channel signal is repaired.\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__": main()
