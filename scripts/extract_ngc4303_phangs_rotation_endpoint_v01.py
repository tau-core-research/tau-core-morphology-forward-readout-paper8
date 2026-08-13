#!/usr/bin/env python3
"""Extract and audit the official PHANGS NGC4303 rotation-curve product."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
SOURCE = ROOT / "data" / "external" / "literature" / "ngc4303_phangs_rotation"
REPORT = ROOT / "reports" / "ngc4303_phangs_rotation_endpoint_v01.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    kpc = SOURCE / "PHANGS_RC_all_kpc.ecsv"
    arcsec = SOURCE / "PHANGS_RC_all_arcsec.ecsv"
    frame = pd.read_csv(kpc, comment="#", sep=r"\s+")
    endpoint = frame[frame.obj.eq("NGC4303")].copy()
    endpoint.columns = ["galaxy", "radius_kpc", "vrot_km_s", "vrot_error_plus_km_s", "vrot_error_minus_km_s"]
    endpoint["source_quality_scope"] = "published_curve_low_inclination_outer_field_truncated_at_60arcsec"
    endpoint["uses_coming_profile_values"] = False
    endpoint.to_csv(DATA / "ngc4303_phangs_rotation_endpoint_v01.csv", index=False)
    result = {
        "schema": "tau_core_ngc4303_phangs_rotation_endpoint_v01",
        "status": "NUMERIC_ENDPOINT_ACQUIRED_QUALITY_LIMITED_SCORING_CLOSED",
        "source": "Lang, Meidt and the PHANGS collaboration (2020)",
        "doi": "10.3847/1538-4357/ab9953",
        "checksums_sha256": {kpc.name: sha256(kpc), arcsec.name: sha256(arcsec)},
        "n_points": len(endpoint),
        "radius_range_kpc": [float(endpoint.radius_kpc.min()), float(endpoint.radius_kpc.max())],
        "inclination_deg": 23.5, "inclination_error_deg": 9.2,
        "paper_unreliable_fit_marker": False,
        "outer_velocity_field_truncated_arcsec": 60.0,
        "outer_truncation_reason": "outer bins overly sensitive to minor-axis information from incomplete coverage",
        "tracer": "PHANGS CO(2-1)",
        "strictly_independent_tracer_from_coming": False,
        "endpoint_values_now_open": True,
        "new_operator_selection_on_ngc4303_allowed": False,
        "existing_prefrozen_operator_diagnostic_only": True,
        "strict_endpoint_scoring_allowed": False,
        "claim_boundary": "official numeric curve acquired; low-inclination and shared-CO quality limits block strict independent validation"
    }
    (DATA / "ngc4303_phangs_rotation_endpoint_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# NGC4303 PHANGS rotation endpoint v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The checksum-frozen official ECSV contains `{len(endpoint)}` NGC4303 points over `{endpoint.radius_kpc.min():.3f}-{endpoint.radius_kpc.max():.3f} kpc`. Lang et al. do not mark NGC4303 as an unreliable orientation fit, but give `i=23.5+/-9.2 deg` and truncate the velocity field at `60 arcsec` because incomplete outer coverage made bins minor-axis sensitive.\n\n"
        "The endpoint is now open. No new operator may be selected from its values. PHANGS and COMING both use CO, so this is not a strict independent-tracer validation endpoint.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
