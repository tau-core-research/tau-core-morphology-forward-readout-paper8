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

The paper uses morphology and projection as related but non-identical notions.
`K_obs` is the catalogue or visually supported 4D morphology handle.
`K_present` is the present source-observed morphology state. `K_readout` is the
readout-relevant morphology/projection state that can select a formula shell.
`O_path` contains observer/path projection information, and `Theta_tau`
contains source-frozen Tau-side morphology trajectory or phase information.
Thus a phrase such as "morphology-specific formula" should be read as
"morphology-projection readout family" unless the context explicitly restricts
the kernel to a pure present-day morphology proxy.

The deeper object behind these operational handles is the Tau morphology
state: a source-side organizing configuration whose different 4D readouts may
appear as visible morphology, matter distribution, gravity response,
trajectory/phase, observer/path appearance, or clock/time projection.  In this
language `Theta_morph` is a morphology-state phase/history readout, while
`Xi_t` is a clock/time-projection readout.  They may share source evidence, but
they are not the same channel and must pass a non-overlap ledger before any
combined endpoint claim.

This is an open channel hierarchy, not a fixed two-term model. Other
projections of the same internal Tau morphology state may also affect the
rotation readout, such as mass-distribution, metric/closure, coherence/phase,
or source-observer path/environment projections. Operationally, a new channel
is allowed into a score only after it is source-frozen, assigned to a distinct
ledger channel, checked for overlap with active kernels, and ablated against
the lower-channel model. Otherwise it remains theory motivation.

The deeper object behind these handles is called a `Tau morphology state`.
This is not a visible galaxy-shape class. It is a Tau-side organizing
configuration whose different 4D readouts may appear as visible morphology,
matter/mass distribution, gravity or metric response, time/clock structure,
observer/path appearance, and quantum/coherence structure. The papers use this
term as theory motivation and claim-boundary discipline; the numerical tests
still operate only on source-frozen manifests and endpoint scores.

Consequence for residuals: in Tau Core a rotation-curve residual is not
assumed to be generated only by the local 4D baryonic mass density at the same
radius. It may be the 4D readout of several source-frozen channels of the
deeper Tau morphology state: baryonic distribution, metric/closure response,
observer/path projection, envelope/history/phase structure, or other
admissible readout channels. This is not a fitting license; every channel must
be residual-blind, ledger-separated, and ablated before endpoint scoring.

The bridge also treats observer/path projection as morphology-trajectory
dependent. The observer/projection layer is not merely an inclination
correction: a source-frozen `K_readout` may depend on present morphology,
observer/path geometry, Tau-side morphology trajectory or phase, and
projection-history environment. In this usage, morphology trajectory is not
limited to past-memory traces. If 4D past, present, and future morphology are
different readout slices of the same deeper Tau-side configuration, then
source-frozen relaxation, settling, accretion, or future-directed phase proxies
may enter the readout state. These terms are allowed only when supported by
residual-blind source evidence, not by endpoint residuals or best-fit family
selection.

The bridge now also isolates a stronger time-readout projection channel. In
that channel, the observed rotation can be affected because the projection
selects a different clock/readout slice than the Newtonian closure-test clock.
The first shell is `v_obs^2 = Xi_t^2 [v_Newt^2 + delta_v_grav/morph^2]`, with
`Xi_t = 1` as the Newtonian clock-readout limit. `Xi_t` is formula-conditional:
it must be frozen from residual-blind source/path/time-readout evidence before
scoring and cannot be inferred from the rotation residual.

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

For projection-enriched cases the bridge refines this to:

```text
K_obs
  -> source-frozen present morphology
     + observer/path projection
     + Tau-side morphology trajectory/phase
     + projection-history environment
  -> K_readout
  -> formula shell:
       delta_v_proj^2(R)
       = sum_j A_j(source)
               w_j(R, O_obs/path, Theta_morph)
               K_j(R; K_present, Theta_morph)
  -> replay / endpoint score
```

The time-readout branch refines the replay shell to:

```text
v_obs^2(R)
  =
  Xi_t^2(R; O_obs/path, Theta_morph, E_proj/history)
  *
  [v_Newt^2(R) + delta_v_grav/morph^2(R)]
```

The current full-time morphology replay is only a diagnostic proxy for this
branch, not a source-complete accepted `Xi_t(R)` endpoint.

When the diagnostic time/projection layer worsens a galaxy, the repository now
records the reason instead of treating the row as a tunable failure. NGC4013
worsens because the active mixed warp/vertical-overlay kernel already carries
the source geometry that the generic `Xi_t` proxy would rescale. NGC7331
worsens more mildly because the broad vertical/outer-warp window already
contains the available phase information. In both cases the operational rule is
to keep `Xi_t = 1` unless independent, non-overlapping clock/readout evidence
is frozen before scoring.

The problematic-galaxy projection-channel ledger is generated by:

```bash
python scripts/build_problematic_galaxy_projection_channel_ledger.py
```

It writes:

```text
data/derived/problematic_galaxy_projection_channel_ledger.csv
data/derived/problematic_galaxy_projection_channel_summary.csv
reports/problematic_galaxy_projection_channel_ledger.md
```

The current ledger does not open any endpoint score. It says that UGC12506
should next test a source-frozen mass/envelope plus metric-closure channel,
NGC4088 should keep clock readout as a control on top of the accepted
warp/history route, NGC4013 and NGC7331 should not promote the current `Xi_t`
proxy, NGC5907 is projection-saturated at the present proxy level, and NGC4183
remains a weak/null projection control.

The ledger is converted into executable next gates by:

```bash
python scripts/build_problematic_projection_channel_next_gates.py
```

It writes:

```text
data/derived/problematic_projection_channel_next_gates.csv
data/derived/problematic_projection_channel_next_gates_summary.csv
reports/problematic_projection_channel_next_gates.md
```

The current next-gate artifact is still not an endpoint permission artifact:
`n_endpoint_allowed = 0`. It opens only two control/replay paths. UGC12506 may
continue through the source-native NFW/HSE mass-envelope plus metric-closure
ablation gate, and NGC4088 keeps its accepted additive warp/history route while
clock readout remains a control. NGC4013 is explicitly blocked for the current
generic `Xi_t` proxy, NGC7331 needs source-sharpened outer-warp/vertical
windowing before a refined replay, NGC5907 is saturated at the present
projection proxy level, and NGC4183 remains the weak/null control.

The UGC12506 source-native NFW/HSE replay is generated by:

```bash
python scripts/build_ugc12506_source_native_nfw_hse_shell.py
python scripts/run_ugc12506_source_native_nfw_hse_replay.py
```

It writes:

```text
data/derived/ugc12506_source_native_nfw_hse_replay_summary.csv
data/derived/ugc12506_source_native_nfw_hse_replay_scores.csv
figures/endpoint_diagnostics/ugc12506_source_native_nfw_hse_replay.png
reports/ugc12506_source_native_nfw_hse_replay.md
```

Current result: the source-native NFW/HSE branch improves the older
`R_d`-proxy NFW/HSE control slightly (`77.86 -> 77.54 km/s` RMSE), improves
strongly over the pure envelope/edge-on source branches (`~102.45 -> 77.54
km/s` RMSE), and improves over the baryonic carrier (`116.02 -> 77.54 km/s`
RMSE). It still does not reach the prior diagnostic Tau/MOND/TPG-level
references (`best diagnostic RMSE = 37.36 km/s`). Thus it is evidence that
UGC12506 needs a real mass/envelope plus closure channel, but not yet a
source-complete endpoint solution.

The fixed-shape normalization diagnostic and the first source-derived
beta-closure replay are generated by:

```bash
python scripts/run_ugc12506_source_native_nfw_hse_normalization_diagnostic.py
python scripts/run_ugc12506_source_derived_beta_closure_replay.py
```

The residual-aware diagnostic finds the required velocity-squared multiplier
`beta_diag = 3.876` and lowers RMSE to `7.48 km/s`; this is diagnostic only
because it uses the observed curve to set beta. The source-derived candidate

```text
beta_cl = 1
          + (lambda_spin / 0.10) * (chi2_iso / chi2_NFW - 1)_+
          + sin^2(i) * max((i - 80 deg) / 10 deg, 0)
```

uses only source-frozen spin, Table-5 NFW preference, and inclination. For
UGC12506 it gives `beta_cl = 3.954`, within about `2.1%` of the diagnostic
normalization, and scores `7.67 km/s` RMSE. This is a strong shape/source
normalization candidate, but it is still post-diagnostic and must be
predeclared and transferred to independent high-spin edge-on systems before it
can be treated as an endpoint-grade normalization law.

The independent transfer predeclaration is generated by:

