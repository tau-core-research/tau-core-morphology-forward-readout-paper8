#!/usr/bin/env python3
"""One-command reproduction check for the Paper 8 public package."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper8_submission_source"


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("$ " + " ".join(cmd) + f"  # cwd={cwd}")
    subprocess.run(cmd, cwd=cwd, check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    run([sys.executable, "scripts/generate_paper8_artifacts.py"])
    run([sys.executable, "scripts/audit_paper8_foundations.py"])
    run([sys.executable, "scripts/run_available_morphology_readout_pilot.py"])
    run([sys.executable, "scripts/build_morphology_parameter_manifest.py"])
    run([sys.executable, "scripts/run_morphology_matched_proxy_endpoint.py"])
    run([sys.executable, "scripts/run_morphology_formula_shell_proxy_endpoint.py"])
    run([sys.executable, "scripts/run_source_native_readout_formula_endpoint.py"])
    run([sys.executable, "scripts/run_manifest_confidence_diagnostics.py"])
    run([sys.executable, "scripts/run_amplitude_policy_diagnostics.py"])
    run([sys.executable, "scripts/run_amplitude_shrinkage_path.py"])
    run([sys.executable, "scripts/run_train_selected_shrinkage_diagnostic.py"])
    if shutil.which("tectonic") is None:
        raise SystemExit("tectonic is required to compile paper8_submission_source/main.tex")
    run(["tectonic", "main.tex"], cwd=SOURCE)
    run([sys.executable, "scripts/build_arxiv_source.py"])
    run([sys.executable, "-m", "pytest", "-q"])
    print(f"paper8_pdf_sha256: {sha256(SOURCE / 'main.pdf')}")
    print("PAPER8_MORPHOLOGY_FORWARD_READOUT_REPRODUCTION_COMPLETE")


if __name__ == "__main__":
    main()
