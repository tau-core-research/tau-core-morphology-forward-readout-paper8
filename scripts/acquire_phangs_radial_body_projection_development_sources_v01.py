#!/usr/bin/env python3
"""Acquire source-only morphology fields for the radial body projection.

The development cohort is frozen by the v01 preregistration.  This script
downloads only S4G 3.6 micron imaging/masks and PHANGS-ALMA broad CO moment-0
maps.  It never requests a velocity, tracer-contrast, or rotation-residual
product.
"""

from __future__ import annotations

import csv
import hashlib
import json
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
EXTERNAL = ROOT / "data/external/literature/phangs_radial_body_projection_development_v01"
REPORT = ROOT / "reports/phangs_radial_body_projection_development_source_acquisition_v01.md"
PREREG = DATA / "phangs_radial_body_projection_preregistration_v01.json"
SAMPLE = ROOT / "data/external/phangs/phangs_public_sample.csv"

S4G_ROOT = "https://irsa.ipac.caltech.edu/data/SPITZER/S4G/galaxies"
PHANGS_ROOT = "https://almascience.nrao.edu/almadata/lp/PHANGS/phangs_groups"

# These are exact public delivery directories.  Duplicate delivery groups for
# NGC1087/1433/1566 contain numerically identical broad-moment arrays; one
# deterministic representative is frozen here before any velocity endpoint.
CO_GROUP = {
    "NGC1087": "group.uid___A001_X13b3_X90.lp_schinner",
    "NGC1433": "group.uid___A001_X136e_X9b.lp_schinner",
    "NGC1566": "group.uid___A001_X136e_X9f.lp_schinner",
    "NGC1672": "group.uid___A001_X2fb_X272.lp_schinner",
    "NGC7496": "group.uid___A001_X1284_X2634.lp_schinner",
}
EXPECTED_SHA256 = {
    "NGC1087.phot.1.fits": "2011444277dfd329bb9f3ffb44906de5e8e2fa69c3ea2613a46c2d504009e62d",
    "NGC1087.1.final_mask.fits": "ffbfff8512e2bb40414fb57dd8bda6476b3b7c3955d0d43c1d7a263f1ead05e8",
    "group.uid___A001_X13b3_X90.lp_schinner.ngc1087_12m7mtp_co21_broad_mom0.fits": "e261f51c5612f09128215cb95432eb399901d2b5f9efd41744f1d442c4cbeb1f",
    "NGC1365.phot.1.fits": "729ad32f7277e602576389582a60959a0b280ed9d5fc67ff99e5a691376c3a67",
    "NGC1365.1.final_mask.fits": "a5bdacaa8ac75c290227d1a4cbc072b8cc43b58f72d1c409fc6771642d602e6f",
    "NGC1433.phot.1.fits": "2549daa15d1d82d91c29313ecfe85b3be0526f4c4f6b89afb2c4cb1e5ced8e80",
    "NGC1433.1.final_mask.fits": "bee1210f48ccd9272e8946b8d1bb8df7808fd0b18153b6e0791e077fc9b2e598",
    "group.uid___A001_X136e_X9b.lp_schinner.ngc1433_12m7mtp_co21_broad_mom0.fits": "95d254e9cf09e5758b8424181db1dd8239e5deaf180093d17d1334f58b1429ac",
    "NGC1566.phot.1.fits": "d3244d9c9e67f06feb7b42cc821a61f6cc9534470beabef09b3a96053b7d66d1",
    "NGC1566.1.final_mask.fits": "f380e4ac2269fffd4e60b4e78e7b71bb4c9a3ce3a579ac3f36209dbda3576370",
    "group.uid___A001_X136e_X9f.lp_schinner.ngc1566_12m7mtp_co21_broad_mom0.fits": "8cebc677b6416c81958827c25a60bafe0d82a6118814a02ca574db7b6e70fb17",
    "NGC1672.phot.1.fits": "4673569db208bb6c95c2b0fbb3a69f79814c17ab3dae98470370943f9ef3d46b",
    "NGC1672.1.final_mask.fits": "fda08ea058fd48d7553741356cbf1e3ee8b2c96afb453b2d6119af7375459c9a",
    "group.uid___A001_X2fb_X272.lp_schinner.ngc1672_12m7mtp_co21_broad_mom0.fits": "afa585705734105959b7d4aa293892e94728f792f2758de63277c9ec8143457c",
    "NGC7496.phot.1.fits": "93e92f19722bfce99a3100c01dc7a52deec7126d7e1316e7003785e91e3aecba",
    "NGC7496.1.final_mask.fits": "2299a8622cff17e08bf79db7be7f0086e4a534b0473a27d49f4b09da3676950e",
    "group.uid___A001_X1284_X2634.lp_schinner.ngc7496_12m7mtp_co21_broad_mom0.fits": "5b06225655ad6e1d4f91ee28397cd338dce024fb35c29bd3894198f22074a198",
}


