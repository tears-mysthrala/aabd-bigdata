"""FastAPI scoring interface for a locally trained, trusted CNC model.

Run: CNC_MODEL_PATH=/path/to/model.joblib uv run --locked --with fastapi --with uvicorn uvicorn cnc_guard.api:app
Never load untrusted joblib/pickle files. Do not expose this demonstrator to OT.
"""
from __future__ import annotations

import os
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, model_validator

from cnc_guard.supervised import FEATURES, features_for_reading


class PriorSample(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    timestamp: datetime
    temperature: float = Field(ge=-40, le=200)
    vibration: float = Field(ge=0, le=100)


class Reading(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    machine_id: str = Field(min_length=1, max_length=32, pattern=r"^[A-Za-z0-9_-]+$")
    timestamp: datetime
    temperature: float = Field(ge=-40, le=200)
    vibration: float = Field(ge=0, le=100)
    pressure: float = Field(ge=0, le=5000)
    history: list[PriorSample] = Field(default_factory=list, max_length=3)

    @model_validator(mode="after")
    def validate_history(self):
        if self.timestamp.tzinfo is None:
            raise ValueError("timestamp must include timezone")
        times = [item.timestamp for item in self.history]
        if any(t.tzinfo is None for t in times):
            raise ValueError("history timestamps must include timezone")
        if times != sorted(times) or len(set(times)) != len(times):
            raise ValueError("history must be strictly chronological")
        if any(t >= self.timestamp for t in times):
            raise ValueError("history must precede the current reading")
        return self


class Prediction(BaseModel):
    machine_id: str
    timestamp: datetime
    failure_predicted: bool
    failure_probability: float = Field(ge=0, le=1)
    alert_level: str
    history_available: bool
    model_schema: int


def create_app(model_bundle: dict | None = None) -> FastAPI:
    state: dict = {}

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        bundle = model_bundle
        if bundle is None:
            filename = os.getenv("CNC_MODEL_PATH")
            if not filename:
                raise RuntimeError("CNC_MODEL_PATH must point to a trusted local artifact")
            # Joblib is pickle-based: never deserialize third-party untrusted data.
            bundle = joblib.load(Path(filename))
        if bundle.get("model_schema") != 1 or bundle.get("features") != list(FEATURES):
            raise RuntimeError("Unsupported model bundle/schema")
        state["bundle"] = bundle
        yield
        state.clear()

    api = FastAPI(title="CNC Guard scoring (synthetic demonstrator)", lifespan=lifespan)

    @api.get("/health")
    def health():
        return {"status": "ok", "model_loaded": "bundle" in state}

    @api.post("/predict", response_model=Prediction)
    def predict(payload: Reading):
        bundle = state.get("bundle")
        if bundle is None:
            raise HTTPException(status_code=503, detail="model unavailable")
        history = [{"temperature": p.temperature, "vibration": p.vibration}
                   for p in payload.history]
        values = features_for_reading(payload.temperature, payload.vibration,
                                      payload.pressure, history)
        frame = pd.DataFrame([[values[f] for f in FEATURES]], columns=list(FEATURES))
        prob = float(bundle["model"].predict_proba(frame)[0, 1])
        if not 0 <= prob <= 1:
            raise HTTPException(status_code=503, detail="invalid model output")
        level = "CRITICA" if prob >= 0.7 else "AVISO" if prob >= 0.15 else "OK"
        return Prediction(
            machine_id=payload.machine_id, timestamp=payload.timestamp,
            failure_predicted=prob >= float(bundle["binary_threshold"]),
            failure_probability=prob, alert_level=level,
            history_available=bool(history), model_schema=1,
        )

    return api


app = create_app()
