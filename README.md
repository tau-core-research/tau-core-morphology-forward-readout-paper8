# Paper 8: Tau Core Morphology-Matched Forward Readout Gate

This repository is the public reproducibility package for:

**Morphology-matched forward readout gates for Tau Core gravity: extending SPARC residual Papers 1-3 from inverse diagnostics to predeclared family tests**

The package is intentionally small. It contains only the files needed to
compile the manuscript, regenerate compact protocol tables and figures, build
the arXiv-oriented source package, and verify the publication-facing claim
boundary.

## Main Claim

The publication-facing claim is deliberately narrow:

```text
The Tau Core gravity bridge can sharpen SPARC residual Papers 1-3 by turning
the Paper 3 inverse required-S_tau diagnostic into a morphology-matched
forward-readout gate with matched-family, wrong-family, shuffled-label, and
standard-baseline controls.
```

The key endpoint proposed by the paper is:

```text
MORPHOLOGY-MATCHED-FORWARD-READOUT-GATE
```

with pass condition:

```text
For predeclared candidates and controls, the morphology-matched Tau Core
readout family improves residual structure more than wrong morphology
families, shuffled morphology labels, Newtonian baryonic, MOND-simple, and
empirical RAR baselines.
```

## Does Not Claim

This paper does **not** claim:

```text
Tau Core is proven.
The real SPARC matched-family endpoint has already passed.
Tau Core fits all galaxies better than MOND/RAR/Newtonian baselines.
MOND, RAR, or Newtonian baryonic baselines have been superseded.
A universal weak-field galaxy law has been derived.
Non-axisymmetric bar/lopsided families are fully testable from 1D curves alone.
```

## Theory Context

The broader Tau Core theory and gravity bridge architecture are maintained
separately at:

```text
https://github.com/tau-core-research/tau-core-theory
```

The most relevant local theory entrypoint is:

```text
docs/tau_core_gravity_bridge_central.md
```

in this repository. It is the local bridge single-source-of-truth for the
Paper 8 morphology-layer discipline. In particular, it separates the observed
4D morphology handle `K_obs` from the readout-relevant proxy `K_readout` used
to select a formula shell.

This Paper 8 repository is standalone. It does not require accepting Tau Core
as a completed physical theory.

## Current Endpoint Exemplars

The repository now contains a small set of claim-bounded single-galaxy endpoint
or control exemplars. These are useful because they show that the residual-blind
source-review to freeze to scoring workflow is executable, but they do not by
themselves establish population validation.

Current examples:

```text
NGC5907:
    accepted mixed projection-control endpoint
    beats Newtonian, TPG/v6, MOND, and wrong-family controls in its
    frozen single-galaxy lane

NGC7331:
    caveated accepted mixed vertical/outer-warp endpoint
    scored with the broad-window caveat preserved

NGC4183:
    accepted null-control interval endpoint
    built from an independently reviewed weak-projection tilted-ring source,
    frozen as an interval rather than a residual-tuned point fit
    better than MOND and slightly better than TPG/v6 on this artifact,
    but not stronger than the simple exponential-disk carrier baseline

Narrow accepted exponential-disk population lane:
    first population-level matched-family accepted endpoint in the repo
    restricted to 13 externally audited K_exponential_disk rows with accepted scale radii
    uses the frozen train-only exponential-disk amplitude, not a pool refit
    better than MOND on average, but still slightly worse than TPG/v6 on average
    does not unblock the full 175-row accepted launch

NGC4088:
    caveated accepted warp-history endpoint
    operationally useful, but still carries explicit law-level caveats
```

The correct reading is narrow:

```text
These are single-galaxy predeclared endpoints or controls.
Together with the narrow accepted exponential-disk population lane, they strengthen the paper's operational and methodological case.
They do not yet authorize a claim that Tau Core beats all baselines in general,
nor do they replace the blocked population-level accepted-observable launch.
```

## Relation To Papers 1-3

Paper 1:

```text
Residual-blind external disturbance labels are associated with increased
low-acceleration residual scatter.
```

Paper 2:

```text
Residual-shape features can infer external disturbance labels better than
shuffled labels, while MOND/RAR-like baselines remain important comparators.
```

Paper 3:

```text
Candidate/control framework plus inverse required-S_tau diagnostic.
```

Paper 8:

```text
Forward morphology-matched readout gate:
K_obs -> K_readout -> formula shell -> delta_g^K -> matched-vs-wrong/shuffled endpoint.
```

## Main Files

```text
LICENSE
CITATION.cff
DATA_NOTICE.md
requirements.txt
README.md
paper8_submission_source/main.tex
paper8_submission_source/refs.bib
paper8_submission_source/main.pdf
paper8_submission_source/figures/
figures/
data/derived/
scripts/generate_paper8_artifacts.py
scripts/build_arxiv_source.py
scripts/reproduce.py
tests/test_public_reproducibility_package.py
arxiv_submission_source.zip
```

## Included Data

The package includes compact derived protocol artifacts:

```text
data/derived/morphology_family_registry.csv
data/derived/paper3_candidate_control_crosswalk.csv
data/derived/forward_readout_gate_schema.csv
data/derived/synthetic_forward_gate_demo.csv
data/derived/paper8_readiness_table.csv
```

These are protocol fixtures and claim-boundary artifacts. They are not raw
SPARC data and not an empirical matched-family endpoint result.

## Reproduce

Create an environment with Python 3.10 or newer, then install the lightweight
dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the one-command reproduction check:

```bash
python scripts/reproduce.py
```

This regenerates the derived tables and figures, compiles
`paper8_submission_source/main.tex` with `tectonic`, builds the arXiv source
ZIP, runs the foundation audit, and runs the public package tests.

## Foundation Audit

The preparation checks for the Paper 8 basis are generated by:

```bash
python scripts/audit_paper8_foundations.py
```

This writes:

```text
data/derived/paper8_foundation_audit.csv
reports/paper8_foundation_audit.md
```

The audit checks the Paper 1-3 inheritance, the Paper 3 inverse-to-forward
bridge, leakage boundaries, family registry readiness, arXiv package status,
and the remaining blockers before any empirical matched-family endpoint can be
claimed.

## Available-Data Morphology Readout Pilot

The currently available empirical-prep check is generated by:

```bash
python scripts/run_available_morphology_readout_pilot.py
```

This writes:

```text
data/derived/available_data_morphology_readout_availability.csv
data/derived/available_data_wide_fixed_tpg_proxy_summary.csv
data/derived/available_data_wide_fixed_tpg_proxy_ranks.csv
data/derived/available_data_wide_fixed_tpg_proxy_rank_summary.csv
data/derived/available_data_morphology_decomposition_holdout.csv
data/derived/available_data_morphology_decomposition_summary.csv
data/derived/available_data_full_sparc_tau_proxy_galaxies.csv
data/derived/available_data_full_sparc_tau_proxy_overall.csv
data/derived/available_data_full_sparc_tau_proxy_by_type.csv
data/derived/available_data_paper1_73_galaxy_baseline_pivot.csv
data/derived/available_data_paper1_73_galaxy_tau_baseline_summary.csv
data/derived/available_data_paper1_73_galaxy_tau_baseline_by_class.csv
data/derived/available_data_limited_rmond_gallery.csv
reports/available_morphology_readout_pilot.md
```

This pilot is intentionally claim-bounded. It checks existing local proxy data
for Tau-like/FixedTPG behavior against available TPG/v6, Newtonian, MOND, RAR,
and limited RMOND/MOND comparators. The largest current layer is a 175-galaxy
Tau-proxy versus TPG/MOND check; the full Newtonian/RAR layer is smaller and
comes from the Paper 1 A/B/C packet. This does not replace the final Paper 8
endpoint, because residual-blind morphology-family labels and scored per-family
`delta_g^K` tables are still pending.

## Morphology-Matched Tau-Proxy Endpoint

## Morphology Parameter Manifest

The current residual-blind morphology parameter manifest is generated by:

```bash
python scripts/build_morphology_parameter_manifest.py
```

This writes:

```text
data/derived/morphology_parameter_manifest.csv
data/derived/morphology_parameter_manifest_family_counts.csv
data/derived/morphology_parameter_manifest_confidence_summary.csv
reports/morphology_parameter_manifest.md
```

The manifest freezes the available-data morphology family, scale-radius,
tail-cutoff, compact-support, and thickness proxies for each galaxy. It is the
declared input table consumed by the source-native bridge readout formula
endpoint. It is still a proxy manifest, not the final hand-curated morphology
catalog.

## Morphology-Matched Tau-Proxy Endpoint

The first direct check of the matched-family idea is generated by:

```bash
python scripts/run_morphology_matched_proxy_endpoint.py
```

This writes:

```text
data/derived/morphology_labels_predeclared_proxy.csv
data/derived/morphology_matched_proxy_family_betas.csv
data/derived/morphology_matched_proxy_scores_by_galaxy.csv
data/derived/morphology_matched_proxy_endpoint_summary.csv
data/derived/morphology_matched_proxy_endpoint_by_family.csv
data/derived/morphology_matched_proxy_shuffled_null.csv
data/derived/morphology_matched_proxy_shuffled_null_summary.csv
reports/morphology_matched_tau_proxy_endpoint.md
```

This endpoint is closer to the Paper 8 target than the generic Tau-proxy
runner: each galaxy receives a metadata-proxy morphology label, a family
amplitude is fit on the train split only, and holdout galaxies are scored with
their matched family against wrong families, shuffled morphology labels,
TPG/v6, and MOND. It is still not the final endpoint because the family
functions are built from the available `rparent_cd` channel, not from the final
morphology-specific 4D readout formula shells.

## Morphology Formula-Shell Proxy Endpoint

The next available-data preflight is generated by:

```bash
python scripts/run_morphology_formula_shell_proxy_endpoint.py
```

This writes:

```text
data/derived/morphology_formula_shell_proxy_labels.csv
data/derived/morphology_formula_shell_proxy_amplitudes.csv
data/derived/morphology_formula_shell_proxy_scores_by_galaxy.csv
data/derived/morphology_formula_shell_proxy_endpoint_summary.csv
data/derived/morphology_formula_shell_proxy_endpoint_by_family.csv
data/derived/morphology_formula_shell_proxy_shuffled_null.csv
data/derived/morphology_formula_shell_proxy_shuffled_null_summary.csv
reports/morphology_formula_shell_proxy_endpoint.md
```

This endpoint assigns different predeclared radial shell proxies to different
morphology classes. The current holdout result is weaker than the
single-channel matched Tau-proxy result, which is preserved as a negative
preflight finding: naive available-data shell shapes are not enough to produce
a strong morphology-specific endpoint. The final Paper 8 endpoint still needs
source-native morphology labels, audited 4D readout shells, dimensional checks,
and a stronger amplitude policy.

## Source-Native Bridge Readout Formula Endpoint

The bridge-formula preflight is generated by:

```bash
python scripts/run_source_native_readout_formula_endpoint.py
```

This writes:

```text
data/derived/source_native_readout_formula_labels.csv
data/derived/source_native_readout_formula_amplitudes.csv
data/derived/source_native_readout_formula_scores_by_galaxy.csv
data/derived/source_native_readout_formula_endpoint_summary.csv
data/derived/source_native_readout_formula_endpoint_by_family.csv
data/derived/source_native_readout_formula_shuffled_null.csv
data/derived/source_native_readout_formula_shuffled_null_summary.csv
reports/source_native_readout_formula_endpoint.md
```

Unlike the naive shell-proxy endpoint, this preflight consumes the declared
morphology parameter manifest and evaluates the concrete Tau Core bridge
formulas as `delta v^2` readout kernels: scale-tail `n=2`, finite exponential
disk Freeman/Bessel kernel, compact finite-source exterior response, and
thick/flared damped vertical-kernel response. The current holdout result gives
a strong matched-vs-wrong morphology-specific signal, but does not beat TPG/v6
or MOND on average. This is preserved as a claim-bounded preparation result:
it supports formula-family specificity, not empirical validation.

## Readout-Mixture Proxy Diagnostic

The readout-mixture proxy diagnostic is generated by:

```bash
python scripts/run_readout_mixture_proxy_endpoint.py
```

This writes:

```text
data/derived/readout_mixture_proxy_weights.csv
data/derived/readout_mixture_proxy_scores_by_galaxy.csv
data/derived/readout_mixture_proxy_endpoint_summary.csv
reports/readout_mixture_proxy_endpoint.md
```

This diagnostic keeps the same concrete bridge formula kernels, but replaces
hard `one galaxy = one family` selection with a residual-blind available-data
proxy mixture over readout components. The current holdout result is negative:
the mixture beats the hard matched family in only `0.455` of galaxies, beats
TPG/v6 in `0.500`, and beats MOND in `0.455`. This is preserved as a useful
failure map. It shows that a mixture layer is not automatically stronger; its
weights must be sourced from accepted residual-blind morphology-memory/readout
observables rather than coarse 4D proxy heuristics.

## Readout-State Vector Intake Gate

The readout-state vector intake schema and gap audit are generated by:

```bash
python scripts/build_readout_state_vector_intake_schema.py
```

This writes:

```text
data/derived/readout_state_vector_intake_schema.csv
data/derived/readout_state_vector_gap_audit.csv
data/derived/readout_state_vector_gap_summary.csv
reports/readout_state_vector_intake_schema.md
```

This gate converts the negative mixture result into an operational next-data
requirement. It asks which residual-blind source observables are needed before
the mixture weights can be promoted into an accepted Tau-side readout-state
vector. The current answer is deliberately blocking: no component is endpoint
ready under the strict accepted-input rule, the morphology-memory layer remains
proxy-only, and the amplitude normalization rule is still missing. This is not
an endpoint score; it is the source-observable checklist for the next run.

## Manifest Confidence Diagnostics

The manifest-quality diagnostic is generated by:

```bash
python scripts/run_manifest_confidence_diagnostics.py
```

This writes:

```text
data/derived/manifest_confidence_diagnostics_summary.csv
data/derived/manifest_confidence_diagnostics_shuffled.csv
reports/manifest_confidence_diagnostics.md
```

This diagnostic asks whether the source-native bridge formula endpoint improves
when restricted to higher-confidence morphology-parameter manifest subsets. In
the current preflight, higher-confidence subsets preserve the strong
matched-vs-wrong signal, but do not by themselves produce a stable TPG/MOND
baseline win. Removing low-inclination or large-distance-error cases improves
some baseline comparisons, so data quality matters, but amplitude policy and
source-native morphology observables remain central blockers.

## Baseline Success Morphology Audit

The baseline-success morphology audit is generated by:

```bash
python scripts/audit_baseline_success_morphology.py
```

This writes:

```text
data/derived/baseline_success_morphology_audit.csv
data/derived/baseline_success_morphology_summary.csv
data/derived/baseline_success_morphology_by_family.csv
data/derived/baseline_success_conventional_available_audit.csv
data/derived/baseline_success_conventional_available_summary.csv
reports/baseline_success_morphology_audit.md
```

This diagnostic asks the control-side question: if TPG/MOND/Newton/RAR already
fit a galaxy well, what morphology/readout regime might that indicate? In the
current holdout split, TPG/v6 wins concentrate in scale-tail/irregular rows and
have `0.000` current-proxy/readout-memory match fraction, suggesting a possible
smooth closure-like or memory-integrated readout regime. Tau-matched wins have
higher current-readout consistency, while MOND wins are compatible with simpler
radial low-acceleration or diffuse-disk scaling regimes. Where Newtonian wins
in the smaller conventional tables, the claim-safe Tau Core reading is a quiet
or regular baryonic-readout regime, not a universal failure of morphology
specificity.

The control interpretation is:

```text
Newtonian good fit
  -> present-day and history/readout may both be regular or baryonic-dominated;
     a strong Tau residual should not be forced.

MOND/RAR good fit
  -> the readout may scalarize into a simple radial low-acceleration law;
     morphology dependence may be weak or effectively averaged.

TPG good fit
  -> the object may live in a smooth closure-like or memory-integrated readout
     regime; present-day morphology can be a poor direct proxy for K_readout.

Tau matched-family good fit
  -> the current morphology proxy may be closer to the readout-relevant state,
     so family-specific structure is visible in the rotation endpoint.
```

