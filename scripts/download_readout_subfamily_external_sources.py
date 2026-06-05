#!/usr/bin/env python3
"""Download/cache external source hits for readout-subfamily review.

The script intentionally caches source documents only. It does not extract
observables, score endpoints, or promote accepted readout labels.
"""

from __future__ import annotations

from pathlib import Path
import ssl
import shutil
import subprocess
from urllib.request import Request, urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
LITERATURE = ROOT / "data" / "external" / "literature"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "readout_subfamily_source_cache_not_label_acceptance"


SOURCE_DOWNLOADS = [
    {
        "galaxy": "IC2574",
        "evidence_id": "hi_asymmetry_map",
        "source_url": "https://academic.oup.com/mnras/article/493/2/2618/5734519",
        "cache_name": "ic2574_deblok_2020_m81_hi_survey.pdf",
        "source_kind": "pdf",
        "local_source_path": "/Users/jolcsak/Desktop/staa415.pdf",
    },
    {
        "galaxy": "IC2574",
        "evidence_id": "environment_history",
        "source_url": "https://arxiv.org/pdf/astro-ph/9904002",
        "cache_name": "ic2574_walter_brinks_1999_hi_holes_shells.pdf",
        "source_kind": "pdf",
        "local_source_path": "",
    },
    {
        "galaxy": "IC2574",
        "evidence_id": "outer_tail_transition",
        "source_url": "https://astronomia.unam.mx/journals/rmxaa/article/view/2002rmxaa..38...39s",
        "cache_name": "ic2574_sanchez_salcedo_hidalgo_gamez_2002_holes.html",
        "source_kind": "html",
        "local_source_path": "",
    },
    {
        "galaxy": "NGC4013",
        "evidence_id": "disk_overlay_check",
        "source_url": "https://arxiv.org/pdf/1506.05123",
        "cache_name": "ngc4013_zschaechner_rand_2015_hi_kinematics.pdf",
        "source_kind": "pdf",
        "local_source_path": "",
    },
    {
        "galaxy": "NGC5907",
        "evidence_id": "velocity_field_sanity",
        "source_url": "https://arxiv.org/pdf/astro-ph/9806395",
        "cache_name": "ngc5907_shang_1998_ring_warp_interaction.pdf",
        "source_kind": "pdf",
        "local_source_path": "",
    },
    {
        "galaxy": "NGC5907",
        "evidence_id": "vertical_or_warp_source",
        "source_url": "https://arxiv.org/pdf/1408.5905",
        "cache_name": "ngc5907_wiegert_2015_edge_on_ism.pdf",
        "source_kind": "pdf",
        "local_source_path": "",
    },
    {
        "galaxy": "NGC5907",
        "evidence_id": "projection_geometry",
        "source_url": "https://academic.oup.com/pasj/article/39/6/849/8078264",
        "cache_name": "ngc5907_sasaki_1987_surface_photometry_warp.pdf",
        "source_kind": "pdf",
        "local_source_path": "/Users/jolcsak/Desktop/pasj_39_6_849.pdf",
    },
    {
        "galaxy": "NGC7331",
        "evidence_id": "vertical_scale_or_thickness",
        "source_url": "https://arxiv.org/pdf/1706.08615",
        "cache_name": "ngc7331_patra_2018_molecular_scale_height.pdf",
        "source_kind": "pdf",
        "local_source_path": "",
    },
    {
        "galaxy": "NGC4183",
        "evidence_id": "bar_core_projection_history_overlay",
        "source_url": "https://arxiv.org/pdf/1103.4928",
        "cache_name": "ngc4183_whisp_lopsidedness_context_2011.pdf",
        "source_kind": "pdf",
        "local_source_path": "",
    },
    {
        "galaxy": "UGC05716",
        "evidence_id": "hi_asymmetry_map",
        "source_url": "https://astroweb.case.edu/ssm/papers/AAv505p577.pdf",
        "cache_name": "ugc05716_swaters_2009_late_type_dwarf_rotation_shapes.pdf",
        "source_kind": "pdf",
        "local_source_path": "",
    },
]


def fetch(url: str, destination: Path) -> tuple[str, int, str]:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 source-cache for reproducible academic review; "
                "contact: local research workflow"
            )
        },
    )
    try:
        context = ssl._create_unverified_context() if "astroweb.case.edu" in url else None
        with urlopen(request, timeout=60, context=context) as response:
            payload = response.read()
        destination.write_bytes(payload)
        return "CACHED", len(payload), ""
    except Exception as exc:  # pragma: no cover - network-specific diagnostic
        return "DOWNLOAD_FAILED", 0, str(exc)


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    LITERATURE.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in SOURCE_DOWNLOADS:
        local_path = LITERATURE / item["cache_name"]
        local_source = Path(str(item.get("local_source_path", "")))
        if local_path.exists() and local_path.stat().st_size > 0:
            status = "ALREADY_CACHED"
            bytes_cached = local_path.stat().st_size
            error = ""
        elif str(local_source) and local_source.exists() and local_source.stat().st_size > 0:
            shutil.copyfile(local_source, local_path)
            status = "LOCAL_SOURCE_CACHED"
            bytes_cached = local_path.stat().st_size
            error = ""
        else:
            status, bytes_cached, error = fetch(item["source_url"], local_path)
        text_path = ""
        text_status = "NOT_APPLICABLE"
        if local_path.suffix.lower() == ".pdf" and local_path.exists() and local_path.stat().st_size > 0:
            text_target = local_path.with_suffix(".txt")
            text_path = str(text_target)
            if text_target.exists() and text_target.stat().st_size > 0:
                text_status = "TEXT_ALREADY_EXTRACTED"
            elif shutil.which("pdftotext"):
                try:
                    subprocess.run(
                        ["pdftotext", str(local_path), str(text_target)],
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    text_status = "TEXT_EXTRACTED"
                except subprocess.CalledProcessError as exc:
                    text_status = f"TEXT_EXTRACTION_FAILED: {exc.stderr.strip()}"
            else:
                text_status = "PDFTOTEXT_NOT_AVAILABLE"
        rows.append(
            {
                **item,
                "cache_status": status,
                "bytes_cached": bytes_cached,
                "local_path": str(local_path),
                "text_cache_status": text_status,
                "text_local_path": text_path,
                "download_error": error,
                "accepted_label_promoted": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    manifest = pd.DataFrame(rows)
    manifest.to_csv(DATA / "readout_subfamily_external_source_cache_manifest.csv", index=False)
    summary = (
        manifest.groupby(["galaxy", "cache_status"], as_index=False)
        .agg(n_sources=("evidence_id", "size"), bytes_cached=("bytes_cached", "sum"))
        .sort_values(["galaxy", "cache_status"])
    )
    summary.to_csv(DATA / "readout_subfamily_external_source_cache_summary.csv", index=False)
    report = [
        "# Readout-Subfamily External Source Cache",
        "",
        "This cache stores the targeted source documents used by the",
        "readout-subfamily acquisition pass. It is residual-blind and does not",
        "promote accepted labels.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Manifest",
        "",
        markdown_table(
            manifest[
                [
                    "galaxy",
                    "evidence_id",
                    "cache_status",
                    "bytes_cached",
                    "source_url",
                    "local_path",
                    "text_cache_status",
                    "text_local_path",
                    "claim_boundary",
                ]
            ]
        ),
        "",
    ]
    (REPORTS / "readout_subfamily_external_source_cache.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
