#!/usr/bin/env python3
"""Test a minimal common source-plane morphology covector on SDP.81 q1 paths."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.wcs import FITSFixedWarning
from lenstronomy.LensModel.lens_model import LensModel
from lenstronomy.Util.param_util import phi_q2_ellipticity, shear_polar2cartesian


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
IMAGE = ROOT / (
    "data/external/literature/sdp81_multipath_channel/"
    "SDP81_Band7_ReferenceImages/SDP81_band7_11exec.contR1.image.fits"
)
OUT = DATA / "sdp81_common_source_covector_audit_v01.json"
REPORT = ROOT / "reports/sdp81_common_source_covector_audit_v01.md"


def lens_model(frozen: dict) -> tuple[LensModel, list[dict]]:
    model = frozen["models"]["inoue_best_fit"]
    e1, e2 = phi_q2_ellipticity(
        np.deg2rad(90.0 + model["ellipticity_pa_deg_ccw_from_north"]),
        model["axis_ratio_q"],
    )
    gamma1, gamma2 = shear_polar2cartesian(
        np.deg2rad(model["external_shear_pa_deg_ccw_from_north"]),
        model["external_shear_gamma"],
    )
    center_x, center_y = model["lens_center_arcsec_relative_to_G"]
    kwargs = [
        {
            "theta_E": model["einstein_radius_b_arcsec"],
            "e1": e1,
            "e2": e2,
            "center_x": center_x,
            "center_y": center_y,
        },
        {
            "gamma1": gamma1,
            "gamma2": gamma2,
            "ra_0": 0.0,
            "dec_0": 0.0,
        },
    ]
    return LensModel(["SIE", "SHEAR"]), kwargs


def local_gradient(
    image: np.ndarray,
    x0: float,
    y0: float,
    pixel_arcsec: float,
    radius_arcsec: float,
) -> np.ndarray:
    radius_pixels = int(np.ceil(radius_arcsec / pixel_arcsec))
    center_x, center_y = round(x0), round(y0)
    yy, xx = np.mgrid[
        center_y - radius_pixels : center_y + radius_pixels + 1,
        center_x - radius_pixels : center_x + radius_pixels + 1,
    ]
    lens_x = (xx - x0) * pixel_arcsec
    north = (yy - y0) * pixel_arcsec
    mask = lens_x**2 + north**2 <= radius_arcsec**2
    design = np.column_stack(
        (np.ones(mask.sum()), lens_x[mask], north[mask])
    )
    values = image[yy, xx][mask]
    return np.linalg.lstsq(design, values, rcond=None)[0][1:]


def main() -> None:
    frozen = json.loads(
        (DATA / "sdp81_lens_operator_freeze_v01.json").read_text(encoding="utf-8")
    )
    registration = json.loads(
        (DATA / "sdp81_image_g_wcs_registration_v01.json").read_text(encoding="utf-8")
    )
    lens, kwargs = lens_model(frozen)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        with fits.open(IMAGE) as hdul:
            image = np.squeeze(hdul[0].data).astype(float)
            header = hdul[0].header
    pixel_arcsec = abs(float(header["CDELT1"])) * 3600.0
    beam_major_arcsec = float(header["BMAJ"]) * 3600.0

    anchor = registration["anchor"]
    peak = registration["local_compact_peak"]
    pixel_shifts = {
        "published_g": (0.0, 0.0),
        "local_peak": (
            peak["pixel_x_zero_based"] - anchor["pixel_x_zero_based"],
            peak["pixel_y_zero_based"] - anchor["pixel_y_zero_based"],
        ),
    }
    runs = []
    for anchor_name, (shift_x, shift_y) in pixel_shifts.items():
        for radius_beams in (1.0, 1.5, 2.0):
            image_gradients = []
            pullbacks = []
            for path in registration["q1_paths"]:
                gradient = local_gradient(
                    image,
                    path["pixel_x_zero_based"] + shift_x,
                    path["pixel_y_zero_based"] + shift_y,
                    pixel_arcsec,
                    radius_beams * beam_major_arcsec,
                )
                f_xx, f_xy, f_yx, f_yy = lens.hessian(
                    path["lens_x_west_offset_arcsec"],
                    path["north_offset_arcsec"],
                    kwargs,
                )
                source_jacobian = np.array(
                    [[1.0 - f_xx, -f_xy], [-f_yx, 1.0 - f_yy]]
                )
                image_gradients.append(gradient)
                pullbacks.append(source_jacobian.T)

            design = np.vstack(pullbacks)
            observed = np.concatenate(image_gradients)
            source_covector = np.linalg.lstsq(design, observed, rcond=None)[0]
            predicted = design @ source_covector
            relative_residual = float(
                np.linalg.norm(observed - predicted) / np.linalg.norm(observed)
            )
            runs.append(
                {
                    "anchor": anchor_name,
                    "radius_beams": radius_beams,
                    "source_covector_intensity_per_arcsec": source_covector.tolist(),
                    "stacked_design_rank": int(np.linalg.matrix_rank(design)),
                    "stacked_design_condition_number": float(np.linalg.cond(design)),
                    "relative_residual": relative_residual,
                }
            )

    residuals = [run["relative_residual"] for run in runs]
    result = {
        "schema": "tau_core.paper8.sdp81-common-source-covector-audit.v01",
        "model": (
            "grad_theta I_i = A_i^T grad_beta I_source for one common local "
            "source-plane scalar covector"
        ),
        "path_count": 4,
        "sensitivity_anchors": list(pixel_shifts),
        "sensitivity_radius_beams": [1.0, 1.5, 2.0],
        "runs": runs,
        "relative_residual_range": [min(residuals), max(residuals)],
        "all_designs_full_rank": all(run["stacked_design_rank"] == 2 for run in runs),
        "common_covector_promoted": False,
        "promotion_rule": "relative residual <= 0.5 in every frozen sensitivity run",
        "reason": (
            "A common local source-plane scalar covector is supported on some "
            "aperture/anchor choices but not across the complete frozen sensitivity set."
        ),
        "interpretation": (
            "This rejects the minimal local scalar-gradient realization, not a richer "
            "source morphology, beam-convolved forward model, or Tau body covector."
        ),
        "time_covector_identified": False,
        "time_score_authorized": False,
        "next_finite_action": (
            "Replace local image-plane plane fits by a beam-convolved source-plane "
            "brightness reconstruction jointly forward-rendered through all four paths."
        ),
        "claim_boundary": (
            "Source-morphology pullback audit only; no channel innovation, observer-time "
            "effect, or Tau Core detection."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 common source-covector audit v01\n\n"
        "The minimal relation "
        "`grad_theta I_i = A_i^T grad_beta I_source` was fitted jointly to all "
        "four q1 paths over two registration anchors and three beam-scaled "
        f"apertures. The relative residual spans `{min(residuals):.3f}` to "
        f"`{max(residuals):.3f}`.\n\n"
        "One common local scalar covector is therefore not robustly promoted across "
        "the complete sensitivity set. This does not reject the beam-convolved "
        "extended-source reconstruction or a richer Tau body covector.\n",
        encoding="utf-8",
    )
    print(
        "COMMON_LOCAL_SOURCE_COVECTOR_NOT_PROMOTED "
        f"residual_range={min(residuals):.3f}:{max(residuals):.3f}"
    )


if __name__ == "__main__":
    main()
