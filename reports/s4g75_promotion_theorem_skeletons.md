# S4G75 Promotion Theorem Skeletons

These are conditional theorem skeletons for the three S4G75 promotion gates. They are not endpoint results and not full physical proofs. They state the minimal corrected claims needed before conditional kernel rows can become strict kernel-ready rows.

## Verdict

All three promotion claims are conditional. The conclusion follows only after the missing source-support assumption or Tau-side promotion theorem is supplied. Endpoint improvement cannot supply that missing assumption.

## Theorem Skeletons

| theorem_id | promotion_gate | formula_family | minimal_corrected_statement | proof_status | verdict | weakest_step |
| --- | --- | --- | --- | --- | --- | --- |
| TAIL-HI-EXTENT-PROMOTION-LEMMA-001 | TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION | K_scale_tail_spiral | R_HI can be promoted to a scale-tail cutoff only under a predeclared transition/support rule; generic HI extent alone is partial support, not strict kernel readiness. | CONDITIONAL_INCOMPLETE | Plausible but not proven for endpoint use | Showing that R_HI constrains the same outer-disk transition kernel rather than merely bounding generic gas extent. |
| COMPACT-SUPPORT-PROMOTION-LEMMA-001 | COMPACT-COMPONENT-SUPPORT-PROMOTION | K_compact_finite | A compact component radius can promote the compact kernel if it constrains compact support; Reff alone is conditional unless a support theorem maps it to the compact component. | CONDITIONAL_INCOMPLETE | Definition-level proof after support evidence; incomplete for Reff-only rows | Proving that Reff or a listed component is the compact support used by F_compact, rather than a global half-light proxy. |
| EDGE-DISK-VERTICAL-PROMOTION-LEMMA-001 | EDGE-DISK-TO-VERTICAL-KERNEL-PROMOTION | K_thick_flared | Edge-disk evidence can promote thick/flared only when it constrains the vertical kernel parameter; an edge-on label or inclination proxy alone is not strict kernel readiness. | CONDITIONAL_INCOMPLETE | Plausible for direct h/Rs or flare measurements; incomplete for component-label-only evidence | Showing that edge-disk/component evidence yields a measured or bounded vertical kernel parameter rather than only a projection caveat. |

## Formal Claims

### TAIL-HI-EXTENT-PROMOTION-LEMMA-001

**Formal claim**

Let R_HI be a residual-blind source-native gas-extent observable. Let F_tail use kernel parameters R_tail_in and R_tail_cut. If a fixed residual-blind transition rule maps R_HI and disk-scale source data to R_tail_in and R_tail_cut, and if R_tail_cut constrains the same outer-disk/tail support class used by F_tail, then the HI extent proxy is admissible as a conditional scale-tail kernel observable.

**Proof sketch**

By definition, strict kernel readiness requires source evidence for the actual kernel observable. If a predeclared rule fixes R_tail_cut from R_HI and proves support compatibility with the tail kernel, then the source constrains F_tail's cutoff parameter. Without support compatibility, R_HI remains only a proxy.

**Hidden assumptions**

monotone outer support; no endpoint-selected transition constant; R_HI is measured consistently across galaxies; gas extent is a valid readout support proxy for the stellar/morphological tail

**Edge cases**

gas disk extends beyond stellar tail; disturbed HI without a stellar tail; compact HI cutoff but broad stellar tail; low inclination or distance uncertainty

### COMPACT-SUPPORT-PROMOTION-LEMMA-001

**Formal claim**

Let R_c be a residual-blind compact component support observable from a source-native decomposition. Let F_compact use a finite compact support kernel. If R_c bounds or represents the compact component support used by the kernel, with the bound selected before endpoint scoring, then R_c is admissible as a strict compact finite-source kernel observable.

**Proof sketch**

The compact kernel is finite-source by construction. If a residual-blind source provides the support radius or a proven bound for that finite source, then the same source constrains the kernel parameter. If only Reff exists, the conclusion requires an additional theorem connecting Reff to compact support.

**Hidden assumptions**

decomposition separates compact and disk components; component radius has stable physical meaning; compact support radius is not chosen from rotation residuals

**Edge cases**

bar radius confused with compact support; diffuse bulge; no component radius; Reff dominated by disk light; multi-component central structure

### EDGE-DISK-VERTICAL-PROMOTION-LEMMA-001

