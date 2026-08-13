#!/usr/bin/env python3
"""Freeze the one-coordinate UNGC Theta1 environment attribution hypothesis."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
SALT = "tau-core-ungc-theta1-environment-v01"
N_FOLDS = 5

SOURCE_FILES = {
    "ungc_crossmatch": DATA / "ungc_sparc_tidal_environment_crossmatch_v01.csv",
    "ungc_provenance": DATA / "ungc_sparc_tidal_environment_source_v01.json",
    "sparc_source": DATA / "external_sparc_master_table.csv",
}

BASELINE_FEATURES = [
    "sparc_t_type",
    "log_distance_mpc",
    "inclination_deg",
    "log_l36",
    "log_rdisk_kpc",
    "log_mhi",
]
ENVIRONMENT_FEATURES = ["theta1"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_log(value: object) -> float:
    if pd.isna(value) or float(value) <= 0:
        return math.nan
    return math.log(float(value))


def fold_for(galaxy: str) -> int:
    digest = hashlib.sha256(f"{SALT}:{galaxy}".encode()).hexdigest()
    return int(digest[:8], 16) % N_FOLDS


def main() -> None:
    for path in SOURCE_FILES.values():
        if not path.exists():
            raise FileNotFoundError(path)
    provenance = json.loads(
        SOURCE_FILES["ungc_provenance"].read_text(encoding="utf-8")
    )
    if provenance["endpoint_access"]:
        raise RuntimeError("UNGC source provenance permits endpoint access")

    crossmatch = pd.read_csv(SOURCE_FILES["ungc_crossmatch"])
    sparc = pd.read_csv(SOURCE_FILES["sparc_source"])
    usable = crossmatch.loc[
        crossmatch["match_status"].eq("UNIQUE_NAME_MATCH")
        & crossmatch["theta1"].notna()
    ].copy()
    merged = usable.merge(
        sparc,
        left_on="galaxy",
        right_on="Galaxy",
        how="inner",
        validate="one_to_one",
    )

    out = pd.DataFrame({"galaxy": merged["galaxy"].astype(str)})
    out["fold"] = out["galaxy"].map(fold_for)
    out["source_family"] = "UNGC_2013_DOMINANT_NEIGHBOR_TIDAL_INDEX"
    out["endpoint_blind"] = True
    out["retrospective_lock"] = True
    out["sparc_t_type"] = merged["T"].astype(float)
    out["log_distance_mpc"] = merged["D_Mpc"].map(safe_log)
    out["inclination_deg"] = merged["Inc_deg"].astype(float)
    out["log_l36"] = merged["L36_1e9Lsun"].map(safe_log)
    out["log_rdisk_kpc"] = merged["Rdisk_kpc"].map(safe_log)
    out["log_mhi"] = merged["MHI_1e9Msun"].map(safe_log)
    out["theta1"] = merged["theta1"].astype(float)
    out["theta1_group_bound"] = (out["theta1"] > 0).astype(int)

    missing_features = []
    for feature in BASELINE_FEATURES:
        if out[feature].isna().any():
            name = f"{feature}__missing"
            out[name] = out[feature].isna().astype(int)
            missing_features.append(name)

    out = out.sort_values("galaxy").reset_index(drop=True)
    source_path = DATA / "ungc_theta1_environment_attribution_source_v01.csv"
    out.to_csv(source_path, index=False)
    fold_counts = {
        str(key): int(value) for key, value in out["fold"].value_counts().sort_index().items()
    }

    manifest = {
        "schema": "ungc_theta1_environment_attribution_freeze_v01",
        "status": "SOURCE_ONLY_THETA1_ENVIRONMENT_FREEZE_READY",
        "source_only": True,
        "endpoint_access": False,
        "retrospective_lock": True,
        "prospective_validation": False,
        "n_rows": int(len(out)),
        "n_folds": N_FOLDS,
        "fold_salt": SALT,
        "fold_counts": fold_counts,
        "baseline_features": BASELINE_FEATURES,
        "baseline_missingness_features": missing_features,
        "environment_features": ENVIRONMENT_FEATURES,
        "theory_role": "environment_channel_to_W_B_coupling_constraint",
        "frozen_sign": "positive_theta1_coefficient_for_log_tpg_v6_rmse",
        "model": "ridge_linear_fixed_lambda_1",
        "primary_metric": "five_fold_oof_mse_reduction",
        "primary_target": "log_tpg_v6_velocity_rmse",
        "control_target": "log_newtonian_baryonic_velocity_rmse",
        "n_permutations": 2000,
        "permutation_seed": 20260711,
        "promotion_rule": (
            "positive OOF MSE reduction; Theta1 shuffle p<=0.05; observed "
            "reduction above shuffle q95; positive Theta1 coefficient in at least "
            "4/5 folds; proportional gain exceeds Newtonian control"
        ),
        "claim_boundary": (
            "retrospective source-family-specific prevalidation only; positive "
            "result would not exclude ordinary tidal astrophysics or prove M_tau"
        ),
        "input_sha256": {name: sha256(path) for name, path in SOURCE_FILES.items()},
        "source_features_sha256": sha256(source_path),
    }
    manifest_path = DATA / "ungc_theta1_environment_attribution_freeze_v01.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / "ungc_theta1_environment_attribution_freeze_v01.md"
    report_path.write_text(
        f"""# UNGC Theta1 Environment Attribution Freeze v0.1

**Status:** `SOURCE_ONLY_THETA1_ENVIRONMENT_FREEZE_READY`

This freeze selects one theory-derived environment coordinate: the UNGC
dominant-neighbor tidal index `Theta1`. Higher values are frozen to predict
higher low-acceleration residual burden through the environment-channel
coupling hypothesis.

| quantity | value |
| --- | ---: |
| usable galaxies | {len(out)} |
| folds | {N_FOLDS} |
| fold counts | `{fold_counts}` |
| baseline features | {len(BASELINE_FEATURES)} |
| environment features | 1 |

The source builder reads no velocity endpoint, residual, model RMSE, or score.
The hypothesis, sign, folds, baseline, model, metrics, controls, and promotion
rule are frozen before the separate endpoint scorer runs.

This is retrospective prevalidation. A positive result would remain compatible
with ordinary tidal astrophysics and would not prove `M_tau`.
""",
        encoding="utf-8",
    )
    print(manifest["status"])
    print(source_path)
    print(manifest_path)
    print(report_path)


if __name__ == "__main__":
    main()
