#!/usr/bin/env python3
"""Audit local absolute-velocity maps for the common-mode spectral invariant."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from astropy.io import fits
from astropy.coordinates import ICRS, LSRK, SkyCoord
import astropy.units as u


ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data/derived/common_mode_multitracer_source_audit_v01.json"
OUT_REPORT = ROOT / "reports/common_mode_multitracer_source_audit_v01.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def audit(galaxy: str, maps_name: str, co_name: str, center: tuple[float, float]) -> dict:
    base = ROOT / f"data/external/literature/{galaxy}_phangs_tracer_velocity"
    maps_path = base / maps_name
    co_path = base / co_name
    with fits.open(maps_path, memmap=True) as hdul:
        systemic = float(hdul[0].header["REDSHIFT"])
        specsys = hdul[0].header.get("SPECSYS")
        optical = [
            name
            for name in ("HB4861_VEL", "OIII5006_VEL", "HA6562_VEL", "NII6583_VEL")
            if name in hdul
        ]
        optical_shape = list(hdul[optical[0]].data.shape)
    with fits.open(co_path, memmap=True) as hdul:
        co_shape = list(hdul[0].data.shape)
        co_unit = hdul[0].header.get("BUNIT")
        co_specsys = hdul[0].header.get("SPECSYS")
    coordinate = SkyCoord(
        ra=center[0] * u.deg,
        dec=center[1] * u.deg,
        distance=1 * u.Mpc,
        radial_velocity=0 * u.km / u.s,
        pm_ra_cosdec=0 * u.mas / u.yr,
        pm_dec=0 * u.mas / u.yr,
        frame=ICRS(),
    )
    barycentric_to_lsrk = float(coordinate.transform_to(LSRK()).radial_velocity.to_value(u.km / u.s))
    return {
        "galaxy": galaxy.upper(),
        "muse_maps": str(maps_path.relative_to(ROOT)),
        "muse_sha256": sha256(maps_path),
        "muse_reference_velocity_km_s": systemic,
        "muse_spectral_frame": specsys,
        "muse_velocity_layers": optical,
        "muse_shape": optical_shape,
        "co_moment1": str(co_path.relative_to(ROOT)),
        "co_sha256": sha256(co_path),
        "co_unit": co_unit,
        "co_spectral_frame": co_specsys,
        "co_shape": co_shape,
        "absolute_reconstruction_possible": True,
        "spectral_frames_match": specsys == co_specsys,
        "muse_velocity_convention": "systemic-subtracted optical line velocity; restore FITS REDSHIFT reference",
        "co_velocity_convention": "radio Doppler velocity in LSRK",
        "barycentric_to_lsrk_direction_correction_km_s": barycentric_to_lsrk,
        "frame_transform_frozen": True,
        "cross_tracer_common_mode_ready": False,
        "cross_tracer_blocker": (
            "frame transform is frozen, but WCS/PSF, paired geometry, masks, standard baseline, "
            "and covariance remain to be frozen before endpoint scoring"
        ),
        "endpoint_scored": False,
    }


def main() -> None:
    records = [
        audit(
            "ngc4254",
            "NGC4254_MAPS_copt_0.89asec.fits",
            "group.uid___A001_X2fb_X29a.lp_schinner.ngc4254_12m7mtp_co21_mom1wprior.fits",
            (184.7067, 14.4168),
        ),
        audit(
            "ngc3351",
            "NGC3351_MAPS_copt_1.05asec.fits",
            "group.uid___A001_X2fb_X27c.lp_schinner.ngc3351_12m7mtp_co21_mom1wprior.fits",
            (160.9906, 11.7037),
        ),
    ]
    result = {
        "schema": "common_mode_multitracer_source_audit_v01",
        "statistic": "G_spec(R)=sqrt((1+z_plus)(1+z_minus))",
        "primary_candidate": "NGC4254",
        "replication_candidate": "NGC3351",
        "records": records,
        "freeze_before_scoring": [
            "common WCS and PSF/beam",
            "center, position angle, inclination, and opposite-side apertures",
            "radial bins and reference radius R0",
            "velocity-to-redshift convention for MUSE and CO",
            "source-derived BARYCENT-to-LSRK spectral-frame transform",
            "line S/N, fit-quality, profile-width, and outlier masks",
            "standard relativistic and instrumental common-mode baseline",
            "shared geometry and wavelength-calibration covariance",
        ],
        "claim_boundary": (
            "source eligibility only; no common channel, time readout, or Tau Core signal scored"
        ),
        "convention_sources": [
            "https://doi.org/10.1051/0004-6361/202141727",
            "https://openaccess.inaf.it/bitstream/20.500.12386/31307/7/2104.07665-compr.pdf",
            "https://docs.astropy.org/en/stable/api/astropy.coordinates.LSRK.html",
        ],
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2) + "\n")
    lines = [
        "# Common-mode multitracer source audit v01",
        "",
        "The conditional statistic is",
        "`G_spec(R)=sqrt((1+z_plus)(1+z_minus))`. This audit does not evaluate it.",
        "",
        "| role | galaxy | MUSE reference (km/s) | optical velocity layers | CO moment-1 |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for role, row in zip(("primary", "replication"), records):
        lines.append(
            f"| {role} | {row['galaxy']} | {row['muse_reference_velocity_km_s']:.3f} | "
            f"{len(row['muse_velocity_layers'])} | {row['co_unit']} |"
        )
    lines += [
        "",
        "Both local packets can reconstruct absolute velocities within each native",
        "product. MUSE velocities are systemic-subtracted in BARYCENT; CO uses the",
        "radio Doppler convention in LSRK. The source-derived convention and the",
        "Astropy ICRS/LSRK direction transform are now frozen without fitting an offset.",
        "NGC4254 is frozen as the first method preflight and NGC3351 as replication.",
        "Pixel scoring remains closed until frame transport, WCS/PSF, geometry, radial",
        "pairing, masks, velocity conventions, conventional baselines, and covariance",
        "are frozen.",
        "",
        "**Claim boundary:** source eligibility only; no common channel, effective",
        "time readout, or Tau Core signal has been measured.",
    ]
    OUT_REPORT.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
