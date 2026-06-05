#!/usr/bin/env python3
"""Audit the original/source-native H I data route for NGC4088 B1.

This is a residual-blind source-acquisition audit.  It tries stable public
source routes for an original or source-coordinate H I product that could
replace the printed-page first-pass warp-onset mapping.  It never reads
observed rotation velocities, residuals, endpoint scores, or fit ranks.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd

try:
    import requests
except ImportError:  # pragma: no cover - requests is available in the package env
    requests = None


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CACHE = ROOT / "data" / "external" / "literature" / "ngc4088_source_native_hi_route"
CLAIM_BOUNDARY = "ngc4088_b1_original_hi_data_acquisition_audit_not_endpoint"


@dataclass(frozen=True)
class SourceCandidate:
    candidate_id: str
    route: str
    url: str
    expected_product: str
    source_role: str


CANDIDATES = [
    SourceCandidate(
        "WHISP_FRAMESET_BY_NAME",
        "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE",
        "https://www.astro.rug.nl/~whisp/Database/OverviewCatalog/ListByName/list_by_name.html",
        "overview catalog frameset, not a source-native data product by itself",
        "catalog_navigation",
    ),
    SourceCandidate(
        "WHISP_LISTING_BY_NAME",
        "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE",
        "https://www.astro.rug.nl/~whisp/Database/OverviewCatalog/ListByName/listing_by_name.html",
        "searchable WHISP overview catalog listing",
        "catalog_listing",
    ),
    SourceCandidate(
        "WHISP_NGC4088_GUESSED_PAGE",
        "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE",
        "https://www.astro.rug.nl/~whisp/Database/OverviewCatalog/ListByName/ngc4088.html",
        "direct NGC4088 overview page if present",
        "guessed_direct_page",
    ),
    SourceCandidate(
        "WHISP_UGC7081_DIRECT_PAGE",
        "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE",
        "https://www.astro.rug.nl/~whisp/Database/OverviewCatalog/ListByName/U7075/u7075p38302.html",
        "WHISP direct UGC 7081 overview page for NGC4088",
        "direct_whisp_overview_page",
    ),
    SourceCandidate(
        "WHISP_UGC7081_GRAPHICAL_OVERVIEW_GIF",
        "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE",
        "https://www.astro.rug.nl/~whisp/Database/OverviewCatalog/ListByName/U7075/u7075plot38302.gif",
        "WHISP graphical overview of H I data for UGC 7081",
        "source_graphical_overview",
    ),
    SourceCandidate(
        "WHISP_UGC7081_OBS_REDUCTION_NOTES",
        "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE",
        "https://www.astro.rug.nl/~whisp/Database/OverviewCatalog/ListByName/U7075/u7075p38302obsred.html",
        "WHISP observation and reduction notes for UGC 7081",
        "source_observation_metadata",
    ),
    SourceCandidate(
        "LOCAL_VERHEIJEN_SANCISI_PAGE_IMAGES",
        "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE",
        "data/external/literature/2001_verheijen_sancisi_pages/",
        "cached paper/page images; not source-coordinate H I data",
        "local_printed_source_context",
    ),
    SourceCandidate(
        "NED_NGC4088_METADATA",
        "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE",
        "https://ned.ipac.caltech.edu/byname?objname=NGC%204088",
        "metadata and literature gateway, not a direct cached H I product",
        "metadata_gateway",
    ),
]


def fetch_url(url: str, timeout: int = 20) -> tuple[str, int | None, str, int, str]:
    if requests is None:
        return "FETCH_SKIPPED_REQUESTS_UNAVAILABLE", None, "", 0, ""
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "paper8-source-audit/1.0"})
    except Exception as exc:  # noqa: BLE001 - provenance ledger should record failures
        return "FETCH_FAILED", None, "", 0, str(exc)

    content_type = response.headers.get("content-type", "")
    text = ""
    if "text" in content_type or "html" in content_type:
        text = response.text
    status = f"HTTP_{response.status_code}"
    return status, response.status_code, content_type, len(response.content), text[:200000]


def fetch_binary(url: str, timeout: int = 20) -> tuple[str, int | None, str, bytes, str]:
    if requests is None:
        return "FETCH_SKIPPED_REQUESTS_UNAVAILABLE", None, "", b"", ""
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "paper8-source-audit/1.0"})
    except Exception as exc:  # noqa: BLE001
        return "FETCH_FAILED", None, "", b"", str(exc)
    return (
        f"HTTP_{response.status_code}",
        response.status_code,
        response.headers.get("content-type", ""),
        response.content,
        "",
    )


def classify_fetch(candidate: SourceCandidate, status: str, http_status: int | None, text: str) -> tuple[str, str, bool]:
    haystack = text.lower()
    found_name = any(token in haystack for token in ["ngc 4088", "ngc4088", "ugc 7083", "ugc7083", "u7083", "u07083"])
    has_fits_hint = any(token in haystack for token in [".fits", ".fit", "fits", "data cube", "cube"])

    if candidate.url.startswith("data/"):
        local_path = ROOT / candidate.url
        if not local_path.exists():
            return "LOCAL_CACHE_MISSING", "local printed-source context directory is missing", False
        products = list(local_path.glob("*4088*")) + list(local_path.glob("*ngc4088*"))
        if products:
            return (
                "LOCAL_PRINTED_CONTEXT_FOUND_NOT_SOURCE_NATIVE",
                f"found {len(products)} cached NGC4088 printed-page/context files",
                False,
            )
        return "LOCAL_CONTEXT_FOUND_NO_NGC4088_MATCH", "directory exists but no direct NGC4088 file matched", False

    if http_status is None:
        return status, "network fetch did not return an HTTP response", False
    if http_status >= 400:
        return status, "HTTP error; no source-native product cached", False
    if candidate.candidate_id == "WHISP_UGC7081_DIRECT_PAGE":
        if "graphical overview of hi data of ugc 7081" in haystack:
            return (
                "WHISP_DIRECT_PAGE_FOUND_GRAPHICAL_PRODUCT_LINKED",
                "direct WHISP page for UGC 7081/NGC4088 found; links to graphical overview and observation notes",
                False,
            )
        return "WHISP_DIRECT_PAGE_REACHED_REVIEW_REQUIRED", "direct WHISP page reached but expected overview link was not parsed", False
    if candidate.candidate_id == "WHISP_UGC7081_GRAPHICAL_OVERVIEW_GIF":
        if http_status == 200:
            return (
                "WHISP_GRAPHICAL_OVERVIEW_CACHED_REVIEW_REQUIRED",
                "WHISP graphical H I overview cached; it is source-provenance image data but not a FITS/source-coordinate product",
                False,
            )
    if candidate.candidate_id == "WHISP_UGC7081_OBS_REDUCTION_NOTES":
        if "synthesized beam full resolution" in haystack and "7081" in haystack:
            return (
                "WHISP_OBSERVATION_METADATA_CACHED",
                "observation/reduction notes cached with beam, channel, central velocity, and noise metadata",
                False,
            )
    if candidate.candidate_id == "WHISP_LISTING_BY_NAME":
        if found_name:
            if has_fits_hint:
                return "CATALOG_MATCH_WITH_FITS_HINT_REVIEW_REQUIRED", "listing contains NGC4088/UGC7083 and FITS-like hints", False
            return "CATALOG_MATCH_METADATA_ONLY", "listing contains NGC4088/UGC7083 but no direct source-native product was cached", False
        return "CATALOG_REACHED_NO_NGC4088_MATCH", "WHISP listing reached but no NGC4088/UGC7083 token found", False
    if "ned.ipac.caltech.edu" in candidate.url:
        return "METADATA_GATEWAY_REACHED_NOT_SOURCE_NATIVE", "NED route is a metadata/literature gateway, not a cached H I product", False
    if has_fits_hint and found_name:
        return "POSSIBLE_SOURCE_NATIVE_PRODUCT_REVIEW_REQUIRED", "page has name and FITS-like hints, but no product was cached automatically", False
    return "PAGE_REACHED_NOT_SOURCE_NATIVE", "page reached but no direct source-native NGC4088 H I product was identified", False


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
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
    CACHE.mkdir(parents=True, exist_ok=True)

    attempts: list[dict[str, object]] = []
    for candidate in CANDIDATES:
        if candidate.url.startswith("http"):
            if candidate.url.lower().endswith(".gif"):
                status, http_status, content_type, content, text = fetch_binary(candidate.url)
                n_bytes = len(content)
                if http_status == 200:
                    cache_file = CACHE / "whisp_ugc7081_overview.gif"
                    cache_file.write_bytes(content)
                    cached_path = str(cache_file.relative_to(ROOT))
                else:
                    cached_path = ""
            else:
                status, http_status, content_type, n_bytes, text = fetch_url(candidate.url)
                content = b""
                cached_path = ""
            if candidate.candidate_id in {
                "WHISP_FRAMESET_BY_NAME",
                "WHISP_LISTING_BY_NAME",
                "WHISP_UGC7081_DIRECT_PAGE",
                "WHISP_UGC7081_OBS_REDUCTION_NOTES",
            } and http_status == 200:
                cache_file = CACHE / f"{candidate.candidate_id.lower()}.html"
                cache_file.write_text(text, encoding="utf-8", errors="replace")
                cached_path = str(cache_file.relative_to(ROOT))
        else:
            status, http_status, content_type, n_bytes, text = "LOCAL_PATH_AUDITED", None, "", 0, ""
            cached_path = candidate.url

        product_status, status_detail, direct_cached = classify_fetch(candidate, status, http_status, text)
        attempts.append(
            {
                "candidate_id": candidate.candidate_id,
                "route": candidate.route,
                "source_role": candidate.source_role,
                "url": candidate.url,
                "fetch_status": status,
                "http_status": "" if http_status is None else http_status,
                "content_type": content_type,
                "n_bytes": n_bytes,
                "product_status": product_status,
                "status_detail": status_detail,
                "direct_source_native_product_cached": direct_cached,
                "cached_path": cached_path,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    attempts_df = pd.DataFrame(attempts)
    cached_overview = CACHE / "whisp_ugc7081_overview.gif"
    if cached_overview.exists():
        mask = attempts_df["candidate_id"].eq("WHISP_UGC7081_GRAPHICAL_OVERVIEW_GIF")
        attempts_df.loc[mask, "product_status"] = (
            "WHISP_GRAPHICAL_OVERVIEW_CACHED_REVIEW_REQUIRED"
        )
        attempts_df.loc[mask, "status_detail"] = (
            "WHISP graphical H I overview present in local cache; it is "
            "source-provenance image data but not a FITS/source-coordinate product"
        )
        attempts_df.loc[mask, "cached_path"] = str(cached_overview.relative_to(ROOT))
    cached_direct_page = CACHE / "whisp_ugc7081_direct_page.html"
    if cached_direct_page.exists():
        mask = attempts_df["candidate_id"].eq("WHISP_UGC7081_DIRECT_PAGE")
        attempts_df.loc[mask, "product_status"] = (
            "WHISP_DIRECT_PAGE_FOUND_GRAPHICAL_PRODUCT_LINKED"
        )
        attempts_df.loc[mask, "status_detail"] = (
            "direct WHISP page for UGC 7081/NGC4088 present in local cache; "
            "links to graphical overview and observation notes"
        )
        attempts_df.loc[mask, "cached_path"] = str(cached_direct_page.relative_to(ROOT))
    direct_cached = bool(attempts_df["direct_source_native_product_cached"].any())
    graphical_overview_cached = bool(
        attempts_df["product_status"].eq("WHISP_GRAPHICAL_OVERVIEW_CACHED_REVIEW_REQUIRED").any()
    )
    whisp_direct_page_found = bool(
        attempts_df["product_status"].eq("WHISP_DIRECT_PAGE_FOUND_GRAPHICAL_PRODUCT_LINKED").any()
    )

    source_candidates = pd.DataFrame(
        [
            {
                "route_id": "RC1_INDEPENDENT_REVIEWER_DIRECT_ARCMIN",
                "route_status_after_audit": "UNCHANGED_READY_RESPONSE_PENDING",
                "can_close_b1_now": False,
                "why": "requires an independent reviewer response, not an automated web/source audit",
            },
            {
                "route_id": "RC2_FROZEN_IMAGE_REPEAT_WITH_RADIAL_TICK_CALIBRATION",
                "route_status_after_audit": "UNCHANGED_OPEN",
                "can_close_b1_now": False,
                "why": "printed-image repeat is inconclusive until source-native radial calibration is accepted",
            },
            {
                "route_id": "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE",
                "route_status_after_audit": (
                    "DIRECT_SOURCE_NATIVE_PRODUCT_CACHED_REVIEW_REQUIRED"
                    if direct_cached
                    else "WHISP_GRAPHICAL_OVERVIEW_CACHED_EXTRACTION_REVIEW_REQUIRED"
                    if graphical_overview_cached
                    else "AUDITED_NO_DIRECT_SOURCE_NATIVE_PRODUCT_CACHED"
                ),
                "can_close_b1_now": False,
                "why": (
                    "a cached direct product would still require extraction/review"
                    if direct_cached
                    else "WHISP graphical overview was cached, but no FITS/source-coordinate product was cached"
                    if graphical_overview_cached
                    else "no direct FITS/source-coordinate NGC4088 H I product was cached by the audit"
                ),
            },
        ]
    )
    source_candidates["uses_vobs_or_residual"] = False
    source_candidates["endpoint_scores_allowed"] = False
    source_candidates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "original_hi_data_audit_status": (
                    "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE_AUDITED_SOURCE_PRODUCT_REVIEW_REQUIRED"
                    if direct_cached
                    else "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE_AUDITED_NO_DIRECT_PRODUCT_CACHED"
                ),
                "galaxy": "NGC4088",
                "b1_resolution_status": (
                    "B1_NOT_RESOLVED_ORIGINAL_DATA_ROUTE_REVIEW_REQUIRED"
                    if direct_cached
                    else "B1_NOT_RESOLVED_ORIGINAL_DATA_ROUTE_OPEN"
                ),
                "direct_source_native_product_cached": direct_cached,
                "whisp_direct_page_found": whisp_direct_page_found,
                "whisp_graphical_overview_cached": graphical_overview_cached,
                "n_source_candidates_audited": len(attempts_df),
                "n_http_success": int((attempts_df["fetch_status"] == "HTTP_200").sum()),
                "n_direct_products_cached": int(attempts_df["direct_source_native_product_cached"].sum()),
                "formula_freeze_allowed_now": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "obtain a direct WHISP/NED/VizieR/source-coordinate H I product or complete the independent "
                    "reviewer direct-arcmin x_w response; the cached WHISP graphical overview may support a "
                    "separate residual-blind extraction review but does not close B1 by itself"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    attempts_df.to_csv(DATA / "ngc4088_b1_original_hi_data_acquisition_attempts.csv", index=False)
    source_candidates.to_csv(
        DATA / "ngc4088_b1_original_hi_data_source_candidates.csv", index=False
    )
    summary.to_csv(DATA / "ngc4088_b1_original_hi_data_acquisition_summary.csv", index=False)

    report = [
        "# NGC4088 B1 Original H I Data Acquisition Audit",
        "",
        "This audit records the residual-blind RC3 route for B1: can the package cache",
        "an original or source-coordinate H I product for NGC4088 that could support",
        "a source-native warp-onset extraction? It is not an endpoint score.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Source Candidates",
        "",
        markdown_table(source_candidates),
        "",
        "## Acquisition Attempts",
        "",
        markdown_table(attempts_df[[
            "candidate_id",
            "fetch_status",
            "http_status",
            "product_status",
            "direct_source_native_product_cached",
            "cached_path",
        ]]),
        "",
        "## Interpretation",
        "",
        "The original-data route is now audited, not assumed. In the current package",
        "the automated route now finds and caches the WHISP UGC 7081 graphical H I",
        "overview and observation/reduction notes, but it still does not cache a",
        "direct FITS/source-coordinate data cube or table. Therefore B1 remains",
        "open. The cached WHISP overview can support a separate residual-blind",
        "extraction-review packet, but it cannot close B1 by itself.",
        "",
    ]
    (REPORTS / "ngc4088_b1_original_hi_data_acquisition_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
