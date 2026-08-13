#!/usr/bin/env python3
"""Build an approximate common-HI-resolution NGC4254 source-only cube."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.wcs import WCS

from ngc4254_source_covariance_utils import (
    aips_clean_beam_from_header,
    beam_covariance_pixels,
    matching_kernel,
    normalized_convolution,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
EXTERNAL = ROOT / "data" / "external" / "literature" / "ngc4254_phangs_tracer_velocity"
REPORTS = ROOT / "reports"

FIELDS_PATH = DATA / "ngc4254_baryonic_surface_density_fields_v01.fits"
FIELDS_META_PATH = DATA / "ngc4254_baryonic_surface_density_fields_v01.json"
CO_PATH = next(EXTERNAL.glob("*co21_broad_mom0.fits"))
HI_PATH = EXTERNAL / "ngc4254.viva.mom0.fits"
STELLAR_PATH = EXTERNAL / "NGC4254.stellar.fits"
OUTPUT_PATH = DATA / "ngc4254_common_hi_resolution_source_cube_v03.fits"
JSON_PATH = DATA / "ngc4254_common_hi_resolution_source_cube_v03.json"
REPORT_PATH = REPORTS / "ngc4254_common_hi_resolution_source_cube_v03.md"

STATUS = "COMMON_HI_RESOLUTION_SOURCE_CUBE_BUILT_APPROXIMATE_NOT_ENDPOINT_READY"
CLAIM_BOUNDARY = (
    "source-only beam-matched morphology input with explicit stellar-PSF limitation; "
    "not a complete noise covariance, physical FFL response, channel detection, or endpoint score"
)
MINIMUM_COVERAGE = 0.5
STELLAR_NATIVE_FWHM_CONTROLS_ARCSEC = [0.0, 2.0, 4.0]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def native_circular_covariance(fwhm_arcsec: float, pixel_scale_arcsec: float) -> np.ndarray:
    if fwhm_arcsec == 0.0:
        return np.zeros((2, 2), dtype=float)
    return beam_covariance_pixels(
        fwhm_arcsec, fwhm_arcsec, 0.0, pixel_scale_arcsec
    )


def clean_image_header(source_header, beam: tuple[float, float, float]):
    header = WCS(source_header, naxis=2).to_header()
    header["BUNIT"] = "MSUN/PC2"
    header["BMAJ"] = beam[0] / 3600.0
    header["BMIN"] = beam[1] / 3600.0
    header["BPA"] = beam[2]
    header["TCRES"] = ("HI", "Tau Core common-resolution target")
    return header


def main() -> None:
    with fits.open(FIELDS_PATH) as hdul:
        source_header = hdul["SIGMA_STAR"].header.copy()
        star = np.asarray(hdul["SIGMA_STAR"].data, dtype=float)
        h2 = np.asarray(hdul["SIGMA_H2"].data, dtype=float)
        hi = np.asarray(hdul["SIGMA_HI"].data, dtype=float)
        wcs = WCS(source_header, naxis=2)
    if star.shape != h2.shape or star.shape != hi.shape:
        raise ValueError("Input source fields do not share one grid")

    with fits.open(HI_PATH) as hdul:
        target_beam = aips_clean_beam_from_header(hdul[0].header)
    with fits.open(CO_PATH) as hdul:
        co_beam = aips_clean_beam_from_header(hdul[0].header)
    with fits.open(STELLAR_PATH) as hdul:
        stellar_header_has_beam = all(
            hdul[0].header.get(key) is not None for key in ("BMAJ", "BMIN")
        )
    if stellar_header_has_beam:
        raise ValueError("Stellar-map beam appeared; revise the frozen unknown-PSF policy")
    if not math.isclose(co_beam[0], co_beam[1], rel_tol=0.0, abs_tol=1.0e-9):
        raise ValueError("The frozen CO native beam is expected to be circular")

    pixel_matrix = np.asarray(wcs.pixel_scale_matrix, dtype=float)
    pixel_scale_arcsec = math.sqrt(abs(float(np.linalg.det(pixel_matrix)))) * 3600.0
    target_covariance = beam_covariance_pixels(*target_beam, pixel_scale_arcsec)
    co_native_covariance = native_circular_covariance(co_beam[0], pixel_scale_arcsec)
    co_kernel, co_match_covariance = matching_kernel(
        target_covariance, co_native_covariance
    )
    star_matches = {}
    stellar_controls = []
    for assumed_fwhm in STELLAR_NATIVE_FWHM_CONTROLS_ARCSEC:
        native = native_circular_covariance(assumed_fwhm, pixel_scale_arcsec)
        star_kernel, star_match_covariance = matching_kernel(target_covariance, native)
        star_matched_control, star_coverage_control = normalized_convolution(
            star, star_kernel, minimum_coverage=MINIMUM_COVERAGE
        )
        extension = f"STAR_P{int(round(assumed_fwhm * 10.0)):02d}"
        star_matches[extension] = (star_matched_control, star_coverage_control)
        stellar_controls.append(
            {
                "extension": extension,
                "assumed_native_fwhm_arcsec": assumed_fwhm,
                "matching_covariance_xy_pixels": star_match_covariance.tolist(),
                "kernel_shape_yx": list(star_kernel.shape),
            }
        )
    star_matched, star_coverage = star_matches["STAR_P00"]
    h2_matched, h2_coverage = normalized_convolution(
        h2, co_kernel, minimum_coverage=MINIMUM_COVERAGE
    )
    common = (
        np.logical_and.reduce(
            [np.isfinite(values[0]) for values in star_matches.values()]
        )
        & np.isfinite(h2_matched)
        & np.isfinite(hi)
        & (star_matched > 0.0)
        & ((h2_matched + hi) > 0.0)
    )
    star_matched[~common] = np.nan
    for matched, _ in star_matches.values():
        matched[~common] = np.nan
    h2_matched[~common] = np.nan
    hi_common = np.where(common, hi, np.nan)
    gas_common = h2_matched + hi_common

    header = clean_image_header(source_header, target_beam)
    coverage_header = WCS(source_header, naxis=2).to_header()
    coverage_header["BUNIT"] = "1"
    hdus = [fits.PrimaryHDU()]
    for name, values in (
        ("SIGMA_STAR", star_matched),
        ("SIGMA_H2", h2_matched),
        ("SIGMA_HI", hi_common),
        ("SIGMA_GAS", gas_common),
    ):
        hdus.append(fits.ImageHDU(values.astype("f4"), header=header, name=name))
    for extension, (values, _) in star_matches.items():
        hdus.append(fits.ImageHDU(values.astype("f4"), header=header, name=extension))
    hdus.extend(
        [
            fits.ImageHDU(star_coverage.astype("f4"), header=coverage_header, name="COV_STAR"),
            fits.ImageHDU(h2_coverage.astype("f4"), header=coverage_header, name="COV_H2"),
            fits.ImageHDU(common.astype("u1"), header=coverage_header, name="COMMON"),
        ]
    )
    # The package manifest hashes the complete FITS file. Astropy's generated
    # CHECKSUM strings are not byte-stable across equivalent rewrites here, so
    # omit those redundant cards to preserve exact package reproducibility.
    fits.HDUList(hdus).writeto(OUTPUT_PATH, overwrite=True)

    manifest = {
        "schema": "ngc4254_common_hi_resolution_source_cube_v03",
        "status": STATUS,
        "galaxy": "NGC4254",
        "inputs": {
            "surface_density_fields": str(FIELDS_PATH.relative_to(ROOT)),
            "surface_density_fields_sha256": sha256(FIELDS_PATH),
            "surface_density_metadata": str(FIELDS_META_PATH.relative_to(ROOT)),
            "surface_density_metadata_sha256": sha256(FIELDS_META_PATH),
            "stellar_moment0": str(STELLAR_PATH.relative_to(ROOT)),
            "stellar_moment0_sha256": sha256(STELLAR_PATH),
            "co_moment0": str(CO_PATH.relative_to(ROOT)),
            "co_moment0_sha256": sha256(CO_PATH),
            "hi_moment0": str(HI_PATH.relative_to(ROOT)),
            "hi_moment0_sha256": sha256(HI_PATH),
            "velocity_or_residual_inputs": [],
        },
        "common_grid": {
            "shape_yx": list(star.shape),
            "pixel_scale_arcsec": pixel_scale_arcsec,
            "minimum_normalized_convolution_coverage": MINIMUM_COVERAGE,
            "common_valid_pixels": int(np.count_nonzero(common)),
            "common_valid_fraction": float(np.mean(common)),
        },
        "target_beam": {
            "major_arcsec": target_beam[0],
            "minor_arcsec": target_beam[1],
            "pa_deg_east_of_north": target_beam[2],
            "provenance": "VIVA FITS HISTORY AIPS CLEAN BMAJ/BMIN/BPA",
            "covariance_xy_pixels": target_covariance.tolist(),
        },
        "tracer_matching": {
            "hi": "already at target CLEAN beam; not convolved again",
            "co": {
                "native_beam_arcsec": list(co_beam),
                "matching_covariance_xy_pixels": co_match_covariance.tolist(),
                "kernel_shape_yx": list(co_kernel.shape),
            },
            "stellar": {
                "native_psf_status": "not recorded in supplied FITS header",
                "primary_approximation": "native PSF negligible relative to HI target",
                "mandatory_native_fwhm_controls": stellar_controls,
            },
        },
        "outputs": {
            "common_resolution_cube": str(OUTPUT_PATH.relative_to(ROOT)),
            "common_resolution_cube_sha256": sha256(OUTPUT_PATH),
            "report": str(REPORT_PATH.relative_to(ROOT)),
        },
        "audit_checks": {
            "source_only_moment0_inputs": True,
            "velocity_or_residual_inputs_empty": True,
            "co_matching_covariance_positive_definite": bool(
                np.min(np.linalg.eigvalsh(co_match_covariance)) > 0.0
            ),
            "stellar_control_matching_covariances_positive_definite": bool(
                all(
                    np.min(
                        np.linalg.eigvalsh(
                            np.asarray(row["matching_covariance_xy_pixels"], dtype=float)
                        )
                    )
                    > 0.0
                    for row in stellar_controls
                )
            ),
            "all_common_output_fields_finite_on_common_mask": bool(
                np.isfinite(star_matched[common]).all()
                and np.isfinite(h2_matched[common]).all()
                and np.isfinite(hi_common[common]).all()
            ),
        },
        "complete_measurement_covariance_ready": False,
        "endpoint_scored": False,
        "known_limitations": [
            "stellar native PSF is absent from the supplied FITS header",
            "high-resolution stellar and CO fields were first sampled onto the 5 arcsec VIVA grid in the inherited v01 source cube",
            "normalized convolution handles finite support but is not a measurement-noise model",
            "no moment0 uncertainty maps, calibration covariance, or nonlinear median bootstrap are available",
            "the common-resolution cube does not supply physical eta, kappa_X/kappa_Y, terminal gain, or a role-to-probe identity",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }

    report = f"""# NGC4254 Common H I Resolution Source Cube v03

