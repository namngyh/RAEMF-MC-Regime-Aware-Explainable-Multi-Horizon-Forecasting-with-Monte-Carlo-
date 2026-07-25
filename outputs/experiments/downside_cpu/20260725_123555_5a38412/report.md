# CPU downside experiment — experimental, not production

Báo cáo nghiên cứu trung lập. Kết quả không phải khuyến nghị đầu tư và không được dùng để tự động thay mô hình production.

## 1. Thiết kế thử nghiệm

Evaluation scope: `nested_purged_development_oos`. Mọi target development phải kết thúc trước 2021-04-02. Outer test không tham gia feature selection, calibration hoặc threshold selection.

## 2. Tình trạng baseline

Baseline Risk-off được giữ nguyên là `P(Bear) + P(Stress)` từ EBM bốn lớp. Giai đoạn từ 2021-04-02 chỉ là `legacy_audit_test`, không phải untouched holdout mới.

| model | horizon | recall | precision | pr_auc | brier | ece | expected_cost | alert_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| candidate_risk_off | 20 | 0.2885 | 0.2483 | 0.2512 | 0.2903 | 0.2986 | 0.0650 | 0.3038 |
| multiclass_probability_sum | 20 | 0.4154 | 0.2348 | 0.2270 | 0.2495 | 0.2276 | 0.0582 | 0.4628 |

## 3. Tác động của Risk-off head

![So sánh Risk-off OOS](figures/risk_off_oos_comparison.png)

**Nhận xét:** Bảng là nguồn số chính; hình chỉ trực quan hóa recall và expected cost. Không kết luận cải thiện nếu bootstrap hoặc consistency theo fold không đạt.

## 4. Threshold được chọn và lý do

Có 1 quyết định fold/horizon. Mỗi threshold được chọn trên outer validation. Khi ràng buộc precision/recall thất bại, artifact ghi rõ `constraint_failure_minimum_expected_cost`.

![Chi phí theo threshold](figures/risk_off_cost_curve.png)

Điểm cực tiểu trên curve chỉ là validation estimate; outer-test metrics không dùng để dịch chuyển threshold.

## 5. Precision–recall trade-off

![Precision–recall trade-off](figures/risk_off_precision_recall_curve.png)

Threshold thấp có thể tăng recall nhưng cũng tăng false-positive exposure. Acceptance criteria yêu cầu precision tối thiểu 25%.

## 6. Expected cost

Expected cost dùng độ lớn `abs(min(future_mae, 0))` cho false negative và `max(forward_return, 0)` cho false positive, không chỉ đếm lỗi.

## 7. False negative nguy hiểm nhất

| date | horizon | fold | model | actual_risk_off | probability | threshold | alert | forward_return | future_mae |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-02-25 | 20 | 0 | multiclass_probability_sum | 1 | 0.4430 | 0.4900 | 0 | -0.3220 | -0.3220 |
| 2020-02-27 | 20 | 0 | multiclass_probability_sum | 1 | 0.4885 | 0.4900 | 0 | -0.2579 | -0.3096 |
| 2020-02-24 | 20 | 0 | multiclass_probability_sum | 1 | 0.4793 | 0.4900 | 0 | -0.3039 | -0.3039 |
| 2020-03-05 | 20 | 0 | multiclass_probability_sum | 1 | 0.4775 | 0.4900 | 0 | -0.2413 | -0.3039 |
| 2020-03-06 | 20 | 0 | multiclass_probability_sum | 1 | 0.4790 | 0.4900 | 0 | -0.1906 | -0.3018 |
| 2020-03-03 | 20 | 0 | multiclass_probability_sum | 1 | 0.4730 | 0.4900 | 0 | -0.2958 | -0.3009 |
| 2020-03-04 | 20 | 0 | multiclass_probability_sum | 1 | 0.4879 | 0.4900 | 0 | -0.2681 | -0.2995 |
| 2020-03-02 | 20 | 0 | multiclass_probability_sum | 1 | 0.4834 | 0.4900 | 0 | -0.2893 | -0.2939 |
| 2020-02-20 | 20 | 0 | multiclass_probability_sum | 1 | 0.4657 | 0.4900 | 0 | -0.2564 | -0.2564 |
| 2020-03-10 | 20 | 0 | multiclass_probability_sum | 1 | 0.4498 | 0.4900 | 0 | -0.1130 | -0.2394 |
| 2020-02-17 | 20 | 0 | multiclass_probability_sum | 1 | 0.4813 | 0.4900 | 0 | -0.2231 | -0.2231 |
| 2020-03-11 | 20 | 0 | multiclass_probability_sum | 1 | 0.4649 | 0.4900 | 0 | -0.0649 | -0.2077 |
| 2020-02-14 | 20 | 0 | multiclass_probability_sum | 1 | 0.4844 | 0.4900 | 0 | -0.2075 | -0.2075 |
| 2020-02-13 | 20 | 0 | multiclass_probability_sum | 1 | 0.4564 | 0.4900 | 0 | -0.1986 | -0.1986 |
| 2020-03-12 | 20 | 0 | multiclass_probability_sum | 1 | 0.4812 | 0.4900 | 0 | -0.0148 | -0.1544 |

