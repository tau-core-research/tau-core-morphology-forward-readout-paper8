#!/usr/bin/env python3
"""Record the source-native NGC5204 tilted-ring warp body from Jozsa et al. 2007."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "ugc08490_ngc5204_warp_body_v01.md"


ROWS = [
    (0, 0.00, 56.1, 23.7, 257.4, 26.2, 0.0, 0.0, 349.0, 180.0),
    (12, 0.24, 56.1, 14.1, 257.4, 38.7, 0.0, 0.0, 349.0, 180.0),
    (24, 0.48, 56.1, 4.0, 257.4, 11.0, 0.0, 0.0, 349.0, 180.0),
    (36, 0.72, 56.1, 7.4, 257.4, 6.2, 0.0, 0.0, 349.0, 180.0),
    (48, 0.96, 56.1, 9.5, 257.4, 4.0, 0.0, 0.0, 349.0, 180.0),
    (60, 1.20, 56.1, 11.7, 257.4, 7.2, 0.0, 0.0, 349.0, 180.0),
    (72, 1.45, 56.1, 6.2, 257.4, 4.3, 0.0, 0.0, 349.0, 180.0),
    (84, 1.69, 56.1, 4.0, 257.4, 4.0, 0.0, 0.0, 349.0, 180.0),
    (96, 1.93, 56.1, 4.0, 257.4, 4.0, 0.0, 0.0, 349.0, 180.0),
    (108, 2.17, 56.1, 4.0, 257.4, 4.0, 0.0, 0.0, 349.0, 180.0),
    (120, 2.41, 56.1, 4.0, 257.4, 4.0, 0.0, 0.0, 349.0, 180.0),
    (132, 2.65, 56.1, 4.0, 257.4, 4.0, 0.0, 0.0, 349.0, 180.0),
    (144, 2.89, 56.1, 4.0, 257.4, 4.0, 0.0, 0.0, 349.0, 180.0),
    (156, 3.13, 50.4, 4.0, 258.8, 4.0, 5.8, 4.0, 349.8, 31.1),
    (168, 3.37, 48.0, 4.0, 261.4, 4.0, 8.6, 3.9, 339.9, 21.1),
    (180, 3.61, 42.7, 4.0, 264.0, 4.0, 14.3, 3.9, 341.5, 12.0),
    (210, 4.22, 28.9, 4.0, 286.3, 6.1, 32.9, 3.5, 334.6, 6.6),
    (240, 4.82, 30.1, 4.0, 310.6, 18.9, 42.9, 9.3, 323.9, 6.5),
    (270, 5.42, 34.8, 4.0, 309.7, 4.0, 41.6, 2.4, 317.1, 6.0),
    (300, 6.02, 37.6, 4.0, 317.5, 4.0, 46.0, 2.5, 312.7, 5.6),
    (330, 6.63, 39.3, 4.0, 316.1, 4.0, 45.2, 2.6, 310.3, 5.7),
    (360, 7.23, 42.4, 4.0, 318.5, 4.0, 46.9, 2.8, 306.1, 5.5),
    (390, 7.83, 39.0, 4.0, 319.4, 4.0, 47.2, 2.6, 310.9, 5.5),
    (420, 8.43, 34.1, 25.0, 322.2, 25.0, 48.6, 14.1, 317.5, 33.4),
]


def main() -> None:
    columns = ["radius_arcsec", "radius_kpc_source", "inclination_deg", "inclination_error_deg",
               "pa_deg", "pa_error_deg", "tip_deg", "tip_error_deg", "lon_deg", "lon_error_deg"]
    frame = pd.DataFrame(ROWS, columns=columns)
    frame["inner_flat_source_zone"] = frame.radius_arcsec <= 144
    frame["warp_transition_or_outer_zone"] = frame.radius_arcsec >= 156
    frame.to_csv(DATA / "ugc08490_ngc5204_warp_body_profile_v01.csv", index=False)
    onset = frame[frame.tip_deg.gt(0)].iloc[0]
    result = {
        "schema": "tau_core_ugc08490_ngc5204_warp_body_v01",
        "status": "SOURCE_NATIVE_TWO_PLANE_WARP_BODY_PROMOTED_OUTER_MODE_ONLY",
        "source": "Jozsa et al. 2007 A&A 468 903-917, Table 6",
        "source_pdf_sha256": "15b4ae9e2bb3268509e75b40e62def8cc4664a117fdcccafae8afb7f170ec8ba",
        "n_tilted_rings": len(frame),
        "inner_reference_orientation": {"inclination_deg": 56.1, "pa_deg": 257.4},
        "warp_onset": {"radius_arcsec": float(onset.radius_arcsec), "radius_kpc_source": float(onset.radius_kpc_source),
                       "tip_deg": float(onset.tip_deg), "tip_error_deg": float(onset.tip_error_deg)},
        "inner_outer_mean_mutual_inclination_deg": 41.1,
        "inner_outer_mean_mutual_inclination_error_deg": 5.7,
        "source_inner_disk_range_arcsec": [30.0, 180.0],
        "source_outer_disk_range_arcsec": [240.0, 420.0],
        "source_rotation_rise_inner_km_s": 67.9,
        "source_rotation_rise_delta_km_s": 14.6,
        "source_rotation_rise_fraction": 0.22,
        "ghasp_oriented_preflight_max_radius_kpc": 2.37,
        "ghasp_preflight_overlaps_warp_onset": False,
        "body_reclassification": "inner irregular/ringed disk plus outer two-plane grand-design warp",
        "same_tracer_inner_context": {
            "source": "Garrido et al. 2002 GHASP Halpha survey I",
            "central_ring_radius_arcsec_approx": 30.0,
            "central_ring_radius_kpc_approx": 0.68,
            "morphology": "mottled appearance; spiral structure hard to see",
            "source_rotation_assessment": "fairly symmetric",
            "redshifted_high_point_caveat": "not significant; comes from a single isolated HII region",
            "independent_body_coordinate": False
        },
        "outer_warp_can_explain_current_inner_side_incompatibility": False,
        "endpoint_values_used_for_body_construction": False,
        "claim_boundary": "source-native outer warp body; it begins beyond the current GHASP common-radius preflight and cannot be assigned as its cause"
    }
    (DATA / "ugc08490_ngc5204_warp_body_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# UGC08490 / NGC5204 source-native warp body v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "The 3D TiRiFiC tilted-ring source fixes an inner plane at `i=56.1 deg`, `PA=257.4 deg` through 144 arcsec. "
        "The first nonzero source tip is `5.8 +/- 4.0 deg` at `156 arcsec = 3.13 kpc`; the outer plane reaches about 43-49 deg tip. "
        "The source reports inner/outer mutual inclination `41.1 +/- 5.7 deg` and a `14.6 km/s` (22%) rotation rise across the transition.\n\n"
        "The current GHASP oriented-law preflight ends at `2.37 kpc`, inside the flat inner plane. The outer warp is therefore source-supported "
        "but cannot explain that inner side incompatibility. The same-tracer Halpha source describes a mottled disk and an approximate `30 arcsec` "
        "central ring, calls the curve fairly symmetric, and flags high redshifted points from one isolated HII region as insignificant. This is nuisance "
        "context, not an independent body kernel. No q or endpoint residual enters the outer-warp construction.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
