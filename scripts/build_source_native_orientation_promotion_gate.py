#!/usr/bin/env python3
"""Build the source-native orientation promotion gate for Paper 8.

This is a residual-blind audit.  It does not score endpoints and does not
choose signs from rotation residuals.  It asks whether the predeclared
readout-orientation signs have enough source-native support to be promoted
inside the current bridge geometry.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "source_native_orientation_promotion_gate_not_endpoint"

FAMILY_REQUIREMENTS = {
    "K_compact_finite": {
        "required_statuses": {"SOURCE_CANDIDATE_COMPACT_READY"},
        "source_count_column": "n_source_candidate_components",
        "minimum_source_count": 1,
        "orientation": 1.0,
        "orientation_role": "positive finite-source residual orientation",
        "promotion_basis": "compact/core finite-support source candidate",
    },
    "K_scale_tail_spiral": {
        "required_statuses": {"SOURCE_CANDIDATE_HI_TAIL_READY"},
        "source_count_column": "n_source_candidate_components",
        "minimum_source_count": 1,
        "orientation": 1.0,
        "orientation_role": "positive n=2 tail/closure-source orientation",
        "promotion_basis": "HI/tail source candidate",
    },
    "K_exponential_disk": {
        "required_statuses": {"SOURCE_CANDIDATE_S4G_SCALE_READY"},
        "source_count_column": "n_source_candidate_components",
        "minimum_source_count": 1,
        "orientation": -1.0,
        "orientation_role": "negative smoothing/counter-readout orientation",
        "promotion_basis": "S4G disk-scale source candidate",
    },
    "K_thick_flared": {
        "required_statuses": {"SOURCE_CANDIDATE_VELOCITY_FIELD_READY"},
        "source_count_column": "n_velocity_field_components",
        "minimum_source_count": 1,
        "orientation": -1.0,
        "orientation_role": "negative projection/vertical smoothing orientation",
        "promotion_basis": "velocity-field or vertical-structure source candidate",
    },
}


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    constants = pd.read_csv(DATA / "tau_side_source_normalization_derivation_constants.csv")
    component_audit = pd.read_csv(
        DATA / "morphology_information_gain_l2_weight_freeze_component_audit.csv"
    )
    readiness = pd.read_csv(DATA / "morphology_information_gain_l2_weight_freeze_readiness.csv")
    return constants, component_audit, readiness


def build_family_gate(constants: pd.DataFrame, component_audit: pd.DataFrame) -> pd.DataFrame:
    orientation = constants.loc[constants["constant_type"] == "orientation_sign"].copy()
    rows = []
    for _, row in orientation.iterrows():
        family = row["constant_key"]
        req = FAMILY_REQUIREMENTS[family]
        family_components = component_audit.loc[component_audit["component_family"] == family]
        status_counts = family_components["component_evidence_status"].value_counts().to_dict()
        n_required = int(
            family_components["component_evidence_status"].isin(req["required_statuses"]).sum()
        )
        n_proxy = int(
            family_components["component_evidence_status"].eq("PROXY_OR_PARTIAL_SOURCE_ONLY").sum()
        )
        n_missing = int(
            family_components["component_evidence_status"].eq("MISSING_SOURCE_SUPPORT").sum()
        )
        sign_matches = float(row["constant_value"]) == float(req["orientation"])
        source_ready = n_required >= int(req["minimum_source_count"])
        if sign_matches and source_ready:
            promotion_status = "PROMOTED_WITHIN_CURRENT_BRIDGE_READOUT_GEOMETRY"
            weakest_step = "needs covariant/source-native variational promotion before physical acceptance"
        elif not source_ready:
            promotion_status = "BLOCKED_SOURCE_NATIVE_ORIENTATION_EVIDENCE_MISSING"
            weakest_step = "required source-native orientation evidence is not assembled"
        else:
            promotion_status = "BLOCKED_SIGN_MISMATCH_WITH_CURRENT_BRIDGE_RULE"
            weakest_step = "predeclared sign disagrees with family promotion rule"

        rows.append(
            {
                "component_family": family,
                "predeclared_orientation_sign": float(row["constant_value"]),
                "expected_orientation_sign": float(req["orientation"]),
                "sign_matches_family_rule": sign_matches,
                "orientation_role": req["orientation_role"],
                "promotion_basis": req["promotion_basis"],
                "required_statuses": ";".join(sorted(req["required_statuses"])),
                "n_components": int(len(family_components)),
                "n_required_source_components": n_required,
                "n_proxy_components": n_proxy,
                "n_missing_components": n_missing,
                "status_counts": ";".join(f"{k}:{v}" for k, v in sorted(status_counts.items())),
                "promotion_status": promotion_status,
                "endpoint_scores_computed": False,
                "uses_vobs_or_residual": False,
                "weakest_step": weakest_step,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows).sort_values("component_family")


def build_component_gate(
    family_gate: pd.DataFrame, component_audit: pd.DataFrame, readiness: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    family_status = dict(zip(family_gate["component_family"], family_gate["promotion_status"]))
    family_promoted = {
        row["component_family"]: row["promotion_status"]
        == "PROMOTED_WITHIN_CURRENT_BRIDGE_READOUT_GEOMETRY"
        for _, row in family_gate.iterrows()
    }
    component_rows = []
    for _, row in component_audit.iterrows():
        family = row["component_family"]
        active = float(row["component_weight"]) > 0.0
        source_ready = str(row["component_evidence_status"]).startswith("SOURCE_CANDIDATE")
        component_promoted = active and bool(family_promoted.get(family, False)) and source_ready
        if not active:
            status = "INACTIVE_COMPONENT_NOT_BLOCKING"
        elif component_promoted:
            status = "COMPONENT_ORIENTATION_PROMOTED"
        elif not family_promoted.get(family, False):
            status = "BLOCKED_FAMILY_ORIENTATION_NOT_PROMOTED"
        elif not source_ready:
            status = "BLOCKED_COMPONENT_SOURCE_NOT_ACCEPTED"
        else:
            status = "BLOCKED_COMPONENT_ORIENTATION_UNKNOWN"
        component_rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "component_family": family,
                "component_weight": float(row["component_weight"]),
                "component_evidence_status": row["component_evidence_status"],
                "family_promotion_status": family_status.get(family, "UNKNOWN"),
                "component_orientation_status": status,
                "endpoint_scores_computed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    component_gate = pd.DataFrame(component_rows).sort_values(
        ["split", "galaxy", "component_family"]
    )

    promoted_active = component_gate.loc[
        component_gate["component_orientation_status"].eq("COMPONENT_ORIENTATION_PROMOTED")
    ]
    blocked_active = component_gate.loc[
        component_gate["component_orientation_status"].str.startswith("BLOCKED")
    ]
    galaxy_rows = []
    for _, row in readiness.iterrows():
        sub = component_gate.loc[
            (component_gate["galaxy"] == row["galaxy"])
            & (component_gate["component_weight"] > 0.0)
        ]
        all_promoted = len(sub) > 0 and sub["component_orientation_status"].eq(
            "COMPONENT_ORIENTATION_PROMOTED"
        ).all()
        if all_promoted:
            gate_status = "ORIENTATION_PROMOTION_READY_FOR_ACTIVE_COMPONENTS"
        else:
            gate_status = "ORIENTATION_PROMOTION_BLOCKED_FOR_ACTIVE_COMPONENTS"
        galaxy_rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "n_active_components": int(len(sub)),
                "n_promoted_active_components": int(
                    sub["component_orientation_status"].eq("COMPONENT_ORIENTATION_PROMOTED").sum()
                ),
                "n_blocked_active_components": int(
                    sub["component_orientation_status"].str.startswith("BLOCKED").sum()
                ),
                "orientation_gate_status": gate_status,
                "endpoint_freeze_allowed": False,
                "endpoint_scores_computed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    galaxy_gate = pd.DataFrame(galaxy_rows).sort_values(["split", "galaxy"])
    return component_gate, galaxy_gate


def summarize(
    family_gate: pd.DataFrame, component_gate: pd.DataFrame, galaxy_gate: pd.DataFrame
) -> pd.DataFrame:
    rows = []
    for split, sub in galaxy_gate.groupby("split"):
        comp = component_gate.loc[component_gate["split"] == split]
        rows.append(summary_row(split, sub, comp, family_gate))
    all_row = summary_row("all", galaxy_gate, component_gate, family_gate)
    return pd.concat([pd.DataFrame([all_row]), pd.DataFrame(rows)], ignore_index=True)


def summary_row(
    split: str, galaxies: pd.DataFrame, components: pd.DataFrame, family_gate: pd.DataFrame
) -> dict[str, object]:
    active = components.loc[components["component_weight"] > 0.0]
    return {
        "split": split,
        "n_galaxies": int(len(galaxies)),
        "n_family_orientation_promoted": int(
            family_gate["promotion_status"].eq(
                "PROMOTED_WITHIN_CURRENT_BRIDGE_READOUT_GEOMETRY"
            ).sum()
        ),
        "n_family_orientation_blocked": int(
            family_gate["promotion_status"].str.startswith("BLOCKED").sum()
        ),
        "n_active_components": int(len(active)),
        "n_promoted_active_components": int(
            active["component_orientation_status"].eq("COMPONENT_ORIENTATION_PROMOTED").sum()
        ),
        "n_blocked_active_components": int(
            active["component_orientation_status"].str.startswith("BLOCKED").sum()
        ),
        "n_galaxies_orientation_ready": int(
            galaxies["orientation_gate_status"].eq(
                "ORIENTATION_PROMOTION_READY_FOR_ACTIVE_COMPONENTS"
            ).sum()
        ),
        "n_galaxies_orientation_blocked": int(
            galaxies["orientation_gate_status"].eq(
                "ORIENTATION_PROMOTION_BLOCKED_FOR_ACTIVE_COMPONENTS"
            ).sum()
        ),
        "endpoint_scores_computed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda value: f"{value:.6g}")
        else:
            display[col] = display[col].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def write_report(
    family_gate: pd.DataFrame,
    component_gate: pd.DataFrame,
    galaxy_gate: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    full = summary.loc[summary["split"] == "all"].iloc[0]
    lines = [
        "# Source-Native Orientation Promotion Gate",
        "",
        "This audit asks whether the predeclared source-normalization orientation",
        "signs can be promoted from theory-conditional bridge signs to",
        "source-native readout-orientation candidates. It computes no endpoint",
        "scores and uses no rotation residuals.",
        "",
        "## Verdict",
        "",
        f"- Family orientations promoted: {int(full['n_family_orientation_promoted'])}/4",
        f"- Family orientations blocked: {int(full['n_family_orientation_blocked'])}/4",
        f"- Active components promoted: {int(full['n_promoted_active_components'])}/{int(full['n_active_components'])}",
        f"- Active components blocked: {int(full['n_blocked_active_components'])}/{int(full['n_active_components'])}",
        f"- Galaxies orientation-ready: {int(full['n_galaxies_orientation_ready'])}/{int(full['n_galaxies'])}",
        f"- Galaxies orientation-blocked: {int(full['n_galaxies_orientation_blocked'])}/{int(full['n_galaxies'])}",
        "",
        "The proxy-gate blocker has already been resolved by the conservative",
        "E_tau readout-admission product. This audit shows the next blocker:",
        "orientation promotion is partially source-native at the family level,",
        "but still blocked for galaxies whose active components require the",
        "thick/flared vertical channel or have proxy/missing component evidence.",
        "",
        "## Family Orientation Gate",
        "",
        markdown_table(family_gate),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Active Component Status Counts",
        "",
        markdown_table(
            component_gate.loc[component_gate["component_weight"] > 0.0]
            .groupby(["component_family", "component_orientation_status"])
            .size()
            .reset_index(name="n_components")
        ),
        "",
        "## Claim Boundary",
        "",
        "This gate is a source-native promotion audit, not empirical validation.",
        "A promoted orientation is still a current-bridge readout-orientation",
        "candidate, not a covariant Tau-side physical law. Endpoint use remains",
        "blocked until orientation, per-galaxy q_i evidence, and",
        "morphology-memory/projection evidence are accepted residual-blindly.",
    ]
    (REPORTS / "source_native_orientation_promotion_gate.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    constants, component_audit, readiness = load_inputs()
    family_gate = build_family_gate(constants, component_audit)
    component_gate, galaxy_gate = build_component_gate(family_gate, component_audit, readiness)
    summary = summarize(family_gate, component_gate, galaxy_gate)
    family_gate.to_csv(DATA / "source_native_orientation_family_gate.csv", index=False)
    component_gate.to_csv(DATA / "source_native_orientation_component_gate.csv", index=False)
    galaxy_gate.to_csv(DATA / "source_native_orientation_galaxy_gate.csv", index=False)
    summary.to_csv(DATA / "source_native_orientation_promotion_summary.csv", index=False)
    write_report(family_gate, component_gate, galaxy_gate, summary)
    print("PAPER8_SOURCE_NATIVE_ORIENTATION_PROMOTION_GATE_COMPLETE")


if __name__ == "__main__":
    main()
