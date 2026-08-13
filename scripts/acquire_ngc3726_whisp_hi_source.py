#!/usr/bin/env python3
"""Acquire the public WHISP H I packet for source-ranked NGC3726/UGC6537."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
OUT = ROOT / "data" / "external" / "literature" / "ngc3726_whisp_hi_route"
REPORTS = ROOT / "reports"
CANDIDATES = DATA / "ghasp_sparc_source_only_candidate_federation_v01.csv"
BASE = "https://www.astro.rug.nl/~whisp/Database/OverviewCatalog/ListByName/"


def download(url: str) -> tuple[bytes, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "tau-core-source-audit/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read(), response.headers.get_content_type()


def extract(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError(f"missing WHISP metadata pattern: {pattern}")
    return re.sub(r"\s+", " ", match.group(1)).strip()


def main() -> None:
    rows = list(csv.DictReader(CANDIDATES.open(newline="", encoding="utf-8")))
    selected = next(row for row in rows if row["source_only_rank"] == "1")
    if selected["galaxy"] != "NGC3726" or "UGC6537" not in selected["aliases"]:
        raise RuntimeError("Frozen rank-1 source candidate is not NGC3726/UGC6537")

    object_url = urllib.parse.urljoin(BASE, selected["whisp_relative_url"])
    object_payload, object_type = download(object_url)
    object_html = object_payload.decode("latin-1")
    overview_href = extract(r'href\s*=\s*["\']?([^"\' >]+plot[^"\' >]*\.gif)', object_html)
    notes_href = extract(r'href\s*=\s*["\']?([^"\' >]+obsred\.html)', object_html)
    overview_url = urllib.parse.urljoin(object_url, overview_href)
    notes_url = urllib.parse.urljoin(object_url, notes_href)
    overview_payload, overview_type = download(overview_url)
    notes_payload, notes_type = download(notes_url)
    notes_html = notes_payload.decode("latin-1")

    OUT.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    products = [
        ("object_page", object_url, "whisp_ngc3726_object_page.html", object_payload, object_type),
        ("graphical_overview", overview_url, "whisp_ngc3726_overview.gif", overview_payload, overview_type),
        ("observation_notes", notes_url, "whisp_ngc3726_obs_reduction_notes.html", notes_payload, notes_type),
    ]
    manifest = []
    for source_id, url, filename, payload, content_type in products:
        path = OUT / filename
        path.write_bytes(payload)
        manifest.append(
            {
                "source_id": source_id,
                "url": url,
                "local_path": str(path.relative_to(ROOT)),
                "content_type": content_type,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "source_native": True,
                "endpoint_access": False,
            }
        )

    overview_path = OUT / "whisp_ngc3726_overview.gif"
    with Image.open(overview_path) as image:
        image_size = list(image.size)
    metadata = {
        "quality": extract(r"Quality:</font>\s*([^<]+)", notes_html),
        "bandwidth_mhz": float(extract(r"<th>6537</th>\s*<th>([^<]+)</th>", notes_html)),
        "n_channels": int(extract(r"<th>6537</th>\s*<th>[^<]+</th>\s*<th>([^<]+)</th>", notes_html)),
        "central_velocity_km_s": float(extract(r"<th>6537</th>(?:\s*<th>[^<]+</th>){2}\s*<th>([^<]+)</th>", notes_html)),
        "channel_separation_km_s": float(extract(r"<th>6537</th>(?:\s*<th>[^<]+</th>){3}\s*<th>([^<]+)</th>", notes_html)),
        "beam_full_resolution_arcsec": extract(r"<th>6537</th>(?:\s*<th>[^<]+</th>){4}\s*<th>([^<]+)</th>", notes_html),
        "rms_noise_mjy_beam": float(extract(r"<th>6537</th>(?:\s*<th>[^<]+</th>){5}\s*<th>([^<]+)</th>", notes_html)),
        "channel_map_quality": extract(r"Quality Fourier-transformed data\s*\(= channel maps\):</font>\s*([^<]+)", notes_html),
        "cleaned_map_quality": extract(r'Quality "cleaned" channel maps:</font>\s*([^<]+)', notes_html),
    }
    direct_fits = re.findall(
        r'href\s*=\s*["\']?([^"\' >]+\.fits(?:\.gz)?)', object_html, flags=re.IGNORECASE
    )
    result = {
        "schema": "ngc3726_whisp_hi_source_v01",
        "status": "WHISP_NGC3726_GRAPHICAL_HI_VELOCITY_FIELD_ACQUIRED_FITS_OPEN",
        "galaxy": "NGC3726",
        "whisp_name": "UGC6537",
        "source_only_rank": 1,
        "source_only_selection_verified": True,
        "selection_uses_vobs_or_residual": False,
        "metadata": metadata,
        "overview_image_size_pixels": image_size,
        "direct_fits_links_found": direct_fits,
        "source_coordinate_fits_acquired": False,
        "graphical_velocity_field_acquired": True,
        "physical_a_row_constructed": False,
        "endpoint_access": False,
        "claim_boundary": "rank-1 source acquisition only; no calibrated common H I-Halpha coordinates, channel statistic, residual test, or Tau Core validation",
        "manifest": manifest,
    }
    (DATA / "ngc3726_whisp_hi_source_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    with (DATA / "ngc3726_whisp_hi_source_manifest_v01.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0]))
        writer.writeheader()
        writer.writerows(manifest)
    (REPORTS / "ngc3726_whisp_hi_source_v01.md").write_text(
        f"""# NGC3726 / UGC6537 WHISP H I Source Acquisition v0.1

**Status:** `{result['status']}`

NGC3726 was selected before H I inspection as rank 1 in the residual-blind
GHASP-SPARC source federation. Its public WHISP object page, graphical
overview, and observation/reduction notes are now cached with SHA-256
provenance.

| field | value |
| --- | ---: |
| WHISP quality | {metadata['quality']} |
| channels | {metadata['n_channels']} |
| channel separation | {metadata['channel_separation_km_s']} km/s |
| full-resolution beam | {metadata['beam_full_resolution_arcsec']} arcsec |
| cleaned-map rms | {metadata['rms_noise_mjy_beam']} mJy/beam |
| overview size | {image_size[0]} x {image_size[1]} pixels |
| direct FITS links | {len(direct_fits)} |

The source confirms a usable graphical H I route with good observation and
reduction quality. It exposes no direct FITS link, so WCS-calibrated transport,
beam covariance, and a physical common H I-Halpha probe remain open. Endpoint
data were not used or accessed.
""",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
