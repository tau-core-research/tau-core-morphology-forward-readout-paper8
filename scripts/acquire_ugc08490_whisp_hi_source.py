#!/usr/bin/env python3
"""Acquire the public WHISP UGC08490 graphical H I source packet."""

from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/external/literature/ugc08490_whisp_hi_route"
DATA = ROOT / "data/derived"
BASE = "https://www.astro.rug.nl/~whisp/Database/OverviewCatalog/ListByName/U8490"
SOURCES = [
    ("object_page", f"{BASE}/u8490.html", "whisp_ugc08490_object_page.html"),
    ("graphical_overview", f"{BASE}/u8490plot.gif", "whisp_ugc08490_overview.gif"),
    ("observation_notes", f"{BASE}/u8490obsred.html", "whisp_ugc08490_obs_reduction_notes.html"),
]


def download(url):
    request = urllib.request.Request(url, headers={"User-Agent": "tau-core-source-audit/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read(), response.headers.get_content_type()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for source_id, url, filename in SOURCES:
        payload, content_type = download(url)
        path = OUT / filename
        path.write_bytes(payload)
        manifest.append({
            "source_id": source_id, "url": url,
            "local_path": str(path.relative_to(ROOT)), "content_type": content_type,
            "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest(),
            "source_native": True, "endpoint_access": False,
        })
    image_path = OUT / "whisp_ugc08490_overview.gif"
    with Image.open(image_path) as image:
        image_size = list(image.size)
    result = {
        "schema": "ugc08490_whisp_hi_source_v01",
        "status": "WHISP_UGC08490_GRAPHICAL_HI_SOURCE_ACQUIRED_FITS_NOT_LINKED",
        "galaxy": "UGC08490", "alias": "NGC5204", "source_family": "WHISP",
        "metadata": {
            "quality": "good", "bandwidth_mhz": 2.48, "n_channels": 127,
            "central_velocity_km_s": 204.0, "channel_separation_km_s": 4.14,
            "beam_full_resolution_arcsec": "13.5 x 11.3", "rms_noise_mjy_beam": 1.9,
            "channel_map_quality": "reasonable", "cleaned_map_quality": "good",
        },
        "overview_image_size_pixels": image_size,
        "direct_fits_links_found": [], "source_coordinate_fits_acquired": False,
        "graphical_velocity_field_acquired": True, "digitization_allowed": True,
        "source_selection_reason": (
            "pre-ranked residual-blind GHASP-WHISP candidate with two Halpha sides and "
            "Halpha coverage 7.45 times the frozen D>=2 onset"
        ),
        "endpoint_access": False, "physical_channel_detected": False,
        "claim_boundary": (
            "source acquisition only; graphical field requires frozen panel/legend calibration "
            "before same-body tracer-kernel scoring"
        ),
        "manifest": manifest,
    }
    (DATA / "ugc08490_whisp_hi_source_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
