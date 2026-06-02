#!/usr/bin/env python3
"""Build a partial accepted morphology-observable manifest from acquired sources.

The manifest is deliberately conservative.  It may accept individual
source-native observables, such as an S4G/SPARC-derived disk scale, while still
blocking the endpoint row if family labels or family-specific kernel fields
remain unaudited.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


FAMILY_REQUIRED_FIELDS = {
    "K_exponential_disk": ["scale_radius_kpc"],
    "K_scale_tail_spiral": [
        "scale_radius_kpc",
        "tail_inner_radius_kpc",
        "tail_cutoff_radius_kpc",
    ],
    "K_thick_flared": ["scale_radius_kpc", "thickness_h_over_rs"],
    "K_compact_finite": ["compact_support_radius_kpc"],
}


def has_text(value: object) -> bool:
    text = "" if pd.isna(value) else str(value).strip()
    return bool(text) and text.lower() != "nan"


def has_positive(value: object) -> bool:
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def caveat_tokens(value: object) -> list[str]:
    if not has_text(value) or str(value).strip() == "none":
        return []
    return [token.strip() for token in str(value).split(";") if token.strip()]


def accepted_scale(row: pd.Series) -> bool:
    provenance = str(row.get("observable_provenance", ""))
    return (
        row.get("candidate_observable_status")
        == "ACQUIRED_S4G_SPARC_DERIVED"
        and has_positive(row.get("scale_radius_kpc"))
        and "VizieR_J/ApJS/219/4" in provenance
        and row.get("residual_blind_certification")
        == "pre_endpoint_external_catalog_query"
    )


def row_missing_fields(row: pd.Series) -> list[str]:
    family = row["formula_family"]
    required = FAMILY_REQUIRED_FIELDS.get(family, [])
    missing = []
    for field in required:
        if field == "scale_radius_kpc":
            if not bool(row["scale_radius_accepted"]):
                missing.append(field)
        elif not has_positive(row.get(field)):
            missing.append(field)
    return missing


def build_manifest() -> pd.DataFrame:
    candidates = pd.read_csv(DATA / "external_s4g_sparc_observable_candidates.csv")
    proxy = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    keep = [
        "galaxy",
        "formula_family",
        "manifest_confidence",
        "manifest_caveat",
        "inclination_deg",
        "distance_frac_error",
        "role",
        "split",
    ]
    df = candidates.merge(proxy[keep], on="galaxy", how="left", validate="one_to_one")
    df["formula_family_candidate"] = df["proxy_formula_family_for_scope"]
    df["formula_family"] = df["formula_family"]
    df["family_label_source_status"] = "REVIEW_PROXY_LABEL_NEEDS_EXTERNAL_MORPHOLOGY_AUDIT"
    df["family_label_claim_boundary"] = (
        "predeclared proxy family is residual-blind but not yet promoted to an "
        "accepted external morphology label"
    )
    df["scale_radius_accepted"] = df.apply(accepted_scale, axis=1)
    df["scale_radius_source_status"] = df["scale_radius_accepted"].map(
        {
            True: "ACCEPTED_SOURCE_OBSERVABLE",
            False: "MISSING_OR_UNACCEPTED_SOURCE_OBSERVABLE",
        }
    )
    df["scale_radius_kpc"] = df["scale_radius_kpc"].where(df["scale_radius_accepted"])
    df["tail_inner_radius_kpc"] = pd.NA
    df["tail_cutoff_radius_kpc"] = pd.NA
    df["compact_support_radius_kpc"] = pd.NA
    df["thickness_h_over_rs"] = pd.NA
    df["ring_radius_kpc"] = pd.NA
    df["bar_m2_strength"] = df["bar_radius_kpc"].where(df["bar_radius_kpc"].notna())
    df["lopsided_m1_strength"] = pd.NA
    df["source_dataset"] = df["scale_radius_accepted"].map(
        {
            True: "SPARC_Lelli2016c;VizieR_J/ApJS/219/4_S4G_Pipeline4",
            False: "SPARC_Lelli2016c",
        }
    )
    df["measurement_method"] = df["scale_radius_accepted"].map(
        {
            True: "S4G disk-scale arcsec converted to kpc with SPARC distance",
            False: "no accepted source-native morphology observable acquired",
        }
    )
    df["pre_scoring_timestamp"] = "2026-06-02"
    df["residual_blind_certification"] = "pre_endpoint_external_catalog_query"
    df["missing_required_fields"] = df.apply(row_missing_fields, axis=1).str.join(";")
    df["caveat_tokens"] = df["manifest_caveat"].apply(caveat_tokens).str.join(";")
    df["accepted_source_status"] = df["scale_radius_accepted"].map(
        {
            True: "PARTIAL_ACCEPTED_SCALE_RADIUS_ONLY",
            False: "MISSING_ACCEPTED_SOURCE_OBSERVABLES",
        }
    )
    df["endpoint_eligibility_status"] = "BLOCKED_NOT_ENDPOINT_ELIGIBLE"
    df.loc[
        df["scale_radius_accepted"] & df["missing_required_fields"].eq(""),
        "endpoint_eligibility_status",
    ] = "BLOCKED_FAMILY_LABEL_AUDIT_PENDING"
    df["endpoint_blocker"] = df.apply(
        lambda row: (
            "external_family_label_audit_pending"
            if row["missing_required_fields"] == ""
            else "external_family_label_audit_pending;" + row["missing_required_fields"]
        ),
        axis=1,
    )
    df["observable_provenance"] = df["observable_provenance"].where(
        df["scale_radius_accepted"], "SPARC_Lelli2016c.mrt"
    )
    df["claim_boundary"] = (
        "partial_field_level_accepted_observables_not_endpoint_validation"
    )
    columns = [
        "galaxy",
        "split",
        "role",
        "formula_family",
        "formula_family_candidate",
        "family_label_source_status",
        "family_label_claim_boundary",
        "manifest_confidence",
        "manifest_caveat",
        "inclination_deg",
        "distance_frac_error",
        "scale_radius_kpc",
        "scale_radius_source_status",
        "tail_inner_radius_kpc",
        "tail_cutoff_radius_kpc",
        "compact_support_radius_kpc",
        "thickness_h_over_rs",
        "ring_radius_kpc",
        "bar_m2_strength",
        "lopsided_m1_strength",
        "source_dataset",
        "measurement_method",
        "pre_scoring_timestamp",
        "residual_blind_certification",
        "observable_provenance",
        "accepted_source_status",
        "missing_required_fields",
        "caveat_tokens",
        "endpoint_eligibility_status",
        "endpoint_blocker",
        "claim_boundary",
    ]
    return df[columns]


def build_validation(manifest: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    n = len(manifest)
    scale_accepted = int(
        (manifest["scale_radius_source_status"] == "ACCEPTED_SOURCE_OBSERVABLE").sum()
    )
    family_review = int(
        (
            manifest["family_label_source_status"]
            == "REVIEW_PROXY_LABEL_NEEDS_EXTERNAL_MORPHOLOGY_AUDIT"
        ).sum()
    )
    endpoint_ready = int(
        (manifest["endpoint_eligibility_status"] == "READY_FOR_FROZEN_ENDPOINT").sum()
    )
    rows.extend(
        [
            {
                "gate": "row_identity_ready",
                "gate_status": "PASS",
                "n_rows": n,
                "n_pass": n,
                "n_blocked": 0,
                "decision_rule": "all rows preserve SPARC galaxy identity",
            },
            {
                "gate": "scale_radius_source_observables",
                "gate_status": "PARTIAL_PASS",
                "n_rows": n,
                "n_pass": scale_accepted,
                "n_blocked": n - scale_accepted,
                "decision_rule": "S4G disk scale converted with SPARC distance",
            },
            {
                "gate": "external_family_label_audit",
                "gate_status": "BLOCKED",
                "n_rows": n,
                "n_pass": n - family_review,
                "n_blocked": family_review,
                "decision_rule": "proxy family labels must be externally audited before endpoint use",
            },
            {
                "gate": "family_kernel_completeness",
                "gate_status": "BLOCKED",
                "n_rows": n,
                "n_pass": int(manifest["missing_required_fields"].eq("").sum()),
                "n_blocked": int(manifest["missing_required_fields"].ne("").sum()),
                "decision_rule": "all family-specific kernel fields must be source-native",
            },
            {
                "gate": "endpoint_eligibility",
                "gate_status": "BLOCKED",
                "n_rows": n,
                "n_pass": endpoint_ready,
                "n_blocked": n - endpoint_ready,
                "decision_rule": "field-level accepted observables do not by themselves authorize scoring",
            },
        ]
    )
    validation = pd.DataFrame(rows)
    by_family = (
        manifest.groupby("formula_family", as_index=False)
        .agg(
            n_rows=("galaxy", "size"),
            n_scale_radius_accepted=(
                "scale_radius_source_status",
                lambda s: int((s == "ACCEPTED_SOURCE_OBSERVABLE").sum()),
            ),
            n_family_label_review=(
                "family_label_source_status",
                lambda s: int(
                    (s == "REVIEW_PROXY_LABEL_NEEDS_EXTERNAL_MORPHOLOGY_AUDIT").sum()
                ),
            ),
            n_kernel_complete=("missing_required_fields", lambda s: int(s.eq("").sum())),
            n_endpoint_ready=(
                "endpoint_eligibility_status",
                lambda s: int((s == "READY_FOR_FROZEN_ENDPOINT").sum()),
            ),
        )
        .sort_values("formula_family")
    )
    return validation, by_family


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(
    manifest: pd.DataFrame, validation: pd.DataFrame, by_family: pd.DataFrame
) -> None:
    n = len(manifest)
    scale_accepted = int(
        (manifest["scale_radius_source_status"] == "ACCEPTED_SOURCE_OBSERVABLE").sum()
    )
    endpoint_ready = int(
        (manifest["endpoint_eligibility_status"] == "READY_FOR_FROZEN_ENDPOINT").sum()
    )
    lines = [
        "# Accepted Morphology Manifest Draft",
        "",
        "This report builds the first partial accepted morphology-observable manifest",
        "from acquired external SPARC/S4G sources. It accepts only field-level",
        "source-native observables where the provenance is residual-blind and",
        "documented. It does not promote proxy morphology-family labels into",
        "accepted endpoint labels.",
        "",
        "## Verdict",
        "",
        f"Rows in manifest: {n}.",
        f"Accepted S4G/SPARC scale-radius observables: {scale_accepted}.",
        f"Endpoint-ready rows: {endpoint_ready}.",
        "",
        "The manifest is a real data-acquisition upgrade, but it remains endpoint",
        "blocked. The largest remaining blockers are external family-label audit and",
        "family-specific source-native kernel observables for scale-tail, compact,",
        "and thick/flared branches.",
        "",
        "## Gate Status",
        "",
        markdown_table(validation),
        "",
        "## Family Summary",
        "",
        markdown_table(by_family),
        "",
        "## Claim Boundary",
        "",
        "This accepted morphology manifest draft is not an endpoint score.",
        "This manifest is partial. It can be used to audit source coverage and to",
        "prepare the frozen endpoint, but it must not be used as evidence that Tau",
        "Core fits better than MOND, RAR, TGP, or Newtonian baselines. Endpoint",
        "scores remain blocked until the accepted family labels and required",
        "source-native observables pass the readiness gate.",
    ]
    (REPORTS / "accepted_morphology_manifest.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest()
    validation, by_family = build_validation(manifest)
    manifest.to_csv(DATA / "accepted_morphology_manifest.csv", index=False)
    validation.to_csv(DATA / "accepted_morphology_manifest_validation.csv", index=False)
    by_family.to_csv(DATA / "accepted_morphology_manifest_by_family.csv", index=False)
    write_report(manifest, validation, by_family)
    print("PAPER8_ACCEPTED_MORPHOLOGY_MANIFEST_COMPLETE")


if __name__ == "__main__":
    main()
