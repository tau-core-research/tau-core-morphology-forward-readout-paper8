# Tau Core Gravity Bridge Central Architecture

This page is the local Paper 8 bridge entrypoint. It records the morphology
layer discipline used by the morphology-matched forward-readout gate.

## Scope

The Paper 8 bridge does not assume that present-day visual morphology is a
fundamental Tau-side class. It uses observed morphology as a residual-blind
source handle, then separates that handle from the readout-relevant proxy used
to choose a candidate 4D readout shell.

This distinction is a Tau Core bridge consequence: the bridge treats galaxy
morphology as a projection/readout structure, not merely as a 4D visual label.

## Tau Morphology State

The bridge uses `Tau morphology state` for the deeper Tau-side organizing
configuration behind the observable galaxy.  It is not the same object as a
visible spiral/bar/ring/warp class.  A Tau morphology state is a
configuration-level descriptor whose different four-dimensional readouts may
appear as:

```text
time / clock readout
matter or mass-distribution readout
gravity / metric-response readout
quantum or coherence readout
visible 4D morphology
observer/path readout
```

In this language, the visible galaxy morphology is one readout of the Tau
morphology state, not the state itself.  The current Paper 8/Paper 2 machinery
does not model all of these readouts.  It uses the concept to keep the
operational hierarchy honest: visible morphology is a source handle, while
`K_readout`, `Theta_tau`, and possible clock/path factors are partial
four-dimensional projections of the same deeper Tau-side state.

Equivalently, the internal Tau morphology state is the shared source-side
organizing object that determines which readout channels can be visible in 4D.
It is not itself a rotation-curve correction, a visual class, or a clock
factor.  The correction terms used in this bridge are channel-specific
readouts of it:

```text
Tau morphology state
    -> visible/source morphology readout       K_present, K_obs
    -> morphology/gravity readout              K_readout, delta_v_morph^2
    -> morphology trajectory/phase readout     Theta_morph
    -> clock/time projection readout           Xi_t or Xi_eff
    -> observer/path projection readout        O_obs/path, E_proj/history
```

Thus `Theta_morph` and `Xi_t` are not two names for the same effect.
`Theta_morph` records how the source's internal morphology state appears as a
settling/history/phase readout, while `Xi_t` records how the observed clock or
time-slice readout changes the velocity quotient.  They may share source
evidence because they are readouts of the same deeper state, but a combined
endpoint requires a nonoverlap ledger to prevent counting the same evidence
twice.

This channel list is open, but not freely tunable. Other projections of the
same internal Tau morphology state can in principle affect the effective
rotation readout, including:

```text
mass-distribution readout
metric / closure readout
coherence or phase readout
source-observer path / environment readout
```

Bridge rule: a new projection channel is not an allowed correction merely
because it is conceptually available. It must be turned into a residual-blind
source observable, assigned to a distinct ledger channel, checked for overlap
with active morphology/projection/time kernels, and tested by ablation against
the lower-channel kernel. Until then it remains Tau-side motivation, not an
endpoint-scored readout factor.

## Projection-Induction / Source-Grounding Gate

The source-freeze rule is necessary but not sufficient for a Tau-side
derivation claim. A source-frozen observable only says that a channel was chosen
without endpoint residual leakage. To promote that channel from an operational
proxy to a Tau-induced 4D source, it must also pass the projection-induction
gate:

```text
activation
    -> quotient survival
    -> closure stability
    -> 4D readout survival
```

In compact notation the induced observable has the form

```text
O_i^4D = R_i^4D( Pi_stab([A_tau(u)]) )
```

where `u` is a Tau-side mode, `A_tau` is the activation map,
`[A_tau(u)]` is the class after null/gauge quotienting, `Pi_stab` keeps only
the closure-stable part, and `R_i^4D` is the channel-specific 4D readout map.

Bridge status for Paper 8:

```text
SOURCE_GROUNDING_GATE_DEFINED
SOURCE_GROUNDING_DERIVATION_PENDING
```

Therefore the morphology formula shells below are source-frozen, auditable
readout proxies unless the corresponding source-grounding derivation is
separately discharged. This gate protects the paper from over-reading a
successful matched-family score as a final Tau Core derivation.

## Core Chain

```text
Tau morphology state
    -> projection and 4D readout
    -> observed 4D morphology handle K_obs
    -> residual-blind source review, caveats, and provenance
    -> readout-relevant morphology proxy K_readout
    -> predeclared 4D readout formula shell F_{K_readout}
    -> forward delta_g or delta_v^2 pilot score
```

`K_obs` is the apparent or catalogue-supported 4D morphology handle. It may be
a thin disk, thick/flared disk, bar, ring, compact component, tail, lopsided
feature, or other projected morphology descriptor.

`K_readout` is the predeclared readout-relevant morphology proxy. It is the
object allowed to select the formula shell. It may equal `K_obs`, but this is
not assumed.

## Morphology Versus Projection

The bridge uses morphology and projection as related but distinct notions.
Observed 4D morphology is already a projection/readout handle, not the
fundamental Tau-side configuration itself.  A visual or catalogue label can
start the residual-blind source review, but it does not automatically select
the active readout kernel.

Operationally the bridge separates:

```text
K_obs:
    catalogue or visually supported 4D morphology handle

K_present:
    present source-observed 4D morphology state used in a local formula shell

K_readout:
    readout-relevant morphology/projection state allowed to select F_K

O_path:
    observer/path projection data: inclination, line-of-sight stacking,
    warp visibility, beam/path geometry, source-observer viewing context

Theta_tau:
    Tau-side morphology trajectory / phase information: history,
    relaxation, settling, asymmetry, or future-directed phase proxy
```

The safe relationship is:

```text
K_obs
    -> source review and caveats
    -> K_present
    +  O_path
    +  Theta_tau
    +  E_proj/history
    -> K_readout
    -> F_{K_readout}
```

Thus the older shorthand "morphology-specific formula" should be read as
"morphology-projection readout family."  A barred, ringed, warped, thick,
compact, or lopsided 4D morphology label is a first-pass projected handle.  The
active kernel may instead be projection-dominated, history-dominated,
mixed-readout, clock/readout-controlled, or a null/quiet limit.

This distinction also defines the double-count discipline.  The same
source-side fact cannot be counted once as the morphology kernel and again as an
independent observer/path, trajectory, or clock/readout correction.  Any such
second channel must provide residual-blind non-overlap evidence before endpoint
use.

Kernel-level audit after the terminology clarification:

```text
status:
    MORPHOLOGY_PROJECTION_KERNEL_LEVEL_AUDIT_COMPLETE

galaxies audited:
    6

routes audited:
    11

endpoint-allowed routes:
    7

routes requiring immediate rescoring:
    0

routes numerically changed by the terminology audit:
    0

time-control routes:
    2
```

Bridge consequence: the morphology/projection distinction changes route
interpretation and future gate requirements, not the frozen numerical endpoint
kernels.  The main watchlist is:

```text
NGC4088:
    clock-only Xi_eff control overlaps the accepted additive warp/history route

UGC12506:
    Theta_morph and Xi_t routes require non-overlap separation before endpoint.
    The channel roles are now separated, but the combined endpoint remains
    blocked by source overlap.

NGC4013:
    mixed overlay prospective replay remains quarantined, not endpoint

NGC7331:
    broad vertical/outer-warp window remains caveated and should be source-sharpened
```

Artifacts:

```text
data/derived/morphology_projection_kernel_level_audit.csv
data/derived/morphology_projection_kernel_level_audit_summary.csv
data/derived/morphology_projection_kernel_double_count_worklist.csv
reports/morphology_projection_kernel_level_audit.md
```

## Observer / Path Projection Is Morphology-History Dependent

The bridge treats observer/path projection as part of the readout structure,
not as a merely geometric viewing-angle correction. In Tau Core bridge terms,
the apparent projection seen by an observer can depend on the present
morphology, the observer/path geometry, and the source's Tau-side morphology
trajectory or phase profile.

The operational rule is therefore:

```text
K_readout =
K_readout(
    present source morphology,
    observer/path projection,
    Tau-side morphology trajectory / phase,
    projection-history environment
)
```

Equivalently, the projection-enriched rotation readout shell is:

```text
delta_v_proj^2(R)
  =
  sum_j A_j(source)
        w_j(R, O_obs/path, Theta_morph)
        K_j(R; K_present, Theta_morph)
```

where `Theta_morph` is the residual-blind Tau-side morphology trajectory/phase
profile. It may include present morphology, past traces, and future-directed
relaxation or settling indicators, but only as source-frozen observables.

This is a bridge consequence, not an endpoint fitting license. The
observer/path and trajectory/phase terms may enter a formula shell only through
residual-blind source evidence: inclination, warp geometry, vertical overlay,
H I envelope/asymmetry, resolved velocity-field context, interaction history,
relaxation or settling indicators, environment notes, or other source-native
observables. Endpoint residuals, best-fitting families, and baseline comparison
scores cannot define these terms.

In Tau Core language, future-directed morphology or path-environment terms are
not treated as backward causal influences. They are treated as
trajectory/phase components of a deeper Tau-side configuration, whose
four-dimensional past, present, and future appearances may be different
readout slices. Thus future-directed relaxation, settling, accretion,
morphological phase, or path-environment indicators may be admissible readout
inputs when they are supported by residual-blind source evidence.

The current observer/path projection audits are first-order approximations.
The fuller object is the galaxy-to-observer null-geodesic bundle environment:
the light path or beam neighborhood together with the metric/matter
distribution that can influence the causal past of that observed beam. A
present-day line-of-sight or inclination proxy may therefore be incomplete if
the Tau-side morphology trajectory contains earlier morphology, current
projection, or future-directed relaxation/settling phase information with a
readout-relevant imprint.

Consequently, a weak present-day morphology match is not automatically a Tau
Core failure. The correct next question is whether the source record supports a
different `K_readout` after projection/trajectory enrichment. Conversely, if a
source-complete, residual-blind projection/trajectory-enriched `K_readout` fails
under a frozen formula shell, that case becomes a stronger true-negative
candidate.

The bridge therefore distinguishes four operational kernel levels:

```text
K^(0)(R) = K(R; K_present)
K^(1)(R) = K(R; K_present, O_obs/path)
K^(2)(R) = K(R; K_present, O_obs/path, Theta_morph)
K^(3)(R) = K(R; K_present, O_obs/path, Theta_morph, E_proj/history)
```

Existing Paper 2 curves are to be read as `K^(0)`, `K^(1)`, or partial
`K^(2)` approximations depending on the source artifact. They are not full
`K^(3)` path-aware kernels.

## Time-Readout Projection Channel

The bridge now separates morphology/trajectory phase from a stronger
time-readout projection channel. The point is not only that the source
morphology may have past/current/future Tau-side trajectory components. The
stronger claim to be tested is:

```text
Tau-side configuration
    -> projection-dependent time / clock readout
    -> gravity / morphology readout
    -> observed rotation dynamics
```

In this channel, the observed rotation speed can differ because the time
parameter used by the observed 4D readout is not identical to the Newtonian
closure-test time parameter. This is not an extra force term. It is a
clock/readout mismatch.

The first shell is:

```text
v_obs^2(R)
  =
  Xi_t^2(R; O_obs/path, Theta_morph, E_proj/history)
  *
  [
    v_Newt^2(R)
    + delta_v_grav/morph^2(R)
  ]
```

where `Xi_t = 1` is the Newtonian clock-readout limit. For a small
projection-time mismatch:

```text
Xi_t(R) = 1 + epsilon_t(R)
```

the linearized contribution is:

```text
delta_v_t^2(R)
  ~= 2 epsilon_t(R)
     [
       v_Newt^2(R) + delta_v_grav/morph^2(R)
     ].
```

This is formula-conditional. `Xi_t` or `epsilon_t` must be frozen from
residual-blind source-side time/projection evidence before scoring. It cannot
be inferred from the rotation residual, a best-fit Tau family, or a
MOND/RAR/TPG comparison score.

The current Paper 2 full-time morphology replay is only a diagnostic proxy for
this channel. It tests whether a morphology-trajectory layer behaves like a
source-dependent readout correction. It is not yet a source-complete
time-projection endpoint, because no accepted residual-blind `Xi_t(R)` manifest
exists.

Operationally the channel affects five projection subchannels:

| Subchannel | What changes | Formula role | Source-freeze requirement |
| --- | --- | --- | --- |
| Observer/path projection | which source clock slice is visible along the observed light bundle | argument of `Xi_t` through `O_obs/path` | inclination, edge-on overlay, warp visibility, beam/path geometry, foreground/path audit |
| Morphology trajectory / phase | whether present 4D morphology is a settled or phase-shifted readout slice | argument of `Xi_t` through `Theta_morph` | settling state, warp/asymmetry stage, interaction history, relaxation/future-directed phase proxy |
| Gravity/readout projection | additive morphology/gravity residual is clock-rescaled | `Xi_t^2 [v_Newt^2 + delta_v_grav/morph^2]` | separate morphology/gravity residual shell must be frozen before time-readout scoring |
| Clock-rate / time-slice projection | effective time parameter in the observed velocity quotient changes | `Xi_t = 1 + epsilon_t`; `delta_v_t^2 ~= 2 epsilon_t (...)` | residual-blind clock/readout mismatch proxy |
| Path/environment projection | metric/matter environment of the observed light bundle can affect the clock factor | possible `E_proj/history` dependence in `Xi_t` | null-geodesic bundle environment or rejected image-plane coincidence |

This matrix is a checklist for future manifests. It is not a statement that all
five subchannels are active for a given galaxy.

First diagnostic replay status:

```text
Xi_t(R) = 1 + epsilon_0 K_t(R)
```

with `epsilon_0` capped and inherited from residual-blind source-status loads
was run on the current trial galaxies. The diagnostic improved the strongest
warp/history/asymmetry case (`NGC4088`) and the high-spin edge-on stress case
(`UGC12506`), was nearly neutral for the weak-projection control (`NGC4183`),
and degraded already close or saturated projection kernels (`NGC4013`,
`NGC5907`, `NGC7331`). This is useful only as a diagnostic: it suggests the
time-readout channel is not a universal amplitude rescue term, but no accepted
`Xi_t(R)` endpoint exists yet.

The corresponding readiness manifest has the following current policy:

```text
P1 source-review targets:
    NGC4088, UGC12506

P2 weak/null control:
    NGC4183

P3 reject current Xi_t proxy / keep Xi_t = 1 unless new source evidence appears:
    NGC4013, NGC5907, NGC7331
```

This is an important bridge discipline. A failed or neutral `Xi_t` replay is
not patched by increasing `epsilon_t`; it either becomes a null-control
confirmation or rejects the current time-readout proxy for that source state.

The P1 source-review worklist is now explicit and remains non-endpoint:

```text
NGC4088:
    required source route:
        independent warp/asymmetry phase proxy
        interaction/companion context
        accepted epsilon_t normalization law
    key audit:
        separate clock/readout phase from the already-used additive
        warp/history morphology kernel

UGC12506:
    required source route:
        high-spin edge-on H I envelope or position-velocity consistency proxy
        source-side clock/readout settling proxy
        path/foreground review
    key audit:
        decide whether the path term is active or zero before endpoint scoring
```

Bridge consequence: `NGC4088` and `UGC12506` are not accepted `Xi_t`
endpoints. They are source-review targets. The next accepted endpoint can only
be run after `K_t(R)` and `epsilon_t` are frozen from source observables alone,
with no rotation-residual promotion and no post-hoc amplitude rescue.

First P1 source-review intake:

```text
NGC4088:
    status:
        strong source context, measurement blocked
    filled:
        warp presence flag
        PV asymmetry flag
        PA asymmetry flag
    blocked:
        q_warp_measured
        m_history_warp
        independent review
        epsilon_t normalization law
    consequence:
        Xi_t route remains measurement-blocked until the source worksheets
        are filled and reviewed.

UGC12506:
    status:
        strong source context, foreground/path term not established
    filled:
        high-inclination PV/envelope requirement
        extended H I support
        asymmetric PV/envelope context
        low-density stable H I context
        high-spin context
    blocked:
        accepted K_t(R) envelope mapping
        epsilon_t normalization law
        clock/readout settling proxy
    consequence:
        foreground/path term is set to zero unless a later cone/path review
        supports it. The active route is high-spin/envelope clock readout,
        not foreground rescue.
```

UGC12506 first source-only `Xi_t` shell:

```text
Xi_t(R) = 1 + epsilon_t K_t(R)

K_t = norm[
    w_spin K_spin
  + w_edge K_edge_clock
  + w_env K_envelope_settling
  + w_asym K_asymmetric_PV_phase
  + 0 * K_path
]

epsilon_t = min(0.035, 0.035 * Gamma_clock)
Gamma_clock = L / (1 + L)
```

Current source-shell value:

```text
epsilon_t ~= 0.023844
path_load = 0
endpoint_scores_allowed = false
```

Bridge consequence: this is the first concrete source-only UGC12506 clock
readout shell. It remains blocked as an accepted endpoint because the
`epsilon_t` normalization law is still a source-shell candidate rather than an
accepted Tau-side clock/readout law.

UGC12506 `epsilon_t` normalization derivation gate:

```text
Given:
    L >= 0 is a residual-blind source clock/readout load.

Require:
    epsilon_t is dimensionless.
    epsilon_t(0) = 0.
    epsilon_t is monotone in L.
    epsilon_t <= epsilon_cap.

Minimal bounded response map:
    Gamma_clock = L / (1 + L)
    epsilon_t = epsilon_cap * Gamma_clock
```

Current UGC12506 specialization:

```text
L ~= 2.13728
Gamma_clock ~= 0.681253
epsilon_cap = 0.035
epsilon_t ~= 0.023844
```

Bridge consequence: the shape `L/(1+L)` is now a conditional derived bounded
response map. The open piece is the origin of `epsilon_cap`: it must be derived
from Tau-side clock/readout geometry or frozen as a predeclared class constant
before any accepted `Xi_t` endpoint is allowed.

UGC12506 small-mismatch cap protocol gate:

```text
Xi_t = 1 + epsilon_t
Xi_t^2 = 1 + 2 epsilon_t + epsilon_t^2

quadratic-to-linear ratio = epsilon_t / 2

protocol tolerance:
    eta_quad = 0.02

admissible linear-regime bound:
    epsilon_t <= 2 eta_quad = 0.04

frozen protocol cap:
    epsilon_cap = 0.035
```

Current cap consequences:

```text
epsilon_cap = 0.035 < 0.04
max quadratic-to-linear ratio at cap = 0.0175
max Xi_t^2 fractional shift at cap = (1.035)^2 - 1 ~= 0.071225
```

Bridge consequence: `epsilon_cap = 0.035` is now frozen only as a conservative
small-mismatch protocol cap inside the linearized time-readout regime. It is
not a universal Tau Core constant and does not turn the UGC12506 source shell
into an endpoint. Promotion still requires either an accepted class-cap
manifest or a deeper Tau-side clock/readout geometry derivation.

UGC12506 accepted-manifest gate:

```text
status:
    U12506_XI_T_ACCEPTED_MANIFEST_NOT_READY

passes:
    source-only Xi_t shell exists
    no residual/v_obs leakage in shell, normalization, or cap summaries
    path term is zero because path evidence is not established
    bounded normalization shape is available
    epsilon_cap is protocol-frozen inside the linearized regime

blocked:
    K_t(R) envelope mapping still needs independent source review
    clock/readout settling proxy is still unfilled
    epsilon_cap must be recorded as protocol cap, not universal Tau constant
    deeper Tau-side cap origin remains open for any universal-law claim

endpoint_scores_allowed:
    false
```

Bridge consequence: UGC12506 is now stronger than a raw diagnostic `Xi_t`
replay, because it has a source-only clock shell, bounded source-load
normalization, and small-mismatch cap protocol. It is still not an endpoint.
The next promotion step is a residual-blind source review of the `K_t(R)`
envelope mapping and clock/readout settling proxy, followed by rerunning the
accepted-manifest gate.

UGC12506 source-review packet:

```text
status:
    U12506_XI_T_SOURCE_REVIEW_PACKET_READY_RESPONSE_PENDING

review obligations:
    high-spin / low-density H I envelope as clock-readout settling proxy
    high-inclination PV/envelope context as time-slice proxy
    radial K_t envelope ramp from R_d/R_opt to R_HI
    caveated approaching/receding asymmetry phase component
    zero path/environment policy unless cone/path evidence appears
    epsilon_cap carried only as small-mismatch protocol cap

forbidden promotion inputs:
    rotation residuals
    endpoint RMSE
    Newton/MOND/RAR/RMOND/TPG baseline ranks
    wrong-family Tau scores
    post-hoc epsilon_cap changes
    foreground/path rescue without source evidence

endpoint_scores_allowed:
    false
```

Bridge consequence: the UGC12506 `Xi_t` route has moved from informal
worklist to review-ready source packet. The packet does not validate the route;
it makes the next validation step auditable.

UGC12506 source-review response intake:

```text
status after completed reviewer response:
    U12506_XI_T_SOURCE_REVIEW_RESPONSE_USABLE_MANIFEST_GATE_REQUIRED

reviewer verdict:
    ACCEPT_KT_CARRY_CAP_AS_CAVEATED_INTERVAL

validator checks:
    response uses one allowed response
    source inputs are cited
    forbidden inputs are absent
    response does not authorize endpoint scoring
    response does not authorize accepted manifest by itself
    response does not promote epsilon_cap to universal Tau constant

next gate:
    rerun UGC12506 Xi_t accepted-manifest gate

endpoint_scores_allowed:
    false
```

Bridge consequence: the executable promotion chain is now explicit:

```text
source packet
    -> independent source-review response
    -> response intake validator
    -> accepted-manifest gate
    -> caveated interval/control manifest
    -> separate endpoint-permission gate before any scoring
```

UGC12506 caveated interval/control manifest:

```text
accepted-manifest gate status:
    U12506_XI_T_CAVEATED_INTERVAL_CONTROL_MANIFEST_READY_ENDPOINT_BLOCKED

control manifest status:
    U12506_XI_T_CAVEATED_INTERVAL_CONTROL_MANIFEST_READY

manifest kind:
    caveated_interval_control

frozen interval:
    epsilon_t in [0, 0.0238438]
    Xi_t in [1, 1.02384]

policies:
    K_t(R) is carried only as caveated interval/control manifest
    asymmetry remains caveated phase component
    path term remains zero unless later source path review establishes it
    epsilon_cap = 0.035 remains protocol cap, not universal Tau constant

artifact:
    data/derived/ugc12506_xi_t_caveated_interval_control_manifest.csv

builder:
    scripts/build_ugc12506_xi_t_caveated_interval_control_manifest.py
```

Bridge consequence: UGC12506 has moved beyond a raw diagnostic `Xi_t` replay.
It now has a source-reviewed, caveated interval/control manifest. This is a
stronger protocol object, but endpoint scoring remains blocked until a separate
endpoint-permission gate is defined and passed.

UGC12506 caveated interval/control replay:

```text
status:
    U12506_XI_T_CAVEATED_INTERVAL_CONTROL_REPLAY_COMPLETE_NOT_ENDPOINT

control interval:
    epsilon_t in [0, 0.0238438]
    Xi_t in [1, 1.02384]

scores:
    control low RMSE  = 77.540886 km/s
    control mid RMSE  = 77.011360 km/s
    control high RMSE = 76.485611 km/s

effect:
    RMSE improvement versus low edge = 1.055275 km/s
    observed points inside interval = 0.0
    observed points inside interval with errors = 0.0

artifact:
    data/derived/ugc12506_xi_t_caveated_interval_control_replay_summary.csv

figure:
    figures/endpoint_diagnostics/ugc12506_xi_t_caveated_interval_control_replay.png
```

Bridge consequence: the source-reviewed `Xi_t` route moves UGC12506 in the
expected direction, but the protocol cap is too small to rescue the rotation
curve. This is a useful negative-control discipline: the time-readout channel is
not being used as an arbitrary amplitude knob.

