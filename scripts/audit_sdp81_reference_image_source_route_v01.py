#!/usr/bin/env python3
"""Freeze a resource-bounded SDP.81 source-reconstruction route.

Only the already-open Band-4 CO(5-4) and Band-6 CO(8-7) reference-image cubes
are inspected.  The sealed Band-7 CO(10-9) member is neither opened nor hashed.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
OUT = DATA / "sdp81_reference_image_source_route_v01.json"
REPORT = ROOT / "reports/sdp81_reference_image_source_route_v01.md"

PRODUCTS = [
    {
        "line": "CO(5-4)",
        "path": "data/external/literature/sdp81_multipath_channel/SDP81_Band4_ReferenceImages_z3.042/SDP.81.Band4.CO_smooth_z3.042.fits",
        "bytes": 215072640,
        "sha256": "b26f3e4cbff43bab9d6c4c082ff513788f9dcf20b2e640edf607dbc3fe34a656",
        "shape": [1, 119, 672, 672],
    },
    {
        "line": "CO(8-7)",
        "path": "data/external/literature/sdp81_multipath_channel/SDP81_Band6_ReferenceImages/SDP81_9exec.co87.R1uvtaper1000klambda.fits",
        "bytes": 180855360,
        "sha256": "aeea985de1e590921a6282cdd9d017f0a888958e7e07b54d4d51435772475ea3",
        "shape": [1, 100, 672, 672],
    },
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    inspected = []
    for frozen in PRODUCTS:
        path = ROOT / str(frozen["path"])
        with fits.open(path, memmap=True) as hdul:
            shape = list(hdul[0].data.shape)
            header = hdul[0].header
            inspected.append(
                {
                    **frozen,
                    "actual_bytes": path.stat().st_size,
                    "actual_sha256": digest(path),
                    "actual_shape": shape,
                    "beam_major_arcsec": float(header["BMAJ"]) * 3600.0,
                    "beam_minor_arcsec": float(header["BMIN"]) * 3600.0,
                    "rest_frequency_hz": float(header["RESTFRQ"]),
                    "spectral_increment_hz": float(header["CDELT3"]),
                }
            )
    previous = json.loads(
        (DATA / "sdp81_source_spectral_cube_v01.json").read_text()
    )
    total = sum(int(p["actual_bytes"]) for p in inspected)
    checks = {
        "both_open_transition_cubes_present": len(inspected) == 2,
        "frozen_hashes_match": all(
            p["actual_sha256"] == p["sha256"] for p in inspected
        ),
        "frozen_sizes_match": all(
            p["actual_bytes"] == p["bytes"] for p in inspected
        ),
        "frozen_shapes_match": all(
            p["actual_shape"] == p["shape"] for p in inspected
        ),
        "resource_bound_is_395928000_bytes": total == 395928000,
        "previous_toy_inverse_not_promoted": previous.get(
            "common_source_spectral_cube_promoted"
        )
        is False,
        "co109_header_not_read": True,
        "co109_pixels_not_read": True,
    }
    result = {
        "schema": "tau-core.paper8.sdp81-reference-image-source-route.v01",
        "status": "LOCAL_REFERENCE_IMAGE_ROUTE_AVAILABLE_DEVELOPMENT_ONLY",
        "scientific_role": "resource-bounded successor to the rejected small-aperture toy inverse",
        "products": inspected,
        "total_bytes": total,
        "total_mib": total / 2**20,
        "successor_reconstruction_contract": {
            "image_support": "full source-connected arc masks for all four q1 paths; no centroid-only circular apertures",
            "forward_operator": "exact frozen lens ray shooting followed by line-specific restored-beam convolution",
            "source_model": "one common nonnegative adaptive or convergence-tested source grid per channel",
            "regularization": "source-gradient/curvature family with lambda selected only from open-line evidence and frozen before any CO(10-9) access",
            "noise": "blank-image correlated covariance or validated stationary approximation, propagated through the inversion",
            "joint_open_line_constraint": "shared kinematic support across CO(5-4) and CO(8-7), with transition-specific amplitudes and opacity/excitation freedom",
            "validation": [
                "leave-one-path-out image prediction",
                "leave-one-channel-block-out prediction",
                "source-grid and regularization stability",
                "beam and astrometric perturbation audit",
                "wrong-lens/path-assignment controls",
            ],
            "promotion_rule": "development source profile only if at least 3/4 held paths improve over independent/background controls and median held-path squared-residual improvement exceeds 5 percent under every declared stability family",
        },
        "limitations": [
            "restored image cubes do not retain the full visibility likelihood",
            "deconvolution and correlated imaging errors can bias source-plane covariance",
            "this route cannot by itself validate the final confirmatory endpoint",
            "two open transitions still do not uniquely determine the CO(10-9) excitation-opacity response",
        ],
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "source_reconstruction_completed": False,
        "transition_readiness_increment": 0,
        "endpoint_authorized": False,
        "next_finite_action": "Run the frozen full-arc regularized inversion on the two local reference cubes. Promote only a development source profile that survives all path/channel/grid/beam controls; retain raw visibilities as the later confirmatory route.",
        "claim_boundary": "This proves that a 395.928-MB local development route exists and diagnoses why the earlier 7x7 small-aperture inverse was not decisive. It does not yet reconstruct a promoted source cube, identify D_Zp, validate visibility-level covariance, authorize CO(10-9), or score Tau Core.",
    }
    if not all(checks.values()):
        raise RuntimeError("reference-image source-route audit failed")
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# SDP.81 resource-bounded reference-image source route v01\n\n"
        f"Status: `{result['status']}`. Checks: `{result['checks_passed']}/{result['checks_total']}`. "
        "Endpoint authorized: `False`.\n\n"
        f"The already local CO(5-4) and CO(8-7) reference cubes total {result['total_mib']:.3f} MiB "
        "(395.928 MB), so the 211.709-GB raw-ASDM route is not required for the next "
        "development iteration. The earlier negative inverse used a 7x7 source basis, "
        "small path-centred apertures and no complete correlated image likelihood; it "
        "does not prove that the reference cubes contain no recoverable common source.\n\n"
        "The successor contract uses full arcs, exact frozen ray shooting, beam "
        "convolution, nonnegative regularized source inversion, blank-image covariance, "
        "joint open-line kinematics and held-path/channel/grid/beam controls. This remains "
        "development-only because restored images cannot reproduce the full visibility "
        "likelihood. CO(10-9) remains sealed.\n\n"
        f"Claim boundary: {result['claim_boundary']}\n"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
