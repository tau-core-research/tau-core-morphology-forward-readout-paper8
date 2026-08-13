#!/usr/bin/env python3
"""Test whether three SDP.81 paths predict the fourth without a fitted gain."""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import FITSFixedWarning, WCS


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from reconstruct_sdp81_extended_source_v01 import (  # noqa: E402
    GRID_SIDE,
    IMAGE_RADIUS_ARCSEC,
    build_lens,
    fit_nonnegative,
    source_grid,
)
from reconstruct_sdp81_exact_ray_source_v02 import (  # noqa: E402
    beam_kernel,
    exact_path_design,
)


DATA = ROOT / "data/derived"
CUBE = ROOT / (
    "data/external/literature/sdp81_multipath_channel/"
    "SDP81_Band6_ReferenceImages/SDP81_9exec.co87.R1uvtaper1000klambda.fits"
)
OUT = DATA / "sdp81_spectral_leave_one_path_out_v01.json"
REPORT = ROOT / "reports/sdp81_spectral_leave_one_path_out_v01.md"
CHANNELS = list(range(46, 52))


def path_pixels(header, frozen: dict, geometry: dict) -> list[dict]:
    g_data = frozen["coordinates"]["image_G_icrs_j2000"]
    g = SkyCoord(
        g_data["ra_hms"],
        g_data["dec_dms"],
        unit=(u.hourangle, u.deg),
        frame="icrs",
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        wcs = WCS(header).celestial
    rows = []
    for index, (lens_x, north) in enumerate(
        geometry["image_positions_arcsec_relative_to_G"]["q1"], start=1
    ):
        sky = SkyCoord(
            ra=(g.ra.deg - lens_x / (3600.0 * np.cos(g.dec.radian))) * u.deg,
            dec=(g.dec.deg + north / 3600.0) * u.deg,
        )
        x, y = wcs.world_to_pixel(sky)
        rows.append(
            {
                "path_index": index,
                "lens_x": lens_x,
                "north": north,
                "pixel_x": float(x),
                "pixel_y": float(y),
            }
        )
    return rows


def main() -> None:
    frozen = json.loads(
        (DATA / "sdp81_lens_operator_freeze_v01.json").read_text(encoding="utf-8")
    )
    geometry = json.loads(
        (DATA / "sdp81_lens_operator_geometry_validation_v01.json").read_text(
            encoding="utf-8"
        )
    )
    lens, kwargs = build_lens(frozen)
    beta_center = tuple(
        frozen["models"]["inoue_best_fit"]["source_positions_arcsec"]["q1"]
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        with fits.open(CUBE, memmap=True) as hdul:
            cube = np.squeeze(np.asarray(hdul[0].data, dtype=float))
            header = hdul[0].header.copy()
    pixel_arcsec = abs(float(header["CDELT1"])) * 3600.0
    kernel = beam_kernel(
        pixel_arcsec,
        float(header["BMAJ"]) * 3600.0,
        float(header["BMIN"]) * 3600.0,
        float(header.get("BPA", 0.0)),
    )
    _, source_x, source_y = source_grid()
    paths = path_pixels(header, frozen, geometry)

    designs = []
    pixel_indices = []
    for path in paths:
        x0, y0 = path["pixel_x"], path["pixel_y"]
        radius_pixels = int(np.ceil(IMAGE_RADIUS_ARCSEC / pixel_arcsec))
        cx, cy = round(x0), round(y0)
        yy, xx = np.mgrid[
            cy - radius_pixels : cy + radius_pixels + 1,
            cx - radius_pixels : cx + radius_pixels + 1,
        ]
        lens_x = (xx - x0) * pixel_arcsec
        north = (yy - y0) * pixel_arcsec
        mask = lens_x**2 + north**2 <= IMAGE_RADIUS_ARCSEC**2
        design = exact_path_design(
            lens,
            kwargs,
            path["lens_x"] + lens_x,
            path["north"] + north,
            beta_center,
            source_x,
            source_y,
            kernel,
        )
        designs.append(design[mask])
        pixel_indices.append((yy[mask], xx[mask]))

    folds = []
    for channel in CHANNELS:
        observations = [
            cube[channel, yy, xx] for yy, xx in pixel_indices
        ]
        for heldout in range(len(paths)):
            training = [index for index in range(len(paths)) if index != heldout]
            _, _, solution = fit_nonnegative(
                [designs[index] for index in training],
                [observations[index] for index in training],
                shared_source=True,
            )
            source_coefficients = solution[: GRID_SIDE**2]
            source_prediction = designs[heldout] @ source_coefficients
            support = designs[heldout].sum(axis=1)
            background_mask = support <= np.quantile(support, 0.20)
            observed = observations[heldout]
            background = float(np.median(observed[background_mask]))
            prediction = source_prediction + background
            baseline = np.full_like(observed, background)
            model_sse = float(np.sum((observed - prediction) ** 2))
            baseline_sse = float(np.sum((observed - baseline) ** 2))
            predictive_r2 = 1.0 - model_sse / baseline_sse
            folds.append(
                {
                    "channel_one_based": channel + 1,
                    "heldout_path": heldout + 1,
                    "training_paths": [index + 1 for index in training],
                    "heldout_background_from_lowest_support_20pct": background,
                    "predictive_r2_vs_background": predictive_r2,
                    "improves_background": predictive_r2 > 0.0,
                    "uses_heldout_gain": False,
                }
            )

    scores = np.asarray([fold["predictive_r2_vs_background"] for fold in folds])
    path_scores = {
        str(path + 1): [
            fold["predictive_r2_vs_background"]
            for fold in folds
            if fold["heldout_path"] == path + 1
        ]
        for path in range(len(paths))
    }
    all_paths_positive_median = all(
        np.median(values) > 0.0 for values in path_scores.values()
    )
    promoted = bool(np.median(scores) > 0.0 and all_paths_positive_median)
    result = {
        "schema": "tau_core.paper8.sdp81-spectral-leave-one-path-out.v01",
        "method": (
            "fit common nonnegative source on three paths; predict fourth with no "
            "held-out gain; estimate only a low-model-support background"
        ),
        "fold_count": len(folds),
        "folds": folds,
        "predictive_r2_range": [float(scores.min()), float(scores.max())],
        "predictive_r2_median": float(np.median(scores)),
        "positive_fold_count": int(np.sum(scores > 0.0)),
        "path_median_predictive_r2": {
            path: float(np.median(values)) for path, values in path_scores.items()
        },
        "all_paths_positive_median": all_paths_positive_median,
        "transferable_common_source_dynamics_promoted": promoted,
        "body_clock_theta_M_materialized": False,
        "time_score_authorized": False,
        "verdict": (
            "COMMON_SOURCE_SPECTRAL_STRUCTURE_TRANSFERS_ACROSS_PATHS"
            if promoted
            else "COMMON_SOURCE_SPECTRAL_TRANSFER_NOT_ESTABLISHED"
        ),
        "claim_boundary": (
            "No-gain held-out path prediction of a 4D spectral source model; not a "
            "parent body clock, observer-time covector, or Tau Core detection."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 spectral leave-one-path-out audit v01\n\n"
        f"Verdict: `{result['verdict']}`\n\n"
        f"Across `{len(folds)}` channel/path folds the predictive `R^2` range is "
        f"`{scores.min():.3f}` to `{scores.max():.3f}`, with median "
        f"`{np.median(scores):.3f}` and `{np.sum(scores > 0)}` positive folds. "
        f"Per-path medians are `{result['path_median_predictive_r2']}`.\n\n"
        "No held-out source amplitude or gain is fitted. The low-support background "
        "is a declared calibration nuisance, not a source-response parameter.\n",
        encoding="utf-8",
    )
    print(result["verdict"])


if __name__ == "__main__":
    main()
