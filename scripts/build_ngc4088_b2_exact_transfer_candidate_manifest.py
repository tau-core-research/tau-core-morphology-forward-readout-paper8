#!/usr/bin/env python3
"""Build exact-transfer candidate manifest for the NGC4088 B2 source-load law.

The NGC4088 B2 law candidate is an exact warp/history source-load protocol:

    Lambda_tau = sigma_warp q_warp x_w Vflat^2

This script asks which already inspected galaxies can enter an exact transfer
lane. It does not score curves and does not use residuals. Mixed overlay or
projection protocols are retained as analogues, not counted as exact transfer.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_b2_exact_transfer_candidate_manifest_not_endpoint"

REQUIRED_FIELDS = [
    "x_w",
    "q_warp",
    "sigma_warp",
    "Vflat",
    "epsilon_cross_inputs",
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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv").set_index("Galaxy")
    queue = pd.read_csv(DATA / "mixed_readout_candidate_acquisition_queue.csv")
    preflight = pd.read_csv(DATA / "ngc4088_b2_population_transfer_preflight_cases.csv")
    ngc4088_freeze = pd.read_csv(DATA / "ngc4088_warp_history_formula_freeze_manifest.csv").iloc[0]
    ngc7331_onset = pd.read_csv(DATA / "ngc7331_fractional_warp_onset_source_summary.csv").iloc[0]

    inspected = ["NGC4088", "NGC4013", "NGC5907", "NGC7331", "NGC4183"]
    rows: list[dict[str, object]] = []
    for galaxy in inspected:
        sparc_row = sparc.loc[galaxy] if galaxy in sparc.index else None
        vflat_available = bool(sparc_row is not None and float(sparc_row["Vflat_kms"]) > 0)
        queue_rows = queue[queue["galaxy"].eq(galaxy)]
        queue_row = queue_rows.iloc[0] if not queue_rows.empty else None
        preflight_rows = preflight[preflight["galaxy"].eq(galaxy)]
        preflight_status = (
            str(preflight_rows.iloc[0]["population_transfer_status"])
            if not preflight_rows.empty
            else "NOT_IN_PREFLIGHT_CASE_TABLE"
        )

        if galaxy == "NGC4088":
            field_status = {
                "x_w": "SOURCE_FROZEN_CAVEATED_ACCEPTED",
                "q_warp": "PROTOCOL_ACCEPTED_Q_MEMORY_REVIEW",
                "sigma_warp": "PROTOCOL_FROZEN_POSITIVE_SIGN",
                "Vflat": "SOURCE_CATALOG_AVAILABLE",
                "epsilon_cross_inputs": "PARTIAL_NUMERIC_BOUND_AVAILABLE_NOT_FULLY_CLOSED",
            }
            candidate_status = "REFERENCE_EXACT_PROTOCOL_NOT_INDEPENDENT_TRANSFER"
            next_action = (
                "use as reference; acquire independent exact transfer galaxies rather "
                "than counting this row as population transfer"
            )
            source_summary = (
                f"x_w={ngc4088_freeze['x_w_formula_freeze']}; "
                f"q={ngc4088_freeze['q_warp']}; sigma={ngc4088_freeze['sigma_warp']}; "
                f"Vflat={ngc4088_freeze['vflat_km_s']}"
            )
        elif galaxy == "NGC7331":
            field_status = {
                "x_w": (
                    "FRACTIONAL_OUTER_WARP_ONSET_AVAILABLE_REPLAY_ONLY"
                    if bool(ngc7331_onset["fractional_warp_onset_available"])
                    else "MISSING"
                ),
                "q_warp": "MISSING_EXACT_Q_WARP_REVIEW",
                "sigma_warp": "MISSING_EXACT_SIGN_RULE",
                "Vflat": "SOURCE_CATALOG_AVAILABLE" if vflat_available else "MISSING",
                "epsilon_cross_inputs": "MISSING_EXACT_CROSS_TERM_OBSERVABLES",
            }
            candidate_status = "PARTIAL_EXACT_TRANSFER_CANDIDATE_SOURCE_GAPS"
            next_action = (
                "convert outer-warp replay onset into exact source-load review only if "
                "q_warp, sigma_warp, and epsilon_cross fields are source-frozen"
            )
            source_summary = (
                f"fractional_onset={ngc7331_onset['fractional_warp_onset_available']}; "
                f"approx_x_w={ngc7331_onset['approx_warp_onset_over_RHI']}"
            )
        else:
            has_numeric_warp = (
                False
                if queue_row is None
                else bool(queue_row["has_numeric_warp_activation"])
            )
            has_context = False if queue_row is None else bool(queue_row["has_overlay_context"])
            field_status = {
                "x_w": (
                    "OVERLAY_OR_WARP_ACTIVATION_AVAILABLE_NOT_EXACT_XW"
                    if has_numeric_warp
                    else "MISSING_EXACT_XW"
                ),
                "q_warp": "MISSING_EXACT_Q_WARP_REVIEW",
                "sigma_warp": (
                    "OVERLAY_CONTEXT_AVAILABLE_NOT_EXACT_SIGN_RULE"
                    if has_context
                    else "MISSING_EXACT_SIGN_RULE"
                ),
                "Vflat": "SOURCE_CATALOG_AVAILABLE" if vflat_available else "MISSING",
                "epsilon_cross_inputs": "MISSING_EXACT_CROSS_TERM_OBSERVABLES",
            }
            if has_numeric_warp and has_context and vflat_available:
                candidate_status = "ANALOGUE_WITH_ONSET_CONTEXT_NOT_EXACT_TRANSFER"
            else:
                candidate_status = "ACQUISITION_REQUIRED_FOR_EXACT_TRANSFER"
            next_action = (
                "acquire exact warp/history x_w, q_warp, sigma_warp, and cross-term "
                "observables from source-native H I/velocity-field morphology"
            )
            source_summary = (
                "no mixed queue row"
                if queue_row is None
                else str(queue_row["accepted_or_support_observables"])
            )

        accepted_exact_fields = sum(
            not field_status[field].startswith("MISSING")
            and "NOT_EXACT" not in field_status[field]
            for field in REQUIRED_FIELDS
        )
        rows.append(
            {
                "galaxy": galaxy,
                "preflight_population_transfer_status": preflight_status,
                "candidate_status": candidate_status,
                "accepted_exact_field_count": accepted_exact_fields,
                "required_exact_field_count": len(REQUIRED_FIELDS),
                "x_w_status": field_status["x_w"],
                "q_warp_status": field_status["q_warp"],
                "sigma_warp_status": field_status["sigma_warp"],
                "vflat_status": field_status["Vflat"],
                "epsilon_cross_inputs_status": field_status["epsilon_cross_inputs"],
                "source_summary": source_summary,
                "next_action": next_action,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    candidates = pd.DataFrame(rows)
    exact_ready = candidates[
        candidates["candidate_status"].eq("EXACT_TRANSFER_READY")
    ]
    partial = candidates[
        candidates["candidate_status"].str.contains("PARTIAL|ANALOGUE", regex=True)
    ]

    requirements = pd.DataFrame(
        [
            {
                "requirement_id": f"ET{i + 1}_{field.upper()}",
                "required_field": field,
                "definition": definition,
                "accepted_source_status_needed": status,
                "forbidden_inputs": (
                    "vobs residuals; endpoint score ranks; best-fit readout family; "
                    "required-S_tau diagnostic"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for i, (field, definition, status) in enumerate(
                [
                    (
                        "x_w",
                        "source-native warp/history onset fraction normalized to R_HI or an equivalent frozen source scale",
                        "numeric residual-blind onset accepted before scoring",
                    ),
                    (
                        "q_warp",
                        "source-side warp/history strength or accepted bounded strength proxy",
                        "numeric or bounded residual-blind source review",
                    ),
                    (
                        "sigma_warp",
                        "orientation/sign rule for added-readout or attenuation convention",
                        "source-side orientation/readout rule frozen before scoring",
                    ),
                    (
                        "Vflat",
                        "source/catalog asymptotic carrier value",
                        "catalog/source value independent of endpoint residuals",
                    ),
                    (
                        "epsilon_cross_inputs",
                        "orientation, side-asymmetry, memory/history, and locality inputs needed to bound cross terms",
                        "closed or explicitly carried source-side uncertainty interval",
                    ),
                ]
            )
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "exact_transfer_candidate_manifest_status": (
                    "EXACT_TRANSFER_CANDIDATE_MANIFEST_BUILT_NO_READY_INDEPENDENT_CASE"
                ),
                "n_cases": len(candidates),
                "n_reference_rows": int(
                    candidates["candidate_status"].str.contains("REFERENCE").sum()
                ),
                "n_exact_transfer_ready": len(exact_ready),
                "n_partial_or_analogue_candidates": len(partial),
                "n_requirements": len(requirements),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "population_claim_allowed": False,
                "next_required_action": (
                    "prioritize NGC7331 for exact-transfer upgrade, then search/acquire "
                    "additional source-native warp/history cases with all five fields"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    candidates.to_csv(DATA / "ngc4088_b2_exact_transfer_candidates.csv", index=False)
    requirements.to_csv(DATA / "ngc4088_b2_exact_transfer_requirements.csv", index=False)
    summary.to_csv(DATA / "ngc4088_b2_exact_transfer_candidate_summary.csv", index=False)

    report = [
        "# NGC4088 B2 Exact Transfer Candidate Manifest",
        "",
        "This manifest defines what would count as an exact transfer of the",
        "NGC4088 B2 source-load law. It does not score curves and does not use",
        "endpoint residuals.",
        "",
        "## Candidates",
        "",
        markdown_table(candidates),
        "",
        "## Requirements",
        "",
        markdown_table(requirements),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        "NGC4088 remains the exact reference case. NGC7331 is the closest current",
        "upgrade target because it has a residual-blind fractional outer-warp",
        "onset, but it still lacks exact q_warp, sigma_warp, and cross-term source",
        "observables. NGC4013, NGC5907, and NGC4183 remain useful analogues or",
        "acquisition targets, not exact B2 transfer cases.",
        "",
    ]
    (REPORTS / "ngc4088_b2_exact_transfer_candidate_manifest.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
