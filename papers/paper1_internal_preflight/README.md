# Paper 1: Internal Preflight

This lane contains the manuscript source and arXiv package for the first
operational paper.

## Scope

Paper 1 frames the Tau Core morphology-matched forward-readout programme as a
reproducible internal-preflight signal.  It emphasizes leakage prevention,
matched-vs-wrong family tests, shuffled-label controls, source ledgers, and
claim-boundary discipline.

It should not claim discovery of a new gravitational law or population-level
validation of Tau Core.

## Contents

- `source/main.tex`
- `source/refs.bib`
- `source/main.pdf`
- `source/figures/`
- `arxiv_source.zip`

## Build Compatibility

The historical top-level path `paper8_submission_source/` is kept as a symlink
to `source/`, and `arxiv_submission_source.zip` is kept as a symlink to
`arxiv_source.zip`.

Existing commands still work:

```bash
python scripts/reproduce.py
python scripts/build_arxiv_source.py
```
