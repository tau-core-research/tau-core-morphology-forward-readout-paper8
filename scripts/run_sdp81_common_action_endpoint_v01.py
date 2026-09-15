#!/usr/bin/env python3
"""Run the frozen common-action SDP.81 score only after source authorization."""

from __future__ import annotations

import json
from itertools import permutations
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
MODEL = DATA / "sdp81_common_action_forward_model_v01.json"
OUT = DATA / "sdp81_common_action_endpoint_v01.json"
REPORT = ROOT / "reports/sdp81_common_action_endpoint_v01.md"


def centered_log_modes(spectra: np.ndarray, basis: np.ndarray) -> np.ndarray:
    if spectra.ndim != 2 or spectra.shape[1] != basis.shape[0]:
        raise ValueError("spectra and terminal basis have incompatible shapes")
    if np.any(~np.isfinite(spectra)) or np.any(spectra <= 0.0):
        raise ValueError("spectral endpoint must be finite and strictly positive")
    log_spectra = np.log(spectra)
    centered = log_spectra - log_spectra.mean(axis=1, keepdims=True)
    return centered @ basis


def loo_score(
    observed_modes: np.ndarray,
    transfers: list[np.ndarray],
    covariances: list[np.ndarray],
) -> dict[str, Any]:
    path_count, mode_dim = observed_modes.shape
    if len(transfers) != path_count or len(covariances) != path_count:
        raise ValueError("path count mismatch")
    folds = []
    for held_out in range(path_count):
        normal = np.zeros((mode_dim, mode_dim), dtype=float)
        rhs = np.zeros(mode_dim, dtype=float)
        for index in range(path_count):
            if index == held_out:
                continue
            precision = np.linalg.inv(covariances[index])
            normal += transfers[index].T @ precision @ transfers[index]
            rhs += transfers[index].T @ precision @ observed_modes[index]
        source = np.linalg.solve(normal, rhs)
        prediction = transfers[held_out] @ source
        residual = observed_modes[held_out] - prediction
        precision = np.linalg.inv(covariances[held_out])
        folds.append(
            {
                "held_out_index": held_out,
                "mahalanobis_chi2": float(residual @ precision @ residual),
                "mode_rmse": float(np.sqrt(np.mean(residual**2))),
            }
        )
    return {
        "folds": folds,
        "total_mahalanobis_chi2": float(sum(fold["mahalanobis_chi2"] for fold in folds)),
        "mean_mode_rmse": float(np.mean([fold["mode_rmse"] for fold in folds])),
    }


def score_controls(
    observed_modes: np.ndarray,
    transfers: list[np.ndarray],
    covariances: list[np.ndarray],
) -> dict[str, Any]:
    matched = loo_score(observed_modes, transfers, covariances)
    identity = [np.eye(observed_modes.shape[1]) for _ in transfers]
    lossless = loo_score(observed_modes, identity, covariances)
    wrong = []
    for permutation in permutations(range(len(transfers))):
        if permutation == tuple(range(len(transfers))):
            continue
        score = loo_score(observed_modes, [transfers[i] for i in permutation], covariances)
        wrong.append({"permutation": list(permutation), **score})
    wrong_chi2 = np.asarray([item["total_mahalanobis_chi2"] for item in wrong])
    return {
        "matched": matched,
        "lossless_identity": lossless,
        "wrong_path_assignment": wrong,
        "matched_beats_lossless": matched["total_mahalanobis_chi2"] < lossless["total_mahalanobis_chi2"],
        "matched_beats_wrong_median": matched["total_mahalanobis_chi2"] < float(np.median(wrong_chi2)),
        "matched_beats_every_wrong_assignment": matched["total_mahalanobis_chi2"] < float(wrong_chi2.min()),
    }


