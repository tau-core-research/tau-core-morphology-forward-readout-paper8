# Inclusion-Lane Endpoint Analysis

This analysis slices existing score tables by the strict/caution/acquisition
lanes. It does not select a new endpoint, does not tune a model, and does
not turn caution rows into accepted evidence.

## Holdout Strict+Caution Reading

- Tau evidence L2 rows: 16
- Tau evidence L2 beats TPG/v6: 0.375
- Tau evidence L2 beats MOND: 0.312
- Tau evidence L2 median minus TPG/v6 RMSE: 1.46329
- Tau evidence L2 median minus MOND RMSE: 2.27317
- Source-native hard-family rows: 16
- Source-native hard-family beats wrong mean: 0.812
- Source-native hard-family beats TPG/v6: 0.500
- Source-native hard-family beats MOND: 0.438

The strict+caution lane increases usable holdout coverage to the
orientation-ready rows, but remains a support lane. Baseline comparison
numbers from this lane are diagnostic, not validation.

## Caution Sub-Lanes

The caution lane is not homogeneous. Projection-caveated and
memory-history-proxy rows are reported separately so that weak baseline
behavior is not hidden inside a single support bucket.

| score_layer | split | inclusion_lane | allowed_use | n_galaxies | median_rmse_prediction | median_minus_wrong_mean | median_minus_tpg_v6 | median_minus_mond | beats_wrong_fraction | beats_tpg_v6_fraction | beats_mond_fraction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_native_hard_family | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 2 | 11.0235 | -42.10621338905556 | 2.50713 | 2.15304 | 1.0 | 0.5 | 0 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 14 | 25.5511 | -12.27650246743915 | 0.0526969 | -0.834653 | 0.7857142857142857 | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |

| score_layer | split | inclusion_lane | allowed_use | n_galaxies | median_rmse_prediction | median_minus_wrong_mean | median_minus_tpg_v6 | median_minus_mond | beats_wrong_fraction | beats_tpg_v6_fraction | beats_mond_fraction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tau_side_evidence_measure_l2 | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 2 | 8.69049 | <NA> | 0.174162 | -0.179931 | <NA> | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 14 | 29.8864 | <NA> | 3.14572 | 2.2821 | <NA> | 0.357143 | 0.285714 | inclusion_lane_endpoint_analysis_not_validation |

## Summary

