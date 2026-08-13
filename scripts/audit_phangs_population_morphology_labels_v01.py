#!/usr/bin/env python3
"""Audit whether the preregistered S4G component rule proves bar absence."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/phangs_population_morphology_label_audit_v01.md"

# Stuber et al. (2023), Table 1. These are source-side CO morphology labels,
# independent of the CO/H-alpha velocity contrast tested here.
PHANGS_CO_BAR_CLASS = {
    "NGC4254": {"class": "A", "agreement": 0.80, "meaning": "no bar-like feature"},
    "NGC4321": {"class": "C", "agreement": 1.00, "meaning": "clear bar-like feature"},
}


def main() -> None:
    preregistration = json.loads(
        (DATA / "phangs_population_channel_preregistration_v01.json").read_text()
    )
    decomposition = pd.read_csv(DATA / "external_s4g_disk_component_summary.csv").set_index("s4g_name")
    rows = []
    for galaxy in preregistration["eligible_galaxies"]:
        components = str(decomposition.loc[galaxy, "s4g_model_components"])
        external = PHANGS_CO_BAR_CLASS.get(galaxy)
        if external is None:
            verdict = "BAR_ABSENCE_NOT_PROVED"
            reason = "S4G fit omits an explicit BAR component, but no independent validated bar-absence label is frozen"
        elif external["class"] == "A":
            verdict = "NONBARRED_LABEL_SUPPORTED"
            reason = "independent PHANGS CO morphology supports absence of a bar-like feature"
        else:
            verdict = "NONBARRED_LABEL_CONTRADICTED"
            reason = "independent PHANGS CO morphology identifies a clear bar-like feature"
        rows.append({
            "galaxy": galaxy,
            "s4g_fitted_components": components,
            "phangs_co_bar_class": None if external is None else external["class"],
            "phangs_inspector_agreement": None if external is None else external["agreement"],
            "verdict": verdict,
            "reason": reason,
            "confirmatory_endpoint": galaxy in preregistration["confirmatory_unopened_galaxies"],
        })
    confirmatory = [row for row in rows if row["confirmatory_endpoint"]]
    integrity_pass = all(row["verdict"] == "NONBARRED_LABEL_SUPPORTED" for row in confirmatory)
    result = {
        "schema": "phangs_population_morphology_label_audit_v01",
        "status": "CONFIRMATORY_MORPHOLOGY_LABEL_INTEGRITY_FAILED",
        "rows": rows,
        "confirmatory_label_integrity_pass": integrity_pass,
        "source_rule_error": (
            "absence of a fitted BAR component in one S4G decomposition model was treated as proof of physical bar absence"
        ),
        "source_reference": "Stuber et al. 2023, The Gas Morphology of Nearby Star-Forming Galaxies, Table 1",
        "source_url": "https://arxiv.org/abs/2305.17172",
        "endpoint_timing": "audit performed after the confirmatory tracer contrasts were opened; it can demote but cannot replace endpoints",
        "replacement_endpoint_allowed": False,
        "claim_boundary": (
            "source-label integrity audit; it preserves the raw frozen statistic but blocks morphology-conditioned "
            "channel promotion and any post-result replacement selection"
        ),
    }
    (DATA / "phangs_population_morphology_label_audit_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    table = "\n".join(
        f"| {row['galaxy']} | {row['s4g_fitted_components']} | {row['phangs_co_bar_class']} | "
        f"{row['phangs_inspector_agreement']} | {row['verdict']} |"
        for row in rows
    )
    REPORT.write_text(
        "# PHANGS population morphology-label audit v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "| galaxy | S4G fit components | PHANGS CO bar class | agreement | verdict |\n"
        "| --- | --- | --- | --- | --- |\n"
        f"{table}\n\n"
        "The preregistration used absence of a fitted `BAR` component as if it proved "
        "physical bar absence. It does not. NGC4321 is PHANGS class `C` with unanimous "
        "agreement, while IC5332 has no validated label in that catalogue. The already "
        "opened numerical result is preserved, but no endpoint replacement or morphology-"
        "conditioned channel promotion is allowed.\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
