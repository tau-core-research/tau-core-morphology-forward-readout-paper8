#!/usr/bin/env python3
"""Fit two frozen spectral components with separate SDP.81 source maps."""

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
from scipy.optimize import nnls


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from reconstruct_sdp81_extended_source_v01 import (  # noqa: E402
    GRID_SIDE,
    IMAGE_RADIUS_ARCSEC,
    build_lens,
    source_grid,
)
from reconstruct_sdp81_exact_ray_source_v02 import (  # noqa: E402
    beam_kernel,
    exact_path_design,
)


DATA = ROOT / "data/derived"
CUBE = ROOT / (
    "data/external/literature/sdp81_multipath_channel/"
    "SDP81_Band6_ReferenceImages/"
    "SDP81_9exec.co87.R1uvtaper1000klambda.fits"
)
OUT = DATA / "sdp81_two_component_spatial_operator_v01.json"
REPORT = ROOT / "reports/sdp81_two_component_spatial_operator_v01.md"
CHANNELS = np.arange(47, 58)
CENTERS = (51, 54)
SIGMA_CHANNELS = 1.5


def fit_linear_operator(
    observations: list[np.ndarray],
    spatial_designs: list[np.ndarray],
    profiles: np.ndarray,
    path_count: int = 4,
) -> dict:
    """Fit nonnegative source maps after profiling one background per block."""
    source_count = GRID_SIDE**2
    component_count = profiles.shape[1]
    matrices = []
    targets = []
    for block, (values, spatial) in enumerate(zip(observations, spatial_designs)):
        channel_index = block // path_count
        matrix = np.zeros((len(values), source_count * component_count))
        for component in range(component_count):
            first = component * source_count
            matrix[:, first : first + source_count] = (
                spatial * profiles[channel_index, component]
            )
        matrices.append(matrix - matrix.mean(axis=0, keepdims=True))
        targets.append(values - values.mean())

    matrix = np.vstack(matrices)
    target = np.concatenate(targets)
    solution, residual_norm = nnls(matrix, target, maxiter=1000)
    residual = target - matrix @ solution
    rss = float(residual @ residual)
    target_ss = float(target @ target)
    n = len(target)
    nominal_k = source_count * component_count + len(observations)
    bic = float(n * np.log(max(rss / n, np.finfo(float).tiny)) + nominal_k * np.log(n))
    component_fluxes = [
        float(
            solution[
                component * source_count : (component + 1) * source_count
            ].sum()
        )
        for component in range(component_count)
    ]
    component_maps = [
        solution[
            component * source_count : (component + 1) * source_count
        ]
        for component in range(component_count)
    ]
    map_cosine = None
    if component_count == 2 and all(np.linalg.norm(values) > 0 for values in component_maps):
        map_cosine = float(
            component_maps[0] @ component_maps[1]
            / (np.linalg.norm(component_maps[0]) * np.linalg.norm(component_maps[1]))
        )
    return {
        "relative_residual": float(np.sqrt(rss / target_ss)),
        "rss": rss,
        "bic": bic,
        "nominal_parameter_count": nominal_k,
        "component_source_fluxes": component_fluxes,
        "component_map_cosine_similarity": map_cosine,
        "nnls_reported_residual_norm": float(residual_norm),
        "_source_solution": solution.tolist(),
    }


def held_path_residual(
    observations: list[np.ndarray],
    spatial_designs: list[np.ndarray],
    profiles: np.ndarray,
    source_solution: np.ndarray,
) -> float:
    residuals = []
    targets = []
    for block, (values, spatial) in enumerate(zip(observations, spatial_designs)):
        channel_index = block // 1
        source_count = GRID_SIDE**2
        prediction = np.zeros(len(values))
        for component in range(profiles.shape[1]):
            coefficients = source_solution[
                component * source_count : (component + 1) * source_count
            ]
            prediction += (
                spatial @ coefficients * profiles[channel_index, component]
            )
        residuals.append((values - values.mean()) - (prediction - prediction.mean()))
        targets.append(values - values.mean())
    return float(
        np.linalg.norm(np.concatenate(residuals))
        / np.linalg.norm(np.concatenate(targets))
    )


