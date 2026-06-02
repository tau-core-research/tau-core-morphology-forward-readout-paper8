#!/usr/bin/env python3
"""Audit the gap between the proxy manifest and accepted morphology observables."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


FIELD_MAP = {
    "galaxy": ("galaxy", "accepted_available"),
    "formula_family": ("formula_family", "proxy_available"),
    "manifest_confidence": ("manifest_confidence", "proxy_available"),
    "manifest_caveat": ("manifest_caveat", "proxy_available"),
    "inclination_deg": ("inclination_deg", "accepted_available"),
    "distance_frac_error": ("distance_frac_error", "accepted_available"),
    "scale_radius_kpc": ("scale_radius_proxy_kpc", "proxy_available"),
    "tail_inner_radius_kpc": ("tail_inner_radius_proxy_kpc", "proxy_available"),
    "tail_cutoff_radius_kpc": ("tail_cutoff_radius_proxy_kpc", "proxy_available"),
    "compact_support_radius_kpc": ("compact_support_radius_proxy_kpc", "proxy_available"),
    "thickness_h_over_rs": ("thickness_h_over_rs_proxy", "proxy_available"),
    "ring_radius_kpc": ("ring_radius_proxy_kpc", "proxy_available"),
    "bar_m2_strength": ("bar_m2_proxy", "proxy_available"),
    "lopsided_m1_strength": ("lopsided_m1_proxy", "proxy_available"),
    "observable_provenance": ("parameter_source", "proxy_available"),
}


STATUS_ACTIONS = {
    "accepted_available": "keep as pre-scoring catalog/geometry input",
    "proxy_available": "replace proxy with accepted residual-blind morphology observable",
    "not_in_current_family_set": "not applicable to current 1D SPARC first-pass family set",
    "missing_required": "block endpoint until field is supplied",
    "missing_optional": "keep family caveated or out of current endpoint",
}


def nonnull(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return series.notna()
    text = series.fillna("").astype(str).str.strip()
    return text.ne("") & text.ne("nan")


def scope_mask(manifest: pd.DataFrame, scope: str) -> pd.Series:
    all_scopes = {"all", "primary quality gate", "secondary quality gate"}
    if scope in all_scopes:
        return pd.Series(True, index=manifest.index)
    families = [part.strip() for part in scope.split(";") if part.strip().startswith("K_")]
    if not families:
        return pd.Series(False, index=manifest.index)
    return manifest["formula_family"].isin(families)


def audit_rows(manifest: pd.DataFrame, schema: pd.DataFrame) -> pd.DataFrame:
    rows = []
    current_families = set(manifest["formula_family"])
    for _, item in schema.iterrows():
        field = item["field"]
        source_field, base_status = FIELD_MAP.get(field, ("", "missing_optional"))
        mask = scope_mask(manifest, item["scope"])
        n_applicable = int(mask.sum())

        scoped_families = [
            part.strip()
            for part in str(item["scope"]).split(";")
            if part.strip().startswith("K_")
        ]
        if n_applicable == 0 and scoped_families and not current_families.intersection(scoped_families):
            status = "not_in_current_family_set"
            n_available = 0
            coverage_fraction = 0.0
        elif source_field in manifest.columns:
            available = nonnull(manifest.loc[mask, source_field])
            n_available = int(available.sum())
            coverage_fraction = n_available / n_applicable if n_applicable else 0.0
            status = base_status
            if n_available < n_applicable and bool(item["required"]):
                status = "missing_required"
            elif n_available < n_applicable:
                status = "missing_optional"
        else:
            status = "missing_required" if bool(item["required"]) else "missing_optional"
            n_available = 0
            coverage_fraction = 0.0

        rows.append(
            {
                "field": field,
                "required": bool(item["required"]),
                "scope": item["scope"],
                "manifest_source_field": source_field,
                "availability_status": status,
                "n_applicable_rows": n_applicable,
                "n_available_rows": n_available,
                "coverage_fraction": round(coverage_fraction, 3),
                "accepted_ready": status == "accepted_available",
                "required_next_action": STATUS_ACTIONS[status],
            }
        )
    return pd.DataFrame(rows)


def family_rows(manifest: pd.DataFrame, gap: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for family, family_df in manifest.groupby("formula_family"):
        relevant = gap[
            gap["scope"].isin(["all", "primary quality gate", "secondary quality gate"])
            | gap["scope"].str.contains(family, regex=False)
        ]
        required = relevant[relevant["required"]]
        rows.append(
            {
                "formula_family": family,
                "n_galaxies": len(family_df),
                "required_fields_applicable": int(len(required)),
                "accepted_ready_required_fields": int(required["accepted_ready"].sum()),
                "proxy_required_fields": int(
                    (required["availability_status"] == "proxy_available").sum()
                ),
                "missing_required_fields": int(
                    (required["availability_status"] == "missing_required").sum()
                ),
                "readiness_status": (
                    "proxy_coverage_ready_acceptance_not_ready"
                    if (required["availability_status"] == "proxy_available").any()
                    else "accepted_ready"
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("formula_family")


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(gap: pd.DataFrame, by_family: pd.DataFrame) -> None:
    status_counts = (
        gap.groupby("availability_status", as_index=False)
        .size()
        .rename(columns={"size": "n_fields"})
        .sort_values(["availability_status"])
    )
    n_required_missing = int((gap["availability_status"] == "missing_required").sum())
    n_proxy = int((gap["availability_status"] == "proxy_available").sum())
    lines = [
        "# Morphology Observable Gap Audit",
        "",
        "This audit compares the current available-data proxy manifest against the",
        "residual-blind morphology-observable intake schema. It is not an endpoint",
        "score and not an empirical validation claim.",
        "",
        "## Verdict",
        "",
        "The current manifest is coverage-rich but acceptance-limited. It has broad",
        "proxy coverage for the active morphology families, but most kernel-driving",
        "fields are not accepted residual-blind observables yet. The next Paper 8",
        "upgrade should therefore replace proxies with external/pre-scoring",
        "morphology measurements rather than changing endpoint gates or tuning",
        "formula families after seeing residuals.",
        "",
        f"- Missing required fields: {n_required_missing}",
        f"- Proxy fields requiring accepted-source upgrade: {n_proxy}",
        "",
        "## Field Status Counts",
        "",
        markdown_table(status_counts),
        "",
        "## Required/Optional Field Gap",
        "",
        markdown_table(
            gap[
                [
                    "field",
                    "required",
                    "scope",
                    "manifest_source_field",
                    "availability_status",
                    "n_applicable_rows",
                    "n_available_rows",
                    "coverage_fraction",
                    "required_next_action",
                ]
            ]
        ),
        "",
        "## Family-Level Readiness",
        "",
        markdown_table(by_family),
        "",
        "## Claim Boundary",
        "",
        "This gap audit is not an endpoint score.",
        "",
        "A field marked `proxy_available` may be useful for preparation diagnostics,",
        "but it must not be promoted to discovery evidence. The accepted run needs",
        "residual-blind morphology labels and kernel observables fixed before",
        "endpoint scoring.",
    ]
    (REPORTS / "morphology_observable_gap_audit.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    schema = pd.read_csv(DATA / "morphology_observable_intake_schema.csv")

    gap = audit_rows(manifest, schema)
    by_family = family_rows(manifest, gap)

    gap.to_csv(DATA / "morphology_observable_gap_audit.csv", index=False)
    by_family.to_csv(DATA / "morphology_observable_gap_by_family.csv", index=False)
    write_report(gap, by_family)
    print("PAPER8_MORPHOLOGY_OBSERVABLE_GAP_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