```bash
python scripts/build_ugc12506_beta_closure_transfer_predeclaration.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_transfer_candidates.csv
data/derived/ugc12506_beta_closure_transfer_source_worklist.csv
data/derived/ugc12506_beta_closure_transfer_predeclaration_summary.csv
reports/ugc12506_beta_closure_transfer_predeclaration.md
```

The current gate finds 11 non-UGC12506 SPARC proxy candidates and allows no
replay or endpoint score yet. The top source-acquisition targets are
`UGC11455`, `ESO563-G021`, `IC4202`, `NGC0891`, `NGC4013`, `NGC2841`,
`NGC4157`, and `NGC4217`. Each requires source-native `lambda_spin`,
`chi2_NFW`, `chi2_ISO`, halo-fit provenance, and PV/envelope notes before the
`beta_cl` rule can be replayed as an independent transfer test.

The first source-acquisition blocker is reduced by:

```bash
python scripts/acquire_ugc12506_beta_closure_transfer_halo_fit_fields.py
```

It caches the Li et al. (2020) SPARC halo-model catalogue through VizieR and
writes:

```text
data/external/literature/li2020_sparc_halo_catalog/table1_vizier.tsv
data/derived/ugc12506_beta_closure_transfer_halo_fit_fields.csv
data/derived/ugc12506_beta_closure_transfer_halo_fit_worklist_update.csv
data/derived/ugc12506_beta_closure_transfer_halo_fit_acquisition_summary.csv
reports/ugc12506_beta_closure_transfer_halo_fit_acquisition.md
```

All 11 candidates now have pISO/NFW reduced-chi2 fields filled, but endpoint
replay remains blocked because `lambda_spin` and PV/envelope evidence are still
unfrozen. The halo-fit acquisition also shows that the highest edge-on/massive
H I proxy targets are not automatically UGC12506-like NFW-preference systems:
positive `nfw_preference_load` appears for `NGC0891`, `NGC7331`, `NGC2841`,
`NGC0801`, and weakly `NGC4013`.

The post-halo prioritization gate is:

```bash
python scripts/build_ugc12506_beta_closure_transfer_priority_gate.py
```

It promotes no endpoint score. It narrows the immediate transfer source-review
queue to two primary NFW-preference targets, `NGC0891` and `NGC7331`, keeps
`NGC2841`, `NGC0801`, and `NGC4013` as weak/secondary transfer targets, and
preserves the pISO-preferred rows as controls or alternative-branch candidates.

The primary target source-freeze preflight is:

```bash
python scripts/build_ugc12506_beta_closure_primary_source_freeze_preflight.py
```

It accepts PV/envelope context for both `NGC0891` and `NGC7331`, but freezes no
`lambda_spin` value. Consequently `beta_cl` replay and endpoint scoring remain
blocked. The next admissible gate is either a direct source-native spin
acquisition or a predeclared source-only spin-proxy rule, before inspecting any
transfer residual.

The direct lambda/spin source-acquisition gate is:

```bash
python scripts/acquire_ugc12506_beta_closure_direct_lambda_spin_sources.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_direct_lambda_spin_source_evidence.csv
data/derived/ugc12506_beta_closure_direct_lambda_spin_source_gate_summary.csv
reports/ugc12506_beta_closure_direct_lambda_spin_source_gate.md
```

Current status: no direct value is accepted for the `beta_cl` `lambda_spin`
slot. `NGC7331` has a published disc-spin-like value, `lambda = 0.423`, from a
lognormal self-gravitating disc model, but this is a definition mismatch rather
than a direct halo/envelope `lambda_spin` replacement. `NGC0891` remains direct
lambda blocked; NGC891-like simulation context is model-analogue only.

The NGC0891 spin-source hunt update is:

```bash
python scripts/acquire_ugc12506_beta_closure_ngc0891_spin_source_hunt_update.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_ngc0891_spin_source_hunt_update_sources.csv
data/derived/ugc12506_beta_closure_ngc0891_spin_source_hunt_update_worklist.csv
data/derived/ugc12506_beta_closure_ngc0891_spin_source_hunt_update_summary.csv
reports/ugc12506_beta_closure_ngc0891_spin_source_hunt_update.md
```

Status: `NGC0891_CONTEXT_STRENGTHENED_DIRECT_LAMBDA_STILL_BLOCKED`. Four
NGC891/NGC0891 halo/extraplanar-gas sources strengthen the envelope/projection
context, but none supplies a direct dimensionless `beta_cl` `lambda_spin`
measurement. Replay remains blocked.

The NGC7331 definition-conversion gate is:

```bash
python scripts/build_ugc12506_beta_closure_lambda_definition_conversion_gate.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_lambda_definition_conversion_checks.csv
data/derived/ugc12506_beta_closure_lambda_definition_conversion_comparison.csv
data/derived/ugc12506_beta_closure_lambda_definition_conversion_worklist.csv
data/derived/ugc12506_beta_closure_lambda_definition_conversion_summary.csv
reports/ugc12506_beta_closure_lambda_definition_conversion_gate.md
```

Verdict: `NGC7331_DISC_LAMBDA_CONTEXT_ACCEPTED_DIRECT_SUBSTITUTION_REJECTED`.
The Marr value remains useful source-side angular-momentum context, but direct
substitution is rejected. A residual-blind disc-to-halo/envelope conversion
functional is required before it can replace the `lambda_spin_proxy` slot.

The Bullock-like disk-inferred spin conversion proxy gate is:

```bash
python scripts/build_ugc12506_beta_closure_bullock_spin_conversion_proxy_gate.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv
data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_comparison.csv
data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_checks.csv
data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_summary.csv
reports/ugc12506_beta_closure_bullock_spin_conversion_proxy_gate.md
```

Status: `BULLOCK_DISK_INFERRED_SPIN_PROXY_COMPUTED_REVIEW_REQUIRED`. This
gate computes the residual-blind conversion proxy
`lambda'_disk = j_disk / (sqrt(2) R200 V200)` with
`j_disk = 2 Rdisk Vflat` and `R200 = V200/(10 H0)`, using SPARC source fields
and Li2020 NFW-flat `V200`. It is a conservative angular-momentum control:
`NGC0891` gives `lambda'_disk ~= 0.035`, while the earlier exposure proxy gives
`lambda_spin_proxy ~= 0.149`. The discrepancy is not replay permission; it is
the reason an independent reviewer must choose between direct spin acquisition,
the exposure proxy, the Bullock-like conversion proxy, or rejection of the
route.

The predeclared source-only spin-proxy gate is:

```bash
python scripts/build_ugc12506_beta_closure_source_declared_spin_proxy_gate.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_source_declared_spin_proxy_fields.csv
data/derived/ugc12506_beta_closure_source_declared_spin_proxy_transfer_queue.csv
data/derived/ugc12506_beta_closure_source_declared_spin_proxy_gate_summary.csv
reports/ugc12506_beta_closure_source_declared_spin_proxy_gate.md
```

This gate declares a bounded residual-blind proxy candidate,
`lambda_spin_proxy = 0.10 * (1 + 0.35 extent_load + 0.25 velocity_load +
0.25 gas_load + 0.15 edgeon_load)`, using only `RHI/Rdisk`, `Vflat`, H I mass,
and inclination. It is not accepted as a direct `lambda_spin` measurement and
authorizes no replay or endpoint score. It changes the next source-review queue:
`NGC0891` is the only primary proxy-transfer review target, while `NGC7331`,
`NGC2841`, `NGC0801`, and `NGC4013` remain secondary transfer-review targets.

The independent spin-proxy review bundle is:

```bash
python scripts/build_ugc12506_beta_closure_spin_proxy_review_bundle.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_spin_proxy_review_packet.csv
data/derived/ugc12506_beta_closure_spin_proxy_review_obligations.csv
data/derived/ugc12506_beta_closure_spin_proxy_review_forbidden_inputs.csv
data/derived/ugc12506_beta_closure_spin_proxy_review_response_template.csv
data/derived/ugc12506_beta_closure_spin_proxy_review_bundle_manifest.csv
data/derived/ugc12506_beta_closure_spin_proxy_review_bundle_summary.csv
reports/ugc12506_beta_closure_spin_proxy_review_prompt.md
reports/ugc12506_beta_closure_spin_proxy_review_bundle.md
review_bundles/ugc12506_beta_closure_spin_proxy_review_bundle.zip
```

Status: `U12506_BETA_SPIN_PROXY_REVIEW_BUNDLE_READY_RESPONSE_PENDING`.
The bundle is for residual-blind independent review only. It includes both the
source-declared exposure proxy and the Bullock-like disk-inferred conversion
proxy, but promotes neither. It does not authorize `beta_cl` replay and keeps
endpoint scoring false.
The response form now requires an explicit `selected_spin_normalization_route`
decision: `EXPOSURE_PROXY`, `BULLOCK_DISK_CONVERSION`,
`DIRECT_SOURCE_NATIVE_SPIN`, `NEW_RESIDUAL_BLIND_RULE`, or rejection/blocking
via the review decisions.

