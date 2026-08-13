#!/usr/bin/env python3
"""Freeze the source-side test of refined morphological-body subfamilies."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


FAMILIES = [
    {
        "family": "K_scale_tail_turbulent_holey",
        "motivating_objects_not_test_eligible": "UGC04305;DDO_50;Holmberg_II",
        "required_source_fields": "HI_hole_catalog;HI_velocity_dispersion_profile;hole_covering_fraction;outer_HI_support_radius",
        "classification_rule": "resolved HI holes plus a published or source-measurable non-thermal dispersion profile across the optical disk",
        "kernel_change_frozen": "smooth scale-tail carrier multiplied by a bounded radial porosity-dispersion modulation",
        "primary_active_zone": "published HI-hole support union outer turbulent HI disk",
    },
    {
        "family": "K_disturbed_tidal_history",
        "motivating_objects_not_test_eligible": "UGC07577;DDO_125",
        "required_source_fields": "companion_or_stream_detection;projected_stream_support;kinematic_asymmetry;interaction_confidence",
        "classification_rule": "independent tidal stream or companion evidence and a source-side disturbed-kinematics flag",
        "kernel_change_frozen": "coarse carrier plus a bounded asymmetric outer-support term restricted to the source-marked disturbance zone",
        "primary_active_zone": "source-marked stream or disturbed outer-disk support",
    },
    {
        "family": "K_warped_asymmetric_disturbed_disk",
        "motivating_objects_not_test_eligible": "NGC4088;UGC7081",
        "required_source_fields": "warp_onset_radius;tilted_ring_PA_profile;approaching_receding_asymmetry;outer_HI_radius",
        "classification_rule": "source-measured warp onset plus significant side-to-side or position-angle asymmetry",
        "kernel_change_frozen": "thick/flared carrier split into symmetric vertical and signed warp-asymmetry components",
        "primary_active_zone": "R greater than or equal to the source-frozen warp onset",
    },
    {
        "family": "K_bar_dominated_non_circular",
        "motivating_objects_not_test_eligible": "NGC4389;UGC7514",
        "required_source_fields": "bar_length;bar_position_angle;harmonic_non_circular_amplitude;bar_confidence",
        "classification_rule": "independently measured stellar bar and a source-side non-circular velocity harmonic",
        "kernel_change_frozen": "thick/flared carrier with a compact bar-windowed non-circular component",
        "primary_active_zone": "R less than or equal to the source-frozen bar length",
    },
]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    csv_path = DATA / "refined_body_subfamily_preregistration_v01.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FAMILIES[0].keys())
        writer.writeheader()
        writer.writerows(FAMILIES)

    payload = {
        "schema": "tau_core_refined_body_subfamily_preregistration_v01",
        "status": "SOURCE_ACQUISITION_ONLY",
        "construction_uses_vobs_or_rotation_residual": False,
        "inspected_motivating_objects_endpoint_eligible": False,
        "alias_resolution_required_before_sample_freeze": True,
        "minimum_independent_galaxies_per_family": 5,
        "minimum_total_independent_galaxies": 20,
        "primary_endpoint": "per-galaxy RMSE of the frozen matched body kernel",
        "primary_control": "mean RMSE over frozen wrong-family kernels",
        "primary_population_success_rule": "matched-minus-wrong-family mean delta below zero with a galaxy-level one-sided permutation p <= 0.05",
        "specificity_rule": "matched kernel beats the best wrong family in at least 0.60 of independent galaxies",
        "zone_rule": "improvement must be larger in the source-frozen active zone than outside it",
        "newton_rule": "report matched-versus-Newton win fraction; no universal-superiority threshold is imposed",
        "channel_handoff_rule": "fit no nonconventional channel term until the refined body test is frozen and scored; only cross-tracer residual structure surviving the matched body model may nominate a channel test",
        "failure_rule": "failure of population, specificity, or active-zone rule rejects the refined family version without post-score retuning",
        "families": FAMILIES,
        "endpoint_scoring_allowed": False,
        "next_gate": "acquire source-native fields and freeze an alias-resolved untouched galaxy manifest",
    }
    (DATA / "refined_body_subfamily_preregistration_v01.json").write_text(
        json.dumps(payload, indent=2) + "\n"
    )

    lines = [
        "# Refined body-subfamily preregistration v01",
        "",
        "Status: `SOURCE_ACQUISITION_ONLY`",
        "",
        "This freezes a residual-blind test of four refined morphological-body families. The motivating P0 failures are explicitly excluded from endpoint evidence, including all aliases. Classification and radial activation must be determined from source-native morphology and kinematics before rotation-curve scoring is opened.",
        "",
        "## Frozen decision order",
        "",
        "1. Resolve physical aliases and remove every historical or motivating object.",
        "2. Acquire all required source fields and classify without `vobs` or residual access.",
        "3. Freeze family, kernel, amplitude policy, sign, and active radial zone.",
        "4. Score matched, wrong-family, and Newtonian controls in a separate process.",
        "5. Test a channel only on cross-tracer residual structure left after the matched refined body.",
        "",
        "## Population verdict",
        "",
        "The refined-body route passes only if the matched-minus-wrong-family mean RMSE difference is negative with a one-sided galaxy permutation `p <= 0.05`, the matched family beats the best wrong family in at least `60%` of independent galaxies, and its gain is stronger inside the source-frozen active zone. At least five independent galaxies per family and twenty total are required.",
        "",
        "No universal superiority over Newton, MOND, or TPG is assumed. Every comparison is reported, including negative results.",
        "",
        "## Frozen families",
        "",
    ]
    for row in FAMILIES:
        lines.extend(
            [
                f"### `{row['family']}`",
                "",
                f"- Motivating objects, excluded from endpoint evidence: `{row['motivating_objects_not_test_eligible']}`.",
                f"- Required fields: `{row['required_source_fields']}`.",
                f"- Classification: {row['classification_rule']}.",
                f"- Kernel change: {row['kernel_change_frozen']}.",
                f"- Active zone: {row['primary_active_zone']}.",
                "",
            ]
        )
    lines.extend(
        [
            "## Claim boundary",
            "",
            "This document is a preregistration, not evidence that any refined family is physically correct. It also does not identify time, quantum, capacity, light-cone, or other channel physics. Such attribution is permitted only after a source-frozen refined-body score leaves a reproducible cross-tracer remainder.",
            "",
        ]
    )
    (REPORTS / "refined_body_subfamily_preregistration_v01.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
