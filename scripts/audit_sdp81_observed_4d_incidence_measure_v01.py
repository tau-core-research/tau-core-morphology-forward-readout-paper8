#!/usr/bin/env python3
"""Build an endpoint-blind observed 4D path-incidence counting measure."""

from __future__ import annotations

import hashlib
import json
import warnings
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.wcs import FITSFixedWarning


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REGISTRATION = DATA / "sdp81_image_g_wcs_registration_v01.json"
CONTINUUM = ROOT / (
    "data/external/literature/sdp81_multipath_channel/"
    "SDP81_Band7_ReferenceImages/SDP81_band7_11exec.contR1.image.fits"
)
OUT = DATA / "sdp81_observed_4d_incidence_measure_v01.json"
REPORT = ROOT / "reports/sdp81_observed_4d_incidence_measure_v01.md"

APERTURE_RADIUS_ARCSEC = 0.12
OFF_SOURCE_INNER_RADIUS_ARCSEC = 4.0
DETECTION_THRESHOLD_SIGMA = 5.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def robust_rms(values: np.ndarray) -> float:
    values = values[np.isfinite(values)]
    median = float(np.median(values))
    return 1.4826 * float(np.median(np.abs(values - median)))


def main() -> dict[str, object]:
    registration = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FITSFixedWarning)
        with fits.open(CONTINUUM) as hdul:
            image = np.squeeze(hdul[0].data).astype(float)
            header = hdul[0].header

    pixel_arcsec = abs(float(header["CDELT1"])) * 3600.0
    beam_major_arcsec = float(header["BMAJ"]) * 3600.0
    beam_minor_arcsec = float(header["BMIN"]) * 3600.0
    beam_area_arcsec2 = (
        np.pi * beam_major_arcsec * beam_minor_arcsec / (4.0 * np.log(2.0))
    )
    pixel_area_arcsec2 = pixel_arcsec**2
    pixels_per_beam = beam_area_arcsec2 / pixel_area_arcsec2

    gy, gx = np.indices(image.shape)
    anchor_x = float(registration["anchor"]["pixel_x_zero_based"])
    anchor_y = float(registration["anchor"]["pixel_y_zero_based"])
    radius_arcsec = np.hypot(gx - anchor_x, gy - anchor_y) * pixel_arcsec
    off_source = image[(radius_arcsec >= OFF_SOURCE_INNER_RADIUS_ARCSEC) & np.isfinite(image)]
    rms_per_beam = robust_rms(off_source)

    atoms: list[dict[str, object]] = []
    for path in registration["q1_paths"]:
        x0 = float(path["pixel_x_zero_based"])
        y0 = float(path["pixel_y_zero_based"])
        rr = np.hypot(gx - x0, gy - y0) * pixel_arcsec
        mask = (rr <= APERTURE_RADIUS_ARCSEC) & np.isfinite(image)
        aperture_values = image[mask]
        aperture_beams = float(mask.sum() / pixels_per_beam)
        integrated_flux_jy = float(aperture_values.sum() / pixels_per_beam)
        integrated_sigma_jy = float(rms_per_beam * np.sqrt(aperture_beams))
        integrated_snr = integrated_flux_jy / integrated_sigma_jy
        peak_jy_per_beam = float(np.max(aperture_values))
        peak_snr = peak_jy_per_beam / rms_per_beam
        detected = bool(
            integrated_snr >= DETECTION_THRESHOLD_SIGMA
            and peak_snr >= DETECTION_THRESHOLD_SIGMA
            and integrated_flux_jy > 0.0
        )
        incidence_payload = {
            "path_key": f"q1_path_{path['path_index']}",
            "ra_deg": path["ra_deg"],
            "dec_deg": path["dec_deg"],
            "continuum_sha256": sha256(CONTINUUM),
        }
        atoms.append(
            {
                **incidence_payload,
                "incidence_key": hashlib.sha256(
                    json.dumps(
                        incidence_payload, sort_keys=True, separators=(",", ":")
                    ).encode()
                ).hexdigest(),
                "aperture_radius_arcsec": APERTURE_RADIUS_ARCSEC,
                "aperture_beams": aperture_beams,
                "integrated_flux_jy": integrated_flux_jy,
                "integrated_sigma_jy": integrated_sigma_jy,
                "integrated_snr": integrated_snr,
                "peak_jy_per_beam": peak_jy_per_beam,
                "peak_snr": peak_snr,
                "detected": detected,
                "counting_mass": 1.0 if detected else 0.0,
            }
        )

    detected_atoms = [atom for atom in atoms if atom["detected"]]
    total_mass = float(sum(atom["counting_mass"] for atom in atoms))
    normalized_mass = [
        float(atom["counting_mass"] / total_mass) if total_mass > 0.0 else 0.0
        for atom in atoms
    ]
    checks = {
        "band7_continuum_artifact_present": CONTINUUM.is_file(),
        "absolute_wcs_registration_operational": registration[
            "absolute_wcs_registration_operational"
        ]
        is True,
        "four_registered_q1_locations": len(atoms) == 4,
        "robust_off_source_rms_positive": rms_per_beam > 0.0,
        "all_four_paths_detected_above_five_sigma": len(detected_atoms) == 4,
        "positive_nonzero_counting_measure": total_mass > 0.0,
        "normalized_measure_has_unit_mass": abs(sum(normalized_mass) - 1.0) < 1.0e-12,
        "unique_incidence_keys": len({atom["incidence_key"] for atom in atoms})
        == len(atoms),
        "no_spectral_or_velocity_endpoint_read": True,
        "no_parent_lift_or_transfer_field_materialized": True,
    }
    status = (
        "OBSERVED_4D_INCIDENCE_MEASURE_PASS"
        if all(checks.values())
        else "OBSERVED_4D_INCIDENCE_MEASURE_NOT_ESTABLISHED"
    )
    result: dict[str, object] = {
        "schema": "tau-core.paper8.sdp81-observed-4d-incidence-measure.v01",
        "status": status,
        "scientific_role": (
            "endpoint-blind positive counting measure on Band-7-detected 4D image-path incidences"
        ),
        "inputs": {
            "continuum": str(CONTINUUM.relative_to(ROOT)),
            "continuum_sha256": sha256(CONTINUUM),
            "registration": str(REGISTRATION.relative_to(ROOT)),
            "registration_sha256": sha256(REGISTRATION),
            "spectral_or_velocity_endpoint_read": False,
        },
        "measurement": {
            "image_unit": header.get("BUNIT"),
            "pixel_arcsec": pixel_arcsec,
            "beam_major_arcsec": beam_major_arcsec,
            "beam_minor_arcsec": beam_minor_arcsec,
            "robust_off_source_rms_jy_per_beam": rms_per_beam,
            "off_source_inner_radius_arcsec": OFF_SOURCE_INNER_RADIUS_ARCSEC,
            "aperture_radius_arcsec": APERTURE_RADIUS_ARCSEC,
            "detection_threshold_sigma": DETECTION_THRESHOLD_SIGMA,
        },
        "atoms": atoms,
        "counting_measure": {
            "total_mass": total_mass,
            "normalized_masses_in_path_order": normalized_mass,
            "semantics": (
                "unweighted positive counting measure on independently detected 4D incidence atoms"
            ),
        },
        "checks": checks,
        "checks_passed": int(sum(checks.values())),
        "checks_total": len(checks),
        "parent_selector_or_lift_occupation_materialized": False,
        "claim_boundary": (
            "This is observed post-body 4D path-incidence support conditional on the "
            "frozen standard lens/WCS registration. It is not a Tau parent lift, "
            "does not select a parent section, and does not establish parent-law "
            "Nature occupation, transfer, loss, time, quantum structure, or gravity."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 observed 4D incidence measure v01\n\n"
        f"Status: `{status}`; checks: "
        f"**{result['checks_passed']}/{result['checks_total']}**.\n\n"
        "A frozen `0.12 arcsec` aperture was evaluated at each of the four "
        "registered q1 image-path locations in the independent ALMA Band-7 "
        "continuum image. Noise is the robust MAD scale outside `4 arcsec` "
        "from image G. A path is counted only when both its integrated and peak "
        "continuum signal exceed `5 sigma`.\n\n"
        f"Detected atoms: `{len(detected_atoms)}/4`; counting-measure mass: "
        f"`{total_mass:.1f}`. Integrated SNR range: "
        f"`{min(atom['integrated_snr'] for atom in atoms):.3f}` to "
        f"`{max(atom['integrated_snr'] for atom in atoms):.3f}`; peak SNR range: "
        f"`{min(atom['peak_snr'] for atom in atoms):.3f}` to "
        f"`{max(atom['peak_snr'] for atom in atoms):.3f}`.\n\n"
        "This establishes only positive observed 4D incidence support, "
        "conditional on the standard lens/WCS registration. It supplies no "
        "parent section or lift occupation.\n",
        encoding="utf-8",
    )
    print(status)
    print(f"checks={result['checks_passed']}/{result['checks_total']}")
    print(f"detected_paths={len(detected_atoms)}/4")
    return result


if __name__ == "__main__":
    main()
