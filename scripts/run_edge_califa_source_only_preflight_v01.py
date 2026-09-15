#!/usr/bin/env python3
"""Freeze the EDGE--CALIFA cohort from non-velocity source fields only."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import h5py
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
PREREG = DATA / "edge_califa_rotation_morphology_preregistration_v01.json"
OUTPUT = DATA / "edge_califa_rotation_morphology_source_preflight_v01.json"
TABLE = DATA / "edge_califa_rotation_morphology_source_preflight_v01.csv"
MATRICES = DATA / "edge_califa_rotation_morphology_source_matrices_v01.npz"
HASH = DATA / "edge_califa_rotation_morphology_source_preflight_v01.sha256"
REPORT = ROOT / "reports/edge_califa_rotation_morphology_source_preflight_v01.md"

N_ZONES = 5
N_SECTORS = 12
RELATIVE_SVD_TOLERANCE = 1.0e-10
EXPECTED_SIZE = 84941807
EXPECTED_MD5 = "b7e308d0985e8f85ef7afbe1ec4c48b8"

REQUESTED_FIELDS = {
    "comom_dil": [
        "Name", "ix", "iy", "rad_arc", "azi_ang", "cosi", "snrpk_12",
        "mom0_12", "e_mom0_12",
    ],
    "ELINES_sm": ["Name", "ix", "iy", "Vdisp_sm"],
    "flux_elines_sm": [
        "Name", "ix", "iy", "flux_Halpha_sm", "e_flux_Halpha_sm",
        "flux_[SII]6717_sm", "flux_[SII]6731_sm", "flux_sigsfr_adopt_sm",
    ],
    "SSP_sm": ["Name", "ix", "iy", "sigstar_sm"],
}


def md5(path: Path) -> str:
    digest = hashlib.md5()  # noqa: S324 - required to verify the published checksum
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_fields(handle: h5py.File, path: str, fields: list[str]) -> pd.DataFrame:
    dataset = handle[path]
    missing = sorted(set(fields) - set(dataset.dtype.names or ()))
    if missing:
        raise RuntimeError(f"Missing fields in {path}: {missing}")
    record = dataset.fields(fields)[()]
    frame = pd.DataFrame.from_records(record)
    frame["Name"] = frame["Name"].str.decode("ascii")
    if frame.duplicated(["Name", "ix", "iy"]).any():
        raise RuntimeError(f"Duplicate source keys in {path}")
    return frame


def load_source_frame(path: Path) -> pd.DataFrame:
    frames = []
    with h5py.File(path, "r") as handle:
        for table, fields in REQUESTED_FIELDS.items():
            frames.append(read_fields(handle, table, fields))
    joined = frames[0]
    for frame in frames[1:]:
        joined = joined.merge(frame, on=["Name", "ix", "iy"], how="inner", validate="one_to_one")
    return joined


def stable_rank(array: np.ndarray) -> int:
    singular = np.linalg.svd(array, compute_uv=False)
    if singular.size == 0 or singular[0] == 0:
        return 0
    return int(np.sum(singular > RELATIVE_SVD_TOLERANCE * singular[0]))


def normalized(vector: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(vector))
    if not np.isfinite(norm) or norm <= 1.0e-12:
        raise RuntimeError("Null or non-finite frozen source column")
    return vector / norm


def harmonic_profile(
    values: np.ndarray,
    radius: np.ndarray,
    angle: np.ndarray,
    support: np.ndarray,
    edges: np.ndarray,
    mode: int,
) -> np.ndarray:
    profile = []
    for zone in range(N_ZONES):
        select = support & (radius >= edges[zone]) & (
            radius <= edges[zone + 1] if zone == N_ZONES - 1 else radius < edges[zone + 1]
        )
        weights = np.where(select, np.clip(values, 0.0, None), 0.0)
        total = float(np.sum(weights))
        if int(select.sum()) < 20 or not np.isfinite(total) or total <= 0:
            raise RuntimeError(f"Insufficient source profile support in zone {zone}")
        profile.append(np.sum(weights * np.exp(1j * mode * angle)) / total)
    return np.asarray(profile, dtype=complex)


def embed(profile: np.ndarray, mode: int) -> np.ndarray:
    vector = np.zeros(4 * N_ZONES, dtype=float)
    offset = 0 if mode == 1 else 2
    for zone, value in enumerate(profile):
        vector[4 * zone + offset] = value.real
        vector[4 * zone + offset + 1] = value.imag
    return normalized(vector)


def finite_difference(profile: np.ndarray) -> np.ndarray:
    return np.gradient(profile)


def lag_template(linear: bool) -> np.ndarray:
    vector = np.zeros(4 * N_ZONES, dtype=float)
    amplitude = np.arange(N_ZONES, dtype=float) - (N_ZONES - 1) / 2 if linear else np.ones(N_ZONES)
    for zone, value in enumerate(amplitude):
        vector[4 * zone] = value
    return normalized(vector)


def split_role(name: str) -> str:
    bucket = int(hashlib.sha256(name.encode("ascii")).hexdigest()[:8], 16) % 3
    return "development_no_claim" if bucket == 0 else "confirmatory_untouched"


def source_products(group: pd.DataFrame) -> tuple[dict[str, Any], dict[str, np.ndarray] | None]:
    radius = group["rad_arc"].to_numpy(float)
    angle = np.deg2rad(group["azi_ang"].to_numpy(float))
    co = group["mom0_12"].to_numpy(float)
    eco = group["e_mom0_12"].to_numpy(float)
    peak = group["snrpk_12"].to_numpy(float)
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
        co_snr = co / eco
        ha_snr = ha / eha
        sii_ratio = sii / ha
    common = (
        np.isfinite(radius) & np.isfinite(angle)
        & np.isfinite(co) & np.isfinite(eco) & (eco > 0) & (co_snr >= 3.5)
        & np.isfinite(peak) & (peak >= 3.5)
        & np.isfinite(ha) & np.isfinite(eha) & (eha > 0) & (ha_snr >= 3.5)
        & np.isfinite(stellar) & (stellar > 0)
        & np.isfinite(dispersion) & (dispersion > 0)
        & np.isfinite(sfr) & (sfr > 0)
        & np.isfinite(sii_ratio) & (sii_ratio > 0)
    )
    cosi = float(np.nanmedian(group["cosi"].to_numpy(float)))
    base = {
        "n_rows": int(len(group)),
        "common_source_rows": int(common.sum()),
        "median_cosi": cosi,
        "inclination_gate": bool(0.3420201433 <= cosi <= 0.8660254038),
        "minimum_common_rows_gate": bool(common.sum() >= 120),
        "source_sector_gate": False,
        "body_rank": None,
        "standard_rank": None,
        "combined_rank": None,
        "complement_dimension": None,
    }
    if not base["inclination_gate"] or not base["minimum_common_rows_gate"]:
        return base, None
    edges = np.quantile(radius[common], np.linspace(0.0, 1.0, N_ZONES + 1))
    if np.any(np.diff(edges) <= 0):
        return base, None
    sector_counts = []
    for zone in range(N_ZONES):
        select = common & (radius >= edges[zone]) & (
            radius <= edges[zone + 1] if zone == N_ZONES - 1 else radius < edges[zone + 1]
        )
        sectors = np.floor(((angle[select] + np.pi) % (2 * np.pi)) / (2 * np.pi) * N_SECTORS).astype(int)
        sector_counts.append(int(len(np.unique(sectors))))
    base["source_sector_counts"] = sector_counts
    base["source_sector_gate"] = all(count == N_SECTORS for count in sector_counts)
    base["radial_edges_arcsec"] = edges.tolist()
    if not base["source_sector_gate"]:
        return base, None

    profiles = {}
    for label, values in {
        "stellar": stellar,
        "co": co,
        "dispersion": dispersion,
        "sii_ratio": sii_ratio,
        "sfr": sfr,
    }.items():
        for mode in (1, 2):
            profiles[f"{label}_m{mode}"] = harmonic_profile(
                values, radius, angle, common, edges, mode
            )
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
    base.update({
        "body_rank": stable_rank(body),
        "standard_rank": stable_rank(standard),
        "combined_rank": stable_rank(combined),
        "complement_dimension": int(20 - stable_rank(combined)),
    })
    base["rank_gate"] = bool(
        base["body_rank"] == 8
        and base["standard_rank"] == 8
        and base["combined_rank"] == 16
        and base["complement_dimension"] == 4
    )
    if not base["rank_gate"]:
        return base, None
    return base, {"body": body, "standard": standard, "combined": combined, "edges": edges}


def run(path: Path) -> tuple[dict[str, Any], pd.DataFrame, dict[str, np.ndarray]]:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    if prereg["endpoint_opened"] or prereg["construction_uses_velocity_values"]:
        raise RuntimeError("Preregistration opening boundary is invalid")
    file_md5 = md5(path)
    published_file = path.stat().st_size == EXPECTED_SIZE
    if published_file and file_md5 != EXPECTED_MD5:
        raise RuntimeError("Published EDGE HDF5 checksum mismatch")
    forbidden = set(prereg["source_only_fields"]["explicitly_forbidden_during_source_freeze"])
    requested = {f"{table}.{field}" for table, fields in REQUESTED_FIELDS.items() for field in fields}
    if requested & forbidden:
        raise RuntimeError("A terminal field entered the source-only preflight")

    frame = load_source_frame(path)
    excluded = set(prereg["historical_overlap"]["excluded_from_development_and_confirmation"])
    rows = []
    matrices: dict[str, np.ndarray] = {}
    eligible = []
    for name, group in frame.groupby("Name", sort=True):
        metrics, products = source_products(group)
        if name in excluded:
            disposition = "HISTORICAL_LEVY_2018_KSS_EXCLUDED"
        elif products is None:
            disposition = "SOURCE_ONLY_GATE_FAILED"
        else:
            disposition = split_role(name).upper()
            eligible.append(name)
            for label, array in products.items():
                matrices[f"{name}__{label}"] = array
        rows.append({"galaxy": name, "disposition": disposition, **metrics})
    audit = pd.DataFrame(rows)
    development = sorted(audit.loc[audit.disposition.eq("DEVELOPMENT_NO_CLAIM"), "galaxy"].tolist())
    confirmatory = sorted(audit.loc[audit.disposition.eq("CONFIRMATORY_UNTOUCHED"), "galaxy"].tolist())
    ready = len(confirmatory) >= prereg["deterministic_split"]["minimum_confirmatory_galaxies"]
    result = {
        "schema": "edge_califa_rotation_morphology_source_preflight_v01",
        "status": (
            "SOURCE_ONLY_COHORT_FROZEN_ENDPOINT_REMAINS_UNOPENED"
            if ready else "SOURCE_ONLY_COHORT_INSUFFICIENT_NO_ENDPOINT_OPENING"
        ),
        "input_file": path.name,
        "input_size_bytes": path.stat().st_size,
        "input_md5": file_md5,
        "input_sha256": sha256(path),
        "matches_published_file_size": published_file,
        "matches_published_md5": bool(published_file and file_md5 == EXPECTED_MD5),
        "requested_source_fields": REQUESTED_FIELDS,
        "velocity_terminal_fields_requested": False,
        "velocity_terminal_values_opened": False,
        "historical_excluded": sorted(excluded),
        "source_eligible": sorted(eligible),
        "development_no_claim": development,
        "confirmatory_untouched": confirmatory,
        "n_total_galaxies": int(audit.shape[0]),
        "n_source_eligible": len(eligible),
        "n_development": len(development),
        "n_confirmatory": len(confirmatory),
        "minimum_confirmatory": prereg["deterministic_split"]["minimum_confirmatory_galaxies"],
        "endpoint_opening_authorized": ready,
        "claim_boundary": (
            "source-only cohort and operator-rank freeze; no CO--Halpha velocity contrast, "
            "endpoint statistic, Tau signal, or dark-sector evidence"
        ),
    }
    return result, audit, matrices


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("/tmp/edge_carma.2d_smo7.hdf5"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result, table, matrices = run(args.input)
    if args.dry_run:
        print(json.dumps({k: result[k] for k in (
            "status", "n_total_galaxies", "n_source_eligible", "n_development", "n_confirmatory"
        )}, indent=2))
        return
    DATA.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8")
    TABLE.write_text(table.to_csv(index=False), encoding="utf-8")
    np.savez_compressed(MATRICES, **matrices)
    HASH.write_text(
        f"{hashlib.sha256(payload.encode('utf-8')).hexdigest()}  data/derived/{OUTPUT.name}\n",
        encoding="utf-8",
    )
    REPORT.write_text(
        "# EDGE--CALIFA source-only preflight v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The published packet contains `{result['n_total_galaxies']}` galaxies.  After the "
        f"17-galaxy historical exclusion and all source-only support, geometry, sector, and "
        f"rank gates, `{result['n_source_eligible']}` remain: `{result['n_development']}` "
        f"development-only and `{result['n_confirmatory']}` untouched confirmatory galaxies.\n\n"
        "No CO or Halpha velocity value was requested or opened.  A failed source-only gate "
        "cannot be repaired after endpoint opening.\n",
        encoding="utf-8",
    )
    print(result["status"], result["n_source_eligible"], result["n_confirmatory"])
    if not result["endpoint_opening_authorized"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
