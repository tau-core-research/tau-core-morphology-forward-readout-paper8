#!/usr/bin/env python3
"""Freeze NGC3893 as a zero-point-safe disturbed-galaxy control."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/ngc3893_disturbed_control_freeze_v01.md"
UMA = ROOT / "data/external/catalogs/ngc3726_uma_hi/uma_rotation_table4.dat.gz"
HALPHA = DATA / "ghasp_full_federation_side_points_v01.csv"
PRIMARY = ROOT / "data/external/literature/ngc3893_replication_eligibility/astro-ph_0701878_source.tar.gz"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def bracket(radii, target):
    lo = max(x for x in radii if x <= target)
    hi = min(x for x in radii if x >= target)
    if lo == hi:
        return lo, hi, 1.0, 0.0
    whi = (target - lo) / (hi - lo)
    return lo, hi, 1.0 - whi, whi

def main() -> None:
    lines = gzip.decompress(UMA.read_bytes()).decode("utf-8").splitlines()
    source_rows = []
    for line in lines:
        if line[3:8].strip() != "N3893":
            continue
        source_rows.append({
            "radius_arcsec": float(line[9:12]),
            "approaching_present": bool(line[13:16].strip()),
            "receding_present": bool(line[25:28].strip()),
            "hi_inclination_deg": float(line[41:44]),
            "hi_receding_pa_deg": float(line[45:48]) % 360,
        })
    ha = [row for row in csv.DictReader(HALPHA.open(newline="", encoding="utf-8")) if "NGC3893" in row["aliases"].split(";")]
    by_side = {side: sorted(float(row["radius_arcsec"]) for row in ha if row["side"] == side) for side in ("a", "r")}
    support = min(max(by_side["a"]), max(by_side["r"]))
    selected = [row for row in source_rows if row["approaching_present"] and row["receding_present"] and row["radius_arcsec"] <= support]
    if [row["radius_arcsec"] for row in selected] != [20.0, 40.0, 60.0, 80.0]:
        raise RuntimeError("Unexpected NGC3893 common support")
    frozen_rows = []
    for row in selected:
        radius = row["radius_arcsec"]
        a0, a1, aw0, aw1 = bracket(by_side["a"], radius)
        r0, r1, rw0, rw1 = bracket(by_side["r"], radius)
        frozen_rows.append({
            **row,
            "halpha_a_lower_arcsec": a0, "halpha_a_upper_arcsec": a1,
            "halpha_a_lower_weight": aw0, "halpha_a_upper_weight": aw1,
            "halpha_r_lower_arcsec": r0, "halpha_r_upper_arcsec": r1,
            "halpha_r_lower_weight": rw0, "halpha_r_upper_weight": rw1,
            "outer_disturbance_template": int(radius > 75.0),
            "endpoint_access": False,
        })
    csv_path = DATA / "ngc3893_disturbed_control_freeze_v01.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(frozen_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(frozen_rows)
    result = {
        "schema": "ngc3893_disturbed_control_freeze_v01",
        "status": "DISTURBED_CONTROL_SOURCE_FREEZE_COMPLETE_VELOCITIES_UNOPENED",
        "galaxy": "NGC3893",
        "role": "CONVENTIONAL_DISTURBED_CONTROL_NOT_TAU_ENDPOINT",
        "common_radii_arcsec": [20.0, 40.0, 60.0, 80.0],
        "source_template": [0.0, 0.0, 0.0, 1.0],
        "control_templates": {
            "inner_single_ring": [1.0, 0.0, 0.0, 0.0],
            "linear_radius": [0.0, 1.0 / 3.0, 2.0 / 3.0, 1.0],
        },
        "template_rule": "one for R>75 arcsec, zero otherwise",
        "template_source": "Fuentes-Carrera et al. report perturbed optical RC points above 75 arcsec and uncertain H I beyond 120 arcsec",
        "zero_point_nuisance_tangent": "(-2,+2) repeated at every radius",
        "expected_projector_rank": 3,
        "score_rule": "two-sided covariance-weighted matched-template z after zero-point projection",
        "omnibus_rule": "projected zero-vector chi-square with three degrees of freedom",
        "input_sha256": {"uma_table4": sha(UMA), "halpha_federation": sha(HALPHA), "interaction_source": sha(PRIMARY)},
        "velocity_columns_parsed_during_freeze": False,
        "endpoint_access": False,
        "selection_uses_velocity_difference_or_residual": False,
        "literature_overlap_caveat": "the disturbance source analyzed related optical and H I kinematics, so this can validate sensitivity only",
        "next_action": "run a separate disturbed-control score without changing radii, template, nuisance span or covariance rules",
        "claim_boundary": "source-frozen conventional disturbance control; not a clean replication, Tau signal, q_R, or dark-matter result",
    }
    (DATA / "ngc3893_disturbed_control_freeze_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# NGC3893 disturbed-control freeze v0.1\n\n"
        f"Status: {result['status']}\n\n"
        "The previously missed machine-readable Ursa Major side table is present. Four two-sided H I radii lie inside both GHASP sides: 20, 40, 60 and 80 arcsec. No velocity column was parsed during this freeze.\n\n"
        "The external interaction study identifies the optical curve above 75 arcsec as perturbed, so the frozen nonconstant control template is (0,0,0,1). The constant systemic-velocity nuisance will be projected out, leaving three shape degrees of freedom. Because that study analyzed related kinematics, this is a conventional disturbed-system sensitivity control, not an independent Tau endpoint.\n"
    )
    print(result["status"])

if __name__ == "__main__":
    main()