UGC12506 `Theta_morph` / `Xi_t` separation gate:

```text
separation status:
    U12506_THETA_XIT_CHANNELS_SEPARATED_ENDPOINT_STILL_BLOCKED

Theta_morph role:
    additive morphology/trajectory phase kernel
    v_theta^2(R) = v_projection_history^2(R) + A_theta K_theta(R)

Xi_t role:
    multiplicative clock/readout interval control
    Xi_t(R) = 1 + epsilon_t K_t(R)

formula roles distinct:
    true

source overlap present:
    true

path term established:
    false

combined endpoint allowed:
    false
```

Bridge consequence: with the refined terminology, UGC12506 is no longer an
ambiguous single "time/morphology" route.  `Theta_morph` is the additive
morphology-state phase diagnostic, while `Xi_t` is the small clock/readout
control interval.  This is a real architectural clarification.  It is not an
endpoint promotion, because the current evidence still overlaps through the
high-spin/envelope/asymmetry source context and the path term remains
unestablished.

UGC12506 source-nonoverlap gate:

```text
nonoverlap status:
    PARTIAL_NONOVERLAP_CONTROL_ALLOWED_COMBINED_ENDPOINT_BLOCKED

Theta-only evidence:
    late-settling outer radial shape

Xi_t-only evidence:
    epsilon_t small-mismatch protocol cap

shared / partially shared evidence:
    high spin
    extended low-density H I envelope
    high-inclination / edge-on PV geometry
    approaching-receding H I asymmetry

excluded:
    foreground/path environment until source path review establishes it

combined control replay allowed:
    true

combined endpoint allowed:
    false
```

Bridge consequence: UGC12506 can now proceed to a combined-control replay with
the assignments frozen by the nonoverlap ledger.  That replay is allowed only
as a control because enough source facts remain shared that a positive score
would not yet be an endpoint validation of independent `Theta_morph` and
`Xi_t` channels.

UGC12506 combined-control replay:

```text
combined control status:
    U12506_THETA_XIT_COMBINED_CONTROL_REPLAY_COMPLETE_NOT_ENDPOINT

Theta_morph-only RMSE:
    64.12 km/s

ledger-strict combined cap-only RMSE:
    60.31 km/s

caveated shared-K_t high stress RMSE:
    63.21 km/s

best control:
    Theta_morph + Xi_t protocol cap only

combined endpoint allowed:
    false
```

Bridge consequence: the strict ledger-controlled combination improves the
UGC12506 control curve by about `3.81 km/s` relative to the `Theta_morph`
diagnostic alone.  The shared-context shaped `K_t(R)` stress curve improves
less.  This supports the channel-accounting choice: the cleanest current
control signal is the morphology-phase curve plus the small `Xi_t` cap, while
the shaped `K_t` route remains caveated because its source context overlaps
with the morphology channel.  No endpoint claim follows from this replay.

Time-projection + morphology control-galaxy audit:

```text
audit status:
    TIME_MORPHOLOGY_CONTROL_GALAXY_IMPROVEMENT_AUDIT_COMPLETE_NOT_ENDPOINT

galaxies audited:
    6

improves clearly:
    UGC12506  delta RMSE = -3.81 km/s
    NGC4088  delta RMSE = -1.04 km/s

near neutral:
    NGC4183  delta RMSE = -0.01 km/s
    NGC5907  delta RMSE = +0.03 km/s

worsens:
    NGC7331  delta RMSE = +0.16 km/s
    NGC4013  delta RMSE = +0.53 km/s

endpoint validation claim:
    false
```

Bridge consequence: the current time/projection-morphology layer is selective,
not universal.  It helps where source context indicates strong history,
asymmetry, or projection-clock relevance, and it is neutral or harmful where
the current proxy is not independently supported.  This is a useful guardrail:
`Xi_t` is not behaving as an all-purpose amplitude knob.

Why the worsened rows worsened:

```text
NGC4013:
    current active route:
        mixed warp / vertical-overlay readout
    failure mode:
        the generic Xi_t proxy overlaps the already active mixed geometry
    interpretation:
        adding Xi_t double-counts source structure already present in the
        mixed kernel and moves an already close curve in the wrong direction
    gate consequence:
        keep Xi_t = 1 unless independent, non-overlapping clock/readout
        evidence is source-frozen

NGC7331:
    current active route:
        broad vertical / outer-warp mixed readout
    failure mode:
        the broad mixed window already carries the available phase information
    interpretation:
        adding Xi_t over-rescales a saturated broad-window proxy rather than
        adding a separately frozen time/readout channel
    gate consequence:
        sharpen the outer-warp / vertical source window before any clock layer;
        keep Xi_t = 1 for the current endpoint score

NGC5907:
    current active route:
        edge-on projection / warp-truncation readout
    failure mode:
        near-neutral to slightly worse response
    interpretation:
        projection kernel is already saturated at the present proxy level
    gate consequence:
        no accepted Xi_t promotion from the present proxy
```

Bridge rule: a worsened `Xi_t` replay is a rejection of the current
clock/readout proxy for that source state. It is not permission to retune the
clock amplitude from the rotation residual. The default is `Xi_t = 1` until a
non-overlapping, residual-blind clock/readout manifest is promoted.

Problematic-galaxy projection-channel ledger:

```text
ledger status:
    PROBLEMATIC_GALAXY_PROJECTION_CHANNEL_LEDGER_BUILT_NOT_ENDPOINT

endpoint-allowed rows:
    0

UGC12506:
    priority channel = mass-distribution / envelope + metric-closure readout
    secondary        = observer/path edge-on projection, clock interval control
    reason           = high-spin, edge-on, extended H I envelope stress remains
                       underpredicted by the current small Xi_t cap

NGC4088:
    priority channel = trajectory/phase + asymmetry/history readout
    secondary        = clock readout as control only
    reason           = warp/history/asymmetry source state is the clearest
                       current improving time/projection case

NGC4013:
    priority channel = mixed warp / vertical-overlay readout
    forbidden now    = generic Xi_t promotion
    reason           = current Xi_t proxy double-counts the mixed geometry

NGC7331:
    priority channel = source-sharpened vertical / outer-warp readout
    secondary        = metric/closure only after window sharpening
    reason           = broad mixed window is saturated and over-rescaled by Xi_t

NGC5907:
    priority channel = observer/path edge-on projection
    reason           = projection kernel appears saturated at current proxy level

NGC4183:
    priority channel = quiet weak-projection limit
    reason           = null/weak projection control
```

Bridge consequence: the next work should not apply the same extra projection
layer to every problematic galaxy. Each row gets a different source-side
channel hypothesis, and every new channel remains blocked until source-freeze,
non-overlap, and ablation checks pass.

Problematic projection-channel next-gate execution plan:

```text
script:
    scripts/build_problematic_projection_channel_next_gates.py

outputs:
    data/derived/problematic_projection_channel_next_gates.csv
    data/derived/problematic_projection_channel_next_gates_summary.csv
    reports/problematic_projection_channel_next_gates.md

status:
    PROBLEMATIC_PROJECTION_CHANNEL_NEXT_GATES_BUILT_NOT_ENDPOINT

endpoint permissions:
    n_endpoint_allowed = 0

currently runnable control/replay paths:
    UGC12506:
        U12506_MASS_ENVELOPE_METRIC_CLOSURE_ABLATION_GATE
        status = CONTROL_REPLAY_READY_ENDPOINT_BLOCKED
        interpretation = source-native NFW/HSE mass-envelope plus
                         metric-closure seed can be ablated against
                         Theta_morph-only, Theta+Xi_t cap-only, and
                         source-envelope controls

    NGC4088:
        N4088_CLOCK_NONOVERLAP_EVIDENCE_GATE
        status = NO_NEW_ENDPOINT_KEEP_ACCEPTED_ADDITIVE_ROUTE
        interpretation = accepted additive warp/history route remains active;
                         clock readout stays a control unless independent
                         non-overlapping source-clock evidence is acquired

blocked or inactive rows:
    NGC4013:
        BLOCKED_CURRENT_XIT_REJECTED
    NGC7331:
        REPLAY_PATH_EXISTS_ENDPOINT_NOT_PROMOTED
    NGC5907:
        SATURATED_CONTROL_NO_NEW_LAYER
    NGC4183:
        RETAIN_NULL_CONTROL
```

Bridge consequence: the channel ledger is now operational. The framework can
move forward on UGC12506 and NGC4088 as control/replay work, but it still
prevents endpoint promotion for every problematic row until the relevant
source-freeze, non-overlap, and ablation obligations are closed.

UGC12506 source-native mass/envelope--closure ablation replay:

```text
scripts:
    scripts/build_ugc12506_source_native_nfw_hse_shell.py
    scripts/run_ugc12506_source_native_nfw_hse_replay.py

outputs:
    data/derived/ugc12506_source_native_nfw_hse_replay_summary.csv
    data/derived/ugc12506_source_native_nfw_hse_replay_scores.csv
    figures/endpoint_diagnostics/ugc12506_source_native_nfw_hse_replay.png
    reports/ugc12506_source_native_nfw_hse_replay.md

status:
    UGC12506_SOURCE_NATIVE_NFW_HSE_REPLAY_IMPROVES_RD_PROXY_NOT_PRIOR_DIAGNOSTICS

RMSE:
    baryonic carrier:              116.02 km/s
    source-envelope branch:        102.48 km/s
    edge-on/envelope/asym branch:  102.43 km/s
    old Rd-proxy NFW/HSE branch:    77.86 km/s
    source-native NFW/HSE branch:   77.54 km/s
    best prior diagnostic branch:   37.36 km/s

claim boundary:
    replay/control evidence, not endpoint validation
```

Bridge consequence: UGC12506 is no longer well-described as a pure clock or
observer-projection problem. The source-native NFW/HSE replay confirms that a
mass/envelope plus metric-closure channel moves in the right direction and
beats the lower source branches, but it still leaves a large residual gap. The
next UGC12506 theory task is therefore not to turn up `Xi_t`; it is to derive a
stronger source-frozen closure/readout channel that can account for the rapid
rise and high-spin envelope without using the rotation residual to choose the
kernel or amplitude.

UGC12506 source-derived beta-closure normalization candidate:

```text
diagnostic fixed-shape optimum:
    beta_diag = 3.876
    RMSE      = 7.48 km/s
    status    = residual-aware diagnostic only

source-only candidate:
    beta_cl
      = 1
        + (lambda_spin / 0.10) * (chi2_iso / chi2_NFW - 1)_+
        + sin^2(i) * max((i - 80 deg) / 10 deg, 0)

UGC12506 value:
    lambda_spin = 0.15
    chi2_iso / chi2_NFW - 1 = 1.571
    edge-on load = 0.597
    beta_cl = 3.954
    RMSE    = 7.67 km/s

script:
    scripts/run_ugc12506_source_derived_beta_closure_replay.py

outputs:
    data/derived/ugc12506_source_derived_beta_closure_replay_summary.csv
    data/derived/ugc12506_source_derived_beta_closure_replay_scores.csv
    data/derived/ugc12506_source_derived_beta_closure_derivation.csv
    figures/endpoint_diagnostics/ugc12506_source_derived_beta_closure_replay.png
    reports/ugc12506_source_derived_beta_closure_replay.md

status:
    UGC12506_SOURCE_DERIVED_BETA_CLOSURE_REPLAY_MATCHES_DIAGNOSTIC_SHAPE_NOT_ENDPOINT
```

Bridge consequence: this is the first concrete UGC12506 closure-normalization
formula that reproduces the needed amplitude scale without using the rotation
curve to compute `beta_cl`. It remains post-diagnostic because the rule was
formulated after the residual-aware beta diagnostic. The next proof/validation
gate is to predeclare this beta-closure rule and transfer it to independent
high-spin, high-inclination NFW/envelope systems, or derive the same expression
from the Tau-side closure/load functional before scoring.

UGC12506 beta-closure transfer predeclaration:

```text
script:
    scripts/build_ugc12506_beta_closure_transfer_predeclaration.py

outputs:
    data/derived/ugc12506_beta_closure_transfer_candidates.csv
    data/derived/ugc12506_beta_closure_transfer_source_worklist.csv
    data/derived/ugc12506_beta_closure_transfer_predeclaration_summary.csv
    reports/ugc12506_beta_closure_transfer_predeclaration.md

status:
    UGC12506_BETA_CLOSURE_TRANSFER_CANDIDATES_PREDECLARED_SOURCE_ACQUISITION_REQUIRED

selection inputs:
    SPARC inclination, RHI/Rdisk, MHI, Vflat, quality flag
    no rotation residuals

candidate count:
    11 non-UGC12506 galaxies

top source-acquisition targets:
    UGC11455
    ESO563-G021
    IC4202
    NGC0891
    NGC4013
    NGC2841
    NGC4157
    NGC4217

required source-native fields before replay:
    lambda_spin
    chi2_NFW
    chi2_ISO
    source-native halo-fit reference
    PV/envelope method notes

endpoint/replay permission:
    none yet
```

Bridge consequence: the beta-closure rule now has an independent transfer
route. The correct next move is source acquisition for the predeclared target
list, not further tuning on UGC12506.

UGC12506 beta-closure transfer halo-fit acquisition:

```text
script:
    scripts/acquire_ugc12506_beta_closure_transfer_halo_fit_fields.py

source:
    Li et al. 2020, ApJS 247, 31; VizieR J/ApJS/247/31

outputs:
    data/external/literature/li2020_sparc_halo_catalog/table1_vizier.tsv
    data/derived/ugc12506_beta_closure_transfer_halo_fit_fields.csv
    data/derived/ugc12506_beta_closure_transfer_halo_fit_worklist_update.csv
    data/derived/ugc12506_beta_closure_transfer_halo_fit_acquisition_summary.csv
    reports/ugc12506_beta_closure_transfer_halo_fit_acquisition.md

status:
    UGC12506_BETA_CLOSURE_TRANSFER_HALO_FIT_FIELDS_FILLED_SPIN_AND_PV_STILL_BLOCKED

filled fields:
    chi2_ISO
    chi2_NFW
    nfw_preference_load = max(chi2_ISO / chi2_NFW - 1, 0)

still blocked:
    lambda_spin
    PV/envelope method notes
    independent replay freeze

endpoint/replay permission:
    none
```

Bridge consequence: the first transfer blocker is reduced, but the result is
not a transfer replay. The acquisition also sharpens the source-side meaning of
the UGC12506 beta-closure mechanism: high inclination, large H I extent, and
large gas mass are not sufficient by themselves. The UGC12506-style
normalization route needs a positive source-side NFW-preference load. In the
current predeclared list, that load is positive for NGC0891, NGC7331, NGC2841,
NGC0801, and weakly NGC4013, while UGC11455, ESO563-G021, and IC4202 are
edge-on/massive candidates with pISO-preferred halo fits under Li et al. (2020).
Those rows are still scientifically useful, but mainly as control or
alternative-branch candidates unless an independent spin/PV source review
changes the admissible transfer route.

UGC12506 beta-closure transfer priority gate:

```text
script:
    scripts/build_ugc12506_beta_closure_transfer_priority_gate.py

outputs:
    data/derived/ugc12506_beta_closure_transfer_priority_gate.csv
    data/derived/ugc12506_beta_closure_transfer_priority_gate_summary.csv
    reports/ugc12506_beta_closure_transfer_priority_gate.md

status:
    UGC12506_BETA_CLOSURE_TRANSFER_PRIORITY_GATE_BUILT_ENDPOINT_BLOCKED

primary NFW-preference targets:
    NGC0891
    NGC7331

weak/secondary NFW-preference targets:
    NGC2841
    NGC0801
    NGC4013

pISO-preferred controls or alternative branches:
    UGC11455
    ESO563-G021
    IC4202
    NGC4157
    NGC4217
    NGC3521

endpoint/replay permission:
    none
```

Bridge consequence: this is a useful tightening, not a validation result. The
beta-closure transfer now has a defensible first source-review queue:
NGC0891 and NGC7331. The next allowed work is to freeze their `lambda_spin`
and PV/envelope evidence from independent sources before any replay score is
computed.

UGC12506 beta-closure primary source-freeze preflight:

```text
script:
    scripts/build_ugc12506_beta_closure_primary_source_freeze_preflight.py

outputs:
    data/derived/ugc12506_beta_closure_primary_source_freeze_preflight.csv
    data/derived/ugc12506_beta_closure_primary_source_freeze_evidence.csv
    data/derived/ugc12506_beta_closure_primary_source_freeze_preflight_summary.csv
    reports/ugc12506_beta_closure_primary_source_freeze_preflight.md

status:
    UGC12506_BETA_CLOSURE_PRIMARY_SOURCE_FREEZE_PREFLIGHT_BUILT_SPIN_BLOCKED

NGC0891:
    PV/envelope context accepted from edge-on H I XV/PV and envelope-tracing literature.
    lambda_spin remains blocked.

NGC7331:
    PV/envelope context accepted from cached THINGS products and published
    H I/vertical-context literature.
    lambda_spin remains blocked.

endpoint/replay permission:
    none
```

Bridge consequence: the primary transfer targets have passed only the
PV/envelope-context side of the source-freeze gate. The missing object is now
precise: either a direct source-native `lambda_spin` measurement must be
acquired, or a residual-blind source-only spin proxy must be predeclared before
any beta-closure replay can be run.

UGC12506 beta-closure direct lambda/spin source-acquisition gate:

```text
script:
    scripts/acquire_ugc12506_beta_closure_direct_lambda_spin_sources.py

outputs:
    data/derived/ugc12506_beta_closure_direct_lambda_spin_source_evidence.csv
    data/derived/ugc12506_beta_closure_direct_lambda_spin_source_gate_summary.csv
    reports/ugc12506_beta_closure_direct_lambda_spin_source_gate.md

status:
    UGC12506_BETA_CLOSURE_DIRECT_LAMBDA_SOURCE_GATE_PARTIAL_ENDPOINT_BLOCKED

NGC7331:
    disc-spin-like lambda = 0.423 from Marr 2015 lognormal disc model.
    Not accepted for beta_cl because it is not the same halo/envelope
    lambda_spin definition.

NGC0891:
    no accepted direct source-native lambda_spin cached.
    NGC891-like lambda context is model-analogue only.

endpoint/replay permission:
    none
```

Bridge consequence: the direct-source route is informative but does not yet
unlock a transfer replay. The NGC7331 value requires a definition-conversion
review; NGC0891 requires either direct spin acquisition or proxy review.

NGC0891 beta-closure spin-source hunt update:

```text
script:
    scripts/acquire_ugc12506_beta_closure_ngc0891_spin_source_hunt_update.py

outputs:
    data/derived/ugc12506_beta_closure_ngc0891_spin_source_hunt_update_sources.csv
    data/derived/ugc12506_beta_closure_ngc0891_spin_source_hunt_update_worklist.csv
    data/derived/ugc12506_beta_closure_ngc0891_spin_source_hunt_update_summary.csv
    reports/ugc12506_beta_closure_ngc0891_spin_source_hunt_update.md

status:
    NGC0891_CONTEXT_STRENGTHENED_DIRECT_LAMBDA_STILL_BLOCKED

context accepted:
    cold H I halo
    lagging extraplanar rotation
    low-angular-momentum accretion context
    stationary/extraplanar-gas model context

endpoint/replay permission:
    none
```

Bridge consequence: NGC0891 is strengthened as a physically relevant
halo/envelope/projection transfer target, but the precise `lambda_spin` slot is
still not filled. Context is not a substitute for the Tau-side normalization
field.

NGC7331 beta-closure lambda definition-conversion gate:

```text
script:
    scripts/build_ugc12506_beta_closure_lambda_definition_conversion_gate.py

outputs:
    data/derived/ugc12506_beta_closure_lambda_definition_conversion_checks.csv
    data/derived/ugc12506_beta_closure_lambda_definition_conversion_comparison.csv
    data/derived/ugc12506_beta_closure_lambda_definition_conversion_worklist.csv
    data/derived/ugc12506_beta_closure_lambda_definition_conversion_summary.csv
    reports/ugc12506_beta_closure_lambda_definition_conversion_gate.md

status:
    NGC7331_DISC_LAMBDA_CONTEXT_ACCEPTED_DIRECT_SUBSTITUTION_REJECTED

direct-substitution comparison:
    beta_if_direct_disc_lambda_substituted = 1.731
    beta_if_proxy_candidate_used           = 1.235

endpoint/replay permission:
    none
```

Bridge consequence: this is a preserved negative gate, not a setback. Marr's
NGC7331 disc-spin value is source-side and useful, but it is not the same
Tau-side halo/envelope normalization slot used by `beta_cl`. A residual-blind
disc-to-halo/envelope conversion functional must be derived before this route
can replay.

UGC12506 beta-closure Bullock-like disk-inferred spin conversion proxy gate:

```text
script:
    scripts/build_ugc12506_beta_closure_bullock_spin_conversion_proxy_gate.py

outputs:
    data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv
    data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_comparison.csv
    data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_checks.csv
    data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_summary.csv
    reports/ugc12506_beta_closure_bullock_spin_conversion_proxy_gate.md

status:
    BULLOCK_DISK_INFERRED_SPIN_PROXY_COMPUTED_REVIEW_REQUIRED

formula:
    j_disk = 2 Rdisk Vflat
    R200   = V200 / (10 H0)
    lambda'_disk = j_disk / (sqrt(2) R200 V200)

primary comparison:
    NGC0891 lambda'_disk = 0.035
    NGC0891 exposure-proxy lambda_spin = 0.149
    NGC7331 lambda'_disk = 0.033
    NGC7331 exposure-proxy lambda_spin = 0.136

endpoint/replay permission:
    none
```

Bridge consequence: this is a more standard angular-momentum conversion
candidate, but it is deliberately conservative and does not fill the Tau-side
`beta_cl` spin slot by itself. The disagreement with the exposure proxy is
useful: it forces the next gate to be an independent review choosing direct
spin acquisition, exposure proxy, Bullock-like conversion, or route rejection
before any replay.

UGC12506 beta-closure source-declared spin proxy gate:

```text
script:
    scripts/build_ugc12506_beta_closure_source_declared_spin_proxy_gate.py

outputs:
    data/derived/ugc12506_beta_closure_source_declared_spin_proxy_fields.csv
    data/derived/ugc12506_beta_closure_source_declared_spin_proxy_transfer_queue.csv
    data/derived/ugc12506_beta_closure_source_declared_spin_proxy_gate_summary.csv
    reports/ugc12506_beta_closure_source_declared_spin_proxy_gate.md

status:
    UGC12506_BETA_CLOSURE_SOURCE_DECLARED_SPIN_PROXY_BUILT_ENDPOINT_BLOCKED

proxy candidate:
    lambda_spin_proxy =
        0.10 * (1 + 0.35 extent_load
                  + 0.25 velocity_load
                  + 0.25 gas_load
                  + 0.15 edgeon_load)

source fields:
    RHI/Rdisk
    Vflat
    H I mass
    inclination

primary proxy-transfer review target:
    NGC0891

secondary proxy-transfer review targets:
    NGC7331
    NGC2841
    NGC0801
    NGC4013

endpoint/replay permission:
    none
```

Bridge consequence: this reduces the old undefined `lambda_spin` slot to a
source-only, dimensionless, reviewable proxy candidate. It does not prove that
the proxy is a physical spin measurement and it does not promote a transfer
endpoint. The next admissible step is an independent review or direct
source-native spin acquisition before any beta-closure transfer replay.

UGC12506 beta-closure spin proxy independent-review bundle:

