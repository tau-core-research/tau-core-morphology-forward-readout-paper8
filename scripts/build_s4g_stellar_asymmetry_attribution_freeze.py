#!/usr/bin/env python3
"""Freeze a direct stellar-asymmetry attribution hypothesis before scoring."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
SALT = "tau-core-s4g-stellar-asymmetry-v01"
N_FOLDS = 5

CROSSMATCH_PATH = DATA / "s4g_stellar_asymmetry_crossmatch_v01.csv"
PROVENANCE_PATH = DATA / "s4g_stellar_asymmetry_source_v01.json"
BROAD_SOURCE_PATH = DATA / "s4g_optical_morphology_attribution_source_features_v02.csv"
BROAD_FREEZE_PATH = DATA / "s4g_optical_morphology_attribution_freeze_v02.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fold_for(galaxy: str) -> int:
    digest = hashlib.sha256(f"{SALT}:{galaxy}".encode()).hexdigest()
    return int(digest[:8], 16) % N_FOLDS


def main() -> None:
    for path in (CROSSMATCH_PATH, PROVENANCE_PATH, BROAD_SOURCE_PATH, BROAD_FREEZE_PATH):
        if not path.exists():
            raise FileNotFoundError(path)
    provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
    if provenance["endpoint_access"]:
        raise RuntimeError("S4G asymmetry provenance permits endpoint access")
    broad_freeze = json.loads(BROAD_FREEZE_PATH.read_text(encoding="utf-8"))

    crossmatch = pd.read_csv(CROSSMATCH_PATH)
    usable = crossmatch.loc[
        crossmatch["match_status"].eq("UNIQUE_TWO_CHANNEL_NAME_MATCH")
        & crossmatch["asymmetry_3p6"].notna()
        & crossmatch["asymmetry_4p5"].notna()
    ][["galaxy", "asymmetry_3p6", "asymmetry_error_3p6", "asymmetry_4p5", "asymmetry_error_4p5"]]
    broad = pd.read_csv(BROAD_SOURCE_PATH)
    out = broad.merge(usable, on="galaxy", how="inner", validate="one_to_one")
    out["fold"] = out["galaxy"].astype(str).map(fold_for)
    out["source_family"] = "S4G_2014_ROTATIONAL_STELLAR_ASYMMETRY"
    out["endpoint_blind"] = True
    out["retrospective_lock"] = True
    out = out.sort_values("galaxy").reset_index(drop=True)

    source_path = DATA / "s4g_stellar_asymmetry_attribution_source_v01.csv"
    out.to_csv(source_path, index=False)
    fold_counts = {
        str(key): int(value)
        for key, value in out["fold"].value_counts().sort_index().items()
    }
    channel_correlation = float(
        np.corrcoef(out["asymmetry_3p6"], out["asymmetry_4p5"])[0, 1]
    )
    baseline_features = (
        broad_freeze["baseline_features"]
        + broad_freeze["baseline_missingness_features"]
        + broad_freeze["morphology_features"]
        + broad_freeze["morphology_missingness_features"]
    )

    manifest = {
        "schema": "s4g_stellar_asymmetry_attribution_freeze_v01",
        "status": "SOURCE_ONLY_S4G_STELLAR_ASYMMETRY_FREEZE_READY",
        "source_only": True,
        "endpoint_access": False,
        "retrospective_lock": True,
        "prospective_validation": False,
        "n_rows": int(len(out)),
        "n_folds": N_FOLDS,
        "fold_salt": SALT,
        "fold_counts": fold_counts,
        "baseline_features": baseline_features,
        "asymmetry_features": ["asymmetry_3p6", "asymmetry_4p5"],
        "source_channel_correlation": channel_correlation,
        "source_channel_concordance_gate": channel_correlation >= 0.8,
        "theory_role": "direct_nonaxisymmetric_stellar_structure_coordinate_for_B_W_channel_constraint",
        "frozen_sign": "higher_stellar_asymmetry_predicts_higher_log_tpg_v6_rmse",
        "model": "ridge_linear_fixed_lambda_1",
        "primary_metric": "five_fold_oof_mse_reduction_for_3p6um_asymmetry",
        "replication_metric": "same_frozen_test_for_4p5um_asymmetry",
        "primary_target": "log_tpg_v6_velocity_rmse",
        "control_target": "log_newtonian_baryonic_velocity_rmse",
        "n_permutations": 2000,
        "permutation_seed": 20260712,
        "promotion_rule": (
            "source-channel correlation >=0.8; positive TPG OOF MSE reduction in both bands; "
            "paired-row shuffle p<=0.05 and observed reduction above q95 in both bands; "
            "positive asymmetry coefficient in at least 4/5 folds in both bands; primary "
            "TPG proportional gain exceeds the Newtonian control"
        ),
        "claim_boundary": (
            "retrospective source-family-specific prevalidation; a pass would show only "
            "incremental stellar-asymmetry information, not unique M_tau attribution"
        ),
        "input_sha256": {
            "crossmatch": sha256(CROSSMATCH_PATH),
            "provenance": sha256(PROVENANCE_PATH),
            "broad_source": sha256(BROAD_SOURCE_PATH),
            "broad_freeze": sha256(BROAD_FREEZE_PATH),
        },
        "source_features_sha256": sha256(source_path),
    }
    manifest_path = DATA / "s4g_stellar_asymmetry_attribution_freeze_v01.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / "s4g_stellar_asymmetry_attribution_freeze_v01.md"
    report_path.write_text(
        f"""# S4G Stellar Asymmetry Attribution Freeze v0.1

**Status:** `SOURCE_ONLY_S4G_STELLAR_ASYMMETRY_FREEZE_READY`

This freeze tests one direct structural coordinate, rotational asymmetry `A`,
after controlling for the previously frozen SPARC and broad S4G structural
features. The 3.6 micron measurement is primary; 4.5 micron repeats the same
locked hypothesis as a source-internal replication.

| quantity | value |
| --- | ---: |
| usable galaxies | {len(out)} |
| folds | {N_FOLDS} |
| fold counts | `{fold_counts}` |
| 3.6/4.5 asymmetry correlation | {channel_correlation:.6f} |

No velocity endpoint, residual, RMSE, or score is read by this builder.
""",
        encoding="utf-8",
    )
    print(manifest["status"])
    print(source_path)
    print(manifest_path)
    print(report_path)


if __name__ == "__main__":
    main()
