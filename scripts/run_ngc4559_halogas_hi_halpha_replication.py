#!/usr/bin/env python3
"""Run the frozen NGC4559 HALOGAS H I-Halpha odd-contrast replication."""

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
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
SOURCE_JSON = DATA / "ngc4559_halogas_moment_sources_v01.json"
FREEZE_JSON = DATA / "ngc4559_halogas_extraction_freeze_v01.json"
FREEZE_CSV = DATA / "ngc4559_halogas_extraction_freeze_v01.csv"
HALPHA_POINTS = DATA / "ghasp_full_federation_side_points_v01.csv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def weighted_median(values: np.ndarray, weights: np.ndarray) -> float:
    order = np.argsort(values)
    sorted_values = values[order]
    cumulative = np.cumsum(weights[order])
    return float(sorted_values[np.searchsorted(cumulative, 0.5 * cumulative[-1])])


def interpolate(
    by_radius: dict[float, dict[str, str]],
    lower: float,
    upper: float,
    lower_weight: float,
    upper_weight: float,
) -> tuple[float, float]:
    low = by_radius[lower]
    high = by_radius[upper]
    velocity = lower_weight * float(low["velocity_km_s"]) + upper_weight * float(
        high["velocity_km_s"]
    )
    error = math.sqrt(
        (lower_weight * float(low["velocity_error_km_s"])) ** 2
        + (upper_weight * float(high["velocity_error_km_s"])) ** 2
    )
    return velocity, error


def block_bootstrap(
    values: np.ndarray,
    weights: np.ndarray,
    block_ids: np.ndarray,
    draws: int,
    rng: np.random.Generator,
) -> np.ndarray:
    unique = np.unique(block_ids)
    block_values = []
    block_weights = []
    for block in unique:
        select = block_ids == block
        block_values.append(weighted_median(values[select], weights[select]))
        block_weights.append(float(np.sum(weights[select])))
    block_values = np.asarray(block_values)
    block_weights = np.asarray(block_weights)
    samples = np.empty(draws)
    for index in range(draws):
        chosen = rng.integers(0, len(unique), size=len(unique))
        samples[index] = weighted_median(block_values[chosen], block_weights[chosen])
    return samples


def geometry_arrays(header, center, inclination_deg, pa_deg):
    ny, nx = int(header["NAXIS2"]), int(header["NAXIS1"])
    yy, xx = np.indices((ny, nx), dtype=float)
    ra, dec = WCS(header, naxis=2).pixel_to_world_values(xx, yy)
    east = (ra - center["ra_deg"]) * math.cos(math.radians(center["dec_deg"])) * 3600
    north = (dec - center["dec_deg"]) * 3600
    pa = math.radians(pa_deg)
    major = east * math.sin(pa) + north * math.cos(pa)
    minor = -east * math.cos(pa) + north * math.sin(pa)
    radius = np.sqrt(major**2 + (minor / math.cos(math.radians(inclination_deg))) ** 2)
    cos_theta = np.divide(major, radius, out=np.zeros_like(major), where=radius > 0)
    return xx, yy, radius, cos_theta


