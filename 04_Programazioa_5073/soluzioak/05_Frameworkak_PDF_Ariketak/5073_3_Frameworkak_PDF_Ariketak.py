"""5073 3. gaia (AA Frameworka) PDF ariketak — hezurdura.

Iturria: `04_Programazioa_5073/materialak/5073_3_Programazioa.pdf` (63 or., v1.1).
Egoera: denak `pendiente`; funtzio bakoitzak PDFko enuntziatua docstring-ean
jasotzen du eta `NotImplementedError` jaurtitzen du inplementatu arte.
Exekuzioa: `python 5073_3_Frameworkak_PDF_Ariketak.py` (inportagarria, no-op).

Oharra: 1.3 eta 4.3 ariketak ez daude PDFan (1.2→1.4 eta 4.2→4.4 jauziak).
"""

# %% blokea: inportazio arinak (heavy deps ariketaren barruan, lazy)
from __future__ import annotations

ARIKETA_ZERRENDA = [
    "1.1", "1.2", "1.4", "1.5", "1.6",
    "2.1", "2.2", "2.3", "2.4",
    "3.1", "3.2", "3.3", "3.4", "3.5",
    "4.1", "4.2", "4.4",
    "5.1", "5.2", "5.3", "5.4",
    "6.1", "6.2", "6.3", "6.4",
    "7.1",
]


def _ez_inplementatuta(gid: str, menpekotasuna: str):
    raise NotImplementedError(f"Ariketa {gid} pendiente (behar: {menpekotasuna}).")


# %% 1. Scikit-Learn
def ariketa_1_1():
    """1.1 (15 min, banaka): 5 urratseko eskema load_wine/iris-ekin, KNN→LogisticRegression, test_size=0.3. Behar: scikit-learn."""
    _ez_inplementatuta("1.1", "scikit-learn")


def ariketa_1_2():
    """1.2 (20 min, taldeka): ColumnTransformer salmenta-daturako (kategoriko/zenbakizko/stock). Behar: scikit-learn, pandas."""
    _ez_inplementatuta("1.2", "scikit-learn, pandas")


def ariketa_1_4():
    """1.4 (15 min, banaka): load_diabetes-ekin LinearRegression vs erregularizatua, R² interpretazioa. Behar: scikit-learn."""
    _ez_inplementatuta("1.4", "scikit-learn")


def ariketa_1_5():
    """1.5 (25 min, taldeka): pipeline osoa (ColumnTransformer + eredua), joblib gorde/kargatu + iragarpena. Behar: scikit-learn, joblib."""
    _ez_inplementatuta("1.5", "scikit-learn, joblib")


def ariketa_1_6():
    """1.6 (25 min, taldeka): GridSearchCV 2-3 hiperparametrorekin. Behar: scikit-learn."""
    _ez_inplementatuta("1.6", "scikit-learn")


# %% 2. Hugging Face
def ariketa_2_1():
    """2.1 (10 min, banaka): huggingface.co/models arakatu eta kasura egokitu. Behar: web (HF Hub)."""
    _ez_inplementatuta("2.1", "web: huggingface.co")


def ariketa_2_2():
    """2.2 (20 min, taldeka): 8-10 iruzkin fikziozko (EN) sentiment-analysis pipelinetik + laburpen-taula. Behar: transformers, torch."""
    _ez_inplementatuta("2.2", "transformers, torch")


def ariketa_2_3():
    """2.3 (15 min, banaka): hiru esaldi euskaraz tokenizatu bert-base-multilingual-ekin. Behar: transformers."""
    _ez_inplementatuta("2.3", "transformers")


def ariketa_2_4():
    """2.4 (15 min, taldeka): imdb kargatu, positiboak iragazi. Behar: datasets."""
    _ez_inplementatuta("2.4", "datasets")


# %% 3. FastAPI
def ariketa_3_1():
    """3.1 (10 min, banaka): FastAPI + uvicorn instalatu, / ibilbidea. Behar: fastapi, uvicorn."""
    _ez_inplementatuta("3.1", "fastapi, uvicorn")


