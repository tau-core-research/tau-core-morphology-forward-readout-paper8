#!/usr/bin/env python3
"""Calibrate path shifts from continuum leave-one-path-out prediction."""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.wcs import FITSFixedWarning


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
IMAGE = ROOT / (
    "data/external/literature/sdp81_multipath_channel/"
    "SDP81_Band7_ReferenceImages/SDP81_band7_11exec.contR1.image.fits"
)
OUT = DATA / "sdp81_continuum_path_registration_v01.json"
REPORT = ROOT / "reports/sdp81_continuum_path_registration_v01.md"
SHIFT_GRID_MAS = [-40.0, -20.0, 0.0, 20.0, 40.0]
SCHEMA = "tau_core.paper8.sdp81-continuum-path-registration.v01"


def main() -> None:
    frozen = json.loads(
        (DATA / "sdp81_lens_operator_freeze_v01.json").read_text(encoding="utf-8")
    )
    registration = json.loads(
        (DATA / "sdp81_image_g_wcs_registration_v01.json").read_text(encoding="utf-8")
    )
    lens, kwargs = build_lens(frozen)
    beta_center = tuple(
        frozen["models"]["inoue_best_fit"]["source_positions_arcsec"]["q1"]
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        with fits.open(IMAGE) as hdul:
            image = np.squeeze(hdul[0].data).astype(float)
            header = hdul[0].header
    pixel_arcsec = abs(float(header["CDELT1"])) * 3600.0
    kernel = beam_kernel(
        pixel_arcsec,
        float(header["BMAJ"]) * 3600.0,
        float(header["BMIN"]) * 3600.0,
        float(header.get("BPA", 0.0)),
    )
    _, source_x, source_y = source_grid()

    observations = []
    coordinate_grids = []
    nominal_designs = []
    for path in registration["q1_paths"]:
        x0, y0 = path["pixel_x_zero_based"], path["pixel_y_zero_based"]
        radius_pixels = int(np.ceil(IMAGE_RADIUS_ARCSEC / pixel_arcsec))
        cx, cy = round(x0), round(y0)
        yy, xx = np.mgrid[
            cy - radius_pixels : cy + radius_pixels + 1,
            cx - radius_pixels : cx + radius_pixels + 1,
        ]
        lens_x = (xx - x0) * pixel_arcsec
        north = (yy - y0) * pixel_arcsec
        mask = lens_x**2 + north**2 <= IMAGE_RADIUS_ARCSEC**2
        coordinate_grids.append((lens_x, north, mask))
        observations.append(image[yy, xx][mask])
        nominal = exact_path_design(
            lens,
            kwargs,
            path["lens_x_west_offset_arcsec"] + lens_x,
            path["north_offset_arcsec"] + north,
            beta_center,
            source_x,
            source_y,
            kernel,
        )
        nominal_designs.append(nominal[mask])

    path_calibrations = []
    for heldout, path in enumerate(registration["q1_paths"]):
        training = [index for index in range(4) if index != heldout]
        _, _, solution = fit_nonnegative(
            [nominal_designs[index] for index in training],
            [observations[index] for index in training],
            shared_source=True,
        )
        source_coefficients = solution[: GRID_SIDE**2]
        lens_x, north, mask = coordinate_grids[heldout]
        observed = observations[heldout]
        candidates = []
        for dx_mas in SHIFT_GRID_MAS:
            for dy_mas in SHIFT_GRID_MAS:
                full_design = exact_path_design(
                    lens,
                    kwargs,
                    path["lens_x_west_offset_arcsec"] + lens_x + dx_mas / 1000.0,
                    path["north_offset_arcsec"] + north + dy_mas / 1000.0,
                    beta_center,
                    source_x,
                    source_y,
                    kernel,
                )
                design = full_design[mask]
                source_prediction = design @ source_coefficients
                support = design.sum(axis=1)
                low_support = support <= np.quantile(support, 0.20)
                background = float(np.median(observed[low_support]))
                prediction = source_prediction + background
                sse = float(np.sum((observed - prediction) ** 2))
                candidates.append(
                    {
                        "dx_lens_x_mas": dx_mas,
                        "dy_north_mas": dy_mas,
                        "sse": sse,
                        "background": background,
                    }
                )
        best = min(candidates, key=lambda row: row["sse"])
        nominal = next(
            row
            for row in candidates
            if row["dx_lens_x_mas"] == 0.0 and row["dy_north_mas"] == 0.0
        )
        path_calibrations.append(
            {
                "path_index": heldout + 1,
                "training_paths": [index + 1 for index in training],
                "selected_dx_lens_x_mas": best["dx_lens_x_mas"],
                "selected_dy_north_mas": best["dy_north_mas"],
                "selected_sse": best["sse"],
                "nominal_sse": nominal["sse"],
                "fractional_sse_improvement": 1.0 - best["sse"] / nominal["sse"],
                "grid_boundary_selected": (
                    abs(best["dx_lens_x_mas"]) == max(abs(x) for x in SHIFT_GRID_MAS)
                    or abs(best["dy_north_mas"]) == max(abs(x) for x in SHIFT_GRID_MAS)
                ),
                "heldout_gain_fitted": False,
            }
        )

    boundary_count = sum(
        row["grid_boundary_selected"] for row in path_calibrations
    )
    result = {
        "schema": SCHEMA,
        "source_tracer": "ALMA Band-7 continuum",
        "calibration_method": (
            "leave one path out; reconstruct source on three paths; select held-out "
            "geometric shift on fixed grid with no source gain"
        ),
        "shift_grid_mas": SHIFT_GRID_MAS,
        "path_calibrations": path_calibrations,
        "boundary_selection_count": boundary_count,
        "registration_freeze_usable_for_band6": boundary_count == 0,
        "verdict": (
            "CONTINUUM_PATH_REGISTRATION_FROZEN_INTERIOR_SOLUTIONS"
            if boundary_count == 0
            else "CONTINUUM_PATH_REGISTRATION_GRID_NOT_CLOSED"
        ),
        "claim_boundary": (
            "Independent-tracer geometric calibration only; not a spectral fit, "
            "clock effect, observer-time signal, or Tau Core detection."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 continuum path registration v01\n\n"
        f"Verdict: `{result['verdict']}`\n\n"
        f"Selected path shifts: `{[(r['selected_dx_lens_x_mas'], r['selected_dy_north_mas']) for r in path_calibrations]}` mas. "
        f"`{boundary_count}` of four paths select a grid boundary.\n\n"
        "Each calibration is held out from the three-path continuum source fit and "
        "uses no held-out source gain. Transfer to Band-6 is authorized only when "
        "all selected solutions are interior to the frozen grid.\n",
        encoding="utf-8",
    )
    print(result["verdict"])


if __name__ == "__main__":
    main()