The review-response intake validator is:

```bash
python scripts/run_ugc12506_beta_closure_spin_proxy_review_response_intake.py
```

With no completed reviewer CSV present, the current status is
`U12506_BETA_SPIN_PROXY_REVIEW_RESPONSE_PENDING_ENDPOINT_BLOCKED`. The proxy
promotion gate, `beta_cl` replay preflight, and endpoint scoring all remain
false. The selected spin-normalization route remains
`PENDING_INDEPENDENT_REVIEW`.

The downstream spin-route prefreeze gate is:

```bash
python scripts/build_ugc12506_beta_closure_spin_route_prefreeze_gate.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_spin_route_prefreeze_gate.csv
data/derived/ugc12506_beta_closure_spin_route_prefreeze_values.csv
data/derived/ugc12506_beta_closure_spin_route_prefreeze_summary.csv
reports/ugc12506_beta_closure_spin_route_prefreeze_gate.md
```

Current status:
`U12506_BETA_SPIN_ROUTE_PREFREEZE_BLOCKED_REVIEW_ROUTE_PENDING`. This gate is
the replay-side lock: even after the proxy bundle exists, no transfer prefreeze
values are emitted until an independent response selects a spin-normalization
route. Endpoint scoring remains false.

The spin-route decision matrix is:

```bash
python scripts/build_ugc12506_beta_closure_spin_route_decision_matrix.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_spin_route_decision_matrix.csv
data/derived/ugc12506_beta_closure_spin_route_decision_matrix_summary.csv
reports/ugc12506_beta_closure_spin_route_decision_matrix.md
```

Status:
`U12506_BETA_SPIN_ROUTE_DECISION_MATRIX_READY_REVIEW_REQUIRED`. It compares four
routes: `EXPOSURE_PROXY`, `BULLOCK_DISK_CONVERSION`,
`DIRECT_SOURCE_NATIVE_SPIN`, and `REJECT_ROUTE`. The preferred scientific route
is still direct source-native halo/envelope spin, but the current practical
reviewable routes are the exposure proxy and Bullock-like disk conversion. The
matrix chooses none of them and authorizes no replay.

The beta-closure scoring launch gate is:

```bash
python scripts/build_ugc12506_beta_closure_scoring_launch_gate.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_scoring_launch_inputs.csv
data/derived/ugc12506_beta_closure_scoring_launch_gates.csv
data/derived/ugc12506_beta_closure_scoring_protocol_skeleton.csv
data/derived/ugc12506_beta_closure_scoring_launch_summary.csv
reports/ugc12506_beta_closure_scoring_launch_gate.md
```

Current status:
`U12506_BETA_CLOSURE_SCORING_LAUNCH_BLOCKED_REVIEW_PREFREEZE_PENDING`.
All nine required launch inputs exist, but the review route, prefreeze value,
and carrier-freeze gates are blocked. This is the last non-scoring gate: the
future scoring script may read `vobs` only after a formula manifest is frozen
from accepted spin-route values and an accepted carrier.

The beta-closure transfer carrier-freeze gate is:

```bash
python scripts/build_ugc12506_beta_closure_transfer_carrier_freeze_gate.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_transfer_carrier_route_decision_matrix.csv
data/derived/ugc12506_beta_closure_transfer_carrier_manifest.csv
data/derived/ugc12506_beta_closure_transfer_carrier_freeze_gates.csv
data/derived/ugc12506_beta_closure_transfer_carrier_freeze_summary.csv
reports/ugc12506_beta_closure_transfer_carrier_freeze_gate.md
```

Current status:
`U12506_BETA_CLOSURE_TRANSFER_CARRIER_FREEZE_BLOCKED_CARRIER_REVIEW_PENDING`.
The gate records three carrier routes: a reviewable-but-not-accepted
`BARYONIC_050_FAST_PACKET` stress carrier, a `LI2020_NFW_FIT_CARRIER`
diagnostic/control route that is not endpoint-safe by default because it uses
published rotation-curve fit products, and a preferred-but-missing
`SOURCE_NATIVE_NFW_HSE_TRANSFER_CARRIER`. No carrier row is frozen.

The carrier review bundle and response intake are:

```bash
python scripts/build_ugc12506_beta_closure_carrier_review_bundle.py
python scripts/run_ugc12506_beta_closure_carrier_review_response_intake.py
```

They write:

```text
data/derived/ugc12506_beta_closure_carrier_review_bundle_summary.csv
data/derived/ugc12506_beta_closure_carrier_review_obligations.csv
data/derived/ugc12506_beta_closure_carrier_review_forbidden_inputs.csv
data/derived/ugc12506_beta_closure_carrier_review_response_template.csv
data/derived/ugc12506_beta_closure_carrier_review_response_intake_summary.csv
data/derived/ugc12506_beta_closure_carrier_review_response_intake_checks.csv
review_bundles/ugc12506_beta_closure_carrier_review_bundle.zip
reports/ugc12506_beta_closure_carrier_review_bundle.md
reports/ugc12506_beta_closure_carrier_review_response_intake.md
```

Current status:
`U12506_BETA_CARRIER_REVIEW_BUNDLE_READY_RESPONSE_PENDING` and
`U12506_BETA_CARRIER_REVIEW_RESPONSE_PENDING_ENDPOINT_BLOCKED`. A future
independent response can accept the minimal baryonic stress carrier, require a
source-native transfer carrier, or reject the route. Until then, no carrier row
is frozen.

The beta-closure transfer formula-freeze gate is:

```bash
python scripts/build_ugc12506_beta_closure_transfer_formula_freeze_gate.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_transfer_formula_manifest.csv
data/derived/ugc12506_beta_closure_transfer_formula_freeze_gates.csv
data/derived/ugc12506_beta_closure_transfer_formula_freeze_summary.csv
reports/ugc12506_beta_closure_transfer_formula_freeze_gate.md
```

Current status:
`U12506_BETA_CLOSURE_TRANSFER_FORMULA_FREEZE_BLOCKED_PREFREEZE_PENDING`. The
gate writes the transfer formula manifest with headers and zero rows. The
halo-fit and priority-field gates pass, but independent route review,
prefrozen spin-route values, and carrier freeze are still blocked. It reads no
observed rotation curves and authorizes no endpoint score.

The separate blocked scoring runner is:

```bash
python scripts/run_ugc12506_beta_closure_transfer_scoring.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_transfer_scoring_summary.csv
data/derived/ugc12506_beta_closure_transfer_scoring_gates.csv
data/derived/ugc12506_beta_closure_transfer_scoring_scores.csv
data/derived/ugc12506_beta_closure_transfer_scoring_points.csv
reports/ugc12506_beta_closure_transfer_scoring.md
```

Current status:
`U12506_BETA_CLOSURE_TRANSFER_SCORING_BLOCKED_LAUNCH_GATE`. In this state the
runner sees an existing but empty formula manifest, writes no scores, and does
not read observed rotation curves. The dormant scoring branch is implemented
for a future accepted `BARYONIC_050_FAST_PACKET` carrier: after launch and
formula-freeze gates pass, the runner will compute
`v_readout = sqrt(beta_cl * v_baryon_050^2)` and write both score-level and
point-level control artifacts. It exists to enforce that `vobs` can only be
read by the separate scoring script after launch and formula-freeze gates pass.

The no-vobs scoring contract dry run is:

```bash
python scripts/build_ugc12506_beta_closure_transfer_scoring_contract_dry_run.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_transfer_scoring_contract_dry_run_summary.csv
data/derived/ugc12506_beta_closure_transfer_scoring_contract_dry_run_scenarios.csv
data/derived/ugc12506_beta_closure_transfer_scoring_contract_dry_run_manifest.csv
data/derived/ugc12506_beta_closure_transfer_scoring_contract_dry_run_predictions.csv
reports/ugc12506_beta_closure_transfer_scoring_contract_dry_run.md
```

Current status:
`U12506_BETA_CLOSURE_TRANSFER_SCORING_CONTRACT_DRY_RUN_READY_REVIEWS_PENDING`.
It checks the two implemented spin-normalization routes
(`EXPOSURE_PROXY`, `BULLOCK_DISK_CONVERSION`) against the reviewable
`BARYONIC_050_FAST_PACKET` carrier without reading `vobs`. Both scenarios are
contract-ready if independent reviews accept them: 22 dry-run manifest rows
and 656 prediction rows are produced with `scoring_used_vobs = false`.

The final pre-scoring unlock packet is:

