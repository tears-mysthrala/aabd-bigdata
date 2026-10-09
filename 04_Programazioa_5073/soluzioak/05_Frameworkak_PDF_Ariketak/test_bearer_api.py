"""Ejemplo docente 3.5: autenticación y predicción con modelo local propio."""

import secrets

import api_ariketak
import joblib
import pandas as pd
import pytest
from fastapi.testclient import TestClient
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


@pytest.fixture
def protected_client(monkeypatch, tmp_path):
    training = pd.DataFrame(
        {
            "produktua": ["A", "B"],
            "eskualdea": ["N", "S"],
            "prezioa": [10.0, 20.0],
            "stock": [1.0, 2.0],
        }
    )
    model = Pipeline(
        [
            (
                "preprocess",
                ColumnTransformer(
                    [
                        (
                            "category",
                            OneHotEncoder(handle_unknown="ignore"),
                            ["produktua", "eskualdea"],
                        ),
                        ("numeric", "passthrough", ["prezioa", "stock"]),
                    ]
                ),
            ),
            ("classifier", DummyClassifier(strategy="constant", constant=1)),
        ]
    ).fit(training, [0, 1])
    path = tmp_path / "own_model.joblib"
    joblib.dump(model, path)
    token = secrets.token_urlsafe(24)
    monkeypatch.setattr(api_ariketak, "MODEL_PATH", path)
    monkeypatch.setenv("MODEL_API_TOKEN", token)
    with TestClient(api_ariketak.ml_app(True)) as client:
        yield client, token


SALE = {"produktua": "A", "eskualdea": "N", "prezioa": 10.0, "stock": 1.0}


def test_missing_or_wrong_token_cannot_predict(protected_client):
    client, _ = protected_client
    for headers in ({}, {"Authorization": "Bearer invalid-fixture"}):
        response = client.post("/iragarri", json=SALE, headers=headers)
        assert response.status_code == 401
        assert response.headers["www-authenticate"] == "Bearer"


def test_valid_token_predicts_and_rejects_invalid_schema(protected_client):
    client, token = protected_client
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/iragarri", json=SALE, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"salmenta_altua": True}
    assert (
        client.post("/iragarri", json={"produktua": "A"}, headers=headers).status_code
        == 422
    )


def test_missing_operator_configuration_rejects_even_valid_previous_token(
    protected_client, monkeypatch
):
    client, token = protected_client
    monkeypatch.delenv("MODEL_API_TOKEN")
    response = client.post(
        "/iragarri", json=SALE, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
