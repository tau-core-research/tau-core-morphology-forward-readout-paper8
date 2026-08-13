#!/usr/bin/env python3
"""Prove the terminal-gain identifiability boundary of the NGC4254 v07 proxy.

The audit reads only the source-side v07 freeze.  It proves that one terminal
readout cannot test the FFL spectral law while its source-to-terminal gain is
free, and records the rank conditions required for a future multi-readout
component separation.  No velocity, residual, or dark-discrepancy endpoint is
read.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

V07_PATH = DATA / "ngc4254_ffl_direct_beam_m2_operator_v07.json"
V07_SUMMARY_PATH = DATA / "ngc4254_ffl_direct_beam_m2_summary_v07.csv"
JSON_PATH = DATA / "ngc4254_ffl_terminal_identifiability_v08.json"
REPORT_PATH = REPORTS / "ngc4254_ffl_terminal_identifiability_v08.md"

STATUS = "SOURCE_ONLY_TERMINAL_IDENTIFIABILITY_NO_GO_PROVED_NO_ENDPOINT"
CLAIM_BOUNDARY = (
    "algebraic source-to-terminal identifiability result using the frozen v07 "
    "q_shape proxy; not a physical gain derivation, channel-component recovery, "
    "time/quantum/gravity attribution, dark-matter replacement, or endpoint score"
)
RANDOM_SEED = 425408
N_IDENTITY_CHECKS = 10000


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def beta_read(beta_dyn: np.ndarray, q_terminal: np.ndarray) -> np.ndarray:
    response = np.tanh(q_terminal)
    return (beta_dyn + response) / (1.0 + beta_dyn * response)


def required_gain(
    beta_dyn: np.ndarray, beta_obs: np.ndarray, q_source: float
) -> np.ndarray:
    relative = (beta_obs - beta_dyn) / (1.0 - beta_obs * beta_dyn)
    return np.arctanh(relative) / q_source


def main() -> None:
    v07 = json.loads(V07_PATH.read_text())
    summary = pd.read_csv(V07_SUMMARY_PATH)
    if v07["inputs"]["velocity_or_residual_inputs"]:
        raise ValueError("v07 unexpectedly declares endpoint inputs")
    if not v07["result"]["m2_family_specificity_pass"]:
        raise ValueError("v07 m=2 source family did not pass its frozen specificity gate")

    m2 = summary.loc[summary["harmonic"].eq(2)]
    if len(m2) != 1:
        raise ValueError("Expected exactly one v07 m=2 summary row")
    q_source = float(m2["baseline_q_shape_proxy"].iloc[0])
    q_min = float(m2["source_q_min"].iloc[0])
    q_max = float(m2["source_q_max"].iloc[0])
    if q_source == 0.0 or q_min <= 0.0:
        raise ValueError("The v08 nonidentifiability proof requires the surviving nonzero source proxy")

    rng = np.random.default_rng(RANDOM_SEED)
    beta_dyn = rng.uniform(-0.2, 0.2, N_IDENTITY_CHECKS)
    beta_obs = rng.uniform(-0.2, 0.2, N_IDENTITY_CHECKS)
    gain = required_gain(beta_dyn, beta_obs, q_source)
    replay = beta_read(beta_dyn, gain * q_source)
    maximum_identity_error = float(np.max(np.abs(replay - beta_obs)))
    single_terminal_saturated = maximum_identity_error < 1.0e-12

    manifest = {
        "schema": "ngc4254_ffl_terminal_identifiability_v08",
        "status": STATUS,
        "galaxy": "NGC4254",
        "source_result": {
            "family": "direct stellar-m2 morphology-phase operator",
            "q_shape_proxy_baseline": q_source,
            "q_shape_proxy_source_range": [q_min, q_max],
            "source_family_specificity_pass": True,
            "physical_q_det_constructed": False,
        },
        "single_terminal_theorem": {
            "forward_law": "beta_read=(beta_dyn+tanh(g*q_shape))/(1+beta_dyn*tanh(g*q_shape))",
            "inverse_gain": "g_req=atanh((beta_obs-beta_dyn)/(1-beta_obs*beta_dyn))/q_shape",
            "domain": "q_shape != 0, beta_dyn,beta_obs in (-1,1), and the fitted gain g is unconstrained over the reals",
            "verdict": "a free gain exactly saturates one scalar terminal endpoint",
            "consequence": "single-terminal scoring is nonfalsifiable until the gain is source-derived or independently frozen",
            "random_seed": RANDOM_SEED,
            "identity_checks": N_IDENTITY_CHECKS,
            "maximum_reconstruction_error": maximum_identity_error,
            "single_terminal_free_gain_saturated": single_terminal_saturated,
        },
        "factorization_no_go": {
            "model": "q_req=A*c for source-frozen terminal sensitivity matrix A and channel-component vector c",
            "component_identifiability_iff": "A is independently frozen and has full column rank",
            "minimum_terminal_coordinate_count": "the number of independent scalar terminal coordinates must be at least the number of claimed components",
            "unknown_factorization_gauge": "A->A*S and c->S^-1*c leaves q_req unchanged for every invertible S",
            "named_readouts_are_independent_by_name": False,
            "one_scalar_source_proxy_separates_components": False,
        },
        "minimum_future_measurement_contract": [
            "derive or independently freeze the physical gain from kappa_X, kappa_Y, Q_*, lambda, w_A, and w_S",
            "freeze one shared parent-readout descriptor before terminal maps",
            "supply at least K independent scalar terminal coordinates for K claimed channel components, obtained from mutually nonfactorizing terminal maps",
            "freeze the terminal sensitivity matrix A without using scored residuals",
            "verify full column rank and a non-negligible smallest singular value under complete covariance",
            "use side-resolved spectra to retain both common and differential channel sectors",
            "treat time, quantum, gravity, and other names as interpretations only after their terminal maps are recovered",
        ],
        "paired_spectral_boundary": {
            "relative_observable": "side odd/even ratio isolates the differential q sector conditionally",
            "absolute_observable": "side geometric mean retains the terminal-visible common sector conditionally",
            "two_observables_identify_time_quantum_gravity_components": False,
            "reason": "common/differential separation is not a physical component basis without independently derived terminal sensitivities",
        },
        "inputs": {
            "v07_manifest": str(V07_PATH.relative_to(ROOT)),
            "v07_manifest_sha256": sha256(V07_PATH),
            "v07_summary": str(V07_SUMMARY_PATH.relative_to(ROOT)),
            "v07_summary_sha256": sha256(V07_SUMMARY_PATH),
            "velocity_or_residual_inputs": [],
        },
        "result": {
            "morphology_source_coordinate_robust": True,
            "single_terminal_physical_test_ready": False,
            "channel_presence_detected": False,
            "channel_components_identifiable": False,
            "endpoint_scoring_allowed": False,
            "next_finite_target": "source-derived terminal gain plus a source-frozen full-rank multi-readout sensitivity matrix",
        },
        "audit_checks": {
            "source_only": True,
            "velocity_or_residual_inputs_empty": True,
            "v07_q_nonzero": q_source != 0.0,
            "v07_source_range_excludes_zero": q_min > 0.0,
            "inverse_forward_identity_verified": single_terminal_saturated,
            "free_gain_not_fitted_to_endpoint": True,
            "endpoint_scored": False,
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }

    report = f"""# NGC4254 FFL Terminal Identifiability Audit v08

