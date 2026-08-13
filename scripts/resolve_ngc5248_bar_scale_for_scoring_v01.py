#!/usr/bin/env python3
"""Freeze the NGC5248 primary bar scale without endpoint access."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "ngc5248_bar_scale_resolution_v01.md"


def main() -> None:
    payload = {
        "schema": "tau_core_ngc5248_bar_scale_resolution_v01",
        "status": "UNIFORM_CATALOG_SMALL_BAR_PRIMARY_LARGE_OVAL_SENSITIVITY_FROZEN",
        "galaxy": "NGC 5248",
        "primary_bar_radius_kpc": 1.78,
        "primary_bar_radius_error_kpc": 0.18,
        "primary_definition": "deprojected S4G infrared ellipticity-maximum bar used uniformly by the COMING analysis",
        "primary_source": "Salak et al. 2019 Table 2 adopting Herrera-Endoqui et al. 2015",
        "alternative_large_oval_radius_arcsec": 95.0,
        "alternative_role": "predeclared source sensitivity control only",
        "selection_uses_rotation_endpoint_or_dark_discrepancy": False,
        "post_score_scale_switch_allowed": False,
        "source_scale_resolved_for_primary_protocol": True,
        "endpoint_scoring_allowed_by_this_gate": False,
        "claim_boundary": "operational source hierarchy; does not prove the small bar is the unique physical decomposition",
    }
    (DATA / "ngc5248_bar_scale_resolution_v01.json").write_text(json.dumps(payload, indent=2) + "\n")
    REPORT.write_text(
        "# NGC5248 bar-scale resolution v01\n\n"
        f"Status: `{payload['status']}`\n\n"
        "The primary protocol uses `a_bar=1.78+/-0.18 kpc`, the same deprojected S4G ellipticity-maximum definition used across the COMING barred sample. "
        "The published approximately `95 arcsec` large oval remains a predeclared sensitivity control. No endpoint result may select between them, and post-score scale switching is forbidden.\n\n"
        "This resolves the operational source scale, not the uniqueness of the physical decomposition.\n"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
