#!/usr/bin/env python3
"""Generate compact Paper 8 derived tables and figures.

The numbers here are protocol fixtures, not empirical validation results.
They encode the morphology-matched forward-readout gate that extends the
Paper 1-3 candidate/control sequence.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
FIGURES = ROOT / "figures"
SOURCE_FIGURES = ROOT / "paper8_submission_source" / "figures"


MORPHOLOGY_FAMILIES = [
    {
        "family_id": "K_scale_tail_spiral",
        "morphology_label": "scale-tail spiral / extended low-surface-brightness disk",
        "formula_shell": "sigma_morph(R) ~ A_K / (R + R_c)^2 with finite inner cutoff",
        "primary_readout": "delta_g^K_R from Poisson-like closure source tail",
        "sparc_first_pass_status": "1D rotation-curve testable",
        "caveat": "amplitude must be frozen or tightly bounded before endpoint scoring",
    },
    {
        "family_id": "K_exponential_disk",
        "morphology_label": "regular exponential disk",
        "formula_shell": "sigma_morph(R) ~ A_K exp(-R/R_d)",
        "primary_readout": "finite-support disk-like solved response",
        "sparc_first_pass_status": "1D rotation-curve testable",
        "caveat": "degenerate with baryonic scale-length if not residual-blind",
    },
    {
        "family_id": "K_compact_finite",
        "morphology_label": "compact finite source / centrally concentrated support",
        "formula_shell": "I_morph(R) saturates, delta_g^K_R ~ -I_infty/R^2",
        "primary_readout": "Newtonian-like finite-tail residual correction",
        "sparc_first_pass_status": "1D rotation-curve testable",
        "caveat": "should not be overread as a universal dark component",
    },
    {
        "family_id": "K_ring_resonance",
        "morphology_label": "ring / resonance feature",
        "formula_shell": "sigma_morph(R) localized near R_ring with width w_ring",
        "primary_readout": "localized radial response feature",
        "sparc_first_pass_status": "1D proxy testable",
        "caveat": "requires morphology-fixed ring radius, not residual-selected radius",
    },
    {
        "family_id": "K_thick_flared",
        "morphology_label": "thick or flared disk",
        "formula_shell": "sigma_morph(R,z) projected through thickness/flaring kernel",
        "primary_readout": "geometry-smoothed radial response",
        "sparc_first_pass_status": "1D proxy testable",
        "caveat": "vertical geometry is only proxied in SPARC-like 1D curves",
    },
    {
        "family_id": "K_barred_m2",
        "morphology_label": "barred spiral / m=2 non-axisymmetric mode",
        "formula_shell": "sigma_morph(R,phi) includes m=2 harmonic readout",
        "primary_readout": "azimuthal velocity-field response, not only 1D curve",
        "sparc_first_pass_status": "velocity-field preferred",
        "caveat": "1D SPARC use is caveat/proxy only",
    },
    {
        "family_id": "K_lopsided_m1",
        "morphology_label": "lopsided / m=1 asymmetric mode",
        "formula_shell": "sigma_morph(R,phi) includes m=1 harmonic readout",
        "primary_readout": "asymmetric velocity-field response",
        "sparc_first_pass_status": "velocity-field preferred",
        "caveat": "1D SPARC use is caveat/proxy only",
    },
]


CANDIDATE_CONTROL_CROSSWALK = [
    {
        "paper3_role": "positive anchor",
        "galaxy": "DDO126",
        "paper3_status": "fixed TPG public endpoint anchor",
        "paper8_forward_role": "matched-family candidate once morphology label is residual-blind",
        "allowed_inputs": "morphology label, baryonic components, geometry proxies",
        "forbidden_inputs": "required S_tau, endpoint residual gain, post-hoc family choice",
    },
    {
        "paper3_role": "quiet control",
        "galaxy": "DDO50",
        "paper3_status": "Newtonian-best or near-quiet control",
        "paper8_forward_role": "control object for false-positive suppression",
        "allowed_inputs": "same frozen morphology and baryonic inputs as candidates",
        "forbidden_inputs": "endpoint-conditioned family switching",
    },
    {
        "paper3_role": "geometry stress",
        "galaxy": "WLM",
        "paper3_status": "geometry/observability stress context",
        "paper8_forward_role": "observability-caveated endpoint row",
        "allowed_inputs": "morphology and observability covariates declared before scoring",
        "forbidden_inputs": "using caveat label to discard a bad endpoint after scoring",
    },
    {
        "paper3_role": "candidate ladder",
        "galaxy": "DDO168",
        "paper3_status": "specificity-support example after repair",
        "paper8_forward_role": "candidate/control ladder consistency row",
        "allowed_inputs": "accepted component table or frozen public reconstruction",
        "forbidden_inputs": "inverse S_tau as predictor",
    },
    {
        "paper3_role": "countercontrol",
        "galaxy": "DDO154",
        "paper3_status": "near-one control/countercontrol",
        "paper8_forward_role": "rank-sensitive wrong-family stress row",
        "allowed_inputs": "predeclared morphology label and candidate family set",
        "forbidden_inputs": "residual-selected morphology class",
    },
]


FORWARD_GATE_SCHEMA = [
    {
        "step": 1,
        "gate_component": "residual-blind morphology label",
        "required_artifact": "morphology_labels_predeclared.csv",
        "pass_condition": "K_g assigned before reading forward residual endpoints",
    },
    {
        "step": 2,
        "gate_component": "formula-shell selection",
        "required_artifact": "morphology_family_registry.csv",
        "pass_condition": "family shell selected from K_g, not from endpoint fit quality",
    },
    {
        "step": 3,
        "gate_component": "geometry and amplitude discipline",
        "required_artifact": "amplitude_policy.csv",
        "pass_condition": "geometry fixed from morphology; amplitude frozen or tightly bounded",
    },
    {
        "step": 4,
        "gate_component": "matched-vs-wrong family endpoint",
        "required_artifact": "matched_wrong_family_scores.csv",
        "pass_condition": "matched family improves residual structure over wrong families",
    },
    {
        "step": 5,
        "gate_component": "shuffled-K null",
        "required_artifact": "shuffled_label_null.csv",
        "pass_condition": "matched score exceeds shuffled morphology-label distribution",
    },
    {
        "step": 6,
        "gate_component": "baseline comparison",
        "required_artifact": "baseline_comparison_scores.csv",
        "pass_condition": "reported against Newtonian baryonic, MOND-simple, empirical RAR",
    },
]


SYNTHETIC_DEMO = [
    {"condition": "matched_family", "rms": 0.111, "rank": 1},
    {"condition": "wrong_family_mean", "rms": 0.156, "rank": 3},
    {"condition": "shuffled_K_median", "rms": 0.151, "rank": 3},
    {"condition": "newtonian_baryonic", "rms": 0.181, "rank": 5},
    {"condition": "mond_simple", "rms": 0.142, "rank": 2},
    {"condition": "empirical_rar", "rms": 0.139, "rank": 2},
]


READINESS = [
    {"item": "Paper 1 residual-blind disturbance association", "status": "available"},
    {"item": "Paper 2 residual-shape inference and shuffled-label null", "status": "available"},
    {"item": "Paper 3 candidate/control ladder and required S_tau diagnostic", "status": "available"},
    {"item": "Morphology-family formula registry", "status": "defined_in_this_package"},
    {"item": "Accepted source-native component tables for all candidates", "status": "pending"},
    {"item": "Residual-blind morphology labels for full endpoint sample", "status": "pending"},
    {"item": "Real matched-vs-wrong family endpoint", "status": "not_yet_run"},
]


def write_tables() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(MORPHOLOGY_FAMILIES).to_csv(DATA / "morphology_family_registry.csv", index=False)
    pd.DataFrame(CANDIDATE_CONTROL_CROSSWALK).to_csv(
        DATA / "paper3_candidate_control_crosswalk.csv", index=False
    )
    pd.DataFrame(FORWARD_GATE_SCHEMA).to_csv(DATA / "forward_readout_gate_schema.csv", index=False)
    pd.DataFrame(SYNTHETIC_DEMO).to_csv(DATA / "synthetic_forward_gate_demo.csv", index=False)
    pd.DataFrame(READINESS).to_csv(DATA / "paper8_readiness_table.csv", index=False)


def savefig(name: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    SOURCE_FIGURES.mkdir(parents=True, exist_ok=True)
    svg = FIGURES / f"{name}.svg"
    pdf = SOURCE_FIGURES / f"{name}.pdf"
    plt.savefig(svg, bbox_inches="tight")
    plt.savefig(pdf, bbox_inches="tight")
    plt.close()
    # Matplotlib SVG paths often contain trailing spaces before line breaks.
    # Strip them so `git diff --check` stays useful for the public package.
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )


def make_figures() -> None:
    families = pd.DataFrame(MORPHOLOGY_FAMILIES)
    status_counts = families["sparc_first_pass_status"].value_counts().sort_index()
    plt.figure(figsize=(7.2, 4.0))
    colors = ["#31688e", "#35b779", "#fde725"]
    status_counts.plot(kind="bar", color=colors[: len(status_counts)])
    plt.ylabel("family count")
    plt.xlabel("first-pass observability status")
    plt.title("Morphology-family testability split")
    plt.xticks(rotation=18, ha="right")
    plt.tight_layout()
    savefig("fig01_morphology_family_registry")

    demo = pd.DataFrame(SYNTHETIC_DEMO)
    order = [
        "matched_family",
        "empirical_rar",
        "mond_simple",
        "shuffled_K_median",
        "wrong_family_mean",
        "newtonian_baryonic",
    ]
    demo = demo.set_index("condition").loc[order].reset_index()
    plt.figure(figsize=(7.4, 4.2))
    bar_colors = ["#2a9d8f" if x == "matched_family" else "#6c757d" for x in demo["condition"]]
    plt.barh(demo["condition"], demo["rms"], color=bar_colors)
    plt.xlabel("RMS residual score (synthetic protocol fixture)")
    plt.title("Forward gate endpoint: matched family versus controls")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    savefig("fig02_forward_gate_score_schema")

    steps = pd.DataFrame(FORWARD_GATE_SCHEMA)
    plt.figure(figsize=(7.4, 4.4))
    y = range(len(steps), 0, -1)
    plt.scatter([1] * len(steps), y, s=520, color="#457b9d")
    for yi, (_, row) in zip(y, steps.iterrows()):
        plt.text(1.08, yi, f"{row['step']}. {row['gate_component']}", va="center", fontsize=9)
    plt.xlim(0.8, 3.2)
    plt.ylim(0.3, len(steps) + 0.7)
    plt.axis("off")
    plt.title("MORPHOLOGY-MATCHED-FORWARD-READOUT-GATE")
    plt.tight_layout()
    savefig("fig03_forward_readout_gate_flow")


def copy_readme() -> None:
    (FIGURES / "README.md").write_text(
        "# Figures\n\nGenerated SVG source figures live here. PDF copies used by LaTeX live under `paper8_submission_source/figures/`.\n",
        encoding="utf-8",
    )


def main() -> None:
    write_tables()
    make_figures()
    copy_readme()
    print("PAPER8_ARTIFACTS_GENERATED")


if __name__ == "__main__":
    main()