```text
script:
    scripts/build_ugc12506_beta_closure_spin_proxy_review_bundle.py

outputs:
    data/derived/ugc12506_beta_closure_spin_proxy_review_packet.csv
    data/derived/ugc12506_beta_closure_spin_proxy_review_obligations.csv
    data/derived/ugc12506_beta_closure_spin_proxy_review_forbidden_inputs.csv
    data/derived/ugc12506_beta_closure_spin_proxy_review_response_template.csv
    data/derived/ugc12506_beta_closure_spin_proxy_review_bundle_manifest.csv
    data/derived/ugc12506_beta_closure_spin_proxy_review_bundle_summary.csv
    reports/ugc12506_beta_closure_spin_proxy_review_prompt.md
    reports/ugc12506_beta_closure_spin_proxy_review_bundle.md
    review_bundles/ugc12506_beta_closure_spin_proxy_review_bundle.zip

status:
    U12506_BETA_SPIN_PROXY_REVIEW_BUNDLE_READY_RESPONSE_PENDING

review obligations:
    source fields accepted or proxy rejected
    weight rule accepted or replaced before replay
    NGC7331 disc-lambda context-only boundary accepted or conversion supplied
    transfer target scope accepted or restricted

endpoint/replay permission:
    none
```

Bridge consequence: the source-only proxy route is now reviewable without repo
access and without residual leakage. It now includes the Bullock-like
conversion proxy as a conservative control alongside the source-declared
exposure proxy. Neither is an accepted Tau-side amplitude law. The next gate is
an independent response intake with an explicit spin-normalization route
selection: `EXPOSURE_PROXY`, `BULLOCK_DISK_CONVERSION`,
`DIRECT_SOURCE_NATIVE_SPIN`, `NEW_RESIDUAL_BLIND_RULE`, or rejection. Until
that route is selected and accepted, the beta-closure transfer replay remains
blocked.

UGC12506 beta-closure spin proxy review-response intake:

```text
script:
    scripts/run_ugc12506_beta_closure_spin_proxy_review_response_intake.py

outputs:
    data/derived/ugc12506_beta_closure_spin_proxy_review_response_intake_checks.csv
    data/derived/ugc12506_beta_closure_spin_proxy_review_response_intake_summary.csv
    reports/ugc12506_beta_closure_spin_proxy_review_response_intake.md

current status:
    U12506_BETA_SPIN_PROXY_REVIEW_RESPONSE_PENDING_ENDPOINT_BLOCKED

selected spin-normalization route:
    PENDING_INDEPENDENT_REVIEW

endpoint/replay permission:
    none
```

Bridge consequence: the response-intake contract is now explicit. Without a
completed independent review response, proxy promotion, beta-closure replay
preflight, and endpoint scoring all remain blocked.

UGC12506 beta-closure spin-route prefreeze gate:

```text
script:
    scripts/build_ugc12506_beta_closure_spin_route_prefreeze_gate.py

outputs:
    data/derived/ugc12506_beta_closure_spin_route_prefreeze_gate.csv
    data/derived/ugc12506_beta_closure_spin_route_prefreeze_values.csv
    data/derived/ugc12506_beta_closure_spin_route_prefreeze_summary.csv
    reports/ugc12506_beta_closure_spin_route_prefreeze_gate.md

current status:
    U12506_BETA_SPIN_ROUTE_PREFREEZE_BLOCKED_REVIEW_ROUTE_PENDING

selected spin-normalization route:
    PENDING_INDEPENDENT_REVIEW

endpoint/replay permission:
    none
```

Bridge consequence: this is the mechanical replay lock after the review
bundle. The bridge now has a route-selection contract, an intake contract, and
a downstream prefreeze contract. No `beta_cl` transfer values can be frozen
until the independent review selects an accepted spin-normalization route.

UGC12506 beta-closure spin-route decision matrix:

```text
script:
    scripts/build_ugc12506_beta_closure_spin_route_decision_matrix.py

outputs:
    data/derived/ugc12506_beta_closure_spin_route_decision_matrix.csv
    data/derived/ugc12506_beta_closure_spin_route_decision_matrix_summary.csv
    reports/ugc12506_beta_closure_spin_route_decision_matrix.md

status:
    U12506_BETA_SPIN_ROUTE_DECISION_MATRIX_READY_REVIEW_REQUIRED

routes:
    EXPOSURE_PROXY
    BULLOCK_DISK_CONVERSION
    DIRECT_SOURCE_NATIVE_SPIN
    REJECT_ROUTE

endpoint/replay permission:
    none
```

Bridge consequence: the amplitude-normalization choice is now explicitly
auditable. The bridge no longer has a single hidden proxy path; it exposes the
two computable residual-blind routes, the preferred-but-missing direct-source
route, and the valid negative outcome where the route is rejected.

UGC12506 beta-closure scoring launch gate:

```text
script:
    scripts/build_ugc12506_beta_closure_scoring_launch_gate.py

outputs:
    data/derived/ugc12506_beta_closure_scoring_launch_inputs.csv
    data/derived/ugc12506_beta_closure_scoring_launch_gates.csv
    data/derived/ugc12506_beta_closure_scoring_protocol_skeleton.csv
    data/derived/ugc12506_beta_closure_scoring_launch_summary.csv
    reports/ugc12506_beta_closure_scoring_launch_gate.md

status:
    U12506_BETA_CLOSURE_SCORING_LAUNCH_BLOCKED_REVIEW_PREFREEZE_PENDING

current gate counts:
    required inputs = 9
    missing inputs = 0
    pass gates = 2
    blocked gates = 3

endpoint/replay permission:
    none
```

Bridge consequence: the path to scoring is now explicit. The launch blocker is
not missing files; it is missing independent route acceptance, prefrozen
spin-normalization values, and an accepted carrier. The future scoring script
is isolated as the only step allowed to read `vobs`, and that step remains
blocked until the formula manifest exists.

UGC12506 beta-closure transfer carrier-freeze gate:

```text
script:
    scripts/build_ugc12506_beta_closure_transfer_carrier_freeze_gate.py

outputs:
    data/derived/ugc12506_beta_closure_transfer_carrier_route_decision_matrix.csv
    data/derived/ugc12506_beta_closure_transfer_carrier_manifest.csv
    data/derived/ugc12506_beta_closure_transfer_carrier_freeze_gates.csv
    data/derived/ugc12506_beta_closure_transfer_carrier_freeze_summary.csv
    reports/ugc12506_beta_closure_transfer_carrier_freeze_gate.md

status:
    U12506_BETA_CLOSURE_TRANSFER_CARRIER_FREEZE_BLOCKED_CARRIER_REVIEW_PENDING

carrier routes:
    BARYONIC_050_FAST_PACKET = reviewable, not accepted
    LI2020_NFW_FIT_CARRIER = diagnostic/control only by default
    SOURCE_NATIVE_NFW_HSE_TRANSFER_CARRIER = preferred, currently missing

observed-curve read permission:
    false

endpoint/replay permission:
    none
```

Bridge consequence: `beta_cl` is now correctly treated as an amplitude/closure
factor, not a complete scoring formula. A velocity-squared carrier must be
source-frozen before scoring. The Li et al. NFW route remains useful as a
control, but because it is based on published rotation-curve fit products it is
not promoted to an endpoint-safe carrier by default.

UGC12506 beta-closure carrier review bundle and intake:

```text
scripts:
    scripts/build_ugc12506_beta_closure_carrier_review_bundle.py
    scripts/run_ugc12506_beta_closure_carrier_review_response_intake.py

outputs:
    data/derived/ugc12506_beta_closure_carrier_review_bundle_summary.csv
    data/derived/ugc12506_beta_closure_carrier_review_obligations.csv
    data/derived/ugc12506_beta_closure_carrier_review_forbidden_inputs.csv
    data/derived/ugc12506_beta_closure_carrier_review_response_template.csv
    data/derived/ugc12506_beta_closure_carrier_review_response_intake_summary.csv
    data/derived/ugc12506_beta_closure_carrier_review_response_intake_checks.csv
    review_bundles/ugc12506_beta_closure_carrier_review_bundle.zip
    reports/ugc12506_beta_closure_carrier_review_bundle.md
    reports/ugc12506_beta_closure_carrier_review_response_intake.md

status:
    U12506_BETA_CARRIER_REVIEW_BUNDLE_READY_RESPONSE_PENDING
    U12506_BETA_CARRIER_REVIEW_RESPONSE_PENDING_ENDPOINT_BLOCKED

endpoint/replay permission:
    none
```

Bridge consequence: the carrier blocker is now actionable. A reviewer can
accept the minimal baryonic stress carrier, require a source-native transfer
carrier, or reject the route. The intake validator keeps endpoint scoring
blocked unless the response declares no forbidden residual or score inputs.

UGC12506 beta-closure transfer formula-freeze gate:

```text
script:
    scripts/build_ugc12506_beta_closure_transfer_formula_freeze_gate.py

outputs:
    data/derived/ugc12506_beta_closure_transfer_formula_manifest.csv
    data/derived/ugc12506_beta_closure_transfer_formula_freeze_gates.csv
    data/derived/ugc12506_beta_closure_transfer_formula_freeze_summary.csv
    reports/ugc12506_beta_closure_transfer_formula_freeze_gate.md

status:
    U12506_BETA_CLOSURE_TRANSFER_FORMULA_FREEZE_BLOCKED_PREFREEZE_PENDING

current gate counts:
    pass gates = 2
    blocked gates = 3
    formula manifest rows = 0

observed-curve read permission:
    false

endpoint/replay permission:
    none
```

Bridge consequence: the beta-closure transfer formula shell is now separated
from scoring. The manifest path is present, but it contains only headers until
an independent spin-route review and source-frozen spin values exist. This
prevents the future scoring runner from reading rotation curves before the
source-side formula is frozen.

UGC12506 beta-closure transfer scoring runner:

```text
script:
    scripts/run_ugc12506_beta_closure_transfer_scoring.py

outputs:
    data/derived/ugc12506_beta_closure_transfer_scoring_summary.csv
    data/derived/ugc12506_beta_closure_transfer_scoring_gates.csv
    data/derived/ugc12506_beta_closure_transfer_scoring_scores.csv
    data/derived/ugc12506_beta_closure_transfer_scoring_points.csv
    reports/ugc12506_beta_closure_transfer_scoring.md

status:
    U12506_BETA_CLOSURE_TRANSFER_SCORING_BLOCKED_LAUNCH_GATE

formula manifest:
    exists, but has zero rows

observed-curve read permission:
    false

endpoint/replay permission:
    none
```

Bridge consequence: the scoring script now exists as a separate stage, but it
correctly refuses to score while launch and formula-freeze conditions are not
met. The dormant scoring branch is implemented for a future accepted
`BARYONIC_050_FAST_PACKET` carrier: once a non-empty frozen formula manifest
and launch permission exist, it computes
`v_readout = sqrt(beta_cl * v_baryon_050^2)` and writes score-level plus
point-level control artifacts. This moves the bridge closer to scoring without
weakening leakage prevention.

UGC12506 beta-closure transfer scoring contract dry run:

```text
script:
    scripts/build_ugc12506_beta_closure_transfer_scoring_contract_dry_run.py

outputs:
    data/derived/ugc12506_beta_closure_transfer_scoring_contract_dry_run_summary.csv
    data/derived/ugc12506_beta_closure_transfer_scoring_contract_dry_run_scenarios.csv
    data/derived/ugc12506_beta_closure_transfer_scoring_contract_dry_run_manifest.csv
    data/derived/ugc12506_beta_closure_transfer_scoring_contract_dry_run_predictions.csv
    reports/ugc12506_beta_closure_transfer_scoring_contract_dry_run.md

status:
    U12506_BETA_CLOSURE_TRANSFER_SCORING_CONTRACT_DRY_RUN_READY_REVIEWS_PENDING

scenario count:
    2

dry-run manifest rows:
    22

prediction rows without vobs:
    656
```

Bridge consequence: the transfer path now has a no-vobs execution contract.
If an independent reviewer accepts either implemented spin-normalization route
and accepts the baryonic stress carrier, the scoring runner has the
non-observed inputs needed to execute. This is not a replay or endpoint score:
it only proves that the remaining blocker is review/freeze authorization, not
missing scoring infrastructure.

UGC12506 beta-closure transfer scoring unlock packet:

```text
script:
    scripts/build_ugc12506_beta_closure_transfer_scoring_unlock_packet.py

outputs:
    data/derived/ugc12506_beta_closure_transfer_scoring_unlock_packet_summary.csv
    data/derived/ugc12506_beta_closure_transfer_scoring_unlock_requirements.csv
    data/derived/ugc12506_beta_closure_spin_proxy_review_response_example_only_exposure_proxy.csv
    data/derived/ugc12506_beta_closure_spin_proxy_review_response_example_only_bullock_conversion.csv
    data/derived/ugc12506_beta_closure_carrier_review_response_example_only_baryonic_stress.csv
    review_bundles/ugc12506_beta_closure_transfer_scoring_unlock_packet.zip
    reports/ugc12506_beta_closure_transfer_scoring_unlock_packet.md

status:
    U12506_BETA_CLOSURE_TRANSFER_SCORING_UNLOCK_PACKET_READY_ACTIVE_RESPONSES_PENDING

required active response files:
    2

active response files present:
    0

example-only response files:
    3
```

Bridge consequence: the reviewer handoff is now explicit and machine-readable.
The packet gives exact acceptable response fields for the spin-route and
carrier decisions, but it does not write the active response files. Endpoint
scoring remains blocked until an independent response is supplied and the
standard intakes pass.

UGC12506 beta-closure post-review scoring launcher:

```text
script:
    scripts/run_ugc12506_beta_closure_post_review_scoring_launcher.py

outputs:
    data/derived/ugc12506_beta_closure_post_review_scoring_launcher_summary.csv
    data/derived/ugc12506_beta_closure_post_review_scoring_launcher_active_inputs.csv
    data/derived/ugc12506_beta_closure_post_review_scoring_launcher_chain.csv
    reports/ugc12506_beta_closure_post_review_scoring_launcher.md

status:
    U12506_BETA_CLOSURE_POST_REVIEW_SCORING_BLOCKED_ACTIVE_RESPONSES_PENDING

required active response files:
    2

active response files present:
    0

chain return codes:
    all zero
```

Bridge consequence: the post-review scoring path is now executable as one
command after external review. In the present state it proves the chain itself
is mechanically consistent while preserving the scientific blocker: no active
review response, no scoring, no observed-curve read.

UGC12506 beta-closure active review response installer:

```text
script:
    scripts/install_ugc12506_beta_closure_active_review_responses.py

default incoming directory:
    review_bundles/incoming/ugc12506_beta_closure_transfer_scoring/

expected incoming files:
    ugc12506_beta_closure_spin_proxy_review_response.csv
    ugc12506_beta_closure_carrier_review_response.csv

outputs:
    data/derived/ugc12506_beta_closure_active_review_response_install_summary.csv
    data/derived/ugc12506_beta_closure_active_review_response_install_checks.csv
    reports/ugc12506_beta_closure_active_review_response_installer.md

status:
    U12506_BETA_ACTIVE_REVIEW_RESPONSE_INSTALL_BLOCKED_INCOMING_PENDING_OR_INVALID

incoming active responses:
    0/2
```

Bridge consequence: the response installation step is now explicit and guarded.
Example-only rows, pending rows, missing files, endpoint flags, or residual-use
flags cannot silently become active reviewer responses. This preserves the
review wall while making the path to scoring operationally short once genuine
responses arrive.

UGC12506 beta-closure scoring-readiness dashboard:

```text
script:
    scripts/build_ugc12506_beta_closure_scoring_readiness_dashboard.py

outputs:
    data/derived/ugc12506_beta_closure_scoring_readiness_summary.csv
    data/derived/ugc12506_beta_closure_scoring_readiness_dashboard.csv
    reports/ugc12506_beta_closure_scoring_readiness_dashboard.md

status:
    U12506_BETA_CLOSURE_SCORING_READINESS_BLOCKED_ACTIVE_RESPONSES_PENDING

ready stages:
    no-vobs scoring contract dry run
    unlock packet

blocked stages:
    active response installer
    post-review launcher
    scoring launch gate
    formula-freeze gate
    transfer scoring runner
```

Bridge consequence: the route now has a single status ledger for moving toward
scoring without weakening the review wall. It records that the computational
path is mechanically prepared and the remaining blocker is scientific:
two independent active response files must be supplied and validated before the
launcher can open the formula/scoring gates. In the current state it reports no
scores, no endpoint claim, and no observed-curve read.

## Multichannel Time Projection Refinement

The current `Xi_t` tests should not be read as the full Tau Core time
projection mechanism. They instantiate only a narrow proxy/control slice. If
time projection is fundamental, it must be allowed to act in at least two
different places:

```text
1. source morphology time / phase:
       the galaxy's own Tau-side morphology clock state changes which
       morphology kernel or source phase is read out

2. observer/path projection time:
       the observer sees a projection-selected clock slice through the
       source-observer light bundle

3. optional path/environment time:
       the null-bundle environment may add a path term only when supported
       by source/path evidence
```

The factorized shell is:

```text
Xi_eff(R) =
    Xi_morph(R; Theta_src^tau)
  * Xi_obs(R; O_obs/path)
  * Xi_path(R; E_proj/history)

v_obs^2(R) =
  Xi_eff^2(R)
  [
    v_Newt^2(R)
    + delta_v_morph^2(R; Theta_src^tau, O_obs/path)
  ]
```

The morphology kernel itself may also change:

```text
K_readout(R)
  =
  K_0(R; K_present)
  + deltaK_morph_time(R; Theta_src^tau)
  + deltaK_obs_time(R; O_obs/path)
```

Small-mismatch expansion:

```text
Xi_i = 1 + epsilon_i

delta_v_t^2
  ~= 2 (epsilon_morph + epsilon_obs + epsilon_path)
      [
        v_Newt^2 + delta_v_morph^2
      ]
```

Bridge consequence: UGC12506's weak caveated `Xi_t` improvement does not test
this full branch. The current UGC12506 control only partially covers
`Xi_morph`, partially covers `Xi_obs`, sets `Xi_path = 1`, and does not include
kernel-deformation terms. Therefore its small improvement is evidence that the
narrow protocol cap is not a rescue knob, not evidence that fundamental time
projection is weak.

Current audit artifact:

```text
summary:
    data/derived/time_projection_multichannel_summary.csv

report:
    reports/time_projection_multichannel_fundamental_gate.md

status:
    TIME_PROJECTION_FUNDAMENTAL_MULTICHANNEL_GATE_RECORDED_NOT_DERIVED
```

Open proof obligation: derive the Tau-side origin and normalization of
`Xi_morph`, `Xi_obs`, and `Xi_path`, then freeze each channel from residual-blind
source evidence before any full time-projection endpoint.

Endpoint-preflight status:

```text
status:
    TIME_PROJECTION_ENDPOINT_PREFLIGHT_BUILT_NO_ENDPOINTS_ALLOWED

galaxies audited:
    6

control replay allowed:
    2

endpoint scores allowed:
    0

strongest current route:
    UGC12506 caveated interval/control replay
    NGC4088 Xi_eff control manifest route

main blocker:
    no endpoint-permitted Xi_eff route with additive-kernel / clock-layer
    double-count separation resolved
```

The preflight splits the time channel into two operational manifests:

```text
source-morphology time manifest:
    data/derived/time_projection_source_morphology_time_manifest.csv

observer/projection time manifest:
    data/derived/time_projection_observer_projection_time_manifest.csv

endpoint preflight:
    data/derived/time_projection_endpoint_preflight_gate.csv

report:
    reports/time_projection_endpoint_preflight_gate.md
```

Current consequence: the next legitimate endpoint calculation cannot be a
single fitted `Xi_t` score. It must first produce an accepted `Xi_eff` manifest
where the source-morphology clock channel and the observer/projection clock
channel are frozen separately. UGC12506 can continue as a caveated control
replay. NGC4088 has now passed the `q_warp`, `m_history`, independent review,
and `B_i` coefficient protocol gates, but remains endpoint-blocked until the
clock/readout contribution is separated from the already active additive
warp-history morphology kernel.

NGC4088 time-projection update:

```text
q_warp:
    accepted for protocol numeric bound
    q_warp = 1.0

m_history:
    accepted for protocol numeric bound
    m_history = 1.0

B_i coefficient rule:
    residual-blind sharpened protocol coefficients ready
    B_i = 0.5 under second-order remainder bound

Xi_eff candidate:
    raw source load L = 1.375
    epsilon_clock = 0.020263...
    Xi_eff(R) = 1 + epsilon_clock K_t(R)

status:
    NGC4088_XI_EFF_CONTROL_READY_ENDPOINT_BLOCKED

blocking gate:
    double-count separation
```

Control replay result:

```text
base projection RMSE:
    11.619

additive warp/history RMSE:
    9.391

clock-only Xi_eff on base RMSE:
    10.496

additive + Xi_eff stress RMSE:
    8.384

interpretation:
    ADDITIVE_PLUS_CLOCK_IMPROVES_BUT_DOUBLE_COUNT_BLOCKED
```

Bridge consequence: this is a meaningful endpoint-step, not an accepted
endpoint. The clock-only layer improves the base projection curve, while the
additive-plus-clock stress curve improves further. But the latter cannot be
claimed as the endpoint route until the clock/readout contribution is separated
from the already active additive warp-history morphology kernel. This is exactly
the discipline expected if time projection is a real channel rather than a
universal amplitude rescue term.

Artifacts:

```text
manifest:
    data/derived/ngc4088_time_projection_xi_eff_manifest_gate.csv

ablation replay:
    data/derived/ngc4088_time_projection_ablation_control_summary.csv

figure:
    figures/endpoint_diagnostics/ngc4088_time_projection_ablation_control_replay.png
```

Double-count resolution:

```text
status:
    NGC4088_DOUBLE_COUNT_RESOLVED_ACCEPTED_COMBINED_XI_ONE

source-space audit:
    f_PA  overlaps additive C_warp geometry
    f_R   overlaps additive x_w radial-onset support
    f_q   overlaps additive q_warp source-strength factor
    f_mem overlaps additive sigma_warp history phase

result:
    all four current Xi_eff terms overlap the already active additive
    warp-history morphology route.

accepted combined endpoint route:
    additive_warp_history_with_Xi_eff_equal_one

preserved control:
    clock-only Xi_eff replay on the base projection kernel

rejected endpoint route:
    additive_warp_history + Xi_eff clock multiplier
```

Bridge consequence: the double-count blocker is resolved, but not by opening a
new time-projection endpoint.  The clean combined endpoint uses the accepted
additive warp/history morphology kernel with `Xi_eff=1`.  The clock-only replay
remains useful as a control signal, while a true time-projection endpoint can be
reopened only if independent non-overlapping clock/readout evidence is supplied.

Artifacts:

```text
summary:
    data/derived/ngc4088_time_projection_double_count_resolution_summary.csv

overlap audit:
    data/derived/ngc4088_time_projection_double_count_overlap_audit.csv

report:
    reports/ngc4088_time_projection_double_count_resolution_gate.md
```

Accepted combined-route handoff:

```text
status:
    NGC4088_ACCEPTED_COMBINED_ROUTE_HANDOFF_READY

accepted combined route:
    additive_warp_history_endpoint_with_Xi_eff_equal_one

accepted combined RMSE:
    11.619 km/s

clock-only control RMSE:
    10.496 km/s

additive-plus-clock stress RMSE:
    8.384 km/s

endpoint policy:
    stress_test_endpoint_allowed = False
    time_endpoint_reopened = False
    requires_new_nonoverlap_clock_evidence = True
```

Bridge consequence: the endpoint-relevant NGC4088 route is now unambiguous.
The accepted combined route is exactly the caveated accepted additive
warp/history endpoint, interpreted with `Xi_eff=1`.  The lower RMSE
additive-plus-clock stress curve remains scientifically useful as a diagnostic
that the clock/readout channel can move the curve, but it is explicitly not an
endpoint route because it reuses the same warp/onset/strength/history evidence.

Artifacts:

```text
summary:
    data/derived/ngc4088_time_projection_accepted_combined_route_handoff_summary.csv

routes:
    data/derived/ngc4088_time_projection_accepted_combined_route_handoff_routes.csv

report:
    reports/ngc4088_time_projection_accepted_combined_route_handoff.md
```

UGC12506 external-review handoff:

