#!/usr/bin/env python3
"""Build a P0 readout-relevant morphology proxy layer.

The Tau Core bridge does not require the apparent 4D morphology label to be the
fundamental Tau-side readout class.  This layer separates the source-reviewed
4D label from a residual-blind readout-relevant proxy suggested by source
caveats. It is not an endpoint label and does not use rotation residuals.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "p0_readout_relevant_morphology_proxy_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def readout_proxy(row: pd.Series) -> dict[str, str]:
    caveat = str(row["manifest_caveat"])
    label = str(row["present_day_morphology_label"]).lower()
    if "edge_projection" in caveat or "edge-on" in label:
        return {
            "readout_relevant_proxy_family": "K_projection_corrected_expdisk",
            "readout_proxy_components": "K_exponential_disk+projection_or_thick_flared_correction",
            "proxy_reason": "apparent 4D disk label is projection-contaminated; readout may require edge/thickness correction",
            "pilot_implication": "plain K_exponential_disk is expected to be a weak control, not final readout",
        }
    if "bar" in caveat or "bar" in label:
        return {
            "readout_relevant_proxy_family": "K_barred_expdisk_m2_overlay",
            "readout_proxy_components": "K_exponential_disk+barred_spiral_m2_overlay",
            "proxy_reason": "apparent disk label has bar support; 1D expdisk readout may miss non-axisymmetric m=2 structure",
            "pilot_implication": "plain K_exponential_disk is a baseline component; bar overlay should be tested separately",
        }
    if "nuclear" in caveat or "nuclear" in label:
        return {
            "readout_relevant_proxy_family": "K_expdisk_compact_core_overlay",
            "readout_proxy_components": "K_exponential_disk+compact_finite_core_overlay",
            "proxy_reason": "apparent disk label has nuclear/compact caveat; readout may include compact-core contribution",
            "pilot_implication": "plain K_exponential_disk may underfit inner/transition structure",
        }
    return {
        "readout_relevant_proxy_family": "K_clean_exponential_disk_control",
        "readout_proxy_components": "K_exponential_disk",
        "proxy_reason": "source-reviewed 4D disk label has no current source-side correction caveat",
        "pilot_implication": "plain K_exponential_disk is the appropriate first control",
    }


def build_proxy() -> tuple[pd.DataFrame, pd.DataFrame]:
    labels = pd.read_csv(DATA / "p0_codex_accepted_label_manifest.csv")
    rows = []
    for _, row in labels.iterrows():
        proxy = readout_proxy(row)
        rows.append(
            {
                "galaxy": row["galaxy"],
                "k_obs": row["accepted_formula_family"],
                "k_readout": proxy["readout_relevant_proxy_family"],
                "formula_shell": proxy["readout_relevant_proxy_family"],
                "promotion_status": (
                    "K_OBS_DIRECT"
                    if proxy["readout_relevant_proxy_family"]
                    == "K_clean_exponential_disk_control"
                    else "K_OBS_TO_K_READOUT_PROXY"
                ),
                "readout_proxy_source": "p0_codex_source_review_caveat_mapping",
                "observed_4d_family_label": row["accepted_formula_family"],
                "observed_4d_morphology_label": row["present_day_morphology_label"],
                "manifest_caveat": row["manifest_caveat"],
                "review_confidence": row["review_confidence"],
                **proxy,
                "uses_rotation_residuals": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    proxy_df = pd.DataFrame(rows).sort_values("galaxy").reset_index(drop=True)
    summary = (
        proxy_df.groupby("readout_relevant_proxy_family", as_index=False)
        .agg(
            n_galaxies=("galaxy", "size"),
            median_review_confidence=("review_confidence", "median"),
            n_direct_k_obs=("promotion_status", lambda s: int((s == "K_OBS_DIRECT").sum())),
            n_proxy_promotions=(
                "promotion_status",
                lambda s: int((s == "K_OBS_TO_K_READOUT_PROXY").sum()),
            ),
            uses_rotation_residuals=("uses_rotation_residuals", "any"),
            endpoint_scores_computed=("endpoint_scores_computed", "any"),
        )
        .sort_values(["n_galaxies", "readout_relevant_proxy_family"], ascending=[False, True])
    )
    summary["claim_boundary"] = CLAIM_BOUNDARY
    return proxy_df, summary


def write_report(proxy: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# P0 Readout-Relevant Morphology Proxy",
        "",
        "This layer separates the apparent 4D morphology label from the possible",
        "Tau-side readout-relevant morphology proxy. The current P0 Codex/source",
        "review labels all have an apparent 4D `K_exponential_disk` handle, but",
        "source-side caveats suggest different readout-relevant corrections.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Proxy Rows",
        "",
        markdown_table(proxy),
        "",
        "## Interpretation",
        "",
        "The operational scoring fields are `k_obs`, `k_readout`,",
        "`readout_proxy_source`, `promotion_status`, and `formula_shell`. The",
        "formula shell is attached to `k_readout`, not automatically to `k_obs`.",
        "",
        "The thin/thick disk, bar, ring, compact, and tail labels are treated here",
        "as projected 4D morphology handles, not as proven fundamental Tau-side",
        "classes. A future endpoint should predeclare whether it tests the observed",
        "4D handle directly or a source-justified readout-relevant proxy.",
        "They are not as proven fundamental Tau-side classes.",
        "",
        "This explains why a plain P0 `K_exponential_disk` pilot can be weak: only",
        "one row is a clean exponential-disk control, while the other rows carry",
        "projection, bar, or compact/nuclear correction caveats.",
        "",
        "## Claim Boundary",
        "",
        "This proxy does not use rotation residuals, does not compute endpoint scores,",
        "and does not validate Tau Core. It is a pre-endpoint architecture layer for",
        "separating observed 4D morphology from readout-relevant morphology.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_readout_relevant_morphology_proxy.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    proxy, summary = build_proxy()
    proxy.to_csv(DATA / "p0_readout_relevant_morphology_proxy.csv", index=False)
    summary.to_csv(DATA / "p0_readout_relevant_morphology_proxy_summary.csv", index=False)
    write_report(proxy, summary)
    print("PAPER8_P0_READOUT_RELEVANT_MORPHOLOGY_PROXY_COMPLETE")


if __name__ == "__main__":
    main()
