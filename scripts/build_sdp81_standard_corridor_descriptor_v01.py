#!/usr/bin/env python3
"""Build an endpoint-free standard-lens corridor descriptor for SDP.81 q1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from lenstronomy.LensModel.lens_model import LensModel
from lenstronomy.Util.param_util import phi_q2_ellipticity, shear_polar2cartesian


ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "data/derived/sdp81_lens_operator_freeze_v01.json"
GEOMETRY = ROOT / "data/derived/sdp81_lens_operator_geometry_validation_v01.json"
OUT = ROOT / "data/derived/sdp81_standard_corridor_descriptor_v01.json"
REPORT = ROOT / "reports/sdp81_standard_corridor_descriptor_v01.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> None:
    frozen = json.loads(FREEZE.read_text(encoding="utf-8"))
    geometry = json.loads(GEOMETRY.read_text(encoding="utf-8"))
    model = frozen["models"]["inoue_best_fit"]

    theta_e = model["ellipticity_pa_deg_ccw_from_north"]
    theta_g = model["external_shear_pa_deg_ccw_from_north"]
    e1, e2 = phi_q2_ellipticity(np.deg2rad(90.0 + theta_e), model["axis_ratio_q"])
    gamma1, gamma2 = shear_polar2cartesian(
        np.deg2rad(theta_g), model["external_shear_gamma"]
    )
    center_x, center_y = model["lens_center_arcsec_relative_to_G"]
    kwargs_lens = [
        {
            "theta_E": model["einstein_radius_b_arcsec"],
            "e1": e1,
            "e2": e2,
            "center_x": center_x,
            "center_y": center_y,
        },
        {"gamma1": gamma1, "gamma2": gamma2, "ra_0": 0.0, "dec_0": 0.0},
    ]
    lens = LensModel(["SIE", "SHEAR"])
    positions = np.asarray(
        geometry["image_positions_arcsec_relative_to_G"]["q1"], dtype=float
    )
    source_x, source_y = model["source_positions_arcsec"]["q1"]
    fermat = np.asarray(
        lens.fermat_potential(
            positions[:, 0],
            positions[:, 1],
            kwargs_lens,
            x_source=source_x,
            y_source=source_y,
        ),
        dtype=float,
    )
    relative_fermat = fermat - np.min(fermat)
    magnification = np.asarray(
        lens.magnification(positions[:, 0], positions[:, 1], kwargs_lens), dtype=float
    )
    f_xx, f_xy, f_yx, f_yy = lens.hessian(
        positions[:, 0], positions[:, 1], kwargs_lens
    )

    paths = []
    determinant_errors = []
    for index, (x, y) in enumerate(positions):
        jacobian = np.array(
            [
                [1.0 - f_xx[index], -f_xy[index]],
                [-f_yx[index], 1.0 - f_yy[index]],
            ]
        )
        singular_values = np.linalg.svd(jacobian, compute_uv=False)
        determinant = float(np.linalg.det(jacobian))
        determinant_errors.append(abs(determinant - 1.0 / magnification[index]))
        paths.append(
            {
                "path_id": f"q1_path_{index + 1}",
                "image_position_arcsec_relative_to_G": [float(x), float(y)],
                "fermat_potential_arcsec2": float(fermat[index]),
                "relative_fermat_potential_arcsec2": float(relative_fermat[index]),
                "lens_jacobian_d_beta_d_theta": jacobian.tolist(),
                "jacobian_singular_values": [float(v) for v in singular_values],
                "jacobian_determinant": determinant,
                "signed_magnification": float(magnification[index]),
                "parity": "positive" if determinant > 0.0 else "negative",
            }
        )

    path_matrix = np.column_stack(
        [
            relative_fermat,
            np.log(np.abs(magnification)),
            np.sign(magnification),
        ]
    )
    centered_rank = int(np.linalg.matrix_rank(path_matrix - path_matrix.mean(axis=0)))
    maximum_jacobian_singular_value = float(
        max(max(path["jacobian_singular_values"]) for path in paths)
    )
    paths_above_unit_operator_norm = int(
        sum(max(path["jacobian_singular_values"]) > 1.0 for path in paths)
    )
    checks = {
        "four_q1_paths": bool(len(paths) == 4),
        "finite_fermat_potentials": bool(np.isfinite(fermat).all()),
        "finite_nonzero_magnifications": bool(
            np.isfinite(magnification).all() and np.all(np.abs(magnification) > 0.0)
        ),
        "both_lens_parities_present": bool(
            np.any(magnification > 0.0) and np.any(magnification < 0.0)
        ),
        "jacobian_magnification_identity": bool(max(determinant_errors) < 1.0e-10),
        "path_descriptor_has_relative_rank": bool(centered_rank >= 2),
        "no_spectral_endpoint_input": True,
    }
    payload = {
        "schema": "tau-core.paper8.sdp81-standard-corridor-descriptor.v01",
        "status": (
            "STANDARD_CORRIDOR_COMPARATOR_DERIVED_TAU_PARENT_DEPTH_OPEN"
            if all(checks.values())
            else "STANDARD_CORRIDOR_COMPARATOR_FAILED"
        ),
        "scientific_role": (
            "source-side standard SIE+shear path comparator; not parent depth or Tau loss"
        ),
        "inputs": {
            "lens_freeze": str(FREEZE.relative_to(ROOT)),
            "lens_freeze_sha256": sha256(FREEZE),
            "geometry_validation": str(GEOMETRY.relative_to(ROOT)),
            "geometry_validation_sha256": sha256(GEOMETRY),
            "spectral_or_velocity_endpoint_read": False,
        },
        "source_position_arcsec_relative_to_G": [source_x, source_y],
        "paths": paths,
        "summary": {
            "relative_fermat_span_arcsec2": float(np.ptp(relative_fermat)),
            "absolute_magnification_range": [
                float(np.min(np.abs(magnification))),
                float(np.max(np.abs(magnification))),
            ],
            "centered_descriptor_rank": centered_rank,
            "maximum_jacobian_magnification_identity_error": float(
                max(determinant_errors)
            ),
            "maximum_jacobian_singular_value": maximum_jacobian_singular_value,
            "paths_above_unit_operator_norm": paths_above_unit_operator_norm,
            "negative_parity_paths": int(sum(path["parity"] == "negative" for path in paths)),
        },
        "direct_parent_contraction_identification_allowed": False,
        "direct_identification_no_go": (
            "The lens Jacobian is a standard 4D angular-coordinate map, includes "
            "parity reversal, and has a path with operator norm above one. It is a "
            "comparator/nuisance map, not the positive-metric parent contraction C_P."
        ),
        "checks": checks,
        "checks_passed": int(sum(checks.values())),
        "checks_total": len(checks),
        "endpoint_authorized": False,
        "remaining_blockers": [
            "select and occupy one physical causal-body Hessian rather than identifying Fermat potential with parent depth",
            "prove PATHLIFT-C1 fiber-basicness or freeze four occupied parent-lift keys under one common physical parent packet",
            "propagate full lens, differential-magnification, beam and source-reconstruction covariance",
            "freeze observer access, noise, stable quantizer and terminal calibration on an untouched endpoint",
        ],
        "claim_boundary": (
            "Fermat potential and lens Jacobians are standard 4D corridor descriptors and "
            "nuisance/comparator inputs. They are not Tau parent distance, do not select "
            "T_P|OS, and do not establish nonzero parent loss or Nature occupation."
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 standard corridor descriptor v01\n\n"
        f"Status: `{payload['status']}`; checks: "
        f"**{payload['checks_passed']}/{payload['checks_total']}**.\n\n"
        "The frozen smooth SIE+external-shear model supplies four q1 path records "
        "without reading a spectral or velocity endpoint. The standard descriptor "
        "contains relative Fermat potential, local lens Jacobian, signed "
        "magnification, singular values and parity.\n\n"
        f"The relative Fermat-potential span is "
        f"`{payload['summary']['relative_fermat_span_arcsec2']:.6f} arcsec^2`; "
        f"the absolute magnification range is "
        f"`{payload['summary']['absolute_magnification_range'][0]:.3f}` to "
        f"`{payload['summary']['absolute_magnification_range'][1]:.3f}`. The "
        f"centered three-feature path descriptor has rank "
        f"`{payload['summary']['centered_descriptor_rank']}`.\n\n"
        f"The maximum local lens-Jacobi singular value is "
        f"`{maximum_jacobian_singular_value:.6f}` and "
        f"`{paths_above_unit_operator_norm}` path exceeds unit operator norm. Together "
        "with the two negative-parity paths and the different typed domain, this "
        "forbids identifying the standard lens Jacobian directly with the parent "
        "loss contraction.\n\n"
        "This closes the standard path-comparator object only. Fermat potential is "
        "not identified with Tau parent depth. The conditional FULLCONE map from "
        "an occupied causal-body Hessian to transfer is available, but PATHLIFT-C1 "
        "still requires fibre-basicness or four occupied common-parent lift keys. "
        "Covariance, observer resolution and calibration also remain frozen-source "
        "requirements before an endpoint.\n",
        encoding="utf-8",
    )
    print(payload["status"])
    print(f"checks={payload['checks_passed']}/{payload['checks_total']}")


if __name__ == "__main__":
    main()
