#!/usr/bin/env python3
"""Audit the foundation gates that must hold before a Paper 8 endpoint run.

This script does not validate Tau Core and does not run a real SPARC endpoint.
It checks whether the public package is internally consistent about the
Paper 1-3 inheritance, leakage boundaries, morphology-family registry, and
remaining blockers for the morphology-matched forward-readout gate.
"""

from __future__ import annotations

import csv
import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
SOURCE = ROOT / "paper8_submission_source"
REPORTS = ROOT / "reports"

PAPER1 = Path("/Users/jolcsak/Projects/sparc-residual-disturbance-paper1")
PAPER2 = Path("/Users/jolcsak/Projects/sparc-residual-disturbance-paper2")
PAPER3 = Path("/Users/jolcsak/Projects/sparc-residual-disturbance-paper3")


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8")


def add(rows: list[dict[str, str]], gate: str, status: str, evidence: str, action: str) -> None:
    rows.append(
        {
            "gate": gate,
            "status": status,
            "evidence": evidence,
            "required_next_action": action,
        }
    )


def audit() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    paper8_tex = SOURCE / "main.tex"
    readme = ROOT / "README.md"
    registry = pd.read_csv(DATA / "morphology_family_registry.csv")
    schema = pd.read_csv(DATA / "forward_readout_gate_schema.csv")
    crosswalk = pd.read_csv(DATA / "paper3_candidate_control_crosswalk.csv")
    readiness = pd.read_csv(DATA / "paper8_readiness_table.csv")

    paper_repos = {
        "Paper 1": PAPER1 / "paper1_submission_source" / "main.tex",
        "Paper 2": PAPER2 / "paper2_submission_source" / "main.tex",
        "Paper 3": PAPER3 / "paper3_submission_source" / "main.tex",
    }
    missing = [name for name, path in paper_repos.items() if not path.exists()]
    add(
        rows,
        "paper1_3_local_context",
        "PASS" if not missing else "BLOCKED",
        "local Paper 1-3 manuscripts found" if not missing else f"missing: {', '.join(missing)}",
        "Keep Paper 8 citations pointed to archived Paper 1-3 packages.",
    )

    paper3_tex = paper_repos["Paper 3"]
    paper3_text = paper3_tex.read_text(encoding="utf-8")
    paper3_lower = paper3_text.lower()
    paper3_bridge_ok = (
        "inverse residual-absorption diagnostic" in paper3_lower
        and "endpoint-conditioned" in paper3_lower
        and "predictive validation gate" in paper3_lower
        and "may not use vobs residuals" in paper3_lower
        and "required $S_\\tau$" in paper3_text
    )
    add(
        rows,
        "paper3_inverse_to_forward_bridge",
        "PASS" if paper3_bridge_ok else "REVIEW",
        "Paper 3 states required-S_tau is inverse and asks for a frozen predictive gate.",
        "Paper 8 may use Paper 3 as the direct launch point, but must not use required-S_tau as a predictor.",
    )

    forbidden_phrases = [
        "Tau Core is proven",
        "has already beaten MOND/RAR",
        "MOND, RAR, or Newtonian baryonic baselines have been superseded",
        "universal weak-field galaxy law has been derived",
    ]
    forbidden_present = [phrase for phrase in forbidden_phrases if phrase in paper8_tex.read_text(encoding="utf-8")]
    add(
        rows,
        "claim_boundary",
        "PASS" if forbidden_present else "REVIEW",
        "Forbidden claims appear only inside explicit non-claim lists." if forbidden_present else "No explicit forbidden-claim list detected.",
        "Keep all empirical wording at protocol/gate status until real matched-family endpoints are run.",
    )

    required_components = {
        "residual-blind morphology label",
        "formula-shell selection",
        "geometry and amplitude discipline",
        "matched-vs-wrong family endpoint",
        "shuffled-K null",
        "baseline comparison",
    }
    found_components = set(schema["gate_component"])
    add(
        rows,
        "forward_gate_schema_complete",
        "PASS" if required_components <= found_components else "BLOCKED",
        f"{len(found_components)} schema rows present: {', '.join(schema['gate_component'])}",
        "Before real endpoint work, materialize every required artifact named in the schema.",
    )

    leakage_terms = ["required S_tau", "endpoint", "post-hoc", "residual"]
    leakage_ok = all(
        any(term in str(value) for value in crosswalk["forbidden_inputs"]) for term in leakage_terms
    )
    add(
        rows,
        "leakage_boundary",
        "PASS" if leakage_ok else "REVIEW",
        "Crosswalk forbids required S_tau, endpoint residual gain, post-hoc family choice, and residual-selected morphology.",
        "Add the same forbidden-input discipline to any future endpoint-run manifest.",
    )

    statuses = set(registry["sparc_first_pass_status"])
    family_count_ok = len(registry) == 7 and {
        "1D rotation-curve testable",
        "1D proxy testable",
        "velocity-field preferred",
    } <= statuses
    add(
        rows,
        "morphology_family_registry",
        "PASS" if family_count_ok else "REVIEW",
        f"{len(registry)} families; statuses: {', '.join(sorted(statuses))}",
        "Promote only 1D-testable/proxy families into the first SPARC endpoint; keep m=1/m=2 as velocity-field follow-up.",
    )

    shell_unit_risk = registry["formula_shell"].str.contains("A_K|I_infty|sigma_morph").all()
    add(
        rows,
        "formula_shell_dimensional_readiness",
        "REVIEW" if shell_unit_risk else "BLOCKED",
        "Formula shells expose amplitudes/source terms but do not yet define a unit-normalized amplitude policy.",
        "Write amplitude_policy.csv before empirical scoring; state units and allowed bounds for A_K, R_c, R_d, R_ring, and kernel widths.",
    )

    real_endpoint_status = readiness.loc[
        readiness["item"] == "Real matched-vs-wrong family endpoint", "status"
    ].iloc[0]
    labels_status = readiness.loc[
        readiness["item"] == "Residual-blind morphology labels for full endpoint sample", "status"
    ].iloc[0]
    component_status = readiness.loc[
        readiness["item"] == "Accepted source-native component tables for all candidates", "status"
    ].iloc[0]
    blocked = [real_endpoint_status, labels_status, component_status]
    add(
        rows,
        "empirical_endpoint_readiness",
        "BLOCKED" if any(value != "available" for value in blocked) else "PASS",
        f"component tables={component_status}; morphology labels={labels_status}; endpoint={real_endpoint_status}",
        "Do not claim empirical pass. Next concrete work is residual-blind label manifest plus component-table intake.",
    )

    archive_path = ROOT / "arxiv_submission_source.zip"
    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())
    arxiv_ok = {"main.tex", "refs.bib"} <= names and "main.pdf" not in names
    add(
        rows,
        "arxiv_source_package",
        "PASS" if arxiv_ok else "BLOCKED",
        f"{archive_path.name} includes main.tex and refs.bib; compiled PDF excluded.",
        "Optional hardening: include generated .bbl if a submission venue requires bibliography without BibTeX.",
    )

    tests_ok = (ROOT / "paper8_submission_source" / "main.pdf").exists() and contains(
        readme, "python scripts/reproduce.py"
    )
    add(
        rows,
        "one_command_reproducibility_path",
        "PASS" if tests_ok else "BLOCKED",
        "README documents python scripts/reproduce.py and compiled PDF exists.",
        "Keep reproduce.py as the authoritative pre-submission command.",
    )

    return rows


