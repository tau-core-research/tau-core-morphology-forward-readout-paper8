import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper8_submission_source"
DATA = ROOT / "data" / "derived"


def test_publication_files_exist():
    required = [
        ROOT / "README.md",
        ROOT / "docs" / "tau_core_gravity_bridge_central.md",
        ROOT / "LICENSE",
        ROOT / "CITATION.cff",
        ROOT / "DATA_NOTICE.md",
        ROOT / "requirements.txt",
        SOURCE / "main.tex",
        SOURCE / "refs.bib",
        SOURCE / "main.pdf",
        SOURCE / "figures",
        ROOT / "figures",
        ROOT / "scripts/reproduce.py",
        ROOT / "scripts/generate_paper8_artifacts.py",
        ROOT / "scripts/audit_paper8_foundations.py",
        ROOT / "scripts/run_source_native_readout_formula_endpoint.py",
        ROOT / "scripts/run_source_native_carrier_robustness.py",
        ROOT / "arxiv_submission_source.zip",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert not missing


def test_paper1_source_boundary_is_explicit():
    reproduce = (ROOT / "scripts" / "reproduce.py").read_text(encoding="utf-8")
    assert "Paper 9 repository" in reproduce
    assert "PAPER8_INTERNAL_PREFLIGHT_REPRODUCTION_COMPLETE" in reproduce
    assert "build_arxiv_projection_enriched_source.py" not in reproduce


def test_headline_artifacts_are_present():
    required = [
        DATA / "source_native_readout_formula_endpoint_summary.csv",
        DATA / "source_native_readout_formula_robustness_summary.csv",
        DATA / "source_native_carrier_robustness_summary.csv",
        DATA / "accepted_morphology_manifest.csv",
        DATA / "narrow_accepted_exponential_disk_population_endpoint_summary.csv",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert not missing

    summary = pd.read_csv(DATA / "source_native_readout_formula_endpoint_summary.csv")
    assert not summary.empty


def test_arxiv_source_package_contains_latex_sources():
    zip_path = ROOT / "arxiv_submission_source.zip"
    assert zip_path.exists()
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "main.pdf" not in names
