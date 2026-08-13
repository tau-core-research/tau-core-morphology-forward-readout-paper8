#!/usr/bin/env python3
"""Extract published gas and stellar curves from LITTLE THINGS vector figures."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path

import fitz
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/external/literature/little_things_oh2015_mass_models"
DATA = ROOT / "data/derived"
ROTATION = DATA / "little_things_rotation_curves_v01.csv"
OUT = DATA / "little_things_baryonic_vector_components_v01.csv"
AUDIT = DATA / "little_things_baryonic_vector_extraction_audit_v01.csv"
SUMMARY = DATA / "little_things_baryonic_vector_extraction_v01.json"


def key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def line_vertices(drawing: dict) -> np.ndarray:
    points = []
    for item in drawing["items"]:
        if item[0] == "l":
            points.extend([(item[1].x, item[1].y), (item[2].x, item[2].y)])
    if not points:
        return np.empty((0, 2))
    frame = pd.DataFrame(points, columns=["x", "y"]).groupby("x", as_index=False).y.mean()
    return frame.sort_values("x")[["x", "y"]].to_numpy()


def observed_markers(drawings: list[dict]) -> tuple[np.ndarray, int]:
    candidates = []
    for index, drawing in enumerate(drawings):
        rect = drawing["rect"]
        color = drawing.get("color")
        if not color or drawing.get("dashes") != "[] 0" or not (80 < rect.x0 < 125):
            continue
        if not (435 < rect.y0 < 570 and rect.width > 40 and len(drawing["items"]) > 20):
            continue
        if abs(float(color[0]) - 0.587891) > 0.03:
            continue
        by_x: dict[float, list[tuple[float, float]]] = collections.defaultdict(list)
        for item in drawing["items"]:
            if item[0] == "l" and abs(item[1].x - item[2].x) < 0.02:
                by_x[round(item[1].x, 2)].append((item[1].y, item[2].y))
        points = []
        for x, segments in by_x.items():
            counts = collections.Counter(round(y, 2) for segment in segments for y in segment)
            shared = [(count, y) for y, count in counts.items() if count >= 2]
            if shared:
                points.append((x, max(shared)[1]))
        if len(points) >= 4:
            candidates.append((len(points), index, np.asarray(sorted(points))))
    if not candidates:
        raise ValueError("observed error-bar path not found")
    _, index, points = max(candidates, key=lambda item: item[0])
    return points, index


def component(drawings: list[dict], stellar: bool) -> tuple[np.ndarray, int] | tuple[None, None]:
    token = "7.6800005" if stellar else "1.4399999 2.8799999"
    candidates = []
    for index, drawing in enumerate(drawings):
        rect = drawing["rect"]
        dash = drawing.get("dashes", "")
        color = drawing.get("color")
        if not color or abs(float(color[0]) - 0.313721) > 0.03:
            continue
        match = token in dash and ("7.6800005" in dash) == stellar
        if match and 435 < rect.y0 < 575 and rect.width > 20:
            vertices = line_vertices(drawing)
            if len(vertices) >= 4:
                candidates.append((rect.width, index, vertices))
    if not candidates:
        return None, None
    _, index, vertices = max(candidates, key=lambda item: item[0])
    return vertices, index


def calibrate(markers: np.ndarray, numeric: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, float, float]:
    n = min(len(markers), len(numeric))
    marker = markers[:n]
    rows = numeric.iloc[:n]
    x_fit = np.polyfit(rows.radius_kpc, marker[:, 0], 1)
    y_fit = np.polyfit(rows.velocity_km_s, marker[:, 1], 1)
    x_rmse = float(np.sqrt(np.mean((np.polyval(x_fit, rows.radius_kpc) - marker[:, 0]) ** 2)))
    y_rmse = float(np.sqrt(np.mean((np.polyval(y_fit, rows.velocity_km_s) - marker[:, 1]) ** 2)))
    return x_fit, y_fit, x_rmse, y_rmse


def physical(vertices: np.ndarray | None, x_fit: np.ndarray, y_fit: np.ndarray) -> pd.DataFrame:
    if vertices is None:
        return pd.DataFrame(columns=["radius_kpc", "velocity_km_s"])
    return pd.DataFrame({
        "radius_kpc": (vertices[:, 0] - x_fit[1]) / x_fit[0],
        "velocity_km_s": (vertices[:, 1] - y_fit[1]) / y_fit[0],
    }).query("radius_kpc >= 0").sort_values("radius_kpc")


def main() -> None:
    rotation = pd.read_csv(ROTATION)
    figures = {key(path.stem.removeprefix("rMD_DH_DM_profiles_")): path for path in SOURCE.glob("*.pdf")}
    rows, audits = [], []
    for galaxy, numeric in rotation.loc[rotation.curve_type.eq("Data")].groupby("galaxy", sort=True):
        path = figures.get(key(galaxy))
        if path is None:
            audits.append({"galaxy": galaxy, "status": "figure_missing"})
            continue
        drawings = fitz.open(path)[0].get_drawings()
        try:
            markers, observed_index = observed_markers(drawings)
            x_fit, y_fit, x_rmse, y_rmse = calibrate(markers, numeric.sort_values("radius_kpc"))
            gas_vertices, gas_index = component(drawings, stellar=False)
            star_vertices, star_index = component(drawings, stellar=True)
            gas = physical(gas_vertices, x_fit, y_fit)
            star = physical(star_vertices, x_fit, y_fit)
            support_lo = max(gas.radius_kpc.min(), star.radius_kpc.min() if len(star) else gas.radius_kpc.min())
            support_hi = min(gas.radius_kpc.max(), star.radius_kpc.max() if len(star) else gas.radius_kpc.max())
            selected = numeric[(numeric.radius_kpc >= support_lo) & (numeric.radius_kpc <= support_hi)].copy()
            selected["v_gas_km_s"] = np.interp(selected.radius_kpc, gas.radius_kpc, gas.velocity_km_s)
            if len(star):
                selected["v_star_km_s"] = np.interp(selected.radius_kpc, star.radius_kpc, star.velocity_km_s)
                star_status = "extracted"
            else:
                selected["v_star_km_s"] = 0.0
                star_status = "absent_in_published_panel_assumed_zero"
            selected["v_baryon_newton_km_s"] = np.sqrt(np.maximum(
                selected.v_gas_km_s * np.abs(selected.v_gas_km_s) + selected.v_star_km_s ** 2, 0.0
            ))
            selected["figure_file"] = path.name
            selected["coordinate_calibration_uses_published_vobs"] = True
            rows.extend(selected[["galaxy", "radius_kpc", "velocity_km_s", "velocity_error_km_s",
                                  "v_gas_km_s", "v_star_km_s", "v_baryon_newton_km_s", "figure_file",
                                  "coordinate_calibration_uses_published_vobs"]].to_dict("records"))
            passed = x_rmse <= 0.35 and y_rmse <= 0.35 and len(gas) >= 4 and len(selected) >= 4
            audits.append({
                "galaxy": galaxy, "status": "pass" if passed else "fail_quality_gate",
                "n_numeric_data_points": len(numeric), "n_pdf_markers": len(markers),
                "n_scoring_points": len(selected), "x_calibration_rmse_pdf_points": x_rmse,
                "y_calibration_rmse_pdf_points": y_rmse, "gas_path_index": gas_index,
                "stellar_path_index": star_index, "stellar_status": star_status,
                "observed_path_index": observed_index,
            })
        except Exception as error:
            audits.append({"galaxy": galaxy, "status": f"extraction_error:{error}"})
    extracted = pd.DataFrame(rows)
    audit = pd.DataFrame(audits)
    extracted.to_csv(OUT, index=False)
    audit.to_csv(AUDIT, index=False)
    passed = audit.status.eq("pass")
    result = {
        "schema": "little_things_baryonic_vector_extraction_v01",
        "status": "PREFLIGHT_NOT_ENDPOINT" if passed.any() else "NEGATIVE_RESULT_PRESERVED",
        "n_galaxies": len(audit), "n_quality_pass": int(passed.sum()),
        "n_extracted_scoring_points": len(extracted),
        "quality_gate": "axis calibration RMSE <= 0.35 PDF points; gas path and >=4 common-support points",
        "endpoint_access": True,
        "endpoint_access_scope": "published vobs used only to calibrate vector-figure coordinates",
        "prospective_formula_retuning": False,
        "claim_boundary": "vector extraction preflight; failed galaxies excluded; no Tau endpoint score",
    }
    SUMMARY.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["status"], result["n_quality_pass"], result["n_extracted_scoring_points"])


if __name__ == "__main__":
    main()
