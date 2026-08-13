#!/usr/bin/env python3
"""Run the preregistered geometry perturbations for the cross-wedge remainder."""

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
SCRIPT = ROOT / "scripts/score_ngc4254_cross_wedge_gasdynamics_remainder_v05.py"
VARIANTS = [
    ("pa_m5", {"TC_PA_OFFSET_DEG": "-5"}), ("pa_p5", {"TC_PA_OFFSET_DEG": "5"}),
    ("inc_m5", {"TC_INC_OFFSET_DEG": "-5"}), ("inc_p5", {"TC_INC_OFFSET_DEG": "5"}),
    ("east_m1", {"TC_CENTER_EAST_OFFSET_ARCSEC": "-1"}), ("east_p1", {"TC_CENTER_EAST_OFFSET_ARCSEC": "1"}),
    ("north_m1", {"TC_CENTER_NORTH_OFFSET_ARCSEC": "-1"}), ("north_p1", {"TC_CENTER_NORTH_OFFSET_ARCSEC": "1"}),
    ("wedge20", {"TC_WEDGE_HALF_DEG": "20"}), ("wedge40", {"TC_WEDGE_HALF_DEG": "40"}),
]


def main():
    nominal = json.loads((DATA / "ngc4254_cross_wedge_gasdynamics_remainder_v05.json").read_text())
    rows = [{"id": "nominal", "max_abs_km_s": nominal["maximum_absolute_residual_km_s"],
             "chi2": nominal["residual_zero_chi2"], "p": nominal["residual_zero_p"]}]
    for name, changes in VARIANTS:
        env = os.environ.copy(); env.update(changes); env["TC_SENSITIVITY_ID"] = name
        subprocess.run(["python3", str(SCRIPT)], cwd=ROOT, env=env, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        item = json.loads((DATA / f"ngc4254_cross_wedge_gasdynamics_remainder_v05_{name}.json").read_text())
        rows.append({"id": name, "max_abs_km_s": item["maximum_absolute_residual_km_s"],
                     "chi2": item["residual_zero_chi2"], "p": item["residual_zero_p"]})
    maxima = [x["max_abs_km_s"] for x in rows]
    result = {
        "schema": "ngc4254_cross_wedge_geometry_sensitivity_v06",
        "variants": rows,
        "maximum_absolute_residual_range_km_s": [min(maxima), max(maxima)],
        "all_formal_residual_tests_p_below_0_01": all(x["p"] < 0.01 for x in rows),
        "geometry_eliminates_remainder": min(maxima) < 1.0,
        "full_spatial_covariance_complete": False,
        "common_channel_remainder_identified": False,
        "claim_boundary": "predeclared geometry sensitivity of same-endpoint spatial holdout; not a channel detection",
    }
    (DATA / "ngc4254_cross_wedge_geometry_sensitivity_v06.json").write_text(json.dumps(result, indent=2)+"\n")
    lines = ["# NGC4254 cross-wedge geometry sensitivity v06", "",
             f"Across 11 nominal/perturbed geometries, maximum absolute residual spans "
             f"`{min(maxima):.2f}-{max(maxima):.2f} km/s`. All formal zero-residual tests "
             f"have `p<0.01`: `{result['all_formal_residual_tests_p_below_0_01']}`.", "",
             "This establishes geometry robustness only within the declared perturbations. Full spatial covariance "
             "and an endpoint-independent source-body prediction remain absent; no channel remainder is identified."]
    (ROOT / "reports/ngc4254_cross_wedge_geometry_sensitivity_v06.md").write_text("\n".join(lines)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
