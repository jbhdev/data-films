# pages/2_Recherche.py
import streamlit as st
from utils.css_loader import load_css

load_css("style.css")
load_css("sidebar_style.css")

st.title("Rechercher un Film")
search_query = st.text_input("Titre du film", "")
if search_query:
    st.write(f"Recherche pour : {search_query}")
    # Add your search logic here
    st.info("Résultats de recherche simulés pour " + search_query)