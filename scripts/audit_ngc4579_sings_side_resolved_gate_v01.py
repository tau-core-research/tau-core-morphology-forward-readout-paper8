#!/usr/bin/env python3
"""Audit the side-resolved gate and unsigned side-error information for NGC4579."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "ngc4579_sings_side_resolved_gate_v01.md"


def main() -> None:
    freeze = json.loads((DATA / "ngc4579_sings_figure_c2_side_extraction_freeze_v01.json").read_text())
    endpoint = pd.read_csv(DATA / "ngc4579_sings_halpha_rotation_endpoint_v01.csv")
    primary = endpoint[endpoint.post_bar_primary].copy()
    side = primary.side_error_km_s.to_numpy(float)
    formal = primary.gipsy_error_km_s.to_numpy(float)
    result = {
        "schema": "tau_core_ngc4579_sings_side_resolved_gate_v01",
        "status": "SIDE_RESOLVED_GATE_FAILED_SINGLE_AVERAGED_CURVE_ONLY",
        "freeze_status": freeze["status"],
        "full_pdf_sha256": freeze["source_sha256"],
        "figure_c2_visual_series_count": 1,
        "approaching_receding_assignment_available": False,
        "side_values_algebraically_reconstructed": False,
        "n_post_bar_points": int(len(primary)),
        "n_side_error_dominates_formal_error": int((side >= formal).sum()),
        "side_error_km_s": {
            "median": float(np.median(side)),
            "rms": float(np.sqrt(np.mean(side**2))),
            "maximum": float(np.max(side)),
        },
        "formal_error_km_s": {
            "median": float(np.median(formal)),
            "rms": float(np.sqrt(np.mean(formal**2))),
            "maximum": float(np.max(formal)),
        },
        "unsigned_side_asymmetry_information_available": True,
        "signed_orientation_odd_information_available": False,
        "odd_channel_scoring_allowed": False,
        "claim_boundary": "side_error is an unsigned source uncertainty/asymmetry magnitude; it is not a signed orientation-odd time-channel observable"
    }
    (DATA / "ngc4579_sings_side_resolved_gate_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# NGC4579 SINGS side-resolved gate v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "The full Figure C2 NGC4579 panel contains one averaged rotation curve and error bars, not two source-labelled side series. "
        "The prefrozen side-resolved extraction gate therefore fails and no side values are reconstructed from the average.\n\n"
        f"In the post-bar domain, side difference dominates the formal ROTCUR error at `{result['n_side_error_dominates_formal_error']}` of `{len(primary)}` points. "
        f"Its median/RMS/maximum are `{result['side_error_km_s']['median']:.2f}`, `{result['side_error_km_s']['rms']:.2f}`, and "
        f"`{result['side_error_km_s']['maximum']:.2f} km/s`. This is unsigned asymmetry/uncertainty information, not a signed odd-channel observable.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
