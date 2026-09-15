#!/usr/bin/env python3
"""Post-open uncertainty audit for the frozen NGC2541 HALOGAS endpoint."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RINGS = ROOT / "data/derived/ngc2541_halogas_independent_side_consistency_endpoint_v01_rings.csv"
OUT = ROOT / "data/derived/ngc2541_halogas_side_consistency_robustness_v01.json"
REPORT = ROOT / "reports/ngc2541_halogas_side_consistency_robustness_v01.md"


def main() -> None:
    rings = pd.read_csv(RINGS)
    fixed = rings[(rings.geometry == "fixed") & rings.eligible][
        ["radius_arcsec", "absolute_side_difference_kms"]
    ].rename(columns={"absolute_side_difference_kms": "fixed"})
    variable = rings[(rings.geometry == "variable") & rings.eligible][
        ["radius_arcsec", "absolute_side_difference_kms"]
    ].rename(columns={"absolute_side_difference_kms": "variable"})
    paired = fixed.merge(variable, on="radius_arcsec")
    delta = paired.variable.to_numpy(float) - paired.fixed.to_numpy(float)
    n = len(delta)
    if n < 2:
        raise RuntimeError("insufficient paired rings")

    rng = np.random.default_rng(2541)
    bootstrap = delta[rng.integers(0, n, size=(100000, n))].mean(axis=1)
    signs = rng.choice(np.array([-1.0, 1.0]), size=(100000, n))
    null_means = (signs * np.abs(delta)).mean(axis=1)
    observed = float(delta.mean())
    loo = np.array([np.delete(delta, i).mean() for i in range(n)])
    result = {
        "schema": "tau_core_ngc2541_halogas_side_consistency_robustness_v01",
        "status": "NAIVE_CORRELATED_RING_UNCERTAINTY_DIAGNOSTIC_ONLY",
        "n_paired_rings": n,
        "mean_delta_variable_minus_fixed_kms": observed,
        "bootstrap_95pct_ci_kms": [float(np.quantile(bootstrap, 0.025)), float(np.quantile(bootstrap, 0.975))],
        "one_sided_sign_flip_p": float((1 + np.sum(null_means <= observed)) / (1 + len(null_means))),
        "rings_improved": int(np.sum(delta < 0)),
        "rings_worsened": int(np.sum(delta > 0)),
        "leave_one_out_delta_range_kms": [float(loo.min()), float(loo.max())],
        "leave_one_out_direction_always_improves": bool(np.all(loo < 0)),
        "interpretation": "rings are beam-correlated and the iid-ring bootstrap/sign-flip assumptions are not established; quoted interval and p-value are descriptive only",
        "claim_boundary": "Post-open robustness diagnostic; it cannot upgrade the standard calibration control into a Tau-specific or dark-matter-replacement result.",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# NGC2541 HALOGAS side-consistency robustness audit v01\n\n"
        + f"Paired rings: `{n}`. Mean variable-minus-fixed difference: `{observed:.6f} km/s`. "
        + f"Bootstrap 95% interval: `[{result['bootstrap_95pct_ci_kms'][0]:.6f}, "
        + f"{result['bootstrap_95pct_ci_kms'][1]:.6f}] km/s`. One-sided paired sign-flip "
        + f"p-value: `{result['one_sided_sign_flip_p']:.6f}`. Rings improved/worsened: "
        + f"`{result['rings_improved']}/{result['rings_worsened']}`.\n\n"
        + result["claim_boundary"] + "\n"
    )
    print("NGC2541_HALOGAS_SIDE_CONSISTENCY_ROBUSTNESS_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
