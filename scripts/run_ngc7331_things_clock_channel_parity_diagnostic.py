#!/usr/bin/env python3
"""Run the frozen NGC7331 THINGS odd/even clock-channel parity diagnostic."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
TAU_ROOT = ROOT.parent
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
FREEZE_PATH = DATA / "ngc7331_things_clock_channel_parity_freeze_v01.json"
CLOCK_ATLAS_PATH = (
    TAU_ROOT
    / "tau-core-theory/source_material/tau_core_foundations/numerical_checks/"
    "tau_core_galactic_clock_channel_reparameterization_v01_galaxies.csv"
)
C_KM_S = 299792.458


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_image(path: Path) -> np.ndarray:
    return np.squeeze(np.asarray(fits.getdata(path), dtype=float))


def weighted_median(values: np.ndarray, weights: np.ndarray) -> float:
    finite = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    values = values[finite]
    weights = weights[finite]
    if len(values) == 0:
        return math.nan
    order = np.argsort(values)
    values = values[order]
    weights = weights[order]
    cutoff = 0.5 * float(weights.sum())
    return float(values[np.searchsorted(np.cumsum(weights), cutoff, side="left")])


def extract_pairs(
    product: str, mom0_path: Path, mom1_path: Path, freeze: dict
) -> pd.DataFrame:
    mom0 = read_image(mom0_path)
    mom1 = read_image(mom1_path) / 1000.0
    if mom0.shape != mom1.shape:
        raise RuntimeError(f"MOM0/MOM1 shape mismatch for {product}")

    y_idx, x_idx = np.indices(mom0.shape)
    x0 = float(freeze["center_x_zero_based"])
    y0 = float(freeze["center_y_zero_based"])
    reflected_x = np.rint(2.0 * x0 - x_idx).astype(int)
    reflected_y = np.rint(2.0 * y0 - y_idx).astype(int)
    inside = (
        (reflected_x >= 0)
        & (reflected_x < mom0.shape[1])
        & (reflected_y >= 0)
        & (reflected_y < mom0.shape[0])
    )
    reflected_x_safe = np.clip(reflected_x, 0, mom0.shape[1] - 1)
    reflected_y_safe = np.clip(reflected_y, 0, mom0.shape[0] - 1)
    mom0_reflected = mom0[reflected_y_safe, reflected_x_safe]
    mom1_reflected = mom1[reflected_y_safe, reflected_x_safe]

    positive = np.where(np.isfinite(mom0), np.maximum(mom0, 0.0), 0.0)
    positive_reflected = np.where(
        np.isfinite(mom0_reflected), np.maximum(mom0_reflected, 0.0), 0.0
    )
    positive_values = positive[positive > 0]
    threshold = 0.20 * float(np.percentile(positive_values, 95))

    dx = x_idx.astype(float) - x0
    dy = y_idx.astype(float) - y0
    angle = math.radians(float(freeze["image_major_axis_deg"]))
    major = np.array([math.cos(angle), math.sin(angle)])
    minor = np.array([-major[1], major[0]])
    u = dx * major[0] + dy * major[1]
    v = dx * minor[0] + dy * minor[1]
    cos_i = math.cos(math.radians(float(freeze["inclination_deg"])))
    deprojected_minor = v / cos_i
    radius_pix = np.hypot(u, deprojected_minor)
    cos_theta = np.divide(
        u,
        radius_pix,
        out=np.zeros_like(u, dtype=float),
        where=radius_pix > 0,
    )

    pair_mask = (
        inside
        & (u > 0)
        & (positive >= threshold)
        & (positive_reflected >= threshold)
        & np.isfinite(mom1)
        & np.isfinite(mom1_reflected)
        & (np.abs(cos_theta) >= float(freeze["major_axis_wedge_abs_cos_theta_min"]))
    )
    weights = np.sqrt(positive[pair_mask] * positive_reflected[pair_mask])
    velocity_positive = mom1[pair_mask]
    velocity_reflected = mom1_reflected[pair_mask]
    odd = 0.5 * (velocity_positive - velocity_reflected)
    even = (
        0.5 * (velocity_positive + velocity_reflected)
        - float(freeze["systemic_velocity_km_s"])
    )
    radius_kpc = radius_pix[pair_mask] * float(freeze["kpc_per_pixel"])
    ring_width = float(freeze["ring_width_kpc"])
    ring_index = np.floor(radius_kpc / ring_width).astype(int)

    return pd.DataFrame(
        {
            "galaxy": "NGC7331",
            "product": product,
            "radius_kpc": radius_kpc,
            "ring_index": ring_index,
            "pair_weight": weights,
            "velocity_positive_side_km_s": velocity_positive,
            "velocity_reflected_side_km_s": velocity_reflected,
            "odd_los_km_s": odd,
            "even_los_km_s": even,
            "absolute_odd_los_km_s": np.abs(odd),
            "absolute_even_los_km_s": np.abs(even),
            "claim_boundary": "single_galaxy_clock_channel_parity_diagnostic",
        }
    )


def ring_profile(pairs: pd.DataFrame, freeze: dict) -> pd.DataFrame:
    rows = []
    ring_width = float(freeze["ring_width_kpc"])
    for (product, ring_index), group in pairs.groupby(["product", "ring_index"]):
        if len(group) < int(freeze["minimum_pairs_per_ring"]):
            continue
        weights = group["pair_weight"].to_numpy(dtype=float)
        odd = group["odd_los_km_s"].to_numpy(dtype=float)
        even = group["even_los_km_s"].to_numpy(dtype=float)
        abs_odd = np.abs(odd)
        abs_even = np.abs(even)
        odd_median = weighted_median(odd, weights)
        even_median = weighted_median(even, weights)
        abs_odd_median = weighted_median(abs_odd, weights)
        abs_even_median = weighted_median(abs_even, weights)
        rows.append(
            {
                "galaxy": "NGC7331",
                "product": product,
                "ring_index": int(ring_index),
                "radius_mid_kpc": (int(ring_index) + 0.5) * ring_width,
                "n_pairs": int(len(group)),
                "odd_los_weighted_median_km_s": odd_median,
                "even_los_weighted_median_km_s": even_median,
                "absolute_odd_weighted_median_km_s": abs_odd_median,
                "absolute_even_weighted_median_km_s": abs_even_median,
                "absolute_even_over_odd": abs_even_median
                / max(abs_odd_median, 1.0e-12),
                "source_outer_region": (int(ring_index) + 0.5) * ring_width
                >= float(freeze["source_outer_region_start_kpc"]),
                "claim_boundary": "single_galaxy_clock_channel_parity_diagnostic",
            }
        )
    return pd.DataFrame(rows).sort_values(["product", "ring_index"]).reset_index(drop=True)


def summarize_product(profile: pd.DataFrame, product: str) -> dict[str, object]:
    subset = profile.loc[profile["product"].eq(product)]
    outer = subset.loc[subset["source_outer_region"]]
    return {
        "n_rings": int(len(subset)),
        "n_outer_rings": int(len(outer)),
        "all_median_abs_even_km_s": float(
            subset["absolute_even_weighted_median_km_s"].median()
        ),
        "all_median_abs_odd_km_s": float(
            subset["absolute_odd_weighted_median_km_s"].median()
        ),
        "all_median_even_over_odd": float(subset["absolute_even_over_odd"].median()),
        "outer_median_abs_even_km_s": float(
            outer["absolute_even_weighted_median_km_s"].median()
        ),
        "outer_median_abs_odd_km_s": float(
            outer["absolute_odd_weighted_median_km_s"].median()
        ),
        "outer_median_even_over_odd": float(outer["absolute_even_over_odd"].median()),
        "outer_max_even_over_odd": float(outer["absolute_even_over_odd"].max()),
    }


def main() -> None:
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    if freeze["status"] != "SOURCE_FROZEN_THINGS_CLOCK_CHANNEL_PARITY_DIAGNOSTIC_READY":
        raise RuntimeError("THINGS clock-channel parity freeze is not ready")
    if not freeze["source_only"] or freeze["endpoint_access"]:
        raise RuntimeError("THINGS parity source/endpoint boundary failed")

    pairs = []
    for product, mom0_id, mom1_id in (
        ("NATURAL", "NA_MOM0", "NA_MOM1"),
        ("ROBUST", "RO_MOM0", "RO_MOM1"),
    ):
        mom0_path = Path(freeze["products"][mom0_id]["path"])
        mom1_path = Path(freeze["products"][mom1_id]["path"])
        for product_id, path in ((mom0_id, mom0_path), (mom1_id, mom1_path)):
            if sha256(path) != freeze["products"][product_id]["sha256"]:
                raise RuntimeError(f"Frozen THINGS hash mismatch for {product_id}")
        pairs.append(extract_pairs(product, mom0_path, mom1_path, freeze))
    pair_frame = pd.concat(pairs, ignore_index=True)
    profile = ring_profile(pair_frame, freeze)

    product_metrics = {
        product: summarize_product(profile, product) for product in ("NATURAL", "ROBUST")
    }
    atlas = pd.read_csv(CLOCK_ATLAS_PATH)
    galaxy_clock = atlas.loc[atlas["galaxy"].eq("NGC7331")].iloc[0]
    outer_clock_factor = float(galaxy_clock["outer3_required_clock_factor_median"])
    required_multiplier = 1.0 / outer_clock_factor
    simple_multiplier_even_shift = C_KM_S * (required_multiplier - 1.0)
    observed_outer_even_max = max(
        product_metrics[product]["outer_median_abs_even_km_s"]
        for product in product_metrics
    )
    predicted_to_observed_even_ratio = simple_multiplier_even_shift / max(
        observed_outer_even_max, 1.0e-12
    )
    representative_outer_odd = float(
        np.mean(
            [
                product_metrics[product]["outer_median_abs_odd_km_s"]
                for product in product_metrics
            ]
        )
    )
    beta_obs = representative_outer_odd / C_KM_S
    beta_dyn = outer_clock_factor * beta_obs
    required_differential_path_delta = (beta_obs - beta_dyn) / (
        1.0 - beta_obs * beta_dyn
    )

    pair_path = DATA / "ngc7331_things_clock_channel_parity_pairs_v01.csv"
    profile_path = DATA / "ngc7331_things_clock_channel_parity_profile_v01.csv"
    pair_frame.to_csv(pair_path, index=False)
    profile.to_csv(profile_path, index=False)

    status = "SIMPLE_COMMON_MULTIPLICATIVE_CLOCK_CHANNEL_INCOMPATIBLE_SINGLE_GALAXY"
    result = {
        "schema": "ngc7331_things_clock_channel_parity_v01",
        "status": status,
        "galaxy": "NGC7331",
        "claim_level": "single_galaxy_velocity_field_diagnostic",
        "product_metrics": product_metrics,
        "outer_clock_factor_from_sparc_diagnostic": outer_clock_factor,
        "required_simple_spectral_multiplier": required_multiplier,
        "required_simple_multiplier_even_shift_km_s": simple_multiplier_even_shift,
        "observed_outer_even_median_max_across_products_km_s": observed_outer_even_max,
        "predicted_to_observed_even_ratio": predicted_to_observed_even_ratio,
        "differential_observer_path_channel": {
            "model": "A_plus=A_bar*(1+delta), A_minus=A_bar*(1-delta)",
            "parity_law": "beta_inferred=(beta_dynamic+delta)/(1+delta*beta_dynamic)",
            "representative_outer_odd_km_s": representative_outer_odd,
            "beta_observed": beta_obs,
            "beta_dynamic_from_sparc_ratio": beta_dyn,
            "required_delta": required_differential_path_delta,
            "required_fractional_side_to_side_difference": (
                2.0 * required_differential_path_delta
            ),
            "status": "KINEMATIC_SCALE_ESTIMATE_NOT_PATH_CHANNEL_TEST",
        },
        "model_scope": (
            "rules out only a common multiplicative factor in 1+z that is large enough "
            "to supply the outer SPARC velocity scaling; it does not test a differential "
            "observer-to-emission-point light-cone channel, nonlinear systemic-anchored "
            "map, tracer-dependent channel, or dynamics-changing channel"
        ),
        "freeze_sha256": sha256(FREEZE_PATH),
        "clock_atlas_sha256": sha256(CLOCK_ATLAS_PATH),
        "outputs": {"pairs": pair_path.name, "profile": profile_path.name},
        "claim_boundary": (
            "single-galaxy diagnostic; not a general time-channel rejection, quantum "
            "channel test, dark-matter falsification, or Tau Core validation"
        ),
    }
    result_path = DATA / "ngc7331_things_clock_channel_parity_v01.json"
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / "ngc7331_things_clock_channel_parity_v01.md"
    report_path.write_text(
        f"""# NGC7331 THINGS Clock-Channel Parity Diagnostic v0.1