```bash
python scripts/build_ugc12506_beta_closure_transfer_scoring_unlock_packet.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_transfer_scoring_unlock_packet_summary.csv
data/derived/ugc12506_beta_closure_transfer_scoring_unlock_requirements.csv
data/derived/ugc12506_beta_closure_spin_proxy_review_response_example_only_exposure_proxy.csv
data/derived/ugc12506_beta_closure_spin_proxy_review_response_example_only_bullock_conversion.csv
data/derived/ugc12506_beta_closure_carrier_review_response_example_only_baryonic_stress.csv
review_bundles/ugc12506_beta_closure_transfer_scoring_unlock_packet.zip
reports/ugc12506_beta_closure_transfer_scoring_unlock_packet.md
```

Current status:
`U12506_BETA_CLOSURE_TRANSFER_SCORING_UNLOCK_PACKET_READY_ACTIVE_RESPONSES_PENDING`.
The packet contains example-only response rows and exact active-response
requirements. It does not create active reviewer responses. Scoring remains
blocked until an independent reviewer writes the two active response files and
the standard intake/prefreeze/formula-freeze/scoring-launch gates pass.

The post-review scoring launcher is:

```bash
python scripts/run_ugc12506_beta_closure_post_review_scoring_launcher.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_post_review_scoring_launcher_summary.csv
data/derived/ugc12506_beta_closure_post_review_scoring_launcher_active_inputs.csv
data/derived/ugc12506_beta_closure_post_review_scoring_launcher_chain.csv
reports/ugc12506_beta_closure_post_review_scoring_launcher.md
```

Current status:
`U12506_BETA_CLOSURE_POST_REVIEW_SCORING_BLOCKED_ACTIVE_RESPONSES_PENDING`.
The launcher already runs the whole post-review chain and all chain scripts
return successfully. Because zero active reviewer response files are present,
it keeps the scoring runner blocked and reads no observed rotation curve.

Completed reviewer responses can be installed only through:

```bash
python scripts/install_ugc12506_beta_closure_active_review_responses.py
```

The default incoming directory is:

```text
review_bundles/incoming/ugc12506_beta_closure_transfer_scoring/
```

The installer expects exactly:

```text
ugc12506_beta_closure_spin_proxy_review_response.csv
ugc12506_beta_closure_carrier_review_response.csv
```

It writes:

```text
data/derived/ugc12506_beta_closure_active_review_response_install_summary.csv
data/derived/ugc12506_beta_closure_active_review_response_install_checks.csv
reports/ugc12506_beta_closure_active_review_response_installer.md
```

Current status:
`U12506_BETA_ACTIVE_REVIEW_RESPONSE_INSTALL_BLOCKED_INCOMING_PENDING_OR_INVALID`.
No active responses are present. The installer rejects missing, placeholder, or
`EXAMPLE_ONLY` rows and does not create review decisions.

The scoring-readiness dashboard is:

```bash
python scripts/build_ugc12506_beta_closure_scoring_readiness_dashboard.py
```

It writes:

```text
data/derived/ugc12506_beta_closure_scoring_readiness_summary.csv
data/derived/ugc12506_beta_closure_scoring_readiness_dashboard.csv
reports/ugc12506_beta_closure_scoring_readiness_dashboard.md
```

Current status:
`U12506_BETA_CLOSURE_SCORING_READINESS_BLOCKED_ACTIVE_RESPONSES_PENDING`.
The dashboard is a compact pre-scoring ledger: the no-`vobs` dry-run contract
and unlock packet are ready, the installer and launcher are wired, but the two
active independent response files are still absent. After those files are
placed in `review_bundles/incoming/ugc12506_beta_closure_transfer_scoring/`,
the scoring path is:

```bash
python scripts/install_ugc12506_beta_closure_active_review_responses.py
python scripts/run_ugc12506_beta_closure_post_review_scoring_launcher.py
python scripts/build_ugc12506_beta_closure_scoring_readiness_dashboard.py
```

Until the installer validates both active responses, no endpoint scores are
allowed and observed rotation curves are not read by this route.

The operational ablation ladder is:

```text
K^(0)(R) = K(R; K_present)
K^(1)(R) = K(R; K_present, O_obs/path)
K^(2)(R) = K(R; K_present, O_obs/path, Theta_morph)
K^(3)(R) = K(R; K_present, O_obs/path, Theta_morph, E_proj/history)
```

Current projection-enriched curves are first-order or partial approximations on
this ladder, not full path-aware `K^(3)` kernels.

## Paper Layout

The manuscript-facing material is split into two paper lanes:

```text
papers/paper1_internal_preflight/
papers/paper2_projection_enriched/
papers/common/
```

Paper 1 contains the original internal-preflight paper package. Paper 2 contains
the projection-enriched companion paper and should be used for the current
observer/path/projection-kernel work. Shared data, scripts, figures, reports,
tests, and bridge context remain in the repository-level common infrastructure.

For backward compatibility with existing scripts, the old top-level paths are
kept as symlinks:

```text
paper8_submission_source -> papers/paper1_internal_preflight/source
paper8_projection_enriched_source -> papers/paper2_projection_enriched/source
arxiv_submission_source.zip -> papers/paper1_internal_preflight/arxiv_source.zip
arxiv_projection_enriched_source.zip -> papers/paper2_projection_enriched/arxiv_source.zip
```

New work should prefer the `papers/...` layout; existing reproducibility scripts
may continue to use the historical paths.

## Main Files

```text
LICENSE
CITATION.cff
DATA_NOTICE.md
requirements.txt
README.md
papers/paper1_internal_preflight/source/main.tex
papers/paper1_internal_preflight/source/refs.bib
papers/paper1_internal_preflight/source/main.pdf
papers/paper1_internal_preflight/source/figures/
papers/paper1_internal_preflight/arxiv_source.zip
papers/paper2_projection_enriched/source/main.tex
papers/paper2_projection_enriched/source/refs.bib
papers/paper2_projection_enriched/source/main.pdf
papers/paper2_projection_enriched/source/figures/
papers/paper2_projection_enriched/arxiv_source.zip
papers/common/
figures/
data/derived/
scripts/generate_paper8_artifacts.py
scripts/build_arxiv_source.py
scripts/reproduce.py
tests/test_public_reproducibility_package.py
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
dependencies.  The current committed artifact set was last audited on Python
3.9.6 as well; Python 3.10+ remains the recommended fresh-environment target.

```bash
python -m pip install -r requirements.txt
```

Run the one-command reproduction check:

```bash
python scripts/reproduce.py
```

This regenerates the derived tables and figures, compiles Paper 1 through the
compatibility path `paper8_submission_source/main.tex` with `tectonic`, builds
the Paper 1 arXiv source ZIP, runs the foundation audit, and runs the public
package tests.

The reproduction script sets a fixed `SOURCE_DATE_EPOCH` for the TeX build and
the arXiv ZIP builder writes deterministic archive timestamps.  Matplotlib
figures strip version/date metadata, and carrier-robustness CSVs use fixed
floating-point formatting so that reruns should avoid scientifically irrelevant
byte-level drift.  If a remote dataset cannot be downloaded, the acquisition
step uses the committed/cacheable source copy and reports the fallback in the
terminal output.

### Online Data Dependencies

The one-command reproduction path includes one source-acquisition step:

```bash
python scripts/acquire_external_morphology_inputs.py
```

That script queries/downloads residual-blind catalogue inputs before endpoint
scoring:

- SPARC Table 1 from the official SPARC site:
  `https://astroweb.case.edu/SPARC/SPARC_Lelli2016c.mrt`
- S4G catalogue/decomposition tables through VizieR via `astroquery`.

The SPARC table is cached under:

```text
data/external/sparc/SPARC_Lelli2016c.mrt
```

If the remote SPARC download fails, the script uses the cached local copy and
prints a fallback message.  S4G/VizieR queries require network access for a
fresh acquisition; the generated derived tables are committed for reproducing
the paper state.  Other source-hunt and acquisition scripts in this repository
are optional workbench/provenance upgrades unless they are explicitly listed in
`scripts/reproduce.py`.

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
    projection caveats, trajectory/phase caveats, bar/core overlays.

Level 2: low-dimensional readout-state vector
    q_tail, q_compact, q_thick, q_bar, q_phase, q_regular.

Level 3: source-native scales and amplitudes
    disk scale, HI/tail radius, compact-core radius, flare support, bar length,
    and residual-blind closure/readout normalization.

Level 4: richer morphology/kinematic data
    velocity fields, HI maps, decompositions, and trajectory/phase indicators.
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

The full-launch closure roadmap is generated by:

```bash
python scripts/build_175_row_launch_closure_roadmap.py
```

This writes:

```text
data/derived/launch_175_row_closure_family_plan.csv
data/derived/launch_175_row_closure_gate_plan.csv
data/derived/launch_175_row_closure_summary.csv
reports/launch_175_row_closure_roadmap.md
```

This artifact turns the blocked 175-row launch into an execution order. It
shows that the remaining path is accepted-input closure across all active
families, not a post-score endpoint redesign.

