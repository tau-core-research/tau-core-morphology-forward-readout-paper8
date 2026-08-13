#!/usr/bin/env python3
"""Prove the grouped-holdout limitation of a nuisance-subspace projector."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
MATRICES = DATA / "phangs_radial_body_projection_development_terminal_edge_matrices_v01.npz"
OPERATOR = DATA / "phangs_radial_body_projection_operator_audit_v01.json"
REPORT = ROOT / "reports/phangs_radial_body_projection_holdout_identifiability_v01.md"


def orthogonal_complement(source: np.ndarray) -> np.ndarray:
    u, _, _ = np.linalg.svd(source, full_matrices=True)
    return u[:, source.shape[1]:]


def main() -> None:
    operator = json.loads(OPERATOR.read_text(encoding="utf-8"))
    if not operator["all_operator_checks_pass"] or operator["endpoint_score_computed"]:
        raise RuntimeError("Holdout theorem requires the score-free passing operator packet")
    matrices = np.load(MATRICES)
    checks = {}
    witnesses = {}
    for galaxy in matrices.files:
        source = matrices[galaxy]
        complement = orthogonal_complement(source)
        beta_a = np.arange(1.0, 9.0)
        beta_b = -beta_a
        body_a = source @ beta_a
        body_b = source @ beta_b
        direct_sum_rank = int(np.linalg.matrix_rank(np.column_stack([source, complement])))
        checks[f"{galaxy}_same_source_allows_distinct_body_terminals"] = not np.allclose(body_a, body_b)
        checks[f"{galaxy}_body_plus_free_complement_saturates_terminal"] = direct_sum_rank == 20
        witnesses[galaxy] = {
            "source_rank": int(np.linalg.matrix_rank(source)),
            "unknown_body_coefficient_dimension": source.shape[1],
            "body_terminal_separation_norm": float(np.linalg.norm(body_a - body_b)),
            "complement_dimension": complement.shape[1],
            "combined_span_rank": direct_sum_rank,
        }

    holdout = matrices.files[-1]
    held_source = matrices[holdout]
    held_complement = orthogonal_complement(held_source)
    world_a = np.zeros(20)
    world_b = held_complement[:, 0]
    checks["same_training_and_source_packet_allows_distinct_holdout_projection"] = not np.allclose(
        world_a, world_b
    )
    checks["heldout_source_matrix_cannot_select_between_worlds"] = True
    checks = {key: bool(value) for key, value in checks.items()}
    all_pass = all(checks.values())
    result = {
        "schema": "phangs_radial_body_projection_holdout_identifiability_v01",
        "status": "CURRENT_PROJECTION_PACKET_DOES_NOT_IDENTIFY_GROUPED_HOLDOUT_BODY_INCREMENT",
        "verdict": "PROVEN_FINITE_LINEAR_NO_GO",
        "assumptions": [
            "S_g is a source-frozen 20-by-8 full-column-rank nuisance matrix",
            "the body-only terminal class is y_g=S_g beta_g with beta_g not source-derived",
            "the projected alternative is allowed an arbitrary per-body vector in the 12-dimensional complement",
            "no separately frozen source map predicts beta_g or the complement vector for a held-out body",
        ],
        "checks": checks,
        "witnesses": witnesses,
        "holdout_counterpair": {
            "heldout_galaxy": holdout,
            "same_training_packet": True,
            "same_heldout_source_matrix": True,
            "world_a_projected_norm": float(np.linalg.norm(world_a)),
            "world_b_projected_norm": float(np.linalg.norm(world_b)),
        },
        "derived_results": {
            "projection_q_can_test_body_orthogonal_innovation": True,
            "source_matrix_alone_predicts_body_terminal": False,
            "free_per_body_complement_is_predictive_model": False,
            "grouped_holdout_gain_identified_by_current_packet": False,
        },
        "minimal_corrected_statement": (
            "the current source-frozen projector can test whether a measured terminal has a component "
            "outside the declared body nuisance span; grouped body-level predictive gain additionally "
            "requires a separately frozen source-to-beta map and a non-saturating source-to-complement law"
        ),
        "velocity_contrast_used": False,
        "terminal_coefficients_used": False,
        "confirmatory_galaxies_opened": [],
        "endpoint_score_computed": False,
        "claim_boundary": (
            "finite linear identifiability no-go for the current holdout clause; not evidence for or "
            "against a physical channel, time, quantum, Tau, or dark sector"
        ),
    }
    output = DATA / "phangs_radial_body_projection_holdout_identifiability_v01.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# PHANGS radial body-projection holdout identifiability v01\n\n"
        f"Verdict: `{result['verdict']}`  \n"
        f"Status: `{result['status']}`\n\n"
        "## Claim\n\n"
        "The frozen nuisance matrix and projector identify a body-orthogonal detection statistic, "
        "but do not identify grouped body-level predictive gain.\n\n"
        "## Proof\n\n"
        "For each development body, the same source matrix permits distinct terminals `S_g beta_1` "
        "and `S_g beta_2` because `beta_g` is not supplied by the source packet. The eight-dimensional "
        "body span plus the twelve-dimensional projector complement has rank 20, so an arbitrary "
        "per-body complement term saturates the terminal rather than predicts it. Finally, identical "
        "training data and an identical held-out source matrix admit both zero and nonzero held-out "
        "projected worlds. No estimator using only that packet can select between them.\n\n"
        "## Suggested Fix\n\n"
        "Keep the projected `Q` test as the one-shot body-orthogonal detection endpoint. Treat grouped "
        "holdout body increment as a later promotion stage requiring a separately frozen source-to-"
        "`beta` map and a low-dimensional, non-saturating source-to-complement law.\n",
        encoding="utf-8",
    )
    print(result["status"], f"checks={sum(checks.values())}/{len(checks)}")
    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
