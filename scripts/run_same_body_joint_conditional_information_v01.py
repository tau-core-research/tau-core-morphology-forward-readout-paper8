#!/usr/bin/env python3
"""Measure same-body H I/H-alpha conditional information with block covariance."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/same_body_joint_conditional_information_v01.md"
SOURCE_SIGMAS_KM_S = (10.0, 30.0, 100.0)
CROSS_RHOS = (0.0, 0.25, 0.5)


def information(channel: np.ndarray, source_cov: np.ndarray, noise_cov: np.ndarray) -> float:
    sign_n, logdet_n = np.linalg.slogdet(noise_cov)
    total = noise_cov + channel @ source_cov @ channel.T
    sign_t, logdet_t = np.linalg.slogdet(total)
    if sign_n <= 0 or sign_t <= 0:
        raise RuntimeError("Non-positive covariance in conditional-information calculation")
    return float(0.5 * (logdet_t - logdet_n) / np.log(2.0))


def block_noise(n_hi: np.ndarray, n_ha: np.ndarray, rho: float) -> np.ndarray:
    # This Cholesky coupling gives a positive block covariance for |rho|<1.
    jitter_hi = 1.0e-10 * max(float(np.trace(n_hi) / len(n_hi)), 1.0)
    jitter_ha = 1.0e-10 * max(float(np.trace(n_ha) / len(n_ha)), 1.0)
    l_hi = np.linalg.cholesky(n_hi + jitter_hi * np.eye(len(n_hi)))
    l_ha = np.linalg.cholesky(n_ha + jitter_ha * np.eye(len(n_ha)))
    cross = rho * l_hi @ l_ha.T
    return np.block([[n_hi, cross], [cross.T, n_ha]])


def source_covariance(radius: np.ndarray, sigma: float, length_factor: float = 1.0) -> np.ndarray:
    spacing = float(np.median(np.diff(np.sort(radius)))) if len(radius) > 1 else 1.0
    length = max(length_factor * spacing, 1.0e-12)
    delta = radius[:, None] - radius[None, :]
    return sigma**2 * np.exp(-0.5 * (delta / length) ** 2)


def evaluate(
    galaxy: str,
    resolution: str,
    radius: np.ndarray,
    n_hi: np.ndarray,
    n_ha: np.ndarray,
) -> list[dict]:
    identity = np.eye(len(radius))
    joint_channel = np.vstack([identity, identity])
    rows = []
    for sigma in SOURCE_SIGMAS_KM_S:
        q = source_covariance(radius, sigma)
        i_hi = information(identity, q, n_hi)
        i_ha = information(identity, q, n_ha)
        for rho in CROSS_RHOS:
            noise = block_noise(n_hi, n_ha, rho)
            i_joint = information(joint_channel, q, noise)
            delta_hi = i_joint - i_ha
            delta_ha = i_joint - i_hi
            rows.append({
                "galaxy": galaxy,
                "resolution": resolution,
                "n_radii": len(radius),
                "source_sigma_km_s": sigma,
                "cross_noise_rho": rho,
                "i_hi_bits": i_hi,
                "i_halpha_bits": i_ha,
                "i_joint_bits": i_joint,
                "delta_i_hi_given_halpha_bits": delta_hi,
                "delta_i_halpha_given_hi_bits": delta_ha,
                "redundant_information_bits": i_hi + i_ha - i_joint,
                "hi_unique_fraction_of_joint": delta_hi / i_joint,
                "halpha_unique_fraction_of_joint": delta_ha / i_joint,
            })
    return rows


def main() -> None:
    rows = []
    n3726 = json.loads(
        (DATA / "ngc3726_hi_halpha_channel_preflight_v01.json").read_text()
    )
    p3726 = pd.read_csv(DATA / "ngc3726_hi_halpha_channel_preflight_v01.csv")
    c3726 = n3726["covariance_components"]
    rows.extend(evaluate(
        "NGC3726", "published_profiles",
        p3726.radius_arcsec.to_numpy(),
        np.asarray(c3726["hi_odd"]), np.asarray(c3726["halpha_odd"]),
    ))

    n4559 = json.loads(
        (DATA / "ngc4559_halogas_hi_halpha_replication_v01.json").read_text()
    )
    p4559 = pd.read_csv(DATA / "ngc4559_halogas_hi_halpha_replication_v01.csv")
    for resolution in ("HR", "LR"):
        profile = p4559[p4559.resolution.eq(resolution)].sort_values("radius_arcsec")
        components = n4559["maps"][resolution]["covariance_components"]
        rows.extend(evaluate(
            "NGC4559", resolution, profile.radius_arcsec.to_numpy(),
            np.asarray(components["hi_odd"]), np.asarray(components["halpha_odd"]),
        ))

    frame = pd.DataFrame(rows)
    nominal = frame[
        frame.source_sigma_km_s.eq(30.0) & frame.cross_noise_rho.eq(0.0)
    ].copy()
    robust_hi = bool((frame.delta_i_hi_given_halpha_bits > 0.0).all())
    robust_ha = bool((frame.delta_i_halpha_given_hi_bits > 0.0).all())
    result = {
        "schema": "same_body_joint_conditional_information_v01",
        "status": "SHARED_SOURCE_PRECISION_GAIN_MEASURED_DISTINCT_TRACER_MODE_NOT_DETECTED",
        "law": "Delta I_j=I(source;y_j|other tracer)",
        "galaxies": 2,
        "channel_pairs": 3,
        "source_sigma_sensitivity_km_s": list(SOURCE_SIGMAS_KM_S),
        "cross_noise_rho_sensitivity": list(CROSS_RHOS),
        "nominal": {
            "mean_joint_information_bits": float(nominal.i_joint_bits.mean()),
            "mean_hi_given_halpha_bits": float(nominal.delta_i_hi_given_halpha_bits.mean()),
            "mean_halpha_given_hi_bits": float(nominal.delta_i_halpha_given_hi_bits.mean()),
            "mean_redundant_information_bits": float(nominal.redundant_information_bits.mean()),
            "mean_hi_unique_fraction": float(nominal.hi_unique_fraction_of_joint.mean()),
            "mean_halpha_unique_fraction": float(nominal.halpha_unique_fraction_of_joint.mean()),
        },
        "positive_incremental_information_all_sensitivities": {
            "hi_given_halpha": robust_hi,
            "halpha_given_hi": robust_ha,
        },
        "declared_tracer_jacobians": "C_HI=I and C_Halpha=I on the same radial source carrier",
        "stacked_rank_increment": 0,
        "shared_source_innovation_null_rejected": False,
        "innovation_evidence": {
            "ngc3726_zero_contrast_p": 0.14888777907332534,
            "ngc4559_hr_zero_contrast_rejected": False,
            "ngc4559_lr_zero_contrast_rejected": False,
        },
        "distinct_tracer_source_mode_detected": False,
        "cross_covariance_measured": False,
        "cross_covariance_treatment": "positive-definite rho sensitivity 0, 0.25, 0.5; not fitted",
        "shared_source_prior_parent_derived": False,
        "observer_time_channel_identified": False,
        "quantum_channel_identified": False,
        "physical_channel_detected": False,
        "interpretation": "each tracer improves precision about the declared shared radial odd-velocity source beyond the other, but the stacked Jacobian adds no source rank and the shared-source innovation null is not rejected; no distinct tracer source mode is detected",
        "claim_boundary": "two-galaxy, three-pair conditional-information diagnostic with source-scale and cross-noise sensitivity; line formation, pressure support, remaining geometry, and parent source covariance prevent time/path/quantum attribution",
    }
    frame.to_csv(DATA / "same_body_joint_conditional_information_v01.csv", index=False)
    (DATA / "same_body_joint_conditional_information_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    n = result["nominal"]
    REPORT.write_text(
        "# Same-body joint H I/H-alpha conditional information v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "The two tracers are treated as noisy views of one shared radial side-odd source. "
        "The full block covariance uses persisted tracer covariance matrices and an unfitted "
        "cross-noise sensitivity.\n\n"
        f"At the nominal `30 km/s`, `rho=0` convention, mean joint information is "
        f"`{n['mean_joint_information_bits']:.3f}` bits per profile. H I adds "
        f"`{n['mean_hi_given_halpha_bits']:.3f}` bits beyond H-alpha; H-alpha adds "
        f"`{n['mean_halpha_given_hi_bits']:.3f}` bits beyond H I. Mean redundant information "
        f"is `{n['mean_redundant_information_bits']:.3f}` bits. Both increments remain positive "
        "over all declared source-scale and cross-noise sensitivities.\n\n"
        "Positive conditional information here is a precision gain: both declared tracer "
        "Jacobians are identities on the same source, so stacked rank does not grow. The "
        "covariance-aware contrast tests also do not reject the shared-source innovation null. "
        "No distinct tracer mode, gas-physics, geometry, path, observer-time, or quantum-access "
        "origin is identified.\n",
        encoding="utf-8",
    )
    print(result["status"], json.dumps(result["nominal"], sort_keys=True))


if __name__ == "__main__":
    main()