```text
status:
    U12506_XI_T_EXTERNAL_REVIEW_HANDOFF_READY

contains:
    reviewer prompt
    fillable response CSV
    six source-review tasks
    five allowed route-level responses
    forbidden-input guardrails
    input hash ledger

response form:
    data/derived/ugc12506_xi_t_source_review_response_blank.csv

prompt:
    reports/ugc12506_xi_t_external_review_prompt.md

intake script:
    scripts/run_ugc12506_xi_t_source_review_response_intake.py

portable bundle:
    review_bundles/ugc12506_xi_t_external_review_bundle.zip

bundle builder:
    scripts/build_ugc12506_xi_t_external_review_bundle.py
```

Bridge consequence: the next UGC12506 step no longer requires interpreting a
conversation log. A residual-blind reviewer can fill the response form, after
which the intake validator decides whether the route can feed the
accepted-manifest gate.

The portable bundle is still not an accepted manifest and not an endpoint. It
only packages the review prompt, usage note, fillable response form,
source-review packet, source evidence, forbidden-input ledger, and relative-path
hash manifest so that the review can be performed outside the working thread.

## Main Clarification

Observed 4D morphology handles are not fundamental Tau-side classes. Thin disk,
thick disk, bar, ring, compact, tail, scale-tail, and lopsided labels are
projected 4D morphology handles unless an additional Tau-side or source-review
argument promotes them to readout-relevant proxies.

Therefore the formula-selection rule is:

```text
F = F_{K_readout}
```

not automatically:

```text
F = F_{K_obs}
```

This prevents a present-day visual exponential disk from being silently treated
as a clean exponential-disk readout when the source evidence points to
projection, bar, compact-core, outer-disk, or morphology-trajectory caveats.

Bridge consequence for residuals: a Tau Core residual is not required to be
locally sourced only by the four-dimensional baryonic mass density at the same
radius. It may descend through multiple readout/projection channels of the
deeper Tau morphology state, including baryonic distribution, metric/closure
response, observer/path projection, envelope/history/phase structure, or other
admissible source-frozen channels. This is not an arbitrary nonlocal-force
license. Each channel must have residual-blind source support, a non-overlap
ledger assignment, and an ablation check before it can affect endpoint scoring.

## Morphology Trajectory / Phase Layer

The bridge also permits a morphology-trajectory or phase proxy layer. A
galaxy's current observed 4D shape may be an incomplete proxy for the
readout-relevant morphology if the solved readout encodes delayed, integrated,
projection-filtered, or future-directed relaxation structure.

This layer is only a hypothesis layer until populated by residual-blind source
evidence. Rotation-curve-inferred readout families may motivate review, but
they cannot define accepted morphology labels or endpoint families.

Forbidden inputs for `K_readout` include:

```text
endpoint residual gain
required-S_tau diagnostic
best-fit Tau Core readout family
MOND/RAR/TGP comparison score
post-hoc family switching
per-galaxy residual tuning
```

## P0 Example

The current P0 source-reviewed rows all have the apparent 4D handle
`K_exponential_disk`, but the bridge layer separates them into different
readout-relevant proxy rows:

| Galaxy | K_obs | K_readout proxy |
| --- | --- | --- |
| NGC0100 | K_exponential_disk | K_projection_corrected_expdisk |
| NGC0247 | K_exponential_disk | K_barred_expdisk_m2_overlay |
| NGC0300 | K_exponential_disk | K_clean_exponential_disk_control |
| NGC6503 | K_exponential_disk | K_expdisk_compact_core_overlay |

This is not an endpoint label and not an empirical Tau Core validation. It is a
bridge-consistent source-review distinction.

## Consequences For Paper 8

The plain `K_exponential_disk` P0 pilot is a weak or control-style test unless
the row is a clean exponential-disk control. For caveated rows, the correct
next test is the predeclared `K_readout` shell or overlay family, not the raw
observed 4D handle.

The central endpoint remains claim-bounded:

```text
Does the predeclared morphology/readout family rank better than wrong families
and shuffled labels, while remaining competitive against Newtonian, MOND/RAR,
and TGP-like baselines?
```

The bridge does not yet claim that these readout proxies are final Tau-side
classes, that Tau Core is empirically validated, or that MOND/RAR/TGP
comparators have been superseded.

## Baseline Success As Readout-Regime Control

The bridge also records the complementary control reading: if a conventional or
historical baseline already fits a galaxy well, that success may itself mark a
Tau Core readout regime.

```text
Newtonian good fit
    -> quiet / regular baryonic-readout regime.

MOND or RAR good fit
    -> scalarized radial low-acceleration or diffuse-disk regime.

TPG good fit
    -> smooth closure-like or memory-integrated readout regime.

Tau matched-family good fit
    -> current morphology proxy may be close to K_readout.
```

This matters because Paper 8 should not claim that Tau Core must beat every
baseline everywhere. A stronger claim-safe endpoint is that baseline success
zones and Tau-family success zones map to distinct predeclared
morphology/readout regimes. Baseline winners may therefore become controls,
especially for galaxies whose present-day 4D morphology is regular, scalarized,
or historically/memory integrated.

## Baselines As Conditional Tau Core Limits

The bridge therefore treats Newtonian, MOND/RAR, TPG, and RMOND-facing behavior
as possible conditional readout limits. This is not a proof that the full
historical theories have been derived. It is a proof obligation: if the stated
conditions hold, the corresponding effective readout should arise naturally
from the Tau Core architecture.

```text
Newtonian limit
    conditions:
        quiet/current-regular K_readout,
        small alpha_tau,
        quotient-visible morphology residual suppressed,
        stable baryonic weak-field closure
    expected effective readout:
        g_eff -> g_Newt

MOND/RAR-like scalarized limit
    conditions:
        radial low-acceleration response,
        morphology dependence weak or averaged,
        Tau-side closure/readout supplies the crossover scale
    expected effective readout:
        MOND/RAR-like radial solved response as a special subcase

TPG-like closure limit
    conditions:
        smooth closure/readout defect,
        memory-integrated or projection-integrated residual,
        outer log-like / near-flat-speed solved branch
    expected effective readout:
        classical TPG-like formula as a solved closure branch

RMOND-facing metric limit
    conditions:
        quotient residual descends through a gauge-safe,
        metric-compatible weak-field readout map
    expected effective readout:
        relativistic/metric audit candidate, not yet RMOND recovered
```

Minimal corrected claim:

```text
Tau Core does not need to reject Newtonian/MOND/RAR/TPG successes.
It must show that their success zones correspond to predeclared Tau-side
readout regimes, and that each baseline appears as the effective 4D readout
when its regime conditions hold.
```

## Formula Status Imported From The Theory Bridge

The Paper 8 bridge uses the following formula-status ladder. This keeps
baseline-limit interpretation separate from empirical validation.

```text
Newtonian limit
    status:
        FORMULA-DERIVED
    bridge content:
        suppressed quotient-visible morphology residual gives
        delta_g_morph -> 0 and g_eff -> g_Newt.

TPG-like shape
    status:
        FORMULA-DERIVED under the n=2 source-tail gate
    bridge content:
        sigma_morph ~ A/r^2
            -> delta_g ~ A/r
            -> delta Phi ~ A log r.

Fixed historical TPG branch
    status:
        FORMULA-CONDITIONAL
    bridge content:
        the log-like solved-response shape is derived, but finite-load
        constants, branch selection, and historical normalization still need
        additional Tau-side closure/readout input.

MOND/RAR-like scaling
    status:
        FORMULA-CONDITIONAL
    bridge content:
        A^2 = G M_b g_* gives delta_g = sqrt(g_N g_*), but this is a Tau Core
        derivation only if g_* is supplied internally rather than imported as
        empirical a0.

RMOND-facing branch
    status:
        READOUT-FORM-ONLY
    bridge content:
        weak-field metric/readout compatibility can be audited, but no
        covariant relativistic field equation, conservation law, or lensing
        sector is derived here.
```

The internal acceleration-scale construction used by the amplitude gate is:

```text
g_* := lambda_* ell_*
[lambda_*] = T^-2
[ell_*] = L
```

`lambda_*` must be a residual-blind Tau-side closure/readout stiffness, and
`ell_*` must be an admissible readout length. This establishes an internal
acceleration-scale object by dimensional construction. It does not establish a
numerical a0 value, a universal MOND scale, or baseline superiority.

## Conditional Baseline-Selection Theorem

Let `R_g` be a residual-blind readout-regime label assigned to a galaxy before
rotation endpoint scoring.

```text
If R_g = quiet baryonic-readout regime:
    suppressed morphology residual
        -> delta_g_morph -> 0
        -> Newtonian branch.

If R_g = scalarized radial low-acceleration regime:
    morphology dependence weak or averaged
    plus internal g_* = lambda_* ell_*
        -> delta_g = sqrt(g_N g_*)
        -> MOND/RAR-like solved-response branch.

If R_g = smooth closure/readout source-tail regime:
    n=2 tail sigma_morph ~ A/r^2
        -> delta_g ~ A/r
        -> delta Phi ~ A log r
        -> TPG-like logarithmic / near-flat-speed branch.

If R_g = gauge-safe metric-readout descent regime:
    quotient residual descends through metric-compatible weak-field readout
        -> RMOND-facing branch, readout-form-only.
```

Proof status:

```text
The theorem is FORMULA-CONDITIONAL as a baseline-selection statement.
For each row, the effective branch follows by substituting the row's
predeclared assumptions into the formula-status ladder above.
```

Claim boundary:

```text
The bridge explains why a baseline should be good only if the corresponding
readout-regime label was fixed before endpoint scoring. If multiple predicates
hold, the galaxy is an overlap/control case rather than a unique baseline
selection proof. If no predicate holds, the current bridge has not explained
that baseline success.
```

## Morphology Information Gain Test

The bridge should not try to fit a complete high-dimensional morphology model
for every galaxy from incomplete data. The more falsifiable Paper 8 direction
is a residual-blind information-gain test:

```text
If Tau Core morphology/readout structure is the right explanatory direction,
then improving the morphology/readout information should improve the forward
readout prediction in predeclared metrics.
```

Information levels:

```text
L0 coarse K_obs:
    projected 4D morphology handle only.

L1 source-reviewed K_readout:
    residual-blind promotion/caveat layer.

L2 readout-state vector:
    q_tail, q_compact, q_thick, q_bar, q_phase, q_regular.

L3 source-native scales and normalization:
    disk scale, tail/HI radius, core radius, flare support, bar length,
    internal closure/readout normalization.

L4 enriched morphology/kinematic evidence:
    velocity fields, HI maps, decompositions, history indicators.
```

Pass condition:

```text
Moving from lower to higher residual-blind information levels improves one or
more predeclared endpoints:
    matched-vs-wrong rank,
    shuffled-label separation,
    residual RMS,
    baseline competitiveness,
    or readout-regime classification.
```

Fail condition:

```text
Extra morphology/readout information does not improve prediction, or improves
only when endpoint residuals are used to choose labels, weights, scales, or
gates.
```

This reframes the 0.886 matched-vs-wrong preflight result. It is evidence of
family specificity at an idealized formula-shell level, not a final fit claim.
The next question is whether progressively better residual-blind morphology
information turns that specificity into better predictive rotation endpoints.

Executable preflight:

```bash
python scripts/run_morphology_information_gain_test.py
```

Current local data status:

```text
SPARC rows: 175 acquired.
S4G scale-radius candidates: 75 acquired.
DustPedia full-sample source-candidate matches: 31.
HI full-sample SPARC-ready galaxies: 171.
PHANGS full-sample public-sample matches: 2.
MUSE-ready velocity-field candidates: 0.
L2 tail source candidates: 172.
L2 compact source candidates: 48.
L2 bar source candidates: 19.
Accepted readout-state vector components: 0 endpoint-ready.
```

Current holdout verdict:

```text
L0 -> L1:
    family specificity improves, raw RMSE does not.

L1 -> L2:
    mixture/readout-state proxy remains mixed or negative.

L2 -> L3:
    train-selected normalization improves the proxy mixture layer.
```

This is not a monotonicity proof. It is an executable failure map showing that
the next data task is accepted source-native morphology-memory, HI/tail,
compact/core, thickness/flare, and normalization evidence.

All-sample source expansion:

```bash
python scripts/build_morphology_information_gain_source_expansion.py
```

This acquisition layer is residual-blind and upstream of endpoint scoring.
It records source candidates only; it does not promote accepted labels or
accepted L2 mixture weights.

L2 weight-intake candidate layer:

```bash
python scripts/build_l2_weight_intake_candidates.py
```

This layer converts the source-expansion fields into residual-blind candidate
weights over the current four executable readout components.
It is not an accepted Tau-side readout-state vector and it does not score rotation curves.

Current full-sample status:

```text
Source-informative L2 weight candidates: 174/175.
Uninformative equal fallbacks:          1/175.
Tail nonzero candidates:                172.
Exponential-disk nonzero candidates:    75.
Compact nonzero candidates:             48.
Thick/flared nonzero candidates:        107.
```

Bridge interpretation: these weights are an intake map from projected 4D
morphology handles toward a readout-state vector. They are useful exactly
because they can disagree with the coarse `K_obs` family label without using
endpoint residuals. They still require freeze-and-audit before endpoint use.

Endpoint preflight for the intake map:

```bash
python scripts/run_l2_weight_intake_endpoint_preflight.py
```

Current holdout status:

```text
Beats old L2 mixture proxy:       0.409.
Beats hard source-native family:  0.409.
Beats TPG/v6:                    0.477.
Beats MOND:                      0.432.
Median intake-minus-old-L2 RMSE: +0.847.
```

Bridge interpretation: this is a preserved negative/mixed result, not a Tau
Core validation failure. The current source-intake weights are closer to a
readout-state vector than the old `K_obs` handle, but they are still too raw to
improve the endpoint globally. The positive hint is channel-local: the
dominant `K_thick_flared` intake subgroup improves relative to the old L2 proxy
on median, while compact and several tail/exponential cases remain weak. The
next bridge task is therefore source-native weight freeze/audit, not another
endpoint-selected mixture.

Freeze-readiness audit:

```bash
python scripts/build_source_native_orientation_promotion_gate.py
python scripts/build_memory_projection_acceptance_gate.py
python scripts/build_inclusion_lane_expansion_audit.py
python scripts/run_inclusion_lane_endpoint_analysis.py
python scripts/audit_l2_weight_freeze_readiness.py
```

Current full-sample status:

```text
Endpoint-freeze allowed:                  0/175.
Proxy-gate blocker resolved by E_tau:     175/175.
Blocked by missing Tau-side normalization: 0/175.
Family orientations promoted:             3/4.
Family orientations blocked:              1/4.
Galaxies orientation-ready:               67/175.
Blocked by source-native orientation:     108/175.
Blocked by projection acceptance:         47/175.
Blocked by memory/history acceptance:     19/175.
Blocked by q_i/normalization acceptance:  1/175.
Formula-conditional normalization present: 175/175.
Strict-ready candidates:                  1/175.
Caution/proxy-supported rows:             66/175.
Analysis-includable strict+caution rows:  67/175.
Acquisition-required rows:                108/175.
Holdout strict+caution rows:              16/44.
Hard-family beats wrong on strict+caution: 0.8125.
Hard-family beats TPG/v6 on strict+caution: 0.5000.
Hard-family beats MOND on strict+caution:  0.4375.
Tau evidence L2 beats TPG/v6 there:        0.3750.
Tau evidence L2 beats MOND there:          0.3125.
Projection-caveat sub-lane rows:           14/44.
Hard-family beats wrong there:             0.7857.
Tau evidence L2 beats TPG/v6 there:        0.3571.
Tau evidence L2 beats MOND there:          0.2857.
Dominant source-candidate support:        141/175.
Dominant proxy/partial only:              31/175.
Dominant missing source support:          3/175.
```

Bridge interpretation: the source layer is informative, but it is not yet an
accepted Tau-side readout-state vector. The missing object is not another
per-galaxy endpoint fit. The source-native orientation gate promotes compact,
scale-tail, and exponential orientations, but blocks thick/flared until a
velocity-field/vertical source layer exists. The 67 rows that pass orientation
then split into projection-blocked, memory/history-blocked, and one
memory/projection-ready candidate. That last candidate is still not an endpoint
launch, because accepted per-galaxy q_i assignments and an accepted
normalization law are not yet in place. Until those gates are accepted, the L2
weights remain candidates and the endpoint launch stays blocked.

Inclusion-lane interpretation: the strict accepted lane remains tiny, but the
bridge should not throw away the 66 additional orientation-ready rows. They
belong in a caution/support lane, not an endpoint-validation lane. This gives a
larger analysis-includable set for sensitivity and acquisition planning while
keeping the final empirical claim restricted to strict accepted lanes. The
first lane-scored analysis is mixed: morphology-specific matched-vs-wrong
structure survives in the strict+caution holdout subset, but baseline
superiority does not. This is a data-acquisition diagnostic, not validation.
The allowed-use split sharpens the repair path: the projection-caveat sub-lane
still carries morphology-family specificity, while the Tau evidence L2
normalization is weak against baselines. The immediate repair target is
therefore projection/scale quality plus source-normalization, not another
endpoint-selected morphology family.

Projection/scale repair and source-normalization failure-mode audits:

```bash
python scripts/build_projection_scale_repair_audit.py
python scripts/audit_source_normalization_failure_modes_by_lane.py
```

Current repair map:

```text
No projection/scale repair required:                         71/175.
Needs vertical-geometry source evidence:                     34/175.
Needs inclination/projection review:                         26/175.
Needs distance/scale source support:                         30/175.
Repairable with existing scale source plus distance audit:   14/175.
Holdout projection-caveat rows with projection-scale
normalization failure:                                        7/14.
```

Bridge interpretation: the weak baseline comparison is now more localized. In
the projection-caveat holdout sub-lane, seven of fourteen rows preserve
hard-family morphology specificity but fail to transfer that specificity into a
baseline-competitive Tau evidence L2 solved response. This is not a new
endpoint gate and not validation. It is a residual-blind repair map: improve
projection/scale sources, vertical-geometry evidence, distance-scale review,
and the source-normalization rule before claiming baseline superiority.

S4G75 source-rich lane:

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

Current source-rich holdout reading:

```text
S4G scale-source rows:                    75.
Holdout S4G scale-source rows:            21.
Hard-family beats wrong there:            0.9524.
Hard-family beats TPG/v6 there:           0.5238.
Hard-family beats MOND there:             0.5714.
Tau L2 beats old L2 intake there:         0.6190.
Tau L2 beats TPG/v6 there:                0.3810.
Tau L2 beats MOND there:                  0.6190.
```

Bridge interpretation: this is the current best development lane, not the
final accepted endpoint lane. It shows that adding source-native disk-scale
information strongly preserves morphology-family specificity, while baseline
competitiveness still depends on projection/scale, vertical-geometry, and
source-normalization repair. The full 175-row sample remains a stress and
acquisition lane; the 75-row S4G lane should be repaired first before making a
larger accepted-claim sample.

The holdout repair packet currently turns this into 15 galaxy-level review
targets and 71 residual-blind review fields. The shared blocker is no longer
absence of S4G/SPARC scale evidence; it is external family-label audit plus
missing family-specific kernel observables. Compact rows need compact-support
radius, scale-tail rows need tail inner/cutoff support, and thick/flared rows
need source-native vertical geometry (`thickness_h_over_rs`, flare, warp, or
gas-plane evidence). This is the next bridge repair gate before rerunning a
cleaner S4G75 endpoint stress test.

The kernel-observable fill gives the first concrete values for those fields.
All 15 repair rows retain source-derived S4G/SPARC scale radii. Seven
scale-tail rows receive source-constrained tail inner/cutoff candidates from
SPARC HI extent plus the predeclared disk-to-HI transition rule. The compact
row receives a compact-support candidate from SPARC effective radius because no
direct S4G bulge radius is present. Seven thick/flared rows receive h/Rs
candidates from inclination plus HI extent, and NGC5907 receives an edge-disk
candidate from its S4G `Z:edgedisk` component. These are concrete readout
inputs, but not yet accepted observables. Their status remains
`SOURCE_CONSTRAINED_FORMULA_CANDIDATE` or
`SOURCE_CONSTRAINED_EDGE_DISK_CANDIDATE` until direct source-native
measurements or a stronger Tau-side promotion rule is supplied.

The filled-kernel stress test is therefore an important negative control. It
keeps holdout matched-vs-wrong specificity at 0.9524, leaves MOND comparison at
0.5714, but lowers TPG/v6 comparison from 0.5238 to 0.4286. The bridge reading
is not that morphology failed; the family-specific signal stayed strong. The
reading is that source-constrained formula-candidate kernel filling is still
too weak to replace direct source-native observables and a better
normalization/projection descent. This blocks any baseline-superiority claim
and points the next gate toward direct kernel-observable acquisition or a
stronger Tau-side promotion rule.

The filled-kernel delta-driver audit sharpens this gate. It splits the filled
stress-test delta by morphology family and observable type. The current
diagnostic assigns three scale-tail rows and six thick/flared rows to
`P0_DIRECT_SOURCE_NATIVE_REQUIRED`. These rows need direct outer-disk/HI
transition observables or direct vertical-geometry observables before they can
support a stronger endpoint. The same audit assigns one compact row, three
scale-tail rows, and two thick/flared rows to
`P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE`, where the filled candidates helped but
still require source-native confirmation or a stronger bridge promotion rule.

Bridge consequence: the weak filled-kernel baseline transfer is not evidence
against the morphology-specific readout idea. It is evidence that several
filled observables are still only 4D proxy or formula-conditional
representatives. The next bridge step is direct kernel-observable acquisition
or Tau-side promotion of those representatives, not endpoint-selected
refitting.

The direct source-native acquisition manifest converts that bridge consequence
into a residual-blind source queue. The current queue has fifteen S4G75
holdout tasks: nine `P0_DIRECT_SOURCE_NATIVE_REQUIRED` tasks and six
`P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE` tasks. P0 rows are the ones where
formula-conditional filled observables worsened baseline transfer; P1 rows are
the ones where they helped but still need source-native confirmation or a
stronger Tau-side promotion rule. The required evidence families are S4G,
NED/NED-D, DustPedia, HI survey support, and PHANGS where applicable. The
manifest is not an accepted morphology manifest and cannot by itself change an
endpoint result.

The source-native availability audit then separates generic source coverage
from direct kernel-observable readiness. In the current local cache, all fifteen
queue rows have S4G support and fourteen have SPARC HI radius support, but only
three have direct DustPedia matches and none are in the local PHANGS public
sample. More importantly, the kernel-specific gap remains: scale-tail rows have
HI extent support but still need an outer-disk transition profile, break
radius, truncation radius, or source-native tail cutoff; the compact row has
component support but still needs a compact-support radius; most thick/flared
rows still lack direct vertical scale height, flare, warp, or gas-plane
thickness evidence. NGC5907 is the current partial exception because its S4G
edge-disk component supports a vertical-geometry candidate.

The direct kernel measurement extraction reads the stable direct-source
acquisition manifest rather than the current conditional-promotion list. This
is important because a successful direct promotion must remain present under
repeated reproduction runs instead of disappearing from the input queue. The
extraction tightens two rows using S4G Table 7. NGC5985 receives a direct
compact support candidate from S4G Sersic bulge `Re = 0.735239 kpc`. NGC5907
receives a direct vertical kernel ratio from S4G edge-disk `hz2/hr2 =
0.173321`. Scale-tail rows remain conditional because S4G Table 7 does not
provide their outer-disk/HI transition profile.

Bridge consequence: source-rich is not the same as kernel-ready. The Paper 8
bridge should not promote a filled kernel observable merely because the galaxy
has S4G or SPARC coverage. Promotion requires the source to constrain the
readout kernel actually used by the morphology family.

The kernel-ready promotion gate applies this rule conservatively. After direct
S4G Table 7 extraction, the current S4G75 repair lane has two strict
kernel-ready rows, six conditional kernel rows, and seven proxy-only rows. The
strict subset is therefore runnable only as a tiny stress diagnostic, not as an
accepted endpoint. This is not a failure of the morphology-specific readout
hypothesis; it is a claim-boundary result saying that most current kernel
observables are not yet promoted enough for an accepted endpoint.