## 8. False positive tốn kém nhất

| date | horizon | fold | model | actual_risk_off | probability | threshold | alert | forward_return | future_mae |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-03-24 | 20 | 0 | multiclass_probability_sum | 0 | 0.5192 | 0.4900 | 1 | 0.1539 | 0.0046 |
| 2020-03-30 | 20 | 0 | multiclass_probability_sum | 0 | 0.5147 | 0.4900 | 1 | 0.1471 | 0.0004 |
| 2020-05-04 | 20 | 0 | multiclass_probability_sum | 0 | 0.5252 | 0.4900 | 1 | 0.1418 | 0.0022 |
| 2020-03-23 | 20 | 0 | multiclass_probability_sum | 0 | 0.5090 | 0.4900 | 1 | 0.1401 | -0.0111 |
| 2020-05-05 | 20 | 0 | multiclass_probability_sum | 0 | 0.4999 | 0.4900 | 1 | 0.1352 | 0.0238 |
| 2017-11-02 | 20 | 0 | multiclass_probability_sum | 0 | 0.5262 | 0.4900 | 1 | 0.1312 | 0.0127 |
| 2017-11-03 | 20 | 0 | multiclass_probability_sum | 0 | 0.4913 | 0.4900 | 1 | 0.1294 | 0.0063 |
| 2017-12-15 | 20 | 0 | multiclass_probability_sum | 0 | 0.5277 | 0.4900 | 1 | 0.1286 | 0.0116 |
| 2020-12-17 | 20 | 0 | multiclass_probability_sum | 0 | 0.5285 | 0.4900 | 1 | 0.1270 | 0.0148 |
| 2017-12-13 | 20 | 0 | multiclass_probability_sum | 0 | 0.5147 | 0.4900 | 1 | 0.1257 | 0.0116 |
| 2020-12-11 | 20 | 0 | multiclass_probability_sum | 0 | 0.5039 | 0.4900 | 1 | 0.1247 | 0.0055 |
| 2020-12-10 | 20 | 0 | multiclass_probability_sum | 0 | 0.5525 | 0.4900 | 1 | 0.1246 | 0.0145 |
| 2017-12-11 | 20 | 0 | multiclass_probability_sum | 0 | 0.5320 | 0.4900 | 1 | 0.1192 | 0.0075 |
| 2017-10-31 | 20 | 0 | multiclass_probability_sum | 0 | 0.5200 | 0.4900 | 1 | 0.1170 | -0.0050 |
| 2020-04-29 | 20 | 0 | multiclass_probability_sum | 0 | 0.5037 | 0.4900 | 1 | 0.1169 | -0.0087 |

## 9. Feature ablation

| horizon | outer_fold | model_kind | feature_group | objective | recall | precision | pr_auc | brier | ece | expected_cost | admissible | constraint_failures | inner_folds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20 | 0 | logistic | base_plus_downside_all | 0.4329 | 1.0000 | 0.3833 | 0.5003 | 0.4003 | 0.4075 | 0.0248 | False | brier_tolerance_exceeded | 1 |

