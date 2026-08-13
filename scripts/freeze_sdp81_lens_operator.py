#!/usr/bin/env python3
"""Freeze the published smooth SDP.81 lens operators and claim boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/sdp81_lens_operator_freeze_v01.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    arxiv_source = ROOT / (
        "data/external/literature/sdp81_multipath_channel/"
        "inoue2016_arxiv1510.00150/source.tar"
    )
    models = {
        "inoue_best_fit": {
            "chi2_per_dof": "0.647/3",
            "lens_center_arcsec_relative_to_G": [-0.007, -0.017],
            "einstein_radius_b_arcsec": 1.605,
            "ellipticity_e_one_minus_q": 0.17,
            "axis_ratio_q": 0.83,
            "ellipticity_pa_deg_ccw_from_north": 25.0,
            "external_shear_gamma": 0.057,
            "external_shear_pa_deg_ccw_from_north": -10.0,
            "source_positions_arcsec": {
                "q1": [0.1978, 0.0215],
                "d1": [0.1783, -0.0645],
                "d2": [0.1781, -0.0780],
            },
        },
        "inoue_concordant": {
            "chi2_per_dof": "1.51/3",
            "lens_center_arcsec_relative_to_G": [-0.024, -0.005],
            "einstein_radius_b_arcsec": 1.609,
            "ellipticity_e_one_minus_q": 0.20,
            "axis_ratio_q": 0.80,
            "ellipticity_pa_deg_ccw_from_north": 16.0,
            "external_shear_gamma": 0.041,
            "external_shear_pa_deg_ccw_from_north": -8.0,
        },
        "dye_semilinear_orientation_refit": {
            "chi2_per_dof": "5.18/3",
            "lens_center_arcsec_relative_to_G": [-0.033, 0.005],
            "einstein_radius_b_arcsec": 1.606,
            "ellipticity_e_one_minus_q": 0.20,
            "axis_ratio_q": 0.80,
            "ellipticity_pa_deg_ccw_from_north": 13.0,
            "external_shear_gamma": 0.040,
            "external_shear_pa_deg_ccw_from_north": -4.0,
        },
    }
    payload = {
        "schema": "tau-core.paper8.sdp81-lens-operator-freeze.v01",
        "status": "PARAMETERS_FROZEN_IMAGE_G_WCS_REGISTRATION_OPEN",
        "scientific_role": "standard-lensing path equalization operator",
        "source": {
            "paper": "Inoue et al. (2016), arXiv:1510.00150",
            "arxiv_source_path": str(arxiv_source.relative_to(ROOT)),
            "arxiv_source_sha256": sha256(arxiv_source),
            "parameter_table": "prepri2.tex Tables 1-3",
            "sie_definition": "Kormann et al. (1994)",
        },
        "coordinates": {
            "image_plane_x": "right ascension offset in arcsec",
            "image_plane_y": "declination offset in arcsec",
            "origin": "centroid of image G",
            "angles": "counter-clockwise from North",
            "image_G_icrs_j2000": {
                "ra_hms": "09:03:11.573",
                "dec_dms": "+00:39:06.54",
                "source": "Tamura et al. (2015), arXiv:1503.07605",
                "reported_role": "central compact non-thermal source",
            },
        },
        "models": models,
        "promotion_gates": [
            "register image G in the selected ALMA image WCS",
            "implement Kormann SIE plus external shear with explicit convention transforms",
            "reproduce published critical-curve or multiple-image positions",
            "repeat the path comparison over all three frozen smooth models",
        ],
        "forbidden_claims": [
            "A residual before lens-operator validation is not a channel effect.",
            "A multipath residual does not identify time, quantum, or Tau Core origin.",
            "The published anomaly is compatible with line-of-sight structure and lens-model systematics.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
