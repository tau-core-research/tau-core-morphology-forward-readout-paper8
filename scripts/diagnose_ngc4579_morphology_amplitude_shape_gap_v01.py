#!/usr/bin/env python3
"""Diagnose amplitude versus radial-shape content after the NGC4579 endpoint opened."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "ngc4579_morphology_amplitude_shape_gap_v01.md"
MATCHED_XMAX = 1.834039
MATCHED_TOTAL_CAPACITY = 0.9463529510688321


def rmse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sqrt(np.mean((a - b) ** 2)))


def main() -> None:
    points = pd.read_csv(DATA / "ngc4579_sings_halpha_modal_capacity_points_v01.csv")
    summaries = []
    details = []
    for sensitivity, frame in points.groupby("baryonic_sensitivity", sort=False):
        q_required = (frame.vobs_halpha_km_s.to_numpy(float) / frame.vbar_km_s.to_numpy(float)) ** 2 - 1.0
        q_morph = frame.matched_modal_response.to_numpy(float)
        vbar = frame.vbar_km_s.to_numpy(float)
        vobs = frame.vobs_halpha_km_s.to_numpy(float)
        inside = frame.radius_over_bar.to_numpy(float) <= MATCHED_XMAX
        scale = float(np.dot(q_morph, q_required) / np.dot(q_morph, q_morph))
        q_scaled = scale * q_morph
        v_scaled = vbar * np.sqrt(1.0 + q_scaled)
        response_capture = q_morph / q_required
        summaries.append({
            "baryonic_sensitivity": sensitivity,
            "n_points": len(frame), "n_inside_source_support": int(inside.sum()),
            "n_beyond_source_support": int((~inside).sum()),
            "q_required_min": float(q_required.min()), "q_required_max": float(q_required.max()),
            "q_morph_min": float(q_morph.min()), "q_morph_max": float(q_morph.max()),
            "q_required_dynamic_range": float(np.ptp(q_required)),
            "q_morph_dynamic_range": float(np.ptp(q_morph)),
            "median_q_response_fraction": float(np.median(response_capture)),
            "n_q_required_above_frozen_capacity": int((q_required > MATCHED_TOTAL_CAPACITY).sum()),
            "pearson_q_all": float(np.corrcoef(q_required, q_morph)[0, 1]),
            "pearson_q_inside_support": float(np.corrcoef(q_required[inside], q_morph[inside])[0, 1]),
            "post_open_scale_only_factor": scale,
            "rmse_prefrozen_matched_km_s": rmse(vobs, frame.vpred_matched_km_s.to_numpy(float)),
            "rmse_post_open_scaled_diagnostic_km_s": rmse(vobs, v_scaled),
        })
        for i, row in enumerate(frame.itertuples(index=False)):
            details.append({
                "baryonic_sensitivity": sensitivity, "radius_kpc": row.radius_kpc,
                "radius_over_bar": row.radius_over_bar, "inside_source_support": bool(inside[i]),
                "q_required": q_required[i], "q_morph_prefrozen": q_morph[i],
                "q_response_fraction": response_capture[i], "q_post_open_scaled_diagnostic": q_scaled[i],
            })
    summary = pd.DataFrame(summaries)
    pd.DataFrame(details).to_csv(DATA / "ngc4579_morphology_amplitude_shape_gap_points_v01.csv", index=False)
    summary.to_csv(DATA / "ngc4579_morphology_amplitude_shape_gap_summary_v01.csv", index=False)
    ranges = lambda c: [float(summary[c].min()), float(summary[c].max())]
    result = {
        "schema": "tau_core_ngc4579_morphology_amplitude_shape_gap_v01",
        "status": "POST_OPEN_AMPLITUDE_VERSUS_SHAPE_DIAGNOSTIC_COMPLETE",
        "n_baryonic_sensitivities": len(summary),
        "source_support_counts": {
            "inside": int(summary.n_inside_source_support.iloc[0]),
            "beyond": int(summary.n_beyond_source_support.iloc[0]),
        },
        "q_required_dynamic_range": ranges("q_required_dynamic_range"),
        "q_morph_dynamic_range": ranges("q_morph_dynamic_range"),
        "median_q_response_fraction": ranges("median_q_response_fraction"),
        "frozen_total_capacity": MATCHED_TOTAL_CAPACITY,
        "n_q_required_above_frozen_capacity": [
            int(summary.n_q_required_above_frozen_capacity.min()),
            int(summary.n_q_required_above_frozen_capacity.max()),
        ],
        "pearson_q_all": ranges("pearson_q_all"),
        "pearson_q_inside_support": ranges("pearson_q_inside_support"),
        "post_open_scale_only_factor": ranges("post_open_scale_only_factor"),
        "rmse_prefrozen_matched_km_s": ranges("rmse_prefrozen_matched_km_s"),
        "rmse_post_open_scaled_diagnostic_km_s": ranges("rmse_post_open_scaled_diagnostic_km_s"),
        "interpretation": "the prefrozen matched win is dominated by morphology-conditioned capacity level; radial shape is weakly resolved and a substantial endpoint fraction lies beyond source support",
        "new_formula_selection_allowed": False,
        "tau_morphology_detected": False,
        "physical_channel_detected": False,
        "claim_boundary": "post-open diagnostic only; the fitted scale is not predictive and may not be promoted into the operator"
    }
    (DATA / "ngc4579_morphology_amplitude_shape_gap_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# NGC4579 morphology amplitude-shape gap v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"Only `{result['source_support_counts']['inside']}` of 20 post-bar Halpha points lie inside the matched source-profile support; "
        f"`{result['source_support_counts']['beyond']}` sample the frozen terminal response. Required `Q` dynamic range is "
        f"`{result['q_required_dynamic_range']}`, versus only `{result['q_morph_dynamic_range']}` for the prefrozen response. "
        f"The response supplies a median `{result['median_q_response_fraction']}` fraction of required `Q`; "
        f"`{result['n_q_required_above_frozen_capacity']}` points exceed the frozen capacity ceiling across sensitivities.\n\n"
        f"A post-open scale-only diagnostic would require factor `{result['post_open_scale_only_factor']}` and reduce RMSE to "
        f"`{result['rmse_post_open_scaled_diagnostic_km_s']} km/s`, but this factor is endpoint-fitted and forbidden from promotion. "
        "The current positive attribution is therefore primarily a morphology-conditioned capacity-level result, not a resolved radial-shape or physical-channel detection.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
