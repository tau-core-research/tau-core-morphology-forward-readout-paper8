#!/usr/bin/env python3
"""Audit whether the v07 source chart identifies primitive FFL curvatures.

The audit constructs local FFL actions with the same stationary source state
and different positive primitive Hessian curvatures.  It also keeps physical
action curvature distinct from measurement-likelihood covariance.  Only v07
and v08 source-side artifacts are read; no terminal endpoint is opened.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

V07_PATH = DATA / "ngc4254_ffl_direct_beam_m2_operator_v07.json"
V08_PATH = DATA / "ngc4254_ffl_terminal_identifiability_v08.json"
JSON_PATH = DATA / "ngc4254_ffl_primitive_curvature_identifiability_v09.json"
REPORT_PATH = REPORTS / "ngc4254_ffl_primitive_curvature_identifiability_v09.md"

STATUS = "SOURCE_STATE_DOES_NOT_IDENTIFY_PRIMITIVE_FFL_CURVATURES_PROVED_NO_ENDPOINT"
CLAIM_BOUNDARY = (
    "constructive source-state/Hessian identifiability no-go and measurement-"
    "covariance separation; not a physical curvature or gain derivation, "
    "channel detection, component recovery, or endpoint score"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def effective_stiffness(kappa_x: float, kappa_y: float, mu_r: float) -> float:
    return kappa_x * kappa_y / (mu_r + kappa_x + kappa_y)


def terminal_gain(k: float, q_star: float, access_offset: float) -> float:
    return k / (q_star * (access_offset + k))


def main() -> None:
    v07 = json.loads(V07_PATH.read_text())
    v08 = json.loads(V08_PATH.read_text())
    if v07["inputs"]["velocity_or_residual_inputs"]:
        raise ValueError("v07 unexpectedly declares endpoint inputs")
    if v08["inputs"]["velocity_or_residual_inputs"]:
        raise ValueError("v08 unexpectedly declares endpoint inputs")
    if not v07["result"]["m2_family_specificity_pass"]:
        raise ValueError("The source chart required by v09 did not survive v07")

    q_source = float(v08["source_result"]["q_shape_proxy_baseline"])
    mu_r = 0.0
    q_star = 1.0
    access_offset = 1.0
    curvature_pairs = ((1.0, 1.0), (1.0, 9.0), (4.0, 4.0), (2.0, 8.0))
    witnesses = []
    for kappa_x, kappa_y in curvature_pairs:
        k = effective_stiffness(kappa_x, kappa_y, mu_r)
        gain = terminal_gain(k, q_star, access_offset)
        witnesses.append(
            {
                "kappa_X": kappa_x,
                "kappa_Y": kappa_y,
                "mu_R": mu_r,
                "effective_k": k,
                "conditional_gain": gain,
                "same_stationary_q_shape_proxy": q_source,
                "conditional_terminal_q": gain * q_source,
            }
        )
    gains = np.asarray([row["conditional_gain"] for row in witnesses], dtype=float)
    distinct_gains = int(len(np.unique(gains))) == len(witnesses)

    manifest = {
        "schema": "ngc4254_ffl_primitive_curvature_identifiability_v09",
        "status": STATUS,
        "galaxy": "NGC4254",
        "stationary_state_countermodel": {
            "local_action_family": "A=(mu_R/2)||c-c0||^2+(kappa_X/2)||(c-c0)-(x-x0)||^2+(kappa_Y/2)||(c-c0)-iota(y-y0)||^2",
            "shared_stationary_state": "(x,c,y)=(x0,c0,y0) for every positive kappa_X,kappa_Y and nonnegative mu_R",
            "shared_action_value_at_state": 0.0,
            "shared_first_variation_at_state": 0.0,
            "different_second_variations": True,
            "verdict": "zeroth-order source coordinates and a stationary morphology chart do not identify primitive Hessian curvatures",
        },
        "finite_witness": {
            "normalization": {
                "mu_R": mu_r,
                "Q_star": q_star,
                "access_offset_1_plus_lambda_terms": access_offset,
                "role": "dimensionless algebraic witness only; not a physical normalization choice",
            },
            "models": witnesses,
            "same_q_shape_in_every_model": True,
            "all_conditional_gains_distinct": distinct_gains,
            "gain_min": float(np.min(gains)),
            "gain_max": float(np.max(gains)),
        },
        "measurement_covariance_no_go": {
            "physical_object": "H_action=D^2 A_parent on a physically normalized source perturbation direction",
            "measurement_object": "H_like=J^T Sigma_measurement^-1 J or propagated estimator covariance",
            "not_equal_without_bridge": True,
            "missing_bridge": "an independently derived fluctuation/statistical law plus conjugate scale and source-coordinate normalization",
            "v05_monte_carlo_role": "measurement and declared systematic robustness of q_shape_proxy only",
            "v05_or_v07_covariance_can_define_kappa_X_kappa_Y": False,
            "reason": "measurement noise can vary while the physical action is fixed, and physical curvature can vary while the same measurement covariance is retained",
        },
        "minimal_curvature_routes": [
            {
                "route": "parent_action",
                "requirement": "derive the primitive matched-access and source-consensus terms from B_tau^base, the universal seed, stabilized M_tau, and irreducible observer-source relation",
                "claim_level_if_completed": "physical source-side derivation",
            },
            {
                "route": "controlled_source_response",
                "requirement": "independently normalized physical source perturbation with measured first response around the same body-conditioned lane",
                "claim_level_if_completed": "empirical source-curvature estimate under the proved perturbation map",
            },
            {
                "route": "fluctuation_bridge",
                "requirement": "derive a fluctuation law, conjugate scale, equilibrium class, and map from measured fluctuations to the parent source coordinate",
                "claim_level_if_completed": "conditional curvature inference",
            },
        ],
        "forbidden_substitutions": [
            "fit kappa_X or kappa_Y to a velocity or dark-discrepancy residual",
            "identify inverse measurement variance with parent action stiffness",
            "treat the 72 nuisance/systematic scenarios as physical source interventions",
            "use cross-galaxy variation as a local Hessian without proving common coordinates and perturbation equivalence",
        ],
        "inputs": {
            "v07_manifest": str(V07_PATH.relative_to(ROOT)),
            "v07_manifest_sha256": sha256(V07_PATH),
            "v08_manifest": str(V08_PATH.relative_to(ROOT)),
            "v08_manifest_sha256": sha256(V08_PATH),
            "velocity_or_residual_inputs": [],
        },
        "result": {
            "robust_source_shape_retained": True,
            "primitive_curvatures_identified": False,
            "physical_gain_identified": False,
            "measurement_covariance_promoted_to_parent_hessian": False,
            "endpoint_scoring_allowed": False,
            "next_finite_target": "derive one physically normalized parent/source perturbation direction and its primitive second variation",
        },
        "audit_checks": {
            "source_only": True,
            "velocity_or_residual_inputs_empty": True,
            "positive_curvature_witnesses": all(
                row["kappa_X"] > 0.0 and row["kappa_Y"] > 0.0 for row in witnesses
            ),
            "same_stationary_source_state": True,
            "different_effective_gains": distinct_gains,
            "endpoint_scored": False,
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }

    rows = "\n".join(
        "| "
        f"{row['kappa_X']:.1f} | {row['kappa_Y']:.1f} | "
        f"{row['effective_k']:.6f} | {row['conditional_gain']:.6f} | "
        f"{row['conditional_terminal_q']:.6f} |"
        for row in witnesses
    )
    report = f"""# NGC4254 FFL Primitive-Curvature Identifiability Audit v09

