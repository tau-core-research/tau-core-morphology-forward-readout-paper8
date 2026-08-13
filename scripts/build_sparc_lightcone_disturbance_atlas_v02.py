#!/usr/bin/env python3
"""Promote the preliminary SIMBAD foreground proxy into the S/P/O atlas."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"


def main() -> None:
    base = pd.read_csv(DATA / "sparc_lightcone_disturbance_atlas_v01.csv")
    path = pd.read_csv(DATA / "sparc_simbad_lightcone_foregrounds_v01.csv")
    joined = base.drop(columns=["path_disturbance_class", "path_disturbance_basis", "combined_class"]).merge(
        path[["galaxy", "foreground_candidate_count", "foreground_inverse_angle_weight",
              "background_redshift_control_count", "stellar_crowding_control_count",
              "path_disturbance_class", "query_status"]],
        on="galaxy", how="left", validate="one_to_one",
    )
    joined["path_disturbance_basis"] = joined.apply(
        lambda row: (
            f"SIMBAD 10arcmin cone; foreground_n={int(row.foreground_candidate_count)}; "
            f"inverse_angle_weight={row.foreground_inverse_angle_weight:.6f}"
            if row.query_status == "OK" else "SIMBAD cone unavailable"
        ), axis=1,
    )
    joined["combined_class"] = (
        joined["source_disturbance_class"] + "-" + joined["path_disturbance_class"]
        + "-" + joined["observation_disturbance_class"]
    )
    joined.to_csv(DATA / "sparc_lightcone_disturbance_atlas_v02.csv", index=False)
    payload = {
        "schema": "sparc_lightcone_disturbance_atlas_v02",
        "status": "PRELIMINARY_S_P_O_CLASSES_READY_SIMBAD_PATH_INCOMPLETE",
        "n_galaxies": len(joined),
        "source_class_counts": joined.source_disturbance_class.value_counts().sort_index().to_dict(),
        "path_class_counts": joined.path_disturbance_class.value_counts().sort_index().to_dict(),
        "observation_class_counts": joined.observation_disturbance_class.value_counts().sort_index().to_dict(),
        "path_proxy": "redshift-confirmed foreground extragalactic objects in a fixed 10 arcmin SIMBAD cone",
        "path_proxy_is_complete": False,
        "allowed_use": "exploratory stratification and acquisition prioritization",
        "forbidden_use": "physical lightcone transfer coefficient or causal channel attribution",
        "verdict": "S_P_O_ATLAS_V02_READY_FOR_CONFOUNDED_STRATIFICATION_ONLY",
    }
    (DATA / "sparc_lightcone_disturbance_atlas_v02.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["verdict"])


if __name__ == "__main__":
    main()
