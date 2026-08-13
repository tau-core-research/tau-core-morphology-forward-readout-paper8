#!/usr/bin/env python3
"""Evaluate the source-frozen PHANGS confirmatory population endpoint."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.stats import chi2


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/phangs_population_channel_test_v01.md"
CONFIRMATORY = {"IC5332": "ic5332", "NGC4321": "ngc4321"}
RETAINED_M2 = [3, 4]
WRONG_M1 = [1, 2]


def quadratic_test(document: dict, indices: list[int]) -> tuple[float, int]:
    statistic = 0.0
    rank = 0
    for block in document["zone_mode_blocks"]:
        coefficient = np.asarray(block["coefficient_km_s"], float)[indices]
        covariance = np.asarray(block["sector_jackknife_covariance_km2_s2"], float)[np.ix_(indices, indices)]
        statistic += float(coefficient @ np.linalg.pinv(covariance) @ coefficient)
        rank += int(np.linalg.matrix_rank(covariance))
    return statistic, rank


def main() -> None:
    preregistration = json.loads(
        (DATA / "phangs_population_channel_preregistration_v01.json").read_text()
    )
    label_audit = json.loads(
        (DATA / "phangs_population_morphology_label_audit_v01.json").read_text()
    )
    frozen = preregistration["confirmatory_unopened_galaxies"]
    if frozen != list(CONFIRMATORY):
        raise RuntimeError(f"Confirmatory endpoint drifted from source freeze: {frozen}")
    if preregistration["construction_uses_tracer_contrast"]:
        raise RuntimeError("Preregistration is not tracer-contrast blind")

    galaxies = []
    retained_global = retained_dof = wrong_global = wrong_dof = 0
    individual_passes = []
    for galaxy, slug in CONFIRMATORY.items():
        document = json.loads(
            (DATA / f"{slug}_phangs_tracer_velocity_field_rank_test_v01.json").read_text()
        )
        if document["galaxy"] != galaxy:
            raise RuntimeError(f"Galaxy mismatch for {slug}")
        retained, retained_rank = quadratic_test(document, RETAINED_M2)
        wrong, wrong_rank = quadratic_test(document, WRONG_M1)
        retained_p = float(chi2.sf(retained, retained_rank))
        wrong_p = float(chi2.sf(wrong, wrong_rank))
        retained_global += retained
        retained_dof += retained_rank
        wrong_global += wrong
        wrong_dof += wrong_rank
        individual_passes.append(retained_p < 0.05)
        galaxies.append({
            "galaxy": galaxy,
            "beam_independent_pixels": document["beam_independent_pixels"],
            "retained_m2_chi2": retained,
            "retained_m2_dof": retained_rank,
            "retained_m2_p": retained_p,
            "wrong_family_m1_chi2": wrong,
            "wrong_family_m1_dof": wrong_rank,
            "wrong_family_m1_p": wrong_p,
            "individual_p_lt_0_05": retained_p < 0.05,
            "sector_jackknife_max_absolute_mode_z": document["sector_jackknife_max_absolute_mode_z"],
        })

    retained_p = float(chi2.sf(retained_global, retained_dof))
    wrong_p = float(chi2.sf(wrong_global, wrong_dof))
    numerical_gate_pass = retained_p < 0.01 and all(individual_passes)
    label_integrity_pass = label_audit["confirmatory_label_integrity_pass"]
    promotion_pass = numerical_gate_pass and label_integrity_pass
    if numerical_gate_pass and not label_integrity_pass:
        status = "PREREGISTERED_POPULATION_M2_NUMERICAL_GATE_PASSED_LABEL_INTEGRITY_FAILED"
    elif promotion_pass:
        status = "PREREGISTERED_POPULATION_M2_PROMOTION_GATE_PASSED"
    else:
        status = "PREREGISTERED_POPULATION_M2_PROMOTION_GATE_NOT_PASSED"
    result = {
        "schema": "phangs_population_channel_test_v01",
        "status": status,
        "confirmatory_galaxies": galaxies,
        "retained_family": "m2 after source-frozen m0+m1 nuisance removal",
        "global_retained_m2_chi2": retained_global,
        "global_retained_m2_dof": retained_dof,
        "global_retained_m2_p": retained_p,
        "wrong_family_control": "m1, does not enter the promotion decision",
        "global_wrong_family_m1_chi2": wrong_global,
        "global_wrong_family_m1_dof": wrong_dof,
        "global_wrong_family_m1_p": wrong_p,
        "promotion_rule": preregistration["promotion_rule"],
        "numerical_gate_passed": numerical_gate_pass,
        "confirmatory_morphology_label_integrity_pass": label_integrity_pass,
        "promotion_gate_passed": promotion_pass,
        "body_increment_score_open_allowed": promotion_pass,
        "body_increment_score_run": False,
        "construction_uses_rotation_residual": False,
        "time_channel_identified": False,
        "quantum_channel_identified": False,
        "claim_boundary": (
            "source-frozen two-galaxy population test of low-order differential CO/H-alpha m2 structure; "
            "a null constrains only this basis and sensitivity, while a positive result would remain tracer-field "
            "structure until body increment, nuisance, parity and independent replication gates are passed"
        ),
    }
    (DATA / "phangs_population_channel_test_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    verdict = (
        "The frozen numerical threshold passed, but the source morphology-label integrity audit failed. "
        "No body-increment score or replacement endpoint is authorized."
        if numerical_gate_pass and not label_integrity_pass
        else "The frozen promotion gate passed, but no physical origin is identified and the body-increment "
        "stage remains a separate frozen test."
        if promotion_pass
        else "The frozen promotion gate did not pass. No body-increment score is authorized, and no replacement endpoint is selected."
    )
    REPORT.write_text(
        "# PHANGS preregistered population channel test v01\n\n"
        f"Status: `{status}`\n\n"
        f"The confirmatory `IC5332 + NGC4321` retained `m2` block gives "
        f"`chi2={retained_global:.3f}` for `{retained_dof}` dof (`p={retained_p:.4g}`). "
        f"The non-decisional wrong-family `m1` control gives `chi2={wrong_global:.3f}` "
        f"for `{wrong_dof}` dof (`p={wrong_p:.4g}`).\n\n"
        f"{verdict}\n\n"
        "This endpoint does not identify observer-time, quantum, path, Tau Core, or dark-sector origin.\n",
        encoding="utf-8",
    )
    print(status, retained_global, retained_dof, retained_p)


if __name__ == "__main__":
    main()
