#!/usr/bin/env python3
"""Audit SkyView image availability for P0 morphology targets.

This checks whether the P0 external imaging requests return at least one image
for DSS2 Red, 2MASS-K, and WISE W1.  It records availability only; temporary
SkyView FITS URLs are intentionally not written to disk.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from astropy import units as u
from astroquery.skyview import SkyView


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "p0_skyview_availability_not_image_classification_not_endpoint"

SURVEYS = [
    ("DSS2 Red", "skyview_dss2_red_url"),
    ("2MASS-K", "skyview_2mass_ks_url"),
    ("WISE 3.4", "skyview_wise_w1_url"),
]


def query_count(row: pd.Series, survey: str) -> tuple[int, str]:
    radius = (float(row["suggested_fov_arcmin"]) / 120.0) * u.deg
    try:
        urls = SkyView.get_image_list(
            position=f"{float(row['ra_deg']):.6f} {float(row['dec_deg']):.6f}",
            survey=[survey],
            radius=radius,
        )
        return len(urls), "QUERY_OK"
    except Exception as exc:  # pragma: no cover - external-service failure path
        return 0, f"QUERY_ERROR:{type(exc).__name__}:{str(exc)[:120]}"


def build_audit() -> tuple[pd.DataFrame, pd.DataFrame]:
    requests = pd.read_csv(DATA / "p0_external_imaging_request_manifest.csv")
    rows = []
    for _, row in requests.iterrows():
        for survey, query_column in SURVEYS:
            n_images, query_status = query_count(row, survey)
            rows.append(
                {
                    "galaxy": row["galaxy"],
                    "survey": survey,
                    "ra_deg": row["ra_deg"],
                    "dec_deg": row["dec_deg"],
                    "suggested_fov_arcmin": row["suggested_fov_arcmin"],
                    "stable_query_url": row[query_column],
                    "skyview_image_count": n_images,
                    "availability_status": "AVAILABLE" if n_images > 0 else "UNAVAILABLE",
                    "query_status": query_status,
                    "temporary_image_urls_recorded": False,
                    "accepted_label_output_allowed": False,
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    audit = pd.DataFrame(rows)
    summary = (
        audit.groupby("survey", as_index=False)
        .agg(
            n_galaxies=("galaxy", "size"),
            n_available=("availability_status", lambda values: int((values == "AVAILABLE").sum())),
            n_unavailable=("availability_status", lambda values: int((values == "UNAVAILABLE").sum())),
            median_image_count=("skyview_image_count", "median"),
        )
        .sort_values("survey")
    )
    return audit, summary


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(audit: pd.DataFrame, summary: pd.DataFrame) -> None:
    compact = audit[
        [
            "galaxy",
            "survey",
            "suggested_fov_arcmin",
            "skyview_image_count",
            "availability_status",
            "query_status",
        ]
    ]
    lines = [
        "# P0 SkyView Availability Audit",
        "",
        "This audit checks whether the P0 external imaging requests return at least",
        "one SkyView image for DSS2 Red, 2MASS-K, and WISE W1. It does not download,",
        "classify, or interpret images, and it does not write temporary SkyView FITS",
        "URLs to disk.",
        "",
        "## Availability Summary",
        "",
        markdown_table(summary),
        "",
        "## Per-Request Availability",
        "",
        markdown_table(compact),
        "",
        "## Claim Boundary",
        "",
        "This is image-source availability only. It is not a morphology label, not",
        "image-based validation, and not an endpoint score.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_skyview_availability_audit.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    audit, summary = build_audit()
    audit.to_csv(DATA / "p0_skyview_availability_audit.csv", index=False)
    summary.to_csv(DATA / "p0_skyview_availability_summary.csv", index=False)
    write_report(audit, summary)
    print("PAPER8_P0_SKYVIEW_AVAILABILITY_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
