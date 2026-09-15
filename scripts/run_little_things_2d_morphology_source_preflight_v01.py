#!/usr/bin/env python3
"""Measure source-only support and freeze LITTLE THINGS m=1 descriptors."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import label


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
FREEZE = DATA / "little_things_2d_morphology_population_preregistration_v01.json"
ACQUISITION = DATA / "little_things_2d_morphology_source_acquisition_v01.json"
K_BLOCKS = 8
RHO_IN = 0.20
RHO_OUT = 1.00


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def weighted_quantile(values: np.ndarray, weights: np.ndarray, q: float) -> float:
    order = np.argsort(values)
    cumulative = np.cumsum(weights[order])
    return float(values[order[np.searchsorted(cumulative, q * cumulative[-1])]])


def largest_positive_component(image: np.ndarray) -> np.ndarray:
    components, count = label(np.isfinite(image) & (image > 0), np.ones((3, 3), dtype=int))
    if count == 0:
        return np.zeros_like(image, dtype=bool)
    sizes = np.bincount(components.ravel())
    return components == (1 + int(np.argmax(sizes[1:])))


def maximum_block_gap(blocks: np.ndarray) -> float:
    occupied = np.unique(blocks)
    if occupied.size == 0:
        return 2.0 * math.pi
    centers = (occupied + 0.5) * (2.0 * math.pi / K_BLOCKS)
    gaps = np.diff(np.r_[centers, centers[0] + 2.0 * math.pi])
    return float(gaps.max())


def main() -> None:
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    acquisition = json.loads(ACQUISITION.read_text(encoding="utf-8"))
    if acquisition["status"] != "SOURCE_MOM0_ACQUISITION_COMPLETE":
        raise RuntimeError("Source acquisition is incomplete")
    if acquisition["preregistration_sha256"] != sha256(FREEZE):
        raise RuntimeError("Source acquisition does not match the current freeze")
    ledger_path = ROOT / acquisition["ledger"]
    if acquisition["ledger_sha256"] != sha256(ledger_path):
        raise RuntimeError("Source acquisition ledger hash mismatch")
    acquired = {row["galaxy"]: row for row in csv.DictReader(ledger_path.open(encoding="utf-8"))}
    frozen = {row["galaxy"]: row for row in freeze["rows"]}

    rows = []
    descriptors = {}
    for galaxy in sorted(acquired):
        source = frozen[galaxy]
        if source["catalog_ra_hms"] is None or source["catalog_dec_dms"] is None:
            raise RuntimeError(f"Missing frozen catalog center for {galaxy}")
        path = ROOT / acquired[galaxy]["local_path"]
        if sha256(path) != acquired[galaxy]["sha256"]:
            raise RuntimeError(f"Source-map hash mismatch for {galaxy}")
        with fits.open(path, memmap=True) as hdul:
            image = np.asarray(np.squeeze(hdul[0].data), dtype=float)
            wcs = WCS(hdul[0].header).celestial
        component = largest_positive_component(image)
        yy, xx = np.nonzero(component)
        intensity = image[yy, xx]
        center = SkyCoord(source["catalog_ra_hms"], source["catalog_dec_dms"], unit=("hourangle", "deg"))
        x0, y0 = wcs.world_to_pixel_values(center.ra.deg, center.dec.deg)
        delta_world = wcs.pixel_scale_matrix @ np.vstack((xx - x0, yy - y0))
        east = delta_world[0] * math.cos(center.dec.rad) * 3600.0
        north = delta_world[1] * 3600.0
        pa = math.radians(float(source["optical_pa_deg"]))
        inclination = math.radians(float(source["optical_inclination_deg"]))
        major = east * math.sin(pa) + north * math.cos(pa)
        minor = (east * math.cos(pa) - north * math.sin(pa)) / math.cos(inclination)
        radius = np.hypot(major, minor)
        theta = np.mod(np.arctan2(minor, major), 2.0 * math.pi)
        r95 = weighted_quantile(radius, intensity, 0.95)
        beam = math.sqrt(
            float(source["robust_beam_major_arcsec"]) * float(source["robust_beam_minor_arcsec"])
        )
        beams_per_radius = r95 / beam
        j_capacity = min(5, int(math.floor((RHO_OUT - RHO_IN) * beams_per_radius / 2.0)))
        radial_zones = max(j_capacity, 1)
        support = (radius >= RHO_IN * r95) & (radius <= RHO_OUT * r95)
        block = np.floor(theta[support] * K_BLOCKS / (2.0 * math.pi)).astype(int)
        cells = np.stack((np.floor(east[support] / beam), np.floor(north[support] / beam)), axis=1).astype(int)
        beams_by_block = [int(np.unique(cells[block == k], axis=0).shape[0]) for k in range(K_BLOCKS)]
        blocks_by_zone = []
        mode_rows = []
        for j in range(radial_zones):
            lo = RHO_IN + (RHO_OUT - RHO_IN) * j / radial_zones
            hi = RHO_IN + (RHO_OUT - RHO_IN) * (j + 1) / radial_zones
            zone = support & (radius / r95 >= lo) & (
                radius / r95 < hi if j < radial_zones - 1 else radius / r95 <= hi
            )
            zone_blocks = np.floor(theta[zone] * K_BLOCKS / (2.0 * math.pi)).astype(int)
            blocks_by_zone.append(int(np.unique(zone_blocks).size))
            total = float(image[yy[zone], xx[zone]].sum())
            coefficient = np.sum(image[yy[zone], xx[zone]] * np.exp(-1j * theta[zone])) / total
            mode_rows.append({
                "zone": j,
                "rho_lo": lo,
                "rho_hi": hi,
                "m1_real": float(coefficient.real),
                "m1_imag": float(coefficient.imag),
                "m1_amplitude": float(abs(coefficient)),
                "m1_phase_rad": float(np.angle(coefficient)),
            })
        gap = maximum_block_gap(block)
        support_gate = bool(
            beams_per_radius >= 10.0
            and j_capacity >= 2
            and min(beams_by_block) >= 2
            and min(blocks_by_zone) >= 4
            and gap <= math.pi / 2.0 + 1e-12
        )
        rows.append({
            "galaxy": galaxy,
            "source_map": str(path.relative_to(ROOT)),
            "source_map_sha256": sha256(path),
            "largest_component_pixels": int(component.sum()),
            "source_r95_arcsec": r95,
            "beam_geometric_mean_arcsec": beam,
            "beams_per_source_radius": beams_per_radius,
            "radial_capacity_j": j_capacity,
            "minimum_independent_beams_per_block": min(beams_by_block),
            "minimum_occupied_blocks_per_zone": min(blocks_by_zone),
            "maximum_azimuth_gap_rad": gap,
            "support_gate": support_gate,
        })
        descriptors[galaxy] = {
            "catalog_center_ra_deg": float(center.ra.deg),
            "catalog_center_dec_deg": float(center.dec.deg),
            "optical_pa_deg": float(source["optical_pa_deg"]),
            "optical_inclination_deg": float(source["optical_inclination_deg"]),
            "source_r95_arcsec": r95,
            "radial_capacity_j": j_capacity,
            "m1_radial_descriptor": mode_rows,
            "beams_by_azimuth_block": beams_by_block,
            "occupied_blocks_by_radial_zone": blocks_by_zone,
        }

    passing = [row["galaxy"] for row in rows if row["support_gate"]]
    failing = [row["galaxy"] for row in rows if not row["support_gate"]]
    derangement = {galaxy: passing[(index + 1) % len(passing)] for index, galaxy in enumerate(passing)}
    csv_path = DATA / "little_things_2d_morphology_source_preflight_v01.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = {
        "schema": "little_things_2d_morphology_source_preflight_v01",
        "status": "SOURCE_SUPPORT_PASSED_OPERATOR_CALIBRATION_PENDING" if len(passing) >= 19 else "SOURCE_SUPPORT_POPULATION_INSUFFICIENT",
        "preregistration": str(FREEZE.relative_to(ROOT)),
        "preregistration_sha256": sha256(FREEZE),
        "acquisition": str(ACQUISITION.relative_to(ROOT)),
        "acquisition_sha256": sha256(ACQUISITION),
        "support_ledger": str(csv_path.relative_to(ROOT)),
        "support_ledger_sha256": sha256(csv_path),
        "source_map_count": len(rows),
        "support_pass_count": len(passing),
        "support_fail_count": len(failing),
        "passing_galaxies": passing,
        "failing_galaxies": failing,
        "source_descriptors": descriptors,
        "cross_galaxy_derangement": derangement,
        "source_radius_definition": "deprojected radius enclosing 95% of positive integrated intensity in the largest 8-connected moment-0 component around the frozen optical center",
        "source_mask_definition": "largest 8-connected component of finite strictly positive pixels in the survey-provided robust primary-beam-corrected moment-0 map",
        "hard_support_gate": "B_source>=10, J>=2, >=2 independent beam cells in each of 8 contiguous azimuth blocks, every radial zone represented in >=4 blocks, and maximum occupied-block gap <=pi/2",
        "source_mode_definition": "complex intensity-normalized m=1 coefficient in each of J source-frozen radial zones",
        "operator_calibration_complete": False,
        "velocity_product_acquisition_allowed": False,
        "velocity_pixels_opened": False,
        "endpoint_scoring_allowed": False,
        "tau_endpoint_allowed": False,
        "claim_boundary": "source-only support and morphology descriptor freeze; no kinematic association, parent loss, gravity result, dark-matter replacement, or Tau validation",
    }
    out = DATA / "little_things_2d_morphology_source_preflight_v01.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    report = ROOT / "reports/little_things_2d_morphology_source_preflight_v01.md"
    report.write_text(
        "# LITTLE THINGS 2D morphology source preflight v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The velocity-blind moment-0 audit retained **{len(passing)} of {len(rows)}** acquired "
        f"source galaxies and rejected {len(failing)} under the frozen spatial-support rule. "
        "The retained sample is larger than the 19-object provisional sensitivity floor.\n\n"
        "For each retained galaxy the packet freezes the optical center/orientation, a 95%-flux "
        "source radius, adaptive radial capacity, eight beam-separated azimuth blocks, the complex "
        "radial m=1 descriptor, and a deterministic cross-galaxy derangement. Observed velocity "
        "products remain unopened. The next permitted step is velocity-blind injection/recovery and "
        "rank/leverage calibration of the two-dimensional k=2 target operator.\n\n"
        "This is a source feasibility result only. It does not show a morphology--kinematics "
        "association and has no direct Tau or dark-matter interpretation.\n",
        encoding="utf-8",
    )
    print(result["status"], len(passing), len(failing), failing)


if __name__ == "__main__":
    main()
