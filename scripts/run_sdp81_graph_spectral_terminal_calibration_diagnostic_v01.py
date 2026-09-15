#!/usr/bin/env python3
"""Retrospectively score the frozen graph-spectral calibration candidates."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from run_sdp81_4d_corridor_proxy_covariance_robustness_v01 import log_mode_covariances
from run_sdp81_common_action_endpoint_v01 import centered_log_modes, load_frozen_endpoint
from run_sdp81_pcrr_source_hessian_diagnostic_v01 import summarize_candidate


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
MODEL = DATA / "sdp81_graph_spectral_terminal_calibration_diagnostic_freeze_v01.json"
COVARIANCES = DATA / "sdp81_4d_corridor_proxy_covariance_robustness_v01.json"
BASE = DATA / "sdp81_4d_corridor_proxy_diagnostic_freeze_v01.json"
OUT = DATA / "sdp81_graph_spectral_terminal_calibration_diagnostic_score_v01.json"
REPORT = ROOT / "reports/sdp81_graph_spectral_terminal_calibration_diagnostic_score_v01.md"


def main() -> None:
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    covariance_source = json.loads(COVARIANCES.read_text(encoding="utf-8"))
    if not model.get("diagnostic_run_allowed") or model.get("physical_endpoint_authorized"):
        raise RuntimeError("graph-spectral diagnostic freeze is not valid")

    base = json.loads(BASE.read_text(encoding="utf-8"))
    basis = np.asarray(model["helmert_basis"], dtype=float)
    fluxes = load_frozen_endpoint(base)
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

    monotone = candidate_results["wr_t19_graph_monotone_half"]["summary"]
    reverse = candidate_results["wr_t19_graph_reverse_half"]["summary"]
    isotropic = candidate_results["isotropic_mean_half"]["summary"]
    ensemble_results = []
    for assignment in model["mode_assignment_ensemble"]:
        scored = summarize_candidate(
            modes,
            fluxes,
            basis,
            [np.asarray(item, dtype=float) for item in assignment["transfers"]],
            covariance_source["geometry_records"],
        )
        ensemble_results.append(
            {
                "assignment_id": assignment["assignment_id"],
                "permutation": assignment["permutation"],
                "matched_scores": [
                    record["matched_score"] for record in scored["geometry_records"]
                ],
            }
        )
    score_matrix = np.asarray([item["matched_scores"] for item in ensemble_results])
    permutations = [tuple(item["permutation"]) for item in ensemble_results]
    monotone_index = permutations.index((0, 1, 2, 3, 4))
    reverse_index = permutations.index((4, 3, 2, 1, 0))
    mode_assignment_records = []
    for geometry_index, geometry in enumerate(covariance_source["geometry_records"]):
        column = score_matrix[:, geometry_index]
        monotone_rank = int(1 + np.sum(column < column[monotone_index] - 1e-12))
        reverse_rank = int(1 + np.sum(column < column[reverse_index] - 1e-12))
        best_index = int(np.argmin(column))
        mode_assignment_records.append(
            {
                "inner_radius_arcsec": geometry["inner_radius_arcsec"],
                "outer_radius_arcsec": geometry["outer_radius_arcsec"],
                "grid_step_arcsec": geometry["grid_step_arcsec"],
                "monotone_rank_of_120": monotone_rank,
                "monotone_exact_mode_assignment_p": monotone_rank / 120.0,
                "reverse_rank_of_120": reverse_rank,
                "reverse_exact_mode_assignment_p": reverse_rank / 120.0,
                "best_assignment": list(permutations[best_index]),
                "best_matched_score": float(column[best_index]),
            }
        )
    monotone_mode_ranks = [item["monotone_rank_of_120"] for item in mode_assignment_records]
    reverse_mode_ranks = [item["reverse_rank_of_120"] for item in mode_assignment_records]
    best_assignments = {tuple(item["best_assignment"]) for item in mode_assignment_records}
    mode_assignment_summary = {
        "assignment_count": len(ensemble_results),
        "monotone_rank_range_of_120": [min(monotone_mode_ranks), max(monotone_mode_ranks)],
        "monotone_exact_p_range": [min(monotone_mode_ranks) / 120.0, max(monotone_mode_ranks) / 120.0],
        "reverse_rank_range_of_120": [min(reverse_mode_ranks), max(reverse_mode_ranks)],
        "reverse_exact_p_range": [min(reverse_mode_ranks) / 120.0, max(reverse_mode_ranks) / 120.0],
        "distinct_best_assignment_count": len(best_assignments),
        "distinct_best_assignments": [list(item) for item in sorted(best_assignments)],
    }
    checks = {
        "nine_covariance_geometries_preserved": monotone["geometry_count"] == 9,
        "all_candidates_scored_without_geometry_selection": all(
            item["summary"]["geometry_count"] == 9 for item in candidate_results.values()
        ),
        "monotone_beats_lossless_all_geometries": monotone["matched_beats_lossless_geometries"] == 9,
        "reverse_beats_lossless_all_geometries": reverse["matched_beats_lossless_geometries"] == 9,
        "no_candidate_beats_every_wrong_assignment": all(
            item["summary"]["matched_beats_every_wrong_assignment_geometries"] == 0
            for item in candidate_results.values()
        ),
        "no_candidate_passes_exact_assignment_0_05": all(
            item["summary"]["exact_assignment_p_le_0_05_geometries"] == 0
            for item in candidate_results.values()
        ),
        "reverse_control_attains_better_rank_than_monotone": (
            min(reverse["exact_assignment_rank_p_value_range"])
            < min(monotone["exact_assignment_rank_p_value_range"])
        ),
        "all_120_mode_assignments_scored": len(ensemble_results) == 120,
        "monotone_not_selected_within_mode_assignments": min(monotone_mode_ranks) > 6,
        "best_mode_assignment_is_not_geometry_stable": len(best_assignments) > 1,
        "physical_endpoint_remains_unauthorized": True,
    }
    result = {
        "schema": "tau-core.paper8.sdp81-graph-spectral-terminal-calibration-score.v01",
        "status": "RETROSPECTIVE_DIAGNOSTIC_ONLY_NOT_ENDPOINT",
        "verdict": "CANONICAL_BASIS_DERIVED_MONOTONE_ASSIGNMENT_NOT_SUPPORTED",
        "model": str(MODEL.relative_to(ROOT)),
        "covariance_source": str(COVARIANCES.relative_to(ROOT)),
        "spectral_endpoint_read": True,
        "candidate_results": candidate_results,
        "monotone_summary": monotone,
        "reverse_summary": reverse,
        "isotropic_summary": isotropic,
        "mode_assignment_records": mode_assignment_records,
        "mode_assignment_summary": mode_assignment_summary,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "physical_endpoint_authorized": False,
        "confirmatory_prediction": False,
        "claim_boundary": (
            "The P6 graph gives a canonical mode basis, but the source-frozen "
            "monotone WR-T19 assignment is not selected by this endpoint: its exact "
            "path-assignment rank range is worse than the predeclared reverse control, "
            "and its rank within all 120 stiffness-to-mode assignments is only mid-pack. "
            "That comparison is retrospective and the depth remains a 4D Fermat "
            "proxy. It neither chooses a replacement assignment nor validates a "
            "parent-to-terminal calibration or Nature occupation."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 graph-spectral terminal-calibration score v01\n\n"
        f"Status: `{result['status']}`. Verdict: `{result['verdict']}`.\n\n"
        "The declared P6 graph removes arbitrary Helmert-column ordering. The "
        f"monotone assignment beats lossless in `{monotone['matched_beats_lossless_geometries']}/9` "
        "geometries, but never every wrong path assignment; its exact assignment-rank "
        f"range is `{monotone['exact_assignment_rank_p_value_range'][0]:.3f}--"
        f"{monotone['exact_assignment_rank_p_value_range'][1]:.3f}`. The reverse "
        f"control gives `{reverse['exact_assignment_rank_p_value_range'][0]:.3f}--"
        f"{reverse['exact_assignment_rank_p_value_range'][1]:.3f}`, and the isotropic "
        f"control gives `{isotropic['exact_assignment_rank_p_value_range'][0]:.3f}--"
        f"{isotropic['exact_assignment_rank_p_value_range'][1]:.3f}`.\n\n"
        f"Across all 120 stiffness-to-mode permutations, the monotone assignment "
        f"ranks `{mode_assignment_summary['monotone_rank_range_of_120'][0]}--"
        f"{mode_assignment_summary['monotone_rank_range_of_120'][1]}/120` "
        f"(`p={mode_assignment_summary['monotone_exact_p_range'][0]:.3f}--"
        f"{mode_assignment_summary['monotone_exact_p_range'][1]:.3f}`); the reverse "
        f"ranks `{mode_assignment_summary['reverse_rank_range_of_120'][0]}--"
        f"{mode_assignment_summary['reverse_rank_range_of_120'][1]}/120`. There are "
        f"`{mode_assignment_summary['distinct_best_assignment_count']}` distinct best "
        "assignments across the nine covariance geometries.\n\n"
        f"{result['claim_boundary']}\n",
        encoding="utf-8",
    )
    print(result["verdict"])


if __name__ == "__main__":
    main()