def ariketa_3_2():
    """3.2 (20 min, taldeka): liburutegi API-a (id, izenburua...). Behar: fastapi."""
    _ez_inplementatuta("3.2", "fastapi")


def ariketa_3_3():
    """3.3 (20 min, banaka): Pydantic erabiltzaile-eredua + balioztatzea. Behar: pydantic."""
    _ez_inplementatuta("3.3", "pydantic")


def ariketa_3_4():
    """3.4 (25 min, taldeka): 1.5eko pipeline-a startup-ean kargatu, POST /iragarri + /osasuna. Behar: fastapi, joblib, scikit-learn."""
    _ez_inplementatuta("3.4", "fastapi, joblib, scikit-learn")


def ariketa_3_5():
    """3.5 (20 min, banaka): /iragarri Bearer token bidez babestu. Behar: fastapi."""
    _ez_inplementatuta("3.5", "fastapi")


# %% 4. Streamlit
def ariketa_4_1():
    """4.1 (15 min, banaka): Streamlit app izenburu + DataFrame. Behar: streamlit, pandas."""
    _ez_inplementatuta("4.1", "streamlit, pandas")


def ariketa_4_2():
    """4.2 (20 min, taldeka): formularioa sidebar-ekin (hizkuntza, gaia). Behar: streamlit."""
    _ez_inplementatuta("4.2", "streamlit")


def ariketa_4_4():
    """4.4 (30 min, taldeka): ML aplikazio osoa sidebar-nabigazioarekin. Behar: streamlit, scikit-learn."""
    _ez_inplementatuta("4.4", "streamlit, scikit-learn")


# %% 5. LangChain + Gemini
def ariketa_5_1():
    """5.1 (10 min, banaka): Gemini API-gako doakoa AI Studio-tik. Behar: web (Google AI Studio), .env (inoiz ez versionatu)."""
    _ez_inplementatuta("5.1", "GEMINI_API_KEY (.env)")


def ariketa_5_2():
    """5.2 (25 min, taldeka): chain Gemini-rekin produktuaren ezaugarrietarako. Behar: langchain, google-generativeai."""
    _ez_inplementatuta("5.2", "langchain, google-generativeai")


def ariketa_5_3():
    """5.3 (25 min, banaka): txatbot sinplea memoria + Gemini. Behar: langchain, google-generativeai."""
    _ez_inplementatuta("5.3", "langchain, google-generativeai")


def ariketa_5_4():
    """5.4 (30 min, taldeka): agentea bi tresnarekin (kalkulua + ...). Behar: langchain."""
    _ez_inplementatuta("5.4", "langchain")


# %% 6. RAG
def ariketa_6_1():
    """6.1 (15 min, taldeka): NotebookLM-en sartu eta dokumentua indexatu. Behar: web (NotebookLM)."""
    _ez_inplementatuta("6.1", "web: NotebookLM")


def ariketa_6_2():
    """6.2 (20 min, banaka): testu luzea (2-3 or.) zatitu chunketan. Behar: langchain."""
    _ez_inplementatuta("6.2", "langchain")


def ariketa_6_3():
    """6.3 (20 min, taldeka): 6-8 dokumentu, embedding-ak + bilaketa semantikoa. Behar: sentence-transformers, chromadb/faiss."""
    _ez_inplementatuta("6.3", "sentence-transformers, chromadb")


def ariketa_6_4():
    """6.4 (30 min, taldeka): RAG chain osoa Gemini-rekin (4-5 dokumentu). Behar: langchain, google-generativeai."""
    _ez_inplementatuta("6.4", "langchain, google-generativeai")


# %% 7. Proiektu integratzailea
def ariketa_7_1():
    """7.1 (60 min, taldeka): FastAPI (RAG + Gemini) backend + Streamlit frontend, 3-4 dokumentu. Behar: fastapi, streamlit, langchain, google-generativeai."""
    _ez_inplementatuta("7.1", "fastapi, streamlit, langchain, google-generativeai")


def main() -> None:
    print(f"5073 3. gaia: {len(ARIKETA_ZERRENDA)} ariketa (denak pendiente, stubs).")
    print("Inplementatu funtzioak banan-banan; test: python test_frameworkak.py")


if __name__ == "__main__":
    main()
