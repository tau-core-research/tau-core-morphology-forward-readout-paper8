#!/usr/bin/env python3
"""Build an NGC7331 H I warp acquisition route for exact B2 transfer.

This route identifies residual-blind source products that can eventually fill
q_warp, sigma_warp, and epsilon_cross for the NGC7331 exact-transfer packet.
It records candidate sources and extraction routes only. It does not download
or digitize maps, and it does not score rotation curves.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_b2_hi_warp_acquisition_route_not_endpoint"

BOSMA_NED_URL = "https://ned.ipac.caltech.edu/level5/March05/Bosma/Bosma4_7.html"
THINGS_ARXIV_URL = "https://arxiv.org/abs/0810.2125"
RADIAL_GAS_MOTION_URL = "https://academic.oup.com/mnras/article/457/3/2642/2588886"
PATRA_ARXIV_URL = "https://arxiv.org/abs/1706.08615"


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.6g}")
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    evidence_summary = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_source_evidence_summary.csv"
    ).iloc[0]
    product_audit_path = DATA / "ngc7331_things_hi_product_audit_summary.csv"
    product_audit = (
        pd.read_csv(product_audit_path).iloc[0] if product_audit_path.exists() else None
    )
    things_cached = (
        product_audit is not None
        and bool(product_audit["worksheet_ready"])
        and str(product_audit["things_hi_product_audit_status"])
        == "NGC7331_THINGS_HI_PRODUCTS_AUDITED_WORKSHEET_READY"
    )

    source_candidates = pd.DataFrame(
        [
            {
                "source_id": "N7331_HI_SRC1_BOSMA_NED_21CM",
                "source_rank": 1,
                "source_type": "literature_figures_and_tilted_ring_context",
                "source_url": BOSMA_NED_URL,
                "source_status": "PRIMARY_CONTEXT_SOURCE_FIGURE_DIGITIZATION_CANDIDATE",
                "supports_fields": "q_warp;sigma_warp;epsilon_cross_inputs",
                "source_evidence": (
                    "NGC7331 H I distribution is warped; channel maps show outer "
                    "parts deviating from the main plane; tilted-ring model has "
                    "radial PA/inclination curves; warp starts near 0.5 Holmberg radius"
                ),
                "line_refs": "Bosma/NED lines 31-36, 67-84",
                "download_or_cache_status": "WEB_SOURCE_AVAILABLE_NO_LOCAL_FIGURE_DIGITIZATION_CACHE",
            },
            {
                "source_id": "N7331_HI_SRC2_THINGS_DATA_PRODUCTS",
                "source_rank": 2,
                "source_type": "public_hi_data_product_route",
                "source_url": THINGS_ARXIV_URL,
                "source_status": (
                    "PUBLIC_DATA_ROUTE_CACHED_AND_AUDITED_WORKSHEET_READY"
                    if things_cached
                    else "PUBLIC_DATA_ROUTE_IDENTIFIED_SOURCE_NATIVE_DOWNLOAD_PENDING"
                ),
                "supports_fields": "q_warp;epsilon_cross_inputs",
                "source_evidence": (
                    "THINGS provides high-resolution H I data products, including "
                    "integrated maps, velocity fields, dispersion maps, and channel maps"
                ),
                "line_refs": "THINGS arXiv abstract lines 38-41",
                "download_or_cache_status": (
                    "LOCAL_THINGS_MOMENT_MAP_CACHE_AUDITED"
                    if things_cached
                    else "DATA_PRODUCTS_PUBLIC_BUT_NGC7331_FITS_NOT_CACHED_HERE"
                ),
            },
            {
                "source_id": "N7331_HI_SRC3_THINGS_RADIAL_GAS_MOTION_TABLE",
                "source_rank": 3,
                "source_type": "derived_things_kinematic_context",
                "source_url": RADIAL_GAS_MOTION_URL,
                "source_status": "SECONDARY_CONTEXT_SOURCE_NOT_WARP_AMPLITUDE",
                "supports_fields": "epsilon_cross_inputs",
                "source_evidence": (
                    "NGC7331 appears in a THINGS radial gas-motion analysis with "
                    "H I mass, SFR, and radial-flow context; data products include "
                    "moment maps and cubes"
                ),
                "line_refs": "MNRAS table lines 147-161 and data-product discussion lines 194-196",
                "download_or_cache_status": "WEB_SOURCE_AVAILABLE_NOT_DIRECT_Q_WARP",
            },
            {
                "source_id": "N7331_HI_SRC4_PATRA_VERTICAL_CONTEXT",
                "source_rank": 4,
                "source_type": "vertical_projection_context",
                "source_url": PATRA_ARXIV_URL,
                "source_status": "SUPPORTING_CONTEXT_SOURCE_ALREADY_CACHED",
                "supports_fields": "sigma_warp;epsilon_cross_inputs",
                "source_evidence": (
                    "Patra records NGC7331 vertical/projection context and possible "
                    "outer-warp emission, useful for sign and cross-term review"
                ),
                "line_refs": "local cached text lines 715-721, 960-971, 1009-1024",
                "download_or_cache_status": "LOCAL_TEXT_CACHE_AVAILABLE",
            },
        ]
    )
    source_candidates["galaxy"] = GALAXY
    source_candidates["endpoint_scores_allowed"] = False
    source_candidates["uses_vobs_or_residual"] = False
    source_candidates["claim_boundary"] = CLAIM_BOUNDARY
    source_candidates = source_candidates[
        [
            "galaxy",
            "source_id",
            "source_rank",
            "source_type",
            "source_url",
            "source_status",
            "supports_fields",
            "source_evidence",
            "line_refs",
            "download_or_cache_status",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    extraction_routes = pd.DataFrame(
        [
            {
                "route_id": "N7331_HI_ROUTE1_THINGS_MOMENT_MAP_EXTRACTION",
                "route_priority": 1,
                "route_goal": "source-native q_warp amplitude and side-asymmetry bound",
                "input_product": "THINGS NGC7331 moment-0 and moment-1 maps or data cube",
                "measurement_rule": (
                    "measure outer H I ridge displacement/asymmetry relative to inner disk "
                    "and normalize by local disk reference extent"
                ),
                "required_outputs": "q_warp;side_asymmetry_bound;orientation_mismatch_bound",
                "current_route_status": (
                    "PREFERRED_ROUTE_SOURCE_PRODUCTS_CACHED_WORKSHEET_READY"
                    if things_cached
                    else "PREFERRED_ROUTE_DATA_DOWNLOAD_PENDING"
                ),
                "endpoint_scores_allowed": False,
            },
            {
                "route_id": "N7331_HI_ROUTE2_BOSMA_FIGURE_DIGITIZATION",
                "route_priority": 2,
                "route_goal": "fallback q_warp and sign/context extraction",
                "input_product": "Bosma/NED channel-map and tilted-ring figures",
                "measurement_rule": (
                    "digitize outer H I contour/ridge offset and radial PA/inclination "
                    "turning from published figures using a predeclared worksheet"
                ),
                "required_outputs": "q_warp_candidate;sigma_warp_context;epsilon_cross_context",
                "current_route_status": "FALLBACK_ROUTE_FIGURE_CACHE_OR_SCREENSHOT_PENDING",
                "endpoint_scores_allowed": False,
            },
            {
                "route_id": "N7331_HI_ROUTE3_TILTED_RING_PROFILE_EXTRACTION",
                "route_priority": 3,
                "route_goal": "orientation/sign rule and cross-term bound",
                "input_product": "radial PA(R), inclination(R), and H I surface density profile",
                "measurement_rule": (
                    "extract direction changes, sign reversals, and outer/inner plane mismatch "
                    "from source-side ring geometry"
                ),
                "required_outputs": "sigma_warp;orientation_mismatch_bound;locality_onset_coupling",
                "current_route_status": "PROFILE_NUMERICS_NOT_EXTRACTED",
                "endpoint_scores_allowed": False,
            },
            {
                "route_id": "N7331_HI_ROUTE4_CONTEXT_ONLY_CROSS_TERM_REVIEW",
                "route_priority": 4,
                "route_goal": "nonzero cross-term obligation review",
                "input_product": "Bosma complex warp context plus Patra vertical/projection context",
                "measurement_rule": "decide whether cross terms may be assumed negligible; current evidence says no",
                "required_outputs": "epsilon_cross_must_be_bounded_or_carried",
                "current_route_status": "CONTEXT_READY_BOUND_NOT_CLOSED",
                "endpoint_scores_allowed": False,
            },
        ]
    )
    extraction_routes["galaxy"] = GALAXY
    extraction_routes["uses_vobs_or_residual"] = False
    extraction_routes["claim_boundary"] = CLAIM_BOUNDARY
    extraction_routes = extraction_routes[
        [
            "galaxy",
            "route_id",
            "route_priority",
            "route_goal",
            "input_product",
            "measurement_rule",
            "required_outputs",
            "current_route_status",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_HIAG1_SOURCE_CANDIDATES_IDENTIFIED",
                "gate_status": "PASS",
                "evidence": "Bosma/NED, THINGS, radial gas-motion, and Patra routes are identified",
                "remaining_obligation": "none at candidate-identification level",
            },
            {
                "gate_id": "N7331_HIAG2_SOURCE_NATIVE_HI_PRODUCT_CACHED",
                "gate_status": "PASS" if things_cached else "BLOCKED_DATA_NOT_CACHED",
                "evidence": (
                    "THINGS NGC7331 moment maps are locally cached and FITS-audited"
                    if things_cached
                    else "THINGS route is identified but NGC7331 FITS/moment products are not cached in this package"
                ),
                "remaining_obligation": (
                    "build residual-blind q_warp/sign/cross-term measurement worksheet"
                    if things_cached
                    else "download/cache source-native H I map/cube or build a Bosma figure digitization worksheet"
                ),
            },
            {
                "gate_id": "N7331_HIAG3_Q_WARP_MEASURABLE",
                "gate_status": "BLOCKED_EXTRACTION_PENDING",
                "evidence": "q_warp requires actual H I ridge/asymmetry measurement",
                "remaining_obligation": "measure q_warp with a residual-blind worksheet",
            },
            {
                "gate_id": "N7331_HIAG4_SIGMA_SIGN_REVIEW",
                "gate_status": "BLOCKED_SIGN_REVIEW_PENDING",
                "evidence": "Bosma complex warp/opposite-direction context prevents inherited sign",
                "remaining_obligation": "freeze added-readout/attenuation convention from source geometry",
            },
            {
                "gate_id": "N7331_HIAG5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "route uses source candidates and geometry requirements only",
                "remaining_obligation": "future scoring must remain separate after formula freeze",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "hi_warp_acquisition_status": (
                    "NGC7331_HI_WARP_ACQUISITION_ROUTE_SOURCE_PRODUCTS_CACHED_WORKSHEET_READY"
                    if things_cached
                    else "NGC7331_HI_WARP_ACQUISITION_ROUTE_BUILT_SOURCE_DATA_NOT_CACHED"
                ),
                "source_evidence_review_status": str(
                    evidence_summary["source_evidence_review_status"]
                ),
                "n_source_candidates": len(source_candidates),
                "n_extraction_routes": len(extraction_routes),
                "n_gates": len(gates),
                "n_pass": int(gates["gate_status"].eq("PASS").sum()),
                "n_blocked": int(gates["gate_status"].str.startswith("BLOCKED").sum()),
                "preferred_next_route": (
                    "THINGS_QWARP_SIGN_CROSS_TERM_WORKSHEET"
                    if things_cached
                    else "THINGS_MOMENT_MAP_OR_DATA_CUBE_DOWNLOAD"
                ),
                "fallback_next_route": "BOSMA_FIGURE_DIGITIZATION_WORKSHEET",
                "q_warp_measurement_ready": False,
                "sigma_warp_sign_ready": False,
                "epsilon_cross_bound_ready": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "population_claim_allowed": False,
                "next_required_action": (
                    "build/fill residual-blind THINGS q_warp, sign, and cross-term worksheet"
                    if things_cached
                    else "cache source-native THINGS NGC7331 H I products or build a "
                    "Bosma figure-digitization worksheet before q_warp measurement"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    source_candidates.to_csv(DATA / "ngc7331_b2_hi_warp_source_candidates.csv", index=False)
    extraction_routes.to_csv(DATA / "ngc7331_b2_hi_warp_extraction_routes.csv", index=False)
    gates.to_csv(DATA / "ngc7331_b2_hi_warp_acquisition_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_b2_hi_warp_acquisition_summary.csv", index=False)

    report = [
        "# NGC7331 B2 H I Warp Acquisition Route",
        "",
        "This route identifies source-native or source-figure paths for filling",
        "the NGC7331 exact-transfer packet. It is not a formula freeze and not",
        "an endpoint score.",
        "",
        "## Source Candidates",
        "",
        markdown_table(source_candidates),
        "",
        "## Extraction Routes",
        "",
        markdown_table(extraction_routes),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        "The preferred next route is source-native THINGS H I map/cube acquisition.",
        "If that remains unavailable, Bosma/NED figure digitization is the fallback.",
        "Either route must produce q_warp, sigma_warp, and epsilon_cross inputs",
        "without reading endpoint residuals.",
        "",
    ]
    (REPORTS / "ngc7331_b2_hi_warp_acquisition_route.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
