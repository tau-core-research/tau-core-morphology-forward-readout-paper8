#!/usr/bin/env python3
"""Open the frozen NGC3893 conventional disturbed-system control."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import chi2, norm

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/ngc3893_disturbed_control_score_v01.md"
FREEZE_JSON = DATA / "ngc3893_disturbed_control_freeze_v01.json"
FREEZE_CSV = DATA / "ngc3893_disturbed_control_freeze_v01.csv"
UMA = ROOT / "data/external/catalogs/ngc3726_uma_hi/uma_rotation_table4.dat.gz"
HALPHA = DATA / "ghasp_full_federation_side_points_v01.csv"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def val(text):
    text = text.strip()
    return float(text) if text else None

def interpolate(rows, lo, hi, wlo, whi):
    a, b = rows[lo], rows[hi]
    v = wlo * float(a["velocity_km_s"]) + whi * float(b["velocity_km_s"])
    e = math.hypot(wlo * float(a["velocity_error_km_s"]), whi * float(b["velocity_error_km_s"]))
    return v, e

def side_stats(a, r, ea, er, inc):
    angle = math.radians(inc)
    return {
        "odd": (r - a) * math.sin(angle),
        "variance": (math.sin(angle) * math.hypot(ea, er)) ** 2,
        "di": (r - a) * math.cos(angle),
    }

def main():
    freeze = json.loads(FREEZE_JSON.read_text())
    if freeze["velocity_columns_parsed_during_freeze"] or freeze["endpoint_access"]:
        raise RuntimeError("Residual-blind freeze failed")
    if sha(UMA) != freeze["input_sha256"]["uma_table4"] or sha(HALPHA) != freeze["input_sha256"]["halpha_federation"]:
        raise RuntimeError("Frozen input changed")
    frozen = list(csv.DictReader(FREEZE_CSV.open(newline="", encoding="utf-8")))
    hi = {}
    for line in gzip.decompress(UMA.read_bytes()).decode("utf-8").splitlines():
        if line[3:8].strip() == "N3893" and float(line[9:12]) in freeze["common_radii_arcsec"]:
            hi[float(line[9:12])] = {
                "a": val(line[13:16]), "ea+": val(line[17:20]), "ea-": val(line[21:24]),
                "r": val(line[25:28]), "er+": val(line[29:32]), "er-": val(line[33:36]),
            }
    ha_rows = [row for row in csv.DictReader(HALPHA.open(newline="", encoding="utf-8")) if "NGC3893" in row["aliases"].split(";")]
    by_side = {side: {float(row["radius_arcsec"]): row for row in ha_rows if row["side"] == side} for side in ("a", "r")}
    delta, variances, dha, dhi, detail = [], [], [], [], []
    for row in frozen:
        radius = float(row["radius_arcsec"])
        ha_a, eha_a = interpolate(by_side["a"], float(row["halpha_a_lower_arcsec"]), float(row["halpha_a_upper_arcsec"]), float(row["halpha_a_lower_weight"]), float(row["halpha_a_upper_weight"]))
        ha_r, eha_r = interpolate(by_side["r"], float(row["halpha_r_lower_arcsec"]), float(row["halpha_r_upper_arcsec"]), float(row["halpha_r_lower_weight"]), float(row["halpha_r_upper_weight"]))
        h = hi[radius]
        ehi_a = 0.5 * (h["ea+"] + h["ea-"])
        ehi_r = 0.5 * (h["er+"] + h["er-"])
        hs = side_stats(ha_a, ha_r, eha_a, eha_r, 49.0)
        is_ = side_stats(h["a"], h["r"], ehi_a, ehi_r, float(row["hi_inclination_deg"]))
        d = hs["odd"] - is_["odd"]
        delta.append(d)
        variances.append(hs["variance"] + is_["variance"])
        dha.append(hs["di"])
        dhi.append(-is_["di"])
        detail.append({"radius_arcsec": radius, "delta_odd_los_km_s": d, "measurement_sigma_km_s": math.sqrt(variances[-1])})
    delta = np.asarray(delta)
    covariance = np.diag(variances) + np.outer(dha, dha) * math.radians(4.0) ** 2 + np.outer(dhi, dhi) * math.radians(2.0) ** 2
    inverse = np.linalg.inv(covariance)
    nuisance = np.column_stack((-2.0 * np.ones(4), 2.0 * np.ones(4)))
    projection = np.eye(4) - nuisance @ np.linalg.pinv(nuisance.T @ inverse @ nuisance) @ nuisance.T @ inverse
    q = float(delta @ inverse @ projection @ delta)
    def score(template):
        s = np.asarray(template)
        den = float(s @ inverse @ projection @ s)
        num = float(s @ inverse @ projection @ delta)
        z = num / math.sqrt(den)
        return {"amplitude_km_s": num / den, "sigma_km_s": 1.0 / math.sqrt(den), "z": z, "two_sided_p": float(2 * norm.sf(abs(z)))}
    matched = score(freeze["source_template"])
    controls = {name: score(template) for name, template in freeze["control_templates"].items()}
    detected = matched["two_sided_p"] < 0.05
    result = {
        "schema": "ngc3893_disturbed_control_score_v01",
        "status": "DISTURBED_CONTROL_DETECTED" if detected else "NEGATIVE_RESULT_PRESERVED",
        "role": "CONVENTIONAL_DISTURBED_CONTROL_NOT_TAU_ENDPOINT",
        "freeze_unchanged": True,
        "common_radii_arcsec": freeze["common_radii_arcsec"],
        "delta_odd_los_km_s": delta.tolist(),
        "covariance_km2_s2": covariance.tolist(),
        "projector_rank": int(np.linalg.matrix_rank(projection)),
        "omnibus_shape": {"chi2": q, "dof": 3, "p": float(chi2.sf(q, 3))},
        "matched_outer_disturbance": matched,
        "wrong_template_controls": controls,
        "control_detected_at_5pct": detected,
        "interpretation": (
            "the frozen outer-disturbance template is detected as a conventional sensitivity control"
            if detected else
            "the frozen outer-disturbance template is not detected; the terminal fails this conventional sensitivity control"
        ),
        "claim_boundary": "negative conventional sensitivity control; not a Tau endpoint, q_R, parent morphology, Nature occupation, or dark-matter result",
    }
    (DATA / "ngc3893_disturbed_control_score_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    with (DATA / "ngc3893_disturbed_control_score_v01.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(detail[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(detail)
    REPORT.write_text(
        "# NGC3893 disturbed-control score v0.1\n\n"
        f"Status: {result['status']}\n\n"
        f"The zero-point-projected three-degree-of-freedom shape test gives chi2={q:.4f}, p={result['omnibus_shape']['p']:.4f}. "
        f"The frozen outer-disturbance template gives amplitude {matched['amplitude_km_s']:.3f} +/- {matched['sigma_km_s']:.3f} km/s, "
        f"z={matched['z']:.3f}, two-sided p={matched['two_sided_p']:.4f}.\n\n"
        + (
            "The conventional disturbed-system control is detected, supporting instrument sensitivity but not Tau Core."
            if detected else
            "The conventional disturbed-system control is not detected. This weakens the current side-odd terminal as a morphology-sensitive instrument."
        )
        + " It does not favor Tau Core or standard gravity. No post-open repair is allowed.\n"
    )
    print(result["status"], json.dumps(result["matched_outer_disturbance"]))

if __name__ == "__main__":
    main()
