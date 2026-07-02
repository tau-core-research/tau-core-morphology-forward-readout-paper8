# Paper 8 KernelRecord Status Audit

**Doc class:** paper-level kernel status audit
**Reader role:** reproducibility / claim-boundary reviewer
**Status:** audit map only; not endpoint scoring; not validation
**Canonical theory schema:** `KernelRecord_tau^S`

This report maps the Paper 8 morphology-forward readout kernels onto the
current Tau Core kernel discipline:

```text
diagnostic/control
-> source-proxy kernel
-> source-factored Tau kernel candidate
-> endpoint-active frozen kernel
-> validated physical readout
```

No row below is promoted to `validated physical readout`.  The strongest Paper
8 results remain endpoint-active or caveated single-object control endpoints.

## Population and Triage Kernels

| kernel / lane | sector | status | source quotient | source support and overlap policy | composition policy | validation boundary |
| --- | --- | --- | --- | --- | --- | --- |
| 175-galaxy morphology manifest / triage | galaxy gravity readout | source-proxy triage | `Q_src^P` from available morphology metadata | residual-blind labels; incomplete source morphology; no true-negative closure | label-to-family selection only | triage / preparation evidence, not endpoint validation |
| 44-galaxy holdout matched Tau-proxy endpoint | galaxy gravity readout | source-proxy preflight | `Q_src^P`; proxy families built from available `rparent_cd` channel | train/holdout split and shuffled-label null preserve leakage boundary | train-only family amplitudes around frozen proxy carrier | internal-preflight signal; not final Tau Core formula validation |
| quality-gate endpoint decision matrix | galaxy gravity readout | endpoint decision aid | same as above | records tradeoff between shuffled-null support and baseline flags | does not create a new kernel | protocol decision aid, not empirical validation |

## Object-Specific Endpoint-Active Kernels

| galaxy / kernel | status | source quotient | source support | overlap / double-count policy | endpoint result role | validation boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4088 warp/history accepted route | caveated endpoint-active frozen kernel | `Q_src^P` source-frozen warp/history morphology | warp/history/asymmetry source manifest; no residual construction | additive route only; clock/path additions require non-overlap evidence | strong single-galaxy preliminary control endpoint; beats listed baselines and wrong families in the stored run | not population validation; law-level and source-review caveats remain |
| NGC5907 projection accepted route | endpoint-active frozen projection kernel | `Q_src^P` projection/edge-on source manifest | projection attenuation and vertical/path context | source-frozen formula read from accepted manifest | accepted single-galaxy preliminary control endpoint | not universal physical validation |
| NGC7331 mixed exponential/vertical/outer-warp route | caveated accepted mixed endpoint | `Q_src^P` mixed morphology/projection support | exponential disk plus broad vertical/outer-warp support | mixed composition allowed only under frozen manifest | useful accepted mixed object endpoint | broad-window outer-warp caveat remains |
| NGC4013 warp/vertical-overlay route | caveated mixed/projection candidate | `Q_src^P` incomplete mixed support | warp plus vertical-overlay evidence; previously best wrong-family controls close | mixed replay / proof-of-concept | useful kernel-development case | not fresh independent holdout validation |

## Controls and Negative Results

| artifact class | status | required treatment |
| --- | --- | --- |
| wrong-family controls | control kernels | preserved as specificity controls; no demotion of Tau Core from a single wrong-family win unless source-complete matched route was frozen |
| shuffled morphology labels | null controls | used to test label-specificity; not physical validation |
| weak negatives / morphology-underdetermined cases | caveated negative controls | retained as underdetermined unless source-complete morphology, frozen matched family, and endpoint replay all fail |
| branch-level negatives | diagnostic/control | may reject a pure branch, not the whole morphology-readout framework |

## KernelRecord Verdict

Paper 8 currently supports this status:

```text
PAPER8_MORPHOLOGY_FORWARD_READOUT =
    source-proxy and endpoint-active preflight program
    with several caveated single-object endpoint kernels,
    no validated physical readout,
    no source-complete true negative yet.
```

The correct next promotion route is not to fit residuals, but to fill
`KernelRecord_tau^S` fields for each object:

```text
source_quotient
SourceSupp(Delta K_a)
overlap_decision
Compose_S
forbidden_input_policy
endpoint_protocol
controls
negative_result_record
```

Only after these are frozen before scoring can a Paper 8 kernel move beyond
source-proxy preflight into validation-oriented endpoint status.