The Phase 1 exponential-disk expansion packet is generated by:

```bash
python scripts/build_phase1_exponential_disk_expansion_packet.py
```

This writes:

```text
data/derived/phase1_exponential_disk_expansion_packet.csv
data/derived/phase1_exponential_disk_expansion_summary.csv
reports/phase1_exponential_disk_expansion_packet.md
```

This packet turns the first family-level closure phase into a concrete worklist
for all 32 `K_exponential_disk` rows: 14 already in the near-term accepted-lane
pool, 1 remaining S4G-matched scale-recovery row, and 17 external-crossmatch rows.

The Phase 1 exponential-disk family-label promotion manifest is generated by:

```bash
python scripts/build_phase1_exponential_disk_family_label_promotion_manifest.py
```

This writes:

```text
data/derived/phase1_exponential_disk_family_label_promotion_manifest.csv
data/derived/phase1_exponential_disk_family_label_promotion_summary.csv
reports/phase1_exponential_disk_family_label_promotion_manifest.md
```

This promotes the current 14-row near-term audit pool into an explicit
accepted-manifest family-label promotion packet. After the `NGC5023` alias fix
and the refreshed external family-label audit, `UGC08286` now also clears this
promotion gate, so the Phase 1 expdisk promotion manifest is now 14 rows wide.

The `ESO116-G012` scale-recovery packet is generated by:

```bash
python scripts/build_eso116_g012_scale_recovery_packet.py
```

This writes:

```text
data/derived/eso116_g012_scale_recovery_packet.csv
data/derived/eso116_g012_scale_recovery_summary.csv
reports/eso116_g012_scale_recovery_packet.md
```

This inspects the single `B_S4G_MATCHED_SCALE_RECOVERY` row in Phase 1. It
records a useful terminal local negative result: `ESO116-G012` is S4G-matched,
the S4G object row itself is flagged `No fit`, DustPedia fallback matches are
present, but the currently cached local sources still do not yield a direct
accepted scale radius. So this row is now cleanly closed as `local source
exhausted` until a genuinely new external decomposition/profile source is added.

The Phase 1 external-crossmatch packet is generated by:

```bash
python scripts/build_phase1_exponential_disk_external_crossmatch_packet.py
```

This writes:

```text
data/derived/phase1_exponential_disk_external_crossmatch_packet.csv
data/derived/phase1_exponential_disk_external_crossmatch_summary.csv
reports/phase1_exponential_disk_external_crossmatch_packet.md
```

This converts the remaining 17 no-S4G exponential-disk rows into a prioritized
fallback-source queue. It records which rows need outer-disk/HI review, which
need compact-support review, and which need projection/thickness review before
any family-label promotion can occur.

The dedicated Phase 1 `P1` crossmatch packet is generated by:

```bash
python scripts/build_phase1_exponential_disk_p1_crossmatch_packet.py
```

This writes:

```text
data/derived/phase1_exponential_disk_p1_crossmatch_packet.csv
data/derived/phase1_exponential_disk_p1_crossmatch_summary.csv
reports/phase1_exponential_disk_p1_crossmatch_packet.md
```

This now isolates the single remaining highest-priority no-S4G row,
`UGC07603`, into a direct outer-disk/HI fallback-source acquisition lane.

The dedicated Phase 1 `P2` crossmatch packet is generated by:

```bash
python scripts/build_phase1_exponential_disk_p2_crossmatch_packet.py
```

This writes:

```text
data/derived/phase1_exponential_disk_p2_crossmatch_packet.csv
data/derived/phase1_exponential_disk_p2_crossmatch_summary.csv
reports/phase1_exponential_disk_p2_crossmatch_packet.md
```

This isolates the 7 medium-priority no-S4G rows into a separate residual-blind
review lane, mostly split between outer-disk/tail reclassification candidates
and compact-support review candidates.

The endpoint-conversion roadmap for the remaining `17` no-S4G rows is generated by:

```bash
python scripts/build_phase1_exponential_disk_endpoint_conversion_roadmap.py
```

This writes:

```text
data/derived/phase1_exponential_disk_endpoint_conversion_roadmap.csv
data/derived/phase1_exponential_disk_endpoint_conversion_summary.csv
reports/phase1_exponential_disk_endpoint_conversion_roadmap.md
```

This does not run any endpoint yet. Instead, it identifies the shortest
admissible path from the remaining `17` rows toward a future subgroup endpoint:
an accepted `K_scale_tail_spiral` founder subset seeded by `F568-3`, `F574-1`,
and `NGC2403`.

The first concrete founder-source packet from that subgroup path is generated by:

```bash
python scripts/build_ngc2403_scale_tail_founder_source_packet.py
```

This writes:

```text
data/derived/ngc2403_scale_tail_founder_source_packet.csv
data/derived/ngc2403_scale_tail_founder_source_summary.csv
reports/ngc2403_scale_tail_founder_source_packet.md
```

This upgrades `NGC2403` from a generic P2 queue item to a local-source-backed
scale-tail founder candidate. It still does not promote accepted scale-tail
observables or authorize endpoint scoring.

The founder review gate for that first subgroup target is generated by:

```bash
python scripts/build_ngc2403_scale_tail_founder_review_gate.py
```

This writes:

```text
data/derived/ngc2403_scale_tail_founder_review_decisions.csv
data/derived/ngc2403_scale_tail_founder_review_gate.csv
reports/ngc2403_scale_tail_founder_review_gate.md
```

This records the next boundary precisely: `NGC2403` now supports a
conditional scale-tail surrogate candidate, but not an accepted founder
promotion, because direct outer-disk transition evidence is still missing.

The first founder-subset preflight gate is generated by:

```bash
python scripts/build_phase1_scale_tail_founder_preflight_gate.py
```

This writes:

```text
data/derived/phase1_scale_tail_founder_preflight_gate.csv
data/derived/phase1_scale_tail_founder_preflight_summary.csv
reports/phase1_scale_tail_founder_preflight_gate.md
```

This combines the initial founder trio into one endpoint-facing preflight view:
`NGC2403` is a local-context conditional candidate, while `F568-3` and `F574-1`
are still SPARC-HI-only conditional candidates that require external source review.

The second founder-source packet from that subgroup path is generated by:

```bash
python scripts/build_f574_1_scale_tail_founder_source_packet.py
```

This writes:

```text
data/derived/f574_1_scale_tail_founder_source_packet.csv
data/derived/f574_1_scale_tail_founder_source_summary.csv
reports/f574_1_scale_tail_founder_source_packet.md
```

This isolates `F574-1` as a SPARC-HI-only conditional founder candidate with a
usable `Vflat`/`Rdisk`/`RHI` bundle, but still blocked on external morphology review.

The direct founder external-review request for this galaxy is generated by:

```bash
python scripts/build_f574_1_founder_external_review_request.py
```

This writes:

```text
data/derived/f574_1_founder_external_review_request.csv
data/derived/f574_1_founder_external_review_summary.csv
reports/f574_1_founder_external_review_request.md
```

This makes `F574-1` the second concrete founder-unlock lane in the remaining
`17`: it already has a usable SPARC-HI conditional candidate, and now its
missing external morphology/HI review is isolated as a direct request packet.

The intake-ready source lane for that same founder is generated by:

```bash
python scripts/build_f574_1_founder_external_review_intake_packet.py
```

This writes:

```text
data/derived/f574_1_founder_external_review_intake_packet.csv
data/derived/f574_1_founder_external_review_intake_summary.csv
reports/f574_1_founder_external_review_intake_packet.md
```

This promotes `F574-1` from a founder request into a concrete residual-blind
external morphology plus HI intake lane without authorizing accepted founder
promotion or endpoint scoring.

The first external source-search audit for that intake lane is generated by:

```bash
python scripts/build_f574_1_external_source_search_audit.py
```

This writes:

```text
data/derived/f574_1_external_source_search_audit.csv
data/derived/f574_1_external_source_search_summary.csv
reports/f574_1_external_source_search_audit.md
```

This records the first primary-source pass for `F574-1` and shows that the
currently reviewed external literature is still context-only: useful for the
founder lane, but not yet enough to freeze an accepted outer-disk transition
observable or authorize endpoint scoring.

The next numeric-unlock request for that same lane is generated by:

```bash
python scripts/build_f574_1_transition_numeric_acquisition_request.py
```

This writes:

```text
data/derived/f574_1_transition_numeric_acquisition_request.csv
data/derived/f574_1_transition_numeric_summary.csv
reports/f574_1_transition_numeric_acquisition_request.md
```

This reduces the remaining `F574-1` founder blocker to a concrete missing
numeric: a source-native outer-disk break, truncation, or HI-side transition
measurement, still without authorizing accepted founder promotion or endpoint
scoring.

The direct 1996 HI table extraction for `F574-1` and `F568-3` is generated by:

