#!/usr/bin/env python3
"""Run the explicitly nonphysical SDP.81 4D-corridor proxy diagnostic."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from run_sdp81_common_action_endpoint_v01 import (
    centered_log_modes,
    load_frozen_endpoint,
    score_controls,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
MODEL = DATA / "sdp81_4d_corridor_proxy_diagnostic_freeze_v01.json"
OUT = DATA / "sdp81_4d_corridor_proxy_diagnostic_score_v01.json"
REPORT = ROOT / "reports/sdp81_4d_corridor_proxy_diagnostic_score_v01.md"


def main() -> None:
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    allowed = bool(
        model.get("status") == "DIAGNOSTIC_ONLY_NOT_ENDPOINT"
        and model.get("diagnostic_run_allowed") is True
        and model.get("physical_endpoint_authorized") is False
        and model.get("inputs", {}).get("spectral_or_velocity_endpoint_read") is False
    )
    if not allowed:
        raise RuntimeError("diagnostic proxy was not validly frozen")
    calibration = model["terminal_calibration"]
    basis = np.asarray(calibration["centered_log_channel_basis"], dtype=float)
    path_ids = [item["path_id"] for item in model["compiled_paths"]]
    transfers = [
        np.asarray(item["selected_transfer"], dtype=float)
        for item in model["compiled_paths"]
    ]
    covariances = [
        np.asarray(calibration["mode_noise_covariance_by_path"][path_id], dtype=float)
        for path_id in path_ids
    ]
    spectra = load_frozen_endpoint(model)
    modes = centered_log_modes(spectra, basis)
    scores = score_controls(modes, transfers, covariances)
    wrong = scores["wrong_path_assignment"]
    matched_chi2 = scores["matched"]["total_mahalanobis_chi2"]
    wrong_chi2 = np.asarray([item["total_mahalanobis_chi2"] for item in wrong])
    permutation_fraction_not_worse = float(np.mean(wrong_chi2 <= matched_chi2))
    verdict = (
        "FIXED_4D_PROXY_OUTPERFORMS_BOTH_CONTROLS"
        if scores["matched_beats_lossless"] and scores["matched_beats_wrong_median"]
        else "FIXED_4D_PROXY_NOT_PREFERRED"
    )
    result = {
        "schema": "tau-core.paper8.sdp81-4d-corridor-proxy-diagnostic-score.v01",
        "status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
        "verdict": verdict,
        "model": str(MODEL.relative_to(ROOT)),
        "spectral_endpoint_read": True,
        "score_emitted": True,
        "observed_spectra": spectra.tolist(),
        "observed_centered_log_modes": modes.tolist(),
        "scores": scores,
        "descriptive_permutation_fraction_not_worse": permutation_fraction_not_worse,
        "statistical_caveat": (
            "identity mode covariance makes the quadratic score a sensitivity norm, "
            "not a calibrated chi-square or p-value"
        ),
        "physical_endpoint_authorized": False,
        "claim_boundary": (
            "Retrospective diagnostic of one fixed conventional-4D proxy only. "
            "The result neither identifies parent distance nor tests a physically "
            "occupied Tau action. The endpoint was already opened, and the covariance "
            "is an uncalibrated identity sensitivity metric."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 fixed 4D-corridor proxy diagnostic score v01\n\n"
        f"Status: `{result['status']}`. Verdict: `{verdict}`.\n\n"
        f"Matched sensitivity score: `{matched_chi2:.6g}`; lossless identity: "
        f"`{scores['lossless_identity']['total_mahalanobis_chi2']:.6g}`. "
        f"Matched beats wrong-assignment median: "
        f"`{scores['matched_beats_wrong_median']}`; fraction of wrong assignments "
        f"not worse than matched: `{permutation_fraction_not_worse:.6g}`.\n\n"
        f"{result['statistical_caveat']}\n\n{result['claim_boundary']}\n",
        encoding="utf-8",
    )
    print(verdict)


if __name__ == "__main__":
    main()
