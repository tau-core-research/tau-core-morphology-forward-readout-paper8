#!/usr/bin/env python3
"""Test path-dependent spectral centroids for the SDP.81 q1 quadruple."""

import json
from pathlib import Path

import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
import astropy.units as u

from score_sdp81_q1_multipath_spectra import aperture_spectrum


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
CUBE = ROOT / "data/external/literature/sdp81_multipath_channel/SDP81_Band6_ReferenceImages/SDP81_9exec.co87.R1uvtaper1000klambda.fits"
C = 299792.458


def centroid(axis, flux):
    scale = np.sum(flux)
    return float(np.sum(axis * flux) / scale) if np.isfinite(scale) and scale > 0 else np.nan


def main():
    freeze = json.loads((DATA / "sdp81_lens_operator_freeze_v01.json").read_text())
    geometry = json.loads((DATA / "sdp81_lens_operator_geometry_validation_v01.json").read_text())
    g = freeze["coordinates"]["image_G_icrs_j2000"]
    gc = SkyCoord(g["ra_hms"], g["dec_dms"], unit=(u.hourangle,u.deg), frame="icrs")
    positions = geometry["image_positions_arcsec_relative_to_G"]["q1"]
    with fits.open(CUBE, memmap=True) as h:
        cube=np.squeeze(np.asarray(h[0].data,float)); header=h[0].header
    channel=np.arange(cube.shape[0]); freq=header["CRVAL3"]+(channel+1-header["CRPIX3"])*header["CDELT3"]
    velocity=C*(1-freq/header["RESTFRQ"])
    runs=[]; nominal_spectra=None
    for radius in [0.08,0.10,0.12,0.15]:
      for dx in [-20.,0.,20.]:
       for dy in [-20.,0.,20.]:
        spectra=[]
        for x,y in positions:
            ra=gc.ra.deg-(x+dx/1000)/(3600*np.cos(gc.dec.radian)); dec=gc.dec.deg+(y+dy/1000)/3600
            s,_=aperture_spectrum(cube,header,ra,dec,radius); spectra.append(s)
        spectra=np.asarray(spectra)
        if radius==.12 and dx==0 and dy==0: nominal_spectra=spectra.copy()
        values=np.array([centroid(velocity[46:52],s[46:52]) for s in spectra])
        runs.append({"radius_arcsec":radius,"dx_mas":dx,"dy_mas":dy,
                     "path_centroids_radio_lsrk_km_s":values.tolist(),
                     "centroid_path_std_km_s":float(np.nanstd(values,ddof=1)),
                     "centroid_path_range_km_s":float(np.nanmax(values)-np.nanmin(values))})
    nominal=next(x for x in runs if x["radius_arcsec"]==.12 and x["dx_mas"]==0 and x["dy_mas"]==0)
    rolling=[]
    for start in range(cube.shape[0]-5):
        vals=np.array([centroid(velocity[start:start+6],s[start:start+6]) for s in nominal_spectra])
        if np.all(np.isfinite(vals)):
            rolling.append(float(np.std(vals,ddof=1)))
    endpoint=nominal["centroid_path_std_km_s"]
    tail=float(np.mean(np.asarray(rolling)>=endpoint))
    result={"schema":"sdp81_q1_multipath_centroid_v02","path_count":4,
            "target_channels_one_based":[47,52],"nominal":nominal,
            "registration_aperture_centroid_std_range_km_s":[float(min(x["centroid_path_std_km_s"] for x in runs)),float(max(x["centroid_path_std_km_s"] for x in runs))],
            "rolling_six_channel_finite_windows":len(rolling),"empirical_upper_tail_fraction":tail,
            "frequency_axis":"radio velocity from FITS FREQ/RESTFRQ in LSRK","constant_magnification_removed_by_centroid":True,
            "differential_magnification_line_shape_control_complete":False,"lens_family_null_complete":False,
            "multipath_common_channel_detected":False,"effective_time_readout_detected":False,
            "claim_boundary":"same-source multipath centroid diagnostic; lens mapping, beam covariance, and differential magnification remain open"}
    (DATA/"sdp81_q1_multipath_centroid_v02.json").write_text(json.dumps(result,indent=2)+"\n")
    (ROOT/"reports/sdp81_q1_multipath_centroid_v02.md").write_text(
        "# SDP.81 q1 multipath centroid diagnostic v02\n\n"
        f"The four nominal path centroids have standard deviation `{endpoint:.2f} km/s` "
        f"and range `{nominal['centroid_path_range_km_s']:.2f} km/s`. Across aperture and "
        f"`+/-20 mas` registration variants the standard deviation spans "
        f"`{result['registration_aperture_centroid_std_range_km_s'][0]:.2f}-"
        f"{result['registration_aperture_centroid_std_range_km_s'][1]:.2f} km/s`. Its empirical "
        f"upper-tail fraction among finite rolling six-channel windows is `{tail:.3f}`.\n\n"
        "This is not a multipath channel/time detection. Differential magnification of a resolved "
        "velocity field, correlated beam noise, and lens-family alternatives remain unclosed.\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__": main()
