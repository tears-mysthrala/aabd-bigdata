"""4.4: Streamlit ML demo; ebaluazioa holdout bereizi batean."""
import pandas as pd
import streamlit as st
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from importlib import import_module

exercise = import_module("5073_3_Frameworkak_PDF_Ariketak")


@st.cache_resource
def trained_model():
    data = exercise.salmentak()
    X_train, X_test, y_train, y_test = train_test_split(
        data.drop(columns="salmenta_altua"), data["salmenta_altua"],
        test_size=0.25, random_state=42, stratify=data["salmenta_altua"])
    model = exercise.salmenta_pipeline().fit(X_train, y_train)
    return model, X_test, y_test


model, X_test, y_test = trained_model()
page = st.sidebar.radio("Orria", ["Iragarpena", "Ebaluazioa"])
st.title("Salmenta handia: datu sintetikoen demo")
if page == "Iragarpena":
    product = st.selectbox("Produktua", ["liburua", "jokoa", "kablea", "koadernoa"])
    region = st.selectbox("Eskualdea", ["iparra", "hegoa", "ekialdea"])
    price = st.number_input("Prezioa", min_value=0.0, value=20.0)
    stock = st.number_input("Stock", min_value=0, value=10)
    row = pd.DataFrame([{"produktua": product, "eskualdea": region,
                         "prezioa": price, "stock": stock}])
    if st.button("Iragarri"):
        st.write("Salmenta altua:", bool(model.predict(row)[0]))
else:
    pred = model.predict(X_test)
    a, b, c = st.columns(3)
    a.metric("Accuracy", f"{accuracy_score(y_test, pred):.2f}")
    b.metric("Precision", f"{precision_score(y_test, pred, zero_division=0):.2f}")
    c.metric("Recall", f"{recall_score(y_test, pred, zero_division=0):.2f}")
    st.pyplot(ConfusionMatrixDisplay.from_predictions(y_test, pred).figure_)
    st.caption("Holdout sintetikoa; ez du industria-datu errealetarako errendimendua frogatzen.")