The conditional promotion requirements make that theorem work explicit. The
six remaining conditional rows reduce to one active family-level gate:

```text
TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION
    RHI or HI extent may promote a scale-tail kernel only if it constrains the
    same outer-disk transition, break, truncation, or tail-support radius used
    by the readout formula.
```

The compact and edge-disk gates remain general bridge gates for future rows,
but their current S4G75 waiting rows have direct S4G Table 7 measurements:

```text
COMPACT-COMPONENT-SUPPORT-PROMOTION
    Reff or component presence may promote a compact finite-source kernel only
    if it constrains the compact component support radius.

EDGE-DISK-TO-VERTICAL-KERNEL-PROMOTION
    an S4G edge-disk component may promote thick/flared only if it constrains
    vertical scale height, h/Rs, flare, warp, or gas-plane thickness.
```

Each gate has two admissible routes: direct source-native measurement, or a
residual-blind Tau-side promotion theorem. Endpoint improvement, best-fit
family choice, or post-hoc residual shape cannot satisfy these gates.

The tail RHI promotion attempt is now recorded as a separate theorem-conditional
audit. All six remaining scale-tail rows have enough local SPARC `RHI` support
to be treated as conservative upper-cutoff candidates, with external context
from Wang et al. 2014 on homogeneous outer HI profiles. This is deliberately
not strict kernel readiness: RHI is an extent, not yet the same object as the
outer transition, break, truncation, or tail-support radius required by the
readout kernel. The missing step is still the residual-blind Tau-side theorem
that proves when RHI bounds the relevant tail kernel.

The remaining kernel acquisition ledger turns the non-strict rows into the next
source/theorem work queue. It preserves two lanes:

```text
SCALE_TAIL_TRANSITION_MISSING:
    6 rows.
    Direct route: resolved HI radial profile, optical/IR outer-disk break,
    truncation, or source-native tail transition.
    Theorem route: RHI conservative upper-cutoff theorem.

VERTICAL_KERNEL_MISSING:
    7 rows.
    Direct route: vertical scale height, h/Rs, flare, warp, or gas-plane
    thickness.
    Theorem route: edge-disk/inclination-to-vertical-kernel theorem.
```

This ledger is now the bridge's most concrete answer to “what data are still
missing?” It does not score endpoints and it does not promote labels. It only
states the admissible source-native route by which a current proxy row could
become kernel-ready.

The first targeted literature-source hit pass adds one important bridge-facing
result. NGC2683 has a direct HI flare-profile source: Vollmer, Nehlig & Ibata
2016 model the gas disk with an exponential flare that rises from `H = 0.5 kpc`
at `R = 9 kpc` to `H = 4 kpc` at `R = 15 kpc`, stays saturated to `R = 22 kpc`,
and includes an outer ring vertical offset of `1.3 kpc`. This is not yet a
scalar `h/Rs` endpoint override, because the current executable thick/flared
shell still uses a simplified scalar thickness proxy. Bridge consequence: the
next vertical-kernel proof/software task is a residual-blind
flare-profile-to-readout-kernel mapping.

For the scale-tail rows, the literature hit pass records source candidates
rather than promotions. NGC4214 has HI/warp context from Lelli, Verheijen &
Fraternali 2014. UGC06917 and UGC06983 have Verheijen & Sancisi 2001 HI atlas
profile candidates. UGC00891, UGC04499, and UGC05829 have van Zee/Swaters
source-family candidates. None of these rows has a machine-extracted
outer-transition radius yet, so they remain profile-extraction or
theorem-conditional tasks.

The NGC2683 flare-profile mapping gate then demonstrates why a more realistic
Tau Core morphology readout cannot simply be a scalar proxy substitution. The
gate maps the source-native flare profile onto the observed radii and finds
seven mapped points and four post-22 kpc points where the source states that
the flare decreases but does not provide a unique executable decrease law. The
old scalar `h/Rs` proxy is `0.202408`, while the mapped source profile spans
`h/Rs = 0.226281 ... 1.810245` with median `0.545702` on the mapped points.
Bridge consequence: NGC2683 is now a concrete profile-aware vertical-kernel
development target, not an accepted endpoint row.

The profile-aware preflight then tests the simplest possible insertion: replace
the scalar thickness by the mapped local profile where the source is defined.
This intentionally weak policy barely changes the score and slightly worsens
it (`+0.000069` RMSE on the mapped-only diagnostic; `+0.000038` on the hybrid
diagnostic). The important signal is structural rather than performance-based:
three mapped points exceed the current executable shell's `h/Rs <= 0.75` clip.
The bridge conclusion is therefore that NGC2683 needs a genuine radial
`H(R)`-aware thick/flared readout kernel, not a pointwise scalar substitution.
The unclipped variant strengthens this: removing the clip worsens the mapped
diagnostic by `+0.004542` RMSE and the hybrid diagnostic by `+0.002546`. Thus
the blocker is not just clipping, but the local-scalar damping form itself.

The first nonlocal `H(R)`-aware prototype preserves the same failure-map. Using
a source-weighted local average of the flare profile with locality width fixed
to the S4G/SPARC disk scale gives `+0.003803` RMSE for the post-22 kpc plateau
policy and `+0.003029` RMSE for the post-22 kpc taper policy. Bridge
consequence: merely injecting `H(R)` into the old damping family is not enough.
The vertical/readout operator itself must change, likely treating flare/warp as
a distinct closure source rather than only a damping factor on an
exponential-disk shell.

The first flare closure-source prototype supports that operator-level move. It
uses the positive radial gradient of `log H(R)` as a separate closure source,
with an optional localized outer-ring offset term. Under the same non-endpoint
amplitude policy, the NGC2683 stress score improves from the scalar
`10.331859` RMSE to `10.203145` for the gradient source and `10.178731` for the
gradient-plus-ring source. This is not validation and not an accepted endpoint,
but it is the first constructive bridge signal that source-native flare
morphology helps when represented as a closure source rather than as scalar
damping.

The closure-source sensitivity audit strengthens the formula-development
signal. Across twelve residual-blind prototype settings (four locality widths
times three ring strengths), all twelve improve over the scalar thick/flared
shell, with best delta `-0.353217` RMSE. This is still one-galaxy evidence and
not endpoint validation, but it identifies the next plausible bridge formula
family: profile-aware vertical closure sources.

The closure-source generalization gate then limits the claim. In the current
S4G75 thick/flared lane, only NGC2683 is
`PROFILE_CLOSURE_SOURCE_READY_PROTOTYPE_ONLY`. NGC3972 is an
`EDGE_ON_VERTICAL_PROFILE_SEARCH_REQUIRED` target, NGC4088 is a
`HIGH_INCLINATION_WARP_FLARE_SEARCH_REQUIRED` target, and NGC0024, NGC3726,
NGC3949, and NGC4389 remain `INSUFFICIENT_VERTICAL_PROFILE_SUPPORT`. No row is
authorized for closure-source endpoint scoring. Bridge consequence: the formula
family direction is now explicit, but population-level use needs more direct
profile sources or a predeclared source theorem.

The vertical source-search audit sharpens this into a reproducible data
acquisition statement. NGC2683 remains the only direct profile-source row.
NGC3972 has object-specific HI morphology support from O'Brien et al. 2016 and
WHISP/Ursa Major observing context from Verheijen & Sancisi 2001, but no
extracted vertical scale, flare profile, warp radius, or gas-plane thickness.
NGC4088 is now the strongest next target: Verheijen & Sancisi 2001 record a
strongly distorted disk, an asymmetric position-velocity diagram, and an
asymmetric warp; O'Brien et al. 2018 add object-specific HI kinematic asymmetry
context. Bridge consequence: NGC4088 can move from generic source search to a
warp/asymmetry profile-extraction lane, but it is still not a target-galaxy
readout kernel. General EPG/HI-flaring literature can motivate the
closure-source theorem lane, but it cannot fill a target-galaxy readout kernel
without residual-blind profile or bound extraction.

The NGC4088 warp/asymmetry extraction gate records the first concrete source
observables for that lane: inclination `69 deg`, position angle `231 deg`, HI
diameter `8.5 arcmin`, HI flux `102.9 Jy km/s`, and qualitative warp/PV/PA
asymmetry flags. The bridge blocker is now explicit rather than vague:
warp-onset radius, a radial `theta_warp(R)` or `PA(R)` profile, vertical height
`H(R)`, and a residual-blind closure-source mapping rule are still missing.
Bridge consequence: NGC4088 is a legitimate formula-development target, not an
endpoint-scoring row.

The NGC4088 pre-kernel normalization step then checks that the source-native HI
diameter is geometrically consistent with the SPARC `RHI` scale. At SPARC
distance `18 Mpc`, the WHISP diameter `8.5 arcmin` gives `R_HI = 22.253 kpc`,
matching SPARC `RHI = 22.25 kpc` to fractional difference `1.33e-4`. The
dimensionless pre-kernel scales are `R_HI/Rdisk = 8.63` and
`R_HI/Rs4g = 6.83`. Bridge consequence: NGC4088 now has a residual-blind
normalization layer for formula development, but it still lacks the radial
warp/asymmetry source profile needed for a true readout kernel.

The first NGC4088 warp/asymmetry mapping shell is now explicit. With
dimensionless radius `x := R/R_HI`, define

```text
C_warp(x; x_w, p) = q_warp * max(0, (x - x_w)/(1 - x_w))^p .
```

Here `q_warp` is the source-side warp/asymmetry strength and
`x_w := R_warp/R_HI` is the source-native onset control. This is a
Tau Core bridge object in the correct sense: it is morphology-indexed,
dimensionless, residual-blind, and closure-source shaped. It is not yet a 4D
readout endpoint because `x_w`, a radial `PA(R)` or `theta_warp(R)` profile,
and the readout normalization are still source-missing.

The NGC4088 onset extraction protocol freezes the admissible ways to supply
`x_w`. Accepted source classes are a radial `PA(R)` profile, a radial
warp-angle or tilted-ring profile, or a predeclared channel-map digitization of
the ridge/bend. A text-only warp statement is explicitly insufficient for
`x_w`; it supports only the development lane. Bridge consequence: the next
missing object is not vague data, but a specific residual-blind onset
measurement.

The digitization target manifest now identifies the concrete source page for
that measurement route. The N4088 channel-map panel is rendered from Verheijen
& Sancisi 2001 PDF page `76` into
`data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_76-076.png`.
The required digitization outputs are an inner disk axis, outer ridge axes by
side, onset radius in arcmin, side-combination rule, and uncertainty. Bridge
consequence: the source-acquisition task is now operational, but `x_w` is still
not extracted.

The channel-map digitization worksheet is the next operational layer. The page
76 ROI is split into panel-level measurement targets and a companion overlay:
`data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_76_channel_maps_roi_worksheet_overlay.png`.
The worksheet records 24 panel boxes, 23 measurement targets, and empty fields
for inner-axis, outer-ridge, onset-radius, uncertainty, and side label. Bridge
consequence: the source target has become a reproducible measurement worksheet,
but the measurement values are intentionally absent; `x_w` remains unavailable
until a residual-blind manual or frozen image-analysis protocol fills those
fields.

The frozen channel-map digitization protocol then separates measurement intake
from endpoint use. The current first-pass residual-blind response records an
inner-axis PA of `229 deg`, side outer axes `319 deg` and `229 deg`, side onset
radii `1.2 arcmin` and `1.6 arcmin`, the predeclared `MIN_SIDE` combination
rule, and uncertainty `0.3 arcmin`. The conversion audit maps this into
`x_w = R_warp/R_HI = 0.282353 +/- 0.070588`, with onset `6.283 kpc`. Bridge
consequence: NGC4088 now has a provisional source-side onset control for the
warp/asymmetry mapping rule, but this remains a digitization-derived
formula-development input. It still does not authorize endpoint scoring or a
matched-family validation claim.

The filled NGC4088 warp closure-source mapping uses that accepted `x_w` only to
populate the dimensionless ramp basis
`C_warp(x; x_w, p) = q_warp * max(0, (x - x_w)/(1 - x_w))^p` for powers `1`
and `2`. The profile rows are marked `FILLED_SOURCE_BASIS_NOT_ENDPOINT`.
Bridge consequence: the source onset blocker is discharged for the development
lane, while kernel-to-velocity normalization and the final 4D readout law remain
open.

The NGC4088 kernel-to-velocity normalization candidate is now the first
dimensionful bridge from the filled source basis to a `delta v^2` readout
scale. It uses a theory-conditional positive warp orientation, source-side
`q_warp = 1`, source-filled `c_warp = x_w = 0.282353`, and a catalog scale
carrier `Vflat^2 = 29480.89 km^2/s^2`, giving normalization prefactor
`8324.016 km^2/s^2`. The candidate remains
`THEORY_CONDITIONAL_FILLED_SOURCE_RULE`, not an endpoint law. Bridge
consequence: the dimensional carrier exists, but the physical normalization law
is still not proven or endpoint-authorized.

The NGC4088 readout preflight profile then evaluates this candidate on the
local SPARC/TPG point radii without fitting amplitudes and without using
observed velocities for generation. The exported p=1 and p=2 turn-on branches
have maximum preflight velocities `190.381 km/s` and `189.582 km/s`
respectively, with status `PREDECLARED_READOUT_EXPORT_NOT_ENDPOINT`. Bridge
consequence: there is now a concrete radial candidate profile for inspection,
but no baseline comparison, matched-family claim, or validation endpoint has
been computed.

The NGC4088 physical normalization-law gate now makes the open
`PHYSICAL_NORMALIZATION_LAW` blocker explicit. The candidate formula is
`delta_v2_warp(R;p) = sigma_warp q_warp x_w Vflat^2 C_warp(R/R_HI; x_w, p)`.
Five checks pass: dimensional consistency, prefactor reproduction, source-onset
suppression, positive warp orientation, and residual-blind export. One check is
only `FORMULA_CONDITIONAL`: the formula is executable and dimensionally
consistent. Three law-level checks remain blocked:
`TAU_SIDE_VARIATIONAL_OR_CLOSURE_DERIVATION`, `SCALE_UNIQUENESS`, and
`POPULATION_TRANSFER`. Bridge consequence: the normalizer is no longer vague,
but its status is `FORMULA_CONDITIONAL_PHYSICAL_LAW_BLOCKED`, not an accepted
Tau-side 4D readout law.

The NGC4088 scale-uniqueness audit explains why `SCALE_UNIQUENESS` remains
blocked. It enumerates five residual-blind, dimensionally valid scale carriers:
`x_w * Vflat^2 = 8324.016`, `x_w * median_r(v_n^2) = 6038.611`,
`x_w * median_r(v_v6^2) = 12316.148`,
`c_g * median_r(v_n^2) = 10509.153`, and
`x_w * c_g * median_r(v_n^2) = 2967.290`, all in `km^2/s^2`.
Bridge consequence: the current `x_w * Vflat^2` carrier is a valid selected
candidate, but not a unique Tau-side consequence. The gate status is
`BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES` until a Tau-side closure/readout
principle selects or rejects the alternatives without endpoint residual tuning.

The Tau-side scale-selection gate supplies a conditional version of that
principle. It requires residual blindness, source-onset coupling, an asymptotic
readout carrier rather than point-sampled median curve statistics, no external
TPG-like closure comparator as the normalizer, and a minimal single-source
factor unless Tau-side theory derives a composite. Under this
`MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE`, only `CURRENT_XW_VFLAT2` passes
all five criteria. Bridge consequence: the scale ambiguity is narrowed to
`THEORY_SELECTION_CONDITIONAL_CURRENT_ONLY`, but not closed; the selection rule
itself still needs a Tau-side closure/readout derivation before the law can be
promoted. Its law status is therefore
`SELECTION_RULE_CONDITIONAL_NOT_DERIVED_LAW`.

The follow-up Tau-side scale-derivation gate turns that status into a concrete
proof-obligation ledger. It records a conditional skeleton: if the
warp/asymmetry closure readout is local at the source onset, asymptotically
carried by the catalog flat-speed scale, autonomous from external closure
comparators, and minimal in source factors, then the dimensionful carrier
reduces to `x_w * Vflat^2`. This is explicitly
`DERIVATION_SKELETON_NOT_PROOF`. The gate reports
`DERIVATION_BLOCKED_SELECTION_RULE_AUDITED` and
`NOT_DERIVED_TAU_SIDE_LAW`: dimensional consistency passes;
source-onset locality, comparator autonomy, and minimal-source-factor status
remain formula-conditional; asymptotic carrier dominance, the Tau-side
closure/readout functional, and population transfer remain blocked.

The asymptotic-carrier dominance subgate then refines the first of those
blockers. `Vflat^2` passes catalog-availability and dimensional checks, and the
protocol rejects point-sampled median curve statistics and external TPG-like
comparators. But this is still only a source-catalog carrier candidate. The
subgate status is `ASYMPTOTIC_CARRIER_DOMINANCE_NOT_DERIVED`, with law status
`VFLAT2_SOURCE_CANDIDATE_NOT_TAU_SIDE_CARRIER_PROOF`, because no Tau-side
closure functional yet derives `Vflat^2` as the unique asymptotic readout
carrier and no population transfer has been performed.

The closure-functional requirement gate refines the next blocker. It specifies
the minimal functional shape needed for a genuine derivation:
`J_tau[lambda_w] = closure_cost + asymptotic_carrier_penalty + autonomy_penalty`,
with the desired solved scale
`lambda_w = sigma_warp q_warp x_w Vflat^2`. This is not yet constructed. The
status is `CLOSURE_FUNCTIONAL_REQUIREMENT_SPECIFIED_NOT_DERIVED`, with law
status `NO_TAU_SIDE_EULER_CLOSURE_DERIVATION_YET`, because no explicit
Tau-side closure cost or stationarity equation currently yields the selected
scale.

The minimal Euler-ansatz gate supplies the first explicit stationarity
calculation. Conditional on
`J_min(lambda_w)=1/2 kappa_lambda (lambda_w - sigma_warp q_warp x_w Vflat^2)^2`,
the Euler condition `dJ_min/dlambda_w=0` gives
`lambda_w = sigma_warp q_warp x_w Vflat^2 = 8324.016 km^2/s^2`. This is real
algebraic progress, but it is not a Tau-side law derivation: the status is
`EULER_CONDITION_SOLVED_GIVEN_TARGET_ANSATZ`, with law status
`TARGET_FUNCTIONAL_NOT_TAU_SIDE_DERIVED`, because the target term and closure
stiffness are not derived from Tau-side morphology/readout structure.

The target-functional origin gate decomposes that target term. The factors
`sigma_warp`, `q_warp`, `x_w`, and `Vflat^2` are available before endpoint
scoring, and their product has the correct `km^2/s^2` dimension:
`sigma_warp q_warp x_w Vflat^2 = 8324.016 km^2/s^2`. But the product coupling
and quadratic penalty are not derived. The status is
`SOURCE_FACTORS_AVAILABLE_COUPLING_NOT_DERIVED`, with law status
`TARGET_TERM_NOT_TAU_SIDE_DERIVED`.

The multiplicative-coupling separability gate upgrades the product term from a
bare ansatz to a conditional theorem. If the local warp/asymmetry readout
amplitude separates into orientation sign, source strength, onset-support
fraction, and asymptotic carrier, then
`lambda_w = sigma_warp q_warp x_w Vflat^2` follows. The status is
`CONDITIONAL_PRODUCT_DERIVED_IF_SEPARABLE`. The remaining law blocker is
`SEPARABILITY_AND_CROSS_TERM_SUPPRESSION_NOT_DERIVED`: Tau-side geometry still
has to derive factor separability and suppress mixed source-source terms.

The cross-term suppression gate makes that last caveat explicit. It promotes
the current product to a leading-order model
`lambda_w = lambda_0 * (1 + epsilon_cross)`, where
`lambda_0 = sigma_warp q_warp x_w Vflat^2`. The zero-cross limit recovers the
current formula, but the status is `CROSS_TERMS_DECLARED_NOT_SUPPRESSED`, with
law status `LEADING_PRODUCT_ONLY_UNTIL_EPSILON_CROSS_BOUND`. The mixed terms
include orientation-strength, onset-strength, onset-carrier, and
geometry/memory corrections; none is yet derived away or bounded from
residual-blind source observables.

The epsilon-cross source-bound protocol is the next forward step. It declares
a residual-blind bound form
`|epsilon_cross| <= B_PA f_PA + B_R f_R + B_q f_q + B_mem f_mem`. For NGC4088,
three first-pass source observables are already available: 90 degree
orientation mismatch, 0.4 arcmin side-onset asymmetry, and 0.25 onset
uncertainty fraction. The numeric bound remains blocked with status
`SOURCE_BOUND_PROTOCOL_PARTIAL_NUMERIC_BOUND_BLOCKED` and
`SYMBOLIC_UNBOUNDED_UNTIL_Q_AND_MEMORY_READY`, because quantitative
`q_warp`, a residual-blind memory/history proxy, and the bound coefficients
are not yet supplied.

The q_warp measurement protocol addresses the first missing input. It turns
the qualitative `q_warp=1` into a residual-blind channel-map measurement task:
`q_warp_measured = clipped_mean(outer_asymmetry_extent / local_disk_reference_extent)`.
The protocol has 23 panel measurement targets and five required fields, but its
response template is intentionally empty. Status:
`QWARP_PROTOCOL_READY_MEASUREMENT_BLOCKED`; after source measurement and
independent review it would unblock the q component of the `epsilon_cross`
bound.

The NGC4088 memory/history proxy protocol addresses the second missing source
input without using rotation residuals. It defines
`m_history_warp = weighted_source_score(warp_persistence, HI_lopsidedness, outer_disk_asymmetry, interaction_context)`
as a residual-blind source proxy for the `B_mem f_mem` term. The allowed lane is
WHISP/HI morphology, channel-map persistence, outer-disk asymmetry, and
residual-blind environment notes; the forbidden lane includes `vobs`, rotation
residuals, `rotation-inferred family`, and endpoint-selected models. The WHISP
source lane is available, but the response template is still empty. Bridge
consequence: the memory branch is
`MEMORY_PROTOCOL_READY_MEASUREMENT_BLOCKED`, with impact
`UNBLOCKS_MEMORY_COMPONENT_AFTER_MEASUREMENT_AND_REVIEW`.

The first-pass source-response fill now supplies provisional source values from
the already frozen channel-map digitization response: `q_warp_measured=1.0` and
`m_history_warp=1.0`. These are residual-blind, but they are not accepted
numeric-bound inputs because no independent source review exists and the
environment/context memory component is still incomplete. Bridge consequence:
`FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED`.

The independent source-response review then recomputes these source quantities
without endpoint residuals. The q response is accepted for the protocol numeric
bound. The previously missing H4 interaction/context component is now filled by
a residual-blind review of the NGC4088 source literature: the galaxy is described
as strongly distorted, with asymmetric PV/warp behavior and nearby
companion/context. The `m_history_warp` term is therefore accepted for this
protocol-bound layer as a morphology-carried source-history proxy, not as a
separate fundamental memory object. Bridge consequence:
`SOURCE_RESPONSES_ACCEPTED_FOR_PROTOCOL_BOUND`.

The B_i coefficient freeze rule then supplies a conservative residual-blind
protocol rule, `B_PA=B_R=B_q=B_mem=1`. This is a unit-Lipschitz/triangle-bound
default for a first protocol upper bound, not a final Tau-side sharp-amplitude
derivation and not an endpoint fit. Bridge consequence:
`BI_COEFFICIENTS_FROZEN_PROTOCOL_BOUND_READY`.

A sharper residual-blind coefficient rule is then added on top of that baseline:
`B_PA=B_R=B_q=B_mem=0.5`. This follows only under a declared second-order
Taylor-remainder interpretation with normalized source-space Hessian cap `<=1`.
It is formula-conditional, not a final Tau-side coefficient derivation. Bridge
consequence: `BI_COEFFICIENTS_SHARPENED_PROTOCOL_BOUND_READY`.

