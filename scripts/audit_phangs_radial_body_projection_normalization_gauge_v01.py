#!/usr/bin/env python3
"""Audit recovery of raw source-column norms behind the frozen body matrix."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
PROFILES = DATA / "phangs_radial_body_projection_development_terminal_edge_profiles_v01.csv"
MATRICES = DATA / "phangs_radial_body_projection_development_terminal_edge_matrices_v01.npz"
OUT = DATA / "phangs_radial_body_projection_normalization_gauge_v01.json"
REPORT = ROOT / "reports" / "phangs_radial_body_projection_normalization_gauge_v01.md"

FAMILIES = ("stellar_m1", "stellar_m2", "co_m1", "co_m2")


def raw_embed(profile: np.ndarray, mode: int) -> np.ndarray:
    vector = np.zeros(20, dtype=float)
    offset = 0 if mode == 1 else 2
    for zone, value in enumerate(profile):
        vector[4 * zone + offset] = value.real
        vector[4 * zone + offset + 1] = value.imag
    return vector


def main() -> None:
    rows = pd.read_csv(PROFILES)
    frozen = np.load(MATRICES)
    results: dict[str, dict[str, object]] = {}
    all_checks = True

    for galaxy in frozen.files:
        subset = rows.loc[rows.galaxy.eq(galaxy)]
        profiles: dict[str, np.ndarray] = {}
        for family in FAMILIES:
            family_rows = subset.loc[subset.profile.eq(family)].sort_values("zone")
            if len(family_rows) != 5:
                raise RuntimeError(f"{galaxy} {family} does not have five radial zones")
            profiles[family] = family_rows.real.to_numpy() + 1j * family_rows.imag.to_numpy()

        raw_columns = []
        labels = []
        for family in FAMILIES:
            mode = 1 if family.endswith("m1") else 2
            profile = profiles[family]
            raw_columns.extend((raw_embed(profile, mode), raw_embed(np.gradient(profile), mode)))
            labels.extend((family, f"{family}_radial_difference"))

        raw_matrix = np.column_stack(raw_columns)
        norms = np.linalg.norm(raw_matrix, axis=0)
        if np.any(norms <= 1.0e-12):
            raise RuntimeError(f"{galaxy} contains a null raw source column")
        normalized = raw_matrix / norms
        frozen_matrix = frozen[galaxy]
        source_gains = np.arange(1.0, 9.0)
        normalized_coefficients = norms * source_gains
        raw_terminal = raw_matrix @ source_gains
        normalized_terminal = frozen_matrix @ normalized_coefficients
        checks = {
            "all_raw_norms_positive": bool(np.all(norms > 1.0e-12)),
            "normalized_matrix_reconstructed": bool(
                np.allclose(normalized, frozen_matrix, atol=1.0e-12)
            ),
            "normalization_coordinate_identity": bool(
                np.allclose(raw_terminal, normalized_terminal, atol=1.0e-12)
            ),
        }
        all_checks = all_checks and all(checks.values())
        results[galaxy] = {
            "column_labels": labels,
            "raw_column_norms": norms.tolist(),
            "minimum_raw_column_norm": float(np.min(norms)),
            "maximum_raw_column_norm": float(np.max(norms)),
            "matrix_reconstruction_error": float(np.linalg.norm(normalized - frozen_matrix)),
            "coordinate_identity_error": float(np.linalg.norm(raw_terminal - normalized_terminal)),
            "checks": checks,
        }

    result = {
        "schema": "phangs_radial_body_projection_normalization_gauge_v01",
        "status": "RAW_SOURCE_AMPLITUDE_GAUGE_RECOVERED_SOURCE_SIDE",
        "galaxies": results,
        "all_checks_pass": all_checks,
        "endpoint_opened": False,
        "score_computed": False,
        "law": "S_tilde=S D and beta=D beta_tilde, so S_tilde beta_tilde=S beta",
        "claim_boundary": (
            "source-coordinate audit only; recovers normalization factors but does not derive "
            "physical response gains, a terminal map, channel, time, quantum, or dark-sector signal"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# PHANGS radial body-projection normalization-gauge audit v01",
        "",
        f"Status: `{result['status']}`",
        "",
        "The exact-edge source profiles reconstruct every frozen normalized matrix column. "
        "All pre-normalization column norms are finite and positive, and the identity "
        "`S_tilde beta_tilde = S (D beta_tilde)` holds numerically for every development body. "
        "Thus normalization fixes a coefficient coordinate gauge; it does not destroy the source "
        "amplitudes retained in the profile table. The physical response gains and velocity unit "
        "remain underived.",
        "",
    ]
    for galaxy, item in results.items():
        lines.append(
            f"- `{galaxy}`: norm range `{item['minimum_raw_column_norm']:.6g}` to "
            f"`{item['maximum_raw_column_norm']:.6g}`, reconstruction error "
            f"`{item['matrix_reconstruction_error']:.3e}`."
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(result["status"], f"galaxies={len(results)}")
    if not all_checks:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