def load_frozen_endpoint(model: dict[str, Any]) -> np.ndarray:
    """Open the CO cube only after caller has verified authorization."""
    from astropy.coordinates import SkyCoord
    from astropy.io import fits
    import astropy.units as u

    freeze = json.loads((DATA / "sdp81_lens_operator_freeze_v01.json").read_text())
    geometry = json.loads((DATA / "sdp81_lens_operator_geometry_validation_v01.json").read_text())
    cube_path = ROOT / (
        "data/external/literature/sdp81_multipath_channel/SDP81_Band6_ReferenceImages/"
        "SDP81_9exec.co87.R1uvtaper1000klambda.fits"
    )
    g = freeze["coordinates"]["image_G_icrs_j2000"]
    g_coord = SkyCoord(g["ra_hms"], g["dec_dms"], unit=(u.hourangle, u.deg), frame="icrs")
    positions = geometry["image_positions_arcsec_relative_to_G"]["q1"]
    extraction = model["endpoint_extraction_freeze"]
    radius = float(extraction["aperture_radius_arcsec"])
    with fits.open(cube_path, memmap=True) as hdul:
        cube = np.squeeze(hdul[0].data).astype(float)
        header = hdul[0].header
    yy, xx = np.indices(cube.shape[1:])
    spectra = []
    for x_arcsec, y_arcsec in positions:
        ra = g_coord.ra.deg - x_arcsec / (3600 * np.cos(g_coord.dec.radian))
        dec = g_coord.dec.deg + y_arcsec / 3600
        x_arc = (ra - header["CRVAL1"]) * np.cos(np.deg2rad(dec)) * 3600.0
        y_arc = (dec - header["CRVAL2"]) * 3600.0
        xpix = x_arc / (header["CDELT1"] * 3600.0) + header["CRPIX1"] - 1
        ypix = y_arc / (header["CDELT2"] * 3600.0) + header["CRPIX2"] - 1
        mask = (
            ((xx - xpix) * abs(header["CDELT1"] * 3600.0)) ** 2
            + ((yy - ypix) * abs(header["CDELT2"] * 3600.0)) ** 2
            <= radius**2
        )
        spectra.append(np.nanmean(cube[46:52, mask], axis=1))
    return np.asarray(spectra)


def main() -> None:
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    authorized = bool(
        model.get("endpoint_authorized") is True
        and model.get("status") == "FORMULA_FROZEN_ENDPOINT_AUTHORIZED_RETROSPECTIVE_ONLY"
        and len(model.get("compiled_paths", [])) == 4
        and model.get("terminal_calibration") is not None
    )
    if not authorized:
        result = {
            "schema": "tau-core.paper8.sdp81-common-action-endpoint.v01",
            "status": "FORMULA_SHELL_DERIVED_ENDPOINT_BLOCKED",
            "model": str(MODEL.relative_to(ROOT)),
            "spectral_endpoint_read": False,
            "score_emitted": False,
            "blocker": model.get("blocker", "source model not authorized"),
            "claim_boundary": "Fail-closed result; no spectral endpoint was opened.",
        }
    else:
        calibration = model["terminal_calibration"]
        basis = np.asarray(calibration["centered_log_channel_basis"], dtype=float)
        path_ids = [item["path_id"] for item in model["compiled_paths"]]
        transfers = [np.asarray(item["selected_transfer"], dtype=float) for item in model["compiled_paths"]]
        covariances = [
            np.asarray(calibration["mode_noise_covariance_by_path"][path_id], dtype=float)
            for path_id in path_ids
        ]
        spectra = load_frozen_endpoint(model)
        modes = centered_log_modes(spectra, basis)
        scores = score_controls(modes, transfers, covariances)
        result = {
            "schema": "tau-core.paper8.sdp81-common-action-endpoint.v01",
            "status": "RETROSPECTIVE_COMMON_ACTION_DIAGNOSTIC_SCORED",
            "model": str(MODEL.relative_to(ROOT)),
            "spectral_endpoint_read": True,
            "score_emitted": True,
            "scores": scores,
            "claim_boundary": (
                "Retrospective diagnostic only. The endpoint was previously opened and "
                "cannot validate Tau Core, Nature occupation, or a novel prediction."
            ),
        }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 common-action endpoint v01\n\n"
        f"Status: `{result['status']}`.\n\n"
        f"Spectral endpoint read: `{result['spectral_endpoint_read']}`. "
        f"Score emitted: `{result['score_emitted']}`.\n\n"
        f"{result['claim_boundary']}\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
