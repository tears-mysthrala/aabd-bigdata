"""Ebazpen didaktikoak: 5073_3_Programazioa.pdf (1.3 eta 4.3 ez daude PDFan).

Funtzioek emaitzak itzultzen dituzte; ez dute API dei, deskarga edo fitxategi
idazketarik egiten inportatze hutsagatik. Kanpoko zerbitzuen ariketak exekuzio
errealaren zain daude eta ezin dira ebidentzia gisa aurkeztu exekutatu arte.
"""

from __future__ import annotations

import ast
import operator
import os
from pathlib import Path
from time import perf_counter

ARIKETA_ZERRENDA = [
    "1.1", "1.2", "1.4", "1.5", "1.6", "2.1", "2.2", "2.3", "2.4",
    "3.1", "3.2", "3.3", "3.4", "3.5", "4.1", "4.2", "4.4",
    "5.1", "5.2", "5.3", "5.4", "6.1", "6.2", "6.3", "6.4", "7.1",
]
HERE = Path(__file__).resolve().parent
MODEL_PATH = HERE / "salmentak_pipeline.joblib"


def salmentak():
    """1.2/1.5erako datu txiki fikziozkoak; target-a salmenta altua da."""
    import pandas as pd

    rows = []
    for i in range(80):
        price = 8 + (i * 7) % 53
        stock = 2 + (i * 11) % 25
        rows.append({
            "produktua": ["liburua", "jokoa", "kablea", "koadernoa"][i % 4],
            "eskualdea": ["iparra", "hegoa", "ekialdea"][i % 3],
            "prezioa": None if i % 13 == 0 else float(price),
            "stock": None if i % 17 == 0 else float(stock),
            "salmenta_altua": int(stock >= 14 and price <= 39),
        })
    return pd.DataFrame(rows)


def salmenta_pipeline():
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    numeric = Pipeline([("impute", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler())])
    categorical = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore"))])
    pre = ColumnTransformer([("num", numeric, ["prezioa", "stock"]),
                             ("cat", categorical, ["produktua", "eskualdea"])])
    return Pipeline([("preprocess", pre), ("model", LogisticRegression(max_iter=1000))])


