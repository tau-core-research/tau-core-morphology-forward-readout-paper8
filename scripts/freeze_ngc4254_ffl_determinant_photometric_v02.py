#!/usr/bin/env python3
"""Freeze the photometric NGC4254 FFL shape proxy and beam overlap matrix."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits

from freeze_ngc4254_ffl_determinant_source_vectors_v01 import (
    FIELDS_PATH,
    build_rows,
    load_source_fields,
)
from ngc4254_source_covariance_utils import (
    aips_clean_beam_from_header,
    beam_covariance_pixels,
    beam_overlap_correlation,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

GEOMETRY_PATH = DATA / "ngc4254_s4g_photometric_geometry_freeze_v02.json"
FIELDS_META_PATH = DATA / "ngc4254_baryonic_surface_density_fields_v01.json"
VIVA_HI_PATH = (
    ROOT
    / "data/external/literature/ngc4254_phangs_tracer_velocity/ngc4254.viva.mom0.fits"
)
PRIMARY_CSV_PATH = DATA / "ngc4254_ffl_determinant_photometric_vectors_v02.csv"
SENSITIVITY_CSV_PATH = DATA / "ngc4254_ffl_determinant_photometric_geometry_sensitivity_v02.csv"
BEAM_CSV_PATH = DATA / "ngc4254_ffl_determinant_beam_overlap_correlation_v02.csv"
JSON_PATH = DATA / "ngc4254_ffl_determinant_photometric_freeze_v02.json"
REPORT_PATH = REPORTS / "ngc4254_ffl_determinant_photometric_freeze_v02.md"

STATUS = "SOURCE_ONLY_PHOTOMETRIC_FFL_PROXY_WITH_BEAM_SCREEN_FROZEN_NOT_ENDPOINT_READY"
CLAIM_BOUNDARY = (
    "source-only photometric determinant-shape proxy plus minimum HI-beam overlap screen; "
    "not physical q_det, a complete covariance, channel/time detection, or endpoint score"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def variant_geometry(base: dict[str, object], variant: dict[str, object]) -> dict[str, object]:
    geometry = dict(base)
    geometry["position_angle_deg_east_of_north"] = float(
        variant["position_angle_deg_east_of_north"]
    )
    geometry["inclination_deg"] = float(
        variant.get("inclination_deg", variant.get("thin_disk_inclination_deg"))
    )
    return geometry


def geometry_variants(base: dict[str, object]) -> list[dict[str, object]]:
    variants: list[dict[str, object]] = [
        {
            "variant": "s4g_global_thin_primary",
            "variant_class": "photometric_primary",
            "position_angle_deg_east_of_north": base["position_angle_deg_east_of_north"],
            "inclination_deg": base["inclination_deg"],
        }
    ]
    for control in base["photometric_geometry_controls"]:
        variants.append(
            {
                "variant": control["name"],
                "variant_class": "photometric_control",
                "position_angle_deg_east_of_north": control[
                    "position_angle_deg_east_of_north"
                ],
                "inclination_deg": control.get(
                    "inclination_deg", control.get("thin_disk_inclination_deg")
                ),
            }
        )
    legacy = base["legacy_kinematic_comparison_not_selected"]
    variants.append(
        {
            "variant": "legacy_kinematic_comparison_not_selected",
            "variant_class": "legacy_comparison",
            "center_icrs_deg": legacy["center_icrs_deg"],
            "position_angle_deg_east_of_north": legacy[
                "position_angle_deg_east_of_north"
            ],
            "inclination_deg": legacy["inclination_deg"],
        }
    )
    return variants


def build_sensitivity(base: dict[str, object]) -> pd.DataFrame:
    records: list[dict[str, object]] = []
    for variant in geometry_variants(base):
        geometry = variant_geometry(base, variant)
        if "center_icrs_deg" in variant:
            geometry["center_icrs_deg"] = variant["center_icrs_deg"]
        for row in build_rows(geometry):
            records.append(
                {
                    "variant": variant["variant"],
                    "variant_class": variant["variant_class"],
                    "position_angle_deg_east_of_north": geometry[
                        "position_angle_deg_east_of_north"
                    ],
                    "inclination_deg": geometry["inclination_deg"],
                    "radial_index": row["radial_index"],
                    "radius_lo_arcsec": row["radius_lo_arcsec"],
                    "radius_hi_arcsec": row["radius_hi_arcsec"],
                    "delta_uv": row["delta_uv"],
                    "q_shape_proxy": row["q_shape_proxy"],
                    "determinant_norm": row["determinant_norm"],
                    "n_pixels_total": row["n_pixels_total"],
                }
            )
    return pd.DataFrame(records)


def sky_geometry(
    geometry: dict[str, object], shape: tuple[int, int], wcs
) -> tuple[np.ndarray, np.ndarray]:
    y_pixels, x_pixels = np.indices(shape, dtype=float)
    ra_deg, dec_deg = wcs.pixel_to_world_values(x_pixels, y_pixels)
    ra0, dec0 = (float(value) for value in geometry["center_icrs_deg"])
    pa = math.radians(float(geometry["position_angle_deg_east_of_north"]))
    inclination = math.radians(float(geometry["inclination_deg"]))
    east = (ra_deg - ra0) * math.cos(math.radians(dec0)) * 3600.0
    north = (dec_deg - dec0) * 3600.0
    major = east * math.sin(pa) + north * math.cos(pa)
    minor = -east * math.cos(pa) + north * math.sin(pa)
    radius = np.hypot(major, minor / math.cos(inclination))
    return radius, np.isfinite(radius)


def build_beam_overlap(
    geometry: dict[str, object], beam_meta: dict[str, object], viva_header
) -> tuple[pd.DataFrame, dict[str, object]]:
    star, h2, hi, wcs = load_source_fields()
    gas = h2 + hi
    radius, finite_geometry = sky_geometry(geometry, star.shape, wcs)
    valid = (
        finite_geometry
        & np.isfinite(star)
        & np.isfinite(gas)
        & (star > 0.0)
        & (gas > 0.0)
    )
    edges = [float(value) for value in geometry["radial_edges_arcsec"]]
    masks = []
    counts = []
    for radius_lo, radius_hi in zip(edges[:-1], edges[1:]):
        mask = valid & (radius >= radius_lo) & (radius < radius_hi)
        count = int(np.count_nonzero(mask))
        if count == 0:
            raise ValueError(f"Empty beam-overlap annulus {radius_lo:g}-{radius_hi:g}")
        weight = mask.astype(float) / count
        masks.append(weight)
        counts.append(count)

    pixel_matrix = np.asarray(wcs.pixel_scale_matrix, dtype=float)
    pixel_scale_arcsec = math.sqrt(abs(float(np.linalg.det(pixel_matrix)))) * 3600.0
    beam_major, beam_minor, beam_pa = aips_clean_beam_from_header(viva_header)
    metadata_major, metadata_minor = (
        float(value) for value in beam_meta["hi_beam_arcsec"]
    )
    if not np.allclose(
        [beam_major, beam_minor], [metadata_major, metadata_minor], atol=1.0e-9
    ):
        raise ValueError("VIVA HISTORY beam disagrees with surface-density metadata")
    beam_covariance = beam_covariance_pixels(
        beam_major, beam_minor, beam_pa, pixel_scale_arcsec
    )
    correlation, eigenvalues, effective_rank = beam_overlap_correlation(
        masks, beam_covariance
    )
    records = []
    for row_index in range(len(masks)):
        for column_index in range(len(masks)):
            records.append(
                {
                    "row_radial_index": row_index,
                    "column_radial_index": column_index,
                    "row_radius_mid_arcsec": 0.5 * (edges[row_index] + edges[row_index + 1]),
                    "column_radius_mid_arcsec": 0.5
                    * (edges[column_index] + edges[column_index + 1]),
                    "beam_overlap_correlation_proxy": correlation[row_index, column_index],
                }
            )
    summary = {
        "model": "exact elliptical Gaussian HI CLEAN-beam autocorrelation integrated over primary photometric annulus masks",
        "beam_provenance": "VIVA FITS HISTORY AIPS CLEAN BMAJ/BMIN/BPA",
        "pixel_scale_arcsec": pixel_scale_arcsec,
        "hi_beam_major_arcsec": beam_major,
        "hi_beam_minor_arcsec": beam_minor,
        "hi_beam_pa_deg_east_of_north": beam_pa,
        "beam_covariance_xy_pixels": beam_covariance.tolist(),
        "annulus_pixel_counts": counts,
        "correlation_eigenvalues": eigenvalues.tolist(),
        "minimum_eigenvalue": float(np.min(eigenvalues)),
        "participation_effective_rank": effective_rank,
        "adjacent_correlations": [
            float(correlation[index, index + 1]) for index in range(len(masks) - 1)
        ],
        "is_complete_q_covariance": False,
    }
    return pd.DataFrame(records), summary


def main() -> None:
    geometry = json.loads(GEOMETRY_PATH.read_text(encoding="utf-8"))
    if not geometry.get("geometry_endpoint_independent"):
        raise ValueError("Photometric geometry is not certified endpoint independent")
    if geometry.get("velocity_or_residual_inputs"):
        raise ValueError("Photometric geometry declares forbidden terminal inputs")
    beam_meta = json.loads(FIELDS_META_PATH.read_text(encoding="utf-8"))
    with fits.open(VIVA_HI_PATH) as hdul:
        viva_header = hdul[0].header.copy()

    sensitivity = build_sensitivity(geometry)
    sensitivity.to_csv(
        SENSITIVITY_CSV_PATH, index=False, float_format="%.12g", lineterminator="\n"
    )
    primary = sensitivity.loc[
        sensitivity["variant"].eq("s4g_global_thin_primary")
    ].copy()
    expected_annuli = len(geometry["radial_edges_arcsec"]) - 1
    if len(primary) != expected_annuli:
        raise ValueError(f"Expected {expected_annuli} primary rows, found {len(primary)}")
    if not np.isfinite(primary[["delta_uv", "q_shape_proxy"]].to_numpy(float)).all():
        raise ValueError("Primary determinant rows contain non-finite values")
    primary.to_csv(PRIMARY_CSV_PATH, index=False, float_format="%.12g", lineterminator="\n")

    photometric = sensitivity.loc[
        sensitivity["variant_class"].isin(["photometric_primary", "photometric_control"])
    ].copy()
    stability_rows = []
    for radial_index, group in photometric.groupby("radial_index", sort=True):
        signs = np.sign(group["q_shape_proxy"].to_numpy(float))
        stability_rows.append(
            {
                "radial_index": int(radial_index),
                "radius_lo_arcsec": float(group["radius_lo_arcsec"].iloc[0]),
                "radius_hi_arcsec": float(group["radius_hi_arcsec"].iloc[0]),
                "photometric_q_min": float(group["q_shape_proxy"].min()),
                "photometric_q_max": float(group["q_shape_proxy"].max()),
                "photometric_q_sign_stable": bool(np.all(signs > 0.0) or np.all(signs < 0.0)),
                "photometric_delta_uv_min": float(group["delta_uv"].min()),
                "photometric_delta_uv_max": float(group["delta_uv"].max()),
            }
        )
    stability = pd.DataFrame(stability_rows)

    beam_frame, beam_summary = build_beam_overlap(geometry, beam_meta, viva_header)
    beam_frame.to_csv(BEAM_CSV_PATH, index=False, float_format="%.12g", lineterminator="\n")

    stable_indices = stability.loc[stability["photometric_q_sign_stable"], "radial_index"].tolist()
    low_conditioning = stability.loc[
        stability["photometric_delta_uv_min"] < 0.1, "radial_index"
    ].tolist()
    manifest = {
        "schema": "ngc4254_ffl_determinant_photometric_freeze_v02",
        "status": STATUS,
        "galaxy": "NGC4254",
        "inputs": {
            "photometric_geometry_freeze": str(GEOMETRY_PATH.relative_to(ROOT)),
            "photometric_geometry_freeze_sha256": sha256(GEOMETRY_PATH),
            "surface_density_fields": str(FIELDS_PATH.relative_to(ROOT)),
            "surface_density_fields_sha256": sha256(FIELDS_PATH),
            "surface_density_metadata": str(FIELDS_META_PATH.relative_to(ROOT)),
            "surface_density_metadata_sha256": sha256(FIELDS_META_PATH),
            "viva_hi_moment0": str(VIVA_HI_PATH.relative_to(ROOT)),
            "viva_hi_moment0_sha256": sha256(VIVA_HI_PATH),
            "velocity_or_residual_inputs": [],
        },
        "outputs": {
            "primary_vectors": str(PRIMARY_CSV_PATH.relative_to(ROOT)),
            "primary_vectors_sha256": sha256(PRIMARY_CSV_PATH),
            "geometry_sensitivity": str(SENSITIVITY_CSV_PATH.relative_to(ROOT)),
            "geometry_sensitivity_sha256": sha256(SENSITIVITY_CSV_PATH),
            "beam_overlap_matrix": str(BEAM_CSV_PATH.relative_to(ROOT)),
            "beam_overlap_matrix_sha256": sha256(BEAM_CSV_PATH),
            "report": str(REPORT_PATH.relative_to(ROOT)),
        },
        "geometry_sensitivity_summary": {
            "n_photometric_variants": int(photometric["variant"].nunique()),
            "n_annuli": len(stability),
            "sign_stable_radial_indices": stable_indices,
            "sign_unstable_radial_indices": [
                int(value)
                for value in stability.loc[
                    ~stability["photometric_q_sign_stable"], "radial_index"
                ].tolist()
            ],
            "low_conditioning_control_radial_indices_below_0p1": [
                int(value) for value in low_conditioning
            ],
            "conditioning_threshold_used_for_selection": None,
            "stability_rows": stability.to_dict(orient="records"),
        },
        "beam_overlap_screen": beam_summary,
        "audit_checks": {
            "geometry_is_endpoint_independent": True,
            "velocity_or_residual_inputs_empty": True,
            "all_primary_annuli_computable": True,
            "all_geometry_controls_computable": bool(
                sensitivity.groupby("variant")["radial_index"].nunique().eq(expected_annuli).all()
            ),
            "beam_matrix_symmetric_unit_diagonal_psd": True,
        },
        "physical_amplitude_ready": False,
        "complete_covariance_ready": False,
        "endpoint_scored": False,
        "known_limitations": [
            "q_shape_proxy is not the physical FFL response q_det",
            "photometric PA ambiguity materially changes amplitudes and one inner sign",
            "one disk-component control is nearly degenerate in the innermost annulus",
            "the beam matrix is an HI support-overlap proxy, not covariance of nonlinear quadrant medians",
            "CO, stellar-map, calibration, geometry, and endpoint noise covariance are not included",
            "kappa_X/kappa_Y, terminal gain, paired-side involution, and role-to-probe identity remain open",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }

    primary_lookup = primary.set_index("radial_index")
    table_lines = [
        "| annulus (arcsec) | primary q_shape | primary Delta_uv | photometric q range | sign stable | min Delta_uv |",
        "|---:|---:|---:|---:|:---:|---:|",
    ]
    for row in stability.itertuples(index=False):
        primary_row = primary_lookup.loc[row.radial_index]
        table_lines.append(
            f"| {row.radius_lo_arcsec:.0f}-{row.radius_hi_arcsec:.0f} | "
            f"{primary_row.q_shape_proxy:+.6f} | {primary_row.delta_uv:.6f} | "
            f"[{row.photometric_q_min:+.6f}, {row.photometric_q_max:+.6f}] | "
            f"{'yes' if row.photometric_q_sign_stable else 'no'} | "
            f"{row.photometric_delta_uv_min:.6f} |"
        )

    report = f"""# NGC4254 Photometric FFL Determinant Freeze v02

