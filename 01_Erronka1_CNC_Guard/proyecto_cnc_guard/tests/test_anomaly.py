"""Tests: anomalia-detektzioa (determinismoa, tasa, monotonia) + fusioa."""

import numpy as np
import pandas as pd

from cnc_guard.anomaly import anomaly_score, build_features, fit_anomaly, riesgo_final


def _toy(n: int = 2000, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame(
        {
            "tenperatura": rng.normal(65, 4, size=n),
            "bibrazioa": rng.normal(3, 0.8, size=n),
            "presioa": rng.normal(1012, 1.5, size=n),
        }
    )


def test_features_ingenieria():
    df = _toy(10)
    X = build_features(df)
    assert list(X.columns) == ["tenperatura", "bibrazioa", "presioa", "txv", "t2"]
    assert np.allclose(X["txv"], df["tenperatura"] * df["bibrazioa"])


def test_determinismo():
    df = _toy()
    m1 = fit_anomaly(build_features(df))
    m2 = fit_anomaly(build_features(df))
    s1 = anomaly_score(m1[0], m1[1], build_features(df), m1[2], m1[3])
    s2 = anomaly_score(m2[0], m2[1], build_features(df), m2[2], m2[3])
    np.testing.assert_array_equal(s1, s2)


def test_tasa_aproximada():
    df = _toy(5000)
    X = build_features(df)
    model, scaler, dmin, dmax = fit_anomaly(X, contamination=0.02)
    # IsolationForest semantika: decision<0 tasa ~ contamination
    rate = float((model.decision_function(scaler.transform(X)) < 0).mean())
    assert 0.005 < rate < 0.06, rate
    # Score-a monotonoa decision-arekiko (ranking bera)
    s = anomaly_score(model, scaler, X, dmin, dmax)
    assert float(np.corrcoef(model.decision_function(scaler.transform(X)), -s)[0, 1]) > 0.99


def test_extremo_mas_anomalo_que_centro():
    df = _toy()
    model, scaler, dmin, dmax = fit_anomaly(build_features(df))
    centro = pd.DataFrame({"tenperatura": [65.0], "bibrazioa": [3.0], "presioa": [1012.0]})
    extremo = pd.DataFrame({"tenperatura": [95.0], "bibrazioa": [8.0], "presioa": [1000.0]})
    s = anomaly_score(model, scaler, build_features(pd.concat([centro, extremo])), dmin, dmax)
    assert s[1] > s[0], s


def test_score_acotado():
    df = _toy()
    model, scaler, dmin, dmax = fit_anomaly(build_features(df))
    s = anomaly_score(model, scaler, build_features(df), dmin, dmax)
    assert float(s.min()) >= 0.0 and float(s.max()) <= 1.0


def test_fusion_max_y_cotas():
    assert riesgo_final(0.2, 0.8) == 0.8
    assert riesgo_final(0.9, 0.1) == 0.9
    assert 0.0 <= riesgo_final(0.0, 0.0) <= 1.0
