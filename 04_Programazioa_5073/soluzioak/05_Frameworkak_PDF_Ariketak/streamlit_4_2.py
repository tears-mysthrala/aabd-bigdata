"""4.2: streamlit run streamlit_4_2.py"""
import streamlit as st

st.title("Formularioa")
language = st.sidebar.selectbox("Hizkuntza", ["Euskara", "Castellano", "English"])
theme = st.sidebar.radio("Gaia", ["Argia", "Iluna"])
with st.form("profil"):
    name = st.text_input("Izena")
    age = st.number_input("Adina", min_value=0, max_value=120, step=1)
    interests = st.multiselect("Interesak", ["Python", "Datuak", "ML", "Kafka"])
    submitted = st.form_submit_button("Bidali")
if submitted:
    st.json({"izena": name, "adina": age, "interesak": interests,
             "hizkuntza": language, "gaia": theme})
if "clicks" not in st.session_state:
    st.session_state.clicks = 0
if st.button("Kontagailua handitu"):
    st.session_state.clicks += 1
st.write("Klikak:", st.session_state.clicks)
