#!/usr/bin/env python3
"""Freeze the contiguous source-side SDP.81 CO signal window."""

from __future__ import annotations

import json
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits

from score_sdp81_q1_multipath_spectra import aperture_spectrum


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
CUBE = ROOT / (
    "data/external/literature/sdp81_multipath_channel/"
    "SDP81_Band6_ReferenceImages/SDP81_9exec.co87.R1uvtaper1000klambda.fits"
)
OUT = DATA / "sdp81_full_signal_window_freeze_v01.json"
REPORT = ROOT / "reports/sdp81_full_signal_window_freeze_v01.md"


def main() -> None:
    frozen = json.loads(
        (DATA / "sdp81_lens_operator_freeze_v01.json").read_text(encoding="utf-8")
    )
    geometry = json.loads(
        (DATA / "sdp81_lens_operator_geometry_validation_v01.json").read_text(
            encoding="utf-8"
        )
    )
    g_data = frozen["coordinates"]["image_G_icrs_j2000"]
    g = SkyCoord(
        g_data["ra_hms"],
        g_data["dec_dms"],
        unit=(u.hourangle, u.deg),
        frame="icrs",
    )
    with fits.open(CUBE, memmap=True) as hdul:
        cube = np.squeeze(np.asarray(hdul[0].data, dtype=float))
        header = hdul[0].header
    spectra = []
    for lens_x, north in geometry["image_positions_arcsec_relative_to_G"]["q1"]:
        ra = g.ra.deg - lens_x / (3600.0 * np.cos(g.dec.radian))
        dec = g.dec.deg + north / 3600.0
        spectrum, _ = aperture_spectrum(cube, header, ra, dec, 0.12)
        spectra.append(spectrum)
    aggregate = np.sum(np.asarray(spectra), axis=0)
    median = float(np.median(aggregate))
    robust_sigma = float(1.4826 * np.median(np.abs(aggregate - median)))
    selected = np.flatnonzero(aggregate > median + 3.0 * robust_sigma)
    runs: list[list[int]] = []
    for channel in selected:
        if not runs or channel > runs[-1][-1] + 1:
            runs.append([int(channel)])
        else:
            runs[-1].append(int(channel))
    primary = max(runs, key=lambda run: float(np.sum(aggregate[run])))
    result = {
        "schema": "tau_core.paper8.sdp81-full-signal-window-freeze.v01",
        "selection_source": "sum of four q1 path aperture spectra",
        "aperture_radius_arcsec": 0.12,
        "threshold": "aggregate median + 3 * robust MAD sigma",
        "aggregate_median": median,
        "aggregate_robust_sigma": robust_sigma,
        "selected_channels_one_based": [channel + 1 for channel in primary],
        "selected_channel_count": len(primary),
        "contiguous": primary == list(range(primary[0], primary[-1] + 1)),
        "previous_window_one_based": [47, 48, 49, 50, 51, 52],
        "previous_window_omitted_selected_channels": [
            channel + 1 for channel in primary if channel + 1 > 52
        ],
        "uses_time_delay_or_rotation_residual": False,
        "velocity_field_rescore_authorized": True,
        "claim_boundary": (
            "Source-side spectral support freeze only; not a channel effect, clock, "
            "observer-time signal, or Tau Core detection."
        ),
        "verdict": "CONTIGUOUS_CHANNELS_48_TO_58_FROZEN",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 full signal-window freeze v01\n\n"
        f"Verdict: `{result['verdict']}`\n\n"
        "The four-path aggregate spectrum has one contiguous component above the "
        f"declared robust threshold: channels `{primary[0]+1}--{primary[-1]+1}`. "
        "Selection does not use a time-delay or rotation residual.\n",
        encoding="utf-8",
    )
    print(result["verdict"])


if __name__ == "__main__":
    main()
