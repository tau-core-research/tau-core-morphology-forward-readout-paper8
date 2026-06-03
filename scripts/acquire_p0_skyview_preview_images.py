#!/usr/bin/env python3
"""Acquire P0 SkyView preview PNGs.

This downloads SkyView image data for the available P0 requests and renders
small PNG previews for manual residual-blind morphology review.  The previews
are not morphology labels, not image classifications, and not endpoint scores.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from astropy import units as u
from astroquery.skyview import SkyView
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
PREVIEW_DIR = REPORTS / "p0_skyview_previews"

CLAIM_BOUNDARY = "p0_skyview_previews_not_image_classification_not_endpoint"


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")


def normalize(data: np.ndarray) -> np.ndarray:
    values = np.asarray(data, dtype=float)
    finite = np.isfinite(values)
    if not finite.any():
        return np.zeros_like(values, dtype=float)
    lo, hi = np.nanpercentile(values[finite], [1, 99])
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        lo, hi = np.nanmin(values[finite]), np.nanmax(values[finite])
    if hi <= lo:
        return np.zeros_like(values, dtype=float)
    scaled = (values - lo) / (hi - lo)
    return np.clip(scaled, 0.0, 1.0)


def render_png(data: np.ndarray, output: Path, title: str) -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(4, 4), dpi=120)
    plt.imshow(normalize(data), cmap="gray", origin="lower")
    plt.title(title, fontsize=9)
    plt.axis("off")
    plt.tight_layout(pad=0.05)
    plt.savefig(output, bbox_inches="tight", pad_inches=0.02)
    plt.close()


def acquire_preview(row: pd.Series) -> tuple[str, str, int, int]:
    galaxy = str(row["galaxy"])
    survey = str(row["survey"])
    output = PREVIEW_DIR / f"{galaxy}_{safe_name(survey)}.png"
    radius = (float(row["suggested_fov_arcmin"]) / 120.0) * u.deg
    try:
        images = SkyView.get_images(
            position=f"{float(row['ra_deg']):.6f} {float(row['dec_deg']):.6f}",
            survey=[survey],
            radius=radius,
        )
        if not images:
            return str(output.relative_to(ROOT)), "NO_IMAGE_RETURNED", 0, 0
        data = images[0][0].data
        render_png(data, output, f"{galaxy} - {survey}")
        height, width = data.shape[:2]
        return str(output.relative_to(ROOT)), "PREVIEW_RENDERED", int(width), int(height)
    except Exception as exc:  # pragma: no cover - external-service failure path
        if output.exists():
            cached = plt.imread(output)
            height, width = cached.shape[:2]
            return str(output.relative_to(ROOT)), "PREVIEW_RENDERED", int(width), int(height)
        return str(output.relative_to(ROOT)), f"PREVIEW_ERROR:{type(exc).__name__}:{str(exc)[:120]}", 0, 0


def build_previews() -> tuple[pd.DataFrame, pd.DataFrame]:
    availability = pd.read_csv(DATA / "p0_skyview_availability_audit.csv")
    rows = []
    for _, row in availability.iterrows():
        path, status, width, height = acquire_preview(row)
        rows.append(
            {
                "galaxy": row["galaxy"],
                "survey": row["survey"],
                "preview_png_path": path,
                "preview_status": status,
                "preview_width_px": width,
                "preview_height_px": height,
                "suggested_fov_arcmin": row["suggested_fov_arcmin"],
                "source_query_url": row["stable_query_url"],
                "image_classification_performed": False,
                "accepted_label_output_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    manifest = pd.DataFrame(rows).sort_values(["galaxy", "survey"])
    summary = (
        manifest.groupby("survey", as_index=False)
        .agg(
            n_requests=("galaxy", "size"),
            n_rendered=("preview_status", lambda values: int((values == "PREVIEW_RENDERED").sum())),
            median_width_px=("preview_width_px", "median"),
            median_height_px=("preview_height_px", "median"),
        )
        .sort_values("survey")
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
            "survey",
            "preview_png_path",
            "preview_status",
            "preview_width_px",
            "preview_height_px",
        ]
    ]
    image_lines = []
    for _, row in manifest.iterrows():
        if row["preview_status"] == "PREVIEW_RENDERED":
            image_lines.append(
                f"![{row['galaxy']} {row['survey']}]({row['preview_png_path'].replace('reports/', '')})"
            )
    lines = [
        "# P0 SkyView Preview Images",
        "",
        "This report records PNG previews rendered from SkyView image data for the",
        "P0 morphology-inspection targets. The previews are source material for a",
        "future residual-blind human review only. They are not morphology labels,",
        "not image classifications, and not endpoint scores.",
        "",
        "## Preview Summary",
        "",
        markdown_table(summary),
        "",
        "## Preview Manifest",
        "",
        markdown_table(compact),
        "",
        "## Preview Gallery",
        "",
        "\n\n".join(image_lines),
        "",
        "## Claim Boundary",
        "",
        "No image classification is performed. No accepted morphology label is",
        "emitted. No endpoint score is computed.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_skyview_preview_images.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    manifest, summary = build_previews()
    manifest.to_csv(DATA / "p0_skyview_preview_image_manifest.csv", index=False)
    summary.to_csv(DATA / "p0_skyview_preview_image_summary.csv", index=False)
    write_report(manifest, summary)
    print("PAPER8_P0_SKYVIEW_PREVIEW_IMAGES_COMPLETE")


if __name__ == "__main__":
    main()
