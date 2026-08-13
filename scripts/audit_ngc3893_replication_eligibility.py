#!/usr/bin/env python3
"""Audit NGC3893 as a source-ranked channel-replication candidate."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import tarfile
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
OUT = ROOT / "data" / "external" / "literature" / "ngc3893_replication_eligibility"
REPORTS = ROOT / "reports"
PRIMARY_URL = "https://export.arxiv.org/e-print/astro-ph/0701878"
LOPSIDEDNESS_URL = "https://export.arxiv.org/e-print/1103.4928"
WHISP_BASE = "https://www.astro.rug.nl/~whisp/Database/OverviewCatalog/ListByName/"


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "tau-core-source-audit/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def source_text(payload: bytes) -> str:
    chunks = []
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:*") as archive:
        for member in archive.getmembers():
            if member.isfile() and member.name.lower().endswith((".tex", ".txt")):
                handle = archive.extractfile(member)
                if handle:
                    chunks.append(handle.read().decode("latin-1", errors="ignore"))
    return re.sub(r"\s+", " ", " ".join(chunks))


def main() -> None:
    with (DATA / "ghasp_sparc_source_only_candidate_federation_v01.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        candidate = next(row for row in csv.DictReader(handle) if row["source_only_rank"] == "3")
    if candidate["galaxy"] != "NGC3893":
        raise RuntimeError("Frozen rank-3 source candidate is not NGC3893")

    OUT.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    primary_payload = download(PRIMARY_URL)
    lopsidedness_payload = download(LOPSIDEDNESS_URL)
    whisp_url = WHISP_BASE + candidate["whisp_relative_url"]
    whisp_payload = download(whisp_url)
    (OUT / "astro-ph_0701878_source.tar.gz").write_bytes(primary_payload)
    (OUT / "1103.4928_source.tar.gz").write_bytes(lopsidedness_payload)
    (OUT / "whisp_ugc6778_overview.html").write_bytes(whisp_payload)

    primary = source_text(primary_payload).lower()
    lopsidedness = source_text(lopsidedness_payload).lower()
    evidence = {
        "interaction_and_non_circular_motion": all(
            phrase in primary for phrase in ("non-circular motions are detected", "interaction with ngc 3896")
        ),
        "common_hi_envelope_or_bridge": "common hi" in primary and "broad arm" in primary,
        "dedicated_curve_symmetry_targeted": (
            "obtain a symmetric curve in the inner parts" in primary
            and "minimize scatter on each side" in primary
        ),
        "ugc6778_in_whisp_lopsidedness_source_package": bool(
            re.search(r"ugc\s*0*6778|ngc\s*3893", lopsidedness)
        ),
        "whisp_graphical_page_cached": len(whisp_payload) > 0,
    }
    if not all(
        evidence[key]
        for key in (
            "interaction_and_non_circular_motion",
            "common_hi_envelope_or_bridge",
            "dedicated_curve_symmetry_targeted",
            "whisp_graphical_page_cached",
        )
    ):
        raise RuntimeError("Expected primary-source evidence was not recovered")

    gates = {
        "source_only_rank_frozen": True,
        "both_ghasp_halpha_sides": candidate["both_halpha_sides"] == "True",
        "whisp_graphical_source_available": candidate["whisp_overview_available"] == "True",
        "low_disturbance_primary_replication": False,
        "independent_machine_readable_hi_radial_sides_acquired": False,
        "side_curve_not_symmetry_targeted": False,
    }
    result = {
        "schema": "ngc3893_replication_eligibility_v01",
        "status": "NGC3893_DISTURBED_CONTROL_PRIMARY_REPLICATION_BLOCKED",
        "galaxy": "NGC3893",
        "aliases": ["UGC6778"],
        "source_only_rank": 3,
        "role": "DISTURBED_CONVENTIONAL_ASYMMETRY_CONTROL_NOT_PRIMARY_CHANNEL_REPLICATION",
        "gates": gates,
        "primary_replication_eligible": all(gates.values()),
        "channel_statistic_run": False,
        "counts_as_negative_channel_test": False,
        "selection_uses_vobs_or_residual": False,
        "sparc_endpoint_opened": False,
        "endpoint_access": False,
        "evidence": evidence,
        "sources": {
            "interaction_kinematics": "https://arxiv.org/abs/astro-ph/0701878",
            "whisp_overview": whisp_url,
            "whisp_lopsidedness_catalog_audit": "https://arxiv.org/abs/1103.4928",
        },
        "source_hashes_sha256": {
            "astro-ph_0701878": hashlib.sha256(primary_payload).hexdigest(),
            "1103.4928": hashlib.sha256(lopsidedness_payload).hexdigest(),
            "whisp_overview": hashlib.sha256(whisp_payload).hexdigest(),
        },
        "next_clean_candidate": "UGC08490",
        "claim_boundary": (
            "source-side eligibility audit only; NGC3893 is retained as a disturbed-control case, "
            "not counted as a channel detection or a failed channel replication"
        ),
    }
    (DATA / "ngc3893_replication_eligibility_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    with (DATA / "ngc3893_replication_eligibility_gates_v01.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=["gate", "pass"])
        writer.writeheader()
        writer.writerows({"gate": key, "pass": value} for key, value in gates.items())

    gate_rows = "\n".join(f"| {key} | {value} |" for key, value in gates.items())
    (REPORTS / "ngc3893_replication_eligibility_v01.md").write_text(
        f"""# NGC3893 Replication Eligibility Audit v0.1

**Status:** `{result['status']}`

NGC3893 was reached as residual-blind source rank 3. The dedicated source,
however, describes the NGC3893/3896 interaction, detected non-circular
motions, a common H I envelope/connecting arm, and a rotation-curve geometry
chosen to make the inner curve symmetric and minimize side scatter. Those are
useful properties for a disturbed-galaxy control, but they block an independent
primary odd-channel replication.

| gate | pass |
| --- | --- |
{gate_rows}

The WHISP graphical overview is cached. The searched WHISP lopsidedness source
package does not contain UGC6778/NGC3893, and no independent machine-readable
H I radial side table has been acquired in this audit. This is a bounded source
audit, not a universal non-existence claim.

No channel statistic was run, so this object is neither a positive detection
nor a third negative channel test. It remains available as a predeclared
disturbed/non-circular-motion control. The next clean-candidate audit is
UGC08490 (NGC5204).
""",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
