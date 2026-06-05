#!/usr/bin/env python3
"""Build a narrow accepted manifest for the audited exponential-disk lane.

This does not unblock the full Paper 8 frozen launch. It freezes only the
externally audited 13-row exponential-disk lane where both the family label
and the scale observable are source-backed enough for a narrow accepted
population endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = (
    "narrow_accepted_population_manifest_not_full_launch_not_population_validation"
)


def build_manifest() -> tuple[pd.DataFrame, pd.DataFrame]:
    audit = pd.read_csv(DATA / "exponential_disk_family_label_audit.csv").copy()
    audit["accepted_population_lane"] = "NARROW_ACCEPTED_EXPONENTIAL_DISK_13"
    audit["accepted_population_family"] = "K_exponential_disk"
    audit["accepted_kernel_observable"] = "scale_radius_kpc"
    audit["accepted_kernel_formula"] = (
        "tau_core_gravity_rmond_exponential_disk_readout_formula_001:Freeman_Bessel"
    )
    audit["accepted_population_endpoint_ready"] = True
    audit["accepted_population_claim_boundary"] = CLAIM_BOUNDARY
    audit["accepted_population_caveat"] = audit["external_family_label_caveat"].fillna(
        "none"
    )
    audit["accepted_population_support_tier"] = audit["narrow_dry_run_lane"].map(
        {
            "STRICT_NARROW_DRY_RUN_READY_CANDIDATE": "STRICT",
            "CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL": "CAVEATED",
        }
    ).fillna("REVIEW")
    manifest = audit[
        [
            "galaxy",
            "accepted_population_lane",
            "accepted_population_family",
            "accepted_population_support_tier",
            "external_family_label_status",
            "external_family_label_confidence",
            "accepted_population_caveat",
            "scale_radius_kpc",
            "accepted_kernel_observable",
            "accepted_kernel_formula",
            "observable_provenance",
            "external_family_label_source",
            "residual_blind_certification",
            "accepted_population_endpoint_ready",
            "accepted_population_claim_boundary",
        ]
    ].sort_values(["accepted_population_support_tier", "galaxy"])
    summary = pd.DataFrame(
        [
            {
                "accepted_population_lane": "NARROW_ACCEPTED_EXPONENTIAL_DISK_13",
                "n_rows": int(len(manifest)),
                "n_strict_rows": int(
                    (manifest["accepted_population_support_tier"] == "STRICT").sum()
                ),
                "n_caveated_rows": int(
                    (manifest["accepted_population_support_tier"] == "CAVEATED").sum()
                ),
                "accepted_population_endpoint_ready": bool(
                    manifest["accepted_population_endpoint_ready"].all()
                ),
                "accepted_population_claim_boundary": CLAIM_BOUNDARY,
                "launch_scope": "narrow_family_restricted_lane_only",
                "full_175_launch_unblocked": False,
            }
        ]
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
    lines = [
        "# Narrow Accepted Exponential-Disk Manifest",
        "",
        "This manifest freezes the first population-level matched-family lane that",
        "is source-backed enough for Paper 8: the 13 externally audited",
        "exponential-disk rows with accepted scale-radius observables.",
        "",
        "## Verdict",
        "",
        "This is an accepted narrow population manifest, not the full 175-row launch.",
        "It authorizes a family-restricted endpoint lane only for the audited",
        "exponential-disk support pool.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Manifest Rows",
        "",
        markdown_table(manifest),
        "",
        "## Claim Boundary",
        "",
        "This manifest does not imply that the global Paper 8 launch guard has",
        "passed. It does not authorize unmatched families, does not validate the",
        "full 175-row packet, and does not by itself establish population-level",
        "superiority over MOND, RAR, TPG, or Newtonian baselines.",
    ]
    (REPORTS / "narrow_accepted_exponential_disk_manifest.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    manifest, summary = build_manifest()
    manifest.to_csv(DATA / "narrow_accepted_exponential_disk_manifest.csv", index=False)
    summary.to_csv(
        DATA / "narrow_accepted_exponential_disk_manifest_summary.csv", index=False
    )
    write_report(manifest, summary)
    print("PAPER8_NARROW_ACCEPTED_EXPONENTIAL_DISK_MANIFEST_COMPLETE")


if __name__ == "__main__":
    main()
