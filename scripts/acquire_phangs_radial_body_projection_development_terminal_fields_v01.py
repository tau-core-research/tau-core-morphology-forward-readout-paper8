#!/usr/bin/env python3
"""Acquire development-only PHANGS velocity fields for terminal-edge replay."""

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
EXTERNAL = ROOT / "data/external/literature/phangs_radial_body_projection_development_terminal_v01"
PREREG = DATA / "phangs_radial_body_projection_preregistration_v01.json"
SOURCE_ACQUISITION = DATA / "phangs_radial_body_projection_development_source_acquisition_v01.json"
REPORT = ROOT / "reports/phangs_radial_body_projection_development_terminal_acquisition_v01.md"
ALMA_ROOT = "https://almascience.nrao.edu/almadata/lp/PHANGS/phangs_groups"

CONFIRMATORY = {"NGC1300", "NGC1385", "NGC1512", "NGC5068"}
CONFIG = {
    "NGC1087": ("ADP.2021-07-16T10:20:56.350", "NGC1087_MAPS_copt_0.92asec.fits", 231868800, 0.92, "group.uid___A001_X13b3_X90.lp_schinner"),
    "NGC1433": ("ADP.2021-07-16T10:20:56.398", "NGC1433_MAPS_copt_0.91asec.fits", 574395840, 0.91, "group.uid___A001_X136e_X9b.lp_schinner"),
    "NGC1566": ("ADP.2021-07-16T10:20:56.422", "NGC1566_MAPS_copt_0.80asec.fits", 452128320, 0.80, "group.uid___A001_X136e_X9f.lp_schinner"),
    "NGC1672": ("ADP.2021-07-16T10:20:56.434", "NGC1672_MAPS_copt_0.96asec.fits", 372602880, 0.96, "group.uid___A001_X2fb_X272.lp_schinner"),
    "NGC7496": ("ADP.2021-07-16T10:20:56.542", "NGC7496_MAPS_copt_0.89asec.fits", 211412160, 0.89, "group.uid___A001_X1284_X2634.lp_schinner"),
}
ALMA_BYTES = {
    "NGC1087": 1131840,
    "NGC1433": 1932480,
    "NGC1566": 1941120,
    "NGC1672": 544320,
    "NGC7496": 406080,
}

