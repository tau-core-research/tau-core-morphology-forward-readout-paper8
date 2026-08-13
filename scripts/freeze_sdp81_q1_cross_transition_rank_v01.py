#!/usr/bin/env python3
"""Freeze the SDP.81 q1 CO(5-4)/CO(8-7) cross-transition test."""

import hashlib
import json
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data/derived'
FILES={
 'CO(5-4)':ROOT/'data/external/literature/sdp81_multipath_channel/SDP81_Band4_ReferenceImages_z3.042/SDP.81.Band4.CO_smooth_z3.042.fits',
 'CO(8-7)':ROOT/'data/external/literature/sdp81_multipath_channel/SDP81_Band6_ReferenceImages/SDP81_9exec.co87.R1uvtaper1000klambda.fits'}


def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()


def main():
 result={'schema':'sdp81_q1_cross_transition_rank_freeze_v01','readouts':['CO(5-4)','CO(8-7)'],'path_count':4,
  'cube_sha256':{k:sha(v) for k,v in FILES.items()},'shared_wcs_shape':[672,672],
  'spectral_frame':'LSRK','velocity_convention':'radio','channels_one_based':[47,52],
  'velocity_window_km_s':[-34.0,71.0],'nominal_aperture_radius_arcsec':0.12,
  'aperture_sensitivity_arcsec':[0.08,0.10,0.12,0.15],'registration_sensitivity_mas':[-20,0,20],
  'statistic':'center each four-path centroid vector; compare cross-transition cosine/correlation and permutation path-label null',
  'constant_transition_magnification_removed':True,'differential_magnification_model_complete':False,
  'cube_flux_opened_during_freeze':False,'freeze_complete':True,
  'claim_boundary':'metadata/geometry/statistic freeze only; no cross-transition endpoint score'}
 (DATA/'sdp81_q1_cross_transition_rank_freeze_v01.json').write_text(json.dumps(result,indent=2)+'\n')
 (ROOT/'reports/sdp81_q1_cross_transition_rank_freeze_v01.md').write_text(
 '# SDP.81 q1 cross-transition rank freeze v01\n\nThe CO(5-4) and CO(8-7) cubes share the same image grid, LSRK radio-velocity grid, and exact channels 47--52 velocity window (`-34` to `+71 km/s`). Four q1 paths, a `0.12 arcsec` nominal aperture, the existing aperture/registration sensitivity suite, centered path-centroid vectors, and a path-label permutation null are frozen before cube flux is opened.\n')


if __name__=='__main__': main()
