#!/usr/bin/env python3
"""Build and validate the empty accepted-observable manifest template."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


SOURCE_COLUMNS = [
    "source_dataset",
    "measurement_method",
    "pre_scoring_timestamp",
    "residual_blind_certification",
    "accepted_source_status",
]


def nonnull(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return series.notna()
    text = series.fillna("").astype(str).str.strip()
    return text.ne("") & text.ne("nan") & text.ne("TO_BE_FILLED")


def scope_mask(manifest: pd.DataFrame, scope: str) -> pd.Series:
    all_scopes = {"all", "primary quality gate", "secondary quality gate"}
    if scope in all_scopes:
        return pd.Series(True, index=manifest.index)
    families = [part.strip() for part in scope.split(";") if part.strip().startswith("K_")]
    if not families:
        return pd.Series(False, index=manifest.index)
    return manifest["proxy_formula_family_for_scope"].isin(families)


def build_template(manifest: pd.DataFrame, schema: pd.DataFrame) -> pd.DataFrame:
    rows = []
    fields = list(schema["field"])
    for _, item in manifest.iterrows():
        row = {field: "" for field in fields}
        row["galaxy"] = item["galaxy"]
        row["inclination_deg"] = item["inclination_deg"]
        row["distance_frac_error"] = item["distance_frac_error"]
        row["proxy_formula_family_for_scope"] = item["formula_family"]
        row["proxy_manifest_caveat_for_scope"] = item["manifest_caveat"]
        for column in SOURCE_COLUMNS:
            row[column] = "TO_BE_FILLED"
        rows.append(row)
    return pd.DataFrame(rows)


def validate_template(template: pd.DataFrame, schema: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, item in schema.iterrows():
        field = item["field"]
        mask = scope_mask(template, item["scope"])
        n_applicable = int(mask.sum())
        if n_applicable == 0:
            status = "not_applicable_current_template"
            n_present = 0
        else:
            n_present = int(nonnull(template.loc[mask, field]).sum())
            if n_present == n_applicable:
                status = "template_prefilled"
            elif bool(item["required"]):
                status = "blocked_missing_required_accepted_source"
            else:
                status = "optional_missing_or_caveated"
        rows.append(
            {
                "field": field,
                "required": bool(item["required"]),
                "scope": item["scope"],
                "n_applicable_rows": n_applicable,
                "n_present_rows": n_present,
                "n_missing_rows": n_applicable - n_present,
                "template_validation_status": status,
                "accepted_source_rule": item["accepted_source"],
                "forbidden_source": item["forbidden_source"],
            }
        )
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(validation: pd.DataFrame, template: pd.DataFrame) -> None:
    status_counts = (
        validation.groupby("template_validation_status", as_index=False)
        .size()
        .rename(columns={"size": "n_fields"})
        .sort_values("template_validation_status")
    )
    blocked = validation[
        validation["template_validation_status"]
        == "blocked_missing_required_accepted_source"
    ]
    lines = [
        "# Accepted Observable Manifest Template Validation",
        "",
        "This report validates the empty accepted-observable manifest template. The",
        "template is intentionally blocked: it carries galaxy identifiers and",
        "pre-scoring geometry fields, but it does not promote proxy morphology",
        "fields into accepted discovery inputs.",
        "",
        "## Verdict",
        "",
        "The accepted manifest template is collection-ready but endpoint-blocked.",
        f"It contains {len(template)} galaxy rows. Required morphology/source fields",
        f"remain blocked in {len(blocked)} schema fields until accepted residual-blind",
        "sources are entered. This is a guardrail, not a negative empirical result.",
        "",
        "## Status Counts",
        "",
        markdown_table(status_counts),
        "",
        "## Field Validation",
        "",
        markdown_table(validation),
        "",
        "## Claim Boundary",
        "",
        "A future endpoint run should consume a populated accepted manifest, not this",
        "empty template and not the proxy manifest. Passing this validator is a data",
        "readiness condition only; it would not by itself prove Tau Core or guarantee",
        "a better fit than MOND, RAR, TGP, or Newtonian baselines.",
    ]
    (REPORTS / "accepted_observable_manifest_template_validation.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    schema = pd.read_csv(DATA / "morphology_observable_intake_schema.csv")
    template = build_template(manifest, schema)
    validation = validate_template(template, schema)
    template.to_csv(DATA / "accepted_morphology_observable_manifest_template.csv", index=False)
    validation.to_csv(DATA / "accepted_observable_manifest_template_validation.csv", index=False)
    write_report(validation, template)
    print("PAPER8_ACCEPTED_OBSERVABLE_MANIFEST_TEMPLATE_COMPLETE")


if __name__ == "__main__":
    main()
