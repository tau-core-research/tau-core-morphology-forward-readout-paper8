#!/usr/bin/env python3
"""Compare frozen S4G disk-break radii with endpoint-derived dynamic onsets."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TAU_ROOT = ROOT.parent
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
FREEZE_PATH = DATA / "s4g_disk_break_dynamic_onset_freeze_v01.json"
SOURCE_PATH = DATA / "s4g_disk_break_dynamic_onset_freeze_v01.csv"
DYNAMIC_PATH = (
    TAU_ROOT
    / "tau-core-theory/source_material/tau_core_foundations/numerical_checks/"
    "tau_core_galactic_clock_channel_reparameterization_v01_galaxies.csv"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alignment_metric(dynamic_radius: np.ndarray, source_radius: np.ndarray) -> float:
    return float(np.median(np.abs(np.log(dynamic_radius / source_radius))))


def score_threshold(
    joined: pd.DataFrame, onset_column: str
) -> tuple[dict[str, object], pd.DataFrame]:
    paired = joined.loc[
        joined[onset_column].notna() & joined["break_radius_kpc"].gt(0)
    ].copy()
    dynamic = paired[onset_column].astype(float).to_numpy()
    breaks = paired["break_radius_kpc"].astype(float).to_numpy()
    rdisk = paired["sparc_rdisk_kpc"].astype(float).to_numpy()
    observed = alignment_metric(dynamic, breaks)
    rdisk_control = alignment_metric(dynamic, rdisk)

    permutations = list(itertools.permutations(breaks))
    null = np.array(
        [alignment_metric(dynamic, np.asarray(values)) for values in permutations]
    )
    p_lower = float((1 + np.sum(null <= observed)) / (len(null) + 1))
    paired["dynamic_onset_kpc"] = dynamic
    paired["rdyn_over_rbreak"] = dynamic / breaks
    paired["absolute_log_rdyn_over_rbreak"] = np.abs(np.log(dynamic / breaks))
    paired["rdyn_over_rdisk"] = dynamic / rdisk
    return (
        {
            "n_paired": int(len(paired)),
            "median_absolute_log_rdyn_over_rbreak": observed,
            "median_absolute_log_rdyn_over_rdisk_control": rdisk_control,
            "break_alignment_better_than_rdisk_control": observed < rdisk_control,
            "exact_permutations": int(len(null)),
            "permutation_p_lower_is_better": p_lower,
            "null_median": float(np.median(null)),
            "null_q05": float(np.quantile(null, 0.05)),
        },
        paired,
    )


def main() -> None:
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    if freeze["status"] != "SOURCE_ONLY_DISK_BREAK_ALIGNMENT_PILOT_FREEZE_READY_SMALL_N":
        raise RuntimeError("Disk-break onset freeze is not ready")
    if not freeze["source_only"] or freeze["endpoint_access"]:
        raise RuntimeError("Disk-break source/endpoint boundary failed")
    if sha256(SOURCE_PATH) != freeze["frozen_source_sha256"]:
        raise RuntimeError("Frozen disk-break source hash mismatch")

    source = pd.read_csv(SOURCE_PATH)
    dynamic = pd.read_csv(DYNAMIC_PATH)
    joined = source.merge(dynamic, on="galaxy", how="inner", validate="one_to_one")
    if len(joined) != freeze["n_source_rows"]:
        raise RuntimeError(
            f"Dynamic join changed source sample: {len(joined)} != {freeze['n_source_rows']}"
        )

    thresholds = {
        "d1p5": "onset_radius_kpc_d1p5",
        "d2p0_primary": "onset_radius_kpc_d2p0",
        "d3p0": "onset_radius_kpc_d3p0",
    }
    metrics = {}
    point_frames = []
    for label, column in thresholds.items():
        result, paired = score_threshold(joined, column)
        metrics[label] = result
        paired.insert(1, "threshold_label", label)
        point_frames.append(paired)

    points = pd.concat(point_frames, ignore_index=True)
    points_path = DATA / "s4g_disk_break_dynamic_onset_alignment_points_v01.csv"
    points.to_csv(points_path, index=False)

    primary = metrics["d2p0_primary"]
    status = "DIAGNOSTIC_ONLY_S4G_DISK_BREAK_DYNAMIC_ONSET_SMALL_N"
    summary = {
        "schema": "s4g_disk_break_dynamic_onset_alignment_v01",
        "status": status,
        "source_rows": len(source),
        "minimum_population_n": freeze["minimum_population_n"],
        "population_claim_allowed": False,
        "metrics": metrics,
        "primary_descriptive_verdict": (
            "ALIGNMENT_PILOT_NOT_SIGNIFICANT"
            if primary["permutation_p_lower_is_better"] > 0.05
            else "ALIGNMENT_PILOT_LOW_P_BUT_UNDERPOWERED"
        ),
        "freeze_sha256": sha256(FREEZE_PATH),
        "source_sha256": sha256(SOURCE_PATH),
        "dynamic_atlas_sha256": sha256(DYNAMIC_PATH),
        "claim_boundary": (
            "retrospective small-N alignment diagnostic; alignment cannot identify source "
            "versus clock, quantum, path, gravity, or mixed channel origin"
        ),
    }
    summary_path = DATA / "s4g_disk_break_dynamic_onset_alignment_v01.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / "s4g_disk_break_dynamic_onset_alignment_v01.md"
    report_path.write_text(
        f"""# S4G Disk-Break/Dynamic-Onset Alignment v0.1

**Status:** `{status}`

| threshold | paired N | median abs log(Rdyn/Rbreak) | Rdisk control | exact permutation p |
| --- | ---: | ---: | ---: | ---: |
| `D>=1.5` | {metrics['d1p5']['n_paired']} | {metrics['d1p5']['median_absolute_log_rdyn_over_rbreak']:.6f} | {metrics['d1p5']['median_absolute_log_rdyn_over_rdisk_control']:.6f} | {metrics['d1p5']['permutation_p_lower_is_better']:.6f} |
| `D>=2` primary | {primary['n_paired']} | {primary['median_absolute_log_rdyn_over_rbreak']:.6f} | {primary['median_absolute_log_rdyn_over_rdisk_control']:.6f} | {primary['permutation_p_lower_is_better']:.6f} |
| `D>=3` | {metrics['d3p0']['n_paired']} | {metrics['d3p0']['median_absolute_log_rdyn_over_rbreak']:.6f} | {metrics['d3p0']['median_absolute_log_rdyn_over_rdisk_control']:.6f} | {metrics['d3p0']['permutation_p_lower_is_better']:.6f} |

Only {primary['n_paired']} galaxies have both a published break radius and the
primary persistent dynamic onset. The frozen minimum for a population claim is
15. This pilot is therefore descriptive regardless of its permutation rank.

An onset alignment would show a radial coupling but would not decide whether
the origin is source morphology, gravity, a clock/path channel, a quantum
measurement channel, or a mixed source-channel response.
""",
        encoding="utf-8",
    )
    print(status)
    print(summary_path)
    print(report_path)
    print(points_path)


if __name__ == "__main__":
    main()
