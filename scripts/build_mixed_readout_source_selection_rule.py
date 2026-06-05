#!/usr/bin/env python3
"""Build a residual-blind source rule for mixed readout selection.

The rule is deliberately source-side only. It may promote a galaxy to a
mixed-readout formula-freeze worklist, but it does not authorize endpoint
scoring and it does not use rotation residuals, RMSE ranks, or best-family
diagnostics as label inputs.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "mixed_readout_source_selection_rule_not_endpoint"


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


def bool_text(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def source_value(row: pd.Series, key: str, default: object = "") -> object:
    return row[key] if key in row.index and pd.notna(row[key]) else default


def build_ngc4013_case() -> dict[str, object]:
    compact = pd.read_csv(DATA / "ngc4013_compact_overlay_source_summary.csv").iloc[0]
    preflight = pd.read_csv(DATA / "ngc4013_warp_overlay_preflight_summary.csv").iloc[0]
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    sparc_row = sparc.loc[sparc["Galaxy"] == "NGC4013"].iloc[0]

    has_smooth_component = "edgedisk" in str(compact["s4g_components"]).lower()
    has_disk_scale = pd.notna(sparc_row["Rdisk_kpc"]) and float(sparc_row["Rdisk_kpc"]) > 0.0
    compact_rejected = str(compact["compact_lane_decision"]) == "COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED"
    has_warp_window = pd.notna(preflight["warp_onset_kpc"])
    has_vertical_overlay = (
        pd.notna(compact["s4g_edge_disk_h_over_r"])
        and float(compact["s4g_edge_disk_h_over_r"]) > 0.0
    )
    has_extended_component = (
        pd.notna(compact["extended_component_mass_fraction"])
        and float(compact["extended_component_mass_fraction"]) > 0.0
    )
    has_lag_context = "lag" in str(source_value(preflight, "lag_context", "")).lower()

    smooth_carrier_gate = has_smooth_component and has_disk_scale
    overlay_modifier_gate = has_warp_window and (
        has_vertical_overlay or has_extended_component or has_lag_context
    )
    anti_compact_gate = compact_rejected
    forbidden_inputs_gate = True
    source_rule_pass = (
        smooth_carrier_gate
        and overlay_modifier_gate
        and anti_compact_gate
        and forbidden_inputs_gate
    )

    return {
        "galaxy": "NGC4013",
        "candidate_mixed_readout": "K_expdisk_warp_vertical_overlay",
        "carrier_rule": "smooth_disk_carrier_from_source_component_and_disk_scale",
        "overlay_rule": "source_windowed_warp_vertical_lag_overlay",
        "smooth_component_source": str(compact["s4g_components"]),
        "disk_scale_kpc": float(sparc_row["Rdisk_kpc"]),
        "compact_lane_decision": str(compact["compact_lane_decision"]),
        "warp_onset_kpc": float(preflight["warp_onset_kpc"]),
        "h_over_r": float(compact["s4g_edge_disk_h_over_r"]),
        "extended_component_fraction": float(compact["extended_component_mass_fraction"]),
        "lag_context": str(source_value(preflight, "lag_context", "accepted_context")),
        "smooth_carrier_gate": smooth_carrier_gate,
        "overlay_modifier_gate": overlay_modifier_gate,
        "anti_compact_gate": anti_compact_gate,
        "forbidden_inputs_excluded_gate": forbidden_inputs_gate,
        "source_rule_pass": source_rule_pass,
        "formula_freeze_required": True,
        "endpoint_scores_allowed": False,
        "diagnostic_scores_allowed": True,
        "case_status": (
            "MIXED_SOURCE_RULE_PASS_FORMULA_FREEZE_REQUIRED"
            if source_rule_pass
            else "MIXED_SOURCE_RULE_BLOCKED"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    protocol = pd.DataFrame(
        [
            {
                "rule_id": "MXR1_SMOOTH_CARRIER",
                "rule_kind": "required_source_gate",
                "definition": "A smooth disk carrier is allowed only when source-side disk/decomposition evidence gives a disk-like component and a numeric disk scale before endpoint scoring.",
                "allowed_inputs": "S4G/SPARC/decomposition disk component fields; source-native disk scale",
                "forbidden_inputs": "vobs residuals; RMSE ranks; best Tau family; required S_tau diagnostics",
                "endpoint_effect": "does not score; only allows mixed formula-freeze worklist entry",
            },
            {
                "rule_id": "MXR2_OVERLAY_MODIFIER",
                "rule_kind": "required_source_gate",
                "definition": "A source-windowed overlay modifier is allowed only with residual-blind warp/projection/vertical/lag source evidence and at least one numeric activation or amplitude field.",
                "allowed_inputs": "warp onset; projection/warp window; h/R; extended-component fraction; lag-map context",
                "forbidden_inputs": "endpoint residual sign; post-hoc radial error pattern",
                "endpoint_effect": "does not score; only supplies the formula-freeze target",
            },
            {
                "rule_id": "MXR3_COMPACT_ONLY_VETO",
                "rule_kind": "required_source_gate",
                "definition": "A mixed smooth+overlay label can replace a compact-only proxy only if compact-only support is absent, rejected, or source-caveated before scoring.",
                "allowed_inputs": "bulge/decomposition review; compact support radius review",
                "forbidden_inputs": "compact family RMSE weakness",
                "endpoint_effect": "prevents using mixed label as a residual-rescue path",
            },
            {
                "rule_id": "MXR4_SCORE_EXCLUSION",
                "rule_kind": "claim_boundary_gate",
                "definition": "Diagnostic mixed scores may be recorded only as motivation for a future source-blind rule; they cannot promote the label.",
                "allowed_inputs": "source ledgers and frozen source fields",
                "forbidden_inputs": "mixed diagnostic RMSE as label evidence",
                "endpoint_effect": "keeps all promoted cases formula-freeze-blocked until a separate freeze gate passes",
            },
        ]
    )
    protocol["claim_boundary"] = CLAIM_BOUNDARY

    cases = pd.DataFrame([build_ngc4013_case()])
    n_cases = len(cases)
    n_pass = int(cases["source_rule_pass"].sum())
    n_endpoint_allowed = int(cases["endpoint_scores_allowed"].sum())

    summary = pd.DataFrame(
        [
            {
                "rule_status": "MIXED_SOURCE_RULE_PREDECLARED_NOT_ENDPOINT",
                "n_cases_evaluated": n_cases,
                "n_source_rule_pass": n_pass,
                "n_endpoint_scores_allowed": n_endpoint_allowed,
                "endpoint_scores_allowed": False,
                "formula_freeze_required_for_passing_cases": True,
                "diagnostic_scores_used_as_label_input": False,
                "next_required_gate": "mixed_readout_formula_freeze_gate",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    protocol.to_csv(DATA / "mixed_readout_source_selection_protocol.csv", index=False)
    cases.to_csv(DATA / "mixed_readout_source_selection_cases.csv", index=False)
    summary.to_csv(DATA / "mixed_readout_source_selection_summary.csv", index=False)

    report = [
        "# Mixed Readout Source-Selection Rule",
        "",
        "This report predeclares a residual-blind source rule for selecting a",
        "mixed smooth-carrier plus source-windowed overlay readout candidate.",
        "It does not authorize endpoint scoring. Passing cases move only to a",
        "formula-freeze gate.",
        "",
        "## Protocol",
        "",
        markdown_table(protocol),
        "",
        "## Evaluated Cases",
        "",
        markdown_table(cases),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "A passing source-rule case means that the mixed readout is supported by",
        "residual-blind source evidence beyond intuition. It is not an empirical",
        "validation and not an endpoint result until a separate formula-freeze",
        "gate passes and a separate scoring script reads the frozen manifest.",
    ]
    (REPORTS / "mixed_readout_source_selection_rule.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