@dataclass(frozen=True)
class Product:
    galaxy: str
    family: str
    role: str
    filename: str
    url: str


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(product: Product, destination: Path) -> str:
    if destination.exists() and destination.stat().st_size > 0:
        return "reused_nonempty"
    temporary = destination.with_suffix(destination.suffix + ".part")
    temporary.unlink(missing_ok=True)
    request = urllib.request.Request(
        product.url, headers={"User-Agent": "paper8-source-only-body-acquisition/1.0"}
    )
    last_error: Exception | None = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(request, timeout=180, context=ssl.create_default_context()) as response:
                with temporary.open("wb") as handle:
                    while block := response.read(1024 * 1024):
                        handle.write(block)
            temporary.replace(destination)
            return "downloaded"
        except (TimeoutError, urllib.error.URLError) as error:
            last_error = error
            temporary.unlink(missing_ok=True)
    raise RuntimeError(f"Could not acquire {product.url}") from last_error


def fits_summary(path: Path) -> dict[str, Any]:
    with fits.open(path, memmap=False) as hdul:
        hdu = hdul[0]
        image = np.squeeze(np.asarray(hdu.data, dtype=float))
        header = hdu.header.copy()
        if "A_ORDER" in header:
            for axis in (1, 2):
                key = f"CTYPE{axis}"
                if "-SIP" not in str(header.get(key, "")):
                    header[key] = str(header[key]) + "-SIP"
        wcs = WCS(header, naxis=2)
        finite = np.isfinite(image)
        return {
            "shape": list(image.shape),
            "finite_fraction": float(np.mean(finite)),
            "celestial_wcs": bool(wcs.has_celestial),
            "bunit": str(hdu.header.get("BUNIT", "")),
            "pixel_scale_arcsec": float(
                np.mean(np.abs(proj_plane_pixel_scales(wcs))) * 3600.0
            ),
            "beam_major_arcsec": (
                float(hdu.header["BMAJ"]) * 3600.0 if "BMAJ" in hdu.header else None
            ),
            "beam_minor_arcsec": (
                float(hdu.header["BMIN"]) * 3600.0 if "BMIN" in hdu.header else None
            ),
        }


def products_for(galaxy: str) -> list[Product]:
    products = [
        Product(
            galaxy,
            "S4G_IRAC",
            "masked_3p6um_stellar_morphology_input",
            f"{galaxy}.phot.1.fits",
            f"{S4G_ROOT}/{galaxy}/P1/{galaxy}.phot.1.fits",
        ),
        Product(
            galaxy,
            "S4G_IRAC",
            "foreground_background_mask",
            f"{galaxy}.1.final_mask.fits",
            f"{S4G_ROOT}/{galaxy}/P2/{galaxy}.1.final_mask.fits",
        ),
    ]
    group = CO_GROUP.get(galaxy)
    if group is not None:
        filename = f"{group}.{galaxy.lower()}_12m7mtp_co21_broad_mom0.fits"
        products.append(
            Product(
                galaxy,
                "PHANGS_ALMA_CO21",
                "source_molecular_gas_morphology_input",
                filename,
                f"{PHANGS_ROOT}/{group}/{filename}",
            )
        )
    return products