```bash
python scripts/build_f574_f568_hi1996_table_extraction.py
```

This writes:

```text
data/derived/f574_f568_hi1996_table_extraction.csv
data/derived/f574_f568_hi1996_table_extraction_summary.csv
reports/f574_f568_hi1996_table_extraction.md
```

This upgrades the founder-side source record from pure context to source-native
table numerics: both galaxies now have explicit `R_out` and `R_HI`, and
`F568-3` also gains outer-velocity context from the 1996 HI source. The
remaining block is no longer missing table depth, but missing a frozen direct
transition or tail-onset numeric.

The follow-on multi-source radius support packet is generated by:

```bash
python scripts/build_f574_f568_multisource_radius_support.py
```

This writes:

```text
data/derived/f574_f568_multisource_radius_support.csv
data/derived/f574_f568_multisource_radius_support_summary.csv
reports/f574_f568_multisource_radius_support.md
```

This records that `F574-1` and `F568-3` now have outer-radius support from
more than one primary source family: HI-side `Rout/RHI` numerics from `1996`
and Halpha-side `Rmax` support from the `2001` high-resolution sample. This
still does not isolate a direct transition radius, but it strengthens the
founder lanes materially on the road toward a future subgroup endpoint.

The targeted direct-transition source-hunt update is generated by:

```bash
python scripts/build_f574_f568_direct_transition_source_hunt_update.py
```

This writes:

```text
data/derived/f574_f568_direct_transition_source_hunt_update.csv
data/derived/f574_f568_direct_transition_source_hunt_update_summary.csv
reports/f574_f568_direct_transition_source_hunt_update.md
```

This records the next source-search outcome cleanly: the `2001` Halpha and
model papers do strengthen founder-side support and curve-quality confidence
for `F574-1` and `F568-3`, but they still do not isolate a frozen direct
`transition/break/truncation` numeric. So the founder lanes are stronger than
before, yet the endpoint remains blocked at the transition-observable step.

The local PS figure-extraction blocker is generated by:

```bash
python scripts/build_f574_f568_ps_figure_extraction_blocker.py
```

This writes:

```text
data/derived/f574_f568_ps_figure_extraction_blocker.csv
data/derived/f574_f568_ps_figure_extraction_blocker_summary.csv
reports/f574_f568_ps_figure_extraction_blocker.md
```

This records the current technical limit of the local environment: the `.ps`
 figure assets from the `2001` source bundles are present and text-level source
 hunting is complete, but figure-level raster rendering is blocked because
 Ghostscript is not installed. That keeps the figure lane from contributing new
 claim-safe transition numerics for now.

Once Ghostscript is available and the figures are rendered, the follow-on
figure review packet is generated by:

```bash
python scripts/build_f574_f568_ps_figure_review.py
```

This writes:

```text
data/derived/f574_f568_ps_figure_review.csv
data/derived/f574_f568_ps_figure_review_summary.csv
reports/f574_f568_ps_figure_review.md
```

This records the visual review outcome from the rendered `2001` PS figures.
The figures strengthen founder-side support and outer-radius interpretation for
`F574-1` and `F568-3`, but still do not isolate a frozen direct
`transition/break` numeric.

The direct primary-source review of the `F574-1` colour-profile kink candidate
is generated by:

```bash
python scripts/build_f574_1_color_profile_kink_source_review.py
```

This writes:

```text
data/derived/f574_1_color_profile_kink_source_review.csv
data/derived/f574_1_color_profile_kink_source_review_summary.csv
reports/f574_1_color_profile_kink_source_review.md
```

This replaces the weaker thesis-search hit with a real primary-source review:
the `2000` MNRAS colour-profile paper does confirm a conspicuous `F574-1`
colour-profile kink, but it also explicitly attributes the central colour
behaviour to likely heavy dust reddening. That means the source is valuable
founder-side context, but it still does not provide a frozen tail-transition,
break, or truncation numeric.

The consolidated primary-transition source review for `F574-1` and `F568-3`
is generated by:

```bash
python scripts/build_f574_f568_primary_transition_source_review.py
```

This writes:

```text
data/derived/f574_f568_primary_transition_source_review.csv
data/derived/f574_f568_primary_transition_source_review_summary.csv
reports/f574_f568_primary_transition_source_review.md
```

This captures the best newly surfaced primary sources on both lanes:
`F574-1` now has a real Appendix-side radial R-band profile source plus the
confirmed colour-profile kink source, and `F568-3` now has a primary HI
surface-density profile-shape statement plus the already extracted inner
profile-feature numerics. Together these materially strengthen founder-side
support, but still do not provide a frozen direct transition or truncation
radius.

The next-closer break-radius candidate update for those two lanes is generated by:

```bash
python scripts/build_f574_f568_break_radius_candidate_update.py
```

This writes:

```text
data/derived/f574_f568_break_radius_candidate_update.csv
data/derived/f574_f568_break_radius_candidate_update_summary.csv
reports/f574_f568_break_radius_candidate_update.md
```

This records a more specific new source family: the `2001` ApJ mass-density
profile letter explicitly says it determines a `break radius` where the slope
changes most rapidly, and it includes both `F568-3` and a rederived `F574-1`
profile. That makes it a better direct-transition candidate than generic outer
profile support, but the actual per-galaxy break-radius numerics still need
extraction.

The direct figure-level extraction gate for that break-radius source is generated by:

```bash
python scripts/build_f574_f568_break_radius_extraction_gate.py
```

This writes:

```text
data/derived/f574_f568_break_radius_extraction_gate.csv
data/derived/f574_f568_break_radius_extraction_gate_summary.csv
reports/f574_f568_break_radius_extraction_gate.md
```

This confirms that the `2001` source is genuinely relevant at the panel level,
but also makes the blocker precise: the figure does not print per-galaxy
break-radius numerics, so a frozen value would require either a predeclared
digitization step or a different table/source that states the number directly.

The predeclared digitization route for those two break-radius panels is generated by:

```bash
python scripts/build_f574_f568_break_radius_digitization_protocol.py
```

This writes:

```text
data/derived/f574_f568_break_radius_digitization_protocol.csv
data/derived/f574_f568_break_radius_digitization_response_template.csv
data/derived/f574_f568_break_radius_digitization_response_schema.csv
data/derived/f574_f568_break_radius_digitization_response_validation.csv
data/derived/f574_f568_break_radius_digitization_response_summary.csv
reports/f574_f568_break_radius_digitization_protocol.md
```

This freezes the allowed reading logic before any number is filled: use only the
printed `2001` panels, define the axes first, apply one predeclared break
selection rule, record one candidate `log(R/kpc)` break radius plus uncertainty,
and forbid any residual- or endpoint-guided choice.

The first residual-blind candidate fill for those panels is generated by:

```bash
python scripts/build_f574_f568_break_radius_first_pass_fill.py
python scripts/build_f574_f568_break_radius_digitization_protocol.py
```

This updates:

```text
data/derived/f574_f568_break_radius_digitization_response_template.csv
reports/f574_f568_break_radius_first_pass_fill.md
```

and refreshes:

```text
data/derived/f574_f568_break_radius_digitization_response_validation.csv
data/derived/f574_f568_break_radius_digitization_response_summary.csv
```

The current first-pass candidate fill records conservative panel-read break
radii for `F574-1` and `F568-3`, but these remain candidate digitization fills
only and still do not authorize endpoint scoring.

The first-pass candidate audit for those fills is generated by:

```bash
python scripts/build_f574_f568_break_radius_candidate_audit.py
```

This writes:

```text
data/derived/f574_f568_break_radius_candidate_audit.csv
data/derived/f574_f568_break_radius_candidate_audit_summary.csv
reports/f574_f568_break_radius_candidate_audit.md
```

This is the promotion check after filling: it confirms that the current
break-radius numbers are valid residual-blind candidates, but keeps them
blocked because the source does not print direct per-galaxy break-radius
numerics and no independent review has yet accepted the panel reads.

The independent review packet for those candidate fills is generated by:

```bash
python scripts/build_f574_f568_break_radius_independent_review_packet.py
```

This writes:

```text
data/derived/f574_f568_break_radius_independent_review_items.csv
data/derived/f574_f568_break_radius_independent_review_packet.csv
data/derived/f574_f568_break_radius_independent_review_obligations.csv
data/derived/f574_f568_break_radius_independent_review_response_template.csv
data/derived/f574_f568_break_radius_independent_review_summary.csv
reports/f574_f568_break_radius_independent_review_packet.md
```

This is the next gate after the first-pass candidate audit: it freezes the
independent panel-review questions, the required reviewer obligations, and the
response template, but it still leaves the package in `response pending`
status until an actual non-first-pass reviewer accepts, corrects, or rejects
the panel reads.

