#!/usr/bin/env python3
"""Run the frozen LITTLE THINGS morphology-to-kinematics sensitivity endpoint."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from astropy.io import fits
from scipy.stats import spearmanr

from freeze_little_things_2d_morphology_operator_calibration_v01 import (
    cv_improvement,
    cv_predictors,
    descriptor_array,
    design,
    rank,
    sample_source,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
LAUNCH = DATA / "little_things_2d_morphology_endpoint_launch_freeze_v01.json"
TARGETS = DATA / "little_things_2d_morphology_velocity_acquisition_v01.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_sign_flip_p(values: np.ndarray) -> float:
    observed = float(values.sum())
    sums = np.zeros(1)
    for value in values:
        sums = np.concatenate((sums + value, sums - value))
    return float(np.mean(sums >= observed - 1e-15))


def main() -> None:
    launch = json.loads(LAUNCH.read_text(encoding="utf-8"))
    targets = json.loads(TARGETS.read_text(encoding="utf-8"))
    script_path = Path(__file__).resolve()
    if launch["scoring_script_sha256"] != sha256(script_path):
        raise RuntimeError("Scoring implementation changed after launch freeze")
    if targets["launch_freeze_sha256"] != sha256(LAUNCH):
        raise RuntimeError("Velocity acquisition does not match launch freeze")
    if targets["status"] != "FROZEN_VELOCITY_PRODUCTS_ACQUIRED_UNOPENED":
        raise RuntimeError("Frozen velocity products are incomplete")
    preflight_path = ROOT / launch["source_preflight"]
    operator_path = ROOT / launch["operator_calibration"]
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    operator = json.loads(operator_path.read_text(encoding="utf-8"))
    support_rows = {
        row["galaxy"]: row
        for row in csv.DictReader((ROOT / preflight["support_ledger"]).open(encoding="utf-8"))
    }
    target_rows = {
        row["galaxy"]: row
        for row in csv.DictReader((ROOT / targets["ledger"]).open(encoding="utf-8"))
    }
    frozen_rows = launch["targets"]
    calibration = {row["galaxy"]: row for row in operator["results"]}

    score_rows = []
    endpoint_failures = []
    for galaxy in launch["eligible_galaxies"]:
        support = support_rows[galaxy]
        support["beam_geometric_mean_arcsec"] = float(support["beam_geometric_mean_arcsec"])
        descriptor = preflight["source_descriptors"][galaxy]
        theta, rho, blocks, xx, yy = sample_source(support, descriptor)
        target_path = ROOT / target_rows[galaxy]["local_path"]
        if sha256(target_path) != target_rows[galaxy]["sha256"]:
            raise RuntimeError(f"Velocity-product hash mismatch for {galaxy}")
        with fits.open(target_path, memmap=True) as hdul:
            velocity = np.asarray(np.squeeze(hdul[0].data), dtype=float)
        if velocity.shape != tuple(frozen_rows[galaxy]["expected_image_shape"]):
            endpoint_failures.append({"galaxy": galaxy, "reason": "target_shape_mismatch"})
            continue
        y = velocity[yy, xx]
        valid = np.isfinite(y)
        if float(valid.mean()) < 0.70:
            endpoint_failures.append({"galaxy": galaxy, "reason": "target_valid_fraction_below_0.70"})
            continue
        theta, rho, blocks, y = theta[valid], rho[valid], blocks[valid], y[valid]
        zones = descriptor["radial_capacity_j"]
        matched_coeff = descriptor_array(preflight, galaxy, zones)
        x, matched = design(theta, rho, matched_coeff, zones)
        phases = np.exp(1j * (np.arange(zones) % 4) * (math.pi / 2.0))
        other = preflight["cross_galaxy_derangement"][galaxy]
        wrong_designs = {
            "radial_reversal": design(theta, rho, matched_coeff[::-1], zones)[1],
            "annular_phase_scramble": design(theta, rho, matched_coeff * phases, zones)[1],
            "cross_galaxy": design(theta, rho, descriptor_array(preflight, other, zones), zones)[1],
        }
        fold_ok = True
        nuisance_rank = rank(x)
        for block in range(8):
            train = blocks != block
            test = ~train
            fold_ok &= (
                rank(x[train]) == nuisance_rank
                and rank(np.column_stack((x[train], matched[train]))) - rank(x[train]) == 2
                and rank(np.column_stack((x[test], matched[test]))) - rank(x[test]) == 2
            )
        if not fold_ok:
            endpoint_failures.append({"galaxy": galaxy, "reason": "post_target_missingness_rank_gate"})
            continue
        matched_gain = cv_improvement(y, cv_predictors(x, matched, blocks))
        wrong_gains = {
            name: cv_improvement(y, cv_predictors(x, candidate, blocks))
            for name, candidate in wrong_designs.items()
        }
        specificity = matched_gain - max(wrong_gains.values())
        source_row = frozen_rows[galaxy]
        score_rows.append({
            "galaxy": galaxy,
            "valid_target_fraction": float(valid.mean()),
            "independent_samples": int(y.size),
            "matched_cv_sse_reduction": matched_gain,
            "radial_reversal_cv_sse_reduction": wrong_gains["radial_reversal"],
            "annular_phase_scramble_cv_sse_reduction": wrong_gains["annular_phase_scramble"],
            "cross_galaxy_cv_sse_reduction": wrong_gains["cross_galaxy"],
            "matched_minus_best_wrong_specificity": specificity,
            "above_gaussian_null_95": specificity > calibration[galaxy]["null_specificity_95"],
            "published_hi_asymmetry": source_row["published_hi_asymmetry"],
            "published_hi_asymmetry_error": source_row["published_hi_asymmetry_error"],
        })

    values = np.asarray([row["matched_minus_best_wrong_specificity"] for row in score_rows])
    if values.size:
        mean_specificity = float(np.mean(values))
        median_specificity = float(np.median(values))
        positive_fraction = float(np.mean(values > 0))
        sign_flip_p = exact_sign_flip_p(values)
    else:
        mean_specificity = median_specificity = positive_fraction = sign_flip_p = None
    secondary = [row for row in score_rows if row["published_hi_asymmetry_error"] > 0]
    if len(secondary) >= 3:
        spearman = spearmanr(
            [row["published_hi_asymmetry"] for row in secondary],
            [row["matched_minus_best_wrong_specificity"] for row in secondary],
        )
        asymmetry_secondary = {"n": len(secondary), "rho": float(spearman.statistic), "two_sided_p": float(spearman.pvalue)}
    else:
        asymmetry_secondary = None
    population_gate = len(score_rows) >= launch["success_gate"]["minimum_endpoint_galaxies"]
    success = bool(
        population_gate
        and mean_specificity > 0
        and median_specificity > 0
        and positive_fraction >= launch["success_gate"]["minimum_positive_fraction"]
        and sign_flip_p <= launch["success_gate"]["maximum_one_sided_sign_flip_p"]
    )
    if not population_gate:
        status = "ENDPOINT_BLOCKED_BY_POST_TARGET_POPULATION_GATE"
    elif success:
        status = "CONVENTIONAL_MORPHOLOGY_SENSITIVITY_PASS"
    else:
        status = "CONVENTIONAL_MORPHOLOGY_SENSITIVITY_NOT_DEMONSTRATED"
    output = {
        "schema": "little_things_2d_morphology_population_endpoint_v01",
        "status": status,
        "launch_freeze": str(LAUNCH.relative_to(ROOT)),
        "launch_freeze_sha256": sha256(LAUNCH),
        "velocity_acquisition": str(TARGETS.relative_to(ROOT)),
        "velocity_acquisition_sha256": sha256(TARGETS),
        "frozen_target_count": len(launch["eligible_galaxies"]),
        "scored_galaxy_count": len(score_rows),
        "endpoint_failures": endpoint_failures,
        "mean_specificity": mean_specificity,
        "median_specificity": median_specificity,
        "positive_fraction": positive_fraction,
        "exact_one_sided_sign_flip_p": sign_flip_p,
        "published_asymmetry_secondary": asymmetry_secondary,
        "score_rows": score_rows,
        "conventional_morphology_sensitivity_demonstrated": success,
        "tau_endpoint_scored": False,
        "parent_loss_inferred": False,
        "gravity_or_dark_matter_claim_allowed": False,
        "claim_boundary": "observational same-tracer morphology-sensitivity control; conventional lopsided, tidal, feedback, projection, and shared-mask mechanisms remain sufficient alternatives",
    }
    out = DATA / "little_things_2d_morphology_population_endpoint_v01.json"
    out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    report = ROOT / "reports/little_things_2d_morphology_population_endpoint_v01.md"
    report.write_text(
        "# LITTLE THINGS 2D morphology population endpoint v01\n\n"
        f"Status: `{status}`\n\n"
        f"Scored galaxies: **{len(score_rows)}/{len(launch['eligible_galaxies'])}**. Mean matched-minus-best-wrong "
        f"specificity: `{mean_specificity}`; median: `{median_specificity}`; positive fraction: "
        f"`{positive_fraction}`; exact one-sided sign-flip p: `{sign_flip_p}`.\n\n"
        "The result tests whether the source-frozen H I m=1 pattern predicts held-out H I velocity "
        "structure better than three predeclared wrong-template families. It is not a dark-matter, "
        "gravity, parent-loss, or Tau endpoint; ordinary gas dynamics and shared moment-map construction "
        "remain live explanations even when the conventional sensitivity gate passes.\n",
        encoding="utf-8",
    )
    print(status, len(score_rows), mean_specificity, median_specificity, positive_fraction, sign_flip_p)


if __name__ == "__main__":
    main()
