"""Local educational API. Load only the locally generated, trusted model file."""

from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, FiniteFloat

from train_pipeline import MODEL_PATH

LABELS = {0: "Gaiztoa", 1: "Ona"}


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ezaugarriak: list[FiniteFloat] = Field(min_length=30, max_length=30)


class PredictionResponse(BaseModel):
    iragarpena: int
    etiketa: str
    probabilitatea: float = Field(ge=0, le=1)
    probabilitate_klasea: int


def predict_response(model, values):
    X = np.asarray(values, dtype=float).reshape(1, -1)
    prediction = int(model.predict(X)[0])
    classes = list(model.classes_)
    probability = float(model.predict_proba(X)[0][classes.index(prediction)])
    return PredictionResponse(
        iragarpena=prediction,
        etiketa=LABELS[prediction],
        probabilitatea=probability,
        probabilitate_klasea=prediction,
    )


def create_app(model_path=MODEL_PATH):
    @asynccontextmanager
    async def lifespan(app):
        app.state.model = None
        try:
            if Path(model_path).is_file():
                # This path is local operator configuration, never a request parameter.
                app.state.model = joblib.load(model_path)
            yield
        finally:
            app.state.model = None

    app = FastAPI(title="ML Iragarpen API — laboratorio", lifespan=lifespan)
    app.state.model = None

    @app.get("/osasuna")
    def health():
        if app.state.model is None:
            raise HTTPException(status_code=503, detail="Eredua ez dago prest.")
        return {"egoera": "martxan", "eredu_prest": True}

    @app.post("/iragarri", response_model=PredictionResponse)
    def predict(request: PredictionRequest):
        if app.state.model is None:
            raise HTTPException(status_code=503, detail="Eredua ez dago prest.")
        return predict_response(app.state.model, request.ezaugarriak)

    return app


app = create_app()
