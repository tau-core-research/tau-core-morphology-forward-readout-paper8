#!/usr/bin/env python3
"""Freeze the NGC7331 THINGS odd/even clock-channel parity diagnostic."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
MANIFEST_PATH = DATA / "ngc7331_things_hi_product_manifest.csv"
GEOMETRY_PATH = DATA / "ngc7331_things_qwarp_measurement_geometry.csv"
MORPHOLOGY_PATH = DATA / "ngc7331_things_qwarp_first_pass_response.csv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = pd.read_csv(MANIFEST_PATH)
    geometry = pd.read_csv(GEOMETRY_PATH).iloc[0]
    morphology = pd.read_csv(MORPHOLOGY_PATH).iloc[0]
    required_products = ["NA_MOM0", "NA_MOM1", "RO_MOM0", "RO_MOM1"]
    selected = manifest.loc[manifest["product_id"].isin(required_products)].copy()
    if set(selected["product_id"]) != set(required_products):
        raise RuntimeError("Required THINGS parity products are incomplete")

    products = {}
    for _, row in selected.iterrows():
        path = Path(row["local_cache_path"])
        if not path.exists():
            raise FileNotFoundError(path)
        digest = sha256(path)
        if digest != row["sha256"]:
            raise RuntimeError(f"THINGS source hash mismatch for {row['product_id']}")
        products[row["product_id"]] = {
            "path": str(path),
            "sha256": digest,
        }

    freeze = {
        "schema": "ngc7331_things_clock_channel_parity_freeze_v01",
        "status": "SOURCE_FROZEN_THINGS_CLOCK_CHANNEL_PARITY_DIAGNOSTIC_READY",
        "galaxy": "NGC7331",
        "source_only": True,
        "mom1_values_opened_by_freeze": False,
        "endpoint_access": False,
        "systemic_velocity_km_s": 818.3,
        "systemic_velocity_source": "de_Blok_et_al_2008_THINGS_Table_2",
        "inclination_deg": 75.8,
        "inclination_source": "de_Blok_et_al_2008_THINGS_Table_2",
        "image_major_axis_deg": float(morphology["inner_disk_pa_image_deg_first_pass"]),
        "image_major_axis_source": "source_only_THINGS_MOM0_principal_axis",
        "center_x_zero_based": float(geometry["crpix1"]) - 1.0,
        "center_y_zero_based": float(geometry["crpix2"]) - 1.0,
        "kpc_per_pixel": float(geometry["kpc_per_pixel"]),
        "rdisk_kpc": float(geometry["rdisk_kpc"]),
        "source_outer_region_start_kpc": 3.0 * float(geometry["rdisk_kpc"]),
        "mom0_signal_threshold": "positive_mom0_at_or_above_0p20_times_positive_p95",
        "pairing_rule": "centrosymmetric_integer_pixel_pair_about_frozen_CRPIX_center",
        "pair_selection_half": "positive_frozen_major_axis_coordinate_only",
        "deprojected_radius": "sqrt(u^2+(v/cos(i))^2)*kpc_per_pixel",
        "major_axis_wedge_abs_cos_theta_min": 0.7,
        "ring_width_kpc": 1.0,
        "minimum_pairs_per_ring": 20,
        "pair_weight": "sqrt(nonnegative_mom0_pixel_times_reflected_pixel)",
        "odd_definition": "0.5*(v_positive_major_side-v_reflected_side)",
        "even_definition": "0.5*(v_positive_major_side+v_reflected_side)-Vsys",
        "primary_metric": "outer_weighted_median_abs_even_over_abs_odd",
        "simple_multiplier_test": (
            "A common multiplicative spectral-clock factor that scales odd velocity must "
            "also appear in the even redshift factor"
        ),
        "product_replication_rule": "NATURAL_and_ROBUST_profiles_must_be_reported_separately",
        "claim_boundary": (
            "single-galaxy velocity-field diagnostic; not a population result, physical "
            "clock-channel detection, quantum-channel detection, or Tau Core validation"
        ),
        "products": products,
        "input_sha256": {
            "manifest": sha256(MANIFEST_PATH),
            "geometry": sha256(GEOMETRY_PATH),
            "morphology": sha256(MORPHOLOGY_PATH),
        },
    }
    freeze_path = DATA / "ngc7331_things_clock_channel_parity_freeze_v01.json"
    freeze_path.write_text(json.dumps(freeze, indent=2) + "\n", encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / "ngc7331_things_clock_channel_parity_freeze_v01.md"
    report_path.write_text(
        f"""# NGC7331 THINGS Clock-Channel Parity Freeze v0.1

**Status:** `SOURCE_FROZEN_THINGS_CLOCK_CHANNEL_PARITY_DIAGNOSTIC_READY`

The freeze records the THINGS product hashes, published systemic velocity and
inclination, MOM0-only image major axis, centrosymmetric pairing, deprojection,
major-axis wedge, 1 kpc radial bins, minimum pair count, odd/even definitions,
and the source-defined outer region `R>=3 R_disk={freeze['source_outer_region_start_kpc']:.3f} kpc`.

The freeze does not open moment-1 velocity values. Natural- and robust-weighted
products must be reported separately. The result remains a single-galaxy
diagnostic regardless of score.
""",
        encoding="utf-8",
    )
    print(freeze["status"])
    print(freeze_path)
    print(report_path)


if __name__ == "__main__":
    main()
