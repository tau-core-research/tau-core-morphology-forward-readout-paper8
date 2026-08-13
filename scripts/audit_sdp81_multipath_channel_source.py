#!/usr/bin/env python3
"""Freeze and audit the public SDP.81 multipath CO cube."""
from __future__ import annotations
import hashlib,json,math
from pathlib import Path
import numpy as np
from astropy.io import fits
ROOT=Path(__file__).resolve().parents[1];EXT=ROOT/'data/external/literature/sdp81_multipath_channel';DATA=ROOT/'data/derived';REPORT=ROOT/'reports/sdp81_multipath_channel_source_audit_v01.md'
ARCH=EXT/'SDP81_Band4_ReferenceImages_z3.042.tgz';CUBE=EXT/'SDP81_Band4_ReferenceImages_z3.042/SDP.81.Band4.CO_smooth_z3.042.fits';MOM0=EXT/'SDP81_Band4_ReferenceImages_z3.042/SDP.81.Band4.CO_smooth.mom0_z3.042.fits'
B6_ARCH=EXT/'SDP81_Band6_ReferenceImages.tgz';B6_CUBE=EXT/'SDP81_Band6_ReferenceImages/SDP81_9exec.co87.R1uvtaper1000klambda.fits';B6_CONT=EXT/'SDP81_Band6_ReferenceImages/SDP81_band6_9exec.contR1.image.fits'
B7_ARCH=EXT/'SDP81_Band7_ReferenceImages.tgz';B7_CONT=EXT/'SDP81_Band7_ReferenceImages/SDP81_band7_11exec.contR1.image.fits'
def sha(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 with fits.open(CUBE,memmap=True) as h:
  x=h[0];shape=list(x.data.shape);hdr=x.header;beam=[float(hdr['BMAJ'])*3600,float(hdr['BMIN'])*3600];freq=float(hdr['CRVAL3'])+np.arange(shape[1])*float(hdr['CDELT3']);velocity=299792.458*(float(hdr['RESTFRQ'])-freq)/float(hdr['RESTFRQ'])
 with fits.open(MOM0,memmap=True) as h: finite=np.isfinite(h[0].data); peak=float(np.nanmax(h[0].data)); support=int((finite&(h[0].data>0)).sum())
 with fits.open(B6_CUBE,memmap=True) as h:
  b6shape=list(h[0].data.shape);b6hdr=h[0].header;b6beam=[float(b6hdr['BMAJ'])*3600,float(b6hdr['BMIN'])*3600]
 result={'schema':'sdp81_multipath_channel_source_audit_v01','status':'SDP81_MULTIPATH_DATA_ACQUIRED_OPERATOR_VALIDATION_REQUIRED','source':'SDP.81 / HATLAS J090311.6+003906','source_redshift':3.042,'lens_redshift':0.2999,'preflight_band4':{'line':'CO(5-4)','archive_url':'https://almascience.nrao.edu/almadata/sciver/SDP81Band4/SDP81_Band4_ReferenceImages_z3.042.tgz','archive_md5':'6c4ed2a251aac9ec4a8ddf1fad2d09a2','archive_sha256':sha(ARCH),'cube_sha256':sha(CUBE),'cube_shape':shape,'beam_arcsec':beam,'n_spectral_channels':shape[1],'radio_velocity_range_km_s':[float(velocity.min()),float(velocity.max())],'moment0_positive_pixel_count':support,'moment0_peak':peak},'published_endpoint_band6':{'line':'CO(8-7)','archive_url':'https://bulk.cv.nrao.edu/almadata/sciver/SDP81Band6/SDP81_Band6_ReferenceImages.tgz','archive_sha256':sha(B6_ARCH),'cube_sha256':sha(B6_CUBE),'continuum_sha256':sha(B6_CONT),'cube_shape':b6shape,'beam_arcsec':b6beam,'n_spectral_channels':b6shape[1],'published_channels_of_interest_one_based':[47,48,49,50,51,52]},'lens_registration_band7':{'role':'highest-resolution continuum used for the published smooth lens fit and image-G registration','archive_url':'https://bulk.cv.nrao.edu/almadata/sciver/SDP81Band7/SDP81_Band7_ReferenceImages.tgz','archive_sha256':sha(B7_ARCH),'continuum_sha256':sha(B7_CONT),'line_in_archive':'CO(10-9), not the published CO(8-7) endpoint'},'same_source_multiple_null_paths':True,'pathwise_comparison_allowed':False,'blocker':'image-G WCS registration and published lens operator geometry have not yet been reproduced','forbidden_shortcut':'compare image-plane arc pixels or integrated spectra as if they were identical source elements','claim_boundary':'source-native multipath data acquisition; no channel anomaly, time-readout effect, or Tau detection'}
 (DATA/'sdp81_multipath_channel_source_audit_v01.json').write_text(json.dumps(result,indent=2)+'\n');REPORT.write_text(f"# SDP.81 multipath channel source audit\n\nStatus: `{result['status']}`\n\nThe ALMA source pack now contains the Band-4 CO(5-4) preflight cube, the Band-7 continuum used to constrain the published lens model, and the `{b6shape}` Band-6 CO(8-7) cube containing the published channels 47--52 endpoint. The Band-7 line product is CO(10-9), not CO(8-7). SDP.81 supplies the same source through multiple lensed null paths, but pathwise comparison remains closed until image G is registered in WCS and the frozen lens operator reproduces the published geometry. Image-plane arc differences are not channel residuals.\n");print(result['status'])
if __name__=='__main__':main()