**Status:** `{STATUS}`

**Claim boundary:** {CLAIM_BOUNDARY}.

## Source Input

The v07 direct `m=2` source operator survives its internal specificity gate
with baseline `q_shape_proxy={q_source:+.8f}` and 72-scenario source range
`[{q_min:+.8f},{q_max:+.8f}]`. This audit accepts that source-coordinate result
without promoting it to physical `q_det`.

## Single-Terminal No-Go

Suppose the conditional complete spectral law is reduced to one scalar
terminal with an unknown source-to-terminal gain `g`:

```text
beta_read = (beta_dyn + tanh(g q_shape))
            / (1 + beta_dyn tanh(g q_shape)).
```

For every admissible `beta_dyn` and `beta_obs`, nonzero `q_shape` and an
unconstrained real gain give

```text
g_req = atanh[(beta_obs-beta_dyn)/(1-beta_obs beta_dyn)] / q_shape.
```

Substitution recovers `beta_obs` exactly. The fixed-seed numerical identity
check over `{N_IDENTITY_CHECKS}` pairs has maximum error
`{maximum_identity_error:.3e}`. Therefore a freely fitted gain makes one scalar
endpoint saturated and nonfalsifiable. The gain must come from the primitive
curvatures and normalization, or be frozen independently, before scoring.

## Multi-Readout Rank Condition

For `K` claimed channel components, write the required terminal coordinates as

```text
q_req = A c.
```

Within this fixed linear component model, the component vector `c` is
identifiable only if the terminal sensitivity matrix `A` is independently
frozen and has full column rank `K`. Merely naming several readouts does not
supply independent scalar rows. If both `A` and `c` are
unknown, `A -> A S` and `c -> S^-1 c` leave every prediction unchanged for any
invertible `S`.

Side-resolved spectra can conditionally separate a common sector from a
differential sector, but those two observables do not by themselves identify
time, quantum, gravity, or other physical components.

## Verdict

The robust v07 morphology coordinate is real at the declared source-audit
level. What remains missing is not just more endpoint data: it is the physical
gain and a source-frozen, full-rank terminal sensitivity matrix. Until those
exist, neither channel presence nor channel-component decomposition is
identified, and endpoint scoring remains closed.
"""
    REPORT_PATH.write_text(report)
    JSON_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(STATUS)
    print(f"q_shape={q_source:+.8f} max_identity_error={maximum_identity_error:.3e}")


if __name__ == "__main__":
    main()
