#!/usr/bin/env python3
"""Acquire source-native NGC3726 WSRT H I side rotation and GHASP geometry."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "external" / "catalogs" / "ngc3726_uma_hi"
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
UMA = "https://cdsarc.cds.unistra.fr/ftp/J/A+A/370/765"
GHASP = "https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/390/466"
SOURCES = {
    "uma_readme": f"{UMA}/ReadMe",
    "uma_identity": f"{UMA}/table1.dat.gz",
    "uma_rotation": f"{UMA}/table4.dat.gz",
    "uma_summary": f"{UMA}/table5.dat.gz",
    "ghasp_readme": f"{GHASP}/ReadMe",
    "ghasp_model": f"{GHASP}/tableb2.dat",
}


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "tau-core-source-audit/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def value(text: str) -> int | None:
    text = text.strip()
    return int(text) if text else None


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    manifest = []
    texts = {}
    for source_id, url in SOURCES.items():
        payload = download(url)
        filename = url.rsplit("/", 1)[-1]
        path = OUT / f"{source_id}_{filename}"
        path.write_bytes(payload)
        text_payload = gzip.decompress(payload) if filename.endswith(".gz") else payload
        texts[source_id] = text_payload.decode("utf-8")
        manifest.append(
            {
                "source_id": source_id,
                "url": url,
                "local_path": str(path.relative_to(ROOT)),
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "source_native": True,
                "endpoint_access": False,
            }
        )

    identity_line = next(line for line in texts["uma_identity"].splitlines() if line[3:10].strip() == "N3726")
    summary_line = next(line for line in texts["uma_summary"].splitlines() if line[3:8].strip() == "N3726")
    ghasp_line = next(line for line in texts["ghasp_model"].splitlines() if line.startswith("UGC 6537"))
    hi_rows = []
    for line in texts["uma_rotation"].splitlines():
        if line[3:8].strip() != "N3726":
            continue
        hi_rows.append(
            {
                "galaxy": "NGC3726",
                "source_name": "N3726",
                "sample": line[0:2].strip(),
                "radius_arcsec": value(line[9:12]),
                "approaching_velocity_km_s": value(line[13:16]),
                "approaching_error_plus_km_s": value(line[17:20]),
                "approaching_error_minus_km_s": value(line[21:24]),
                "receding_velocity_km_s": value(line[25:28]),
                "receding_error_plus_km_s": value(line[29:32]),
                "receding_error_minus_km_s": value(line[33:36]),
                "average_velocity_km_s": value(line[37:40]),
                "inclination_deg": value(line[41:44]),
                "receding_pa_deg": value(line[45:48]),
                "source_url": SOURCES["uma_rotation"],
                "endpoint_access": False,
            }
        )
    if len(hi_rows) != 12:
        raise RuntimeError(f"Expected 12 NGC3726 H I rows, got {len(hi_rows)}")
    with (DATA / "ngc3726_uma_hi_side_rotation_points_v01.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(hi_rows[0]))
        writer.writeheader()
        writer.writerows(hi_rows)

    metadata = {
        "hi_adopted_inclination_deg": value(identity_line[68:70]),
        "hi_adopted_inclination_error_deg": value(identity_line[71:72]),
        "hi_receding_pa_deg": value(identity_line[56:59]),
        "hi_radius_arcmin": float(summary_line[66:70]),
        "hi_last_rotation_radius_arcmin": float(summary_line[71:75]),
        "hi_systemic_velocity_km_s": float(summary_line[34:40]),
        "hi_systemic_velocity_error_km_s": float(summary_line[41:44]),
        "ghasp_systemic_velocity_km_s": value(ghasp_line[18:22]),
        "ghasp_systemic_velocity_error_km_s": value(ghasp_line[23:26]),
        "ghasp_morphological_inclination_deg": value(ghasp_line[27:29]),
        "ghasp_morphological_inclination_error_deg": value(ghasp_line[30:32]),
        "ghasp_kinematic_inclination_deg": value(ghasp_line[33:35]),
        "ghasp_kinematic_inclination_error_deg": value(ghasp_line[36:38]),
        "ghasp_kinematic_pa_deg": value(ghasp_line[72:75]),
        "ghasp_pa_side": ghasp_line[75:76].strip(),
        "ghasp_kinematic_pa_error_deg": value(ghasp_line[77:79]),
    }
    ghasp_receding_pa = (metadata["ghasp_kinematic_pa_deg"] + 180) % 360
    pa_difference = abs(((ghasp_receding_pa - metadata["hi_receding_pa_deg"] + 180) % 360) - 180)
    result = {
        "schema": "ngc3726_uma_hi_rotation_source_v01",
        "status": "NGC3726_SOURCE_NATIVE_HI_SIDE_ROTATION_ACQUIRED_GEOMETRY_COMPATIBLE",
        "galaxy": "NGC3726",
        "hi_source": "Verheijen and Sancisi 2001 WSRT Ursa Major synthesis survey",
        "ghasp_source": "Epinat et al. 2008 GHASP Paper VII",
        "n_hi_rows": len(hi_rows),
        "hi_radius_min_arcsec": min(row["radius_arcsec"] for row in hi_rows),
        "hi_radius_max_arcsec": max(row["radius_arcsec"] for row in hi_rows),
        "metadata": metadata,
        "ghasp_receding_pa_from_side_convention_deg": ghasp_receding_pa,
        "hi_ghasp_receding_pa_difference_deg": pa_difference,
        "selection_uses_vobs_or_residual": False,
        "endpoint_access": False,
        "physical_a_row_constructed": False,
        "claim_boundary": "source-native side curves and geometry only; no tracer comparison, path-channel statistic, SPARC residual, or Tau Core validation",
        "manifest": manifest,
    }
    (DATA / "ngc3726_uma_hi_rotation_source_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    with (DATA / "ngc3726_uma_hi_rotation_source_manifest_v01.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0]))
        writer.writeheader()
        writer.writerows(manifest)
    (REPORTS / "ngc3726_uma_hi_rotation_source_v01.md").write_text(
        f"""# NGC3726 Source-Native H I Side Rotation v0.1

**Status:** `{result['status']}`

The WSRT Ursa Major source provides twelve H I rotation rows from
`{result['hi_radius_min_arcsec']}` to `{result['hi_radius_max_arcsec']}` arcsec,
with approaching/receding values and asymmetric uncertainty columns. GHASP
provides dense Halpha side curves to `156.7` arcsec.

| geometry | H I | Halpha |
| --- | ---: | ---: |
| adopted/kinematic inclination | {metadata['hi_adopted_inclination_deg']} +/- {metadata['hi_adopted_inclination_error_deg']} deg | {metadata['ghasp_kinematic_inclination_deg']} +/- {metadata['ghasp_kinematic_inclination_error_deg']} deg |
| receding position angle | {metadata['hi_receding_pa_deg']} deg | {ghasp_receding_pa} +/- {metadata['ghasp_kinematic_pa_error_deg']} deg |
| systemic velocity | {metadata['hi_systemic_velocity_km_s']} +/- {metadata['hi_systemic_velocity_error_km_s']} km/s | {metadata['ghasp_systemic_velocity_km_s']} +/- {metadata['ghasp_systemic_velocity_error_km_s']} km/s |

The receding-axis difference is `{pa_difference}` degrees, so the side labels
are geometrically compatible. The deprojected velocities are not directly
comparable because the adopted inclinations differ. Any comparison must first
return both curves to line-of-sight equivalents and propagate the geometry
uncertainty. No SPARC velocity or residual was opened.
""",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
