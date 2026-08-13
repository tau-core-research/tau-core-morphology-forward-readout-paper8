#!/usr/bin/env python3
"""Freeze a residual-blind morphology-body amplitude-law candidate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/body_amplitude_law_freeze_v01.json"


def main() -> None:
    result = {
        "schema": "tau-core.paper8.body-amplitude-law-freeze.v01",
        "status": "SOURCE_SIDE_BODY_AMPLITUDE_LAW_FROZEN_DIAGNOSTIC_SCORE_ALLOWED",
        "formula": (
            "v_body^2=max(v_Newton^2 + K_f(B,R) * "
            "[b_f + sum_j w_j z_j(B)],0)"
        ),
        "source_features": [
            "total_gas_fraction",
            "mean_log_sbdisk",
            "mean_bulge",
            "log_scale_radius_proxy_kpc",
            "log_tail_to_scale_ratio",
        ],
        "feature_transforms": {
            "log_scale_radius_proxy_kpc": "log(scale_radius_proxy_kpc)",
            "log_tail_to_scale_ratio": (
                "log(tail_cutoff_radius_proxy_kpc/scale_radius_proxy_kpc)"
            ),
            "standardization": "train-galaxy mean and population standard deviation",
        },
        "coefficient_structure": (
            "four family intercepts plus five global source-feature slopes"
        ),
        "ridge_alpha_grid": [0.0, 0.01, 0.1, 1.0, 10.0, 100.0],
        "alpha_selection": "five-fold grouped train-galaxy CV minimizing galaxy-balanced MSE",
        "point_weighting": "each train galaxy has total weight one",
        "morphology_family_labels_frozen": True,
        "kernel_shapes_frozen": True,
        "uses_vobs_or_residual": False,
        "channel_coordinates": [],
        "known_limits": {
            "zero_kernel": "v_body=v_Newton",
            "zero_amplitude": "v_body=v_Newton",
        },
        "claim_boundary": (
            "source-side diagnostic amplitude-law freeze; coefficients and ridge strength "
            "may use train endpoints, but no holdout retuning or physical derivation claim"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(result["status"])


if __name__ == "__main__":
    main()