The epsilon-cross input review packet now consolidates these obligations into a
single pre-bound artifact. It lists the two residual-blind source measurements,
`q_warp_measured` and the source-reviewed morphological-history proxy
`m_history_warp`, plus the four active residual-blind coefficient-rule inputs
`B_PA`, `B_R`, `B_q`, and `B_mem`. Bridge consequence: the cross-term branch is
`INPUT_REVIEW_PACKET_NUMERIC_PROTOCOL_BOUND_READY`; the next required action is
`evaluate_numeric_epsilon_cross_protocol_bound`. This is still not endpoint
authorization.

The B_i coefficient-rule gate then fixes the feature-normalization side of the
same bound and carries the frozen protocol coefficients. The source-normalized
features are `f_PA=0.5`, `f_R=0.25`, `f_q=1.0`, and `f_mem=1.0`; `f_mem` is a
source-reviewed morphological-history proxy. The conservative baseline keeps
the coefficients `B_PA`, `B_R`, `B_q`, and `B_mem` frozen to `1`; the active
formula-conditional sharpened protocol uses `0.5`. Bridge consequence:
`FEATURE_NORMALIZATION_AND_B_VALUES_READY_PROTOCOL_BOUND` and
`NUMERIC_EPSILON_PROTOCOL_BOUND_READY`.

The epsilon-cross bound-expression shell then makes the current algebraic
state explicit:
`|epsilon_cross| <= 0.5*B_PA + 0.25*B_R + 1*B_q + 1*B_mem`. This is a
numeric protocol expression. Under the conservative `B_i=1` baseline it gives
`|epsilon_cross| <= 2.75`; under the active second-order-remainder `B_i=0.5`
rule it gives `|epsilon_cross| <= 1.375`. Bridge consequence:
`NUMERIC_EPSILON_PROTOCOL_BOUND_READY_CAVEATED`. This is a residual-blind
protocol upper bound, not a final physical amplitude derivation.

The readout sensitivity audit then propagates the active `1.375` bound through
the generated NGC4088 preflight profile without comparing to observed rotation
residuals. It preserves an important negative/preparatory result: the sharpened
bound is materially tighter than the `2.75` unit baseline, but it remains
larger than one, so sign stability and monotonicity are not guaranteed. Bridge
consequence: cross-term promotion still needs sharper Tau-side locality, sign,
or monotonicity constraints before endpoint use.

The locality-coupled narrowing supplies that next source-side restriction in a
residual-blind way. Instead of allowing all normalized source features to add
independently, the cross-term is required to be supported by adjacent
source/readout couplings:
`|epsilon_cross| <= 0.5*f_PA*f_R + 0.5*f_R*f_q + 0.5*f_q*f_mem`. For NGC4088,
with `f_PA=0.5`, `f_R=0.25`, `f_q=1.0`, and `f_mem=1.0`, this gives
`|epsilon_cross| <= 0.6875`. Bridge consequence:
`LOCALITY_EPSILON_BOUND_READY_SIGN_STABLE`. This is a useful narrowing because
it is below one, so the negative extreme cannot invert the leading correction.
It is still formula-conditional: the adjacency chain must eventually be derived
from a final Tau-side locality theorem before physical promotion.

The NGC4088 readout promotion gate then separates preflight readiness from
endpoint authorization. Five gates pass: `SOURCE_ONSET_READY`,
`DIMENSIONAL_CARRIER_READY`, `SOURCE_BASIS_SANITY`,
`RESIDUAL_BLIND_GENERATION`, and `ENDPOINT_SCORE_GUARD`. Three gates remain
blocked: `INDEPENDENT_DIGITIZATION_REVIEW`, `PHYSICAL_NORMALIZATION_LAW`, and
`POPULATION_GENERALIZATION`. Bridge consequence: NGC4088 is now
`PROMOTION_BLOCKED_PREFLIGHT_READY`. This is progress, because the remaining
blockers are precise; it is not validation, because the candidate still lacks
an independently reviewed onset, a derived/accepted physical normalization law,
and a predeclared source-rich comparison sample.

The promotion theorem skeletons now state the minimal corrected claims. Their
current proof status is `CONDITIONAL_INCOMPLETE`, not proven endpoint
eligibility:

```text
TAIL-HI-EXTENT-PROMOTION-LEMMA-001
    RHI can promote scale-tail only if it constrains the same outer-disk
    transition kernel, not merely generic gas extent.

COMPACT-SUPPORT-PROMOTION-LEMMA-001
    Reff/component evidence can promote compact only if it constrains compact
    support, not merely global half-light structure.

EDGE-DISK-VERTICAL-PROMOTION-LEMMA-001
    edge-disk evidence can promote thick/flared only if it gives a measured or
    bounded vertical kernel parameter, not merely a projection caveat.
```

Bridge consequence: the theorem layer is now explicit enough to block
overclaiming. A conditional row can become strict kernel-ready only when the
missing assumption in the relevant lemma is discharged by direct source-native
data or by a residual-blind Tau-side derivation.

The promoted-kernel stress diagnostic reruns the S4G75 lane with the two direct
S4G overrides. NGC5985 improves strongly when compact support is replaced by
direct S4G bulge `Re` (`matched RMSE 59.896708 -> 50.032494`). NGC5907 is
essentially unchanged/slightly worse when the thick/flared proxy is replaced by
direct S4G edge-disk `hz2/hr2` (`17.013339 -> 17.025301`). Bridge consequence:
direct compact support is promising in this pilot, while thick/flared still
needs a better vertical readout or projection rule.

Formula-conditional source-normalized L2 preflight:

```bash
python scripts/build_tau_side_source_normalization_derivation_audit.py
```

Bridge interpretation: this derivation audit is the source of the predeclared
orientation signs and source-evidence gates used below. It records compact/tail
as positive readout-orientation candidates and exponential/thick as negative
readout-orientation candidates, with proxy evidence attenuated to 0.35 and
missing source support set to zero. This is a derivation manifest, not endpoint
selection: the signs are theory-conditional bridge derivations, while the proxy
attenuation is the coarse executable representative of the conservative
Tau-side readout-admission product. None of these constants may be selected from
endpoint residuals, and the conservative evidence geometry is not claimed as a
final universal Tau-side evidence law.

```bash
python scripts/run_tau_side_source_normalized_l2_endpoint.py
```

Residual-blind rule:

```text
normalized_shape_gK(r) = kernel_gK(r) / median_r |kernel_gK(r)|
c_g = median_r max(v_v6^2 - v_n^2, 0) / median_r v_v6^2
delta v_gK^2(r) = sigma_K e_gK w_gK c_g median_r(v_n^2) normalized_shape_gK(r)
```

Current holdout status:

```text
Beats old L2 intake endpoint: 0.568.
Beats TPG/v6:                0.455.
Beats MOND:                  0.545.
Median minus old L2 RMSE:   -0.272.
```

Bridge interpretation: this is the first concrete residual-blind Tau-side
source-normalization candidate in the Paper 8 pipeline. It weakly improves the
raw L2 intake endpoint, but it is still not an accepted normalization law. The
weakest remaining steps are source-native promotion of the orientation signs,
accepted per-galaxy evidence assignments, and accepted
morphology-memory/projection evidence before the rule can be frozen. The proxy
gate is no longer treated as a free protocol constant: within the current
conservative Tau-side readout-admission geometry, the standard proxy product is
derived as `0.70 * 0.70 * 0.85 * 0.85 = 0.354025`.

Sensitivity audit:

```bash
python scripts/audit_tau_side_source_normalization_sensitivity.py
```

Current holdout status:

```text
primary proxy gate 0.35: beats old L2 0.568, TPG/v6 0.455, MOND 0.545.
no proxy gate:           beats old L2 0.545.
full proxy gate:         beats old L2 0.523, TPG/v6 0.523.
all-positive signs:      beats old L2 0.477.
all-negative signs:      beats old L2 0.432.
```

Bridge interpretation: the orientation structure is not cosmetic. If all signs
are forced positive or negative, the source-normalized rule weakens. The proxy
gate is still sensitive, so it cannot be endpoint-selected; its bin ladder is
now derived inside the conservative Tau-side readout-admission geometry, while
the galaxy/component evidence assignments must still be accepted before freeze.

Tau-side evidence-measure gate:

```bash
python scripts/build_tau_side_evidence_measure_gate.py
python scripts/run_tau_side_evidence_measure_l2_endpoint.py
```

Current full-sample evidence-measure status:

```text
Components audited:            406.
Proxy/partial components:      105.
Median proxy E_tau:            0.354025.
Mean proxy E_tau:              0.335798.
Median proxy minus fixed 0.35: +0.004025.
```

Current holdout endpoint stress test with `E_tau(g,K)` gates:

```text
beats old L2 intake 0.568, TPG/v6 0.455, MOND 0.545.
median E_tau-minus-old-L2 RMSE: -0.236.
```

Bridge interpretation: the fixed proxy bin is now replaceable by a
galaxy/family-specific residual-blind evidence-measure candidate. The median
proxy value reproduces the old `0.35` gate as the coarse-grid consequence
`0.354025` of the conservative readout-admission product. This is a promotion
path, not model selection. The `q_i` factors are still theory-candidate
source/readout assignments and must not be chosen from endpoint residuals. The
generated component table now also stores per-factor status labels: accepted
and missing gates are definition-derived limit cases, while proxy/partial
factors remain
`THEORY_CANDIDATE_FACTOR_GEOMETRY_NOT_ACCEPTED`.

## Mixed Readout Candidate Acquisition Queue

Paper 8 now separates the mixed-readout population claim from the useful
NGC4013 diagnostic/frozen-protocol milestone. The operational queue is
generated by:

```bash
python scripts/build_mixed_readout_candidate_acquisition_queue.py
```

Current status:

```text
MIXED_CANDIDATE_QUEUE_CREATED_NOT_ENDPOINT
Frozen reference mixed protocols:             1
Source-rule candidate rows:                   3
P0 formula-freeze candidates:                 1
Minimum prospective mixed protocols required: 3
Additional protocols needed after reference:  2
Next recommended mixed freeze case:           NGC5907
Endpoint scores allowed:                      false
Uses vobs/residuals in selection:             false
```

Bridge interpretation: mixed readouts can only become a population-level
Tau Core test if the candidate lane is selected from source-side morphology,
decomposition, projection, warp, vertical, or history evidence before scoring.
NGC4013 is the reference frozen prospective mixed protocol, but it is not
retroactive population validation. NGC5907 is the strongest next formula-freeze
candidate because its source layer already contains disk/truncation scale
information, optical-warp geometry, interaction/warp context, and
vertical/projection context. Its prior projection endpoint cannot be reused as
mixed-readout evidence; it requires a fresh mixed formula-freeze gate. NGC7331
is a caveated vertical/outer-warp candidate, while NGC4183, NGC4088, and the
S4G75 rows are source-acquisition or independent-review rows rather than
endpoint-ready mixed cases.

NGC5907 mixed formula-freeze:

```bash
python scripts/build_ngc5907_expdisk_projection_mixed_formula_freeze_gate.py
python scripts/build_mixed_readout_population_validation_gate.py
```

Current status:

```text
MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING
Formula: v_mix^2(R)=v_K_exponential_disk^2(R)*(1-gamma_proj*K_proj(R))
Delta:   -gamma_proj*K_proj(R)*v_K_exponential_disk^2(R)
Carrier: v_K_exponential_disk
Projection kernel: inherited unchanged from NGC5907_PROJECTION_ATTENUATION_V1
Dimension check: pass
Carrier limits: K_proj=0 or gamma_proj=0 recovers v_K_exponential_disk
Uses vobs/residual in construction: false
Prior projection endpoint used as mixed evidence: false
Mixed endpoint scores allowed by this gate: false
Prospective mixed protocol ready: true
```

Population-gate status after this freeze:

```text
Prospective mixed protocols ready: 3/3
Ready rows: NGC4013, NGC5907, caveated NGC7331
Endpoint scores run: false
Next requirement: run predeclared mixed-population endpoints from unchanged
                  frozen manifests, preserving NGC7331 broad-window caveats.
```

Bridge interpretation: this is the first concrete improvement over the previous
one-case mixed state. It does not show that the mixed family fits NGC5907, and
it does not turn the old projection endpoint into mixed evidence. It only
establishes that a second source-supported mixed readout formula has been
frozen before mixed scoring.

NGC7331 caveated mixed formula-freeze:

```bash
python scripts/build_ngc7331_outer_warp_vertical_caveat_gate.py
python scripts/build_ngc7331_fractional_warp_onset_source_gate.py
python scripts/build_ngc7331_fractional_onset_v2_replay_freeze_gate.py
python scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.py
python scripts/build_mixed_readout_population_validation_gate.py
```

Current status:

```text
CAVEATED_MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING
Formula: v_mix^2(R)=v_K_exponential_disk^2(R)*(1-gamma_vow*K_vow(R))
Delta:   -gamma_vow*K_vow(R)*v_K_exponential_disk^2(R)
Carrier: v_K_exponential_disk
Window:  broad source-scale outer window R_s -> R_HI
Reason:  V1 was frozen before the later fractional-onset source gate
Fractional onset source gate:
         FRACTIONAL_WARP_ONSET_SOURCE_READY_REPLAY_REQUIRED
         R_onset ~= 0.5 R_Ho ~= 14.431691 kpc
         candidate V2 window: 14.431691 -> 27.01 kpc
V2 replay freeze:
         V2_REPLAY_PROTOCOL_READY_NOT_SCORED
         formula_id = NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1
         endpoint scores allowed = false
Dimension check: pass
Carrier limits: W_outer=0 or gamma_vow=0 recovers v_K_exponential_disk
Uses vobs/residual in construction: false
Mixed endpoint scores allowed by this gate: false
Prospective mixed protocol ready: true
```

Bridge interpretation: NGC7331 resolves the minimum case-count blocker, but in
a caveated way. The vertical scale and projected HWHM are source-derived; the
V1 outer-warp term uses a broad source-scale window. The later source-only gate
tightens the caveat by recording a Bosma fractional onset, and the V2 replay
freeze gate makes that input executable as a frozen formula manifest. This
still cannot be applied retroactively to the already scored V1 endpoint. It is
a replay/holdout V2 input, not a post-hoc endpoint repair.

Mixed-population endpoint run:

```bash
python scripts/run_mixed_readout_population_endpoint.py
```

Current status:

```text
MIXED_POPULATION_ENDPOINT_PRELIMINARY_CONTROL_RESULT
Cases scored:                         3
Fresh prospective cases:              2
Caveated cases:                       1
Mean RMSE mixed readout:              16.414 km/s
Mean RMSE Newtonian baryonic:         70.510 km/s
Mean RMSE TPG/v6 proxy:               18.181 km/s
Mean RMSE MOND proxy:                 20.747 km/s
Mean RMSE exponential-disk carrier:   17.241 km/s
Mixed beats Newton/TPG/MOND/carrier:  3/3, 3/3, 3/3, 3/3
Construction used vobs/residuals:     false
Scoring used vobs:                    true
```

Per-case score:

```text
NGC4013  RMSE mixed=10.615, TPG/v6=12.274, MOND=14.334,
         carrier=10.880
         Caveat: retrospective frozen-reference protocol.

NGC5907  RMSE mixed=16.373, TPG/v6=16.786, MOND=18.595,
         carrier=17.370
         Caveat: prior projection endpoint is not reused as mixed evidence.

NGC7331  RMSE mixed=22.256, TPG/v6=25.485, MOND=29.312,
         carrier=23.473
         Caveat: broad outer window; no numeric warp onset yet.
```

Bridge interpretation: this is the first executable mixed-readout endpoint
signal from frozen manifests. It is encouraging because the mixed readout beats
the local comparators in all three prepared rows, but it is not yet a
population-validation result. The next required bridge gate is a
wrong-family / shuffled-label mixed-population control: the result must show
that source-matched mixed readouts beat wrong mixed readouts, not merely that
three hand-audited source-supported lanes score well.

NGC4013 mixed accepted-endpoint blocker:

```bash
python scripts/build_ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_gate.py
```

Current status:

```text
MIXED_ACCEPTED_ENDPOINT_BLOCKED_RETROACTIVE_PROTOCOL_READY
source rule ready = true
formula frozen for future scoring = true
endpoint-blind construction = true
frozen protocol RMSE = 10.614758 km/s
best local baseline RMSE = 10.880207 km/s
wrong mixed-family mean RMSE = 12.132137 km/s
best wrong mixed-family RMSE = 11.367008 km/s
endpoint scores allowed as accepted endpoint = false
```

Bridge interpretation: NGC4013 is now sharper, not weaker. The mixed
exponential-disk plus WVO readout is source-supported, formula-frozen, and
prospective-ready, and its inspected score is encouraging. It is still blocked
as an accepted endpoint because the mixed lane was developed after the NGC4013
wrong-family/control context had already been inspected. The correct use is as
a frozen-reference/protocol-ready row, or as a formula to be used in a
predeclared replay/holdout lane or future source-selected cases.

Mixed-population wrong-label / shuffled-label control:

```bash
python scripts/run_mixed_readout_population_control_audit.py
```

Current status:

```text
PASSED_3CASE_WRONG_LABEL_AND_SHUFFLED_CONTROL
Formula labels tested:                 3
Galaxies tested:                       3
Mean RMSE matched labels:              16.414 km/s
Mean RMSE wrong labels:                17.287 km/s
Matched minus wrong-label mean:        -0.872 km/s
Matched labels rank first per galaxy:  3/3
Matched diagonal permutation rank:     1/6
Best shuffled mean RMSE:               16.710 km/s
Matched minus best shuffled:           -0.296 km/s
Construction used vobs/residuals:      false
Scoring used vobs:                     true
```

Per-galaxy wrong-label control:

```text
NGC4013  matched=10.615, wrong mean=12.132, best wrong=11.367
NGC5907  matched=16.373, wrong mean=17.055, best wrong=16.848
NGC7331  matched=22.256, wrong mean=22.673, best wrong=22.668
```

Bridge interpretation: this is the first direct mixed-readout specificity
signal. The result is no longer merely "the three mixed curves look good";
within the three frozen formula labels, the source-matched diagonal is the best
assignment. The claim remains small-N and caveated, especially because NGC4013
is a retrospective frozen-reference case and NGC7331 uses a broad outer-window
caveat. The next bridge requirement is to repeat the same matched-vs-wrong
control on more source-rich mixed candidates.

Strict replay/holdout mixed endpoint:

```bash
python scripts/run_mixed_readout_replay_holdout_endpoint.py
```

Current status:

```text
MIXED_REPLAY_HOLDOUT_2CASE_PRELIMINARY_RESULT
Cases scored:                           2
Case set:                               NGC5907 fresh prospective;
                                        NGC7331 V2 fractional-onset replay
NGC4013:                                excluded as retrospective reference
Mean RMSE mixed replay/holdout:         19.552 km/s
Mean RMSE Newtonian baryonic:           72.919 km/s
Mean RMSE TPG/v6 proxy:                 21.135 km/s
Mean RMSE MOND proxy:                   23.954 km/s
Mean RMSE exponential-disk carrier:     20.421 km/s
Mixed beats Newton/TPG/MOND/carrier:    2/2, 2/2, 2/2, 2/2
Matched beats all wrong labels:         0/2
Matched permutation rank:               2/2
Best shuffled mean RMSE:                19.508 km/s
Matched minus best shuffled:            +0.044 km/s
Construction used vobs/residuals:       false
Scoring used vobs:                      true
```

Per-case replay/holdout score:

```text
NGC5907  matched=16.373, best wrong=16.349,
         matched rank=2/2.

NGC7331  V2 matched=22.732, best wrong=22.668,
         matched rank=2/2.
```

Bridge interpretation: the strict replay/holdout run is a preserved negative
specificity result. It still improves over Newtonian, TPG/v6, MOND, and the
exponential-disk carrier in both fresh rows, but the matched formulas do not
beat the wrong-label controls. This means the current two fresh mixed formulas
are not yet readout-specific enough under the V2 replay/holdout criterion. The
likely bottleneck is not the existence of a mixed attenuation response, but the
source-native subfamily separation: projection/vertical/outer-warp attenuation
branches remain too similar unless their kernels are sharpened by independent
source-native morphology fields. This result must be kept as a failure map, not
converted into a validation claim.

Mixed kernel observable separation gate:

```bash
python scripts/build_mixed_kernel_observable_separation_gate.py
```

Current source-side status:

```text
SOURCE_KERNEL_OBSERVABLE_SEPARATION_PASS
Diagnostic status:                     DIAGNOSTIC_ONLY_NOT_ENDPOINT
Cases audited:                         2
Matched source-rank first:             2/2
Minimum source-similarity margin:       0.501
Mean source-similarity margin:          0.651
Uses vobs/residuals:                   false
Endpoint scores allowed:               false
```

Per-source-lane similarity:

```text
NGC5907  projection-mixed similarity=0.921,
         vertical/outer-warp V2 similarity=0.419.

NGC7331  vertical/outer-warp V2 similarity=0.978,
         projection-mixed similarity=0.177.
```

Bridge interpretation: the replay/holdout specificity failure is now sharper.
At the source-observable level, the two fresh lanes do separate: NGC5907 is
projection/truncation dominated, while NGC7331 V2 is fractional-onset
vertical/outer-warp dominated. Therefore the immediate bottleneck is not that
the residual-blind source labels are indistinguishable. The bottleneck is the
current source-to-kernel map: the projection and vertical/outer-warp 4D readout
kernels are still too similar after conversion into attenuation curves. The
next bridge obligation is to derive sharper, source-native kernel shapes before
rerunning the replay/holdout wrong-label and shuffled-label specificity test.

Mixed kernel sharpening preflight:

```bash
python scripts/build_mixed_kernel_sharpening_preflight.py
```

Current source-side formula-shape status:

```text
SOURCE_KERNEL_SHARPENING_PREFLIGHT_READY_NOT_ENDPOINT
Diagnostic status:                         DIAGNOSTIC_ONLY_NOT_ENDPOINT
Current kernel cross-similarity:           0.991
Source-sharpened kernel cross-similarity:  0.644
Kernel shape separation gain:              0.347
Projection edge exponent:                  2.527
Vertical decay:                            2.165
Uses vobs/residuals:                       false
Endpoint scores allowed:                   false
```

Preflight source-sharpened shells:

```text
K_proj_sharp(u)
    = S(u)^(1 + Pi_projection + C_trunc)
      * (1 + C_trunc S(u))/(1 + C_trunc)

K_vow_sharp(u)
    = S(u) exp(-(1 + R_onset/R_HI + A_vertical)u)
      + T_projected S(u)(1 - S(u))
```

Here `u` is the dimensionless active-window coordinate and `S(u)` is the
smoothstep window. All sharpening coefficients are dimensionless source-native
quantities. The projection branch becomes outer-edge/truncation dominated; the
vertical/outer-warp branch becomes onset/vertical-response dominated. Bridge
interpretation: this is not a fit improvement and not an endpoint score. It is
the next formula-freeze obligation: create V2/V3 manifests with these
source-sharpened kernels before any new replay/holdout scoring.

NGC5907 accepted mixed endpoint promotion:

```bash
python scripts/build_ngc5907_expdisk_projection_mixed_accepted_endpoint_gate.py
python scripts/run_ngc5907_expdisk_projection_mixed_accepted_endpoint.py
```

Current status:

```text
ACCEPTED_MIXED_ENDPOINT_FREEZE_READY
ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT
matched mixed RMSE = 16.372532 km/s
best local baseline = TPG/v6, RMSE = 16.785510 km/s
wrong mixed-family mean RMSE = 17.055166 km/s
best wrong mixed-family RMSE = 16.847989 km/s
matched rank among all inspected models = 1
previous projection endpoint used as mixed evidence = false
```

Bridge interpretation: NGC5907 is the first row from the three-case mixed
packet promoted to its own accepted mixed single-galaxy endpoint. The promotion
is narrow but real: the mixed formula was frozen before scoring, the scoring
script reads the accepted manifest unchanged, and the prior NGC5907 projection
endpoint is recorded only as control context rather than as mixed-label
evidence. This strengthens the three-case packet without turning it into
population validation.

