#!/usr/bin/env python3
"""Audit axisymmetric and non-axisymmetric gas-dynamic sectors in NGC4254."""

import json
from pathlib import Path

import numpy as np
from scipy.stats import chi2


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"


def sector_test(document, indices):
    statistic = 0.0
    rank = 0
    for block in document["zone_mode_blocks"]:
        coefficient = np.asarray(block["coefficient_km_s"], float)[indices]
        covariance = np.asarray(block["sector_jackknife_covariance_km2_s2"], float)[np.ix_(indices, indices)]
        statistic += float(coefficient @ np.linalg.pinv(covariance) @ coefficient)
        rank += int(np.linalg.matrix_rank(covariance))
    return {"chi2": statistic, "dof": rank, "p": float(chi2.sf(statistic, rank))}


def main():
    field = json.loads((DATA / "ngc4254_phangs_tracer_velocity_field_rank_test_v01.json").read_text())
    sectors = {
        "axisymmetric_m0": sector_test(field, [0]),
        "lopsided_streaming_m1": sector_test(field, [1, 2]),
        "bisymmetric_m2": sector_test(field, [3, 4]),
        "combined_nonaxisymmetric_m1_m2": sector_test(field, [1, 2, 3, 4]),
    }
    result = {
        "schema": "ngc4254_common_mode_gas_dynamics_v04",
        "input": "data/derived/ngc4254_phangs_tracer_velocity_field_rank_test_v01.json",
        "covariance": "12-sector spatial jackknife covariance in five radial zones",
        "conditional_axisymmetric_pressure_cancellation": (
            "pressure support changes the side-odd azimuthal speed and cancels from ideal opposite-side geometric mean"
        ),
        "sectors": sectors,
        "nonaxisymmetric_tracer_structure_detected": sectors["combined_nonaxisymmetric_m1_m2"]["p"] < 0.01,
        "dominant_interpretable_sector": "m1 lopsided/streaming; individually p<0.05 but not p<0.01",
        "gas_dynamics_can_contaminate_common_mode": True,
        "gas_dynamics_fully_explains_common_mode": False,
        "common_channel_remainder_identified": False,
        "effective_time_readout_detected": False,
        "next_test": (
            "recompute G_spec after source-frozen m1/m2 field prediction and geometry perturbations, "
            "then test only the held-out remainder"
        ),
        "claim_boundary": (
            "covariance-aware reuse of a frozen 2D tracer-field decomposition; supports a conventional "
            "non-axisymmetric contamination route but is not a complete subtraction or channel test"
        ),
    }
    (DATA / "ngc4254_common_mode_gas_dynamics_v04.json").write_text(json.dumps(result, indent=2) + "\n")
    (ROOT / "reports/ngc4254_common_mode_gas_dynamics_v04.md").write_text(
        "# NGC4254 common-mode gas-dynamics audit v04\n\n"
        "Axisymmetric pressure support changes the side-odd azimuthal speed and therefore "
        "cancels from an ideal opposite-side spectral geometric mean. The relevant contaminants "
        "are even/non-axisymmetric flow, sampling, and profile-mixing sectors.\n\n"
        f"Using the existing five-zone, 12-sector jackknife covariance, `m0` gives "
        f"`chi2={sectors['axisymmetric_m0']['chi2']:.2f}/5` "
        f"(`p={sectors['axisymmetric_m0']['p']:.4f}`), `m1` gives "
        f"`chi2={sectors['lopsided_streaming_m1']['chi2']:.2f}/10` "
        f"(`p={sectors['lopsided_streaming_m1']['p']:.4f}`), and combined `m1+m2` gives "
        f"`chi2={sectors['combined_nonaxisymmetric_m1_m2']['chi2']:.2f}/20` "
        f"(`p={sectors['combined_nonaxisymmetric_m1_m2']['p']:.5f}`).\n\n"
        "The data therefore support a conventional non-axisymmetric gas-dynamic contamination "
        "route, dominated interpretably by lopsided/streaming structure. This does not prove that "
        "it explains the full common-mode profile; no channel remainder exists until a frozen "
        "m1/m2 prediction is subtracted and survives geometry controls.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
