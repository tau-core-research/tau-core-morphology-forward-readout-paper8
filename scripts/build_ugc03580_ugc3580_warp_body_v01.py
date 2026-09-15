#!/usr/bin/env python3
"""Build the source-only UGC03580/UGC3580 outer-warp body record."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "data"
    / "external"
    / "literature"
    / "ugc08490_ngc5204_warp"
    / "gentile2007_warped_disks.pdf"
)
DATA_OUT = ROOT / "data" / "derived" / "ugc03580_ugc3580_warp_body_v01.json"
REPORT_OUT = ROOT / "reports" / "ugc03580_ugc3580_warp_body_v01.md"

EXPECTED_SOURCE_SHA256 = "15b4ae9e2bb3268509e75b40e62def8cc4664a117fdcccafae8afb7f170ec8ba"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    source_sha = sha256(SOURCE)
    if source_sha != EXPECTED_SOURCE_SHA256:
        raise RuntimeError("Jozsa source PDF hash mismatch")

    body = {
        "schema": "tau_core_ugc03580_ugc3580_warp_body_v01",
        "status": "SOURCE_NATIVE_OUTER_WARP_BODY_PROMOTED_WITH_SIGNIFICANCE_CAVEAT",
        "galaxy": "UGC03580",
        "alias": "UGC3580",
        "source": "Jozsa 2007 A&A 468 903-917, Tables 1, 4, 5, and 6",
        "source_pdf": str(SOURCE.relative_to(ROOT)),
        "source_pdf_sha256": source_sha,
        "inner_reference_orientation": {
            "inclination_deg": 67.2,
            "pa_deg": 96.3,
        },
        "warp_onset": {
            "radius_arcsec": 180.0,
            "radius_kpc_source": 13.18,
            "tip_deg": 5.5,
            "tip_error_deg": 3.9,
        },
        "source_hi_radius": {
            "radius_arcsec": 240.0,
            "radius_kpc_source": 17.6,
            "radius_arcsec_error": 30.0,
            "radius_kpc_error": 4.1,
        },
        "source_terminal_radius": {
            "radius_arcsec": 375.0,
            "radius_kpc_source": 27.5,
            "radius_arcsec_error": 30.0,
            "radius_kpc_error": 6.4,
        },
        "source_inner_disk_range_arcsec": [30.0, 180.0],
        "source_outer_disk_range_arcsec": [240.0, 375.0],
        "inner_outer_mean_mutual_inclination_deg": 13.9,
        "inner_outer_mean_mutual_inclination_error_deg": 2.5,
        "source_rotation_rise_inner_km_s": 108.9,
        "source_rotation_rise_delta_km_s": 9.7,
        "source_rotation_rise_fraction": 0.09,
        "source_classification": "SA(s)a",
        "source_assessment": {
            "outer_planar_regime": True,
            "warp_is_less_significant_than_ngc2541_and_ngc5204": True,
            "rotation_rise_to_warp_connection_requires_caution": True,
            "slow_extraplanar_gas_component_reported": True,
        },
        "endpoint_values_used_for_body_construction": False,
        "target_endpoint_opened_in_prior_repo_analyses": True,
        "claim_boundary": (
            "source-native outer-warp class member with a published significance caveat; "
            "not a complete galaxy morphology and not a Tau Core identification"
        ),
    }

    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    DATA_OUT.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    REPORT_OUT.write_text(
        "\n".join(
            [
                "# UGC03580 / UGC3580 source-native warp body v01",
                "",
                "Status: `SOURCE_NATIVE_OUTER_WARP_BODY_PROMOTED_WITH_SIGNIFICANCE_CAVEAT`",
                "",
                "Jozsa (2007) fixes an inner plane at `i=67.2 deg`, `PA=96.3 deg`",
                "through 150 arcsec. The first nonzero source tip is",
                "`5.5 +/- 3.9 deg` at `180 arcsec = 13.18 kpc` on the source distance",
                "scale. The source places the outer-disk comparison range at",
                "`240--375 arcsec` and gives an inner/outer mutual inclination of",
                "`13.9 +/- 2.5 deg`.",
                "",
                "The same study reports a `9.7 km/s` (9%) inner-to-outer rotation",
                "rise, but explicitly says that the warp is less significant than for",
                "NGC2541 and NGC5204 and that the rotation-rise/warp connection must be",
                "treated cautiously. Those caveats are part of the promoted body record.",
                "",
                "No pointwise SPARC velocity or residual enters this construction. The",
                "SPARC endpoint has appeared in earlier repository analyses, so any",
                "later transfer score is necessarily retrospective.",
                "",
                f"Source PDF SHA-256: `{source_sha}`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(body, indent=2))


if __name__ == "__main__":
    main()
