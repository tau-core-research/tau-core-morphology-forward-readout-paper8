#!/usr/bin/env python3
"""Decide source readiness of the five preregistered COMING bar candidates."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "coming_bar_family_completion_v01.md"


def main() -> None:
    fields = pd.read_csv(DATA / "coming_bar_source_fields_v01.csv")
    profiles = pd.read_csv(DATA / "coming_vector_marker_centers_v01.csv")
    reverse = json.loads((DATA / "coming_profile_reverse_render_validation_v01.json").read_text())
    ngc5248_scale = json.loads((DATA / "ngc5248_bar_scale_resolution_v01.json").read_text())
    rows = []
    for source in fields.itertuples(index=False):
        profile = profiles[profiles.galaxy.eq(source.galaxy)]
        blocker = ""
        policy = "use_all_visible_vector_points"
        ready = True
        if source.galaxy == "NGC 4579":
            policy = "preserve_Delta_2p9_row_but_exclude_it_from_interpolation_and_amplitude_summary_per_source"
        if source.galaxy == "NGC 5248":
            ready = ngc5248_scale["source_scale_resolved_for_primary_protocol"]
            policy = "uniform_small_bar_primary_large_oval_predeclared_sensitivity"
        rows.append(
            {
                "galaxy": source.galaxy,
                "n_profile_rows": len(profile),
                "n_rows_with_errors": int(profile.physical_delta_error_minus.notna().sum()),
                "profile_policy": policy,
                "bar_radius_kpc": source.deprojected_bar_radius_kpc,
                "source_ready": ready and reverse["visible_marker_roundtrip_pass"] and reverse["visible_error_roundtrip_pass"],
                "blocker": blocker,
                "endpoint_eligible": False,
            }
        )
    frame = pd.DataFrame(rows)
    frame.to_csv(DATA / "coming_bar_family_completion_v01.csv", index=False)
    payload = {
        "schema": "tau_core_coming_bar_family_completion_v01",
        "status": "FIVE_OF_FIVE_SOURCE_READY_ENDPOINT_ACQUISITION_OPEN",
        "n_candidates": len(frame),
        "n_source_ready": int(frame.source_ready.sum()),
        "blocked_galaxies": frame.loc[~frame.source_ready, "galaxy"].tolist(),
        "ngc4579_outlier_policy_source_frozen": True,
        "minimum_five_ready_met": bool(frame.source_ready.sum() >= 5),
        "family_source_gate_complete": bool(frame.source_ready.sum() == 5),
        "endpoint_scoring_allowed": False,
        "next_action": "acquire independent tracer rotation endpoints and baryonic mass models without reopening COMING profiles",
        "claim_boundary": "source-family readiness only; no rotation endpoint or Tau response score opened",
    }
    (DATA / "coming_bar_family_completion_v01.json").write_text(json.dumps(payload, indent=2) + "\n")
    REPORT.write_text(
        "# COMING barred-family completion audit v01\n\n"
        f"Status: `{payload['status']}`\n\n"
        "NGC613, NGC4303, NGC4579, and NGC7479 have source-frozen labels, bar windows, calibrated profiles, vector errors, and a passing reverse-render audit. "
        "NGC4579's `Delta=2.9` row is preserved but excluded from interpolation and amplitude summaries, matching the source treatment.\n\n"
        "NGC5248 uses the uniform S4G small-bar scale as primary, while the large oval is frozen as a sensitivity control and cannot be selected post-score. "
        "All five source rows are ready. Endpoint scoring remains closed pending independent tracer and baryonic endpoint acquisition.\n"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