def extract_map(
    moment0_path: Path,
    moment1_path: Path,
    freeze: dict,
    freeze_rows: list[dict[str, str]],
    geometry: dict,
    bootstrap: bool,
    seed_offset: int = 0,
):
    moment0, header = fits.getdata(moment0_path, header=True, memmap=True)
    moment1 = fits.getdata(moment1_path, memmap=True)
    xx, yy, radius, cos_theta = geometry_arrays(
        header,
        geometry["center"],
        geometry["inclination_deg"],
        geometry["pa_deg"],
    )
    base = (
        np.isfinite(moment0)
        & np.isfinite(moment1)
        & (moment0 > 0)
        & (np.abs(cos_theta) >= float(freeze["major_axis_min_abs_cos_theta"]))
    )
    beam_pixels = max(1, int(math.ceil(float(header["BMAJ"]) / abs(float(header["CDELT1"])))))
    block_ids_all = (yy.astype(int) // beam_pixels) * 10000 + (xx.astype(int) // beam_pixels)
    rng = np.random.default_rng(int(freeze["bootstrap_seed"]) + seed_offset)
    rows = []
    odd_bootstrap = []
    for frozen in freeze_rows:
        inner = float(frozen["annulus_inner_arcsec"])
        outer = float(frozen["annulus_outer_arcsec"])
        annulus = base & (radius >= inner) & (radius < outer)
        side_values = {}
        side_bootstrap = {}
        for side, side_mask in (
            ("receding", cos_theta > 0),
            ("approaching", cos_theta < 0),
        ):
            select = annulus & side_mask
            values = (moment1[select] - geometry["systemic_velocity_km_s"]) / cos_theta[select]
            weights = moment0[select] * np.abs(cos_theta[select])
            finite = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
            values, weights = values[finite], weights[finite]
            blocks = block_ids_all[select][finite]
            if len(values) == 0 or len(np.unique(blocks)) < 2:
                raise RuntimeError(f"Insufficient {side} pixels at {frozen['radius_arcsec']} arcsec")
            side_values[side] = weighted_median(values, weights)
            if bootstrap:
                side_bootstrap[side] = block_bootstrap(
                    values,
                    weights,
                    blocks,
                    int(freeze["bootstrap_draws"]),
                    rng,
                )
            rows.append(
                {
                    "radius_arcsec": float(frozen["radius_arcsec"]),
                    "side": side,
                    "n_pixels": len(values),
                    "n_beam_blocks": len(np.unique(blocks)),
                    "u_los_km_s": side_values[side],
                }
            )
        if bootstrap:
            odd_bootstrap.append(side_bootstrap["receding"] - side_bootstrap["approaching"])
    by_radius = {}
    for row in rows:
        by_radius.setdefault(row["radius_arcsec"], {})[row["side"]] = row
    odd = np.asarray(
        [
            by_radius[float(frozen["radius_arcsec"])]["receding"]["u_los_km_s"]
            - by_radius[float(frozen["radius_arcsec"])]["approaching"]["u_los_km_s"]
            for frozen in freeze_rows
        ]
    )
    bootstrap_matrix = np.asarray(odd_bootstrap).T if bootstrap else None
    return rows, odd, bootstrap_matrix


def gls(values: np.ndarray, covariance: np.ndarray):
    inverse = np.linalg.pinv(covariance)
    ones = np.ones(len(values))
    variance = 1.0 / float(ones @ inverse @ ones)
    mean = variance * float(ones @ inverse @ values)
    chi2_zero = float(values @ inverse @ values)
    return {
        "gls_mean_km_s": mean,
        "gls_mean_sigma_km_s": math.sqrt(variance),
        "gls_mean_z": mean / math.sqrt(variance),
        "chi2_zero": chi2_zero,
        "chi2_zero_dof": len(values),
        "chi2_zero_p": float(chi2.sf(chi2_zero, len(values))),
    }


def main() -> None:
    source = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    freeze = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    if not freeze["pixel_values_opened_during_freeze"] is False:
        raise RuntimeError("Pixel-blind freeze gate failed")
    for item in source["manifest"]:
        path = ROOT / item["local_path"]
        if sha256(path) != item["sha256"]:
            raise RuntimeError(f"HALOGAS product changed: {item['filename']}")
    if sha256(HALPHA_POINTS) != freeze["source_provenance"]["halpha_points_sha256"]:
        raise RuntimeError("Frozen Halpha input changed")
    freeze_rows = list(csv.DictReader(FREEZE_CSV.open(newline="", encoding="utf-8")))
    halpha_rows = [
        row
        for row in csv.DictReader(HALPHA_POINTS.open(newline="", encoding="utf-8"))
        if row["sparc_match"] == "NGC4559"
    ]
    halpha_by_side = {
        side: {
            float(row["radius_arcsec"]): row
            for row in halpha_rows
            if row["side"] == side
        }
        for side in ("a", "r")
    }
    ghasp = freeze["source_geometry"]["ghasp"]
    angle = math.radians(float(ghasp["kinematic_inclination_deg"]))
    ha_odd = []
    ha_measurement_variance = []
    ha_inclination_derivative = []
    ha_values = []
    for frozen in freeze_rows:
        a, ea = interpolate(
            halpha_by_side["a"],
            float(frozen["halpha_approaching_lower_radius_arcsec"]),
            float(frozen["halpha_approaching_upper_radius_arcsec"]),
            float(frozen["halpha_approaching_lower_weight"]),
            float(frozen["halpha_approaching_upper_weight"]),
        )
        r, er = interpolate(
            halpha_by_side["r"],
            float(frozen["halpha_receding_lower_radius_arcsec"]),
            float(frozen["halpha_receding_upper_radius_arcsec"]),
            float(frozen["halpha_receding_lower_weight"]),
            float(frozen["halpha_receding_upper_weight"]),
        )
        odd = (r - a) * math.sin(angle)
        ha_odd.append(odd)
        ha_measurement_variance.append((math.sin(angle) * math.hypot(ea, er)) ** 2)
        ha_inclination_derivative.append((r - a) * math.cos(angle))
        ha_values.append((a, r, odd))
    ha_odd = np.asarray(ha_odd)
    ha_covariance = np.diag(ha_measurement_variance) + np.outer(
        ha_inclination_derivative, ha_inclination_derivative
    ) * math.radians(float(ghasp["kinematic_inclination_error_deg"])) ** 2

    product_paths = {item["filename"]: ROOT / item["local_path"] for item in source["manifest"]}
    primary_geometry = {
        "center": freeze["source_geometry"]["primary_center"],
        "inclination_deg": freeze["source_geometry"]["hi"]["inclination_deg"],
        "pa_deg": freeze["source_geometry"]["hi"]["receding_pa_deg"],
        "systemic_velocity_km_s": freeze["source_geometry"]["hi"]["systemic_velocity_km_s"],
    }
    variants = []
    for center in freeze["source_geometry"]["center_variants"]:
        variants.append({**primary_geometry, "center": center})
    for delta in (-1, 1):
        variants.append({**primary_geometry, "pa_deg": primary_geometry["pa_deg"] + delta * freeze["source_geometry"]["hi"]["pa_error_deg"]})
        variants.append({**primary_geometry, "inclination_deg": primary_geometry["inclination_deg"] + delta * freeze["source_geometry"]["hi"]["inclination_error_deg"]})
        variants.append({**primary_geometry, "systemic_velocity_km_s": primary_geometry["systemic_velocity_km_s"] + delta * freeze["source_geometry"]["hi"]["systemic_velocity_error_km_s"]})

    outputs = {}
    detail_rows = []
    for map_index, resolution in enumerate(("HR", "LR")):
        side_rows, hi_odd, bootstrap = extract_map(
            product_paths[f"NGC4559-{resolution}_mom0m.fits"],
            product_paths[f"NGC4559-{resolution}_mom1m.fits"],
            freeze,
            freeze_rows,
            primary_geometry,
            bootstrap=True,
            seed_offset=map_index * 100000,
        )
        variant_odds = []
        for variant in variants:
            _, odd, _ = extract_map(
                product_paths[f"NGC4559-{resolution}_mom0m.fits"],
                product_paths[f"NGC4559-{resolution}_mom1m.fits"],
                freeze,
                freeze_rows,
                variant,
                bootstrap=False,
            )
            variant_odds.append(odd)
        geometry_deviations = np.asarray(variant_odds) - hi_odd
        geometry_covariance = geometry_deviations.T @ geometry_deviations / len(variants)
        hi_bootstrap_covariance = np.cov(bootstrap, rowvar=False)
        delta = ha_odd - hi_odd
        covariance = ha_covariance + hi_bootstrap_covariance + geometry_covariance
        summary = gls(delta, covariance)
        summary.update(
            {
                "delta_odd_by_radius_km_s": delta.tolist(),
                "hi_odd_by_radius_km_s": hi_odd.tolist(),
                "halpha_odd_by_radius_km_s": ha_odd.tolist(),
                "geometry_variant_count": len(variants),
            }
        )
        outputs[resolution] = {
            "summary": summary,
            "covariance": covariance.tolist(),
            "covariance_components": {
                "halpha_odd": ha_covariance.tolist(),
                "hi_odd": (hi_bootstrap_covariance + geometry_covariance).tolist(),
                "cross_tracer": np.zeros_like(covariance).tolist(),
                "cross_tracer_status": "zero working assumption; shared geometry covariance unavailable",
            },
        }
        by_radius_side = {}
        for row in side_rows:
            by_radius_side.setdefault(row["radius_arcsec"], {})[row["side"]] = row
        for index, frozen in enumerate(freeze_rows):
            radius = float(frozen["radius_arcsec"])
            detail_rows.append(
                {
                    "resolution": resolution,
                    "radius_arcsec": radius,
                    "hi_approaching_u_los_km_s": by_radius_side[radius]["approaching"]["u_los_km_s"],
                    "hi_receding_u_los_km_s": by_radius_side[radius]["receding"]["u_los_km_s"],
                    "hi_odd_los_km_s": hi_odd[index],
                    "halpha_approaching_vrot_km_s": ha_values[index][0],
                    "halpha_receding_vrot_km_s": ha_values[index][1],
                    "halpha_odd_los_km_s": ha_odd[index],
                    "delta_odd_los_km_s": delta[index],
                    "hi_approaching_pixels": by_radius_side[radius]["approaching"]["n_pixels"],
                    "hi_receding_pixels": by_radius_side[radius]["receding"]["n_pixels"],
                    "hi_approaching_beam_blocks": by_radius_side[radius]["approaching"]["n_beam_blocks"],
                    "hi_receding_beam_blocks": by_radius_side[radius]["receding"]["n_beam_blocks"],
                    "endpoint_access": False,
                }
            )

    hr = outputs["HR"]["summary"]
    lr = outputs["LR"]["summary"]
    combined_sigma = math.hypot(hr["gls_mean_sigma_km_s"], lr["gls_mean_sigma_km_s"])
    same_sign_fraction = float(
        np.mean(np.sign(hr["delta_odd_by_radius_km_s"]) == np.sign(lr["delta_odd_by_radius_km_s"]))
    )
    gates = {
        "zero_odd_contrast_rejected_in_hr": hr["chi2_zero_p"] < 0.05,
        "zero_odd_contrast_rejected_in_lr": lr["chi2_zero_p"] < 0.05,
        "gls_mean_sign_agreement": bool(
            np.sign(hr["gls_mean_km_s"]) == np.sign(lr["gls_mean_km_s"])
        ),
        "hr_lr_gls_mean_difference_within_2sigma": abs(hr["gls_mean_km_s"] - lr["gls_mean_km_s"]) <= 2 * combined_sigma,
        "minimum_same_sign_radius_fraction": bool(same_sign_fraction >= 0.75),
    }
    gates = {key: bool(value) for key, value in gates.items()}
    channel_positive = all(gates.values())
    result = {
        "schema": "ngc4559_halogas_hi_halpha_replication_v01",
        "status": "NGC4559_HALOGAS_HI_HALPHA_REPLICATION_POSITIVE_SYSTEMATICS_OPEN" if channel_positive else "NGC4559_HALOGAS_HI_HALPHA_REPLICATION_NOT_POSITIVE",
        "galaxy": "NGC4559",
        "source_only_rank": 2,
        "maps": outputs,
        "hr_lr_same_sign_radius_fraction": same_sign_fraction,
        "hr_lr_gls_mean_difference_km_s": hr["gls_mean_km_s"] - lr["gls_mean_km_s"],
        "replication_gates": gates,
        "all_replication_gates_pass": channel_positive,
        "selection_uses_vobs_or_residual": False,
        "sparc_endpoint_opened": False,
        "physical_a_row_constructed": False,
        "observer_channel_detected": False,
        "claim_boundary": "prospective two-resolution map-derived tracer replication; even all gates passing would require conventional-systematics and common-parent controls before any observer-channel claim",
    }
    with (DATA / "ngc4559_halogas_hi_halpha_replication_v01.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(detail_rows[0]))
        writer.writeheader()
        writer.writerows(detail_rows)
    (DATA / "ngc4559_halogas_hi_halpha_replication_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    row_text = "\n".join(
        f"| {row['resolution']} | {row['radius_arcsec']:.0f} | {row['hi_odd_los_km_s']:.2f} | {row['halpha_odd_los_km_s']:.2f} | {row['delta_odd_los_km_s']:.2f} |"
        for row in detail_rows
    )
    (REPORTS / "ngc4559_halogas_hi_halpha_replication_v01.md").write_text(
        f"""# NGC4559 HALOGAS H I-Halpha Replication v0.1

**Status:** `{result['status']}`

| map | radius arcsec | H I odd km/s | Halpha odd km/s | Delta odd km/s |
| --- | ---: | ---: | ---: | ---: |
{row_text}

| resolution | GLS contrast | zero-null p |
| --- | ---: | ---: |
| HR | {hr['gls_mean_km_s']:.2f} +/- {hr['gls_mean_sigma_km_s']:.2f} km/s | {hr['chi2_zero_p']:.4g} |
| LR | {lr['gls_mean_km_s']:.2f} +/- {lr['gls_mean_sigma_km_s']:.2f} km/s | {lr['chi2_zero_p']:.4g} |

HR/LR radius-wise sign agreement is `{same_sign_fraction:.2f}`. Replication
gates: `{gates}`. Overall positive status is `{channel_positive}`.

This prospective test used the frozen WCS geometry, rings, wedge, mask,
weighted median, block bootstrap, and unchanged NGC3726 odd contrast. It did
not use SPARC velocities/residuals or baseline scores. Regardless of the gate
result, no observer-channel detection or physical `A_p` row is claimed:
moment-1 bias from extraplanar/non-bulk gas, Halpha tracer structure, and full
cross-tracer covariance remain physical alternatives.
""",
        encoding="utf-8",
    )
    print(result["status"])
    print(json.dumps({"HR": hr, "LR": lr, "gates": gates}, indent=2))


if __name__ == "__main__":
    main()
