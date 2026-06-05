#!/usr/bin/env python3
"""Build a conservative RHI-to-tail transition promotion attempt.

This is not a direct measurement promotion.  It records whether the remaining
scale-tail conditional rows have enough residual-blind HI extent support to be
treated as theorem-conditional upper-cutoff candidates.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_tail_rhi_promotion_attempt_not_direct_not_endpoint"

LITERATURE_SUPPORT = (
    "Wang et al. 2014, arXiv:1401.8164 / MNRAS; reports homogeneous outer HI "
    "profiles and an exponential outer profile scale of about 0.18 R1, where "
    "R1 is the 1 Msun pc^-2 HI radius."
)
LITERATURE_URL = "https://arxiv.org/abs/1401.8164"


def finite(value: object) -> bool:
    try:
        return pd.notna(value) and float(value) > 0
    except (TypeError, ValueError):
        return False


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


def build_attempt() -> tuple[pd.DataFrame, pd.DataFrame]:
    req = pd.read_csv(DATA / "s4g75_conditional_promotion_requirements.csv")
    fill = pd.read_csv(DATA / "s4g75_promoted_kernel_observable_fill.csv")
    availability = pd.read_csv(DATA / "s4g75_source_native_availability_audit.csv")
    tail = req.loc[req["promotion_gate"] == "TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION"].copy()
    table = (
        tail[["galaxy", "formula_family", "source_priority", "promotion_gate"]]
        .merge(
            fill[
                [
                    "galaxy",
                    "scale_radius_kpc",
                    "tail_inner_radius_kpc",
                    "tail_cutoff_radius_kpc",
                    "tail_observable_status",
                    "kernel_observable_provenance",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
        .merge(
            availability[
                [
                    "galaxy",
                    "RHI_kpc",
                    "Rdisk_kpc",
                    "Ref",
                    "dustpedia_status",
                    "dustpedia_tables",
                    "kernel_specific_source_status",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
    )
    rows = []
    for _, row in table.iterrows():
        has_rhi = finite(row["RHI_kpc"])
        cutoff_matches_rhi = has_rhi and finite(row["tail_cutoff_radius_kpc"]) and abs(
            float(row["tail_cutoff_radius_kpc"]) - float(row["RHI_kpc"])
        ) < 1.0e-9
        inner_inside_cutoff = (
            finite(row["tail_inner_radius_kpc"])
            and finite(row["tail_cutoff_radius_kpc"])
            and float(row["tail_inner_radius_kpc"]) < float(row["tail_cutoff_radius_kpc"])
        )
        if has_rhi and cutoff_matches_rhi and inner_inside_cutoff:
            status = "THEOREM_CONDITIONAL_RHI_UPPER_CUTOFF_CANDIDATE"
            endpoint_allowed = False
            reason = (
                "RHI is available and already used as the cutoff candidate, but "
                "this remains an upper-cutoff support theorem, not a direct "
                "outer-transition measurement."
            )
        elif has_rhi:
            status = "RHI_AVAILABLE_PROTOCOL_MISMATCH_REVIEW"
            endpoint_allowed = False
            reason = "RHI exists but current tail fields do not match the predeclared cutoff protocol."
        else:
            status = "RHI_MISSING_NO_PROMOTION_ATTEMPT"
            endpoint_allowed = False
            reason = "No positive RHI source support is available."
        rows.append(
            {
                "galaxy": row["galaxy"],
                "formula_family": row["formula_family"],
                "source_priority": row["source_priority"],
                "promotion_gate": row["promotion_gate"],
                "scale_radius_kpc": row["scale_radius_kpc"],
                "rdisk_kpc": row["Rdisk_kpc"],
                "rhi_kpc": row["RHI_kpc"],
                "tail_inner_radius_kpc": row["tail_inner_radius_kpc"],
                "tail_cutoff_radius_kpc": row["tail_cutoff_radius_kpc"],
                "promotion_attempt_status": status,
                "promotion_attempt_reason": reason,
                "literature_support": LITERATURE_SUPPORT,
                "literature_url": LITERATURE_URL,
                "sparc_hi_ref": row["Ref"],
                "dustpedia_status": row["dustpedia_status"],
                "dustpedia_tables": row["dustpedia_tables"],
                "strict_kernel_ready": False,
                "endpoint_scores_allowed": endpoint_allowed,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    attempt = pd.DataFrame(rows)
    summary = (
        attempt.groupby(["promotion_attempt_status", "source_priority"], as_index=False)
        .agg(
            n_galaxies=("galaxy", "count"),
            galaxies=("galaxy", lambda values: ";".join(values)),
        )
    )
    summary["claim_boundary"] = CLAIM_BOUNDARY
    return attempt, summary


def write_report(attempt: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# S4G75 Tail RHI Promotion Attempt",
        "",
        "This report checks whether the remaining scale-tail conditional rows can "
        "be treated as theorem-conditional RHI upper-cutoff candidates. It is "
        "not a direct measurement promotion and not an endpoint.",
        "",
        "## Literature Support",
        "",
        f"{LITERATURE_SUPPORT} Source: {LITERATURE_URL}.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Galaxy-Level Attempt",
        "",
        markdown_table(
            attempt[
                [
                    "galaxy",
                    "source_priority",
                    "rhi_kpc",
                    "tail_inner_radius_kpc",
                    "tail_cutoff_radius_kpc",
                    "promotion_attempt_status",
                    "strict_kernel_ready",
                    "promotion_attempt_reason",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "RHI support is not a direct outer-disk transition measurement. It may "
        "support a conservative upper-cutoff theorem, but strict kernel-ready "
        "status still requires either direct transition evidence or an accepted "
        "Tau-side promotion theorem.",
        "",
    ]
    (REPORTS / "s4g75_tail_rhi_promotion_attempt.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    attempt, summary = build_attempt()
    attempt.to_csv(DATA / "s4g75_tail_rhi_promotion_attempt.csv", index=False)
    summary.to_csv(DATA / "s4g75_tail_rhi_promotion_attempt_summary.csv", index=False)
    write_report(attempt, summary)
    print(f"wrote {DATA / 's4g75_tail_rhi_promotion_attempt.csv'}")
    print(f"wrote {DATA / 's4g75_tail_rhi_promotion_attempt_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_tail_rhi_promotion_attempt.md'}")


if __name__ == "__main__":
    main()