NGC7331 caveated accepted mixed endpoint promotion:

```bash
python scripts/build_ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_gate.py
python scripts/run_ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint.py
```

Current status:

```text
CAVEATED_ACCEPTED_MIXED_ENDPOINT_FREEZE_READY
CAVEATED_ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT
matched mixed RMSE = 22.255666 km/s
best local baseline = exponential-disk carrier, RMSE = 23.472977 km/s
wrong mixed-family mean RMSE = 22.673071 km/s
best wrong mixed-family RMSE = 22.668250 km/s
matched rank among all inspected models = 1
outer-warp numeric onset available = false
broad outer-window caveat attached = true
fractional onset source gate = replay/holdout required
candidate V2 onset = 14.431691 kpc
V2 replay freeze status = V2_REPLAY_PROTOCOL_READY_NOT_SCORED
```

Bridge interpretation: NGC7331 is promoted only in caveated accepted form. The
vertical/outer-warp mixed formula is frozen before scoring and the endpoint
script reads the accepted manifest unchanged, but the scored V1 radial window
remains a broad source-scale outer window from `R_s` to `R_HI`. A later
fractional-onset source gate gives a candidate V2 inner window near 14.43 kpc;
the V2 replay freeze gate has already frozen that candidate as an executable
manifest, but using it requires a predeclared replay/holdout run. This makes
the row usable as a narrow single-galaxy mixed control while preserving the
remaining source-side caveat.

Mixed-population expansion gate:

```bash
python scripts/build_mixed_readout_population_expansion_gate.py
```

Current status:

```text
NEXT_MIXED_CASE_IDENTIFIED_FORMULA_FREEZE_BLOCKED
Three-case control passed:             true
Next primary galaxy:                   NGC4088
Candidate readout:                     K_expdisk_warp_history_coupled_mixed_review
Formula freeze allowed now:            false
Candidates ranked:                     10
Candidates freeze-allowed now:         0
Endpoint scores allowed:               false
Uses vobs/residuals in selection:      false
```

NGC4088 source-side ingredients:

```text
x_warp_onset ~= 0.282353
q_warp = 1
m_history_warp = 1
|epsilon_cross| <= 0.6875
input review = INPUT_REVIEW_PACKET_NUMERIC_PROTOCOL_BOUND_READY
breakthrough status = BREAKTHROUGH_PROTOCOL_BOUND_READY_NOT_ENDPOINT
```

NGC4088 remaining blockers:

```text
INDEPENDENT_DIGITIZATION_REVIEW
PHYSICAL_NORMALIZATION_LAW
POPULATION_GENERALIZATION
BLOCKED_MULTIPLE_RESIDUAL_BLIND_SCALES
```

Bridge interpretation: NGC4088 is the closest fourth mixed candidate because it
has a continuous residual-blind warp/history protocol chain. It is nevertheless
formula-freeze blocked. The strong NGC4088 diagnostic curve cannot be used as
promotion evidence; the fourth-case path must first resolve digitization,
normalization, and scale-uniqueness residual-blind.

NGC4088 formula-freeze blocker-resolution plan:

```bash
python scripts/build_ngc4088_mixed_formula_freeze_blocker_resolution_plan.py
```

Current status:

```text
NGC4088_FORMULA_FREEZE_BLOCKER_RESOLUTION_PLAN_CREATED
Formula-freeze blockers:              3
Population-claim blockers:            1
Protocol-ready supports:              3
Formula freeze allowed now:           false
Endpoint scores allowed:              false
Uses vobs/residuals:                  false
```

Local formula-freeze blockers:

```text
B1_INDEPENDENT_XW_DIGITIZATION_REVIEW
B2_PHYSICAL_NORMALIZATION_LAW
B3_SCALE_UNIQUENESS
```

Population-scope blocker:

```text
B4_POPULATION_GENERALIZATION
```

Bridge interpretation: this is a useful sharpening. The NGC4088 warp/history
chain has become strong enough to be the next source-side target, but not strong
enough to score as a fourth mixed endpoint. Three local blockers must close
before formula freeze; population generalization is a separate caveat for broad
claims, not a substitute for those local obligations.

Independent `x_w` review packet for blocker B1:

```bash
python scripts/build_ngc4088_independent_xw_digitization_review_packet.py
```

Current status:

```text
INDEPENDENT_XW_REVIEW_PACKET_READY_RESPONSE_PENDING
B1_NOT_RESOLVED_INDEPENDENT_REVIEW_PENDING
first_pass_x_w = 0.282353
acceptance_tolerance_x_w = 0.070588
formula_freeze_allowed_now = false
endpoint_scores_allowed = false
```

Bridge interpretation: the first-pass `x_w` can remain a preflight mapping
input, but it is not yet an accepted endpoint-freeze input. B1 closes only if an
independent reviewer or frozen image-analysis repeat remeasures the side-by-side
warp onset from the frozen page-76/page-77 source packet without using `vobs`,
rotation residuals, endpoint scores, fit ranks, or required-`S_tau` diagnostics.
If the repeat agrees within the frozen tolerance, B1 can move to resolved; if it
does not, the lane must freeze a wider source-side uncertainty interval or stay
blocked.

Frozen image-analysis repeat attempt for B1:

```bash
python scripts/build_ngc4088_b1_frozen_image_repeat_attempt.py
```

Current status:

```text
FROZEN_IMAGE_REPEAT_ATTEMPT_COMPLETE_INCONCLUSIVE
B1_NOT_RESOLVED_IMAGE_REPEAT_INCONCLUSIVE
n_panels_analyzed = 23
n_elongated_components = 21
repeat_signal_status = WARP_LIKE_PA_DEPARTURE_DETECTED
accepted_x_w_from_repeat_available = false
formula_freeze_allowed_now = false
endpoint_scores_allowed = false
```

Bridge interpretation: the automated repeat is useful but not sufficient. It
detects source-image geometry consistent with a warp-like position-angle
departure, using only the frozen page-76 ROI and worksheet grid. But it cannot
promote an accepted `x_w`, because the printed channel-map crop still lacks a
robust source-native radial calibration and component-selection stability strong
enough to replace independent review. Therefore B1 remains open, now for a
sharper reason rather than an unspecified missing check.

Source-native radial calibration packet for B1:

```bash
python scripts/build_ngc4088_b1_source_native_radial_calibration_packet.py
```

Current status:

```text
B1_SOURCE_NATIVE_RADIAL_CALIBRATION_PACKET_CREATED
RADIAL_CALIBRATION_NOT_ACCEPTED
B1_NOT_RESOLVED_RADIAL_CALIBRATION_OPEN
first_pass_x_w = 0.282353
accepted_x_w_for_formula_freeze = false
formula_freeze_allowed_now = false
endpoint_scores_allowed = false
```

Bridge interpretation: B1 is now split into two separable subproblems. The
image evidence supports a warp-like departure, but formula freeze requires an
accepted source-native radius. The allowed closure routes are: independent
reviewer reports direct arcmin onsets; frozen image repeat gains radial tick or
coordinate calibration; or the original WHISP/channel-map data product is cached
and used for source-native onset extraction. The existing first-pass `x_w` is
dimensionally valid, but not accepted for formula freeze by itself.

Original/source-native H I data acquisition audit for B1:

```bash
python scripts/build_ngc4088_b1_original_hi_data_acquisition_audit.py
```

Current status:

```text
RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE_AUDITED_NO_DIRECT_PRODUCT_CACHED
B1_NOT_RESOLVED_ORIGINAL_DATA_ROUTE_OPEN
direct_source_native_product_cached = false
formula_freeze_allowed_now = false
endpoint_scores_allowed = false
```

Bridge interpretation: the original-data route is now a reproducible audit
object rather than an informal hope. The package probes the WHISP catalog path,
direct UGC7081/NGC4088 pages, cached printed-page context, and NED metadata
gateway without using `vobs`, residuals, or endpoint ranks. The corrected WHISP
identifier is `UGC 7081`, and this route now caches the WHISP graphical H I
overview plus observation/reduction notes. The current result is not an
astrophysical claim that no H I data exist. It says that this public package has
not yet cached a direct source-native H I/FITS product sufficient to close B1 by
itself.

WHISP overview extraction review packet:

```bash
python scripts/build_ngc4088_b1_whisp_overview_extraction_review_packet.py
```

Current status:

```text
WHISP_OVERVIEW_EXTRACTION_PACKET_READY_RESPONSE_PENDING
B1_NOT_RESOLVED_WHISP_OVERVIEW_REVIEW_PENDING
whisp_graphical_overview_cached = true
accepted_x_w_for_formula_freeze = false
formula_freeze_allowed_now = false
endpoint_scores_allowed = false
```

Bridge interpretation: the cached WHISP overview is stronger than the printed
paper crop because its position-velocity panel has an explicit `Offset from
center (arcmin)` axis. It can support a residual-blind direct-arcmin onset
review. It still cannot close B1 by itself: the response must be filled by an
independent reviewer or frozen extraction method, and the resulting `x_w` must
either agree with the first-pass value within tolerance or freeze a source-side
uncertainty interval before formula use.

Frozen WHISP overview extraction attempt:

```bash
python scripts/build_ngc4088_b1_whisp_overview_frozen_extraction_attempt.py
```

Current status:

```text
FROZEN_WHISP_OVERVIEW_EXTRACTION_ATTEMPT_COMPLETE_AGREES_WITH_FIRST_PASS
B1_NOT_RESOLVED_FROZEN_EXTRACTION_PROMOTION_REVIEW_REQUIRED
x_w_review = 0.298333
first_pass_x_w = 0.282353
agrees_with_first_pass_within_tolerance = true
accepted_x_w_for_formula_freeze = false
endpoint_scores_allowed = false
```

Bridge interpretation: this is a real provenance strengthening. A frozen,
residual-blind image script reads the WHISP position-velocity panel, selects the
two largest opposite-side high-saturation components, and maps their centroids
through the source-provided arcmin offset axis. The resulting `x_w_review`
agrees with the first-pass value. It is still not an endpoint; the separate
promotion review below decides whether the value can be used as a caveated B1
formula-freeze input.

WHISP promotion review:

```bash
python scripts/build_ngc4088_b1_whisp_promotion_review.py
```

Current status:

```text
B1_CAVEATED_XW_ACCEPTED_FOR_FORMULA_FREEZE_NOT_ENDPOINT
B1_RESOLVED_CAVEATED_WHISP_GRAPHICAL_XW
x_w_source_consistency_value = 0.298333
accepted_x_w_for_formula_freeze = true
formula_freeze_allowed_now = true
endpoint_scores_allowed = false
```

Bridge interpretation: this closes B1, but only with an explicit provenance
caveat. The WHISP graphical overview extraction is residual-blind, two-sided,
source-axis calibrated, and agrees with the first-pass value; it is therefore
accepted as the B1 `x_w` formula-freeze input. The caveat is that the value comes
from a graphical overview rather than a direct source-coordinate H I/FITS
product. In bridge language: the B1 morphology/readout scale gate is closed, but
the NGC4088 endpoint gate remains closed until B2 and B3 are also closed.

B2 physical-normalization derivation synthesis:

```bash
python scripts/build_ngc4088_b2_physical_normalization_derivation_synthesis.py
```

Current status:

```text
B2_FORMULA_CONDITIONAL_DERIVATION_SYNTHESIZED_LAW_STILL_OPEN
formula_quality = DIMENSIONALLY_VALID_RESIDUAL_BLIND_EXECUTABLE
law_quality = NOT_DERIVED_TAU_SIDE_PHYSICAL_NORMALIZATION_LAW
lambda_w = sigma_warp q_warp x_w Vflat^2
formula_freeze_alignment_status = ALIGNED_TO_FORMULA_FREEZE_MANIFEST
numeric_lambda_w = 8795.111752 km^2/s^2
first_pass_lambda_w = 8324.016 km^2/s^2
normalization_source = FORMULA_FREEZE_MANIFEST_REVIEW_ACCEPTED_XW
formula_freeze_allowed_now = false
endpoint_scores_allowed = false
```

Bridge interpretation: B2 is now narrowed to a precise formula-level result,
not a vague missing-normalization complaint. It is also now aligned to the
accepted NGC4088 formula-freeze manifest: the frozen endpoint formula uses the
caveated WHISP graphical-overview value `x_w = 0.298333`, so
`lambda_w = 8795.111752 km^2/s^2`. The earlier
`8324.016 km^2/s^2` value is preserved as first-pass pre-review provenance,
not as the current frozen endpoint normalization. The executable conditional
formula is

```text
delta_v2_warp(R;p) = lambda_w C_warp(R/R_HI; x_w,p)
lambda_w = sigma_warp q_warp x_w Vflat^2
```

The remaining law obligations are equally explicit: construct the Tau-side
closure functional `J_tau[lambda_w]`, justify `Vflat^2` as the frozen
asymptotic readout carrier, prove or bound separability/cross terms, and
transfer the same derivation gate to a predeclared warp/history sample. Until
those close, the formula remains formula-conditional and endpoint-blocked.

B2 closure/asymptotic conditional derivation gate:

```bash
python scripts/build_ngc4088_b2_closure_asymptotic_conditional_derivation_gate.py
```

Current status:

```text
B2_CONDITIONAL_THEOREM_ALIGNED_TO_FREEZE_MANIFEST_LAW_PREMISES_OPEN
numeric_lambda_w = 8795.111752 km^2/s^2
formula_freeze_alignment_pass = true
law_level_closed = false
endpoint_scores_allowed = false
uses_vobs_or_residual = false
```

Bridge interpretation: this is the strongest current B2 result. Given a
target-stationary `J_tau[lambda_w]`, a Tau-side asymptotic-carrier premise
selecting `Vflat^2`, and separable source factors with controlled cross terms,
the Euler condition algebraically yields
`lambda_w = sigma_warp q_warp x_w Vflat^2`. The gate does not close the
physical law: the Tau-side origin of `J_tau`, final forced `Vflat^2` carrier
dominance, and separability/cross-term theorem remain open.

B2 source-load closure functional gate:

```bash
python scripts/build_ngc4088_b2_source_load_closure_functional_gate.py
```

Current status:

```text
SOURCE_LOAD_CLOSURE_FUNCTIONAL_CONSTRUCTED_CONDITIONALLY
J_load[lambda_w] = 1/2 kappa_lambda || (lambda_w - Lambda_tau) C_warp ||_W^2
Lambda_tau = sigma_warp q_warp x_w Vflat^2
numeric_lambda_w = 8795.111752 km^2/s^2
n_pass = 5
n_open = 3
law_level_closed = false
```

Bridge interpretation: the closure-functional premise has been sharpened.
The package now has an explicit residual-blind norm-square functional whose
Euler equation yields the frozen NGC4088 normalization. This does not derive
the final physical law: the source-load origin of `Lambda_tau`, the final
forced `Vflat^2` carrier theorem, and the cross-term suppression bound remain
open.

B2 frozen asymptotic-carrier theorem gate:

```bash
python scripts/build_ngc4088_b2_frozen_asymptotic_carrier_theorem_gate.py
```

Current status:

```text
FROZEN_VFLAT2_CARRIER_CONDITIONAL_THEOREM_LAW_PROOF_OPEN
carrier_value = 29480.89 km^2/s^2
Lambda_tau = 8795.111752 km^2/s^2
formula_freeze_alignment_pass = true
n_pass = 6
n_conditional = 1
n_open_for_claims = 1
law_level_closed = false
```

Bridge interpretation: `Vflat^2` is no longer merely a convenient carrier name
inside the accepted NGC4088 formula-freeze manifest. Under the residual-blind,
source-onset, asymptotic-carrier, non-comparator, minimal-factorization rule,
it is conditionally justified as the frozen protocol carrier, and
`Lambda_tau = sigma_warp q_warp x_w Vflat^2` reproduces the accepted
`lambda_w = 8795.111752 km^2/s^2`. This is a real B2 strengthening, but not a
final Tau-side law proof: alternative-carrier exclusion, comparator autonomy,
and predeclared warp/history population transfer remain open for claims.

B2 population-transfer preflight gate:

```bash
python scripts/build_ngc4088_b2_population_transfer_preflight_gate.py
```

Current status:

```text
POPULATION_TRANSFER_PREFLIGHT_BUILT_EXACT_TRANSFER_BLOCKED_ANALOGUE_LANE_AVAILABLE
n_cases = 7
n_reference_exact_protocol = 1
n_exact_transfer_ready_excluding_reference = 0
n_partial_analogues = 3
n_blocked_acquisition_controls = 3
population_claim_allowed = false
endpoint_scores_allowed = false
```

Bridge interpretation: the package now distinguishes exact B2 transfer from
nearby mixed overlay/projection analogues. NGC4088 is the exact reference case.
NGC4013, NGC5907, and NGC7331 are useful analogues because they have
source-side mixed or outer-overlay protocols, but they do not instantiate the
same `sigma_warp q_warp x_w Vflat^2` warp/history source-load law. IC2574,
UGC05716, and NGC4183 remain blocked acquisition controls. Therefore the
population-transfer path is operationally defined, but no population claim is
allowed until at least two independent exact warp/history source-load cases
are source-frozen before scoring.

B2 exact-transfer candidate manifest:

```bash
python scripts/build_ngc4088_b2_exact_transfer_candidate_manifest.py
```

Current status:

```text
EXACT_TRANSFER_CANDIDATE_MANIFEST_BUILT_NO_READY_INDEPENDENT_CASE
n_cases = 5
n_reference_rows = 1
n_exact_transfer_ready = 0
n_partial_or_analogue_candidates = 3
n_requirements = 5
population_claim_allowed = false
```

Bridge interpretation: exact transfer now has a concrete five-field input
contract: `x_w`, `q_warp`, `sigma_warp`, `Vflat`, and `epsilon_cross` source
observables must be frozen before scoring. NGC7331 is the closest current
upgrade target because it already has a residual-blind fractional outer-warp
onset candidate. Its former `q_warp`, sign-context, and cross-term blocker is
now reduced by the source-only review/intake path: the exact-transfer
formula-freeze gate may proceed while carrying a `q_warp` interval and an
`epsilon_cross` caveat. NGC4013 and NGC5907 remain useful analogue lanes, not
exact B2 transfer cases.

NGC7331 exact-transfer upgrade gate:

```bash
python scripts/build_ngc7331_b2_exact_transfer_upgrade_gate.py
```

Current status:

```text
NGC7331_EXACT_TRANSFER_UPGRADE_FORMULA_FREEZE_INPUT_READY_NOT_ENDPOINT
x_w_available = true
Vflat_available = true
q_warp_available = true
sigma_warp_available = true
epsilon_cross_inputs_available = true
unit_q_sigma_lambda_preview = 30520.275307 km^2/s^2
n_pass_like = 7
n_blocked = 0
formula_freeze_allowed = true
endpoint_scores_allowed = false
```

Bridge interpretation: NGC7331 is now an actionable exact-transfer upgrade
target rather than a vague analogue. Its residual-blind fractional outer-warp
onset and SPARC `Vflat` carrier are available, and the source-only q-review
intake now supplies the remaining formula-freeze inputs as carried source-side
quantities. The unit-`q/sigma` scale `x_w Vflat^2` remains dimensional
bookkeeping only, not a scored formula. The next step is an exact B2
formula-freeze gate that propagates the `q_warp` interval and conservative
cross-term caveat; endpoint scoring remains forbidden until that separate
freeze gate exists and an accepted endpoint gate reads it unchanged.

NGC7331 exact B2 transfer interval formula-freeze gate:

```bash
python scripts/build_ngc7331_b2_exact_transfer_formula_freeze_gate.py
```

Current status:

```text
NGC7331_EXACT_B2_TRANSFER_INTERVAL_FORMULA_FREEZE_READY_NOT_SCORE
q_warp = [0.0079404475812108, 0.2057957876154617]
lambda_w = [242.344646, 6280.944095] km^2/s^2
epsilon_cross_bound = 0.488571397976179
lambda_w_cross_caveated = [123.941984, 9349.633732] km^2/s^2
n_kernel_grid_rows = 36
n_blocked = 0
endpoint_scores_allowed = false
```

Bridge interpretation: the exact B2 transfer formula is now frozen at
protocol level as an interval-valued source-side readout shell. The gate
strictly transfers the NGC4088 B2 convention
`lambda_w = sigma_warp q_warp x_w Vflat^2` and
`C_warp = q_warp max(0,(x-x_w)/(1-x_w))^p`, while explicitly marking this
`q_warp` placement as a law-level caveat. The output grid contains only
radius and carrier columns plus source-frozen interval readout columns; no
observed velocities or residuals are used. This is a formula-freeze result,
not an endpoint score.

NGC7331 exact B2 transfer interval-control audit:

```bash
python scripts/run_ngc7331_b2_exact_transfer_interval_control_audit.py
```

Current status:

```text
NGC7331_EXACT_B2_INTERVAL_CONTROL_AUDIT_COMPLETE_NOT_POINT_ENDPOINT
n_points = 36
coverage_fraction = 0.0
coverage_fraction_cross_caveated = 0.0
interval_distance_rmse = 56.267392 km/s
interval_distance_rmse_cross_caveated = 54.811910 km/s
best_baseline_model = EXPONENTIAL_DISK_CARRIER
best_baseline_rmse = 23.472977 km/s
construction_used_vobs = false
scoring_used_vobs = true
point_q_selected_from_residual = false
```

Bridge interpretation: after the formula freeze, the source-frozen B2
interval can be audited against the observed rotation curve without choosing a
post-hoc `q_warp` point. This interval-control audit is a negative or weak
transfer result for NGC7331: neither the strict interval nor the
cross-caveated interval covers the measured points, and the existing
exponential-disk carrier baseline has a lower point-RMSE. The result is
therefore not an accepted point endpoint and not a population-validation row.
It is useful because it shows that exact B2 population transfer is not
automatically licensed by a source-side interval freeze; NGC7331 remains a
control/audit case unless a new pre-frozen point-branch or different
source-derived readout protocol is declared before scoring.

NGC7331 exact-transfer source packet:

```bash
python scripts/build_ngc7331_b2_exact_transfer_source_packet.py
```

Current status:

```text
NGC7331_EXACT_TRANSFER_SOURCE_PACKET_BUILT_MEASUREMENTS_PENDING
n_requirements = 3
n_templates = 9
n_pass_like = 3
n_blocked = 3
formula_freeze_allowed = false
endpoint_scores_allowed = false
```

Bridge interpretation: the NGC7331 blocker is now operationally narrowed.
The packet defines residual-blind templates for `q_warp`, `sigma_warp`, and
`epsilon_cross` rather than leaving them as informal missing inputs. This
still does not freeze a formula: all three source packets must be filled and
reviewed before NGC7331 can become an exact B2 transfer endpoint.

NGC7331 exact-transfer source evidence review:

```bash
python scripts/build_ngc7331_b2_exact_transfer_source_evidence_review.py
```

Current status:

```text
NGC7331_SOURCE_EVIDENCE_REVIEW_BUILT_EXACT_TRANSFER_STILL_BLOCKED
complex_warp_context_confirmed = true
cross_terms_must_be_carried_or_bounded = true
q_warp_promoted = false
sigma_warp_promoted = false
epsilon_cross_promoted = false
formula_freeze_allowed = false
```

Bridge interpretation: the source evidence review strengthens NGC7331 as a
scientifically meaningful transfer target while preventing overclaiming. Bosma
H I context and the existing Patra vertical/projection context confirm a real
outer-warp/complex-readout situation, but they also make it unsafe to inherit
the NGC4088 sign and cross-term assumptions. NGC7331 therefore needs a
source-native H I warp amplitude/asymmetry measurement and sign/cross-term
review before exact B2 formula freeze.

NGC7331 H I warp acquisition route:

```bash
python scripts/build_ngc7331_b2_hi_warp_acquisition_route.py
```

Current status:

