#!/usr/bin/env python3
"""Test one- versus two-component q1 source spectra on the frozen full window."""

from __future__ import annotations

import json
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
from scipy.optimize import lsq_linear
from scipy.signal import find_peaks

from score_sdp81_q1_multipath_spectra import aperture_spectrum


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
CUBE = ROOT / "data/external/literature/sdp81_multipath_channel/SDP81_Band6_ReferenceImages/SDP81_9exec.co87.R1uvtaper1000klambda.fits"
OUT = DATA / "sdp81_two_component_spectral_source_v01.json"
REPORT = ROOT / "reports/sdp81_two_component_spectral_source_v01.md"
CHANNELS = np.arange(47, 58)


def fit_model(spectra: np.ndarray, centers: list[int], sigma_channels: float) -> dict:
    profiles = np.column_stack(
        [np.exp(-0.5 * ((CHANNELS - center) / sigma_channels) ** 2) for center in centers]
    )
    blocks = []
    target = spectra[:, CHANNELS].ravel()
    path_count = spectra.shape[0]
    for path in range(path_count):
        block = np.zeros((len(CHANNELS), path_count * (len(centers) + 1)))
        first = path * (len(centers) + 1)
        block[:, first : first + len(centers)] = profiles
        block[:, first + len(centers)] = 1.0
        blocks.append(block)
    matrix = np.vstack(blocks)
    lower = np.full(matrix.shape[1], -np.inf)
    for path in range(path_count):
        first = path * (len(centers) + 1)
        lower[first : first + len(centers)] = 0.0
    solution = lsq_linear(matrix, target, bounds=(lower, np.inf)).x
    residual = target - matrix @ solution
    rss = float(residual @ residual)
    n = len(target)
    k = len(solution)
    bic = float(n * np.log(rss / n) + k * np.log(n))
    return {"rss": rss, "bic": bic, "parameter_count": k, "solution": solution.tolist()}


def main() -> None:
    frozen = json.loads((DATA / "sdp81_lens_operator_freeze_v01.json").read_text())
    geometry = json.loads((DATA / "sdp81_lens_operator_geometry_validation_v01.json").read_text())
    g0 = frozen["coordinates"]["image_G_icrs_j2000"]
    g = SkyCoord(g0["ra_hms"], g0["dec_dms"], unit=(u.hourangle, u.deg))
    with fits.open(CUBE, memmap=True) as h:
        cube = np.squeeze(np.asarray(h[0].data, float))
        header = h[0].header
    spectra = []
    for lens_x, north in geometry["image_positions_arcsec_relative_to_G"]["q1"]:
        spectrum, _ = aperture_spectrum(
            cube, header,
            g.ra.deg - lens_x / (3600 * np.cos(g.dec.radian)),
            g.dec.deg + north / 3600,
            0.12,
        )
        spectra.append(spectrum)
    spectra = np.asarray(spectra)
    aggregate = spectra[:, CHANNELS].sum(axis=0)
    peak_indices = find_peaks(aggregate)[0]
    ranked = sorted(peak_indices, key=lambda index: aggregate[index], reverse=True)
    centers = sorted(int(CHANNELS[index]) for index in ranked[:2])
    one_center = [int(CHANNELS[int(np.argmax(aggregate))])]
    one = fit_model(spectra, one_center, 1.5)
    two = fit_model(spectra, centers, 1.5)
    delta_bic = one["bic"] - two["bic"]
    promoted = delta_bic > 6.0
    result = {
        "schema": "tau_core.paper8.sdp81-two-component-spectral-source.v01",
        "channels_one_based": [int(channel + 1) for channel in CHANNELS],
        "aggregate_local_maxima_one_based": [int(CHANNELS[index] + 1) for index in peak_indices],
        "one_component_center_one_based": [center + 1 for center in one_center],
        "two_component_centers_one_based": [center + 1 for center in centers],
        "profile_sigma_channels": 1.5,
        "one_component": {key: value for key, value in one.items() if key != "solution"},
        "two_component": {key: value for key, value in two.items() if key != "solution"},
        "delta_bic_one_minus_two": delta_bic,
        "two_component_spectral_structure_promoted": promoted,
        "velocity_field_or_clock_identified": False,
        "time_score_authorized": False,
        "verdict": "TWO_COMPONENT_SOURCE_SPECTRUM_SUPPORTED" if promoted else "SECOND_SPECTRAL_COMPONENT_NOT_SUPPORTED",
        "claim_boundary": "Aperture-spectrum complexity audit; not a spatial velocity field, body clock, observer-time effect, or Tau detection.",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# SDP.81 two-component spectral-source audit v01\n\n"
        f"Verdict: `{result['verdict']}`\n\nThe aggregate local maxima are channels "
        f"`{result['aggregate_local_maxima_one_based']}`. The one-minus-two component "
        f"BIC difference is `{delta_bic:.3f}`.\n\nThis establishes only spectral "
        "complexity, not a source velocity field or clock.\n"
    )
    print(result["verdict"])


if __name__ == "__main__":
    main()
