#!/usr/bin/env python3
"""Run the source-developed EDGE--CALIFA v02 preflight without velocities."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from run_edge_califa_source_only_preflight_v01 import (
    EXPECTED_MD5,
    EXPECTED_SIZE,
    N_ZONES,
    REQUESTED_FIELDS,
    embed,
    finite_difference,
    lag_template,
    load_source_frame,
    md5,
    normalized,
    sha256,
    split_role,
    stable_rank,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
PREREG = DATA / "edge_califa_rotation_morphology_preregistration_v02.json"
OUTPUT = DATA / "edge_califa_rotation_morphology_source_preflight_v02.json"
TABLE = DATA / "edge_califa_rotation_morphology_source_preflight_v02.csv"
MATRICES = DATA / "edge_califa_rotation_morphology_source_matrices_v02.npz"
HASH = DATA / "edge_califa_rotation_morphology_source_preflight_v02.sha256"
REPORT = ROOT / "reports/edge_califa_rotation_morphology_source_preflight_v02.md"
N_SECTORS = 6


def profile(
    values: np.ndarray,
    radius: np.ndarray,
    angle: np.ndarray,
    support: np.ndarray,
    edges: np.ndarray,
    mode: int,
) -> np.ndarray:
    result = []
    for zone in range(N_ZONES):
        select = support & (radius >= edges[zone]) & (
            radius <= edges[zone + 1] if zone == N_ZONES - 1 else radius < edges[zone + 1]
        )
        weights = np.where(select, np.clip(values, 0.0, None), 0.0)
        total = float(np.sum(weights))
        if int(select.sum()) < 20 or not np.isfinite(total) or total <= 0:
            raise RuntimeError(f"Insufficient field-specific support in zone {zone}")
        result.append(np.sum(weights * np.exp(1j * mode * angle)) / total)
    return np.asarray(result, dtype=complex)


def source_products(group: pd.DataFrame) -> tuple[dict[str, Any], dict[str, np.ndarray] | None]:
    radius = group["rad_arc"].to_numpy(float)
    angle = np.deg2rad(group["azi_ang"].to_numpy(float))
    co = group["mom0_12"].to_numpy(float)
    eco = group["e_mom0_12"].to_numpy(float)
    ha = group["flux_Halpha_sm"].to_numpy(float)
    eha = group["e_flux_Halpha_sm"].to_numpy(float)
    stellar = group["sigstar_sm"].to_numpy(float)
    dispersion = group["Vdisp_sm"].to_numpy(float)
    sfr = group["flux_sigsfr_adopt_sm"].to_numpy(float)
    sii = (
        group["flux_[SII]6717_sm"].to_numpy(float)
        + group["flux_[SII]6731_sm"].to_numpy(float)
    )
    with np.errstate(divide="ignore", invalid="ignore"):
        ha_snr = ha / eha
        sii_ratio = sii / ha
    geometry = np.isfinite(radius) & np.isfinite(angle)
    co_support = geometry & np.isfinite(co) & np.isfinite(eco) & (eco > 0) & (co > 0)
    ha_support = geometry & np.isfinite(ha) & np.isfinite(eha) & (eha > 0) & (ha_snr >= 3.5)
    stellar_support = geometry & np.isfinite(stellar) & (stellar > 0)
    radial_support = co_support & ha_support & stellar_support
    field_support = {
        "stellar": stellar_support,
        "co": co_support,
        "dispersion": ha_support & np.isfinite(dispersion) & (dispersion > 0),
        "sii_ratio": ha_support & np.isfinite(sii_ratio) & (sii_ratio > 0),
        "sfr": geometry & np.isfinite(sfr) & (sfr > 0),
    }
    cosi = float(np.nanmedian(group["cosi"].to_numpy(float)))
    result: dict[str, Any] = {
        "n_rows": int(len(group)),
        "radial_edge_rows": int(radial_support.sum()),
        "median_cosi": cosi,
        "inclination_gate": bool(0.3420201433 <= cosi <= 0.8660254038),
        "minimum_radial_edge_rows_gate": bool(radial_support.sum() >= 120),
        "source_sector_gate": False,
        "profile_support_gate": False,
        "body_rank": None,
        "standard_rank": None,
        "combined_rank": None,
        "complement_dimension": None,
        "rank_gate": False,
    }
    if not result["inclination_gate"] or not result["minimum_radial_edge_rows_gate"]:
        return result, None
    edges = np.quantile(radius[radial_support], np.linspace(0.0, 1.0, N_ZONES + 1))
    if np.any(np.diff(edges) <= 0):
        return result, None
    sector_counts = []
    for zone in range(N_ZONES):
        select = radial_support & (radius >= edges[zone]) & (
            radius <= edges[zone + 1] if zone == N_ZONES - 1 else radius < edges[zone + 1]
        )
        sectors = np.floor(
            ((angle[select] + np.pi) % (2 * np.pi)) / (2 * np.pi) * N_SECTORS
        ).astype(int)
        sector_counts.append(int(len(np.unique(sectors))))
    result["source_sector_counts"] = sector_counts
    result["source_sector_gate"] = all(count == N_SECTORS for count in sector_counts)
    result["radial_edges_arcsec"] = edges.tolist()
    if not result["source_sector_gate"]:
        return result, None

    profiles = {}
    try:
        for label, values in {
            "stellar": stellar,
            "co": co,
            "dispersion": dispersion,
            "sii_ratio": sii_ratio,
            "sfr": sfr,
        }.items():
            for mode in (1, 2):
                profiles[f"{label}_m{mode}"] = profile(
                    values, radius, angle, field_support[label], edges, mode
                )
    except RuntimeError:
        return result, None
    result["profile_support_gate"] = True
    body = np.column_stack([
        embed(profiles["stellar_m1"], 1),
        embed(finite_difference(profiles["stellar_m1"]), 1),
        embed(profiles["stellar_m2"], 2),
        embed(finite_difference(profiles["stellar_m2"]), 2),
        embed(profiles["co_m1"], 1),
        embed(finite_difference(profiles["co_m1"]), 1),
        embed(profiles["co_m2"], 2),
        embed(finite_difference(profiles["co_m2"]), 2),
    ])
    standard = np.column_stack([
        lag_template(False),
        lag_template(True),
        embed(profiles["dispersion_m1"], 1),
        embed(profiles["dispersion_m2"], 2),
        embed(profiles["sii_ratio_m1"], 1),
        embed(profiles["sii_ratio_m2"], 2),
        embed(profiles["sfr_m1"], 1),
        embed(profiles["sfr_m2"], 2),
    ])
    combined = np.column_stack([standard, body])
    result.update({
        "body_rank": stable_rank(body),
        "standard_rank": stable_rank(standard),
        "combined_rank": stable_rank(combined),
        "complement_dimension": int(20 - stable_rank(combined)),
    })
    result["rank_gate"] = bool(
        result["body_rank"] == 8
        and result["standard_rank"] == 8
        and result["combined_rank"] == 16
        and result["complement_dimension"] == 4
    )
    if not result["rank_gate"]:
        return result, None
    return result, {"body": body, "standard": standard, "combined": combined, "edges": edges}


def main() -> None:
    path = Path("/tmp/edge_carma.2d_smo7.hdf5")
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    if path.stat().st_size != EXPECTED_SIZE or md5(path) != EXPECTED_MD5:
        raise RuntimeError("Published EDGE packet hash/size mismatch")
    if prereg["endpoint_opened"] or prereg["construction_uses_velocity_values"]:
        raise RuntimeError("v02 preregistration opening boundary is invalid")
    forbidden = set(prereg["source_only_fields"]["explicitly_forbidden_during_source_freeze"])
    requested = {f"{table}.{field}" for table, fields in REQUESTED_FIELDS.items() for field in fields}
    if requested & forbidden:
        raise RuntimeError("A terminal field entered v02 source preflight")

    frame = load_source_frame(path)
    excluded = set(prereg["historical_overlap"]["excluded_from_development_and_confirmation"])
    rows = []
    matrices: dict[str, np.ndarray] = {}
    for name, group in frame.groupby("Name", sort=True):
        metrics, products = source_products(group)
        if name in excluded:
            disposition = "HISTORICAL_LEVY_2018_KSS_EXCLUDED"
        elif products is None:
            disposition = "SOURCE_ONLY_GATE_FAILED"
        else:
            disposition = split_role(name).upper()
            for label, array in products.items():
                matrices[f"{name}__{label}"] = array
        rows.append({"galaxy": name, "disposition": disposition, **metrics})
    table = pd.DataFrame(rows)
    development = sorted(table.loc[table.disposition.eq("DEVELOPMENT_NO_CLAIM"), "galaxy"].tolist())
    confirmatory = sorted(table.loc[table.disposition.eq("CONFIRMATORY_UNTOUCHED"), "galaxy"].tolist())
    eligible = sorted(development + confirmatory)
    ready = len(confirmatory) >= prereg["deterministic_split"]["minimum_confirmatory_galaxies"]
    result = {
        "schema": "edge_califa_rotation_morphology_source_preflight_v02",
        "status": (
            "SOURCE_DEVELOPED_V02_COHORT_FROZEN_ENDPOINT_REMAINS_UNOPENED"
            if ready else "SOURCE_DEVELOPED_V02_COHORT_INSUFFICIENT_NO_ENDPOINT_OPENING"
        ),
        "input_file": path.name,
        "input_size_bytes": path.stat().st_size,
        "input_md5": EXPECTED_MD5,
        "input_sha256": sha256(path),
        "requested_source_fields": REQUESTED_FIELDS,
        "velocity_terminal_fields_requested": False,
        "velocity_terminal_values_opened": False,
        "source_eligible": eligible,
        "development_no_claim": development,
        "confirmatory_untouched": confirmatory,
        "n_total_galaxies": int(table.shape[0]),
        "n_source_eligible": len(eligible),
        "n_development": len(development),
        "n_confirmatory": len(confirmatory),
        "minimum_confirmatory": prereg["deterministic_split"]["minimum_confirmatory_galaxies"],
        "endpoint_opening_authorized": ready,
        "source_development_disclosure": prereg["source_development_disclosure"],
        "claim_boundary": (
            "source-developed cohort/rank freeze only; no velocity contrast or endpoint "
            "score has been opened, and no Tau/dark-sector claim is authorized"
        ),
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8")
    TABLE.write_text(table.to_csv(index=False), encoding="utf-8")
    np.savez_compressed(MATRICES, **matrices)
    HASH.write_text(
        f"{hashlib.sha256(payload.encode('utf-8')).hexdigest()}  data/derived/{OUTPUT.name}\n",
        encoding="utf-8",
    )
    REPORT.write_text(
        "# EDGE--CALIFA source-only preflight v02\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The 125-galaxy packet yields `{len(eligible)}` v02 source-eligible galaxies: "
        f"`{len(development)}` development-only and `{len(confirmatory)}` untouched "
        "confirmatory objects.  The cohort, five-zone edges, standard/body matrices, "
        "and deterministic split are now frozen.\n\n"
        "No CO or Halpha velocity value was requested or opened.  v02 remains a "
        "source-developed prevalidation route because its support policy and six-sector "
        "resolution were chosen after source-coverage inspection.\n",
        encoding="utf-8",
    )
    print(result["status"], eligible, confirmatory)
    if not ready:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