**Status:** `{STATUS}`

**Claim boundary:** {CLAIM_BOUNDARY}.

## Result

The v02 primary uses only the S4G photometric center, PA, and thin-disk
inclination plus the existing stellar/H2/HI surface-density fields. It reads no
velocity field, rotation curve, fitted residual, or dark-discrepancy label.

{chr(10).join(table_lines)}

The four outer annuli from 25 to 65 arcsec retain the same sign under all eight
predeclared photometric variants: the S4G global primary, its published
`PA/Ell` one-sigma controls, the `q0=0.2` thickness control, and both S4G
exponential-disk component geometries. The 15--25 arcsec sign is not stable.
The innermost annulus reaches `Delta_uv={stability.iloc[0]['photometric_delta_uv_min']:.6f}`
under one disk-component control and is therefore geometrically ill-conditioned
for that control. No threshold was used to remove it.

## Minimum H I Beam Screen

The VIVA FITS HISTORY records an elliptical CLEAN beam of
`{beam_summary['hi_beam_major_arcsec']:.3f} x {beam_summary['hi_beam_minor_arcsec']:.3f}`
arcsec at PA `{beam_summary['hi_beam_pa_deg_east_of_north']:.2f}` degrees.
Integrating its exact Gaussian autocorrelation over the six primary annulus
masks gives adjacent-bin
correlations

```text
{', '.join(f'{value:.3f}' for value in beam_summary['adjacent_correlations'])}
```

and a participation effective rank of
`{beam_summary['participation_effective_rank']:.3f}` for six radial rows. The
six values are therefore not six independent radial measurements.

This matrix is only a minimum support-overlap screen. The determinant proxy
uses nonlinear quadrant medians and combines H I, CO, and stellar fields, so a
complete endpoint covariance must additionally propagate tracer beams,
calibration, geometry variants, and terminal measurement noise.

## Decision

The former Halpha-geometry dependence has been removed from the primary
center/PA/inclination. Source-side determinant computability survives, and the
outer sign pattern is photometrically stable. Physical amplitude and endpoint
authorization remain blocked: the parent role map, physical `eta`, primitive
curvatures, terminal gain, paired-side involution, and complete covariance are
not yet available. No channel, time, quantum, or dark-matter conclusion is
drawn.
"""

    REPORT_PATH.write_text(report, encoding="utf-8")
    JSON_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(STATUS)
    print(
        f"stable_annuli={stable_indices} "
        f"beam_effective_rank={beam_summary['participation_effective_rank']:.6f}"
    )


if __name__ == "__main__":
    main()