This makes baseline success scientifically useful: it marks control regimes
that the final Tau Core paper should predeclare rather than discard.

The stronger theoretical reading is a conditional limiting-regime claim, not a
baseline-superiority claim. If the Tau-side morphology/readout state satisfies
the regime conditions under which a historical baseline is strong, the baseline
should arise naturally as an effective 4D readout approximation:

```text
Newtonian limit
  Conditions: K_readout is quiet/current-regular, alpha_tau is small, the
  quotient-visible morphology residual is suppressed, and the baryonic
  weak-field closure is stable.
  Tau Core reading: g_eff -> g_Newt. Newtonian success is expected.

MOND/RAR-like limit
  Conditions: the morphology residual scalarizes into an almost radial
  low-acceleration response, family structure is averaged or weak, and a
  source-normalization scale is supplied by Tau-side closure/readout data.
  Tau Core reading: a MOND/RAR-like radial law can appear as a special
  scalarized solved response.

TPG-like limit
  Conditions: the residual is best represented as a smooth closure/readout
  defect, often memory-integrated, and the solved response has an outer
  logarithmic or near-flat-speed branch.
  Tau Core reading: a classical TPG-like formula can appear as a special
  closure-solved branch rather than as an inserted force law.

RMOND-facing limit
  Conditions: the same residual descends through a metric-compatible,
  gauge-safe weak-field readout map.
  Tau Core reading: the branch becomes RMOND-facing, meaning suitable for a
  relativistic/metric audit, not yet a derived relativistic MOND theory.
```

This is the bridge consequence to test: where a baseline is strong, Tau Core
should explain why that baseline is the appropriate effective readout limit for
that galaxy's readout state. Where a morphology-matched Tau family is strong,
the current morphology proxy may be closer to the active `K_readout`. Where a
wrong family or shuffled label is strong, the case remains a failure map.

The theory bridge now imports a stricter formula-status ladder into Paper 8:

```text
Newtonian limit
  Status: FORMULA-DERIVED.
  Reason: if the quotient-visible morphology residual is suppressed,
  delta_g_morph -> 0 and g_eff -> g_Newt.

TPG-like shape
  Status: FORMULA-DERIVED under the n=2 source-tail gate.
  Reason: sigma_morph ~ A/r^2 implies delta_g ~ A/r and
  delta Phi ~ A log r.

Fixed historical TPG branch
  Status: FORMULA-CONDITIONAL.
  Reason: the log-like readout shape is derived, but the finite-load
  constants, branch choice, and historical normalization still require
  additional Tau-side closure/readout input.

MOND/RAR-like scaling
  Status: FORMULA-CONDITIONAL.
  Reason: A^2 = G M_b g_* implies delta_g = sqrt(g_N g_*), but this is a
  Tau Core derivation only if g_* is supplied internally.

RMOND-facing branch
  Status: READOUT-FORM-ONLY.
  Reason: the weak-field readout can be metric-audit-ready, but no covariant
  relativistic field equation, conservation law, or lensing sector is derived
  in this paper.
```

The internal-scale construction used by the amplitude gate is:

```text
g_* := lambda_* ell_*
[lambda_*] = T^-2
[ell_*] = L
```

Here `lambda_*` is a residual-blind Tau-side closure/readout stiffness and
`ell_*` is an admissible readout length. This gives an internal acceleration
scale object by dimensional construction, but it is not a numerical `a0`
validation, not a universal MOND-scale derivation, and not an empirical
baseline-superiority claim.

The baseline-selection theorem used by the paper is conditional:

```text
CONDITIONAL-BASELINE-SELECTION-THEOREM

Assume a galaxy has a residual-blind readout-regime label R_g assigned before
rotation endpoint scoring.

If R_g satisfies the quiet baryonic-readout conditions, then the Tau Core
effective readout reduces to the Newtonian limit.

If R_g satisfies the scalarized radial low-acceleration conditions and an
internal g_* = lambda_* ell_* scale has been supplied, then the Tau Core
effective readout has a MOND/RAR-like solved-response branch.

If R_g satisfies the smooth closure/readout source-tail conditions, especially
the n=2 tail sigma_morph ~ A/r^2, then the Tau Core effective readout has a
TPG-like logarithmic / near-flat-speed branch.

If R_g satisfies the gauge-safe metric-readout descent conditions, then the
same residual becomes RMOND-facing, but only as a weak-field readout form.
```

Thus the bridge can explain why a particular baseline is expected to be good
only when the corresponding regime label is fixed in advance. If multiple
regime predicates hold, the case is not a unique proof of one baseline; it is
an overlap/control regime. If no predicate holds, baseline success is not
explained by the current bridge and must remain a failure map.

## Morphology Information Gain Test

The next endpoint direction is not to write a high-dimensional full morphology
model for every galaxy. That would likely fail from missing or heterogeneous
source data. The claim-safe direction is an information-gain test:

```text
As residual-blind morphology/readout information improves, the predeclared Tau
Core forward readout should improve in a systematic way.
```

The proposed information levels are:

```text
Level 0: coarse K_obs label
    e.g. exponential disk, compact, scale-tail, thick/flared.

Level 1: source-reviewed K_readout
    projection caveats, memory/history caveats, bar/core overlays.

Level 2: low-dimensional readout-state vector
    q_tail, q_compact, q_thick, q_bar, q_memory, q_regular.

Level 3: source-native scales and amplitudes
    disk scale, HI/tail radius, compact-core radius, flare support, bar length,
    and residual-blind closure/readout normalization.

Level 4: richer morphology/kinematic data
    velocity fields, HI maps, decompositions, and history indicators.
```

Pass condition:

```text
Adding residual-blind morphology/readout information improves at least one
predeclared endpoint in the expected direction:
    matched-vs-wrong family rank,
    shuffled-label separation,
    residual RMS,
    baseline competitiveness,
    or readout-regime classification.
```

Fail condition:

```text
More morphology/readout information does not improve prediction,
or the improvement appears only when rotation residuals are used to choose
labels, weights, scales, or gates.
```

This is stronger than a single best-fit comparison. It asks whether the Tau
Core bridge becomes more predictive as the observed morphology proxy is refined
toward the readout-relevant morphology state.

The first executable preflight is generated by:

```bash
python scripts/run_morphology_information_gain_test.py
```

This writes:

```text
data/derived/morphology_information_gain_level_manifest.csv
data/derived/morphology_information_gain_scores_by_galaxy.csv
data/derived/morphology_information_gain_summary.csv
data/derived/morphology_information_gain_transitions.csv
data/derived/morphology_information_gain_data_acquisition.csv
reports/morphology_information_gain_test.md
```

Current holdout reading:

```text
L0 -> L1:
    improves family specificity strongly
    but does not improve raw RMSE yet.

L1 -> L2:
    current readout-state mixture proxy is mixed/negative.
    This supports the accepted-observable gate: mixture weights need real
    morphology-memory/source observables, not coarse present-day proxies.

L2 -> L3:
    train-selected normalization improves the proxy mixture layer.
```

Data acquisition status for this preflight:

```text
SPARC:      175/175 master rows acquired.
S4G:        75 scale-radius candidates acquired.
DustPedia: 31 full-sample source-candidate matches.
HI:         171 full-sample SPARC HI-ready galaxies.
PHANGS:     2 full-sample public-sample matches, but 0 MUSE-ready velocity-field matches.
L2 tail:    172 source candidates.
L2 compact: 48 source candidates.
L2 bar:     19 source candidates.
L2 weights: 0 endpoint-ready accepted readout-state components.
```

This result is not monotonicity proof. It is the first executable failure map
for the morphology-information-gain hypothesis.

The full-sample source expansion is generated by:

```bash
python scripts/build_morphology_information_gain_source_expansion.py
```

This writes:

```text
data/derived/morphology_information_gain_source_expansion.csv
data/derived/morphology_information_gain_dustpedia_matches.csv
data/derived/morphology_information_gain_source_expansion_summary.csv
reports/morphology_information_gain_source_expansion.md
```

The expansion is an acquisition layer only. It does not promote morphology
labels, does not assign accepted mixture weights, and does not score rotations.

The first L2 weight-intake preflight is generated by:

```bash
python scripts/build_l2_weight_intake_candidates.py
```

This writes:

```text
data/derived/morphology_information_gain_l2_weight_intake_candidates.csv
data/derived/morphology_information_gain_l2_weight_intake_summary.csv
reports/morphology_information_gain_l2_weight_intake.md
```

Current full-sample reading:

```text
Source-informative L2 weight candidates: 174/175.
Uninformative equal fallbacks:          1/175.
Tail nonzero candidates:                172.
Exponential-disk nonzero candidates:    75.
Compact nonzero candidates:             48.
Thick/flared nonzero candidates:        107.
```

These are not accepted Tau-side readout-state weights and not endpoint scores.
They are residual-blind intake candidates that separate the present projected
4D morphology handle from a more detailed readout-state vector. Endpoint use
requires a separate freeze-and-audit step.

The endpoint stress test of these intake candidates is generated by:

```bash
python scripts/run_l2_weight_intake_endpoint_preflight.py
```

This writes:

```text
data/derived/morphology_information_gain_l2_weight_intake_endpoint_scores.csv
data/derived/morphology_information_gain_l2_weight_intake_endpoint_summary.csv
data/derived/morphology_information_gain_l2_weight_intake_endpoint_by_family.csv
reports/morphology_information_gain_l2_weight_intake_endpoint_preflight.md
```

Current holdout reading:

```text
Beats old L2 mixture proxy:       0.409
Beats hard source-native family:  0.409
Beats TPG/v6:                    0.477
Beats MOND:                      0.432
Median intake-minus-old-L2 RMSE: +0.847
```

This is a preserved negative/mixed result. The source-intake layer is broader
and more residual-blind than the old mixture proxy, but it is not yet a better
endpoint predictor. By dominant intake family, the thick/flared channel is the
cleanest current positive hint, while compact and several tail/exponential
cases remain weak. This points to a freeze-and-audit step for source-native
weights and morphology-memory/projection observables before endpoint use.

The freeze-readiness audit for these weights is generated by:

```bash
python scripts/audit_l2_weight_freeze_readiness.py
```

This writes:

```text
data/derived/morphology_information_gain_l2_weight_freeze_readiness.csv
data/derived/morphology_information_gain_l2_weight_freeze_component_audit.csv
data/derived/morphology_information_gain_l2_weight_freeze_readiness_summary.csv
reports/morphology_information_gain_l2_weight_freeze_readiness.md
```

The source-native orientation promotion gate is generated by:

```bash
python scripts/build_source_native_orientation_promotion_gate.py
```

This writes:

```text
data/derived/source_native_orientation_family_gate.csv
data/derived/source_native_orientation_component_gate.csv
data/derived/source_native_orientation_galaxy_gate.csv
data/derived/source_native_orientation_promotion_summary.csv
reports/source_native_orientation_promotion_gate.md
```

Current source-native orientation status:

```text
Family orientations promoted:       3/4.
Family orientations blocked:        1/4.
Active components promoted:         295/406.
Active components blocked:          111/406.
Galaxies orientation-ready:         67/175.
Galaxies orientation-blocked:       108/175.
```

This is not endpoint scoring. It promotes compact, scale-tail, and exponential
orientation signs from source-native family evidence, while keeping the
thick/flared sign blocked because the required velocity-field/vertical source
layer is not yet available.

The memory/projection acceptance gate is generated by:

```bash
python scripts/build_memory_projection_acceptance_gate.py
```

This writes:

```text
data/derived/memory_projection_acceptance_gate.csv
data/derived/memory_projection_acceptance_summary.csv
reports/memory_projection_acceptance_gate.md
```

Current memory/projection status:

```text
Orientation-ready:                         67/175.
Projection-ready:                          71/175.
Memory ready or not required:              4/175.
Memory/projection ready candidates:        1/175.
Blocked by orientation:                    108/175.
Blocked by projection after orientation:   47/175.
Blocked by memory/history after projection: 19/175.
```

The existing memory/history proxy is still useful for triage, but it is not an
accepted memory/history observable because part of it is rotation-inferred.

To increase usable coverage without weakening the strict claim boundary, the
inclusion-lane expansion audit is generated by:

```bash
python scripts/build_inclusion_lane_expansion_audit.py
```

This writes:

```text
data/derived/inclusion_lane_expansion_audit.csv
data/derived/inclusion_lane_expansion_summary.csv
reports/inclusion_lane_expansion_audit.md
```

Current inclusion-lane status:

```text
Strict-ready candidates:                 1/175.
Caution/proxy-supported rows:           66/175.
Analysis-includable strict+caution rows: 67/175.
Acquisition-required rows:              108/175.
Rows needing orientation source evidence: 108/175.
Rows needing projection/scale review:    104/175.
Rows needing memory/history source review: 171/175.
```

The caution lane is not accepted evidence and cannot support endpoint
validation. It is a support/sensitivity lane that keeps orientation-ready
galaxies in view while preserving their projection or memory/history caveats.

The inclusion-lane endpoint analysis is generated by:

```bash
python scripts/run_inclusion_lane_endpoint_analysis.py
```

This writes:

```text
data/derived/inclusion_lane_endpoint_scores.csv
data/derived/inclusion_lane_endpoint_summary.csv
data/derived/inclusion_lane_endpoint_allowed_use_summary.csv
data/derived/inclusion_lane_information_gain_transitions.csv
reports/inclusion_lane_endpoint_analysis.md
```

Current holdout strict+caution reading:

```text
Rows:                                      16.
Source-native hard family beats wrong:     0.8125.
Source-native hard family beats TPG/v6:    0.5000.
Source-native hard family beats MOND:      0.4375.
Tau evidence L2 beats TPG/v6:              0.3750.
Tau evidence L2 beats MOND:                0.3125.
L2 -> L3 improves RMSE in:                 0.6250.
```

This is mixed. The lane preserves a matched-vs-wrong morphology-specific signal,
but it does not yet produce baseline superiority. That is useful: it says the
expanded support lane is good for acquisition planning and sensitivity checks,
not for an endpoint-validation claim.

The caution lane is now split by allowed use. On holdout, the projection-caveat
sub-lane contains 14 galaxies. The source-native hard-family formula still
beats the wrong-family mean in `0.7857` of those rows, but the Tau evidence L2
normalization beats TPG/v6 in only `0.3571` and MOND in only `0.2857`. This
points to projection/scale quality and source-normalization as the immediate
weak link, not to loss of morphology-family specificity.

The projection/scale repair audit and source-normalization failure-mode audit
are generated by:

```bash
python scripts/build_projection_scale_repair_audit.py
python scripts/audit_source_normalization_failure_modes_by_lane.py
```

These write:

```text
data/derived/projection_scale_repair_audit.csv
data/derived/projection_scale_repair_summary.csv
reports/projection_scale_repair_audit.md
data/derived/source_normalization_failure_modes_by_lane.csv
data/derived/source_normalization_failure_modes_by_lane_summary.csv
reports/source_normalization_failure_modes_by_lane.md
```

Current repair map:

```text
No projection/scale repair required:             71/175.
Needs vertical geometry source:                  34/175.
Needs inclination/projection review:             26/175.
Needs distance/scale source:                     30/175.
Repairable with existing scale source + audit:   14/175.
```

On the holdout projection-caveat sub-lane, `7/14` rows are classified as
`PROJECTION_SCALE_NORMALIZATION_FAILURE`: morphology-family specificity is
present, but the Tau evidence L2 normalization does not transfer it into
baseline-competitive solved response. This is the most immediate repair target.

### S4G75 source-rich lane

The current source-rich disk-scale lane is generated by:

