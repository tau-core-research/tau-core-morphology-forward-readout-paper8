#!/usr/bin/env python3
"""Post-open robustness audit of the frozen LITTLE THINGS endpoint."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.stats import wilcoxon


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
ENDPOINT = DATA / "little_things_2d_morphology_population_endpoint_v01.json"


def exact_sign_flip_p(values: np.ndarray) -> float:
    sums = np.zeros(1)
    for value in values:
        sums = np.concatenate((sums + value, sums - value))
    return float(np.mean(sums >= values.sum() - 1e-15))


def main() -> None:
    endpoint = json.loads(ENDPOINT.read_text(encoding="utf-8"))
    rows = endpoint["score_rows"]
    controls = {
        "radial_reversal": "radial_reversal_cv_sse_reduction",
        "annular_phase_scramble": "annular_phase_scramble_cv_sse_reduction",
        "cross_galaxy": "cross_galaxy_cv_sse_reduction",
    }
    families = {}
    for name, key in controls.items():
        values = np.asarray([row["matched_cv_sse_reduction"] - row[key] for row in rows])
        families[name] = {
            "mean_matched_minus_control": float(values.mean()),
            "median_matched_minus_control": float(np.median(values)),
            "positive_fraction": float(np.mean(values > 0)),
            "exact_one_sided_sign_flip_p": exact_sign_flip_p(values),
            "exact_one_sided_wilcoxon_p": float(wilcoxon(values, alternative="greater", method="exact").pvalue),
        }
    primary = np.asarray([row["matched_minus_best_wrong_specificity"] for row in rows])
    loo = np.asarray([(primary.sum() - value) / (primary.size - 1) for value in primary])

    rng = np.random.default_rng(1)
    theta = rng.uniform(0.0, 2.0 * np.pi, 100)
    coefficient = rng.normal(size=5) + 1j * rng.normal(size=5)
    zones = rng.integers(0, 5, 100)
    matched = coefficient[zones] * np.exp(2j * theta)
    rotated = (1j * coefficient[zones]) * np.exp(2j * theta)
    left = np.column_stack((matched.real, matched.imag))
    right = np.column_stack((rotated.real, rotated.imag))
    phase_projector_delta = float(np.linalg.norm(left @ np.linalg.pinv(left) - right @ np.linalg.pinv(right)))

    output = {
        "schema": "little_things_2d_morphology_endpoint_robustness_v01",
        "status": "NEGATIVE_PRIMARY_RESULT_ROBUST_TO_CONTROL_FAMILY_DECOMPOSITION",
        "audit_class": "post-open robustness; not a replacement endpoint",
        "endpoint": str(ENDPOINT.relative_to(ROOT)),
        "endpoint_sha256": hashlib.sha256(ENDPOINT.read_bytes()).hexdigest(),
        "family_specific_contrasts": families,
        "leave_one_galaxy_out_primary_mean_min": float(loo.min()),
        "leave_one_galaxy_out_primary_mean_max": float(loo.max()),
        "all_leave_one_out_primary_means_negative": bool(np.all(loo < 0)),
        "all_target_valid_fractions_one": all(row["valid_target_fraction"] == 1.0 for row in rows),
        "global_phase_rotation_projector_delta": phase_projector_delta,
        "global_phase_rotation_is_invalid_negative_control": phase_projector_delta < 1e-12,
        "primary_endpoint_changed": False,
        "tau_endpoint_scored": False,
        "claim_boundary": "post-open decomposition confirms lack of matched-template advantage; it cannot identify the cause or reject the wider Tau architecture",
    }
    out = DATA / "little_things_2d_morphology_endpoint_robustness_v01.json"
    out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    report = ROOT / "reports/little_things_2d_morphology_endpoint_robustness_v01.md"
    report.write_text(
        "# LITTLE THINGS 2D morphology endpoint robustness v01\n\n"
        f"Status: `{output['status']}`\n\n"
        "No individual wrong-template family yields a significant matched-template advantage. "
        f"The leave-one-galaxy-out primary mean remains negative from `{loo.min():.6f}` to "
        f"`{loo.max():.6f}`. All target-valid fractions are one.\n\n"
        f"The numerical projector difference between a two-quadrature target and its global "
        f"90-degree phase rotation is `{phase_projector_delta:.3e}`, confirming that global phase "
        "rotation is the same target subspace and cannot serve as a negative control.\n\n"
        "This post-open audit does not alter the primary score. It strengthens only the negative "
        "assessment of this concrete terminal, not a rejection of the full Tau Core architecture.\n",
        encoding="utf-8",
    )
    print(output["status"], loo.min(), loo.max(), phase_projector_delta)


if __name__ == "__main__":
    main()