**Formal claim**

Let E_Z be a residual-blind edge-disk or vertical-structure source observable. Let F_thick use a vertical kernel parameter h/Rs, flare radius, warp radius, or gas-plane thickness. If E_Z provides a measured value or fixed conservative bound for that vertical kernel parameter, independent of endpoint residuals, then E_Z is admissible as a conditional thick/flared kernel observable.

**Proof sketch**

The thick/flared formula uses a vertical geometry parameter. If source evidence fixes or bounds that same parameter, the source constrains the kernel. If the source only says edge-disk or high inclination, the evidence marks a review caveat but does not yet supply the kernel observable.

**Hidden assumptions**

vertical component is physically tied to the solved readout kernel; h/Rs or flare bounds are residual-blind; projection effects are not mistaken for thickness

**Edge cases**

edge-on projection without thick disk; warp misread as flare; gas-plane thickness differs from stellar thickness; uncertain inclination; multiple vertical components

## Assumption Audit

| promotion_gate | assumption_id | assumption | status | claim_boundary |
| --- | --- | --- | --- | --- |
| TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION | T1 | R_HI is measured residual-blind and not selected from endpoint residuals. | DATA_DEPENDENT | s4g75_promotion_theorem_skeletons_not_endpoint |
| TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION | T2 | A fixed transition rule maps R_HI and disk scale to R_tail_in and R_tail_cut. | THEOREM_OR_PROTOCOL_REQUIRED | s4g75_promotion_theorem_skeletons_not_endpoint |
| TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION | T3 | The mapped cutoff constrains the same outer-disk/tail support class used by F_tail. | WEAKEST_STEP | s4g75_promotion_theorem_skeletons_not_endpoint |
| COMPACT-COMPONENT-SUPPORT-PROMOTION | C1 | A source-native component decomposition identifies a compact component. | DATA_DEPENDENT | s4g75_promotion_theorem_skeletons_not_endpoint |
| COMPACT-COMPONENT-SUPPORT-PROMOTION | C2 | A compact support radius or bound is available before endpoint scoring. | DATA_OR_THEOREM_REQUIRED | s4g75_promotion_theorem_skeletons_not_endpoint |
| COMPACT-COMPONENT-SUPPORT-PROMOTION | C3 | Reff is not used as compact support unless a support theorem justifies the map. | CLAIM_BOUNDARY_RULE | s4g75_promotion_theorem_skeletons_not_endpoint |
| EDGE-DISK-TO-VERTICAL-KERNEL-PROMOTION | V1 | The source identifies vertical structure rather than only projection or inclination. | DATA_DEPENDENT | s4g75_promotion_theorem_skeletons_not_endpoint |
| EDGE-DISK-TO-VERTICAL-KERNEL-PROMOTION | V2 | A measured or bounded h/Rs, flare, warp, or gas-plane thickness parameter is supplied. | DATA_OR_THEOREM_REQUIRED | s4g75_promotion_theorem_skeletons_not_endpoint |
| EDGE-DISK-TO-VERTICAL-KERNEL-PROMOTION | V3 | Projection effects are not promoted to vertical kernel parameters without a theorem. | CLAIM_BOUNDARY_RULE | s4g75_promotion_theorem_skeletons_not_endpoint |

## Waiting Conditional Rows

| promotion_gate | formula_family | n_waiting_galaxies | waiting_galaxies | source_priorities | theorem_id | proof_status | weakest_step | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION | K_scale_tail_spiral | 6 | NGC4214;UGC06917;UGC06983;UGC00891;UGC04499;UGC05829 | P0_DIRECT_SOURCE_NATIVE_REQUIRED;P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | TAIL-HI-EXTENT-PROMOTION-LEMMA-001 | CONDITIONAL_INCOMPLETE | Showing that R_HI constrains the same outer-disk transition kernel rather than merely bounding generic gas extent. | s4g75_promotion_theorem_skeletons_not_endpoint |

## Claim Boundary

These theorem skeletons do not prove that the S4G75 conditional rows are endpoint-eligible. They define what must be proven or measured before promotion. The corrected claim is: source-rich proxy rows become strict kernel-ready rows only when the source constrains the same kernel observable used by the formula family, or when a residual-blind Tau-side theorem proves that the proxy is an admissible representative of that kernel.