```bash
python scripts/run_s4g75_scale_source_subset_endpoint_stress_test.py
python scripts/analyze_s4g75_failure_modes.py
python scripts/build_s4g75_source_rich_lane_action_plan.py
python scripts/build_s4g75_holdout_repair_review_packet.py
python scripts/build_s4g75_kernel_observable_fill.py
python scripts/run_s4g75_filled_kernel_endpoint_stress_test.py
python scripts/audit_s4g75_filled_kernel_delta_drivers.py
python scripts/build_s4g75_direct_source_native_acquisition_manifest.py
python scripts/audit_s4g75_source_native_availability.py
python scripts/acquire_s4g75_direct_kernel_measurements.py
python scripts/build_s4g75_kernel_ready_promotion_gate.py
python scripts/build_s4g75_promoted_kernel_observable_fill.py
python scripts/run_s4g75_promoted_kernel_endpoint_stress_test.py
python scripts/build_s4g75_conditional_promotion_requirements.py
python scripts/build_s4g75_promotion_theorem_skeletons.py
```

These write:

```text
data/derived/s4g75_scale_source_subset_endpoint_scores.csv
data/derived/s4g75_scale_source_subset_endpoint_summary.csv
data/derived/s4g75_failure_mode_breakdown.csv
data/derived/s4g75_repair_priority_queue.csv
data/derived/s4g75_source_rich_lane_action_plan.csv
data/derived/s4g75_holdout_repair_review_packet.csv
data/derived/s4g75_holdout_repair_review_galaxy_summary.csv
data/derived/s4g75_kernel_observable_fill.csv
data/derived/s4g75_kernel_observable_fill_summary.csv
data/derived/s4g75_filled_kernel_endpoint_scores.csv
data/derived/s4g75_filled_kernel_endpoint_summary.csv
data/derived/s4g75_filled_vs_proxy_delta.csv
data/derived/s4g75_filled_kernel_delta_drivers.csv
data/derived/s4g75_filled_kernel_delta_driver_summary.csv
data/derived/s4g75_direct_source_native_observable_targets.csv
data/derived/s4g75_direct_source_native_acquisition_manifest.csv
data/derived/s4g75_direct_source_native_acquisition_source_summary.csv
data/derived/s4g75_direct_source_native_acquisition_family_summary.csv
data/derived/s4g75_source_native_availability_audit.csv
data/derived/s4g75_source_native_availability_summary.csv
data/derived/s4g75_source_native_availability_source_coverage.csv
data/derived/s4g75_direct_kernel_measurements.csv
data/derived/s4g75_direct_kernel_measurement_summary.csv
data/derived/s4g75_kernel_ready_promotion_gate.csv
data/derived/s4g75_kernel_ready_promotion_summary.csv
data/derived/s4g75_kernel_ready_endpoint_subset_status.csv
data/derived/s4g75_promoted_kernel_observable_fill.csv
data/derived/s4g75_promoted_kernel_observable_fill_summary.csv
data/derived/s4g75_promoted_kernel_endpoint_scores.csv
data/derived/s4g75_promoted_kernel_endpoint_summary.csv
data/derived/s4g75_promoted_vs_proxy_delta.csv
data/derived/s4g75_promoted_vs_filled_delta_summary.csv
data/derived/s4g75_conditional_promotion_requirements.csv
data/derived/s4g75_conditional_promotion_requirement_summary.csv
data/derived/s4g75_promotion_theorem_skeletons.csv
data/derived/s4g75_promotion_theorem_assumptions.csv
data/derived/s4g75_promotion_theorem_waiting_rows.csv
reports/s4g75_scale_source_subset_endpoint_stress_test.md
reports/s4g75_failure_mode_breakdown.md
reports/s4g75_source_rich_lane_action_plan.md
reports/s4g75_holdout_repair_review_packet.md
reports/s4g75_kernel_observable_fill.md
reports/s4g75_filled_kernel_endpoint_stress_test.md
reports/s4g75_filled_kernel_delta_driver_audit.md
reports/s4g75_direct_source_native_acquisition_manifest.md
reports/s4g75_source_native_availability_audit.md
reports/s4g75_direct_kernel_measurement_extraction.md
reports/s4g75_kernel_ready_promotion_gate.md
reports/s4g75_promoted_kernel_observable_fill.md
reports/s4g75_promoted_kernel_endpoint_stress_test.md
reports/s4g75_conditional_promotion_requirements.md
reports/s4g75_promotion_theorem_skeletons.md
```

Current S4G75 holdout reading:

```text
Rows:                                  21.
Hard matched family beats wrong mean:  0.9524.
Hard matched family beats TPG/v6:      0.5238.
Hard matched family beats MOND:        0.5714.
Tau L2 beats old L2 intake:            0.6190.
Tau L2 beats TPG/v6:                   0.3810.
Tau L2 beats MOND:                     0.6190.
```

This makes the 75-row S4G source-rich lane the best current development lane:
it is source-richer than the full 175-row stress sample and preserves a strong
matched-vs-wrong morphology signal. It is still not an accepted endpoint
validation lane, because the rows mix strict, caution, and acquisition states.
The next action is P0/P1 source repair inside this 75-row lane before expanding
the accepted-claim sample.

The holdout repair packet currently covers 15 galaxies and 71 residual-blind
review fields. Its key operational result is that S4G/SPARC scale evidence is
already present for the repair rows, but endpoint eligibility remains blocked
by external family-label audit and missing family-specific kernel fields:
compact support radius for the compact row, tail inner/cutoff radii for
scale-tail rows, and `thickness_h_over_rs` for thick/flared rows.

The kernel-observable fill then assigns concrete numerical candidates for those
missing fields:

```text
Scale radius:      SOURCE_DERIVED_S4G_SPARC_SCALE for 15/15.
Tail fields:       SOURCE_CONSTRAINED_FORMULA_CANDIDATE for 7 scale-tail rows.
Compact support:  SOURCE_CONSTRAINED_FORMULA_CANDIDATE for 1 compact row.
Thickness h/Rs:    SOURCE_CONSTRAINED_FORMULA_CANDIDATE for 7 thick/flared rows.
Edge-disk h/Rs:    SOURCE_CONSTRAINED_EDGE_DISK_CANDIDATE for 1 thick/flared row.
```

Concrete here means numerically filled, not accepted. The values are
residual-blind and source-constrained, but tail, compact, and thickness fields
remain formula-conditional candidates until direct source-native morphology
measurements or an accepted bridge promotion rule exists.

The filled-kernel endpoint stress test preserves the strong morphology-family
specificity but does not improve the baseline comparison:

```text
Holdout matched-vs-wrong: old 0.9524, filled 0.9524.
Holdout matched-vs-TPG/v6: old 0.5238, filled 0.4286.
Holdout matched-vs-MOND: old 0.5714, filled 0.5714.
```

This is a preserved negative/mixed result. It says that concrete
source-constrained formula-candidate filling is not enough by itself. The next
repair target is stronger direct source-native kernel observables and the
source-normalization/projection layer, not another endpoint-selected family.

The filled-kernel delta-driver audit localizes that next repair target:

```text
P0 direct source-native required:
    scale-tail HI/break/tail cutoff rows: 3.
    thick/flared vertical-geometry rows: 6.

P1 promote or confirm source-native:
    compact-support rows: 1.
    scale-tail HI/break/tail cutoff rows: 3.
    thick/flared vertical-geometry rows: 2.
```

The strongest negative diagnostic is therefore not the morphology match itself.
It is the kernel-observable layer: direct outer-disk/HI transition data and
direct vertical-geometry data are needed before the filled S4G75 lane can make
a baseline-superiority claim.

The direct source-native acquisition manifest turns this into an explicit
source queue:

```text
Total source tasks:        15.
P0 direct source-native:    9.
P1 promote/confirm:         6.
```

P0 tasks target `NGC4214`, `UGC06917`, `UGC06983`, `NGC0024`, `NGC2683`,
`NGC3726`, `NGC3949`, `NGC4088`, and `NGC5907`. The required source families
are S4G, NED/NED-D, DustPedia, HI survey support, and PHANGS where relevant.
This manifest is an acquisition queue only; it cannot create accepted readout
labels or endpoint wins without a later residual-blind audit.

The source-native availability audit checks the same queue against the locally
acquired S4G/SPARC/DustPedia/HI/PHANGS cache:

```text
S4G match coverage:       15/15.
SPARC HI radius coverage: 14/15.
DustPedia direct match:    3/15.
PHANGS public sample:      0/15.
```

Kernel-specific reading:

```text
Scale-tail rows:
    HI extent is mostly present, but this is still only partial support.
    A direct outer-disk transition profile, break radius, truncation radius,
    or source-native tail cutoff is still missing.

Compact row:
    a compact/bulge component is present. S4G Table 7 supplies a direct
    Sersic bulge Re for NGC5985.

Thick/flared rows:
    five P0 and two P1 rows still lack direct vertical geometry.
    NGC5907 has S4G edge-disk hz2/hr2 support.
```

This explains the weak filled-kernel baseline transfer: generic source coverage
is good, but the bridge needs kernel-specific source-native observables, not
only 4D proxy substitutes.

The direct kernel measurement extraction reads the stable direct-source
acquisition manifest, not the current conditional-promotion table. This keeps
already promoted rows in the extraction under repeated reproduction runs. It
finds two S4G Table 7 kernel measurements:

```text
NGC5985:
    compact_support_radius_kpc = 0.735239 from S4G Sersic bulge Re.

NGC5907:
    h/Rs = 0.173321 from S4G edge-disk hz2/hr2.
```

The kernel-ready promotion gate is deliberately stricter:

```text
Strict kernel-ready endpoint rows: 2.
Conditional kernel rows:          6.
Proxy-only kernel rows:           7.
```

So the S4G75 repair lane now has a tiny strict kernel-ready subset
(`NGC5985`, `NGC5907`), but it is too small for accepted validation. The six
remaining conditional rows are all scale-tail rows awaiting either direct
outer-disk transition evidence or a residual-blind Tau-side RHI promotion rule.

The conditional promotion requirements now reduce the remaining six conditional
rows to one active family-level gate:

```text
TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION:
    SPARC HI extent may promote scale-tail cutoff only if it constrains the
    same outer-disk transition, break, truncation, or tail-support radius used
    by the formula kernel.
```

The compact and edge-disk gates are no longer waiting on the current S4G75
conditional list because direct S4G Table 7 kernel measurements were extracted
for their waiting rows. They remain general bridge gates for future rows:

```text
COMPACT-COMPONENT-SUPPORT-PROMOTION:
    compact finite-source support requires a compact component support radius,
    not merely an effective light radius.

EDGE-DISK-TO-VERTICAL-KERNEL-PROMOTION:
    an edge-disk component may promote thick/flared only if it constrains
    vertical scale height, flare, warp, or gas-plane thickness.
```

Each gate can be satisfied either by direct source-native measurement or by a
residual-blind Tau-side promotion theorem. Endpoint improvement itself cannot
satisfy these gates.

The current tail RHI promotion attempt records all six remaining scale-tail
rows as theorem-conditional upper-cutoff candidates, not strict measurements.
It uses the fact that SPARC `RHI` is available in the local lane and cites the
homogeneous outer HI profile context from Wang et al. 2014, but it preserves
the claim boundary: an HI extent can support a conservative upper-cutoff
theorem only after we prove that it constrains the same outer transition used
by the readout kernel. Until then these rows remain non-endpoint and
`endpoint_scores_allowed = False`.

The remaining kernel acquisition ledger then separates the non-strict rows into
actionable acquisition/theorem lanes:

```text
Scale-tail transition missing:
    6 galaxies.
    Direct route: resolved HI radial profile, outer-disk break/truncation, or
    source-native transition radius.
    Theorem route: residual-blind RHI conservative upper-cutoff theorem.

Vertical kernel missing:
    7 galaxies.
    Direct route: vertical scale height, h/Rs, flare/warp radius, or gas-plane
    thickness.
    Theorem route: residual-blind edge-disk/inclination-to-vertical-kernel
    theorem.
```

Within the vertical-kernel blockers, `NGC2683` and `NGC3972` are the highest
priority direct literature-search targets because their inclinations make
edge-on vertical decomposition or warp evidence more plausible. `NGC4088` is a
high-inclination flare/warp target. `NGC0024`, `NGC3726`, `NGC3949`, and
`NGC4389` remain lower-confidence kinematic or multi-band thickness-proxy
review targets. None of these rows is endpoint-ready yet.

The first targeted literature-hit pass improves this map without yet changing
endpoint eligibility:

```text
NGC2683:
    direct literature flare-profile source found.
    Vollmer, Nehlig & Ibata 2016 model the HI disk with an exponential flare:
        H = 0.5 kpc at R = 9 kpc,
        H = 4 kpc at R = 15 kpc,
        saturated to R = 22 kpc,
        outer ring vertical offset = 1.3 kpc.
    Status: direct profile ready, but mapping required into the current
    thick/flared executable kernel.

Scale-tail rows:
    NGC4214 has HI/warp profile context from Lelli, Verheijen & Fraternali
    2014, but no tail transition radius is extracted here.
    UGC06917 and UGC06983 have Verheijen & Sancisi 2001 HI atlas/profile
    source candidates.
    UGC00891, UGC04499, and UGC05829 have van Zee / Swaters source-family
    candidates.
    Status: profile extraction still required before strict promotion.
```

This is a useful strengthening but also a claim-boundary result. `NGC2683`
should not be converted directly into a scalar `h/Rs` endpoint override until a
residual-blind profile-to-kernel mapping is implemented. The tail rows likewise
remain extraction/theorem tasks, not accepted kernel-ready rows.

The NGC2683 flare-profile mapping gate is the first concrete version of that
next layer. It maps the source-native profile onto the observed rotation radii
without using residuals:

```text
NGC2683 rotation points checked:       11.
Profile-mapped points:                  7.
Post-22 kpc unmapped decrease points:   4.

Old scalar h/Rs proxy:                  0.202408.
Mapped profile h/Rs range:              0.226281 to 1.810245.
Mapped profile h/Rs median:             0.545702.
```

The source profile is therefore much richer than the current scalar proxy. It
also stresses the existing executable thick/flared kernel because the profile
enters a large-flare regime and the source does not give a unique executable
decrease law beyond 22 kpc. The correct next task is not to force this into the
old scalar shell, but to define a residual-blind profile-aware thick/flared
readout kernel.

The first profile-aware stress preflight confirms this diagnosis. Using the
source profile as a pointwise scalar substitution changes the NGC2683 score
only at the `~1e-4` RMSE level and slightly worsens it:

```text
Mapped-only policy:
    scalar RMSE  = 9.100678
    profile RMSE = 9.100747
    delta        = +0.000069

Hybrid mapped/scalar-unmapped policy:
    scalar RMSE  = 10.331859
    profile RMSE = 10.331898
    delta        = +0.000038

Mapped profile points exceeding current h/Rs clip: 3
```

This is not a failure of the source-native flare profile. It is a failure map
for the current executable shell: the thick/flared kernel still clips
`h/Rs <= 0.75` and treats thickness as a local scalar damping parameter. A real
profile-aware readout should use the radial `H(R)` structure itself, including
the flare rise, saturation, and post-saturation ambiguity.

The unclipped diagnostic strengthens this conclusion rather than removing it:

```text
Mapped-only policy:
    clipped profile delta   = +0.000069
    unclipped profile delta = +0.004542

Hybrid policy:
    clipped profile delta   = +0.000038
    unclipped profile delta = +0.002546
```

So the main problem is not merely the `h/Rs <= 0.75` clip. Removing the clip
still does not turn the direct flare profile into a better readout under the
current pointwise scalar damping shell. The next kernel must be genuinely
radial-profile aware, not only unclipped.

The first nonlocal `H(R)`-aware prototype also preserves this negative result:

```text
post22_hold_plateau_upper:
    scalar RMSE      = 10.331859
    H(R) RMSE        = 10.335662
    delta            = +0.003803

post22_linear_taper_to_inner_height:
    scalar RMSE      = 10.331859
    H(R) RMSE        = 10.334888
    delta            = +0.003029
```

