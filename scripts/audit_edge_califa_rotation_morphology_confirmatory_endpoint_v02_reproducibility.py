#!/usr/bin/env python3
"""Independent saved-artifact audit of the EDGE--CALIFA v02 endpoint.

This module deliberately does not import the endpoint or scoring-contract
implementation.  It reconstructs the terminal coefficients, covariance,
weighted projections, scores, contrasts, and exact tests from the published
HDF5 packet and the frozen saved artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import warnings
from pathlib import Path
from typing import Any

import h5py
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"

ENDPOINT = DATA / "edge_califa_rotation_morphology_confirmatory_endpoint_v02.json"
ENDPOINT_HASH = DATA / "edge_califa_rotation_morphology_confirmatory_endpoint_v02.sha256"
COEFFICIENTS = DATA / "edge_califa_rotation_morphology_confirmatory_endpoint_v02_coefficients.csv"
PREREGISTRATION = DATA / "edge_califa_rotation_morphology_preregistration_v04.json"
PREREGISTRATION_HASH = DATA / "edge_califa_rotation_morphology_preregistration_v04.sha256"
CONTRACT = DATA / "edge_califa_rotation_morphology_scoring_contract_v02.json"
CONTRACT_HASH = DATA / "edge_califa_rotation_morphology_scoring_contract_v02.sha256"
PREFLIGHT = DATA / "edge_califa_rotation_morphology_source_preflight_v02.json"
PREFLIGHT_HASH = DATA / "edge_califa_rotation_morphology_source_preflight_v02.sha256"
SOURCE_MATRICES = DATA / "edge_califa_rotation_morphology_source_matrices_v02.npz"
IMPLEMENTATION = DATA / "edge_califa_rotation_morphology_endpoint_implementation_v02.json"
IMPLEMENTATION_HASH = DATA / "edge_califa_rotation_morphology_endpoint_implementation_v02.sha256"
ENDPOINT_SCRIPT = ROOT / "scripts/run_edge_califa_rotation_morphology_endpoint_v02.py"
CALIBRATION = DATA / "edge_califa_velocity_frame_calibration_v01.json"
CALIBRATION_HASH = DATA / "edge_califa_velocity_frame_calibration_v01.sha256"
CALIBRATION_TABLE = DATA / "edge_califa_velocity_frame_calibration_v01.csv"

OUTPUT = DATA / "edge_califa_rotation_morphology_confirmatory_endpoint_v02_reproducibility_audit.json"
REPORT = REPORTS / "edge_califa_rotation_morphology_confirmatory_endpoint_v02_reproducibility_audit.md"

N_ZONES = 5
N_MODES = 4
N_SECTORS = 6
MIN_OCCUPIED_SECTORS = 5
MIN_ZONE_ROWS = 20
MAX_VELOCITY_ERROR = 20.0
C_KM_S = 299792.458
RELATIVE_SVD_TOLERANCE = 1.0e-10
NULL_ABSOLUTE_TOLERANCE = 1.0e-8
NUMERIC_RTOL = 2.0e-9
NUMERIC_ATOL = 2.0e-9
MODES = ("m1_cos", "m1_sin", "m2_cos", "m2_sin")
CONTROL_LABELS = ("radial_reversal", "phase_rotation_pi_over_2", "cross_galaxy")

SOURCE_FIELDS = {
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
TERMINAL_FIELDS = {
    "comom_dil": ["Name", "ix", "iy", "mom1_12", "e_mom1_12"],
    "flux_elines_sm": ["Name", "ix", "iy", "vel_Halpha_sm", "e_vel_Halpha_sm"],
}


def file_digest(path: Path, algorithm: str = "sha256") -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sidecar_digest(path: Path) -> str:
    fields = path.read_text(encoding="utf-8").strip().split()
    if len(fields) < 2 or len(fields[0]) != 64:
        raise ValueError(f"Malformed SHA-256 sidecar: {path}")
    return fields[0]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_rank(array: np.ndarray) -> int:
    singular = np.linalg.svd(array, compute_uv=False)
    if singular.size == 0 or singular[0] == 0:
        return 0
    return int(np.sum(singular > RELATIVE_SVD_TOLERANCE * singular[0]))


def fit_modes(design: np.ndarray, values: np.ndarray, variance: np.ndarray) -> np.ndarray:
    weight = 1.0 / variance
    normal = design.T @ (weight[:, None] * design)
    rhs = design.T @ (weight * values)
    return np.linalg.pinv(normal, rcond=RELATIVE_SVD_TOLERANCE) @ rhs


def occupied_sector_jackknife(
    design: np.ndarray, values: np.ndarray, variance: np.ndarray, sectors: np.ndarray
) -> np.ndarray:
    occupied = sorted(int(value) for value in np.unique(sectors))
    if not MIN_OCCUPIED_SECTORS <= len(occupied) <= N_SECTORS:
        raise ValueError("zone does not occupy five or six macrosectors")
    estimates = np.asarray([
        fit_modes(design[sectors != omitted], values[sectors != omitted], variance[sectors != omitted])
        for omitted in occupied
    ])
    centered = estimates - estimates.mean(axis=0)
    covariance = (len(occupied) - 1) / len(occupied) * centered.T @ centered
    return covariance[np.ix_([1, 2, 3, 4], [1, 2, 3, 4])]


def block_diagonal(blocks: list[np.ndarray]) -> np.ndarray:
    size = sum(block.shape[0] for block in blocks)
    result = np.zeros((size, size), dtype=float)
    offset = 0
    for block in blocks:
        stop = offset + block.shape[0]
        result[offset:stop, offset:stop] = block
        offset = stop
    return result


def radial_reverse(body: np.ndarray) -> np.ndarray:
    return body.reshape(N_ZONES, N_MODES, body.shape[1])[::-1].reshape(body.shape)


def phase_rotate_pi_over_2(body: np.ndarray) -> np.ndarray:
    rotated = body.reshape(N_ZONES, N_MODES, body.shape[1]).copy()
    for offset in (0, 2):
        real = rotated[:, offset, :].copy()
        imaginary = rotated[:, offset + 1, :].copy()
        rotated[:, offset, :] = -imaginary
        rotated[:, offset + 1, :] = real
    return rotated.reshape(body.shape)


def score(source: np.ndarray, covariance: np.ndarray, terminal: np.ndarray) -> dict[str, Any]:
    if not (
        np.isfinite(source).all() and np.isfinite(covariance).all()
        and np.isfinite(terminal).all()
    ):
        raise FloatingPointError("non-finite score input")
    # NumPy/Accelerate combinations used on macOS can emit spurious matmul
    # overflow warnings for these finite, moderately scaled matrices.  Keep
    # the endpoint's operation order for bit-level comparison, suppress only
    # those known warnings, and reject any non-finite result immediately.
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=r"(divide by zero|overflow|invalid value) encountered in matmul",
            category=RuntimeWarning,
        )
        inverse = np.linalg.inv(covariance)
        gram = source.T @ inverse @ source
        projection = np.eye(source.shape[0]) - source @ np.linalg.pinv(
            gram, rcond=RELATIVE_SVD_TOLERANCE
        ) @ source.T @ inverse
        innovation = projection @ terminal
        projected_covariance = projection @ covariance @ projection.T
        q_value = float(
            innovation
            @ np.linalg.pinv(projected_covariance, rcond=RELATIVE_SVD_TOLERANCE)
            @ innovation
        )
        annihilation = projection @ source
    if not (
        np.isfinite(inverse).all() and np.isfinite(gram).all()
        and np.isfinite(projection).all() and np.isfinite(innovation).all()
        and np.isfinite(projected_covariance).all() and np.isfinite(q_value)
        and np.isfinite(annihilation).all()
    ):
        raise FloatingPointError("non-finite score reconstruction")
    return {
        "q": max(0.0, q_value),
        "source_rank": stable_rank(source),
        "projection_rank": stable_rank(projection),
        "projected_covariance_rank": stable_rank(projected_covariance),
        "annihilation_max_abs": float(np.max(np.abs(annihilation))),
    }


def studentized_mean(values: np.ndarray) -> float:
    mean = float(np.mean(values))
    scale = float(np.std(values, ddof=1) / np.sqrt(values.size))
    if scale == 0:
        return float(np.sign(mean) * np.inf) if mean != 0 else 0.0
    return mean / scale


def exact_shared_sign_tests(differences: np.ndarray) -> dict[str, Any]:
    primary_values = differences.mean(axis=1)
    observed_primary = float(primary_values.mean())
    observed_t = np.asarray([studentized_mean(differences[:, index]) for index in range(3)])
    primary_null: list[float] = []
    max_t_null: list[float] = []
    for sign_tuple in itertools.product((-1.0, 1.0), repeat=differences.shape[0]):
        signs = np.asarray(sign_tuple)
        signed = signs[:, None] * differences
        primary_null.append(float(np.mean(signs * primary_values)))
        max_t_null.append(max(studentized_mean(signed[:, index]) for index in range(3)))
    primary_null_array = np.asarray(primary_null)
    max_t_null_array = np.asarray(max_t_null)
    tolerance = 1.0e-12
    return {
        "n_galaxies": int(differences.shape[0]),
        "n_exact_sign_vectors": int(2 ** differences.shape[0]),
        "observed_primary_mean_d": observed_primary,
        "primary_exact_one_sided_p": float(
            np.mean(primary_null_array >= observed_primary - tolerance)
        ),
        "control_studentized_statistics": observed_t.tolist(),
        "control_max_t_adjusted_p": [
            float(np.mean(max_t_null_array >= value - tolerance)) for value in observed_t
        ],
        "median_primary_d": float(np.median(primary_values)),
        "positive_primary_count": int(np.sum(primary_values > 0)),
        "primary_tail_count": int(np.sum(primary_null_array >= observed_primary - tolerance)),
    }


def read_fields(handle: h5py.File, table: str, fields: list[str]) -> pd.DataFrame:
    dataset = handle[table]
    missing = sorted(set(fields) - set(dataset.dtype.names or ()))
    if missing:
        raise RuntimeError(f"Missing fields in {table}: {missing}")
    frame = pd.DataFrame.from_records(dataset.fields(fields)[()])
    frame["Name"] = frame["Name"].str.decode("ascii")
    if frame.duplicated(["Name", "ix", "iy"]).any():
        raise RuntimeError(f"Duplicate keys in {table}")
    return frame


def load_terminal_frame(path: Path) -> pd.DataFrame:
    with h5py.File(path, "r") as handle:
        frames = [read_fields(handle, table, fields) for table, fields in SOURCE_FIELDS.items()]
        frames.extend(read_fields(handle, table, fields) for table, fields in TERMINAL_FIELDS.items())
    joined = frames[0]
    for frame in frames[1:]:
        joined = joined.merge(frame, on=["Name", "ix", "iy"], how="inner", validate="one_to_one")
    return joined


def radio_to_relativistic(velocity: np.ndarray) -> np.ndarray:
    u = 1.0 - velocity / C_KM_S
    return C_KM_S * (1.0 - u**2) / (1.0 + u**2)


def optical_to_relativistic(velocity: np.ndarray) -> np.ndarray:
    s = 1.0 + velocity / C_KM_S
    return C_KM_S * (s**2 - 1.0) / (s**2 + 1.0)


def radio_jacobian(velocity: np.ndarray) -> np.ndarray:
    u = 1.0 - velocity / C_KM_S
    return 4.0 * u / (1.0 + u**2) ** 2


def optical_jacobian(velocity: np.ndarray) -> np.ndarray:
    s = 1.0 + velocity / C_KM_S
    return 4.0 * s / (1.0 + s**2) ** 2


def reconstruct_terminal(
    group: pd.DataFrame, edges: np.ndarray, frame_correction: float
) -> tuple[np.ndarray, np.ndarray, list[dict[str, Any]]]:
    radius = group["rad_arc"].to_numpy(float)
    angle = np.deg2rad(group["azi_ang"].to_numpy(float))
    raw_co = group["mom1_12"].to_numpy(float)
    raw_co_error = group["e_mom1_12"].to_numpy(float)
    raw_ha = group["vel_Halpha_sm"].to_numpy(float)
    raw_ha_error = group["e_vel_Halpha_sm"].to_numpy(float)
    co_helio = raw_co - frame_correction
    co_rel = radio_to_relativistic(co_helio)
    ha_rel = optical_to_relativistic(raw_ha)
    co_error = np.abs(radio_jacobian(co_helio)) * raw_co_error
    ha_error = np.abs(optical_jacobian(raw_ha)) * raw_ha_error
    contrast = co_rel - ha_rel
    variance = co_error**2 + ha_error**2
    co0 = group["mom0_12"].to_numpy(float)
    co0_error = group["e_mom0_12"].to_numpy(float)
    ha0 = group["flux_Halpha_sm"].to_numpy(float)
    ha0_error = group["e_flux_Halpha_sm"].to_numpy(float)
    stellar = group["sigstar_sm"].to_numpy(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        ha_snr = ha0 / ha0_error
    base_support = (
        np.isfinite(radius) & np.isfinite(angle)
        & np.isfinite(co0) & np.isfinite(co0_error) & (co0_error > 0) & (co0 > 0)
        & np.isfinite(ha0) & np.isfinite(ha0_error) & (ha0_error > 0) & (ha_snr >= 3.5)
        & np.isfinite(stellar) & (stellar > 0)
    )
    support = (
        base_support
        & np.isfinite(raw_co) & np.isfinite(raw_co_error) & (raw_co_error > 0)
        & np.isfinite(raw_ha) & np.isfinite(raw_ha_error) & (raw_ha_error > 0)
        & np.isfinite(co_rel) & np.isfinite(ha_rel) & np.isfinite(variance) & (variance > 0)
        & (co_error <= MAX_VELOCITY_ERROR) & (ha_error <= MAX_VELOCITY_ERROR)
    )
    coefficients: list[float] = []
    covariance_blocks: list[np.ndarray] = []
    metadata: list[dict[str, Any]] = []
    for zone in range(N_ZONES):
        select = support & (radius >= edges[zone]) & (
            radius <= edges[zone + 1] if zone == N_ZONES - 1 else radius < edges[zone + 1]
        )
        zone_angle = angle[select]
        sectors = np.floor(
            ((zone_angle + np.pi) % (2 * np.pi)) / (2 * np.pi) * N_SECTORS
        ).astype(int)
        design = np.column_stack([
            np.ones(select.sum()), np.cos(zone_angle), np.sin(zone_angle),
            np.cos(2 * zone_angle), np.sin(2 * zone_angle),
        ])
        coefficient = fit_modes(design, contrast[select], variance[select])
        coefficients.extend(float(value) for value in coefficient[1:5])
        covariance_blocks.append(
            occupied_sector_jackknife(design, contrast[select], variance[select], sectors)
        )
        metadata.append({
            "zone": zone,
            "n_terminal_rows": int(select.sum()),
            "occupied_macrosectors": int(len(np.unique(sectors))),
            "radius_min_arcsec": float(edges[zone]),
            "radius_max_arcsec": float(edges[zone + 1]),
        })
    return np.asarray(coefficients), block_diagonal(covariance_blocks), metadata


def isclose(left: float, right: float) -> bool:
    return bool(np.isclose(left, right, rtol=NUMERIC_RTOL, atol=NUMERIC_ATOL))


def allclose(left: Any, right: Any) -> bool:
    return bool(np.allclose(np.asarray(left, float), np.asarray(right, float), rtol=NUMERIC_RTOL, atol=NUMERIC_ATOL))


def add_check(
    checks: list[dict[str, Any]], identifier: str, passed: bool, evidence: Any,
    severity: str = "error",
) -> None:
    checks.append({"id": identifier, "passed": bool(passed), "severity": severity, "evidence": evidence})


def build_audit(input_path: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    endpoint = load_json(ENDPOINT)
    prereg = load_json(PREREGISTRATION)
    contract = load_json(CONTRACT)
    preflight = load_json(PREFLIGHT)
    implementation = load_json(IMPLEMENTATION)
    calibration = load_json(CALIBRATION)

    actual_hashes = {
        "audit_script": file_digest(Path(__file__).resolve()),
        "endpoint_json": file_digest(ENDPOINT),
        "coefficient_csv": file_digest(COEFFICIENTS),
        "preregistration_json": file_digest(PREREGISTRATION),
        "scoring_contract_json": file_digest(CONTRACT),
        "source_preflight_json": file_digest(PREFLIGHT),
        "source_matrices_npz": file_digest(SOURCE_MATRICES),
        "implementation_json": file_digest(IMPLEMENTATION),
        "endpoint_script": file_digest(ENDPOINT_SCRIPT),
        "calibration_json": file_digest(CALIBRATION),
        "calibration_csv": file_digest(CALIBRATION_TABLE),
        "raw_input_sha256": file_digest(input_path),
        "raw_input_md5": file_digest(input_path, "md5"),
    }
    sidecars = {
        "endpoint_json": sidecar_digest(ENDPOINT_HASH),
        "preregistration_json": sidecar_digest(PREREGISTRATION_HASH),
        "scoring_contract_json": sidecar_digest(CONTRACT_HASH),
        "source_preflight_json": sidecar_digest(PREFLIGHT_HASH),
        "implementation_json": sidecar_digest(IMPLEMENTATION_HASH),
        "calibration_json": sidecar_digest(CALIBRATION_HASH),
    }
    for label, expected in sidecars.items():
        add_check(checks, f"hash.sidecar.{label}", actual_hashes[label] == expected, {
            "actual": actual_hashes[label], "sidecar": expected,
        })

    provenance = endpoint["provenance"]
    add_check(checks, "hash.endpoint_to_preregistration", provenance["preregistration_sha256"] == actual_hashes["preregistration_json"], provenance)
    add_check(checks, "hash.endpoint_to_contract", provenance["scoring_contract_sha256"] == actual_hashes["scoring_contract_json"], provenance)
    add_check(checks, "hash.endpoint_to_executed_script", provenance["endpoint_implementation_sha256"] == actual_hashes["endpoint_script"], provenance)
    add_check(checks, "hash.implementation_to_script", implementation["endpoint_script_sha256"] == actual_hashes["endpoint_script"], implementation["endpoint_script_sha256"])
    add_check(checks, "hash.implementation_to_preregistration", implementation["preregistration_sha256"] == actual_hashes["preregistration_json"], implementation["preregistration_sha256"])
    add_check(checks, "hash.implementation_to_contract", implementation["scoring_contract_sha256"] == actual_hashes["scoring_contract_json"], implementation["scoring_contract_sha256"])
    add_check(checks, "hash.implementation_to_preflight", implementation["source_preflight_sha256"] == actual_hashes["source_preflight_json"], implementation["source_preflight_sha256"])
    add_check(checks, "hash.contract_to_preregistration", contract["preregistration_sha256"] == actual_hashes["preregistration_json"], contract["preregistration_sha256"])
    add_check(checks, "hash.contract_to_preflight", contract["source_preflight_sha256"] == actual_hashes["source_preflight_json"], contract["source_preflight_sha256"])
    add_check(checks, "hash.contract_to_source_matrices", contract["source_matrices_sha256"] == actual_hashes["source_matrices_npz"], contract["source_matrices_sha256"])
    frozen_calibration_hash = prereg["velocity_frame_and_convention"]["frame_correction"]["frozen_table_sha256"]
    add_check(checks, "hash.calibration_json_to_csv", calibration["correction_table_sha256"] == actual_hashes["calibration_csv"], calibration["correction_table_sha256"])
    add_check(checks, "hash.preregistration_to_calibration_csv", frozen_calibration_hash == actual_hashes["calibration_csv"], frozen_calibration_hash)
    raw_size = input_path.stat().st_size
    raw_expected = prereg["external_data"]
    add_check(checks, "hash.raw_input_md5", actual_hashes["raw_input_md5"] == raw_expected["md5"] == preflight["input_md5"], actual_hashes["raw_input_md5"])
    add_check(checks, "hash.raw_input_sha256", actual_hashes["raw_input_sha256"] == preflight["input_sha256"] == provenance["input_sha256"], actual_hashes["raw_input_sha256"])
    add_check(checks, "hash.raw_input_size", raw_size == raw_expected["size_bytes"] == preflight["input_size_bytes"], raw_size)

    names = list(endpoint["galaxies_opened_once"])
    membership_sources = {
        "endpoint": names,
        "preregistration": prereg["amendment_audit"]["confirmatory_untouched"],
        "contract": contract["confirmatory_galaxies"],
        "preflight": preflight["confirmatory_untouched"],
    }
    add_check(checks, "cohort.seven_frozen_galaxies", len(names) == 7 and all(value == names for value in membership_sources.values()), membership_sources)

    coefficient_frame = pd.read_csv(COEFFICIENTS)
    expected_sequence = [(name, zone, mode) for name in names for zone in range(N_ZONES) for mode in MODES]
    observed_sequence = list(zip(
        coefficient_frame["galaxy"], coefficient_frame["zone"].astype(int), coefficient_frame["mode"]
    ))
    counts = coefficient_frame.groupby("galaxy").size().to_dict()
    add_check(checks, "coefficients.shape_7_by_20", coefficient_frame.shape[0] == 140 and counts == {name: 20 for name in names}, {"rows": int(coefficient_frame.shape[0]), "per_galaxy": counts})
    add_check(checks, "coefficients.canonical_order", observed_sequence == expected_sequence, {"expected_entries": 140, "observed_entries": len(observed_sequence)})
    add_check(checks, "coefficients.finite", bool(np.isfinite(coefficient_frame["co_minus_halpha_relativistic_km_s"].to_numpy(float)).all()), actual_hashes["coefficient_csv"])

    matrices = np.load(SOURCE_MATRICES)
    calibration_frame = pd.read_csv(CALIBRATION_TABLE).set_index("galaxy")
    terminal_frame = load_terminal_frame(input_path)
    reconstructed: dict[str, Any] = {}
    difference_rows: list[list[float]] = []
    coefficient_residual_max = 0.0
    metric_residual_max = 0.0
    matrix_gate_pass = True
    coefficient_metadata_pass = True
    for index, name in enumerate(names):
        edges = matrices[f"{name}__edges"]
        group = terminal_frame.loc[terminal_frame["Name"].eq(name)].copy()
        terminal, covariance, metadata = reconstruct_terminal(
            group, edges, float(calibration_frame.loc[name, "lsrk_to_heliocentric_subtract_km_s"]),
        )
        saved_rows = coefficient_frame.loc[coefficient_frame["galaxy"].eq(name)]
        saved_terminal = saved_rows["co_minus_halpha_relativistic_km_s"].to_numpy(float)
        coefficient_residual_max = max(coefficient_residual_max, float(np.max(np.abs(terminal - saved_terminal))))
        for zone, zone_metadata in enumerate(metadata):
            four = saved_rows.loc[saved_rows["zone"].eq(zone)]
            coefficient_metadata_pass &= (
                len(four) == 4
                and four["n_terminal_rows"].nunique() == 1
                and int(four["n_terminal_rows"].iloc[0]) == zone_metadata["n_terminal_rows"]
                and four["occupied_macrosectors"].nunique() == 1
                and int(four["occupied_macrosectors"].iloc[0]) == zone_metadata["occupied_macrosectors"]
                and allclose(four["radius_min_arcsec"], [zone_metadata["radius_min_arcsec"]] * 4)
                and allclose(four["radius_max_arcsec"], [zone_metadata["radius_max_arcsec"]] * 4)
                and zone_metadata["n_terminal_rows"] >= MIN_ZONE_ROWS
                and MIN_OCCUPIED_SECTORS <= zone_metadata["occupied_macrosectors"] <= N_SECTORS
            )
        standard = matrices[f"{name}__standard"]
        body = matrices[f"{name}__body"]
        cross_name = names[(index + 1) % len(names)]
        sources = {
            "standard": standard,
            "correct": np.column_stack([standard, body]),
            "radial_reversal": np.column_stack([standard, radial_reverse(body)]),
            "phase_rotation_pi_over_2": np.column_stack([standard, phase_rotate_pi_over_2(body)]),
            "cross_galaxy": np.column_stack([standard, matrices[f"{cross_name}__body"]]),
        }
        scores = {label: score(source, covariance, terminal) for label, source in sources.items()}
        differences = {label: scores[label]["q"] - scores["correct"]["q"] for label in CONTROL_LABELS}
        primary_d = float(np.mean(list(differences.values())))
        difference_rows.append([differences[label] for label in CONTROL_LABELS])
        saved = endpoint["galaxies"][name]
        per_metric_match = True
        for label, rebuilt_score in scores.items():
            saved_score = saved["scores"][label]
            for metric in ("q", "annihilation_max_abs"):
                metric_residual_max = max(metric_residual_max, abs(rebuilt_score[metric] - saved_score[metric]))
                per_metric_match &= isclose(rebuilt_score[metric], saved_score[metric])
            for metric in ("source_rank", "projection_rank", "projected_covariance_rank"):
                per_metric_match &= rebuilt_score[metric] == saved_score[metric]
        per_metric_match &= all(isclose(differences[label], saved["control_differences"][label]) for label in CONTROL_LABELS)
        per_metric_match &= isclose(primary_d, saved["primary_d"])
        per_metric_match &= stable_rank(covariance) == saved["terminal_covariance_rank"] == 20
        per_metric_match &= isclose(float(np.min(np.linalg.eigvalsh(covariance))), saved["terminal_covariance_minimum_eigenvalue"])
        per_metric_match &= saved["cross_galaxy_body"] == cross_name
        expected_ranks = {
            "standard": (8, 12, 12),
            "correct": (16, 4, 4),
            "radial_reversal": (16, 4, 4),
            "phase_rotation_pi_over_2": (16, 4, 4),
            "cross_galaxy": (16, 4, 4),
        }
        rank_and_null = all(
            (
                scores[label]["source_rank"], scores[label]["projection_rank"],
                scores[label]["projected_covariance_rank"],
            ) == expected_ranks[label]
            and scores[label]["annihilation_max_abs"] <= NULL_ABSOLUTE_TOLERANCE
            for label in sources
        )
        rank_and_null &= float(np.min(np.linalg.eigvalsh(covariance))) > 0
        matrix_gate_pass &= per_metric_match and rank_and_null
        reconstructed[name] = {
            "primary_d": primary_d,
            "control_differences": differences,
            "terminal_covariance_rank": stable_rank(covariance),
            "terminal_covariance_minimum_eigenvalue": float(np.min(np.linalg.eigvalsh(covariance))),
            "scores": scores,
            "rank_and_null_gate_pass": bool(rank_and_null),
            "saved_metric_match": bool(per_metric_match),
        }

    add_check(checks, "coefficients.raw_reconstruction", coefficient_residual_max <= NUMERIC_ATOL, {"maximum_absolute_residual_km_s": coefficient_residual_max})
    add_check(checks, "coefficients.metadata_reconstruction", coefficient_metadata_pass, "row count, occupied sectors, and radial edges match raw reconstruction")
    add_check(checks, "matrices.rank_null_and_score_reconstruction", matrix_gate_pass, {"maximum_saved_metric_absolute_residual": metric_residual_max, "null_absolute_tolerance": NULL_ABSOLUTE_TOLERANCE})

    differences_array = np.asarray(difference_rows)
    inference = exact_shared_sign_tests(differences_array)
    saved_inference = endpoint["exact_inference"]
    inference_match = (
        inference["n_galaxies"] == saved_inference["n_galaxies"]
        and inference["n_exact_sign_vectors"] == saved_inference["n_exact_sign_vectors"]
        and isclose(inference["observed_primary_mean_d"], saved_inference["observed_primary_mean_d"])
        and inference["primary_exact_one_sided_p"] == saved_inference["primary_exact_one_sided_p"]
        and allclose(inference["control_studentized_statistics"], saved_inference["control_studentized_statistics"])
        and inference["control_max_t_adjusted_p"] == saved_inference["control_max_t_adjusted_p"]
        and isclose(inference["median_primary_d"], saved_inference["median_primary_d"])
        and inference["positive_primary_count"] == saved_inference["positive_primary_count"]
    )
    add_check(checks, "inference.exact_shared_sign_reconstruction", inference_match, inference)
    add_check(checks, "inference.primary_p_is_77_over_128", inference["primary_tail_count"] == 77 and inference["primary_exact_one_sided_p"] == 0.6015625, {"tail_count": inference["primary_tail_count"], "denominator": 128, "p": inference["primary_exact_one_sided_p"]})
    add_check(checks, "inference.max_t_controls_reconstructed", inference["control_max_t_adjusted_p"] == [0.9765625, 0.9453125, 0.3359375], inference["control_max_t_adjusted_p"])

    positive_fraction = inference["positive_primary_count"] / inference["n_galaxies"]
    gates = {
        "primary_exact_p_below_0_01": inference["primary_exact_one_sided_p"] < 0.01,
        "median_primary_d_positive": inference["median_primary_d"] > 0,
        "strictly_more_than_60_percent_primary_d_positive": positive_fraction > 0.60,
        "all_three_max_t_adjusted_control_p_below_0_05": all(value < 0.05 for value in inference["control_max_t_adjusted_p"]),
    }
    expected_status = (
        "SOURCE_DEVELOPED_EXTERNAL_MORPHOLOGY_ALIGNMENT_PREVALIDATION_PASS"
        if all(gates.values())
        else "SOURCE_DEVELOPED_EXTERNAL_MORPHOLOGY_ALIGNMENT_PREVALIDATION_FAIL"
    )
    negative_match = (
        gates == endpoint["decision_gates"]
        and not endpoint["preregistered_prevalidation_pass"]
        and endpoint["status"] == expected_status
        and not endpoint["physical_tau_source_identified"]
        and not endpoint["beyond_standard_component_identified"]
        and not endpoint["dark_sector_identified"]
    )
    add_check(checks, "decision.negative_status_reconstructed", negative_match, {"gates": gates, "expected_status": expected_status})

    limitations = [
        {
            "id": "freeze_chronology_not_externally_anchored",
            "impact": "The current bytes and their internal hash chain agree, but local sidecars do not independently prove that preregistration and implementation bytes predated endpoint opening. A trusted commit, release, registry, or timestamp is required for that historical claim.",
        },
        {
            "id": "implementation_manifest_runtime_trust_gap",
            "impact": "The endpoint runtime reads the implementation manifest to obtain the expected script hash but does not first pin that manifest to its sidecar or another immutable anchor. The present audit verifies the current manifest sidecar and script relation only.",
        },
        {
            "id": "coefficient_csv_not_in_original_endpoint_provenance",
            "impact": "The original endpoint JSON/sidecar does not bind the coefficient CSV. This audit records its current SHA-256 and independently reconstructs every coefficient from the hash-matched raw packet.",
        },
        {
            "id": "external_raw_packet_not_vendored",
            "impact": "Full matrix-level reproduction requires the 84,941,807-byte public HDF5 packet. It is identified by DOI, MD5 and SHA-256 but is not stored in the repository.",
        },
        {
            "id": "negative_endpoint_not_tau_specific",
            "impact": "The reproduced failure is a negative result for this development-informed proxy only. It neither validates nor falsifies the general Tau Core architecture, and the declared standard/eDIG span is not exhaustive.",
        },
    ]
    failed_errors = [check["id"] for check in checks if check["severity"] == "error" and not check["passed"]]
    status = (
        "PASS_WITH_PROVENANCE_LIMITATIONS_NEGATIVE_ENDPOINT_CONFIRMED"
        if not failed_errors
        else "FAIL_REPRODUCIBILITY_ERROR"
    )
    return {
        "schema": "edge_califa_rotation_morphology_confirmatory_endpoint_v02_reproducibility_audit",
        "status": status,
        "audit_scope": "independent reconstruction from saved frozen artifacts and the hash-matched public raw packet; no import of endpoint/scoring implementation",
        "input_path_used": str(input_path.resolve()),
        "actual_hashes": actual_hashes,
        "checks": checks,
        "failed_error_checks": failed_errors,
        "coefficient_structure": {
            "n_galaxies": len(names), "components_per_galaxy": 20,
            "n_rows": int(coefficient_frame.shape[0]), "mode_order": list(MODES),
            "maximum_absolute_raw_reconstruction_residual_km_s": coefficient_residual_max,
        },
        "reconstructed_galaxies": reconstructed,
        "reconstructed_exact_inference": inference,
        "reconstructed_decision_gates": gates,
        "reconstructed_status": expected_status,
        "limitations": limitations,
        "claim_boundary": (
            "This audit confirms the saved numerical negative endpoint conditional on the hash-matched "
            "raw packet and current artifacts. It does not establish freeze chronology, a Tau-specific law, "
            "a beyond-standard component, dark-sector physics, or exhaustive conventional comparison."
        ),
    }


def render_report(audit: dict[str, Any]) -> str:
    inference = audit["reconstructed_exact_inference"]
    passed = sum(check["passed"] for check in audit["checks"])
    total = len(audit["checks"])
    limitations = "\n".join(
        f"- `{item['id']}`: {item['impact']}" for item in audit["limitations"]
    )
    failures = ", ".join(audit["failed_error_checks"]) if audit["failed_error_checks"] else "none"
    d_rows = "\n".join(
        f"| {name} | {values['primary_d']:.15g} |"
        for name, values in audit["reconstructed_galaxies"].items()
    )
    return f"""# EDGE--CALIFA confirmatory endpoint v02: independent reproducibility audit