| score_layer | split | inclusion_lane | n_galaxies | median_rmse_prediction | median_minus_wrong_mean | median_minus_tpg_v6 | median_minus_mond | beats_wrong_fraction | beats_tpg_v6_fraction | beats_mond_fraction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | holdout | ACQUISITION_REQUIRED | 28 | 11.7761 | 0.09170266491027139 | 0.1449 | -0.41503 | 0.4642857142857143 | 0.428571 | 0.607143 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | holdout | ALL_ROWS | 44 | 14.0213 | -0.0012605214126067028 | 0.136226 | -0.41503 | 0.5 | 0.477273 | 0.590909 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | holdout | CAUTION_READY_PROXY_SUPPORTED | 16 | 22.9765 | -0.9046002663938122 | -0.741973 | -0.332644 | 0.5625 | 0.5625 | 0.5625 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | holdout | STRICT_PLUS_CAUTION | 16 | 22.9765 | -0.9046002663938122 | -0.741973 | -0.332644 | 0.5625 | 0.5625 | 0.5625 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | train | ACQUISITION_REQUIRED | 80 | 10.1629 | -0.22439932488089995 | -0.0606961 | -0.195062 | 0.5875 | 0.525 | 0.525 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | train | ALL_ROWS | 131 | 12.0521 | -0.1610408632889974 | -0.00475567 | -0.0827949 | 0.5725190839694656 | 0.503817 | 0.519084 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | train | CAUTION_READY_PROXY_SUPPORTED | 50 | 16.3303 | -0.0962556513991685 | 0.0201829 | 0.0736433 | 0.56 | 0.48 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | train | STRICT_PLUS_CAUTION | 51 | 16.4169 | -0.0759459658356362 | 0.0309536 | -0.0131747 | 0.5490196078431373 | 0.470588 | 0.509804 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | train | STRICT_READY_CANDIDATE | 1 | 35.4156 | 0.0040084188067623 | 0.334591 | -2.87421 | 0.0 | 0 | 1 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | holdout | ACQUISITION_REQUIRED | 28 | 11.4619 | -13.784893510161018 | 1.02725 | 0.03146 | 0.9285714285714286 | 0.464286 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | holdout | ALL_ROWS | 44 | 15.3531 | -13.974199559618807 | 0.644948 | 0.173401 | 0.8863636363636364 | 0.477273 | 0.477273 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | holdout | CAUTION_READY_PROXY_SUPPORTED | 16 | 22.9449 | -13.974199559618807 | 0.0526969 | 0.217324 | 0.8125 | 0.5 | 0.4375 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | holdout | STRICT_PLUS_CAUTION | 16 | 22.9449 | -13.974199559618807 | 0.0526969 | 0.217324 | 0.8125 | 0.5 | 0.4375 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | train | ACQUISITION_REQUIRED | 80 | 10.4547 | -15.867050207546441 | 0.378257 | 0.411284 | 0.9375 | 0.4625 | 0.4375 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | train | ALL_ROWS | 131 | 13.1754 | -11.122740256969614 | 0.226571 | 0.331001 | 0.8702290076335878 | 0.450382 | 0.458015 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | train | CAUTION_READY_PROXY_SUPPORTED | 50 | 18.4661 | -4.279999087527054 | 0.168944 | 0.0658245 | 0.76 | 0.42 | 0.48 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | train | STRICT_PLUS_CAUTION | 51 | 19.2659 | -4.3494822678215 | 0.111317 | 0.0398529 | 0.7647058823529411 | 0.431373 | 0.490196 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | train | STRICT_READY_CANDIDATE | 1 | 31.4042 | -6.752959116046792 | -3.67678 | -6.88558 | 1.0 | 1 | 1 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | holdout | ACQUISITION_REQUIRED | 28 | 12.9694 | <NA> | 0.111816 | 0.866016 | <NA> | 0.5 | 0.428571 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | holdout | ALL_ROWS | 44 | 15.3602 | <NA> | 0.111816 | 0.298487 | <NA> | 0.5 | 0.454545 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | holdout | CAUTION_READY_PROXY_SUPPORTED | 16 | 24.4876 | <NA> | 0.41515 | -0.0292532 | <NA> | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | holdout | STRICT_PLUS_CAUTION | 16 | 24.4876 | <NA> | 0.41515 | -0.0292532 | <NA> | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | train | ACQUISITION_REQUIRED | 80 | 12.0155 | <NA> | 0.374592 | 0.104249 | <NA> | 0.425 | 0.4875 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | train | ALL_ROWS | 131 | 14.5375 | <NA> | 0.40461 | 0.20171 | <NA> | 0.419847 | 0.458015 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | train | CAUTION_READY_PROXY_SUPPORTED | 50 | 19.4701 | <NA> | 0.615106 | 0.558253 | <NA> | 0.4 | 0.4 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | train | STRICT_PLUS_CAUTION | 51 | 19.6403 | <NA> | 0.428583 | 0.511516 | <NA> | 0.411765 | 0.411765 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | train | STRICT_READY_CANDIDATE | 1 | 32.7393 | <NA> | -2.34171 | -5.55051 | <NA> | 1 | 1 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | holdout | ACQUISITION_REQUIRED | 28 | 12.5133 | -4.323680768849266 | 0.124458 | -0.950214 | 0.8214285714285714 | 0.464286 | 0.678571 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | holdout | ALL_ROWS | 44 | 13.2154 | -5.470945659132824 | 0.124458 | -0.950214 | 0.8181818181818182 | 0.477273 | 0.613636 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | holdout | CAUTION_READY_PROXY_SUPPORTED | 16 | 22.5946 | -5.629327810610777 | 0.0477035 | -0.440967 | 0.8125 | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | holdout | STRICT_PLUS_CAUTION | 16 | 22.5946 | -5.629327810610777 | 0.0477035 | -0.440967 | 0.8125 | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | train | ACQUISITION_REQUIRED | 80 | 10.4093 | -5.742542358552787 | 0.00149686 | -0.837772 | 0.875 | 0.5 | 0.575 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | train | ALL_ROWS | 131 | 12.4957 | -3.5413550841611077 | 0.033531 | -0.693044 | 0.8015267175572519 | 0.480916 | 0.580153 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | train | CAUTION_READY_PROXY_SUPPORTED | 50 | 17.4835 | -2.390986219728916 | 0.0621961 | -0.541446 | 0.68 | 0.44 | 0.58 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | train | STRICT_PLUS_CAUTION | 51 | 17.5386 | -2.454735691577909 | 0.057508 | -0.56105 | 0.6862745098039216 | 0.45098 | 0.588235 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | train | STRICT_READY_CANDIDATE | 1 | 32.9465 | -3.0918713026056466 | -2.13449 | -5.3433 | 1.0 | 1 | 1 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | holdout | ACQUISITION_REQUIRED | 28 | 11.4619 | -13.784893510161018 | 1.02725 | 0.03146 | 0.9285714285714286 | 0.464286 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | holdout | ALL_ROWS | 44 | 15.3531 | -13.974199559618807 | 0.644948 | 0.173401 | 0.8863636363636364 | 0.477273 | 0.477273 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | holdout | CAUTION_READY_PROXY_SUPPORTED | 16 | 22.9449 | -13.974199559618807 | 0.0526969 | 0.217324 | 0.8125 | 0.5 | 0.4375 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | holdout | STRICT_PLUS_CAUTION | 16 | 22.9449 | -13.974199559618807 | 0.0526969 | 0.217324 | 0.8125 | 0.5 | 0.4375 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | train | ACQUISITION_REQUIRED | 80 | 10.4547 | -15.867050207546441 | 0.378257 | 0.411284 | 0.9375 | 0.4625 | 0.4375 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | train | ALL_ROWS | 131 | 13.1754 | -11.122740256969614 | 0.226571 | 0.331001 | 0.8702290076335878 | 0.450382 | 0.458015 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | train | CAUTION_READY_PROXY_SUPPORTED | 50 | 18.4661 | -4.279999087527054 | 0.168944 | 0.0658245 | 0.76 | 0.42 | 0.48 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | train | STRICT_PLUS_CAUTION | 51 | 19.2659 | -4.3494822678215 | 0.111317 | 0.0398529 | 0.7647058823529411 | 0.431373 | 0.490196 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | train | STRICT_READY_CANDIDATE | 1 | 31.4042 | -6.752959116046792 | -3.67678 | -6.88558 | 1.0 | 1 | 1 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | holdout | ACQUISITION_REQUIRED | 28 | 11.9367 | <NA> | -0.0785966 | -0.565514 | <NA> | 0.5 | 0.678571 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | holdout | ALL_ROWS | 44 | 14.1102 | <NA> | 0.0663734 | -0.25148 | <NA> | 0.454545 | 0.545455 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | holdout | CAUTION_READY_PROXY_SUPPORTED | 16 | 26.2302 | <NA> | 1.46329 | 2.27317 | <NA> | 0.375 | 0.3125 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | holdout | STRICT_PLUS_CAUTION | 16 | 26.2302 | <NA> | 1.46329 | 2.27317 | <NA> | 0.375 | 0.3125 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | train | ACQUISITION_REQUIRED | 80 | 10.1709 | <NA> | -0.0369305 | -0.463469 | <NA> | 0.5125 | 0.575 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | train | ALL_ROWS | 131 | 11.7901 | <NA> | 0.220372 | 0.114766 | <NA> | 0.458015 | 0.48855 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | train | CAUTION_READY_PROXY_SUPPORTED | 50 | 17.4472 | <NA> | 1.16253 | 1.00781 | <NA> | 0.38 | 0.36 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | train | STRICT_PLUS_CAUTION | 51 | 17.7618 | <NA> | 1.1774 | 1.04131 | <NA> | 0.372549 | 0.352941 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | train | STRICT_READY_CANDIDATE | 1 | 51.2973 | <NA> | 16.2164 | 13.0075 | <NA> | 0 | 0 | inclusion_lane_endpoint_analysis_not_validation |

