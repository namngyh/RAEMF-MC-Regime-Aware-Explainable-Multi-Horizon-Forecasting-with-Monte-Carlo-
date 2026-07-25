import numpy as np
import pandas as pd

from raemf_mc.evaluation.downside_experiment import _multiclass_probability_frame


def test_multiclass_probability_export_keeps_raw_and_calibrated_outputs():
    calibrated = np.array(
        [
            [0.10, 0.20, 0.60, 0.10],
            [0.55, 0.25, 0.10, 0.10],
        ]
    )
    raw = np.array(
        [
            [0.05, 0.15, 0.70, 0.10],
            [0.65, 0.20, 0.10, 0.05],
        ]
    )
    frame = _multiclass_probability_frame(
        dates=pd.Series(pd.to_datetime(["2020-01-02", "2020-01-03"])),
        actual_class=pd.Series(["Bear", "Bull"]),
        calibrated_probability=calibrated,
        raw_probability=raw,
        candidate_probability=np.array([0.75, 0.20]),
        raw_candidate_probability=np.array([0.85, 0.10]),
        horizon=20,
        fold=0,
        baseline_threshold=0.45,
        candidate_threshold=0.50,
        baseline_temperature=2.0,
        candidate_temperature=1.5,
        forward_return=pd.Series([-0.05, 0.03]),
        future_mae=pd.Series([-0.08, -0.01]),
        evaluation_scope="nested_purged_development_oos",
    )
    assert frame["predicted_class"].tolist() == ["Bear", "Bull"]
    np.testing.assert_allclose(
        frame[["prob_bull", "prob_sideway", "prob_bear", "prob_stress"]].sum(axis=1),
        1.0,
    )
    np.testing.assert_allclose(
        frame[
            [
                "raw_prob_bull",
                "raw_prob_sideway",
                "raw_prob_bear",
                "raw_prob_stress",
            ]
        ].sum(axis=1),
        1.0,
    )
    assert frame.loc[0, "baseline_risk_off_probability"] == 0.70
    assert frame.loc[0, "candidate_risk_off_alert"] == 1
    assert frame.loc[1, "actual_risk_off"] == 0
