#!/usr/bin/env python3
"""Build the NGC4088 channel-map digitization target manifest.

This manifest points to concrete source pages/panels that can be digitized to
extract a residual-blind warp-onset control.  It does not perform the
digitization and does not create x_w.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
PAGE_DIR = ROOT / "data" / "external" / "literature" / "2001_verheijen_sancisi_pages"
CLAIM_BOUNDARY = "s4g75_ngc4088_digitization_target_manifest_not_endpoint"


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


def build_manifest() -> tuple[pd.DataFrame, pd.DataFrame]:
    page_path = PAGE_DIR / "ngc4088_page_76-076.png"
    rows = [
        {
            "galaxy": "NGC4088",
            "source_authors_year": "Verheijen & Sancisi 2001",
            "source_pdf": "data/external/literature/2001_verheijen_sancisi_ursa_major_hi.pdf",
            "source_pdf_page": 76,
            "rendered_page_png": str(page_path.relative_to(ROOT)),
            "target_panel": "N4088 channel maps",
            "target_observable": "warp_onset_radius_or_PA_bend_from_channel_map",
            "digitization_route": "CHANNEL_MAP_DIGITIZATION",
            "required_measurement_outputs": (
                "inner_disk_axis;outer_ridge_axis_by_side;onset_radius_arcmin;"
                "side_combination_rule;uncertainty_arcmin"
            ),
            "acceptance_rule": (
                "digitization protocol, tolerance, and side-combination rule "
                "must be frozen before any endpoint scoring"
            ),
            "page_render_available": page_path.exists(),
            "x_warp_onset_available": False,
            "endpoint_scores_allowed": False,
            "endpoint_scores_computed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC4088",
            "source_authors_year": "Verheijen & Sancisi 2001",
            "source_pdf": "data/external/literature/2001_verheijen_sancisi_ursa_major_hi.pdf",
            "source_pdf_page": 77,
            "rendered_page_png": "data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_77-077.png",
            "target_panel": "N4088 continuation panels / position-velocity diagnostics",
            "target_observable": "cross-check_PA_or_PV_asymmetry",
            "digitization_route": "PV_OR_CONTINUATION_CROSS_CHECK",
            "required_measurement_outputs": (
                "PV_asymmetry_side;outer_extent_side;consistency_with_channel_map"
            ),
            "acceptance_rule": "cross-check only unless a radial onset can be measured",
            "page_render_available": (PAGE_DIR / "ngc4088_page_77-077.png").exists(),
            "x_warp_onset_available": False,
            "endpoint_scores_allowed": False,
            "endpoint_scores_computed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    manifest = pd.DataFrame(rows)
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "n_digitization_targets": len(manifest),
                "n_rendered_pages_available": int(manifest["page_render_available"].sum()),
                "primary_digitization_route": "CHANNEL_MAP_DIGITIZATION",
                "x_warp_onset_available": False,
                "manifest_status": "DIGITIZATION_TARGET_READY_XW_NOT_EXTRACTED",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return manifest, summary


def write_report(manifest: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Digitization Target Manifest",
        "",
        "This manifest identifies the source pages/panels needed for a residual-blind "
        "NGC4088 warp-onset extraction. It does not perform digitization.",
        "",
        "## Verdict",
        "",
        "The N4088 channel-map page is available as a rendered source target. The "
        "next action is a frozen channel-map digitization protocol that measures "
        "an onset radius or PA bend. No `x_w` has been extracted here.",
        "",
        "## Targets",
        "",
        markdown_table(manifest),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "A digitization target is not a measurement. The endpoint remains blocked "
        "until the digitization protocol produces a residual-blind `x_w` with a "
        "predeclared uncertainty and side-combination rule.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_digitization_target_manifest.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    manifest, summary = build_manifest()
    manifest.to_csv(DATA / "s4g75_ngc4088_digitization_target_manifest.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_digitization_target_summary.csv", index=False)
    write_report(manifest, summary)
    print(f"wrote {DATA / 's4g75_ngc4088_digitization_target_manifest.csv'}")
    print(f"wrote {DATA / 's4g75_ngc4088_digitization_target_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_ngc4088_digitization_target_manifest.md'}")


if __name__ == "__main__":
    main()
