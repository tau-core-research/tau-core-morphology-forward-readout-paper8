#!/usr/bin/env python3
"""Build an endpoint-blind HALOGAS candidate-pool audit for the next score."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HALOGAS_DIR = ROOT / "data/external/literature/halogas_dr1_confirmatory_pool_v01"
NGC925_DIR = ROOT / "data/external/literature/ngc0925_signed_geometry_source_v01"
SPARC = ROOT / "data/derived/external_sparc_master_table.csv"
OUT_CSV = ROOT / "data/derived/multigalaxy_halogas_confirmatory_candidate_pool_v01.csv"
OUT_JSON = ROOT / "data/derived/multigalaxy_halogas_confirmatory_candidate_pool_v01.json"
REPORT = ROOT / "reports/multigalaxy_halogas_confirmatory_candidate_pool_v01.md"
NGC925_FREEZE = ROOT / "data/derived/ngc0925_signed_descriptor_source_geometry_freeze_v01.json"
NGC925_PHYSICAL = ROOT / "data/derived/ngc0925_physical_geometry_uncertainty_v02.json"
NGC925_OUTER = ROOT / "data/derived/ngc0925_outer_only_source_support_v01.json"
NGC4062_ENDPOINT = ROOT / "data/derived/ngc4062_halogas_confirmatory_endpoint_v01.json"


# Values transcribed from Heald et al. (2011), Table 1, cached as 15938.tex.
HALOGAS_SAMPLE = [
    ("NGC0672", "UGC01256", 70, "SBcd"),
    ("NGC0891", "UGC01831", 84, "SAb"),
    ("NGC0925", "UGC01913", 54, "SABd"),
    ("NGC0949", "UGC01983", 52, "SAd"),
    ("UGC2082", "UGC02082", 89, "SAc"),
    ("NGC1003", "UGC02137", 67, "SAcd"),
    ("NGC2403", "UGC03918", 62, "SAcd"),
    ("UGC4278", "UGC04278", 90, "SAd"),
    ("NGC2541", "UGC04284", 67, "SAcd"),
    ("NGC3198", "UGC05572", 71, "SBc"),
    ("NGC4062", "UGC07045", 68, "SAc"),
    ("NGC4244", "UGC07322", 90, "SAcd"),
    ("NGC4258", "UGC07353", 71, "SABbc"),
    ("NGC4274", "UGC07377", 72, "SBab"),
    ("NGC4414", "UGC07539", 50, "SAc"),
    ("NGC4448", "UGC07591", 71, "SBab"),
    ("NGC4559", "UGC07766", 69, "SABcd"),
    ("NGC4565", "UGC07772", 90, "SAb"),
    ("UGC7774", "UGC07774", 90, "SAd"),
    ("NGC4631", "UGC07865", 85, "SBd"),
    ("NGC5023", "UGC08286", 90, "SAc"),
    ("NGC5055", "UGC08334", 55, "SAbc"),
    ("NGC5229", "UGC08550", 90, "SBc"),
    ("NGC5585", "UGC09179", 51, "SABd"),
]

EXPLICIT_DEVELOPMENT = {
    "NGC2541": "NGC2541 side-consistency statistic and nuisance development",
    "NGC3198": "prior Paper 8 diagnostic scan and predeclared replay score",
    "NGC4559": "prior HALOGAS/Halpha replication endpoint",
    "NGC4062": "frozen two-resolution HALOGAS/Halpha confirmatory endpoint opened",
}

SOURCE_STATUS = {
    "NGC0672": "INTERACTING_COMPANION_CONTAMINATION",
    "NGC0925": "PHYSICAL_MC_ACQUIRED_INNER_NONIDENTIFIABLE_OUTER_TERMINAL_CONTAMINATED",
    "NGC0949": "HALOGAS_WARP_GT10_DEG_CONSTANT_GEOMETRY_ONLY",
    "NGC4062": "SOURCE_GEOMETRY_COMPLETE_TWO_RING_ENDPOINT_OPENED_NULL_AND_ZEROPOINT_UNSTABLE",
    "NGC4258": "HALOGAS_WARP_STREAMING_ACTIVE_NUCLEUS_COMPLEX",
    "NGC4274": "HALOGAS_FEW_RESOLUTION_ELEMENTS_BEAM_SMEARING_LIMITED",
    "NGC4414": "HALOGAS_PA_WARP_WHOLE_CUBE_POOR_FIT",
    "NGC4448": "HALOGAS_FEW_RESOLUTION_ELEMENTS_BEAM_SMEARING_LIMITED",
}

PRIORITY = {"NGC4062": 1, "NGC4414": 2, "NGC0949": 3}

EXPECTED_HASHES = {
    HALOGAS_DIR / "heald2011_15938.tex": "6985ce18fd7978f16a921a3b7df6444ab0fc66c02dacb359a780d0d221d53017",
    HALOGAS_DIR / "heald2011_arxiv_1012.0816_source.tar.gz": "dcf89d58c6c1326a36a6b64d9dde14270d54b1a8ea108396cce2f48ab4485f52",
    HALOGAS_DIR / "zenodo_2552349_record.json": "8a81bdd20d2322a839e89b288e81cb60dbeeacfc071c16453220ac3694b67f8b",
    NGC925_DIR / "deblok2008_arxiv_0810.2100v2_source.tar.gz": "5f9d482231d6528a6c120c66fcd717551a633c5e974adbcf3716fb80d2a55427",
    NGC925_DIR / "deblok2008_deblok_astroph.tex": "6c76c8d95dc671727370a44d7e040fa17e752971f2ad8c8b053438b998caa199",
    NGC925_DIR / "deblok2008_figuur68_ngc925.ps": "ed3b8e197e523531b5b9e77c9a58f8f7a5e275c4cc3f30ff773977e64fa0b2a0",
}


def canonical(value: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", value.upper())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for path, expected in EXPECTED_HASHES.items():
        assert path.exists(), path
        assert sha256(path) == expected, path

    heald_text = (HALOGAS_DIR / "heald2011_15938.tex").read_text()
    deblok_text = (NGC925_DIR / "deblok2008_deblok_astroph.tex").read_text()
    assert "The Full HALOGAS Sample" in heald_text
    assert "NGC 925  & 02 27 16.5 & +33 34 43.5" in deblok_text
    assert "9.2 & 3.0 & 546.3 & 66.0 & 286.6" in deblok_text
    assert "global trend from $i \\sim 75^{\\circ}$" in deblok_text
    assert "approaching\nand receding sides are fairly symmetric" in deblok_text

    ngc925_freeze = json.loads(NGC925_FREEZE.read_text())
    assert ngc925_freeze["status"] == "SOURCE_GEOMETRY_DIGITIZATION_COMPLETE_ENDPOINT_BLOCKED_PHYSICAL_UNCERTAINTY"
    assert ngc925_freeze["endpoint_pixels_read"] is False
    assert ngc925_freeze["endpoint_allowed"] is False
    ngc925_physical = json.loads(NGC925_PHYSICAL.read_text())
    ngc925_outer = json.loads(NGC925_OUTER.read_text())
    ngc4062_endpoint = json.loads(NGC4062_ENDPOINT.read_text())
    assert ngc925_physical["status"] == "PHYSICAL_MC_ACQUIRED_GEOMETRY_IDENTIFIABILITY_FAIL_ENDPOINT_BLOCKED"
    assert ngc925_outer["status"] == "OUTER_GEOMETRIC_CAPACITY_PASS_TERMINAL_CLEANLINESS_FAIL_ENDPOINT_BLOCKED"
    assert ngc925_physical["endpoint_pixels_read"] is False
    assert ngc925_outer["endpoint_pixels_read"] is False
    assert ngc4062_endpoint["status"] == "NGC4062_CONFIRMATORY_ENDPOINT_FAIL"
    assert ngc4062_endpoint["confirmatory_pass"] is False

    with SPARC.open(newline="") as handle:
        sparc_names = {canonical(row["Galaxy"]) for row in csv.DictReader(handle)}

    zenodo = json.loads((HALOGAS_DIR / "zenodo_2552349_record.json").read_text())
    keys = {item["key"] for item in zenodo["files"]}

    rows = []
    for galaxy, ugc, inclination, hubble_type in HALOGAS_SAMPLE:
        endpoint_products = sorted(
            key for key in keys if key.upper().startswith(galaxy.upper() + "-") and "MOM" in key.upper()
        )
        sparc_exposed = canonical(galaxy) in sparc_names or canonical(ugc) in sparc_names
        development_reason = EXPLICIT_DEVELOPMENT.get(galaxy, "")
        prior_endpoint_exposed = bool(sparc_exposed or development_reason)
        moderate = 50 <= inclination <= 75
        source_status = SOURCE_STATUS.get(galaxy, "SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED")
        endpoint_unopened_candidate = moderate and not prior_endpoint_exposed and bool(endpoint_products)
        clean_source_candidate = endpoint_unopened_candidate and source_status == "SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED"

        if prior_endpoint_exposed:
            status = "EXCLUDED_PRIOR_ENDPOINT_EXPOSURE"
        elif not moderate:
            status = "EXCLUDED_EDGE_ON_FOR_CURRENT_SIDE_GEOMETRY_PROTOCOL"
        elif not endpoint_products:
            status = "BLOCKED_NO_DR1_MOMENT_ENDPOINT_PRODUCT"
        elif source_status != "SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED":
            status = "SOURCE_DEMOTED_FROM_CLEAN_CONFIRMATORY_LANE"
        else:
            status = "P2_SOURCE_ACQUISITION_REQUIRED_ENDPOINT_UNOPENED"

        rows.append(
            {
                "galaxy": galaxy,
                "ugc_id": ugc,
                "hubble_type": hubble_type,
                "heald_inclination_deg": inclination,
                "moderate_inclination_50_to_75": moderate,
                "halogas_moment_products_in_zenodo": len(endpoint_products),
                "sparc_rotation_population_exposed": sparc_exposed,
                "explicit_development_exposure": development_reason,
                "prior_endpoint_exposed": prior_endpoint_exposed,
                "signed_radial_geometry_source_status": source_status,
                "endpoint_unopened_candidate": endpoint_unopened_candidate,
                "clean_source_candidate": clean_source_candidate,
                "source_acquisition_priority": PRIORITY.get(galaxy, ""),
                "candidate_status": status,
                "endpoint_pixels_read_by_this_audit": False,
            }
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    candidates = [row for row in rows if row["endpoint_unopened_candidate"]]
    clean_candidates = [row for row in rows if row["clean_source_candidate"]]
    summary = {
        "status": "SOURCE_ACQUISITION_ONLY_HALOGAS_ALONE_INSUFFICIENT_FOR_CONFIRMATORY_N12",
        "n_halogas_galaxies": len(rows),
        "n_prior_endpoint_exposed": sum(row["prior_endpoint_exposed"] for row in rows),
        "n_current_protocol_edge_on_excluded": sum(
            row["candidate_status"] == "EXCLUDED_EDGE_ON_FOR_CURRENT_SIDE_GEOMETRY_PROTOCOL" for row in rows
        ),
        "n_endpoint_unopened_moderate_candidates": len(candidates),
        "confirmatory_minimum_galaxies": 12,
        "n_clean_source_candidates": len(clean_candidates),
        "halogas_clean_shortfall": 12 - len(clean_candidates),
        "priority_order": [row["galaxy"] for row in sorted(clean_candidates, key=lambda r: (r["source_acquisition_priority"] == "", r["source_acquisition_priority"] or 999, r["galaxy"]))],
        "next_clean_source_acquisition_target": None,
        "ngc4062_endpoint": {
            "status": ngc4062_endpoint["status"],
            "confirmatory_pass": ngc4062_endpoint["confirmatory_pass"],
            "hr_gls_mean_km_s": ngc4062_endpoint["outputs"]["HR"]["primary_score"]["gls_mean_km_s"],
            "hr_gls_sigma_km_s": ngc4062_endpoint["outputs"]["HR"]["primary_score"]["gls_mean_sigma_km_s"],
            "lr_gls_mean_km_s": ngc4062_endpoint["outputs"]["LR"]["primary_score"]["gls_mean_km_s"],
            "lr_gls_sigma_km_s": ngc4062_endpoint["outputs"]["LR"]["primary_score"]["gls_mean_sigma_km_s"],
            "velocity_zero_point_sign_stable": ngc4062_endpoint["gates"]["all_twelve_nuisance_scores_preserve_sign"],
        },
        "ngc0925_source_constants": {
            "centre_ra_j2000": "02 27 16.5",
            "centre_dec_j2000": "+33 34 43.5",
            "distance_mpc": 9.2,
            "ring_spacing_arcsec": 3.0,
            "systemic_velocity_km_s": 546.3,
            "mean_inclination_deg": 66.0,
            "mean_position_angle_deg": 286.6,
            "published_radial_geometry_statement": "inclination trends from about 75 deg inner to about 60 deg outer; PA is continuous and well-defined",
            "digitized_geometry_status": ngc925_freeze["status"],
            "digitized_ring_count": ngc925_freeze["digitization"]["sampled_ring_count"],
            "digitized_mean_pa_deg": ngc925_freeze["digitization"]["digitized_mean_pa_deg"],
            "physical_uncertainty_status": ngc925_physical["status"],
            "outer_only_status": ngc925_outer["status"],
            "disposition": ngc925_outer["disposition"],
            "remaining_freeze": "retain only as a preregistered disturbed-system robustness/stronger-terminal case; source-specific centre weights, joint covariance, signed PA ray, masked beam support, solver tolerance, and wrong-family controls remain open",
        },
        "endpoint_pixels_read_by_this_audit": False,
        "claim_boundary": "Pool bookkeeping incorporates the separately frozen NGC4062 endpoint result but does not create a new score. No Tau q_R, parent morphology, Nature occupation, or dark-matter-replacement result is produced.",
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n")

    table_rows = "\n".join(
        f"| {row['galaxy']} | {row['heald_inclination_deg']} | {row['prior_endpoint_exposed']} | {row['signed_radial_geometry_source_status']} | {row['candidate_status']} |"
        for row in rows
    )
    REPORT.write_text(
        "# HALOGAS confirmatory candidate-pool audit v01\n\n"
        f"Status: `{summary['status']}`.\n\n"
        "This audit reads the cached Heald et al. (2011) sample table, the HALOGAS DR1 Zenodo file manifest, "
        "the Paper 8 SPARC membership table, and the cached de Blok et al. (2008) source text for NGC925. "
        "It does not open a HALOGAS FITS image or calculate a new endpoint statistic; it imports the separately frozen NGC4062 result.\n\n"
        f"The 24-object HALOGAS sample leaves `{len(candidates)}` moderate-inclination, endpoint-unopened "
        f"objects after prior Paper 8 rotation/development exposure is removed, but source audit leaves "
        f"`{len(clean_candidates)}` clean candidates. The frozen confirmatory minimum is 12.\n\n"
        "NGC3198 is excluded because its diagnostic and replay scores were already opened. NGC5055 is excluded "
        "because it was in the Paper 8 SPARC training population. The first source-acquisition target is NGC925: "
        "the primary THINGS paper provides the centre, 3-arcsec sampling, mean inclination and PA, and an adopted "
        "radial geometry curve in Figure 68. Both adopted orientation curves are now reproducibly digitized into "
        "93 rings. An independent residual-rescrambling Monte Carlo supplies 15 marginal orientation-error pairs, "
        "but its source declares the inner 250 arcsec non-identifiable. Six outer rings have adequate ideal beam "
        "capacity, yet the same outer disk is a documented minor-merger stream with warp/spiral ambiguity and "
        "anomalous gas. NGC925 is therefore demoted from a clean primary endpoint and retained only as a disturbed-"
        "system robustness/stronger-terminal case. NGC4062 was then frozen and opened as the only remaining clean "
        "HALOGAS case: HR and LR are both consistent with zero, while the sign is unstable between the two published "
        "systemic-velocity choices. Every remaining moderate-inclination unopened HALOGAS system is source-flagged "
        "as interacting, substantially warped, kinematically complex, or too poorly resolved for the clean lane. "
        "HALOGAS therefore has no further clean candidate under this protocol. These standard-physics limitations "
        "and the NGC4062 null result are not Tau evidence.\n\n"
        "| galaxy | i (deg) | prior endpoint exposure | source geometry/status | status |\n"
        "| --- | ---: | --- | --- | --- |\n"
        + table_rows
        + "\n\nNo new endpoint score is authorized by this audit. NGC925 endpoint access remains closed for the clean "
        "confirmatory lane; any later disturbed-system route requires a separately frozen stronger terminal or "
        "contamination treatment. A population claim additionally requires at least four eligible galaxies "
        "from an independent survey family or a preregistered change to the sample-size design.\n"
    )
    print("MULTIGALAXY_HALOGAS_CONFIRMATORY_CANDIDATE_POOL_V01_COMPLETE")


if __name__ == "__main__":
    main()
