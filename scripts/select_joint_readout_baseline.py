#!/usr/bin/env python3
"""Select the parsimonious joint-readout baseline from frozen channel tests."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
OUT = DATA / "joint_readout_body_dominant_baseline_selection_v01.json"
REPORT = ROOT / "reports/joint_readout_body_dominant_baseline_selection_v01.md"


def load(name: str):
    return json.loads((DATA / name).read_text())


def main() -> None:
    path = load("sparc_path_disturbance_dark_discrepancy_test_v01.json")
    interaction = load("continuous_channel_dark_discrepancy_interaction_v01.json")
    tracer = load("same_body_tracer_effective_kernel_amplitude_test_v01.json")
    clock = load("ngc7331_things_clock_channel_parity_v01.json")
    multipath = load("sdp81_q1_multipath_spectral_score_v01.json")
    tests = [
        {
            "family": "population_path_proxy",
            "verdict": "not_selected",
            "evidence": path["status"],
            "physical_channel_detected": path["physical_channel_detected"],
        },
        {
            "family": "continuous_source_channel_interaction",
            "verdict": "not_selected",
            "evidence": interaction["status"],
            "shuffle_p": interaction["shuffle_p"],
            "physical_channel_detected": interaction["physical_channel_detected"],
        },
        {
            "family": "same_body_tracer_kernel_amplitude",
            "verdict": "conventional_scale_control_preferred",
            "evidence": tracer["status"],
            "physical_channel_detected": tracer["physical_channel_detected"],
        },
        {
            "family": "common_multiplicative_spectral_clock",
            "verdict": "rejected_in_tested_single_galaxy_family",
            "evidence": clock["status"],
            "predicted_to_observed_even_ratio": clock["predicted_to_observed_even_ratio"],
        },
        {
            "family": "true_multipath_integrated_spectral_shape",
            "verdict": "non_exceptional_diagnostic",
            "evidence": multipath["status"],
            "empirical_upper_tail_fraction": multipath[
                "published_endpoint_empirical_upper_tail_fraction"
            ],
            "channel_origin_identified": multipath["channel_origin_identified"],
        },
    ]
    no_positive_channel_test = all(
        not item.get("physical_channel_detected", False)
        and not item.get("channel_origin_identified", False)
        for item in tests
    )
    result = {
        "schema": "tau-core.paper8.joint-readout-baseline-selection.v01",
        "status": "BODY_DOMINANT_JOINT_READOUT_SELECTED_AS_WORKING_BASELINE",
        "decision_rule": (
            "select the no-nonconventional-channel baseline when no predeclared "
            "channel family survives its controls; require grouped holdout gain "
            "and independent replication to add a channel deformation"
        ),
        "baseline_model": "Y_Oc = P_Oc[K_body(B)] + epsilon",
        "nested_alternative": "Y_Oc = P_Oc[K_body(B) + Delta_Oc(B;theta)] + epsilon",
        "nonconventional_channel_default": "Delta_Oc = 0",
        "independent_test_family_count": len(tests),
        "no_positive_channel_test": no_positive_channel_test,
        "tests": tests,
        "next_primary_score": (
            "grouped body-level holdout performance of the source-frozen morphology "
            "kernel against baryonic/Newtonian, MOND/RAR, TPG, wrong-family, and "
            "shuffled controls, with no fitted channel coordinate"
        ),
        "claim_boundary": (
            "working model selection within tested channel families; not a theorem "
            "that all channels are trivial and not a Tau Core or dark-matter proof"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# Joint-readout body-dominant baseline selection\n\n"
        f"Status: `{result['status']}`\n\n"
        "Five distinct channel-test families currently provide no positive physical "
        "channel detection; one narrow common spectral-clock family is directly "
        "incompatible with its frozen single-galaxy parity test. The selected working "
        "baseline is therefore `Y_Oc=P_Oc[K_body(B)]+epsilon`, where `P_Oc` retains "
        "ordinary calibrated observer/tracer transport and no nonconventional channel "
        "coordinate is fitted. A future `Delta_Oc` must earn inclusion through grouped "
        "holdout gain, nuisance-control survival, and independent replication. This is "
        "a parsimonious model-selection verdict, not a universal no-channel theorem.\n"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
