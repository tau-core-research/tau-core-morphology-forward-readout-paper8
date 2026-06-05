#!/usr/bin/env python3
"""Acquire or audit THINGS H I products for NGC7331.

By default this script builds a download manifest only. With ``--download`` it
caches the six NGC7331 THINGS moment maps used for source-side q_warp,
sigma_warp, and epsilon_cross preparation. It never reads rotation endpoint
residuals and never computes an endpoint score.
"""

from __future__ import annotations

import argparse
import hashlib
import urllib.request
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CACHE = ROOT / "data" / "external" / "literature" / "ngc7331_things_hi_route"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_things_hi_products_source_acquisition_not_endpoint"
BASE = "https://www2.mpia-hd.mpg.de/THINGS/Data_files"

PRODUCTS = [
    ("NA_MOM0", "natural_weight_moment0_integrated_hi_intensity"),
    ("NA_MOM1", "natural_weight_moment1_velocity_field"),
    ("NA_MOM2", "natural_weight_moment2_velocity_dispersion"),
    ("RO_MOM0", "robust_weight_moment0_integrated_hi_intensity"),
    ("RO_MOM1", "robust_weight_moment1_velocity_field"),
    ("RO_MOM2", "robust_weight_moment2_velocity_dispersion"),
]


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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def head(url: str) -> tuple[int | None, int | None, str]:
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=30) as response:
            length = response.headers.get("Content-Length")
            return response.status, int(length) if length else None, ""
    except Exception as exc:  # pragma: no cover - network failure is recorded.
        return None, None, str(exc)


def download(url: str, path: Path) -> tuple[bool, str]:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, path)
        return True, ""
    except Exception as exc:  # pragma: no cover - network failure is recorded.
        return False, str(exc)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--download",
        action="store_true",
        help="download/cache FITS products instead of building only the manifest",
    )
    args = parser.parse_args()

    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)

    rows = []
    for product, role in PRODUCTS:
        filename = f"NGC_7331_{product}_THINGS.FITS"
        url = f"{BASE}/{filename}"
        local_path = CACHE / filename
        status_code, content_length, head_error = head(url)
        download_status = "NOT_REQUESTED"
        download_error = ""
        if args.download and status_code == 200:
            ok, download_error = download(url, local_path)
            download_status = "DOWNLOADED" if ok else "DOWNLOAD_FAILED"
        elif local_path.exists():
            download_status = "ALREADY_CACHED"

        file_exists = local_path.exists()
        rows.append(
            {
                "galaxy": GALAXY,
                "product_id": product,
                "product_role": role,
                "source_url": url,
                "http_status": status_code,
                "content_length_bytes": content_length,
                "head_error": head_error,
                "download_status": download_status,
                "local_cache_path": str(local_path),
                "local_cache_exists": file_exists,
                "local_size_bytes": local_path.stat().st_size if file_exists else pd.NA,
                "sha256": sha256(local_path) if file_exists else pd.NA,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    manifest = pd.DataFrame(rows)
    cached_count = int(manifest["local_cache_exists"].sum())
    downloadable_count = int(manifest["http_status"].eq(200).sum())
    download_requested = bool(args.download)
    cache_complete = cached_count == len(manifest)
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "things_hi_acquisition_status": (
                    "NGC7331_THINGS_HI_PRODUCTS_CACHED_SOURCE_NATIVE_READY"
                    if cache_complete
                    else "NGC7331_THINGS_HI_DOWNLOAD_MANIFEST_BUILT_CACHE_INCOMPLETE"
                ),
                "n_products": len(manifest),
                "n_downloadable": downloadable_count,
                "n_cached": cached_count,
                "download_requested": download_requested,
                "cache_complete": cache_complete,
                "preferred_products_for_q_warp": "NA_MOM0;NA_MOM1;RO_MOM0;RO_MOM1",
                "cube_download_required_now": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "population_claim_allowed": False,
                "next_required_action": (
                    "build residual-blind THINGS map worksheet for q_warp and sign/cross-term extraction"
                    if cache_complete
                    else "run with --download or use Bosma figure digitization fallback"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "ngc7331_things_hi_product_manifest.csv", index=False)
    summary.to_csv(DATA / "ngc7331_things_hi_product_acquisition_summary.csv", index=False)

    report = [
        "# NGC7331 THINGS H I Product Acquisition",
        "",
        "This acquisition artifact identifies and optionally caches source-native",
        "THINGS NGC7331 H I moment maps. It is source-side only and not an",
        "endpoint score.",
        "",
        "## Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
    ]
    (REPORTS / "ngc7331_things_hi_product_acquisition.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
