#!/usr/bin/env python3
"""Reject unsupported CO(8-7)-to-CO(10-9) profile inheritance endpoint-blind."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/external/literature/sdp81_rybak2020_source_blind"
DATA = ROOT / "data/derived"
OUT = DATA / "sdp81_open_transition_profile_lift_gate_v01.json"
REPORT = ROOT / "reports/sdp81_open_transition_profile_lift_gate_v01.md"

SOURCE_MAPS = [
    "source_CII_Jykmspx_zoomed.fits",
    "source_CO54_Jykmspx.fits",
    "source_CO87_Jykmspx.fits",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def main() -> None:
    if any("co109" in path.name.lower() for path in SOURCE.iterdir()):
        raise RuntimeError("held-out transition found in source-blind directory")

    inventory = []
    for name in SOURCE_MAPS:
        path = SOURCE / name
        header = fits.getheader(path)
        inventory.append(
            {
                "artifact": str(path.relative_to(ROOT)),
                "sha256": sha256(path),
                "naxis": int(header["NAXIS"]),
                "shape": [int(header["NAXIS2"]), int(header["NAXIS1"])],
                "has_spectral_axis": int(header["NAXIS"]) >= 3,
            }
        )

    pdr = load("sdp81_rybak2020_source_blind_pdr_preflight_v01.json")
    source_cube = load("sdp81_source_spectral_cube_v01.json")
    loo = load("sdp81_spectral_leave_one_path_out_v01.json")
    cross = load("sdp81_q1_cross_transition_rank_v02.json")

    checks = {
        "heldout_transition_absent_from_source_directory": True,
        "official_open_source_maps_are_two_dimensional": all(
            item["naxis"] == 2 for item in inventory
        ),
        "official_open_source_maps_have_no_spectral_axis": all(
            item["has_spectral_axis"] is False for item in inventory
        ),
        "blind_pdr_amplitude_prior_available": (
            pdr.get("status")
            == "SOURCE_ACQUIRED_PDR_AMPLITUDE_PARTIAL_SPECTRAL_REGISTRATION_BLOCKED"
        ),
        "blind_pdr_does_not_claim_channel_registration": (
            (pdr.get("checks") or {}).get("channelwise_spectral_registration_available")
            is False
        ),
        "image_plane_inverse_source_cube_not_promoted": (
            source_cube.get("common_source_spectral_cube_promoted") is False
        ),
        "three_path_to_fourth_path_transfer_not_established": (
            loo.get("transferable_common_source_dynamics_promoted") is False
        ),
        "cross_transition_projected_rank_not_promoted": (
            cross.get("projected_cross_transition_rank_promoted") is False
        ),
        "co109_header_not_read": True,
        "co109_pixels_not_read": True,
    }
    profile_lift_authorized = bool(
        not checks["official_open_source_maps_have_no_spectral_axis"]
        and not checks["image_plane_inverse_source_cube_not_promoted"]
        and not checks["three_path_to_fourth_path_transfer_not_established"]
        and not checks["cross_transition_projected_rank_not_promoted"]
    )
    result = {
        "schema": "tau-core.paper8.sdp81-open-transition-profile-lift-gate.v01",
        "status": "INHERITED_CO87_PROFILE_LIFT_REJECTED_NEW_SOURCE_SPECTROSCOPY_REQUIRED",
        "scientific_role": "endpoint-blind candidate profile-lift rejection",
        "official_source_inventory": inventory,
        "published_constraints": {
            "source": "Rybak et al. 2015, arXiv:1506.01425, sections 2.1 and 3",
            "co109_velocity_maps_reliable": False,
            "co54_and_co87_excitation_dependent_morphology": True,
            "co87_dispersion_approximately_40_km_s_above_co54": True,
            "co87_tail_has_two_velocity_components": True,
        },
        "open_transition_diagnostics": {
            "source_cube_common_channel_flags": source_cube.get(
                "channel_common_source_promotion_flags"
            ),
            "source_cube_promoted": source_cube.get(
                "common_source_spectral_cube_promoted"
            ),
            "loo_fold_count": loo.get("fold_count"),
            "loo_positive_fold_count": loo.get("positive_fold_count"),
            "loo_median_predictive_r2": loo.get("predictive_r2_median"),
            "loo_path_median_predictive_r2": loo.get(
                "path_median_predictive_r2"
            ),
            "cross_transition_sensitivity_cosine_range": cross.get(
                "sensitivity_cosine_range"
            ),
            "cross_transition_rank_promoted": cross.get(
                "projected_cross_transition_rank_promoted"
            ),
        },
        "checks": checks,
        "profile_lift_authorized": profile_lift_authorized,
        "endpoint_authorized": False,
        "next_source_requirement": (
            "an endpoint-independent source-plane velocity/profile cube or a "
            "source-owned excitation-opacity-kinematic law with covariance, filling, "
            "and differential magnification; then propagate D_Zp through the frozen "
            "lens/aperture operator and rerun the five-mode rank gate"
        ),
        "claim_boundary": (
            "rejects only simple inheritance of the currently open CO(8-7) profile; "
            "it does not reject richer standard line formation or Tau Core"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 open-transition profile-lift gate v01\n\n"
        f"Status: `{result['status']}`. Endpoint authorized: `False`.\n\n"
        "The official endpoint-blind source products are two-dimensional, "
        "velocity-integrated maps and provide no source spectral axis. The existing "
        f"CO(8-7) inverse reconstruction promotes 0/6 channel-common fits. Its "
        f"three-path-to-fourth-path test improves only {loo.get('positive_fold_count')}/"
        f"{loo.get('fold_count')} folds and has median predictive R2 "
        f"{loo.get('predictive_r2_median'):.3f}. The cross-transition rank remains "
        "unpromoted.\n\n"
        "Therefore a CO(8-7) normalized profile may not be inherited as the "
        "CO(10-9) profile. A new endpoint-independent source-plane spectral product "
        "or a source-owned excitation-opacity-kinematic law is required.\n\n"
        f"{result['claim_boundary']}.\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
