# 05_Frameworkak_PDF_Ariketak (5073 Modulua - 3. Gaia: AA Frameworka)

Karpeta honek `5073_3_Programazioa.pdf` apunte-dokumentuko (63 or., v1.1) ariketa
guztiak jasoko ditu: Scikit-Learn, Hugging Face, FastAPI, Streamlit, LangChain,
RAG eta proiektu integratzailea (GenAI + Gemini).

## Egoera (2026-09-25)

**Hezurdura**: 26 stub (`pendiente`). 1.3 eta 4.3 ez daude PDFan
(1.2→1.4 eta 4.2→4.4 jauziak), beraz zuzen falta dira.

| Blokea | Ariketak | Menpekotasun nagusiak |
|---|---|---|
| 1. Scikit-Learn | 1.1, 1.2, 1.4, 1.5, 1.6 | `scikit-learn`, `joblib` |
| 2. Hugging Face | 2.1–2.4 | `transformers`, `datasets` (+`torch`) |
| 3. FastAPI | 3.1–3.5 | `fastapi`, `uvicorn`, `pydantic` |
| 4. Streamlit | 4.1, 4.2, 4.4 | `streamlit` |
| 5. LangChain + Gemini | 5.1–5.4 | `langchain`, `google-generativeai`, `GEMINI_API_KEY` |
| 6. RAG | 6.1–6.4 | `langchain`, `sentence-transformers`, `chromadb` |
| 7. Integratzailea | 7.1 (60 min) | denak + `rag_api.py` |

## Edukia

- **`5073_3_Frameworkak_PDF_Ariketak.py`**: 26 stub (`# %%` gelaxkekin), enuntziatua docstring-ean.
- **`5073_3_Frameworkak_PDF_Ariketak.ipynb`**: biki sinkronizatua (53 gelaxka).
- **`test_frameworkak.py`**: stub-ak existitu eta `NotImplementedError` jaurtitzen dutela.
- **`requirements.txt`**: blokeen araberako menpekotasunak.

## Exekuzioa

```bash
python 5073_3_Frameworkak_PDF_Ariketak.py   # no-op: zenbatu pendienteak
python test_frameworkak.py                  # ✅ 26 stub
```

## Ingurunea: sistema vs venv

Makina honetan menpekotasun astunak **sisteman** daude (yay; venv bakoitzean
dozenaka GB bikoiztea saihesteko). Aukerak:

1. **Sistema** (uneko hobespena): `python` zuzenean; ez sortu `.venv` karpeta honetan.
2. **uv venv isolatua** (erregelamendu orokorra, [CONTRIBUTING](../../../CONTRIBUTING.md)):
   `uv venv --system-site-packages && uv sync` — sistemakoak berrerabili + isolamendua.

API-gakoak (`GEMINI_API_KEY` 5.x/6.x/7.1) `.env`-an, **inoiz ez versionatu**
([SECURITY](../../../SECURITY.md)).
