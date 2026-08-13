#!/usr/bin/env python3
"""Score cross-transition agreement of four SDP.81 q1 path centroids."""

import itertools, json
from pathlib import Path
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
import astropy.units as u
from score_sdp81_q1_multipath_spectra import aperture_spectrum

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data/derived'; C=299792.458
FILES=[ROOT/'data/external/literature/sdp81_multipath_channel/SDP81_Band4_ReferenceImages_z3.042/SDP.81.Band4.CO_smooth_z3.042.fits',ROOT/'data/external/literature/sdp81_multipath_channel/SDP81_Band6_ReferenceImages/SDP81_9exec.co87.R1uvtaper1000klambda.fits']

def centroid(v,f): return float(np.sum(v*f)/np.sum(f)) if np.sum(f)>0 else np.nan
def cosine(a,b):
 a=a-np.mean(a);b=b-np.mean(b);return float(a@b/np.sqrt((a@a)*(b@b)))

def main():
 freeze=json.loads((DATA/'sdp81_q1_cross_transition_rank_freeze_v01.json').read_text())
 op=json.loads((DATA/'sdp81_lens_operator_freeze_v01.json').read_text()); geo=json.loads((DATA/'sdp81_lens_operator_geometry_validation_v01.json').read_text())
 g=op['coordinates']['image_G_icrs_j2000'];gc=SkyCoord(g['ra_hms'],g['dec_dms'],unit=(u.hourangle,u.deg),frame='icrs');pos=geo['image_positions_arcsec_relative_to_G']['q1']
 cubes=[]
 for p in FILES:
  with fits.open(p,memmap=True) as h:
   cube=np.squeeze(np.asarray(h[0].data,float));hd=h[0].header.copy()
  i=np.arange(cube.shape[0]);freq=hd['CRVAL3']+(i+1-hd['CRPIX3'])*hd['CDELT3'];vel=C*(1-freq/hd['RESTFRQ']);cubes.append((cube,hd,vel))
 runs=[]
 for radius in freeze['aperture_sensitivity_arcsec']:
  for dx in freeze['registration_sensitivity_mas']:
   for dy in freeze['registration_sensitivity_mas']:
    vectors=[]
    for cube,hd,vel in cubes:
     values=[]
     for x,y in pos:
      ra=gc.ra.deg-(x+dx/1000)/(3600*np.cos(gc.dec.radian));dec=gc.dec.deg+(y+dy/1000)/3600
      spec,_=aperture_spectrum(cube,hd,ra,dec,radius);values.append(centroid(vel[46:52],spec[46:52]))
     vectors.append(np.asarray(values))
    valid=all(np.all(np.isfinite(x)) for x in vectors)
    score=cosine(*vectors) if valid else None
    runs.append({'radius_arcsec':radius,'dx_mas':dx,'dy_mas':dy,'co54_centroids_km_s':vectors[0].tolist(),'co87_centroids_km_s':vectors[1].tolist(),'centered_path_cosine':score})
 nominal=next(x for x in runs if x['radius_arcsec']==.12 and x['dx_mas']==0 and x['dy_mas']==0)
 a=np.asarray(nominal['co54_centroids_km_s']);b=np.asarray(nominal['co87_centroids_km_s']);obs=nominal['centered_path_cosine']
 null=[cosine(a,b[list(p)]) for p in itertools.permutations(range(4))]
 pval=float(np.mean(np.abs(null)>=abs(obs)))
 scores=[x['centered_path_cosine'] for x in runs if x['centered_path_cosine'] is not None]
 result={'schema':'sdp81_q1_cross_transition_rank_v02','nominal':nominal,'path_label_permutations':len(null),
  'runs':runs,
  'two_sided_permutation_p':pval,'sensitivity_cosine_range':[float(min(scores)),float(max(scores))],
  'sign_stable_across_all_sensitivity_runs':all(np.sign(x)==np.sign(obs) for x in scores),
  'projected_cross_transition_rank_promoted':False,'reason':'four paths only; differential magnification/lens nuisance operator unclosed',
  'mode_selective_channel_detected':False,'effective_time_readout_detected':False,
  'claim_boundary':'two-transition same-source multipath pattern diagnostic; not physical K_Gamma identification'}
 (DATA/'sdp81_q1_cross_transition_rank_v02.json').write_text(json.dumps(result,indent=2)+'\n')
 (ROOT/'reports/sdp81_q1_cross_transition_rank_v02.md').write_text(
  '# SDP.81 q1 cross-transition rank diagnostic v02\n\n'
  f"The centered four-path centroid vectors have nominal cosine `{obs:.3f}`. The exact 24-label two-sided permutation value is `{pval:.3f}`; aperture/registration sensitivity spans `{min(scores):.3f}` to `{max(scores):.3f}`, with stable sign `{result['sign_stable_across_all_sensitivity_runs']}`.\n\n"
  'With four paths and no closed differential-magnification/lens nuisance operator, projected cross-transition rank is not promoted and no mode-selective channel is detected.\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
