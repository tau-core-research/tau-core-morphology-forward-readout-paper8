#!/usr/bin/env python3
"""Post-open diagnostic for resolved PHANGS morphology/tracer structure.

The frozen endpoint failed its 12-sector covariance gate.  This script does
not repair or reopen it: it reports formal-covariance sensitivity with fixed
error floors and retains the preregistered geometric controls.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import freeze_phangs_radial_body_projection_scoring_contract_v01 as scoring
import run_phangs_radial_body_projection_confirmatory_endpoint_v01 as endpoint


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/phangs_postopen_resolved_morphology_diagnostic_v01.md"
STEM = "phangs_postopen_resolved_morphology_diagnostic_v01"
FLOORS = (5.0, 10.0, 20.0)


def markdown_table(frame: pd.DataFrame) -> str:
    columns = list(frame.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in frame.itertuples(index=False, name=None):
        lines.append(
            "| "
            + " | ".join(f"{value:.6g}" if isinstance(value, float) else str(value) for value in row)
            + " |"
        )
    return "\n".join(lines)


def covariance_block(error_floor: float):
    def calculate(design, values, variance, sectors):
        del values, sectors
        weight = 1.0 / (variance + error_floor**2)
        covariance = np.linalg.pinv(
            design.T @ (weight[:, None] * design), rcond=1.0e-10
        )
        return covariance[np.ix_([1, 2, 3, 4], [1, 2, 3, 4])]

    return calculate


def main() -> None:
    failed = json.loads(
        (DATA / "phangs_radial_body_projection_confirmatory_endpoint_v01.json").read_text()
    )
    if failed["status"] != "CONFIRMATORY_ENDPOINT_OPENED_NONIDENTIFIABLE_GATE_FAILURE":
        raise RuntimeError("This diagnostic requires the preserved failed endpoint")
    sample = pd.read_csv(endpoint.SAMPLE, skiprows=[1]).set_index("Name")
    rows = []
    summaries = []
    for floor in FLOORS:
        endpoint.sector_jackknife_block = covariance_block(floor)
        opened = {}
        for galaxy in endpoint.CONFIRMATORY:
            center = (
                float(sample.loc[galaxy, "R.A."]),
                float(sample.loc[galaxy, "Dec."]),
            )
            opened[galaxy] = endpoint.open_galaxy(galaxy, center)
            metrics = opened[galaxy]["metrics"]
            primary = metrics["primary"]
            reverse = metrics["radial_reversal"]
            phase = metrics["phase_rotation_pi_over_2"]
            rows.append(
                {
                    "error_floor_km_s": floor,
                    "galaxy": galaxy,
                    "q_primary": primary["q"],
                    "p_primary": primary["p_chi_square_approximation"],
                    "q_radial_reversal": reverse["q"],
                    "q_phase_rotation": phase["q"],
                    "primary_below_radial_reversal": primary["q"] < reverse["q"],
                    "primary_below_phase_rotation": primary["q"] < phase["q"],
                    "beam_independent_pixels": metrics["beam_independent_pixels"],
                }
            )
        primary = scoring.aggregate(
            [opened[g]["metrics"]["primary"] for g in endpoint.CONFIRMATORY]
        )
        reverse = scoring.aggregate(
            [opened[g]["metrics"]["radial_reversal"] for g in endpoint.CONFIRMATORY]
        )
        phase = scoring.aggregate(
            [opened[g]["metrics"]["phase_rotation_pi_over_2"] for g in endpoint.CONFIRMATORY]
        )
        subset = [row for row in rows if row["error_floor_km_s"] == floor]
        reverse_count = sum(row["primary_below_radial_reversal"] for row in subset)
        phase_count = sum(row["primary_below_phase_rotation"] for row in subset)
        summaries.append(
            {
                "error_floor_km_s": floor,
                "q_primary": primary["q"],
                "dof_primary": primary["dof"],
                "p_primary_formal": primary["p_chi_square_approximation"],
                "individual_p_below_0_05": primary["individual_p_below_0_05"],
                "q_radial_reversal": reverse["q"],
                "primary_below_reversal_global": primary["q"] < reverse["q"],
                "primary_below_reversal_count": reverse_count,
                "radial_control_pass": bool(
                    primary["q"] < reverse["q"] and reverse_count >= 3
                ),
                "q_phase_rotation": phase["q"],
                "primary_below_phase_global": primary["q"] < phase["q"],
                "primary_below_phase_count": phase_count,
                "phase_control_pass": bool(
                    primary["q"] < phase["q"] and phase_count >= 3
                ),
            }
        )

    detail = pd.DataFrame(rows)
    summary = pd.DataFrame(summaries)
    detail.to_csv(DATA / f"{STEM}_by_galaxy.csv", index=False)
    summary.to_csv(DATA / f"{STEM}_summary.csv", index=False)
    result = {
        "schema": STEM,
        "status": "NEGATIVE_RESULT_PRESERVED_POSTOPEN_DIAGNOSTIC",
        "endpoint_reopened": False,
        "original_gate_failure_preserved": True,
        "galaxies": endpoint.CONFIRMATORY,
        "resolved_body_basis": (
            "five radial zones of stellar and CO m1/m2 amplitudes, phases, "
            "and first radial differences"
        ),
        "terminal": "beam-matched CO minus Halpha m1/m2 velocity contrast",
        "error_floors_km_s": list(FLOORS),
        "all_formal_primary_nonzero": bool((summary.p_primary_formal < 0.01).all()),
        "radial_control_pass_all_floors": bool(summary.radial_control_pass.all()),
        "phase_control_pass_all_floors": bool(summary.phase_control_pass.all()),
        "interpretation": (
            "resolved tracer structure remains outside the declared body span under "
            "diagonal formal covariance, but the matched morphology fails the frozen "
            "geometric specificity controls"
        ),
        "strongest_alternative": (
            "spatially correlated measurement noise, incomplete azimuthal support, "
            "ordinary tracer physics and an incomplete morphology nuisance basis"
        ),
        "claim_boundary": (
            "retrospective sensitivity diagnostic after a preregistered covariance-gate "
            "failure; not an endpoint, parent kernel, channel detection or Tau evidence"
        ),
    }
    (DATA / f"{STEM}.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# PHANGS post-open resolved-morphology diagnostic v01\n\n"
        f"Status: `{result['status']}`.\n\n"
        "The original four-galaxy endpoint remains failed and closed because every "
        "body missed the frozen 12-sector covariance gate. This retrospective "
        "diagnostic substitutes diagonal formal covariance with fixed 5, 10 and "
        "20 km/s error floors; it cannot repair the endpoint.\n\n"
        "## Sensitivity summary\n\n"
        + markdown_table(summary)
        + "\n\nThe formal body-orthogonal contrast is nonzero at every floor, but the "
        "matched resolved morphology does not pass both radial-reversal and phase-"
        "rotation specificity controls. Ordinary tracer dynamics, incomplete body "
        "description, spatial covariance and incomplete angular coverage remain "
        "stronger explanations.\n",
        encoding="utf-8",
    )
    print(summary.to_string(index=False))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
