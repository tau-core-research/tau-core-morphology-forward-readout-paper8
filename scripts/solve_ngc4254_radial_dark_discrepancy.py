#!/usr/bin/env python3
"""Solve the coarse radial NGC4254 baryonic gravity and dark discrepancy."""

from __future__ import annotations

import json, math
from pathlib import Path
import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.signal import fftconvolve

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data/derived'; EXT=ROOT/'data/external/literature/ngc4254_phangs_tracer_velocity'
G=4.30091e-3; DIST=13.1; INC=34.4; PA=68.1; RA0=184.7067; DEC0=14.4168; PIX_ARCSEC=5.0

def clean_wcs(header):
    h=header.copy(); h['CUNIT1']=h['CUNIT2']='deg'; return WCS(h,naxis=2)

def sample(a,w,tw,shape):
    y,x=np.indices(shape,float); ra,dec=tw.pixel_to_world_values(x,y); sx,sy=w.world_to_pixel_values(ra,dec)
    return map_coordinates(a,[sy,sx],order=1,mode='constant',cval=np.nan)

def gravity_velocity(radius_pc, sigma, scale_star, scale_h2, height_pc):
    n=501; pix_pc=DIST*1e6*PIX_ARCSEC/206265; axis=(np.arange(n)-n//2)*pix_pc
    yy,xx=np.meshgrid(axis,axis,indexing='ij'); rr=np.hypot(xx,yy)
    total=np.interp(rr,radius_pc,sigma[:,0]*scale_star+sigma[:,1]*scale_h2+sigma[:,2],left=sigma[0].sum(),right=0)
    mass=total*pix_pc**2
    denom=(xx**2+yy**2+height_pc**2)**1.5; kx=np.divide(G*xx,denom,out=np.zeros_like(xx),where=denom>0)
    gx=fftconvolve(mass,kx,mode='same')
    center=n//2; sample_x=np.clip(np.rint(radius_pc/pix_pc).astype(int)+center,0,n-1)
    acceleration=np.abs(gx[center,sample_x])
    return np.sqrt(np.maximum(radius_pc*acceleration,0))

def main():
    profile=pd.read_csv(DATA/'ngc4254_baryonic_surface_density_profile_v01.csv')
    radius_pc=profile.radius_kpc.to_numpy()*1000
    sigma=profile[['sigma_star_msun_pc2','sigma_h2_msun_pc2','sigma_hi_msun_pc2']].to_numpy()
    with fits.open(EXT/'ngc4254.viva.mom0.fits') as h:
        hh=h[0].header.copy(); hw=clean_wcs(hh); shape=h[0].data.shape
    with fits.open(DATA/'ngc4254_phangs_common_tracer_velocity_field_v01.fits') as h:
        velocity=sample(np.asarray(h['COMMON_VEL'].data,float),WCS(h['COMMON_VEL'].header,naxis=2),hw,shape)
        support=sample(np.asarray(h['COMMON_MASK'].data,float),WCS(h['COMMON_MASK'].header,naxis=2),hw,shape)>0.5
    velocity=gaussian_filter(np.nan_to_num(velocity,nan=0),3.0)/np.maximum(gaussian_filter(np.isfinite(velocity).astype(float),3.0),1e-6)
    y,x=np.indices(shape,float); ra,dec=hw.pixel_to_world_values(x,y); east=(ra-RA0)*math.cos(math.radians(DEC0))*3600; north=(dec-DEC0)*3600; p=math.radians(PA)
    major=east*math.sin(p)+north*math.cos(p); minor=-east*math.cos(p)+north*math.sin(p); theta=np.arctan2(minor/math.cos(math.radians(INC)),major); radius=np.hypot(major,minor/math.cos(math.radians(INC)))
    usable=support&np.isfinite(velocity)&(np.abs(np.cos(theta))>0.5)
    design=np.column_stack([np.ones(usable.sum()),np.cos(theta[usable])]); beta=np.linalg.lstsq(design,velocity[usable],rcond=None)[0]; vsys=float(beta[0])
    vobs=[]; verr=[]
    for r in profile.radius_arcsec:
        q=usable&(radius>=r-7.5)&(radius<r+7.5); c=np.cos(theta[q])*math.sin(math.radians(INC))
        if q.sum()<4 or np.sum(c*c)<=0: vobs.append(np.nan); verr.append(np.nan); continue
        value=np.sum(c*(velocity[q]-vsys))/np.sum(c*c); residual=velocity[q]-vsys-value*c
        vobs.append(abs(value)); verr.append(float(np.std(residual)/math.sqrt(np.sum(c*c))))
    rows=[]
    for ss in (0.7,1.0,1.3):
      for hs in (0.7,1.0,1.3):
       for h in (100,300,600):
        vb=gravity_velocity(radius_pc,sigma,ss,hs,h)
        for i,r in profile.iterrows(): rows.append({'star_scale':ss,'h2_scale':hs,'height_pc':h,'radius_kpc':r.radius_kpc,'vobs_km_s':vobs[i],'vobs_error_km_s':verr[i],'vbar_km_s':vb[i],'dark_discrepancy_ratio':vobs[i]**2/vb[i]**2 if vb[i]>0 else np.nan,'delta_v2_km2_s2':vobs[i]**2-vb[i]**2})
    out=pd.DataFrame(rows); out.to_csv(DATA/'ngc4254_radial_dark_discrepancy_sensitivity_v01.csv',index=False)
    nominal=out[(out.star_scale==1)&(out.h2_scale==1)&(out.height_pc==300)].copy(); nominal.to_csv(DATA/'ngc4254_radial_dark_discrepancy_nominal_v01.csv',index=False)
    outer=nominal[nominal.radius_kpc>=6]
    result={'schema':'ngc4254_radial_dark_discrepancy_v01','status':'NGC4254_RADIAL_DARK_DISCREPANCY_DIAGNOSTIC_SOLVED','systemic_velocity_km_s':vsys,'n_observed_radial_bins':int(nominal.vobs_km_s.notna().sum()),'n_sensitivity_models':27,'outer_nominal_median_ratio':float(outer.dark_discrepancy_ratio.median()),'outer_all_models_ratio_range':[float(out[out.radius_kpc>=6].dark_discrepancy_ratio.quantile(.05)),float(out[out.radius_kpc>=6].dark_discrepancy_ratio.quantile(.95))],'two_dimensional_attribution_allowed':False,'tau_morphology_detected':False,'channel_detected':False,'limitations':['axisymmetric gravity from azimuthal median surface-density profiles','VIVA-beam radial resolution only','fixed distance and inclination','formal tilted-ring errors omit full inter-ring covariance'],'claim_boundary':'coarse radial fixed-convention diagnostic; not a halo comparison, 2D morphology attribution, or Tau/channel detection'}
    (DATA/'ngc4254_radial_dark_discrepancy_v01.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'reports/ngc4254_radial_dark_discrepancy_v01.md').write_text(f"# NGC4254 radial dark-discrepancy diagnostic\n\nStatus: `{result['status']}`\n\nThe nominal outer (`R>=6 kpc`) median ratio is `D=v_obs^2/v_bar^2={result['outer_nominal_median_ratio']:.3f}`. Across 27 frozen stellar-scale, molecular-conversion, and disk-height models, the outer 5--95% range is `{result['outer_all_models_ratio_range'][0]:.3f}--{result['outer_all_models_ratio_range'][1]:.3f}`. The baryonic model therefore does not remove the radial discrepancy. The coarse radial product identifies the target conventionally assigned to dark matter; it cannot attribute that target to Tau Core morphology or channel response.\n")
    print(result)
if __name__=='__main__': main()
