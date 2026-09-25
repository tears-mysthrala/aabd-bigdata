# 5073 · 3. gaia · Frameworkak (PDFko 26 ariketak)

`5073_3_Programazioa.pdf`-ko 1.1–7.1 ariketen erreferentzia-ebazpenak.
1.3 eta 4.3 zenbakiak ez daude PDFan. Ariketa bakoitzak
`5073_3_Frameworkak_PDF_Ariketak.py`-n sarrera bat dauka; koadernoak sarrera
horiek gaika erakusten ditu.

## Egoera

- **1.x**: scikit-learn kodea prest. Train/test banaketa aurreprozesamenduaren
  aurretik egiten da. 1.5ek sortzen duen `salmentak_pipeline.joblib` fitxategia
  3.4/3.5ek erabiltzen dute. Datuak sintetikoak dira, eta emaitza ez da
  negozio-erabilerarako ebidentzia.
- **2.x**: Hugging Face Hub, sentimentu-analisia, tokenizazioa eta IMDb kodea
  prest. 2.1eko katalogo-kopurua alda daiteke; 2.2–2.4ek deskarga behar dute.
- **3.x**: `api_ariketak.py`-k 3.1/3.2/3.4/3.5 APIak eta 3.3ko Pydantic eredua
  dauzka. 3.2ko liburuak memorian soilik gordetzen dira. 3.5eko tokena
  `MODEL_API_TOKEN` ingurune-aldagaitik dator. APIak demo lokalak dira.
- **4.x**: `streamlit_4_1.py`, `streamlit_4_2.py` eta `streamlit_4_4.py`.
  4.4ko ebaluazioak holdout bereizia du, baina datuak sintetikoak dira.
- **5.x**: 5.1ek gakoaren *presentzia* soilik egiaztatzen du. 5.2–5.4ko
  Gemini deiak ez dira exekutatu. 5.4ko kalkulagailuak ASTko eragiketa
  baimenduak bakarrik interpretatzen ditu; `eval` ez du erabiltzen.
- **6.x**: 6.1 NotebookLM-ko giza/GUI jarduera da. 6.2ko chunk alderaketa
  lokala da. 6.3/6.4 Gemini embeddings + FAISS bidez idatzi dira;
  benetako bilaketa eta `Ez dakit` erantzuna egiaztatu gabe daude.
- **7.1**: `rag_api.py` + `rag_streamlit.py` proiektu integratua; TXT kargak
  mugatuta daude. APIak berreskuratutako iturriak erakusten ditu; horrek ez du
  LLMak sortutako baieztapen bakoitza iturriak sostengatzen duela ziurtatzen.

**Egoera orokorra: kodea prestatuta, exekuzio osoa eta kanpoko zerbitzuen
emaitzak egiaztatu gabe.** Koadernoan ez dago aurrez betetako irteerarik.

### Exekuzio lokal behatua (2026-09-25)

Python 3.14 eta scikit-learn 1.9.1 ingurune lokalean: 1.1eko test accuracy
`0.9815` (54 lagin); 1.4ko R² test `0.4773` linealean, `0.4703` basoan eta
`0.4774/0.4776/0.4781` Ridge α `0.1/1/10`-erako. 1.5eko modeloa lokalki
gorde eta berriz kargatu da: lehen iragarpena berdina, test accuracy `0.75`
20 datu sintetikotan. 1.6: grid CV `0.9837`, test `1.0`; random CV `0.9837`,
test `0.9815`. Denbora makina honetako exekuzio puntualari dagokio eta ez da
benchmark fidagarria. 6.2ko chunk kopuruak: overlap 0/100/200 → 8/9/12.

FastAPIren TestClient lokalarekin: 3.1ek 200, 3.2k 404/201/200/204,
3.4k 200/200 eta 3.5ek tokenik gabe 401 eta token lokalarekin 200 eman
dituzte; 3.3ko hiru sarrera okerrak baztertu dira. Ez da zerbitzari bereizi,
Swagger GUI edo kanpo-sareko egiaztapenik egin.