def write_outputs(rows: list[dict[str, str]]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    csv_path = DATA / "paper8_foundation_audit.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["gate", "status", "evidence", "required_next_action"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    status_counts = pd.DataFrame(rows)["status"].value_counts().to_dict()
    lines = [
        "# Paper 8 Foundation Audit",
        "",
        "This audit checks whether Paper 8 is ready to serve as a claim-bounded",
        "preparation paper for the morphology-matched forward-readout endpoint.",
        "It does not run a real SPARC matched-family score and does not validate",
        "Tau Core.",
        "",
        "## Verdict",
        "",
        f"- PASS gates: {status_counts.get('PASS', 0)}",
        f"- REVIEW gates: {status_counts.get('REVIEW', 0)}",
        f"- BLOCKED gates: {status_counts.get('BLOCKED', 0)}",
        "",
        "The package is suitable as a theory-method/reproducibility preparation",
        "paper. It is not yet suitable for an empirical discovery claim because",
        "the residual-blind morphology-label manifest, amplitude policy, accepted",
        "component tables, and real matched-vs-wrong endpoint remain open.",
        "",
        "## Gate Results",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"### {row['gate']}",
                "",
                f"- Status: {row['status']}",
                f"- Evidence: {row['evidence']}",
                f"- Required next action: {row['required_next_action']}",
                "",
            ]
        )
    (REPORTS / "paper8_foundation_audit.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {csv_path}")
    print(f"wrote {REPORTS / 'paper8_foundation_audit.md'}")


def main() -> None:
    rows = audit()
    write_outputs(rows)
    counts = pd.DataFrame(rows)["status"].value_counts().to_dict()
    print(f"PAPER8_FOUNDATION_AUDIT_COMPLETE {counts}")


if __name__ == "__main__":
    main()
