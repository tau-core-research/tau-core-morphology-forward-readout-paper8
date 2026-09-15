#!/usr/bin/env python3
"""Freeze the v04-compatible occupied-sector EDGE--CALIFA scoring contract."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np

from freeze_edge_califa_rotation_morphology_scoring_contract_v01 import (
    N_MODES,
    N_SECTORS,
    N_ZONES,
    assemble_covariance,
    exact_shared_sign_tests,
    fit_modes,
    phase_rotate_pi_over_2,
    radial_reverse,
    score,
    stable_rank,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
PREREG = DATA / "edge_califa_rotation_morphology_preregistration_v04.json"
PREFLIGHT = DATA / "edge_califa_rotation_morphology_source_preflight_v02.json"
MATRICES = DATA / "edge_califa_rotation_morphology_source_matrices_v02.npz"
V01 = DATA / "edge_califa_rotation_morphology_scoring_contract_v01.json"
OUTPUT = DATA / "edge_califa_rotation_morphology_scoring_contract_v02.json"
HASH = DATA / "edge_califa_rotation_morphology_scoring_contract_v02.sha256"
REPORT = ROOT / "reports/edge_califa_rotation_morphology_scoring_contract_v02.md"
MIN_OCCUPIED_SECTORS = 5


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def occupied_sector_jackknife_block(
    design: np.ndarray, values: np.ndarray, variance: np.ndarray, sectors: np.ndarray
) -> np.ndarray:
    occupied = sorted(int(value) for value in np.unique(sectors))
    if len(occupied) < MIN_OCCUPIED_SECTORS or len(occupied) > N_SECTORS:
        raise ValueError("A zone must occupy five or six frozen macrosectors")
    estimates = []
    for omitted in occupied:
        keep = sectors != omitted
        estimates.append(fit_modes(design[keep], values[keep], variance[keep]))
    estimates = np.asarray(estimates)
    mean = estimates.mean(axis=0)
    j_count = len(occupied)
    covariance = (j_count - 1) / j_count * (estimates - mean).T @ (estimates - mean)
    retained = covariance[np.ix_([1, 2, 3, 4], [1, 2, 3, 4])]
    if stable_rank(retained) != N_MODES:
        raise ValueError("Occupied-sector jackknife covariance is not rank four")
    if np.min(np.linalg.eigvalsh(retained)) <= 0:
        raise ValueError("Occupied-sector jackknife covariance is not positive definite")
    return retained


def synthetic_covariance_audit() -> dict[str, Any]:
    rng = np.random.default_rng(20260831)
    blocks = []
    occupied_counts = []
    for zone in range(N_ZONES):
        count = 5 if zone % 2 == 0 else 6
        occupied = np.arange(count)
        sectors = np.repeat(occupied, 12)
        angle = 2 * np.pi * (sectors + rng.uniform(0.05, 0.95, sectors.size)) / N_SECTORS - np.pi
        design = np.column_stack([
            np.ones(angle.size), np.cos(angle), np.sin(angle),
            np.cos(2 * angle), np.sin(2 * angle),
        ])
        variance = rng.uniform(0.5, 2.0, angle.size)
        truth = np.array([0.2, 1.0, -0.6, 0.4, -0.3]) * (zone + 1)
        values = design @ truth + rng.normal(scale=np.sqrt(variance))
        blocks.append(occupied_sector_jackknife_block(design, values, variance, sectors))
        occupied_counts.append(count)
    covariance = assemble_covariance(blocks)
    source = rng.normal(size=(20, 16))
    while stable_rank(source) != 16:
        source = rng.normal(size=(20, 16))
    terminal = source @ rng.normal(size=16)
    projected = score(source, covariance, terminal)
    return {
        "occupied_sector_counts": occupied_counts,
        "zone_covariance_ranks": [stable_rank(block) for block in blocks],
        "assembled_covariance_rank": stable_rank(covariance),
        "minimum_eigenvalue": float(np.min(np.linalg.eigvalsh(covariance))),
        "pure_source_q": projected["q"],
        "projected_rank": projected["projected_covariance_rank"],
        "all_gates_pass": bool(
            all(stable_rank(block) == 4 for block in blocks)
            and stable_rank(covariance) == 20
            and projected["projected_covariance_rank"] == 4
            and projected["q"] < 1.0e-8
        ),
    }


def main() -> None:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    if preflight["velocity_terminal_values_opened"]:
        raise RuntimeError("Confirmatory values must remain unopened during contract freeze")
    names = list(preflight["confirmatory_untouched"])
    packet = np.load(MATRICES)
    rank_rows = []
    for index, name in enumerate(names):
        standard = packet[f"{name}__standard"]
        body = packet[f"{name}__body"]
        cross_name = names[(index + 1) % len(names)]
        sources = {
            "correct": np.column_stack([standard, body]),
            "radial_reversal": np.column_stack([standard, radial_reverse(body)]),
            "phase_rotation_pi_over_2": np.column_stack([standard, phase_rotate_pi_over_2(body)]),
            "cross_galaxy": np.column_stack([standard, packet[f"{cross_name}__body"]]),
        }
        row = {"galaxy": name, "cross_galaxy_body": cross_name}
        row.update({f"{label}_rank": stable_rank(value) for label, value in sources.items()})
        row["all_equal_rank_16"] = all(stable_rank(value) == 16 for value in sources.values())
        rank_rows.append(row)
    audit = synthetic_covariance_audit()
    if not audit["all_gates_pass"] or not all(row["all_equal_rank_16"] for row in rank_rows):
        raise RuntimeError("v02 unopened scoring contract failed its algebraic audit")
    result = {
        "schema": "edge_califa_rotation_morphology_scoring_contract_v02",
        "status": "V02_OCCUPIED_SECTOR_SCORING_CONTRACT_FROZEN_AND_AUDITED",
        "supersedes_v01_sha256": sha256(V01),
        "preregistration_sha256": sha256(PREREG),
        "source_preflight_sha256": sha256(PREFLIGHT),
        "source_matrices_sha256": sha256(MATRICES),
        "confirmatory_galaxies": names,
        "source_control_rank_audit": rank_rows,
        "synthetic_covariance_audit": audit,
        "sector_rule": (
            "five or six occupied fixed macrosectors; delete one occupied sector at a time; "
            "unregularized retained 4x4 covariance must be full rank and positive definite"
        ),
        "per_galaxy_primary": "D_g=mean(Q_radial,Q_phase,Q_cross)-Q_correct",
        "primary_inference": "exact one-sided shared-sign permutation over all 2^N sign vectors",
        "control_inference": "exact shared-sign studentized max-T across the three controls",
        "thresholds": {
            "primary_p_less_than": 0.01,
            "median_d_positive": True,
            "strictly_more_than_fraction_positive": 0.60,
            "every_control_max_t_adjusted_p_less_than": 0.05,
        },
        "confirmatory_terminal_values_opened": False,
        "claim_boundary": (
            "development-informed source-frozen external prevalidation; not a Tau-specific "
            "prediction and not an exhaustive standard-astrophysics comparator"
        ),
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    HASH.write_text(f"{digest}  data/derived/{OUTPUT.name}\n", encoding="utf-8")
    REPORT.write_text(
        "# EDGE--CALIFA scoring contract v02\n\n"
        f"Status: `{result['status']}`\n\n"
        "Synthetic five- and six-sector zones both retain rank-four unregularized covariance. "
        "All seven correct/control source constructions remain equal-rank. Confirmatory "
        "velocity values remain unopened.\n",
        encoding="utf-8",
    )
    print(result["status"], digest)


if __name__ == "__main__":
    main()
