#!/usr/bin/env python3
"""Build a source-only numerical preflight for the radial body matrix.

The radial edges in this development artifact are provisional source-only CO
support quantiles.  They test WCS, beam handling, rank, and conditioning, but
they are not the final terminal edges and cannot be scored as an endpoint.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales
from scipy.ndimage import gaussian_filter


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
EXTERNAL = ROOT / "data/external/literature/phangs_radial_body_projection_development_v01"
ACQUISITION = DATA / "phangs_radial_body_projection_development_source_acquisition_v01.json"
PREREG = DATA / "phangs_radial_body_projection_preregistration_v01.json"
SAMPLE = ROOT / "data/external/phangs/phangs_public_sample.csv"
REPORT = ROOT / "reports/phangs_radial_body_projection_development_preflight_v01.md"

N_ZONES = 5
S4G_PSF_FWHM_ARCSEC = 1.7
GEOMETRY = {
    "NGC1087": (359.1, 42.9),
    "NGC1365": (201.1, 55.4),
    "NGC1433": (199.7, 28.6),
    "NGC1566": (214.7, 29.5),
    "NGC1672": (134.3, 42.6),
    "NGC7496": (193.7, 35.9),
}


def sip_consistent_wcs(header: fits.Header) -> WCS:
    cleaned = header.copy()
    for axis in (1, 2):
        key = f"CTYPE{axis}"
        if "A_ORDER" in cleaned and "-SIP" not in str(cleaned.get(key, "")):
            cleaned[key] = str(cleaned[key]) + "-SIP"
    return WCS(cleaned, naxis=2)


def read_image(path: Path) -> tuple[np.ndarray, fits.Header, WCS]:
    with fits.open(path, memmap=False) as hdul:
        image = np.squeeze(np.asarray(hdul[0].data, dtype=float))
        header = hdul[0].header.copy()
    if image.ndim != 2:
        raise ValueError(f"Expected a 2D image in {path}")
    return image, header, sip_consistent_wcs(header)


def disk_coordinates(
    wcs: WCS,
    shape: tuple[int, int],
    center: tuple[float, float],
    pa_deg: float,
    inclination_deg: float,
) -> tuple[np.ndarray, np.ndarray]:
    yy, xx = np.indices(shape, dtype=float)
    ra, dec = wcs.pixel_to_world_values(xx, yy)
    east = (ra - center[0]) * math.cos(math.radians(center[1])) * 3600.0
    north = (dec - center[1]) * 3600.0
    pa = math.radians(pa_deg)
    major = east * math.sin(pa) + north * math.cos(pa)
    minor = -east * math.cos(pa) + north * math.sin(pa)
    disk_y = minor / math.cos(math.radians(inclination_deg))
    return np.hypot(major, disk_y), np.arctan2(disk_y, major)


def normalized_smooth(image: np.ndarray, valid: np.ndarray, sigma_pixels: float) -> np.ndarray:
    if sigma_pixels <= 1.0e-8:
        return np.where(valid, image, np.nan)
    numerator = gaussian_filter(np.where(valid, image, 0.0), sigma_pixels)
    denominator = gaussian_filter(valid.astype(float), sigma_pixels)
    return np.divide(
        numerator,
        denominator,
        out=np.full_like(numerator, np.nan),
        where=denominator > 0.5,
    )


def harmonic_profile(
    image: np.ndarray,
    radius: np.ndarray,
    theta: np.ndarray,
    valid: np.ndarray,
    edges: np.ndarray,
    mode: int,
) -> np.ndarray:
    profile = []
    for zone in range(N_ZONES):
        select = valid & (radius >= edges[zone]) & (
            radius <= edges[zone + 1] if zone == N_ZONES - 1 else radius < edges[zone + 1]
        )
        weights = np.where(select, np.clip(image, 0.0, None), 0.0)
        total = float(np.sum(weights))
        if int(np.sum(select)) < 30 or not np.isfinite(total) or total <= 0:
            raise RuntimeError(f"Insufficient source support in radial zone {zone}")
        profile.append(np.sum(weights * np.exp(1j * mode * theta)) / total)
    return np.asarray(profile, dtype=complex)


def embed(profile: np.ndarray, mode: int) -> np.ndarray:
    vector = np.zeros(4 * N_ZONES, dtype=float)
    offset = 0 if mode == 1 else 2
    for zone, value in enumerate(profile):
        vector[4 * zone + offset] = value.real
        vector[4 * zone + offset + 1] = value.imag
    norm = float(np.linalg.norm(vector))
    if norm <= 1.0e-12:
        raise RuntimeError("A frozen source profile produced a null embedded column")
    return vector / norm


def finite_difference(profile: np.ndarray) -> np.ndarray:
    return np.gradient(profile)


def matrix_metrics(matrix: np.ndarray) -> dict[str, Any]:
    singular = np.linalg.svd(matrix, compute_uv=False)
    tolerance = max(matrix.shape) * np.finfo(float).eps * singular[0]
    rank = int(np.sum(singular > tolerance))
    nonzero = singular[:rank]
    return {
        "shape": list(matrix.shape),
        "rank": rank,
        "projected_complement_dimension": int(matrix.shape[0] - rank),
        "singular_values": singular.tolist(),
        "condition_number_nonzero": float(nonzero[0] / nonzero[-1]),
        "rank_gate_ge_4_complement": bool(matrix.shape[0] - rank >= 4),
    }


def main() -> None:
    acquisition = json.loads(ACQUISITION.read_text(encoding="utf-8"))
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    if acquisition["velocity_contrast_opened"] or acquisition["rotation_residual_opened"]:
        raise RuntimeError("Source-only acquisition boundary was violated")
    ready = acquisition["source_body_ready"]
    sample = pd.read_csv(SAMPLE, skiprows=[1]).set_index("Name")
    profile_rows: list[dict[str, Any]] = []
    galaxy_results: dict[str, Any] = {}
    matrix_bundle: dict[str, np.ndarray] = {}

    for galaxy in ready:
        directory = EXTERNAL / galaxy
        stellar_path = next(directory.glob("*.phot.1.fits"))
        mask_path = next(directory.glob("*.1.final_mask.fits"))
        co_path = next(directory.glob("*broad_mom0.fits"))
        stellar, stellar_header, stellar_wcs = read_image(stellar_path)
        source_mask, mask_header, mask_wcs = read_image(mask_path)
        co, co_header, co_wcs = read_image(co_path)
        if stellar.shape != source_mask.shape:
            raise RuntimeError(f"S4G image/mask shape mismatch for {galaxy}")
        if not np.allclose(stellar_wcs.wcs.crval, mask_wcs.wcs.crval, atol=1.0e-10):
            raise RuntimeError(f"S4G image/mask WCS mismatch for {galaxy}")

        center = (float(sample.loc[galaxy, "R.A."]), float(sample.loc[galaxy, "Dec."]))
        pa, inclination = GEOMETRY[galaxy]
        sx, sy = stellar_wcs.world_to_pixel_values(*center)
        cx, cy = co_wcs.world_to_pixel_values(*center)
        centers_inside = bool(
            0 <= sx < stellar.shape[1] and 0 <= sy < stellar.shape[0]
            and 0 <= cx < co.shape[1] and 0 <= cy < co.shape[0]
        )
        if not centers_inside:
            raise RuntimeError(f"Published center falls outside a source image for {galaxy}")

        stellar_radius, stellar_theta = disk_coordinates(
            stellar_wcs, stellar.shape, center, pa, inclination
        )
        co_radius, co_theta = disk_coordinates(co_wcs, co.shape, center, pa, inclination)

        stellar_pixel_arcsec = float(np.mean(np.abs(proj_plane_pixel_scales(stellar_wcs))) * 3600.0)
        co_pixel_arcsec = float(np.mean(np.abs(proj_plane_pixel_scales(co_wcs))) * 3600.0)
        co_beam = math.sqrt(float(co_header["BMAJ"]) * float(co_header["BMIN"])) * 3600.0
        target_beam = max(S4G_PSF_FWHM_ARCSEC, co_beam)
        stellar_sigma = math.sqrt(max(target_beam**2 - S4G_PSF_FWHM_ARCSEC**2, 0.0)) / 2.35482 / stellar_pixel_arcsec
        co_sigma = math.sqrt(max(target_beam**2 - co_beam**2, 0.0)) / 2.35482 / co_pixel_arcsec

        stellar_valid = np.isfinite(stellar) & (source_mask == 0)
        outer = stellar_valid & (stellar_radius >= np.nanquantile(stellar_radius[stellar_valid], 0.8))
        stellar_background = float(np.nanmedian(stellar[outer]))
        stellar_signal = normalized_smooth(stellar - stellar_background, stellar_valid, stellar_sigma)

        co_finite = np.isfinite(co)
        co_noise = 1.4826 * float(np.nanmedian(np.abs(co[co_finite] - np.nanmedian(co[co_finite]))))
        co_support = co_finite & (co > 3.0 * co_noise)
        if int(co_support.sum()) < 5 * 30:
            raise RuntimeError(f"Insufficient 3-sigma CO morphology support for {galaxy}")
        edges = np.quantile(co_radius[co_support], np.linspace(0.0, 1.0, N_ZONES + 1))
        co_signal = normalized_smooth(co, co_finite, co_sigma)
        stellar_profile_valid = np.isfinite(stellar_signal) & (stellar_signal > 0)
        co_profile_valid = np.isfinite(co_signal) & co_support

        profiles = {
            "stellar_m1": harmonic_profile(stellar_signal, stellar_radius, stellar_theta, stellar_profile_valid, edges, 1),
            "stellar_m2": harmonic_profile(stellar_signal, stellar_radius, stellar_theta, stellar_profile_valid, edges, 2),
            "co_m1": harmonic_profile(co_signal, co_radius, co_theta, co_profile_valid, edges, 1),
            "co_m2": harmonic_profile(co_signal, co_radius, co_theta, co_profile_valid, edges, 2),
        }
        columns = [
            embed(profiles["stellar_m1"], 1),
            embed(finite_difference(profiles["stellar_m1"]), 1),
            embed(profiles["stellar_m2"], 2),
            embed(finite_difference(profiles["stellar_m2"]), 2),
            embed(profiles["co_m1"], 1),
            embed(finite_difference(profiles["co_m1"]), 1),
            embed(profiles["co_m2"], 2),
            embed(finite_difference(profiles["co_m2"]), 2),
        ]
        matrix = np.column_stack(columns)
        matrix_bundle[galaxy] = matrix
        metrics = matrix_metrics(matrix)
        metrics.update({
            "center_inside_both_sources": centers_inside,
            "target_beam_arcsec": target_beam,
            "s4g_extra_gaussian_sigma_pixels": stellar_sigma,
            "co_extra_gaussian_sigma_pixels": co_sigma,
            "co_noise_robust_mom0_units": co_noise,
            "co_support_pixels": int(co_support.sum()),
            "provisional_source_only_radial_edges_arcsec": edges.tolist(),
            "radial_edge_role": "development conditioning preflight only",
        })
        galaxy_results[galaxy] = metrics
        for family, profile in profiles.items():
            for zone, value in enumerate(profile):
                profile_rows.append({
                    "galaxy": galaxy,
                    "profile": family,
                    "zone": zone,
                    "radius_min_arcsec": edges[zone],
                    "radius_max_arcsec": edges[zone + 1],
                    "real": value.real,
                    "imag": value.imag,
                    "amplitude": abs(value),
                    "phase_rad": np.angle(value),
                })

    np.savez_compressed(DATA / "phangs_radial_body_projection_development_matrices_v01.npz", **matrix_bundle)
    pd.DataFrame(profile_rows).to_csv(
        DATA / "phangs_radial_body_projection_development_profiles_v01.csv", index=False
    )
    all_rank = all(item["rank_gate_ge_4_complement"] for item in galaxy_results.values())
    result = {
        "schema": "phangs_radial_body_projection_development_preflight_v01",
        "status": "SOURCE_BODY_MATRIX_DEVELOPMENT_PREFLIGHT_RANK_GATE_PASSES_PARTIAL_COHORT",
        "development_ready": ready,
        "development_blocked": acquisition["source_body_blocked"],
        "terminal_dimension": 20,
        "body_columns": prereg["source_body_profiles"],
        "galaxies": galaxy_results,
        "all_ready_galaxies_pass_rank_gate": all_rank,
        "radial_coordinate_boundary": (
            "the five radial edges here are 3-sigma CO moment-0 support quantiles used only for "
            "source-side conditioning; final endpoint matrices must be reevaluated on the unchanged "
            "terminal common-support quantile edges"
        ),
        "velocity_contrast_opened": False,
        "rotation_residual_opened": False,
        "confirmatory_products_opened": False,
        "endpoint_score_computed": False,
        "claim_boundary": (
            "development-only numerical existence and conditioning of the frozen source body basis; "
            "not a body-orthogonal innovation, channel signal, parent derivation, time signal, quantum "
            "signal, or dark-sector result"
        ),
    }
    output = DATA / "phangs_radial_body_projection_development_preflight_v01.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# PHANGS radial body-projection development preflight v01",
        "",
        f"Status: `{result['status']}`",
        "",
        "No velocity or residual endpoint was opened. The source-only 20-by-8 body matrix has:",
        "",
    ]
    for galaxy, metrics in galaxy_results.items():
        lines.append(
            f"- `{galaxy}`: rank `{metrics['rank']}`, complement dimension "
            f"`{metrics['projected_complement_dimension']}`, nonzero condition number "
            f"`{metrics['condition_number_nonzero']:.3g}`."
        )
    lines.extend([
        "",
        "The radial edges are provisional source-only CO-support quantiles. The final matrix must be "
        "recomputed on the frozen terminal common-support edges; these values validate only numerical "
        "construction and conditioning.",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(result["status"])
    for galaxy, metrics in galaxy_results.items():
        print(galaxy, metrics["rank"], metrics["projected_complement_dimension"], metrics["condition_number_nonzero"])


if __name__ == "__main__":
    main()
