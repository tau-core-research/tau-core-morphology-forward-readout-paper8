#!/usr/bin/env python3
"""Build an endpoint-blind radial two-plane body proxy for UGC03580/UGC3580."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from two_plane_morphology_common_v01 import (
    angle_deg,
    chordal_mean,
    connection_diagnostics,
    load_source_geometry,
    max_slerp_norm_error,
    orientation_normal,
    radial_zone,
    unit_rows,
)


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
POINTS_OUT = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_body_v01_points.csv"
SUMMARY_OUT = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_body_v01.json"
REPORT_OUT = ROOT / "reports" / "ugc03580_ugc3580_two_plane_body_v01.md"
FIGURE_OUT = (
    ROOT
    / "paper8_submission_source"
    / "figures"
    / "fig_ugc03580_ugc3580_two_plane_body_v01.png"
)

EXPECTED_SOURCE_PDF_SHA256 = "15b4ae9e2bb3268509e75b40e62def8cc4664a117fdcccafae8afb7f170ec8ba"
EXPECTED_SOURCE_TABLE_SHA256 = "fb27253af89e667395eca2ccec23055b79dd74ee0fe38bbc5e26ae800ba4e568"
SOURCE_TABLE4_MUTUAL_INCLINATION_DEG = 13.9
SOURCE_TABLE4_MUTUAL_INCLINATION_ERROR_DEG = 2.5


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def vector_record(vector: np.ndarray) -> dict[str, float]:
    return {
        "n_w": float(vector[0]),
        "n_n": float(vector[1]),
        "n_los": float(vector[2]),
    }


def make_figure(points: pd.DataFrame, inner: np.ndarray, outer: np.ndarray) -> None:
    FIGURE_OUT.parent.mkdir(parents=True, exist_ok=True)
    radius = points["radius_kpc_source"].to_numpy(dtype=float)
    supported = points["within_source_terminal_support"].to_numpy(dtype=bool)

    fig, axes = plt.subplots(2, 2, figsize=(10.2, 7.7), constrained_layout=True)
    ax = axes[0, 0]
    ax.plot(radius[supported], points.loc[supported, "inclination_deg"], "o-", label="inclination")
    ax.plot(radius[supported], points.loc[supported, "pa_deg"], "s-", label="position angle")
    ax.scatter(radius[~supported], points.loc[~supported, "inclination_deg"], marker="x", color="0.4", label="beyond support")
    ax.scatter(radius[~supported], points.loc[~supported, "pa_deg"], marker="x", color="0.4")
    ax.axvspan(13.18, 17.57, color="#f4a261", alpha=0.18, label="transition")
    ax.axvline(27.45, color="0.35", linestyle=":", label="source terminal radius")
    ax.set(xlabel="source radius [kpc]", ylabel="orientation [deg]", title="Published ring orientation")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25)

    ax = axes[0, 1]
    ax.errorbar(
        radius[supported],
        points.loc[supported, "tip_deg"],
        yerr=points.loc[supported, "tip_error_deg"],
        fmt="o-",
        capsize=2,
        label="published tip",
    )
    ax.plot(radius[supported], points.loc[supported, "tip_from_orientation_deg"], "--", label="reconstructed tip")
    ax.plot(radius[supported], points.loc[supported, "distance_to_outer_plane_deg"], ":", label="distance to outer plane")
    ax.scatter(radius[~supported], points.loc[~supported, "tip_deg"], marker="x", color="0.4", label="beyond support")
    ax.axhline(float(angle_deg(inner, outer)), color="k", linewidth=1, alpha=0.6, label="inner/outer separation")
    ax.axvline(27.45, color="0.35", linestyle=":")
    ax.set(xlabel="source radius [kpc]", ylabel="angular distance [deg]", title="Two-plane geometry")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25)

    ax = axes[1, 0]
    ax.plot(radius[supported], points.loc[supported, "delta_tilt"], "o-", color="#9c2f2f", label=r"$1-\mathbf{n}_0\cdot\mathbf{n}(R)$")
    ax.scatter(radius[~supported], points.loc[~supported, "delta_tilt"], marker="x", color="0.4", label="beyond support")
    ax.set(xlabel="source radius [kpc]", ylabel="bounded tilt defect", title="Bounded source morphology invariant")
    ax.grid(alpha=0.25)
    density_axis = ax.twinx()
    density_axis.plot(radius[supported], points.loc[supported, "sigma_hi_msun_pc2"], "s--", color="#457b9d", alpha=0.75, label=r"$\Sigma_{HI}$")
    density_axis.set_ylabel(r"H I surface density [$M_\odot\,pc^{-2}$]")
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = density_axis.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, fontsize=8)

    ax = axes[1, 1]
    scatter = ax.scatter(
        points.loc[supported, "n_w_orientation"],
        points.loc[supported, "n_n_orientation"],
        c=radius[supported],
        cmap="viridis",
        edgecolor="black",
        linewidth=0.35,
        label="published rings",
    )
    ax.plot(
        points.loc[supported, "n_w_orientation"],
        points.loc[supported, "n_n_orientation"],
        color="0.65",
        linewidth=0.8,
        zorder=0,
    )
    ax.scatter(inner[0], inner[1], marker="*", s=150, color="#e76f51", label="inner plane")
    ax.scatter(outer[0], outer[1], marker="D", s=65, color="#264653", label="outer mean plane")
    ax.set(xlabel=r"$n_W$", ylabel=r"$n_N$", title="Normal-vector path on the source support")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.colorbar(scatter, ax=ax, label="source radius [kpc]", shrink=0.82)

    fig.suptitle("UGC03580 / UGC3580: endpoint-blind radial two-plane body proxy", fontsize=13)
    fig.savefig(FIGURE_OUT, dpi=220)
    plt.close(fig)


def main() -> None:
    pdf_hash = sha256(SOURCE_PDF)
    table_hash = sha256(SOURCE_TABLE)
    if pdf_hash != EXPECTED_SOURCE_PDF_SHA256:
        raise RuntimeError("Jozsa source PDF hash mismatch")
    if table_hash != EXPECTED_SOURCE_TABLE_SHA256:
        raise RuntimeError("UGC3580 source geometry table hash mismatch")

    points = load_source_geometry(SOURCE_TABLE)
    orientation_normals = orientation_normal(
        points["inclination_deg"].to_numpy(dtype=float),
        points["pa_deg"].to_numpy(dtype=float),
    )
    table_normals_raw = points[["n_w", "n_n", "n_los"]].to_numpy(dtype=float)
    table_normals = unit_rows(table_normals_raw)
    inner = orientation_normal(np.array([67.2]), np.array([96.3]))[0]

    outer_mask = points["radius_arcsec"].between(240.0, 375.0, inclusive="both").to_numpy()
    supported_mask = (points["radius_arcsec"] <= 375.0).to_numpy()
    inner_mask = (points["radius_arcsec"] <= 150.0).to_numpy()
    outer_normals = orientation_normals[outer_mask]
    outer = chordal_mean(outer_normals)
    outer_density_weighted = chordal_mean(
        outer_normals,
        points.loc[outer_mask, "sigma_hi_msun_pc2"].to_numpy(dtype=float),
    )
    outer_with_beyond_support = chordal_mean(orientation_normals[points["radius_arcsec"] >= 240.0])

    tip_from_orientation = angle_deg(orientation_normals, inner)
    tip_from_table_normal = angle_deg(table_normals, unit_rows(table_normals_raw[:1])[0])
    distance_to_outer = angle_deg(orientation_normals, outer)
    delta_tilt = 1.0 - np.clip(orientation_normals @ inner, -1.0, 1.0)
    segment_angle, segment_gradient = connection_diagnostics(
        points["radius_kpc_source"].to_numpy(dtype=float), orientation_normals
    )

    points = points.copy()
    points["zone"] = points["radius_arcsec"].map(radial_zone)
    points["within_source_terminal_support"] = supported_mask
    points["n_w_orientation"] = orientation_normals[:, 0]
    points["n_n_orientation"] = orientation_normals[:, 1]
    points["n_los_orientation"] = orientation_normals[:, 2]
    points["published_normal_norm_before_renormalization"] = np.linalg.norm(table_normals_raw, axis=1)
    points["orientation_vs_published_normal_deg"] = angle_deg(orientation_normals, table_normals)
    points["tip_from_orientation_deg"] = tip_from_orientation
    points["tip_from_published_normal_deg"] = tip_from_table_normal
    points["tip_residual_orientation_minus_published_deg"] = tip_from_orientation - points["tip_deg"]
    points["delta_tilt"] = delta_tilt
    points["distance_to_outer_plane_deg"] = distance_to_outer
    points["connection_angle_from_previous_ring_deg"] = segment_angle
    points["connection_gradient_deg_per_kpc"] = segment_gradient
    points["geodesic_progress_diagnostic_not_kernel"] = tip_from_orientation / float(angle_deg(inner, outer))
    points["lon_phase_cos"] = np.where(points["tip_deg"] > 0.0, np.cos(np.deg2rad(points["lon_deg"])), np.nan)
    points["lon_phase_sin"] = np.where(points["tip_deg"] > 0.0, np.sin(np.deg2rad(points["lon_deg"])), np.nan)

    leave_one_out_shifts = []
    for index in range(len(outer_normals)):
        candidate = chordal_mean(np.delete(outer_normals, index, axis=0))
        leave_one_out_shifts.append(float(angle_deg(candidate, outer)))

    downsampled_outer = chordal_mean(outer_normals[::2])
    inner_outer_angle = float(angle_deg(inner, outer))
    table4_z = (
        inner_outer_angle - SOURCE_TABLE4_MUTUAL_INCLINATION_DEG
    ) / SOURCE_TABLE4_MUTUAL_INCLINATION_ERROR_DEG
    max_tip_residual = float(
        np.max(np.abs(points.loc[supported_mask, "tip_residual_orientation_minus_published_deg"]))
    )
    max_normal_disagreement = float(
        np.max(points.loc[supported_mask, "orientation_vs_published_normal_deg"])
    )
    max_slerp_error = max_slerp_norm_error(orientation_normals[supported_mask])
    max_inner_defect = float(np.max(points.loc[inner_mask, "delta_tilt"]))

    summary = {
        "schema": "tau_core_ugc03580_ugc3580_two_plane_body_v01",
        "status": "SOURCE_ACQUISITION_ONLY",
        "galaxy": "UGC03580",
        "alias": "UGC3580",
        "descriptor_type": "localized_galaxy_body_proxy_not_universe_level_M_tau",
        "source": {
            "citation": "Jozsa 2007 A&A 468 903-917, Tables 1, 4 and 6",
            "pdf_path": str(SOURCE_PDF.relative_to(ROOT)),
            "pdf_sha256": pdf_hash,
            "geometry_table_path": str(SOURCE_TABLE.relative_to(ROOT)),
            "geometry_table_sha256": table_hash,
            "published_rotation_velocity_columns_imported": False,
            "sparc_endpoint_accessed": False,
        },
        "construction": {
            "inner_reference_plane": {"inclination_deg": 67.2, "pa_deg": 96.3, **vector_record(inner)},
            "outer_plane_support_arcsec": [240.0, 375.0],
            "outer_plane_estimator": "unweighted chordal mean of source orientation normals",
            "outer_mean_plane": vector_record(outer),
            "transition_interpolation": "piecewise shortest great-circle interpolation on S2",
            "bounded_tilt_defect": "delta_tilt(R)=1-n_inner dot n(R), in [0,2]",
            "connection_gradient": "acos(n_j dot n_(j-1))/(R_j-R_(j-1))",
            "geodesic_progress_is_kernel": False,
        },
        "derived_geometry": {
            "n_source_rings": int(len(points)),
            "n_primary_supported_rings": int(np.sum(supported_mask)),
            "n_outer_plane_rings": int(np.sum(outer_mask)),
            "inner_outer_plane_separation_deg": inner_outer_angle,
            "published_table4_inner_outer_mean_mutual_inclination_deg": SOURCE_TABLE4_MUTUAL_INCLINATION_DEG,
            "published_table4_error_deg": SOURCE_TABLE4_MUTUAL_INCLINATION_ERROR_DEG,
            "table4_standardized_difference": float(table4_z),
            "outer_plane_mean_ring_distance_deg": float(np.mean(angle_deg(outer_normals, outer))),
            "outer_plane_max_ring_distance_deg": float(np.max(angle_deg(outer_normals, outer))),
            "maximum_supported_delta_tilt": float(np.max(points.loc[supported_mask, "delta_tilt"])),
            "maximum_supported_connection_gradient_deg_per_kpc": float(
                np.nanmax(points.loc[supported_mask, "connection_gradient_deg_per_kpc"])
            ),
        },
        "validation": {
            "endpoint_columns_absent": True,
            "maximum_orientation_vs_published_normal_deg": max_normal_disagreement,
            "maximum_tip_reconstruction_residual_deg": max_tip_residual,
            "maximum_inner_reference_delta_tilt": max_inner_defect,
            "maximum_slerp_unit_norm_error": max_slerp_error,
            "table4_reproduction_within_one_published_sigma": bool(abs(table4_z) <= 1.0),
            "all_delta_tilt_within_mathematical_bounds": bool(
                np.all((points["delta_tilt"] >= -1.0e-12) & (points["delta_tilt"] <= 2.0 + 1.0e-12))
            ),
        },
        "source_only_sensitivity": {
            "density_weighted_outer_plane_shift_deg": float(angle_deg(outer_density_weighted, outer)),
            "include_420_arcsec_beyond_support_shift_deg": float(angle_deg(outer_with_beyond_support, outer)),
            "every_other_outer_ring_shift_deg": float(angle_deg(downsampled_outer, outer)),
            "maximum_leave_one_outer_ring_out_shift_deg": float(max(leave_one_out_shifts)),
            "interpretation": "support and weighting sensitivity only; no endpoint selected these variants",
        },
        "claim_ledger": {
            "facts": [
                "Table 6 supplies radial orientation and H I source fields.",
                "The source fixes the inner plane through 150 arcsec and defines the outer comparison range as 240-375 arcsec.",
            ],
            "definitions": [
                "The primary outer plane is the unweighted chordal mean on the published outer support.",
                "The radial body proxy is the piecewise geodesic path of published plane normals.",
            ],
            "derived_results": [
                "The bounded tilt defect and connection gradients follow from the frozen source normals.",
                "The reconstructed plane separation can be checked against the independent Table 4 summary.",
            ],
            "assumptions": [
                "Tilted-ring orientations are adequate local plane descriptors despite reported non-circular structure.",
                "An unweighted chordal mean is an admissible source-only outer-plane summary.",
            ],
            "not_derived": [
                "No velocity readout kernel, amplitude, sign or terminal law is selected.",
                "No identification with the universe-level morphological body M_tau is made.",
            ],
        },
        "endpoint_allowed": False,
        "readout_formula_selected": False,
        "next_gate": "derive a source-side bounded two-plane readout shell before opening a new endpoint",
    }

    POINTS_OUT.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    # Canonicalize derived floating output across supported NumPy builds.
    # The source angles are reported at far lower precision; 13 significant
    # digits preserve the numerical audit while preventing sub-ulp library
    # differences from invalidating the source-freeze byte hash.
    points.to_csv(POINTS_OUT, index=False, float_format="%.13g")
    SUMMARY_OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    make_figure(points, inner, outer)

    REPORT_OUT.write_text(
        "\n".join(
            [
                "# UGC03580 / UGC3580 radial two-plane body proxy v01",
                "",
                "Status: `SOURCE_ACQUISITION_ONLY`",
                "",
                "## What changed",
                "",
                "The former scalar body proxy retained only a warp onset. This source-only",
                "reconstruction instead uses every published UGC3580 Table 6 ring orientation",
                "while deliberately omitting the published rotation-velocity columns and all",
                "SPARC endpoint values.",
                "",
                "For each radius the local plane is represented by the source normal",
                "",
                "```text",
                "n(R) = (sin(i) sin(PA), -sin(i) cos(PA), cos(i)) in S2.",
                "```",
                "",
                "Adjacent rings are connected by shortest great-circle interpolation. The",
                "source-native bounded morphology defect is",
                "",
                "```text",
                "delta_tilt(R) = 1 - n_inner dot n(R),    0 <= delta_tilt <= 2.",
                "```",
                "",
                "It is a descriptor, not a velocity kernel.",
                "",
                "## Primary source geometry",
                "",
                f"- supported rings: `{int(np.sum(supported_mask))}` through `375 arcsec`;",
                f"- outer-plane rings: `{int(np.sum(outer_mask))}` over `240-375 arcsec`;",
                f"- reconstructed inner/outer separation: `{inner_outer_angle:.3f} deg`;",
                f"- independent Table 4 summary: `13.9 +/- 2.5 deg` (`z={table4_z:.3f}`);",
                f"- maximum supported bounded defect: `{float(np.max(points.loc[supported_mask, 'delta_tilt'])):.6f}`;",
                f"- maximum connection gradient: `{float(np.nanmax(points.loc[supported_mask, 'connection_gradient_deg_per_kpc'])):.3f} deg/kpc`.",
                "",
                "## Validation",
                "",
                f"- maximum orientation/table-normal disagreement: `{max_normal_disagreement:.4f} deg`;",
                f"- maximum published-tip reconstruction residual: `{max_tip_residual:.4f} deg`;",
                f"- maximum inner-plane defect through 150 arcsec: `{max_inner_defect:.3e}`;",
                f"- maximum sampled SLERP unit-norm error: `{max_slerp_error:.3e}`;",
                f"- density-weighted outer-plane sensitivity: `{float(angle_deg(outer_density_weighted, outer)):.3f} deg`;",
                f"- include-420-arcsec support sensitivity: `{float(angle_deg(outer_with_beyond_support, outer)):.3f} deg`;",
                f"- maximum leave-one-outer-ring-out shift: `{max(leave_one_out_shifts):.3f} deg`.",
                "",
                "## Claim boundary",
                "",
                "This closes a source-representation defect: UGC03580 is no longer reduced",
                "to one onset radius. It does not show that the refined morphology explains",
                "the rotation curve. A readout shell, amplitude and carrier still have to be",
                "derived without endpoint access and then frozen on a genuinely new target.",
                "The object is a localized galaxy-scale body proxy, not a separately seeded",
                "universe-level Tau morphological body.",
                "",
                f"Source PDF SHA-256: `{pdf_hash}`.",
                f"Source table SHA-256: `{table_hash}`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
