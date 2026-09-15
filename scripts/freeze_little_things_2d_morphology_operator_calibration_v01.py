#!/usr/bin/env python3
"""Freeze and velocity-blind calibrate the LITTLE THINGS m=1 -> k=2 operator."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import label


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
FREEZE = DATA / "little_things_2d_morphology_population_preregistration_v01.json"
PREFLIGHT = DATA / "little_things_2d_morphology_source_preflight_v01.json"
TRIALS = 128
AMPLITUDES = (0.0, 0.5, 1.0, 2.0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank(matrix: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(matrix, tol=max(matrix.shape) * np.finfo(float).eps * np.linalg.norm(matrix, 2)))


def projected_target(x: np.ndarray, g: np.ndarray) -> np.ndarray:
    return g - x @ np.linalg.lstsq(x, g, rcond=None)[0]


def normalized_columns(g: np.ndarray) -> np.ndarray:
    scales = np.sqrt(np.mean(g * g, axis=0))
    return g / scales


def design(theta: np.ndarray, rho: np.ndarray, coefficient: np.ndarray, zones: int) -> tuple[np.ndarray, np.ndarray]:
    zone = np.minimum((rho * zones).astype(int), zones - 1)
    x_columns = [np.ones(theta.size)]
    for j in range(zones):
        indicator = (zone == j).astype(float)
        x_columns.extend((indicator * np.cos(theta), indicator * np.sin(theta)))
    x = np.column_stack(x_columns)
    local = coefficient[zone] * np.exp(2j * theta)
    g = np.column_stack((local.real, local.imag))
    return x, normalized_columns(g)


def descriptor_array(preflight: dict, galaxy: str, zones: int) -> np.ndarray:
    source = preflight["source_descriptors"][galaxy]["m1_radial_descriptor"]
    native = np.asarray([complex(row["m1_real"], row["m1_imag"]) for row in source])
    native_rho = (np.arange(native.size) + 0.5) / native.size
    target_rho = (np.arange(zones) + 0.5) / zones
    return np.interp(target_rho, native_rho, native.real) + 1j * np.interp(target_rho, native_rho, native.imag)


def sample_source(row: dict, descriptor: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    path = ROOT / row["source_map"]
    with fits.open(path, memmap=True) as hdul:
        image = np.asarray(np.squeeze(hdul[0].data), dtype=float)
        wcs = WCS(hdul[0].header).celestial
    components, count = label(np.isfinite(image) & (image > 0), np.ones((3, 3), dtype=int))
    sizes = np.bincount(components.ravel())
    component = components == (1 + int(np.argmax(sizes[1:])))
    yy, xx = np.nonzero(component)
    intensity = image[yy, xx]
    center = SkyCoord(
        descriptor["catalog_center_ra_deg"], descriptor["catalog_center_dec_deg"], unit="deg"
    )
    x0, y0 = wcs.world_to_pixel_values(center.ra.deg, center.dec.deg)
    delta = wcs.pixel_scale_matrix @ np.vstack((xx - x0, yy - y0))
    east = delta[0] * math.cos(center.dec.rad) * 3600.0
    north = delta[1] * 3600.0
    pa = math.radians(descriptor["optical_pa_deg"])
    inc = math.radians(descriptor["optical_inclination_deg"])
    major = east * math.sin(pa) + north * math.cos(pa)
    minor = (east * math.cos(pa) - north * math.sin(pa)) / math.cos(inc)
    radius = np.hypot(major, minor)
    theta = np.mod(np.arctan2(minor, major), 2.0 * math.pi)
    r95 = descriptor["source_r95_arcsec"]
    use = (radius >= 0.20 * r95) & (radius <= r95)
    east, north, theta, radius, intensity, xx, yy = (
        array[use] for array in (east, north, theta, radius, intensity, xx, yy)
    )
    beam = row["beam_geometric_mean_arcsec"]
    cell_x = np.floor(east / beam).astype(int)
    cell_y = np.floor(north / beam).astype(int)
    selected = {}
    for index, key in enumerate(zip(cell_x, cell_y)):
        if key not in selected or intensity[index] > intensity[selected[key]]:
            selected[key] = index
    keep = np.asarray(sorted(selected.values()), dtype=int)
    rho = (radius[keep] / r95 - 0.20) / 0.80
    blocks = np.floor(theta[keep] * 8 / (2.0 * math.pi)).astype(int)
    return theta[keep], rho, blocks, xx[keep], yy[keep]


def cv_predictors(x: np.ndarray, g: np.ndarray, blocks: np.ndarray) -> list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    predictors = []
    full = np.column_stack((x, g))
    for block in range(8):
        train = blocks != block
        test = ~train
        predictors.append((
            np.flatnonzero(train),
            np.flatnonzero(test),
            np.linalg.pinv(x[train]),
            x[test],
            np.linalg.pinv(full[train]),
            full[test],
        ))
    return predictors


def cv_improvement(y: np.ndarray, predictors: list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]]) -> float:
    null_sse = 0.0
    full_sse = 0.0
    for train, test, null_inverse, null_test, full_inverse, full_test in predictors:
        null_sse += float(np.sum((y[test] - null_test @ (null_inverse @ y[train])) ** 2))
        full_sse += float(np.sum((y[test] - full_test @ (full_inverse @ y[train])) ** 2))
    return (null_sse - full_sse) / null_sse


def subspace_overlap(x: np.ndarray, left: np.ndarray, right: np.ndarray) -> float:
    ql, _ = np.linalg.qr(projected_target(x, left))
    qr, _ = np.linalg.qr(projected_target(x, right))
    return float(np.linalg.svd(ql[:, :2].T @ qr[:, :2], compute_uv=False)[0])


def main() -> None:
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    if preflight["status"] != "SOURCE_SUPPORT_PASSED_OPERATOR_CALIBRATION_PENDING":
        raise RuntimeError("Source support has not passed")
    if preflight["preregistration_sha256"] != sha256(FREEZE):
        raise RuntimeError("Source preflight does not match current freeze")
    support_rows = {
        row["galaxy"]: row
        for row in __import__("csv").DictReader((ROOT / preflight["support_ledger"]).open(encoding="utf-8"))
    }
    for row in support_rows.values():
        for key in ("beam_geometric_mean_arcsec", "source_r95_arcsec"):
            row[key] = float(row[key])

    results = []
    all_pass = True
    for galaxy in preflight["passing_galaxies"]:
        row = support_rows[galaxy]
        descriptor = preflight["source_descriptors"][galaxy]
        zones = descriptor["radial_capacity_j"]
        theta, rho, blocks, _, _ = sample_source(row, descriptor)
        matched_coeff = descriptor_array(preflight, galaxy, zones)
        x, matched = design(theta, rho, matched_coeff, zones)
        reversed_g = design(theta, rho, matched_coeff[::-1], zones)[1]
        phases = np.exp(1j * (np.arange(zones) % 4) * (math.pi / 2.0))
        scrambled_g = design(theta, rho, matched_coeff * phases, zones)[1]
        other = preflight["cross_galaxy_derangement"][galaxy]
        cross_coeff = descriptor_array(preflight, other, zones)
        cross_g = design(theta, rho, cross_coeff, zones)[1]
        wrong = {"radial_reversal": reversed_g, "annular_phase_scramble": scrambled_g, "cross_galaxy": cross_g}
        matched_predictors = cv_predictors(x, matched, blocks)
        wrong_predictors = {
            name: cv_predictors(x, candidate, blocks) for name, candidate in wrong.items()
        }

        nuisance_rank = rank(x)
        full = np.column_stack((x, matched))
        target = projected_target(x, matched)
        singular = np.linalg.svd(target, compute_uv=False)
        condition = float(singular[0] / singular[-1])
        leverage = np.sum(np.linalg.qr(full, mode="reduced")[0] ** 2, axis=1)
        fold_checks = []
        for block in range(8):
            train = blocks != block
            test = ~train
            fold_checks.append({
                "block": block,
                "training_nuisance_rank": rank(x[train]),
                "training_added_target_rank": rank(np.column_stack((x[train], matched[train]))) - rank(x[train]),
                "heldout_added_target_rank": rank(np.column_stack((x[test], matched[test]))) - rank(x[test]),
            })
        overlaps = {name: subspace_overlap(x, matched, candidate) for name, candidate in wrong.items()}
        structural_pass = bool(
            rank(full) == nuisance_rank + 2
            and condition <= 100.0
            and float(leverage.max()) <= 0.25
            and theta.size - rank(full) >= max(10, nuisance_rank + 2)
            and all(check["training_nuisance_rank"] == nuisance_rank for check in fold_checks)
            and all(check["training_added_target_rank"] == 2 for check in fold_checks)
            and all(check["heldout_added_target_rank"] == 2 for check in fold_checks)
            and max(overlaps.values()) < 0.999
        )
        all_pass &= structural_pass

        seed = int(hashlib.sha256(galaxy.encode()).hexdigest()[:8], 16)
        rng = np.random.default_rng(seed)
        calibration = {}
        null_values = []
        trial_values = {amplitude: [] for amplitude in AMPLITUDES}
        for amplitude in AMPLITUDES:
            for _ in range(TRIALS):
                angle = rng.uniform(0.0, 2.0 * math.pi)
                signal = amplitude * matched @ np.array([math.cos(angle), math.sin(angle)])
                y = signal + rng.normal(size=theta.size)
                matched_gain = cv_improvement(y, matched_predictors)
                wrong_gain = max(cv_improvement(y, predictors) for predictors in wrong_predictors.values())
                trial_values[amplitude].append(matched_gain - wrong_gain)
            if amplitude == 0.0:
                null_values = trial_values[amplitude]
        threshold = float(np.quantile(null_values, 0.95))
        for amplitude in AMPLITUDES:
            values = np.asarray(trial_values[amplitude])
            calibration[str(amplitude)] = {
                "median_specificity": float(np.median(values)),
                "fraction_above_null_95": float(np.mean(values > threshold)),
            }
        results.append({
            "galaxy": galaxy,
            "independent_source_samples": int(theta.size),
            "radial_capacity_j": zones,
            "nuisance_rank": nuisance_rank,
            "target_rank": rank(full) - nuisance_rank,
            "target_condition_number": condition,
            "maximum_leverage": float(leverage.max()),
            "residual_df": int(theta.size - rank(full)),
            "fold_checks": fold_checks,
            "wrong_subspace_overlap": overlaps,
            "null_specificity_95": threshold,
            "injection_calibration": calibration,
            "structural_operator_gate": structural_pass,
        })

    operator_passing = [row["galaxy"] for row in results if row["structural_operator_gate"]]
    operator_failing = [row["galaxy"] for row in results if not row["structural_operator_gate"]]
    population_gate = len(operator_passing) >= 19
    output = {
        "schema": "little_things_2d_morphology_operator_calibration_v01",
        "status": "SOURCE_OPERATOR_CALIBRATED_20_GALAXY_VELOCITY_ACQUISITION_ALLOWED" if population_gate else "SOURCE_OPERATOR_POPULATION_INSUFFICIENT",
        "source_preflight": str(PREFLIGHT.relative_to(ROOT)),
        "source_preflight_sha256": sha256(PREFLIGHT),
        "galaxy_count": len(results),
        "all_structural_operator_gates_pass": all_pass,
        "population_operator_gate_pass": population_gate,
        "operator_pass_count": len(operator_passing),
        "operator_fail_count": len(operator_failing),
        "operator_passing_galaxies": operator_passing,
        "operator_failing_galaxies": operator_failing,
        "results": results,
        "operator": "source m=1 radial complex envelope embedded into one global two-quadrature k=2 target after per-zone k=1 nuisance removal",
        "wrong_templates": ["radial_reversal", "nonconstant_annular_phase_scramble", "cross_galaxy_derangement"],
        "global_phase_wrong_template_forbidden": True,
        "calibration": f"{TRIALS} fixed-seed Gaussian trials per amplitude {AMPLITUDES}; per-galaxy null 95% specificity recorded without observed velocity pixels",
        "velocity_pixels_opened": False,
        "velocity_product_acquisition_allowed": population_gate,
        "endpoint_scoring_allowed": False,
        "tau_endpoint_allowed": False,
        "claim_boundary": "velocity-blind structural and injection calibration of a conventional morphology-sensitivity operator; no observed kinematic or Tau result",
    }
    out = DATA / "little_things_2d_morphology_operator_calibration_v01.json"
    out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    report = ROOT / "reports/little_things_2d_morphology_operator_calibration_v01.md"
    failed = operator_failing
    report.write_text(
        "# LITTLE THINGS 2D morphology operator calibration v01\n\n"
        f"Status: `{output['status']}`\n\n"
        f"The velocity-blind structural audit evaluated {len(results)} source-qualified galaxies. "
        f"Structural failures: `{failed}`. The operator retains exactly two global k=2 target "
        "dimensions irrespective of radial capacity; radial zones shape the source envelope rather "
        "than introducing independent fitted gains.\n\n"
        "Each leave-one-azimuth-block fold checks nuisance rank, two-dimensional target novelty, "
        "conditioning, leverage, residual degrees of freedom, and distinguishability from radial "
        "reversal, nonconstant annular phase scrambling, and a cross-galaxy derangement. Fixed-seed "
        "synthetic injections record the null specificity threshold and sensitivity curve without "
        "reading observed velocity pixels.\n\n"
        "Even a later observational pass can be generated by conventional lopsided or tidal gas "
        "dynamics. This calibration neither validates Tau Core nor supports a gravity or dark-matter claim.\n",
        encoding="utf-8",
    )
    print(output["status"], len(results), failed)


if __name__ == "__main__":
    main()
