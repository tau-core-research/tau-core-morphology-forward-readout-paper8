#!/usr/bin/env python3
"""Open the frozen VIVA cubes and score the preregistered 2D control terminal."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import re
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales
from scipy.ndimage import binary_dilation


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
EXTERNAL = ROOT / "data/external/literature/viva_2d_morphology_sensitivity_v01"
PREREG = DATA / "viva_2d_morphology_sensitivity_preregistration_v01.json"
ACQUISITION = DATA / "viva_2d_morphology_sensitivity_acquisition_v01.json"
OPERATOR = DATA / "viva_2d_morphology_sensitivity_operator_freeze_v01.json"
RADIAL_EDGES = np.asarray([0.20, 0.40, 0.60, 0.80, 1.00])
PHASE_OFFSETS = np.asarray([0.0, 0.5 * np.pi, np.pi, 1.5 * np.pi])
N_SECTORS = 12


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def robust_sigma(values: np.ndarray) -> float:
    median = float(np.median(values))
    sigma = 1.4826 * float(np.median(np.abs(values - median)))
    return sigma if sigma > 0 and np.isfinite(sigma) else float(np.std(values))


def beam_from_history(header: fits.Header) -> tuple[float, float]:
    history = header.get("HISTORY", [])
    if isinstance(history, str):
        history = [history]
    pattern = re.compile(r"CLEAN BMAJ=\s*([0-9.E+-]+) BMIN=\s*([0-9.E+-]+)")
    for line in history:
        match = pattern.search(str(line))
        if match:
            return float(match.group(1)) * 3600.0, float(match.group(2)) * 3600.0
    raise RuntimeError("Synthesized beam not found in AIPS HISTORY")


def disk_coordinates(
    header: fits.Header, shape: tuple[int, int], item: dict
) -> tuple[np.ndarray, np.ndarray, float]:
    wcs = WCS(header).celestial
    yy, xx = np.indices(shape, dtype=float)
    ra, dec = wcs.pixel_to_world_values(xx, yy)
    east = (ra - item["ra_deg"]) * math.cos(math.radians(item["dec_deg"])) * 3600.0
    north = (dec - item["dec_deg"]) * 3600.0
    pa = math.radians(item["pa_deg"])
    major = east * math.sin(pa) + north * math.cos(pa)
    minor = -east * math.cos(pa) + north * math.sin(pa)
    disk_y = minor / math.cos(math.radians(item["inclination_deg"]))
    radius = np.hypot(major, disk_y)
    theta = np.arctan2(disk_y, major)
    r25 = 30.0 * float(item["d25_arcmin"])
    return radius / r25, theta, r25


def reduce_cube(path: Path, item: dict) -> dict:
    with fits.open(path, memmap=False) as hdul:
        cube = np.squeeze(np.asarray(hdul[0].data, dtype=float))
        header = hdul[0].header.copy()
    if cube.ndim != 3:
        raise RuntimeError(f"{item['galaxy']}: expected a 3D cube")
    nchan = cube.shape[0]
    channel_index = np.arange(nchan, dtype=float) + 1.0
    velocity = (
        float(header["CRVAL3"])
        + (channel_index - float(header["CRPIX3"])) * float(header["CDELT3"])
    ) / 1000.0
    medians = np.median(cube, axis=(1, 2))
    sigmas = np.asarray([robust_sigma(cube[k]) for k in range(nchan)])
    centered = cube - medians[:, None, None]
    above = centered > 3.0 * sigmas[:, None, None]
    adjacent = above & (np.roll(above, 1, axis=0) | np.roll(above, -1, axis=0))
    adjacent[0] &= above[1]
    adjacent[-1] &= above[-2]
    grown = binary_dilation(adjacent, iterations=1)
    positive = np.where(grown & (centered > 0), centered, 0.0)
    npositive = np.count_nonzero(positive, axis=0)
    moment0 = positive.sum(axis=0)
    moment1 = np.divide(
        np.sum(positive * velocity[:, None, None], axis=0), moment0,
        out=np.full_like(moment0, np.nan), where=moment0 > 0,
    )
    noise = float(np.median(sigmas))
    snr = np.divide(
        moment0, noise * np.sqrt(np.maximum(npositive, 1)),
        out=np.zeros_like(moment0), where=npositive > 0,
    )
    radius, theta, r25 = disk_coordinates(header, moment0.shape, item)
    base = np.isfinite(moment1) & (snr >= 5.0) & (radius >= RADIAL_EDGES[0]) & (radius <= RADIAL_EDGES[-1])
    bmaj, bmin = beam_from_history(header)
    pixel_arcsec = float(np.mean(np.abs(proj_plane_pixel_scales(WCS(header).celestial)))) * 3600.0
    step = max(1, int(math.ceil(math.sqrt(bmaj * bmin) / pixel_arcsec)))
    yy, xx = np.indices(moment0.shape)
    independent = base & ((xx % step) == 0) & ((yy % step) == 0)
    return {
        "moment0": moment0, "moment1": moment1, "snr": snr, "radius": radius,
        "theta": theta, "mask": independent, "r25_arcsec": r25,
        "beam_arcsec": [bmaj, bmin], "pixel_arcsec": pixel_arcsec,
        "beam_sampling_step_pixels": step, "noise_jy_beam": noise,
    }


def source_profile(field: dict) -> tuple[np.ndarray, np.ndarray, list[dict]]:
    p, q, rows = [], [], []
    for zone, (low, high) in enumerate(zip(RADIAL_EDGES[:-1], RADIAL_EDGES[1:])):
        choose = field["mask"] & (field["radius"] >= low) & (
            (field["radius"] <= high) if zone == len(RADIAL_EDGES) - 2 else (field["radius"] < high)
        )
        theta = field["theta"][choose]
        intensity = field["moment0"][choose]
        design = np.column_stack([np.ones(choose.sum()), np.cos(theta), np.sin(theta)])
        coefficient = np.linalg.pinv(design) @ intensity
        scale = coefficient[0]
        pj = float(coefficient[1] / scale) if scale != 0 else 0.0
        qj = float(coefficient[2] / scale) if scale != 0 else 0.0
        p.append(pj)
        q.append(qj)
        sectors = np.unique(np.floor(((theta + np.pi) % (2 * np.pi)) / (2 * np.pi) * N_SECTORS).astype(int))
        rows.append({
            "zone": zone, "r_min_r25": low, "r_max_r25": high,
            "samples": int(choose.sum()), "occupied_sectors": int(len(sectors)),
            "source_m1_cos": pj, "source_m1_sin": qj,
            "source_m1_amplitude": float(math.hypot(pj, qj)),
        })
    return np.asarray(p), np.asarray(q), rows


def build_design(field: dict, profile: tuple[np.ndarray, np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    choose = field["mask"]
    radius = field["radius"][choose]
    theta = field["theta"][choose]
    values = field["moment1"][choose]
    zone_index = np.clip(np.digitize(radius, RADIAL_EDGES) - 1, 0, len(RADIAL_EDGES) - 2)
    nuisance = np.zeros((choose.sum(), 3 * (len(RADIAL_EDGES) - 1)))
    p, q = profile
    target = np.zeros((choose.sum(), 2))
    for zone in range(len(RADIAL_EDGES) - 1):
        z = zone_index == zone
        nuisance[z, 3 * zone] = 1.0
        nuisance[z, 3 * zone + 1] = np.cos(theta[z])
        nuisance[z, 3 * zone + 2] = np.sin(theta[z])
        target[z, 0] = p[zone] * np.cos(2 * theta[z]) + q[zone] * np.sin(2 * theta[z])
        target[z, 1] = -q[zone] * np.cos(2 * theta[z]) + p[zone] * np.sin(2 * theta[z])
    sectors = np.floor(((theta + np.pi) % (2 * np.pi)) / (2 * np.pi) * N_SECTORS).astype(int)
    return values, nuisance, target, sectors


def projected_rank(nuisance: np.ndarray, target: np.ndarray) -> int:
    projected = target - nuisance @ (np.linalg.pinv(nuisance) @ target)
    return int(np.linalg.matrix_rank(projected))


def cross_validated_improvement(values: np.ndarray, nuisance: np.ndarray, target: np.ndarray, sectors: np.ndarray) -> float:
    sse_nuisance = 0.0
    sse_full = 0.0
    for held in range(N_SECTORS):
        test = sectors == held
        train = ~test
        if test.sum() == 0 or train.sum() <= nuisance.shape[1] + target.shape[1]:
            raise RuntimeError("Cross-validation sector support failed")
        beta_n = np.linalg.pinv(nuisance[train]) @ values[train]
        full = np.column_stack([nuisance, target])
        beta_f = np.linalg.pinv(full[train]) @ values[train]
        sse_nuisance += float(np.sum((values[test] - nuisance[test] @ beta_n) ** 2))
        sse_full += float(np.sum((values[test] - full[test] @ beta_f) ** 2))
    return (sse_nuisance - sse_full) / sse_nuisance if sse_nuisance > 0 else float("nan")


def phase_permuted(profile: tuple[np.ndarray, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    p, q = profile
    return p * np.cos(PHASE_OFFSETS) - q * np.sin(PHASE_OFFSETS), p * np.sin(PHASE_OFFSETS) + q * np.cos(PHASE_OFFSETS)


def score_with_profile(field: dict, profile: tuple[np.ndarray, np.ndarray]) -> tuple[float, int]:
    values, nuisance, target, sectors = build_design(field, profile)
    rank = projected_rank(nuisance, target)
    if rank != 2:
        return float("nan"), rank
    return cross_validated_improvement(values, nuisance, target, sectors), rank


def main() -> None:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    acquisition = json.loads(ACQUISITION.read_text(encoding="utf-8"))
    operator = json.loads(OPERATOR.read_text(encoding="utf-8"))
    if acquisition["preregistration_sha256"] != sha256(PREREG):
        raise RuntimeError("Preregistration changed after acquisition")
    if operator["scoring_script_sha256"] != sha256(Path(__file__)):
        raise RuntimeError("Scoring implementation changed after operator freeze")
    ledger_rows = list(csv.DictReader((ROOT / acquisition["ledger"]).open(encoding="utf-8")))
    ledger = {row["galaxy"]: row for row in ledger_rows}
    fields, profiles, zone_rows, gates = {}, {}, [], []
    for item in prereg["cohort"]:
        row = ledger[item["galaxy"]]
        cube_path = ROOT / row["local_path"]
        if sha256(cube_path) != row["sha256"]:
            raise RuntimeError(f"{item['galaxy']}: cube hash mismatch")
        field = reduce_cube(cube_path, item)
        profile_p, profile_q, rows = source_profile(field)
        fields[item["galaxy"]] = field
        profiles[item["galaxy"]] = (profile_p, profile_q)
        for row_out in rows:
            zone_rows.append({"galaxy": item["galaxy"], "role": item["role"], **row_out})
        gate = all(r["samples"] >= 24 and r["occupied_sectors"] >= 8 for r in rows)
        gates.append({
            "galaxy": item["galaxy"], "role": item["role"], "support_gate": gate,
            "beam_sampling_step_pixels": field["beam_sampling_step_pixels"],
            "beam_major_arcsec": field["beam_arcsec"][0], "beam_minor_arcsec": field["beam_arcsec"][1],
            "independent_samples": int(field["mask"].sum()),
        })

    score_rows = []
    all_support = all(row["support_gate"] for row in gates)
    if all_support:
        by_role = {
            role: sorted(item["galaxy"] for item in prereg["cohort"] if item["role"] == role)
            for role in ("disturbed", "quiet")
        }
        for item in prereg["cohort"]:
            galaxy, role = item["galaxy"], item["role"]
            peers = by_role[role]
            donor = peers[(peers.index(galaxy) + 1) % len(peers)]
            matched, rank = score_with_profile(fields[galaxy], profiles[galaxy])
            reversed_score, reverse_rank = score_with_profile(
                fields[galaxy], (profiles[galaxy][0][::-1], profiles[galaxy][1][::-1])
            )
            phase_score, phase_rank = score_with_profile(fields[galaxy], phase_permuted(profiles[galaxy]))
            cross_score, cross_rank = score_with_profile(fields[galaxy], profiles[donor])
            wrong_mean = float(np.mean([reversed_score, phase_score, cross_score]))
            score_rows.append({
                "galaxy": galaxy, "role": role, "matched_cv_fraction": matched,
                "radial_reversal_cv_fraction": reversed_score,
                "phase_permutation_cv_fraction": phase_score,
                "cross_galaxy_cv_fraction": cross_score, "cross_galaxy_donor": donor,
                "matched_minus_wrong_specificity": matched - wrong_mean,
                "matched_rank": rank, "radial_reversal_rank": reverse_rank,
                "phase_permutation_rank": phase_rank, "cross_galaxy_rank": cross_rank,
            })

    if score_rows:
        z = np.asarray([row["matched_minus_wrong_specificity"] for row in score_rows])
        observed_labels = np.asarray([row["role"] == "disturbed" for row in score_rows])
        observed = float(np.mean(z[observed_labels]) - np.mean(z[~observed_labels]))
        permutation_values = []
        for selected in itertools.combinations(range(len(z)), 3):
            labels = np.zeros(len(z), dtype=bool)
            labels[list(selected)] = True
            permutation_values.append(float(np.mean(z[labels]) - np.mean(z[~labels])))
        p_exact = float(np.mean(np.asarray(permutation_values) >= observed - 1e-15))
        disturbed_median = float(np.median(z[observed_labels]))
        success = observed > 0 and p_exact <= 0.05 and disturbed_median > 0
        status = "CONVENTIONAL_SENSITIVITY_CONTROL_PASSED" if success else "NEGATIVE_RESULT_PRESERVED_CONVENTIONAL_SENSITIVITY_NOT_SHOWN"
    else:
        observed = p_exact = disturbed_median = None
        success = False
        status = "PREFLIGHT_BLOCKED_BY_FROZEN_SUPPORT_GATE"

    zone_path = DATA / "viva_2d_morphology_sensitivity_endpoint_v01_zones.csv"
    gate_path = DATA / "viva_2d_morphology_sensitivity_endpoint_v01_gates.csv"
    score_path = DATA / "viva_2d_morphology_sensitivity_endpoint_v01_scores.csv"
    for path, rows in [(zone_path, zone_rows), (gate_path, gates), (score_path, score_rows)]:
        if rows:
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader(); writer.writerows(rows)
    result = {
        "schema": "viva_2d_morphology_sensitivity_endpoint_v01",
        "status": status, "all_frozen_support_gates_pass": all_support,
        "conventional_sensitivity_demonstrated": success,
        "primary_disturbed_minus_quiet_specificity": observed,
        "exact_one_sided_permutation_p": p_exact,
        "disturbed_median_specificity": disturbed_median,
        "score_rows": score_rows, "support_gates": gates,
        "source_geometry_uncertainty_tangents_supported": False,
        "geometry_caveat": "the VIVA atlas supplies one adopted center/PA/inclination per object but no covariance sufficient for frozen tangent marginalization",
        "same_cube_source_velocity_caveat": "H I moment-0 and moment-1 are reduced from the same cube; shared masking/noise may contribute to apparent coupling",
        "construction_uses_rotation_or_gravity_residual": False,
        "tau_endpoint_scored": False,
        "claim_boundary": "frozen conventional morphology-correlated 2D kinematic sensitivity control only; passing would not identify causality or Tau, and failure demotes only this terminal",
        "outputs": {"zones": str(zone_path.relative_to(ROOT)), "gates": str(gate_path.relative_to(ROOT)), "scores": str(score_path.relative_to(ROOT))},
    }
    json_path = DATA / "viva_2d_morphology_sensitivity_endpoint_v01.json"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    report = ROOT / "reports/viva_2d_morphology_sensitivity_endpoint_v01.md"
    if score_rows:
        summary = (
            f"The disturbed-minus-quiet matched-template specificity is `{observed:.6g}`; "
            f"the exact one-sided 3-of-6 permutation p-value is `{p_exact:.6g}`, and the disturbed "
            f"median specificity is `{disturbed_median:.6g}`."
        )
    else:
        failed = ", ".join(row["galaxy"] for row in gates if not row["support_gate"])
        summary = f"The frozen footprint gate failed for `{failed}`; no velocity-field score was computed."
    report.write_text(
        "# VIVA 2D morphology-sensitivity endpoint v01\n\n"
        f"Status: `{status}`\n\n{summary}\n\n"
        "This is a conventional instrument-sensitivity control. It neither scores a Tau prediction nor "
        "measures a parent-loss kernel or a galaxy-rotation correction. The fixed-geometry and shared-cube "
        "moment-0/moment-1 caveats remain explicit. No post-open repair is authorized.\n",
        encoding="utf-8",
    )
    print(status, json.dumps({"contrast": observed, "p": p_exact, "support": all_support}))


if __name__ == "__main__":
    main()
