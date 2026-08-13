#!/usr/bin/env python3
"""Acquire source-native uncertainty inputs for the NGC4254 FFL proxy.

This pass is deliberately residual blind.  It acquires only imaging products,
source masks, source documentation, and the public H I spectral cube needed to
construct measurement uncertainties before any terminal endpoint is opened.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import ssl
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = ROOT / "data" / "external" / "literature" / "ngc4254_ffl_uncertainty_v04"
EXISTING = ROOT / "data" / "external" / "literature" / "ngc4254_phangs_tracer_velocity"
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

MANIFEST_PATH = DATA / "ngc4254_ffl_uncertainty_source_acquisition_v04.json"
LEDGER_PATH = DATA / "ngc4254_ffl_uncertainty_source_ledger_v04.csv"
REPORT_PATH = REPORTS / "ngc4254_ffl_uncertainty_source_acquisition_v04.md"
S4G_P3_NOISE_PATH = EXTERNAL / "NGC4254.s4gcat_p3_noise.json"

STATUS = "SOURCE_UNCERTAINTY_ACQUISITION_PARTIAL_CO_EXACT_HI_CONTROL_STELLAR_INPUTS_READY"
CLAIM_BOUNDARY = (
    "source-native uncertainty acquisition and product-identity audit only; "
    "not a complete covariance, morphology attribution, channel signal, or endpoint score"
)

PHANGS_ROOT = (
    "https://almascience.nrao.edu/almadata/lp/PHANGS/phangs_groups/"
    "group.uid___A001_X2fb_X29a.lp_schinner"
)
S4G_ROOT = "https://irsa.ipac.caltech.edu/data/SPITZER/S4G"
VIVA_ROOT = "https://www.astro.yale.edu/viva"


@dataclass(frozen=True)
class Source:
    family: str
    role: str
    filename: str
    url: str
    expected_bytes: int | None = None
    tls_compatibility_mode: bool = False


SOURCES = [
    Source(
        "PHANGS_ALMA_CO21",
        "pixelwise_broad_moment0_uncertainty",
        "group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_broad_emom0.fits",
        f"{PHANGS_ROOT}/group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_broad_emom0.fits",
        754560,
    ),
    Source(
        "PHANGS_ALMA_CO21",
        "delivery_readme",
        "group.uid___A001_X2fb_X29a.lp_schinner.README.txt",
        f"{PHANGS_ROOT}/group.uid___A001_X2fb_X29a.lp_schinner.README.txt",
    ),
    Source(
        "VIVA_HI",
        "spectral_cube_for_empirical_noise_and_moment_support",
        "ngc4254.cube.fits.gz",
        f"{VIVA_ROOT}/cubes/ngc4254.cube.fits.gz",
        63413775,
        True,
    ),
    Source(
        "VIVA_HI",
        "survey_atlas_and_published_noise_constraint",
        "viva_atlas.pdf",
        f"{VIVA_ROOT}/papers/viva_atlas.pdf",
        tls_compatibility_mode=True,
    ),
    Source(
        "S4G_IRAC",
        "channel1_science_mosaic_before_ica",
        "NGC4254.phot.1.fits",
        f"{S4G_ROOT}/galaxies/NGC4254/P1/NGC4254.phot.1.fits",
        9682560,
    ),
    Source(
        "S4G_IRAC",
        "channel2_science_mosaic_before_ica",
        "NGC4254.phot.2.fits",
        f"{S4G_ROOT}/galaxies/NGC4254/P1/NGC4254.phot.2.fits",
        9535680,
    ),
    Source(
        "S4G_IRAC",
        "channel1_coverage_weight_map",
        "NGC4254.phot.1_wt.fits",
        f"{S4G_ROOT}/galaxies/NGC4254/P1/NGC4254.phot.1_wt.fits",
        9682560,
    ),
    Source(
        "S4G_IRAC",
        "channel2_coverage_weight_map",
        "NGC4254.phot.2_wt.fits",
        f"{S4G_ROOT}/galaxies/NGC4254/P1/NGC4254.phot.2_wt.fits",
        9535680,
    ),
    Source(
        "S4G_IRAC",
        "channel1_foreground_background_mask",
        "NGC4254.1.final_mask.fits",
        f"{S4G_ROOT}/galaxies/NGC4254/P2/NGC4254.1.final_mask.fits",
    ),
    Source(
        "S4G_IRAC",
        "channel2_foreground_background_mask",
        "NGC4254.2.final_mask.fits",
        f"{S4G_ROOT}/galaxies/NGC4254/P2/NGC4254.2.final_mask.fits",
    ),
    Source(
        "S4G_IRAC",
        "channel1_surface_photometry_with_radial_errors",
        "NGC4254.1fr6a_noclean_fin.dat",
        f"{S4G_ROOT}/galaxies/NGC4254/P3/NGC4254.1fr6a_noclean_fin.dat",
    ),
    Source(
        "S4G_IRAC",
        "channel2_surface_photometry_with_radial_errors",
        "NGC4254.2fr6a_noclean_fin.dat",
        f"{S4G_ROOT}/galaxies/NGC4254/P3/NGC4254.2fr6a_noclean_fin.dat",
    ),
    Source(
        "S4G_IRAC",
        "ica_exclusion_and_recursive_solution_mask",
        "NGC4254.ICAmask.fits",
        f"{S4G_ROOT}/galaxies/NGC4254/P5/NGC4254.ICAmask.fits",
        3055680,
    ),
    Source(
        "S4G_IRAC",
        "ica_cleaned_stellar_color_map",
        "NGC4254.colormap.fits",
        f"{S4G_ROOT}/galaxies/NGC4254/P5/NGC4254.colormap.fits",
        3055680,
    ),
    Source(
        "S4G_IRAC",
        "ica_removed_nonstellar_component",
        "NGC4254.nonstellar.fits",
        f"{S4G_ROOT}/galaxies/NGC4254/P5/NGC4254.nonstellar.fits",
        3055680,
    ),
    Source(
        "S4G_IRAC",
        "pipeline_product_and_noise_documentation",
        "pipelines_readme.html",
        f"{S4G_ROOT}/docs/pipelines_readme.html",
    ),
    Source(
        "S4G_IRAC",
        "ica_product_documentation",
        "P5_README.html",
        f"{S4G_ROOT}/docs/P5_README.html",
    ),
    Source(
        "S4G_IRAC",
        "ica_sample_status_table",
        "P5_table.txt",
        f"{S4G_ROOT}/docs/P5_table.txt",
    ),
    Source(
        "SPITZER_IRAC",
        "instrument_psf_and_calibration_documentation",
        "IRAC_Instrument_Handbook.pdf",
        "https://irsa.ipac.caltech.edu/data/SPITZER/docs/irac/iracinstrumenthandbook/IRAC_Instrument_Handbook.pdf",
    ),
    Source(
        "S4G_IRAC",
        "pipeline5_uncertainty_equations_and_validation",
        "Querejeta_2015_S4G_P5_arxiv1410.0009.pdf",
        "https://arxiv.org/pdf/1410.0009",
        2429870,
    ),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(source: Source, destination: Path) -> str:
    if destination.exists() and destination.stat().st_size > 0:
        if source.expected_bytes is None or destination.stat().st_size == source.expected_bytes:
            return "reused_verified_size"
    temporary = destination.with_suffix(destination.suffix + ".part")
    if temporary.exists():
        temporary.unlink()
    request = urllib.request.Request(source.url, headers={"User-Agent": "paper8-source-acquisition/1.0"})
    context = ssl._create_unverified_context() if source.tls_compatibility_mode else None
    with urllib.request.urlopen(request, timeout=180, context=context) as response:
        with temporary.open("wb") as handle:
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                handle.write(block)
    if source.expected_bytes is not None and temporary.stat().st_size != source.expected_bytes:
        raise ValueError(
            f"Unexpected size for {source.filename}: {temporary.stat().st_size} != {source.expected_bytes}"
        )
    temporary.replace(destination)
    return "downloaded"


def fits_summary(path: Path) -> dict[str, Any]:
    # Integer S4G masks carry BSCALE/BZERO cards, which Astropy cannot scale
    # through a memory map. The largest acquired image is still modest enough
    # to inspect in memory during this one-time source audit.
    with fits.open(path, memmap=False) as hdul:
        hdu = hdul[0]
        header = hdu.header
        data = np.asarray(hdu.data)
        finite = np.isfinite(data)
        summary: dict[str, Any] = {
            "shape": list(data.shape),
            "dtype": str(data.dtype),
            "bunit": str(header.get("BUNIT", "")),
            "ctype": [str(header.get(f"CTYPE{index}", "")) for index in range(1, data.ndim + 1)],
            "finite_fraction": float(np.mean(finite)),
        }
        if data.size <= 5_000_000:
            values = np.asarray(data[finite], dtype=float)
            summary.update(
                {
                    "finite_min": float(np.min(values)) if values.size else None,
                    "finite_median": float(np.median(values)) if values.size else None,
                    "finite_max": float(np.max(values)) if values.size else None,
                }
            )
        for key in ("BMAJ", "BMIN", "BPA", "CDELT1", "CDELT2", "CDELT3", "CRVAL3", "CRPIX3"):
            if header.get(key) is not None:
                summary[key.lower()] = float(header[key])
        return summary


def same_spatial_grid(first: Path, second: Path) -> bool:
    with fits.open(first) as a_hdul, fits.open(second) as b_hdul:
        a = a_hdul[0].header
        b = b_hdul[0].header
        keys = ("NAXIS1", "NAXIS2", "CRPIX1", "CRPIX2", "CRVAL1", "CRVAL2", "CDELT1", "CDELT2")
        return all(np.isclose(float(a[key]), float(b[key]), rtol=0.0, atol=1.0e-12) for key in keys)


def aips_clean_beam_arcsec(path: Path) -> dict[str, float]:
    pattern = re.compile(
        r"CLEAN\s+BMAJ=\s*([0-9.Ee+-]+)\s+BMIN=\s*([0-9.Ee+-]+)\s+BPA=\s*([0-9.Ee+-]+)"
    )
    with fits.open(path, memmap=False) as hdul:
        history = hdul[0].header.get("HISTORY", [])
        lines = [history] if isinstance(history, str) else list(history)
    matches = [pattern.search(str(line)) for line in lines]
    matches = [match for match in matches if match is not None]
    if not matches:
        raise ValueError(f"No AIPS CLEAN beam found in {path}")
    match = matches[-1]
    return {
        "major_arcsec": float(match.group(1)) * 3600.0,
        "minor_arcsec": float(match.group(2)) * 3600.0,
        "pa_deg": float(match.group(3)),
    }


def hi_public_cube_noise_control(path: Path) -> dict[str, Any]:
    """Measure a residual-blind noise control outside the moment channel range."""

    with fits.open(path, memmap=False) as hdul:
        cube = np.asarray(hdul[0].data[0], dtype=float)
    if cube.shape != (63, 512, 512):
        raise ValueError(f"Unexpected public VIVA cube shape: {cube.shape}")

    # The frozen moment0 history maps original channels 7--55 into MOMNT.
    # The complement is therefore a source-provenance line-free control set.
    linefree = np.concatenate([np.arange(0, 6), np.arange(55, 63)])
    y, x = np.mgrid[: cube.shape[1], : cube.shape[2]]
    edge = (x < 100) | (x >= 412) | (y < 100) | (y >= 412)
    sigma_jy = []
    for channel in linefree:
        values = cube[channel][edge]
        median = float(np.median(values))
        sigma_jy.append(1.4826 * float(np.median(np.abs(values - median))))

    adjacent_correlations = []
    for first, second in zip(linefree[:-1], linefree[1:]):
        if second != first + 1:
            continue
        first_values = cube[first][edge]
        second_values = cube[second][edge]
        first_median = float(np.median(first_values))
        second_median = float(np.median(second_values))
        first_sigma = 1.4826 * float(np.median(np.abs(first_values - first_median)))
        second_sigma = 1.4826 * float(np.median(np.abs(second_values - second_median)))
        keep = (np.abs(first_values - first_median) < 8.0 * first_sigma) & (
            np.abs(second_values - second_median) < 8.0 * second_sigma
        )
        adjacent_correlations.append(
            float(np.corrcoef(first_values[keep], second_values[keep])[0, 1])
        )

    median_sigma_mjy = 1000.0 * float(np.median(sigma_jy))
    published_sigma_mjy = 0.41
    return {
        "role": "robust1_control_not_robust5_moment0_covariance",
        "linefree_channels_one_based": [int(channel + 1) for channel in linefree],
        "spatial_control": "outer_100_pixel_border_of_512x512_cube",
        "estimator": "1.4826_median_absolute_deviation_per_channel",
        "per_channel_sigma_mjy_beam": [1000.0 * float(value) for value in sigma_jy],
        "median_sigma_mjy_beam": median_sigma_mjy,
        "minimum_sigma_mjy_beam": 1000.0 * float(np.min(sigma_jy)),
        "maximum_sigma_mjy_beam": 1000.0 * float(np.max(sigma_jy)),
        "median_clipped_adjacent_channel_correlation": float(
            np.median(adjacent_correlations)
        ),
        "published_viva_atlas_rms_mjy_beam": published_sigma_mjy,
        "median_to_published_ratio": median_sigma_mjy / published_sigma_mjy,
        "published_value_role": "survey_table_cross_check_for_robust1_cube",
    }


def acquire_s4g_p3_noise_row() -> tuple[dict[str, Any], str]:
    """Freeze the exact NGC4254 P3 sky/noise columns from the IRSA catalog."""

    if S4G_P3_NOISE_PATH.exists():
        return json.loads(S4G_P3_NOISE_PATH.read_text(encoding="utf-8")), "reused"

    from astropy.coordinates import SkyCoord
    import astropy.units as u
    from astroquery.ipac.irsa import Irsa

    columns = "object,ra,dec,sky1,ssky1,esky1,sky2,ssky2,esky2"
    table = Irsa.query_region(
        SkyCoord(184.70677 * u.deg, 14.41649 * u.deg),
        catalog="s4gcat",
        spatial="Cone",
        radius=5.0 * u.arcsec,
        columns=columns,
    )
    rows = [row for row in table if str(row["object"]).strip().upper() == "NGC4254"]
    if len(rows) != 1:
        raise ValueError(f"Expected one NGC4254 S4G catalog row, found {len(rows)}")
    row = rows[0]
    result = {
        "schema": "ngc4254_s4gcat_p3_noise_v01",
        "object": "NGC4254",
        "ra_deg": float(row["ra"]),
        "dec_deg": float(row["dec"]),
        "sky1_mjy_sr": float(row["sky1"]),
        "ssky1_mjy_sr": float(row["ssky1"]),
        "esky1_mjy_sr": float(row["esky1"]),
        "sky2_mjy_sr": float(row["sky2"]),
        "ssky2_mjy_sr": float(row["ssky2"]),
        "esky2_mjy_sr": float(row["esky2"]),
        "catalog": "IRSA S4G Catalog (s4gcat)",
        "query": (
            "SELECT object,ra,dec,sky1,ssky1,esky1,sky2,ssky2,esky2 FROM s4gcat "
            "WITHIN 5 arcsec OF ICRS(184.70677,14.41649)"
        ),
        "catalog_documentation_url": (
            "https://irsa.ipac.caltech.edu/data/SPITZER/S4G/gator_docs/s4g_colDescriptions.html"
        ),
    }
    S4G_P3_NOISE_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result, "queried_and_normalized"


def main() -> None:
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    records = []
    product_summaries: dict[str, Any] = {}
    for source in SOURCES:
        destination = EXTERNAL / source.filename
        action = download(source, destination)
        record = {
            "family": source.family,
            "role": source.role,
            "filename": source.filename,
            "url": source.url,
            "local_path": str(destination.relative_to(ROOT)),
            "bytes": destination.stat().st_size,
            "sha256": sha256(destination),
            "action": action,
            "tls_compatibility_mode": source.tls_compatibility_mode,
        }
        records.append(record)
        if destination.suffix.lower() in (".fits", ".gz") and (
            destination.name.endswith(".fits") or destination.name.endswith(".fits.gz")
        ):
            product_summaries[source.filename] = fits_summary(destination)

    s4g_p3_noise, p3_action = acquire_s4g_p3_noise_row()
    records.append(
        {
            "family": "S4G_IRAC",
            "role": "galaxy_specific_p3_sky_and_noise_row",
            "filename": S4G_P3_NOISE_PATH.name,
            "url": s4g_p3_noise["catalog_documentation_url"],
            "local_path": str(S4G_P3_NOISE_PATH.relative_to(ROOT)),
            "bytes": S4G_P3_NOISE_PATH.stat().st_size,
            "sha256": sha256(S4G_P3_NOISE_PATH),
            "action": p3_action,
            "tls_compatibility_mode": False,
        }
    )

    existing_co = EXISTING / "group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_broad_mom0.fits"
    acquired_co_error = EXTERNAL / "group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_broad_emom0.fits"
    existing_stellar = EXISTING / "NGC4254.stellar.fits"
    existing_hi_moment0 = EXISTING / "ngc4254.viva.mom0.fits"
    acquired_hi_cube = EXTERNAL / "ngc4254.cube.fits.gz"
    if not existing_co.exists() or not existing_stellar.exists() or not existing_hi_moment0.exists():
        raise FileNotFoundError("An already frozen CO, H I, or S4G source product is missing")

    co_grid_match = same_spatial_grid(existing_co, acquired_co_error)
    if not co_grid_match:
        raise ValueError("PHANGS broad moment0 and broad emom0 grids differ")

    p5_table = (EXTERNAL / "P5_table.txt").read_text(encoding="utf-8", errors="replace")
    p5_ngc4254_rows = [line.strip() for line in p5_table.splitlines() if "NGC4254" in line.upper()]
    if not p5_ngc4254_rows:
        raise ValueError("NGC4254 is absent from the acquired P5 status table")

    hi_public_cube_beam = aips_clean_beam_arcsec(acquired_hi_cube)
    hi_frozen_moment0_beam = aips_clean_beam_arcsec(existing_hi_moment0)
    hi_noise_control = hi_public_cube_noise_control(acquired_hi_cube)
    hi_exact_parent_cube = all(
        np.isclose(hi_public_cube_beam[key], hi_frozen_moment0_beam[key], rtol=0.0, atol=1.0e-5)
        for key in ("major_arcsec", "minor_arcsec", "pa_deg")
    )
    if hi_exact_parent_cube:
        raise ValueError("Expected the public robust-1 cube and robust-5 moment0 beam audit to differ")

    ledger_fields = list(records[0].keys())
    with LEDGER_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ledger_fields)
        writer.writeheader()
        writer.writerows(records)

    manifest = {
        "schema": "ngc4254_ffl_uncertainty_source_acquisition_v04",
        "status": STATUS,
        "galaxy": "NGC4254",
        "source_products_acquired": len(records),
        "co_pixelwise_moment0_uncertainty_acquired": True,
        "co_error_map_matches_frozen_moment0_grid": co_grid_match,
        "hi_public_spectral_cube_acquired": True,
        "hi_public_cube_role": "nonidentical_noise_and_channel_correlation_control",
        "hi_public_cube_beam": hi_public_cube_beam,
        "hi_frozen_moment0_beam": hi_frozen_moment0_beam,
        "hi_public_cube_is_exact_parent_of_frozen_moment0": hi_exact_parent_cube,
        "hi_public_cube_noise_control": hi_noise_control,
        "hi_pixelwise_moment0_uncertainty_acquired": False,
        "hi_exact_moment0_uncertainty_construction_now_possible": False,
        "hi_control_uncertainty_construction_now_possible": True,
        "hi_exact_parent_blocker": (
            "the public cube is robust=1 with a different CLEAN beam, while the frozen moment0 "
            "history identifies a robust=5, 8 klambda UV-tapered parent cube; that exact parent "
            "cube or a source-native moment0 error map is not exposed in the public archive index"
        ),
        "stellar_pixelwise_p5_uncertainty_acquired": False,
        "stellar_uncertainty_inputs_acquired": {
            "pre_ica_channel_maps": True,
            "coverage_weight_maps": True,
            "foreground_background_masks": True,
            "radial_photometric_errors": True,
            "ica_mask": True,
            "ica_color_map": True,
            "removed_nonstellar_component": True,
            "instrument_psf_documentation": True,
            "galaxy_specific_p3_sky_and_noise": True,
        },
        "s4g_p3_noise_row": s4g_p3_noise,
        "existing_frozen_products": {
            "co_broad_moment0": str(existing_co.relative_to(ROOT)),
            "co_broad_moment0_sha256": sha256(existing_co),
            "s4g_p5_stellar": str(existing_stellar.relative_to(ROOT)),
            "s4g_p5_stellar_sha256": sha256(existing_stellar),
        },
        "p5_ngc4254_status_rows": p5_ngc4254_rows,
        "products": product_summaries,
        "ledger": str(LEDGER_PATH.relative_to(ROOT)),
        "ledger_sha256": sha256(LEDGER_PATH),
        "velocity_or_residual_inputs": [],
        "endpoint_scoring_allowed": False,
        "next_construction": (
            "derive the exact CO uncertainty field and a documented stellar uncertainty construction; "
            "use the robust-1 H I cube only as a noise/correlation control while requesting or locating "
            "the robust-5 parent cube before any exact H I covariance claim"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    family_counts: dict[str, int] = {}
    for record in records:
        family_counts[record["family"]] = family_counts.get(record["family"], 0) + 1
    report = [
        "# NGC4254 FFL uncertainty-source acquisition v04",
        "",
        f"Status: `{STATUS}`",
        "",
        "This residual-blind pass acquired the source products required to replace the v03 equal-weight source scenarios with measurement-informed uncertainty constructions. No observed rotation endpoint, dark-discrepancy residual, or terminal score was read.",
        "",
        "## Acquired source families",
        "",
    ]
    report.extend(f"- `{family}`: {count} products" for family, count in sorted(family_counts.items()))
    report.extend(
        [
            "",
            "## What is now available",
            "",
            "- CO: the official PHANGS `broad_emom0` map is acquired and exactly matches the frozen `broad_mom0` spatial grid.",
            "- H I: the public VIVA spectral cube is acquired, but its robust-1 CLEAN beam differs from the robust-5, UV-tapered beam recorded in the frozen moment-0 history. It is therefore a noise/channel-correlation control only. The exact parent cube or a source-native moment-0 error map remains missing; the atlas noise value is also only a cross-check.",
            f"- H I control check: the outer-field line-free channels give median robust noise `{hi_noise_control['median_sigma_mjy_beam']:.3f}` mJy/beam versus the VIVA atlas value `{hi_noise_control['published_viva_atlas_rms_mjy_beam']:.2f}` mJy/beam, with median clipped adjacent-channel correlation `{hi_noise_control['median_clipped_adjacent_channel_correlation']:.3f}`. These values characterize the nonidentical robust-1 control cube only.",
            "- Stellar: the P1 channel mosaics, coverage maps, P2 masks, P3 radial-error profiles, P5 ICA mask/color/nonstellar products, and IRAC handbook are acquired. S4G does not distribute a P5 pixelwise stellar uncertainty map in this product directory, so the uncertainty must be constructed and kept separate from the global mass-to-light scale.",
            "",
            "## Claim boundary",
            "",
            CLAIM_BOUNDARY + ".",
            "",
            f"Machine-readable manifest: `{MANIFEST_PATH.relative_to(ROOT)}`.",
            f"Source ledger: `{LEDGER_PATH.relative_to(ROOT)}`.",
        ]
    )
    REPORT_PATH.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(STATUS)
    print(f"acquired_products={len(records)}")
    print(f"co_grid_match={co_grid_match}")


if __name__ == "__main__":
    main()
