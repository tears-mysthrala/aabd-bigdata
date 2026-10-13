"""FastAPI contract tests without a trained artifact or external services."""
from __future__ import annotations

import numpy as np
import pytest

from cnc_guard.supervised import FEATURES

api_module = pytest.importorskip("cnc_guard.api")
TestClient = pytest.importorskip("fastapi.testclient").TestClient
pytest.importorskip("httpx")
create_app = api_module.create_app


class FixedModel:
    def __init__(self, p):
        self.p = p

    def predict_proba(self, _frame):
        return np.array([[1 - self.p, self.p]])


def bundle(prob):
    return {"model_schema": 1, "features": list(FEATURES),
            "model": FixedModel(prob), "binary_threshold": 0.3}


def reading():
    return {"machine_id": "M1", "timestamp": "2026-10-13T08:00:00Z",
            "temperature": 78, "vibration": 4.3, "pressure": 1007,
            "history": [{"timestamp": "2026-10-13T07:59:00Z",
                         "temperature": 77, "vibration": 4.1}]}


def test_health_and_all_three_alert_levels():
    for p, level in ((0.149, "OK"), (0.15, "AVISO"),
                     (0.699, "AVISO"), (0.7, "CRITICA")):
        with TestClient(create_app(bundle(p))) as client:
            assert client.get("/health").json()["model_loaded"]
            obj = client.post("/predict", json=reading())
            assert obj.status_code == 200, obj.text
            assert obj.json()["alert_level"] == level
            assert obj.json()["failure_predicted"] == (p >= 0.3)
            assert obj.json()["history_available"]


def test_bad_inputs_fail_closed():
    with TestClient(create_app(bundle(0.5))) as client:
        for changes in ({"temperature": "not-a-number"},
                        {"pressure": -1},
                        {"history": [{"timestamp": "2026-10-13T09:00:00Z",
                                      "temperature": 75, "vibration": 4}]},
                        {"timestamp": "2026-10-13T08:00:00"}):
            payload = {**reading(), **changes}
            assert client.post("/predict", json=payload).status_code == 422
