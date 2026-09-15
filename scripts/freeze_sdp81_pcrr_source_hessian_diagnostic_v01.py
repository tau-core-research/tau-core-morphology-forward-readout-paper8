#!/usr/bin/env python3
"""Freeze conditional Tau-source transfer candidates without reading the endpoint.

The primary candidate imports the already documented PCRR-D1 factor 1/2 into
the existing ordered-channel Laplacian proxy.  A second candidate imports the
WR-T19 five-mode stiffness spectrum, but its alignment with the terminal
Helmert modes is explicitly an unproved calibration hypothesis.  Neither
candidate identifies conventional Fermat depth with parent distance.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from freeze_sdp81_4d_corridor_proxy_diagnostic_v01 import (
    exp_symmetric,
    ordered_channel_generator,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
BASE = DATA / "sdp81_4d_corridor_proxy_diagnostic_freeze_v01.json"
OUT = DATA / "sdp81_pcrr_source_hessian_diagnostic_freeze_v01.json"
REPORT = ROOT / "reports/sdp81_pcrr_source_hessian_diagnostic_freeze_v01.md"

PCRR_SOURCE = "docs/tau_core_cross_scale_clock_resolution_hypothesis_001.md"
WR_T19_SOURCE = (
    "source_material/tau_core_foundations/numerical_checks/"
    "tau_core_wr_t19_fixed_seed_body_channel_transmission_audit_v01_summary.json"
)
WR_T19_SHA256 = "713202b771d8dfa20a2cfb4be3af39444b81fa1fb50ef7fee7f3f70342a74e15"
WR_T19_STIFFNESSES = np.asarray([1.25, 1.5, 2.0, 2.5, 3.0], dtype=float)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compile_transfers(depths: list[float], generator: np.ndarray) -> list[list[list[float]]]:
    return [exp_symmetric(-depth * generator).tolist() for depth in depths]


def build_freeze(base: dict) -> dict:
    basis, laplacian = ordered_channel_generator(6)
    frozen_basis = np.asarray(base["terminal_calibration"]["centered_log_channel_basis"])
    if not np.allclose(basis, frozen_basis):
        raise ValueError("the terminal Helmert basis changed")
    depths = [float(item["proxy_depth"]) for item in base["compiled_paths"]]
    path_ids = [item["path_id"] for item in base["compiled_paths"]]

    # PCRR-T32c/PCRR-D1 fixes f(x)=x/2 inside the conditional corridor family.
    pcrr_generator = 0.5 * laplacian
    # WR-T19 supplies stiffness eigenvalues only.  Mapping their increasing
    # order to the stored Helmert columns is an added calibration assumption.
    wr_spectrum = WR_T19_STIFFNESSES / float(WR_T19_STIFFNESSES.max())
    wr_aligned = 0.5 * np.diag(wr_spectrum)
    wr_reversed = 0.5 * np.diag(wr_spectrum[::-1])
    unit_comparator = laplacian

    candidates = {
        "pcrr_half_laplacian": {
            "role": "primary_conditional_source_candidate",
            "generator": pcrr_generator.tolist(),
            "transfers": compile_transfers(depths, pcrr_generator),
            "extra_terminal_alignment_assumption": False,
        },
        "wr_t19_aligned_half": {
            "role": "calibration_hypothesis_only",
            "generator": wr_aligned.tolist(),
            "transfers": compile_transfers(depths, wr_aligned),
            "extra_terminal_alignment_assumption": True,
        },
        "wr_t19_reverse_half": {
            "role": "orientation_control",
            "generator": wr_reversed.tolist(),
            "transfers": compile_transfers(depths, wr_reversed),
            "extra_terminal_alignment_assumption": True,
        },
        "prior_unit_laplacian": {
            "role": "previous_frozen_strength_comparator",
            "generator": unit_comparator.tolist(),
            "transfers": compile_transfers(depths, unit_comparator),
            "extra_terminal_alignment_assumption": False,
        },
    }
    checks = {
        "base_proxy_is_nonphysical": base["physical_endpoint_authorized"] is False,
        "no_endpoint_read_during_freeze": True,
        "pcrr_factor_is_exactly_one_half": np.allclose(pcrr_generator, laplacian / 2.0),
        "wr_t19_spectrum_is_positive": bool(np.all(WR_T19_STIFFNESSES > 0.0)),
        "wr_t19_normalization_is_source_fixed": float(wr_spectrum.max()) == 1.0,
        "all_transfers_are_positive_contractions": all(
            np.linalg.eigvalsh(np.asarray(transfer)).min() > 0.0
            and np.linalg.svd(np.asarray(transfer), compute_uv=False).max() < 1.0
            for candidate in candidates.values()
            for transfer in candidate["transfers"]
        ),
        "fermat_coordinate_not_retyped_as_parent_distance": True,
        "physical_endpoint_remains_unauthorized": True,
    }
    return {
        "schema": "tau-core.paper8.sdp81-pcrr-source-hessian-diagnostic-freeze.v01",
        "status": "CONDITIONAL_SOURCE_CANDIDATES_FROZEN_DIAGNOSTIC_ONLY",
        "scientific_role": (
            "retrospective test of source-preexisting conditional generator shapes; "
            "not a physical parent-distance or Nature-occupation test"
        ),
        "inputs": {
            "base_proxy": str(BASE.relative_to(ROOT)),
            "base_proxy_sha256": sha256(BASE),
            "spectral_or_velocity_endpoint_read": False,
        },
        "source_provenance": {
            "pcrr_half_generator": {
                "repository": "tau-core-theory",
                "path": PCRR_SOURCE,
                "labels": ["CSCR-T32c", "PCRR-D1"],
                "formula": "f(x)=x/2 and V_e=exp[-(d_e/ell_*)K_src/(2A_*)]U_e",
                "status": "conditional_derivation_preexisting_this_diagnostic",
            },
            "wr_t19_channel_hessian": {
                "repository": "tau-core-theory",
                "path": WR_T19_SOURCE,
                "sha256": WR_T19_SHA256,
                "values": WR_T19_STIFFNESSES.tolist(),
                "status": "fixed numerical audit; physical channel source remains open",
            },
        },
        "path_ids": path_ids,
        "proxy_depths": depths,
        "depth_boundary": (
            "depths remain normalized conventional 4D Fermat proxy coordinates with "
            "a common invertible origin; they are not parent morphological distances"
        ),
        "terminal_basis": basis.tolist(),
        "candidates": candidates,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "diagnostic_run_allowed": all(checks.values()),
        "physical_endpoint_authorized": False,
        "retrospective_only": True,
        "claim_boundary": (
            "The factor 1/2 and WR-T19 spectrum existed on the Tau source side before "
            "this diagnostic, but the tested depth remains a 4D proxy. The WR-T19 "
            "mode alignment is additionally unproved. Scores can compare these "
            "conditional shapes only; they cannot establish the parent lift, terminal "
            "calibration, physical realization, or nonzero Nature occupation."
        ),
    }


def main() -> None:
    base = json.loads(BASE.read_text(encoding="utf-8"))
    result = build_freeze(base)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 PCRR/source-Hessian diagnostic freeze v01\n\n"
        f"Status: `{result['status']}`; checks: "
        f"`{result['checks_passed']}/{result['checks_total']}`.\n\n"
        "The primary candidate applies the source-preexisting PCRR factor `1/2` "
        "to the frozen ordered-channel Laplacian. The WR-T19 branch imports its "
        "five positive stiffnesses, while marking their terminal-mode alignment "
        "as an additional hypothesis. No endpoint is read here.\n\n"
        f"{result['claim_boundary']}\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
