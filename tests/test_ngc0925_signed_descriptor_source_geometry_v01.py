import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ngc0925_source_geometry_is_reproducible_and_endpoint_blocked():
    subprocess.run(
        [sys.executable, "scripts/freeze_ngc0925_signed_descriptor_source_geometry_v01.py"],
        cwd=ROOT,
        check=True,
    )
    payload = json.loads(
        (ROOT / "data/derived/ngc0925_signed_descriptor_source_geometry_freeze_v01.json").read_text()
    )
    with (ROOT / "data/derived/ngc0925_signed_descriptor_source_geometry_freeze_v01_points.csv").open() as handle:
        rows = list(csv.DictReader(handle))

    assert payload["status"] == "SOURCE_GEOMETRY_DIGITIZATION_COMPLETE_ENDPOINT_BLOCKED_PHYSICAL_UNCERTAINTY"
    assert payload["source"]["embedded_jpeg_shape_yx"] == [756, 561]
    assert payload["digitization"]["ensemble_size"] == 486
    assert len(rows) == 93
    assert payload["digitization"]["absolute_difference_from_published_mean_pa_deg"] < 1.0
    assert payload["digitization"]["maximum_90pct_digitization_width_deg"] < 5.0
    assert len({float(row["inclination_deg"]) for row in rows}) > 5
    assert payload["digitization"]["absolute_difference_from_published_mean_inclination_deg"] < 3.0
    assert payload["digitization"]["maximum_inclination_90pct_digitization_width_deg"] < 10.0
    assert payload["endpoint_pixels_read"] is False
    assert payload["endpoint_allowed"] is False
    assert "not a physical tilted-ring uncertainty" in payload["digitization"]["meaning"]
