#!/usr/bin/env python3
"""Audit the author-source route for residual-blind COMING profile extraction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "external" / "literature" / "coming_bar_harmonics"
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "coming_vector_profile_source_audit_v01.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    archive = SOURCE / "1901.00640_source.tar"
    required = ["noncirc.eps", "PLOTS1.eps", "PLOTS2.eps", "PLOTS3.eps", "PLOTS4.eps", "PLOTS5.eps"]
    files = []
    for name in required:
        path = SOURCE / name
        files.append(
            {
                "name": name,
                "exists": path.exists(),
                "sha256": sha256(path) if path.exists() else None,
                "vector_eps": path.exists() and path.read_bytes().startswith(b"%!PS-Adobe"),
            }
        )
    payload = {
        "schema": "tau_core_coming_vector_profile_source_audit_v01",
        "status": "VECTOR_AUTHOR_SOURCE_ACQUIRED_DIGITIZATION_FREEZE_REQUIRED",
        "arxiv_id": "1901.00640",
        "journal_doi": "10.1093/pasj/psz004",
        "archive_sha256": sha256(archive),
        "numeric_profile_table_present": False,
        "required_vector_files_complete": all(row["exists"] and row["vector_eps"] for row in files),
        "files": files,
        "digitization_protocol": [
            "freeze panel bounding boxes and linear axis transforms before extracting markers",
            "map EPS stroke/fill colors to the published galaxy legend",
            "extract marker centers and vertical error-bar endpoints in vector coordinates",
            "retain NGC4579 central Delta=2.9 as a flagged source point rather than deleting it",
            "run a reverse-render pixel check against the source EPS",
        ],
        "uses_dark_discrepancy_endpoint": False,
        "profile_values_frozen": False,
        "endpoint_scoring_allowed": False,
        "claim_boundary": "source/provenance audit only; vector availability is not a physical result",
    }
    (DATA / "coming_vector_profile_source_audit_v01.json").write_text(json.dumps(payload, indent=2) + "\n")
    lines = [
        "# COMING vector-profile source audit v01",
        "",
        f"Status: `{payload['status']}`",
        "",
        "The checksum-frozen arXiv author package contains the original vector EPS figures but no separate numeric harmonic-profile table. The journal DOI is `10.1093/pasj/psz004`; the earlier local `psz033` value was incorrect and has been repaired.",
        "",
        f"Archive SHA-256: `{payload['archive_sha256']}`.",
        "",
        "The source route is therefore viable but not yet numeric. Panel transforms, legend-color mappings, marker/error extraction, and reverse-render validation must be frozen before values are promoted. NGC4579's central `Delta=2.9` point must remain present with an outlier flag.",
        "",
        "No dark-discrepancy endpoint was opened, and endpoint scoring remains prohibited.",
        "",
    ]
    REPORT.write_text("\n".join(lines))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
