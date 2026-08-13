#!/usr/bin/env python3
"""Fit one affine source velocity field through all SDP.81 paths and channels."""

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
    source_grid,
)
from reconstruct_sdp81_exact_ray_source_v02 import beam_kernel, exact_path_design  # noqa: E402


DATA = ROOT / "data/derived"
CUBE = ROOT / "data/external/literature/sdp81_multipath_channel/SDP81_Band6_ReferenceImages/SDP81_9exec.co87.R1uvtaper1000klambda.fits"
OUT = DATA / "sdp81_velocity_field_operator_v01.json"
REPORT = ROOT / "reports/sdp81_velocity_field_operator_v01.md"
CHANNELS = list(range(46, 52))
SCHEMA = "tau_core.paper8.sdp81-velocity-field-operator.v01"
C_KM_S = 299792.458


def main() -> None:
    frozen = json.loads((DATA / "sdp81_lens_operator_freeze_v01.json").read_text())
    geometry = json.loads((DATA / "sdp81_lens_operator_geometry_validation_v01.json").read_text())
    g0 = frozen["coordinates"]["image_G_icrs_j2000"]
    g = SkyCoord(g0["ra_hms"], g0["dec_dms"], unit=(u.hourangle, u.deg))
    lens, kwargs = build_lens(frozen)
    beta0 = tuple(frozen["models"]["inoue_best_fit"]["source_positions_arcsec"]["q1"])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        with fits.open(CUBE, memmap=True) as h:
            cube = np.squeeze(np.asarray(h[0].data, float))
            header = h[0].header.copy()
            wcs = WCS(header).celestial
    pix = abs(float(header["CDELT1"])) * 3600.0
    kernel = beam_kernel(pix, float(header["BMAJ"])*3600, float(header["BMIN"])*3600, float(header.get("BPA", 0)))
    _, sx, sy = source_grid()
    frequency = float(header["CRVAL3"]) + (np.arange(cube.shape[0])+1-float(header["CRPIX3"])) * float(header["CDELT3"])
    velocity = C_KM_S * (1-frequency/float(header["RESTFRQ"]))

    spatial_designs, pixel_indices = [], []
    for lens_x0, north0 in geometry["image_positions_arcsec_relative_to_G"]["q1"]:
        sky = SkyCoord(
            ra=(g.ra.deg-lens_x0/(3600*np.cos(g.dec.radian)))*u.deg,
            dec=(g.dec.deg+north0/3600)*u.deg,
        )
        x0, y0 = (float(v) for v in wcs.world_to_pixel(sky))
        rp = int(np.ceil(IMAGE_RADIUS_ARCSEC/pix))
        cx, cy = round(x0), round(y0)
        yy, xx = np.mgrid[cy-rp:cy+rp+1, cx-rp:cx+rp+1]
        lx, ny = (xx-x0)*pix, (yy-y0)*pix
        mask = lx**2+ny**2 <= IMAGE_RADIUS_ARCSEC**2
        design = exact_path_design(lens, kwargs, lens_x0+lx, north0+ny, beta0, sx, sy, kernel)
        spatial_designs.append(design[mask])
        pixel_indices.append((yy[mask], xx[mask]))

    observations = [cube[ch, yy, xx][::4] for ch in CHANNELS for yy, xx in pixel_indices]
    spatial_designs = [design[::4] for design in spatial_designs]
    target_norm = np.linalg.norm(np.concatenate(observations))

    def fast_fit(designs):
        n_source = GRID_SIDE**2
        rows = sum(len(x) for x in observations)
        matrix = np.zeros((rows, n_source + len(designs)))
        target = np.concatenate(observations)
        start = 0
        for block, design in enumerate(designs):
            stop = start + len(design)
            matrix[start:stop, :n_source] = design
            matrix[start:stop, n_source + block] = 1.0
            start = stop
        solution = np.linalg.lstsq(matrix, target, rcond=1e-8)[0]
        solution[:n_source] = np.maximum(solution[:n_source], 0.0)
        prediction = matrix @ solution
        residual = target - prediction
        block_residuals = []
        start = 0
        for values in observations:
            stop = start + len(values)
            block_residuals.append(float(np.linalg.norm(residual[start:stop]) / np.linalg.norm(values)))
            start = stop
        return float(np.linalg.norm(residual) / target_norm), block_residuals, solution

    def solve(parameters):
        v0, gx, gy, log_sigma = parameters
        sigma = np.exp(log_sigma)
        cell_velocity = v0 + gx*sx + gy*sy
        designs = []
        for ch in CHANNELS:
            weight = np.exp(-0.5*((velocity[ch]-cell_velocity)/sigma)**2)
            designs.extend([design*weight[None, :] for design in spatial_designs])
        rel, path_rel, solution = fast_fit(designs)
        return rel, path_rel, solution

    candidates = [
        [7.77, -93.78, 72.24, np.log(30.0)],
        [7.77, -93.78, 72.24, np.log(60.0)],
        [8.0, 0.0, 0.0, np.log(30.0)],
    ]
    evaluated = [(solve(np.asarray(candidate)), candidate) for candidate in candidates]
    (relative_residual, block_residuals, solution), best = min(
        evaluated, key=lambda item: item[0][0]
    )
    v0, gx, gy, log_sigma = best
    sigma = float(np.exp(log_sigma))

    # Null limit: a spatial source with no spectral structure, fitted to all blocks.
    null_designs = [design for _ in CHANNELS for design in spatial_designs]
    null_residual, _, _ = fast_fit(null_designs)
    improvement = 1.0 - relative_residual**2/null_residual**2
    promoted = bool(
        relative_residual < 1.0
        and max(block_residuals) < 2.0
        and relative_residual < null_residual
        and improvement > 0.05
        and np.hypot(gx, gy) > 0.0
    )
    result = {
        "schema": SCHEMA,
        "channels_one_based": [channel + 1 for channel in CHANNELS],
        "operator": "I_s(x,y) times Gaussian[v-v0-gx*x-gy*y; sigma_v], exact lens ray shooting, ALMA beam convolution",
        "fit_blocks": len(observations),
        "source_amplitude_count": GRID_SIDE**2,
        "velocity_parameters": {
            "v0_km_s": float(v0),
            "gx_km_s_per_arcsec": float(gx),
            "gy_km_s_per_arcsec": float(gy),
            "gradient_norm_km_s_per_arcsec": float(np.hypot(gx, gy)),
            "sigma_v_km_s": sigma,
        },
        "candidate_count": len(candidates),
        "selection": "minimum residual over frozen finite candidate set",
        "solver": "unconstrained least squares followed by nonnegative source projection; preflight only",
        "relative_residual": relative_residual,
        "maximum_block_relative_residual": max(block_residuals),
        "spectrally_flat_null_relative_residual": null_residual,
        "squared_residual_improvement_over_flat_null": improvement,
        "promotion_rule": "relative residual < 1, every block < 2, >5% null improvement, and nonzero velocity gradient",
        "velocity_field_operator_promoted": promoted,
        "theta_M_identified": False,
        "a_O_identified": False,
        "time_score_authorized": False,
        "verdict": "VELOCITY_FIELD_DIFFERENTIAL_MAGNIFICATION_OPERATOR_SUPPORTED" if promoted else "VELOCITY_FIELD_OPERATOR_NOT_SUPPORTED",
        "claim_boundary": "4D source-kinematic forward operator; not parent Theta_M, observer-time covector, or Tau detection.",
    }
    OUT.write_text(json.dumps(result, indent=2)+"\n")
    REPORT.write_text(
        "# SDP.81 velocity-field operator v01\n\n"
        f"Verdict: `{result['verdict']}`\n\nRelative residual `{relative_residual:.3f}` versus spectrally flat null `{null_residual:.3f}`; squared-residual improvement `{improvement:.3f}`. "
        f"Fitted gradient norm `{np.hypot(gx,gy):.2f} km/s/arcsec`, line width `{sigma:.2f} km/s`.\n\n"
        "This is a 4D kinematic differential-magnification operator, not a body clock or time signal.\n"
    )
    print(result["verdict"])


if __name__ == "__main__":
    main()
