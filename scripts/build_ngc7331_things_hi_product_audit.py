#!/usr/bin/env python3
"""Audit cached THINGS H I products for NGC7331.

This script reads locally cached source-native FITS moment maps and records
basic integrity/header/statistical checks needed before any residual-blind
q_warp worksheet is built. It does not inspect observed rotation residuals.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_things_hi_product_audit_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.6g}")
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def finite_stats(array: np.ndarray) -> dict[str, float | int]:
    data = np.asarray(array, dtype=float)
    finite = np.isfinite(data)
    finite_values = data[finite]
    if finite_values.size == 0:
        return {
            "n_pixels": int(data.size),
            "n_finite": 0,
            "finite_fraction": 0.0,
            "min_value": np.nan,
            "max_value": np.nan,
            "median_value": np.nan,
            "p95_value": np.nan,
        }
    return {
        "n_pixels": int(data.size),
        "n_finite": int(finite_values.size),
        "finite_fraction": float(finite_values.size / data.size),
        "min_value": float(np.nanmin(finite_values)),
        "max_value": float(np.nanmax(finite_values)),
        "median_value": float(np.nanmedian(finite_values)),
        "p95_value": float(np.nanpercentile(finite_values, 95)),
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(DATA / "ngc7331_things_hi_product_manifest.csv")
    rows = []
    for _, item in manifest.iterrows():
        path = Path(str(item["local_cache_path"]))
        if not path.exists():
            rows.append(
                {
                    "galaxy": GALAXY,
                    "product_id": item["product_id"],
                    "audit_status": "BLOCKED_LOCAL_CACHE_MISSING",
                    "local_cache_path": str(path),
                    "shape": pd.NA,
                    "bunit": pd.NA,
                    "ctype1": pd.NA,
                    "ctype2": pd.NA,
                    "cdelt1": pd.NA,
                    "cdelt2": pd.NA,
                    **finite_stats(np.array([], dtype=float)),
                }
            )
            continue

        with fits.open(path, memmap=True) as hdul:
            hdu = hdul[0]
            header = hdu.header
            data = hdu.data
            stats = finite_stats(data)
            rows.append(
                {
                    "galaxy": GALAXY,
                    "product_id": item["product_id"],
                    "audit_status": "PASS_FITS_READABLE",
                    "local_cache_path": str(path),
                    "shape": "x".join(str(dim) for dim in np.shape(data)),
                    "bunit": header.get("BUNIT", pd.NA),
                    "ctype1": header.get("CTYPE1", pd.NA),
                    "ctype2": header.get("CTYPE2", pd.NA),
                    "cdelt1": header.get("CDELT1", pd.NA),
                    "cdelt2": header.get("CDELT2", pd.NA),
                    **stats,
                }
            )

    audit = pd.DataFrame(rows)
    audit["endpoint_scores_allowed"] = False
    audit["uses_vobs_or_residual"] = False
    audit["claim_boundary"] = CLAIM_BOUNDARY
    audit = audit[
        [
            "galaxy",
            "product_id",
            "audit_status",
            "local_cache_path",
            "shape",
            "bunit",
            "ctype1",
            "ctype2",
            "cdelt1",
            "cdelt2",
            "n_pixels",
            "n_finite",
            "finite_fraction",
            "min_value",
            "max_value",
            "median_value",
            "p95_value",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    all_readable = bool(audit["audit_status"].eq("PASS_FITS_READABLE").all())
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "things_hi_product_audit_status": (
                    "NGC7331_THINGS_HI_PRODUCTS_AUDITED_WORKSHEET_READY"
                    if all_readable
                    else "NGC7331_THINGS_HI_PRODUCTS_AUDIT_BLOCKED_CACHE_MISSING"
                ),
                "n_products_audited": len(audit),
                "n_readable": int(audit["audit_status"].eq("PASS_FITS_READABLE").sum()),
                "n_missing": int(audit["audit_status"].eq("BLOCKED_LOCAL_CACHE_MISSING").sum()),
                "worksheet_ready": all_readable,
                "q_warp_measurement_ready": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "population_claim_allowed": False,
                "next_required_action": (
                    "build residual-blind map worksheet defining inner-disk reference, outer ridge mask, and side weights"
                    if all_readable
                    else "complete local THINGS H I product cache"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    audit.to_csv(DATA / "ngc7331_things_hi_product_audit.csv", index=False)
    summary.to_csv(DATA / "ngc7331_things_hi_product_audit_summary.csv", index=False)

    report = [
        "# NGC7331 THINGS H I Product Audit",
        "",
        "This audit verifies that the cached THINGS NGC7331 H I moment maps are",
        "readable and suitable as source-native inputs for a later residual-blind",
        "q_warp/sign/cross-term worksheet. It does not measure q_warp and does",
        "not score an endpoint.",
        "",
        "## FITS Audit",
        "",
        markdown_table(audit),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
    ]
    (REPORTS / "ngc7331_things_hi_product_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
