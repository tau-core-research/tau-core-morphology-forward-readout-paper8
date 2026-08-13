#!/usr/bin/env python3
"""Audit whether the UGC08490 H I/H-alpha scale is geometric or channel-specific."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/ugc08490_tracer_scale_origin_audit_v01.md"
I_HA = 40.0
E_I_HA = 15.0
I_HI = 50.3
E_I_HI = 2.0
SEED = 8490


def scale(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.dot(x, y) / np.dot(x, x))


def rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(x**2)))


def main() -> None:
    common = pd.read_csv(DATA / "ugc08490_repetto_hi_halpha_common_profile_v01.csv")
    ha = pd.read_csv(DATA / "ghasp_full_federation_side_points_v01.csv")
    ha = ha[ha.sparc_match.eq("UGC08490")]
    radii = common.radius_arcsec.to_numpy()
    hi = common.hi_rotation_km_s.to_numpy()
    side_values = {}
    for side in ("a", "r"):
        source = ha[ha.side.eq(side)].sort_values("radius_arcsec")
        side_values[side] = np.interp(radii, source.radius_arcsec, source.velocity_km_s)
    ha_mean = (side_values["a"] + side_values["r"]) / 2
    fitted = scale(ha_mean, hi)
    inclination_prediction = math.sin(math.radians(I_HA)) / math.sin(math.radians(I_HI))
    geometry_residual_factor = fitted / inclination_prediction

    rng = np.random.default_rng(SEED)
    bootstrap = []
    for _ in range(20_000):
        index = rng.integers(0, len(hi), len(hi))
        bootstrap.append(scale(ha_mean[index], hi[index]))
    ci = np.quantile(bootstrap, [0.025, 0.5, 0.975])
    split = np.median(radii)
    inner = radii <= split
    outer = radii > split
    side_scales = {side: scale(values, hi) for side, values in side_values.items()}
    radial_scales = {"inner": scale(ha_mean[inner], hi[inner]), "outer": scale(ha_mean[outer], hi[outer])}
    raw_rms = rms(hi - ha_mean)
    geometry_rms = rms(hi - inclination_prediction * ha_mean)
    fitted_rms = rms(hi - fitted * ha_mean)

    # Propagate the published inclination errors only; this is deliberately not a fit.
    inclination_draws = rng.normal(I_HA, E_I_HA, 200_000)
    hi_draws = rng.normal(I_HI, E_I_HI, 200_000)
    valid = (inclination_draws > 1) & (inclination_draws < 89) & (hi_draws > 1) & (hi_draws < 89)
    predicted_draws = np.sin(np.radians(inclination_draws[valid])) / np.sin(np.radians(hi_draws[valid]))
    prediction_ci = np.quantile(predicted_draws, [0.025, 0.5, 0.975])
    result = {
        "schema": "ugc08490_tracer_scale_origin_audit_v01",
        "status": "NEGATIVE_RESULT_PRESERVED",
        "n_common_points": len(common),
        "measured_hi_over_halpha_scale": fitted,
        "point_bootstrap_scale_95_interval": ci.tolist(),
        "scale_differs_from_unity_in_point_bootstrap": bool(ci[2] < 1),
        "source_inclinations_deg": {
            "ghasp_halpha_kinematic": [I_HA, E_I_HA],
            "repetto_hi_kinematic": [I_HI, E_I_HI],
        },
        "inclination_only_predicted_scale": inclination_prediction,
        "inclination_prediction_95_interval": prediction_ci.tolist(),
        "measured_scale_inside_inclination_prediction_interval": bool(prediction_ci[0] <= fitted <= prediction_ci[2]),
        "residual_scale_after_inclination_harmonization": geometry_residual_factor,
        "side_specific_scales": side_scales,
        "radial_half_scales": radial_scales,
        "rms_km_s": {"unscaled": raw_rms, "inclination_only": geometry_rms, "free_scale": fitted_rms},
        "distance_scale_used_in_comparison": False,
        "tau_core_scale_candidate_promoted": False,
        "physical_channel_detected": False,
        "endpoint_access": False,
        "claim_boundary": (
            "the measured scale is consistent with the independently published inclination mismatch; "
            "no residual observer-channel time factor is identified"
        ),
    }
    (DATA / "ugc08490_tracer_scale_origin_audit_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    REPORT.write_text(
        "# UGC08490 tracer-scale origin audit v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The measured H I/Halpha scale is `{fitted:.4f}` with a point-bootstrap 95% "
        f"interval of `[{ci[0]:.4f}, {ci[2]:.4f}]`. GHASP used a kinematic inclination "
        f"of `{I_HA:.0f} +/- {E_I_HA:.0f} deg`, while Repetto et al. used "
        f"`{I_HI:.1f} +/- {E_I_HI:.1f} deg`. Pure deprojection therefore predicts "
        f"`sin({I_HA:.0f})/sin({I_HI:.1f}) = {inclination_prediction:.4f}`.\n\n"
        f"Using the inclination-only factor lowers RMS from `{raw_rms:.2f}` to "
        f"`{geometry_rms:.2f} km/s`; a freely fitted scale reaches `{fitted_rms:.2f} km/s`. "
        f"The remaining multiplicative factor after inclination harmonization is "
        f"`{geometry_residual_factor:.4f}`.\n\n"
        "The scale is a real difference between the published readouts, but this audit "
        "does not promote it as a Tau Core channel signal: the independently documented "
        "inclination mismatch already predicts its magnitude.\n",
        encoding="utf-8",
    )
    print(result["status"], f"measured={fitted:.4f}", f"geometry={inclination_prediction:.4f}")


if __name__ == "__main__":
    main()
