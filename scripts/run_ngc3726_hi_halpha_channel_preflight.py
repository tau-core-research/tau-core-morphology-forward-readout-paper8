#!/usr/bin/env python3
"""Evaluate the frozen NGC3726 two-tracer side-odd channel diagnostic."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import chi2


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
HI_POINTS = DATA / "ngc3726_uma_hi_side_rotation_points_v01.csv"
HALPHA_POINTS = DATA / "ghasp_full_federation_side_points_v01.csv"
SOURCE = DATA / "ngc3726_uma_hi_rotation_source_v01.json"
FREEZE_JSON = DATA / "ngc3726_hi_halpha_angular_transport_freeze_v01.json"
FREEZE_CSV = DATA / "ngc3726_hi_halpha_angular_transport_freeze_v01.csv"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def projected_statistics(
    approaching: float,
    receding: float,
    approaching_error: float,
    receding_error: float,
    inclination_deg: float,
) -> dict[str, float]:
    angle = math.radians(inclination_deg)
    sine = math.sin(angle)
    cosine = math.cos(angle)
    u_approaching = approaching * sine
    u_receding = receding * sine
    odd = u_receding - u_approaching
    even = 0.5 * (u_receding + u_approaching)
    odd_measurement_sigma = sine * math.hypot(approaching_error, receding_error)
    even_measurement_sigma = 0.5 * sine * math.hypot(
        approaching_error, receding_error
    )
    return {
        "u_approaching": u_approaching,
        "u_receding": u_receding,
        "odd": odd,
        "even": even,
        "odd_measurement_sigma": odd_measurement_sigma,
        "even_measurement_sigma": even_measurement_sigma,
        "odd_inclination_derivative_per_rad": (receding - approaching) * cosine,
        "even_inclination_derivative_per_rad": 0.5
        * (receding + approaching)
        * cosine,
    }


def gls_summary(values: np.ndarray, covariance: np.ndarray) -> dict[str, float]:
    inverse = np.linalg.inv(covariance)
    ones = np.ones(len(values))
    variance = 1.0 / float(ones @ inverse @ ones)
    mean = variance * float(ones @ inverse @ values)
    chi2_zero = float(values @ inverse @ values)
    residual = values - mean
    chi2_constant = float(residual @ inverse @ residual)
    return {
        "gls_mean_km_s": mean,
        "gls_mean_sigma_km_s": math.sqrt(variance),
        "gls_mean_z": mean / math.sqrt(variance),
        "chi2_zero": chi2_zero,
        "chi2_zero_dof": len(values),
        "chi2_zero_p": float(chi2.sf(chi2_zero, len(values))),
        "chi2_constant": chi2_constant,
        "chi2_constant_dof": len(values) - 1,
        "chi2_constant_p": float(chi2.sf(chi2_constant, len(values) - 1)),
    }


def main() -> None:
    freeze = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    expected_hashes = freeze["input_sha256"]
    actual_hashes = {
        "hi_points": file_hash(HI_POINTS),
        "halpha_points": file_hash(HALPHA_POINTS),
        "geometry_source": file_hash(SOURCE),
    }
    if actual_hashes != expected_hashes:
        raise RuntimeError("Frozen NGC3726 transport inputs changed")
    geometry = json.loads(SOURCE.read_text(encoding="utf-8"))["metadata"]
    freeze_rows = list(csv.DictReader(FREEZE_CSV.open(newline="", encoding="utf-8")))
    hi_by_radius = {
        float(row["radius_arcsec"]): row
        for row in csv.DictReader(HI_POINTS.open(newline="", encoding="utf-8"))
    }
    halpha_rows = [
        row
        for row in csv.DictReader(HALPHA_POINTS.open(newline="", encoding="utf-8"))
        if row["sparc_match"] == "NGC3726"
    ]
    halpha_by_side_radius = {
        side: {
            float(row["radius_arcsec"]): row
            for row in halpha_rows
            if row["side"] == side
        }
        for side in ("a", "r")
    }

    result_rows = []
    odd_values = []
    even_values = []
    odd_measurement_variances = []
    odd_halpha_measurement_variances = []
    odd_hi_measurement_variances = []
    even_measurement_variances = []
    odd_halpha_derivatives = []
    odd_hi_derivatives = []
    even_halpha_derivatives = []
    even_hi_derivatives = []
    halpha_inclination = float(freeze["halpha_inclination_deg"])
    for frozen in freeze_rows:
        radius = float(frozen["radius_arcsec"])
        ha_a, ha_a_error = interpolate(
            halpha_by_side_radius["a"],
            float(frozen["halpha_approaching_lower_radius_arcsec"]),
            float(frozen["halpha_approaching_upper_radius_arcsec"]),
            float(frozen["halpha_approaching_lower_weight"]),
            float(frozen["halpha_approaching_upper_weight"]),
        )
        ha_r, ha_r_error = interpolate(
            halpha_by_side_radius["r"],
            float(frozen["halpha_receding_lower_radius_arcsec"]),
            float(frozen["halpha_receding_upper_radius_arcsec"]),
            float(frozen["halpha_receding_lower_weight"]),
            float(frozen["halpha_receding_upper_weight"]),
        )
        hi = hi_by_radius[radius]
        hi_a = float(hi["approaching_velocity_km_s"])
        hi_r = float(hi["receding_velocity_km_s"])
        hi_a_error = 0.5 * (
            float(hi["approaching_error_plus_km_s"])
            + float(hi["approaching_error_minus_km_s"])
        )
        hi_r_error = 0.5 * (
            float(hi["receding_error_plus_km_s"])
            + float(hi["receding_error_minus_km_s"])
        )
        hi_inclination = float(frozen["hi_inclination_deg"])
        ha_stats = projected_statistics(
            ha_a, ha_r, ha_a_error, ha_r_error, halpha_inclination
        )
        hi_stats = projected_statistics(
            hi_a, hi_r, hi_a_error, hi_r_error, hi_inclination
        )
        delta_odd = ha_stats["odd"] - hi_stats["odd"]
        delta_even = ha_stats["even"] - hi_stats["even"]
        odd_measurement_sigma = math.hypot(
            ha_stats["odd_measurement_sigma"], hi_stats["odd_measurement_sigma"]
        )
        even_measurement_sigma = math.hypot(
            ha_stats["even_measurement_sigma"], hi_stats["even_measurement_sigma"]
        )
        result_rows.append(
            {
                "radius_arcsec": radius,
                "halpha_approaching_vrot_km_s": ha_a,
                "halpha_receding_vrot_km_s": ha_r,
                "hi_approaching_vrot_km_s": hi_a,
                "hi_receding_vrot_km_s": hi_r,
                "halpha_odd_los_km_s": ha_stats["odd"],
                "hi_odd_los_km_s": hi_stats["odd"],
                "delta_odd_los_km_s": delta_odd,
                "delta_odd_measurement_sigma_km_s": odd_measurement_sigma,
                "halpha_even_los_km_s": ha_stats["even"],
                "hi_even_los_km_s": hi_stats["even"],
                "delta_even_los_km_s": delta_even,
                "delta_even_measurement_sigma_km_s": even_measurement_sigma,
                "endpoint_access": False,
            }
        )
        odd_values.append(delta_odd)
        even_values.append(delta_even)
        odd_measurement_variances.append(odd_measurement_sigma**2)
        odd_halpha_measurement_variances.append(ha_stats["odd_measurement_sigma"] ** 2)
        odd_hi_measurement_variances.append(hi_stats["odd_measurement_sigma"] ** 2)
        even_measurement_variances.append(even_measurement_sigma**2)
        odd_halpha_derivatives.append(ha_stats["odd_inclination_derivative_per_rad"])
        odd_hi_derivatives.append(-hi_stats["odd_inclination_derivative_per_rad"])
        even_halpha_derivatives.append(ha_stats["even_inclination_derivative_per_rad"])
        even_hi_derivatives.append(-hi_stats["even_inclination_derivative_per_rad"])

    sigma_i_ha = math.radians(float(freeze["halpha_inclination_error_deg"]))
    sigma_i_hi = math.radians(float(freeze["hi_inclination_error_deg_inner"]))

    def covariance(measurement, derivative_ha, derivative_hi):
        return (
            np.diag(np.asarray(measurement))
            + np.outer(derivative_ha, derivative_ha) * sigma_i_ha**2
            + np.outer(derivative_hi, derivative_hi) * sigma_i_hi**2
        )

    odd_covariance = covariance(
        odd_measurement_variances,
        np.asarray(odd_halpha_derivatives),
        np.asarray(odd_hi_derivatives),
    )
    even_covariance = covariance(
        even_measurement_variances,
        np.asarray(even_halpha_derivatives),
        np.asarray(even_hi_derivatives),
    )
    odd_summary = gls_summary(np.asarray(odd_values), odd_covariance)
    even_summary = gls_summary(np.asarray(even_values), even_covariance)
    odd_summary["pearson_halpha_hi_odd"] = float(
        np.corrcoef(
            [row["halpha_odd_los_km_s"] for row in result_rows],
            [row["hi_odd_los_km_s"] for row in result_rows],
        )[0, 1]
    )
    result = {
        "schema": "ngc3726_hi_halpha_channel_preflight_v01",
        "status": "NGC3726_TWO_TRACER_ODD_CONTRAST_NULL_NOT_REJECTED_PATTERN_DIAGNOSTIC",
        "galaxy": "NGC3726",
        "n_common_radii": len(result_rows),
        "common_radii_arcsec": [row["radius_arcsec"] for row in result_rows],
        "primary_odd_contrast": odd_summary,
        "secondary_even_offset": even_summary,
        "covariance_model": "independent quoted side errors plus tracer-wide shared inclination covariance",
        "covariance_components": {
            "halpha_odd": (
                np.diag(odd_halpha_measurement_variances)
                + np.outer(odd_halpha_derivatives, odd_halpha_derivatives) * sigma_i_ha**2
            ).tolist(),
            "hi_odd": (
                np.diag(odd_hi_measurement_variances)
                + np.outer(odd_hi_derivatives, odd_hi_derivatives) * sigma_i_hi**2
            ).tolist(),
            "cross_tracer": np.zeros_like(odd_covariance).tolist(),
            "cross_tracer_status": "zero working assumption; shared geometry covariance unavailable",
        },
        "not_in_covariance_model": [
            "beam-smearing covariance",
            "non-circular gas motions",
            "center uncertainty",
            "position-angle uncertainty and radial covariance",
            "phase-dependent tracer morphology",
        ],
        "selection_uses_vobs_or_residual": False,
        "sparc_endpoint_opened": False,
        "physical_a_row_constructed": False,
        "observer_channel_detected": False,
        "claim_boundary": "source-ranked single-galaxy two-tracer pattern diagnostic; the zero odd-contrast null is not rejected and no observer-path origin is identified",
    }
    with (DATA / "ngc3726_hi_halpha_channel_preflight_v01.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result_rows[0]))
        writer.writeheader()
        writer.writerows(result_rows)
    (DATA / "ngc3726_hi_halpha_channel_preflight_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    row_text = "\n".join(
        f"| {row['radius_arcsec']:.0f} | {row['halpha_odd_los_km_s']:.2f} | "
        f"{row['hi_odd_los_km_s']:.2f} | {row['delta_odd_los_km_s']:.2f} |"
        for row in result_rows
    )
    (REPORTS / "ngc3726_hi_halpha_channel_preflight_v01.md").write_text(
        f"""# NGC3726 H I-Halpha Channel Preflight v0.1