This prototype uses a source-weighted local average of the NGC2683 flare
profile with locality width fixed to the S4G/SPARC disk scale. It is still not
an accepted endpoint, but it sharpens the formula lesson: putting `H(R)` into
the old damping family is insufficient. The next candidate should change the
vertical/readout operator itself, for example by treating flare/warp structure
as a separate closure source rather than only a damping factor on an
exponential-disk shell.

The first closure-source prototype is therefore the first constructive signal
in this branch. Instead of damping by local thickness, it builds a separate
source from the positive radial gradient of `log H(R)`, optionally with a
localized outer-ring offset source. With the same non-endpoint amplitude policy,
it improves the NGC2683 thick/flared stress score:

```text
flare_gradient_source:
    scalar RMSE  = 10.331859
    closure RMSE = 10.203145
    delta        = -0.128714

flare_gradient_plus_ring_offset_source:
    scalar RMSE  = 10.331859
    closure RMSE = 10.178731
    delta        = -0.153128
```

This is not validation, and it is only one galaxy. But it is the first
source-native formula-development result in this lane where the more realistic
morphology profile helps in the expected direction once it is treated as a
closure source rather than a scalar damping substitute.

A residual-blind sensitivity audit then varies only prototype knobs around this
closure-source family:

```text
locality multiplier: 0.5, 1.0, 1.5, 2.0
ring strength:       0.0, 0.5, 1.0
grid size:           12
improved over scalar thick/flared: 12/12
best delta RMSE:     -0.353217
```

This makes the constructive signal more robust: the closure-source direction is
not just one delicate NGC2683 setting. It is still a single-galaxy
formula-development map, not validation, but it gives a clear next bridge
candidate for profile-aware thick/flared galaxies.

The closure-source generalization gate then prevents overclaiming. In the
current S4G75 thick/flared lane:

```text
PROFILE_CLOSURE_SOURCE_READY_PROTOTYPE_ONLY:
    NGC2683

EDGE_ON_VERTICAL_PROFILE_SEARCH_REQUIRED:
    NGC3972

HIGH_INCLINATION_WARP_FLARE_SEARCH_REQUIRED:
    NGC4088

INSUFFICIENT_VERTICAL_PROFILE_SUPPORT:
    NGC0024, NGC3726, NGC3949, NGC4389
```

No row is authorized for closure-source endpoint scoring. The bridge result is
therefore precise: NGC2683 supplies a constructive prototype, while NGC3972 and
NGC4088 are the next source-acquisition targets needed before this can become a
population-level formula family.

A targeted vertical-source search audit now makes that blocker reproducible
rather than informal. NGC2683 remains the only row with a direct profile source.
NGC3972 now has object-specific HI morphology support from O'Brien et al. 2016
and WHISP/Ursa Major observing context from Verheijen & Sancisi 2001, but no
vertical scale, flare profile, warp radius, or gas-plane thickness is extracted.
NGC4088 is stronger: Verheijen & Sancisi 2001 record a strongly distorted disk,
an asymmetric position-velocity diagram, and an asymmetric warp; O'Brien et al.
2018 add object-specific HI kinematic asymmetry context. This is still not an
endpoint input. It is a profile-extraction target: the bridge can now ask for a
source-native warp/asymmetry-to-closure-source mapping, but it cannot yet fill a
galaxy-specific kernel observable. HALOGAS and Patra 2020 remain useful
context for extraplanar/scale-height physics, but they likewise cannot be
promoted into NGC3972/NGC4088 kernel observables without residual-blind profile
or bound extraction for the target galaxy.

The NGC4088 warp/asymmetry extraction gate makes the next step concrete. The
WHISP/Ursa Major source provides source-native observables such as inclination
`69 deg`, position angle `231 deg`, HI diameter `8.5 arcmin`, integrated HI
flux `102.9 Jy km/s`, and qualitative warp/PV/PA asymmetry flags. The missing
pieces are exactly the profile-kernel observables: warp-onset radius,
`theta_warp(R)` or `PA(R)`, vertical height `H(R)`, a radial closure-source
profile, and a residual-blind mapping rule. Thus NGC4088 is now a
closure-source development target, not an endpoint-scoring galaxy.

A pre-kernel normalization step then converts the source-native WHISP/SPARC
geometry into dimensionless observables. The WHISP HI diameter and SPARC
distance reconstruct `R_HI = 22.253 kpc`, consistent with the SPARC catalog
value `RHI = 22.25 kpc` at fractional difference `1.33e-4`. This gives
`R_HI/Rdisk = 8.63` using SPARC `Rdisk` and `R_HI/Rs4g = 6.83` using the S4G
scale radius. These quantities are useful for a future warp/asymmetry
closure-source formula, but they are still pre-kernel observables. They do not
replace the missing radial warp profile or authorize endpoint scoring.

The first mapping-rule shell is now explicit. Using the dimensionless radius
`x := R/R_HI`, the NGC4088 warp/asymmetry source basis is defined as

```text
C_warp(x; x_w, p) = q_warp * max(0, (x - x_w)/(1 - x_w))^p
```

where `q_warp` is the source-side qualitative warp/asymmetry strength and
`x_w := R_warp/R_HI` is the source-native warp-onset control. This is the right
kind of object for the Tau Core bridge: it is morphology/readout indexed,
dimensionless, and residual-blind. It is still blocked for endpoint use because
`x_w`, a radial `PA(R)` or `theta_warp(R)` profile, and the final readout
normalization are not source-extracted yet.

The onset extraction protocol now freezes what would count as a legitimate
source for `x_w`. Accepted routes are: a source-native radial `PA(R)` profile, a
radial warp-angle/tilted-ring profile, or a predeclared channel-map
digitization of the ridge/bend. A text-only statement that the galaxy is warped
is not accepted for `x_w`; it only supports the formula-development lane. This
keeps the mapping shell residual-blind: `x_w` cannot be chosen from the
rotation-curve residual.

The first digitization target manifest now identifies the concrete source page
for the manual/frozen route. The N4088 channel maps are rendered from
Verheijen & Sancisi 2001 PDF page `76` into
`data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_76-076.png`.
The manifest requires an inner disk axis, outer ridge axes by side, onset radius
in arcmin, side-combination rule, and uncertainty. This still does not extract
`x_w`; it only turns the missing source task into a reproducible digitization
target.

The next artifact is now a frozen channel-map digitization worksheet. The ROI
crop
`data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_76_channel_maps_roi.png`
is split into panel-level measurement targets with a companion overlay and
empty measurement fields for inner-axis, outer-ridge, onset-radius, and
uncertainty extraction. This is still not an `x_w` measurement and still not an
endpoint input; it only converts the rendered source page into a reproducible
panel worksheet for later frozen/manual digitization.

The worksheet is generated by:

```text
python scripts/build_s4g75_ngc4088_channel_map_digitization_worksheet.py
```

and writes:

```text
data/derived/s4g75_ngc4088_channel_map_digitization_worksheet.csv
data/derived/s4g75_ngc4088_channel_map_digitization_worksheet_summary.csv
reports/s4g75_ngc4088_channel_map_digitization_worksheet.md
data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_76_channel_maps_roi_worksheet_overlay.png
```

The next operational artifact is the frozen digitization protocol plus blank
response intake. This freezes the allowed measurement logic before any manual
digitization fills values:

```text
python scripts/build_s4g75_ngc4088_channel_map_digitization_protocol.py
```

and writes:

```text
data/derived/s4g75_ngc4088_channel_map_digitization_protocol.csv
data/derived/s4g75_ngc4088_channel_map_digitization_response_template.csv
data/derived/s4g75_ngc4088_channel_map_digitization_response_schema.csv
data/derived/s4g75_ngc4088_channel_map_digitization_response_validation.csv
data/derived/s4g75_ngc4088_channel_map_digitization_response_summary.csv
reports/s4g75_ngc4088_channel_map_digitization_protocol.md
```

This still does not extract `x_w`. It freezes how `x_w` may later be measured:
one inner-disk axis, two outer-side axes, side-by-side onset radii, a frozen
`MIN_SIDE` combination rule, one uncertainty field, and a page-77 consistency
cross-check. A completed response would only authorize a later residual-blind
`x_w` conversion audit; it still would not allow endpoint scoring.

That downstream conversion gate is now explicit:

```text
python scripts/build_s4g75_ngc4088_xw_conversion_audit.py
```

and writes:

```text
data/derived/s4g75_ngc4088_xw_conversion_audit.csv
data/derived/s4g75_ngc4088_xw_conversion_summary.csv
reports/s4g75_ngc4088_xw_conversion_audit.md
```

This audit reads the validated digitization response plus the pre-kernel `R_HI`
normalization and converts a filled response into the dimensionless
`x_w = R_warp / R_HI` control. In the current package it is correctly blocked,
because the response template is still pending. Even a passing `x_w` conversion
would only open the mapping-rule lane; it still would not allow endpoint
scoring.

With `x_w` available, the next source-side artifact is a filled NGC4088
closure-source mapping:

```text
python scripts/build_s4g75_ngc4088_filled_warp_closure_mapping.py
```

and writes:

```text
data/derived/s4g75_ngc4088_filled_warp_closure_mapping.csv
data/derived/s4g75_ngc4088_filled_warp_closure_profile.csv
data/derived/s4g75_ngc4088_filled_warp_closure_summary.csv
reports/s4g75_ngc4088_filled_warp_closure_mapping.md
```

This fills the source-side onset control in the closure-source shell using the
residual-blind `x_w` audit. It still does not supply the final
kernel-to-velocity normalization, so it remains a filled source-basis artifact,
not an endpoint or baseline-comparison result.

The next bridge artifact is an NGC4088-specific kernel-to-velocity
normalization candidate:

```text
python scripts/build_s4g75_ngc4088_kernel_to_velocity_normalization_candidate.py
```

and writes:

```text
data/derived/s4g75_ngc4088_kernel_to_velocity_normalization_constants.csv
data/derived/s4g75_ngc4088_kernel_to_velocity_normalization_profile.csv
data/derived/s4g75_ngc4088_kernel_to_velocity_normalization_summary.csv
reports/s4g75_ngc4088_kernel_to_velocity_normalization_candidate.md
```

This is the first NGC4088-specific candidate bridge from the filled
closure-source basis to a `delta v^2` scale. It remains theory-conditional:
the source-side onset control is now filled, but the physical normalization law
is still not endpoint-authorized and still not a matched-family result.

The next operational export is the NGC4088-specific readout preflight profile:

```text
python scripts/build_s4g75_ngc4088_readout_preflight_profile.py
```

and writes:

```text
data/derived/s4g75_ngc4088_readout_preflight_profile.csv
data/derived/s4g75_ngc4088_readout_preflight_summary.csv
reports/s4g75_ngc4088_readout_preflight_profile.md
```

This evaluates the filled NGC4088 candidate on the local SPARC/TPG point radii
and exports `delta v^2` plus candidate velocity curves for the `p=1` and `p=2`
turn-on branches. It is still a preflight profile export only: no amplitude fit
is performed there, no endpoint score is computed there, and no baseline or
matched-family claim is made there.

The physical normalization-law gate is generated by:

```text
python scripts/build_s4g75_ngc4088_physical_normalization_law_gate.py
```

and writes:

```text
data/derived/s4g75_ngc4088_physical_normalization_formula.csv
data/derived/s4g75_ngc4088_physical_normalization_law_gate.csv
data/derived/s4g75_ngc4088_physical_normalization_law_summary.csv
reports/s4g75_ngc4088_physical_normalization_law_gate.md
```

This gate records the exact candidate formula
`delta_v2_warp(R;p) = sigma_warp q_warp x_w Vflat^2 C_warp(R/R_HI; x_w, p)`.
The formula is dimensionally consistent and reproduces the prefactor
`8324.016 km^2/s^2`, but the law status is
`FORMULA_CONDITIONAL_PHYSICAL_LAW_BLOCKED`. The remaining blockers are the
Tau-side closure/readout derivation of the scale, scale uniqueness, and
population transfer.

Later NGC4088 formula-freeze bookkeeping uses the caveated WHISP graphical
overview review value `x_w = 0.298333`, not this pre-review first-pass value.
The frozen endpoint-protocol normalization is therefore
`8795.111752 km^2/s^2`; the `8324.016 km^2/s^2` value remains recorded as
first-pass provenance and as part of the earlier conditional law audit.

The scale-uniqueness audit is generated by:

```text
python scripts/build_s4g75_ngc4088_scale_uniqueness_audit.py
```

and writes:

```text
data/derived/s4g75_ngc4088_scale_uniqueness_audit.csv
data/derived/s4g75_ngc4088_scale_uniqueness_summary.csv
reports/s4g75_ngc4088_scale_uniqueness_audit.md
```

It lists five residual-blind, dimensionally valid `delta v^2` scale carriers:
the current `x_w * Vflat^2` candidate, `x_w * median_r(v_n^2)`,
`x_w * median_r(v_v6^2)`, `c_g * median_r(v_n^2)`, and
`x_w * c_g * median_r(v_n^2)`. Therefore the current decision is
`BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES`: the scale cannot be selected by
endpoint residuals, and a Tau-side closure/readout principle must choose or
reject the alternatives.

The Tau-side scale-selection gate is generated by:

```text
python scripts/build_s4g75_ngc4088_tau_side_scale_selection_gate.py
```

and writes:

```text
data/derived/s4g75_ngc4088_tau_side_scale_selection_criteria.csv
data/derived/s4g75_ngc4088_tau_side_scale_selection_gate.csv
data/derived/s4g75_ngc4088_tau_side_scale_selection_summary.csv
reports/s4g75_ngc4088_tau_side_scale_selection_gate.md
```

Under the conditional `MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE`, the
current `x_w * Vflat^2` carrier is the only selected scale. The status is
`THEORY_SELECTION_CONDITIONAL_CURRENT_ONLY`, not a final law: the selection rule
still needs a Tau-side closure/readout derivation before endpoint use. Its law
status is `SELECTION_RULE_CONDITIONAL_NOT_DERIVED_LAW`.

The follow-up derivation gate is generated by:

```text
python scripts/build_s4g75_ngc4088_tau_side_scale_derivation_gate.py
```

and writes:

```text
data/derived/s4g75_ngc4088_tau_side_scale_derivation_skeleton.csv
data/derived/s4g75_ngc4088_tau_side_scale_derivation_gate.csv
data/derived/s4g75_ngc4088_tau_side_scale_derivation_summary.csv
reports/s4g75_ngc4088_tau_side_scale_derivation_gate.md
```

The gate records the exact missing proof obligations behind the selected
carrier. It currently reports
`DERIVATION_BLOCKED_SELECTION_RULE_AUDITED` and
`NOT_DERIVED_TAU_SIDE_LAW`: dimensional consistency passes, source-onset
locality/comparator autonomy/minimal-source-factor status remains
formula-conditional, and asymptotic carrier dominance, a Tau-side
closure/readout functional, and population transfer remain blocked.

The asymptotic-carrier dominance subgate is generated by:

```text
python scripts/build_s4g75_ngc4088_asymptotic_carrier_dominance_gate.py
```

and writes:

```text
data/derived/s4g75_ngc4088_asymptotic_carrier_candidate.csv
data/derived/s4g75_ngc4088_asymptotic_carrier_dominance_gate.csv
data/derived/s4g75_ngc4088_asymptotic_carrier_dominance_summary.csv
reports/s4g75_ngc4088_asymptotic_carrier_dominance_gate.md
```

This subgate sharpens the `G3_ASYMPTOTIC_CARRIER_DOMINANCE` blocker. `Vflat^2`
passes catalog-availability, dimensional, point-sampled-median rejection, and
external-comparator rejection checks, but the status remains
`ASYMPTOTIC_CARRIER_DOMINANCE_NOT_DERIVED` and
`VFLAT2_SOURCE_CANDIDATE_NOT_TAU_SIDE_CARRIER_PROOF`.

The closure-functional requirement gate is generated by:

