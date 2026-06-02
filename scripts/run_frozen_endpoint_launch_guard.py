#!/usr/bin/env python3
"""Guard the frozen blind endpoint against premature launch."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    readiness = pd.read_csv(DATA / "accepted_manifest_readiness_summary.csv")
    gates = pd.read_csv(DATA / "accepted_manifest_readiness_gates.csv")
    protocol = pd.read_csv(DATA / "predeclared_endpoint_protocol.csv")

    decision = readiness["endpoint_readiness_decision"].iloc[0]
    blocked = gates[gates["gate_status"] == "BLOCKED"].copy()
    launch_status = (
        "AUTHORIZED_DRY_RUN_ONLY"
        if decision == "READY_FOR_FROZEN_BLIND_ENDPOINT"
        else "LAUNCH_BLOCKED"
    )
    guard_reason = (
        "accepted manifest passed readiness gate"
        if launch_status == "AUTHORIZED_DRY_RUN_ONLY"
        else "accepted residual-blind observables missing"
    )

    primary_lane = protocol.loc[
        protocol["protocol_layer"] == "primary_endpoint_lane", "predeclared_choice"
    ].iloc[0]
    amplitude_policy = protocol.loc[
        protocol["protocol_layer"] == "amplitude_policy", "predeclared_choice"
    ].iloc[0]

    launch = pd.DataFrame(
        [
            {
                "launch_status": launch_status,
                "readiness_decision": decision,
                "primary_endpoint_lane": primary_lane,
                "amplitude_policy": amplitude_policy,
                "blocked_gate_count": int((gates["gate_status"] == "BLOCKED").sum()),
                "guard_reason": guard_reason,
                "endpoint_scores_computed": False,
                "next_action": (
                    "populate accepted manifest and rerun readiness gate"
                    if launch_status == "LAUNCH_BLOCKED"
                    else "run frozen blind endpoint without changing protocol choices"
                ),
            }
        ]
    )

    blocked_summary = blocked[
        ["gate", "blocked_missing_rows", "field_group", "next_action"]
    ].reset_index(drop=True)
    if blocked_summary.empty:
        blocked_summary = pd.DataFrame(
            [
                {
                    "gate": "none",
                    "blocked_missing_rows": 0,
                    "field_group": "none",
                    "next_action": "endpoint launch guard is open",
                }
            ]
        )

    launch.to_csv(DATA / "frozen_endpoint_launch_guard.csv", index=False)
    blocked_summary.to_csv(DATA / "frozen_endpoint_blockers.csv", index=False)

    lines = [
        "# Frozen Endpoint Launch Guard",
        "",
        "This guard decides whether the frozen Paper 8 endpoint protocol may be",
        "launched. It does not compute endpoint scores and it is not an empirical",
        "validation result.",
        "",
        "This launch guard is not an endpoint score.",
        "",
        "## Verdict",
        "",
        f"Launch status: `{launch_status}`.",
        f"Readiness decision: `{decision}`.",
        "",
        "The current package must not run the discovery-style endpoint on the proxy",
        "manifest or on the empty accepted template. This preserves the blind",
        "protocol boundary.",
        "",
        "## Launch Guard",
        "",
        markdown_table(launch),
        "",
        "## Blockers",
        "",
        markdown_table(blocked_summary),
        "",
        "## Claim Boundary",
        "",
        "A blocked launch is a protocol safeguard, not a negative empirical result.",
        "An authorized launch would only permit the frozen endpoint calculation; it",
        "would not by itself prove Tau Core or guarantee superiority over MOND, RAR,",
        "TGP, or Newtonian baselines.",
    ]
    (REPORTS / "frozen_endpoint_launch_guard.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("PAPER8_FROZEN_ENDPOINT_LAUNCH_GUARD_COMPLETE")


if __name__ == "__main__":
    main()
