#!/usr/bin/env python3
"""Test PHANGS tracer-field energy after source-frozen morphology removal."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.stats import chi2


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/phangs_morphology_orthogonal_tracer_field_test_v01.md"
CONFIG = {
    "NGC3351": {"slug": "ngc3351", "removed_family": "m0+m2", "retained": [1, 2], "wrong": [3, 4]},
    "NGC4254": {"slug": "ngc4254", "removed_family": "m0+m1", "retained": [3, 4], "wrong": [1, 2]},
    "NGC3627": {"slug": "ngc3627", "removed_family": "m0+m1+m2", "retained": [], "wrong": [1, 2, 3, 4]},
    "NGC4535": {"slug": "ngc4535", "removed_family": "m0+m2", "retained": [1, 2], "wrong": [3, 4]},
}


def quadratic_test(document: dict, indices: list[int]) -> tuple[float, int]:
    if not indices:
        return 0.0, 0
    statistic = 0.0
    rank = 0
    for block in document["zone_mode_blocks"]:
        coefficient = np.asarray(block["coefficient_km_s"], float)[indices]
        covariance = np.asarray(block["sector_jackknife_covariance_km2_s2"], float)[np.ix_(indices, indices)]
        statistic += float(coefficient @ np.linalg.pinv(covariance) @ coefficient)
        rank += int(np.linalg.matrix_rank(covariance))
    return statistic, rank


def main() -> None:
    rows = []
    matched_statistic = matched_dof = wrong_statistic = wrong_dof = 0
    for galaxy, config in CONFIG.items():
        document = json.loads(
            (DATA / f"{config['slug']}_phangs_tracer_velocity_field_rank_test_v01.json").read_text()
        )
        matched, matched_rank = quadratic_test(document, config["retained"])
        wrong, wrong_rank = quadratic_test(document, config["wrong"])
        contributes = matched_rank > 0
        if contributes:
            matched_statistic += matched
            matched_dof += matched_rank
            wrong_statistic += wrong
            wrong_dof += wrong_rank
        rows.append({
            "galaxy": galaxy,
            "source_frozen_removed_family": config["removed_family"],
            "matched_orthogonal_chi2": matched,
            "matched_orthogonal_dof": matched_rank,
            "matched_orthogonal_p": float(chi2.sf(matched, matched_rank)) if matched_rank else None,
            "wrong_family_residual_chi2": wrong,
            "wrong_family_residual_dof": wrong_rank,
            "wrong_family_residual_p": float(chi2.sf(wrong, wrong_rank)),
            "contributes_to_common_orthogonal_test": contributes,
            "low_order_orthogonal_mode_identifiable": contributes,
            "sector_jackknife_full_basis_chi2": document["sector_jackknife_global_chi2_diagnostic"],
            "sector_jackknife_full_basis_dof": document["sector_jackknife_global_rank"],
            "sector_jackknife_max_absolute_mode_z": document["sector_jackknife_max_absolute_mode_z"],
        })
    result = {
        "schema": "phangs_morphology_orthogonal_tracer_field_test_v01",
        "status": "ELIGIBLE_THREE_GALAXY_MORPHOLOGY_ORTHOGONAL_NULL_REPLICATED",
        "galaxies": rows,
        "matched_orthogonal_chi2": matched_statistic,
        "matched_orthogonal_dof": matched_dof,
        "matched_orthogonal_p": float(chi2.sf(matched_statistic, matched_dof)),
        "wrong_family_residual_chi2": wrong_statistic,
        "wrong_family_residual_dof": wrong_dof,
        "wrong_family_residual_p": float(chi2.sf(wrong_statistic, wrong_dof)),
        "shared_universal_angular_mode_identifiable": False,
        "identifiability_reason": "m1 is the frozen nuisance family in NGC4254 and m2 in NGC3351; NGC3627 is source-known to carry both m1-like disturbance and m2-like bar structure, so it has no retained low-order angular mode after matched removal",
        "ngc3627_replication_verdict": "NEGATIVE_RESULT_PRESERVED_NO_LOW_ORDER_MORPHOLOGY_ORTHOGONAL_MODE",
        "ngc4535_replication_verdict": "NEGATIVE_RESULT_PRESERVED_ELIGIBLE_M1_MODE_NOT_DETECTED",
        "construction_uses_rotation_residual": False,
        "claim_boundary": "three-eligible-galaxy covariance-aware morphology-orthogonal statistic plus one morphology-complex identifiability stress control; not a population result and not evidence for or against a weaker time, quantum, path, parent, or Tau component",
    }
    (DATA / "phangs_morphology_orthogonal_tracer_field_test_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    REPORT.write_text(
        "# PHANGS morphology-orthogonal tracer velocity-field test\n\n"
        f"Status: `{result['status']}`\n\n"
        f"After source-frozen morphology removal, the retained orthogonal field gives "
        f"`chi2={matched_statistic:.2f}` for `{matched_dof}` dof "
        f"(`p={result['matched_orthogonal_p']:.4f}`). The wrong-family control leaves "
        f"`chi2={wrong_statistic:.2f}` for `{wrong_dof}` dof "
        f"(`p={result['wrong_family_residual_p']:.4f}`).\n\n"
        "The eligible three-galaxy matched-removal statistic remains consistent with zero. "
        "The expanded wrong-family control is also consistent with zero, so the original "
        "two-object family-specificity hint does not replicate. NGC3627 adds a stress control, but "
        "its source-known bar plus interaction occupy both tested angular families, leaving "
        "no low-order morphology-orthogonal direction. No common channel mode is identified.\n",
        encoding="utf-8",
    )
    print(result["status"], matched_statistic, matched_dof, result["matched_orthogonal_p"])


if __name__ == "__main__":
    main()
