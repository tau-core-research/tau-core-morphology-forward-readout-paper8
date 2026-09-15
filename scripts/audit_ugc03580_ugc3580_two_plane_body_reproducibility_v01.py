#!/usr/bin/env python3
"""Independent numerical audit of the UGC03580 source-only two-plane body proxy."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = (
    ROOT
    / "data"
    / "external"
    / "literature"
    / "ugc08490_ngc5204_warp"
    / "gentile2007_warped_disks.pdf"
)
SOURCE_TABLE = SOURCE_PDF.with_name("ugc3580_table6_geometry_v01.csv")
BUILDER = ROOT / "scripts" / "build_ugc03580_ugc3580_two_plane_body_v01.py"
POINTS = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_body_v01_points.csv"
SUMMARY = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_body_v01.json"
OUT = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_body_reproducibility_audit_v01.json"
REPORT = ROOT / "reports" / "ugc03580_ugc3580_two_plane_body_reproducibility_audit_v01.md"

EXPECTED_SOURCE_PDF_SHA256 = "15b4ae9e2bb3268509e75b40e62def8cc4664a117fdcccafae8afb7f170ec8ba"
EXPECTED_SOURCE_TABLE_SHA256 = "fb27253af89e667395eca2ccec23055b79dd74ee0fe38bbc5e26ae800ba4e568"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normal_from_orientation(inclination_deg: np.ndarray, pa_deg: np.ndarray) -> np.ndarray:
    inclination = np.deg2rad(np.asarray(inclination_deg, dtype=float))
    pa = np.deg2rad(np.asarray(pa_deg, dtype=float))
    normals = np.column_stack(
        (
            np.sin(inclination) * np.sin(pa),
            -np.sin(inclination) * np.cos(pa),
            np.cos(inclination),
        )
    )
    return normals / np.linalg.norm(normals, axis=1, keepdims=True)


def angle_deg(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return np.rad2deg(
        np.arccos(np.clip(np.sum(np.asarray(left) * np.asarray(right), axis=-1), -1.0, 1.0))
    )


def mean_normal(normals: np.ndarray, weights: np.ndarray | None = None) -> np.ndarray:
    if weights is None:
        value = np.sum(normals, axis=0)
    else:
        value = np.sum(normals * np.asarray(weights)[:, None], axis=0)
    return value / np.linalg.norm(value)


def close(left: float, right: float, tolerance: float = 1.0e-10) -> bool:
    return bool(math.isclose(left, right, rel_tol=tolerance, abs_tol=tolerance))


def main() -> None:
    source = pd.read_csv(SOURCE_TABLE)
    points = pd.read_csv(POINTS)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    normals = normal_from_orientation(source["inclination_deg"], source["pa_deg"])
    inner = normal_from_orientation(np.array([67.2]), np.array([96.3]))[0]
    outer_mask = source["radius_arcsec"].between(240.0, 375.0, inclusive="both").to_numpy()
    supported = (source["radius_arcsec"] <= 375.0).to_numpy()
    outer = mean_normal(normals[outer_mask])
    separation = float(angle_deg(inner, outer))
    tip = angle_deg(normals, inner)
    delta = 1.0 - np.clip(normals @ inner, -1.0, 1.0)
    density_outer = mean_normal(normals[outer_mask], source.loc[outer_mask, "sigma_hi_msun_pc2"])
    support_extended_outer = mean_normal(normals[source["radius_arcsec"] >= 240.0])
    downsampled_outer = mean_normal(normals[outer_mask][::2])
    leave_one_out = [
        float(angle_deg(mean_normal(np.delete(normals[outer_mask], index, axis=0)), outer))
        for index in range(int(np.sum(outer_mask)))
    ]

    table_normals = source[["n_w", "n_n", "n_los"]].to_numpy(dtype=float)
    table_normals /= np.linalg.norm(table_normals, axis=1, keepdims=True)
    orientation_table_disagreement = angle_deg(normals, table_normals)
    tip_residual = tip - source["tip_deg"].to_numpy(dtype=float)

    builder_text = BUILDER.read_text(encoding="utf-8").lower()
    endpoint_snippets = ["data/external/sparc", "vobs", "rotmod", "load_sparc_endpoint", "warp_prediction"]
    output_endpoint_columns = [
        column
        for column in points.columns
        if any(token in column.lower() for token in ("vobs", "vrot", "sparc", "rotation_model"))
    ]

    derived = summary["derived_geometry"]
    validation = summary["validation"]
    sensitivity = summary["source_only_sensitivity"]
    checks = {
        "source_pdf_hash_matches": sha256(SOURCE_PDF) == EXPECTED_SOURCE_PDF_SHA256,
        "source_table_hash_matches": sha256(SOURCE_TABLE) == EXPECTED_SOURCE_TABLE_SHA256,
        "source_table_has_18_rows": len(source) == 18,
        "source_radii_strictly_increase": bool(np.all(np.diff(source["radius_arcsec"]) > 0.0)),
        "source_table_has_no_endpoint_columns": not any(
            token in column.lower()
            for column in source.columns
            for token in ("vobs", "vrot", "residual", "sparc")
        ),
        "builder_has_no_endpoint_path_or_loader": not any(token in builder_text for token in endpoint_snippets),
        "derived_points_have_no_endpoint_columns": len(output_endpoint_columns) == 0,
        "primary_support_excludes_420_arcsec": bool(
            not points.loc[points["radius_arcsec"] == 420.0, "within_source_terminal_support"].iloc[0]
        ),
        "primary_support_has_17_rings": int(np.sum(supported)) == 17,
        "outer_support_has_5_rings": int(np.sum(outer_mask)) == 5,
        "orientation_normals_are_unit": bool(np.max(np.abs(np.linalg.norm(normals, axis=1) - 1.0)) < 1.0e-14),
        "orientation_matches_published_normals": float(np.max(orientation_table_disagreement[supported])) < 0.1,
        "published_tip_reconstructed": float(np.max(np.abs(tip_residual[supported]))) < 0.11,
        "inner_reference_limit_is_exact": float(np.max(delta[source["radius_arcsec"] <= 150.0])) < 1.0e-14,
        "bounded_defect_holds": bool(np.all((delta >= -1.0e-14) & (delta <= 2.0 + 1.0e-14))),
        "plane_separation_matches_summary": close(separation, float(derived["inner_outer_plane_separation_deg"])),
        "plane_separation_reproduces_table4": abs(separation - 13.9) <= 2.5,
        "maximum_tip_residual_matches_summary": close(
            float(np.max(np.abs(tip_residual[supported]))),
            float(validation["maximum_tip_reconstruction_residual_deg"]),
        ),
        "density_weight_sensitivity_matches": close(
            float(angle_deg(density_outer, outer)),
            float(sensitivity["density_weighted_outer_plane_shift_deg"]),
        ),
        "support_extension_sensitivity_matches": close(
            float(angle_deg(support_extended_outer, outer)),
            float(sensitivity["include_420_arcsec_beyond_support_shift_deg"]),
        ),
        "resolution_sensitivity_matches": close(
            float(angle_deg(downsampled_outer, outer)),
            float(sensitivity["every_other_outer_ring_shift_deg"]),
        ),
        "leave_one_out_sensitivity_matches": close(
            max(leave_one_out),
            float(sensitivity["maximum_leave_one_outer_ring_out_shift_deg"]),
        ),
        "all_primary_sensitivities_below_published_table4_error": max(
            float(angle_deg(density_outer, outer)),
            float(angle_deg(support_extended_outer, outer)),
            float(angle_deg(downsampled_outer, outer)),
            max(leave_one_out),
        ) < 2.5,
        "endpoint_remains_blocked": summary["endpoint_allowed"] is False,
        "readout_formula_remains_unselected": summary["readout_formula_selected"] is False,
    }
    passed = int(sum(checks.values()))
    status = "REPRODUCIBILITY_AUDIT_PASS" if passed == len(checks) else "REPRODUCIBILITY_AUDIT_FAIL"
    result = {
        "schema": "tau_core_ugc03580_ugc3580_two_plane_body_reproducibility_audit_v01",
        "status": status,
        "checks_passed": passed,
        "checks_total": len(checks),
        "checks": checks,
        "independent_recomputation": {
            "inner_outer_plane_separation_deg": separation,
            "maximum_orientation_vs_published_normal_deg": float(np.max(orientation_table_disagreement[supported])),
            "maximum_tip_reconstruction_residual_deg": float(np.max(np.abs(tip_residual[supported]))),
            "density_weighted_outer_plane_shift_deg": float(angle_deg(density_outer, outer)),
            "include_420_arcsec_shift_deg": float(angle_deg(support_extended_outer, outer)),
            "every_other_ring_shift_deg": float(angle_deg(downsampled_outer, outer)),
            "maximum_leave_one_out_shift_deg": max(leave_one_out),
        },
        "claim_boundary": "source-geometry reproducibility only; no terminal or Tau-specific physical validation",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "\n".join(
            [
                "# UGC03580 two-plane body reproducibility audit v01",
                "",
                f"Status: `{status}`",
                "",
                f"Independent checks passed: `{passed}/{len(checks)}`.",
                "",
                "The audit independently reconstructs the spherical ring normals,",
                "inner/outer plane angle, bounded tilt defect and four source-only",
                "support/weighting/resolution sensitivities. It also inspects the",
                "builder and output schemas for endpoint-bearing paths or columns.",
                "",
                "All primary sensitivity shifts remain below the published 2.5 deg",
                "Table 4 uncertainty. This is a geometry robustness result only; it",
                "does not select a velocity kernel or validate Tau Core.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if status != "REPRODUCIBILITY_AUDIT_PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
