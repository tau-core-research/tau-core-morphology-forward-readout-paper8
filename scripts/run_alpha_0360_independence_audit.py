#!/usr/bin/env python3
"""Audit independent and inherited appearances of the TPG alpha scale."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/alpha_0360_independence_audit.md"
A0 = 1.2e-10
KPC_M = 3.085677581491367e19
SEED = 20260711


def fit_alpha(frame: pd.DataFrame) -> float:
    return float((frame.basis * frame.target).sum() / frame.basis.pow(2).sum())


def load_etg() -> pd.DataFrame:
    rows = []
    path = ROOT / "data/external/catalogs/atlas3d_etg_lelli2017/etg_lelli2017.txt"
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        token = line.split()
        rows.extend([
            {"galaxy": token[0], "log_abar": float(token[5]), "log_aobs": float(token[1])},
            {"galaxy": token[0], "log_abar": float(token[7]), "log_aobs": float(token[3])},
        ])
    return pd.DataFrame(rows)


def fit_etg_alpha(frame: pd.DataFrame) -> float:
    abar = np.power(10.0, frame.log_abar.to_numpy())
    log_aobs = frame.log_aobs.to_numpy()
    def objective(alpha: float) -> float:
        prediction = np.log10(abar * np.power(1.0 + alpha * np.log1p(A0 / abar), 2.0))
        return float(np.mean((prediction - log_aobs) ** 2))
    return float(minimize_scalar(objective, bounds=(0.0, 2.0), method="bounded").x)


def main() -> None:
    points = pd.read_csv(DATA / "little_things_prospective_kernel_scored_points_v01.csv")
    points = points[points.prospective_name_freeze & (points.inclination_deg >= 40)].copy()
    acceleration = (points.v_baryon_newton_km_s.clip(lower=1.0e-6) * 1000.0) ** 2 / (
        points.r.clip(lower=1.0e-6) * KPC_M
    )
    points["basis"] = points.v_baryon_newton_km_s * np.log1p(A0 / acceleration)
    points["target"] = points.velocity_km_s - points.v_baryon_newton_km_s
    external_alpha = fit_alpha(points)
    groups = {galaxy: group for galaxy, group in points.groupby("galaxy")}
    galaxies = np.asarray(sorted(groups))
    rng = np.random.default_rng(SEED)
    draws = []
    for _ in range(20_000):
        sample = rng.choice(galaxies, len(galaxies), replace=True)
        numerator = sum((groups[name].basis * groups[name].target).sum() for name in sample)
        denominator = sum(groups[name].basis.pow(2).sum() for name in sample)
        draws.append(numerator / denominator)
    interval = np.quantile(draws, [0.025, 0.5, 0.975]).tolist()

    etg = load_etg()
    etg_alpha = fit_etg_alpha(etg)
    etg_groups = {galaxy: group for galaxy, group in etg.groupby("galaxy")}
    etg_names = np.asarray(sorted(etg_groups))
    etg_draws = []
    for _ in range(20_000):
        sample = rng.choice(etg_names, len(etg_names), replace=True)
        etg_draws.append(fit_etg_alpha(pd.concat([etg_groups[name] for name in sample])))
    etg_interval = np.quantile(etg_draws, [0.025, 0.5, 0.975]).tolist()

    ledger = pd.DataFrame([
        ["SPARC global fit", 0.360, "SPARC rotation curves", "primary empirical estimate", "one precise empirical origin"],
        ["SPARC CV and spiral subset", 0.360, "same SPARC parent sample", "robustness, not independent", "shared galaxies and baryonic assumptions"],
        ["LITTLE THINGS external fit", external_alpha, "Oh et al. dwarf rotation curves", "partially independent empirical estimate", "vector-extracted baryonic components; broad interval"],
        ["Atlas3D ETG external fit", etg_alpha, "Lelli et al. early-type accelerations", "independent empirical estimate", "32 points; pressure-support and anisotropy caveats"],
        ["2 a0/(c H0), Planck", 0.366, "empirical a0 plus Planck H0", "partially independent cosmological candidate", "shares empirical a0; factor 2 unproved"],
        ["Omega_Lambda-Omega_m", 0.3684, "Planck base-LCDM", "correlated cosmological candidate", "not independent of Planck cosmology route"],
        ["2/pi^(3/2)", 0.3592, "mathematical constants", "post-hoc closed-form hit", "best of 747; look-elsewhere dominated"],
        ["1/(4 ln 2)", 0.3607, "mathematical constants", "post-hoc curated hit", "best-near hit in earlier curated scan"],
        ["9/25", 0.3600, "small integers", "numerology control", "exact but no mechanism"],
        ["DTL capacity normalization", np.nan, "Tau/DTL source architecture", "unresolved theoretical route", "does not yet output 0.360 independently"],
    ], columns=["route", "value", "input_provenance", "independence_class", "caveat"])
    ledger.to_csv(DATA / "alpha_0360_independence_ledger.csv", index=False)
    result = {
        "schema": "alpha_0360_independence_audit",
        "status": "MULTIPLE_APPEARANCES_CONFIRMED_ONLY_ONE_PRECISE_EMPIRICAL_ORIGIN",
        "little_things": {
            "n_galaxies": len(galaxies), "n_points": len(points),
            "alpha_hat": external_alpha,
            "galaxy_bootstrap_95_interval": interval,
            "canonical_0_360_inside_interval": interval[0] <= 0.360 <= interval[2],
        },
        "atlas3d_etg": {
            "n_galaxies": len(etg_names), "n_points": len(etg), "alpha_hat": etg_alpha,
            "galaxy_bootstrap_95_interval": etg_interval,
            "canonical_0_360_inside_interval": etg_interval[0] <= 0.360 <= etg_interval[2],
        },
        "counts": {
            "precise_independent_empirical_determinations": 1,
            "independent_or_partially_independent_external_empirical_checks": 2,
            "cosmological_candidate_family": 1,
            "posthoc_mathematical_coincidence_family": 1,
            "completed_first_principles_derivations": 0,
        },
        "claim_boundary": (
            "multiple numerical appearances are real, but correlated inputs, inherited constants, "
            "and look-elsewhere searches prevent counting them as independent confirmations"
        ),
    }
    (DATA / "alpha_0360_independence_audit.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    REPORT.write_text(
        "# Alpha 0.360 independence audit\n\n"
        f"Status: `{result['status']}`\n\n"
        "The value near 0.360 genuinely appears in several constructions, but they do not all "
        "supply independent evidence. SPARC is the only current precise empirical determination. "
        "SPARC cross-validation and subsamples test stability of the same source rather than "
        "creating new origins. The Planck ratios form one correlated cosmological candidate family. "
        "Closed-form matches are post-hoc searches with a look-elsewhere penalty.\n\n"
        f"On the independent LITTLE THINGS primary lane, direct refitting gives "
        f"`alpha_hat={external_alpha:.3f}` with galaxy-bootstrap 95% interval "
        f"`[{interval[0]:.3f}, {interval[2]:.3f}]`. Canonical 0.360 is compatible but not sharply "
        "recovered. The independent Atlas3D ETG estimate gives "
        f"`alpha_hat={etg_alpha:.3f}` with interval "
        f"`[{etg_interval[0]:.3f}, {etg_interval[2]:.3f}]`; canonical 0.360 lies at its lower edge.\n\n"
        "Therefore the correct status is multiple suggestive appearances, one precise empirical "
        "origin, one broad external compatibility check, and zero completed first-principles "
        "derivations.\n",
        encoding="utf-8",
    )
    print(result["status"], external_alpha)


if __name__ == "__main__":
    main()
