#!/usr/bin/env python3
"""Freeze the pre-opening EDGE--CALIFA v03 convention-safe amendment."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
V02 = DATA / "edge_califa_rotation_morphology_preregistration_v02.json"
PREFLIGHT = DATA / "edge_califa_rotation_morphology_source_preflight_v02.json"
CALIBRATION = DATA / "edge_califa_velocity_frame_calibration_v01.json"
OUTPUT = DATA / "edge_califa_rotation_morphology_preregistration_v03.json"
HASH = DATA / "edge_califa_rotation_morphology_preregistration_v03.sha256"
REPORT = ROOT / "reports/edge_califa_rotation_morphology_preregistration_v03.md"
C_KM_S = 299792.458


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    v02 = json.loads(V02.read_text(encoding="utf-8"))
    preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    calibration = json.loads(CALIBRATION.read_text(encoding="utf-8"))
    if v02["endpoint_opened"] or preflight["velocity_terminal_values_opened"]:
        raise RuntimeError("v03 must be frozen before any terminal velocity is opened")
    if calibration["velocity_terminal_values_opened"]:
        raise RuntimeError("Frame calibration crossed the opening boundary")
    if not preflight["endpoint_opening_authorized"]:
        raise RuntimeError("The source-only v02 gate did not authorize endpoint construction")

    protocol = copy.deepcopy(v02)
    protocol["schema"] = "edge_califa_rotation_morphology_preregistration_v03"
    protocol["status"] = "V03_CONVENTION_SAFE_PROTOCOL_FROZEN_FULL_VELOCITY_ENDPOINT_UNOPENED"
    protocol["frozen_date"] = "2026-08-30"
    protocol["supersedes"] = {
        "v02_protocol_sha256": sha256(V02),
        "v02_source_preflight_sha256": sha256(PREFLIGHT),
        "frame_calibration_sha256": sha256(CALIBRATION),
        "reason": (
            "pre-opening correction of the internally inconsistent v02 twelve-versus-six "
            "confirmatory threshold and explicit radio/optical/frame conversion required "
            "by the primary EDGE--CALIFA kinematic analysis"
        ),
        "source_cohort_or_matrices_changed": False,
        "velocity_values_opened_before_amendment": False,
    }
    protocol["amendment_audit"] = {
        "v02_conflict": (
            "deterministic_split.minimum_confirmatory_galaxies was six while one inherited "
            "hard-fail string said twelve"
        ),
        "resolution": "six is controlling and agrees with the frozen split and small-sample design",
        "eligible_galaxies": preflight["source_eligible"],
        "development_no_claim": preflight["development_no_claim"],
        "confirmatory_untouched": preflight["confirmatory_untouched"],
    }
    protocol["decision_rule"]["hard_fail"] = [
        "fewer than 6 source-eligible confirmatory galaxies",
        "any rank, covariance, support, provenance, or hash gate failure",
        "any post-open change to fields, zones, masks, split, controls, conversions, or thresholds",
    ]
    protocol["velocity_frame_and_convention"] = {
        "speed_of_light_km_s": C_KM_S,
        "primary_reference": (
            "Levy et al. 2018, ApJ 860, 92, Appendix A (arXiv:1804.05853): "
            "EDGE uses the radio convention, CALIFA the optical convention, and both "
            "must be converted to the relativistic convention before comparison"
        ),
        "frame_correction": {
            "formula": "v_CO,helio,radio = mom1_12 - rfLSRK2helio",
            "source": calibration["source"],
            "frozen_table": calibration["correction_table"],
            "frozen_table_sha256": calibration["correction_table_sha256"],
        },
        "co_radio_to_relativistic": (
            "v_CO,rel/c = [1-(1-v_CO,helio,radio/c)^2] / "
            "[1+(1-v_CO,helio,radio/c)^2]"
        ),
        "halpha_optical_to_relativistic": (
            "v_Ha,rel/c = [(1+v_Ha,opt/c)^2-1] / [(1+v_Ha,opt/c)^2+1]"
        ),
        "co_error_derivative": (
            "sigma_CO,rel = abs(4*u/(1+u^2)^2)*sigma_CO,radio, u=1-v_CO,helio,radio/c"
        ),
        "halpha_error_derivative": (
            "sigma_Ha,rel = abs(4*s/(1+s^2)^2)*sigma_Ha,opt, s=1+v_Ha,opt/c"
        ),
        "contrast": "Delta_v_rel = v_CO,rel - v_Ha,rel",
        "constant_offset_handling": (
            "the per-zone intercept is fitted and discarded; no endpoint-derived affine "
            "rescaling or tracer-to-tracer calibration is allowed"
        ),
        "audit_boundary": (
            "a later failure of the public products to satisfy these documented conventions "
            "closes the endpoint; it does not authorize empirical refitting"
        ),
    }
    protocol["terminal_opening"]["contrast"] = "v_CO,rel - v_Halpha,rel after the frozen v03 conversions"
    protocol["terminal_opening"]["variance"] = (
        "sigma_CO,rel^2 + sigma_Halpha,rel^2 using the frozen analytic Jacobians"
    )
    protocol["terminal_opening"]["zero_point"] = (
        "intercept included independently in every zone and discarded; harmonic coefficients only"
    )

    payload = json.dumps(protocol, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    HASH.write_text(f"{digest}  data/derived/{OUTPUT.name}\n", encoding="utf-8")
    REPORT.write_text(
        "# EDGE--CALIFA rotation-morphology preregistration v03\n\n"
        f"Status: `{protocol['status']}`\n\n"
        "This pre-opening amendment preserves the v02 cohort and all source matrices. "
        "It resolves the clerical 12/6 threshold conflict in favor of the already frozen "
        "minimum of six confirmatory galaxies and freezes the published EDGE/CALIFA "
        "radio/optical-to-relativistic velocity conversions, including the public "
        "LSRK-to-heliocentric correction. No terminal velocity field has been opened.\n\n"
        "The route remains source-developed prevalidation, not a Tau-specific prediction "
        "or a test that exhausts standard astrophysics.\n",
        encoding="utf-8",
    )
    print(protocol["status"], digest)


if __name__ == "__main__":
    main()