def main() -> None:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    development = prereg["pipeline_development_no_claim"]
    if set(development) != {
        "NGC1087", "NGC1365", "NGC1433", "NGC1566", "NGC1672", "NGC7496"
    }:
        raise RuntimeError("Development cohort differs from the frozen v01 preregistration")

    sample = pd.read_csv(SAMPLE, skiprows=[1]).set_index("Name")
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    summaries: dict[str, Any] = {}
    for galaxy in development:
        galaxy_dir = EXTERNAL / galaxy
        galaxy_dir.mkdir(exist_ok=True)
        for product in products_for(galaxy):
            destination = galaxy_dir / product.filename
            action = download(product, destination)
            actual_sha256 = sha256(destination)
            if actual_sha256 != EXPECTED_SHA256[product.filename]:
                raise RuntimeError(
                    f"Source hash changed for {product.filename}: {actual_sha256}"
                )
            summary = fits_summary(destination)
            records.append({
                "galaxy": galaxy,
                "family": product.family,
                "role": product.role,
                "filename": product.filename,
                "url": product.url,
                "local_path": str(destination.relative_to(ROOT)),
                "bytes": destination.stat().st_size,
                "sha256": actual_sha256,
                "action": action,
                "velocity_product": False,
                "rotation_residual_product": False,
            })
            summaries[f"{galaxy}/{product.filename}"] = summary

    ledger_path = DATA / "phangs_radial_body_projection_development_source_ledger_v01.csv"
    with ledger_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

    coverage = []
    for galaxy in development:
        available = [row for row in records if row["galaxy"] == galaxy]
        coverage.append({
            "galaxy": galaxy,
            "ra_deg": float(sample.loc[galaxy, "R.A."]),
            "dec_deg": float(sample.loc[galaxy, "Dec."]),
            "s4g_image_acquired": any(row["role"].startswith("masked_3p6um") for row in available),
            "s4g_mask_acquired": any(row["role"] == "foreground_background_mask" for row in available),
            "co_moment0_acquired": any(row["role"] == "source_molecular_gas_morphology_input" for row in available),
            "source_body_ready": len(available) == 3,
            "blocker": (
                None if len(available) == 3 else
                "no NGC1365 broad-moment0 product appears in the indexed PHANGS LP delivery groups"
            ),
        })
    coverage_frame = pd.DataFrame(coverage)
    coverage_path = DATA / "phangs_radial_body_projection_development_source_coverage_v01.csv"
    coverage_frame.to_csv(coverage_path, index=False)

    ready = coverage_frame.loc[coverage_frame.source_body_ready, "galaxy"].tolist()
    blocked = coverage_frame.loc[~coverage_frame.source_body_ready, "galaxy"].tolist()
    manifest = {
        "schema": "phangs_radial_body_projection_development_source_acquisition_v01",
        "status": "SOURCE_ONLY_DEVELOPMENT_FIELDS_ACQUIRED_PARTIAL_COHORT",
        "development_cohort": development,
        "source_body_ready": ready,
        "source_body_blocked": blocked,
        "products_acquired": len(records),
        "product_summaries": summaries,
        "ledger": str(ledger_path.relative_to(ROOT)),
        "coverage": str(coverage_path.relative_to(ROOT)),
        "velocity_products_acquired": 0,
        "velocity_contrast_opened": False,
        "rotation_residual_opened": False,
        "confirmatory_products_requested": False,
        "endpoint_scoring_allowed": False,
        "claim_boundary": (
            "source-only development acquisition and WCS/product audit; not a body-orthogonal "
            "endpoint, channel detection, parent derivation, time signal, quantum signal, or dark-sector result"
        ),
    }
    manifest_path = DATA / "phangs_radial_body_projection_development_source_acquisition_v01.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# PHANGS radial body-projection development-source acquisition v01\n\n"
        f"Status: `{manifest['status']}`\n\n"
        f"Source-only stellar and CO morphology inputs are ready for `{', '.join(ready)}`. "
        f"`{', '.join(blocked)}` remains in the frozen cohort but is blocked because its public "
        "broad CO moment-0 product was not present in the indexed PHANGS large-program delivery. "
        "No replacement galaxy was selected.\n\n"
        "No velocity field, CO-minus-Halpha contrast, rotation residual, or confirmatory product "
        "was requested or opened.\n",
        encoding="utf-8",
    )
    print(manifest["status"])
    print(f"ready={ready}")
    print(f"blocked={blocked}")


if __name__ == "__main__":
    main()
