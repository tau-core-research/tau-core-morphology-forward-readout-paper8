#!/usr/bin/env python3
"""Build P0 external imaging/source request manifest.

The manifest converts the P0 inspection packets into concrete residual-blind
source requests: coordinates, suggested field of view, source URLs, and the
observable to inspect. It does not download or interpret images.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote_plus

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "p0_external_imaging_request_not_morphology_label_not_endpoint"


def deg_to_skyview_size(arcmin: float) -> str:
    size_deg = max(arcmin / 60.0, 0.05)
    return f"{size_deg:.4f}"


def rhi_arcmin(rhi_kpc: float, distance_mpc: float) -> float:
    if not np.isfinite(rhi_kpc) or not np.isfinite(distance_mpc) or distance_mpc <= 0:
        return np.nan
    return rhi_kpc / (distance_mpc * 1000.0) * 206265.0 / 60.0


def build_url_set(galaxy: str, ra_deg: float, dec_deg: float, fov_arcmin: float) -> dict[str, str]:
    name_query = quote_plus(galaxy)
    coord_query = quote_plus(f"{ra_deg:.6f} {dec_deg:.6f}")
    size_deg = deg_to_skyview_size(fov_arcmin)
    return {
        "ned_url": f"https://ned.ipac.caltech.edu/byname?objname={name_query}",
        "simbad_url": f"https://simbad.cds.unistra.fr/simbad/sim-id?Ident={name_query}",
        "skyview_dss2_red_url": (
            "https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl"
            f"?Position={coord_query}&Survey=DSS2%20Red&Size={size_deg}"
        ),
        "skyview_2mass_ks_url": (
            "https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl"
            f"?Position={coord_query}&Survey=2MASS-K&Size={size_deg}"
        ),
        "skyview_wise_w1_url": (
            "https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl"
            f"?Position={coord_query}&Survey=WISE%203.4&Size={size_deg}"
        ),
    }


def build_manifest() -> tuple[pd.DataFrame, pd.DataFrame]:
    packet_index = pd.read_csv(DATA / "p0_morphology_inspection_packet_index.csv")
    queue = pd.read_csv(DATA / "morphology_inspection_queue.csv")
    s4g = pd.read_csv(DATA / "external_s4g_galaxies.csv")
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")

    rows = packet_index.merge(
        queue[
            [
                "galaxy",
                "inspection_priority_score",
                "scale_radius_kpc",
                "bar_radius_kpc",
                "s4g_model_components",
            ]
        ],
        on="galaxy",
        how="left",
        validate="one_to_one",
    )
    rows = rows.merge(
        s4g.rename(columns={"Name": "s4g_name"})[
            ["s4g_name", "_RA", "_DE", "PA", "Ell", "Rmax", "Flag", "q", "PA1", "n", "Re"]
        ],
        left_on="galaxy",
        right_on="s4g_name",
        how="left",
    )
    rows = rows.merge(
        sparc[
            ["Galaxy", "D_Mpc", "Inc_deg", "Rdisk_kpc", "RHI_kpc", "SBdisk_Lsun_pc2", "Q"]
        ].rename(columns={"Galaxy": "galaxy"}),
        on="galaxy",
        how="left",
    )

    manifest_rows = []
    for _, row in rows.iterrows():
        disk_arcmin = (
            row["scale_radius_kpc"] / (row["D_Mpc"] * 1000.0) * 206265.0 / 60.0
            if pd.notna(row["scale_radius_kpc"]) and pd.notna(row["D_Mpc"]) and row["D_Mpc"] > 0
            else np.nan
        )
        hi_arcmin = rhi_arcmin(float(row["RHI_kpc"]), float(row["D_Mpc"]))
        fov_arcmin = np.nanmax(
            [
                8.0,
                8.0 * disk_arcmin if np.isfinite(disk_arcmin) else np.nan,
                1.3 * hi_arcmin if np.isfinite(hi_arcmin) and hi_arcmin > 0 else np.nan,
                float(row["Rmax"]) / 60.0 * 1.5 if pd.notna(row["Rmax"]) else np.nan,
            ]
        )
        urls = build_url_set(str(row["galaxy"]), float(row["_RA"]), float(row["_DE"]), float(fov_arcmin))
        manifest_rows.append(
            {
                "galaxy": row["galaxy"],
                "ra_deg": row["_RA"],
                "dec_deg": row["_DE"],
                "suggested_fov_arcmin": round(float(fov_arcmin), 3),
                "sparc_distance_mpc": row["D_Mpc"],
                "sparc_inclination_deg": row["Inc_deg"],
                "sparc_rdisk_kpc": row["Rdisk_kpc"],
                "sparc_rhi_kpc": row["RHI_kpc"],
                "s4g_position_angle_deg": row["PA"],
                "s4g_ellipticity": row["Ell"],
                "s4g_rmax_arcsec": row["Rmax"],
                "s4g_model_components": row["s4g_model_components"],
                "inspection_focus": row["inspection_focus"],
                "requested_external_sources": row["requested_external_sources"],
                **urls,
                "request_status": "PENDING_EXTERNAL_IMAGE_AND_CATALOG_REVIEW",
                "accepted_label_output_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    manifest = pd.DataFrame(manifest_rows).sort_values("galaxy")
    summary = (
        manifest.assign(source=manifest["requested_external_sources"].str.split(";"))
        .explode("source")
        .groupby("source", as_index=False)
        .agg(
            n_requests=("galaxy", "size"),
            median_fov_arcmin=("suggested_fov_arcmin", "median"),
        )
        .sort_values(["n_requests", "source"], ascending=[False, True])
    )
    return manifest, summary


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(manifest: pd.DataFrame, summary: pd.DataFrame) -> None:
    compact = manifest[
        [
            "galaxy",
            "ra_deg",
            "dec_deg",
            "suggested_fov_arcmin",
            "inspection_focus",
            "s4g_model_components",
        ]
    ]
    lines = [
        "# P0 External Imaging Request Manifest",
        "",
        "This manifest prepares residual-blind external image and catalogue review",
        "for the four P0 morphology-inspection targets. It records coordinates,",
        "recommended fields of view, and source URLs. It does not download, classify,",
        "or interpret images.",
        "",
        "## P0 Requests",
        "",
        markdown_table(compact),
        "",
        "## Requested Source Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "This is not an accepted morphology manifest, not image-based validation,",
        "and not an endpoint score. It is a source-request layer for future",
        "residual-blind morphology inspection.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_external_imaging_request_manifest.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    manifest, summary = build_manifest()
    manifest.to_csv(DATA / "p0_external_imaging_request_manifest.csv", index=False)
    summary.to_csv(DATA / "p0_external_imaging_request_summary.csv", index=False)
    write_report(manifest, summary)
    print("PAPER8_P0_EXTERNAL_IMAGING_REQUEST_MANIFEST_COMPLETE")


if __name__ == "__main__":
    main()
