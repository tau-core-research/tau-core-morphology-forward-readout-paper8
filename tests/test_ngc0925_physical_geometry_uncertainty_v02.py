import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ngc0925_physical_errors_expose_identifiability_failure_without_endpoint_access():
    subprocess.run(
        [sys.executable, "scripts/audit_ngc0925_physical_geometry_uncertainty_v02.py"],
        cwd=ROOT,
        check=True,
    )
    payload = json.loads(
        (ROOT / "data/derived/ngc0925_physical_geometry_uncertainty_v02.json").read_text()
    )
    with (ROOT / "data/derived/ngc0925_physical_geometry_uncertainty_v02_points.csv").open() as handle:
        rows = list(csv.DictReader(handle))

    assert payload["status"] == "PHYSICAL_MC_ACQUIRED_GEOMETRY_IDENTIFIABILITY_FAIL_ENDPOINT_BLOCKED"
    assert len(rows) == 15
    assert payload["uncertainty_model"]["iterations"] == 100
    assert payload["uncertainty_model"]["cross_ring_covariance_published"] is False
    assert payload["identifiability"]["inner_boundary_arcsec"] == 250.0
    assert payload["identifiability"]["outer_robust_independent_comparison_ring_count"] == 1
    assert payload["cross_source_comparison"]["outer_270_arcsec_inclination_gap_over_schmidt_mc_sigma"] < 2.0
    assert payload["cross_source_comparison"]["outer_270_arcsec_pa_gap_over_schmidt_mc_sigma"] > 2.0
    assert payload["cross_source_comparison"]["outer_270_arcsec_one_sigma_pa_intervals_overlap"] is False
    assert payload["endpoint_pixels_read"] is False
    assert payload["endpoint_allowed"] is False
