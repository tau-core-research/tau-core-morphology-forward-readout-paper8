#!/usr/bin/env python3
"""Score source-matched q1 spectra across the four SDP.81 lens paths."""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
import astropy.units as u


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
CUBE = ROOT / (
    "data/external/literature/sdp81_multipath_channel/SDP81_Band6_ReferenceImages/"
    "SDP81_9exec.co87.R1uvtaper1000klambda.fits"
)
OUT = DATA / "sdp81_q1_multipath_spectral_score_v01.json"
REPORT = ROOT / "reports/sdp81_q1_multipath_spectral_score_v01.md"


def aperture_spectrum(cube, header, ra_deg, dec_deg, radius_arcsec):
    cos_dec = np.cos(np.deg2rad(dec_deg))
    x = (ra_deg - header["CRVAL1"]) * cos_dec * 3600.0
    y = (dec_deg - header["CRVAL2"]) * 3600.0
    xpix = x / (header["CDELT1"] * 3600.0) + header["CRPIX1"] - 1
    ypix = y / (header["CDELT2"] * 3600.0) + header["CRPIX2"] - 1
    yy, xx = np.indices(cube.shape[1:])
    scale_x = abs(header["CDELT1"] * 3600.0)
    scale_y = abs(header["CDELT2"] * 3600.0)
    mask = ((xx - xpix) * scale_x) ** 2 + ((yy - ypix) * scale_y) ** 2 <= radius_arcsec**2
    return np.nanmean(cube[:, mask], axis=1), int(mask.sum())


def main() -> None:
    freeze = json.loads((DATA / "sdp81_lens_operator_freeze_v01.json").read_text())
    geometry = json.loads(
        (DATA / "sdp81_lens_operator_geometry_validation_v01.json").read_text()
    )
    g = freeze["coordinates"]["image_G_icrs_j2000"]
    g_coord = SkyCoord(g["ra_hms"], g["dec_dms"], unit=(u.hourangle, u.deg), frame="icrs")
    q1 = geometry["image_positions_arcsec_relative_to_G"]["q1"]
    with fits.open(CUBE, memmap=True) as hdul:
        cube = np.squeeze(hdul[0].data).astype(float)
        header = hdul[0].header

    radii = [0.08, 0.10, 0.12, 0.15]
    registrations_mas = [-20.0, 0.0, 20.0]
    runs = []
    nominal_full_spectra = None
    for radius in radii:
        for dx_mas in registrations_mas:
            for dy_mas in registrations_mas:
                spectra = []
                npix = None
                for x_arcsec, y_arcsec in q1:
                    # The published image x-axis increases to the right, opposite ICRS RA.
                    ra = g_coord.ra.deg - (x_arcsec + dx_mas / 1000) / (
                        3600 * np.cos(g_coord.dec.radian)
                    )
                    dec = g_coord.dec.deg + (y_arcsec + dy_mas / 1000) / 3600
                    spectrum, npix = aperture_spectrum(cube, header, ra, dec, radius)
                    spectra.append(spectrum)
                spectra = np.asarray(spectra)
                if radius == 0.12 and dx_mas == 0 and dy_mas == 0:
                    nominal_full_spectra = spectra.copy()
                # One-based channels 47--52 are indices 46--51.
                endpoint = spectra[:, 46:52]
                scale = np.sum(endpoint, axis=1)
                valid = np.all(np.isfinite(scale)) and np.all(scale > 0)
                if valid:
                    normalized = endpoint / scale[:, None]
                    pair_rms = [
                        float(np.sqrt(np.mean((normalized[i] - normalized[j]) ** 2)))
                        for i, j in combinations(range(4), 2)
                    ]
                    score = float(np.mean(pair_rms))
                    ch50_spread = float(np.std(normalized[:, 49 - 46], ddof=1))
                else:
                    score = None
                    ch50_spread = None
                runs.append(
                    {
                        "aperture_radius_arcsec": radius,
                        "registration_dx_mas": dx_mas,
                        "registration_dy_mas": dy_mas,
                        "pixels_per_aperture": npix,
                        "all_path_endpoint_flux_positive": bool(valid),
                        "mean_pairwise_normalized_spectral_rms": score,
                        "channel_50_normalized_path_spread": ch50_spread,
                    }
                )
    valid_scores = [r["mean_pairwise_normalized_spectral_rms"] for r in runs if r["mean_pairwise_normalized_spectral_rms"] is not None]
    nominal = next(
        r for r in runs
        if r["aperture_radius_arcsec"] == 0.12
        and r["registration_dx_mas"] == 0
        and r["registration_dy_mas"] == 0
    )
    rolling_scores = []
    for start in range(cube.shape[0] - 5):
        window = nominal_full_spectra[:, start : start + 6]
        scale = np.sum(window, axis=1)
        if np.all(np.isfinite(scale)) and np.all(scale > 0):
            normalized = window / scale[:, None]
            pair_rms = [
                float(np.sqrt(np.mean((normalized[i] - normalized[j]) ** 2)))
                for i, j in combinations(range(4), 2)
            ]
            rolling_scores.append(
                {
                    "channels_one_based": [start + 1, start + 6],
                    "score": float(np.mean(pair_rms)),
                }
            )
    endpoint_score = nominal["mean_pairwise_normalized_spectral_rms"]
    empirical_tail_fraction = float(
        np.mean([item["score"] >= endpoint_score for item in rolling_scores])
    )
    result = {
        "schema": "tau-core.paper8.sdp81-q1-multipath-spectral-score.v01",
        "status": "Q1_MULTIPATH_DIAGNOSTIC_SCORED_SIGNIFICANCE_AND_OPERATOR_NULLS_OPEN",
        "target": "CO(8-7) one-based channels 47--52 from the same q1 source clump",
        "path_count": 4,
        "image_G_icrs_j2000": g,
        "image_x_to_icrs_ra_convention": "delta_RA*cos(dec) = -x",
        "nominal": nominal,
        "sensitivity_score_range": [float(min(valid_scores)), float(max(valid_scores))],
        "n_sensitivity_runs": len(runs),
        "rolling_six_channel_positive_flux_windows": len(rolling_scores),
        "published_endpoint_empirical_upper_tail_fraction": empirical_tail_fraction,
        "rolling_window_null": rolling_scores,
        "runs": runs,
        "lens_magnification_control": "each path spectrum normalized by its six-channel endpoint flux",
        "physical_significance_computed": False,
        "lens_model_family_null_computed": False,
        "channel_origin_identified": False,
        "claim_boundary": (
            "source-matched spectral-shape diagnostic only; beam mixing, correlated noise, "
            "lens-family sensitivity, and perturbed-lens alternatives remain open"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# SDP.81 q1 multipath spectral score\n\n"
        f"Status: `{result['status']}`\n\n"
        "Four image-plane apertures predicted for the same q1 source clump were scored "
        "over the published CO(8-7) channels 47--52. Per-path normalization removes a "
        "constant magnification factor. The nominal mean pairwise normalized spectral "
        f"RMS is `{nominal['mean_pairwise_normalized_spectral_rms']:.6f}`; the aperture "
        f"and +/-20 mas registration sensitivity range is `{min(valid_scores):.6f}` to "
        f"`{max(valid_scores):.6f}`. Against `{len(rolling_scores)}` positive-flux "
        f"six-channel windows, its empirical upper-tail fraction is "
        f"`{empirical_tail_fraction:.3f}`. This is not yet a significant channel residual: "
        "correlated-noise, beam-mixing, and lens-family nulls remain required.\n"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
