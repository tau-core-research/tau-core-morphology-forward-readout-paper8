#!/usr/bin/env python3
"""Open the frozen EDGE--CALIFA velocity endpoint without post-open repair."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import h5py
import numpy as np
import pandas as pd

from freeze_edge_califa_rotation_morphology_scoring_contract_v01 import (
    N_MODES,
    N_SECTORS,
    N_ZONES,
    assemble_covariance,
    exact_shared_sign_tests,
    fit_modes,
    phase_rotate_pi_over_2,
    radial_reverse,
    score,
    sector_jackknife_block,
    stable_rank,
)
from run_edge_califa_source_only_preflight_v01 import (
    EXPECTED_MD5,
    EXPECTED_SIZE,
    REQUESTED_FIELDS,
    load_source_frame,
    md5,
    read_fields,
    sha256,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
PREREG = DATA / "edge_califa_rotation_morphology_preregistration_v03.json"
PREFLIGHT = DATA / "edge_califa_rotation_morphology_source_preflight_v02.json"
SOURCE_TABLE = DATA / "edge_califa_rotation_morphology_source_preflight_v02.csv"
SOURCE_MATRICES = DATA / "edge_califa_rotation_morphology_source_matrices_v02.npz"
CALIBRATION = DATA / "edge_califa_velocity_frame_calibration_v01.json"
CALIBRATION_TABLE = DATA / "edge_califa_velocity_frame_calibration_v01.csv"
CONTRACT = DATA / "edge_califa_rotation_morphology_scoring_contract_v01.json"
IMPLEMENTATION = DATA / "edge_califa_rotation_morphology_endpoint_implementation_v01.json"
SCRIPT = Path(__file__).resolve()

C_KM_S = 299792.458
MAX_VELOCITY_ERROR = 20.0
MIN_ZONE_ROWS = 20
TERMINAL_FIELDS = {
    "comom_dil": ["Name", "ix", "iy", "mom1_12", "e_mom1_12"],
    "flux_elines_sm": ["Name", "ix", "iy", "vel_Halpha_sm", "e_vel_Halpha_sm"],
}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def radio_to_relativistic(velocity: np.ndarray) -> np.ndarray:
    u = 1.0 - velocity / C_KM_S
    return C_KM_S * (1.0 - u**2) / (1.0 + u**2)


def optical_to_relativistic(velocity: np.ndarray) -> np.ndarray:
    s = 1.0 + velocity / C_KM_S
    return C_KM_S * (s**2 - 1.0) / (s**2 + 1.0)


def radio_to_relativistic_jacobian(velocity: np.ndarray) -> np.ndarray:
    u = 1.0 - velocity / C_KM_S
    return 4.0 * u / (1.0 + u**2) ** 2


def optical_to_relativistic_jacobian(velocity: np.ndarray) -> np.ndarray:
    s = 1.0 + velocity / C_KM_S
    return 4.0 * s / (1.0 + s**2) ** 2


def self_test() -> dict[str, Any]:
    values = np.array([-250.0, 0.0, 4500.0, 8500.0])
    step = 1.0e-3
    radio_numeric = (
        radio_to_relativistic(values + step) - radio_to_relativistic(values - step)
    ) / (2 * step)
    optical_numeric = (
        optical_to_relativistic(values + step) - optical_to_relativistic(values - step)
    ) / (2 * step)
    radio_error = float(np.max(np.abs(radio_numeric - radio_to_relativistic_jacobian(values))))
    optical_error = float(np.max(np.abs(optical_numeric - optical_to_relativistic_jacobian(values))))
    synthetic_differences = np.array(
        [[1.2, 0.8, 1.0], [0.7, 0.9, 0.6], [1.1, 1.3, 0.9],
         [0.8, 0.5, 0.7], [1.4, 1.0, 1.2], [0.6, 0.7, 0.8], [1.0, 1.1, 0.9]]
    )
    exact = exact_shared_sign_tests(synthetic_differences)
    return {
        "radio_jacobian_max_abs_error": radio_error,
        "optical_jacobian_max_abs_error": optical_error,
        "exact_sign_vectors_for_seven": exact["n_exact_sign_vectors"],
        "all_pass": bool(radio_error < 1.0e-7 and optical_error < 1.0e-7 and exact["n_exact_sign_vectors"] == 128),
    }


def load_terminal_frame(path: Path) -> pd.DataFrame:
    source = load_source_frame(path)
    with h5py.File(path, "r") as handle:
        terminal_frames = [read_fields(handle, table, fields) for table, fields in TERMINAL_FIELDS.items()]
    joined = source
    for frame in terminal_frames:
        joined = joined.merge(frame, on=["Name", "ix", "iy"], how="inner", validate="one_to_one")
    return joined


def radial_source_support(group: pd.DataFrame) -> np.ndarray:
    radius = group["rad_arc"].to_numpy(float)
    angle = group["azi_ang"].to_numpy(float)
    co = group["mom0_12"].to_numpy(float)
    eco = group["e_mom0_12"].to_numpy(float)
    ha = group["flux_Halpha_sm"].to_numpy(float)
    eha = group["e_flux_Halpha_sm"].to_numpy(float)
    stellar = group["sigstar_sm"].to_numpy(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        ha_snr = ha / eha
    return (
        np.isfinite(radius) & np.isfinite(angle)
        & np.isfinite(co) & np.isfinite(eco) & (eco > 0) & (co > 0)
        & np.isfinite(ha) & np.isfinite(eha) & (eha > 0) & (ha_snr >= 3.5)
        & np.isfinite(stellar) & (stellar > 0)
    )


def terminal_for_galaxy(
    name: str,
    group: pd.DataFrame,
    matrices: np.lib.npyio.NpzFile,
    edges: np.ndarray,
    frame_correction: float,
    cross_body: np.ndarray,
) -> dict[str, Any]:
    radius = group["rad_arc"].to_numpy(float)
    angle = np.deg2rad(group["azi_ang"].to_numpy(float))
    raw_co = group["mom1_12"].to_numpy(float)
    raw_co_error = group["e_mom1_12"].to_numpy(float)
    raw_ha = group["vel_Halpha_sm"].to_numpy(float)
    raw_ha_error = group["e_vel_Halpha_sm"].to_numpy(float)
    co_helio_radio = raw_co - frame_correction
    co_rel = radio_to_relativistic(co_helio_radio)
    ha_rel = optical_to_relativistic(raw_ha)
    co_rel_error = np.abs(radio_to_relativistic_jacobian(co_helio_radio)) * raw_co_error
    ha_rel_error = np.abs(optical_to_relativistic_jacobian(raw_ha)) * raw_ha_error
    contrast = co_rel - ha_rel
    variance = co_rel_error**2 + ha_rel_error**2
    base_support = radial_source_support(group)
    terminal_support = (
        base_support
        & np.isfinite(raw_co) & np.isfinite(raw_co_error) & (raw_co_error > 0)
        & np.isfinite(raw_ha) & np.isfinite(raw_ha_error) & (raw_ha_error > 0)
        & np.isfinite(co_rel) & np.isfinite(ha_rel) & np.isfinite(variance) & (variance > 0)
        & (co_rel_error <= MAX_VELOCITY_ERROR) & (ha_rel_error <= MAX_VELOCITY_ERROR)
    )

    coefficients = []
    covariance_blocks = []
    rows = []
    for zone in range(N_ZONES):
        select = terminal_support & (radius >= edges[zone]) & (
            radius <= edges[zone + 1] if zone == N_ZONES - 1 else radius < edges[zone + 1]
        )
        if int(select.sum()) < MIN_ZONE_ROWS:
            raise RuntimeError(f"zone {zone} has only {int(select.sum())} terminal rows")
        zone_angle = angle[select]
        sectors = np.floor(
            ((zone_angle + np.pi) % (2 * np.pi)) / (2 * np.pi) * N_SECTORS
        ).astype(int)
        if set(np.unique(sectors)) != set(range(N_SECTORS)):
            raise RuntimeError(f"zone {zone} does not occupy all six terminal macrosectors")
        design = np.column_stack([
            np.ones(select.sum()), np.cos(zone_angle), np.sin(zone_angle),
            np.cos(2 * zone_angle), np.sin(2 * zone_angle),
        ])
        coefficient = fit_modes(design, contrast[select], variance[select])
        covariance_blocks.append(
            sector_jackknife_block(design, contrast[select], variance[select], sectors)
        )
        coefficients.extend(coefficient[1:5])
        for mode, value in zip(("m1_cos", "m1_sin", "m2_cos", "m2_sin"), coefficient[1:5]):
            rows.append({
                "galaxy": name,
                "zone": zone,
                "mode": mode,
                "co_minus_halpha_relativistic_km_s": float(value),
                "n_terminal_rows": int(select.sum()),
                "occupied_macrosectors": int(len(np.unique(sectors))),
                "radius_min_arcsec": float(edges[zone]),
                "radius_max_arcsec": float(edges[zone + 1]),
            })
    covariance = assemble_covariance(covariance_blocks)
    terminal = np.asarray(coefficients, dtype=float)
    standard = matrices[f"{name}__standard"]
    body = matrices[f"{name}__body"]
    sources = {
        "standard": standard,
        "correct": np.column_stack([standard, body]),
        "radial_reversal": np.column_stack([standard, radial_reverse(body)]),
        "phase_rotation_pi_over_2": np.column_stack([standard, phase_rotate_pi_over_2(body)]),
        "cross_galaxy": np.column_stack([standard, cross_body]),
    }
    scores = {label: score(source, covariance, terminal) for label, source in sources.items()}
    if scores["standard"]["projected_covariance_rank"] != 12:
        raise RuntimeError("standard-only projected covariance rank is not 12")
    for label in ("correct", "radial_reversal", "phase_rotation_pi_over_2", "cross_galaxy"):
        if sources[label].shape != (20, 16) or stable_rank(sources[label]) != 16:
            raise RuntimeError(f"{label} source rank gate failed")
        if scores[label]["projection_rank"] != 4 or scores[label]["projected_covariance_rank"] != 4:
            raise RuntimeError(f"{label} projected rank gate failed")
    control_labels = ("radial_reversal", "phase_rotation_pi_over_2", "cross_galaxy")
    control_differences = {
        label: float(scores[label]["q"] - scores["correct"]["q"]) for label in control_labels
    }
    return {
        "rows": rows,
        "metrics": {
            "terminal_rows_total": int(terminal_support.sum()),
            "frame_correction_subtracted_km_s": float(frame_correction),
            "median_raw_co_velocity_km_s": float(np.nanmedian(raw_co[terminal_support])),
            "median_raw_halpha_velocity_km_s": float(np.nanmedian(raw_ha[terminal_support])),
            "median_relativistic_contrast_km_s": float(np.nanmedian(contrast[terminal_support])),
            "median_co_convention_shift_km_s": float(
                np.nanmedian(co_rel[terminal_support] - co_helio_radio[terminal_support])
            ),
            "median_halpha_convention_shift_km_s": float(
                np.nanmedian(ha_rel[terminal_support] - raw_ha[terminal_support])
            ),
            "terminal_covariance_rank": stable_rank(covariance),
            "terminal_covariance_minimum_eigenvalue": float(np.min(np.linalg.eigvalsh(covariance))),
            "scores": scores,
            "control_differences": control_differences,
            "primary_d": float(np.mean(list(control_differences.values()))),
            "standard_minus_correct_q_diagnostic": float(scores["standard"]["q"] - scores["correct"]["q"]),
        },
    }


def write_result(role: str, result: dict[str, Any], rows: list[dict[str, Any]] | None = None) -> None:
    stem = f"edge_califa_rotation_morphology_{role}_endpoint_v01"
    output = DATA / f"{stem}.json"
    report = REPORTS / f"{stem}.md"
    digest_file = DATA / f"{stem}.sha256"
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output.write_text(payload, encoding="utf-8")
    digest_file.write_text(
        f"{hashlib.sha256(payload.encode('utf-8')).hexdigest()}  data/derived/{output.name}\n",
        encoding="utf-8",
    )
    if rows is not None:
        pd.DataFrame(rows).to_csv(DATA / f"{stem}_coefficients.csv", index=False)
    report.write_text(
        f"# EDGE--CALIFA rotation-morphology {role} endpoint v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"{result['summary']}\n\n"
        "This is source-developed external prevalidation. It is not a unique Tau Core "
        "prediction, a dark-sector detection, or an exhaustive rejection of standard "
        "galaxy astrophysics.\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True, choices=("development", "confirmatory"))
    parser.add_argument("--input", type=Path, default=Path("/tmp/edge_carma.2d_smo7.hdf5"))
    args = parser.parse_args()

    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    calibration = json.loads(CALIBRATION.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    implementation = json.loads(IMPLEMENTATION.read_text(encoding="utf-8"))
    checks = {
        "preregistration": (PREREG, contract["preregistration_sha256"]),
        "source_preflight": (PREFLIGHT, contract["source_preflight_sha256"]),
        "source_matrices": (SOURCE_MATRICES, contract["source_matrices_sha256"]),
        "endpoint_script": (SCRIPT, implementation["endpoint_script_sha256"]),
    }
    for label, (path, expected) in checks.items():
        if file_sha256(path) != expected:
            raise RuntimeError(f"Frozen {label} hash mismatch")
    if prereg["endpoint_opened"] or preflight["velocity_terminal_values_opened"]:
        raise RuntimeError("The frozen pre-opening records are inconsistent")
    if args.input.stat().st_size != EXPECTED_SIZE or md5(args.input) != EXPECTED_MD5:
        raise RuntimeError("Published EDGE HDF5 packet hash/size mismatch")
    if calibration["correction_table_sha256"] != file_sha256(CALIBRATION_TABLE):
        raise RuntimeError("Frozen frame-correction table hash mismatch")
    if not self_test()["all_pass"]:
        raise RuntimeError("Endpoint implementation self-test failed")

    role_key = "development_no_claim" if args.role == "development" else "confirmatory_untouched"
    names = list(preflight[role_key])
    if args.role == "confirmatory" and names != contract["confirmatory_galaxies"]:
        raise RuntimeError("Confirmatory membership changed after contract freeze")
    frame_corrections = pd.read_csv(CALIBRATION_TABLE).set_index("galaxy")
    source_table = pd.read_csv(SOURCE_TABLE).set_index("galaxy")
    matrices = np.load(SOURCE_MATRICES)
    terminal_frame = load_terminal_frame(args.input)
    opened: dict[str, Any] = {}
    failures: dict[str, str] = {}
    for index, name in enumerate(names):
        cross_name = (
            names[(index + 1) % len(names)]
            if args.role == "confirmatory"
            else preflight["confirmatory_untouched"][0]
        )
        try:
            edges = matrices[f"{name}__edges"]
            frozen_edges = np.asarray(json.loads(source_table.loc[name, "radial_edges_arcsec"]), float)
            if not np.array_equal(edges, frozen_edges):
                raise RuntimeError("frozen radial edges changed")
            opened[name] = terminal_for_galaxy(
                name,
                terminal_frame.loc[terminal_frame["Name"].eq(name)].copy(),
                matrices,
                edges,
                float(frame_corrections.loc[name, "lsrk_to_heliocentric_subtract_km_s"]),
                matrices[f"{cross_name}__body"],
            )
            opened[name]["metrics"]["cross_galaxy_body"] = cross_name
        except Exception as error:  # one frozen failure closes the corresponding role
            failures[name] = f"{type(error).__name__}: {error}"

    provenance = {
        "input_md5": EXPECTED_MD5,
        "input_sha256": sha256(args.input),
        "preregistration_sha256": file_sha256(PREREG),
        "scoring_contract_sha256": file_sha256(CONTRACT),
        "endpoint_implementation_sha256": file_sha256(SCRIPT),
    }
    if failures:
        result = {
            "schema": f"edge_califa_rotation_morphology_{args.role}_endpoint_v01",
            "status": f"{args.role.upper()}_ENDPOINT_OPENED_FROZEN_GATE_FAILURE_NO_SCORE_RELEASED",
            "galaxies_opened_once": names,
            "failures": failures,
            "scores_released": False,
            "replacement_or_repair_allowed": False,
            "provenance": provenance,
            "summary": (
                "At least one frozen support/rank/covariance gate failed after terminal opening. "
                "No partial or aggregate score is released and no same-packet repair is allowed."
            ),
        }
        write_result(args.role, result)
        print(result["status"], failures)
        return

    all_rows = [row for name in names for row in opened[name]["rows"]]
    metrics = {name: opened[name]["metrics"] for name in names}
    if args.role == "development":
        result = {
            "schema": "edge_califa_rotation_morphology_development_endpoint_v01",
            "status": "DEVELOPMENT_PIPELINE_EXECUTED_NO_CLAIM_NO_RETUNING",
            "galaxies_opened_once": names,
            "galaxies": metrics,
            "inference_performed": False,
            "threshold_or_protocol_change_authorized": False,
            "provenance": provenance,
            "summary": (
                "The single development galaxy passed the frozen terminal pipeline. Its values "
                "are diagnostic only and cannot change the confirmatory protocol."
            ),
        }
        write_result(args.role, result, all_rows)
        print(result["status"])
        return

    differences = np.asarray([
        [
            metrics[name]["control_differences"]["radial_reversal"],
            metrics[name]["control_differences"]["phase_rotation_pi_over_2"],
            metrics[name]["control_differences"]["cross_galaxy"],
        ]
        for name in names
    ])
    inference = exact_shared_sign_tests(differences)
    positive_fraction = inference["positive_primary_count"] / len(names)
    pass_flags = {
        "primary_exact_p_below_0_01": inference["primary_exact_one_sided_p"] < 0.01,
        "median_primary_d_positive": inference["median_primary_d"] > 0,
        "strictly_more_than_60_percent_primary_d_positive": positive_fraction > 0.60,
        "all_three_max_t_adjusted_control_p_below_0_05": all(
            value < 0.05 for value in inference["control_max_t_adjusted_p"]
        ),
    }
    detection = all(pass_flags.values())
    status = (
        "SOURCE_DEVELOPED_EXTERNAL_MORPHOLOGY_ALIGNMENT_PREVALIDATION_PASS"
        if detection else "SOURCE_DEVELOPED_EXTERNAL_MORPHOLOGY_ALIGNMENT_PREVALIDATION_FAIL"
    )
    result = {
        "schema": "edge_califa_rotation_morphology_confirmatory_endpoint_v01",
        "status": status,
        "galaxies_opened_once": names,
        "galaxies": metrics,
        "exact_inference": inference,
        "positive_primary_fraction": positive_fraction,
        "decision_gates": pass_flags,
        "preregistered_prevalidation_pass": detection,
        "replacement_or_repair_allowed": False,
        "physical_tau_source_identified": False,
        "beyond_standard_component_identified": False,
        "dark_sector_identified": False,
        "provenance": provenance,
        "summary": (
            f"The frozen seven-galaxy exact endpoint returned `{status}`. The one-sided exact "
            f"primary p-value is {inference['primary_exact_one_sided_p']:.8f}; "
            f"{inference['positive_primary_count']}/{len(names)} galaxies have positive D."
        ),
        "claim_boundary": (
            "the endpoint tests a source-developed morphology-alignment proxy beyond a declared "
            "low-dimensional nuisance span and equal-rank controls; it neither identifies a "
            "unique Tau source law nor exhausts standard astrophysical alternatives"
        ),
    }
    write_result(args.role, result, all_rows)
    print(status, inference)


if __name__ == "__main__":
    main()
