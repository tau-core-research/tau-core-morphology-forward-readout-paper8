#!/usr/bin/env python3
"""Acquire the public WHISP UGC06787 graphical H I source packet."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import urllib.request
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "external" / "literature" / "ugc06787_whisp_hi_route"
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
BASE = "https://www.astro.rug.nl/~whisp/Database/OverviewCatalog/ListByName/U6787"
SOURCES = [
    ("object_page", f"{BASE}/u6787p36921.html", "whisp_ugc06787_object_page.html"),
    ("graphical_overview", f"{BASE}/u6787plot36921.gif", "whisp_ugc06787_overview.gif"),
    ("observation_notes", f"{BASE}/u6787p36921obsred.html", "whisp_ugc06787_obs_reduction_notes.html"),
]


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
    OUT.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    manifest = []
    payloads: dict[str, bytes] = {}
    for source_id, url, filename in SOURCES:
        payload, content_type = download(url)
        path = OUT / filename
        path.write_bytes(payload)
        payloads[source_id] = payload
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

    object_html = payloads["object_page"].decode("latin-1")
    notes_html = payloads["observation_notes"].decode("latin-1")
    overview_path = OUT / "whisp_ugc06787_overview.gif"
    with Image.open(overview_path) as image:
        image_size = list(image.size)

    metadata = {
        "quality": extract(r"Quality:</font>\s*([^<]+)", notes_html),
        "bandwidth_mhz": float(extract(r"<th>6787</th>\s*<th>([^<]+)</th>", notes_html)),
        "n_channels": int(extract(r"<th>6787</th>\s*<th>[^<]+</th>\s*<th>([^<]+)</th>", notes_html)),
        "central_velocity_km_s": float(extract(r"<th>6787</th>(?:\s*<th>[^<]+</th>){2}\s*<th>([^<]+)</th>", notes_html)),
        "channel_separation_km_s": float(extract(r"<th>6787</th>(?:\s*<th>[^<]+</th>){3}\s*<th>([^<]+)</th>", notes_html)),
        "beam_full_resolution_arcsec": extract(r"<th>6787</th>(?:\s*<th>[^<]+</th>){4}\s*<th>([^<]+)</th>", notes_html),
        "rms_noise_mjy_beam": float(extract(r"<th>6787</th>(?:\s*<th>[^<]+</th>){5}\s*<th>([^<]+)</th>", notes_html)),
        "channel_map_quality": extract(r'Quality Fourier-transformed data\s*\(= channel maps\):</font>\s*([^<]+)', notes_html),
        "cleaned_map_quality": extract(r'Quality "cleaned" channel maps:</font>\s*([^<]+)', notes_html),
        "cleaned_map_note": extract(r'Notes on "cleaned" channel maps:</font>\s*([^<]+)', notes_html),
    }
    linked_fits = re.findall(r'href\s*=\s*["\']?([^"\' >]+\.fits(?:\.gz)?)', object_html, flags=re.IGNORECASE)
    result = {
        "schema": "ugc06787_whisp_hi_source_v01",
        "status": "WHISP_UGC06787_GRAPHICAL_HI_VELOCITY_FIELD_ACQUIRED_FITS_OPEN",
        "galaxy": "UGC06787",
        "source_family": "WHISP",
        "metadata": metadata,
        "overview_image_size_pixels": image_size,
        "overview_contents": [
            "optical image",
            "global H I profile",
            "major-axis position-velocity diagram",
            "full-resolution total H I map",
            "30 arcsec total H I map",
            "60 arcsec total H I map",
            "full-resolution intensity-weighted velocity field",
            "30 arcsec intensity-weighted velocity field",
            "60 arcsec intensity-weighted velocity field",
        ],
        "direct_fits_links_found": linked_fits,
        "source_coordinate_fits_acquired": False,
        "graphical_velocity_field_acquired": True,
        "digitization_allowed": True,
        "physical_a_row_constructed": False,
        "endpoint_access": False,
        "claim_boundary": "source-native graphical H I preflight only; no FITS/cube, calibrated pixel-to-sky field, common H I-Halpha transport, channel detection, or endpoint result",
        "manifest": manifest,
    }
    (DATA / "ugc06787_whisp_hi_source_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    with (DATA / "ugc06787_whisp_hi_source_manifest_v01.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0]))
        writer.writeheader()
        writer.writerows(manifest)

    (REPORTS / "ugc06787_whisp_hi_source_v01.md").write_text(
        f"""# UGC06787 WHISP H I Source Acquisition v0.1

**Status:** `{result['status']}`

The public WHISP object page, graphical overview, and observation/reduction
notes are cached with SHA-256 provenance. The `791 x 1024` overview contains
total-H I and intensity-weighted velocity fields at full, 30 arcsec, and
60 arcsec resolution, plus a global profile and major-axis position-velocity
diagram.

## Observation Metadata

| field | value |
| --- | ---: |
| quality | {metadata['quality']} |
| bandwidth | {metadata['bandwidth_mhz']} MHz |
| channels | {metadata['n_channels']} |
| central velocity | {metadata['central_velocity_km_s']} km/s |
| channel separation | {metadata['channel_separation_km_s']} km/s |
| full-resolution beam | {metadata['beam_full_resolution_arcsec']} arcsec |
| cleaned-map rms | {metadata['rms_noise_mjy_beam']} mJy/beam |

## Product Boundary

No direct FITS or cube link is present on the public object page. The graphical
velocity fields are source-native and sufficient for a declared coarse
digitization preflight, but they are not a calibrated source-coordinate cube
and cannot yet define a physical `A_p` row.

Next finite action: freeze the overview panel geometry and color-to-velocity
legend, digitize the 60 arcsec field with an explicit quantization error, and
compare only source-side radial support/side coverage with the GHASP Halpha
points. Endpoint residuals remain closed.
""",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