**Status:** `{STATUS}`

**Claim boundary:** {CLAIM_BOUNDARY}.

## Constructive No-Go

Center a local FFL action on the same observed stationary source state
`(x0,c0,y0)`:

```text
A = (mu_R/2)||c-c0||^2
  + (kappa_X/2)||(c-c0)-(x-x0)||^2
  + (kappa_Y/2)||(c-c0)-iota(y-y0)||^2.
```

For every positive `kappa_X,kappa_Y`, the action and its first variation vanish
at the same state. Its second variation changes. Therefore the v07 morphology
coordinates and `q_shape_proxy` cannot determine the primitive curvatures.

The following dimensionless countermodels share
`q_shape_proxy={q_source:+.8f}` and the same stationary state. Their
normalization is only an algebraic witness.

| kappa_X | kappa_Y | effective k | conditional gain | conditional terminal q |
|---:|---:|---:|---:|---:|
{rows}

## Covariance Boundary

The v05 Monte Carlo and v07 source-systematic family measure uncertainty and
robustness of the estimator. They are not physical perturbations of the parent
action. A measurement-likelihood curvature such as `J^T Sigma^-1 J` becomes a
physical action Hessian only after an independently derived fluctuation law,
conjugate scale, and source-coordinate normalization. None is currently
available.

## Verdict

The stable `m=2` morphology direction is retained, but its physical stiffness
and terminal gain are not identified. The next finite target is one physically
normalized parent/source perturbation direction and its second variation. It
must come from the parent action, a controlled source response, or a separately
proved fluctuation bridge, not from a rotation residual or measurement noise.
"""
    REPORT_PATH.write_text(report)
    JSON_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(STATUS)
    print(f"same_q={q_source:+.8f} gain_range=[{gains.min():.6f},{gains.max():.6f}]")


if __name__ == "__main__":
    main()
