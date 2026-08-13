#!/usr/bin/env python3
"""Acquire the arXiv source figure containing the numerical UGC08490 H I RC."""

from __future__ import annotations

import hashlib
import io
import json
import tarfile
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/external/literature/ugc08490_repetto2018_route"
DERIVED = ROOT / "data/derived"
URL = "https://export.arxiv.org/e-print/1804.07594"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    payload = urllib.request.urlopen(URL, timeout=120).read()
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        for name in ("f4.pdf", "manuscript.tex"):
            member = archive.getmember(name)
            (OUT / name).write_bytes(archive.extractfile(member).read())
    result = {
        "schema": "ugc08490_repetto_hi_figure_source_v01",
        "status": "UGC08490_REPETTO2018_VECTOR_HI_FIGURE_ACQUIRED",
        "arxiv_id": "1804.07594", "source_url": URL,
        "doi": "10.1093/mnras/sty631",
        "figure": "f4.pdf", "figure_sha256": hashlib.sha256((OUT / "f4.pdf").read_bytes()).hexdigest(),
        "source_native_numeric_table_acquired": False,
        "vector_figure_acquired": True, "endpoint_access": False,
        "claim_boundary": "published vector figure, suitable for figure-derived profile extraction",
    }
    (DERIVED / "ugc08490_repetto_hi_figure_source_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