**Status:** `{status}`

## Odd/Even Velocity-Field Result

| product | rings | outer rings | outer median abs odd (km/s) | outer median abs even (km/s) | outer even/odd |
| --- | ---: | ---: | ---: | ---: | ---: |
| natural | {product_metrics['NATURAL']['n_rings']} | {product_metrics['NATURAL']['n_outer_rings']} | {product_metrics['NATURAL']['outer_median_abs_odd_km_s']:.6f} | {product_metrics['NATURAL']['outer_median_abs_even_km_s']:.6f} | {product_metrics['NATURAL']['outer_median_even_over_odd']:.6f} |
| robust | {product_metrics['ROBUST']['n_rings']} | {product_metrics['ROBUST']['n_outer_rings']} | {product_metrics['ROBUST']['outer_median_abs_odd_km_s']:.6f} | {product_metrics['ROBUST']['outer_median_abs_even_km_s']:.6f} | {product_metrics['ROBUST']['outer_median_even_over_odd']:.6f} |

## Simple Multiplicative Clock Test

The outer SPARC diagnostic requires `N_ch={outer_clock_factor:.6f}`, equivalent
to multiplying the inferred odd velocity by `{required_multiplier:.6f}`. If
that factor multiplies the full spectral redshift `1+z`, it also predicts a
common even shift of approximately `{simple_multiplier_even_shift:.3f} km/s`.
The larger observed outer median even shift across the two THINGS products is
only `{observed_outer_even_max:.6f} km/s`, a ratio of
`{predicted_to_observed_even_ratio:.3e}`.

