#!/usr/bin/env python3
"""Acquire and hash-freeze the unopened PHANGS confirmatory packet."""

from __future__ import annotations

import csv
import hashlib
import json
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
EXTERNAL = ROOT / "data/external/literature/phangs_radial_body_projection_confirmatory_v01"
PREREGISTRATION = DATA / "phangs_radial_body_projection_preregistration_v01.json"
CONTRACT = DATA / "phangs_radial_body_projection_scoring_contract_v01.json"
MANIFEST = DATA / "phangs_radial_body_projection_confirmatory_acquisition_v01.json"
LEDGER = DATA / "phangs_radial_body_projection_confirmatory_acquisition_ledger_v01.csv"
REPORT = ROOT / "reports/phangs_radial_body_projection_confirmatory_acquisition_v01.md"

S4G_ROOT = "https://irsa.ipac.caltech.edu/data/SPITZER/S4G/galaxies"
ALMA_ROOT = "https://almascience.nrao.edu/almadata/lp/PHANGS/phangs_groups"
CONFIRMATORY = ["NGC1300", "NGC1385", "NGC1512", "NGC5068"]
CONFIG = {
    "NGC1300": {
        "muse_adp": "ADP.2021-07-16T10:20:56.362",
        "muse_file": "NGC1300_MAPS_copt_0.89asec.fits",
        "muse_bytes": 564166080,
        "muse_psf_arcsec": 0.89,
        "alma_group": "group.uid___A001_X136d_X13b.lp_schinner",
    },
    "NGC1385": {
        "muse_adp": "ADP.2021-07-16T10:20:56.386",
        "muse_file": "NGC1385_MAPS_copt_0.77asec.fits",
        "muse_bytes": 232021440,
        "muse_psf_arcsec": 0.77,
        "alma_group": "group.uid___A001_X136d_X133.lp_schinner",
    },
    "NGC1512": {
        "muse_adp": "ADP.2021-07-16T10:20:56.410",
        "muse_file": "NGC1512_MAPS_copt_1.25asec.fits",
        "muse_bytes": 348638400,
        "muse_psf_arcsec": 1.25,
        "alma_group": "group.uid___A001_X136d_X137.lp_schinner",
    },
    "NGC5068": {
        "muse_adp": "ADP.2021-07-16T10:20:56.530",
        "muse_file": "NGC5068_MAPS_copt_1.04asec.fits",
        "muse_bytes": 591641280,
        "muse_psf_arcsec": 1.04,
        "alma_group": "group.uid___A001_X2fe_X329.lp_schinner",
    },
}


@dataclass(frozen=True)
class Product:
    galaxy: str
    family: str
    role: str
    filename: str
    url: str
    terminal: bool
    expected_bytes: int | None = None


def products(galaxy: str) -> list[Product]:
    config = CONFIG[galaxy]
    group = str(config["alma_group"])
    stem = f"{group}.{galaxy.lower()}_12m7mtp_co21"
    return [
        Product(
            galaxy, "S4G_IRAC", "masked_3p6um_stellar_morphology_input",
            f"{galaxy}.phot.1.fits", f"{S4G_ROOT}/{galaxy}/P1/{galaxy}.phot.1.fits", False,
        ),
        Product(
            galaxy, "S4G_IRAC", "foreground_background_mask",
            f"{galaxy}.1.final_mask.fits", f"{S4G_ROOT}/{galaxy}/P2/{galaxy}.1.final_mask.fits", False,
        ),
        Product(
            galaxy, "PHANGS_ALMA_CO21", "source_molecular_gas_morphology_input",
            f"{stem}_broad_mom0.fits", f"{ALMA_ROOT}/{group}/{stem}_broad_mom0.fits", False,
        ),
        Product(
            galaxy, "PHANGS_MUSE", "Halpha_flux_velocity_and_errors",
            str(config["muse_file"]),
            f"https://dataportal.eso.org/dataPortal/file/{config['muse_adp']}", True,
            int(config["muse_bytes"]),
        ),
        Product(
            galaxy, "PHANGS_ALMA_CO21", "CO21_velocity",
            f"{stem}_mom1wprior.fits", f"{ALMA_ROOT}/{group}/{stem}_mom1wprior.fits", True,
        ),
        Product(
            galaxy, "PHANGS_ALMA_CO21", "CO21_velocity_error",
            f"{stem}_emom1wprior.fits", f"{ALMA_ROOT}/{group}/{stem}_emom1wprior.fits", True,
        ),
    ]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(product: Product, destination: Path) -> str:
    if destination.exists() and destination.stat().st_size > 0:
        return "reused_nonempty"
    partial = destination.with_suffix(destination.suffix + ".part")
    if partial.exists() and partial.stat().st_size > 0:
        try:
            with fits.open(partial, memmap=True, lazy_load_hdus=True) as hdul:
                if len(hdul) == 0:
                    raise OSError("empty FITS container")
            partial.replace(destination)
            return "recovered_complete_partial"
        except OSError:
            partial.unlink()
    request = urllib.request.Request(product.url, headers={"User-Agent": "paper8-confirmatory-preopen/1.0"})
    with urllib.request.urlopen(request, timeout=600) as response, partial.open("wb") as handle:
        while block := response.read(4 * 1024 * 1024):
            handle.write(block)
    partial.replace(destination)
    return "downloaded"


