# Paper 8 Readiness Upgrade Audit

This audit summarizes the preparation state after the source-native
formula, shrinkage, quality-gate, shuffled-null, decision-matrix, and
predeclaration diagnostics. It does not claim empirical validation.

## Status Counts

- blocked: 1
- diagnostic_ready: 3
- not_started: 1
- predeclaration_ready: 1
- ready: 2
- ready_for_modeling_triage: 1

## Readiness Rows

| readiness_layer | status | evidence | next_action |
| --- | --- | --- | --- |
| paper1_3_inheritance | ready | Paper 1-3 bridge path is explicit in manuscript and foundation audit. | Keep citations and claim boundary stable. |
| source_native_formula_preflight | diagnostic_ready | Concrete bridge formula kernels run on 175-galaxy proxy manifest; holdout matched-vs-wrong signal exists but baseline superiority is not claimed. | Replace proxy manifest with accepted residual-blind morphology observables. |
| amplitude_policy | diagnostic_ready | Train-only shrinkage selection chooses family_weight=0.40 and transfers to holdout. | Derive or justify Tau-side source normalization instead of treating shrinkage as physical law. |
| family_failure_map | ready_for_modeling_triage | Family breakdown and observable-quality diagnostics identify quality-limited and current-best-case rows. | Prioritize morphology-observable extraction for quality-limited families. |
| quality_gate_controls | diagnostic_ready | Predeclared quality gates and shuffled-family nulls expose baseline-vs-null-power tradeoff. | Predeclare the gate before any future endpoint scoring. |
| primary_endpoint_candidate | predeclaration_ready | no_low_inclination is current primary candidate: n=35, matched-vs-wrong=0.857, TPG/v6=0.514, MOND=0.657, p_beats=0.0410, p_mean=0.0110. | Freeze this as a candidate endpoint lane only if the next run uses the same predeclared rule. |
| predeclared_endpoint_protocol | ready | 11 protocol rows record lanes, metrics, forbidden inputs, and caveated-row handling. | Use the protocol as the next-run guardrail. |
| empirical_discovery_claim | blocked | Current outputs are preparation diagnostics on available-data proxies, not a final external endpoint. | Do not claim Tau Core validation or baseline replacement. |
| final_paper8_manuscript | not_started | Repository currently contains a proposal/preparation manuscript, not a full empirical Paper 8. | After accepted morphology observables and predeclared endpoint run, write final results paper. |

## Verdict

Paper 8 is now preparation-ready as a claim-bounded protocol and
diagnostic package. It is not discovery-ready. The next scientific
upgrade is to replace available-data proxy morphology observables with
accepted residual-blind morphology inputs, then run the predeclared
endpoint protocol without changing gates after seeing scores.
