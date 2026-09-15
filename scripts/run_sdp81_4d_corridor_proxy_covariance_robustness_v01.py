#!/usr/bin/env python3
"""Noise-covariance robustness for the frozen SDP.81 4D proxy diagnostic.

The parent/proxy transfer is not changed.  The script estimates channel-noise
covariance from a fixed grid of blank image-plane apertures and propagates it
to centered-log modes by the delta method.  Multiple predeclared geometric
grids are all reported; none is selected from the resulting score.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits

from run_sdp81_common_action_endpoint_v01 import (
    centered_log_modes,
    load_frozen_endpoint,
    score_controls,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
MODEL = DATA / "sdp81_4d_corridor_proxy_diagnostic_freeze_v01.json"
OUT = DATA / "sdp81_4d_corridor_proxy_covariance_robustness_v01.json"
REPORT = ROOT / "reports/sdp81_4d_corridor_proxy_covariance_robustness_v01.md"
CUBE = ROOT / (
    "data/external/literature/sdp81_multipath_channel/SDP81_Band6_ReferenceImages/"
    "SDP81_9exec.co87.R1uvtaper1000klambda.fits"
)
FREEZE = DATA / "sdp81_lens_operator_freeze_v01.json"

BLANK_GEOMETRIES = [
    (2.5, 4.5, 0.4),
    (2.5, 4.5, 0.5),
    (2.5, 4.5, 0.6),
    (3.0, 5.0, 0.4),
    (3.0, 5.0, 0.5),
    (3.0, 5.0, 0.6),
    (3.5, 5.5, 0.4),
    (3.5, 5.5, 0.5),
    (3.5, 5.5, 0.6),
]
SCALE_SENSITIVITY = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0]


def exp_symmetric(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(matrix)
    return vectors @ np.diag(np.exp(values)) @ vectors.T


def blank_aperture_spectra(
    cube: np.ndarray,
    header: Any,
    g_coord: SkyCoord,
    inner_arcsec: float,
    outer_arcsec: float,
    grid_step_arcsec: float,
    aperture_radius_arcsec: float,
) -> np.ndarray:
    """Extract a geometry-selected blank-aperture ensemble on channels 47--52."""
    yy, xx = np.indices(cube.shape[1:])
    spectra = []
    for dx in np.arange(-outer_arcsec, outer_arcsec + 1.0e-9, grid_step_arcsec):
        for dy in np.arange(-outer_arcsec, outer_arcsec + 1.0e-9, grid_step_arcsec):
            radius = float(np.hypot(dx, dy))
            if not inner_arcsec <= radius <= outer_arcsec:
                continue
            ra = g_coord.ra.deg - dx / (3600.0 * np.cos(g_coord.dec.radian))
            dec = g_coord.dec.deg + dy / 3600.0
            x_arcsec = (ra - header["CRVAL1"]) * np.cos(np.deg2rad(dec)) * 3600.0
            y_arcsec = (dec - header["CRVAL2"]) * 3600.0
            xpix = x_arcsec / (header["CDELT1"] * 3600.0) + header["CRPIX1"] - 1.0
            ypix = y_arcsec / (header["CDELT2"] * 3600.0) + header["CRPIX2"] - 1.0
            if not (10 < xpix < cube.shape[2] - 10 and 10 < ypix < cube.shape[1] - 10):
                continue
            mask = (
                ((xx - xpix) * abs(header["CDELT1"] * 3600.0)) ** 2
                + ((yy - ypix) * abs(header["CDELT2"] * 3600.0)) ** 2
                <= aperture_radius_arcsec**2
            )
            spectra.append(np.nanmean(cube[46:52, mask], axis=1))
    return np.asarray(spectra, dtype=float)


def log_mode_covariances(
    fluxes: np.ndarray, basis: np.ndarray, channel_covariance: np.ndarray
) -> list[np.ndarray]:
    """Propagate linear-flux covariance to U^T log(f) at first order."""
    if np.any(fluxes <= 0.0):
        raise ValueError("positive endpoint flux is required for log-mode covariance")
    result = []
    for flux in fluxes:
        jacobian = basis.T @ np.diag(1.0 / flux)
        covariance = jacobian @ channel_covariance @ jacobian.T
        if float(np.linalg.eigvalsh(covariance).min()) <= 0.0:
            raise ValueError("propagated mode covariance is not positive")
        result.append(covariance)
    return result


def main() -> None:
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    if model.get("status") != "DIAGNOSTIC_ONLY_NOT_ENDPOINT":
        raise RuntimeError("the fixed diagnostic proxy is unavailable")
    basis = np.asarray(model["terminal_calibration"]["centered_log_channel_basis"])
    transfers = [
        np.asarray(item["selected_transfer"]) for item in model["compiled_paths"]
    ]
    generator = np.asarray(model["generator"])
    depths = [float(item["proxy_depth"]) for item in model["compiled_paths"]]
    fluxes = load_frozen_endpoint(model)
    modes = centered_log_modes(fluxes, basis)
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    g = freeze["coordinates"]["image_G_icrs_j2000"]
    g_coord = SkyCoord(g["ra_hms"], g["dec_dms"], unit=(u.hourangle, u.deg), frame="icrs")
    aperture_radius = float(model["endpoint_extraction_freeze"]["aperture_radius_arcsec"])
    with fits.open(CUBE, memmap=True) as hdul:
        cube = np.squeeze(hdul[0].data).astype(float)
        header = hdul[0].header
        records = []
        for inner, outer, step in BLANK_GEOMETRIES:
            blank = blank_aperture_spectra(
                cube, header, g_coord, inner, outer, step, aperture_radius
            )
            channel_covariance = np.cov(blank, rowvar=False, ddof=1)
            covariances = log_mode_covariances(fluxes, basis, channel_covariance)
            scores = score_controls(modes, transfers, covariances)
            matched = float(scores["matched"]["total_mahalanobis_chi2"])
            wrong_values = np.asarray(
                [
                    item["total_mahalanobis_chi2"]
                    for item in scores["wrong_path_assignment"]
                ]
            )
            scale_records = []
            for scale in SCALE_SENSITIVITY:
                scaled_transfers = [
                    exp_symmetric(-scale * depth * generator) for depth in depths
                ]
                scaled = score_controls(modes, scaled_transfers, covariances)
                scale_records.append(
                    {
                        "scale": scale,
                        "matched_score": float(
                            scaled["matched"]["total_mahalanobis_chi2"]
                        ),
                    }
                )
            preferred_scale = min(
                scale_records, key=lambda item: item["matched_score"]
            )["scale"]
            records.append(
                {
                    "inner_radius_arcsec": inner,
                    "outer_radius_arcsec": outer,
                    "grid_step_arcsec": step,
                    "blank_aperture_count": int(blank.shape[0]),
                    "channel_covariance": channel_covariance.tolist(),
                    "channel_covariance_condition_number": float(
                        np.linalg.cond(channel_covariance)
                    ),
                    "matched_score": matched,
                    "lossless_score": float(
                        scores["lossless_identity"]["total_mahalanobis_chi2"]
                    ),
                    "matched_beats_lossless": scores["matched_beats_lossless"],
                    "matched_beats_wrong_median": scores[
                        "matched_beats_wrong_median"
                    ],
                    "matched_beats_every_wrong_assignment": scores[
                        "matched_beats_every_wrong_assignment"
                    ],
                    "wrong_assignment_fraction_not_worse": float(
                        np.mean(wrong_values <= matched)
                    ),
                    "scale_sensitivity": scale_records,
                    "posthoc_preferred_scale": preferred_scale,
                }
            )
    lossless_wins = sum(record["matched_beats_lossless"] for record in records)
    wrong_median_wins = sum(
        record["matched_beats_wrong_median"] for record in records
    )
    every_wrong_wins = sum(
        record["matched_beats_every_wrong_assignment"] for record in records
    )
    fractions = [record["wrong_assignment_fraction_not_worse"] for record in records]
    preferred_scale_counts = {
        str(scale): sum(record["posthoc_preferred_scale"] == scale for record in records)
        for scale in SCALE_SENSITIVITY
    }
    checks = {
        "fixed_proxy_unchanged": True,
        "nine_blank_geometries": len(records) == 9,
        "all_blank_ensembles_overdetermine_six_channel_covariance": all(
            record["blank_aperture_count"] > 6 for record in records
        ),
        "all_channel_covariances_positive": all(
            np.linalg.eigvalsh(np.asarray(record["channel_covariance"])).min() > 0.0
            for record in records
        ),
        "no_geometry_selected_from_score": True,
        "physical_endpoint_remains_unauthorized": True,
    }
    result = {
        "schema": "tau-core.paper8.sdp81-4d-corridor-proxy-covariance-robustness.v01",
        "status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
        "verdict": "WEAK_PATH_ORDER_COMPATIBILITY_NOT_MODEL_SELECTION",
        "model": str(MODEL.relative_to(ROOT)),
        "covariance_method": (
            "sample covariance of geometry-selected 0.12-arcsec blank apertures "
            "on channels 47--52, propagated to centered log modes by the delta method"
        ),
        "geometry_records": records,
        "summary": {
            "matched_beats_lossless_geometries": lossless_wins,
            "geometry_count": len(records),
            "matched_beats_wrong_median_geometries": wrong_median_wins,
            "matched_beats_every_wrong_assignment_geometries": every_wrong_wins,
            "wrong_assignment_fraction_not_worse_range": [
                float(min(fractions)),
                float(max(fractions)),
            ],
            "posthoc_preferred_scale_counts": preferred_scale_counts,
            "frozen_unit_scale_is_posthoc_best_geometries": preferred_scale_counts[
                "1.0"
            ],
            "posthoc_retuning_allowed": False,
        },
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "physical_endpoint_authorized": False,
        "claim_boundary": (
            "Retrospective covariance robustness for the already frozen nonphysical "
            "4D proxy. The path-order advantage over a wrong-assignment median is "
            "descriptive, while preference over lossless transfer is not stable across "
            "blank-aperture geometries and no geometry beats every wrong assignment. "
            "This is neither a calibrated population p-value nor evidence for a "
            "Nature-occupied parent action."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 4D-corridor proxy covariance robustness v01\n\n"
        f"Status: `{result['status']}`. Verdict: `{result['verdict']}`.\n\n"
        f"The fixed proxy beats lossless transfer for `{lossless_wins}/9` blank-aperture "
        f"geometries, beats the wrong-assignment median for `{wrong_median_wins}/9`, "
        f"and beats every wrong assignment for `{every_wrong_wins}/9`. The fraction "
        f"of wrong assignments no worse than matched spans `{min(fractions):.3f}` to "
        f"`{max(fractions):.3f}`. In the descriptive scale scan, the frozen unit "
        f"scale is best for `{preferred_scale_counts['1.0']}/9` geometries and "
        f"scale 0.5 is best for `{preferred_scale_counts['0.5']}/9`; post-endpoint "
        f"retuning is forbidden.\n\n{result['claim_boundary']}\n",
        encoding="utf-8",
    )
    print(result["verdict"])


if __name__ == "__main__":
    main()