def ariketa_1_1():
    """Bost urrats: kargatu, banatu, sortu eredua, entrenatu, ebaluatu."""
    from sklearn.datasets import load_wine
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    X, y = load_wine(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    model.fit(X_train, y_train)
    return {"accuracy_test": accuracy_score(y_test, model.predict(X_test)),
            "n_train": len(y_train), "n_test": len(y_test)}


def ariketa_1_2():
    """ColumnTransformer: imputazio eta kodetzeak fit barruan, train bakarrik."""
    from sklearn.model_selection import train_test_split

    df = salmentak()
    X = df.drop(columns="salmenta_altua")
    y = df["salmenta_altua"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y)
    model = salmenta_pipeline()
    model.fit(X_train, y_train)
    return {"pipeline": model, "X_test": X_test, "y_test": y_test,
            "zergatik": "Mediana eta moda train multzoan bakarrik kalkulatzen dira."}


def ariketa_1_4():
    """Diabetes: R² testean, eredu guztiak banaketa berean."""
    from sklearn.datasets import load_diabetes
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LinearRegression, Ridge
    from sklearn.metrics import r2_score
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    X, y = load_diabetes(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    models = {"linear": LinearRegression(),
              "forest": RandomForestRegressor(n_estimators=100, random_state=42),
              **{f"ridge_{a}": make_pipeline(StandardScaler(), Ridge(alpha=a))
                 for a in (0.1, 1, 10)}}
    scores = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        scores[name] = r2_score(y_test, model.predict(X_test))
    return {"r2_test": scores,
            "r2_negatiboa": "Testeko y-ren batez bestekoa etengabe aurreikustea baino okerragoa."}


def ariketa_1_5(path: Path = MODEL_PATH):
    """Pipeline osoa serializatu eta berriz kargatu; joblib fitxategia fidagarria izan behar da."""
    import joblib
    from sklearn.model_selection import train_test_split

    df = salmentak()
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(columns="salmenta_altua"), df["salmenta_altua"],
        test_size=0.25, random_state=42, stratify=df["salmenta_altua"])
    model = salmenta_pipeline().fit(X_train, y_train)
    original = model.predict(X_test.iloc[:1]).tolist()
    joblib.dump(model, path)
    loaded = joblib.load(path)  # Sortu berri dugun fitxategia soilik; ez kargatu ezezagunik.
    restored = loaded.predict(X_test.iloc[:1]).tolist()
    return {"path": str(path), "jatorrizkoa": original, "birkargatua": restored,
            "berdina": original == restored, "test_accuracy": loaded.score(X_test, y_test)}


def ariketa_1_6():
    """Grid vs random: CV train multzoan; test amaieran behin bakarrik."""
    from scipy.stats import loguniform
    from sklearn.datasets import load_wine
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    X, y = load_wine(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y)
    base = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    searches = {
        "grid": GridSearchCV(base, {"logisticregression__C": [0.01, 0.1, 1, 10],
                                    "logisticregression__fit_intercept": [True, False],
                                    "logisticregression__class_weight": [None, "balanced"]}, cv=3,
                             error_score="raise"),
        "random": RandomizedSearchCV(base, {"logisticregression__C": loguniform(0.001, 100),
                                        "logisticregression__fit_intercept": [True, False],
                                        "logisticregression__class_weight": [None, "balanced"]},
                                     n_iter=20, cv=3, random_state=42, error_score="raise"),
    }
    result = {}
    for name, search in searches.items():
        start = perf_counter()
        search.fit(X_train, y_train)
        result[name] = {"segundos": perf_counter() - start, "cv": search.best_score_,
                        "test": search.score(X_test, y_test), "parametros": search.best_params_}
    return result


def ariketa_2_1():
    """Hubeko bilaketa bizia; emaitza-kopurua unean unekoa da."""
    from huggingface_hub import HfApi

    # huggingface_hub 1.x: ``language`` kendu da; ``filter`` tag bera erabiltzen du.
    models = list(HfApi().list_models(filter="eu"))
    selected = next((m for m in models if m.id == "ixa-ehu/berteus-base-cased"), None)
    return {"iragazkia": "filter=eu", "une_honetako_kopurua": len(models),
            "oharra": "Katalogoa aldatzen da; etiketa honek ez du Basque kalitatea frogatzen.",
            "hautatutako_eredua": {
                "id": "ixa-ehu/berteus-base-cased", "zeregin_mota": "feature-extraction",
                "url": "https://huggingface.co/ixa-ehu/berteus-base-cased",
                "iragazkian_dago": selected is not None,
                "zergatik": "Euskararako aurreentrenatutako BERT; testu-errepresentazioen demo akademikoa."},
            "azaldu": "Model card-eko lizentzia, entrenamendu-datuak eta mugak berrikusi; "
                      "oinarrizko eredua ez da sentimentu-sailkatzaile entrenatua.",
            "adibideak": [{"id": m.id, "url": f"https://huggingface.co/{m.id}"} for m in models[:5]]}


def ariketa_2_2():
    """Bederatzi iritzi fikziozko; score-a ereduaren konfiantza da, ez egia."""
    import pandas as pd
    from transformers import pipeline

    reviews = ["The room was clean and quiet.", "Breakfast was excellent.",
               "The staff ignored our request.", "The bed was uncomfortable.",
               "Great location and friendly reception.", "The lift was broken.",
               "It was okay, nothing special.", "The view was beautiful.",
               "I would not stay here again."]
    classifier = pipeline("sentiment-analysis",
                          model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
                          device=-1)  # Bederatzi esaldirako CPU nahikoa da.
    predictions = classifier(reviews)
    df = pd.DataFrame({"review": reviews, "label": [p["label"] for p in predictions],
                       "confidence": [p["score"] for p in predictions]})
    return {"taula": df, "kopuruak": df["label"].value_counts().to_dict(),
            "kontuz": "Konfiantza txikia edo iritzi anbiguoak eskuz aztertu."}


def ariketa_2_3():
    """Hiru euskarazko esaldi WordPiece tokenizadorearekin."""
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-multilingual-cased")
    sentences = ["Gaur eguraldi ederra dago.", "Ikasleek datuak aztertzen dituzte.",
                 "Adimen artifiziala arduraz erabili behar da."]
    return {"esaldiak": [{"esaldia": s, "tokenak": tokenizer.tokenize(s),
                          "azpitokenak": [t for t in tokenizer.tokenize(s) if t.startswith("##")]}
                         for s in sentences],
            "azalpena": "WordPiece-k hiztegi mugatuan ez dauden hitzak azpitokenetan "
                       "banatzen ditu; ## markak hitz barruko jarraipena adierazten du."}


def ariketa_2_4():
    """IMDb train multzoko lehen 100 iritzi positiboak eta lehen bostak Pandasen."""
    from datasets import load_dataset

    train = load_dataset("stanfordnlp/imdb", split="train")
    positives = train.filter(lambda row: row["label"] == 1).select(range(100))
    return positives.to_pandas().head(5)


def ariketa_3_1():
    """Exekutatu: uvicorn api_ariketak:app_3_1 --reload; ikus /docs."""
    from api_ariketak import app_3_1
    return app_3_1


def ariketa_3_2():
    """Liburuen CRUD: api_ariketak:app_3_2."""
    from api_ariketak import app_3_2
    return app_3_2


def ariketa_3_3():
    """Pydantic balidazioaren eredu eta adibide baliogabeak."""
    from api_ariketak import Erabiltzailea
    return {"eredua": Erabiltzailea,
            "baliogabeak": [{"izena": "Al", "adina": 25, "email": "a@example.org"},
                            {"izena": "Ane", "adina": 121, "email": "a@example.org"},
                            {"izena": "Ane", "adina": 25, "email": "oker"}]}


def ariketa_3_4():
    """ML API: uvicorn api_ariketak:app_3_4 --reload; lehenik 1.5 exekutatu."""
    from api_ariketak import app_3_4
    return app_3_4


def ariketa_3_5():
    """Bearer babestutako ML API: uvicorn api_ariketak:app_3_5 --reload."""
    from api_ariketak import app_3_5
    return app_3_5


def ariketa_4_1():
    """Exekutatu: streamlit run streamlit_4_1.py."""
    return HERE / "streamlit_4_1.py"


def ariketa_4_2():
    """Exekutatu: streamlit run streamlit_4_2.py."""
    return HERE / "streamlit_4_2.py"


def ariketa_4_4():
    """Exekutatu: streamlit run streamlit_4_4.py."""
    return HERE / "streamlit_4_4.py"


def ariketa_5_1():
    """Gako pertsonala eskuz AI Studio-n sortu; balioa ez da inoiz itzultzen."""
    from dotenv import load_dotenv

    load_dotenv(HERE / ".env")
    return {"google_api_key_prest": bool(os.getenv("GOOGLE_API_KEY")),
            "urratsak": "AI Studio -> API key; .env fitxategian GOOGLE_API_KEY; gitignore egiaztatu."}


def _gemini():
    from dotenv import load_dotenv
    from langchain_google_genai import ChatGoogleGenerativeAI

    load_dotenv(HERE / ".env")
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY falta da; ikus .env.example")
    return ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"), temperature=0)


def ariketa_5_2():
    """Hiru produktu batch bidez; temperature=0 errepikagarritasuna hobesteko."""
    from langchain_core.prompts import ChatPromptTemplate

    chain = ChatPromptTemplate.from_messages([
        ("system", "Idatzi gehienez 40 hitzeko produktu-deskribapen komertziala euskaraz. "
                   "Ez asmatu emandakoak ez diren ezaugarri teknikorik."),
        ("human", "Izena: {izena}; kategoria: {kategoria}; prezioa: {prezioa} EUR")]) | _gemini()
    products = [{"izena": "Koadernoa", "kategoria": "papergintza", "prezioa": 4.5},
                {"izena": "Kable USB", "kategoria": "osagarriak", "prezioa": 8.0},
                {"izena": "Termoa", "kategoria": "etxea", "prezioa": 16.0}]
    return [message.content for message in chain.batch(products)]


def ariketa_5_3():
    """Saio bakarreko txata, RunnableWithMessageHistory erabiliz."""
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.runnables.history import RunnableWithMessageHistory

    histories = {}
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Erantzun labur euskaraz; gogoratu elkarrizketa honetako datuak."),
        MessagesPlaceholder("history"), ("human", "{question}")])
    chain = RunnableWithMessageHistory(
        prompt | _gemini(), lambda session_id: histories.setdefault(session_id, InMemoryChatMessageHistory()),
        input_messages_key="question", history_messages_key="history")
    questions = ["Ane naiz eta Python ikasten ari naiz.",
                 "Zer ikasten ari naiz?", "Nola deitzen naiz?"]
    return [chain.invoke({"question": q}, config={"configurable": {"session_id": "demo"}}).content
            for q in questions]


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv}


