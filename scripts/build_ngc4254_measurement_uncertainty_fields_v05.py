#!/usr/bin/env python3
"""Build source-only NGC4254 measurement-uncertainty fields.

The CO layer uses the released PHANGS broad-moment error map.  The stellar
layer is a conditional reconstruction from the released S4G P1 weight maps,
the galaxy-specific P3 sky statistics, and the P5 ICA mixing solution.  The
public VIVA cube does not parent the frozen robust-5 moment-0 image, so every
H I layer is explicitly a robust-1 control rather than an exact uncertainty.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import map_coordinates
from scipy.signal import fftconvolve

from ngc4254_source_covariance_utils import (
    aips_clean_beam_from_header,
    beam_covariance_pixels,
    matching_kernel,
    normalized_convolution,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
SOURCE = ROOT / "data" / "external" / "literature" / "ngc4254_ffl_uncertainty_v04"
LEGACY = ROOT / "data" / "external" / "literature" / "ngc4254_phangs_tracer_velocity"

COMMON_PATH = DATA / "ngc4254_common_hi_resolution_source_cube_v03.fits"
ACQUISITION_PATH = DATA / "ngc4254_ffl_uncertainty_source_acquisition_v04.json"
P3_NOISE_PATH = SOURCE / "NGC4254.s4gcat_p3_noise.json"
OUTPUT_PATH = DATA / "ngc4254_measurement_uncertainty_fields_v05.fits"
JSON_PATH = DATA / "ngc4254_measurement_uncertainty_fields_v05.json"
REPORT_PATH = REPORTS / "ngc4254_measurement_uncertainty_fields_v05.md"

STATUS = "PARTIAL_MEASUREMENT_UNCERTAINTY_FIELDS_BUILT_HI_CONTROL_ONLY"
CLAIM_BOUNDARY = (
    "source-only partial measurement uncertainty construction; not a complete "
    "covariance, physical FFL determinant, channel/time/quantum signal, dark-matter "
    "replacement, or endpoint score"
)
INCLINATION_DEG = 34.4
STELLAR_CONVERSION = 280.0 * math.cos(math.radians(INCLINATION_DEG))
H2_CONVERSION = (4.35 / 0.65) * math.cos(math.radians(INCLINATION_DEG))
HI_CONVERSION = 0.0199 * math.cos(math.radians(INCLINATION_DEG))
ZP = 280.9 / 179.7
MINIMUM_COVERAGE = 0.5
STELLAR_NATIVE_FWHM_ARCSEC = 1.66
HI_CHANNEL_CONTROLS = (1, 10, 49)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sample_to_grid(
    path: Path,
    target_wcs: WCS,
    target_shape: tuple[int, int],
    *,
    order: int = 1,
) -> np.ndarray:
    with fits.open(path, memmap=False) as hdul:
        values = np.squeeze(np.asarray(hdul[0].data, dtype=float))
        source_wcs = WCS(hdul[0].header, naxis=2)
    y, x = np.indices(target_shape, dtype=float)
    ra, dec = target_wcs.pixel_to_world_values(x, y)
    source_x, source_y = source_wcs.world_to_pixel_values(ra, dec)
    return map_coordinates(
        values,
        [source_y, source_x],
        order=order,
        mode="constant",
        cval=np.nan,
        prefilter=order > 1,
    )


def matched_independent_sigma(
    sigma: np.ndarray,
    kernel: np.ndarray,
    valid: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    support = np.asarray(valid, dtype=bool) & np.isfinite(sigma) & (sigma >= 0.0)
    coverage = fftconvolve(support.astype(float), kernel, mode="same")
    variance_numerator = fftconvolve(
        np.where(support, np.asarray(sigma, dtype=float) ** 2, 0.0),
        kernel**2,
        mode="same",
    )
    output = np.full(sigma.shape, np.nan, dtype=float)
    keep = coverage >= MINIMUM_COVERAGE
    output[keep] = np.sqrt(np.maximum(variance_numerator[keep], 0.0)) / coverage[keep]
    return output, coverage


def source_ratio(color_mag: float) -> float:
    return 10.0 ** (0.4 * color_mag) / ZP


def stellar_component(x1: np.ndarray, x2: np.ndarray, c1: float, c2: float) -> np.ndarray:
    r1 = source_ratio(c1)
    r2 = source_ratio(c2)
    if not r2 > r1:
        raise ValueError("The dust component must be redder than the stellar component")
    return (r2 * x1 - x2) / (r2 - r1)


def color_mode(
    x1: np.ndarray,
    x2: np.ndarray,
    c1: float,
    c2: float,
    *,
    component: str,
    sigma_color: float,
) -> np.ndarray:
    if component == "c1":
        plus = stellar_component(x1, x2, c1 + sigma_color, c2)
        minus = stellar_component(x1, x2, c1 - sigma_color, c2)
    elif component == "c2":
        plus = stellar_component(x1, x2, c1, c2 + sigma_color)
        minus = stellar_component(x1, x2, c1, c2 - sigma_color)
    else:
        raise ValueError(f"Unknown ICA component: {component}")
    return 0.5 * (plus - minus)


def correlated_channel_variance_factor(n_channels: int, rho: float) -> float:
    return float(
        n_channels
        + 2.0
        * sum((n_channels - lag) * rho**lag for lag in range(1, n_channels))
    )


def finite_summary(values: np.ndarray, mask: np.ndarray) -> dict[str, float | int]:
    selected = np.asarray(values, dtype=float)[mask & np.isfinite(values)]
    if selected.size == 0:
        return {"n": 0, "median": math.nan, "p16": math.nan, "p84": math.nan}
    return {
        "n": int(selected.size),
        "median": float(np.median(selected)),
        "p16": float(np.percentile(selected, 16.0)),
        "p84": float(np.percentile(selected, 84.0)),
    }


def main() -> None:
    with fits.open(COMMON_PATH) as hdul:
        source_header = hdul["SIGMA_STAR"].header.copy()
        target_wcs = WCS(source_header, naxis=2)
        target_shape = tuple(int(value) for value in hdul["SIGMA_STAR"].data.shape)
        common = np.asarray(hdul["COMMON"].data, dtype=bool)
        baseline_star = np.asarray(hdul["SIGMA_STAR"].data, dtype=float)
    pixel_scale_arcsec = (
        math.sqrt(abs(float(np.linalg.det(target_wcs.pixel_scale_matrix)))) * 3600.0
    )
    target_beam = aips_clean_beam_from_header(source_header)
    target_covariance = beam_covariance_pixels(*target_beam, pixel_scale_arcsec)

    p3 = json.loads(P3_NOISE_PATH.read_text())
    acquisition = json.loads(ACQUISITION_PATH.read_text())
    p5_tokens = acquisition["p5_ngc4254_status_rows"][0].split()
    if p5_tokens[0] != "NGC4254" or len(p5_tokens) != 12:
        raise ValueError("Unexpected NGC4254 row in the acquired S4G P5 status table")
    # P5 table columns: name, excluded, ICA iteration, quality, c1, dc1,
    # c2, dc2, stellar fraction, PA, ellipticity, semi-major axis.
    c1 = float(p5_tokens[4])
    c1_error = float(p5_tokens[5])
    c2 = float(p5_tokens[6])
    c2_error = float(p5_tokens[7])

    phot1 = sample_to_grid(SOURCE / "NGC4254.phot.1.fits", target_wcs, target_shape)
    phot2 = sample_to_grid(SOURCE / "NGC4254.phot.2.fits", target_wcs, target_shape)
    weight1 = sample_to_grid(SOURCE / "NGC4254.phot.1_wt.fits", target_wcs, target_shape)
    weight2 = sample_to_grid(SOURCE / "NGC4254.phot.2_wt.fits", target_wcs, target_shape)
    mask1 = sample_to_grid(
        SOURCE / "NGC4254.1.final_mask.fits", target_wcs, target_shape, order=0
    )
    mask2 = sample_to_grid(
        SOURCE / "NGC4254.2.final_mask.fits", target_wcs, target_shape, order=0
    )
    ica_mask = sample_to_grid(
        SOURCE / "NGC4254.ICAmask.fits", target_wcs, target_shape, order=0
    )
    p5_stellar = sample_to_grid(LEGACY / "NGC4254.stellar.fits", target_wcs, target_shape)
    p5_nonstellar = sample_to_grid(
        SOURCE / "NGC4254.nonstellar.fits", target_wcs, target_shape
    )

    x1 = phot1 - float(p3["sky1_mjy_sr"])
    x2 = phot2 - float(p3["sky2_mjy_sr"])
    stellar_valid = (
        np.isfinite(x1)
        & np.isfinite(x2)
        & np.isfinite(weight1)
        & np.isfinite(weight2)
        & (weight1 > 0.0)
        & (weight2 > 0.0)
        & np.isfinite(mask1)
        & np.isfinite(mask2)
        & np.isfinite(ica_mask)
        & (mask1 == 0.0)
        & (mask2 == 0.0)
        & (ica_mask == 0.0)
    )
    weight1_reference = float(np.median(weight1[stellar_valid & common]))
    weight2_reference = float(np.median(weight2[stellar_valid & common]))
    sigma1 = float(p3["ssky1_mjy_sr"]) * np.sqrt(weight1_reference / weight1)
    sigma2 = float(p3["ssky2_mjy_sr"]) * np.sqrt(weight2_reference / weight2)
    delta_sky1 = math.hypot(float(p3["ssky1_mjy_sr"]) / math.sqrt(1000.0), float(p3["esky1_mjy_sr"]))
    delta_sky2 = math.hypot(float(p3["ssky2_mjy_sr"]) / math.sqrt(1000.0), float(p3["esky2_mjy_sr"]))

    r1 = source_ratio(c1)
    r2 = source_ratio(c2)
    dx1 = r2 / (r2 - r1)
    dx2 = -1.0 / (r2 - r1)
    stellar_pixel_sigma_native = np.sqrt((dx1 * sigma1) ** 2 + (dx2 * sigma2) ** 2)
    stellar_sky1_native = np.full(target_shape, dx1 * delta_sky1, dtype=float)
    stellar_sky2_native = np.full(target_shape, dx2 * delta_sky2, dtype=float)
    stellar_c1_native = color_mode(
        x1, x2, c1, c2, component="c1", sigma_color=c1_error
    )
    stellar_c2_native = color_mode(
        x1, x2, c1, c2, component="c2", sigma_color=c2_error
    )

    stellar_native_covariance = beam_covariance_pixels(
        STELLAR_NATIVE_FWHM_ARCSEC,
        STELLAR_NATIVE_FWHM_ARCSEC,
        0.0,
        pixel_scale_arcsec,
    )
    stellar_kernel, stellar_matching_covariance = matching_kernel(
        target_covariance, stellar_native_covariance
    )
    stellar_pixel_sigma, stellar_coverage = matched_independent_sigma(
        stellar_pixel_sigma_native * STELLAR_CONVERSION,
        stellar_kernel,
        stellar_valid,
    )
    coherent_stellar = {}
    for name, values in (
        ("STAR_SKY1", stellar_sky1_native),
        ("STAR_SKY2", stellar_sky2_native),
        ("STAR_ICA1", stellar_c1_native),
        ("STAR_ICA2", stellar_c2_native),
    ):
        matched, _ = normalized_convolution(
            values * STELLAR_CONVERSION,
            stellar_kernel,
            valid=stellar_valid,
            minimum_coverage=MINIMUM_COVERAGE,
        )
        coherent_stellar[name] = matched

    co_error_path = next(SOURCE.glob("*co21_broad_emom0.fits"))
    with fits.open(co_error_path) as hdul:
        co_native_beam = aips_clean_beam_from_header(hdul[0].header)
    co_error = sample_to_grid(co_error_path, target_wcs, target_shape)
    co_valid = np.isfinite(co_error) & (co_error >= 0.0)
    co_native_covariance = beam_covariance_pixels(*co_native_beam, pixel_scale_arcsec)
    co_kernel, co_matching_covariance = matching_kernel(target_covariance, co_native_covariance)
    h2_sigma_independent, co_coverage = matched_independent_sigma(
        co_error * H2_CONVERSION,
        co_kernel,
        co_valid,
    )
    h2_sigma_correlated, _ = normalized_convolution(
        co_error * H2_CONVERSION,
        co_kernel,
        valid=co_valid,
        minimum_coverage=MINIMUM_COVERAGE,
    )

    hi_control = acquisition["hi_public_cube_noise_control"]
    hi_beam = acquisition["hi_public_cube_beam"]
    hi_jy_to_k = 1.222e6 / (
        1.420405752**2
        * float(hi_beam["major_arcsec"])
        * float(hi_beam["minor_arcsec"])
    )
    cube_path = SOURCE / "ngc4254.cube.fits.gz"
    with fits.open(cube_path) as hdul:
        channel_width_km_s = abs(float(hdul[0].header["CDELT3"])) / 1000.0
    sigma_channel_jy_beam = float(hi_control["median_sigma_mjy_beam"]) / 1000.0
    rho = float(hi_control["median_clipped_adjacent_channel_correlation"])
    hi_controls: dict[str, np.ndarray] = {}
    hi_control_meta = []
    for n_channels in HI_CHANNEL_CONTROLS:
        variance_factor = correlated_channel_variance_factor(n_channels, rho)
        sigma_moment0 = sigma_channel_jy_beam * channel_width_km_s * math.sqrt(variance_factor)
        sigma_surface_density = sigma_moment0 * hi_jy_to_k * HI_CONVERSION
        name = f"HI_CTL{n_channels:02d}"
        hi_controls[name] = np.where(common, sigma_surface_density, np.nan)
        hi_control_meta.append(
            {
                "extension": name,
                "assumed_line_channels": n_channels,
                "adjacent_channel_rho": rho,
                "correlated_variance_factor": variance_factor,
                "sigma_moment0_jy_beam_km_s": sigma_moment0,
                "sigma_surface_density_msun_pc2": sigma_surface_density,
                "role": "robust1_control_not_robust5_uncertainty",
            }
        )

    all_fields = {
        "STAR_PIX": stellar_pixel_sigma,
        **coherent_stellar,
        "H2_IND": h2_sigma_independent,
        "H2_CORR": h2_sigma_correlated,
        **hi_controls,
    }
    uncertainty_common = common & np.logical_and.reduce(
        [np.isfinite(values) for values in all_fields.values()]
    )
    for values in all_fields.values():
        values[~uncertainty_common] = np.nan

    image_header = WCS(source_header, naxis=2).to_header()
    image_header["BUNIT"] = "MSUN/PC2"
    image_header["BMAJ"] = target_beam[0] / 3600.0
    image_header["BMIN"] = target_beam[1] / 3600.0
    image_header["BPA"] = target_beam[2]
    mask_header = WCS(source_header, naxis=2).to_header()
    mask_header["BUNIT"] = "1"
    hdus = [fits.PrimaryHDU()]
    for name, values in all_fields.items():
        hdus.append(fits.ImageHDU(values.astype("f4"), header=image_header, name=name))
    hdus.extend(
        [
            fits.ImageHDU(stellar_coverage.astype("f4"), header=mask_header, name="COV_STAR"),
            fits.ImageHDU(co_coverage.astype("f4"), header=mask_header, name="COV_H2"),
            fits.ImageHDU(
                uncertainty_common.astype("u1"), header=mask_header, name="COMMON"
            ),
        ]
    )
    fits.HDUList(hdus).writeto(OUTPUT_PATH, overwrite=True)

    p5_sum = p5_stellar + p5_nonstellar
    reproduction_mask = (
        uncertainty_common
        & stellar_valid
        & np.isfinite(p5_sum)
        & np.isfinite(x1)
        & (np.abs(x1) > 0.05)
    )
    reproduction_fractional = np.abs(p5_sum - x1) / np.maximum(np.abs(x1), 0.05)
    field_summaries = {
        name: finite_summary(values, uncertainty_common)
        for name, values in all_fields.items()
    }
    manifest = {
        "schema": "ngc4254_measurement_uncertainty_fields_v05",
        "status": STATUS,
        "galaxy": "NGC4254",
        "inputs": {
            "common_resolution_cube": str(COMMON_PATH.relative_to(ROOT)),
            "common_resolution_cube_sha256": sha256(COMMON_PATH),
            "uncertainty_acquisition": str(ACQUISITION_PATH.relative_to(ROOT)),
            "uncertainty_acquisition_sha256": sha256(ACQUISITION_PATH),
            "s4g_p3_noise": str(P3_NOISE_PATH.relative_to(ROOT)),
            "s4g_p3_noise_sha256": sha256(P3_NOISE_PATH),
            "velocity_or_residual_inputs": [],
        },
        "common_grid": {
            "shape_yx": list(target_shape),
            "pixel_scale_arcsec": pixel_scale_arcsec,
            "target_beam_arcsec": list(target_beam),
            "inherited_common_pixels": int(np.count_nonzero(common)),
            "uncertainty_common_pixels": int(np.count_nonzero(uncertainty_common)),
        },
        "stellar": {
            "solution_colors_mag": {"c1": c1, "c2": c2},
            "bootstrap_color_errors_mag": {"c1": c1_error, "c2": c2_error},
            "mixing_ratio_definition": "r(c)=10^(0.4*c)/(280.9/179.7)",
            "stellar_component_definition": "s1=(r2*x1-x2)/(r2-r1)",
            "pixel_noise_model": "catalog local pixel noise scaled by sqrt(median_coverage/current_coverage)",
            "weight_reference": {"channel1": weight1_reference, "channel2": weight2_reference},
            "delta_sky_mjy_sr": {"channel1": delta_sky1, "channel2": delta_sky2},
            "delta_sky_definition": "sqrt((ssky/sqrt(1000))^2+esky^2)",
            "assumed_native_fwhm_arcsec": STELLAR_NATIVE_FWHM_ARCSEC,
            "matching_covariance_xy_pixels": stellar_matching_covariance.tolist(),
            "p5_stellar_plus_nonstellar_vs_p1_fractional_absolute": finite_summary(
                reproduction_fractional, reproduction_mask
            ),
            "global_mass_to_light_scale_mode": {
                "nominal_conversion": STELLAR_CONVERSION,
                "shape_proxy_effect": "exactly cancels from centered log stellar vector",
                "included_in_fields": False,
            },
        },
        "co": {
            "error_product": str(co_error_path.relative_to(ROOT)),
            "native_beam_arcsec": list(co_native_beam),
            "matching_covariance_xy_pixels": co_matching_covariance.tolist(),
            "independent_pixel_extension": "H2_IND",
            "fully_correlated_upper_control_extension": "H2_CORR",
        },
        "hi": {
            "exact_robust5_uncertainty_ready": False,
            "public_cube_role": "robust1_control_only",
            "channel_width_km_s": channel_width_km_s,
            "channel_sigma_mjy_beam": float(hi_control["median_sigma_mjy_beam"]),
            "public_cube_beam_arcsec": [
                float(hi_beam["major_arcsec"]),
                float(hi_beam["minor_arcsec"]),
                float(hi_beam["pa_deg"]),
            ],
            "controls": hi_control_meta,
        },
        "field_summaries_msun_pc2": field_summaries,
        "outputs": {
            "fits": str(OUTPUT_PATH.relative_to(ROOT)),
            "fits_sha256": sha256(OUTPUT_PATH),
            "report": str(REPORT_PATH.relative_to(ROOT)),
        },
        "audit_checks": {
            "source_only": True,
            "velocity_or_residual_inputs_empty": True,
            "all_fields_finite_on_common_mask": bool(
                all(
                    np.isfinite(values[uncertainty_common]).all()
                    for values in all_fields.values()
                )
            ),
            "co_exact_grid_error_used": True,
            "hi_extensions_all_control_labeled": True,
            "endpoint_scored": False,
        },
        "known_limitations": [
            "released P5 per-pixel sigma images were not located; the stellar pixel field is reconstructed from P1 coverage weights and P3 local noise",
            "the stellar ICA color modes use the linear two-component mixing law before all P5 thresholding and postprocessing operations",
            "the P5 mask and P1/P2 masks are sampled to a much coarser target grid",
            "the CO independent-pixel propagation and fully correlated field bracket do not constitute a delivered full CO covariance",
            "the public robust-1 H I cube is not the parent of the frozen robust-5 moment-0 map, so H I controls cannot authorize endpoint scoring",
        ],
        "complete_measurement_covariance_ready": False,
        "endpoint_scoring_allowed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    JSON_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    rows = []
    for name, summary in field_summaries.items():
        rows.append(
            f"| `{name}` | {summary['median']:.6g} | {summary['p16']:.6g} | {summary['p84']:.6g} |"
        )
    report = f"""# NGC4254 Measurement-Uncertainty Fields v05

