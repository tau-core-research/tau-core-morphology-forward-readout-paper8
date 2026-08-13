#!/usr/bin/env python3
"""Freeze a continuous radial body-subspace projection before new endpoints."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/phangs_radial_body_projection_preregistration_v01.md"
ATLAS = DATA / "phangs_source_certified_morphology_nuisance_atlas_v02.csv"
N_ZONES = 5


def split_role(galaxy: str) -> str:
    bucket = int(hashlib.sha256(galaxy.encode("ascii")).hexdigest()[:8], 16) % 2
    return "pipeline_development_no_claim" if bucket == 0 else "confirmatory_untouched"


def main() -> None:
    atlas = pd.read_csv(ATLAS)
    eligible = atlas[
        (~atlas.endpoint_opened)
        & atlas.geometry_pass
        & atlas.phangs_morphology_validated
        & atlas.s4g_model_components.notna()
    ].copy()
    eligible["split_role"] = eligible.galaxy.map(split_role)
    eligible["split_hash_rule"] = "uint32(sha256(galaxy)[0:8]) mod 2"
    eligible["velocity_contrast_opened"] = False
    eligible["rotation_residual_used"] = False
    eligible = eligible[[
        "galaxy", "split_role", "split_hash_rule", "geometry_pass",
        "phangs_co_bar_class", "phangs_spiral_class", "s4g_model_components",
        "velocity_contrast_opened", "rotation_residual_used",
    ]].sort_values("galaxy")
    development = eligible.loc[
        eligible.split_role.eq("pipeline_development_no_claim"), "galaxy"
    ].tolist()
    confirmatory = eligible.loc[
        eligible.split_role.eq("confirmatory_untouched"), "galaxy"
    ].tolist()
    result = {
        "schema": "phangs_radial_body_projection_preregistration_v01",
        "status": "HIGHER_DIMENSIONAL_BODY_PROJECTION_ENDPOINTS_FROZEN_UNOPENED",
        "eligible_population": eligible.galaxy.tolist(),
        "pipeline_development_no_claim": development,
        "confirmatory_untouched": confirmatory,
        "radial_zones": N_ZONES,
        "terminal_vector": (
            "five-zone CO-minus-Halpha velocity coefficients ordered as "
            "{m1_cos,m1_sin,m2_cos,m2_sin} per zone; dimension 20"
        ),
        "source_body_profiles": [
            "S4G 3.6um stellar m1 complex radial profile",
            "radial finite difference of stellar m1 profile",
            "S4G 3.6um stellar m2 complex radial profile",
            "radial finite difference of stellar m2 profile",
            "PHANGS CO moment-0 m1 complex radial profile",
            "radial finite difference of CO moment-0 m1 profile",
            "PHANGS CO moment-0 m2 complex radial profile",
            "radial finite difference of CO moment-0 m2 profile",
        ],
        "body_nuisance_matrix": (
            "S_B is the 20-by-at-most-8 real matrix embedding the frozen complex source profiles "
            "and radial differences into their matching m1/m2 terminal coordinates"
        ),
        "covariance_weighted_projection": (
            "P_perp=I-S_B (S_B^T Sigma^-1 S_B)^+ S_B^T Sigma^-1"
        ),
        "primary_statistic": (
            "Q=(P_perp y)^T (P_perp Sigma P_perp^T)^+ (P_perp y), "
            "dof=rank(P_perp Sigma P_perp^T)"
        ),
        "rank_gate": "rank(P_perp)>=4 in every confirmatory galaxy; otherwise preserve non-identifiability",
        "primary_null": "all confirmatory body-orthogonal projected coefficients are zero",
        "primary_threshold": "global confirmatory chi-square p<0.01",
        "replication_threshold": "at least 3 of 4 confirmatory galaxies have individual p<0.05",
        "controls": [
            "radially permute each source profile before constructing S_B",
            "rotate each complex source phase by pi/2 without changing amplitude",
            "repeat after removing either stellar or CO morphology block",
        ],
        "promotion_rule": (
            "primary and replication thresholds, rank gate, both geometric controls, and positive grouped "
            "holdout gain over a frozen body-only predictor are all required"
        ),
        "development_boundary": (
            "development galaxies may validate WCS, beam matching and numerical conditioning only; "
            "they cannot change zones, profiles, projection, thresholds, controls or confirmatory membership"
        ),
        "construction_uses_velocity_contrast": False,
        "construction_uses_rotation_residual": False,
        "endpoint_opened": False,
        "claim_boundary": (
            "source-frozen higher-dimensional inverse-readout test design; not a detected channel, "
            "not a parent-derived law, and not time, quantum or dark-sector evidence"
        ),
    }
    eligible.to_csv(DATA / "phangs_radial_body_projection_preregistration_v01.csv", index=False)
    (DATA / "phangs_radial_body_projection_preregistration_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    REPORT.write_text(
        "# PHANGS radial body-projection preregistration v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The untouched confirmatory cohort is `{', '.join(confirmatory)}`. The development-only "
        f"cohort is `{', '.join(development)}`. Membership follows the frozen SHA-256 rule.\n\n"
        "The terminal is a 20-dimensional five-zone `m1+m2` velocity-contrast vector. A continuous "
        "stellar-plus-CO morphology matrix carries radial amplitudes, phases and first radial "
        "differences. The primary statistic tests only the covariance-weighted orthogonal complement "
        "of that complete source body matrix. No new velocity contrast has been opened.\n",
        encoding="utf-8",
    )
    print(result["status"], confirmatory)


if __name__ == "__main__":
    main()
