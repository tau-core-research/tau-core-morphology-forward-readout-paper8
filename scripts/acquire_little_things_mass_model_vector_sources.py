#!/usr/bin/env python3
"""Acquire the Oh et al. LITTLE THINGS vector mass-model figures."""

from __future__ import annotations

import hashlib
import io
import json
import tarfile
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/external/literature/little_things_oh2015_mass_models"
SUMMARY = ROOT / "data/derived/little_things_mass_model_vector_sources_v01.json"
URL = "https://arxiv.org/e-print/1502.01281"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    payload = urllib.request.urlopen(URL, timeout=180).read()
    archive_hash = hashlib.sha256(payload).hexdigest()
    files = {}
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:*") as archive:
        members = [
            member for member in archive.getmembers()
            if Path(member.name).name.startswith("rMD_DH_DM_profiles_")
            and member.name.endswith(".pdf")
        ]
        for member in members:
            name = Path(member.name).name
            content = archive.extractfile(member).read()
            (OUT / name).write_bytes(content)
            files[name] = hashlib.sha256(content).hexdigest()
    result = {
        "schema": "little_things_mass_model_vector_sources_v01",
        "status": "SOURCE_ACQUISITION_ONLY",
        "source": "Oh et al. 2015 arXiv source package",
        "source_url": URL,
        "archive_sha256": archive_hash,
        "n_vector_mass_model_figures": len(files),
        "file_sha256": dict(sorted(files.items())),
        "endpoint_access": False,
        "claim_boundary": "published vector-figure acquisition only; no curve extraction or endpoint score",
    }
    SUMMARY.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["status"], len(files))


if __name__ == "__main__":
    main()
