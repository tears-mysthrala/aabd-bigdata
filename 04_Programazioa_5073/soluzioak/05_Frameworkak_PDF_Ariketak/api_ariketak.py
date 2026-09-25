"""FastAPI 3.1–3.5: adibide lokalak, datu fikziozkoak."""

from __future__ import annotations

import os
import secrets
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Response, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, field_validator

HERE = Path(__file__).resolve().parent
MODEL_PATH = HERE / "salmentak_pipeline.joblib"

app_3_1 = FastAPI(title="3.1 Kaixo")


@app_3_1.get("/")
def kaixo():
    return {"mezua": "Kaixo"}


class Liburua(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int = Field(ge=1450, le=2100)


app_3_2 = FastAPI(title="3.2 Liburutegia")
books: dict[int, Liburua] = {}


@app_3_2.get("/liburuak", response_model=list[Liburua])
def list_books():
    return list(books.values())


@app_3_2.get("/liburuak/{book_id}", response_model=Liburua)
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(404, "Liburua ez da aurkitu")
    return books[book_id]


@app_3_2.post("/liburuak", response_model=Liburua, status_code=201)
def create_book(book: Liburua):
    if book.id in books:
        raise HTTPException(409, "ID hori badago")
    books[book.id] = book
    return book


@app_3_2.delete("/liburuak/{book_id}", status_code=204)
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(404, "Liburua ez da aurkitu")
    del books[book_id]
    return Response(status_code=204)


class Erabiltzailea(BaseModel):
    izena: str = Field(min_length=3)
    adina: int = Field(ge=0, le=120)
    email: str

    @field_validator("email")
    @classmethod
    def emaila_balioztatu(cls, value: str) -> str:
        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError("emailak @ eta bi aldeetan testua behar ditu")
        return value


class Salmenta(BaseModel):
    produktua: str
    eskualdea: str
    prezioa: float | None = None
    stock: float | None = None


def ml_app(protected: bool) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        import joblib

        if not MODEL_PATH.is_file():
            raise RuntimeError("Lehenik 1.5 exekutatu: eredua falta da")
        # joblib/pickle kodea exekutatu dezake: proiektuak sortutako fitxategia bakarrik.
        app.state.model = joblib.load(MODEL_PATH)
        yield

    app = FastAPI(title="3.5 ML babestua" if protected else "3.4 ML", lifespan=lifespan)
    bearer = HTTPBearer(auto_error=False)

    def authorize(credentials: HTTPAuthorizationCredentials | None = Security(bearer)):
        expected = os.getenv("MODEL_API_TOKEN", "")
        if not expected or credentials is None or not secrets.compare_digest(credentials.credentials, expected):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Bearer token baliogabea",
                                headers={"WWW-Authenticate": "Bearer"})

    @app.get("/osasuna")
    def health():
        return {"status": "ok"}

    @app.post("/iragarri", dependencies=[Depends(authorize)] if protected else [])
    def predict(sale: Salmenta):
        import pandas as pd

        data = pd.DataFrame([sale.model_dump()])
        return {"salmenta_altua": bool(app.state.model.predict(data)[0])}

    return app


app_3_4 = ml_app(False)
app_3_5 = ml_app(True)
