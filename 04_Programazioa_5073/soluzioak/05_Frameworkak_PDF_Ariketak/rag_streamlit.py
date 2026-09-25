"""7.1 RAG frontend: streamlit run rag_streamlit.py."""
import os

import requests
import streamlit as st

API_URL = os.getenv("RAG_API_URL", "http://127.0.0.1:8000")
st.title("Dokumentuei galdetu: demo lokala")
st.caption("TXT fitxategiak Gemini-ra bidaliko dira embeddings eta erantzuna sortzeko. "
           "Erabili soilik argitaratzeko baimena duten dokumentuak.")
files = st.file_uploader("3-4 TXT dokumentu (1 MB bakoitza)", type=["txt"],
                         accept_multiple_files=True)
if st.button("Kargatu dokumentuak"):
    if not 3 <= len(files or []) <= 4:
        st.error("Ariketa honetarako 3 edo 4 fitxategi behar dira.")
    elif any(f.size > 1_000_000 for f in files):
        st.error("Fitxategi bat 1 MB baino handiagoa da.")
    else:
        try:
            payload = [("fitxategiak", (f.name, f.getvalue(), "text/plain")) for f in files]
            response = requests.post(f"{API_URL}/dokumentuak/kargatu", files=payload, timeout=120)
            response.raise_for_status()
            st.success(f"{response.json()['zati_kopurua']} zati indexatuta")
        except requests.RequestException as exc:
            st.error(f"API errorea: {exc}")

question = st.text_area("Galdera")
k = st.number_input("Berreskuratutako zatiak", min_value=1, max_value=4, value=3)
if st.button("Galdetu") and question.strip():
    try:
        response = requests.post(f"{API_URL}/galdera", json={"galdera": question,
                                 "k_dokumentu": k}, timeout=120)
        response.raise_for_status()
        data = response.json()
        st.write(data["erantzuna"])
        st.info("Berreskuratutako iturriak: " + ", ".join(data["iturriak"]))
        st.caption(data["oharra"])
    except requests.RequestException as exc:
        st.error(f"API errorea: {exc}")