2.1eko Hugging Face Hub API iragazkiak (`filter=eu`) **2554 eredu etiketatu**
itzuli ditu 2026-09-25ean; kopurua unean unekoa da, eta etiketak ez du
eredu bakoitzaren euskarazko kalitatea frogatzen. Aukeratutako
[`ixa-ehu/berteus-base-cased`](https://huggingface.co/ixa-ehu/berteus-base-cased)
oinarrizko BERT euskarazkoa da, testu-errepresentazioetarako; ez da zuzenean
sentimentu-sailkatzaile bat.

2.3ko hiru esaldiak `bert-base-multilingual-cased` tokenizadorearekin
prozesatu dira: lehenengoaren hasiera `Gaur, e, ##gura, ##ldi`,
bigarrenarena `Ik, ##as, ##lee, ##k` eta hirugarrenarena
`Adi, ##men, arti, ##fi, ##zial, ##a` izan da. Irteera inprimatu ondoren
lehen deskargako prozesua I/O itxaronaldian geratu eta eskuz amaitu zen;
cachea erabiliz errepikatu da eta hiru esaldi/15 `##` azpitokenekin
**exit 0** lortu da.

2.4ko IMDb `train` deskarga/filter/select exekuzioak bost lerroko Pandas
taula eman du, bi zutaberekin eta bost `label=1` balioekin (lehen iritzia
728 karaktere). 2.2ko bederatzi iritzi fikziozkoen exekuzioan 5
`NEGATIVE` eta 4 `POSITIVE` irten dira; score txikiena `0.9821` izan da.
Horrek ez du iritzi anbiguoen ziurtasun erreala edo kalibrazioa frogatzen.

LangChain 0.3 multzo deklaratua beste venv isolatu batean instalatu da:
`langchain 0.3.30`, `core 0.3.86`, `community 0.3.31`,
`google-genai 2.1.12`. 5.x/6.x/7.1eko klaseen inportazioak eta Gemini
chat/embedding objektuen eraikuntza **gako fikziozko lokalarekin, sare-deirik
gabe**, exit 0 izan dira. Horrek ez du Google APIko dei bat, kuota edo
erantzuna balioztatzen.

## Ingurunea eta exekuzioa

Erabili ingurune isolatu bat (edo ikasgelako ingurune adostua). `requirements.txt`
multzo osoa da; bloke lokaletan ez dira LLM menpekotasunak behar.

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python 5073_3_Frameworkak_PDF_Ariketak.py
.venv/bin/python -m uvicorn api_ariketak:app_3_2 --host 127.0.0.1 --port 8000
.venv/bin/python -m streamlit run streamlit_4_1.py
```

1.5: `importlib.import_module("5073_3_Frameworkak_PDF_Ariketak").ariketa_1_5()`.
3.4/3.5: sortu lehenik 1.5eko eredua. 3.5: ezarri `MODEL_API_TOKEN` tokiko
ingurunean. `/docs`-en HTTP 201/204/404 eta Pydantic 422 erantzunak ikus
daitezke, baina oraindik ez dira hemen frogatu.

Gemini: kopiatu `.env.example` -> `.env` eta bete norberaren gakoa. `.env`
ez da versionatu behar. `GEMINI_MODEL` aukerakoa da. 7.1erako:

```bash
.venv/bin/python -m uvicorn rag_api:app --host 127.0.0.1 --port 8000
.venv/bin/python -m streamlit run rag_streamlit.py
```

Erabili baimendutako TXT fitxategiak soilik: embeddings eta galderak Google-ren
APIra bidaltzen dira. `rag_dokumentuak.txt`-ko zortzi fitxak dokumentu
fikziozko/propioak dira; 7.1eko igotze-probarako lau TXT fitxategiak
`rag_laginak/` karpetan prest daude. Zerbitzariak 4 fitxategi,
1 MB/fitxategi eta 200 chunk onartzen ditu.
Ez jarri Interneten autentifikaziorik gabe. `joblib.load`-ek kodea exekuta
dezake: kargatu soilik 1.5ek lokalki sortutako fitxategia.

## Apunteetako zuzenketa kontzeptualak

- R² ez da zehaztasun-portzentaje generikoa; balio negatiboa izan dezake.
- `ast.literal_eval`-ek ez du `15*8` kalkulatzen. 5.4k AST mugatua erabiltzen du.
- Pipelinearen aurreprozesamendua `fit` train multzoan bakarrik egin behar da.
- RAGaren iturri zerrenda retrieval-aren emaitza da; erantzuna eskuz egiaztatu.

Gemini ereduen egungo kodeak [Google-ren dokumentazioan](https://ai.google.dev/gemini-api/docs/models)
eta [embedding-ereduak](https://ai.google.dev/gemini-api/docs/embeddings)
kontsultatu dira; APIaren erabilgarritasuna eta kontuaren kuotak exekuzioan
egiaztatu behar dira.
