#!/usr/bin/env python3
"""Audit channel novelty above the frozen morphology-hosted body baseline."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
STEM = "morphology_conditioned_channel_novelty_audit_v01"


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def main() -> None:
    baseline = load("joint_readout_body_dominant_baseline_selection_v01.json")
    bounded = load("body_conditioned_bounded_channel_score_v01.json")
    conditional = load("same_body_joint_conditional_information_v01.json")
    dark_zone = load("dark_discrepancy_zone_multitracer_channel_audit_v01.json")
    exclusion = load("common_channel_exclusion_matrix_v01.json")
    ngc3351 = load("ngc3351_phangs_tracer_velocity_field_rank_test_v01.json")
    ngc4254 = load("ngc4254_phangs_tracer_velocity_field_rank_test_v01.json")
    population = load("phangs_population_channel_test_v01.json")
    population_labels = load("phangs_population_morphology_label_audit_v01.json")
    nuisance_atlas = load("phangs_source_certified_morphology_nuisance_atlas_v02.json")

    # Two independent noisy measurements of the same scalar source improve
    # precision without opening a new source direction.
    c_first = np.array([[1.0]])
    c_second = np.array([[1.0]])
    rank_first = int(np.linalg.matrix_rank(c_first))
    rank_stacked = int(np.linalg.matrix_rank(np.vstack([c_first, c_second])))
    i_first = 0.5 * np.log2(2.0)
    i_joint = 0.5 * np.log2(3.0)
    conditional_precision_bits = float(i_joint - i_first)

    # A genuinely transverse terminal sees a source direction hidden from the
    # first readout and therefore raises stacked rank.
    c_old = np.array([[1.0, 0.0]])
    c_novel = np.array([[0.0, 1.0]])
    transverse_rank_increment = int(
        np.linalg.matrix_rank(np.vstack([c_old, c_novel]))
        - np.linalg.matrix_rank(c_old)
    )

    decision_rule = {
        "source_freeze": "the body descriptor and terminal operator are fixed without rotation residuals",
        "structural_novelty": "rank([C_existing;C_new])-rank(C_existing)>0 or nonfactorization is independently proved",
        "innovation": "the new-mode contrast survives declared nuisance covariance and parity controls",
        "body_increment": "the frozen body-plus-channel model improves grouped holdout prediction over the frozen body model",
        "replication": "the same signed/mode-specific rule survives an independent body or path",
        "promotion": "all five conditions are required for a detected nonconventional channel component",
    }

    candidates = [
        {
            "candidate": "bounded_population_sightline_load",
            "source_frozen": True,
            "structural_novelty": False,
            "innovation_survives": False,
            "body_increment_pass": bounded["selected_lambda_train_only"] != 0
            and bounded["mean_joint_minus_body_rmse_km_s"] < 0,
            "independent_replication": False,
            "reason": "train selects lambda=0; no holdout increment over the body model",
        },
        {
            "candidate": "same_body_hi_halpha_radial_pair",
            "source_frozen": True,
            "structural_novelty": conditional["stacked_rank_increment"] > 0,
            "innovation_survives": conditional["shared_source_innovation_null_rejected"],
            "body_increment_pass": False,
            "independent_replication": False,
            "reason": "positive conditional information is shared-source precision gain with zero stacked-rank increment",
        },
        {
            "candidate": "dark_discrepancy_zone_hi_halpha_contrast",
            "source_frozen": not dark_zone["retrospective_zone_audit"],
            "structural_novelty": False,
            "innovation_survives": dark_zone["zero_contrast_rejected_in_both_galaxies"],
            "body_increment_pass": False,
            "independent_replication": dark_zone["zero_contrast_rejected_in_both_galaxies"],
            "reason": "retrospective two-body contrast does not replicate and does not reach the body-increment score",
        },
        {
            "candidate": "phangs_2d_morphology_conditioned_tracer_modes",
            "source_frozen": True,
            "structural_novelty": True,
            "innovation_survives": min(
                ngc3351["sector_jackknife_max_absolute_mode_z"],
                ngc4254["sector_jackknife_max_absolute_mode_z"],
            ) >= 3.0,
            "body_increment_pass": False,
            "independent_replication": False,
            "reason": "the 2D harmonic carrier can represent transverse modes, but both robust maxima remain below 3 sigma and no body-increment endpoint was run",
        },
        {
            "candidate": "phangs_preregistered_population_m2_mode",
            "source_frozen": True,
            "structural_novelty": False,
            "innovation_survives": False,
            "body_increment_pass": population["body_increment_score_run"],
            "independent_replication": population["numerical_gate_passed"],
            "reason": (
                "the frozen numerical m2 threshold passes, but the m1 control is also non-null and "
                "the confirmatory nonbarred label fails source integrity; no morphology-specific "
                "nonfactorization or body increment is established"
            ),
        },
        {
            "candidate": "universal_tracer_independent_scalar",
            "source_frozen": True,
            "structural_novelty": False,
            "innovation_survives": False,
            "body_increment_pass": False,
            "independent_replication": False,
            "reason": exclusion["excluded_candidate_family"],
        },
    ]
    for row in candidates:
        row["promotion_pass"] = all(
            row[key]
            for key in (
                "source_frozen",
                "structural_novelty",
                "innovation_survives",
                "body_increment_pass",
                "independent_replication",
            )
        )

    payload = {
        "schema": "tau-core.paper8.morphology-conditioned-channel-novelty-audit.v01",
        "status": "NO_CURRENT_CHANNEL_CANDIDATE_PASSES_MORPHOLOGY_CONDITIONED_NOVELTY_RULE",
        "baseline_status": baseline["status"],
        "theorem": (
            "positive conditional information does not prove a new channel mode; "
            "structural novelty requires a source-frozen stacked-rank increment or "
            "independently proved nonfactorization"
        ),
        "decision_rule": decision_rule,
        "finite_witnesses": {
            "duplicate_readout_rank_before": rank_first,
            "duplicate_readout_rank_after": rank_stacked,
            "duplicate_readout_rank_increment": rank_stacked - rank_first,
            "duplicate_readout_positive_conditional_information_bits": conditional_precision_bits,
            "transverse_readout_rank_increment": transverse_rank_increment,
        },
        "current_candidates": candidates,
        "candidate_count": len(candidates),
        "promotion_pass_count": sum(row["promotion_pass"] for row in candidates),
        "next_single_measurement": (
            "the source-certified nuisance atlas leaves no untouched low-order endpoint; close the "
            "m1/m2 selection lane and freeze a higher-dimensional morphology basis before new contrasts"
        ),
        "time_status": "not identified; any time interpretation is downstream of a detected differential channel mode",
        "quantum_status": "not identified; no frequency/polarization nonfactorization measurement is present",
        "population_label_integrity_pass": population_labels["confirmatory_label_integrity_pass"],
        "untouched_low_order_endpoint_count": nuisance_atlas["untouched_low_order_endpoint_count"],
        "claim_boundary": (
            "finite decision audit over existing Paper 8 results; it neither proves "
            "channel absence nor permits residual-based channel construction"
        ),
    }

    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (DATA / f"{STEM}.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    rows = "\n".join(
        "| {candidate} | {source_frozen} | {structural_novelty} | "
        "{innovation_survives} | {body_increment_pass} | "
        "{independent_replication} | {promotion_pass} |".format(**row)
        for row in candidates
    )
    (REPORTS / f"{STEM}.md").write_text(
        "# Morphology-Conditioned Channel Novelty Audit v0.1\n\n"
        f"**Status:** `{payload['status']}`\n\n"
        "Positive conditional information can arise when two noisy terminals observe "
        "the same source direction. In the finite duplicate-readout witness it is "
        f"`{conditional_precision_bits:.6f}` bits although stacked-rank increment is "
        "zero. The transverse witness raises rank by one.\n\n"
        "| candidate | frozen | rank/nonfactor | innovation | body increment | replication | promote |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
        f"{rows}\n\n"
        "No current candidate passes the joint rule. The next single measurement is a "
        "source-frozen 2D morphology-conditioned differential tracer mode replicated "
        "on an independent galaxy and scored as an increment over the frozen body "
        "predictor. Time or quantum origin is not assigned at this stage.\n",
        encoding="utf-8",
    )
    print(payload["status"])


if __name__ == "__main__":
    main()
