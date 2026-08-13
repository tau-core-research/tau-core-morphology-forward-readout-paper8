#!/usr/bin/env python3
"""Acquire source-ranked NGC4559 HALOGAS moment maps without opening pixels."""

from __future__ import annotations

import csv
import hashlib
import json
import urllib.request
from pathlib import Path

from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
OUT = ROOT / "data" / "external" / "literature" / "ngc4559_halogas_route"
REPORTS = ROOT / "reports"
RECORD_ID = "2552349"
API = f"https://zenodo.org/api/records/{RECORD_ID}"
FILES = {
    "NGC4559-HR_mom0m.fits": "ac8f435c2367e23801a88b5089464b48",
    "NGC4559-HR_mom1m.fits": "46809fb342f4453dc1ab2ee5bf1d0812",
    "NGC4559-LR_mom0m.fits": "7ab549b63b9c858aa5cdde82e3c1ae82",
    "NGC4559-LR_mom1m.fits": "e27de9b2c5320b05b9181bfea6c0a002",
}


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "tau-core-source-audit/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def main() -> None:
    with (DATA / "ghasp_sparc_source_only_candidate_federation_v01.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        candidate = next(
            row for row in csv.DictReader(handle) if row["source_only_rank"] == "2"
        )
    if candidate["galaxy"] != "NGC4559":
        raise RuntimeError("Frozen rank-2 source candidate is not NGC4559")

    record_payload = download(API)
    record = json.loads(record_payload)
    files_by_name = {item["key"]: item for item in record["files"]}
    OUT.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (OUT / "zenodo_record_2552349.json").write_bytes(record_payload)

    manifest = []
    headers = {}
    for filename, expected_md5 in FILES.items():
        item = files_by_name[filename]
        payload = download(item["links"]["self"])
        actual_md5 = hashlib.md5(payload).hexdigest()
        if actual_md5 != expected_md5:
            raise RuntimeError(f"MD5 mismatch for {filename}")
        path = OUT / filename
        path.write_bytes(payload)
        with fits.open(path, memmap=True, lazy_load_hdus=True) as hdus:
            header = hdus[0].header
            headers[filename] = {
                "naxis": int(header["NAXIS"]),
                "shape": [int(header[f"NAXIS{i}"]) for i in range(1, int(header["NAXIS"]) + 1)],
                "ctype1": header.get("CTYPE1", ""),
                "ctype2": header.get("CTYPE2", ""),
                "cunit1": header.get("CUNIT1", ""),
                "cunit2": header.get("CUNIT2", ""),
                "bunit": header.get("BUNIT", ""),
                "bmaj_deg": header.get("BMAJ"),
                "bmin_deg": header.get("BMIN"),
                "bmaj_arcsec": 3600 * float(header.get("BMAJ")),
                "bmin_arcsec": 3600 * float(header.get("BMIN")),
                "bpa_deg": header.get("BPA"),
            }
        manifest.append(
            {
                "filename": filename,
                "url": item["links"]["self"],
                "local_path": str(path.relative_to(ROOT)),
                "bytes": len(payload),
                "md5": actual_md5,
                "sha256": hashlib.sha256(payload).hexdigest(),
                "source_native": True,
                "pixel_values_opened": False,
                "endpoint_access": False,
            }
        )

    with (DATA / "ngc4559_halogas_moment_source_manifest_v01.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0]))
        writer.writeheader()
        writer.writerows(manifest)
    result = {
        "schema": "ngc4559_halogas_moment_sources_v01",
        "status": "NGC4559_HALOGAS_HR_LR_MOMENT0_MOMENT1_FITS_ACQUIRED_PIXELS_UNOPENED",
        "galaxy": "NGC4559",
        "source_only_rank": 2,
        "zenodo_record": RECORD_ID,
        "record_url": f"https://zenodo.org/records/{RECORD_ID}",
        "headers": headers,
        "n_products": len(manifest),
        "pixel_values_opened": False,
        "cube_downloaded": False,
        "selection_uses_vobs_or_residual": False,
        "sparc_endpoint_opened": False,
        "physical_a_row_constructed": False,
        "claim_boundary": "prospective replication source acquisition only; no moment-map pixel inspection, geometry extraction, H I-Halpha comparison, or channel result",
        "manifest": manifest,
    }
    (DATA / "ngc4559_halogas_moment_sources_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    product_text = "\n".join(
        f"| {name} | {headers[name]['shape']} | {headers[name]['bunit']} | "
        f"{headers[name]['bmaj_arcsec']:.2f} x {headers[name]['bmin_arcsec']:.2f} arcsec |"
        for name in FILES
    )
    (REPORTS / "ngc4559_halogas_moment_sources_v01.md").write_text(
        f"""# NGC4559 HALOGAS Moment Source Acquisition v0.1

**Status:** `{result['status']}`

The source-only GHASP federation selected NGC4559 as rank 2 before any H I
pixel inspection. Four public HALOGAS Data Release 1 FITS products are cached
and verified against the archive MD5 values.

| product | FITS shape | unit | beam |
| --- | --- | --- | --- |
{product_text}

Only FITS headers were opened. Pixel values, SPARC velocities, residuals, and
model scores remain closed. The 415 MB HR/LR cubes were not downloaded because
the moment maps are sufficient to freeze a first WCS, center, beam, annulus,
and major-axis wedge extraction protocol.

Next gate: freeze that extraction protocol from source geometry before reading
the moment-map pixels, then apply the unchanged H I-Halpha odd-contrast
statistic used for NGC3726.
""",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