```text
python scripts/build_s4g75_ngc4088_closure_functional_requirement_gate.py
```

and writes:

```text
data/derived/s4g75_ngc4088_closure_functional_requirement.csv
data/derived/s4g75_ngc4088_closure_functional_requirement_gate.csv
data/derived/s4g75_ngc4088_closure_functional_requirement_summary.csv
reports/s4g75_ngc4088_closure_functional_requirement_gate.md
```

This gate sharpens the `G6_TAU_SIDE_CLOSURE_FUNCTIONAL` blocker. It specifies a
minimum functional requirement,
`J_tau[lambda_w] = closure_cost + asymptotic_carrier_penalty + autonomy_penalty`,
but the status is still
`CLOSURE_FUNCTIONAL_REQUIREMENT_SPECIFIED_NOT_DERIVED` and
`NO_TAU_SIDE_EULER_CLOSURE_DERIVATION_YET`: the closure cost and stationarity
equation have not been constructed.

The minimal Euler-ansatz gate is generated by:

```text
python scripts/build_s4g75_ngc4088_minimal_euler_ansatz_gate.py
```

and writes:

```text
data/derived/s4g75_ngc4088_minimal_euler_ansatz.csv
data/derived/s4g75_ngc4088_minimal_euler_ansatz_gate.csv
data/derived/s4g75_ngc4088_minimal_euler_ansatz_summary.csv
reports/s4g75_ngc4088_minimal_euler_ansatz_gate.md
```

This gate performs the first explicit conditional stationarity calculation:
for
`J_min(lambda_w)=1/2 kappa_lambda (lambda_w - sigma_warp q_warp x_w Vflat^2)^2`,
the Euler condition gives
`lambda_w = sigma_warp q_warp x_w Vflat^2 = 8324.016 km^2/s^2`. The status is
`EULER_CONDITION_SOLVED_GIVEN_TARGET_ANSATZ`, but not a law:
`TARGET_FUNCTIONAL_NOT_TAU_SIDE_DERIVED`.

The target-functional origin gate is generated by:

```text
python scripts/build_s4g75_ngc4088_target_functional_origin_gate.py
```

and writes:

```text
data/derived/s4g75_ngc4088_target_functional_origin_factors.csv
data/derived/s4g75_ngc4088_target_functional_origin_gate.csv
data/derived/s4g75_ngc4088_target_functional_origin_summary.csv
reports/s4g75_ngc4088_target_functional_origin_gate.md
```

This gate decomposes the Euler target. The source-side factors are available:
`sigma_warp`, `q_warp`, `x_w`, and `Vflat^2`. The composite target
`sigma_warp q_warp x_w Vflat^2 = 8324.016 km^2/s^2` is dimensionally valid,
but the status remains
`SOURCE_FACTORS_AVAILABLE_COUPLING_NOT_DERIVED` and
`TARGET_TERM_NOT_TAU_SIDE_DERIVED`: the multiplicative coupling and quadratic
penalty are still ansatz-level, not Tau-side derived.

The multiplicative-coupling separability gate is generated by:

```text
python scripts/build_s4g75_ngc4088_multiplicative_coupling_separability_gate.py
```

and writes:

```text
data/derived/s4g75_ngc4088_multiplicative_coupling_theorem.csv
data/derived/s4g75_ngc4088_multiplicative_coupling_assumptions.csv
data/derived/s4g75_ngc4088_multiplicative_coupling_separability_gate.csv
data/derived/s4g75_ngc4088_multiplicative_coupling_separability_summary.csv
reports/s4g75_ngc4088_multiplicative_coupling_separability_gate.md
```

This gate upgrades the product term to a conditional separability result:
if the warp/asymmetry readout amplitude separates into orientation, source
strength, onset-support, and asymptotic-carrier factors, then
`lambda_w = sigma_warp q_warp x_w Vflat^2`. The status is
`CONDITIONAL_PRODUCT_DERIVED_IF_SEPARABLE`, not a final law:
`SEPARABILITY_AND_CROSS_TERM_SUPPRESSION_NOT_DERIVED`.

The cross-term suppression gate is generated by:

```text
python scripts/build_s4g75_ngc4088_cross_term_suppression_gate.py
```

and writes:

```text
data/derived/s4g75_ngc4088_cross_term_model.csv
data/derived/s4g75_ngc4088_cross_term_ledger.csv
data/derived/s4g75_ngc4088_cross_term_suppression_gate.csv
data/derived/s4g75_ngc4088_cross_term_suppression_summary.csv
reports/s4g75_ngc4088_cross_term_suppression_gate.md
```

This gate keeps the leading product honest by introducing
`lambda_w = lambda_0 * (1 + epsilon_cross)`. The zero-cross limit recovers the
current formula, but the current status is
`CROSS_TERMS_DECLARED_NOT_SUPPRESSED` and
`LEADING_PRODUCT_ONLY_UNTIL_EPSILON_CROSS_BOUND`: mixed source-source terms are
declared but not yet derived away or bounded by residual-blind source
observables.

The epsilon-cross source-bound protocol is generated by:

```text
python scripts/build_s4g75_ngc4088_epsilon_cross_source_bound_protocol.py
```

and writes:

```text
data/derived/s4g75_ngc4088_epsilon_cross_source_observables.csv
data/derived/s4g75_ngc4088_epsilon_cross_bound_protocol.csv
data/derived/s4g75_ngc4088_epsilon_cross_source_bound_gate.csv
data/derived/s4g75_ngc4088_epsilon_cross_source_bound_summary.csv
reports/s4g75_ngc4088_epsilon_cross_source_bound_protocol.md
```

This protocol declares a residual-blind bound form for `epsilon_cross`.
NGC4088 already has three first-pass source observables: a 90 degree
orientation mismatch, a 0.4 arcmin side-onset asymmetry, and a 0.25 onset
uncertainty fraction. The numeric bound remains blocked:
`SOURCE_BOUND_PROTOCOL_PARTIAL_NUMERIC_BOUND_BLOCKED` and
`SYMBOLIC_UNBOUNDED_UNTIL_Q_AND_MEMORY_READY`, because quantitative
`q_warp`, a memory/history proxy, and bound coefficients are still missing.

The q_warp measurement protocol is generated by:

```text
python scripts/build_s4g75_ngc4088_qwarp_measurement_protocol.py
```

and writes:

```text
data/derived/s4g75_ngc4088_qwarp_measurement_protocol.csv
data/derived/s4g75_ngc4088_qwarp_measurement_fields.csv
data/derived/s4g75_ngc4088_qwarp_measurement_response_template.csv
data/derived/s4g75_ngc4088_qwarp_measurement_gate.csv
data/derived/s4g75_ngc4088_qwarp_measurement_summary.csv
reports/s4g75_ngc4088_qwarp_measurement_protocol.md
```

This protocol turns qualitative `q_warp=1` into a residual-blind measurement
task:
`q_warp_measured = clipped_mean(outer_asymmetry_extent / local_disk_reference_extent)`.
The protocol has 23 panel measurement targets and five required fields, but the
response is still empty. Status:
`QWARP_PROTOCOL_READY_MEASUREMENT_BLOCKED`; after measurement and independent
review it would unblock the q component of the `epsilon_cross` bound.

The NGC4088 memory/history proxy protocol is generated by:

```text
python scripts/build_s4g75_ngc4088_memory_history_proxy_protocol.py
```

and writes:

```text
data/derived/s4g75_ngc4088_memory_history_proxy_protocol.csv
data/derived/s4g75_ngc4088_memory_history_proxy_components.csv
data/derived/s4g75_ngc4088_memory_history_proxy_response_template.csv
data/derived/s4g75_ngc4088_memory_history_proxy_gate.csv
data/derived/s4g75_ngc4088_memory_history_proxy_summary.csv
reports/s4g75_ngc4088_memory_history_proxy_protocol.md
```

It defines
`m_history_warp = weighted_source_score(warp_persistence, HI_lopsidedness, outer_disk_asymmetry, interaction_context)`
as a residual-blind source proxy for the `B_mem f_mem` term in the
`epsilon_cross` bound. The protocol explicitly forbids `vobs`, rotation
residuals, `rotation-inferred family`, and endpoint-selected models. The WHISP
source lane is available, but all component measurements remain empty. Status:
`MEMORY_PROTOCOL_READY_MEASUREMENT_BLOCKED`; after residual-blind source review
and independent verification it would unblock the memory component:
`UNBLOCKS_MEMORY_COMPONENT_AFTER_MEASUREMENT_AND_REVIEW`.

The first-pass source-response fill is generated by:

```text
python scripts/build_s4g75_ngc4088_first_pass_source_response_fill.py
```

and writes:

```text
data/derived/s4g75_ngc4088_qwarp_first_pass_response.csv
data/derived/s4g75_ngc4088_memory_history_first_pass_components.csv
data/derived/s4g75_ngc4088_memory_history_first_pass_response.csv
data/derived/s4g75_ngc4088_first_pass_source_response_fill_gate.csv
data/derived/s4g75_ngc4088_first_pass_source_response_fill_summary.csv
reports/s4g75_ngc4088_first_pass_source_response_fill.md
```

It fills provisional source values from the already frozen channel-map
digitization response: `q_warp_measured=1.0` and `m_history_warp=1.0`. These are
not accepted numeric-bound inputs. Status:
`FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED`; independent source review and
environment/context completion remain required.

The independent source-response review is generated by:

```text
python scripts/build_s4g75_ngc4088_source_response_independent_review.py
```

and writes:

```text
data/derived/s4g75_ngc4088_source_response_independent_review.csv
data/derived/s4g75_ngc4088_source_response_independent_review_gate.csv
data/derived/s4g75_ngc4088_source_response_independent_review_summary.csv
reports/s4g75_ngc4088_source_response_independent_review.md
```

It recomputes the first-pass source responses without endpoint residuals. The
q response is accepted for the protocol numeric bound. The previously missing
H4 interaction/context component is now filled by a residual-blind source review
of the NGC4088 literature evidence for distortion, asymmetric warp, and nearby
companion/context. The morphological-history warp proxy is therefore accepted
for this protocol-bound layer rather than caveated. Here memory/history means
morphology-carried source history, not a separate fundamental Tau object.
Status: `SOURCE_RESPONSES_ACCEPTED_FOR_PROTOCOL_BOUND`.

The B_i coefficient freeze rule is generated by:

```text
python scripts/build_s4g75_ngc4088_bi_coefficient_freeze_rule.py
```

and writes:

```text
data/derived/s4g75_ngc4088_bi_frozen_coefficients.csv
data/derived/s4g75_ngc4088_bi_coefficient_freeze_rule_gate.csv
data/derived/s4g75_ngc4088_bi_coefficient_freeze_rule_summary.csv
reports/s4g75_ngc4088_bi_coefficient_freeze_rule.md
```

It freezes the conservative residual-blind protocol rule `B_i=1` for all four
coefficients. This is a unit-Lipschitz/triangle-bound default, not a final
Tau-side sharp-amplitude derivation and not an endpoint fit. Status:
`BI_COEFFICIENTS_FROZEN_PROTOCOL_BOUND_READY`.

The sharpened B_i coefficient-bound rule is generated by:

```text
python scripts/build_s4g75_ngc4088_bi_sharp_coefficient_bound_rule.py
```

and writes:

```text
data/derived/s4g75_ngc4088_bi_sharp_coefficients.csv
data/derived/s4g75_ngc4088_bi_sharp_coefficient_bound_rule_gate.csv
data/derived/s4g75_ngc4088_bi_sharp_coefficient_bound_rule_summary.csv
reports/s4g75_ngc4088_bi_sharp_coefficient_bound_rule.md
```

It supplies the stricter residual-blind protocol rule `B_i=0.5` under a
declared second-order Taylor-remainder interpretation with normalized
source-space Hessian cap `<=1`. This is formula-conditional and sharper than
the unit bound, but it is still not a final Tau-side amplitude derivation.
Status: `BI_COEFFICIENTS_SHARPENED_PROTOCOL_BOUND_READY`.

The epsilon-cross input review packet is generated by:

```text
python scripts/build_s4g75_ngc4088_epsilon_cross_input_review_packet.py
```

and writes:

```text
data/derived/s4g75_ngc4088_epsilon_cross_input_review_obligations.csv
data/derived/s4g75_ngc4088_epsilon_cross_input_review_gate.csv
data/derived/s4g75_ngc4088_epsilon_cross_input_review_summary.csv
reports/s4g75_ngc4088_epsilon_cross_input_review_packet.md
```

This packet consolidates the two residual-blind source-measurement obligations
(`q_warp_measured`, `m_history_warp`) and the four coefficient-rule obligations
(`B_PA`, `B_R`, `B_q`, `B_mem`). With the independent source review and the
active residual-blind coefficient protocol present, this gate now authorizes
downstream evaluation of a numeric protocol bound. Status:
`INPUT_REVIEW_PACKET_NUMERIC_PROTOCOL_BOUND_READY`; the next required action is
`evaluate_numeric_epsilon_cross_protocol_bound`.

The B_i coefficient-rule gate is generated by:

```text
python scripts/build_s4g75_ngc4088_bi_coefficient_rule_gate.py
```

and writes:

```text
data/derived/s4g75_ngc4088_bi_feature_normalization.csv
data/derived/s4g75_ngc4088_bi_coefficient_obligations.csv
data/derived/s4g75_ngc4088_bi_coefficient_rule_gate.csv
data/derived/s4g75_ngc4088_bi_coefficient_rule_summary.csv
reports/s4g75_ngc4088_bi_coefficient_rule_gate.md
```

This gate carries the residual-blind, dimensionless feature-normalization side
and the active protocol coefficients. Current NGC4088 values are `f_PA=0.5`,
`f_R=0.25`, `f_q=1.0`, and `f_mem=1.0`; `f_mem` is a source-reviewed
morphological-history proxy, not a separate fundamental memory object. The
conservative baseline keeps `B_PA=B_R=B_q=B_mem=1`, while the active sharpened
formula-conditional protocol uses `B_PA=B_R=B_q=B_mem=0.5`. Status:
`FEATURE_NORMALIZATION_AND_B_VALUES_READY_PROTOCOL_BOUND`; numeric bound status:
`NUMERIC_EPSILON_PROTOCOL_BOUND_READY`.

The epsilon-cross bound-expression shell is generated by:

```text
python scripts/build_s4g75_ngc4088_epsilon_cross_bound_expression_shell.py
```

and writes:

```text
data/derived/s4g75_ngc4088_epsilon_cross_bound_terms.csv
data/derived/s4g75_ngc4088_epsilon_cross_bound_expression.csv
data/derived/s4g75_ngc4088_epsilon_cross_bound_expression_summary.csv
reports/s4g75_ngc4088_epsilon_cross_bound_expression_shell.md
```

It combines the accepted feature-normalization side with the frozen protocol
coefficient side:

```text
|epsilon_cross| <= 0.5*B_PA + 0.25*B_R + 1*B_q + 1*B_mem
```

With the conservative `B_i=1` baseline this evaluates to:

```text
|epsilon_cross| <= 2.75
```

With the active second-order-remainder `B_i=0.5` protocol rule this evaluates to:

```text
|epsilon_cross| <= 1.375
```

This is a residual-blind protocol upper bound, not a final physical amplitude
derivation and not endpoint authorization. The follow-on readout sensitivity
audit preserves the negative/preparatory result that `1.375` is still loose
enough to require additional Tau-side locality, sign, or monotonicity
constraints before promotion.

The narrowed locality-coupled bound is generated by:

```text
python scripts/build_s4g75_ngc4088_epsilon_cross_locality_bound_rule.py
```

and writes:

```text
data/derived/s4g75_ngc4088_epsilon_cross_locality_bound_terms.csv
data/derived/s4g75_ngc4088_epsilon_cross_locality_bound_gate.csv
data/derived/s4g75_ngc4088_epsilon_cross_locality_bound_summary.csv
reports/s4g75_ngc4088_epsilon_cross_locality_bound_rule.md
```