Ablation chạy theo nhóm feature trong inner purged folds; outer test không chọn feature.

## 10. Calibration

![Reliability Risk-off](figures/risk_off_reliability.png)

Calibration được fit trên validation của từng outer fold. Reliability trong hình dùng outer development OOS.

## 11. Backtest risk overlay

| model | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | calmar | max_drawdown | turnover | total_transaction_cost | hit_rate | average_exposure | time_in_market | state_changes | cvar_95 | time_in_risk_reduced_state | avoided_loss | opportunity_cost |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline_no_overlay | 0.2400 | 0.0545 | 0.0796 | 0.6851 | 0.7453 | 0.2453 | -0.2223 | 17.8856 | 0.0179 | 0.5775 | 0.4215 | 0.9990 | 993 | 0.0141 | 0.0000 | nan | nan |
| baseline_risk_overlay | 0.0345 | 0.0086 | 0.0470 | 0.1828 | 0.1710 | 0.0573 | -0.1500 | 24.7800 | 0.0248 | 0.5724 | 0.1747 | 0.9990 | 993 | 0.0084 | 0.9598 | 0.8057 | 0.9879 |
| buy_and_hold | 0.6333 | 0.1244 | 0.1899 | 0.6551 | 0.7080 | 0.2748 | -0.4526 | 1.0000 | 0.0010 | 0.5785 | 0.9990 | 0.9990 | 1 | 0.0337 | 0.0000 | nan | nan |
| cash | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | -0.0000 | 0.0000 | nan | nan |

Overlay chỉ là paper overlay, dùng vị thế trễ một phiên và notional exposure. Không được thay notional bằng tiền ký quỹ futures.

## 12. Runtime và RAM trên CPU

| stage | horizon | fold | wall_time | cpu_time | peak_rss | peak_python_bytes | cache_status | thread_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| load_and_targets | nan | nan | 16.0427 | 15.9375 | 242081792 | 9082047 | targets:miss;features:hit | 2 |
| outer_fold | 20.0000 | 0.0000 | 17.8546 | 18.0156 | 292974592 | 51440940 | fold_indices:miss;hmm_egarch:hit | 2 |

Không phát hiện stage có wall time lớn hơn 4 lần CPU time.



Runner downside không gọi CUDA. `peak_rss=not_available` nghĩa là môi trường thiếu psutil; `peak_python_bytes` vẫn được ghi và giới hạn này phải được nêu rõ.

## 13. Giới hạn nghiên cứu

- Legacy audit đã được quan sát trước và không thể khôi phục thành holdout unbiased.
- Nhãn Risk-off phụ thuộc target bốn lớp hiện tại; binary target không đổi nghĩa bốn lớp.
- OHLCV không bao phủ vĩ mô, breadth, tin tức hoặc đổi thành phần chỉ số.
- Candidate tăng recall nhưng vi phạm precision, cost, calibration hoặc fold consistency vẫn phải bị loại.

### Post-selection legacy audit

_not_available: profile này không chạy legacy audit._

Legacy audit không tham gia chọn model, calibration, threshold hoặc acceptance.

## 14. Điều kiện được phép chạy shadow test

Trạng thái: `inconclusive_or_rejected`; đạt 4/10 kiểm tra đã đăng ký trước. Candidate không tự động thay production classifier hoặc scenario mode.

Chỉ forecast mới, đăng ký bất biến và chấm sau maturity mới tạo bằng chứng prospective.

## 15. Điều kiện chưa được phép dùng tiền thật

Không dùng tiền thật khi acceptance chưa đạt, bootstrap còn inconclusive, registry chưa có đủ forecast matured hoặc distribution calibration/VaR production chưa đạt. Repository không tự động cấp quyền production.

## Phụ lục bootstrap

| horizon | candidate | baseline | metric | mean_difference | ci_low | ci_high | ci_excludes_zero |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 20 | candidate_risk_off | multiclass_probability_sum | recall | -0.1341 | -0.2260 | -0.0522 | True |
| 20 | candidate_risk_off | multiclass_probability_sum | expected_cost | 0.0071 | -0.0024 | 0.0171 | False |
