#!/usr/bin/env python3
"""Run the frozen NGC4062 two-resolution H I--Halpha endpoint."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.stats import chi2


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
SOURCE = ROOT / "data/external/literature/ngc4062_halogas_confirmatory_v01"
FREEZE_JSON = DATA / "ngc4062_halogas_confirmatory_freeze_v01.json"
FREEZE_CSV = DATA / "ngc4062_halogas_confirmatory_freeze_v01.csv"
HALPHA = DATA / "ghasp_full_federation_side_points_v01.csv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def weighted_median(values: np.ndarray, weights: np.ndarray) -> float:
    order = np.argsort(values)
    cumulative = np.cumsum(weights[order])
    return float(values[order][np.searchsorted(cumulative, 0.5 * cumulative[-1])])


def interpolate(rows: dict[float, dict[str, str]], lo: float, hi: float, wlo: float, whi: float) -> tuple[float, float]:
    low, high = rows[lo], rows[hi]
    value = wlo * float(low["velocity_km_s"]) + whi * float(high["velocity_km_s"])
    error = math.hypot(wlo * float(low["velocity_error_km_s"]), whi * float(high["velocity_error_km_s"]))
    return value, error


def geometry_arrays(header, geometry):
    ny, nx = int(header["NAXIS2"]), int(header["NAXIS1"])
    yy, xx = np.indices((ny, nx), dtype=float)
    ra, dec = WCS(header, naxis=2).pixel_to_world_values(xx, yy)
    east = (ra - geometry["center_ra_deg"]) * math.cos(math.radians(geometry["center_dec_deg"])) * 3600
    north = (dec - geometry["center_dec_deg"]) * 3600
    pa = math.radians(geometry["receding_pa_deg"])
    major = east * math.sin(pa) + north * math.cos(pa)
    minor = -east * math.cos(pa) + north * math.sin(pa)
    radius = np.sqrt(major**2 + (minor / math.cos(math.radians(geometry["inclination_deg"]))) ** 2)
    cosine = np.divide(major, radius, out=np.zeros_like(major), where=radius > 0)
    return xx, yy, radius, cosine


def block_bootstrap(values, weights, blocks, draws, rng):
    unique = np.unique(blocks)
    block_values, block_weights = [], []
    for block in unique:
        select = blocks == block
        block_values.append(weighted_median(values[select], weights[select]))
        block_weights.append(float(np.sum(weights[select])))
    block_values, block_weights = np.asarray(block_values), np.asarray(block_weights)
    samples = np.empty(draws)
    for index in range(draws):
        chosen = rng.integers(0, len(unique), size=len(unique))
        samples[index] = weighted_median(block_values[chosen], block_weights[chosen])
    return samples


def extract(moment0_path, moment1_path, geometry, freeze, rings, bootstrap, seed):
    moment0, header = fits.getdata(moment0_path, header=True, memmap=True)
    moment1 = fits.getdata(moment1_path, memmap=True)
    xx, yy, radius, cosine = geometry_arrays(header, geometry)
    base = np.isfinite(moment0) & np.isfinite(moment1) & (moment0 > 0) & (np.abs(cosine) >= freeze["major_axis_min_abs_cos_theta"])
    beam_pixels = max(1, int(math.ceil(float(header["BMAJ"]) / abs(float(header["CDELT1"])))))
    block_ids = (yy.astype(int) // beam_pixels) * 10000 + (xx.astype(int) // beam_pixels)
    rng = np.random.default_rng(seed)
    detail, odds, boot_odds = [], [], []
    for ring in rings:
        annulus = base & (radius >= float(ring["annulus_inner_arcsec"])) & (radius < float(ring["annulus_outer_arcsec"]))
        values_by_side, samples_by_side = {}, {}
        for side, side_mask in (("receding", cosine > 0), ("approaching", cosine < 0)):
            select = annulus & side_mask
            values = (moment1[select] - geometry["systemic_velocity_km_s"]) / cosine[select]
            weights = moment0[select] * np.abs(cosine[select])
            blocks = block_ids[select]
            finite = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
            values, weights, blocks = values[finite], weights[finite], blocks[finite]
            if len(np.unique(blocks)) < 2:
                raise RuntimeError(f"Insufficient beam blocks: {side}, R={ring['radius_arcsec']}")
            values_by_side[side] = weighted_median(values, weights)
            if bootstrap:
                samples_by_side[side] = block_bootstrap(values, weights, blocks, freeze["bootstrap_draws"], rng)
            detail.append({
                "radius_arcsec": float(ring["radius_arcsec"]), "side": side,
                "n_pixels": int(len(values)), "n_beam_blocks": int(len(np.unique(blocks))),
                "u_los_km_s": values_by_side[side],
            })
        odds.append(values_by_side["receding"] - values_by_side["approaching"])
        if bootstrap:
            boot_odds.append(samples_by_side["receding"] - samples_by_side["approaching"])
    return detail, np.asarray(odds), np.asarray(boot_odds).T if bootstrap else None


def gls(values: np.ndarray, covariance: np.ndarray) -> dict:
    inverse = np.linalg.pinv(covariance)
    ones = np.ones(len(values))
    variance = 1.0 / float(ones @ inverse @ ones)
    mean = variance * float(ones @ inverse @ values)
    statistic = float(values @ inverse @ values)
    return {
        "gls_mean_km_s": mean,
        "gls_mean_sigma_km_s": math.sqrt(variance),
        "gls_mean_z": mean / math.sqrt(variance),
        "chi2_zero": statistic,
        "chi2_zero_dof": len(values),
        "chi2_zero_p": float(chi2.sf(statistic, len(values))),
    }


def main() -> None:
    freeze = json.loads(FREEZE_JSON.read_text())
    if freeze["pixel_values_opened_during_freeze"] is not False or freeze["endpoint_access"] is not False:
        raise RuntimeError("Source-blind freeze gate failed")
    for name, expected in freeze["source_sha256"].items():
        if sha256(SOURCE / name) != expected:
            raise RuntimeError(f"Frozen source changed: {name}")
    if sha256(HALPHA) != freeze["halpha_points_sha256"]:
        raise RuntimeError("Frozen GHASP federation changed")

    rings = list(csv.DictReader(FREEZE_CSV.open(newline="", encoding="utf-8")))
    halpha_rows = [
        row for row in csv.DictReader(HALPHA.open(newline="", encoding="utf-8"))
        if "NGC4062" in row["aliases"].split(";")
    ]
    by_side = {
        side: {float(row["radius_arcsec"]): row for row in halpha_rows if row["side"] == side}
        for side in ("a", "r")
    }
    inclination = math.radians(freeze["source_geometry"]["ghasp"]["kinematic_inclination_deg"])
    ha_odd, ha_variance, ha_derivative = [], [], []
    for ring in rings:
        a, ea = interpolate(by_side["a"], float(ring["halpha_approaching_lower_radius_arcsec"]), float(ring["halpha_approaching_upper_radius_arcsec"]), float(ring["halpha_approaching_lower_weight"]), float(ring["halpha_approaching_upper_weight"]))
        r, er = interpolate(by_side["r"], float(ring["halpha_receding_lower_radius_arcsec"]), float(ring["halpha_receding_upper_radius_arcsec"]), float(ring["halpha_receding_lower_weight"]), float(ring["halpha_receding_upper_weight"]))
        ha_odd.append((r - a) * math.sin(inclination))
        ha_variance.append((math.sin(inclination) * math.hypot(ea, er)) ** 2)
        ha_derivative.append((r - a) * math.cos(inclination))
    ha_odd = np.asarray(ha_odd)
    ha_covariance = np.diag(ha_variance) + np.outer(ha_derivative, ha_derivative) * math.radians(freeze["source_geometry"]["ghasp"]["kinematic_inclination_error_deg"]) ** 2

    primary = freeze["source_geometry"]["primary"]
    variant_geometries = [
        {**primary, "variant": "ghasp_center", "center_ra_deg": freeze["source_geometry"]["ghasp"]["center_ra_deg"], "center_dec_deg": freeze["source_geometry"]["ghasp"]["center_dec_deg"]},
        *[{**primary, "variant": f"inclination_{value}", "inclination_deg": value} for value in freeze["source_geometry"]["variants"]["inclination_deg"]],
        *[{**primary, "variant": f"pa_{value}", "receding_pa_deg": value} for value in freeze["source_geometry"]["variants"]["receding_pa_deg"]],
        {**primary, "variant": "ghasp_systemic_758", "systemic_velocity_km_s": 758.0},
    ]

    outputs, detail_rows = {}, []
    for map_index, resolution in enumerate(("HR", "LR")):
        moment0 = SOURCE / f"NGC4062-{resolution}_mom0m.fits"
        moment1 = SOURCE / f"NGC4062-{resolution}_mom1m.fits"
        details, hi_odd, bootstrap = extract(moment0, moment1, primary, freeze, rings, True, freeze["bootstrap_seed"] + map_index * 100000)
        bootstrap_covariance = np.cov(bootstrap, rowvar=False)
        variant_odds, variant_rows = [], []
        for geometry in variant_geometries:
            _, odd, _ = extract(moment0, moment1, geometry, freeze, rings, False, 0)
            variant_odds.append(odd)
        deviations = np.asarray(variant_odds) - hi_odd
        geometry_covariance = deviations.T @ deviations / len(deviations)
        covariance = ha_covariance + bootstrap_covariance + geometry_covariance
        delta = ha_odd - hi_odd
        primary_score = gls(delta, covariance)
        for geometry, odd in zip(variant_geometries, variant_odds):
            variant_delta = ha_odd - odd
            variant_score = gls(variant_delta, ha_covariance + bootstrap_covariance)
            variant_rows.append({
                "variant": geometry["variant"],
                "delta_odd_by_radius_km_s": variant_delta.tolist(),
                **variant_score,
            })
        outputs[resolution] = {
            "halpha_odd_by_radius_km_s": ha_odd.tolist(),
            "hi_odd_by_radius_km_s": hi_odd.tolist(),
            "delta_odd_by_radius_km_s": delta.tolist(),
            "covariance_km2_s2": covariance.tolist(),
            "primary_score": primary_score,
            "nuisance_variants": variant_rows,
        }
        for row in details:
            row["resolution"] = resolution
            detail_rows.append(row)

    hr, lr = outputs["HR"]["primary_score"], outputs["LR"]["primary_score"]
    primary_sign = int(np.sign(hr["gls_mean_km_s"]))
    all_variant_signs = [
        int(np.sign(row["gls_mean_km_s"]))
        for resolution in ("HR", "LR") for row in outputs[resolution]["nuisance_variants"]
    ]
    radius_signs = [
        int(np.sign(value)) for resolution in ("HR", "LR")
        for value in outputs[resolution]["delta_odd_by_radius_km_s"]
    ]
    gates = {
        "hr_rejects_zero": bool(hr["chi2_zero_p"] < 0.05),
        "lr_rejects_zero": bool(lr["chi2_zero_p"] < 0.05),
        "hr_lr_gls_sign_agreement": bool(np.sign(hr["gls_mean_km_s"]) == np.sign(lr["gls_mean_km_s"])),
        "hr_lr_gls_compatible_2sigma": bool(abs(hr["gls_mean_km_s"] - lr["gls_mean_km_s"]) <= 2 * math.hypot(hr["gls_mean_sigma_km_s"], lr["gls_mean_sigma_km_s"])),
        "all_four_radius_resolution_cells_same_sign": bool(all(sign == primary_sign for sign in radius_signs)),
        "all_twelve_nuisance_scores_preserve_sign": bool(all(sign == primary_sign for sign in all_variant_signs)),
    }
    passed = all(gates.values())
    result = {
        "schema": "ngc4062_halogas_confirmatory_endpoint_v01",
        "status": "NGC4062_CONFIRMATORY_ENDPOINT_PASS" if passed else "NGC4062_CONFIRMATORY_ENDPOINT_FAIL",
        "galaxy": "NGC4062",
        "endpoint_opened_after_freeze": True,
        "n_common_rings": len(rings),
        "outputs": outputs,
        "gates": gates,
        "confirmatory_pass": passed,
        "interpretation": "A pass is a replicated cross-tracer side-odd discrepancy under the frozen constant-geometry protocol; a fail is preserved as a negative endpoint result.",
        "claim_boundary": freeze["claim_boundary"],
    }
    json_path = DATA / "ngc4062_halogas_confirmatory_endpoint_v01.json"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    csv_path = DATA / "ngc4062_halogas_confirmatory_endpoint_v01_side_rows.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(detail_rows[0]))
        writer.writeheader()
        writer.writerows(detail_rows)
    (REPORTS / "ngc4062_halogas_confirmatory_endpoint_v01.md").write_text(
        f"""# NGC4062 HALOGAS confirmatory endpoint v0.1

**Status:** `{result['status']}`

The frozen two-ring H I--Halpha side-odd contrast was opened only after the
source geometry, masks, estimators, uncertainties, nuisance variants, and
pass gates were written. HR gives a GLS mean of
`{hr['gls_mean_km_s']:.2f} +/- {hr['gls_mean_sigma_km_s']:.2f} km/s`
(`p={hr['chi2_zero_p']:.3g}`); LR gives
`{lr['gls_mean_km_s']:.2f} +/- {lr['gls_mean_sigma_km_s']:.2f} km/s`
(`p={lr['chi2_zero_p']:.3g}`).

Gates: `{json.dumps(gates, sort_keys=True)}`.

This endpoint contains only two independent radial rings. Even a pass is a
replicated cross-tracer morphology/readout diagnostic, not a derivation of a
Tau correction, physical `q_R`, parent morphology, Nature occupation, or a
dark-matter replacement result. Conventional tracer, extraplanar-gas,
beam-smearing, center, geometry, and velocity-zero-point explanations remain.
""",
        encoding="utf-8",
    )
    print(result["status"])
    print(json.dumps({"HR": hr, "LR": lr, "gates": gates}, indent=2))


if __name__ == "__main__":
    main()
