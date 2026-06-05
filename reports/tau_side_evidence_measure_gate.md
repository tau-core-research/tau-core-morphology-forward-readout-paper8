# Tau-Side Evidence-Measure Gate Candidate

This audit builds a residual-blind candidate for `e_gK = E_tau(g,K)`.
It does not score endpoint residuals and does not accept a final
universal normalization law.

## Candidate Measure

```text
E_tau = q_source q_geometry q_projection q_memory q_resolution
```

Accepted source support is normalized to 1. Missing source support is
set to 0. Proxy/partial support is evaluated by the product measure.
The current proxy ladder is the conservative readout-admission ladder:
`strong proxy = 0.85`, `ordinary proxy = 0.70`, and the standard
proxy template gives `0.70 * 0.70 * 0.85 * 0.85 = 0.354025`.

## Factor-Status Discipline

The numerical product is accompanied by per-factor derivation labels.
Accepted and missing gates are definition-derived limit cases. The
proxy ladder is derived inside the current conservative three-status
readout-admission geometry. Individual proxy rows remain
theory-candidate factor geometry / source-readout assignments until their source,
geometry, projection, memory, and resolution factors are accepted
residual-blind observables.

## Full-Sample Verdict

- Components audited: 406
- Proxy components: 105
- Median proxy E_tau: 0.354025
- Mean proxy E_tau: 0.335798
- Median proxy minus fixed 0.35: 0.004025

## Summary

| split | n_components | n_proxy_components | median_e_tau_all_components | median_e_tau_proxy_components | mean_e_tau_proxy_components | median_proxy_minus_fixed_0p35 | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| all | 406 | 105 | 1 | 0.354025 | 0.335798 | 0.004025 | tau_side_evidence_measure_gate_candidate_not_endpoint |
| holdout | 107 | 28 | 1 | 0.354025 | 0.328328 | 0.004025 | tau_side_evidence_measure_gate_candidate_not_endpoint |
| train | 299 | 77 | 1 | 0.354025 | 0.338514 | 0.004025 | tau_side_evidence_measure_gate_candidate_not_endpoint |

## Claim Boundary

This is the first executable E_tau candidate. It shows how the fixed
proxy gate can be replaced by a source-evidence product whose median
proxy value reproduces the old 0.35 gate as a coarse-grid consequence.
The numerical ladder is derived inside the conservative
readout-admission geometry, while the galaxy/component q_i assignments
must still be frozen from source/readout evidence before endpoint use
and must not be selected from rotation residuals.