Status: `{audit['status']}`

## Result

The independent audit passed {passed}/{total} executable checks. It rebuilt the 7 x 20
terminal packet, all five-zone occupied-sector covariance matrices, source projections,
Q scores, per-galaxy control contrasts, and exact inference without importing the endpoint
or scoring implementation.

- exact primary result: 77/128 = `{inference['primary_exact_one_sided_p']:.7f}`;
- reconstructed mean D: `{inference['observed_primary_mean_d']:.15g}`;
- positive D count: `{inference['positive_primary_count']}/7`;
- max-T adjusted control p-values: `{inference['control_max_t_adjusted_p']}`;
- reconstructed endpoint status: `{audit['reconstructed_status']}`;
- failed executable checks: `{failures}`.

| Galaxy | independently reconstructed D |
| --- | ---: |
{d_rows}

The negative prevalidation status is therefore numerically reproduced. It is not a positive
Tau Core signal and does not identify physics beyond the declared standard comparator.

## Hash and structure audit

The public HDF5 packet matches the frozen size, MD5, and SHA-256. The current preregistration,
scoring contract, source matrices, endpoint script, implementation manifest, calibration table,
and endpoint JSON satisfy their recorded hash relations. The coefficient CSV has SHA-256
`{audit['actual_hashes']['coefficient_csv']}` and all 140 rows reproduce from the raw packet;
the largest coefficient residual is
`{audit['coefficient_structure']['maximum_absolute_raw_reconstruction_residual_km_s']:.3e} km/s`.

For every galaxy, the standard source has rank 8 with a rank-12 complement. The correct and
three wrong-family sources have rank 16 with rank-4 complements; the independently rebuilt
projectors annihilate their source columns below the audit tolerance, and every terminal
covariance is positive definite and rank 20.

## Reproducibility limits

{limitations}

## Claim boundary

{audit['claim_boundary']}
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("/tmp/edge_carma.2d_smo7.hdf5"))
    args = parser.parse_args()
    if not args.input.is_file():
        raise FileNotFoundError(
            f"Raw EDGE packet not found at {args.input}; download the preregistered DOI object "
            "and pass it with --input. Matrix-level verification cannot be inferred from summary JSON."
        )
    audit = build_audit(args.input)
    OUTPUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT.write_text(render_report(audit), encoding="utf-8")
    print(audit["status"])
    if audit["failed_error_checks"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