The deeper source-triage audit for that numeric-unlock lane is generated by:

```bash
python scripts/build_f574_1_deeper_source_triage_audit.py
```

This writes:

```text
data/derived/f574_1_deeper_source_triage_audit.csv
data/derived/f574_1_deeper_source_triage_summary.csv
reports/f574_1_deeper_source_triage_audit.md
```

This separates generic context from the strongest current lead: the 1996 HI
observations paper is now explicitly tracked as the best transition-source
candidate for `F574-1`, and it now contributes source-native table numerics,
but it still does not freeze a direct outer-disk or HI-side transition
observable.

The direct source-depth extraction request for that lead is generated by:

```bash
python scripts/build_f574_1_source_depth_extraction_request.py
```

This writes:

```text
data/derived/f574_1_source_depth_extraction_request.csv
data/derived/f574_1_source_depth_extraction_summary.csv
reports/f574_1_source_depth_extraction_request.md
```

This turns the `F574-1` lane into a single explicit extraction problem: pull
figure- or table-depth HI/profile evidence from the 1996 source if available,
while keeping the founder lane blocked unless a source-native numeric can be
frozen residual-blind.

The local extraction verdict for that request is generated by:

```bash
python scripts/build_f574_1_source_depth_extraction_gate.py
```

This writes:

```text
data/derived/f574_1_source_depth_extraction_gate_items.csv
data/derived/f574_1_source_depth_extraction_gate.csv
reports/f574_1_source_depth_extraction_gate.md
```

This closes the current local extraction attempt in its updated state: the best
lead source is known and source-native table numerics are extracted, but no
frozen direct transition numeric is available yet, so the founder lane remains
blocked without endpoint scoring.

The parallel founder external-review request for `F568-3` is generated by:

```bash
python scripts/build_f568_3_founder_external_review_request.py
```

This writes:

```text
data/derived/f568_3_founder_external_review_request.csv
data/derived/f568_3_founder_external_review_summary.csv
reports/f568_3_founder_external_review_request.md
```

This gives the third founder its own direct unlock lane too: `F568-3` remains a
SPARC-HI conditional candidate, but still needs external morphology/HI review
and has weaker velocity context than `F574-1`.

The intake-ready source lane for that founder is generated by:

```bash
python scripts/build_f568_3_founder_external_review_intake_packet.py
```

This writes:

```text
data/derived/f568_3_founder_external_review_intake_packet.csv
data/derived/f568_3_founder_external_review_intake_summary.csv
reports/f568_3_founder_external_review_intake_packet.md
```

This promotes `F568-3` from a founder request into a concrete residual-blind
external morphology plus HI intake lane while preserving its weaker
velocity-context caveat and without authorizing accepted founder promotion or
endpoint scoring.

The first external source-search audit for that intake lane is generated by:

```bash
python scripts/build_f568_3_external_source_search_audit.py
```

This writes:

```text
data/derived/f568_3_external_source_search_audit.csv
data/derived/f568_3_external_source_search_summary.csv
reports/f568_3_external_source_search_audit.md
```

This records the first primary-source pass for `F568-3` and shows that the
current external literature pass is still context-only: the founder lane is
better specified, but no frozen transition numeric or velocity-context repair
is yet available.

The focused 2018 profile-feature review for `F568-3` is generated by:

```bash
python scripts/build_f568_3_profile_feature_source_review.py
```

This writes:

```text
data/derived/f568_3_profile_feature_source_review.csv
data/derived/f568_3_profile_feature_source_review_summary.csv
reports/f568_3_profile_feature_source_review.md
```

This upgrades the founder-side source packet from pure context into explicit
profile-feature numerics: the paper contributes azimuthal bar radii,
ellipticity-feature radii, and a first phase-crossing radius near `10 arcsec`
for `F568-3`. These values materially strengthen the founder lane, but they
still describe inner bar/profile structure rather than a frozen tail-transition
or truncation observable, so endpoint scoring remains blocked.

The deeper source-triage audit for that founder is generated by:

```bash
python scripts/build_f568_3_deeper_source_triage_audit.py
```

This writes:

```text
data/derived/f568_3_deeper_source_triage_audit.csv
data/derived/f568_3_deeper_source_triage_summary.csv
reports/f568_3_deeper_source_triage_audit.md
```

This separates generic context from the strongest current lead: the 1996 HI
observations paper is now explicitly tracked as the best transition-source
candidate for `F568-3`, and it now contributes source-native table numerics
plus explicit outer-velocity context, but it still does not freeze a direct
outer-disk or HI-side transition observable.

The direct source-depth extraction request for that lead is generated by:

```bash
python scripts/build_f568_3_source_depth_extraction_request.py
```

This writes:

```text
data/derived/f568_3_source_depth_extraction_request.csv
data/derived/f568_3_source_depth_extraction_summary.csv
reports/f568_3_source_depth_extraction_request.md
```

This turns the `F568-3` lane into a single explicit extraction problem: pull
figure- or table-depth HI/profile evidence and any source-side velocity-context
clarifier from the 1996 source if available, while keeping the founder lane
blocked unless a source-native numeric can be frozen residual-blind.

The local extraction verdict for that request is generated by:

```bash
python scripts/build_f568_3_source_depth_extraction_gate.py
```

This writes:

```text
data/derived/f568_3_source_depth_extraction_gate_items.csv
data/derived/f568_3_source_depth_extraction_gate.csv
reports/f568_3_source_depth_extraction_gate.md
```

This closes the current local extraction attempt in its updated state: the best
lead source is known, source-native table numerics are extracted, and the weak
velocity caveat is no longer driven by a total lack of source-side velocity
evidence, but no frozen direct transition numeric is available yet, so the
founder lane remains blocked without endpoint scoring.

The consolidated founder unlock dashboard is generated by:

```bash
python scripts/build_phase1_scale_tail_founder_unlock_dashboard.py
```

This writes:

```text
data/derived/phase1_scale_tail_founder_unlock_dashboard.csv
data/derived/phase1_scale_tail_founder_unlock_summary.csv
reports/phase1_scale_tail_founder_unlock_dashboard.md
```

This ranks the three founder unlock lanes for the remaining `17`: `NGC2403`
first, `F574-1` second, and `F568-3` third.

The shared founder-subset acquisition manifest is generated by:

```bash
python scripts/build_phase1_scale_tail_founder_external_acquisition_manifest.py
```

This writes:

```text
data/derived/phase1_scale_tail_founder_external_acquisition_manifest.csv
data/derived/phase1_scale_tail_founder_external_acquisition_summary.csv
reports/phase1_scale_tail_founder_external_acquisition_manifest.md
```

This converts the current founder trio into a direct subgroup-unblock worklist:
`NGC2403` needs direct transition evidence, while `F574-1` and `F568-3` need
external morphology plus HI review before an accepted scale-tail subgroup endpoint
can be attempted.

The direct-transition request packet for the nearest founder unlock is generated by:

```bash
python scripts/build_ngc2403_direct_transition_request_packet.py
```

This writes:

```text
data/derived/ngc2403_direct_transition_request_packet.csv
data/derived/ngc2403_direct_transition_request_summary.csv
reports/ngc2403_direct_transition_request_packet.md
```

This isolates the single closest subgroup-unblock blocker: `NGC2403` now needs
direct transition evidence rather than broader morphology triage.

The intake-ready packet for that direct-transition search is generated by:

```bash
python scripts/build_ngc2403_direct_transition_intake_packet.py
```

This writes:

```text
data/derived/ngc2403_direct_transition_intake_packet.csv
data/derived/ngc2403_direct_transition_intake_summary.csv
reports/ngc2403_direct_transition_intake_packet.md
```

This is the first fully intake-ready founder-unlock lane in the remaining `17`:
`NGC2403` now has a concrete residual-blind source-search packet for direct
transition evidence.

The first local-source acquisition update for that lane is generated by:

```bash
python scripts/build_ngc2403_direct_transition_acquisition_update.py
```

This writes:

```text
data/derived/ngc2403_direct_transition_acquisition_sources.csv
data/derived/ngc2403_direct_transition_acquisition_update.csv
data/derived/ngc2403_direct_transition_acquisition_summary.csv
reports/ngc2403_direct_transition_acquisition_update.md
```

This upgrades `NGC2403` from a pure intake packet to a concrete local
source-family map: several residual-blind source families are already present,
but the direct transition observable is still missing, so the founder lane
remains blocked short of endpoint scoring.

The negative local extraction gate for that same lane is generated by:

```bash
python scripts/build_ngc2403_direct_transition_extraction_gate.py
```

This writes:

```text
data/derived/ngc2403_direct_transition_extraction_gate.csv
data/derived/ngc2403_direct_transition_extraction_summary.csv
reports/ngc2403_direct_transition_extraction_gate.md
```