```text
NGC7331_HI_WARP_ACQUISITION_ROUTE_SOURCE_PRODUCTS_CACHED_WORKSHEET_READY
preferred_next_route = THINGS_QWARP_SIGN_CROSS_TERM_WORKSHEET
fallback_next_route = BOSMA_FIGURE_DIGITIZATION_WORKSHEET
q_warp_measurement_ready = false
sigma_warp_sign_ready = false
epsilon_cross_bound_ready = false
```

Bridge interpretation: the missing NGC7331 inputs now have concrete source
routes. The preferred THINGS route has now been locally cached and FITS-audited
at the moment-map level; the fallback route remains Bosma/NED figure
digitization of the published H I warp and tilted-ring geometry. The cached
products are sufficient to build a residual-blind worksheet, but they still do
not supply `q_warp`, the sign convention, or the cross-term bound by themselves.

NGC7331 THINGS q-warp measurement worksheet:

```bash
python scripts/build_ngc7331_things_qwarp_measurement_worksheet.py
```

Current status:

```text
NGC7331_THINGS_QWARP_WORKSHEET_READY_MEASUREMENT_PENDING
things_products_audited = true
geometry_defined = true
pa_reference_frozen = false
q_warp_measurement_ready = false
sigma_warp_sign_ready = false
epsilon_cross_bound_ready = false
```

Bridge interpretation: the NGC7331 source-native map geometry is now fixed
enough for review work: the worksheet records the THINGS WCS, SPARC `Rdisk`,
`RHI`, the replay-only `x_w`, and the pixel-space onset/reference scales. The
next task is an independent residual-blind fill of inner PA, outer ridge
offsets, side weights, sign, and cross-term fields.

NGC7331 THINGS q-warp first-pass measurement and sensitivity audit:

```bash
python scripts/build_ngc7331_things_qwarp_first_pass_measurement.py
python scripts/build_ngc7331_things_qwarp_measurement_sensitivity_audit.py
```

Current status:

```text
NGC7331_THINGS_QWARP_FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED
CENTROID_STABLE_BUT_ENVELOPE_STRONGER_REVIEW_REQUIRED
q_warp_first_pass_centroid = 0.006787
q_warp_envelope_p80_range = 0.194693..0.216899
formula_freeze_allowed = false
endpoint_scores_allowed = false
```

Bridge interpretation: the THINGS route now produces a reproducible
source-native `q_warp` candidate, but it also exposes a real observable-choice
gate. A conservative ridge-centroid observable gives a small, stable
`q_warp`, while the outer-envelope p80 observable gives a much stronger and
also stable warp-support measure. This is useful progress, not a freeze: an
independent review must decide which source-native observable corresponds to
the B2 `q_warp` strength carrier, and the MOM1 sign rule plus `epsilon_cross`
bound still have to be filled before exact transfer or endpoint scoring.

NGC7331 THINGS MOM1 sign/cross-term review:

```bash
python scripts/build_ngc7331_things_mom1_sign_cross_review.py
```

Current status:

```text
NGC7331_THINGS_MOM1_SIGN_CROSS_REVIEW_BUILT_FREEZE_BLOCKED
receding_side_consensus = CONSISTENT
inner_outer_receding_orientation_same_all = true
f_PA_max = 0.042833
epsilon_cross_candidate_bound = 0.488571
sigma_warp_sign_ready = false
epsilon_cross_bound_ready = false
```

Bridge interpretation: the MOM1 route adds source-native kinematic context.
The natural and robust velocity fields agree on the receding side and preserve
the inner/outer receding orientation, and the morphology/kinematic PA mismatch
is small. This supports a sign-review path, but it still does not freeze
`sigma_warp`, because the bridge must decide how source-side orientation maps
to added-readout versus attenuation. The candidate `epsilon_cross` bound is
also review-required; it is dominated by the still-open choice between
centroid and envelope `q_warp` observables rather than by a large MOM1 PA
misalignment.

NGC7331 q-warp observable-choice review gate:

```bash
python scripts/build_ngc7331_qwarp_observable_choice_review_gate.py
```

Current status:

```text
NGC7331_QWARP_OBSERVABLE_CHOICE_REVIEW_GATE_BUILT_FREEZE_BLOCKED
q_centroid_mid = 0.007940
q_envelope_mid = 0.205796
q_envelope_to_centroid_ratio = 25.917404
mom1_context_available = true
formula_freeze_allowed = false
endpoint_scores_allowed = false
```

Bridge interpretation: the NGC7331 THINGS route has now moved from data
absence to observable-choice review. The source-native maps support both a
small centroid-shift q observable and a much larger outer-envelope support
observable. Because these differ by a factor of about 26, the bridge cannot
honestly freeze `q_warp` by fiat. The next valid step is an independent
residual-blind review selecting centroid, envelope, or an explicit interval;
until then exact B2 transfer remains blocked.

NGC7331 q-warp observable-choice review packet:

```bash
python scripts/build_ngc7331_qwarp_observable_choice_review_packet.py
```

Current status:

```text
NGC7331_QWARP_OBSERVABLE_CHOICE_REVIEW_PACKET_READY_RESPONSE_PENDING
allowed outcomes = ACCEPT_CENTROID; ACCEPT_ENVELOPE; CARRY_INTERVAL; REJECT_Q_FREEZE
response_pending = true
formula_freeze_allowed = false
endpoint_scores_allowed = false
```

Bridge interpretation: the review obligation is now executable rather than
informal. The packet freezes allowed source inputs, forbidden inputs, and the
four admissible reviewer outcomes. It explicitly forbids `vobs`, rotation
residuals, endpoint scores, baseline RMSE, wrong-family rank, best-fit family,
and required-`S_tau` diagnostics. Packet creation alone still cannot freeze
`q_warp`, `sigma_warp`, or `epsilon_cross`; it only prepares the review
response needed for the next gate.

NGC7331 q-warp source-only review response:

```bash
python scripts/build_ngc7331_qwarp_source_only_review_response.py
```

Current status:

```text
NGC7331_QWARP_SOURCE_ONLY_REVIEW_RESPONSE_FILLED_INTERVAL_CARRIED
review_decision = CARRY_INTERVAL
q_warp_interval = [0.0079404475812108, 0.2057957876154617]
epsilon_cross_candidate_bound = 0.4885713979761795
formula_freeze_allowed_after_review = true
endpoint_scores_allowed = false
```

Bridge interpretation: the pending-response blocker is removed without
pretending that the centroid or envelope observable is uniquely selected. The
response carries the full residual-blind THINGS source-native `q_warp` interval
into the exact-transfer formula-freeze preparation. MOM1 supplies orientation
and cross-term context only; no `vobs`, residuals, endpoint scores, baseline
RMSE, wrong-family ranks, best-fit family, or required-`S_tau` diagnostics are
used.

NGC7331 q-warp observable-choice review intake:

```bash
python scripts/run_ngc7331_qwarp_observable_choice_review_intake.py
```

Current status:

```text
NGC7331_QWARP_REVIEW_INTAKE_FORMULA_FREEZE_INPUT_READY_NOT_ENDPOINT
response_pending = false
formula_freeze_allowed = true
endpoint_scores_allowed = false
```

Bridge interpretation: the intake validator is now present as an executable
gate. The source-only response passes the allowed-outcome, source-input,
forbidden-input, `q_warp` interval, sign-context, and `epsilon_cross` handling
checks. This promotes NGC7331 from response-pending to formula-freeze input
readiness, not to an endpoint result. The next gate must build the actual
exact-transfer formula freeze while carrying the `q_warp` interval and
`epsilon_cross` caveat; no NGC7331 endpoint score is allowed at intake level.

B2 source-load origin derivation gate:

```bash
python scripts/build_ngc4088_b2_source_load_origin_derivation_gate.py
```

Current status:

```text
SOURCE_LOAD_ORIGIN_PARTIALLY_GROUNDED_CARRIER_AND_CROSS_OPEN
Lambda_tau = 8795.111752 km^2/s^2
freeze alignment: true
pass-like gates: 4
formula-conditional gates: 1
conditional-carrier-theorem gates: 1
partial gates: 1
open/open-for-claims gates: 1
law_level_closed = false
```

Bridge interpretation: the source-load origin is no longer a single opaque
ansatz. Its freeze alignment, dimensions/limits, conditional stationarity, and
caveated onset-source acceptance pass. The sign/strength law is still
formula-conditional, `Vflat^2` carrier dominance has a frozen-protocol
conditional theorem, and the cross-term bound is partial: the sharp `B_i`
coefficient rule is ready, but the residual-blind `epsilon_cross` source-bound
inputs are not fully closed.

B3 scale-uniqueness resolution synthesis:

```bash
python scripts/build_ngc4088_b3_scale_uniqueness_resolution_synthesis.py
```

Current status:

```text
B3_CONDITIONAL_UNIQUE_SCALE_SELECTED_LAW_LEVEL_UNIQUENESS_OPEN
initial scales = 5 residual-blind dimensionally valid candidates
selected scale = CURRENT_XW_VFLAT2
conditional_uniqueness_resolved = true
law_level_uniqueness_resolved = false
formula_freeze_allowed_now = false
endpoint_scores_allowed = false
```

Bridge interpretation: B3 is no longer an unstructured ambiguity. Under the
frozen conditional rule, the current `x_w Vflat^2` scale is the only selected
scale. But this is protocol-level uniqueness, not final Tau-side law-level
uniqueness. The law-level result still depends on closing B2: the asymptotic
carrier theorem and the closure-functional derivation.

NGC4088 warp/history formula-freeze gate:

```bash
python scripts/build_ngc4088_warp_history_formula_freeze_gate.py
```

Current status:

```text
NGC4088_WARP_HISTORY_FORMULA_FREEZE_READY_LAW_CAVEATED_NOT_SCORE
B1 = B1_RESOLVED_CAVEATED_WHISP_GRAPHICAL_XW
B2 = B2_PROTOCOL_FORMULA_FREEZE_READY_LAW_LEVEL_OPEN
B3 = B3_PROTOCOL_UNIQUE_SCALE_SELECTED_LAW_LEVEL_OPEN
x_w = 0.298333
Vflat = 171.7 km/s
lambda_w = 8795.111752 km^2/s^2
p = 1 frozen linear onset branch
endpoint_scores_allowed = false
```

Bridge interpretation: the NGC4088 local formula-freeze gate is now closed at
protocol level, not at final law level. The frozen shell is

```text
v_readout^2(R)=v_Newtonian_baryonic^2(R)+lambda_w C_warp(R/R_HI;x_w,p)
C_warp(x;x_w,p)=q_warp max(0,(x-x_w)/(1-x_w))^p
lambda_w=sigma_warp q_warp x_w Vflat^2
```

with the caveated WHISP graphical-overview `x_w`, `q_warp=1`, positive
source-side warp/history sign, and the minimal linear onset branch `p=1`. The
quadratic `p=2` branch remains only a sensitivity/control branch. The dimension
check passes because `lambda_w` has velocity-squared units and `C_warp` is
dimensionless; the inactive-window and zero-source limits recover the baryonic
carrier. This is the first NGC4088 formula that can be carried into a separate
accepted-endpoint gate unchanged. It still does not authorize endpoint scoring:
B2's physical-normalization law and B3's law-level uniqueness remain open, and
the B1 WHISP graphical-overview provenance caveat must travel with the formula.

Consolidated NGC4088 formula-freeze readiness dashboard:

```bash
python scripts/build_ngc4088_formula_freeze_readiness_dashboard.py
```

Current status:

```text
NGC4088_FORMULA_FREEZE_READINESS_DASHBOARD_CREATED
B1 = B1_RESOLVED_CAVEATED_WHISP_GRAPHICAL_XW
B2 = B2_PROTOCOL_FORMULA_FREEZE_READY_LAW_LEVEL_OPEN
B3 = B3_PROTOCOL_UNIQUE_SCALE_SELECTED_LAW_LEVEL_OPEN
resolved local blockers = 3 / 3
formula_freeze_allowed_now = true
endpoint_scores_allowed = false
```

Bridge interpretation: the NGC4088 warp/history-coupled lane now has a frozen
prospective formula protocol rather than a vague open problem. The remaining
state is specific: it is ready for a separate accepted-endpoint gate, but not
yet for endpoint scoring or broad empirical claims. The next script must read
the frozen manifest unchanged and place any scoring in a separate endpoint
stage.

NGC4088 caveated accepted endpoint gate and score:

```bash
python scripts/build_ngc4088_warp_history_accepted_endpoint_gate.py
python scripts/run_ngc4088_warp_history_accepted_endpoint.py
```

Current status:

```text
CAVEATED_ACCEPTED_ENDPOINT_FREEZE_READY
CAVEATED_ACCEPTED_ENDPOINT_PRELIMINARY_CONTROL_RESULT
matched warp/history RMSE = 11.619038 km/s
best baseline = Newtonian, RMSE = 25.396289 km/s
wrong-family mean RMSE = 41.857935 km/s
best wrong-family RMSE = 37.869997 km/s
matched rank among all inspected models = 1
```

Bridge interpretation: this is the first NGC4088 endpoint score produced from
the unchanged frozen warp/history formula rather than from a diagnostic
sensitivity branch. It is a strong single-galaxy control signal: the matched
source-frozen warp/history readout beats Newtonian, TPG/v6, MOND, and the
inspected wrong-family Tau controls on the 12-point NGC4088 curve. The claim
boundary remains narrow. The result is caveated by the WHISP graphical-overview
`x_w`, formula-conditional B2 normalization, and protocol-level B3 uniqueness;
it is not a population validation and it does not close the remaining law-level
Tau-side derivations.

NGC4088 remaining-caveat action gate:

```bash
python scripts/build_ngc4088_remaining_caveat_action_gate.py
```

Current status:

```text
NGC4088_REMAINING_CAVEAT_ACTION_GATE_BUILT_NOT_ENDPOINT
endpoint ready:                         true
endpoint scored:                        true
matched RMSE:                           11.619038 km/s
best baseline RMSE:                     25.396289 km/s
B1 formula-freeze closed caveated:      true
B1 direct H I product cached:           false
B2 protocol ready, law-level open:      true
B3 protocol unique, law-level open:     true
endpoint scores allowed by this gate:   false
next recommended caveat action:         B2_SOURCE_LOAD_ORIGIN_AND_ASYMPTOTIC_CARRIER_DERIVATION
```

Bridge interpretation: this separates the good NGC4088 endpoint signal from the
remaining theory/provenance obligations. B1 is closed for formula freeze with a
WHISP graphical-overview provenance caveat; a direct source-coordinate H I
product would improve provenance but is no longer the primary endpoint blocker.
The primary theory action is B2. This has been sharpened: an explicit
conditional source-load functional now exists, and `Vflat^2` has a
frozen-protocol conditional carrier theorem. The remaining task is to derive the
Tau-side source-load origin, final forced carrier law, comparator autonomy,
population transfer, and cross-term bound that make
`lambda_w = sigma_warp q_warp x_w Vflat^2` internal rather than
formula-conditional. B3 law-level uniqueness then depends on that B2 derivation.

Four inspected endpoint/readout cases status:

```bash
python scripts/build_four_case_endpoint_status_summary.py
```

Current status:

```text
FOUR_INSPECTED_CASES_HETEROGENEOUS_PRELIMINARY_EVIDENCE
Inspected cases:                         4
Three-case mixed-readout packet:         3
Additional caveated endpoint:            1
Accepted single-galaxy endpoints:        3
Matched beats best local baseline:       4/4
Matched beats inspected wrong families:  4/4
Construction used vobs/residuals:        false
Scoring used vobs:                       true
```

Case structure:

```text
NGC4013, NGC5907, NGC7331:
    three-case mixed-readout control packet

NGC5907:
    accepted mixed single-galaxy endpoint inside the three-case packet

NGC7331:
    caveated accepted mixed single-galaxy endpoint inside the three-case packet

NGC4088:
    additional caveated warp/history accepted endpoint
```

Bridge interpretation: the package now contains four inspected cases, but this
must not be read as a uniform four-galaxy population validation. The result is
stronger than four isolated anecdotes because each inspected case compares a
source- or morphology-matched Tau Core readout against local baselines and
wrong-family controls. It is still heterogeneous preliminary evidence, but the
status is stronger now: NGC5907 has accepted mixed endpoint status, NGC7331 has
caveated accepted mixed endpoint status, NGC4088 has caveated accepted endpoint
status, and NGC4013 remains a retrospective frozen-reference row. The correct
bridge-level claim is readout-specificity evidence in four inspected cases,
with three accepted single-galaxy endpoint rows, not empirical validation of
Tau Core. NGC7331's accepted status must always carry the broad outer-window
caveat for the scored V1 row. The newer Bosma fractional-onset source gate
should be treated as a V2 replay/holdout input, not as a retroactive upgrade of
the existing NGC7331 endpoint score.

Four-case caveat reduction audit:

```bash
python scripts/build_four_case_caveat_reduction_audit.py
```

Current caveat-reduction status:

```text
FOUR_CASE_CAVEAT_REDUCTION_AUDIT_COMPLETE
Cases audited:                         4
Caveats reduced:                       3
Caveats isolated but not removed:      1
Sharpened replay specificity pass:     true
Endpoint statuses changed:             false
Endpoint scores recomputed:            false
Population validation claim:           false
```

Case-level reading:

```text
NGC4013: retrospective caveat isolated, not removed.
NGC5907: prior-projection caveat reduced to control context.
NGC7331: broad-window caveat reduced for V2/V3 replay, not retroactive V1.
NGC4088: B1 provenance caveat reduced; B2/B3 law-level caveats remain.
```

Bridge interpretation: the caveats are now sharper and smaller, but not erased.
The main improvement is that the NGC7331 broad-window problem has a
fractional-onset/source-sharpened replay path, NGC5907's prior projection
endpoint is explicitly excluded as mixed evidence, and NGC4088's B1 source
scale is accepted for formula freeze with a WHISP graphical provenance caveat.
NGC4013 still needs a predeclared replay/holdout lane or a future analogous
source-selected case before its retrospective caveat can be reduced.

NGC4013 retrospective-caveat closure gate:

```bash
python scripts/build_ngc4013_retrospective_caveat_closure_gate.py
```

Current status:

```text
NGC4013_RETROSPECTIVE_CAVEAT_CLOSURE_PATH_FORMALIZED_NOT_CLOSED
source rule transferable:                 true
formula freeze transferable:              true
control signal recorded:                  true
retrospective endpoint score forbidden:   true
exact non-NGC4013 analogue ready count:   0
nearest analogue candidate:               NGC4088
nearest analogue freeze allowed now:      false
endpoint statuses changed:                false
endpoint scores recomputed:               false
endpoint scores allowed:                  false
uses vobs/residual:                       false
```

Bridge interpretation: this gate reduces the NGC4013 caveat by making it
operational, not by removing it. The source rule and frozen formula can be
transferred to future use, and the control signal remains recorded. However,
the existing NGC4013 score is still forbidden as accepted endpoint evidence
because the mixed lane was developed after the relevant control context had
already been inspected. The current package has no exact non-NGC4013 analogue
with the same source-rule readiness. NGC4088 is the nearest source-bound
analogue, but it is a warp/history lane rather than the same expdisk plus
warp/vertical-overlay protocol and is not freeze-allowed in this gate.
Therefore the closure path is now explicit: use a predeclared replay/holdout
lane or a future source-selected analogue; do not relabel the retrospective
score.

NGC4013 predeclared replay/holdout gate:

```bash
python scripts/build_ngc4013_predeclared_replay_holdout_gate.py
```

Current status:

```text
NGC4013_PREDECLARED_REPLAY_HOLDOUT_GATE_BUILT_ENDPOINT_STILL_BLOCKED
source rule transferable:              true
formula manifest transferable:         true
prospective endpoint protocol ready:   true
existing score quarantined:            true
same-curve replay allowed:             false
future holdout route defined:          true
future analogue route defined:         true
exact non-NGC4013 analogue ready count: 0
endpoint scores allowed:               false
endpoint scores recomputed:            false
uses vobs/residual:                    false
next required gate:                    FUTURE_UNINSPECTED_HOLDOUT_OR_SOURCE_SELECTED_ANALOGUE
```

Route interpretation:

```text
R1_SAME_CURVE_REPLAY:
    blocked, because the existing NGC4013 curve and controls were already inspected.

R2_PREDECLARED_NEW_HOLDOUT:
    future-only, requiring an uninspected NGC4013-compatible holdout target or data release.

R3_SOURCE_SELECTED_ANALOGUE:
    blocked until an exact non-NGC4013 expdisk+WVO source-selected analogue is promoted.

R4_POPULATION_REPLAY:
    future-only as one member of a predeclared source-selected population packet.
```

Bridge interpretation: the NGC4013 caveat is now narrower but still not
closed. The source rule and mixed expdisk+warp/vertical-overlay formula can be
transferred, but the old score is quarantined. A same-curve replay is not an
accepted endpoint route. This turns the vague retrospective caveat into an
explicit future-data requirement.

Remaining caveat closure roadmap:

```bash
python scripts/build_remaining_caveat_closure_roadmap.py
```

Current status:

```text
REMAINING_CAVEAT_CLOSURE_ROADMAP_UPDATED_AFTER_NGC4088_ACTION_GATE_NOT_ENDPOINT
Cases ranked:                         4
Replay-ready without new source:      0
Replay completed without V1 update:   1
Predeclared replay gates built:        1
Remaining caveat action gates built:   1
Retrospective/population blocked:     3
Source or law blocked:                0
Endpoint statuses changed:            false
Endpoint scores recomputed:           false
Endpoint scores allowed:              false
Uses vobs/residual:                   false
Uses replay endpoint summary:         true
Uses predeclared replay gate summary: true
Uses remaining caveat action summary: true
V1 endpoint updated:                  false
Next recommended gate:                B2_SOURCE_LOAD_ORIGIN_AND_ASYMPTOTIC_CARRIER_DERIVATION_FOR_NGC4088
```

Roadmap interpretation:

```text
P1_SOURCE_AND_THEORY:
    NGC4088 B2 source-load-origin/asymptotic-carrier derivation.
    B1 direct H I product is now a provenance upgrade, not the primary blocker.

P2_POPULATION_SCALE:
    NGC4013 replay gate is built; reduce only with future uninspected holdout data or an exact analogue.
    NGC5907 remains locally accepted; reduce only by adding more fresh analogues.
    NGC7331 V2/V3 replay is completed for the replay path, but V1 remains unchanged.
```

Bridge interpretation: the NGC7331 replay path, NGC4013 predeclared replay
gate, and NGC4088 remaining-caveat action gate have all been built. NGC4088 is
already a caveated accepted single-galaxy control endpoint. The next scientific
action is no longer another endpoint score; it is the B2 law-level derivation
that would internalize the warp/history normalization. B3 law-level uniqueness
then follows as the dependent caveat.

NGC7331 V2/V3 replay/holdout endpoint:

```bash
python scripts/run_ngc7331_v2_v3_replay_holdout_endpoint.py
```

Current status:

```text
NGC7331_V2_V3_REPLAY_HOLDOUT_PRELIMINARY_CONTROL_RESULT
V1 accepted-reference RMSE:            22.255666 km/s
V2 fractional-onset replay RMSE:       22.732383 km/s
V3 source-sharpened replay RMSE:       22.130849 km/s
Best baseline RMSE:                    23.472977 km/s
Wrong projection-sharpened RMSE:       22.906398 km/s
V3 beats V1 reference:                 true
V3 beats V2 fractional onset:          true
V3 beats best baseline:                true
V3 beats wrong projection control:     true
Current V1 endpoint updated:           false
Construction used vobs/residual:       false
Scoring used vobs:                     true
```

Bridge interpretation: this is the replay gate recommended by the remaining
caveat roadmap. It reduces the NGC7331 broad-window caveat for the replay path:
the V3 source-sharpened row beats the V1 accepted reference, the V2 fractional
onset row, the best local baseline, and the wrong sharpened projection control.
It does not rewrite the V1 accepted endpoint. The result remains a
single-galaxy replay/holdout control, not population validation.