It treats `epsilon_cross` as an adjacent source/readout coupling rather than as
an independently additive feature sum:

```text
|epsilon_cross| <= 0.5*f_PA*f_R + 0.5*f_R*f_q + 0.5*f_q*f_mem
```

For NGC4088 this gives:

```text
|epsilon_cross| <= 0.6875
```

This is now below one, so the readout sensitivity audit marks the narrowed
bound as sign-stable in the preflight sense. The status is still
formula-conditional: the adjacency rule is a residual-blind locality-chain
protocol, not a final Tau-side locality theorem. Status:
`NUMERIC_EPSILON_PROTOCOL_BOUND_READY_CAVEATED`; numeric bound status:
`NUMERIC_EPSILON_PROTOCOL_BOUND_AVAILABLE`.

The readout promotion gate is generated by:

```text
python scripts/build_s4g75_ngc4088_readout_promotion_gate.py
```

and writes:

```text
data/derived/s4g75_ngc4088_readout_promotion_gate.csv
data/derived/s4g75_ngc4088_readout_promotion_summary.csv
reports/s4g75_ngc4088_readout_promotion_gate.md
```

This gate separates preflight readiness from endpoint authorization. In the
current package, five gates pass: source onset, dimensional carrier, basis
sanity, residual-blind generation, and endpoint-score guard. Three gates remain
blocked: independent digitization review, physical normalization-law
derivation, and population generalization. Thus NGC4088 is
`PROMOTION_BLOCKED_PREFLIGHT_READY`, not endpoint-ready.

The promotion theorem skeletons currently have deliberately conservative
status:

```text
TAIL-HI-EXTENT-PROMOTION-LEMMA-001:
    CONDITIONAL_INCOMPLETE.
    Weakest step: prove that R_HI constrains the same outer-disk transition
    kernel, not merely generic gas extent.

COMPACT-SUPPORT-PROMOTION-LEMMA-001:
    CONDITIONAL_INCOMPLETE.
    Weakest step: prove that Reff or a listed component is the compact support
    used by the compact kernel, not a global half-light proxy.

EDGE-DISK-VERTICAL-PROMOTION-LEMMA-001:
    CONDITIONAL_INCOMPLETE.
    Weakest step: prove that edge-disk/component evidence yields a measured or
    bounded vertical kernel parameter, not merely a projection caveat.
```

The promoted-kernel stress test then reruns the S4G75 lane with those direct
kernel overrides. It is still not accepted validation, because the strict
subset has only two rows. The direct compact override is encouraging, while the
direct edge-disk override is not:

```text
NGC5985:
    filled matched RMSE  = 59.896708.
    promoted matched RMSE = 50.032494.
    delta = -9.864214.

NGC5907:
    filled matched RMSE  = 17.013339.
    promoted matched RMSE = 17.025301.
    delta = +0.011961.
```

This preserves the core diagnosis: direct compact support helps in this pilot,
but thick/flared still needs a better vertical readout or projection rule.

Current full-sample freeze verdict:

```text
Endpoint-freeze allowed:                  0/175.
Proxy-gate blocker resolved by E_tau:     175/175.
Blocked by missing Tau-side normalization: 0/175.
Source-native orientation ready:          67/175.
Blocked by source-native orientation:     108/175.
Blocked by projection acceptance:         47/175.
Blocked by memory/history acceptance:     19/175.
Blocked by q_i/normalization acceptance:  1/175.
Formula-conditional normalization present: 175/175.
Dominant source-candidate support:        141/175.
Dominant proxy/partial only:              31/175.
Dominant missing source support:          3/175.
```

This is a protocol safeguard, not a negative empirical result. It says that
the source layer is informative, and a residual-blind source-normalization
candidate now exists. The proxy blocker is resolved, and orientation promotion
is now partial rather than absent. The endpoint still cannot freeze because the
remaining thick/flared orientation rows, projection caveats, memory/history
acceptance, accepted per-galaxy evidence assignments, and the accepted
normalization-law step are not yet closed.
is independently accepted as a Tau-side normalization law and paired with an
accepted morphology-memory/projection audit.

The source-normalization derivation audit is generated by:

```bash
python scripts/build_tau_side_source_normalization_derivation_audit.py
```

This writes:

```text
data/derived/tau_side_source_normalization_derivation_constants.csv
data/derived/tau_side_source_normalization_derivation_rule.csv
data/derived/tau_side_source_normalization_derivation_summary.csv
reports/tau_side_source_normalization_derivation_audit.md
```

The audit records the predeclared orientation signs and source-evidence gates
used by the normalization candidate. It also checks the rule dimensionally as a
delta-v-squared candidate. The constants are not selected from endpoint
residuals. The orientation signs are now recorded as theory-conditional bridge
derivations, while the proxy attenuation is the coarse executable
representative of the conservative Tau-side readout-admission product:

```text
E_proxy* = 1/3
epsilon_* = 0.157399...
strong proxy = 0.85
ordinary proxy = 0.70
standard proxy product = 0.70 * 0.70 * 0.85 * 0.85 = 0.354025.
```

This is not a final universal evidence law; it is the current conservative
readout-admission geometry used by the bridge.

The intended promotion path is:

```text
fixed proxy bin e_proxy = 0.35
    -> galaxy/family-specific evidence gate e_gK = E_tau(g,K).
```

Here `E_tau` must be assigned from residual-blind source presence, geometry
relevance, projection safety, morphology-memory reliability, and resolution
adequacy. The median standard proxy value near `0.35` is now derived as the
coarse-grid product `0.354025` inside the current conservative
readout-admission geometry. The remaining caveat is not the internal proxy
product, but whether this conservative evidence geometry is final.

The theory-conditional source-normalized L2 preflight is generated by:

```bash
python scripts/run_tau_side_source_normalized_l2_endpoint.py
```

This writes:

```text
data/derived/tau_side_source_normalization_component_rule.csv
data/derived/tau_side_source_normalization_galaxy_rule.csv
data/derived/tau_side_source_normalized_l2_endpoint_scores.csv
data/derived/tau_side_source_normalized_l2_endpoint_summary.csv
reports/tau_side_source_normalized_l2_endpoint.md
```

Residual-blind normalization rule:

```text
normalized_shape_gK(r) = kernel_gK(r) / median_r |kernel_gK(r)|
c_g = median_r max(v_v6^2 - v_n^2, 0) / median_r v_v6^2
delta v_gK^2(r) = sigma_K e_gK w_gK c_g median_r(v_n^2) normalized_shape_gK(r)
```

Current holdout reading:

```text
Beats old L2 intake endpoint: 0.568.
Beats TPG/v6:                0.455.
Beats MOND:                  0.545.
Median minus old L2 RMSE:   -0.272.
```

This improves over the raw L2 intake endpoint, but remains formula-conditional:
the orientation signs now have a partial source-native promotion gate, while
the thick/flared orientation source layer and the per-galaxy `q_i` evidence
assignments must become accepted source-native observables before endpoint
freeze.
The endpoint script loads those signs and gates from
`tau_side_source_normalization_derivation_constants.csv`; it does not carry a
separate endpoint-local tuning table.

The sensitivity audit for the conditional signs and evidence gates is generated
by:

```bash
python scripts/audit_tau_side_source_normalization_sensitivity.py
```

This writes:

```text
data/derived/tau_side_source_normalization_sensitivity_manifest.csv
data/derived/tau_side_source_normalization_sensitivity_components.csv
data/derived/tau_side_source_normalization_sensitivity_scores.csv
data/derived/tau_side_source_normalization_sensitivity_summary.csv
reports/tau_side_source_normalization_sensitivity.md
```

Current holdout sensitivity:

```text
primary proxy gate 0.35:
    beats old L2 intake 0.568, TPG/v6 0.455, MOND 0.545.
no proxy gate:
    beats old L2 intake 0.545.
full proxy gate:
    beats old L2 intake 0.523 and TPG/v6 0.523.
all-positive orientation:
    beats old L2 intake 0.477.
all-negative orientation:
    beats old L2 intake 0.432.
```

This audit does not select a winning variant. It shows that the orientation
structure matters. The proxy-gate ladder is now derived inside the conservative
Tau-side readout-admission geometry, so the remaining freeze blockers are
orientation promotion and accepted per-galaxy evidence assignments.

The first executable Tau-side evidence-measure gate is generated by:

```bash
python scripts/build_tau_side_evidence_measure_gate.py
```

This writes:

```text
data/derived/tau_side_evidence_measure_gate_components.csv
data/derived/tau_side_evidence_measure_gate_summary.csv
reports/tau_side_evidence_measure_gate.md
```

Candidate measure:

```text
E_tau = q_source q_geometry q_projection q_memory q_resolution
```

Current full-sample reading:

```text
Components audited:              406.
Proxy/partial components:        105.
Median proxy E_tau:              0.354025.
Mean proxy E_tau:                0.335798.
Median proxy minus fixed 0.35:   +0.004025.
```

This shows that the fixed `0.35` proxy gate can be replaced by a
galaxy/family-specific `E_tau(g,K)` candidate while reproducing the old proxy
bin as a coarse-grid consequence for the median proxy component. The proxy
ladder is derived inside the current conservative readout-admission geometry;
the individual `q_i` assignments are still theory-candidate source/readout
assignments, not accepted source-native observables.
The generated component table therefore carries explicit per-factor status
columns: accepted and missing source gates are definition-derived limit cases,
while proxy/partial rows are marked
`THEORY_CANDIDATE_FACTOR_GEOMETRY_NOT_ACCEPTED`.

The endpoint stress test using `E_tau(g,K)` gates is generated by:

```bash
python scripts/run_tau_side_evidence_measure_l2_endpoint.py
```

This writes:

```text
data/derived/tau_side_evidence_measure_l2_component_rule.csv
data/derived/tau_side_evidence_measure_l2_galaxy_rule.csv
data/derived/tau_side_evidence_measure_l2_endpoint_scores.csv
data/derived/tau_side_evidence_measure_l2_endpoint_summary.csv
reports/tau_side_evidence_measure_l2_endpoint.md
```

Current holdout reading:

```text
Beats old L2 intake endpoint: 0.568.
Beats TPG/v6:                0.455.
Beats MOND:                  0.545.
Median E_tau-minus-old-L2 RMSE: -0.236.
```

This is not a model-selection step. It says that the `E_tau` candidate preserves
the fixed-gate signal while exposing the proxy gate as a source-evidence
measure whose galaxy/component assignments still need source-native acceptance
before endpoint freeze.

## Amplitude Policy Diagnostics

The amplitude-policy diagnostic is generated by:

```bash
python scripts/run_amplitude_policy_diagnostics.py
```

This writes:

```text
data/derived/amplitude_policy_diagnostics_amplitudes.csv
data/derived/amplitude_policy_diagnostics_scores_by_galaxy.csv
data/derived/amplitude_policy_diagnostics_summary.csv
reports/amplitude_policy_diagnostics.md
```

This diagnostic keeps the source-native bridge formula kernels fixed and
changes only the amplitude policy. The current preflight shows that a
family-to-global shrinkage policy preserves most matched-vs-wrong specificity
while improving the MOND comparison. This is not a new endpoint claim; it
identifies Tau-side amplitude normalization as a major next proof and modeling
obligation.

## Amplitude Shrinkage Path

The shrinkage-path diagnostic is generated by:

```bash
python scripts/run_amplitude_shrinkage_path.py
```

This writes:

```text
data/derived/amplitude_shrinkage_path_amplitudes.csv
data/derived/amplitude_shrinkage_path_scores_by_galaxy.csv
data/derived/amplitude_shrinkage_path_summary.csv
data/derived/amplitude_shrinkage_path_tradeoff.csv
reports/amplitude_shrinkage_path.md
```

This scan varies the linear family-to-global amplitude weight from `0` to `1`.
The current holdout tradeoff is strongest near `family_weight = 0.5`, where
matched-vs-wrong specificity remains high and the MOND win fraction becomes
majority-positive. TPG/v6 remains the harder baseline.

## Train-Selected Shrinkage Diagnostic

The train-selected shrinkage diagnostic is generated by:

```bash
python scripts/run_train_selected_shrinkage_diagnostic.py
```

This writes:

```text
data/derived/train_selected_shrinkage_selection.csv
data/derived/train_selected_shrinkage_holdout.csv
reports/train_selected_shrinkage_diagnostic.md
```

This diagnostic selects the family-to-global shrinkage weight using train
split metrics only, then evaluates the selected policy on holdout. In the
current run, all four train-only selection rules choose `family_weight = 0.40`.
On holdout this policy keeps matched-vs-wrong specificity high at `0.818`,
beats MOND in `0.614` of galaxies, and remains mixed against TPG/v6 at
`0.477`. This reduces the risk that the shrinkage range was chosen directly
from holdout, but it is still only a diagnostic. It is not a validated
Tau-side amplitude-normalization law.

## Family Breakdown Diagnostics

The family breakdown diagnostic is generated by:

```bash
python scripts/run_family_breakdown_diagnostics.py
```

This writes:

```text
data/derived/family_breakdown_diagnostics.csv
reports/family_breakdown_diagnostics.md
```

This diagnostic keeps the train-selected shrinkage policy fixed and breaks the
result down by morphology family. In the current holdout split, the strongest
matched-vs-wrong specificity is carried by `K_scale_tail_spiral` and
`K_thick_flared`, both at `0.900`. `K_thick_flared` is also competitive against
both TPG/v6 and MOND in this diagnostic, while `K_scale_tail_spiral` is
MOND-competitive but remains TPG-blocked. `K_exponential_disk` and
`K_compact_finite` are weaker under the current available-data manifest. This
is a failure-map diagnostic for the next modeling gate, not a claim that any
family has been empirically validated.

## Family Observable Quality Diagnostics

The family observable quality diagnostic is generated by:

```bash
python scripts/run_family_observable_quality_diagnostics.py
```

This writes:

```text
data/derived/family_observable_quality_diagnostics.csv
data/derived/family_observable_quality_clean_vs_caveated.csv
reports/family_observable_quality_diagnostics.md
```

This joins the train-selected shrinkage scores to the residual-blind
morphology parameter manifest. In the current holdout split,
`K_thick_flared` is the cleanest current-best-case row. `K_compact_finite`,
`K_exponential_disk`, and `K_scale_tail_spiral` are marked quality-limited
under the available-data manifest because a large fraction of their holdout
rows carry low-inclination, distance-error, few-point, or low-confidence
caveats. The clean-vs-caveated comparison preserves the central direction:
clean holdout manifest rows beat wrong families in `0.900` of galaxies and
MOND in `0.750`, while caveated rows fall to `0.750` and `0.500`,
respectively. This indicates that better morphology-observable extraction is
a real Paper 8 requirement, alongside Tau-side amplitude normalization.

## Predeclared Quality Gate Diagnostics

The predeclared quality gate diagnostic is generated by:

```bash
python scripts/run_predeclared_quality_gate_diagnostics.py
```

This writes:

```text
data/derived/predeclared_quality_gate_diagnostics.csv
data/derived/predeclared_quality_gate_by_family.csv
reports/predeclared_quality_gate_diagnostics.md
```

This evaluates several quality rules under the fixed train-selected shrinkage
policy. The best current candidate observability gates on holdout are
`clean_manifest_proxy` and `confidence_ge_0_75_and_clean`, both with `20`
galaxies, `4` families present, matched-vs-wrong specificity `0.900`, TPG/v6
win fraction `0.500`, and MOND win fraction `0.750`. The broader
`no_large_distance_error` gate keeps `26` holdout galaxies and remains a
candidate gate with matched-vs-wrong `0.885`, TPG/v6 `0.538`, and MOND
`0.731`. These gates are not discovery claims. They identify plausible
predeclared observability rules for the next endpoint run.

## Quality Gate Shuffled Null Diagnostics

The quality gate shuffled-null diagnostic is generated by:

```bash
python scripts/run_quality_gate_shuffled_null_diagnostics.py
```

