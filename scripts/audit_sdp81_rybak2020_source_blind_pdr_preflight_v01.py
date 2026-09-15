#!/usr/bin/env python3
"""CO(10-9)-blind PDR source preflight for the SDP.81 held-out score.

Only the independently published 200-pc CII, FIR, CO(3-2), CO(5-4), and
CO(8-7) products are read.  No CO(10-9) file, header, or pixel is opened.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from astropy.io import fits
from pdrtpy.modelset import ModelSet
from scipy.interpolate import RectBivariateSpline


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/external/literature/sdp81_rybak2020_source_blind"
OUT = ROOT / "data/derived/sdp81_rybak2020_source_blind_pdr_preflight_v01.json"
MAPS = ROOT / "data/derived/sdp81_rybak2020_source_blind_pdr_preflight_maps_v01.fits"
REPORT = ROOT / "reports/sdp81_rybak2020_source_blind_pdr_preflight_v01.md"

SOURCE_URL = "https://sites.google.com/view/matusdoesresearch/data"
ARXIV = "https://arxiv.org/abs/1912.12538"
MODEL_NAME = "wk2006"
MODEL_VERSION = "2006"
MODEL_METALLICITY = 1.0
F_PDR = 0.8
FLUX_CAL = 0.10
SYSTEMATIC = {"CII": 0.07, "FIR": 0.07, "CO32": 0.65, "CO54": 0.10, "CO87": 0.20}
FILES = {
    "CII": ("L_CII_200pc.fits", "L_CII_200pc_error.fits"),
    "FIR": ("FIR_200pc.fits", "FIR_200pc_error.fits"),
    "CO32": ("L_CO32_200pc.fits", "L_CO32_200pc_error.fits"),
    "CO54": ("L_CO54_200pc.fits", "L_CO54_200pc_error.fits"),
    "CO87": ("L_CO87_200pc.fits", "L_CO87_200pc_error.fits"),
}
EXPECTED_HASHES = {
    "L_CII_200pc.fits": "f36c10fe2684525342d5e564644c0f88b6890e439e71dc9b35133839e921a61b",
    "L_CII_200pc_error.fits": "bf4e21039c83c78d98d3521d8ad7ca5e6cc905ae858dbfeb4c6742b190672b00",
    "FIR_200pc.fits": "edcd785d6c84d03d26d568a537e4c90b0537fe1afd0e9ac69915fed647dd0707",
    "FIR_200pc_error.fits": "d44547b8b58762460aa4d10f9bff24f65db6120372a8602aee2d161834ce451a",
    "L_CO32_200pc.fits": "61e6d69ac3ac6bd2183bf5e9deb8d09e62d8fcb964251be03a677f5d3b47143d",
    "L_CO32_200pc_error.fits": "60aa4463ccf17ba1ddbfb6c47a2fa32114f0b6d0404367ddaa75889fd41a3229",
    "L_CO54_200pc.fits": "b4ba3e38a8bb80876a8d0370c0b3f2edec920a14bb3427a5c5815f37f71b2d8f",
    "L_CO54_200pc_error.fits": "51302a052bc0b6a59d208287bec91b70d98ac51454f02303f5a1cf65792acbcb",
    "L_CO87_200pc.fits": "066cfd571c9f397298eeff380b8d5344e71a29b1a3c4949292081799684426f3",
    "L_CO87_200pc_error.fits": "33f168de523b9cb7b4461914cb7af7a9b6c5579774e6dab4df3e499b5a145146",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def weighted_quantile(values: np.ndarray, weights: np.ndarray, q: float) -> float:
    order = np.argsort(values)
    sorted_values = values[order]
    cdf = np.cumsum(weights[order])
    return float(np.interp(q, cdf, sorted_values))


def model_grid(step: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    models = ModelSet(MODEL_NAME, z=MODEL_METALLICITY)
    cii = np.asarray(models.get_model("CII_158").data, dtype=float)
    co32 = np.asarray(models.get_model("CO_32").data, dtype=float)
    co54 = np.asarray(models.get_model("CO_54").data, dtype=float)
    base = models.get_model("CII_158/FIR")
    ratios = [
        np.asarray(base.data, dtype=float),
        2.0 * cii / co54,
        2.0 * cii / co32,
        np.asarray(models.get_model("CO_87/CO_54").data, dtype=float),
    ]
    prediction = np.asarray(models.get_model("CO_109/CO_54").data, dtype=float)
    wcs = base.wcs.wcs
    logn = wcs.crval[0] + np.arange(base.shape[1]) * wcs.cdelt[0]
    logg = wcs.crval[1] + np.arange(base.shape[0]) * wcs.cdelt[1]
    fine_n = np.arange(logn.min(), logn.max() + 0.5 * step, step)
    fine_g = np.arange(logg.min(), logg.max() + 0.5 * step, step)

    def interpolate(array: np.ndarray) -> np.ndarray:
        spline = RectBivariateSpline(logg, logn, np.log(np.clip(array, 1e-300, None)), kx=2, ky=2)
        return np.exp(spline(fine_g, fine_n))

    log_ratios = np.stack([np.log(interpolate(item)) for item in ratios], axis=-1)
    return fine_n, fine_g, log_ratios, interpolate(prediction)


def fit(step: float, arrays: dict[str, np.ndarray], errors: dict[str, np.ndarray], mask: np.ndarray, f_pdr: float) -> dict:
    fine_n, fine_g, model_ratios, prediction = model_grid(step)
    prediction_flat = prediction.ravel()
    design = np.array(
        [[1, -1, 0, 0, 0], [1, 0, 0, -1, 0], [1, 0, -1, 0, 0], [0, 0, 0, -1, 1]],
        dtype=float,
    )
    names = ["CII", "FIR", "CO32", "CO54", "CO87"]
    shape = mask.shape
    maps = {name: np.full(shape, np.nan) for name in ["logn", "logg", "chi2red", "ratio50", "ratio16", "ratio84", "neff"]}
    records = []
    for row, col in zip(*np.where(mask)):
        values = np.array([arrays[name][row, col] for name in names], dtype=float)
        sigma = np.array([errors[name][row, col] for name in names], dtype=float)
        values[0] *= f_pdr
        sigma[0] *= f_pdr
        observed = np.log([values[0] / values[1], values[0] / values[3], values[0] / values[2], values[4] / values[3]])
        log_variance = (sigma / values) ** 2 + np.array([SYSTEMATIC[name] ** 2 + FLUX_CAL**2 for name in names])
        covariance = design @ np.diag(log_variance) @ design.T
        inverse = np.linalg.inv(covariance)
        residual = model_ratios - observed
        chi2 = np.einsum("...i,ij,...j->...", residual, inverse, residual)
        best = np.unravel_index(np.argmin(chi2), chi2.shape)
        weights = np.exp(-0.5 * (chi2 - chi2[best])).ravel()
        weights /= weights.sum()
        ratio16 = weighted_quantile(prediction_flat, weights, 0.16)
        ratio50 = weighted_quantile(prediction_flat, weights, 0.50)
        ratio84 = weighted_quantile(prediction_flat, weights, 0.84)
        neff = float(1.0 / np.sum(weights**2))
        values_out = {
            "logn": float(fine_n[best[1]]),
            "logg": float(fine_g[best[0]]),
            "chi2red": float(chi2[best] / 2.0),
            "ratio50": ratio50,
            "ratio16": ratio16,
            "ratio84": ratio84,
            "neff": neff,
        }
        for name, value in values_out.items():
            maps[name][row, col] = value
        records.append(values_out)
    return {"maps": maps, "records": records}


def median(records: list[dict], name: str) -> float:
    return float(np.median([record[name] for record in records]))


def main() -> None:
    if any("co109" in path.name.lower() for path in SOURCE.iterdir()):
        raise RuntimeError("CO(10-9) material is forbidden in the source-blind directory")
    hashes = {name: sha256(SOURCE / name) for name in EXPECTED_HASHES}
    arrays = {key: np.asarray(fits.getdata(SOURCE / pair[0]), dtype=float) for key, pair in FILES.items()}
    errors = {key: np.asarray(fits.getdata(SOURCE / pair[1]), dtype=float) for key, pair in FILES.items()}
    shape = arrays["CII"].shape
    mask = np.ones(shape, dtype=bool)
    detection_counts = {}
    for key in FILES:
        detected = np.isfinite(arrays[key]) & np.isfinite(errors[key]) & (arrays[key] > 0) & (errors[key] > 0)
        detected &= arrays[key] / np.where(errors[key] > 0, errors[key], np.inf) >= 3.0
        detection_counts[key] = int(detected.sum())
        mask &= detected

    primary = fit(0.05, arrays, errors, mask, F_PDR)
    coarse = fit(0.10, arrays, errors, mask, F_PDR)
    sensitivity = {}
    for f_pdr in (0.6, 0.8, 0.9):
        result = primary if f_pdr == F_PDR else fit(0.05, arrays, errors, mask, f_pdr)
        records = result["records"]
        sensitivity[str(f_pdr)] = {
            "median_logn_cm3": median(records, "logn"),
            "median_logg_habing": median(records, "logg"),
            "median_predicted_co109_over_co54": median(records, "ratio50"),
            "fraction_reduced_chi2_below_5": float(np.mean([item["chi2red"] < 5.0 for item in records])),
        }

    records = primary["records"]
    coarse_ratio = np.array([item["ratio50"] for item in coarse["records"]])
    fine_ratio = np.array([item["ratio50"] for item in records])
    eligible = np.array([item["chi2red"] < 5.0 for item in records], dtype=bool)
    relative_half_width = np.array([(item["ratio84"] - item["ratio16"]) / (2.0 * item["ratio50"]) for item in records])
    checks = {
        "all_source_hashes_match": hashes == EXPECTED_HASHES,
        "all_maps_are_40_by_40": all(array.shape == (40, 40) for array in arrays.values()) and all(array.shape == (40, 40) for array in errors.values()),
        "co109_header_not_read": True,
        "co109_pixels_not_read": True,
        "four_independent_log_ratios_for_two_parameters": True,
        "model_prediction_positive": bool(np.all(fine_ratio > 0)),
        "fine_coarse_prediction_stable_on_median": bool(np.median(np.abs(fine_ratio - coarse_ratio) / fine_ratio) < 0.05),
        "at_least_one_well_fit_source_pixel": bool(np.any(eligible)),
        "all_source_pixels_well_fit": bool(np.all(eligible)),
        "channelwise_spectral_registration_available": False,
    }
    status = "SOURCE_ACQUIRED_PDR_AMPLITUDE_PARTIAL_SPECTRAL_REGISTRATION_BLOCKED"
    payload = {
        "schema": "tau-core.paper8.sdp81-rybak2020-source-blind-pdr-preflight.v01",
        "status": status,
        "scientific_role": "CO(10-9)-blind standard-physics source-amplitude preflight",
        "sources": {"author_data_page": SOURCE_URL, "paper": ARXIV, "sha256": hashes},
        "endpoint_access": {"co109_header_read": False, "co109_pixels_read": False},
        "model": {
            "package": "pdrtpy 2.6.4",
            "model_set": MODEL_NAME,
            "model_version": MODEL_VERSION,
            "metallicity_solar": MODEL_METALLICITY,
            "f_pdr_cii": F_PDR,
            "flux_calibration_fraction": FLUX_CAL,
            "reconstruction_systematics": SYSTEMATIC,
            "fit_ratios": ["CII/FIR", "CII/CO54", "CII/CO32", "CO87/CO54"],
            "held_out_prediction": "CO109/CO54",
            "grid_step_dex": 0.05,
        },
        "data": {"shape": list(shape), "detection_counts": detection_counts, "all_five_tracer_pixels": int(mask.sum())},
        "fit_summary": {
            "median_logn_cm3": median(records, "logn"),
            "median_logg_habing": median(records, "logg"),
            "median_reduced_chi2": median(records, "chi2red"),
            "well_fit_chi2red_below_5_pixels": int(eligible.sum()),
            "well_fit_fraction": float(eligible.mean()),
            "median_predicted_co109_over_co54": median(records, "ratio50"),
            "median_relative_68pct_half_width": float(np.median(relative_half_width)),
            "median_fine_coarse_relative_difference": float(np.median(np.abs(fine_ratio - coarse_ratio) / fine_ratio)),
        },
        "f_pdr_sensitivity": sensitivity,
        "checks": checks,
        "endpoint_authorized": False,
        "blocker": "integrated 200-pc PDR amplitudes do not fix the six-channel pathwise source function, opacity, filling, differential magnification, or five-mode terminal Jacobian",
        "claim_boundary": "This is a standard-physics, CO(10-9)-blind source-amplitude preflight. It neither validates Tau Core nor authorizes the held-out spectral endpoint.",
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    hdus = [fits.PrimaryHDU()]
    for name, extname in [("logn", "LOGN"), ("logg", "LOGG"), ("chi2red", "CHI2RED"), ("ratio50", "RATIO50"), ("ratio16", "RATIO16"), ("ratio84", "RATIO84"), ("neff", "NEFF")]:
        hdus.append(fits.ImageHDU(primary["maps"][name], name=extname))
    fits.HDUList(hdus).writeto(MAPS, overwrite=True, checksum=True)

    REPORT.write_text(
        "# SDP.81 Rybak-2020 CO(10-9)-blind PDR preflight v01\n\n"
        f"Status: `{status}`. Endpoint authorized: `False`.\n\n"
        f"The official 200-pc source products supply {int(mask.sum())} pixels with S/N >= 3 in CII, FIR, CO(3-2), CO(5-4), and CO(8-7). No CO(10-9) header or pixel was read.\n\n"
        f"A solar-metallicity `{MODEL_NAME}` PDR fit using CII/FIR, CII/CO(5-4), CII/CO(3-2), and CO(8-7)/CO(5-4) gives median log n={median(records, 'logn'):.2f}, median log G0={median(records, 'logg'):.2f}, and a blind median CO(10-9)/CO(5-4) prediction of {median(records, 'ratio50'):.4f}. Only {int(eligible.sum())}/{int(mask.sum())} pixels have reduced chi2 < 5, and the median 68% relative predictive half-width is {float(np.median(relative_half_width)):.3f}.\n\n"
        "Verdict: the independent maps materially close source acquisition and provide a standard-physics integrated-amplitude prior, but they do not determine the six-channel, four-path terminal Jacobian. The held-out endpoint remains sealed.\n\n"
        "Next finite action: combine the accepted source pixels with an independently frozen velocity/profile model and the ordinary lens/aperture operator, then test whether the resulting five-mode terminal registration is full rank before opening CO(10-9).\n",
        encoding="utf-8",
    )
    print(status)


if __name__ == "__main__":
    main()