def kalkulatu_seguru(expr: str) -> float:
    """Zenbakiak eta +,-,*,/ soilik; tamaina mugatua eta eval gabe."""
    if len(expr) > 80:
        raise ValueError("Adierazpen luzeegia")

    def walk(node, depth=0):
        if depth > 12:
            raise ValueError("Sakontasun handiegia")
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if abs(node.value) > 1e6:
                raise ValueError("Zenbaki handiegia")
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = walk(node.operand, depth + 1)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            value = _OPS[type(node.op)](walk(node.left, depth + 1), walk(node.right, depth + 1))
            if abs(value) > 1e9:
                raise ValueError("Emaitza handiegia")
            return value
        raise ValueError("Baimendu gabeko adierazpena")

    return float(walk(ast.parse(expr, mode="eval").body))


def ariketa_5_4():
    """Gemini-k bi tresna aukeratzen ditu; kalkulagailua AST mugatuarekin."""
    from langchain_core.tools import tool

    @tool
    def kalkulagailua(adierazpena: str) -> float:
        """Kalkulatu +,-,*,/ eragiketak, adibidez 15*8."""
        return kalkulatu_seguru(adierazpena)

    @tool
    def hitzak_kontatu(testua: str) -> int:
        """Kontatu testuko hitzak zuriuneen arabera."""
        return len(testua.split())

    tools = {t.name: t for t in (kalkulagailua, hitzak_kontatu)}
    question = ("Erabili kalkulagailua eta hitzak_kontatu tresnak biak. "
                "Zenbat da 15*8 eta zenbat hitz daude 'Kaixo mundu zabala' esaldian?")
    model = _gemini()
    response = model.bind_tools(list(tools.values())).invoke(question)
    calls = []
    from langchain_core.messages import ToolMessage
    messages = [("human", question), response]
    for call in response.tool_calls:
        if call["name"] in tools:
            result = tools[call["name"]].invoke(call["args"])
            calls.append({"tresna": call["name"], "emaitza": result})
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    if {item["tresna"] for item in calls} != set(tools):
        raise RuntimeError("Gemini-k ez ditu bi tresnak erabili; erantzuna ez da baliozkotu")
    answer = model.invoke(messages).content
    return {"galdera": question, "tresna_deiak": calls, "erantzuna": answer,
            "oharra": "Egiaztatu bi tresnak deitu direla; LLM-ak ez du beti hala egiten."}


