#!/usr/bin/env python3
"""Audit which parts of the Paper 8 Tau kernel are source- or endpoint-informed."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"


def main() -> None:
    observables = pd.read_csv(DATA / "s4g75_promoted_kernel_observable_fill.csv")
    amplitudes = pd.read_csv(DATA / "source_native_readout_formula_amplitudes.csv")
    provenance = ";".join(observables.kernel_observable_provenance.dropna().astype(str).unique()).lower()
    explicit_path_tokens = [token for token in ("foreground", "lightcone", "observer", "shear", "convergence") if token in provenance]
    payload = {
        "schema": "tau_kernel_body_channel_provenance_audit_v01",
        "status": "EFFECTIVE_KERNEL_SOURCE_SHAPE_TRAINED_READOUT_AMPLITUDE_PATH_UNIDENTIFIED",
        "shape_and_scale_layer": {
            "n_kernel_observable_rows": len(observables),
            "sources": ["S4G morphology/scale components", "SPARC distance, RHI, Rdisk, Reff and inclination proxies"],
            "uses_observed_rotation_endpoint": False,
            "explicit_observer_path_inputs": explicit_path_tokens,
        },
        "amplitude_layer": {
            "n_formula_families": len(amplitudes),
            "fit_policy": amplitudes.fit_policy.unique().tolist(),
            "target": "training vobs^2 - v_tpg_v6^2",
            "uses_observed_rotation_endpoint": True,
            "scope": "one population amplitude per formula family",
        },
        "effective_kernel_interpretation": (
            "K_eff,g(R)=beta_family_train*K_shape,g(R); source observables select shape/scale, "
            "while the training endpoint fixes a shared readout amplitude"
        ),
        "identifiability": {
            "body_shape_separable_from_shared_amplitude_by_current_construction": True,
            "physical_path_channel_separable_from_amplitude": False,
            "galaxy_specific_channel_kernel_measured": False,
            "tracer_specific_channel_kernel_measured": False,
        },
        "required_next_measurement": (
            "hold K_shape fixed and infer endpoint-heldout effective kernel deformations from "
            "independent tracers or null paths; test amplitude, radial dilation, onset shift, "
            "tail deformation and family mixing without refitting body coordinates"
        ),
        "claim_boundary": (
            "provenance and identifiability audit only; current kernel success is compatible "
            "with body information, shared readout calibration, or an unresolved combination"
        ),
        "verdict": "CURRENT_KERNEL_CAN_BE_EFFECTIVE_BUT_DOES_NOT_ISOLATE_PHYSICAL_CHANNEL_CONTENT",
    }
    (DATA / "tau_kernel_body_channel_provenance_audit_v01.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["verdict"])


if __name__ == "__main__":
    main()
