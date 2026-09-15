#!/usr/bin/env python3
"""Freeze the source-developed EDGE--CALIFA v02 endpoint before velocities."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from freeze_edge_califa_rotation_morphology_preregistration_v01 import protocol as v01_protocol


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
OUTPUT = DATA / "edge_califa_rotation_morphology_preregistration_v02.json"
HASH = DATA / "edge_califa_rotation_morphology_preregistration_v02.sha256"
REPORT = ROOT / "reports/edge_califa_rotation_morphology_preregistration_v02.md"


def protocol() -> dict:
    frozen = v01_protocol()
    frozen.update({
        "schema": "edge_califa_rotation_morphology_preregistration_v02",
        "status": "SOURCE_DEVELOPED_V02_PROTOCOL_FROZEN_FULL_VELOCITY_ENDPOINT_UNOPENED",
        "supersedes": {
            "preregistration_v01_sha256": "0433b1b25f1c10a19f0099bf1cb98f3e807faf7bcfda436fb0d18cf7722cec3c",
            "source_preflight_v01_sha256": "02e228acfdd69b27251896499a2d397bb38674c202f5d4646986311bb6675bd9",
            "v01_result": "SOURCE_ONLY_COHORT_INSUFFICIENT_NO_ENDPOINT_OPENING",
            "velocity_values_opened_under_v01": False,
        },
        "source_development_disclosure": (
            "v02 was selected after inspecting source-field coverage and ranks but before "
            "requesting either CO or Halpha velocity field; it is a new prevalidation look"
        ),
    })
    frozen["source_support"] = {
        "co_support": (
            "positive finite mom0_12 with positive finite e_mom0_12 inside the public "
            "dilated mask; no second integrated-SNR cut is imposed because the published "
            "mask already grows a two-channel 3.5-sigma seed to a 2-sigma boundary"
        ),
        "halpha_support": "flux_Halpha_sm/e_flux_Halpha_sm >= 3.5",
        "stellar_support": "positive finite sigstar_sm",
        "radial_edge_support": "intersection of CO, Halpha and stellar supports",
        "profile_support": (
            "each source profile uses its own positive finite field support inside the "
            "frozen radial edges; standard nuisance fields are not forced onto the CO mask"
        ),
        "minimum_radial_edge_rows": 120,
        "minimum_profile_rows_per_zone": 20,
        "inclination_window": (
            "30 <= inclination <= 70 degrees, implemented as "
            "0.3420201433 <= median(cosi) <= 0.8660254038"
        ),
        "radial_edges": "five equal-count quantile zones from radial-edge support",
        "azimuth_gate": (
            "all six fixed equal-width macrosectors occupied in every radial-edge zone"
        ),
        "why_six_sectors": (
            "source-only coverage showed that the inherited 12-sector PHANGS gate leaves "
            "only one nonhistorical EDGE galaxy; six sectors retain angular leave-one-sector "
            "variation while matching the public 7-arcsec beam on a sparse 3-arcsec grid"
        ),
    }
    frozen["deterministic_split"].update({
        "minimum_confirmatory_galaxies": 6,
        "small_sample_boundary": (
            "the expected source-eligible cohort is small; v02 can only be prevalidation "
            "and cannot supply discovery or independent replication"
        ),
    })
    frozen["terminal_opening"].update({
        "support": "intersection with the frozen v02 radial-edge support",
        "zone_gate": "at least 20 rows and all six macrosectors in each frozen zone",
        "covariance": (
            "delete-one-of-six-azimuth-macrosectors jackknife in each zone, assembled as "
            "five 4x4 blocks; every block and the 20x20 covariance must be full rank"
        ),
    })
    frozen["decision_rule"].update({
        "primary_test": (
            "one-sided exact shared-sign permutation of mean(D_g)>0 over every 2^N "
            "confirmatory sign vector"
        ),
        "individual_controls": (
            "the same exact shared-sign permutations form a studentized max-T null across "
            "radial-reversal, phase-rotation and cross-galaxy controls; all three adjusted "
            "p-values must be <0.05"
        ),
        "v02_primary_alpha": 0.01,
        "v02_is_additional_program_look": True,
    })
    frozen["interpretation"]["positive"] = (
        "source-developed external morphology-alignment prevalidation beyond the declared "
        "low-dimensional standard source span and equal-rank controls"
    )
    frozen["interpretation"]["v02_limit"] = (
        "source coverage and sector count were selected before terminal opening but after "
        "source inspection; a pass is therefore weaker than a fully untouched protocol"
    )
    return frozen


def main() -> None:
    frozen = protocol()
    payload = json.dumps(frozen, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    HASH.write_text(
        f"{digest}  data/derived/{OUTPUT.name}\n", encoding="utf-8"
    )
    REPORT.write_text(
        "# EDGE--CALIFA rotation/morphology preregistration v02\n\n"
        f"Status: `{frozen['status']}`\n\n"
        "The untouched velocity endpoint remains closed.  The inherited v01 source gate "
        "left zero eligible galaxies and is preserved as a negative source-coverage result. "
        "This separately versioned v02 was developed only from non-velocity source coverage.\n\n"
        "v02 uses the published dilated CO mask, field-specific source supports, and six "
        "azimuth macrosectors.  The five-zone 20D terminal, standard-plus-body rank target, "
        "equal-rank controls, historical 17-galaxy exclusion, and deterministic split remain.\n\n"
        "Because the source gate itself was developed on this survey and the expected cohort "
        "is small, any pass is prevalidation only.  It is not a Tau-specific, dark-sector, "
        "or discovery-level result.\n\n"
        f"Frozen JSON SHA-256: `{digest}`.\n",
        encoding="utf-8",
    )
    print(frozen["status"], digest)


if __name__ == "__main__":
    main()