This writes:

```text
data/derived/quality_gate_shuffled_null.csv
data/derived/quality_gate_shuffled_null_summary.csv
reports/quality_gate_shuffled_null_diagnostics.md
```

This reruns the shuffled-family label null inside each predeclared quality
gate. In the current holdout split, the full `all` gate keeps the strongest
shuffled-null support for matched-vs-wrong morphology specificity, with
`p=0.036` for beats-wrong fraction and `p=0.013` for mean matched-minus-wrong.
The `no_low_inclination` gate is similar, with `p=0.041` and `p=0.011`.
Cleaner gates such as `clean_manifest_proxy` improve baseline comparison but
have weaker shuffled-null evidence because the sample shrinks to 20 galaxies.
This exposes a useful tradeoff for Paper 8: observability cleaning improves
baseline competitiveness, while larger or caveated samples can preserve
stronger label-specificity null power.

## Endpoint Decision Matrix

The endpoint decision matrix is generated by:

```bash
python scripts/run_endpoint_decision_matrix.py
```

This writes:

```text
data/derived/endpoint_decision_matrix.csv
reports/endpoint_decision_matrix.md
```

This combines the predeclared quality-gate metrics with the shuffled-family
null diagnostics. In the current preparation state, `no_low_inclination` is
the natural primary endpoint candidate because it is both baseline-competitive
and supported by the shuffled null: `35` holdout galaxies, matched-vs-wrong
`0.857`, TPG/v6 `0.514`, MOND `0.657`, beats-wrong null `p=0.041`, and mean
endpoint null `p=0.011`. The full `all` gate remains the fuller-sample
specificity support lane, while `no_large_distance_error` is the strongest
baseline-competitiveness secondary gate. This is a protocol decision aid for
future predeclaration, not a selected discovery endpoint.

## Predeclared Endpoint Protocol

The predeclared endpoint protocol sheet is generated by:

```bash
python scripts/build_predeclared_endpoint_protocol.py
```

This writes:

```text
data/derived/predeclared_endpoint_protocol.csv
reports/predeclared_endpoint_protocol.md
```

This freezes the current preparation-state endpoint lanes that a future Paper
8 run should predeclare before scoring: primary lane `no_low_inclination`,
fuller-sample support lane `all`, secondary baseline lane
`no_large_distance_error`, and amplitude policy
`train_selected_family_to_global_shrinkage_0_40`. It also records forbidden
inputs such as endpoint residual gain, required `S_tau`, posthoc gate choice,
and per-galaxy amplitude tuning. The protocol is not a discovery claim; it is
the guardrail that prevents the next run from becoming retrospective endpoint
selection.

## Readiness Upgrade Audit

The readiness upgrade audit is generated by:

```bash
python scripts/build_readiness_upgrade_audit.py
```

This writes:

```text
data/derived/paper8_readiness_upgrade_audit.csv
reports/paper8_readiness_upgrade_audit.md
```

This summarizes the current state after the source-native formula,
train-selected shrinkage, quality-gate, shuffled-null, decision-matrix, and
predeclaration diagnostics. The package is now preparation-ready as a
claim-bounded protocol and diagnostic package. It is not discovery-ready: the
next scientific upgrade is to replace available-data proxy morphology
observables with accepted residual-blind morphology inputs, then run the
predeclared endpoint protocol without changing gates after seeing scores.

## Morphology Observable Intake Schema

The morphology observable intake schema is generated by:

```bash
python scripts/build_morphology_observable_intake_schema.py
```

This writes:

```text
data/derived/morphology_observable_intake_schema.csv
data/derived/morphology_observable_acceptance_gates.csv
reports/morphology_observable_intake_schema.md
```

This is the data-intake contract for the next Paper 8 run. It specifies the
residual-blind fields needed to replace the current proxy manifest, including
family labels, confidence/caveats, inclination and distance-quality fields,
family-specific scale/support/thickness observables, provenance, and forbidden
sources. It explicitly forbids using `vobs` residual gain, required `S_tau`,
endpoint-selected radii, posthoc family choice, or per-galaxy residual tuning.

## Morphology Observable Gap Audit

The morphology observable gap audit is generated by:

```bash
python scripts/run_morphology_observable_gap_audit.py
```

This writes:

```text
data/derived/morphology_observable_gap_audit.csv
data/derived/morphology_observable_gap_by_family.csv
reports/morphology_observable_gap_audit.md
```

This compares the current available-data proxy manifest against the intake
schema. The current package is coverage-rich but acceptance-limited: active
families have broad proxy coverage, but most kernel-driving fields still need
accepted residual-blind morphology-observable sources before a discovery-style
endpoint can be run. This audit is a preparation diagnostic, not an endpoint
score.

## Morphology Observable Source Upgrade Plan

The morphology observable source upgrade plan is generated by:

```bash
python scripts/build_morphology_observable_source_upgrade_plan.py
```

This writes:

```text
data/derived/morphology_observable_source_upgrade_plan.csv
data/derived/morphology_observable_collection_batches.csv
reports/morphology_observable_source_upgrade_plan.md
```

This converts the gap audit into a residual-blind source collection protocol.
The next Paper 8 upgrade is source replacement, not endpoint redesign: replace
proxy family labels and kernel-driving fields with accepted pre-scoring
morphology observables, keep optional non-axisymmetric branches caveated unless
external morphology or velocity-field support exists, and only then rerun the
frozen endpoint protocol.

## Accepted Observable Manifest Template

The accepted observable manifest template and validator are generated by:

```bash
python scripts/build_accepted_observable_manifest_template.py
```

This writes:

```text
data/derived/accepted_morphology_observable_manifest_template.csv
data/derived/accepted_observable_manifest_template_validation.csv
reports/accepted_observable_manifest_template_validation.md
```

The template is intentionally endpoint-blocked. It carries galaxy identifiers
and pre-scoring geometry fields, but it does not promote proxy morphology
labels, kernel observables, or provenance into accepted discovery inputs. A
future endpoint run should consume a populated accepted manifest that passes
this validator, not the empty template and not the proxy manifest.

## Accepted Manifest Readiness Gate

The accepted manifest readiness gate is generated by:

```bash
python scripts/run_accepted_manifest_readiness_gate.py
```

This writes:

```text
data/derived/accepted_manifest_readiness_gates.csv
data/derived/accepted_manifest_readiness_summary.csv
reports/accepted_manifest_readiness_gate.md
```

This converts field-level template validation into an endpoint-level decision.
For the current empty accepted manifest template, the expected decision is
`BLOCKED_ACCEPTED_OBSERVABLES_MISSING`. A future populated manifest must pass
this gate before the frozen blind endpoint protocol is allowed to run.

## Frozen Endpoint Launch Guard

The frozen endpoint launch guard is generated by:

```bash
python scripts/run_frozen_endpoint_launch_guard.py
```

This writes:

```text
data/derived/frozen_endpoint_launch_guard.csv
data/derived/frozen_endpoint_blockers.csv
reports/frozen_endpoint_launch_guard.md
```

This is the final preflight guard before any discovery-style endpoint run. In
the current package the launch status is `LAUNCH_BLOCKED`, and
`endpoint_scores_computed` is `False`. This ensures the proxy manifest and the
empty accepted template cannot be accidentally used as discovery inputs.

## External Morphology Source Registry

The external morphology source registry is generated by:

```bash
python scripts/build_external_morphology_source_registry.py
```

This writes:

```text
data/derived/external_morphology_source_registry.csv
data/derived/morphology_field_source_map.csv
data/derived/sparc_external_source_crossmatch_template.csv
reports/external_morphology_source_registry.md
```

This records the residual-blind acquisition plan for missing accepted inputs:
SPARC remains the sample and baryonic/rotation baseline, S4G is the primary
morphology/decomposition source, NED/NED-D is the identity and
distance/provenance layer, DustPedia is fallback/validation, and PHANGS is an
optional non-axisymmetric/velocity-field branch. The 175-row SPARC crossmatch
template starts as `TO_BE_CHECKED`; it is not accepted-source coverage yet.

## External Morphology Input Acquisition

The first external morphology input acquisition is generated by:

```bash
python scripts/acquire_external_morphology_inputs.py
```

This writes:

```text
data/external/sparc/SPARC_Lelli2016c.mrt
data/derived/external_sparc_master_table.csv
data/derived/external_s4g_galaxies.csv
data/derived/external_s4g_table7.csv
data/derived/external_s4g_disk_component_summary.csv
data/derived/external_s4g_sparc_observable_candidates.csv
data/derived/sparc_external_source_crossmatch_acquired.csv
reports/external_morphology_input_acquisition.md
```

This actually acquires SPARC Table 1 from the official SPARC site and S4G
Pipeline 4 tables from VizieR/CDS. In the current run it obtains 175 SPARC
master rows, 77 S4G crossmatches, and 75 S4G/SPARC-derived disk-scale
candidates. These are source-observable candidates, not a completed accepted
manifest: family labels, tail transition radii, thickness, caveats, and full
provenance still require the accepted-source audit path.

## Accepted Morphology Manifest Draft

The first partial accepted morphology-observable manifest is generated by:

```bash
python scripts/build_accepted_morphology_manifest.py
```

This writes:

```text
data/derived/accepted_morphology_manifest.csv
data/derived/accepted_morphology_manifest_validation.csv
data/derived/accepted_morphology_manifest_by_family.csv
reports/accepted_morphology_manifest.md
```

This promotes only field-level source-native observables with documented
residual-blind provenance. In the current run, 75 S4G/SPARC-derived
scale-radius observables pass the field-level source check, while all 175 rows
remain endpoint-blocked because external morphology-family labels and
family-specific source-native kernel observables are not yet complete. The
manifest is therefore a real source-acquisition upgrade, not an endpoint score
and not empirical validation.

The partial accepted manifest audit is generated by:

```bash
python scripts/audit_accepted_morphology_manifest.py
```

This writes:

```text
data/derived/accepted_morphology_manifest_audit.csv
data/derived/accepted_morphology_manifest_audit_summary.csv
reports/accepted_morphology_manifest_audit.md
```

The audit identifies 13 near-term exponential-disk rows with accepted
S4G/SPARC scale radius and no remaining kernel-field blocker beyond the
external family-label audit. These rows are the next audit pool, not an endpoint
result.

The targeted exponential-disk family-label audit is generated by:

```bash
python scripts/audit_exponential_disk_family_labels.py
```

This writes:

```text
data/derived/exponential_disk_family_label_audit.csv
data/derived/exponential_disk_family_label_audit_summary.csv
reports/exponential_disk_family_label_audit.md
```

This strengthens the 13-row near-term pool using residual-blind S4G component
models. In the current run, 6 rows receive strict external `D:expdisk` support
and 7 rows receive caveated disk-family support from barred or edge-disk
components. This is the first narrow dry-run candidate lane, but it is still not
an endpoint score.

The narrow exponential-disk dry-run calculation is generated by:

```bash
python scripts/run_exponential_disk_narrow_dry_run.py
```

This writes:

```text
data/derived/exponential_disk_narrow_dry_run_points.csv
data/derived/exponential_disk_narrow_dry_run_amplitudes.csv
data/derived/exponential_disk_narrow_dry_run_scores_by_galaxy.csv
data/derived/exponential_disk_narrow_dry_run_summary.csv
reports/exponential_disk_narrow_dry_run.md
```

This dry-run applies the accepted-scale exponential-disk Freeman/Bessel shell to
the 13 S4G-supported rows. The current result is mixed: on the 6 strict rows,
the pool-fit all-13 amplitude beats TPG/v6 in 4/6 cases but beats MOND in only
2/6 cases, while the frozen global train amplitude beats TPG/v6 in 1/6 cases.
The refined amplitude audit adds shrinkage and leave-one-galaxy-out policies;
the leave-one-galaxy-out all-13 policy beats TPG/v6 in 3/6 strict cases and
MOND in 2/6 strict cases. This is a useful executable sanity check, not a
validation result.

The failure and scale-sensitivity audit is generated by:

The first narrow accepted exponential-disk population manifest is generated by:

```bash
python scripts/build_narrow_accepted_exponential_disk_manifest.py
```

This writes:

```text
data/derived/narrow_accepted_exponential_disk_manifest.csv
data/derived/narrow_accepted_exponential_disk_manifest_summary.csv
reports/narrow_accepted_exponential_disk_manifest.md
```

This is the first matched-family accepted population lane in the repo, but only
for the 13 externally audited exponential-disk rows. It does not unblock the
full 175-row launch.

The corresponding narrow accepted population endpoint is generated by:

```bash
python scripts/run_narrow_accepted_exponential_disk_population_endpoint.py
```

This writes:

```text
data/derived/narrow_accepted_exponential_disk_population_endpoint_points.csv
data/derived/narrow_accepted_exponential_disk_population_endpoint_scores.csv
data/derived/narrow_accepted_exponential_disk_population_endpoint_summary.csv
reports/narrow_accepted_exponential_disk_population_endpoint.md
```

This endpoint uses the frozen train-only `K_exponential_disk` amplitude from
the source-native bridge-formula preflight. It is a real, narrow accepted
population endpoint, but not the full matched-family Paper 8 launch and not a
population-wide family validation result.

```bash
python scripts/audit_exponential_disk_failure_sensitivity.py
```

This writes:

```text
data/derived/exponential_disk_failure_sensitivity_scores.csv
data/derived/exponential_disk_failure_sensitivity_summary.csv
data/derived/exponential_disk_failure_sensitivity_best_by_galaxy.csv
reports/exponential_disk_failure_sensitivity_audit.md
```

The audit tests fixed scale multipliers `0.75`, `1.0`, and `1.25` under a
leave-one-galaxy-out amplitude policy. The strict lane remains mixed across all
three multipliers, which points to a readout-normalization or subtype-splitting
problem rather than a simple single-scale correction.

The rotation-inferred morphology diagnostic is generated by:

```bash
python scripts/run_rotation_inferred_morphology_diagnostic.py
```

This writes:

```text
data/derived/rotation_inferred_morphology_diagnostic.csv
data/derived/rotation_inferred_morphology_summary.csv
data/derived/rotation_inferred_external_expdisk_summary.csv
reports/rotation_inferred_morphology_diagnostic.md
```

This inverse diagnostic asks which readout family the rotation-curve scores
would select. It is not residual-blind and must not be used as the accepted
morphology label. In the current run, the rotation-inferred family matches the
predeclared proxy family in about `0.354` of rows, and matches the external
S4G-supported exponential-disk label in about `0.308` of the 13 audited rows.
This supports using the inverse diagnostic as a subtype/readout-split generator,
not as validation.

The morphological memory/history proxy diagnostic is generated by:

```bash
python scripts/build_morphological_memory_history_proxy.py
```

This writes:

```text
data/derived/morphological_memory_history_proxy.csv
data/derived/morphological_memory_history_proxy_summary.csv
data/derived/morphological_memory_history_proxy_external_expdisk.csv
reports/morphological_memory_history_proxy.md
```

This layer records the caution that the currently observed galaxy morphology may
be an insufficient proxy for the Tau Core readout-relevant morphology: a galaxy
may not always have had its current structure, and a 4D readout may encode an
integrated or delayed morphology/history component. The current diagnostic
combines source-side morphology/context flags with the rotation-inferred family
preference. It is therefore a hypothesis layer only, not an accepted morphology
label and not an endpoint score. In the current run, the current proxy family and
rotation-inferred family disagree in `113/175` rows; within the 13 externally
supported exponential-disk rows, `9/13` do not infer the exponential-disk readout
family. This marks targets for future residual-blind history or morphology-memory
observables.

The morphology inspection queue is generated by:

```bash
python scripts/build_morphology_inspection_queue.py
```

This writes:

```text
data/derived/morphology_inspection_queue.csv
data/derived/morphology_inspection_queue_summary.csv
reports/morphology_inspection_queue.md
```

