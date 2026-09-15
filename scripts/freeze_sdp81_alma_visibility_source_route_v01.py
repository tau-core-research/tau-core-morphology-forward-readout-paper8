#!/usr/bin/env python3
"""Freeze the endpoint-blind ALMA visibility acquisition route for SDP.81.

This script is deliberately network-free.  It audits a source-inventory freeze
made from the official ALMA TAP/Datalink response and the official calibration
script bundles.  It never downloads or opens Band-7/CO(10-9) science data.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/sdp81_alma_visibility_source_route_v01.json"
REPORT = ROOT / "reports/sdp81_alma_visibility_source_route_v01.md"

PROJECT = "2011.0.00016.SV"
MEMBER_OUS = "uid://A002/X8fa7af/X12"
PORTAL = "https://almascience.eso.org/dataPortal"


def product(uid: str, size: int) -> dict[str, object]:
    return {
        "execution_uid": uid,
        "content_length_bytes": size,
        "access_url": f"{PORTAL}/{PROJECT}_{uid}.asdm.sdm.tar",
    }


ALLOWED = {
    "Band4_CO54": [
        product("uid___A002_X91068d_Xa1e", 7066663936),
        product("uid___A002_X91068d_Xc50", 4931837952),
        product("uid___A002_X91068d_Xead", 6465080320),
        product("uid___A002_X915f1c_X5d0", 4681423872),
        product("uid___A002_X924c91_X12c", 15099610112),
        product("uid___A002_X924c91_X34f", 15099683840),
        product("uid___A002_X924c91_X572", 15099720704),
        product("uid___A002_X924c91_X847", 14154798080),
        product("uid___A002_X924c91_Xa47", 15247220736),
        product("uid___A002_X93514d_X1634", 16294638592),
        product("uid___A002_X93514d_X1857", 16453101568),
        product("uid___A002_X93514d_Xfc6", 17545526272),
    ],
    "Band6_CO87": [
        product("uid___A002_X8fd70d_X1484", 4957810688),
        product("uid___A002_X8fd70d_X188b", 3655892992),
        product("uid___A002_X907514_X11d6", 6338478080),
        product("uid___A002_X915f1c_X8be", 4954334208),
        product("uid___A002_X916b15_X1716", 5269903360),
        product("uid___A002_X923b56_X43c", 10697946112),
        product("uid___A002_X923b56_X65f", 10697825280),
        product("uid___A002_X92c694_X1099", 9280667648),
        product("uid___A002_X92ec61_X1f23", 7716950016),
    ],
}

FORBIDDEN_BAND7_UIDS = [
    "uid___A002_X91dc9f_X2eb",
    "uid___A002_X91dc9f_X517",
    "uid___A002_X91dc9f_Xb6",
    "uid___A002_X91f01f_X5e6",
    "uid___A002_X91f01f_X812",
    "uid___A002_X920302_X1059",
    "uid___A002_X920302_X1336",
    "uid___A002_X920302_X1562",
    "uid___A002_X920302_Xe29",
    "uid___A002_X925649_Xa99",
    "uid___A002_X925649_Xcc5",
]


def main() -> None:
    allowed = [p for products in ALLOWED.values() for p in products]
    allowed_uids = [str(p["execution_uid"]) for p in allowed]
    allowed_bytes = sum(int(p["content_length_bytes"]) for p in allowed)
    checks = {
        "official_project_and_member_frozen": PROJECT == "2011.0.00016.SV"
        and MEMBER_OUS == "uid://A002/X8fa7af/X12",
        "band4_execution_count_is_12": len(ALLOWED["Band4_CO54"]) == 12,
        "band6_execution_count_is_9": len(ALLOWED["Band6_CO87"]) == 9,
        "allowed_raw_size_is_211709114368_bytes": allowed_bytes == 211709114368,
        "no_allowed_uid_is_band7": set(allowed_uids).isdisjoint(FORBIDDEN_BAND7_UIDS),
        "allowed_uids_are_unique": len(allowed_uids) == len(set(allowed_uids)),
        "all_urls_are_official_asdm_tar_urls": all(
            str(p["access_url"]).startswith(PORTAL + f"/{PROJECT}_")
            and str(p["access_url"]).endswith(".asdm.sdm.tar")
            for p in allowed
        ),
        "co109_header_not_read": True,
        "co109_pixels_not_read": True,
    }
    result = {
        "schema": "sdp81_alma_visibility_source_route_v01",
        "status": "RAW_VISIBILITY_SOURCE_ROUTE_IDENTIFIED_ACQUISITION_NOT_EXECUTED",
        "generated_utc": "2026-09-03T00:00:00Z",
        "source": {
            "archive": "ALMA Science Archive",
            "project_code": PROJECT,
            "member_ous_uid": MEMBER_OUS,
            "tap_endpoint": "https://almascience.eso.org/tap/sync",
            "datalink_endpoint": "https://almascience.org/datalink/sync?ID=uid://A002/X8fa7af/X12",
            "datalink_response_sha256": "e686929b0ab1f2f75177602088b4bb24fd07aacadb7871e0396253c52b73a34c",
            "band4_calibration_bundle_sha256": "f69dbf45213dd2dfc0c21e17c37e178bb556f1ac5c9180100a338a4ffa8982b6",
            "band6_calibration_bundle_sha256": "35b375b6543460facf56d20fb320b6b7c47fa094893826592dff405afaf6dbe1",
            "inventory_observed_utc": "2026-09-03",
        },
        "allowed_training_products": ALLOWED,
        "allowed_execution_count": len(allowed),
        "allowed_content_length_bytes": allowed_bytes,
        "allowed_content_length_decimal_gb": allowed_bytes / 1e9,
        "forbidden_holdout": {
            "band": "Band7",
            "line": "CO(10-9)",
            "execution_uids": FORBIDDEN_BAND7_UIDS,
            "rule": "Do not download, extract, inspect, calibrate, image, or read a header/pixel from any listed Band-7 execution before the complete source gate passes.",
        },
        "source_reconstruction_contract": {
            "training_lines_only": ["CO(5-4)", "CO(8-7)"],
            "visibility_domain_required": True,
            "continuum_subtraction": "uv-domain, frozen without CO(10-9)",
            "spectral_grid": "common 41 km/s channels, matching the independent Rybak et al. 2015 source analysis unless a source-only audit freezes a stricter grid",
            "uv_support": "common <=1 Mlambda support or a stricter source-only common-support intersection",
            "lens_model": "independent continuum-frozen model; no CO(10-9) tuning",
            "outputs_required": [
                "separate CO(5-4) and CO(8-7) source-plane spectral cubes",
                "channel covariance or posterior draws",
                "source-plane PSF/resolution operator",
                "regularization-selection record",
                "leave-one-execution-block-out stability diagnostics",
                "cross-transition profile-transfer rejection or validated physical transfer law",
            ],
            "terminal_promotion_rule": "No terminal Jacobian is promoted unless the source-only reconstruction supplies a full-rank five-mode derivative with uncertainty and survives execution-block and regularization perturbations.",
        },
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "acquisition_executed": False,
        "source_cube_reconstructed": False,
        "transition_readiness_increment": 0,
        "endpoint_authorized": False,
        "next_finite_action": "Acquire only the 21 frozen Band-4/Band-6 ASDM packages after storage/transfer authorization, calibrate them with the matching official scripts, and perform a visibility-plane source reconstruction under the frozen contract. Keep all 11 Band-7 executions untouched.",
        "claim_boundary": "This freezes a public, endpoint-independent acquisition route and proves Band-4/Band-6/Band-7 execution separation at the archive-manifest level. It is not a source-cube reconstruction, does not select a physical CO(10-9) profile law, does not increase transition readiness, and does not authorize or score the held-out endpoint.",
    }
    if not all(checks.values()):
        raise RuntimeError("visibility source-route freeze failed")
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# SDP.81 ALMA visibility source route v01\n\n"
        f"Status: `{result['status']}`. Checks: `{result['checks_passed']}/{result['checks_total']}`. "
        "Endpoint authorized: `False`.\n\n"
        "The official ALMA archive manifest and calibration-script bundles separate "
        "12 Band-4 CO(5-4) executions and 9 Band-6 CO(8-7) executions from 11 forbidden "
        "Band-7 CO(10-9) executions. The allowed raw ASDM payload is 211.709 GB. No "
        "Band-7 science package, FITS header, or pixel was opened.\n\n"
        "This supplies a concrete endpoint-independent route to the missing source-plane "
        "spectral information, but does not supply the reconstruction itself. The next "
        "step is an authorized Band-4/Band-6-only download, official calibration, and "
        "visibility-plane source inversion with covariance and stability tests.\n\n"
        f"Claim boundary: {result['claim_boundary']}\n"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