EXPECTED_SHA256 = {
    "NGC1087_MAPS_copt_0.92asec.fits": "9a240962669f8cb77e1e729faf93f2c4f10fb7b6428fa763153815366937f8a1",
    "group.uid___A001_X13b3_X90.lp_schinner.ngc1087_12m7mtp_co21_mom1wprior.fits": "3eb2f08f83180ea942b46af1b55808937164d6d4b2f671b6143a6133dcec9fed",
    "group.uid___A001_X13b3_X90.lp_schinner.ngc1087_12m7mtp_co21_emom1wprior.fits": "246b69b01a117a4d6b05341b0f471fb4d4240c534bf855b869e0bfabe4d0a6be",
    "NGC1433_MAPS_copt_0.91asec.fits": "bb9fe6fca00d755da0f9f3c12a22c4cb4a56ea8b13c664b779ba976eb53fb2b1",
    "group.uid___A001_X136e_X9b.lp_schinner.ngc1433_12m7mtp_co21_mom1wprior.fits": "b32ca44ddc4392e496932a24ef6539b52dca0b8f9275ea8633ea6b7a4a7634d9",
    "group.uid___A001_X136e_X9b.lp_schinner.ngc1433_12m7mtp_co21_emom1wprior.fits": "93e6c1aa21c676b71d640d26db0fbae46a5dfa3a94344a2f7f24cdc17f7303fa",
    "NGC1566_MAPS_copt_0.80asec.fits": "48bed45f7d439c14a9ba0d4cbdbceec58e3c2eb7ceff888c91402421679f6fcc",
    "group.uid___A001_X136e_X9f.lp_schinner.ngc1566_12m7mtp_co21_mom1wprior.fits": "e133173a86f003efae18d11cb4f65db020ed81f137ffa915ce64763da9c559ea",
    "group.uid___A001_X136e_X9f.lp_schinner.ngc1566_12m7mtp_co21_emom1wprior.fits": "bfc8d666ab47516f0a0b545e9beee59ebec438d6c734e7c6692690d021f555c2",
    "NGC1672_MAPS_copt_0.96asec.fits": "f73b131bf19775955e917e2ad93f3bfcd4316d1eaaf929c11b2c38f7c2eac927",
    "group.uid___A001_X2fb_X272.lp_schinner.ngc1672_12m7mtp_co21_mom1wprior.fits": "6f7c825ba8c55412886c79635fd235821ee00464cdd2de015c1f87022686147c",
    "group.uid___A001_X2fb_X272.lp_schinner.ngc1672_12m7mtp_co21_emom1wprior.fits": "be662b3f5009dda3d549d3d0d0870130a4159e0250dcbc69a4ae70c811f09d4f",
    "NGC7496_MAPS_copt_0.89asec.fits": "34c88581ac87ef6c23889974f8c38c8f14deab1fc05634c1974a783a221750d6",
    "group.uid___A001_X1284_X2634.lp_schinner.ngc7496_12m7mtp_co21_mom1wprior.fits": "16e64552d7c88c0fc2101c25b3c8b4dc6c587747a90c43f53851def6dbd3e8ec",
    "group.uid___A001_X1284_X2634.lp_schinner.ngc7496_12m7mtp_co21_emom1wprior.fits": "acf8d5cec09ac04ba32d4605ef0f3f3e5e2f174cae134591c00e1a8b88c240b6",
}


@dataclass(frozen=True)
class Product:
    galaxy: str
    role: str
    filename: str
    url: str
    expected_bytes: int


def products(galaxy: str) -> list[Product]:
    adp, maps, maps_bytes, _, group = CONFIG[galaxy]
    result = [
        Product(
            galaxy,
            "PHANGS_MUSE_Halpha_flux_velocity_and_errors",
            maps,
            f"https://dataportal.eso.org/dataPortal/file/{adp}",
            maps_bytes,
        )
    ]
    for suffix, role in (
        ("mom1wprior", "PHANGS_ALMA_CO21_velocity"),
        ("emom1wprior", "PHANGS_ALMA_CO21_velocity_error"),
    ):
        filename = f"{group}.{galaxy.lower()}_12m7mtp_co21_{suffix}.fits"
        result.append(Product(galaxy, role, filename, f"{ALMA_ROOT}/{group}/{filename}", ALMA_BYTES[galaxy]))
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download_resumable(product: Product, destination: Path) -> str:
    if destination.exists() and destination.stat().st_size == product.expected_bytes:
        return "reused_verified_size"
    partial = destination.with_suffix(destination.suffix + ".part")
    start = partial.stat().st_size if partial.exists() else 0
    headers = {"User-Agent": "paper8-development-terminal-acquisition/1.0"}
    if start:
        headers["Range"] = f"bytes={start}-"
    request = urllib.request.Request(product.url, headers=headers)
    with urllib.request.urlopen(request, timeout=300) as response:
        resumed = start > 0 and response.status == 206
        mode = "ab" if resumed else "wb"
        if start and not resumed:
            start = 0
        with partial.open(mode) as handle:
            while block := response.read(4 * 1024 * 1024):
                handle.write(block)
    if partial.stat().st_size != product.expected_bytes:
        raise RuntimeError(
            f"Unexpected size for {product.filename}: {partial.stat().st_size} != {product.expected_bytes}"
        )
    partial.replace(destination)
    return "resumed" if start else "downloaded"