def ariketa_6_1():
    """NotebookLM lanaren fitxa; benetako igoera eta aipuak eskuz egiaztatu."""
    return {"url": "https://notebooklm.google.com/",
            "dokumentua": str(HERE / "rag_dokumentuak.txt"),
            "galderak": ["Zein da Bronze geruzaren funtzioa?",
                         "Nola kalkulatzen da R² negatiboa?",
                         "Zein dokumentutan agertzen da Kafka partizioa?"],
            "egoera": "Giza kontua/GUI behar da; ez dago igoera edo aipuen frogarik."}


def ariketa_6_2():
    """500 karaktereko chunkak overlap 0/100/200rekin alderatu."""
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    text = (HERE / "rag_dokumentuak.txt").read_text(encoding="utf-8").replace("\n---\n", " ")
    return {overlap: {"kopurua": len(chunks := RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=overlap).split_text(text)),
                      "lehen_chunka": chunks[0]} for overlap in (0, 100, 200)}


def _documents():
    from langchain_core.documents import Document

    raw = (HERE / "rag_dokumentuak.txt").read_text(encoding="utf-8")
    return [Document(page_content=part.strip(), metadata={"source": f"fitxa-{i}"})
            for i, part in enumerate(raw.split("\n---\n"), start=1) if part.strip()]


def _index(documents):
    from langchain_community.vectorstores import FAISS
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    if not ariketa_5_1()["google_api_key_prest"]:
        raise RuntimeError("GOOGLE_API_KEY falta da")
    return FAISS.from_documents(documents, GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001"))


def ariketa_6_3():
    """Zortzi fitxa: embedding + FAISS; sinonimo bidezko bilaketa."""
    docs = _documents()
    if len(docs) != 8:
        raise ValueError("Zortzi dokumentu behar dira")
    found = _index(docs).similarity_search("Nola antolatzen dira mezuen zatiak?", k=3)
    return [{"source": d.metadata["source"], "text": d.page_content} for d in found]


def ariketa_6_4():
    """Lau fitxako RAG; kanpoko galderari Ez dakit eskatzen dio, egiaztatu behar da."""
    docs = _documents()[:4]
    index = _index(docs)
    questions = ["Zer egiten du Bronze geruzak?", "Zein da Jupiterreko tenperatura?"]
    answers = []
    for question in questions:
        found = index.similarity_search(question, k=2)
        context = "\n\n".join(f"[{d.metadata['source']}] {d.page_content}" for d in found)
        reply = _gemini().invoke(
            "Erantzun euskaraz emandako testuinguruarekin soilik. Erantzuna bertan ez badago, "
            "esan zehazki 'Ez dakit'. Ez asmatu.\nTestuingurua:\n" + context + "\nGaldera: " + question)
        answers.append({"galdera": question, "erantzuna": reply.content,
                        "iturriak": [d.metadata["source"] for d in found]})
    return answers


def ariketa_7_1():
    """FastAPI + Streamlit RAG proiektuaren bi sarrera-puntuak."""
    return {"backend": "uvicorn rag_api:app --host 127.0.0.1 --port 8000",
            "frontend": "streamlit run rag_streamlit.py",
            "dokumentuak": str(HERE / "rag_dokumentuak.txt"),
            "egoera": "Inplementatua; Gemini eta GUI exekuzio errealak egiaztatu gabe."}


def main():
    print(f"{len(ARIKETA_ZERRENDA)} ariketa: ikus README.md; kanpoko deiak ez dira automatikoki exekutatzen.")


if __name__ == "__main__":
    main()
