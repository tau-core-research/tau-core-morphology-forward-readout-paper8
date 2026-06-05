#!/usr/bin/env python3
"""Build a residual-blind MOM1 sign/cross-term review packet for NGC7331.

The packet measures source-native kinematic orientation context from THINGS
moment-1 velocity fields. It does not freeze the B2 sign and does not close
epsilon_cross; it provides review inputs needed before any exact-transfer
formula freeze is allowed.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_things_mom1_sign_cross_review_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.6g}")
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def read_image(path: Path) -> np.ndarray:
    return np.squeeze(np.asarray(fits.getdata(path), dtype=float))


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    total = float(np.sum(weights))
    if total <= 0:
        return math.nan
    return float(np.sum(values * weights) / total)


def principal_axis(x: np.ndarray, y: np.ndarray, weights: np.ndarray) -> np.ndarray:
    x0 = weighted_mean(x, weights)
    y0 = weighted_mean(y, weights)
    dx = x - x0
    dy = y - y0
    total = float(np.sum(weights))
    cov = np.array(
        [
            [float(np.sum(weights * dx * dx) / total), float(np.sum(weights * dx * dy) / total)],
            [float(np.sum(weights * dx * dy) / total), float(np.sum(weights * dy * dy) / total)],
        ]
    )
    eigvals, eigvecs = np.linalg.eigh(cov)
    major = eigvecs[:, int(np.argmax(eigvals))]
    if major[0] < 0:
        major = -major
    return major


def angle_deg(vector: np.ndarray) -> float:
    return math.degrees(math.atan2(float(vector[1]), float(vector[0])))


def acute_delta_deg(a_deg: float, b_deg: float) -> float:
    delta = abs((a_deg - b_deg + 90.0) % 180.0 - 90.0)
    return float(delta)


def weighted_linear_gradient(
    x: np.ndarray, y: np.ndarray, velocity: np.ndarray, weights: np.ndarray
) -> tuple[np.ndarray, float]:
    design = np.column_stack([np.ones_like(x), x, y])
    sqrt_w = np.sqrt(np.maximum(weights, 0.0))
    lhs = design * sqrt_w[:, None]
    rhs = velocity * sqrt_w
    beta, *_ = np.linalg.lstsq(lhs, rhs, rcond=None)
    gradient = np.array([float(beta[1]), float(beta[2])])
    norm = float(np.linalg.norm(gradient))
    if norm > 0:
        gradient = gradient / norm
    return gradient, float(beta[0])


def measure_pair(product_prefix: str, mom0_path: Path, mom1_path: Path, geometry: pd.Series) -> dict:
    mom0 = read_image(mom0_path)
    mom1 = read_image(mom1_path) / 1000.0
    y_idx, x_idx = np.indices(mom0.shape)
    x = x_idx.astype(float) - (float(geometry["crpix1"]) - 1.0)
    y = y_idx.astype(float) - (float(geometry["crpix2"]) - 1.0)
    r_circular = np.hypot(x, y)

    positive = np.where(np.isfinite(mom0), np.maximum(mom0, 0.0), 0.0)
    finite_velocity = np.isfinite(mom1)
    positive_values = positive[positive > 0]
    threshold = 0.20 * float(np.percentile(positive_values, 95))
    signal = (positive >= threshold) & finite_velocity
    warp_onset_pix = float(geometry["warp_onset_pix"])
    rhi_pix = float(geometry["rhi_pix"])
    inner = signal & (r_circular <= warp_onset_pix)
    outer = signal & (np.abs(r_circular) >= warp_onset_pix) & (r_circular <= rhi_pix)

    major = principal_axis(x[inner], y[inner], positive[inner])
    morph_pa = angle_deg(major)
    minor = np.array([-major[1], major[0]])
    u = x * major[0] + y * major[1]

    velocity_inner = mom1[inner]
    weights_inner = positive[inner]
    systemic = weighted_mean(velocity_inner, weights_inner)
    gradient, intercept = weighted_linear_gradient(
        x[inner], y[inner], velocity_inner - systemic, weights_inner
    )
    kin_pa = angle_deg(gradient)
    delta_pa = acute_delta_deg(morph_pa, kin_pa)
    f_pa = abs(math.sin(math.radians(delta_pa)))

    side_a_inner = inner & (u > 0)
    side_b_inner = inner & (u < 0)
    side_a_outer = outer & (u > 0)
    side_b_outer = outer & (u < 0)
    v_a_inner = weighted_mean(mom1[side_a_inner] - systemic, positive[side_a_inner])
    v_b_inner = weighted_mean(mom1[side_b_inner] - systemic, positive[side_b_inner])
    v_a_outer = weighted_mean(mom1[side_a_outer] - systemic, positive[side_a_outer])
    v_b_outer = weighted_mean(mom1[side_b_outer] - systemic, positive[side_b_outer])
    side_a_is_receding = bool(v_a_inner > v_b_inner)
    receding_side = "A_POS_MAJOR_AXIS" if side_a_is_receding else "B_NEG_MAJOR_AXIS"
    inner_contrast = abs(v_a_inner - v_b_inner)
    outer_contrast = abs(v_a_outer - v_b_outer)
    side_contrast_ratio = outer_contrast / max(inner_contrast, 1.0e-12)
    same_orientation = bool((v_a_inner - v_b_inner) * (v_a_outer - v_b_outer) > 0)
    f_velocity_asymmetry = abs(abs(v_a_outer) - abs(v_b_outer)) / max(
        0.5 * (abs(v_a_outer) + abs(v_b_outer)), 1.0e-12
    )

    return {
        "galaxy": GALAXY,
        "product_prefix": product_prefix,
        "mom0_path": str(mom0_path.relative_to(ROOT)),
        "mom1_path": str(mom1_path.relative_to(ROOT)),
        "threshold_rule": "mom0_positive_above_0p20_p95_and_finite_mom1",
        "systemic_velocity_km_s_source_native": systemic,
        "morph_pa_image_deg": morph_pa,
        "kinematic_pa_image_deg": kin_pa,
        "morph_kin_delta_pa_deg": delta_pa,
        "f_pa": f_pa,
        "v_side_a_inner_km_s": v_a_inner,
        "v_side_b_inner_km_s": v_b_inner,
        "v_side_a_outer_km_s": v_a_outer,
        "v_side_b_outer_km_s": v_b_outer,
        "receding_side_inner": receding_side,
        "inner_outer_receding_orientation_same": same_orientation,
        "outer_to_inner_velocity_contrast_ratio": side_contrast_ratio,
        "f_velocity_side_asymmetry": f_velocity_asymmetry,
        "n_inner_pixels": int(np.sum(inner)),
        "n_outer_pixels": int(np.sum(outer)),
        "endpoint_scores_allowed": False,
        "uses_vobs_or_residual": False,
        "measurement_status": "MOM1_KINEMATIC_CONTEXT_REVIEW_REQUIRED",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    geometry = pd.read_csv(DATA / "ngc7331_things_qwarp_measurement_geometry.csv").iloc[0]
    manifest = pd.read_csv(DATA / "ngc7331_things_hi_product_manifest.csv")
    path_by_id = {
        row["product_id"]: Path(row["local_cache_path"]) for _, row in manifest.iterrows()
    }
    rows = [
        measure_pair("NATURAL", path_by_id["NA_MOM0"], path_by_id["NA_MOM1"], geometry),
        measure_pair("ROBUST", path_by_id["RO_MOM0"], path_by_id["RO_MOM1"], geometry),
    ]
    measurements = pd.DataFrame(rows)

    sensitivity_summary = pd.read_csv(
        DATA / "ngc7331_things_qwarp_measurement_sensitivity_summary.csv"
    ).iloc[0]
    q_centroid = float(
        0.5
        * (
            sensitivity_summary["q_centroid_mean_min"]
            + sensitivity_summary["q_centroid_mean_max"]
        )
    )
    q_envelope = float(
        0.5
        * (
            sensitivity_summary["q_envelope_p80_mean_min"]
            + sensitivity_summary["q_envelope_p80_mean_max"]
        )
    )
    f_q_observable_choice = abs(q_envelope - q_centroid) / max(q_envelope, 1.0e-12)
    f_pa = float(measurements["f_pa"].max())
    f_r = float(measurements["f_velocity_side_asymmetry"].max())
    f_context = 1.0
    epsilon_candidate = 0.5 * (f_pa * f_r + f_r * f_q_observable_choice + f_q_observable_choice * f_context)

    response = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "response_id": "N7331_THINGS_MOM1_SIGN_CROSS_REVIEW_V1",
                "receding_side_consensus": (
                    "CONSISTENT"
                    if measurements["receding_side_inner"].nunique() == 1
                    else "PRODUCT_DISAGREEMENT"
                ),
                "inner_outer_receding_orientation_same_all": bool(
                    measurements["inner_outer_receding_orientation_same"].all()
                ),
                "f_pa_max": f_pa,
                "f_velocity_side_asymmetry_max": f_r,
                "f_q_observable_choice": f_q_observable_choice,
                "f_context_complex_warp": f_context,
                "epsilon_cross_candidate_bound": epsilon_candidate,
                "sigma_warp_sign_status": "KINEMATIC_CONTEXT_AVAILABLE_SIGN_NOT_FROZEN",
                "epsilon_cross_status": "CANDIDATE_BOUND_REVIEW_REQUIRED_NOT_CLOSED",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_MOM1SC1_PRODUCTS",
                "gate_status": "PASS",
                "evidence": "NA_MOM1 and RO_MOM1 are cached and paired with MOM0 masks",
                "remaining_obligation": "none at product availability level",
            },
            {
                "gate_id": "N7331_MOM1SC2_KINEMATIC_ORIENTATION",
                "gate_status": "REVIEW_REQUIRED",
                "evidence": (
                    f"max morph/kin delta PA={f_pa:.6g} as sin(delta); "
                    f"consensus={response.iloc[0]['receding_side_consensus']}"
                ),
                "remaining_obligation": "independent review must define sign convention for B2 added-readout vs attenuation",
            },
            {
                "gate_id": "N7331_MOM1SC3_EPSILON_CROSS",
                "gate_status": "CANDIDATE_BOUND_REVIEW_REQUIRED",
                "evidence": f"epsilon_cross_candidate_bound={epsilon_candidate:.6g}",
                "remaining_obligation": "review f_pa, f_R, f_q, and context factor before accepting or carrying interval",
            },
            {
                "gate_id": "N7331_MOM1SC4_FORMULA_FREEZE",
                "gate_status": "BLOCKED",
                "evidence": "sign not frozen and epsilon_cross bound not closed",
                "remaining_obligation": "freeze sign and close/carry epsilon_cross before exact B2 transfer",
            },
            {
                "gate_id": "N7331_MOM1SC5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "script reads THINGS moment maps and source geometry only",
                "remaining_obligation": "none at endpoint-blindness level",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "mom1_sign_cross_status": "NGC7331_THINGS_MOM1_SIGN_CROSS_REVIEW_BUILT_FREEZE_BLOCKED",
                "n_products_measured": int(len(measurements)),
                "sigma_warp_sign_ready": False,
                "epsilon_cross_bound_ready": False,
                "epsilon_cross_candidate_bound": epsilon_candidate,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "independent sign review and accepted epsilon_cross interval/decision"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    measurements.to_csv(DATA / "ngc7331_things_mom1_sign_cross_measurements.csv", index=False)
    response.to_csv(DATA / "ngc7331_things_mom1_sign_cross_response.csv", index=False)
    gates.to_csv(DATA / "ngc7331_things_mom1_sign_cross_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_things_mom1_sign_cross_summary.csv", index=False)

    report = [
        "# NGC7331 THINGS MOM1 Sign/Cross-Term Review",
        "",
        "Status: `NGC7331_THINGS_MOM1_SIGN_CROSS_REVIEW_BUILT_FREEZE_BLOCKED`.",
        "",
        "This packet measures residual-blind kinematic orientation context from",
        "THINGS moment-1 maps. It does not freeze the B2 sign and it does not",
        "close epsilon_cross.",
        "",
        "## MOM1 measurements",
        "",
        markdown_table(measurements),
        "",
        "## Review response",
        "",
        markdown_table(response),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
    ]
    (REPORTS / "ngc7331_things_mom1_sign_cross_review.md").write_text(
        "\n".join(report), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
