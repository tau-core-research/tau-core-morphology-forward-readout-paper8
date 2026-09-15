#!/usr/bin/env python3
"""Score frozen conditional source candidates on all preserved covariances."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from run_sdp81_4d_corridor_proxy_covariance_robustness_v01 import log_mode_covariances
from run_sdp81_common_action_endpoint_v01 import (
    centered_log_modes,
    load_frozen_endpoint,
    score_controls,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
MODEL = DATA / "sdp81_pcrr_source_hessian_diagnostic_freeze_v01.json"
COVARIANCES = DATA / "sdp81_4d_corridor_proxy_covariance_robustness_v01.json"
OUT = DATA / "sdp81_pcrr_source_hessian_diagnostic_score_v01.json"
REPORT = ROOT / "reports/sdp81_pcrr_source_hessian_diagnostic_score_v01.md"


def summarize_candidate(
    modes: np.ndarray,
    fluxes: np.ndarray,
    basis: np.ndarray,
    transfers: list[np.ndarray],
    geometry_records: list[dict],
) -> dict:
    records = []
    for geometry in geometry_records:
        covariances = log_mode_covariances(
            fluxes, basis, np.asarray(geometry["channel_covariance"], dtype=float)
        )
        scores = score_controls(modes, transfers, covariances)
        matched = float(scores["matched"]["total_mahalanobis_chi2"])
        wrong = np.asarray(
            [item["total_mahalanobis_chi2"] for item in scores["wrong_path_assignment"]]
        )
        wrong_not_worse_count = int(np.sum(wrong <= matched))
        # Exact random-assignment rank among all 4! assignments, including the
        # matched one. Lower score is better; ties count conservatively.
        assignment_p = float((1 + wrong_not_worse_count) / (1 + wrong.size))
        records.append(
            {
                "inner_radius_arcsec": geometry["inner_radius_arcsec"],
                "outer_radius_arcsec": geometry["outer_radius_arcsec"],
                "grid_step_arcsec": geometry["grid_step_arcsec"],
                "matched_score": matched,
                "lossless_score": float(
                    scores["lossless_identity"]["total_mahalanobis_chi2"]
                ),
                "matched_beats_lossless": scores["matched_beats_lossless"],
                "matched_beats_wrong_median": scores["matched_beats_wrong_median"],
                "matched_beats_every_wrong_assignment": scores[
                    "matched_beats_every_wrong_assignment"
                ],
                "wrong_assignment_fraction_not_worse": float(
                    wrong_not_worse_count / wrong.size
                ),
                "wrong_assignment_not_worse_count": wrong_not_worse_count,
                "exact_assignment_rank_p_value": assignment_p,
            }
        )
    fractions = [record["wrong_assignment_fraction_not_worse"] for record in records]
    assignment_p_values = [record["exact_assignment_rank_p_value"] for record in records]
    return {
        "geometry_records": records,
        "summary": {
            "geometry_count": len(records),
            "matched_beats_lossless_geometries": sum(
                record["matched_beats_lossless"] for record in records
            ),
            "matched_beats_wrong_median_geometries": sum(
                record["matched_beats_wrong_median"] for record in records
            ),
            "matched_beats_every_wrong_assignment_geometries": sum(
                record["matched_beats_every_wrong_assignment"] for record in records
            ),
            "wrong_assignment_fraction_not_worse_range": [
                float(min(fractions)),
                float(max(fractions)),
            ],
            "exact_assignment_rank_p_value_range": [
                float(min(assignment_p_values)),
                float(max(assignment_p_values)),
            ],
            "exact_assignment_p_le_0_05_geometries": sum(
                value <= 0.05 for value in assignment_p_values
            ),
        },
    }


def main() -> None:
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    covariance_source = json.loads(COVARIANCES.read_text(encoding="utf-8"))
    if not model.get("diagnostic_run_allowed") or model.get("physical_endpoint_authorized"):
        raise RuntimeError("conditional diagnostic freeze is not valid")
    basis = np.asarray(model["terminal_basis"], dtype=float)
    # The endpoint is opened only in this retrospective scoring stage.
    endpoint_model = json.loads(
        (DATA / "sdp81_4d_corridor_proxy_diagnostic_freeze_v01.json").read_text()
    )
    fluxes = load_frozen_endpoint(endpoint_model)
    modes = centered_log_modes(fluxes, basis)
    candidate_results = {}
    for name, candidate in model["candidates"].items():
        candidate_results[name] = summarize_candidate(
            modes,
            fluxes,
            basis,
            [np.asarray(item, dtype=float) for item in candidate["transfers"]],
            covariance_source["geometry_records"],
        )

    primary = candidate_results["pcrr_half_laplacian"]["summary"]
    wr = candidate_results["wr_t19_aligned_half"]["summary"]
    checks = {
        "nine_covariance_geometries_preserved": primary["geometry_count"] == 9,
        "all_candidates_scored_without_geometry_selection": all(
            item["summary"]["geometry_count"] == 9 for item in candidate_results.values()
        ),
        "pcrr_candidate_beats_lossless_all_geometries": (
            primary["matched_beats_lossless_geometries"] == 9
        ),
        "pcrr_candidate_does_not_beat_every_wrong_assignment": (
            primary["matched_beats_every_wrong_assignment_geometries"] == 0
        ),
        "pcrr_candidate_never_passes_exact_assignment_0_05": (
            primary["exact_assignment_p_le_0_05_geometries"] == 0
        ),
        "wr_alignment_remains_explicitly_unproved": model["candidates"]
        ["wr_t19_aligned_half"]["extra_terminal_alignment_assumption"],
        "physical_endpoint_remains_unauthorized": True,
    }
    result = {
        "schema": "tau-core.paper8.sdp81-pcrr-source-hessian-diagnostic-score.v01",
        "status": "RETROSPECTIVE_DIAGNOSTIC_ONLY_NOT_ENDPOINT",
        "verdict": "PCRR_HALF_SHAPE_COMPATIBLE_BUT_NOT_IDENTIFYING",
        "model": str(MODEL.relative_to(ROOT)),
        "covariance_source": str(COVARIANCES.relative_to(ROOT)),
        "spectral_endpoint_read": True,
        "assignment_rank_null": (
            "conditional uniform exchangeability of the 4! path-to-transfer "
            "assignments; not a population-level or noise-model-calibrated p-value"
        ),
        "candidate_results": candidate_results,
        "primary_summary": primary,
        "wr_t19_alignment_summary": wr,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "physical_endpoint_authorized": False,
        "confirmatory_prediction": False,
        "claim_boundary": (
            "The preexisting conditional PCRR half-generator is compatible with the "
            "retrospective covariance-weighted ordering signal, but no geometry beats "
            "every wrong path assignment. The same endpoint previously exposed the "
            "half-strength preference, the depth is still a conventional 4D proxy, "
            "and WR-T19 requires an unproved mode calibration. Therefore this is not "
            "model selection, a physical parent-distance measurement, or evidence of "
            "Nature occupation. The exact assignment ranks are conditional control "
            "p-values only, not population significance."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 PCRR/source-Hessian diagnostic score v01\n\n"
        f"Status: `{result['status']}`. Verdict: `{result['verdict']}`.\n\n"
        f"The PCRR half-generator beats lossless transfer in "
        f"`{primary['matched_beats_lossless_geometries']}/9` geometries, the wrong-"
        f"assignment median in `{primary['matched_beats_wrong_median_geometries']}/9`, "
        f"and every wrong assignment in "
        f"`{primary['matched_beats_every_wrong_assignment_geometries']}/9`. Its wrong-"
        f"assignment fraction-not-worse range is "
        f"`{primary['wrong_assignment_fraction_not_worse_range'][0]:.3f}--"
        f"{primary['wrong_assignment_fraction_not_worse_range'][1]:.3f}`; the exact "
        f"assignment-rank p-value range is "
        f"`{primary['exact_assignment_rank_p_value_range'][0]:.3f}--"
        f"{primary['exact_assignment_rank_p_value_range'][1]:.3f}`.\n\n"
        f"The WR-T19 aligned hypothesis gives a range of "
        f"`{wr['wrong_assignment_fraction_not_worse_range'][0]:.3f}--"
        f"{wr['wrong_assignment_fraction_not_worse_range'][1]:.3f}` and exact-rank "
        f"p-value range `{wr['exact_assignment_rank_p_value_range'][0]:.3f}--"
        f"{wr['exact_assignment_rank_p_value_range'][1]:.3f}`, but its terminal "
        "alignment is not derived.\n\n"
        f"{result['claim_boundary']}\n",
        encoding="utf-8",
    )
    print(result["verdict"])


if __name__ == "__main__":
    main()