def main() -> None:
    frozen = json.loads((DATA / "sdp81_lens_operator_freeze_v01.json").read_text())
    geometry = json.loads(
        (DATA / "sdp81_lens_operator_geometry_validation_v01.json").read_text()
    )
    g0 = frozen["coordinates"]["image_G_icrs_j2000"]
    g = SkyCoord(g0["ra_hms"], g0["dec_dms"], unit=(u.hourangle, u.deg))
    lens, kwargs = build_lens(frozen)
    beta0 = tuple(frozen["models"]["inoue_best_fit"]["source_positions_arcsec"]["q1"])

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        with fits.open(CUBE, memmap=True) as handle:
            cube = np.squeeze(np.asarray(handle[0].data, float))
            header = handle[0].header.copy()
            wcs = WCS(header).celestial

    pixel_arcsec = abs(float(header["CDELT1"])) * 3600.0
    kernel = beam_kernel(
        pixel_arcsec,
        float(header["BMAJ"]) * 3600.0,
        float(header["BMIN"]) * 3600.0,
        float(header.get("BPA", 0.0)),
    )
    _, source_x, source_y = source_grid()
    path_designs = []
    pixel_indices = []
    for lens_x0, north0 in geometry["image_positions_arcsec_relative_to_G"]["q1"]:
        sky = SkyCoord(
            ra=(g.ra.deg - lens_x0 / (3600 * np.cos(g.dec.radian))) * u.deg,
            dec=(g.dec.deg + north0 / 3600) * u.deg,
        )
        x0, y0 = (float(value) for value in wcs.world_to_pixel(sky))
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
            lens_x0 + lens_x,
            north0 + north,
            beta0,
            source_x,
            source_y,
            kernel,
        )
        path_designs.append(design[mask][::4])
        pixel_indices.append((yy[mask][::4], xx[mask][::4]))

    observations = [
        cube[channel, yy, xx]
        for channel in CHANNELS
        for yy, xx in pixel_indices
    ]
    block_designs = [
        design for _channel in CHANNELS for design in path_designs
    ]
    two_profiles = np.column_stack(
        [
            np.exp(-0.5 * ((CHANNELS - center) / SIGMA_CHANNELS) ** 2)
            for center in CENTERS
        ]
    )
    one_profiles = two_profiles[:, :1]
    flat_profiles = np.ones((len(CHANNELS), 1))

    one = fit_linear_operator(observations, block_designs, one_profiles)
    two = fit_linear_operator(observations, block_designs, two_profiles)
    flat = fit_linear_operator(observations, block_designs, flat_profiles)
    leave_one_path_out = []
    for held_path in range(4):
        train_indices = [
            channel_index * 4 + path
            for channel_index in range(len(CHANNELS))
            for path in range(4)
            if path != held_path
        ]
        held_indices = [
            channel_index * 4 + held_path
            for channel_index in range(len(CHANNELS))
        ]
        one_train = fit_linear_operator(
            [observations[index] for index in train_indices],
            [block_designs[index] for index in train_indices],
            one_profiles,
            path_count=3,
        )
        two_train = fit_linear_operator(
            [observations[index] for index in train_indices],
            [block_designs[index] for index in train_indices],
            two_profiles,
            path_count=3,
        )
        held_observations = [observations[index] for index in held_indices]
        held_designs = [block_designs[index] for index in held_indices]
        one_held = held_path_residual(
            held_observations,
            held_designs,
            one_profiles,
            np.asarray(one_train["_source_solution"]),
        )
        two_held = held_path_residual(
            held_observations,
            held_designs,
            two_profiles,
            np.asarray(two_train["_source_solution"]),
        )
        leave_one_path_out.append(
            {
                "held_path_index": held_path,
                "one_component_relative_residual": one_held,
                "two_component_relative_residual": two_held,
                "fractional_squared_residual_improvement": (
                    1.0 - two_held**2 / one_held**2
                ),
            }
        )
    for fit in (one, two, flat):
        fit.pop("_source_solution")
    improvements = [
        fold["fractional_squared_residual_improvement"]
        for fold in leave_one_path_out
    ]
    predictive_positive_count = sum(value > 0 for value in improvements)
    predictive_median_improvement = float(np.median(improvements))
    delta_bic_one = one["bic"] - two["bic"]
    delta_bic_flat = flat["bic"] - two["bic"]
    both_nonzero = min(two["component_source_fluxes"]) > 0.0
    spatially_distinct = (
        two["component_map_cosine_similarity"] is not None
        and two["component_map_cosine_similarity"] < 0.95
    )
    promoted = bool(
        two["relative_residual"] < 1.0
        and delta_bic_one > 6.0
        and delta_bic_flat > 6.0
        and both_nonzero
        and spatially_distinct
        and predictive_positive_count >= 3
        and predictive_median_improvement > 0.05
    )
    result = {
        "schema": "tau_core.paper8.sdp81-two-component-spatial-operator.v01",
        "channels_one_based": [int(channel + 1) for channel in CHANNELS],
        "component_centers_one_based": [center + 1 for center in CENTERS],
        "profile_sigma_channels": SIGMA_CHANNELS,
        "source_basis_count_per_component": GRID_SIDE**2,
        "fit_block_count": len(observations),
        "pixel_decimation": 4,
        "mapping": "exact lens ray shooting plus ALMA beam convolution",
        "one_component": one,
        "two_component": two,
        "spectrally_flat_null": flat,
        "delta_bic_one_minus_two": delta_bic_one,
        "delta_bic_flat_minus_two": delta_bic_flat,
        "both_component_maps_nonzero": both_nonzero,
        "component_maps_spatially_distinct": spatially_distinct,
        "leave_one_path_out": leave_one_path_out,
        "predictive_positive_path_count": predictive_positive_count,
        "predictive_median_squared_residual_improvement": (
            predictive_median_improvement
        ),
        "promotion_rule": (
            "two-component residual < 1, BIC improves by >6 over both "
            "one-component and flat operators, both source maps are nonzero, "
            "their cosine similarity is <0.95, at least 3/4 held paths improve, "
            "and the median held-path squared-residual improvement is >5%"
        ),
        "two_component_spatial_source_promoted": promoted,
        "theta_M_identified": False,
        "a_O_identified": False,
        "time_score_authorized": False,
        "verdict": (
            "TWO_COMPONENT_SPATIAL_SOURCE_SUPPORTED"
            if promoted
            else "TWO_COMPONENT_SPATIAL_SOURCE_NOT_SUPPORTED"
        ),
        "claim_boundary": (
            "Finite 4D source-morphology forward audit; not a velocity field, "
            "body clock, observer-time effect, or Tau Core detection."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# SDP.81 two-component spatial-source operator v01\n\n"
        f"Verdict: `{result['verdict']}`\n\n"
        f"Relative residuals: two-component `{two['relative_residual']:.3f}`, "
        f"one-component `{one['relative_residual']:.3f}`, and flat "
        f"`{flat['relative_residual']:.3f}`. The one-minus-two BIC difference "
        f"is `{delta_bic_one:.3f}` and the flat-minus-two difference is "
        f"`{delta_bic_flat:.3f}`. Leave-one-path-out improves on "
        f"`{predictive_positive_count}/4` paths, with median squared-residual "
        f"improvement `{predictive_median_improvement:.3f}`.\n\n"
        "The component spectra were frozen before this spatial fit. A positive "
        "result supports only spatially resolved source complexity.\n"
    )
    print(result["verdict"])


if __name__ == "__main__":
    main()
