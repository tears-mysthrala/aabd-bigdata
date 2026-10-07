import numpy as np
import pytest
from fastapi.testclient import TestClient
from ml_api import create_app
from sklearn.datasets import load_breast_cancer
from train_pipeline import train_breast_cancer


@pytest.fixture(scope="module")
def trained(tmp_path_factory):
    path = tmp_path_factory.mktemp("owned-model") / "pipeline.pkl"
    model, X, y = train_breast_cancer(path)
    return path, model, X, y


def test_both_labels_and_probability_match_model(trained):
    path, model, X, _ = trained
    predictions = model.predict(X)
    with TestClient(create_app(path)) as client:
        assert client.get("/osasuna").status_code == 200
        for target, label in [(0, "Gaiztoa"), (1, "Ona")]:
            row = X[np.flatnonzero(predictions == target)[0]]
            response = client.post("/iragarri", json={"ezaugarriak": row.tolist()})
            assert response.status_code == 200
            data = response.json()
            assert data["iragarpena"] == data["probabilitate_klasea"] == target
            assert data["etiketa"] == label
            column = list(model.classes_).index(target)
            assert data["probabilitatea"] == pytest.approx(
                model.predict_proba([row])[0, column]
            )
        app = client.app
        assert app.state.model is not None
    assert app.state.model is None


@pytest.mark.parametrize(
    "values", [[1] * 29, [1] * 31, ["not-number"] * 30, [None] * 30]
)
def test_invalid_features_rejected(trained, values):
    with TestClient(create_app(trained[0])) as client:
        assert client.post("/iragarri", json={"ezaugarriak": values}).status_code == 422


def test_missing_model_is_503_and_stays_unloaded(tmp_path):
    app = create_app(tmp_path / "missing.pkl")
    with TestClient(app) as client:
        assert client.get("/osasuna").status_code == 503
        assert (
            client.post("/iragarri", json={"ezaugarriak": [1] * 30}).status_code == 503
        )
    assert app.state.model is None


def test_nonfinite_rejected(trained):
    from ml_api import PredictionRequest
    from pydantic import ValidationError

    for value in [float("nan"), float("inf"), float("-inf")]:
        with pytest.raises(ValidationError):
            PredictionRequest(ezaugarriak=[value] * 30)


def test_no_downloaded_artifact_used(trained):
    assert trained[0].name == "pipeline.pkl"
    assert list(load_breast_cancer().target_names) == ["malignant", "benign"]
