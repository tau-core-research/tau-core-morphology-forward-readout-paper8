#!/usr/bin/env python3
"""Reconstruct a six-channel SDP.81 q1 source cube through four lens paths."""

from __future__ import annotations

import csv
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
OUT = DATA / "sdp81_source_spectral_cube_v01.json"
COEFF = DATA / "sdp81_source_spectral_cube_coefficients_v01.csv"
REPORT = ROOT / "reports/sdp81_source_spectral_cube_v01.md"
CHANNELS_ZERO_BASED = list(range(46, 52))
C_KM_S = 299792.458


def q1_pixels(header, frozen: dict, geometry: dict) -> list[dict]:
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
        ra = g.ra.deg - lens_x / (3600.0 * np.cos(g.dec.radian))
        dec = g.dec.deg + north / 3600.0
        x, y = wcs.world_to_pixel(SkyCoord(ra=ra * u.deg, dec=dec * u.deg))
        rows.append(
            {
                "path_index": index,
                "lens_x_west_offset_arcsec": lens_x,
                "north_offset_arcsec": north,
                "pixel_x_zero_based": float(x),
                "pixel_y_zero_based": float(y),
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

    channel_index = np.arange(cube.shape[0])
    frequency = (
        float(header["CRVAL3"])
        + (channel_index + 1.0 - float(header["CRPIX3"])) * float(header["CDELT3"])
    )
    velocity = C_KM_S * (1.0 - frequency / float(header["RESTFRQ"]))
    selected_velocity = velocity[CHANNELS_ZERO_BASED]
    pixel_arcsec = abs(float(header["CDELT1"])) * 3600.0
    kernel = beam_kernel(
        pixel_arcsec,
        float(header["BMAJ"]) * 3600.0,
        float(header["BMIN"]) * 3600.0,
        float(header.get("BPA", 0.0)),
    )
    paths = q1_pixels(header, frozen, geometry)
    _, source_x, source_y = source_grid()

    designs = []
    path_pixel_indices = []
    for path in paths:
        x0 = path["pixel_x_zero_based"]
        y0 = path["pixel_y_zero_based"]
        radius_pixels = int(np.ceil(IMAGE_RADIUS_ARCSEC / pixel_arcsec))
        cx, cy = round(x0), round(y0)
        yy, xx = np.mgrid[
            cy - radius_pixels : cy + radius_pixels + 1,
            cx - radius_pixels : cx + radius_pixels + 1,
        ]
        lens_x = (xx - x0) * pixel_arcsec
        north = (yy - y0) * pixel_arcsec
        mask = lens_x**2 + north**2 <= IMAGE_RADIUS_ARCSEC**2
        full_design = exact_path_design(
            lens,
            kwargs,
            path["lens_x_west_offset_arcsec"] + lens_x,
            path["north_offset_arcsec"] + north,
            beta_center,
            source_x,
            source_y,
            kernel,
        )
        designs.append(full_design[mask])
        path_pixel_indices.append((yy[mask], xx[mask]))

    coefficients = []
    channel_rows = []
    for channel in CHANNELS_ZERO_BASED:
        observations = [
            cube[channel, yy, xx] for yy, xx in path_pixel_indices
        ]
        common_residual, path_residuals, solution = fit_nonnegative(
            designs, observations, shared_source=True
        )
        independent_residual, _, _ = fit_nonnegative(
            designs, observations, shared_source=False
        )
        excess = (
            common_residual**2 - independent_residual**2
        ) / independent_residual**2
        coefficients.append(solution[: GRID_SIDE**2])
        channel_rows.append(
            {
                "channel_one_based": channel + 1,
                "velocity_radio_lsrk_km_s": float(velocity[channel]),
                "common_source_relative_residual": common_residual,
                "maximum_path_relative_residual": max(path_residuals),
                "independent_source_relative_residual": independent_residual,
                "common_vs_independent_squared_residual_excess": excess,
            }
        )

    coefficient_array = np.asarray(coefficients)
    integrated = coefficient_array.sum(axis=0)
    active = integrated >= 0.10 * integrated.max()
    centroid = np.full(GRID_SIDE**2, np.nan)
    centroid[active] = (
        selected_velocity[:, None] * coefficient_array[:, active]
    ).sum(axis=0) / integrated[active]
    active_design = np.column_stack(
        (np.ones(active.sum()), source_x[active], source_y[active])
    )
    weights = np.sqrt(integrated[active] / integrated[active].max())
    weighted_design = active_design * weights[:, None]
    weighted_centroid = centroid[active] * weights
    clock_plane = np.linalg.lstsq(
        weighted_design, weighted_centroid, rcond=None
    )[0]
    predicted_centroid = active_design @ clock_plane
    centroid_r2 = 1.0 - float(
        np.sum((centroid[active] - predicted_centroid) ** 2)
        / np.sum((centroid[active] - np.mean(centroid[active])) ** 2)
    )

    centered_spectra = coefficient_array[:, active].T
    centered_spectra = centered_spectra - centered_spectra.mean(axis=0)
    singular_values = np.linalg.svd(centered_spectra, compute_uv=False)
    spectral_rank = int(np.sum(singular_values > singular_values[0] * 1e-8))
    proxy_nonzero_fit = bool(
        active.sum() >= 3
        and np.linalg.norm(clock_plane[1:]) > 0.0
        and np.isfinite(centroid_r2)
    )
    channel_promotions = [
        row["common_source_relative_residual"] < 0.5
        and row["maximum_path_relative_residual"] < 0.65
        and row["common_vs_independent_squared_residual_excess"] < 0.5
        for row in channel_rows
    ]
    common_spectral_cube_promoted = all(channel_promotions)
    proxy_stable = bool(
        proxy_nonzero_fit and common_spectral_cube_promoted and centroid_r2 > 0.5
    )

    coefficient_rows = []
    for cell in range(GRID_SIDE**2):
        for channel_offset, channel in enumerate(CHANNELS_ZERO_BASED):
            coefficient_rows.append(
                {
                    "source_cell": cell,
                    "source_x_arcsec_relative_to_q1": float(source_x[cell]),
                    "source_y_arcsec_relative_to_q1": float(source_y[cell]),
                    "channel_one_based": channel + 1,
                    "velocity_radio_lsrk_km_s": float(velocity[channel]),
                    "nonnegative_intensity_coefficient": float(
                        coefficient_array[channel_offset, cell]
                    ),
                    "active_source_cell": bool(active[cell]),
                    "source_spectral_centroid_km_s": (
                        float(centroid[cell]) if active[cell] else ""
                    ),
                }
            )
    with COEFF.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(coefficient_rows[0]))
        writer.writeheader()
        writer.writerows(coefficient_rows)

    result = {
        "schema": "tau_core.paper8.sdp81-source-spectral-cube.v01",
        "tracer": "ALMA Band-6 CO(8-7)",
        "channels_one_based": [channel + 1 for channel in CHANNELS_ZERO_BASED],
        "velocities_radio_lsrk_km_s": selected_velocity.tolist(),
        "path_count": len(paths),
        "source_basis_count": GRID_SIDE**2,
        "active_source_cell_count": int(active.sum()),
        "channel_fits": channel_rows,
        "all_common_channel_residuals_finite": all(
            np.isfinite(row["common_source_relative_residual"])
            for row in channel_rows
        ),
        "source_spectral_rank": spectral_rank,
        "channel_common_source_promotion_flags": channel_promotions,
        "common_source_spectral_cube_promoted": common_spectral_cube_promoted,
        "source_clock_proxy": {
            "name": "Theta_dyn_4D_inverse",
            "definition": "weighted affine fit to source-cell CO spectral centroids",
            "offset_km_s": float(clock_plane[0]),
            "covector_km_s_per_arcsec": clock_plane[1:].tolist(),
            "covector_norm_km_s_per_arcsec": float(np.linalg.norm(clock_plane[1:])),
            "centroid_plane_r2": centroid_r2,
            "nonzero_fit": proxy_nonzero_fit,
            "stable": proxy_stable,
            "parent_body_clock_identified": False,
        },
        "body_clock_theta_M_materialized": False,
        "quotient_basic_time_covector_a_O_materialized": False,
        "time_score_authorized": False,
        "verdict": (
            "SOURCE_SPECTRAL_CUBE_AND_4D_DYNAMICAL_ORDER_PROXY_MATERIALIZED"
            if proxy_stable
            else "CONSTRAINED_SOURCE_SPECTRAL_CUBE_MATERIALIZED__CLOCK_PROXY_NOT_PROMOTED"
        ),
        "claim_boundary": (
            "A 4D inverse dynamical-order proxy reconstructed from a spectral tracer; "
            "not a parent-derived Theta_M, quotient-basic a_O, observer-time effect, "
            "or Tau Core detection."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 source spectral cube v01\n\n"
        f"Verdict: `{result['verdict']}`\n\n"
        f"Six CO(8-7) channels were jointly reconstructed through four exact lens "
        f"paths on `{GRID_SIDE**2}` source cells. `{active.sum()}` cells pass the "
        "frozen 10% integrated-intensity support threshold. The weighted source "
        f"spectral-centroid plane has covector norm "
        f"`{np.linalg.norm(clock_plane[1:]):.3f} km/s/arcsec` and `R^2={centroid_r2:.3f}`.\n\n"
        "The nonzero affine fit is not promoted because common-source spectral "
        "consistency and positive centroid-plane explanatory power are both "
        "required. This is not the parent body clock or an observer-time detection.\n",
        encoding="utf-8",
    )
    print(result["verdict"])


if __name__ == "__main__":
    main()