def header_only_summary(product: Product, path: Path) -> dict[str, Any]:
    with fits.open(path, memmap=True, lazy_load_hdus=True) as hdul:
        names = [hdu.name for hdu in hdul]
        if product.family == "PHANGS_MUSE":
            required = ["HA6562_FLUX", "HA6562_FLUX_ERR", "HA6562_VEL", "HA6562_VEL_ERR"]
            missing = [name for name in required if name not in names]
            if missing:
                raise RuntimeError(f"Missing MUSE extensions in {path}: {missing}")
            header = hdul["HA6562_VEL"].header
        else:
            header = hdul[0].header
        shape = [int(header.get(f"NAXIS{axis}", 0)) for axis in range(int(header.get("NAXIS", 0)), 0, -1)]
        return {
            "hdu_names": names,
            "header_shape": shape,
            "bunit": str(header.get("BUNIT", "")),
            "beam_arcsec": (
                [float(header["BMAJ"]) * 3600.0, float(header["BMIN"]) * 3600.0]
                if "BMAJ" in header and "BMIN" in header else None
            ),
            "pixel_array_read": False,
        }


def main() -> None:
    preregistration = json.loads(PREREGISTRATION.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if preregistration["confirmatory_untouched"] != CONFIRMATORY:
        raise RuntimeError("Confirmatory cohort differs from the frozen preregistration")
    if not contract["all_synthetic_checks_pass"] or contract["confirmatory_galaxies_opened"]:
        raise RuntimeError("The pre-open scoring contract is not ready")

    previous_hashes: dict[str, str] = {}
    if MANIFEST.exists():
        previous = json.loads(MANIFEST.read_text(encoding="utf-8"))
        previous_hashes = previous.get("source_hashes_sha256", {})

    EXTERNAL.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    summaries: dict[str, Any] = {}
    frozen_hashes: dict[str, str] = {}
    for galaxy in CONFIRMATORY:
        directory = EXTERNAL / galaxy
        directory.mkdir(exist_ok=True)
        for product in products(galaxy):
            destination = directory / product.filename
            action = download(product, destination)
            actual_hash = sha256(destination)
            key = f"{galaxy}/{product.filename}"
            if key in previous_hashes and previous_hashes[key] != actual_hash:
                raise RuntimeError(f"Frozen confirmatory hash changed for {key}")
            frozen_hashes[key] = actual_hash
            summaries[key] = header_only_summary(product, destination)
            records.append({
                "galaxy": galaxy,
                "family": product.family,
                "role": product.role,
                "filename": product.filename,
                "url": product.url,
                "local_path": str(destination.relative_to(ROOT)),
                "bytes": destination.stat().st_size,
                "archive_reported_bytes": product.expected_bytes,
                "archive_size_matches": (
                    destination.stat().st_size == product.expected_bytes
                    if product.expected_bytes is not None else None
                ),
                "sha256": actual_hash,
                "action": action,
                "terminal_product": product.terminal,
                "pixel_array_read": False,
            })

    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    result = {
        "schema": "phangs_radial_body_projection_confirmatory_acquisition_v01",
        "status": "CONFIRMATORY_PACKET_ACQUIRED_HASH_FROZEN_VALUES_UNOPENED",
        "confirmatory_galaxies": CONFIRMATORY,
        "products_per_galaxy": 6,
        "products_total": len(records),
        "source_hashes_sha256": frozen_hashes,
        "header_only_product_summaries": summaries,
        "ledger": str(LEDGER.relative_to(ROOT)),
        "source_morphology_pixel_values_opened": False,
        "terminal_pixel_values_opened": False,
        "velocity_contrast_constructed": False,
        "terminal_coefficients_fitted": False,
        "endpoint_score_computed": False,
        "replacement_galaxy_allowed": False,
        "next_gate": "build all four source matrices on common terminal-support edges and require every frozen rank/covariance gate before the single score",
        "claim_boundary": (
            "header-only acquisition and hash freeze of the preregistered confirmatory packet; "
            "not an opened endpoint, tracer innovation, channel, time, quantum, Tau, or dark-sector result"
        ),
    }
    MANIFEST.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# PHANGS radial body-projection confirmatory acquisition v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "The exact four-galaxy confirmatory packet is locally acquired and SHA-256 frozen. "
        "Only FITS headers, extension names, file sizes and hashes were inspected. No source "
        "morphology pixel, velocity pixel, tracer contrast, terminal coefficient or score was "
        "opened. The next operation is the all-body eligibility replay under the already frozen "
        "operator; a failed galaxy cannot be replaced or repaired after opening.\n",
        encoding="utf-8",
    )
    print(result["status"], f"products={len(records)}")


if __name__ == "__main__":
    main()
