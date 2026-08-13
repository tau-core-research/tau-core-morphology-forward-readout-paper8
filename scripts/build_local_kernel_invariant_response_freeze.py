#!/usr/bin/env python3
"""Freeze the first local dimensionless body-kernel response candidate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/local_kernel_invariant_response_freeze_v01.json"


def main() -> None:
    result = {
        "schema": "tau-core.paper8.local-kernel-invariant-response-freeze.v01",
        "status": "LOCAL_DIMENSIONLESS_KERNEL_RESPONSE_FROZEN_DIAGNOSTIC_SCORE_ALLOWED",
        "formula": "v_body^2 = v_Newton^2 * exp(eta_f * phi_f(R))",
        "local_invariant": "u_f(R)=K_f(R)/K_f(R_s)",
        "bounded_activation": "phi_f(R)=u_f(R)/(1+u_f(R))",
        "reference_radius": "source-frozen scale_radius_proxy_kpc",
        "reference_interpolation": "linear interpolation on each galaxy radial grid",
        "reference_floor": "max(abs(K_f(R_s)),1e-12*max(abs(K_f)))",
        "trainable_parameters": "one dimensionless eta_f per frozen morphology family",
        "eta_grid": [-4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.75, -0.5, -0.25,
                     0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
        "eta_selection": "train-only galaxy-balanced RMSE independently by family",
        "uses_vobs_or_residual": False,
        "channel_coordinates": [],
        "known_limits": {
            "eta_zero": "v_body=v_Newton",
            "phi_zero": "v_body=v_Newton",
            "finite_activation": "0<=phi<1 for nonnegative kernels",
            "positive_velocity_squared": True,
        },
        "claim_boundary": (
            "source-side formula freeze; eta uses train endpoints after freeze; diagnostic, "
            "not prospective and not a parent-derived response law"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(result["status"])


if __name__ == "__main__":
    main()