def validate_product(product: Product, path: Path) -> dict[str, Any]:
    with fits.open(path, memmap=True) as hdul:
        if product.role.startswith("PHANGS_MUSE"):
            required = ("HA6562_FLUX", "HA6562_FLUX_ERR", "HA6562_VEL", "HA6562_VEL_ERR")
            missing = [name for name in required if name not in hdul]
            if missing:
                raise RuntimeError(f"Missing MUSE extensions in {path}: {missing}")
            return {"shape": list(hdul["HA6562_VEL"].data.shape), "required_extensions": list(required)}
        image = hdul[0].data
        header = hdul[0].header
        return {
            "shape": list(image.shape),
            "beam_arcsec": [float(header["BMAJ"]) * 3600.0, float(header["BMIN"]) * 3600.0],
        }


def main() -> None:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    source = json.loads(SOURCE_ACQUISITION.read_text(encoding="utf-8"))
    development = source["source_body_ready"]
    if development != ["NGC1087", "NGC1433", "NGC1566", "NGC1672", "NGC7496"]:
        raise RuntimeError("Ready development cohort changed")
    if CONFIRMATORY.intersection(development) or set(development) - set(prereg["pipeline_development_no_claim"]):
        raise RuntimeError("A confirmatory or non-preregistered galaxy entered development acquisition")

    EXTERNAL.mkdir(parents=True, exist_ok=True)
    records = []
    summaries = {}
    for galaxy in development:
        directory = EXTERNAL / galaxy
        directory.mkdir(exist_ok=True)
        for product in products(galaxy):
            destination = directory / product.filename
            action = download_resumable(product, destination)
            actual = sha256(destination)
            expected = EXPECTED_SHA256.get(product.filename)
            if expected is not None and actual != expected:
                raise RuntimeError(f"Source hash changed for {product.filename}: {actual}")
            summaries[f"{galaxy}/{product.filename}"] = validate_product(product, destination)
            records.append({
                "galaxy": galaxy,
                "role": product.role,
                "filename": product.filename,
                "url": product.url,
                "bytes": destination.stat().st_size,
                "sha256": actual,
                "action": action,
                "development_only": True,
                "confirmatory": False,
            })

    ledger = DATA / "phangs_radial_body_projection_development_terminal_ledger_v01.csv"
    with ledger.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    hashes_frozen = len(EXPECTED_SHA256) == len(records)
    manifest = {
        "schema": "phangs_radial_body_projection_development_terminal_acquisition_v01",
        "status": (
            "DEVELOPMENT_TERMINAL_FIELDS_ACQUIRED_HASH_FROZEN" if hashes_frozen
            else "DEVELOPMENT_TERMINAL_FIELDS_ACQUIRED_HASH_FREEZE_PENDING"
        ),
        "development_galaxies": development,
        "confirmatory_galaxies_opened": [],
        "products": summaries,
        "ledger": str(ledger.relative_to(ROOT)),
        "hashes_frozen_in_script": hashes_frozen,
        "velocity_values_opened_for_pipeline_development": True,
        "terminal_edges_computed": False,
        "body_projection_score_computed": False,
        "endpoint_scoring_allowed": False,
        "claim_boundary": (
            "development-only velocity-field acquisition for common-support edge and conditioning replay; "
            "not a confirmatory endpoint, body-orthogonal innovation, physical channel, time, quantum, Tau, "
            "or dark-sector signal"
        ),
    }
    output = DATA / "phangs_radial_body_projection_development_terminal_acquisition_v01.json"
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# PHANGS radial body-projection development terminal acquisition v01\n\n"
        f"Status: `{manifest['status']}`\n\n"
        f"Development-only MUSE Halpha and ALMA CO velocity/error fields were acquired for "
        f"`{', '.join(development)}`. No confirmatory galaxy was requested. The fields may be used "
        "only to replay common-support radial edges and matrix conditioning; no physical endpoint "
        "score is authorized.\n",
        encoding="utf-8",
    )
    print(manifest["status"])


if __name__ == "__main__":
    main()
