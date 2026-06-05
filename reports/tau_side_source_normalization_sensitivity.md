# Tau-Side Source-Normalization Sensitivity Audit

This audit varies only the theory-gated orientation signs and
source-evidence gates. It does not choose a winning variant and it does
not promote the normalization rule to an accepted Tau-side law.

## Primary Holdout Reference

- Beats old L2 intake endpoint: 0.568
- Beats TPG/v6: 0.455
- Beats MOND: 0.545
- Median minus old L2 RMSE: -0.271648

## Variant Manifest

| variant_id | variant_role | proxy_gate | missing_gate | sign_K_compact_finite | sign_K_scale_tail_spiral | sign_K_exponential_disk | sign_K_thick_flared | selection_policy | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| primary_proxy_gate_0p35 | primary_formula_conditional_candidate_from_derivation_manifest | 0.35 | 0 | 1 | 1 | -1 | -1 | predeclared_sensitivity_audit_not_endpoint_selection | tau_side_source_normalization_sensitivity_not_model_selection |
| no_proxy_gate_0p00 | accepted_source_only_control | 0 | 0 | 1 | 1 | -1 | -1 | predeclared_sensitivity_audit_not_endpoint_selection | tau_side_source_normalization_sensitivity_not_model_selection |
| weak_proxy_gate_0p20 | proxy_gate_sensitivity | 0.2 | 0 | 1 | 1 | -1 | -1 | predeclared_sensitivity_audit_not_endpoint_selection | tau_side_source_normalization_sensitivity_not_model_selection |
| strong_proxy_gate_0p50 | proxy_gate_sensitivity | 0.5 | 0 | 1 | 1 | -1 | -1 | predeclared_sensitivity_audit_not_endpoint_selection | tau_side_source_normalization_sensitivity_not_model_selection |
| full_proxy_gate_1p00 | proxy_gate_stress_control | 1 | 0 | 1 | 1 | -1 | -1 | predeclared_sensitivity_audit_not_endpoint_selection | tau_side_source_normalization_sensitivity_not_model_selection |
| all_positive_orientation | orientation_control | 0.35 | 0 | 1 | 1 | 1 | 1 | predeclared_sensitivity_audit_not_endpoint_selection | tau_side_source_normalization_sensitivity_not_model_selection |
| all_negative_orientation | orientation_control | 0.35 | 0 | -1 | -1 | -1 | -1 | predeclared_sensitivity_audit_not_endpoint_selection | tau_side_source_normalization_sensitivity_not_model_selection |

## Holdout Sensitivity

| variant_id | beats_old_l2_intake_fraction | beats_tpg_v6_fraction | beats_mond_fraction | median_source_norm_minus_old_l2_intake | median_source_norm_minus_tpg_v6 | median_source_norm_minus_mond |
| --- | --- | --- | --- | --- | --- | --- |
| primary_proxy_gate_0p35 | 0.568182 | 0.454545 | 0.545455 | -0.271648 | 0.0698845 | -0.316241 |
| no_proxy_gate_0p00 | 0.545455 | 0.454545 | 0.5 | -0.416748 | 0.391237 | 0.0548854 |
| weak_proxy_gate_0p20 | 0.590909 | 0.454545 | 0.522727 | -0.310527 | 0.204009 | -0.136131 |
| strong_proxy_gate_0p50 | 0.545455 | 0.477273 | 0.545455 | -0.224024 | 0.00446002 | -0.407338 |
| full_proxy_gate_1p00 | 0.522727 | 0.522727 | 0.522727 | -0.287445 | -0.0187676 | -0.141904 |
| all_positive_orientation | 0.477273 | 0.409091 | 0.454545 | 0.317625 | 1.39572 | 0.426505 |
| all_negative_orientation | 0.431818 | 0.363636 | 0.454545 | 1.15116 | 1.9974 | 2.54776 |

## Claim Boundary

The sensitivity table is an audit of the weakest conditional step. A
better-looking variant must not be selected for the paper endpoint unless
its signs and gates are independently derived before endpoint scoring.