The queue turns the memory/history proxy layer into a concrete source-acquisition
plan. It ranks galaxies for residual-blind morphology inspection and records
which external observables to request, such as deep outer-disk/LSB profiles, HI
extent or asymmetry, vertical/flaring/projection checks, bulge/disk
decomposition, bar lengths, or velocity-field support. It is not an accepted
morphology manifest and does not change endpoint labels. In the current run, the
queue contains `4` P0 and `18` P1 inspection targets. The P0 targets are
`NGC0300`, `NGC6503`, `NGC0100`, and `NGC0247`.

The P0 morphology inspection packets are generated by:

```bash
python scripts/build_p0_morphology_inspection_packets.py
```

This writes:

```text
data/derived/p0_morphology_inspection_packet_index.csv
data/derived/p0_morphology_inspection_source_needs.csv
reports/p0_morphology_inspection_packets.md
reports/p0_morphology_packets/NGC0100.md
reports/p0_morphology_packets/NGC0247.md
reports/p0_morphology_packets/NGC0300.md
reports/p0_morphology_packets/NGC6503.md
```

The packets are blank residual-blind review templates. They summarize existing
SPARC/S4G context, list requested observables, provide catalogue lookup links,
and reserve empty fields for future image/decomposition/history review. They
forbid endpoint residual gain, required-`S_tau`, best-fit readout family, and
post-hoc family switching as inputs. Across all four P0 packets the shared
source needs are residual-blind multiband morphology labels, deep outer-disk
profiles, and HI extent/asymmetry checks; `NGC0247` additionally requests bar
length and velocity-field support.

The P0 external imaging request manifest is generated by:

```bash
python scripts/build_p0_external_imaging_request_manifest.py
```

This writes:

```text
data/derived/p0_external_imaging_request_manifest.csv
data/derived/p0_external_imaging_request_summary.csv
reports/p0_external_imaging_request_manifest.md
```

This converts the four P0 packets into concrete source requests with S4G-derived
coordinates, suggested fields of view, and residual-blind lookup URLs for DSS2,
2MASS, WISE, NED, and SIMBAD. The current suggested fields are `8.000` arcmin
for `NGC0100`, `29.745` arcmin for `NGC0247`, `20.288` arcmin for `NGC0300`,
and `10.030` arcmin for `NGC6503`. The manifest does not download, classify, or
interpret images; it prepares the next residual-blind image/decomposition review.

The local P0 external imaging review dashboard is generated by:

```bash
python scripts/build_p0_external_imaging_review_dashboard.py
```

This writes:

```text
data/derived/p0_external_imaging_review_dashboard_index.csv
reports/p0_external_imaging_review_dashboard.html
```

Open the dashboard HTML in a browser to review all four P0 galaxies from one
offline launch page. It contains the external source links, requested observable
chips, and blank review checklists. It does not embed accepted morphology labels
or endpoint scores.

The P0 SkyView availability audit is generated by:

```bash
python scripts/audit_p0_skyview_availability.py
```

This writes:

```text
data/derived/p0_skyview_availability_audit.csv
data/derived/p0_skyview_availability_summary.csv
reports/p0_skyview_availability_audit.md
```

The audit checks whether the P0 DSS2 Red, 2MASS-K, and WISE W1 source requests
return at least one SkyView image candidate. It does not download, classify, or
interpret images, and it does not write temporary SkyView FITS URLs to disk. In
the current run all 12 P0 requests are available: `4/4` DSS2 Red, `4/4` 2MASS-K,
and `4/4` WISE W1.

The P0 SkyView preview images are generated by:

```bash
python scripts/acquire_p0_skyview_preview_images.py
```

This writes:

```text
data/derived/p0_skyview_preview_image_manifest.csv
data/derived/p0_skyview_preview_image_summary.csv
reports/p0_skyview_preview_images.md
reports/p0_skyview_previews/*.png
```

This renders 12 local PNG preview panels, one for each P0 galaxy and survey
pair. In the current run all 12 previews render successfully at `300x300`
pixels. These previews are source material for residual-blind human review only;
no image classification, accepted morphology label, or endpoint score is emitted.

The P0 residual-blind visual review template is generated by:

```bash
python scripts/build_p0_visual_review_template.py
```

This writes:

```text
data/derived/p0_visual_review_template.csv
data/derived/p0_visual_review_field_schema.csv
reports/p0_visual_review_template.md
reports/p0_visual_review_form.html
```

The template embeds the 12 preview panels into a local review form and initializes
all reviewer fields as `TO_BE_FILLED_RESIDUAL_BLIND`. The fields include
present-day morphology, outer-disk/LSB/tail evidence, HI asymmetry evidence,
bar/m=2 support, projection caveats, vertical/flare/warp evidence, compact/bulge
support, ring/resonance evidence, a morphological memory/history proxy judgment,
review confidence, source list, and a residual-blind family recommendation for a
future endpoint. It is still not an accepted morphology manifest: endpoint
residual gains, required-`S_tau` diagnostics, best-fit readout families,
MOND/RAR/TGP comparison scores, and post-hoc family switching remain forbidden
inputs.

The P0 visual review completion gate is generated by:

```bash
python scripts/run_p0_visual_review_completion_gate.py
```

This writes:

```text
data/derived/p0_visual_review_completion_gate.csv
data/derived/p0_visual_review_completion_summary.csv
reports/p0_visual_review_completion_gate.md
```

This gate checks whether the residual-blind visual review template has actually
been filled before it can be considered for accepted-manifest promotion. In the
current package the decision is `BLOCKED_VISUAL_REVIEW_PENDING`: all four P0
rows remain blocked and all 60 reviewer fields are still placeholders. This is a
protocol safeguard, not a negative empirical result and not an endpoint score.

The P0 visual review handoff package is generated by:

```bash
python scripts/build_p0_visual_review_handoff.py
```

This writes:

```text
data/derived/p0_visual_review_handoff_tasks.csv
data/derived/p0_visual_review_handoff_summary.csv
reports/p0_visual_review_handoff.md
reports/p0_visual_review_handoff.html
```

The handoff translates the blocked completion gate into concrete reviewer tasks.
It lists the required residual-blind fields, the local preview panels, allowed
source types, and forbidden endpoint-derived inputs for each P0 galaxy. In the
current package it is `READY_FOR_RESIDUAL_BLIND_HUMAN_REVIEW`, while accepted
manifest promotion and endpoint scoring remain disallowed.

The P0 visual review response intake template is generated by:

```bash
python scripts/build_p0_visual_review_response_intake.py
```

This writes:

```text
data/derived/p0_visual_review_response_template.csv
data/derived/p0_visual_review_response_schema.csv
data/derived/p0_visual_review_response_validation.csv
data/derived/p0_visual_review_response_summary.csv
reports/p0_visual_review_response_intake.md
```

This is the reviewer-response contract for the next residual-blind hand review.
It separates the file to be filled from the endpoint machinery and validates
whether the response is complete enough for a later independent accepted-manifest
audit. In the current package the decision is
`BLOCKED_REVIEW_RESPONSE_PENDING`: all four rows are blocked and 56 required
review-response fields remain pending.

The P0 response-to-manifest promotion gate is generated by:

```bash
python scripts/run_p0_response_to_manifest_promotion_gate.py
```

This writes:

```text
data/derived/p0_response_to_manifest_promotion_gates.csv
data/derived/p0_response_to_manifest_promotion_summary.csv
reports/p0_response_to_manifest_promotion_gate.md
```

This gate decides whether completed visual-review responses may enter an
independent accepted morphology-manifest audit. In the current package the
decision is `BLOCKED_RESPONSE_REVIEW_NOT_PROMOTABLE`: the response intake is not
complete, review confidence is missing, residual-blind family recommendations
are missing, and morphology-memory/history judgments are missing. It creates no
accepted labels and computes no endpoint scores.

The P0 missing-data source acquisition plan is generated by:

```bash
python scripts/build_p0_missing_data_source_acquisition_plan.py
```

This writes:

```text
data/derived/p0_missing_data_source_acquisition_plan.csv
data/derived/p0_missing_data_source_acquisition_summary.csv
data/derived/p0_missing_data_source_acquisition_by_galaxy.csv
reports/p0_missing_data_source_acquisition_plan.md
```

This layer operationalizes the requested source policy: use S4G, NED/NED-D,
DustPedia, HI survey data, and PHANGS for the missing residual-blind P0
morphology inputs. It maps each empty review field to source families, including
HI extent/asymmetry checks for outer-disk and morphology-memory/history support
and PHANGS/S4G checks for optional bar or velocity-field evidence. It is a
source-acquisition plan only; all tasks remain
`TO_BE_ACQUIRED_RESIDUAL_BLIND`, accepted-label creation is disabled, and no
endpoint scores are computed.

The P0 DustPedia/HI/PHANGS source evidence pass is generated by:

```bash
python scripts/acquire_p0_dustpedia_hi_phangs_sources.py
```

This writes:

```text
data/derived/p0_dustpedia_source_matches.csv
data/derived/p0_phangs_public_sample.csv
data/derived/p0_phangs_source_matches.csv
data/derived/p0_hi_source_evidence.csv
data/derived/p0_external_source_evidence_summary.csv
reports/p0_dustpedia_hi_phangs_source_evidence.md
```

This pass actually queries the requested external source families. In the
current package, DustPedia direct matches are found for `NGC0300` only, PHANGS
public sample coverage is not found for the four P0 galaxies, and SPARC HI
mass/radius evidence is present for all four P0 galaxies. These are source
evidence records, not accepted morphology labels.

The source-assisted P0 review response draft is generated by:

```bash
python scripts/build_p0_source_assisted_review_response_draft.py
```

This writes:

```text
data/derived/p0_source_assisted_review_response_draft.csv
data/derived/p0_source_assisted_review_response_validation.csv
reports/p0_source_assisted_review_response_draft.md
```

This draft fills review-response fields from the acquired source evidence, but
it remains blocked from accepted-label promotion. It is not a human
residual-blind review response, not an accepted morphology manifest, and not an
endpoint score.

The Codex/source-reviewed P0 response is generated by:

```bash
python scripts/build_p0_codex_source_review_response.py
```

This writes:

```text
data/derived/p0_codex_source_review_response.csv
data/derived/p0_codex_source_review_validation.csv
reports/p0_codex_source_review_response.md
```

It also fills the P0 response-intake files used by the promotion gate:

```text
data/derived/p0_visual_review_response_template.csv
data/derived/p0_visual_review_response_validation.csv
data/derived/p0_visual_review_response_summary.csv
```

In the current package all four P0 rows pass the source-review response
validator as `READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT`. This is a
Codex/source review, not a human visual review and not an endpoint score. It
uses S4G Pipeline 4 components and scales, SPARC HI mass/radius evidence,
DustPedia/VizieR source matches, PHANGS public sample coverage checks, and
NED/SIMBAD/SkyView lookup material. Forbidden endpoint-derived inputs remain
excluded.

The P0 Codex-source-reviewed label manifest is generated by:

```bash
python scripts/build_p0_codex_accepted_label_manifest.py
```

This writes:

```text
data/derived/p0_codex_accepted_label_manifest.csv
data/derived/p0_codex_accepted_label_manifest_summary.csv
reports/p0_codex_accepted_label_manifest.md
```

In the current package the decision is
`P0_CODEX_SOURCE_REVIEW_LABELS_CREATED_NOT_ENDPOINT`: four P0 source-reviewed
audit labels are created, all with `K_exponential_disk` as the residual-blind
family recommendation and explicit caveats where needed. These are not full
175-galaxy endpoint labels and no endpoint scores are computed.

The P0 readout-relevant morphology proxy is generated by:

```bash
python scripts/build_p0_readout_relevant_morphology_proxy.py
```

This writes:

```text
data/derived/p0_readout_relevant_morphology_proxy.csv
data/derived/p0_readout_relevant_morphology_proxy_summary.csv
reports/p0_readout_relevant_morphology_proxy.md
```

This layer separates the apparent 4D morphology handle from the possible
Tau-side readout-relevant proxy. In the current P0 set all four rows have the
apparent 4D handle `K_exponential_disk`, but the source-side caveats split them
into a clean exponential-disk control, a projection-corrected expdisk candidate,
a barred/m=2 overlay candidate, and a compact-core overlay candidate. This is
not an endpoint label; it is the bridge-consistent caution that thin/thick
disk, bar, ring, compact, and tail classes are projected 4D morphology handles,
not proven fundamental Tau-side classes.

The central bridge rule is therefore `F = F_{K_readout}`, not automatically
`F = F_{K_obs}`. This follows from the Tau Core bridge interpretation of
morphology as a projection/readout structure: a present-day 4D morphology label
may need projection, overlay, or memory/history correction before it can select
a readout shell. The emitted proxy table now carries this distinction
operationally through `k_obs`, `k_readout`, `readout_proxy_source`,
`promotion_status`, and `formula_shell`; the formula shell is attached to
`k_readout`.

The narrow P0 Codex/source-reviewed pilot is generated by:

```bash
python scripts/run_p0_codex_source_review_pilot.py
```

This writes:

```text
data/derived/p0_codex_source_review_pilot_scores.csv
data/derived/p0_codex_source_review_pilot_summary.csv
reports/p0_codex_source_review_pilot.md
```

This pilot consumes only the four P0 source-reviewed audit labels. Under the
primary leave-one-galaxy-out all13 exponential-disk policy, the Tau readout
beats TPG/v6 in `0.75` of the P0 cases and beats MOND in `0.25` of the P0
cases. The formula-shell proxy slice beats the wrong-family mean and TPG/v6 in
`1.0` of the P0 cases, but still beats MOND in only `0.25` of them. This is a
useful narrow pilot signal, not the frozen 175-galaxy endpoint and not empirical
validation. The score table also records `scored_formula_shell`: in this narrow
pilot it remains the direct `K_exponential_disk` control, while three P0 rows
are marked `readout_proxy_overlay_not_scored=True` because their projection,
bar/m=2, or compact-core readout proxy shell has not yet been scored.

The P0 requested source-family availability audit is generated by:

```bash
python scripts/audit_p0_requested_source_family_availability.py
```

This writes:

```text
data/derived/p0_requested_source_family_availability.csv
data/derived/p0_requested_source_family_availability_summary.csv
reports/p0_requested_source_family_availability.md
```

This is the next source-side test. It checks the P0 acquisition plan against
the currently available source paths without classifying morphology. In the
current package, S4G is partially source-ready for the P0 galaxies through
existing crossmatches and disk-scale candidates, NED/NED-D lookup paths are
ready, DustPedia is directly matched only for `NGC0300`, HI mass/radius
evidence is ready for all four P0 galaxies through SPARC, and PHANGS public
sample coverage is not found for the four P0 galaxies. It is not an accepted
morphology manifest and not an endpoint score.

The consolidated P0 review pipeline status dashboard is generated by:

```bash
python scripts/build_p0_review_pipeline_status_dashboard.py
```

This writes:

```text
data/derived/p0_review_pipeline_status.csv
data/derived/p0_review_pipeline_status_summary.csv
reports/p0_review_pipeline_status_dashboard.md
reports/p0_review_pipeline_status_dashboard.html
```

This dashboard summarizes the source-request, SkyView availability, preview,
template, completion, handoff, response-intake, promotion-gate, P0 source-label,
and missing-data source-acquisition/source-availability stages. In the current
package the overall decision is
`P0_CODEX_SOURCE_REVIEW_LABELS_READY_FULL_ENDPOINT_BLOCKED`: the P0
Codex/source-reviewed audit-label lane is populated, while full endpoint labels
and endpoint scoring remain disabled.

## arXiv Source Package

Build the arXiv source package directly with:

```bash
python scripts/build_arxiv_source.py
```

This writes:

```text
arxiv_submission_source.zip
```

The ZIP is built from `paper8_submission_source/` and excludes the compiled PDF
and temporary LaTeX build files.

## Scope

This repository is a reproducibility package for Paper 8 only. It excludes raw
SPARC downloads, private workbench outputs, endpoint-fitting notebooks, and
broad Tau Core theory-hub material that is not needed to verify the paper
package.