This makes the current blocker fully explicit: the local evidence package does
not yet yield a frozen outer-break, truncation, or HI-transition radius, so the
lane remains founder-blocked even though its residual-blind source map is now
well organized.

The first external source review pass for that lane is generated by:

```bash
python scripts/build_ngc2403_direct_transition_external_source_review.py
```

This writes:

```text
data/derived/ngc2403_direct_transition_external_source_review.csv
data/derived/ngc2403_direct_transition_external_source_review_summary.csv
reports/ngc2403_direct_transition_external_source_review.md
```

This records that the reviewed `Fraternali`-side HI papers and a stellar
outer-disk context source strengthen the founder rationale, but still do not
yield a claim-safe frozen direct-transition radius for endpoint promotion.

The strongest current transition-context candidate can be isolated with:

```bash
python scripts/build_ngc2403_conditional_transition_candidate_packet.py
```

This writes:

```text
data/derived/ngc2403_conditional_transition_candidate_packet.csv
data/derived/ngc2403_conditional_transition_candidate_summary.csv
reports/ngc2403_conditional_transition_candidate_packet.md
```

This records the current best explicit outer-disk cutoff candidate for `NGC2403`
at `10 kpc`, but keeps it clearly in the conditional, not-yet-accepted bucket.

The promotion audit for that conditional candidate is generated by:

```bash
python scripts/build_ngc2403_transition_candidate_promotion_gate.py
```

This writes:

```text
data/derived/ngc2403_transition_candidate_promotion_gate.csv
data/derived/ngc2403_transition_candidate_promotion_summary.csv
reports/ngc2403_transition_candidate_promotion_gate.md
```

This turns the current founder blocker into three explicit subgates:
source-depth, observable-type, and freeze-readiness. Right now all three remain
blocked, so the candidate helps prioritize the lane but does not yet unlock endpoint scoring.

The concrete request for the first of those blocked subgates is generated by:

```bash
python scripts/build_ngc2403_source_depth_acquisition_request.py
```

This writes:

```text
data/derived/ngc2403_source_depth_acquisition_request.csv
data/derived/ngc2403_source_depth_acquisition_summary.csv
reports/ngc2403_source_depth_acquisition_request.md
```

This is the first truly actionable request packet in the `NGC2403` founder lane:
it asks for deeper numeric source extraction around the current `10 kpc` outer-disk
cutoff candidate before any promotion toward endpoint scoring.

The execution-focus audit for the whole `NGC2403` unlock lane is generated by:

```bash
python scripts/build_ngc2403_unlock_execution_focus_audit.py
```

This writes:

```text
data/derived/ngc2403_unlock_execution_focus_audit.csv
data/derived/ngc2403_unlock_execution_focus_summary.csv
reports/ngc2403_unlock_execution_focus_audit.md
```

This makes explicit that `NGC2403` is now the sole live founder unlock in the
remaining founder set, and that the Barker outer-disk depth lane is the first
actionable target ahead of the Fraternali HI-context support lanes.

The Barker-focused lead audit for that unlock lane is generated by:

```bash
python scripts/build_ngc2403_barker_depth_lead_audit.py
```

This writes:

```text
data/derived/ngc2403_barker_depth_lead_audit.csv
data/derived/ngc2403_barker_depth_lead_summary.csv
reports/ngc2403_barker_depth_lead_audit.md
```

This strengthens the source-side picture by showing that the Barker family is
better sourced than before, including the later faint-structure paper, but that
it still remains stellar outer-structure context rather than a frozen HI-tail
transition numeric.

The concrete request for the second blocked subgate is generated by:

```bash
python scripts/build_ngc2403_observable_type_acquisition_request.py
```

This writes:

```text
data/derived/ngc2403_observable_type_acquisition_request.csv
data/derived/ngc2403_observable_type_acquisition_summary.csv
reports/ngc2403_observable_type_acquisition_request.md
```

This makes explicit that the current `10 kpc` candidate is still the wrong
observable family for founder promotion: we still need an HI-tail / break /
truncation type source-native measurement to move toward endpoint scoring.

The concrete request for the third blocked subgate is generated by:

```bash
python scripts/build_ngc2403_freeze_readiness_acquisition_request.py
```

This writes:

```text
data/derived/ngc2403_freeze_readiness_acquisition_request.csv
data/derived/ngc2403_freeze_readiness_acquisition_summary.csv
reports/ngc2403_freeze_readiness_acquisition_request.md
```

This completes the blocker-triád request layer for `NGC2403`: even if a better
numeric and a better observable family arrive, the lane still needs a
freeze-admissible residual-blind source-native measurement before endpoint scoring.

The first concrete galaxy packet from that lane is generated by:

```bash
python scripts/build_ugc08286_p1_source_acquisition_packet.py
```

This writes:

```text
data/derived/ugc08286_p1_source_acquisition_packet.csv
data/derived/ugc08286_p1_source_acquisition_summary.csv
reports/ugc08286_p1_source_acquisition_packet.md
```

This now records the opposite correction: `UGC08286` is no longer a no-S4G
fallback-source target. The `NGC5023` alias fix reveals an existing S4G match
and accepted scale radius, so the row moves back into the S4G-matched
scale-recovery/family-audit branch.

The first real external-source update for that row is generated by:

```bash
python scripts/build_ugc08286_external_source_acquisition_update.py
```

This writes:

```text
data/derived/ugc08286_external_source_acquisition_sources.csv
data/derived/ugc08286_external_source_acquisition_update.csv
data/derived/ugc08286_external_source_acquisition_summary.csv
reports/ugc08286_external_source_acquisition_update.md
```

This resolves `UGC08286` to `NGC5023/PGC045849`, confirms the accepted S4G
scale, and adds source-side optical/HI context for the family-label audit.

The resulting surrogate review gate is generated by:

```bash
python scripts/build_ugc08286_scale_surrogate_review_gate.py
```

This writes:

```text
data/derived/ugc08286_scale_surrogate_review_decisions.csv
data/derived/ugc08286_scale_surrogate_review_gate.csv
reports/ugc08286_scale_surrogate_review_gate.md
```

This explicitly separates “accepted direct scale already present” from
“family-label audit still pending”. At the current stage, the row remains
blocked only on label audit, not on scale recovery.

Its paired distance-caveated companion is generated by:

```bash
python scripts/build_ugc07603_p1_source_acquisition_packet.py
```

This writes:

```text
data/derived/ugc07603_p1_source_acquisition_packet.csv
data/derived/ugc07603_p1_source_acquisition_summary.csv
reports/ugc07603_p1_source_acquisition_packet.md
```

This preserves the same negative source-result discipline for `UGC07603`, while
keeping the `large_distance_error` caveat explicit.

The first-pass external search audit for that row is generated by:

```bash
python scripts/build_ugc07603_external_source_search_audit.py
```

This writes:

```text
data/derived/ugc07603_external_source_search_audit.csv
data/derived/ugc07603_external_source_search_summary.csv
reports/ugc07603_external_source_search_audit.md
```

This records that `UGC07603` did not yet produce a clean alias-resolved primary
source packet comparable to the now-reclassified `UGC08286` case.

The resulting Phase 1 no-S4G closure gate is generated by:

```bash
python scripts/build_phase1_exponential_disk_external_acquisition_gate.py
```

This writes:

```text
data/derived/phase1_exponential_disk_external_acquisition_gate.csv
data/derived/phase1_exponential_disk_external_acquisition_blockers.csv
reports/phase1_exponential_disk_external_acquisition_gate.md
```

This makes the next blocker explicit: the local cache is no longer enough for
the no-S4G Phase 1 branch, so new residual-blind external source acquisition is
required before further promotion.

The corresponding external source-request manifest is generated by:

```bash
python scripts/build_phase1_exponential_disk_external_source_request_manifest.py
```

This writes:

```text
data/derived/phase1_exponential_disk_external_source_request_manifest.csv
data/derived/phase1_exponential_disk_external_source_request_summary.csv
reports/phase1_exponential_disk_external_source_request_manifest.md
```

This packages the next concrete request order for the remaining live no-S4G P1
queue: `UGC07603` first.

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
papers/paper1_internal_preflight/arxiv_source.zip
```

The ZIP is built from `papers/paper1_internal_preflight/source/` through the
compatibility path `paper8_submission_source/` and excludes the compiled PDF and
temporary LaTeX build files.

Build the projection-enriched companion package with:

```bash
python scripts/build_arxiv_projection_enriched_source.py
```

This writes:

```text
papers/paper2_projection_enriched/arxiv_source.zip
```

## Scope

This repository is now a shared reproducibility workspace for the Paper 1
internal-preflight lane and the Paper 2 projection-enriched lane. It excludes
raw SPARC downloads, private workbench outputs, endpoint-fitting notebooks, and
broad Tau Core theory-hub material that is not needed to verify these paper
packages.