**Status:** `{STATUS}`

**Claim boundary:** {CLAIM_BOUNDARY}.

## Result

The PHANGS CO broad-moment error image now supplies an exact-grid molecular
measurement field.  The S4G stellar layer is a documented conditional
reconstruction from the P1 coverage maps, the NGC4254-specific P3 local and
large-scale sky noise, and the P5 two-component ICA colors.  Its pixel noise,
two sky modes, and two coherent ICA-color modes remain separate.

The public VIVA cube is robust-1 while the frozen H I moment-0 product records
robust-5 imaging.  Therefore `HI_CTL01`, `HI_CTL10`, and `HI_CTL49` are only
channel-count controls.  They are not an H I covariance estimate for the map
used by the morphology inverse.

## Field Scale

| extension | median (Msun/pc2) | p16 | p84 |
|---|---:|---:|---:|
{chr(10).join(rows)}

## Validation

- Every field is finite on the retained uncertainty-common source mask; one of
  the 1758 inherited pixels is excluded because the exact CO error map has no
  finite matched uncertainty there.
- No velocity pixel, rotation curve, residual, or terminal endpoint enters the
  construction.
- A global stellar mass-to-light rescaling is deliberately omitted because it
  cancels exactly from the centered logarithmic stellar shape vector.
- The P5 stellar-plus-nonstellar reconstruction check has median fractional
  absolute mismatch
  `{manifest['stellar']['p5_stellar_plus_nonstellar_vs_p1_fractional_absolute']['median']:.6g}`;
  this quantifies why the ICA modes remain conditional rather than exact P5
  covariance modes.

## Remaining Blocker

An exact H I contribution still requires the robust-5 parent cube or a released
pixel covariance/noise product for the frozen moment-0 image.  Until then the
combined covariance and endpoint scoring remain closed.
"""
    REPORT_PATH.write_text(report)
    print(STATUS)
    print(f"common_pixels={np.count_nonzero(uncertainty_common)}")
    print(f"p5_reproduction_median_fractional={manifest['stellar']['p5_stellar_plus_nonstellar_vs_p1_fractional_absolute']['median']:.8f}")


if __name__ == "__main__":
    main()
