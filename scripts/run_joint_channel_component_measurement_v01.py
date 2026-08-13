#!/usr/bin/env python3
"""Measure available joint-channel components without fabricating a common sample."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/joint_channel_component_measurement_v01.md"
SEED = 20260711
N_PERMUTATIONS = 10000


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def permutation_spearman(x: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> dict:
    observed = float(spearmanr(x, y).statistic)
    null = np.empty(N_PERMUTATIONS)
    for index in range(N_PERMUTATIONS):
        null[index] = spearmanr(x, rng.permutation(y)).statistic
    return {
        "rho": observed,
        "permutation_p_two_sided": float((1 + np.sum(np.abs(null) >= abs(observed))) / (N_PERMUTATIONS + 1)),
    }


def main() -> None:
    rng = np.random.default_rng(SEED)
    oscc = load("little_things_oscc_capacity_scoring_v02.json")
    scores = pd.read_csv(DATA / "little_things_oscc_capacity_scores_by_galaxy_v02.csv")
    scores = scores[scores.inclination_deg >= 40].copy()
    scores["oscc_improvement_vs_tpg"] = scores.rmse_tpg_v6 - scores.rmse_oscc_v02
    scores["oscc_improvement_vs_v02"] = scores.rmse_v02 - scores.rmse_oscc_v02
    scores["median_velocity_error_km_s"] = scores.galaxy.map(
        pd.read_csv(DATA / "little_things_prospective_kernel_scored_points_v01.csv")
        .groupby("galaxy").velocity_error_km_s.median()
    )
    correlations = {}
    for variable in [
        "distance_mpc", "hi_beam_fwhm_kpc", "median_velocity_error_km_s",
        "oscc_improvement_vs_tpg", "oscc_improvement_vs_v02",
    ]:
        correlations[variable] = permutation_spearman(
            scores.capacity_bits.to_numpy(), scores[variable].to_numpy(), rng
        )

    tracer = load("same_body_tracer_effective_kernel_amplitude_test_v01.json")
    ugc = load("ugc08490_tracer_scale_origin_audit_v01.json")
    parity = load("ngc7331_things_clock_channel_parity_v01.json")
    path_discrepancy = load("sparc_path_disturbance_dark_discrepancy_test_v01.json")
    path_beta = load("effective_kernel_amplitude_path_information_test_v01.json")
    zone = load("dark_discrepancy_zone_multitracer_channel_audit_v01.json")
    joint_tracer = load("same_body_joint_conditional_information_v01.json")

    ledger = pd.DataFrame([
        {
            "component": "measured spatial/capacity channel",
            "sample": "LITTLE THINGS primary",
            "n_objects": 14,
            "measured_statistic": f"mean capacity={oscc['primary']['capacity_bits_per_profile_use']['mean']:.3f} bits/profile-use",
            "control_result": "water filling active; negligible score change",
            "identification_status": "operational capacity measured; parent G/P and correlated noise open",
        },
        {
            "component": "same-body joint tracer information",
            "sample": "NGC3726 and NGC4559",
            "n_objects": 2,
            "measured_statistic": (
                f"mean joint={joint_tracer['nominal']['mean_joint_information_bits']:.3f} bits; "
                f"H I|H-alpha={joint_tracer['nominal']['mean_hi_given_halpha_bits']:.3f}; "
                f"H-alpha|H I={joint_tracer['nominal']['mean_halpha_given_hi_bits']:.3f}"
            ),
            "control_result": "both conditional increments positive, but stacked rank increment is zero and innovation null is not rejected",
            "identification_status": "shared-source precision gain measured; distinct tracer mode not detected",
        },
        {
            "component": "same-body tracer terminal",
            "sample": "NGC3726 and NGC4559",
            "n_objects": 2,
            "measured_statistic": "H I/H-alpha amplitudes differ above 2 sigma in all tested lanes",
            "control_result": "multiplicative carrier beats Tau-kernel shape controls",
            "identification_status": "tracer contrast present; Tau-kernel-specific channel not identified",
        },
        {
            "component": "same-body tracer scale",
            "sample": "UGC08490",
            "n_objects": 1,
            "measured_statistic": f"H I/H-alpha scale={ugc['measured_hi_over_halpha_scale']:.3f}",
            "control_result": f"inclination predicts {ugc['inclination_only_predicted_scale']:.3f}; harmonized residual={ugc['residual_scale_after_inclination_harmonization']:.3f}",
            "identification_status": "standard inclination explanation sufficient",
        },
        {
            "component": "common multiplicative clock channel",
            "sample": "NGC7331",
            "n_objects": 1,
            "measured_statistic": f"predicted/observed side-even ratio={parity['predicted_to_observed_even_ratio']:.0f}",
            "control_result": "required common clock multiplier incompatible with side parity",
            "identification_status": "simple common clock law rejected for this galaxy; differential clock/path law untested",
        },
        {
            "component": "foreground/path information on mass discrepancy",
            "sample": "SPARC path subset",
            "n_objects": path_discrepancy["n_galaxies"],
            "measured_statistic": f"OOF MSE reduction={path_discrepancy['proportional_mse_reduction']:.3f}, p={path_discrepancy['shuffle']['p']:.3f}",
            "control_result": "incremental path test fails",
            "identification_status": "no path information detected for outer discrepancy target",
        },
        {
            "component": "foreground/path information on fitted kernel amplitude",
            "sample": "SPARC path subset",
            "n_objects": path_beta["n_galaxies"],
            "measured_statistic": f"OOF MSE reduction={path_beta['proportional_mse_reduction']:.3f}, p={path_beta['shuffle']['p']:.3f}",
            "control_result": "retrospective incremental signal passes",
            "identification_status": "confounded endpoint-derived beta; physical path channel not identified",
        },
        {
            "component": "dark-discrepancy-zone tracer contrast",
            "sample": "NGC3726 and NGC4559",
            "n_objects": 2,
            "measured_statistic": "post-onset contrast appears in one of two galaxies",
            "control_result": f"replicated={zone['zero_contrast_rejected_in_both_galaxies']}",
            "identification_status": "not replicated; time/quantum origin not identified",
        },
        {
            "component": "quantum-access channel",
            "sample": "none",
            "n_objects": 0,
            "measured_statistic": "no phase-sensitive coherent terminal observable",
            "control_result": "not measurable from rotation products",
            "identification_status": "unmeasured",
        },
    ])

    detected_capacity_predictor = any(
        value["permutation_p_two_sided"] < 0.05
        for key, value in correlations.items()
        if key.startswith("oscc_improvement")
    )
    result = {
        "schema": "joint_channel_component_measurement_v01",
        "status": "SAME_BODY_PRECISION_GAIN_MEASURED_DISTINCT_MODE_AND_FULL_ORIGIN_BLOCKED",
        "joint_law": "Delta I_j(Q)=I_Q(all readouts)-I_Q(without j)=I_Q(source;y_j|y_-j)",
        "little_things_capacity_correlations": correlations,
        "capacity_predicts_score_improvement_at_p_lt_0_05": detected_capacity_predictor,
        "component_counts": {
            "operationally_measured": 4,
            "positive_but_confounded": 2,
            "negative_or_standard_explained": 4,
            "quantum_measured": 0,
        },
        "same_body_tracer_delta_i_computed": True,
        "same_body_distinct_tracer_mode_detected": False,
        "full_joint_channel_delta_i_computable": False,
        "blocker": "same-body tracer Delta I is measured on two galaxies, but full tracer/path/time/spectral block covariance and independent replication are absent",
        "time_channel_status": "simple common multiplier rejected in one galaxy; general differential observer-source parameterization unmeasured",
        "quantum_channel_status": "unmeasured",
        "physical_channel_detected": False,
        "claim_boundary": "cross-product component ledger and within-product statistics; heterogeneous samples cannot be combined into a physical joint-channel detection or common conditional-information value",
    }
    ledger.to_csv(DATA / "joint_channel_component_measurement_ledger_v01.csv", index=False)
    scores.to_csv(DATA / "joint_channel_little_things_capacity_correlations_v01.csv", index=False)
    (DATA / "joint_channel_component_measurement_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    corr_lines = "\n".join(
        f"- capacity vs `{name}`: rho `{value['rho']:+.3f}`, permutation p `{value['permutation_p_two_sided']:.3f}`"
        for name, value in correlations.items()
    )
    REPORT.write_text(
        "# Joint observer-source channel component measurement v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "The joint law uses conditional information to test whether one readout adds source "
        "information beyond the others. Same-body H I/H-alpha Delta I is now calculated for "
        "two galaxies with covariance sensitivity. The complete tracer/path/time/spectral "
        "joint Delta I remains unavailable.\n\n"
        "## LITTLE THINGS capacity associations\n\n"
        f"{corr_lines}\n\n"
        "## Component verdict\n\n"
        "Operational beam/noise capacity is measurable, but it does not establish a physical "
        "time, path, or quantum origin. Same-body tracer differences exist in the small sample, "
        "yet kernel-shape and inclination controls prevent promotion. The path proxy does not "
        "predict outer discrepancy, although it retrospectively predicts a confounded fitted "
        "kernel amplitude. One-galaxy parity rejects only the simple common clock multiplier. "
        "The same-body tracer pair improves shared-source precision under every declared "
        "sensitivity, but adds no declared source rank and does not reject the innovation null. "
        "No distinct tracer mode or quantum-access statistic is present.\n",
        encoding="utf-8",
    )
    print(result["status"], json.dumps(correlations, sort_keys=True))


if __name__ == "__main__":
    main()