## Allowed-Use Summary

| score_layer | split | inclusion_lane | allowed_use | n_galaxies | median_rmse_prediction | median_minus_wrong_mean | median_minus_tpg_v6 | median_minus_mond | beats_wrong_fraction | beats_tpg_v6_fraction | beats_mond_fraction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | holdout | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 28 | 11.7761 | 0.09170266491027139 | 0.1449 | -0.41503 | 0.4642857142857143 | 0.428571 | 0.607143 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 2 | 8.68506 | 0.10514935949541959 | 0.168733 | -0.185361 | 0.5 | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 14 | 26.03 | -0.9421594445415304 | -0.775789 | -0.332644 | 0.5714285714285714 | 0.571429 | 0.571429 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | train | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 80 | 10.1629 | -0.22439932488089995 | -0.0606961 | -0.195062 | 0.5875 | 0.525 | 0.525 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | train | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 17 | 14.5079 | -0.211839767471881 | -0.101149 | 0.529982 | 0.7058823529411765 | 0.529412 | 0.352941 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | train | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 33 | 21.2213 | 0.0054231985904831 | 0.322392 | -0.298035 | 0.48484848484848486 | 0.454545 | 0.575758 | inclusion_lane_endpoint_analysis_not_validation |
| L0 | train | STRICT_READY_CANDIDATE | strict_preendpoint_freeze_candidate | 1 | 35.4156 | 0.0040084188067623 | 0.334591 | -2.87421 | 0.0 | 0 | 1 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | holdout | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 28 | 11.4619 | -13.784893510161018 | 1.02725 | 0.03146 | 0.9285714285714286 | 0.464286 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 2 | 11.0235 | -42.10621338905556 | 2.50713 | 2.15304 | 1.0 | 0.5 | 0 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 14 | 25.5511 | -12.27650246743915 | 0.0526969 | -0.834653 | 0.7857142857142857 | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | train | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 80 | 10.4547 | -15.867050207546441 | 0.378257 | 0.411284 | 0.9375 | 0.4625 | 0.4375 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | train | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 17 | 17.6663 | -3.8543471514900745 | 2.15822 | 2.28773 | 0.5882352941176471 | 0.176471 | 0.176471 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | train | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 33 | 20.7046 | -7.161680994387883 | -0.325123 | -0.886298 | 0.8484848484848485 | 0.545455 | 0.636364 | inclusion_lane_endpoint_analysis_not_validation |
| L1 | train | STRICT_READY_CANDIDATE | strict_preendpoint_freeze_candidate | 1 | 31.4042 | -6.752959116046792 | -3.67678 | -6.88558 | 1.0 | 1 | 1 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | holdout | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 28 | 12.9694 | <NA> | 0.111816 | 0.866016 | <NA> | 0.5 | 0.428571 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 2 | 23.5955 | <NA> | 15.0792 | 14.7251 | <NA> | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 14 | 24.4876 | <NA> | 0.41515 | -0.0292532 | <NA> | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | train | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 80 | 12.0155 | <NA> | 0.374592 | 0.104249 | <NA> | 0.425 | 0.4875 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | train | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 17 | 17.7798 | <NA> | 0.428583 | 3.37625 | <NA> | 0.411765 | 0.235294 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | train | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 33 | 22.6554 | <NA> | 0.80163 | 0.133458 | <NA> | 0.393939 | 0.484848 | inclusion_lane_endpoint_analysis_not_validation |
| L2 | train | STRICT_READY_CANDIDATE | strict_preendpoint_freeze_candidate | 1 | 32.7393 | <NA> | -2.34171 | -5.55051 | <NA> | 1 | 1 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | holdout | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 28 | 12.5133 | -4.323680768849266 | 0.124458 | -0.950214 | 0.8214285714285714 | 0.464286 | 0.678571 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 2 | 8.97426 | -24.398326765875943 | 0.457928 | 0.103834 | 1.0 | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 14 | 25.5602 | -5.629327810610777 | 0.0284701 | -0.440967 | 0.7857142857142857 | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | train | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 80 | 10.4093 | -5.742542358552787 | 0.00149686 | -0.837772 | 0.875 | 0.5 | 0.575 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | train | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 17 | 14.2411 | -0.0756115734242897 | 1.15593 | 0.908476 | 0.5294117647058824 | 0.235294 | 0.352941 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | train | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 33 | 20.4268 | -3.234328034403209 | -0.352577 | -0.69585 | 0.7575757575757576 | 0.545455 | 0.69697 | inclusion_lane_endpoint_analysis_not_validation |
| L3 | train | STRICT_READY_CANDIDATE | strict_preendpoint_freeze_candidate | 1 | 32.9465 | -3.0918713026056466 | -2.13449 | -5.3433 | 1.0 | 1 | 1 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | holdout | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 28 | 11.4619 | -13.784893510161018 | 1.02725 | 0.03146 | 0.9285714285714286 | 0.464286 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 2 | 11.0235 | -42.10621338905556 | 2.50713 | 2.15304 | 1.0 | 0.5 | 0 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 14 | 25.5511 | -12.27650246743915 | 0.0526969 | -0.834653 | 0.7857142857142857 | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | train | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 80 | 10.4547 | -15.867050207546441 | 0.378257 | 0.411284 | 0.9375 | 0.4625 | 0.4375 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | train | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 17 | 17.6663 | -3.8543471514900745 | 2.15822 | 2.28773 | 0.5882352941176471 | 0.176471 | 0.176471 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | train | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 33 | 20.7046 | -7.161680994387883 | -0.325123 | -0.886298 | 0.8484848484848485 | 0.545455 | 0.636364 | inclusion_lane_endpoint_analysis_not_validation |
| source_native_hard_family | train | STRICT_READY_CANDIDATE | strict_preendpoint_freeze_candidate | 1 | 31.4042 | -6.752959116046792 | -3.67678 | -6.88558 | 1.0 | 1 | 1 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | holdout | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 28 | 11.9367 | <NA> | -0.0785966 | -0.565514 | <NA> | 0.5 | 0.678571 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 2 | 8.69049 | <NA> | 0.174162 | -0.179931 | <NA> | 0.5 | 0.5 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | holdout | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 14 | 29.8864 | <NA> | 3.14572 | 2.2821 | <NA> | 0.357143 | 0.285714 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | train | ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 80 | 10.1709 | <NA> | -0.0369305 | -0.463469 | <NA> | 0.5125 | 0.575 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | train | CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 17 | 14.506 | <NA> | 1.11095 | 2.67475 | <NA> | 0.411765 | 0.352941 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | train | CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 33 | 18.8152 | <NA> | 1.1774 | 0.434381 | <NA> | 0.363636 | 0.363636 | inclusion_lane_endpoint_analysis_not_validation |
| tau_side_evidence_measure_l2 | train | STRICT_READY_CANDIDATE | strict_preendpoint_freeze_candidate | 1 | 51.2973 | <NA> | 16.2164 | 13.0075 | <NA> | 0 | 0 | inclusion_lane_endpoint_analysis_not_validation |

