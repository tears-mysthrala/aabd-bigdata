"""Train only local models; never deserialize the downloaded Moodle artifact."""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler, StandardScaler

HERE = Path(__file__).resolve().parent
MODEL_PATH = HERE / "models" / "pipeline.pkl"


def train_breast_cancer(path=MODEL_PATH):
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42, stratify=data.target
    )
    preprocess = ColumnTransformer(
        [
            (
                "numeric",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", RobustScaler()),
                    ]
                ),
                list(range(30)),
            )
        ],
        remainder="drop",
    )
    pipeline = Pipeline(
        [
            ("preprocess", preprocess),
            ("model", LogisticRegression(random_state=42, max_iter=2000)),
        ]
    )
    pipeline.fit(X_train, y_train)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, path)
    # Only reload what this process just trained and wrote.
    loaded = joblib.load(path)
    assert np.array_equal(pipeline.predict(X_test), loaded.predict(X_test))
    return pipeline, X_test, y_test


def train_turnover(path=HERE / "models" / "txandakatze_pipeline.pkl"):
    rng = np.random.RandomState(42)
    n = 500
    df = pd.DataFrame(
        {
            "adina": rng.randint(22, 60, n),
            "soldata": rng.randint(20000, 70000, n),
            "lan_urte": rng.randint(0, 20, n),
            "departamentua": rng.choice(["IT", "HR", "Finantza", "Eragiketak"], n),
            "txandakatze": rng.randint(0, 2, n),
        }
    )
    df.loc[rng.choice(df.index, 30), "adina"] = np.nan
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(columns="txandakatze"), df.txandakatze, test_size=0.2, random_state=42
    )
    preprocess = ColumnTransformer(
        [
            (
                "numeric",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="mean")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                ["adina", "soldata", "lan_urte"],
            ),
            (
                "category",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "encoder",
                            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                        ),
                    ]
                ),
                ["departamentua"],
            ),
        ]
    )
    pipeline = Pipeline(
        [
            ("preprocess", preprocess),
            ("model", RandomForestClassifier(n_estimators=100, random_state=42)),
        ]
    )
    pipeline.fit(X_train, y_train)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, path)
    loaded = joblib.load(path)
    assert np.array_equal(loaded.predict(X_test), pipeline.predict(X_test))
    print(classification_report(y_test, pipeline.predict(X_test), zero_division=0))
    return float(accuracy_score(y_test, pipeline.predict(X_test)))


if __name__ == "__main__":
    print("Synthetic turnover accuracy:", train_turnover())
    model, X_test, y_test = train_breast_cancer()
    print(
        classification_report(
            y_test, model.predict(X_test), target_names=["malignant", "benign"]
        )
    )
