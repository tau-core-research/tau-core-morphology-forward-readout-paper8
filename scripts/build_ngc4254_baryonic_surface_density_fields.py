#!/usr/bin/env python3
"""Build source-frozen NGC4254 baryonic surface-density fields on the VIVA grid."""

from __future__ import annotations

import json, math
from pathlib import Path
import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import map_coordinates

ROOT=Path(__file__).resolve().parents[1]; EXT=ROOT/'data/external/literature/ngc4254_phangs_tracer_velocity'; DATA=ROOT/'data/derived'
INC=34.4; PA=68.1; RA0=184.7067; DEC0=14.4168; DIST_MPC=13.1
BMAJ=0.010473*3600; BMIN=0.0091517*3600

def sample(a,w,tw,shape):
    y,x=np.indices(shape,float); ra,dec=tw.pixel_to_world_values(x,y); sx,sy=w.world_to_pixel_values(ra,dec)
    return map_coordinates(a,[sy,sx],order=1,mode='constant',cval=np.nan)

def main():
    with fits.open(EXT/'ngc4254.viva.mom0.fits') as h:
        hh=h[0].header.copy(); hh['CUNIT1']=hh['CUNIT2']='deg'; hi=np.asarray(h[0].data,float); hw=WCS(hh,naxis=2)
    with fits.open(EXT/'NGC4254.stellar.fits') as h: star=sample(np.asarray(h[0].data,float),WCS(h[0].header,naxis=2),hw,hi.shape)
    cp=next(EXT.glob('*co21_broad_mom0.fits'))
    with fits.open(cp) as h: co=sample(np.squeeze(np.asarray(h[0].data,float)),WCS(h[0].header,naxis=2),hw,hi.shape)
    ci=math.cos(math.radians(INC))
    sigma_star=np.clip(star,0,None)*280.0*ci
    sigma_h2=np.clip(co,0,None)*(4.35/0.65)*ci
    jy_to_k=1.222e6/(1.420405752**2*BMAJ*BMIN)
    sigma_hi=np.clip(hi,0,None)*jy_to_k*0.0199*ci
    y,x=np.indices(hi.shape,float); ra,dec=hw.pixel_to_world_values(x,y)
    east=(ra-RA0)*math.cos(math.radians(DEC0))*3600; north=(dec-DEC0)*3600; p=math.radians(PA)
    major=east*math.sin(p)+north*math.cos(p); minor=-east*math.cos(p)+north*math.sin(p); radius=np.hypot(major,minor/ci)
    valid=np.isfinite(sigma_star)&np.isfinite(sigma_h2)&np.isfinite(sigma_hi)&(hi>0)
    edges=np.arange(0,181,15); rows=[]
    for lo,high in zip(edges[:-1],edges[1:]):
        q=valid&(radius>=lo)&(radius<high)
        if q.sum()==0: continue
        rows.append({'radius_arcsec':(lo+high)/2,'radius_kpc':(lo+high)/2*DIST_MPC*1e3/206265,
          'n_pixels':int(q.sum()),'sigma_star_msun_pc2':float(np.nanmedian(sigma_star[q])),
          'sigma_h2_msun_pc2':float(np.nanmedian(sigma_h2[q])),'sigma_hi_msun_pc2':float(np.nanmedian(sigma_hi[q])),
          'sigma_baryon_msun_pc2':float(np.nanmedian((sigma_star+sigma_h2+sigma_hi)[q]))})
    pd.DataFrame(rows).to_csv(DATA/'ngc4254_baryonic_surface_density_profile_v01.csv',index=False)
    fits.HDUList([fits.PrimaryHDU(),fits.ImageHDU(sigma_star.astype('f4'),hh,name='SIGMA_STAR'),fits.ImageHDU(sigma_h2.astype('f4'),hh,name='SIGMA_H2'),fits.ImageHDU(sigma_hi.astype('f4'),hh,name='SIGMA_HI')]).writeto(DATA/'ngc4254_baryonic_surface_density_fields_v01.fits',overwrite=True)
    result={'schema':'ngc4254_baryonic_surface_density_fields_v01','status':'NGC4254_BARYONIC_SURFACE_DENSITY_FIELDS_BUILT_GRAVITY_NOT_YET_SOLVED','distance_mpc':DIST_MPC,'inclination_deg':INC,'stellar_conversion':'Sigma_star=280 I_3.6 cos(i), fixed M/L convention','molecular_conversion':'Sigma_H2=(4.35/0.65) I_CO21 cos(i)','atomic_conversion':f'Sigma_HI=0.0199*{jy_to_k:.6g}*I_JyBeam_kms*cos(i)','hi_beam_arcsec':[BMAJ,BMIN],'n_radial_bins':len(rows),'gravity_field_solved':False,'claim_boundary':'surface-density construction with fixed conversions; no dark discrepancy or Tau attribution'}
    (DATA/'ngc4254_baryonic_surface_density_fields_v01.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],len(rows))
if __name__=='__main__': main()