Thus a common multiplicative spectral-clock factor large enough to explain the
outer velocity discrepancy is kinematically incompatible with this frozen
single-galaxy velocity field.

## Differential Observer-To-Point Path Channel

The older Tau Core hypothesis assigns a distinct observer-to-emission-point
path object to each disk side. Parameterize its first parity component by

```text
A_plus  = A_bar (1 + delta)
A_minus = A_bar (1 - delta).
```

Then

```text
beta_inferred = (beta_dynamic + delta) / (1 + delta beta_dynamic).
```

Using the mean of the two outer odd summaries
`{representative_outer_odd:.6f} km/s` and the cross-packet SPARC ratio gives
`delta_req={required_differential_path_delta:.6e}`, corresponding to a
fractional side-to-side channel difference of
`{2.0 * required_differential_path_delta:.6e}`.

This is only a kinematic scale estimate. No path kernel has been fitted or
tested. It demonstrates that the common-factor rejection does not reject the
differential observer-position/light-cone channel class.

## Boundary

This rejects only the common full-`1+z` multiplier. A differential
observer-to-point light-cone channel, nonlinear map anchored at the systemic
redshift, tracer-dependent quantum-access map, or a channel that changes
dynamics rather than spectral readout requires a different frozen formula and
different controls.
""",
        encoding="utf-8",
    )
    print(status)
    print(result_path)
    print(report_path)
    print(profile_path)
    print(pair_path)


if __name__ == "__main__":
    main()