**Status:** `{STATUS}`

**Claim boundary:** {CLAIM_BOUNDARY}.

The stellar and CO-derived surface-density fields are now convolved on the
common VIVA grid to the exact elliptical H I CLEAN beam
`{target_beam[0]:.3f} x {target_beam[1]:.3f}` arcsec at PA
`{target_beam[2]:.2f}` degrees. H I is retained at its native target beam. The
CO matching kernel subtracts its recorded circular `{co_beam[0]:.3f}` arcsec
native beam in Gaussian covariance space.

The supplied stellar FITS header contains no native PSF. The primary therefore
uses the explicit approximation that it is negligible compared with the H I
beam, while 0, 2, and 4 arcsec circular native-PSF controls are frozen for the
downstream sensitivity pass. This is a declared systematic limitation, not an
estimated error distribution.

The common mask contains `{np.count_nonzero(common)}` pixels. Normalized
convolution requires at least `{MINIMUM_COVERAGE:.1f}` kernel support, but no
moment0 uncertainty maps or calibration covariance are present. The product is
therefore suitable for a beam-matched source-shape sensitivity calculation,
not for a complete covariance or endpoint significance claim.
"""
    REPORT_PATH.write_text(report, encoding="utf-8")
    JSON_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(STATUS)
    print(
        f"common_pixels={np.count_nonzero(common)} "
        f"target_beam={target_beam[0]:.6f}x{target_beam[1]:.6f}@{target_beam[2]:.2f}"
    )


if __name__ == "__main__":
    main()