## Information-Gain Transitions

| split | inclusion_lane | transition | n_galaxies | median_delta_rmse_curr_minus_prev | improved_fraction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| holdout | STRICT_PLUS_CAUTION | L0_to_L1 | 16 | 0.835103 | 0.375 | inclusion_lane_endpoint_analysis_not_validation |
| holdout | STRICT_PLUS_CAUTION | L1_to_L2 | 16 | 0.567445 | 0.4375 | inclusion_lane_endpoint_analysis_not_validation |
| holdout | STRICT_PLUS_CAUTION | L2_to_L3 | 16 | -0.460932 | 0.625 | inclusion_lane_endpoint_analysis_not_validation |
| holdout | ACQUISITION_REQUIRED | L0_to_L1 | 28 | 0.454706 | 0.464286 | inclusion_lane_endpoint_analysis_not_validation |
| holdout | ACQUISITION_REQUIRED | L1_to_L2 | 28 | 0.259884 | 0.464286 | inclusion_lane_endpoint_analysis_not_validation |
| holdout | ACQUISITION_REQUIRED | L2_to_L3 | 28 | -0.636537 | 0.642857 | inclusion_lane_endpoint_analysis_not_validation |
| holdout | ALL_ROWS | L0_to_L1 | 44 | 0.575081 | 0.431818 | inclusion_lane_endpoint_analysis_not_validation |
| holdout | ALL_ROWS | L1_to_L2 | 44 | 0.445057 | 0.454545 | inclusion_lane_endpoint_analysis_not_validation |
| holdout | ALL_ROWS | L2_to_L3 | 44 | -0.602864 | 0.636364 | inclusion_lane_endpoint_analysis_not_validation |
| train | STRICT_PLUS_CAUTION | L0_to_L1 | 51 | 0.37867 | 0.352941 | inclusion_lane_endpoint_analysis_not_validation |
| train | STRICT_PLUS_CAUTION | L1_to_L2 | 51 | 0.436165 | 0.431373 | inclusion_lane_endpoint_analysis_not_validation |
| train | STRICT_PLUS_CAUTION | L2_to_L3 | 51 | -0.160103 | 0.607843 | inclusion_lane_endpoint_analysis_not_validation |
| train | ACQUISITION_REQUIRED | L0_to_L1 | 80 | 0.175078 | 0.4375 | inclusion_lane_endpoint_analysis_not_validation |
| train | ACQUISITION_REQUIRED | L1_to_L2 | 80 | 0.280598 | 0.4375 | inclusion_lane_endpoint_analysis_not_validation |
| train | ACQUISITION_REQUIRED | L2_to_L3 | 80 | -0.345314 | 0.575 | inclusion_lane_endpoint_analysis_not_validation |
| train | ALL_ROWS | L0_to_L1 | 131 | 0.221641 | 0.40458 | inclusion_lane_endpoint_analysis_not_validation |
| train | ALL_ROWS | L1_to_L2 | 131 | 0.343317 | 0.435115 | inclusion_lane_endpoint_analysis_not_validation |
| train | ALL_ROWS | L2_to_L3 | 131 | -0.243042 | 0.587786 | inclusion_lane_endpoint_analysis_not_validation |

## Claim Boundary

The caution lane is not accepted evidence. Any positive or negative
baseline comparison here is a preparation diagnostic for future
residual-blind source acquisition and endpoint predeclaration.