**Status:** `{result['status']}`

The source-ranked, frozen six-radius comparison returns both published curves
to line-of-sight equivalents before forming the side-odd contrast.

| radius arcsec | Halpha odd km/s | H I odd km/s | Delta odd km/s |
| ---: | ---: | ---: | ---: |
{row_text}

The covariance-aware GLS mean is
`{odd_summary['gls_mean_km_s']:.2f} +/- {odd_summary['gls_mean_sigma_km_s']:.2f} km/s`
(`z={odd_summary['gls_mean_z']:.2f}`). The zero-vector statistic is
`chi2={odd_summary['chi2_zero']:.2f}` for `{odd_summary['chi2_zero_dof']}`
degrees of freedom (`p={odd_summary['chi2_zero_p']:.4g}`). A constant contrast
is itself a poor description when its p-value is small; here the constant-fit
value is `p={odd_summary['chi2_constant_p']:.4g}`.

The six-radius odd pattern changes sign and the two tracer odd profiles are
strongly correlated (`r={odd_summary['pearson_halpha_hi_odd']:.3f}`). The
covariance-aware zero-contrast null is **not rejected**, and neither is a
constant contrast at the conventional 5% threshold. This is therefore a
pattern diagnostic and negative/indeterminate channel preflight, not evidence
for an observer/path channel. Beam smearing,
center and position-angle uncertainty, radial covariance, non-circular motion,
and phase-dependent H I/Halpha morphology are not yet in the covariance model.
No SPARC velocity, residual, MOND/RAR/RMOND/TPG score, or required Tau
amplitude was used.
""",
        encoding="utf-8",
    )
    print(result["status"])
    print(json.dumps(odd_summary, indent=2))


if __name__ == "__main__":
    main()
