"""4.1: streamlit run streamlit_4_1.py"""
import pandas as pd
import streamlit as st

employees = pd.DataFrame([
    {"izena": "Ane", "adina": 24, "soldata": 28000},
    {"izena": "Iker", "adina": 31, "soldata": 34000},
    {"izena": "Leire", "adina": 29, "soldata": 32000},
    {"izena": "Unai", "adina": 41, "soldata": 42000},
    {"izena": "Nerea", "adina": 35, "soldata": 38000},
])
st.title("Langileak: datu fikziozkoak")
st.dataframe(employees)
a, b, c = st.columns(3)
a.metric("Langileak", len(employees))
b.metric("Batez besteko adina", f"{employees['adina'].mean():.1f}")
c.metric("Soldata maximoa", f"{employees['soldata'].max():,.0f} €")
st.caption("delta aukerakoa da: aurreko neurri batekin alderatzeko balio du.")
