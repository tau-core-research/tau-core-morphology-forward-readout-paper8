#!/usr/bin/env python3
"""Score the frozen v02 kernel through a measured lightcone-capacity operator."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import run_theory_completed_scale_tail_kernel_v02 as v02


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/little_things_lightcone_capacity_score_v01.md"
THRESHOLDS = (0.01, 0.05, 0.10)
PRIMARY_THRESHOLD = 0.05


def gaussian_measurement_operator(radius: np.ndarray, beam_fwhm_kpc: float) -> np.ndarray:
    """Return the row-normalized radial response implied by the H I beam."""
    sigma = max(beam_fwhm_kpc / 2.354820045, 1.0e-12)
    delta = radius[:, None] - radius[None, :]
    weights = np.exp(-0.5 * (delta / sigma) ** 2)
    return weights / weights.sum(axis=1, keepdims=True)


def finite_capacity_operator(operator: np.ndarray, relative_threshold: float) -> tuple[np.ndarray, int, np.ndarray]:
    """Keep only measurement modes above a fixed relative singular threshold."""
    left, singular, right = np.linalg.svd(operator, full_matrices=False)
    keep = singular >= relative_threshold * singular[0]
    bounded = singular * (singular / (singular + relative_threshold * singular[0]))
    effective = (left[:, keep] * bounded[keep]) @ right[keep]
    return effective, int(keep.sum()), singular / singular[0]


def rmse(observed: pd.Series, predicted: pd.Series) -> float:
    return float(np.sqrt(np.mean((observed - predicted) ** 2)))


def summarize(scores: pd.DataFrame, prediction: str) -> dict:
    delta_tpg = scores[prediction] - scores.rmse_tpg_v6
    delta_v02 = scores[prediction] - scores.rmse_v02
    return {
        "n_galaxies": int(len(scores)),
        "n_points": int(scores.n_points.sum()),
        "mean_rmse_km_s": float(scores[prediction].mean()),
        "mean_minus_tpg_km_s": float(delta_tpg.mean()),
        "mean_minus_v02_km_s": float(delta_v02.mean()),
        "beats_tpg_fraction": float((delta_tpg < 0).mean()),
        "beats_v02_fraction": float((delta_v02 < 0).mean()),
    }


def main() -> None:
    v02_result = json.loads(
        (DATA / "theory_completed_scale_tail_kernel_v02.json").read_text(encoding="utf-8")
    )
    eta = float(v02_result["eta"])
    points = pd.read_csv(DATA / "little_things_prospective_kernel_scored_points_v01.csv")
    audit = pd.read_csv(DATA / "little_things_baryonic_vector_extraction_audit_v01.csv")
    catalog = pd.read_csv(DATA / "little_things_prospective_scoring_freeze_v01.csv")
    allowed = set(audit.loc[audit.status.eq("pass"), "galaxy"])
    points = points[points.galaxy.isin(allowed) & points.prospective_name_freeze].copy()
    points = v02.add_channel_shape(points)
    points["v_v02"] = points.v_tpg_v6 * np.exp(0.5 * eta * points.phi_tail_bounded)
    source_fields = catalog[["galaxy", "distance_mpc", "rmax_over_hi_beam", "hi_beam_fwhm_kpc"]]
    points = points.merge(source_fields, on="galaxy", how="left", validate="many_to_one")
    if points.hi_beam_fwhm_kpc.isna().any():
        raise RuntimeError("Missing source-native H I beam scale")

    diagnostics = []
    for galaxy, indices in points.groupby("galaxy", sort=True).groups.items():
        sub = points.loc[indices].sort_values("r")
        measurement = gaussian_measurement_operator(sub.r.to_numpy(), float(sub.hi_beam_fwhm_kpc.iloc[0]))
        for threshold in THRESHOLDS:
            channel, effective_rank, spectrum = finite_capacity_operator(measurement, threshold)
            transported_u = np.clip(channel @ sub.u_tail_source_normalized.to_numpy(), 0.0, None)
            phi = transported_u / (1.0 + transported_u)
            prediction = sub.v_tpg_v6.to_numpy() * np.exp(0.5 * eta * phi)
            label = f"v_capacity_{str(threshold).replace('.', 'p')}"
            points.loc[sub.index, label] = prediction
            diagnostics.append({
                "galaxy": galaxy,
                "capacity_threshold": threshold,
                "n_sampled_modes": len(sub),
                "effective_rank": effective_rank,
                "effective_rank_fraction": effective_rank / len(sub),
                "largest_suppressed_relative_singular_value": float(
                    spectrum[effective_rank] if effective_rank < len(spectrum) else 0.0
                ),
            })

    rows = []
    for galaxy, sub in points.groupby("galaxy", sort=True):
        row = {
            "galaxy": galaxy,
            "inclination_deg": float(sub.inclination_deg.iloc[0]),
            "distance_mpc": float(sub.distance_mpc.iloc[0]),
            "hi_beam_fwhm_kpc": float(sub.hi_beam_fwhm_kpc.iloc[0]),
            "n_points": len(sub),
            "rmse_tpg_v6": rmse(sub.velocity_km_s, sub.v_tpg_v6),
            "rmse_mond": rmse(sub.velocity_km_s, sub.v_mond),
            "rmse_v02": rmse(sub.velocity_km_s, sub.v_v02),
        }
        for threshold in THRESHOLDS:
            label = f"v_capacity_{str(threshold).replace('.', 'p')}"
            row[f"rmse_capacity_{str(threshold).replace('.', 'p')}"] = rmse(sub.velocity_km_s, sub[label])
        rows.append(row)
    scores = pd.DataFrame(rows)
    primary = scores[scores.inclination_deg >= 40].copy()
    sensitivity = {
        str(threshold): summarize(primary, f"rmse_capacity_{str(threshold).replace('.', 'p')}")
        for threshold in THRESHOLDS
    }
    diagnostics_frame = pd.DataFrame(diagnostics)
    primary_diag = diagnostics_frame[
        diagnostics_frame.galaxy.isin(primary.galaxy) &
        diagnostics_frame.capacity_threshold.eq(PRIMARY_THRESHOLD)
    ]
    result = {
        "schema": "little_things_lightcone_capacity_score_v01",
        "status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
        "operator_order": "K_tail -> H_I beam lightcone geometry -> finite spectral capacity -> bounded activation -> frozen TPG carrier",
        "formula": "W_ij~exp[-(R_i-R_j)^2/(2 sigma_beam^2)]; C_lambda=U diag[s A(s/lambda) 1(s/lambda>=1)] V^T; phi=C_lambda[u]/(1+C_lambda[u]); v^2=v_TPG^2 exp(eta phi)",
        "eta": eta,
        "eta_source": "frozen historical-SPARC v02 value; no LITTLE THINGS refit",
        "capacity_relative_thresholds": list(THRESHOLDS),
        "primary_reporting_threshold": PRIMARY_THRESHOLD,
        "primary": sensitivity[str(PRIMARY_THRESHOLD)],
        "threshold_sensitivity": sensitivity,
        "primary_capacity": {
            "mean_effective_rank": float(primary_diag.effective_rank.mean()),
            "mean_effective_rank_fraction": float(primary_diag.effective_rank_fraction.mean()),
            "min_effective_rank": int(primary_diag.effective_rank.min()),
            "max_effective_rank": int(primary_diag.effective_rank.max()),
            "all_sampled_modes_retained": bool(
                (primary_diag.effective_rank == primary_diag.n_sampled_modes).all()
            ),
        },
        "distance_enters_via": "source-native physical H I beam scale Rmax/(Rmax/HI), equivalent to angular resolution mapped across observer-source distance",
        "raw_null_propagation_claimed_compact": False,
        "measured_channel_finite_dimensional": True,
        "physical_time_operator_identified": False,
        "quantum_operator_identified": False,
        "capacity_result": "finite sampled channel, but no resolved spectral bottleneck at relative thresholds 0.01-0.10",
        "claim_boundary": "opened-sample sensitivity test of a measured lightcone-capacity completion; not a prospective endpoint, intrinsic null-cone law, time detection, quantum detection, or parent-level derivation",
    }
    scores.to_csv(DATA / "little_things_lightcone_capacity_scores_by_galaxy_v01.csv", index=False)
    points.to_csv(DATA / "little_things_lightcone_capacity_scored_points_v01.csv", index=False)
    diagnostics_frame.to_csv(DATA / "little_things_lightcone_capacity_modes_v01.csv", index=False)
    (DATA / "little_things_lightcone_capacity_score_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    p = result["primary"]
    REPORT.write_text(
        "# LITTLE THINGS measured lightcone-capacity score\n\n"
        f"Status: `{result['status']}`\n\n"
        "This replay inserts the source-native physical H I beam response and a finite "
        "singular-mode capacity operator before the bounded channel activation. The v02 "
        f"historical coefficient remains frozen at `eta={eta:.12g}`.\n\n"
        f"At the predeclared primary relative threshold `{PRIMARY_THRESHOLD}`, the 14-galaxy "
        f"lane has mean RMSE `{p['mean_rmse_km_s']:.3f} km/s`, mean delta versus TPG "
        f"`{p['mean_minus_tpg_km_s']:+.3f} km/s`, and mean delta versus raw v02 "
        f"`{p['mean_minus_v02_km_s']:+.3f} km/s`. It beats TPG in "
        f"`{p['beats_tpg_fraction']:.3f}` and raw v02 in `{p['beats_v02_fraction']:.3f}` "
        "of galaxies.\n\n"
        "All sampled radial modes remain above the tested relative thresholds. Thus this "
        "dataset realizes a finite measured channel but does not resolve a spectral capacity "
        "bottleneck; the operator only weakly attenuates the modes.\n\n"
        "The threshold sweep is retained in the JSON. This is an opened-sample sensitivity "
        "diagnostic. It tests whether the new measured-channel structure changes scoring; it "
        "does not identify an intrinsic lightcone, time, quantum, or parent operator.\n",
        encoding="utf-8",
    )
    print(result["status"], json.dumps(result["primary"], sort_keys=True))


if __name__ == "__main__":
    main()
