# Paper 8 Foundation Audit

This audit checks whether Paper 8 is ready to serve as a claim-bounded
preparation paper for the morphology-matched forward-readout endpoint.
It does not run a real SPARC matched-family score and does not validate
Tau Core.

## Verdict

- PASS gates: 7
- REVIEW gates: 2
- BLOCKED gates: 1

The package is suitable as a theory-method/reproducibility preparation
paper. It is not yet suitable for an empirical discovery claim because
the residual-blind morphology-label manifest, amplitude policy, accepted
component tables, and real matched-vs-wrong endpoint remain open.

## Gate Results

### paper1_3_local_context

- Status: PASS
- Evidence: local Paper 1-3 manuscripts found
- Required next action: Keep Paper 8 citations pointed to archived Paper 1-3 packages.

### paper3_inverse_to_forward_bridge

- Status: PASS
- Evidence: Paper 3 states required-S_tau is inverse and asks for a frozen predictive gate.
- Required next action: Paper 8 may use Paper 3 as the direct launch point, but must not use required-S_tau as a predictor.

### claim_boundary

- Status: REVIEW
- Evidence: No explicit forbidden-claim list detected.
- Required next action: Keep all empirical wording at protocol/gate status until real matched-family endpoints are run.

### forward_gate_schema_complete

- Status: PASS
- Evidence: 6 schema rows present: residual-blind morphology label, formula-shell selection, geometry and amplitude discipline, matched-vs-wrong family endpoint, shuffled-K null, baseline comparison
- Required next action: Before real endpoint work, materialize every required artifact named in the schema.

### leakage_boundary

- Status: PASS
- Evidence: Crosswalk forbids required S_tau, endpoint residual gain, post-hoc family choice, and residual-selected morphology.
- Required next action: Add the same forbidden-input discipline to any future endpoint-run manifest.

### morphology_family_registry

- Status: PASS
- Evidence: 7 families; statuses: 1D proxy testable, 1D rotation-curve testable, velocity-field preferred
- Required next action: Promote only 1D-testable/proxy families into the first SPARC endpoint; keep m=1/m=2 as velocity-field follow-up.

### formula_shell_dimensional_readiness

- Status: REVIEW
- Evidence: Formula shells expose amplitudes/source terms but do not yet define a unit-normalized amplitude policy.
- Required next action: Write amplitude_policy.csv before empirical scoring; state units and allowed bounds for A_K, R_c, R_d, R_ring, and kernel widths.

### empirical_endpoint_readiness

- Status: BLOCKED
- Evidence: component tables=pending; morphology labels=pending; endpoint=not_yet_run
- Required next action: Do not claim empirical pass. Next concrete work is residual-blind label manifest plus component-table intake.

### arxiv_source_package

- Status: PASS
- Evidence: arxiv_submission_source.zip includes main.tex and refs.bib; compiled PDF excluded.
- Required next action: Optional hardening: include generated .bbl if a submission venue requires bibliography without BibTeX.

### one_command_reproducibility_path

- Status: PASS
- Evidence: README documents python scripts/reproduce.py and compiled PDF exists.
- Required next action: Keep reproduce.py as the authoritative pre-submission command.
