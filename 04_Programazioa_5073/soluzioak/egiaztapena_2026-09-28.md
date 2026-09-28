# 04 soluzioak: exekuzio-egiaztapena (2026-09-28)

**Ingurunea:** `/tmp/opencode/batchvenv` venv desechable (Python 3.14,
numpy/pandas/scikit-learn/matplotlib/seaborn/pydantic/fastapi/httpx,
PyYAML). Script bakoitza bere karpetan exekutatuta (`cwd` = bere
`soluzioak/` azpikarpeta; 01/02/06 kasuan `/tmp`-ko kopia exekutatu zen
`data/` idazketak repoa ez zikintzeko — script-ak bide erlatiboak erabiltzen
dituzte eta auto-sufizienteak dira).

| Script | Exit | Froga |
|---|---|---|
| `01_Lengoaiak_Ariketak/5073_1_Lengoaiak_Ariketak.py` (25 ariketa) | 0 | 32 assert gaindituta; `✅ Zuzena!` segida osoan |
| `02_Datu_Zientzia_Ariketak/5073_2_Datu_Zientzia_Ariketak.py` (25 ariketa) | 0 | 39 assert gaindituta; `✅ Zuzena!` (matplotlib Agg, `plt.show()` warning ez-blokeatzailea) |
| `03_Lengoaiak_PDF_Ariketak/5073_1_Lengoaiak_PDF_Ariketak.py` | 0 | JSON/YAML roundtrip assert; `.gitignore`/`.env.example`/PR-txantiloia `True`; `katalogoa.*` berridatzi eta berdinak (git garbi) |
| `04_Datu_Zientzia_PDF_Ariketak/5073_2_Datu_Zientzia_PDF_Ariketak.py` | 0 | Benchmark, garbiketa, JOIN/concat, grafikoak (3.1/3.2/3.3), DVC /tmp isolatuan; birsortutako CSV/grafikoak revertitu (`git checkout`, denborak makina-dependenteak) |
| `06_Programazioa_Ariketak/5073_3_Programazioa_Ariketak.py` (25 ariketa) | 0 | Pipeline accuracy 0.927, RF recall 0.634, Pydantic ValidationError espero bezala |

**Estaltzen ditu:** 04-LN (25), 04-DN (25), 04-LP/04-DP exekutagarriak,
04-T3-NB (25). Ez ditu estaltzen: 04-LP-1.2/2.1/2.2/2.4/2.5/4.3/4.4
(giza ebidentzia: taldea, GUI, PR — blokeatuta), 04-T3 Streamlit/GUI eta
Gemini/RAG API deiak (kodea prest, kanpoko zerbitzua behar da).

Run log-ak (makina honetatik kanpo berrerabilgarriak ez diren bideekin):
`/tmp/opencode/batch/*/run.log` — transkripzio iraunkorra ez da repoan
gorde (bide absolutuak dituzte); taula hau da ebidentzia.
